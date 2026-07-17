# Findings — review of July 16, 2026

A record of what a review of this repo and its published claims turned up, and of the
net-position analysis that followed. Kept in the repo because the site's whole premise is
that its numbers can be checked; findings against it belong here too.

**Status.** Sections 1-4 have now been **fixed** — the site, the Word document, and the
share images were corrected on July 16, 2026, and the corrections are noted in-place on
the page rather than made silently. Section 5 (the net-position analysis) shipped as the
"The numbers" section, as a calculator with no argument attached. Section 6 lists what
remains open. The findings are kept here, uncorrected, as the record of what was wrong
and why.

---

## 1. The published Word document contradicts the site

`assets/TSD-Enhancement-Millage-Analysis.docx` is linked twice from the page as
"Download the analysis (Word)". It was last rebuilt in commit `6422d96` (Jul 3, 20:47).
The site's tone was softened six hours later in `819d3da` (Jul 3, 23:53), **which touched
only `index.html`**. The .docx was never regenerated.

So the page says *"This is not a knock on the District, which does disclose the cost and
makes a fair case that schools are stretched"* while the document it links still says:

| phrase | in the .docx | on the site |
|---|---|---|
| "misleading at best" | yes | removed |
| "blank check" | yes | removed |
| "grab bag" | yes | removed |
| "not leveling with voters" | yes | removed |
| "makes the case against itself" | yes | removed |

The two share images (`funding-chart.png`, `problem-vs-plan.png`) are from the same
pre-softening batch, and `funding-chart.png` is also the `og:image` — so every social
share of the softened page carries the unsoftened graphic, which hardcodes a
"widens to nearly 38%" claim that appears nowhere on the page. The .docx also says
$9.6M/$57M for Troy where the site says $9.7M/$58M.

**Fix:** regenerate the .docx and images from the softened copy, or drop the download
links. Whichever way, the deliverables should agree.

## 2. Citation errors

