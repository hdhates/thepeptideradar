# Build scripts

Small Python utilities for keeping the site healthy.

## Setup

```
python -m pip install jinja2 pillow
```

## Scripts

- `gen_sitemap.py` — scans `peptides/*.html` and rewrites `sitemap.xml` with today's `lastmod`. Run after adding/removing a peptide guide.
- `seo_check.py` — lints every HTML page for title/description length, missing OG tags, missing canonical, duplicate titles, and H1 issues. Run before pushing.
- `make_og.py` — regenerates the branded `og-image.png` (1200×630 PNG ~63 KB). Run when the brand or hero copy changes.
- `optimize_og.py` — re-saves an existing `og-image.png` with PIL optimisation; emits a JPEG fallback if the PNG stays heavy.
- `run_all.py` — runs `gen_sitemap` + `seo_check`. Pass `--og` to also regenerate the OG image.

## Typical workflow

```
# After adding a new peptide guide
python build/run_all.py

# After changing brand copy / hero on the OG card
python build/run_all.py --og
```
