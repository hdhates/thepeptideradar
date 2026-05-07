"""Regenerate sitemap.xml from the actual files in the repo."""
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://thepeptideradar.com"
TODAY = date.today().isoformat()

ENTRIES = [
    ("/", "weekly", "1.0"),
    ("/peptides/", "weekly", "0.9"),
]

for guide in sorted(ROOT.glob("peptides/*.html")):
    if guide.name == "index.html":
        continue
    ENTRIES.append((f"/peptides/{guide.name}", "monthly", "0.8"))

ENTRIES += [
    ("/privacy.html", "yearly", "0.3"),
    ("/disclaimer.html", "yearly", "0.3"),
]

lines = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for path, freq, prio in ENTRIES:
    lines += [
        "  <url>",
        f"    <loc>{BASE}{path}</loc>",
        f"    <lastmod>{TODAY}</lastmod>",
        f"    <changefreq>{freq}</changefreq>",
        f"    <priority>{prio}</priority>",
        "  </url>",
    ]
lines.append("</urlset>")

(ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Wrote sitemap.xml with {len(ENTRIES)} URLs")
