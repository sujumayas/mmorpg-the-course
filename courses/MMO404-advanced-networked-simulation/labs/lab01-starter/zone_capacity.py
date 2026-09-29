"""MMO404 Lab 01: how many players fit in one zone server?

    python zone_capacity.py --check          # tests your functions against the week 1 lecture
    python zone_capacity.py --measure        # model vs measured pairs on seeded zones
    python zone_capacity.py --sweep out.csv  # capacity for hot-spot shares 0.00 to 1.00

Implement every function marked TODO. The model is in the week 1 lecture, section 2.
Standard library only.
"""
import csv
import math
import random
import sys
from collections import defaultdict

C_P = 20e-6     # CPU seconds per player per tick
C_I = 2e-6      # CPU seconds per interacting ordered pair per tick
BUDGET = 0.050  # usable CPU seconds per tick (half of a 10 Hz tick)
ZONE = 2000.0   # zone side in metres
R = 100.0       # area-of-interest radius in metres
SPOT = 50.0     # radius of the hot spot in metres (R / 2, so everyone in it sees everyone)


def aoi_fraction(radius=R, side=ZONE):
    """f: the share of the zone's area that one player's AOI disc covers. TODO."""
    raise NotImplementedError


def pair_fraction(h, f):
    """Share of the n*n ordered pairs that interact when a share h of players stands
    in one hot spot and the rest are spread evenly: h^2 + (1 - h^2) * f. TODO."""
    raise NotImplementedError


def tick_ms(n, h, f, c_p=C_P, c_i=C_I):
    """Tick time in milliseconds: c_p * n + c_i * n^2 * pair_fraction(h, f). TODO."""
    raise NotImplementedError


def capacity(h, f, c_p=C_P, c_i=C_I, budget=BUDGET):
    """Largest n (a float) whose tick fits in the budget. Solve the quadratic. TODO."""
    raise NotImplementedError


def count_pairs(points, radius):
    """Ordered pairs (i, j), i != j, closer than or at `radius`. Use a uniform grid with
    cells of side `radius` and check only the 3 x 3 block around each cell. TODO."""
    raise NotImplementedError


def brute_pairs(points, radius):
    """Reference answer for count_pairs. Given. O(n^2)."""
    r2 = radius * radius
    return sum(1 for i, (x1, y1) in enumerate(points) for j, (x2, y2) in enumerate(points)
               if i != j and (x1 - x2) ** 2 + (y1 - y2) ** 2 <= r2)


def make_zone(n, h, size=ZONE, spot=SPOT, seed=1):
    """n players: round(h*n) in a disc of radius `spot` at the centre, the rest uniform. Given."""
    rng = random.Random(seed)
    cx = cy = size / 2
    pts = []
    for i in range(n):
        if i < round(h * n):
            r = spot * math.sqrt(rng.random())
            a = rng.uniform(0, 2 * math.pi)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        else:
            pts.append((rng.uniform(0, size), rng.uniform(0, size)))
    return pts


def check():
    f = aoi_fraction()
    assert abs(f - 0.0078540) < 1e-6, f"aoi_fraction {f}"
    assert abs(pair_fraction(0.0, f) - f) < 1e-12
    assert abs(pair_fraction(1.0, f) - 1.0) < 1e-12
    assert abs(tick_ms(1000, 0.0, f) - 35.7) < 0.05, tick_ms(1000, 0.0, f)
    assert abs(tick_ms(1000, 0.25, f) - 159.7) < 0.05, tick_ms(1000, 0.25, f)
    assert abs(tick_ms(1000, 1.0, f) - 2020.0) < 0.05, tick_ms(1000, 1.0, f)
    for h, want in ((0.0, 1258), (0.1, 938), (0.5, 294), (1.0, 153)):
        got = capacity(h, f)
        assert round(got) == want, f"capacity({h}) = {got:.1f}, lecture says {want}"
        assert abs(tick_ms(got, h, f) - 1000 * BUDGET) < 1e-6, "capacity must fill the budget exactly"
    pts = make_zone(400, 0.2, seed=5)
    assert count_pairs(pts, R) == brute_pairs(pts, R), "count_pairs disagrees with brute force"
    print("all checks passed")


def measure():
    f = aoi_fraction()
    print(" h     measured pairs   model pairs   measured/model")
    for h in (0.0, 0.1, 0.25, 0.5, 1.0):
        n = 1000
        got = count_pairs(make_zone(n, h), R)
        model = n * n * pair_fraction(h, f)
        print(f"{h:4.2f}  {got:14d}  {model:12.0f}   {got / model:6.3f}")


def sweep(path):
    f = aoi_fraction()
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["h", "capacity", "capacity_2x_cpu", "tick_ms_at_1000"])
        for k in range(0, 101, 5):
            h = k / 100
            w.writerow([h, round(capacity(h, f), 1),
                        round(capacity(h, f, C_P / 2, C_I / 2), 1),
                        round(tick_ms(1000, h, f), 2)])
    print("wrote", path)


if __name__ == "__main__":
    if "--check" in sys.argv:
        check()
    elif "--measure" in sys.argv:
        measure()
    elif "--sweep" in sys.argv:
        sweep(sys.argv[sys.argv.index("--sweep") + 1])
    else:
        print(__doc__)
