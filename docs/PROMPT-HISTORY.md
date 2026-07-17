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

---

## Session 2 (July 16, 2026): review, and the net-donor question

**18.** *"Please review the repo 'tsd-enhancementmillage' on my github, which is online at 'https://tsd-enhancementmillage.karpowitsch.org/'"*
→ Reviewed the code, the Cloudflare config, and the live site, and fact-checked the
   published claims against primary sources. Confirmed the PII scrub is clean (no email
   address appears in any file in any commit) and that `.assetsignore` really does keep
   `docs/`, `tools/`, and `README.md` off the deployed site. Findings recorded in
   [`FINDINGS.md`](FINDINGS.md); the significant ones are that the downloadable Word doc
   still carries the pre-softening language, and that the MEA article cited for the
   special-education figures contains no special-education content.

**19.** *"...I want you to build a section called 'the numbers', where you break down the section 705 3 mill count legal maximum, and that the District could potentially come back for up to 3 mills in 2034. Also... I want you to build an interactive graph that uses enrollment numbers for each school, using SEMCOG data projections... I want to model to what degree are Troy School District residents net donors, and if Troy School District loses student population while other Districts gain, as a proportion, Troy's net donor amount will increase... a calculator for taxable value (which is typically half o state equalized value)..."*
→ Two corrections came out of this before any code was written. First, taxable value is
   not half of state equalized value: **SEV** is half of market value, and **taxable
   value is capped *at* SEV** by Proposal A until a transfer of ownership uncaps it.
   Building `TV = SEV/2` would have halved every tax figure on the page. Second, and
   larger: the net-donor premise does not survive the data. See #21.

**20.** *"I want to press you on the Troy taxable claim - where are you getting those numbers? Troy has a huge amount of taxable property, is the largest city in Oakland County"*
→ Fair challenge, and the premise is correct: Troy ranks **4th of 28** in total taxable
   value ($5.08B). But donor status turns on taxable value **per pupil**, and there Troy
   ranks **16th of 28** ($414,336) because it also has the county's second-largest
   enrollment. Birmingham's tax base is larger than Troy's while serving 40% fewer
   students, giving it 2.4x Troy's per-pupil base. Provenance traced to MDE Bulletin
   1014's `HSEV`/`NHSEV` columns, which the bulletin's own glossary defines as ad valorem
   **taxable** value from Form DS4410, and verified against MDE's own published
   per-pupil columns.

**21.** *"Are those %'s your citing for Oakland County? Who gained in Oakland County while Troy decreased? I find this very hard to believe"*
→ Re-checked against a second, independent instrument (MI School Data fall headcount, a
   raw body count rather than blended FTE). Both sources agree: only four of 28 districts
   grew — **Avondale, Oxford, Novi, Ferndale**. The finding is not that Troy shrank while
   others grew; it is that **Troy shrank while almost everyone shrank more**. Troy's
   −6.8% ranks 10th of 28 against a county-wide −11.8%. That is why Troy's *share* of
   pupils rose, and why it is drifting further into net-receiver territory rather than
   toward donor status. `enrollment_trend.py` now runs this cross-check on every
   invocation and prints where the two sources disagree.

**22.** *"Please remember that nearly 700-1000 students are school of choice students outside of Troy. You need to absolutely factor in 105/105c values for each district in this calculation"*
→ A real methodological gap. MCL 380.705(3) distributes on **membership**, so a district
   is paid for the nonresident students it enrolls under Sections 105/105c, while the
   tax is levied on property **inside its boundary**. School of choice therefore breaks
   the link between who pays and who is counted, and the sign depends on direction:
   inbound students make a district more of a net receiver, outbound push it toward
   donor. Researched against primary sources; treatment recorded in
   [`TOOLING.md`](TOOLING.md).

**23.** *"Please use primary sources when identify 105/105c counts"*
→ Restricted the 105/105c research to state primary records (MDE state aid reports, the
   Pupil Accounting Manual, CEPI, MCL 388.1705/1705c) rather than district pages or news
   coverage.

**24.** *"Please ensure this current tooling you've created is captured with version control, .md files are capturing prompt history (are they arleady?), and everything is reproducible and uploaded to github"*
→ They were not — this file stopped at #17. Added entries 18-24, packaged the analysis
   as [`millage_data.py`](../tools/millage_data.py),
   [`net_position.py`](../tools/net_position.py) and
   [`enrollment_trend.py`](../tools/enrollment_trend.py) (all of which fetch their own
   data from state servers and run from a clean checkout), corrected the errors this
   review found in [`TOOLING.md`](TOOLING.md) and [`tools/README.md`](../tools/README.md),
   and recorded the review in [`FINDINGS.md`](FINDINGS.md).

