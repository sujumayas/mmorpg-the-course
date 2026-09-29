"""MMO404 Lab 03: partition a crowded world across 16 servers.

    python partition.py --check        # tests your functions against the week 3 lecture
    python partition.py --compare      # grid vs k-d by headcount vs k-d by load
    python partition.py --crowd 300    # per-server load when one crowd is split 1..32 ways

Load model (week 3 lecture, section 2), in microseconds per tick:
    each owned player            C_P
    each neighbour it interacts   C_I
    extra if that neighbour is owned by another server   C_X
The world, the pair finder, the static grid and the load function are given.
You write kd_headcount, kd_by_load and crowd_split_us. Standard library only.
"""
import bisect
import random
import sys
from collections import defaultdict

SIZE, R = 4000.0, 50.0
C_P, C_I, C_X = 20, 2, 4
SERVERS = 16
BUDGET_MS = 50.0


def make_world(n=3000, seed=7, frac=0.35, spreads=(80, 60, 50, 40, 30)):
    """Given. A 4 km square. A share `frac` of players gathers around five hot spots."""
    rng = random.Random(seed)
    spots = [(rng.uniform(300, 3700), rng.uniform(300, 3700), s) for s in spreads]
    pts = []
    for _ in range(n):
        if rng.random() < frac:
            cx, cy, s = rng.choice(spots)
            x, y = rng.gauss(cx, s), rng.gauss(cy, s)
        else:
            x, y = rng.uniform(0, SIZE), rng.uniform(0, SIZE)
        pts.append((min(max(x, 0), SIZE - 1e-6), min(max(y, 0), SIZE - 1e-6)))
    return pts


def pairs(pts, radius=R):
    """Given. Unordered interacting pairs (i, j), i < j, found with a uniform grid."""
    grid = defaultdict(list)
    for i, (x, y) in enumerate(pts):
        grid[int(x // radius), int(y // radius)].append(i)
    out = []
    r2 = radius * radius
    for (cx, cy), members in grid.items():
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for j in grid.get((cx + dx, cy + dy), ()):
                    for i in members:
                        if i < j and (pts[i][0] - pts[j][0]) ** 2 + (pts[i][1] - pts[j][1]) ** 2 <= r2:
                            out.append((i, j))
    return out


def static_grid(pts, side=4):
    """Given. The zone model: side x side equal squares, one server each."""
    return [int(x * side // SIZE) * side + int(y * side // SIZE) for x, y in pts]


def loads(owner, pr, servers=SERVERS):
    """Given. Per-server load in microseconds per tick, and the number of cross-server pairs."""
    load = [0.0] * servers
    cross = 0
    for s in owner:
        load[s] += C_P
    for i, j in pr:
        a, b = owner[i], owner[j]
        if a == b:
            load[a] += 2 * C_I
        else:
            cross += 1
            load[a] += C_I + C_X
            load[b] += C_I + C_X
    return load, cross


def kd_headcount(pts, idx, servers, depth=0, first=0, out=None):
    """Recursive bisection by headcount. TODO.
    Split `servers` into left = servers // 2 and right = servers - left. Sort idx by x on
    even depths and by y on odd depths. Give the first len(idx) * left // servers players
    to the left half. Recurse until one server remains, then write its number
    (first, first + 1, ...) into out[i]. Return out, a list with one server id per player."""
    raise NotImplementedError


def kd_by_load(pts, idx, servers, neighbours, slack=0.15, first=0, out=None):
    """Recursive bisection by measured load. TODO.
    Weight each player by C_P + 2 * C_I * len(neighbours[i]). At each split, try both
    axes. For every cut position whose left weight share is within `slack` of
    left / servers, count the interacting pairs inside idx that the cut separates.
    Choose the cut with the fewest separated pairs (break ties by closeness to the
    target share). Recurse as in kd_headcount. Return out."""
    raise NotImplementedError


def crowd_split_us(m, s):
    """Per-server load in microseconds when a crowd of m players, all within R of each
    other, is split evenly across s servers: (m/s) * (C_P + C_I*(m-1) + C_X*(m - m/s)). TODO."""
    raise NotImplementedError


def summary(name, owner, pr):
    load, cross = loads(owner, pr)
    mx, mean = max(load) / 1000, sum(load) / len(load) / 1000
    return name, mx, mean, cross, 100 * cross / len(pr)


def build():
    pts = make_world()
    pr = pairs(pts)
    nb = [[] for _ in pts]
    for i, j in pr:
        nb[i].append(j)
        nb[j].append(i)
    everyone = list(range(len(pts)))
    rows = [summary("static 4x4 grid", static_grid(pts), pr),
            summary("k-d by headcount", kd_headcount(pts, everyone, SERVERS), pr),
            summary("k-d by load", kd_by_load(pts, everyone, SERVERS, nb), pr)]
    return pts, pr, rows


def check():
    assert abs(crowd_split_us(300, 1) - 185400) < 1e-6, crowd_split_us(300, 1)
    assert abs(crowd_split_us(300, 4) - 113850) < 1e-6, crowd_split_us(300, 4)
    assert abs(crowd_split_us(300, 16) - 32681.25) < 1e-6, crowd_split_us(300, 16)
    pts, pr, rows = build()
    assert len(pr) == 33056, len(pr)
    grid, head, byload = rows
    assert abs(grid[1] - 68.0) < 0.05, grid
    assert abs(head[1] - 64.7) < 0.05 and abs(head[4] - 28.7) < 0.05, f"kd_headcount: {head}"
    assert byload[1] < BUDGET_MS, f"kd_by_load max {byload[1]:.1f} ms is over the {BUDGET_MS} ms budget"
    assert byload[1] / byload[2] < 2.5, "kd_by_load is not balancing load"
    print("all checks passed")


def compare():
    _, pr, rows = build()
    print(f"interacting pairs: {len(pr)}")
    for name, mx, mean, cross, pct in rows:
        print(f"{name:18} max {mx:6.1f} ms  mean {mean:5.1f} ms  max/mean {mx / mean:4.2f}  "
              f"cross pairs {cross:6d} ({pct:4.1f}%)")


def crowd(m):
    print(f"crowd of {m}: servers, per-server ms, total ms")
    for s in (1, 2, 4, 8, 16, 32):
        per = crowd_split_us(m, s) / 1000
        print(f"{s:3d}  {per:8.1f}  {per * s:8.1f}")


if __name__ == "__main__":
    if "--check" in sys.argv:
        check()
    elif "--compare" in sys.argv:
        compare()
    elif "--crowd" in sys.argv:
        crowd(int(sys.argv[sys.argv.index("--crowd") + 1]))
    else:
        print(__doc__)
