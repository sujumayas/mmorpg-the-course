"""AR101 Lab 09: predict the first look in a value thumbnail (week 9 model).

    .venv/bin/python focal_map.py scene.png --target 1,4,2,5
    .venv/bin/python focal_map.py scene.png --grid 16x9 --target 3,10,5,12

Each pixel's value is CIE lightness L* (0-100), computed exactly as in AR101
week 1 (linearize sRGB, relative luminance Y, then L*). Values are averaged
into a grid of COLSxROWS cells (default 8x5).

For every cell, C = |V - mean of its up-to-8 neighbours|. The focal cell has the
largest C. The rival is the largest C among cells that do not touch the focal
cell. H = C_focal / C_rival.

--target r0,c0,r1,c1 is the inclusive box of cells (rows r0-r1, columns c0-c1)
where you want the first look. The scene PASSES if the focal cell is inside the
box and H >= 1.5. Exit code 0 on pass, 1 on fail, 2 on bad input.
Needs Pillow (in the course .venv).
"""
import argparse
import sys

from PIL import Image

THRESHOLD = 1.5


def lightness(R, G, B):
    """CIE L* of an sRGB color, 0-100 (AR101 week 1)."""
    def linear(v):
        c = v / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    Y = 0.2126 * linear(R) + 0.7152 * linear(G) + 0.0722 * linear(B)
    return 116 * Y ** (1 / 3) - 16 if Y > 216 / 24389 else 24389 / 27 * Y


def value_grid(path, cols, rows):
    img = Image.open(path).convert("RGB")
    w, h = img.size
    px = img.load()
    grid = []
    for r in range(rows):
        row = []
        y0, y1 = r * h // rows, (r + 1) * h // rows
        for c in range(cols):
            x0, x1 = c * w // cols, (c + 1) * w // cols
            total = n = 0
            for y in range(y0, y1):
                for x in range(x0, x1):
                    R, G, B = px[x, y]
                    total += lightness(R, G, B)
                    n += 1
            row.append(total / n)
        grid.append(row)
    return grid


def contrast_map(grid):
    rows, cols = len(grid), len(grid[0])
    out = []
    for r in range(rows):
        row = []
        for c in range(cols):
            near = [grid[rr][cc] for rr in range(r - 1, r + 2) for cc in range(c - 1, c + 2)
                    if (rr, cc) != (r, c) and 0 <= rr < rows and 0 <= cc < cols]
            row.append(abs(grid[r][c] - sum(near) / len(near)))
        out.append(row)
    return out


def focal(con):
    ranked = sorted(((con[r][c], -r, -c) for r in range(len(con)) for c in range(len(con[0]))),
                    reverse=True)
    top, fr, fc = ranked[0][0], -ranked[0][1], -ranked[0][2]
    rival = next(((v, -r, -c) for v, r, c in ranked[1:]
                  if max(abs(-r - fr), abs(-c - fc)) > 1), (0.0, None, None))
    h = float("inf") if rival[0] == 0 else top / rival[0]
    return (fr, fc), top, (rival[1], rival[2]), rival[0], h


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("image")
    ap.add_argument("--grid", default="8x5", help="COLSxROWS, default 8x5")
    ap.add_argument("--target", required=True, help="r0,c0,r1,c1 inclusive cell box")
    a = ap.parse_args()
    try:
        cols, rows = (int(v) for v in a.grid.lower().split("x"))
        r0, c0, r1, c1 = (int(v) for v in a.target.split(","))
    except ValueError:
        print("bad --grid or --target", file=sys.stderr)
        return 2
    grid = value_grid(a.image, cols, rows)
    con = contrast_map(grid)
    print(f"{a.image}: {cols}x{rows} grid")
    print("values (V):")
    for row in grid:
        print("  " + " ".join(f"{v:4.0f}" for v in row))
    print("local contrast (C):")
    for row in con:
        print("  " + " ".join(f"{v:4.0f}" for v in row))
    (fr, fc), top, (rr, rc), rival, h = focal(con)
    inside = r0 <= fr <= r1 and c0 <= fc <= c1
    print(f"focal cell ({fr},{fc}) C={top:.1f} | rival ({rr},{rc}) C={rival:.1f} | H={h:.2f}")
    print(f"focal inside target box: {'yes' if inside else 'no'} | H >= {THRESHOLD}: {'yes' if h >= THRESHOLD else 'no'}")
    ok = inside and h >= THRESHOLD
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
