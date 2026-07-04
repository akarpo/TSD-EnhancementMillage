#!/usr/bin/env python3
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

NAVY=RGBColor(0x1F,0x2A,0x44); RED=RGBColor(0xB2,0x22,0x22)
GRAY=RGBColor(0x55,0x55,0x55); WHITE=RGBColor(0xFF,0xFF,0xFF); GREEN=RGBColor(0x1B,0x5E,0x20)
SCR="."

def shade(cell, fill):
    tcPr=cell._tc.get_or_add_tcPr(); shd=OxmlElement('w:shd')
    shd.set(qn('w:val'),'clear'); shd.set(qn('w:color'),'auto'); shd.set(qn('w:fill'),fill); tcPr.append(shd)

def sf(run,size=None,bold=None,italic=None,color=None,name='Calibri'):
    run.font.name=name
    if size:run.font.size=Pt(size)
    if bold is not None:run.font.bold=bold
    if italic is not None:run.font.italic=italic
    if color is not None:run.font.color.rgb=color

def nd(s):
    assert '—' not in s and '–' not in s, "long dash found: %r"%s
    return s

def para(doc,text='',size=11,bold=False,italic=False,color=None,align=None,after=6,before=0):
    p=doc.add_paragraph();p.paragraph_format.space_after=Pt(after);p.paragraph_format.space_before=Pt(before)
    if align:p.alignment=align
    if text: sf(p.add_run(nd(text)),size,bold,italic,color)
    return p

def heading(doc,text,size=13.5,color=NAVY,before=12):
    p=doc.add_paragraph();p.paragraph_format.space_before=Pt(before);p.paragraph_format.space_after=Pt(3)
    sf(p.add_run(nd(text)),size,True,False,color);return p

def bullet(doc,text,size=11,color=None):
    p=doc.add_paragraph(style='List Bullet');p.paragraph_format.space_after=Pt(2)
    sf(p.add_run(nd(text)),size,False,False,color);return p

doc=Document()
st=doc.styles['Normal'];st.font.name='Calibri';st.font.size=Pt(11)
s=doc.sections[0]
s.left_margin=Inches(0.9);s.right_margin=Inches(0.9);s.top_margin=Inches(0.8);s.bottom_margin=Inches(0.8)

# TITLE
p=doc.add_paragraph();p.paragraph_format.space_after=Pt(2)
sf(p.add_run("Fund the Need They Named."),22,True,False,NAVY)
p=doc.add_paragraph();p.paragraph_format.space_after=Pt(2)
sf(p.add_run(nd("Troy’s own millage email says special education is the problem, then proposes to spend the money on a "
   "grab bag of everything else. If it passes, dedicate it to special education, with measurable results.")),
   12,False,True,GRAY)
p=doc.add_paragraph();p.paragraph_format.space_after=Pt(10)
sf(p.add_run("Oakland County Regional Enhancement Millage · on the ballot Tuesday, August 4, 2026 · prepared July 2026"),9.5,False,False,GRAY)

# THESIS
para(doc,"On June 30, 2026, the Troy School District emailed residents a newsletter urging a “yes” vote on the "
 "1.5-mill county enhancement millage. Read it closely and it makes the case against itself. In the same email, the "
 "District (1) names the real funding problem, special education; then (2) proposes to spend the money on six broad, "
 "uncommitted budget categories; and (3) leans on a “44% of Michigan students already have this” pitch that implies Oakland is "
 "behind when the state’s own data show it is well ahead. That is misleading at best. Asking voters for six years of "
 "“unrestricted” general-fund dollars with no committed plan is, at worst, a blank check.")

# JUXTAPOSITION TABLE
heading(doc,"The District’s own email: the problem it names vs. the plan it offers",before=6)
t=doc.add_table(rows=2,cols=2);t.style='Table Grid';t.alignment=WD_TABLE_ALIGNMENT.CENTER
for j,txt in enumerate(("THE PROBLEM THEY NAME (page 3)","THE PLAN THEY OFFER (page 5)")):
    c=t.rows[0].cells[j];shade(c,'1F2A44');c.width=Inches(3.4)
    c.paragraphs[0].alignment=WD_ALIGN_PARAGRAPH.CENTER;sf(c.paragraphs[0].add_run(txt),10,True,False,WHITE)
c=t.rows[1].cells[0];c.width=Inches(3.4)
sf(c.paragraphs[0].add_run("“Special education funding is underfunded by approximately 40%. This means that districts "
 "must use dollars from their general fund to support students with special needs to close this gap in funding.”"),
 10.5,False,True,NAVY)
