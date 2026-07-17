#!/usr/bin/env python3
"""Who pays and who receives under the Oakland enhancement millage.

The mechanism is set by statute. MCL 380.705(3), verbatim:

    "the intermediate school district shall calculate and pay to each of its
     constituent districts an amount of the revenue calculated by dividing the total
     amount of the revenue by the combined membership of the constituent districts
     within the intermediate school district ... and multiplying that quotient by the
     constituent district's membership"

Taxable value appears nowhere in that formula. Money is raised ad valorem (by property
wealth) and distributed per capita (by pupil count). So:

    a district is a NET DONOR  <=>  its share of the county's taxable value
                                    exceeds its share of the county's pupils

That share formulation is the honest one because it is vintage-independent: scaling
every district's taxable value by the same factor (e.g. 2024-25 values -> the 2026 levy
base) scales both what it pays and what it receives, and cannot flip anyone's sign.
Only DIFFERENTIAL growth between districts can.

Usage:
    python3 net_position.py                 # academies included (ballot language)
    python3 net_position.py --no-academies  # traditional only (the campaign's basis)
"""
import sys

import millage_data as md


def compute(year=25, include_academies=True):
    d = md.districts(year, include_academies=include_academies)
    tot_fte = sum(x["fte"] for x in d.values())
    tot_tv = sum(x["tv"] for x in d.values())
    levy = tot_tv * md.RATE
    per_pupil = levy / tot_fte

    rows = []
    for code, x in d.items():
        pays = x["tv"] * md.RATE
        gets = x["fte"] * per_pupil
        rows.append({
            "code": code, "name": x["name"], "fte": x["fte"], "tv": x["tv"],
            "tvpp": x["tv"] / x["fte"],
            "tv_share": x["tv"] / tot_tv, "fte_share": x["fte"] / tot_fte,
            "pays": pays, "gets": gets, "net": gets - pays,
        })
    rows.sort(key=lambda r: r["net"])
    return {
        "rows": rows, "tot_fte": tot_fte, "tot_tv": tot_tv,
        "levy": levy, "per_pupil": per_pupil,
        "breakeven_tvpp": per_pupil / md.RATE,
    }


def money(n):
    return ("-$" if n < 0 else "$") + format(abs(round(n)), ",")


def _residents(r, troy):
    """District-level and resident-level are different questions with different answers.

    MCL 380.705(3) pays on membership, and Troy's membership includes nonresident
    Section 105/105c choice students whose families pay property tax elsewhere. So
    "does Troy School District come out ahead" is not the same as "do Troy residents
    come out ahead".
    """
    soc_in, soc_out = md.TROY_SOC[2024]        # matches the 2024-25 bulletin vintage
    pp, pays = r["per_pupil"], troy["pays"]
    resident_in_troy = troy["fte"] - soc_in

    print()
    print("=== ADJUSTED FOR SECTION 105/105c SCHOOLS OF CHOICE (2024-25) ===")
    print("  Troy's %s membership includes %d NONRESIDENT choice students."
          % (format(round(troy["fte"]), ","), soc_in))
    print("  Their families pay property tax to their home district, not to Troy.")
    print()
    print("  Q1  does Troy School DISTRICT come out ahead?  (statutory, on membership)")
    print("        pays %s | receives %s | NET %s"
          % (money(pays), money(troy["gets"]), money(troy["net"])))
    print()
    print("  Q2  do Troy RESIDENTS come out ahead?  (money following resident children)")
    for label, kids in (
        ("resident kids in Troy schools only", resident_in_troy),
        ("+ residents at other districts (%d)" % soc_out, resident_in_troy + soc_out),
        ("+ residents at charters (%d)" % md.TROY_CHARTER_OUT_2025,
         resident_in_troy + soc_out + md.TROY_CHARTER_OUT_2025),
    ):
        print("        %-38s %8.0f kids -> %13s  net %s"
              % (label, kids, money(kids * pp), money(kids * pp - pays)))
    print()
    print("  -> Troy residents sit at BREAK-EVEN, within about +/-$100k either way.")
    print("     The district's %s surplus is essentially the %d imported choice"
          % (money(troy["net"]), soc_in))
    print("     students: %d x %s = %s of Troy's payout is earned educating"
          % (soc_in, money(pp), money(soc_in * pp)))
    print("     other districts' children.")
    print()
    print("     Trend: net choice has roughly halved, +1,006 (2016-17) -> +491 (2025-26),")
    print("     as inbound fell off its 2018-19 peak while outbound rose steadily. A model")
    print("     static on one year misses that.")


