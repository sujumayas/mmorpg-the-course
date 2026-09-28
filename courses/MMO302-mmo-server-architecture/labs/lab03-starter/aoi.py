"""MMO302 lab 03: area of interest (week 3 lecture).

Run:
    python aoi.py --table        # the lecture's broadcast / grid / radius table
    python aoi.py --bench        # time brute force against the grid
    python aoi.py --boundary     # the hysteresis table from section 4

Standard library only. Worlds are generated with mulberry32 seed 302, the
same generator and seed as the week 3 interactive, so counts match exactly.
"""
import argparse
import math
import time
from collections import defaultdict


def mulberry32(seed):
    a = seed & 0xFFFFFFFF

    def rnd():
        nonlocal a
        a = (a + 0x6D2B79F5) & 0xFFFFFFFF
        t = a
        t = ((t ^ (t >> 15)) * (t | 1)) & 0xFFFFFFFF
        t ^= (t + (((t ^ (t >> 7)) * (t | 61)) & 0xFFFFFFFF)) & 0xFFFFFFFF
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296
    return rnd


def make_world(n, f, seed=302, w=1000.0, cx=500.0, cy=500.0, crowd_r=20.0):
    """round(f * n) players in a disc of radius crowd_r at (cx, cy), the rest
    uniform over a w x w square. Draw order matches the interactive."""
    rnd = mulberry32(seed)
    k = round(f * n)
    pts = []
    for i in range(n):
        if i < k:
            rr = crowd_r * math.sqrt(rnd())
            th = 2 * math.pi * rnd()
            pts.append((cx + rr * math.cos(th), cy + rr * math.sin(th)))
        else:
            pts.append((w * rnd(), w * rnd()))
    return pts


def brute_sets(pts, r):
    """For each player i, the set of j != i within distance r. O(n^2)."""
    r2 = r * r
    out = []
    for i, (x, y) in enumerate(pts):
        s = set()
        for j, (a, b) in enumerate(pts):
            if i != j and (x - a) ** 2 + (y - b) ** 2 <= r2:
                s.add(j)
        out.append(s)
    return out


def cell_of(p, c):
    return (math.floor(p[0] / c), math.floor(p[1] / c))


def build_grid(pts, c):
    """Spatial hash: dict mapping (cx, cy) -> list of player indices."""
    # TODO: write this (see the docstring and the lecture).
    raise NotImplementedError


def candidates(grid, p, c, k=1):
    """Indices in the (2k+1) x (2k+1) block of cells around p's cell
    (including the player itself if it is in the grid)."""
    # TODO: write this (see the docstring and the lecture).
    raise NotImplementedError


def grid_count(pts, c, k=1):
    """Deliveries per tick under grid AOI: sum over players of
    (players in their block) - 1."""
    # TODO: write this (see the docstring and the lecture).
    raise NotImplementedError


def grid_radius_sets(pts, r, c, k=1):
    """Broad phase with the grid, narrow phase with exact distance.
    Must return exactly what brute_sets returns whenever k * c >= r
    (the block then covers every point within r)."""
    # TODO: write this (see the docstring and the lecture).
    raise NotImplementedError


class Hysteresis:
    """Enter at d <= r_in, leave at d > r_out. Starts outside.
    step(d) returns 'enter', 'leave' or None, and updates self.inside."""

    def __init__(self, r_in, r_out):
        self.r_in, self.r_out, self.inside = r_in, r_out, False

    def step(self, d):
        # TODO: write this (see the docstring and the lecture).
        raise NotImplementedError


# ---- provided below this line -------------------------------------------

def pacing(t, amp=4.0, period=4.0):
    return 50 - amp * math.cos(2 * math.pi * t / period)


def boundary_run(r_in, r_out, seconds=60, hz=10, amp=4.0):
    h = Hysteresis(r_in, r_out)
    enters = leaves = visible = 0
    for k in range(seconds * hz):
        ev = h.step(pacing(k / hz, amp))
        enters += ev == "enter"
        leaves += ev == "leave"
        visible += h.inside
    return enters, leaves, visible


def print_table(n=1000, r=50.0, c=50.0):
    print(f"{'f':>5} {'broadcast':>10} {'grid':>9} {'radius':>9} {'b/g':>6} {'g/r':>5}")
    for f in (0, 0.10, 0.25, 0.50, 0.75, 1.0):
        pts = make_world(n, f)
        b = n * (n - 1)
        g = grid_count(pts, c)
        rad = sum(len(s) for s in grid_radius_sets(pts, r, c))
        print(f"{f:>5.0%} {b:>10,} {g:>9,} {rad:>9,} {b / g:>6.1f} {g / rad:>5.2f}")


def bench():
    for n in (1000, 2000, 5000):
        pts = make_world(n, 0.0)
        t0 = time.perf_counter()
        a = brute_sets(pts, 50.0) if n <= 2000 else None
        t1 = time.perf_counter()
        g = grid_radius_sets(pts, 50.0, 50.0)
        t2 = time.perf_counter()
        brute = f"{(t1 - t0) * 1000:8.1f} ms" if a is not None else "  skipped"
        print(f"n={n:>5}: brute {brute}, grid {(t2 - t1) * 1000:8.1f} ms")


def print_boundary():
    print(f"{'r_in':>4} {'r_out':>5} {'enters':>6} {'leaves':>6} {'visible':>7} {'B@120':>6} {'B@600':>6}")
    for r_out in (50, 52, 54, 60):
        e, l, v = boundary_run(50, r_out)
        print(f"{50:>4} {r_out:>5} {e:>6} {l:>6} {v:>7} {e * 120 + l * 4 + v * 16:>6} "
              f"{e * 600 + l * 4 + v * 16:>6}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--table", action="store_true")
    ap.add_argument("--bench", action="store_true")
    ap.add_argument("--boundary", action="store_true")
    a = ap.parse_args()
    if a.table:
        print_table()
    if a.bench:
        bench()
    if a.boundary:
        print_boundary()
    if not (a.table or a.bench or a.boundary):
        ap.print_help()
