# How this project was built (tooling & method)

This site and its companion deliverables (a Word analysis, share images, and a
Facebook group banner) were produced as an independent, data-based analysis of the
Oakland County Regional Enhancement Millage on the August 4, 2026 ballot, with the
help of an AI coding assistant (Claude Code). This document records the data
pipeline, the scripts, and how to reproduce the results, so the numbers can be
checked and the work re-run.

Everything here is built from **public** data. The headline figures reconcile to
the State of Michigan's own files (see [Validation](#validation)).

---

## 1. Environment & dependencies

- **Python 3** with: `python-docx`, `pandas`, `openpyxl`, `Pillow` (PIL), `matplotlib` (used only for its bundled fonts)
- **poppler** (`pdftotext`) for reading state PDFs
- **curl** (with a browser User-Agent, see below), **Google Chrome** (headless, for rendering/screenshot checks)
- **git** + **GitHub CLI** (`gh`) for the repo, **Cloudflare Pages** for hosting

## 2. Data sources

| Source | File / URL | Used for |
|---|---|---|
| MDE **Bulletin 1014**, "Michigan Public School Districts Ranked by Selected Financial Data," 2024-25 | `mdoe.state.mi.us/SAMSPublic/Reports/others/b1014_25FINAL.pdf` | Per-district **Local Sources per pupil**, Fall FTE membership, taxable value per pupil |
| MDE **Bulletin 1011** data export, 2024-25 | `mdoe.state.mi.us/SAMSPublic/Reports/others/25_Bulletin1011Export.xlsx` | Per-entity local revenue (`LOCREV`); confirmed it **excludes ISD central agencies** |
| MDE **Financial Information Database (FID)**, Revenue Data, 2024-25 | `2025_CEPI_33_FID_REVENUE_DATA.xlsx`, inside `michigan.gov/cepi/.../MISchoolData/2024-25/2025CEPI_32_33_34_Data.zip` (linked from `mischooldata.org/financial-data-files`) | **ISD-entity** revenue by fund & major class (the piece not in the bulletins) |
| Michigan **Senate Fiscal Agency**, "State Property Valuations 1970-2025" | `sfa.senate.michigan.gov/Revenue/StateEqualizedPropertyValues.PDF` | **Statewide taxable value** (2024 = $481.5B) |
| U.S. Census (2024) | census.gov QuickFacts | County population (Oakland ~1,296,888; Macomb ~886,175) |
| Redfin / Zillow / RealtyTrac | web | Troy 2025 median home sale price (~$450,000) |
| MEA, MI House Fiscal Agency, MI League for Public Policy, Autism Alliance of MI | web | IDEA / special-education funding shortfall figures |
| Troy School District newsletter, June 30, 2026 | recipient email (transcript in `assets/district-email.html`, scrubbed) | The District's own quotes and the six proposed uses |
| Oakland enhancement campaign | `oaklandenhancementmillage.com` | Proposal terms: 1.5 mills, 6 years, ~$781/pupil |

