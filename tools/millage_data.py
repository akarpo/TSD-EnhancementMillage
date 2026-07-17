#!/usr/bin/env python3
"""Shared data layer: fetch and load the State of Michigan source files.

Every number in net_position.py and enrollment_trend.py comes from here, so this
module is the single place where a reader has to trust something. It downloads
only from state servers and caches to tools/cache/ (gitignored).

Sources
-------
MDE Bulletin 1014 export, one .xlsx per year, 2017-18 .. 2024-25:
    "Michigan Public School Districts Ranked By Selected Financial Data"
    Supplies BOTH sides of the enhancement-millage equation, per district:
      AVG FTE      fall pupil count (state aid membership)   -> what a district RECEIVES
      HSEV + NHSEV ad valorem taxable value                  -> what a district PAYS

The HSEV/NHSEV column names are legacy. Bulletin 1014's own glossary defines them
as TAXABLE value, not state equalized value:

    "Taxable Value Per State Aid Member (Homestead and Non-Homestead) - The figure
     represents a calculation made by dividing the ad valorem taxable value of real
     and personal property in the district (as reported on the DS4410) by the Fall
     Pupil Count."

That distinction matters: an enhancement millage is levied on taxable value, and in
Michigan SEV = 50% of market value while TV <= SEV (capped by Proposal A until a
transfer of ownership uncaps it). TV is not "half of SEV" -- it is capped AT SEV.

Access note: michigan.gov and mischooldata.org return HTTP 403 to default fetchers.
mdoe.state.mi.us (SAMSPublic) does not. A browser User-Agent works for all three.
"""
import os
import sys
import urllib.request

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache")

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/125.0 Safari/537.36")

OAKLAND_CC = "63"          # county code; Oakland Schools ISD entity code is 63000
TROY_DCODE = "63150"

# Bulletin 1014 exports. MDE renamed the file three times; these are the real URLs.
BULLETIN_1014 = {
    18: "https://mdoe.state.mi.us/SAMSPublic/Reports/others/Bulletin1014Export18.xlsx",
    19: "https://mdoe.state.mi.us/SAMSPublic/Reports/others/Bulletin1014Export19.xlsx",
    20: "https://mdoe.state.mi.us/SAMSPublic/Reports/others/Bulletin1014Export20.xlsx",
    21: "https://mdoe.state.mi.us/SAMSPublic/Reports/others/21_Bulletin1014%20Export.xlsx",
    22: "https://mdoe.state.mi.us/SAMSPublic/Reports/others/22_Bulletin1014%20Export.xlsx",
    23: "https://mdoe.state.mi.us/SAMSPublic/Reports/others/23_Bulletin1014%20Export.xlsx",
    24: "https://mdoe.state.mi.us/SAMSPublic/Reports/others/24_Bulletin1014Export.xlsx",
    25: "https://mdoe.state.mi.us/SAMSPublic/Reports/others/25_Bulletin1014Export.xlsx",
}

# MI School Data fall headcount -- an INDEPENDENT instrument (raw bodies, not blended
# FTE), used by enrollment_trend.py to check the Bulletin 1014 trend against a second
# source. Sheet "Fall Dist K-12 Total Data", header on row 5, column tot_all.
_CEPI = "https://www.michigan.gov/cepi/-/media/Project/Websites/cepi/MISchoolData"
HEADCOUNT = {
    2016: _CEPI + "/2016-17/1617_Fall_headcount.xlsx",
    2024: _CEPI + "/2024-25/Spring_2025_Headcount.xlsx",   # holds the Fall 2024 count
    2025: _CEPI + "/2025-26/Spring_2026_Headcount.xlsx",   # holds the Fall 2025 count
}

# Certified ballot language, Oakland County Regional Enhancement Millage, Aug 4 2026:
# "increased by 1.5 mills ($1.50 on each $1,000 of taxable valuation) for a period of
#  six (6) years, 2026 to 2031 ... would raise an estimated $125,756,247 if approved
#  and first levied in 2026."
MILLS = 1.5
RATE = MILLS / 1000.0
BALLOT_YIELD_2026 = 125_756_247
CAMPAIGN_PER_PUPIL = 781      # oaklandenhancementmillage.com

# Section 105 / 105c schools of choice, Troy School District.
# Source: MI School Data, "Schools of Choice and Other Non-Resident Enrollments"
# (CEPI/MDE; available 2009-10 to current, no login). That report is a residency x
# enrollment cross-tab, queried per district -- there is no bulk download, so these are
# transcribed rather than fetched. 2024-25 is used to match Bulletin 1014's vintage.
#
# Why it matters: MCL 380.705(3) pays on MEMBERSHIP, so a district is paid for the
# nonresident choice students it enrolls, while the tax is levied on property inside its
# boundary. That breaks the link between who pays and who is counted.
#
# MCL 388.1705(1) and the 2025-26 Pupil Accounting Manual Sec 5-I confirm the enrolling
# district counts the pupil and the resident district does not.
TROY_SOC = {
    # year: (inbound nonresidents enrolled in Troy, outbound Troy residents at other LEAs)
    2016: (1094, 88),
    2017: (1111, 99),
    2018: (1124, 124),     # inbound peak
    2019: (1085, 140),
    2020: (1051, 160),
    2021: (1029, 176),
    2022: (927, 166),
    2023: (846, 187),
    2024: (743, 195),      # matches the 2024-25 Bulletin 1014 vintage
    2025: (707, 216),      # 249 Sec 105 + 458 Sec 105c
}
TROY_CHARTER_OUT_2025 = 141   # Troy residents enrolled in charters (tracked separately)