def main():
    incl = "--no-academies" not in sys.argv
    r = compute(25, include_academies=incl)

    print("=== OAKLAND ENHANCEMENT MILLAGE @ %.1f mills, 2024-25 taxable values ===" % md.MILLS)
    print("    academies: %s" % ("INCLUDED (ballot language)" if incl
                                 else "EXCLUDED (the campaign's basis)"))
    print("    entities %d | pupils %s | taxable value %s"
          % (len(r["rows"]), format(round(r["tot_fte"]), ","), money(r["tot_tv"])))
    print("    levy %s -> %s per pupil" % (money(r["levy"]), money(r["per_pupil"])))
    print("    DONOR LINE: %s of taxable value per pupil" % money(r["breakeven_tvpp"]))
    print()

    print("%-46s %8s %13s %13s %13s %13s" % ("district", "pupils", "TV/pupil", "pays", "receives", "NET"))
    for x in r["rows"]:
        mark = "  <== TROY" if x["code"] == md.TROY_DCODE else ""
        print("%-46s %8.0f %13s %13s %13s %13s%s"
              % (x["name"][:46], x["fte"], money(x["tvpp"]), money(x["pays"]),
                 money(x["gets"]), money(x["net"]), mark))

    donors = [x for x in r["rows"] if x["net"] < 0]
    print()
    print("  %d donors, %d receivers | net sums to %s (must be ~0)"
          % (len(donors), len(r["rows"]) - len(donors), money(sum(x["net"] for x in r["rows"]))))

    troy = next(x for x in r["rows"] if x["code"] == md.TROY_DCODE)
    print()
    print("=== TROY ===")
    print("  taxable value  %s  (rank %d of %d by TOTAL taxable value)"
          % (money(troy["tv"]),
             sorted(r["rows"], key=lambda x: -x["tv"]).index(troy) + 1, len(r["rows"])))
    print("  TV per pupil   %s  (rank %d of %d -- this is what decides donor status)"
          % (money(troy["tvpp"]),
             sorted(r["rows"], key=lambda x: -x["tvpp"]).index(troy) + 1, len(r["rows"])))
    print("  share of county taxable value  %.3f%%" % (100 * troy["tv_share"]))
    print("  share of county pupils         %.3f%%" % (100 * troy["fte_share"]))
    print("  -> %s by %s per year"
          % ("NET DONOR" if troy["net"] < 0 else "NET RECEIVER", money(abs(troy["net"]))))
    be_fte = troy["tv"] / r["breakeven_tvpp"]
    print("  Troy would flip to donor below %s pupils (today %s; cushion %s = %.1f%%)"
          % (format(round(be_fte), ","), format(round(troy["fte"]), ","),
             format(round(troy["fte"] - be_fte), ","),
             100 * (troy["fte"] - be_fte) / troy["fte"]))

    _residents(r, troy)

    print()
    print("=== CROSS-CHECK vs the certified ballot language ===")
    print("  ballot: this millage 'would raise an estimated %s if approved and first"
          % money(md.BALLOT_YIELD_2026))
    print("  levied in 2026'. Implied 2026 taxable base: %s" % money(md.BALLOT_YIELD_2026 / md.RATE))
    print("  modeled 2024-25 base: %s  (%.1f%% of it -- two years of growth)"
          % (money(r["tot_tv"]), 100 * r["tot_tv"] / (md.BALLOT_YIELD_2026 / md.RATE)))
    implied_pupils = md.BALLOT_YIELD_2026 / md.CAMPAIGN_PER_PUPIL
    trad = compute(25, include_academies=False)
    print()
    print("  The campaign advertises $%d per pupil. That implies a denominator of %s pupils:"
          % (md.CAMPAIGN_PER_PUPIL, format(round(implied_pupils), ",")))
    print("    traditional districts only  %s   (off by %+.1f%%)"
          % (format(round(trad["tot_fte"]), ","), 100 * (implied_pupils / trad["tot_fte"] - 1)))
    print("    all entities incl academies %s   (off by %+.1f%%)"
          % (format(round(compute(25)["tot_fte"]), ","),
             100 * (implied_pupils / compute(25)["tot_fte"] - 1)))
    print("  -> the $%d matches TRADITIONAL DISTRICTS ONLY, but the ballot says funds go"
          % md.CAMPAIGN_PER_PUPIL)
    print("     to districts 'and eligible public school academies' (MCL 380.705(7)).")
    print("     If academies are in, the real figure is $%.0f per pupil (%.1f%% lower)."
          % (md.BALLOT_YIELD_2026 / compute(25)["tot_fte"],
             100 * (1 - (md.BALLOT_YIELD_2026 / compute(25)["tot_fte"])
                    / (md.BALLOT_YIELD_2026 / trad["tot_fte"]))))


if __name__ == "__main__":
    main()