Added July 16, 2026, for the analysis scripts in [§8](#8-analysis-scripts-who-pays-vs-who-receives-added-july-16-2026). These are fetched automatically by `tools/millage_data.py`:

| Source | File / URL | Used for |
|---|---|---|
| MDE **Bulletin 1014** exports, 8 years (2017-18 .. 2024-25) | `mdoe.state.mi.us/SAMSPublic/Reports/others/{18,19,20}` → `Bulletin1014Export{yy}.xlsx`; `{21,22,23}` → `{yy}_Bulletin1014 Export.xlsx`; `{24,25}` → `{yy}_Bulletin1014Export.xlsx` | Per-district pupil count + taxable value, and the 8-year share trend |
| **MI School Data** fall headcount | `michigan.gov/cepi/-/media/Project/Websites/cepi/MISchoolData/{2016-17/1617_Fall_headcount.xlsx, 2024-25/Spring_2025_Headcount.xlsx, 2025-26/Spring_2026_Headcount.xlsx}` | **Independent** enrollment cross-check (raw headcount vs. blended FTE) |
| **Certified ballot language**, Oakland Regional Enhancement Millage | Oakland Schools / constituent district postings | The $125,756,247 year-one estimate used to validate the modeled levy |
| **MCL 380.705**, Revised School Code | `legislature.mi.gov/documents/mcl/pdf/mcl-380-705.pdf` | The 3-mill cap, the 20-year term limit, the per-pupil distribution formula, academy eligibility |
| **MCL 380.1211**, **MCL 211.7cc** | `legislature.mi.gov` | Proof that the principal residence exemption does **not** reach an enhancement millage |

### Access technique (403 bypass)
`michigan.gov` and `mischooldata.org` return **HTTP 403** to default fetchers
(Cloudflare bot protection). `curl` with a normal browser User-Agent returns 200:

```bash
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/125.0 Safari/537.36"
curl -s -A "$UA" -L "<url>" -o out.file
```

## 3. Key definitions & computations

- **"Local funding"** = an entity's own local sources (**Major Class `1xx`**), **governmental funds** (exclude proprietary/fiduciary fund codes **60/70/80**). In the FID file, revenue amounts are credits (**negative**), so they are negated.
- **Bulletin gotcha:** Bulletin 1014's "Local Sources per pupil" = own local (`1xx`) **plus** `OTHPUBMI` (`5xx`, money passed *through* the ISD to the district). For a clean "own local" measure, use **`1xx` only** — otherwise the ISD's special-ed millage is double-counted.
- **ISD entity code = ISD number × 1000** (Oakland Schools = `63000`, Macomb ISD = `50000`). ISDs are absent from Bulletins 1011/1014; they live only in FID.
- **Local vs. total (the accuracy point):** the 27% Oakland-vs-Macomb gap is in *local* dollars. Counting state + federal aid, total operating funding per pupil is close (~$17,100 vs ~$16,100), because Proposal A sends more state aid to lower-wealth districts.
- **Net contributor:** Oakland's school tax base (~$77B) is ~16% of the statewide $481.5B, but its enrollment (~162k) is ~12% of the state's 1.38M — so under the pooled 6-mill State Education Tax it pays in more than it draws (~$85M/yr net).

## 4. Generator scripts (`/tools`)

| Script | Library | Produces |
|---|---|---|
| `tools/build_doc.py` | `python-docx` | `Oakland_Enhancement_Millage_Analysis.docx` (the analysis + a ready-to-post "Facebook Kit") |
| `tools/make_images.py` | `Pillow` | `fb_table.png` (Oakland vs Macomb funding table + net-contributor banner) and `fb_problem_vs_plan.png` (the "problem they name vs. plan they offer" juxtaposition) |
| `tools/make_banner.py` | `Pillow` | `tsd_group_banner.png` (Facebook group cover, 1640×856) |

> **The generators' filenames do not match the repo's assets.** `fb_table.png` was renamed
> by hand to `assets/funding-chart.png`, `fb_problem_vs_plan.png` to
> `assets/problem-vs-plan.png`, and `Oakland_Enhancement_Millage_Analysis.docx` to
> `assets/TSD-Enhancement-Millage-Analysis.docx`. The scripts reproduce the content, not
> the names. The generators are also **stale relative to the site**: they still emit the
> pre-softening language removed from `index.html` in `819d3da`. See
> [`FINDINGS.md`](FINDINGS.md) §1.

Notable techniques:
- **Dash guard.** `build_doc.py` routes every string through an `nd()` helper that
  `assert`s no em dash (`—`) or en dash (`–`) can slip into the document.
- **Real "last modified" date.** `python-docx` copies a fixed 2013 timestamp from its
  blank template; the script overwrites `core_properties.created/modified` with the
  current time so Word shows the correct date.
- **Brand-color sampling.** The banner's palette (black + vegas gold `#b4a269` + cream)
  was sampled directly from Troy School District's own logo with a `PIL` +
  `collections.Counter` pass over the pixels.
- **Accessible chart colors.** The chart series (Oakland blue / Macomb orange) were
  chosen to pass a color-vision-deficiency separation check, with values direct-labeled.

## 5. Rendering & verification

- The website and each generated image were rendered/inspected with **headless Chrome**:
  ```bash
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    --headless=new --disable-gpu --hide-scrollbars --window-size=1280,7200 \
    --screenshot=out.png "file://.../index.html"
  ```
- The site is a **single `index.html`** (inline CSS, CSS/JS charts, **no external
  dependencies**), with security headers + a content-security-policy in `_headers`.

## 6. Validation

Two independent internal checks kept the numbers honest:
1. **LEA local revenue reconciliation.** Summing FID Major-Class-`1xx` (governmental
   funds) for Oakland's 28 member districts gives **$1,197,278,354** — identical to the
   Bulletin 1011 export's `LOCREV` field. Different files, same number.
2. **Local vs. total sanity check.** Recomputing *total* per-pupil funding (all sources)
   confirmed the two counties are ~6% apart in total but ~27% apart in local dollars,
   which is why the site is careful to say **"local funding," never "spending."**

## 7. Reproduce

1. Create a working directory; download the files in [§2](#2-data-sources) into it
   (use the curl-with-UA technique for `michigan.gov` / `mischooldata.org`).
2. `pip install python-docx pandas openpyxl Pillow matplotlib` and install `poppler`.
3. `pdftotext -layout b1014_25FINAL.pdf b1014_25.txt`, then parse per-district rows.
4. Load the FID xlsx with `pandas` and aggregate as described in [§3](#3-key-definitions--computations).
5. Run `tools/build_doc.py`, `tools/make_images.py`, `tools/make_banner.py`.

> The scripts in `/tools` are the exact ones used. They were run against a local
> working directory of downloaded data; absolute output paths appear as-run and should
> be adjusted for your environment. See `tools/README.md`.

## 8. Analysis scripts: who pays vs. who receives (added July 16, 2026)

The generators above bake their figures in as constants. The scripts added later are
different: they **fetch their own data from state servers and recompute from scratch**, so
anyone can check the arithmetic without a working directory of manual downloads.

```bash
pip install openpyxl
python3 tools/millage_data.py                  # fetch sources into tools/cache/
python3 tools/net_position.py                  # academies included (ballot language)
python3 tools/net_position.py --no-academies   # traditional only (the campaign's basis)
python3 tools/enrollment_trend.py
```

### The mechanism

MCL 380.705(3) is the whole model. Verbatim:

> "the intermediate school district shall calculate and pay to each of its constituent
> districts an amount of the revenue calculated by **dividing the total amount of the
> revenue by the combined membership** of the constituent districts within the
> intermediate school district ... and **multiplying that quotient by the constituent
> district's membership**"

Taxable value appears nowhere in that formula. Revenue is raised *ad valorem* (by property
wealth) and distributed *per capita* (by pupil count), so:

> a district is a **net donor** exactly when its share of the county's taxable value
> exceeds its share of the county's pupils.

That share formulation is used deliberately because it is **vintage-independent**: scaling
every district's taxable value by the same factor (2024-25 values → the 2026 levy base)
scales what it pays *and* what it receives, and cannot flip anyone's sign. Only
*differential* growth between districts can.

### One file, both sides

Both halves come from **MDE Bulletin 1014**, which is why the analysis needs no join:

| column | is | feeds |
|---|---|---|
| `AVG FTE` | fall pupil count (state aid membership) | what a district **receives** |
| `HSEV` + `NHSEV` | ad valorem **taxable** value (Form DS4410) | what a district **pays** |

`HSEV`/`NHSEV` are legacy names for **taxable value**, per Bulletin 1014's own glossary:
*"Taxable Value Per State Aid Member (Homestead and Non-Homestead) ... dividing the ad
valorem taxable value of real and personal property in the district (as reported on the
DS4410) by the Fall Pupil Count."* The distinction is load-bearing: an enhancement millage
is levied on taxable value, and in Michigan **SEV is half of market value while taxable
value is capped *at* SEV** by Proposal A (uncapping to SEV on transfer of ownership).
Taxable value is not half of SEV.

### Validation built into the scripts

1. **Against MDE's own arithmetic.** `HSEV ÷ AVG FTE` reproduces MDE's published
   `AVG HSEV` column to the dollar.
2. **Against the certified ballot language.** The 2024-25 base ($77.07B) is 91.9% of the
   base implied by the ballot's $125,756,247 estimate — two years of taxable-value growth,
   as expected.
3. **Against a second, independent instrument.** `enrollment_trend.py` re-runs the
   enrollment trend on MI School Data fall **headcount** (raw bodies) beside Bulletin
   1014's **blended FTE**, and prints where they disagree. They agree on all four
   districts that gained; they disagree on Clarkston, which is a blended-FTE artifact.
   Levels differ ~5.8% county-wide (1.0% for Troy) because the two count different things.
   The model uses blended FTE, because §705(3) distributes on membership.

### Sections 105 / 105c: district-level is not resident-level

§705(3) distributes on **membership**, so a district is paid for nonresident students it
enrolls under Section 105 (within-ISD) or 105c (contiguous-ISD) school of choice — while
the tax is levied on property **inside its boundary**. School of choice therefore breaks
the link between who pays and who is counted. `net_position.py` reports both views.

Counts come from **MI School Data, "Schools of Choice and Other Non-Resident
Enrollments"** (CEPI/MDE, 2009-10 to present, no login). That report is a residency ×
enrollment cross-tab queried **per district** — there is no bulk download, so the Troy
series in `millage_data.TROY_SOC` is transcribed rather than fetched. A full 28-district
sweep is mechanical against `legacy.mischooldata.org/.../NonResidentStatus.aspx` with
`Common_NonResidentStatus=ChoiceInsideISD|ChoiceOutsideISD` (`ChoiceInsideISD` = Sec 105,
`ChoiceOutsideISD` = Sec 105c), but needs a browser session.

Two dead ends worth recording so nobody repeats them: the **DS-4061/FSR does not itemize
105/105c** (it is a payment-detail report with aggregate membership only), and SAMSPublic's
**"NonResident Foundation Adjustment Report" is not school of choice** — its own footnote
scopes it to Section 20(5) special-education placements.

Authority: **MCL 388.1705(1)** and the **2025-26 Pupil Accounting Manual §5-I** both
confirm the *enrolling* district counts the pupil in membership and the resident district
does not.

Not covered by this data: Troy residents in **private** school, who pay the millage and
generate no per-pupil for anyone. See [`FINDINGS.md`](FINDINGS.md) §5.

## 9. Disclaimer

Independent civic analysis by an Oakland County resident. Not affiliated with,
authorized by, or paid for by any school district or ballot committee. Factual claims
are drawn from the public sources above; conclusions are opinion.
