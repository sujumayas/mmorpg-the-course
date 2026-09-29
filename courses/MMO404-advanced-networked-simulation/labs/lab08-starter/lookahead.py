"""MMO404 lab 08 starter: lookahead on the border between two servers.

    python test_lookahead.py             # checks your functions against the week 8 lecture
    python lookahead.py --pattern        # section 2: the out-of-phase table
    python lookahead.py --random         # section 2: seeded random ticks, L = 1..8
    python lookahead.py --smallest       # smallest L within 5% for delays 0..100 ms
    python lookahead.py --abilities      # border lookahead of the lecture's ability table

Implement every function marked TODO. The model is in the week 8 lecture, section 2.
Standard library only.
"""
import math
import sys

TICK_MS = 50.0   # 20 Hz


def mulberry32(seed):
    """Seeded generator shared with the week 8 interactive. Given."""
    s = seed & 0xFFFFFFFF

    def rnd():
        nonlocal s
        s = (s + 0x6D2B79F5) & 0xFFFFFFFF
        t = ((s ^ (s >> 15)) * (s | 1)) & 0xFFFFFFFF
        t ^= (t + (((t ^ (t >> 7)) * (t | 61)) & 0xFFFFFFFF)) & 0xFFFFFFFF
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296
    return rnd


def random_ticks(n=10_000, lo=30.0, hi=70.0, seed=404):
    """Tick times for A then B, as in the lecture: A's n draws first, then B's. Given."""
    rnd = mulberry32(seed)
    xa = [lo + (hi - lo) * rnd() for _ in range(n)]
    xb = [lo + (hi - lo) * rnd() for _ in range(n)]
    return xa, xb


def finish_times(xa, xb, L, delay=0.0):
    """Return (fa, fb), lists of finish times for ticks 1..N:
        F_A(k) = max(F_A(k-1), F_B(k-L) + delay) + X_A(k)   (second term only when k-L >= 1)
    and the same for B. F(0) = 0. TODO."""
    raise NotImplementedError("finish_times")


def effective_tick(xa, xb, L, delay=0.0):
    """Real ms per tick for the pair: max(F_A(N), F_B(N)) / N. TODO."""
    raise NotImplementedError("effective_tick")


def stalls(xa, xb, L, delay=0.0):
    """Total stall time (ms) of (A, B): for each tick, start minus own previous finish,
    counted only when positive. start = finish - own tick time. TODO."""
    raise NotImplementedError("stalls")


def smallest_lookahead(xa, xb, delay, tol=0.05, max_l=32):
    """Smallest L in 1..max_l whose effective tick is within tol of the pair's own pace,
    max(sum(xa), sum(xb)) / N. None if no L up to max_l is. TODO."""
    raise NotImplementedError("smallest_lookahead")


def border_lookahead(delays_s, tick_ms=TICK_MS):
    """Lookahead of a border in ticks: for each interaction's minimum cause-to-effect delay
    (seconds), floor(delay * 1000 / tick_ms + 1e-9), at least 1; return the minimum.
    TODO."""
    raise NotImplementedError("border_lookahead")


ABILITIES = {                       # the lecture's table, minimum delay in seconds
    "melee, next tick": 0.05,
    "arrow, 5 m minimum at 50 m/s": 0.10,
    "walk through a 7 m band at 7 m/s": 1.0,
    "1.5 s cast": 1.5,
}


def show_pattern():
    xa, xb = [40, 60] * 50, [60, 40] * 50
    for L, d in [(1, 0), (2, 0), (1, 20), (2, 20), (2, 60)]:
        fa, fb = finish_times(xa, xb, L, d)
        print(f"L={L} delay={d:2d}  A {fa[:4]}  B {fb[:4]}  per tick {effective_tick(xa, xb, L, d):.1f} ms")


def show_random():
    xa, xb = random_ticks()
    print("L    delay 20 ms   delay 60 ms")
    for L in (1, 2, 3, 4, 6, 8):
        print(f"{L}    {effective_tick(xa, xb, L, 20):8.1f}      {effective_tick(xa, xb, L, 60):8.1f}")


def show_smallest():
    xa, xb = random_ticks()
    print("delay ms   smallest L within 5%")
    for d in range(0, 101, 10):
        print(f"{d:8d}   {smallest_lookahead(xa, xb, d)}")


def show_abilities():
    for name, s in ABILITIES.items():
        print(f"{name:36s} {border_lookahead([s])} ticks")
    print("border:", border_lookahead(list(ABILITIES.values())), "ticks")


if __name__ == "__main__":
    if "--pattern" in sys.argv:
        show_pattern()
    elif "--random" in sys.argv:
        show_random()
    elif "--smallest" in sys.argv:
        show_smallest()
    elif "--abilities" in sys.argv:
        show_abilities()
    else:
        print(__doc__)
