"""Render all peptide guide pages from build/peptides.yaml + build/suppliers.yaml.

Usage:  py build/render_peptides.py        # render every peptide
        py build/render_peptides.py bpc-157 tb-500   # render specific slugs

Outputs to ../peptides/<slug>.html relative to this script.
Also rewrites ../sitemap.xml and ../peptides/index.html guide hub.
"""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined

ROOT = Path(__file__).resolve().parent.parent
BUILD = Path(__file__).resolve().parent
PEPTIDES_DIR = ROOT / "peptides"


def load_data() -> tuple[dict, dict]:
    suppliers = yaml.safe_load((BUILD / "suppliers.yaml").read_text(encoding="utf-8"))
    peptides = yaml.safe_load((BUILD / "peptides.yaml").read_text(encoding="utf-8"))
    return suppliers, peptides


def render_peptide(env: Environment, slug: str, p: dict, suppliers: dict) -> str:
    tmpl = env.get_template("peptide_template.html.j2")
    resolved_suppliers = [suppliers[k] for k in p["suppliers"]]
    name = p["name"]
    return tmpl.render(
        slug=slug,
        name=name,
        h1_em=p.get("h1_em", name),
        seo_title=p.get("seo_title", f"Where to Buy {name} | ThePeptideRadar"),
        seo_description=p.get(
            "seo_description",
            f"Explore peptide suppliers selling {name} with available COAs, lab sources, "
            "and shipping info. Country-filtered, transparency-first, no paid placements.",
        ),
        seo_keywords=p.get("seo_keywords", f"{name}, buy {name}, {name} supplier, where to buy {name}, {name} review"),
        og_title=p.get("og_title", f"Where to Buy {name} — Trusted Peptide Suppliers"),
        og_description=p.get(
            "og_description",
            f"Explore peptide suppliers selling {name} with available COAs, lab sources, and shipping data.",
        ),
        lead=p.get(
            "lead",
            f"Explore trusted research peptide suppliers selling {name} — with available "
            "third-party COAs, lab sources, and shipping data. No paid rankings.",
        ),
        intro=p["intro"],
        suppliers=resolved_suppliers,
        comparison=p.get("comparison"),
        what_to_look_for=p.get("what_to_look_for"),
        faqs=p["faqs"],
        related=p.get("related", DEFAULT_RELATED),
    )


DEFAULT_RELATED = [
    {"slug": "bpc-157", "label": "BPC-157"},
    {"slug": "retatrutide", "label": "Retatrutide"},
    {"slug": "tirzepatide", "label": "Tirzepatide"},
    {"slug": "sermorelin", "label": "Sermorelin"},
]


def write_sitemap(slugs: list[str]) -> None:
    today = date.today().isoformat()
    static = [
        ("https://thepeptideradar.com/", "1.0", "weekly"),
        ("https://thepeptideradar.com/peptides/", "0.9", "weekly"),
    ]
    peptide_urls = [
        (f"https://thepeptideradar.com/peptides/{s}.html", "0.8", "monthly")
        for s in sorted(slugs)
    ]
    legal = [
        ("https://thepeptideradar.com/privacy.html", "0.3", "yearly"),
        ("https://thepeptideradar.com/disclaimer.html", "0.3", "yearly"),
    ]
    parts = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, prio, freq in static + peptide_urls + legal:
        parts.append("  <url>")
        parts.append(f"    <loc>{loc}</loc>")
        parts.append(f"    <lastmod>{today}</lastmod>")
        parts.append(f"    <changefreq>{freq}</changefreq>")
        parts.append(f"    <priority>{prio}</priority>")
        parts.append("  </url>")
    parts.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(parts) + "\n", encoding="utf-8")


def main() -> None:
    suppliers, peptides = load_data()
    env = Environment(
        loader=FileSystemLoader(str(BUILD)),
        undefined=StrictUndefined,
        keep_trailing_newline=True,
    )

    only = set(sys.argv[1:])
    rendered: list[str] = []
    for slug, p in peptides.items():
        if only and slug not in only:
            continue
        html = render_peptide(env, slug, p, suppliers)
        out = PEPTIDES_DIR / f"{slug}.html"
        out.write_text(html, encoding="utf-8")
        rendered.append(slug)
        print(f"  wrote peptides/{slug}.html")

    if not only:
        write_sitemap(list(peptides.keys()))
        print("  wrote sitemap.xml")

    print(f"done — {len(rendered)} page(s)")


if __name__ == "__main__":
    main()
