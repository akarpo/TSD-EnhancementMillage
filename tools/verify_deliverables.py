#!/usr/bin/env python3
"""Guard against the deliverables drifting away from the site again.

This exists because it already happened once. On 3 July 2026 the site's tone was
softened in 819d3da, which touched only index.html. The Word document and both share
images had last been rebuilt six hours earlier and were never regenerated, so for two
weeks the page said "this is not a knock on the District" while the file it linked as
"Download the analysis" still said "misleading at best" and "not leveling with voters".
funding-chart.png is also the og:image, so every social share carried the old framing.

Nothing structural prevents that recurring: the .docx is a build artifact committed
next to the source that generates it, and only discipline keeps them in step. So run
this after touching index.html, build_doc.py or make_images.py.

    python3 tools/verify_deliverables.py        # exits non-zero if they disagree

See docs/FINDINGS.md section 1.
"""
import html
import os
import re
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DOCX = os.path.join(ROOT, "assets", "TSD-Enhancement-Millage-Analysis.docx")
INDEX = os.path.join(ROOT, "index.html")

# Phrases 819d3da removed from the site. None may reappear in the published document.
SOFTENED_AWAY = [
    "misleading at best",
    "blank check",
    "grab bag",
    "not leveling with voters",
    "case against itself",
    "trust us",
    "wish list",
]

# Figures corrected in the July 2026 review. (stale, current) -- stale must not appear.
CORRECTED = [
    ("9.7 million", "9.6 million"),
    ("$55M", "$66,430,519"),
    ("$450,000", "$435,000"),
    ("$350 to $750", "$616.8 million"),
    ("never exceeded", "10.2%"),
    ("Facts v. Fallacy", "Durant"),
]


def docx_text(path):
    z = zipfile.ZipFile(path)
    xml = z.read("word/document.xml").decode("utf8", "replace")
    return html.unescape(re.sub(r"<[^>]+>", "", xml.replace("</w:p>", "\n")))


def main():
    if not os.path.exists(DOCX):
        print("FAIL: %s is missing" % DOCX)
        return 1

    txt = docx_text(DOCX)
    page = open(INDEX, encoding="utf-8").read()
    bad = []

    print("=== the published .docx must not carry what the site softened away ===")
    for phrase in SOFTENED_AWAY:
        hit = phrase in txt
        if hit:
            bad.append("docx still says %r" % phrase)
        print("   %-26s %s" % (repr(phrase), "STILL PRESENT" if hit else "gone"))

    print("\n=== corrected figures: stale must be gone, current must be present ===")
    for stale, current in CORRECTED:
        s_hit, c_hit = stale in txt, current in txt
        ok = (not s_hit) and c_hit
        if not ok:
            bad.append("docx: stale %r present=%s / current %r present=%s"
                       % (stale, s_hit, current, c_hit))
        print("   %-18s -> %-18s %s" % (repr(stale), repr(current), "ok" if ok else "WRONG"))

    print("\n=== the site itself must be clean too ===")
    for phrase in SOFTENED_AWAY:
        # the page may discuss these only inside a correction note
        for m in re.finditer(re.escape(phrase), page):
            window = page[max(0, m.start() - 400):m.start()]
            if "Correction, July 2026" not in window:
                bad.append("index.html says %r outside a correction note" % phrase)
    print("   %s" % ("clean" if not any("index.html" in b for b in bad) else "PROBLEM"))

    print()
    if bad:
        print("FAIL -- %d problem(s):" % len(bad))
        for b in bad:
            print("  - %s" % b)
        print("\nRegenerate: cd assets && python3 ../tools/make_images.py && "
              "python3 ../tools/build_doc.py")
        return 1
    print("PASS -- the document agrees with the site.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