c=t.rows[1].cells[1];c.width=Inches(3.4)
sf(c.paragraphs[0].add_run("Troy’s six stated uses: broad budget categories offered as “unrestricted” funds, with no target or reporting attached:"),10.5,False,False,GRAY)
for tile in ["Staff Retention & Raises","Enhance Student Wellness Supports","Stabilize the General Fund Budget",
             "Enhance & Maintain Safety Measures","Maintain Staff to Student Ratios","Maintain & Strengthen District Programming"]:
    pp=c.add_paragraph();pp.paragraph_format.space_after=Pt(0);sf(pp.add_run("•  "+tile),10,False,False,RED)
para(doc,"Nowhere in those six buckets is the one thing the District just told you is the problem: special education.",
 10.5,True,False,NAVY,after=8)

# SECTION 1
heading(doc,"1.  They named the real need, special education, and it is real")
para(doc,"The District is right about the gap. When Congress passed the Individuals with Disabilities Education Act (IDEA), "
 "it promised to cover 40% of the extra cost of educating students with disabilities. Federal funding has never exceeded "
 "about 15%. Michigan reimburses only about 28.6% of special-education costs, among the lowest shares in the country. "
 "The remainder falls on local general funds: the very same dollars that pay for regular classroom teachers, textbooks, "
 "and buses. Statewide, closing this shortfall is estimated at $350 to $750 million a year. The MEA, the Autism Alliance "
 "of Michigan, and local school boards have identified this gap, not a general shortage, as the structural problem for years.")
para(doc,"This is a concrete, countable need. You can measure it: dollars of general-fund money a district is forced to divert "
 "to special education, and how much of that a new revenue source relieves. It is exactly the kind of outcome a millage should "
 "be tied to.")

# SECTION 2
heading(doc,"2.  Then they proposed a grab bag, with nothing committed")
para(doc,"Having named the problem, the email does not commit a single dollar to solving it. Instead it advertises that the "
 "money is “unrestricted”: “one district could use the funds to increase pay for their teachers, another could buy school "
 "buses, yet another could hire a school resource officer… a variety of uses to support their budgetary goals.” Troy’s own "
 "six “uses” (above) are broad budget categories, not commitments. Some a district could genuinely measure (a fund balance, "
 "a staffing ratio), which is exactly why it should set targets and report them. It has not: no target, no baseline, and no "
 "reporting for any of the six, and because the money is “unrestricted,” nothing binds it to any of them. No way for a taxpayer to check, "
 "in 2031, whether the $57 million Troy will have collected actually did what was promised. “Local flexibility” is being "
 "used to mean “trust us.” For a six-year tax on your home, voters deserve better than a wish list.")

# SECTION 3
heading(doc,"3.  And the pitch implies you’re behind when Oakland is already ahead")
para(doc,"The email’s headline argument is that “approximately 44% of students in Michigan” already receive enhancement "
 "funding, the classic “everyone else has it” nudge. But the State of Michigan’s own financial data show Oakland is not "
 "trailing anyone. In local funding it out-raises Macomb, a neighbor already on that “44%” list, by 27% per pupil.",after=4)
rows=[("Local school funding per pupil, 2024-25","Oakland today","Oakland if it passes","Macomb*"),
      ("Member districts’ own local revenue","$7,402","$7,402","$5,273"),
      ("County ISD’s own levies (incl. any enhancement)","$1,781","$2,562","$1,973"),
      ("TOTAL LOCAL, PER PUPIL","$9,184","$9,965","$7,247")]
tt=doc.add_table(rows=len(rows),cols=4);tt.style='Table Grid';tt.alignment=WD_TABLE_ALIGNMENT.CENTER
w=[Inches(3.0),Inches(1.2),Inches(1.45),Inches(1.15)]
for i,r in enumerate(rows):
    for j,v in enumerate(r):
        c=tt.rows[i].cells[j];c.width=w[j];pp=c.paragraphs[0]
        pp.alignment=WD_ALIGN_PARAGRAPH.LEFT if j==0 else WD_ALIGN_PARAGRAPH.CENTER;run=pp.add_run(v)
        if i==0: shade(c,'1F2A44');sf(run,9.5,True,False,WHITE)
        elif r[0].startswith("TOTAL"): shade(c,'FBE9E7');sf(run,11,True,False,NAVY if j==0 else RED)
        else: sf(run,10.5,False,False,RED if j==2 else None)
