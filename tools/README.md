# Tools

See [`../docs/TOOLING.md`](../docs/TOOLING.md) for the full method, data sources, and
reproduction steps.

Two groups of scripts live here. The **analysis** scripts fetch their own data from state
servers and run from a clean checkout. The **generator** scripts are the one-shot scripts
that produced the site's deliverables, kept as-run.

## Analysis (reproducible)

| Script | Does | Needs |
|---|---|---|
| `millage_data.py` | shared data layer: downloads and parses the state source files | `openpyxl` |
| `net_position.py` | who pays vs. who receives under the millage, per district | `openpyxl` |
| `enrollment_trend.py` | 8 years of enrollment / taxable-value shares, cross-checked against a second source | `openpyxl` |
| `export_site_data.py` | emits the district table `index.html`'s calculator embeds | `openpyxl` |
| `verify_deliverables.py` | fails if the published `.docx` has drifted away from the site | none |

```bash
pip install openpyxl
python3 verify_deliverables.py           # run after touching index.html or the generators
python3 millage_data.py                  # fetch sources into tools/cache/ (gitignored)
python3 net_position.py                  # academies included, per the ballot language
python3 net_position.py --no-academies   # traditional districts only, the campaign's basis
python3 enrollment_trend.py
```

No arguments, no manual downloads, no API keys. `millage_data.py` caches to `tools/cache/`
and is idempotent; delete that directory to force a refetch. Everything downloads from
`mdoe.state.mi.us` and `michigan.gov` with a browser User-Agent (both 403 default
fetchers).

**Notes**
- Both sides of the millage equation come from one file, MDE Bulletin 1014: `AVG FTE`
  (fall pupil count) is what a district receives on, `HSEV + NHSEV` is what it pays on.
- `HSEV`/`NHSEV` are **taxable** value despite the legacy column names. Bulletin 1014's
  glossary: *"the ad valorem taxable value of real and personal property in the district
  (as reported on the DS4410)"*. This matters — an enhancement millage is levied on
  taxable value, and in Michigan SEV is half of *market* value while taxable value is
  capped **at** SEV (Proposal A), not at half of it.
- `net_position.py` cross-checks itself against the certified ballot language
  ($125,756,247); the gap it reports is two years of taxable-value growth.
- `enrollment_trend.py` checks MDE blended FTE against MI School Data raw headcount and
  prints where they disagree, rather than picking whichever is more convenient.

## Generators (as-run, one-shot)

| Script | Makes | Needs |
|---|---|---|
| `build_doc.py` | the Word analysis + "Facebook Kit" (`.docx`) | `python-docx`; both share images in the working dir |
| `make_images.py` | `funding-chart.png`, `problem-vs-plan.png` | `Pillow`, `matplotlib` (fonts) |
| `make_banner.py` | `tsd_group_banner.png` (FB group cover) | `Pillow`, `matplotlib` (fonts) |

```bash
pip install python-docx Pillow matplotlib
python3 make_images.py      # run first: build_doc.py embeds these images
python3 build_doc.py
python3 make_banner.py
```

Run them from `assets/` so they land where the site expects:

```bash
cd assets && python3 ../tools/make_images.py && python3 ../tools/build_doc.py
python3 ../tools/verify_deliverables.py    # confirm they still agree with the site
```

**Notes**
- `make_images.py` and `build_doc.py` now emit **the repo's actual asset filenames**
  (`funding-chart.png`, `problem-vs-plan.png`, `TSD-Enhancement-Millage-Analysis.docx`).
  Until July 2026 they emitted `fb_table.png`, `fb_problem_vs_plan.png` and
  `Oakland_Enhancement_Millage_Analysis.docx`, and three hand renames closed the gap;
  those renames are gone and the scripts reproduce the names as well as the content.
- **They are also back in step with the site.** They previously still emitted the
  pre-softening language `819d3da` removed from `index.html`, which is how the published
  document came to contradict the page linking it for two weeks. `verify_deliverables.py`
  now fails if that recurs. See [`../docs/FINDINGS.md`](../docs/FINDINGS.md) §1.
- `build_doc.py` reads no data at runtime — the analyzed figures are baked in as constants
  after the data pipeline in `TOOLING.md` produced them. To re-derive them from source,
  follow `TOOLING.md` §7. This is why they can drift, and why the guard exists.
- `build_doc.py` has an `nd()` guard that raises if an em/en dash appears in document
  text, but it does **not** cover every string: the title, the table cells, and several
  runs bypass it. It also relies on `assert`, which `python -O` strips.
- `make_banner.py` is the one script that still writes outside its working directory: it
  also drops a copy in `~/Downloads`. Its palette was sampled from Troy School District's
  own logo (black + vegas gold `#b4a269` + cream).
