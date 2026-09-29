"""AR101 Lab 10: make the chaos plates. Needs Pillow (already in the course .venv).

    python chaos_plates.py            # writes plate_n0.png, plate_n2.png, plate_n4.png, plate_n8.png
    python chaos_plates.py --demo     # also writes the lecture's two telegraphs on every plate

Every plate is 512 x 512. The floor has value (CIE L*) 30. Each stacked effect
adds 10 value points over the telegraph area, capped at 100, exactly as in the
week 10 lecture. The telegraph goes in the dashed guide circle: center (256, 300),
radius 110. Paint your telegraph on a copy of each plate, then measure it with
contrast_probe.py.
"""
import math
import random
import sys

from PIL import Image, ImageDraw

SIZE = 512
CENTER = (256, 300)
RADIUS = 110
V_FLOOR = 30
E = 10


def value_to_gray(v):
    """CIE L* (0-100) -> sRGB gray level 0-255."""
    v = max(0.0, min(100.0, v))
    y = ((v + 16) / 116) ** 3 if v > 8 else v * 27 / 24389
    c = 12.92 * y if y <= 0.0031308 else 1.055 * y ** (1 / 2.4) - 0.055
    return round(255 * c)


def effect_amount(x, y, cx, cy, core=150, edge=175):
    """How much of one effect covers pixel (x, y): 1 inside the core, fading to 0 at the edge."""
    d = math.hypot(x - cx, y - cy)
    if d <= core:
        return 1.0
    if d >= edge:
        return 0.0
    return (edge - d) / (edge - core)


def make_plate(n, seed=10):
    rng = random.Random(seed + n)
    centers = [(CENTER[0] + rng.randint(-8, 8), CENTER[1] + rng.randint(-8, 8)) for _ in range(n)]
    # small decorative sparks away from the telegraph, for looks only
    sparks = [(rng.randint(20, 492), rng.randint(20, 120), rng.randint(10, 28)) for _ in range(2 * n)]
    img = Image.new("RGB", (SIZE, SIZE))
    px = img.load()
    for y in range(SIZE):
        for x in range(SIZE):
            tile = 1 if ((x // 32) + (y // 32)) % 2 else -1      # faint flagstones
            v = V_FLOOR + tile + sum(E * effect_amount(x, y, cx, cy) for cx, cy in centers)
            for sx, sy, sr in sparks:
                d = math.hypot(x - sx, y - sy)
                if d < sr:
                    v += 25 * (1 - d / sr)
            g = value_to_gray(min(100, v))
            px[x, y] = (g, g, g)
    draw = ImageDraw.Draw(img)
    for a in range(0, 360, 12):                                   # dashed guide circle
        t0, t1 = math.radians(a), math.radians(a + 6)
        draw.arc([CENTER[0] - RADIUS, CENTER[1] - RADIUS, CENTER[0] + RADIUS, CENTER[1] + RADIUS],
                 math.degrees(t0), math.degrees(t1), fill=(90, 90, 90))
    return img


def gray_to_value(g):
    c = g / 255
    y = c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return 116 * y ** (1 / 3) - 16 if y > 216 / 24389 else y * 24389 / 27


def draw_demo(img, fill_t=40, rim_alpha=0.8, rim=True):
    """The lecture's telegraph: additive fill of t value points, optional dark rim."""
    out = img.copy()
    px = out.load()
    for y in range(CENTER[1] - RADIUS - 4, CENTER[1] + RADIUS + 5):
        for x in range(CENTER[0] - RADIUS - 4, CENTER[0] + RADIUS + 5):
            d = math.hypot(x - CENTER[0], y - CENTER[1])
            v = gray_to_value(px[x, y][0])
            if rim and RADIUS - 2 <= d <= RADIUS + 2:
                v = (1 - rim_alpha) * v                           # alpha-over black
            elif d < RADIUS - 2:
                v = min(100, v + fill_t)                          # additive fill
            else:
                continue
            g = value_to_gray(v)
            px[x, y] = (g, g, g)
    return out


if __name__ == "__main__":
    demo = "--demo" in sys.argv
    for n in (0, 2, 4, 8):
        plate = make_plate(n)
        plate.save(f"plate_n{n}.png")
        print(f"wrote plate_n{n}.png")
        if demo:
            draw_demo(plate, rim=False).save(f"demo_fill_n{n}.png")
            draw_demo(plate, rim=True).save(f"demo_tone_n{n}.png")
            print(f"wrote demo_fill_n{n}.png and demo_tone_n{n}.png")