para(doc,"*Macomb already levies a 1.82-mill enhancement (since 2020), and Oakland, with no enhancement at all, still raises 27% "
 "more per pupil in local funding. Pass the 1.5 mills and that local-funding gap widens to nearly 38% ($9,965 vs. $7,247 per "
 "pupil). Because Oakland’s property is worth far more per pupil, its lower 1.5-mill rate is estimated to raise more per student "
 "(about $781) than Macomb’s higher 1.82-mill rate does. A note on precision: counting state and federal aid, total per-pupil "
 "funding is much closer (Oakland about $17,100 in operating dollars, Macomb about $16,100); the gap is in local dollars, which "
 "is what this millage adds to.",8.5,False,False,GRAY,after=8)

# SECTION 4
heading(doc,"What an honest proposal would do: fund what they named",color=GREEN)
para(doc,"This is not an argument that schools can’t use money. It’s an argument for spending it where the District itself "
 "says the need is, with results voters can verify:")
bullet(doc,"Dedicate 100% of the enhancement to special education. Because the funds are legally unrestricted, each district’s "
 "board should adopt a public policy committing every dollar to closing its special-education shortfall: the general-fund "
 "money it is currently forced to divert.")
bullet(doc,"Publish measurable targets. State the dollars redirected to special education this year, the general-fund dollars "
 "thereby freed for classrooms, and caseload/service commitments, then report actuals every year through 2031.")
bullet(doc,"Tie the ask to the need. If special education is the reason to tax homes for six years, then say so on the record "
 "and spend it there, not on an unrestricted “variety of uses.”")
para(doc,"For Troy alone, the millage is roughly $9.6 million a year, about $57 million over six years. Aimed squarely at "
 "special education, that is enough to make a real, measurable dent in the gap the District describes. Spread across a grab "
 "bag, it will disappear into general operations with nothing to point to.",after=8)

# BOTTOM LINE
heading(doc,"The bottom line",color=RED)
para(doc,"To its credit, the District’s email does disclose the cost: about $150 a year on a $200,000 home, $300 on a $400,000 "
 "home, and about $338 on a home at Troy’s 2025 median sale price of roughly $450,000 (about $2,025 over six years), levied on "
 "your primary residence. So this isn’t about hiding the price. It’s about the promise. A district that names "
 "special education as the problem, then asks for six years of unrestricted dollars it won’t commit to that problem, while "
 "implying you’re behind when you’re ahead, is not leveling with voters. If the need is special education, fund special "
 "education, and prove it. Anything else is a grab bag.")

# SOURCES
heading(doc,"Sources & method",size=11,color=GRAY)
para(doc,"• District communication: Troy School District, “Oakland County Enhancement Millage Proposal,” email newsletter, "
 "June 30, 2026 (quotations and the six spending tiles are from that email).\n"
 "• Local revenue & membership: MI Dept. of Education Bulletin 1014/1011 (2024-25) and the state Financial Information "
 "Database (Revenue Data, 2024-25); Oakland member-district totals reconcile exactly to the MDE Bulletin 1011 export. "
 "Macomb ISD enhancement (1.8198 mills, ~$55M+/yr, 2020-2029) per Macomb ISD. Population: U.S. Census 2024.\n"
 "• Special-education funding: IDEA’s 40% commitment vs. actual federal funding (never above ~15%) and Michigan’s ~28.6% "
 "reimbursement, per MEA (“Facts v. Fallacy: School Funding”), Michigan House Fiscal Agency testimony, Michigan League for "
 "Public Policy, and the Autism Alliance of Michigan; statewide shortfall estimate $350 to $750M.\n"
 "• “Local funding” = own local sources (property tax + local), governmental funds, excluding state/federal aid and "
 "ISD-to-district pass-through. Per-pupil uses fall membership; the enhancement is shown at the campaign’s own $781/pupil.",
 8.5,False,False,GRAY)

# ---------------- FACEBOOK POST KIT ----------------
doc.add_page_break()
sf(doc.add_paragraph().add_run("READY-TO-POST FACEBOOK KIT"),14,True,False,NAVY)
para(doc,"Facebook posts are plain text (no tables), so the numbers go in as images. To post: paste the caption below, then "
 "click the photo icon and attach BOTH images from your Downloads folder in this order: (1) fb_problem_vs_plan.png, then "
 "(2) fb_table.png. The caption points to them as the “first image” and “the chart.” Both images are shown at the bottom of "
 "this page so you can confirm which is which.",9.5,False,False,GRAY,after=8)
