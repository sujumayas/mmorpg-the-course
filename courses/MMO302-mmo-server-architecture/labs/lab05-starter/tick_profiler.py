"""MMO302 lab 05: tick budget profiler (week 5 lecture).

Run:
    python tick_profiler.py --lecture            # the lecture's budget and feel tables from your functions
    python tick_profiler.py --measure out.csv    # time real ticks of a toy world at several n and crowd sizes
    python tick_profiler.py --fit out.csv        # fit a, d, e from your measurements and print T_max

Standard library only. Fill in every function marked TODO, then run test_tick_profiler.py.
"""
import argparse
import csv
import math
import random
import time


# ---------------------------------------------------------------- the budget model

def tick_cost(a, d, e, n, k):
    """One tick in ms: a + d*n + e*n*k (a, d, e in ms)."""
    # TODO: write this (see the docstring and the lecture).
    raise NotImplementedError


def utilization(c, rate):
    """Share of wall-clock time the server is busy: c * T / 1000."""
    # TODO: write this (see the docstring and the lecture).
    raise NotImplementedError


def t_max(c, u_max=0.6):
    """Highest tick rate (Hz) that keeps utilization at or under u_max."""
    # TODO: write this (see the docstring and the lecture).
    raise NotImplementedError


def timer_length(tau, rate):
    """A timer of tau seconds measured in whole ticks lasts ceil(tau * T) / T seconds.
    Guard against float noise: 1.2 * 5 must count as 6 ticks, not 7."""
    # TODO: write this (see the docstring and the lecture).
    raise NotImplementedError


def same_tick_probability(delta, rate):
    """Chance that two actions delta seconds apart land in the same tick: max(0, 1 - delta*T)."""
    # TODO: write this (see the docstring and the lecture).
    raise NotImplementedError


def multirate_cpu_per_second(a, d, e, n_active, k, n_idle, rate, idle_rate=1.0):
    """CPU ms per second when n_active entities tick at `rate` and n_idle entities tick at
    `idle_rate`. The fixed cost a is paid once per main tick. Idle entities use the same k."""
    # TODO: write this (see the docstring and the lecture).
    raise NotImplementedError


def fit_costs(samples):
    """Least-squares fit of c = a + d*n + e*(n*k) to samples [(n, k, c_ms), ...].
    Return (a, d, e). Solve the 3x3 normal equations yourself (no numpy)."""
    # TODO: write this (see the docstring and the lecture).
    raise NotImplementedError


def schedule(costs, rate, policy="stretch"):
    """Simulate a tick loop. costs[i] is tick i's CPU time in ms; tick i is due at i * (1000/T).
    stretch: each tick starts at max(due, end of previous tick).
    skip:    as stretch, but a tick whose start would be late by one full interval or more
             is skipped (it costs nothing, and the next tick is judged on its own due time).
    Return (starts, skipped): starts[i] is tick i's start in ms, or None if skipped."""
    # TODO: write this (see the docstring and the lecture).
    raise NotImplementedError


# ---------------------------------------------------------------- a toy world to measure (provided)

class World:
    """n entities on a square map with grid AOI of radius r. crowd entities stand in one
    circle of radius crowd_radius at the centre; the rest are spread evenly.
    tick() does per-entity work (move, a little arithmetic) and per-neighbour work
    (distance test against every entity in the 3x3 cells around it)."""

    def __init__(self, n, size=2000.0, radius=50.0, crowd=0, crowd_radius=60.0, seed=1):
        rnd = random.Random(seed)
        self.size, self.r = size, radius
        self.pos = []
        for i in range(n):
            if i < crowd:
                ang, rr = rnd.random() * 2 * math.pi, crowd_radius * math.sqrt(rnd.random())
                self.pos.append([size / 2 + rr * math.cos(ang), size / 2 + rr * math.sin(ang)])
            else:
                self.pos.append([rnd.random() * size, rnd.random() * size])
        self.vel = [[rnd.uniform(-1, 1), rnd.uniform(-1, 1)] for _ in range(n)]
        self.hp = [100.0] * n
        self.last_k = 0.0

    def tick(self):
        size, r, r2 = self.size, self.r, self.r * self.r
        cells = {}
        for i, (x, y) in enumerate(self.pos):            # per-entity: move and bin
            vx, vy = self.vel[i]
            x = (x + vx * 0.1) % size
            y = (y + vy * 0.1) % size
            self.pos[i] = [x, y]
            self.hp[i] = min(100.0, self.hp[i] + 0.01)
            cells.setdefault((int(x // r), int(y // r)), []).append(i)
        pairs = 0
        for i, (x, y) in enumerate(self.pos):            # per-neighbour: AOI test
            cx, cy = int(x // r), int(y // r)
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    for j in cells.get((cx + dx, cy + dy), ()):
                        ox, oy = self.pos[j]
                        if (ox - x) ** 2 + (oy - y) ** 2 <= r2 and j != i:
                            pairs += 1
        self.last_k = pairs / max(1, len(self.pos))


def measure(n, crowd, ticks=5):
    """Mean ms per tick and mean k for a World(n, crowd=crowd). Provided."""
    w = World(n, crowd=crowd)
    w.tick()                                             # warm-up
    t0 = time.perf_counter()
    ks = []
    for _ in range(ticks):
        w.tick()
        ks.append(w.last_k)
    return (time.perf_counter() - t0) * 1000 / ticks, sum(ks) / len(ks)


# ---------------------------------------------------------------- command line

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lecture", action="store_true")
    ap.add_argument("--measure", metavar="CSV")
    ap.add_argument("--fit", metavar="CSV")
    args = ap.parse_args()
    if args.lecture:
        c = tick_cost(1, 0.005, 0.0002, 3000, 50)
        print(f"c = {c:.1f} ms, T_max(0.6) = {t_max(c):.2f} Hz")
        for rate in (1, 2, 5, 10, 13, 20, 30):
            print(f"T={rate:>3}  u={utilization(c, rate):6.1%}")
        for rate in (1, 1 / 0.6, 5, 10, 50, 128):
            print(f"T={rate:6.3f}  wait={500 / rate:6.1f} ms  1.2 s timer={timer_length(1.2, rate):.3f} s"
                  f"  P(same, 100 ms)={same_tick_probability(0.1, rate):.1%}")
        print("multi-rate:", multirate_cpu_per_second(1, 0.005, 0.0002, 1400, 50, 1600, 10), "ms/s")
    if args.measure:
        with open(args.measure, "w", newline="") as f:
            out = csv.writer(f)
            out.writerow(["n", "crowd", "k", "c_ms"])
            for n in (500, 1000, 2000, 3000):
                for crowd in (0, n // 4, n // 2):
                    c, k = measure(n, crowd)
                    out.writerow([n, crowd, f"{k:.2f}", f"{c:.3f}"])
                    print(f"n={n:<5} crowd={crowd:<5} k={k:7.2f}  c={c:8.2f} ms")
    if args.fit:
        with open(args.fit) as f:
            rows = [(int(r["n"]), float(r["k"]), float(r["c_ms"])) for r in csv.DictReader(f)]
        a, d, e = fit_costs(rows)
        print(f"a = {a:.3f} ms, d = {d * 1000:.3f} us, e = {e * 1000:.4f} us")
        c = tick_cost(a, d, e, 3000, 50)
        print(f"lecture zone (n=3000, k=50) on this machine: c = {c:.1f} ms, T_max = {t_max(c):.2f} Hz")


if __name__ == "__main__":
    main()
