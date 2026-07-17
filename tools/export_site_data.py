#!/usr/bin/env python3
"""Emit the district table that index.html's calculator embeds.

The site is a single self-contained page with no external dependencies, so the data
has to be inline. This prints a compact JS literal to paste into index.html, keeping
the published numbers traceable to a script rather than hand-typed.

    python3 export_site_data.py > /tmp/districts.js

Fields per district: name, fall pupil count, taxable value, academy flag. Everything
the calculator shows is derived from those in the browser, using the same arithmetic
as net_position.py:

    levy      = sum(tv) * 0.0015
    per_pupil = levy / sum(fte)
    pays_d    = tv_d * 0.0015
    gets_d    = fte_d * per_pupil
    net_d     = gets_d - pays_d
"""
import millage_data as md


def short(name):
    """Trim MDE's formal district names to something a table can show."""
    for suffix in (" School District", " Community School District", " Community Schools",
                   " Consolidated Schools", " Public School District", " Public Schools",
                   " Schools", " City School District", " District Public Schools"):
        if name.endswith(suffix):
            name = name[:-len(suffix)]
            break
    fixes = {
        "Oak Park, School District of the City of": "Oak Park",
        "Hazel Park, School District of the City of": "Hazel Park",
        "Brandon School District in the Counties of Oakland and Lapeer": "Brandon",
        "Pontiac City": "Pontiac",
        "Dr. Joseph F. Pollack Academic Center of Excellence": "Pollack Academic Center",
        "AGBU Alex-Marie Manoogian School": "AGBU Manoogian",
        "Arts and Technology Academy of Pontiac": "Arts & Technology Pontiac",
        "Michigan Mathematics and Science Academy": "Michigan Math & Science",
    }
    return fixes.get(name, name)


def main():
    d = md.districts(25)
    rows = sorted(d.items(), key=lambda kv: (md.is_academy(kv[0]), -kv[1]["fte"]))

    print("// Oakland County school districts and public school academies, 2024-25.")
    print("// Source: MDE Bulletin 1014 export (25_Bulletin1014Export.xlsx).")
    print("//   f = fall pupil count (AVG FTE)  -- what a district RECEIVES on")
    print("//   v = taxable value (HSEV+NHSEV)  -- what a district PAYS on")
    print("//   a = public school academy (no taxing authority, so v is 0)")
    print("// Regenerate with: python3 tools/export_site_data.py")
    print("var DISTRICTS=[")
    for code, x in rows:
        acad = ",a:1" if md.is_academy(code) else ""
        print('  {c:"%s",n:"%s",f:%.2f,v:%d%s},'
              % (code, short(x["name"]), x["fte"], round(x["tv"]), acad))
    print("];")

    tot_fte = sum(x["fte"] for x in d.values())
    tot_tv = sum(x["tv"] for x in d.values())
    trad = md.districts(25, include_academies=False)
    print()
    print("// sanity, at 1.5 mills on 2024-25 values:")
    print("//   all %d entities   %s pupils, $%s taxable -> $%.2f/pupil"
          % (len(d), format(round(tot_fte), ","), format(round(tot_tv), ","),
             tot_tv * md.RATE / tot_fte))
    print("//   %d traditional    %s pupils            -> $%.2f/pupil"
          % (len(trad), format(round(sum(x["fte"] for x in trad.values())), ","),
             tot_tv * md.RATE / sum(x["fte"] for x in trad.values())))


if __name__ == "__main__":
    main()