**25.** *"After you do that, let's get back to the analysis. Where do we stand there? Along with updating the website?"* / *"I was more referring to a theoretical 2034 vote where they could change it from 1.5 mills to anything they wanted - presumably more, if enrollment continues to decrease. So that should be a part of what you build - a theoretical 2034 calculator that allows people to type in whatever mill count they want, up to 3, and also incorporates the same design for potential changes in enrollment across districts in the calculator"*
→ Built the **"The numbers"** section: a plain-English Section 705 explainer, a
   market-to-SEV-to-taxable-value calculator, and an interactive table of all 52 Oakland
   entities with editable enrollment, an academy toggle, and a millage-rate control that
   runs to the 3-mill statutory cap. Chose, on the author's instruction, to ship the
   calculators **without** an argument attached. One thing the math settled: the rate
   does not change *who* is a donor, because raising it scales what every district pays
   and receives together. Only enrollment and tax-base shares change the sign. Framed as
   "a future renewal" rather than 2034, since the levy runs 2026-2031 and no source
   supports that specific year.

**26.** *"Please ensure this current tooling you've created is captured..."* (continued)
→ Applied all four corrections the review found: regenerated the `.docx` and both share
   images from the softened copy (they had been contradicting the site since July 3),
   replaced the MEA misattribution with the primary sources, corrected Troy's $9.7M to
   $9.6M, Macomb's $55M to the audited $66.4M, and Troy's median sale to $435,000, and
   fixed the dark-mode dead code. Corrections are noted in-place on the page rather than
   made silently.

**27.** *"Can you please find information on how the Oakland ISD building was created in 1990 and there was a scandal about it? I dont want to tell you too much, I want you to find this"* / *"Yes, that is the story I was referring to. I want you to incorporate this into the site in a section at the end called 'OC History'"*
→ Found it, and the date anchor was off by about a dozen years: the millage was **2001**, the
   building opened **2003**, the reforms passed **2004**, the conviction came **2005**. Nothing
   resembling it exists around 1990. (Two plausible sources of the misremembering: Oakland
   Schools' own records show a PA-18 special-education *distribution* shortfall from 1988-89
   discovered in 1990-91, which is also a "special-ed money went wrong at Oakland Schools"
   story; and Oakland Unified in **California** was engulfed in a theft-and-patronage scandal in
   September 1989, which is the wrong Oakland and contaminates almost every search.)
   Built the **OC History** section on the court record rather than on the news reprints, because
   the Free Press / Oakland Press / MIRS coverage survives online only on a parent-advocacy site
   with the Detroit News originals paywalled. The best evidence turned out to be sworn trial
   testimony quoted in the federal habeas opinion: the district's facilities consultant was asked
   to recount the building's square footage attributable to special education, counting corridors
   and storage, to "make sure that they were getting the maximum amount from special ed."

**28.** *"Now I want you to create a 500 word, couple paragraph, plain formatting post saved as a word document on my desktop..."* / *"...in the style of my language that I've used interacting with you across prompts, a largely a 'just the facts', but also a 'Here's the whole picture that no one to date has clearly laid out'"*
→ `tools/make_post.py`, writing to the OneDrive-redirected Desktop.

**29.** *"Yeah fix the Clerk call"* / *"We validated there was a special education millage vote in 2001 so we know immediatley the claim is problematic, even though that millage and this current 705 are functionally diferent"*
→ Nothing to fix, and the flag was mine to withdraw: I had told the author the "Oakland has
   never voted on an enhancement millage" claim was "prominent enough on the page" to warrant
   verifying with the County Clerk. It is not on the page at all. Every claim the site makes is
   present-tense and verified: Oakland levies no enhancement today, Macomb does. The author then
   supplied the reason the claim should never be added, which is better than the one I had:
   **it would contradict this site's own OC History section**, which documents a county-wide,
   ISD-levied school millage vote on September 25, 2001. The instruments differ, but that
   distinction takes a paragraph and the rebuttal takes four words. Item closed in
   [`FINDINGS.md`](FINDINGS.md) §6 rather than left open.
