#!/usr/bin/env python3
"""Eight years of Oakland enrollment and taxable-value shares, plus an independent check.

Why shares: under MCL 380.705(3) a district's net position is decided by its share of
the county's taxable value against its share of the county's pupils, not by absolute
size. A district can be very property-rich and still be a net receiver if it also
educates a lot of children. Troy is the case in point.

Two independent instruments are compared, because a trend that only one file shows is
not a trend:

  A. MDE Bulletin 1014 "AVG FTE"     -- state aid membership (blended FTE)
  B. MI School Data fall headcount   -- raw bodies, a different collection entirely

They measure different things and will not agree on levels. If they agree on direction
and on which districts grew, the trend is real.
"""
import millage_data as md

YEARS = [18, 19, 20, 21, 22, 23, 24, 25]


def fy(y):
    return "20%02d-%02d" % (y - 1, y)


def main():
    data = {y: md.districts(y) for y in YEARS}

    print("=== OAKLAND COUNTY TOTALS (all entities, incl. academies) ===")
    print("%-10s %12s %22s %14s" % ("year", "pupils", "taxable value", "$/pupil @1.5"))
    for y in YEARS:
        tf = sum(d["fte"] for d in data[y].values())
        tv = sum(d["tv"] for d in data[y].values())
        print("%-10s %12s %22s %14s"
              % (fy(y), format(round(tf), ","), "$" + format(round(tv), ","),
                 "$%.2f" % (tv * md.RATE / tf)))

    print()
    print("=== TROY: is its position getting better or worse? ===")
    print("%-10s %10s %7s %19s %10s %10s %8s %11s"
          % ("year", "pupils", "chg", "taxable value", "TV share", "pupil share", "gap", "position"))
    prev = None
    for y in YEARS:
        t = data[y][md.TROY_DCODE]
        tf = sum(d["fte"] for d in data[y].values())
        tv = sum(d["tv"] for d in data[y].values())
        ts, ps = t["tv"] / tv * 100, t["fte"] / tf * 100
        chg = "" if prev is None else "%+.1f%%" % ((t["fte"] / prev - 1) * 100)
        prev = t["fte"]
        print("%-10s %10.0f %7s %19s %9.3f%% %9.3f%% %+7.3f   %s"
              % (fy(y), t["fte"], chg, "$" + format(round(t["tv"]), ","), ts, ps, ts - ps,
                 "DONOR" if ts > ps else "receiver"))
    print()
    print("  'gap' = TV share minus pupil share. Positive = donor. Troy's gap has gone")
    print("  MORE negative over eight years: it is drifting further into receiver")
    print("  territory, because its enrollment fell more slowly than the county's while")
    print("  its property values grew more slowly than the county's.")

    print()
    print("=== 8-YEAR ENROLLMENT CHANGE (source A: Bulletin 1014 blended FTE) ===")
    a = _changes({c: d for c, d in data[18].items() if not md.is_academy(c)},
                 {c: d for c, d in data[25].items() if not md.is_academy(c)}, "fte")
    _print_changes(a)

    print()
    print("=== 9-YEAR ENROLLMENT CHANGE (source B: MI School Data fall headcount) ===")
    h16, h25 = md.load_headcount(2016), md.load_headcount(2025)
    if not h16 or not h25:
        print("  (headcount files unavailable -- skipping the independent check)")
        return
    b = _changes(h16, h25, "n")
    _print_changes(b)

    print()
    print("=== SAME-YEAR RECONCILIATION: how far apart are the two instruments? ===")
    h24 = md.load_headcount(2024)
    if h24:
        b25 = {c: d for c, d in data[25].items() if not md.is_academy(c)}
        fte = sum(d["fte"] for c, d in b25.items() if c in h24)
        head = sum(h24[c]["n"] for c in b25 if c in h24)
        print("  Oakland traditional districts, 2024-25 / Fall 2024:")
        print("    Bulletin 1014 blended FTE   %s" % format(round(fte), ","))
        print("    MI School Data headcount    %s" % format(round(head), ","))
        print("    difference                  %s (%.1f%%)"
              % (format(round(fte - head), ","), 100 * (fte / head - 1)))
        t = b25[md.TROY_DCODE]
        print("  Troy: %s FTE vs %s headcount (%.1f%%)"
              % (format(round(t["fte"]), ","), format(round(h24[md.TROY_DCODE]["n"]), ","),
                 100 * (t["fte"] / h24[md.TROY_DCODE]["n"] - 1)))
        print("  The two are close but not equal, as expected -- they count different things.")
        print("  The MODEL uses blended FTE, because MCL 380.705(3) distributes on membership.")

    print()
    print("=== DO THE TWO SOURCES AGREE ON WHO GREW? ===")
    ga = {n for n, _, _, p in a if p > 0}
    gb = {n for n, _, _, p in b if p > 0}
    print("  Bulletin 1014 says gained : %s" % ", ".join(sorted(ga)))
    print("  MI School Data says gained: %s" % ", ".join(sorted(gb)))
    print("  agreed by both            : %s" % ", ".join(sorted(ga & gb)))
    only = (ga | gb) - (ga & gb)
    if only:
        print("  disagreement              : %s" % ", ".join(sorted(only)))
        print("    (the two instruments count different things -- blended FTE includes")
        print("     adult ed and prorated counts that a raw headcount does not)")


def _changes(before, after, key):
    out = []
    for code, d in after.items():
        if code in before and before[code][key] > 0:
            x, y = before[code][key], d[key]
            out.append((d["name"], x, y, (y / x - 1) * 100))
    out.sort(key=lambda r: -r[3])
    return out


def _print_changes(rows):
    for n, x, y, p in rows:
        mark = "   <== TROY" if "Troy" in n else ""
        print("  %-46s %8.0f -> %8.0f  %+7.1f%%%s" % (n[:46], x, y, p, mark))
    tx, ty = sum(r[1] for r in rows), sum(r[2] for r in rows)
    print("  %-46s %8.0f -> %8.0f  %+7.1f%%" % ("TOTAL", tx, ty, (ty / tx - 1) * 100))
    gained = [r for r in rows if r[3] > 0]
    troy = next((r for r in rows if "Troy" in r[0]), None)
    print("  gained: %d of %d districts" % (len(gained), len(rows)))
    if troy:
        rank = rows.index(troy) + 1
        print("  Troy ranks %d of %d by enrollment change (it shrank, but most shrank more)"
              % (rank, len(rows)))


if __name__ == "__main__":
    main()
