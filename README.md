# TSD Enhancement Millage — Independent Analysis

A static, single-page site presenting an independent, data-based analysis of the
**Oakland County Regional Enhancement Millage** on the ballot **Tuesday, August 4, 2026**.

Live: https://tsd-enhancementmillage.karpowitsch.org

## What this is

The Troy School District's June 30, 2026 newsletter names special education as the
problem, then proposes to spend the millage on a grab bag of six unmeasurable uses.
Using Michigan's own financial data, this site shows that Oakland already raises far
more **local** funding per pupil than its peers, and argues that if the millage passes
it should be dedicated to special education with measurable, reported targets.

## Build & deploy

No build step. Plain `index.html` (inline CSS, CSS/JS charts, no external
dependencies) plus static assets. Deployed on **Cloudflare Pages** connected to this
GitHub repo: pushing to `main` triggers a deploy. Custom domain:
`tsd-enhancementmillage.karpowitsch.org`.

## Key figures (FY2024-25, validated against MDE data)

- Local funding per pupil: **Oakland $9,184** vs **Macomb $7,247** (and Macomb already
  levies a 1.82-mill enhancement; Oakland does not).
- With the proposed 1.5-mill millage (about $781 per pupil): **Oakland $9,965**.
- Important distinction: this is **local** funding, not total spending. Total per-pupil
  operating funding, counting state and federal aid, is much closer (about **$17,100**
  in Oakland vs about **$16,100** in Macomb), because state aid offsets local wealth.

## Data sources

- MDE Bulletin 1014 & 1011 (2024-25) and the state Financial Information Database
  (Revenue Data, 2024-25). Oakland member-district local revenue reconciles exactly to
  the MDE Bulletin 1011 export.
- Troy School District newsletter, June 30, 2026 (all quotations and the six spending tiles).
- U.S. Census (2024) for population; Redfin, Zillow, RealtyTrac for Troy home values (2025-26).
- Special-education funding: Michigan Education Association, Michigan House Fiscal Agency,
  Michigan League for Public Policy, Autism Alliance of Michigan.

## Files

- `index.html` — the site
- `assets/funding-chart.png`, `assets/problem-vs-plan.png` — share/social images
- `assets/TSD-Enhancement-Millage-Analysis.docx` — the full write-up (Word), including a
  ready-to-post Facebook version
- `_headers`, `robots.txt` — Cloudflare Pages headers and crawler policy

## Disclaimer

Independent civic commentary by an Oakland County resident. Not affiliated with,
authorized by, or paid for by the Troy School District, Oakland Schools, any school
district, or any ballot committee. Factual claims are drawn from the public sources
listed above; the conclusions are opinion. Quotations from the District's newsletter
are reproduced for comment and criticism.