- **The MEA article does not support what it is cited for.** `index.html` and
  `build_doc.py` both attribute the IDEA/28.6%/shortfall figures to MEA's *"Facts v.
  Fallacy: School Funding"*. That article
  ([Part II](https://mea.org/facts-v-fallacy-part-ii-school-funding/), Feb 18, 2026) is
  real but contains **no special-education content at all** — it is about
  inflation-adjusted K-12 funding, charters, and pension debt. The figures actually
  trace to the Autism Alliance of Michigan and the Michigan League for Public Policy.
  This is the single easiest citation on the page to check, and it does not hold.

- **"Michigan's reimbursement: 28.6%, among the lowest in the country"** is a *Durant*
  constitutional **floor** (28.6138% of approved costs, fixed by the 1997 Michigan
  Supreme Court ruling), not Michigan's coverage rate. The House Fiscal Agency
  ([Fiscal Brief, Feb 25, 2026](https://www.house.mi.gov/hfa/PDF/Alpha/Fiscal_Brief_Special_Education_Feb2026.pdf))
  puts actual coverage at **86.0%** of approved special-education costs (FY2023-24).
  Presenting the floor as the coverage rate understates it roughly threefold. "Among the
  lowest in the country" is advocacy language from AAoM's MI Blueprint, not a verified
  50-state ranking.

- **The statewide shortfall has a current number.** The site's "$350M to $750M" is a
  2023 AAoM estimate band. HFA now publishes **$616.8M (FY2023-24)** — inside the band,
  but the band is stale.

- **"<15% what Washington has actually ever paid"** mixes denominators. The federal IDEA
  share is ~**10.2% of national APPE** (FY2025, CRS R44624); the ~15% figure is IDEA as a
  share of *special-education costs*, a different metric. Also "never" fails for FY2009,
  when ARRA pushed it to ~35% of APPE. Qualify as *regular appropriations*.

## 3. Numbers worth revisiting

- **Troy's "$9.7 million a year" is high.** $781 × 12,249 fall FTE = **$9.57M**; $781 ×
  12,283 (NCES headcount) = $9.59M. $9.7M needs ~12,420 pupils. The .docx's "$9.6
  million" is the better figure. Separately, the Detroit News (Mar 25, 2026) reports the
  distribution as **$728 in year one, $782 for the next five**, not a flat $781 — which
  would make Troy's year one ~$8.9M.

- **Macomb's "$55M+ per year" is stale by ~20%.** MISD's own audited financials for FY
  ending 6/2024 report enhancement millage levied of **$66,430,519**, and the MD&A states
  *"In 2024-2025, over $70 million will be levied."* $55M was the 2020 first-year ballot
  estimate.

- **The "$85M+" net-subsidy figure is not reproducible from the stated inputs.** The
  site's own numbers (~16% of tax base, ~12% of students) against the $2.845B statewide
  SET imply ~**$114M**, not $85M. "$85M+" survives as a conservative floor, but the page
  shows no work for it. The mechanism description is also loose: the School Aid Fund does
  not return the SET per-pupil in equal dollars — the foundation allowance is funded by
  local 18-mill revenue first with state aid filling the gap, so equalization is
  Proposal A's *purpose*. And the SET is only ~16% of the SAF.

- **Troy's median sale price is ~$434-442K, not $450K.** Redfin: $433,750 (Dec 2025).

- **Rounding.** The site's table components don't sum to its totals ($7,402 + $1,781 =
  $9,183, printed as $9,184; same +1 in all three columns). Normal rounding, but on a
  page inviting readers to check the math it deserves a "components may not sum due to
  rounding" note. Likewise $338/yr × 6 = $2,028, printed as $2,025 (= 337.50 × 6).

## 4. Code and config

- **`.assetsignore` works.** Verified live: `/README.md`, `/docs/TOOLING.md`,
  `/tools/build_doc.py` all 404. Security headers from `_headers` are all applied.
- **The PII scrub is clean.** No email address appears in any file in any commit across
  the whole history; no tracking tokens in `district-email.html`. (Commit *metadata*
  carries the author's address, as it does on any GitHub repo.)
- **Auto dark mode is dead code.** `<html data-theme="light">` is hardcoded, so the
  `@media (prefers-color-scheme:dark)` block — which is gated on
  `:root:not([data-theme="light"])` — can never match on a first visit. A visitor whose
  OS is in dark mode gets the light page. The `matchMedia` fallback in the toggle is
  unreachable for the same reason. Removing the hardcoded attribute fixes both.
- **The generator scripts don't reproduce the repo's filenames.** `make_images.py` writes
  `fb_table.png` and `fb_problem_vs_plan.png`; the repo holds `funding-chart.png` and
  `problem-vs-plan.png`. `build_doc.py` writes `Oakland_Enhancement_Millage_Analysis.docx`;
  the repo holds `TSD-Enhancement-Millage-Analysis.docx`. Three renames happened by hand
  and were never recorded. Documented in `tools/README.md` as of this commit.
- **The `nd()` dash guard is narrower than advertised.** `TOOLING.md` said every string
  routes through it; in fact the title, the table cells, and several runs in
  `build_doc.py` bypass it. (It also relies on `assert`, which `python -O` strips.)
- **`/assets/district-email.html` 307s** to the extensionless URL — Cloudflare Pages'
  default. Harmless; linking `assets/district-email` directly would skip the hop.

## 5. The net-position analysis (new)

Prompted by a request to model Troy as a net donor. **It is not one.**

Under MCL 380.705(3) revenue is raised *ad valorem* and distributed *per capita*, so a
district is a net donor exactly when its share of the county's taxable value exceeds its
share of the county's pupils. Reproduce with `python3 tools/net_position.py`.

Troy holds **6.586%** of Oakland's taxable value and educates **6.885%** of its pupils,
so it comes out ahead:

| basis | Troy receives | Troy pays | net |
|---|---:|---:|---:|
| academies excluded ($781) | $9.52M | $8.28M | **+$1.24M** |
| academies included ($707) | $8.66M | $8.28M | **+$0.38M** |

Troy is property-rich in absolute terms — **4th of 28** by total taxable value ($5.08B) —
but only **16th of 28** per pupil ($414,336), because it has the county's second-largest
enrollment. Birmingham's base is larger than Troy's across 40% fewer students, giving it
2.4x Troy's per-pupil base.

The real donors, at 2024-25 values: **Birmingham −$6.0M, Bloomfield Hills −$4.1M, Royal
Oak −$2.7M, Pontiac −$2.5M, Walled Lake −$2.1M**. Pontiac is the counterintuitive one — a
low-income city that is a large donor because of its commercial base against only 3,769
students. Rochester (−$0.6M here) publicly describes itself as "a donor district of
approximately $202,300", which corroborates the mechanism if not the exact figure.

**The trend runs opposite to the hypothesis.** Over eight years Troy's tax-base share
fell (6.689% → 6.586%) while its pupil share rose (6.832% → 6.885%), because Troy's
enrollment declined *more slowly* than the county's (−6.3% vs −7.0% on blended FTE; −6.8%
vs −11.8% on raw headcount). Troy's net receipt grew from +$111K to +$346K. Only four of
28 districts gained enrollment — Avondale, Oxford, Novi, Ferndale — confirmed
independently by both MDE Bulletin 1014 and MI School Data.

**A genuine finding for the site:** the campaign's **$781/pupil excludes the academies**.
$125,756,247 ÷ $781 = 161,020 pupils, which matches Oakland's 28 traditional districts
(161,744) and not all 52 entities (177,907). But the certified ballot language says funds
go to districts *"and eligible public school academies"*, and MCL 380.705(7) makes
qualifying academies constituent districts for this purpose — with **no grandfather
delay for a new levy** (§705(9)(a) defers academies only for pre-May-2018
authorizations). If the 24 academies and their 16,163 students are in, the figure is
**$707/pupil — 9.1% lower** — and Troy gets $8.66M, not $9.52M.

### Schools of choice changes the answer

MCL 380.705(3) pays on **membership**, and Troy's membership includes nonresident
Section 105/105c students whose families pay property tax elsewhere. So *"does Troy School
District come out ahead"* and *"do Troy residents come out ahead"* are different questions.

Per MI School Data's *Schools of Choice and Other Non-Resident Enrollments* report, Troy
enrolled **743 nonresident choice students in 2024-25** (707 in 2025-26: 249 under Sec 105,
458 under Sec 105c) against 195 residents leaving. Troy is the outlier among affluent
Oakland districts — Birmingham takes 0, Bloomfield Hills 3, Novi 0, Rochester 0.

| question | answer |
|---|---:|
| Does Troy School **District** come out ahead? | **+$346,148** |
| Do Troy **residents** come out ahead? | **−$137K to +$82K — break-even** |

The district's entire surplus *is* the imported students: 743 × $649.76 = **$482,773** of
Troy's payout is earned educating other districts' children. Strip them out and Troy
residents pay $7,612,952 and get $7,476,327 back (**−$136,625**); add back residents who
leave for other districts and charters and it lands within ±$100K of zero.

**A sharper point.** 458 of Troy's 707 inbound (2025-26) are Sec 105c — from *outside*
Oakland ISD, overwhelmingly Macomb (Warren Consolidated 213 + Utica 176 = 389). Those
families pay **Macomb's** 1.8198-mill enhancement and **no Oakland enhancement**, yet
Oakland's payout to Troy counts them: 458 × $649.76 ≈ **$298K/year**. Within Oakland this
is zero-sum — Troy's gain dilutes every other district.

**Don't model this static.** Net choice has roughly halved, +1,006 (2016-17) → +491
(2025-26), inbound falling off its 2018-19 peak while outbound rose steadily.

## 6. Open / unverified
- **The date of any future renewal.** The *substance* here is settled and is what the
  calculator models: MCL 380.705(1) caps enhancement millages at 3 mills, this one asks
  1.5, §705(5) permits terms up to 20 years and renewal, and a renewal may be put to
  voters at any rate up to the cap. Nothing in §705 imposes a waiting period or an
  election-frequency limit either, unlike MCL 380.681(8), which caps CTE millage elections
  at two per year — a deliberate contrast. Wayne County has renewed twice, each time years
  before its levy expired. What is *not* supported is any particular year: this levy runs
  2026-2031, and no source points to 2034. The real procedural gate is §705(2), which
  requires constituent boards representing a majority of the county's pupils to adopt
  matching resolutions before the ISD board can place anything on the ballot.
- ~~**"Oakland has never voted on an enhancement millage before"**~~ — **closed; do not make
  this claim.** It is not on the site and should not be added. Two reasons, and the second is
  the one that matters. First, it can only be supported by absence of evidence: no prior
  Oakland vote turns up, but older local canvass records are poorly indexed and the Clerk's
  own results archive blocks automated retrieval, so "we could not find one" is the ceiling.
  (Wayne County's 2016 approval is the likely source of any "2016" recollection.) Second, and
  fatally: **it would contradict this site's own OC History section**, which documents Oakland
  Schools putting a county-wide, ISD-levied school millage to voters on September 25, 2001.
  That levy and a §705 enhancement millage are genuinely different instruments, but the
  distinction needs a paragraph to explain and a reader will not wait for it. "Oakland has
  never been asked" invites "yes we were, in 2001" — and that exchange is lost even when the
  underlying point is right. A claim that survives only on a technical carve-out is not worth
  making. The present-tense claims the site *does* make — that Oakland levies no enhancement
  today while Macomb does — are verified and sufficient.
- **Basis mixing in the ~16% claim.** The site's $77B numerator is school-district
  taxable value while the $481.5B denominator is all statewide property. Treasury's
  Oakland *county* figure is $80.36B. Consistent basis gives ~16.7-17.0%.
