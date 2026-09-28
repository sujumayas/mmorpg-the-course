"""MMO302 lab 11 starter: a bot fleet that load tests server.py.

Start the server in one terminal:   python server.py
Run a ramp in another terminal:     python bots.py --ramp 200 400 600 800 900 950
Compare the two bot styles:         python bots.py --ramp 900 1200 --closed

You write three small functions marked TODO. The network code is done.
Tests: python -m unittest test_bots.py
"""
import argparse
import asyncio
import math
import random
import time

RATE = 0.5          # requests per second per bot (one action every 2 s)
CONNECTIONS = 50    # bots share connections, the way a load-test agent multiplexes them


def percentile(values, p):
    """p-th percentile (0 <= p <= 1) with the MA102 week 12 rule.

    Sort the values. Position h = (n - 1) * p + 1 (1-based). Interpolate linearly
    between the values at floor(h) and floor(h) + 1. Raise ValueError on an empty list.
    """
    # TODO
    raise NotImplementedError("percentile")


def poisson_schedule(rate, duration, rng):
    """Send times in [0, duration) for one open-loop bot, as a sorted list.

    Gaps between sends are independent exponential draws, rng.expovariate(rate).
    The first send happens after the first gap, not at time 0.
    """
    # TODO
    raise NotImplementedError("poisson_schedule")


def find_knee(results, slo_ms):
    """results: list of (bots, p99_ms) in increasing bot order.

    Return the largest bot count whose p99 is at or under slo_ms, provided every
    smaller step also met it. Return None if even the first step misses the SLO.
    """
    # TODO
    raise NotImplementedError("find_knee")


# ---------------------------------------------------------------- network code

async def _open_conn(port):
    reader, writer = await asyncio.open_connection("127.0.0.1", port)
    return reader, writer


async def run_open(bots, duration, port, seed=1):
    """Open loop: every bot sends on its own schedule, replies or not.
    Latency is measured from the time the request SHOULD have been sent."""
    rng = random.Random(seed)
    conns = [await _open_conn(port) for _ in range(CONNECTIONS)]
    pending = [dict() for _ in conns]        # request id -> intended send time
    latencies = []
    t0 = time.perf_counter()

    async def reader_task(i):
        reader = conns[i][0]
        while True:
            line = await reader.readline()
            if not line:
                return
            intended = pending[i].pop(line.strip().decode(), None)
            if intended is not None:
                latencies.append(time.perf_counter() - intended)

    async def bot(b):
        i = b % CONNECTIONS
        writer = conns[i][1]
        for k, t in enumerate(poisson_schedule(RATE, duration, rng)):
            intended = t0 + t
            await asyncio.sleep(max(0.0, intended - time.perf_counter()))
            rid = f"{b}-{k}"
            pending[i][rid] = intended
            writer.write(rid.encode() + b"\n")

    readers = [asyncio.create_task(reader_task(i)) for i in range(CONNECTIONS)]
    await asyncio.gather(*(bot(b) for b in range(bots)))
    await asyncio.sleep(2.0)                 # grace period for late replies
    unanswered = sum(len(p) for p in pending)
    for _, w in conns:
        w.close()
    for r in readers:
        r.cancel()
    return latencies, unanswered


async def run_closed(bots, duration, port, seed=1):
    """Closed loop: each bot waits for its reply, then thinks, then sends again.
    Each shared connection carries one request at a time, and latency is measured
    from the actual send. This hides queueing (lecture section 3)."""
    rng = random.Random(seed)
    conns = [await _open_conn(port) for _ in range(CONNECTIONS)]
    locks = [asyncio.Lock() for _ in conns]
    latencies = []
    t_end = time.perf_counter() + duration

    async def bot(b):
        i, k = b % CONNECTIONS, 0
        while True:
            await asyncio.sleep(rng.expovariate(RATE))      # think time
            if time.perf_counter() >= t_end:
                return
            async with locks[i]:
                reader, writer = conns[i]
                start = time.perf_counter()
                writer.write(f"{b}-{k}\n".encode())
                await reader.readline()
            latencies.append(time.perf_counter() - start)
            k += 1

    await asyncio.gather(*(bot(b) for b in range(bots)))
    for _, w in conns:
        w.close()
    return latencies, 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ramp", type=int, nargs="+", default=[200, 400, 600, 800, 900, 950])
    ap.add_argument("--seconds", type=float, default=20.0)
    ap.add_argument("--port", type=int, default=9302)
    ap.add_argument("--slo-ms", type=float, default=100.0)
    ap.add_argument("--closed", action="store_true", help="use closed-loop bots")
    a = ap.parse_args()
    run = run_closed if a.closed else run_open
    results = []
    print(f"{'bots':>5} {'offered/s':>9} {'done/s':>7} {'p50 ms':>8} {'p99 ms':>9} {'unanswered':>10}")
    for bots in a.ramp:
        lat, lost = asyncio.run(run(bots, a.seconds, a.port))
        p50, p99 = percentile(lat, 0.5) * 1000, percentile(lat, 0.99) * 1000
        results.append((bots, p99))
        print(f"{bots:>5} {bots * RATE:>9.0f} {len(lat) / a.seconds:>7.0f} "
              f"{p50:>8.1f} {p99:>9.1f} {lost:>10}", flush=True)
    print("knee (last step within SLO):", find_knee(results, a.slo_ms))


if __name__ == "__main__":
    main()
