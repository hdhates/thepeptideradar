"""Generate a clean square logo image for schema.org Organization.logo,
manifest icons, and general brand use.

Outputs: logo-512.png (and a 192 size for PWA / mobile).
Google/Bing recommend a square logo at least 112x112 (ideally 600x600).
"""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent

GREEN = (78, 207, 122)
BG = (10, 10, 15)


def render(size: int, path: Path):
    img = Image.new("RGB", (size, size), BG)
    draw = ImageDraw.Draw(img, "RGBA")
    cx, cy = size / 2, size / 2

    # Concentric rings (matching the SVG nav logo)
    rings = [
        (0.44, max(2, size * 0.060), 255),
        (0.29, max(2, size * 0.040), 153),
        (0.14, max(1, size * 0.030),  90),
    ]
    for r_frac, w, alpha in rings:
        r = size * r_frac
        draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                     outline=GREEN + (alpha,), width=int(w))

    # Sweep line from center to upper-right
    sx, sy = cx + size * 0.34, cy - size * 0.32
    draw.line([cx, cy, sx, sy], fill=GREEN, width=int(max(2, size * 0.05)))

    # Center dot
    dot = size * 0.05
    draw.ellipse([cx - dot, cy - dot, cx + dot, cy + dot], fill=GREEN)

    img.save(path, "PNG", optimize=True)
    kb = path.stat().st_size / 1024
    print(f"Wrote {path.name}: {kb:.0f} KB ({size}x{size})")


render(512, ROOT / "logo-512.png")
render(192, ROOT / "logo-192.png")
