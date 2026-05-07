"""Compress og-image.png if it's larger than the target.

Recommended OG image size is 1200x630 and under ~300 KB.
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "og-image.png"
TARGET_KB = 250
TARGET_DIM = (1200, 630)

if not SRC.exists():
    print("og-image.png not found — skipping")
    raise SystemExit(0)

orig_kb = SRC.stat().st_size / 1024
print(f"Original: {orig_kb:.0f} KB")

img = Image.open(SRC)
if img.size != TARGET_DIM:
    img = img.resize(TARGET_DIM, Image.LANCZOS)
    print(f"Resized to {TARGET_DIM}")

# Convert to RGB and save with optimization
img = img.convert("RGB")
img.save(SRC, "PNG", optimize=True)

new_kb = SRC.stat().st_size / 1024
print(f"Optimized PNG: {new_kb:.0f} KB")

# If still too big, save as JPEG fallback at og-image.jpg + suggest meta swap
if new_kb > TARGET_KB:
    jpg = SRC.with_suffix(".jpg")
    img.save(jpg, "JPEG", quality=85, optimize=True, progressive=True)
    jpg_kb = jpg.stat().st_size / 1024
    print(f"JPEG fallback: {jpg_kb:.0f} KB at {jpg.name}")
    if jpg_kb < new_kb:
        # Replace PNG with JPEG-content saved as .png (cheap trick for the existing references)
        # Actually better: keep both; user can swap meta tags if they want
        print(f"NOTE: Consider swapping og-image.png references to og-image.jpg in meta tags ({jpg_kb:.0f} KB vs {new_kb:.0f} KB)")
