"""Regenerate sitemap.xml from the actual files in the repo."""
import subprocess
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
    ("/advertise.html", "monthly", "0.5"),
    ("/privacy.html", "yearly", "0.3"),
    ("/disclaimer.html", "yearly", "0.3"),
]

lines = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
def lastmod(path):
    """Last git commit date of the file (today if uncommitted changes), so Google
    sees real modification dates instead of every URL bumped on every run."""
    rel = path.lstrip("/") or "index.html"
    if rel.endswith("/"):
        rel += "index.html"
    dirty = subprocess.run(["git", "status", "--porcelain", "--", rel], cwd=ROOT,
                           capture_output=True, text=True).stdout.strip()
    if dirty:
        return TODAY
    out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", rel], cwd=ROOT,
                         capture_output=True, text=True).stdout.strip()
    return out or TODAY

for path, freq, prio in ENTRIES:
    lines += [
        "  <url>",
        f"    <loc>{BASE}{path}</loc>",
        f"    <lastmod>{lastmod(path)}</lastmod>",
        f"    <changefreq>{freq}</changefreq>",
        f"    <priority>{prio}</priority>",
        "  </url>",
    ]
lines.append("</urlset>")

(ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Wrote sitemap.xml with {len(ENTRIES)} URLs")
