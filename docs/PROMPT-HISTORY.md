# Prompt history

A chronological record of the requests that produced this project, for
transparency and provenance. Each entry is the request (verbatim, lightly
trimmed) followed by a short note on what was done. Personal contact details have
been redacted. Work was done with an AI coding assistant (Claude Code); all data
is public and sourced in [`TOOLING.md`](TOOLING.md).

> A few requests arrived mid-task (marked *[while working]*); they are shown where
> they occurred.

---

**1.** *"Can you please identify all schools that are part of the Oakland ISD and Macomb ISD? I would then like to tabulate how much local funding, on a per capita basis, each ISD receives based on a Michigan bulletin report (I think you can search and identify this)"*
→ Identified all 28 Oakland Schools and 21 Macomb ISD member districts; located MDE Bulletin 1014/1011; began extracting per-district local funding.

**2.** *[while working]* *"I think I can download the FID data for you...what file should I download? See screenshot on desktop"*
→ Determined the needed file (the FID Revenue/Balance Sheet/ESP data), then fetched it directly, so no manual download was needed.

**3.** *"With those current figures and what Oakland County is proposing in the August 2026 enhancement millage, how does Oakland compare with Macomb in a scenario where Oakland passes the proposed enhancement millage?"*
→ Modeled the scenario: found the 1.5-mill / ~$781-per-pupil proposal and that Macomb already levies a ~1.82-mill enhancement; built the before/after comparison.

**4.** *"Can you create a Word document of this analysis and include table formatting that would be publishable to Facebook as a post? Please also frame this as an argument that references what's posted to https://oaklandenhancementmillage.com/ is misleading, at best, and somewhat deceptive at worst."*
→ Built the first Word document with formatted tables and a ready-to-post Facebook section.

**5.** *"Please then review and revise the writeup that references the District's communication 'Gmail - Oakland County Enhancement Millage Proposal.pdf' in Downloads, and the section 'Staff Retention and Raises', enhance 'Student Wellness and Support', etc. These are all way too high level, and there's nothing concrete to measure these outcomes, and that all of the enhancement millage should go to fully funding special education, as that has been cited numerous times by the MEA and local school boards (lack of full funding for IDEA). Time to spend the money where their prior communication has referenced, if passed. This is not a grab bag"*
→ Read the District's newsletter, built the "problem they name (special ed) vs. plan they offer (six broad uses)" argument and the dedicate-to-special-education ask; added IDEA-shortfall data.

**6.** *"Please remove em dashes from the writeup"*
→ Removed all em/en dashes and added an automated guard so none can return.

**7.** *"Where is the Word doc saved?"* → Reported the path.

**8.** *"Are you sure its saved there because that .docx file was last edited 20 minutes ago"*
→ Diagnosed it: the file on disk was current; Word was showing `python-docx`'s stale 2013 template date. Fixed the document's internal timestamp.
   *[while working]* *"Please save it in Downloads"* → Confirmed and re-saved to `~/Downloads`.

**9.** *"Let's create a public repo - 'TSD-EnhancementMillage' so we can link it to tsd-enhancementmillage.karpowitsch.org - please build a website from that analysis so we can comprehensively present the analysis you've put together"*
→ Built the single-file website, created the public GitHub repo, and pushed.
   *[while working]* *"...this line stuck out to me - 'Oakland already spends MORE per student ($9,184)...' but thats funding, not spending, right? We need to be very, very sure that there's accuracy... Also please find the average home selling price in Troy in 2025, and what the taxable value/millage cost for that would be. Please run a data accuracy validation pass..."*
→ Confirmed "spending" was wrong (total funding is ~6% apart; the 27% gap is *local*); corrected the language everywhere; added Troy home-cost figures; ran a full accuracy pass.
   *[while working]* *"Please include a section in the Facebook post that breaks down funding vs spending for laypeople"* → Added a plain-English explainer.

**10.** *"Hmm, see the screenshot on my desktop - it doesn't look like the tables will correctly format in the Facebook post. Can you research formatting limitations or drive my Chrome browser to get around this?"*
→ Explained that Facebook strips tables/formatting from posts; produced the numbers as **images** instead (`funding-chart.png`, `problem-vs-plan.png`).

**11.** *"Okay, can you regenerate a .docx file then with text I can copy and paste into the facebook post and revise it to include references to the two tables (fb_problem_vs_plan.png) & fb_table.png"*
→ Rebuilt the doc's "Facebook Kit": copy-paste caption referencing the two images, attach-in-order instructions, and both images embedded.

**12.** *"Is it accurate to say Oakland County taxpayers are shouldering and subsidizing education in Michigan? And by what degree? Need a one-liner here that is defensible with data"*
→ Pulled statewide taxable value and enrollment; derived the net-contributor one-liner (~16% of the tax base vs ~12% of students; ~$85M/yr via the State Education Tax).

**13.** *"Yes, please add it to the FB post and website and image that has the funding table for Oakland vs Macomb"*
→ Added the net-contributor stat to the Facebook post, the website (three stat tiles), and the funding-table image.
   *[while working]* *"Please include a link in the website to where the full text of the District's email can be found, strip out my personal email address ([redacted]) from the email"*
→ Found the newsletter's tracking links encode the recipient email, so instead hosted a **scrubbed transcript** (`assets/district-email.html`) and linked it; confirmed no personal email appears anywhere in the repo.

**14.** *"I like this line A LOT - '...is not leveling with voters.' Can you make a header banner for this (see screenshot of my Facebook group) so I can use this as a slogan? Please use Troy School District's own colors for this (review their website)"*
→ Sampled Troy SD's black + vegas-gold seal palette and built a group-cover banner around the line.

**15.** *"Hmm, I think we can refine this a bit - I want to push them to use 100% of the enhancement millage to fully funding special education and track and report how much that frees up? Can we redo the banner with that? I think stylistically maybe you can put a bit more creative effort into the banner as well"*
→ Redesigned the banner around the constructive demand ("DEDICATE 100%... then track and report what it frees up") with a richer seal-style treatment.

**16.** *"Can you soften the language on the website a little bit? The essence of what I'm trying to say - 'You cannot be handed $9.69M a year (what TSD stands to gain if the millage passes), cite Federal Government Special Education (IDEA) underfunding, and then claim you haven't been handed the solution to the Special Education underfunding problem.'"*
→ Softened the site's sharper phrasing and re-centered it on that constructive logic; reframed a KPI to the $9.7M opportunity.

**17.** *"Thank you, great job with this. Please create .md files for this project for how you created the tooling that you used, and all prompt history, and upload it to the Github repo"*
→ This document, plus [`TOOLING.md`](TOOLING.md) and the scripts in [`/tools`](../tools).
