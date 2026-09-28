"""CS202 Lab 14: an offline, seeded network conditioner and the statistics to check it.

    python conditioner.py --check      # tests your functions and the week 14 formula

The same seed always gives the same losses, delays and duplicates, so any failure a test
finds can be replayed exactly. Implement every function marked TODO. The model is in the
week 14 lecture, sections 2 and 3. Standard library only.
"""
import math
import random
import statistics
import sys


class GilbertLoss:
    """Two-state burst loss: average loss rate p, P(loss | previous packet lost) = q.
    Independent loss is q = p."""

    def __init__(self, p, q, rng):
        self.rng = rng
        self.q = q
        self.a = p * (1 - q) / (1 - p) if p < 1 else 1.0  # P(loss | previous delivered)
        self.lost = False

    def drop(self):
        """Return True if this packet is lost, and remember the answer for the next call.
        Lost with probability q if the previous packet was lost, else with probability a. TODO."""
        raise NotImplementedError


class Conditioner:
    """One direction of a bad network. Given: delay, uniform jitter, loss and duplicates."""

    def __init__(self, delay_ms=0.0, jitter_ms=0.0, p=0.0, q=None, dup=0.0, seed=1):
        self.rng = random.Random(seed)
        self.delay, self.jitter, self.dup = delay_ms, jitter_ms, dup
        self.loss = GilbertLoss(p, p if q is None else q, self.rng) if p > 0 else None

    def one_way_ms(self):
        """netem style: delay +/- jitter, uniform."""
        return self.delay + self.rng.uniform(-self.jitter, self.jitter)

    def run(self, send_times_ms):
        """Return (arrivals, lost_flags). arrivals is a list of (arrive_ms, seq) sorted by
        arrival time; lost_flags[i] is True if packet i was dropped."""
        arrivals, lost = [], []
        for seq, t in enumerate(send_times_ms):
            is_lost = self.loss.drop() if self.loss else False
            lost.append(is_lost)
            if is_lost:
                continue
            arrivals.append((t + self.one_way_ms(), seq))
            if self.dup and self.rng.random() < self.dup:
                arrivals.append((t + self.one_way_ms(), seq))
        arrivals.sort()
        return arrivals, lost


def burst_lengths(lost_flags):
    """Lengths of every run of consecutive True values, in order.
    burst_lengths([F, T, T, F, T]) == [2, 1]. TODO."""
    raise NotImplementedError


def reorder_count(arrival_seqs):
    """Number of arrivals whose seq is lower than some seq that arrived before it.
    reorder_count([0, 2, 1, 3]) == 1. Duplicates of an already-seen seq count too. TODO."""
    raise NotImplementedError


def bursts_per_minute(p, q, k, rate_hz):
    """The lecture's lambda: 60 * r * p * (1 - q) * q**(k - 1). TODO."""
    raise NotImplementedError


def minutes_to_first_burst(p, q, k, rate_hz, seed, limit_min=600):
    """Simulate packets until the first burst of >= k losses ends its k-th packet. Given."""
    loss = GilbertLoss(p, q, random.Random(seed))
    run = 0
    for i in range(int(limit_min * 60 * rate_hz)):
        run = run + 1 if loss.drop() else 0
        if run >= k:
            return (i + 1) / (60 * rate_hz)
    return None


def check():
    ok = True

    def expect(name, got, want, tol):
        nonlocal ok
        good = abs(got - want) <= tol
        ok &= good
        print(f"{'ok  ' if good else 'FAIL'} {name}: got {got:.5g}, want {want:.5g} +/- {tol:g}")

    expect("burst_lengths", len(burst_lengths([False, True, True, False, True])), 2, 0)
    expect("burst_lengths sum", sum(burst_lengths([True, True, False, True, True, True])), 5, 0)
    expect("reorder_count", reorder_count([0, 2, 1, 3, 3]), 2, 0)
    expect("lambda bursty 1%", bursts_per_minute(0.01, 0.5, 3, 30), 2.25, 1e-9)
    expect("lambda indep 3%", bursts_per_minute(0.03, 0.03, 3, 30), 0.047142, 1e-5)

    c = Conditioner(p=0.01, q=0.5, seed=14)
    _, lost = c.run([i * 1000 / 30 for i in range(1_000_000)])
    b = burst_lengths(lost)
    expect("measured loss rate", sum(lost) / len(lost), 0.01, 0.001)
    expect("measured mean burst", statistics.mean(b), 2.0, 0.1)

    c = Conditioner(delay_ms=100, jitter_ms=20, seed=3)
    arr, _ = c.run([i * 1000 / 60 for i in range(100_000)])
    seqs = [s for _, s in arr]
    # adjacent inversions in arrival order are close to, not equal to, the pair formula
    expect("reordered share at 60 Hz, +/-20 ms", reorder_count(seqs) / len(seqs), 0.17, 0.05)

    waits = sorted(minutes_to_first_burst(0.01, 0.5, 3, 30, seed) for seed in range(200))
    lam = bursts_per_minute(0.01, 0.5, 3, 30)
    expect("median first burst (min)", waits[100], math.log(2) / lam, 0.05)
    print("all checks passed" if ok else "some checks failed")
    return ok


if __name__ == "__main__":
    sys.exit(0 if check() else 1)
