# -*- coding: utf-8 -*-
"""Plain-formatting Word post for the site update. Desktop is OneDrive-redirected."""
import os
from datetime import datetime

from docx import Document
from docx.shared import Pt

OUT = os.path.expanduser(r"~\OneDrive\Desktop\Site Update - Calculator and OC Millage History.docx")

BODY = [
    "Two things are new on the site, because the numbers behind this millage have not been laid "
    "out anywhere in one place. The first is a calculator. Every Oakland County district and "
    "academy is in it, with the two figures that decide everything: the pupil count a district is "
    "paid on, and the taxable value it is taxed on. Both come from one state file, MDE Bulletin "
    "1014. Edit any enrollment and watch the money move. Set the rate anywhere up to 3 mills, the "
    "legal ceiling under Section 705. This proposal asks 1.5, half of what the law allows; when it "
    "expires in 2031 a renewal can be sought at any rate up to that cap. There is also a "
    "calculator for your own house: market value, SEV at half of market by law, then taxable "
    "value, which Proposal A caps at SEV and never above. Taxable value is not half of SEV. Get "
    "that wrong and you halve the tax you think you are voting on.",

    "Here is the whole picture, which nobody has stated plainly. You pay in by property value. You "
    "get paid back by pupil count. Taxable value appears nowhere in the payout formula. A district "
    "is a net donor only when its share of the tax base exceeds its share of the students. Troy is "
    "not a donor. Troy is 4th of 28 in total taxable value but 16th per pupil, because it also has "
    "the county's second-largest enrollment. The district nets about $346,000. But Troy's count "
    "includes 743 nonresident schools-of-choice students whose families pay property tax "
    "elsewhere, 458 from Macomb. Remove them and Troy residents are at break-even. The entire "
    "surplus is school of choice, and it has halved since 2016. One more: the campaign's $781 per "
    "pupil assumes the county's 24 academies and their 16,163 students get nothing. The ballot "
    "language includes them. If they are in, it is about $707.",

    "The second addition is history, and it should decide how you read the rest. On September 25, "
    "2001, Oakland Schools passed a special education millage in a special election under 8 "
    "percent of voters turned out for. It then built itself an administration building on Pontiac "
    "Lake Road. Its own forensic accountants found the use of special education money to help fund "
    "a new $29.5 million building. The mechanism is in the trial record, from a witness under "
    "oath: the facilities consultant testified he was asked to recount the building's square "
    "footage attributable to special education, counting corridors and storage, to make sure they "
    "were getting the maximum amount from special ed. That August the Free Press reported the "
    "travel and the gifts, and one sentence is why this matters: while school officials spent "
    "freely, some special-needs students were put on waiting lists for services. The "
    "superintendent was fired, later convicted of misconduct in office and conflict of interest, "
    "acquitted of embezzlement. That case was about self-dealing, not the building. The building "
    "produced no charge. It produced law: seven bills in 2004, Public Acts 412 through 419.",

    "One caveat, because it cuts against the easy version. Section 705 makes the ISD pay every "
    "dollar out to local districts within 10 days and keep none. Oakland Schools cannot build "
    "itself anything with this money. But it lands in 28 local general funds as unrestricted "
    "dollars, which moves the risk rather than removing it. Which is the argument: if special "
    "education is the reason to ask, commit it in writing and report it every year. It has been "
    "asked for here before, and it did not all arrive.",
]

doc = Document()
st = doc.styles["Normal"]
st.font.name = "Calibri"
st.font.size = Pt(11)

p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(12)
r = p.add_run("What's new on the site: a calculator, and Oakland County's own millage history")
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
doc.core_properties.title = "Site update: the calculator and OC millage history"

os.makedirs(os.path.dirname(OUT), exist_ok=True)
doc.save(OUT)

words = sum(len(t.split()) for t in BODY)
print("saved: %s" % OUT)
print("body word count: %d  (target ~500)" % words)
print("paragraphs: %d" % len(BODY))
