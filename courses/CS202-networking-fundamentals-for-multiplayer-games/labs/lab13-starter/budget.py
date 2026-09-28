"""CS202 Lab 13: bandwidth budget for a snapshot server.

    python budget.py --check                   # tests your functions against the lecture's numbers
    python budget.py --sweep sweep.csv         # server upload for n = 2..1000, with and without a cap
    python budget.py --world 500 --radius 60   # interest counts on a seeded 500-player world

Implement every function marked TODO. The model is in the week 13 lecture, section 2.
Standard library only.
"""
import csv
import math
import random
import sys

H = 28      # UDP over IPv4 header bytes per packet (week 1)
MTU = 1280  # largest packet we send, headers included (week 1)


def packets_per_snapshot(k, b, h=H, mtu=MTU):
    """Packets needed to carry k entities of b bytes: ceil(k*b / (mtu - h)), at least 1. TODO."""
    raise NotImplementedError


def snapshot_bytes(k, b, h=H, mtu=MTU):
    """Bytes on the wire for one snapshot of k entities: k*b + h*p. TODO."""
    raise NotImplementedError


def client_Bps(n, r, b, K=None, h=H, mtu=MTU):
    """One client's download in bytes/s. k = n without a cap, min(n, K) with one. TODO."""
    raise NotImplementedError


def server_Bps(n, r, b, K=None, h=H, mtu=MTU):
    """Server upload in bytes/s when every client hears the same k entities. TODO."""
    raise NotImplementedError


def make_world(n, size=1000.0, clusters=5, spread=40.0, seed=13):
    """n player positions on a size x size map, bunched around a few hot spots. Given."""
    rng = random.Random(seed)
    centres = [(rng.uniform(0, size), rng.uniform(0, size)) for _ in range(clusters)]
    pts = []
    for _ in range(n):
        if rng.random() < 0.7:
            cx, cy = rng.choice(centres)
            x, y = rng.gauss(cx, spread), rng.gauss(cy, spread)
        else:
            x, y = rng.uniform(0, size), rng.uniform(0, size)
        pts.append((min(max(x, 0.0), size), min(max(y, 0.0), size)))
    return pts


def interest_counts(points, radius):
    """For each player, the number of players (itself included) within `radius`.
    Use a uniform grid with cells of side `radius`: put every point in its cell, then
    check only the 3x3 block of cells around each player. Must match the brute-force
    answer exactly. TODO."""
    raise NotImplementedError


def brute_counts(points, radius):
    """The O(n^2) reference for interest_counts. Given."""
    r2 = radius * radius
    return [sum((px - x) ** 2 + (py - y) ** 2 <= r2 for (px, py) in points) for (x, y) in points]


def server_Bps_per_client(ks, r, b, K=None, h=H, mtu=MTU):
    """Server upload when client i hears ks[i] entities (optionally capped at K). TODO."""
    raise NotImplementedError


def mbit(Bps):
    return Bps * 8 / 1e6


def kbit(Bps):
    return Bps * 8 / 1e3


def check():
    tests = {
        "p(100,40)": (packets_per_snapshot(100, 40), 4),
        "S(100,40)": (snapshot_bytes(100, 40), 4112),
        "S(32,40)": (snapshot_bytes(32, 40), 1336),
        "client n100": (client_Bps(100, 20, 40), 82240),
        "server n100": (server_Bps(100, 20, 40), 8224000),
        "server n50 K32 Mbit": (round(mbit(server_Bps(50, 20, 40, K=32)), 2), 10.69),
        "server n1000 Mbit": (round(mbit(server_Bps(1000, 20, 40)), 1), 6543.4),
        "lever B Mbit": (round(mbit(server_Bps(100, 20, 16)), 2), 26.5),
        "lever C Mbit": (round(mbit(server_Bps(100, 20, 16, K=32)), 2), 8.64),
        "lever D Mbit": (round(mbit(server_Bps(100, 10, 16, K=32)), 2), 4.32),
        "check-yourself 64p": (client_Bps(64, 30, 24), 47760),
    }
    pts = make_world(300, seed=7)
    try:
        tests["grid == brute"] = (interest_counts(pts, 50.0), brute_counts(pts, 50.0))
    except NotImplementedError:
        tests["grid == brute"] = ("TODO", None)
    try:
        tests["per-client sum"] = (server_Bps_per_client([10, 40], 20, 40, K=32),
                                   20 * snapshot_bytes(10, 40) + 20 * snapshot_bytes(32, 40))
    except NotImplementedError:
        tests["per-client sum"] = ("TODO", None)
    bad = [name for name, (got, want) in tests.items() if got != want]
    print("all checks passed" if not bad else f"check these: {bad}")
    return not bad


def sweep(path, r=20, b=40, K=32):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["n", "client_kbit_nocap", "server_mbit_nocap", "client_kbit_cap", "server_mbit_cap"])
        for n in range(2, 1001):
            w.writerow([n, round(kbit(client_Bps(n, r, b)), 2), round(mbit(server_Bps(n, r, b)), 3),
                        round(kbit(client_Bps(n, r, b, K)), 2), round(mbit(server_Bps(n, r, b, K)), 3)])
    print(f"wrote {path}")


def world_report(n, radius, r=20, b=40, K=None):
    pts = make_world(n)
    ks = interest_counts(pts, radius)
    ks_sorted = sorted(ks)
    print(f"{n} players, radius {radius}: k min {ks_sorted[0]}, median {ks_sorted[n // 2]}, "
          f"max {ks_sorted[-1]}, mean {sum(ks) / n:.1f}")
    print(f"server upload, everyone hears everyone: {mbit(server_Bps(n, r, b)):.2f} Mbit/s")
    print(f"server upload, radius {radius}:          {mbit(server_Bps_per_client(ks, r, b, K)):.2f} Mbit/s")
    worst = max(ks) if K is None else min(max(ks), K)
    print(f"worst client download:                {kbit(r * snapshot_bytes(worst, b)):.1f} kbit/s")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] == "--check":
        sys.exit(0 if check() else 1)
    elif args[0] == "--sweep":
        sweep(args[1] if len(args) > 1 else "sweep.csv")
    elif args[0] == "--world":
        n = int(args[1])
        radius = float(args[args.index("--radius") + 1]) if "--radius" in args else 60.0
        K = int(args[args.index("--cap") + 1]) if "--cap" in args else None
        world_report(n, radius, K=K)
    else:
        print(__doc__)
