"""MMO302 lab 06: movement validators (week 6 lecture).

Run:
    python validators.py --cheat      # sustained factor and blink for each check
    python validators.py --stalls     # corrected stalls per hour against the tolerance

Standard library only. Fill in the three check classes marked TODO, then run test_validators.py.
Each check sees packets in server arrival order: check(t, d) with t the arrival time in seconds
and d the distance the client claims it moved since its previous packet. Return True to accept.
Rejected moves must not change the check's state (no credit spent, nothing added to history).
"""
import argparse
import copy
import random

V = 7.0      # legal speed, m/s
DT = 0.1     # client send interval, s


class PerPacket:
    """Accept d if d <= v * (gap + slack), gap = arrival time since the previous packet.
    The first packet is always accepted."""

    def __init__(self, v=V, slack=0.25, dt=DT):
        self.v, self.slack = v, slack
        self.last = None

    def check(self, t, d):
        # TODO: write this (see the docstring and the lecture).
        raise NotImplementedError


class SlidingWindow:
    """Accept d if (sum of accepted distances that arrived in (t - W, t]) + d <= v * (W + slack)."""

    def __init__(self, v=V, slack=0.25, dt=DT, window=5.0):
        self.v, self.slack, self.window = v, slack, window
        self.history = []    # (arrival time, accepted distance)

    def check(self, t, d):
        # TODO: write this (see the docstring and the lecture).
        raise NotImplementedError


class TokenBucket:
    """credit = min(C, credit + v * gap) with C = v * (dt + slack), starting full.
    Accept d if d <= credit, then subtract it."""

    def __init__(self, v=V, slack=0.25, dt=DT):
        self.v = v
        self.cap = v * (dt + slack)
        self.credit = self.cap
        self.last = None

    def check(self, t, d):
        # TODO: write this (see the docstring and the lecture).
        raise NotImplementedError


CHECKS = {"per-packet": PerPacket, "window": SlidingWindow, "bucket": TokenBucket}


# ---------------------------------------------------------------- traces and measurements (provided)

def cheater_trace(factor, seconds=60, v=V, dt=DT, latency=0.04):
    """A cheater sending on schedule, each packet claiming factor * v * dt metres."""
    return [(i * dt + latency, factor * v * dt) for i in range(int(seconds / dt))]


def rejections(check, trace):
    return sum(0 if check.check(t, d) else 1 for t, d in trace)


def max_sustained_factor(make, step=0.01, top=10.0):
    """Largest cheat factor with zero rejections over 60 s."""
    best, f = 1.0, 1.0
    while f <= top:
        if rejections(make(), cheater_trace(f)) == 0:
            best = f
        f = round(f + step, 10)
    return best


def max_blink(make, idle=10.0, v=V, dt=DT):
    """Largest single move accepted after standing still for `idle` seconds (1 cm resolution)."""
    chk = make()
    for i in range(int(idle / dt)):
        chk.check(i * dt, 0.0)
    lo, hi = 0.0, 500.0
    while hi - lo > 0.005:
        mid = (lo + hi) / 2
        if copy.deepcopy(chk).check(idle, mid):
            lo = mid
        else:
            hi = mid
    return round(lo, 2)


def honest_trace(seconds=3600, stalls_per_minute=1.0, jmin=0.2, jmax=0.8, v=V, dt=DT, seed=3):
    """An honest player at full speed. Stalls (uniform jmin..jmax seconds) hold packets and
    release them together. Returns (trace, list of stall start times)."""
    rnd = random.Random(seed)
    out, stalls, hold_until = [], [], -1.0
    for i in range(int(seconds / dt)):
        send = i * dt
        if send > hold_until and rnd.random() < stalls_per_minute / 60 * dt:
            hold_until = send + rnd.uniform(jmin, jmax)
            stalls.append(send)
        out.append((max(send, hold_until) + 0.04 + rnd.expovariate(1 / 0.005), v * dt))
    out.sort()
    return out, stalls


def corrected_stalls(check, trace):
    """Number of correction events: rejections more than 1 s apart count as separate events."""
    events, last = 0, -9.0
    for t, d in trace:
        if not check.check(t, d):
            if t - last > 1.0:
                events += 1
            last = t
    return events


def predicted_corrections(slack, stalls_per_minute=1.0, jmin=0.2, jmax=0.8):
    """Lecture formula: 60 * f * clamp((jmax - s) / (jmax - jmin), 0, 1) per hour."""
    return 60 * stalls_per_minute * max(0.0, min(1.0, (jmax - slack) / (jmax - jmin)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cheat", action="store_true")
    ap.add_argument("--stalls", action="store_true")
    args = ap.parse_args()
    if args.cheat:
        for name, cls in CHECKS.items():
            print(f"{name:<11} sustained {max_sustained_factor(cls):.2f}x   blink {max_blink(cls):.2f} m")
    if args.stalls:
        trace, stalls = honest_trace()
        print(f"{len(stalls)} stalls in one hour")
        for s in (0.25, 0.5, 0.8):
            row = [corrected_stalls(cls(slack=s), trace) for cls in CHECKS.values()]
            print(f"s={s:.2f}  per-packet {row[0]:>3}  window {row[1]:>3}  bucket {row[2]:>3}"
                  f"   formula {predicted_corrections(s):.0f}")


if __name__ == "__main__":
    main()
