# -*- coding: utf-8 -*-
"""Plain-formatting Word post announcing the site update.

The running order is deliberate. The 2001-2003 special-education millage scandal leads,
because it is the fact that reframes everything after it. The URL lands in the first
paragraph, while the reader is still holding that fact. The transparency-and-reporting
ask follows directly from it, since that is what the history actually argues for. The
calculator and the donor math come after.

Note: this machine's Desktop is OneDrive-redirected. Writing to ~/Desktop produces a file
Explorer cannot see, so write to ~/OneDrive/Desktop.
"""
import os
from datetime import datetime

from docx import Document
from docx.shared import Pt

OUT = os.path.expanduser(r"~\OneDrive\Desktop\Site Update - Calculator and OC Millage History.docx")

TITLE = "Oakland County has voted a school tax for special education before. Here is where it went."

BODY = [
    "On September 25, 2001, Oakland Schools passed a special education and vocational education "
    "millage in a standalone special election that fewer than 8 percent of registered voters "
    "turned out for. The district then built itself an administration building on Pontiac Lake "
    "Road. Its own forensic accountants found the use of special education money to help fund a "
    "new $29.5 million building. The mechanism is in the trial record, from a witness under oath: "
    "the district's facilities consultant testified he was asked to recount how much of that "
    "building's square footage could be attributed to special education, counting corridors and "
    "storage, to make sure they were getting the maximum amount from special ed. That August the "
    "Free Press reported the travel and the gifts, and one sentence is why any of this matters: "
    "while school officials spent freely, some special-needs students were put on waiting lists "
    "for services. It is all laid out, sourced to the court record and the reporting, at "
    "tsd-enhancementmillage.karpowitsch.org.",

    "That story has an ending most people do not know, and it is the reason for the ask. It "
    "produced law. Seven bills passed in 2004 as Public Acts 412 through 419. One is titled uses "
    "for special education and vocational education bond proceeds and millages. Another created "
    "MCL 380.622a, subjecting intermediate districts to state-directed audits for the first time, "
    "and the list of things those audits must examine reads like an index of what had just "
    "happened, down to proper expenditure of special education tax levies. Nothing built in "
    "caught this. A forensic accountant and two newspapers caught it, and the Legislature had to "
    "write transparency into the statute afterward. So: if special education is the reason to tax "
    "homes for six years, commit every dollar to it in writing, publish the target, and report "
    "the actuals every year through 2031. Not because anyone is presumed to act in bad faith. "
    "Because last time, reporting is what worked, and it arrived years late.",

    "The site also has a calculator now, because these numbers have not been in one place "
    "anywhere. Every Oakland district and academy is in it, with the two figures that decide "
    "everything: the pupil count you are paid on, and the taxable value you are taxed on. Both "
    "from one state file, MDE Bulletin 1014. Edit any enrollment and watch the money move. Set "
    "the rate up to 3 mills, the ceiling under Section 705; this asks 1.5, and a renewal in 2031 "
    "can seek any rate up to that cap. Your own house too: market value, SEV at half of market by "
    "law, then taxable value, which Proposal A caps at SEV and never above. Taxable value is not "
    "half of SEV. Get that wrong and you halve the tax you think you are voting on.",

    "Here is the whole picture, which nobody has stated plainly. You pay in by property value. "
    "You get paid back by pupil count. Taxable value appears nowhere in the payout formula, so a "
    "district is a net donor only when its share of the tax base exceeds its share of the "
    "students. Troy is not a donor. It is 4th of 28 in total taxable value but 16th per pupil, "
    "because it also has the county's second-largest enrollment, and it nets about $346,000. But "
    "that count includes 743 nonresident schools-of-choice students whose families pay property "
    "tax elsewhere, 458 from Macomb. Remove them and Troy residents sit at break-even. The whole "
    "surplus is school of choice, and it has halved since 2016. Also: the $781 per pupil assumes "
    "the county's 24 academies and their 16,163 students get nothing. The ballot language "
    "includes them. If they are in, it is about $707.",

    "One caveat, because it cuts against the easy version. Section 705 makes the ISD pay every "
    "dollar out within 10 days and keep none, so Oakland Schools cannot build itself anything "
    "with this money and 2003 cannot repeat in that form. But it lands in 28 local general funds "
    "as unrestricted dollars, which moves the risk rather than removing it. It has been asked for "
    "here before, and it did not all arrive. Commit it in writing. Report it every year. "
    "tsd-enhancementmillage.karpowitsch.org",
]


def build():
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(11)

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(12)
    r = p.add_run(TITLE)
    r.bold = True
    r.font.size = Pt(13)

    for t in BODY:
        para = doc.add_paragraph(t)
        para.paragraph_format.space_after = Pt(10)

    now = datetime.now()
    doc.core_properties.created = now
    doc.core_properties.modified = now
    doc.core_properties.author = "Alex Karpowitsch"
    doc.core_properties.last_modified_by = "Alex Karpowitsch"
    doc.core_properties.title = "Oakland County has voted a school tax for special education before"

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    doc.save(OUT)
    return sum(len(t.split()) for t in BODY)


if __name__ == "__main__":
    n = build()
    print("saved: %s" % OUT)
    print("body word count: %d" % n)
    print("paragraphs: %d" % len(BODY))
    print("URL first appears in paragraph %d of %d" % (
        next(i + 1 for i, t in enumerate(BODY) if "karpowitsch.org" in t), len(BODY)))
