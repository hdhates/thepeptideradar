"""Generate a branded 1200x630 OG image for ThePeptideRadar."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "og-image.png"

W, H = 1200, 630
BG = (10, 10, 15)
GREEN = (78, 207, 122)
TEXT = (240, 237, 232)
TEXT2 = (240, 237, 232, 153)

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img, "RGBA")

# Subtle radial gradient via stacked translucent circles in the corner
for r, alpha in [(900, 18), (700, 22), (500, 28), (300, 36)]:
    cx, cy = 200, 320
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(78, 207, 122, alpha))

# Radar logo: concentric circles + sweep line
cx, cy = 220, 200
for radius, width, alpha in [(140, 8, 255), (95, 6, 180), (50, 4, 110)]:
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
                 outline=GREEN + (alpha,), width=width)
draw.line([cx, cy, cx + 110, cy - 100], fill=GREEN, width=8)
draw.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=GREEN)

# Try to load a system font; fallback chain
def load_font(size, bold=True):
    candidates = [
        r"C:\Windows\Fonts\Arial Bold.ttf" if bold else r"C:\Windows\Fonts\Arial.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for c in candidates:
        try:
            return ImageFont.truetype(c, size)
        except OSError:
            continue
    return ImageFont.load_default()

font_h1 = load_font(82, bold=True)
font_h2 = load_font(36, bold=False)
font_brand = load_font(34, bold=True)
font_tag = load_font(20, bold=True)

# Brand label
draw.text((420, 110), "THEPEPTIDERADAR", font=font_brand, fill=TEXT)
draw.text((420, 150), "INDEPENDENT  ·  TRANSPARENT  ·  DATA-REVIEWED", font=font_tag, fill=GREEN)

# Headline
draw.text((420, 240), "Explore peptide", font=font_h1, fill=TEXT)
draw.text((420, 330), "suppliers with", font=font_h1, fill=TEXT)
draw.text((420, 420), "clear lab data.", font=font_h1, fill=GREEN)

# Subhead
draw.text((420, 530), "COAs · Lab sources · Shipping · Reviews", font=font_h2, fill=(240, 237, 232, 180))

# Domain
draw.text((50, 580), "thepeptideradar.com", font=font_brand, fill=GREEN)

img.save(OUT, "PNG", optimize=True)
kb = OUT.stat().st_size / 1024
print(f"Wrote {OUT.name}: {kb:.0f} KB ({W}x{H})")
