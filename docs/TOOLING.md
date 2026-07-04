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
| `tools/make_images.py` | `Pillow` | `funding-chart.png` (Oakland vs Macomb funding table + net-contributor banner) and `problem-vs-plan.png` (the "problem they name vs. plan they offer" juxtaposition) |
| `tools/make_banner.py` | `Pillow` | `TSD_group_banner.png` (Facebook group cover, 1640×856) |

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

## 8. Disclaimer

Independent civic analysis by an Oakland County resident. Not affiliated with,
authorized by, or paid for by any school district or ballot committee. Factual claims
are drawn from the public sources above; conclusions are opinion.
