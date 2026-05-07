"""Run every build step.

Usage: python build/run_all.py
"""
import subprocess
import sys
from pathlib import Path

BUILD = Path(__file__).resolve().parent
STEPS = [
    ("Regenerate sitemap", "gen_sitemap.py"),
    ("Run SEO linter", "seo_check.py"),
]
# OG image regen is opt-in; only run when --og passed
if "--og" in sys.argv:
    STEPS.insert(0, ("Regenerate OG image", "make_og.py"))

for label, script in STEPS:
    print(f"\n=== {label} ===")
    r = subprocess.run([sys.executable, str(BUILD / script)])
    if r.returncode != 0:
        print(f"FAILED: {script}")
        sys.exit(r.returncode)

print("\nAll steps passed.")