fb=(
"🚨 Read the Troy School District’s own email about the Aug. 4 enhancement millage. It makes the case against itself. "
"(See the two graphics with this post.)\n\n"
"On page 3, the District names the real problem, in its own words: “Special education funding is underfunded by "
"approximately 40%… districts must use dollars from their general fund… to close this gap.” Then on page 5, look at how "
"they say they’d spend your money (first image, their own email side by side):\n"
"• Staff Retention & Raises\n"
"• Enhance Student Wellness Supports\n"
"• Stabilize the General Fund Budget\n"
"• Enhance & Maintain Safety Measures\n"
"• Maintain Staff to Student Ratios\n"
"• Maintain & Strengthen District Programming\n\n"
"Six broad budget categories. The District sets no target and no reporting for any of them, and its own email calls the money "
"“unrestricted”… “a variety of uses.” Not one dollar is committed to the special-education gap it just named. That is not a "
"plan. It is a grab bag.\n\n"
"And the “44% of Michigan already has this” pitch implies we’re behind. We’re not (see the chart, second image). Oakland "
"already raises more LOCAL funding per student ($9,184) than Macomb ($7,247), a county that ALREADY levies an enhancement. We "
"lead in local dollars without one, and passing this only widens that local gap.\n\n"
"📖 FUNDING vs. SPENDING, in plain English:\n"
"• “Local funding” is the slice of school money that comes from YOUR local property taxes. That is the slice this millage "
"raises.\n"
"• “Spending” is the whole pie a school spends per student, which also includes state and federal dollars.\n"
"• So the numbers above ($9,184 vs. $7,247) are LOCAL money, not total spending. Count state aid and the total per student is "
"close: about $17,100 per pupil in Oakland vs. about $16,100 in Macomb. Michigan sends more state aid to places that raise "
"less locally, which evens the total out.\n"
"• Bottom line: Oakland already taxes itself far more LOCALLY for schools (27% more per student) than a county that already "
"has an enhancement. This proposal piles on even more local money.\n\n"
"💡 THE BIGGER PICTURE: Oakland already pays MORE than its share into Michigan's schools. Under Proposal A, the 6-mill State "
"Education Tax (plus state sales and income taxes) is pooled statewide and handed back per pupil. Oakland's districts hold "
"about 16% of the state's school property tax base but educate only about 12% of its students, so Oakland taxpayers already "
"subsidize schools elsewhere by an estimated $85 million or more a year through the State Education Tax alone. We are not "
"behind. We already carry more than our share, and this proposal asks us to tax ourselves even more locally.\n\n"
"THE ASK: If special education is the need, fund THAT. Dedicate 100% of the enhancement to special education, and report "
"every year how much general-fund money it frees up. Measurable. Accountable. Honest.\n\n"
"If it passes, spend it where they said the need is. Not on a grab bag. 🗳️  #Aug4  #OaklandCounty"
)
nd(fb)
tb=doc.add_table(rows=1,cols=1);tb.style='Table Grid';cell=tb.rows[0].cells[0];shade(cell,'F7F7F5')
sf(cell.paragraphs[0].add_run(fb),10.5,False,False,RGBColor(0x11,0x11,0x11))

p=doc.add_paragraph();p.paragraph_format.space_before=Pt(12)
sf(p.add_run(nd("Attach #1 (the “first image”):  fb_problem_vs_plan.png")),10.5,True,False,NAVY)
doc.add_picture(f"{SCR}/fb_problem_vs_plan.png",width=Inches(6.4));doc.paragraphs[-1].alignment=WD_ALIGN_PARAGRAPH.CENTER
p=doc.add_paragraph();p.paragraph_format.space_before=Pt(8)
sf(p.add_run(nd("Attach #2 (“the chart”):  fb_table.png")),10.5,True,False,NAVY)
doc.add_picture(f"{SCR}/fb_table.png",width=Inches(6.4));doc.paragraphs[-1].alignment=WD_ALIGN_PARAGRAPH.CENTER

from datetime import datetime
_now=datetime.now()
doc.core_properties.created=_now
doc.core_properties.modified=_now
doc.core_properties.last_modified_by="Alex Karpowitsch"
doc.core_properties.author="Alex Karpowitsch"
doc.core_properties.title="Fund the Need They Named"

out=f"{SCR}/Oakland_Enhancement_Millage_Analysis.docx"
doc.save(out);print("saved",out)
