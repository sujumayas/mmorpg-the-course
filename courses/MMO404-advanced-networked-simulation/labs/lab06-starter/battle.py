"""MMO404 Lab 06, part A: battle budget.

    python battle.py --check              # tests your functions against the week 6 lecture
    python battle.py --run battle.csv     # seeded battles from 250 to 4,000 pilots

Implement every function marked TODO. The cost model and the speed f are MMO302 week 12's;
the event-stream model is in the week 6 lecture, section 2. Standard library only.
"""
import csv
import math
import random
import sys

A = 0.0003      # CPU-s per pilot per game-second (MMO302 week 12)
B = 0.000001    # CPU-s per ordered pilot pair per game-second
C = 1.0         # CPU-s the node can spend per real second
FLOOR = 0.1     # slowest game speed allowed


def work(n, a=A, b=B):
    """CPU-seconds to simulate one game-second with n pilots, all in range: a*n + b*n*n. TODO."""
    raise NotImplementedError


def speed(w, capacity=C, floor=FLOOR):
    """MMO302's dilation factor for a node whose work per game-second is w:
    max(floor, min(1, capacity / w)). TODO."""
    raise NotImplementedError


def stream_Bps(n, f, r=2.0, k=12, circle=None, squad=10, summary=8):
    """Bytes per real second of combat events for one client at game speed f.
    circle None: every event to everyone, f*n*r*k.
    Otherwise: f*circle*r*k for the circle plus (n/squad)*summary for the rest. TODO."""
    raise NotImplementedError


def count_pairs(points, radius):
    """Number of unordered pairs of points closer than `radius`. Use a uniform grid with
    cells of side `radius` and check only neighbouring cells. Must equal brute_pairs. TODO."""
    raise NotImplementedError


# ---------------------------------------------------------------- given

def brute_pairs(points, radius):
    r2, total = radius * radius, 0
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            if (points[i][0] - points[j][0]) ** 2 + (points[i][1] - points[j][1]) ** 2 < r2:
                total += 1
    return total


def make_battle(n, seed=6, fleets=6, spread=1500.0, field=20000.0):
    """n pilots in a few fleets on a field (metres). Given."""
    rng = random.Random(seed)
    centres = [(rng.uniform(0.3, 0.7) * field, rng.uniform(0.3, 0.7) * field) for _ in range(fleets)]
    return [(rng.gauss(cx, spread), rng.gauss(cy, spread))
            for cx, cy in (centres[i % fleets] for i in range(n))]


def run(path, weapon_range=5000.0):
    """For each battle size: pairs actually in range, work per game-second with the measured
    pair count (each unordered pair in range costs 2*B, the same as B per ordered pair),
    speed, and per-client streams. Given."""
    rows = []
    for n in (250, 500, 1000, 2000, 4000):
        pts = make_battle(n)
        pairs = count_pairs(pts, weapon_range)
        w = A * n + 2 * B * pairs
        f = speed(w)
        rows.append({"pilots": n, "pairs_in_range": pairs, "pair_share": round(pairs / (n * (n - 1) / 2), 3),
                     "work": round(w, 3), "speed": round(f, 3),
                     "full_kbps": round(stream_Bps(n, f) * 8 / 1000, 1),
                     "aggregated_kbps": round(stream_Bps(n, f, circle=20) * 8 / 1000, 1)})
        print(rows[-1])
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {path}")


def close(a, b, tol=1e-3):
    return abs(a - b) <= tol * max(1.0, abs(b))


def check():
    assert close(work(1000), 1.3) and close(work(3000), 9.9), "work"
    assert close(speed(0.4), 1.0), "no dilation under capacity"
    assert close(speed(work(1000)), 1 / 1.3), "dilation"
    assert close(speed(work(4000)), 0.10), "floor"
    assert close(speed(4.0, capacity=2.0), 0.5), "capacity"
    assert close(stream_Bps(1000, 1.0), 24_000), "full fan-out"
    assert close(stream_Bps(3000, speed(work(3000))) * 8 / 1000, 58.2, tol=2e-3), "dilated at 3,000"
    assert close(stream_Bps(3000, speed(work(3000)), circle=20) * 8 / 1000, 19.6, tol=2e-3), "aggregated at 3,000"
    pts = make_battle(400, seed=1)
    assert count_pairs(pts, 1500.0) == brute_pairs(pts, 1500.0), "grid pairs must match brute force"
    assert count_pairs([(0, 0), (0, 0), (5, 0)], 1.0) == 1, "pairs strictly closer than radius"
    print("all checks passed")


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "--check":
        check()
    elif len(sys.argv) >= 3 and sys.argv[1] == "--run":
        run(sys.argv[2])
    else:
        print(__doc__)
