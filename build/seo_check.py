"""Quick SEO linter for static HTML pages.

Checks:
- meta description length (120-160 ideal)
- title length (under 60 ideal)
- exactly one H1
- canonical link present
- og:image / og:title / og:description present
- duplicate titles across pages
"""
import re
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent

PAGES = [ROOT / "index.html",
         ROOT / "privacy.html",
         ROOT / "disclaimer.html",
         ROOT / "peptides/index.html"]
PAGES += sorted((ROOT / "peptides").glob("*.html"))
PAGES = [p for p in PAGES if p.exists()]
PAGES = list(dict.fromkeys(PAGES))  # de-dup, preserve order

def grab(pattern, text, group=1, flags=re.IGNORECASE | re.DOTALL):
    m = re.search(pattern, text, flags)
    return m.group(group).strip() if m else None

def count(pattern, text, flags=re.IGNORECASE | re.DOTALL):
    return len(re.findall(pattern, text, flags))

issues = []
titles = []

for page in PAGES:
    rel = page.relative_to(ROOT)
    text = page.read_text(encoding="utf-8")

    title = grab(r"<title>(.*?)</title>", text)
    desc = grab(r'<meta\s+name="description"\s+content="([^"]*)"', text)
    canon = grab(r'<link\s+rel="canonical"\s+href="([^"]*)"', text)
    og_image = grab(r'<meta\s+property="og:image"\s+content="([^"]*)"', text)
    og_title = grab(r'<meta\s+property="og:title"\s+content="([^"]*)"', text)
    og_desc = grab(r'<meta\s+property="og:description"\s+content="([^"]*)"', text)
    h1_count = count(r"<h1[\s>]", text)

    page_issues = []
    if not title:
        page_issues.append("missing <title>")
    elif len(title) > 65:
        page_issues.append(f"title too long ({len(title)} chars)")
    else:
        titles.append((title, str(rel)))

    if not desc:
        page_issues.append("missing meta description")
    elif len(desc) > 165:
        page_issues.append(f"meta description too long ({len(desc)} chars)")
    elif len(desc) < 80:
        page_issues.append(f"meta description short ({len(desc)} chars)")

    if not canon:
        page_issues.append("missing canonical")
    if not og_image:
        page_issues.append("missing og:image")
    if not og_title:
        page_issues.append("missing og:title")
    if not og_desc:
        page_issues.append("missing og:description")
    if h1_count == 0:
        page_issues.append("no <h1>")
    elif h1_count > 1:
        page_issues.append(f"multiple <h1> tags ({h1_count})")

    if page_issues:
        issues.append((rel, page_issues))

# Duplicate titles
title_counter = Counter(t for t, _ in titles)
dupes = {t: [p for tt, p in titles if tt == t] for t, c in title_counter.items() if c > 1}

print(f"Scanned {len(PAGES)} pages\n")
if not issues and not dupes:
    print("OK - No SEO issues found")
else:
    if issues:
        print("Per-page issues:")
        for rel, errs in issues:
            print(f"  {rel}")
            for e in errs:
                print(f"    - {e}")
        print()
    if dupes:
        print("Duplicate titles:")
        for t, pages in dupes.items():
            print(f"  '{t}'")
            for p in pages:
                print(f"    - {p}")