def _fetch(url, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return dest
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:
        f.write(r.read())
    return dest


def fetch_all(verbose=True):
    """Download every source file into tools/cache/. Idempotent."""
    for year, url in sorted(BULLETIN_1014.items()):
        p = _fetch(url, os.path.join(CACHE, "b1014_%d.xlsx" % year))
        if verbose:
            print("  bulletin 1014  20%02d-%02d  %8d bytes" % (year - 1, year, os.path.getsize(p)))
    for year, url in sorted(HEADCOUNT.items()):
        try:
            p = _fetch(url, os.path.join(CACHE, "headcount_%d.xlsx" % year))
            if verbose:
                print("  fall headcount %d        %8d bytes" % (year, os.path.getsize(p)))
        except Exception as e:                       # noqa: BLE001 - optional cross-check
            print("  fall headcount %d        SKIPPED (%s)" % (year, e), file=sys.stderr)


def _sheet_rows(path, sheet=None):
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb[sheet] if sheet else wb[wb.sheetnames[0]]
    return list(ws.iter_rows(values_only=True))


def _header_index(rows, key):
    for i, r in enumerate(rows[:12]):
        if any(str(c).strip().lower() == key for c in r if c is not None):
            return i
    raise ValueError("no header row containing %r" % key)


def load_bulletin(year):
    """Return {dcode: {name, fte, tv, hs, nhs}} for Oakland entities in a given year.

    Academies are included and carry tv == 0: they have no taxing authority, so they
    receive a per-pupil share but never pay. Filter with is_academy() as needed.
    """
    path = os.path.join(CACHE, "b1014_%d.xlsx" % year)
    if not os.path.exists(path):
        _fetch(BULLETIN_1014[year], path)
    rows = _sheet_rows(path)
    hi = _header_index(rows, "dcode")
    H = {str(h).strip(): j for j, h in enumerate(rows[hi]) if h}
    out = {}
    for r in rows[hi + 1:]:
        if not r[H["DCode"]] or str(r[H["CC"]]).strip() != OAKLAND_CC:
            continue
        fte = r[H["AVG FTE"]] or 0
        if not fte:
            continue
        hs = float(r[H["HSEV"]] or 0)
        nhs = float(r[H["NHSEV"]] or 0)
        out[str(r[H["DCode"]]).strip()] = {
            "name": str(r[H["District Name"]]).strip(),
            "fte": float(fte),
            "hs": hs,
            "nhs": nhs,
            "tv": hs + nhs,
        }
    return out


def load_headcount(year):
    """Independent check: MI School Data fall headcount, Oakland traditional districts.

    Returns {dcode: {name, n}} or None if the file could not be fetched. Excludes the
    ISD itself (63000) and academies (639xx) so it lines up with the 28 named districts
    in the ballot language.
    """
    path = os.path.join(CACHE, "headcount_%d.xlsx" % year)
    if not os.path.exists(path):
        try:
            _fetch(HEADCOUNT[year], path)
        except Exception:                            # noqa: BLE001
            return None
    try:
        rows = _sheet_rows(path, "Fall Dist K-12 Total Data")
    except Exception:                                # noqa: BLE001
        return None
    hi = _header_index(rows, "district code")
    H = {str(h).strip().lower(): j for j, h in enumerate(rows[hi]) if h}
    out = {}
    for r in rows[hi + 1:]:
        code = r[H["district code"]]
        if code is None:
            continue
        code = str(code).strip()
        if not code.startswith(OAKLAND_CC) or len(code) != 5:
            continue
        if code == "63000" or is_academy(code):
            continue
        try:
            n = float(r[H["tot_all"]])
        except (TypeError, ValueError, KeyError):
            continue
        out[code] = {"name": str(r[H["district name"]]).strip(), "n": n}
    return out


def is_academy(dcode):
    """Public school academies use 639xx codes and hold no taxable value."""
    return str(dcode).startswith("639")


def districts(year=25, include_academies=True):
    d = load_bulletin(year)
    if include_academies:
        return d
    return {k: v for k, v in d.items() if not is_academy(k)}


if __name__ == "__main__":
    print("fetching state source files into %s ..." % CACHE)
    fetch_all()
    d = districts(25)
    trad = districts(25, include_academies=False)
    print("\nOakland 2024-25: %d entities (%d traditional districts, %d academies)"
          % (len(d), len(trad), len(d) - len(trad)))
    print("  total pupils         %s" % format(round(sum(x["fte"] for x in d.values())), ","))
    print("  total taxable value  $%s" % format(round(sum(x["tv"] for x in d.values())), ","))
