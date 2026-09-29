"""AR101 Lab 11: the squint test as a script. Needs Pillow (in the course .venv).

    python blur_preview.py screenshot.png            # writes screenshot_squint.png
    python blur_preview.py screenshot.png --gray     # also removes color

The blur radius is 1% of the image width (at least 3 px), as in the lecture.
"""
import sys
from pathlib import Path

from PIL import Image, ImageFilter

if __name__ == "__main__":
    files = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not files:
        sys.exit(__doc__)
    for f in files:
        img = Image.open(f).convert("RGB")
        if "--gray" in sys.argv:
            img = img.convert("L").convert("RGB")
        out = img.filter(ImageFilter.GaussianBlur(max(3, img.width // 100)))
        p = Path(f)
        dest = p.with_name(p.stem + "_squint.png")
        out.save(dest)
        print(f"wrote {dest}")
