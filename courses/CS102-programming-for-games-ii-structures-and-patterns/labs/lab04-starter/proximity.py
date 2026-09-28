"""CS102 Lab 04 starter: counting and timing proximity checks.

Run:  python proximity.py            (prints the table from lecture week 4)
      python proximity.py --clustered (everyone stands in one corner)
      python proximity.py --check     (asserts naive_pairs and grid_pairs agree on hits;
                                       FAILS until you write cluster_fraction_units in step 9)

Two ways to find every pair of units closer than RADIUS:
  naive_pairs  checks every pair: n(n-1)/2 checks, O(n^2)
  grid_pairs   buckets units into cells of size RADIUS and checks only
               the 3x3 block of cells around each unit
Both return (hits, checks) so you can compare work, not only time.
"""
import random
import sys
import time

WORLD = 1000.0   # world is WORLD x WORLD units
RADIUS = 10.0    # "close" means distance < RADIUS


def make_units(n, seed=1, clustered=False):
    rng = random.Random(seed)
    span = 30.0 if clustered else WORLD
    return [(rng.random() * span, rng.random() * span) for _ in range(n)]


def naive_pairs(units, radius=RADIUS):
    r2 = radius * radius
    hits = checks = 0
    n = len(units)
    for i in range(n):
        xi, yi = units[i]
        for j in range(i + 1, n):
            xj, yj = units[j]
            dx, dy = xi - xj, yi - yj
            checks += 1
            if dx * dx + dy * dy < r2:
                hits += 1
    return hits, checks


def grid_pairs(units, radius=RADIUS):
    r2 = radius * radius
    cells = {}                                   # (cx, cy) -> list of unit indices
    for i, (x, y) in enumerate(units):
        cells.setdefault((int(x // radius), int(y // radius)), []).append(i)
    hits = checks = 0
    for i, (x, y) in enumerate(units):
        cx, cy = int(x // radius), int(y // radius)
        for ox in (-1, 0, 1):
            for oy in (-1, 0, 1):
                for j in cells.get((cx + ox, cy + oy), ()):
                    if j <= i:                   # count each pair once
                        continue
                    xj, yj = units[j]
                    dx, dy = x - xj, y - yj
                    checks += 1
                    if dx * dx + dy * dy < r2:
                        hits += 1
    return hits, checks


def timed(fn, units):
    t0 = time.perf_counter()
    hits, checks = fn(units)
    return hits, checks, (time.perf_counter() - t0) * 1000.0


# TODO step 9: write cluster_fraction_units(n, frac, seed=1). It returns n units: the first
# round(frac * n) inside the 30 x 30 corner at the origin, the rest spread over the world.


def check():
    """Both methods must find the same pairs on every layout, or the timing means nothing."""
    ok = True

    def report(label, cond):
        nonlocal ok
        ok &= bool(cond)
        print(("PASS " if cond else "FAIL ") + label)

    for n in (200, 1000):
        for clustered in (False, True):
            units = make_units(n, clustered=clustered)
            for r in (RADIUS, 25.0):
                h1, _ = naive_pairs(units, r)
                h2, _ = grid_pairs(units, r)
                report(f"hits agree: n={n} clustered={clustered} radius={r} ({h1} vs {h2})", h1 == h2)
    mixer = globals().get("cluster_fraction_units")
    report("cluster_fraction_units exists (step 9)", mixer is not None)
    if mixer:
        for frac in (0, 0.1, 0.25, 0.5):
            units = mixer(2000, frac)
            in_corner = sum(1 for x, y in units if x <= 30.0 and y <= 30.0)
            report(f"frac={frac}: 2000 units, at least {round(frac * 2000)} in the corner",
                   len(units) == 2000 and in_corner >= round(frac * 2000))
            h1, _ = naive_pairs(units)
            h2, _ = grid_pairs(units)
            report(f"frac={frac}: hits agree ({h1} vs {h2})", h1 == h2)
    return ok


def main():
    if "--check" in sys.argv:
        sys.exit(0 if check() else 1)
    clustered = "--clustered" in sys.argv
    sizes = [100, 250, 500, 1000, 2000] if clustered else [100, 250, 500, 1000, 2000, 4000]
    print(f"{'n':>6} {'naive checks':>13} {'naive ms':>9} {'grid checks':>12} {'grid ms':>8} {'hits':>7}")
    for n in sizes:
        units = make_units(n, clustered=clustered)
        h1, c1, t1 = timed(naive_pairs, units)
        h2, c2, t2 = timed(grid_pairs, units)
        assert h1 == h2, "both methods must find the same pairs"
        print(f"{n:>6} {c1:>13,} {t1:>9.1f} {c2:>12,} {t2:>8.2f} {h1:>7,}")


if __name__ == "__main__":
    main()
