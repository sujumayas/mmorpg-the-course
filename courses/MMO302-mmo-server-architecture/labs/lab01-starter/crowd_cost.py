"""MMO302 lab 01: the crowd cost model from the week 1 lecture.

Run:
    python crowd_cost.py --table            # reproduce the lecture's table
    python crowd_cost.py --sweep out.csv    # crowd sizes 25..4000 to CSV
    python crowd_cost.py --measure          # time one delivery on this machine
    python crowd_cost.py --break-tick       # largest crowd that fits a 100 ms tick

Standard library only.
"""
import argparse
import csv
import math
import struct
import time

ZONES = 400
SERVERS = 20


def deliveries(groups, u):
    """Deliveries per second for a list of group sizes: u * sum(g * (g - 1))."""
    # TODO: write this (see the docstring and the lecture).
    raise NotImplementedError


def layout(n, c, zones=ZONES):
    """Zone populations. Zone 0 holds the crowd c. The other n - c players are
    spread over zones 1..zones-1; when the split is not exact, the
    lowest-numbered zones get one extra player each."""
    # TODO: write this (see the docstring and the lecture).
    raise NotImplementedError


def per_server(pops, u, servers=SERVERS):
    """(players, deliveries) lists, one entry per server. Zone i runs on server i % servers."""
    # TODO: write this (see the docstring and the lecture).
    raise NotImplementedError


def c_max(budget, u):
    """Largest integer c with u * c * (c - 1) <= budget."""
    # TODO: write this (see the docstring and the lecture).
    raise NotImplementedError


def tick_ms(players, deliveries_per_s, tick_hz=10, fixed=2.0, per_player=0.05, per_delivery=0.001):
    """Tick time in ms: fixed + per_player * players + per_delivery * deliveries per tick."""
    # TODO: write this (see the docstring and the lecture).
    raise NotImplementedError


# ---- provided below this line -------------------------------------------

def scenario(n, c, u):
    pops = layout(n, c)
    players, dels = per_server(pops, u)
    return {"c": c, "p0": players[0], "p1": players[1], "d0": dels[0],
            "d1": dels[1], "world": sum(dels)}


def print_table(n=10_000, u=5):
    base = scenario(n, n // ZONES, u)["world"]
    print(f"{'crowd':>6} {'p0':>6} {'p1':>6} {'d0/s':>12} {'d1/s':>9} {'world/s':>12} {'x base':>7}")
    for c in (25, 250, 500, 1000, 2670):
        s = scenario(n, c, u)
        print(f"{c:>6} {s['p0']:>6} {s['p1']:>6} {s['d0']:>12,} {s['d1']:>9,} "
              f"{s['world']:>12,} {s['world'] / base:>7.2f}")


def sweep(path, n=10_000, u=5):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["crowd", "server0_players", "server0_deliveries", "server1_deliveries",
                    "world_deliveries", "server0_tick_ms"])
        for c in list(range(25, 1000, 25)) + list(range(1000, 4001, 100)):
            s = scenario(n, c, u)
            w.writerow([c, s["p0"], s["d0"], s["d1"], s["world"],
                        round(tick_ms(s["p0"], s["d0"]), 2)])
    print(f"wrote {path}")


def measure(recipients=1000, updates=200):
    """Time how long one delivery takes here: pack a 24-byte position update
    and append it to each recipient's outgoing buffer."""
    buffers = [bytearray() for _ in range(recipients)]
    fmt = struct.Struct("<IfffHH")  # entity id, x, y, z, heading, flags
    start = time.perf_counter()
    for k in range(updates):
        msg = fmt.pack(k, 1.0 * k, 2.0, 3.0, k & 0xFFFF, 0)
        for b in buffers:
            b += msg
    elapsed = time.perf_counter() - start
    per = elapsed / (recipients * updates)
    print(f"{recipients * updates:,} deliveries in {elapsed:.3f} s -> {per * 1e6:.3f} us each, "
          f"budget B about {1 / per:,.0f} deliveries/s per core")
    return per


def break_tick(n=10_000, u=5, limit_ms=100.0):
    last = None
    for c in range(25, n + 1):
        s = scenario(n, c, u)
        if tick_ms(s["p0"], s["d0"]) > limit_ms:
            print(f"largest crowd that fits {limit_ms} ms: {last}; {c} overruns")
            return last
        last = c


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--table", action="store_true")
    ap.add_argument("--sweep")
    ap.add_argument("--measure", action="store_true")
    ap.add_argument("--break-tick", action="store_true")
    a = ap.parse_args()
    if a.table:
        print_table()
    if a.sweep:
        sweep(a.sweep)
    if a.measure:
        measure()
    if a.break_tick:
        break_tick()
    if not any([a.table, a.sweep, a.measure, a.break_tick]):
        ap.print_help()
