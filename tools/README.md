# Tools

The exact scripts used to generate this project's deliverables. See
[`../docs/TOOLING.md`](../docs/TOOLING.md) for the full method, data sources, and
reproduction steps.

| Script | Makes | Needs |
|---|---|---|
| `build_doc.py` | the Word analysis + "Facebook Kit" (`.docx`) | `python-docx`; the two share images present in the working dir |
| `make_images.py` | `funding-chart.png`, `problem-vs-plan.png` | `Pillow`, `matplotlib` (fonts) |
| `make_banner.py` | `TSD_group_banner.png` (FB group cover) | `Pillow`, `matplotlib` (fonts) |

```bash
pip install python-docx pandas openpyxl Pillow matplotlib
python3 make_images.py      # run first: build_doc.py embeds these images
python3 build_doc.py
python3 make_banner.py
```

**Notes**
- These are the scripts *as run*. Output paths were the author's working directory
  (sanitized to `.`) plus `~/Downloads`; adjust for your environment.
- `build_doc.py` reads no data at runtime — the analyzed figures are baked in as
  constants after the data pipeline in `TOOLING.md` produced them. To re-derive the
  numbers from source, follow `TOOLING.md` §7.
- `build_doc.py` includes an `nd()` guard that raises if an em/en dash appears in the
  document text.
- `make_banner.py`'s palette was sampled from Troy School District's own logo
  (black + vegas gold `#b4a269` + cream).
