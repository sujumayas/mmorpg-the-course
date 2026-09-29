"""MMO404 Lab 10: conflicts and convergence between two servers.

    python consistency.py --check          # tests your functions against the week 10 lecture
    python consistency.py --compare        # formula vs continuous and tick-aligned simulations
    python consistency.py --sweep out.csv  # conflict share for claim rates 0.01 to 10 per second

Implement every function or method marked TODO. The model is in the week 10 lecture,
sections 2 to 4. Standard library only.
"""
import csv
import math
import random
import sys

T = 0.100   # server tick interval in seconds (10 Hz)
D = 0.001   # one-way link delay between servers in seconds


# ---------------------------------------------------------------- part A: forward or guess

def conflict_p(lam, W):
    """Share of guessed claims that conflict: 1 - exp(-2 * lam * W). TODO."""
    raise NotImplementedError


def forward_latency(d, t):
    """(average, worst) latency in seconds that forwarding a claim to the owner adds:
    2d + T on average and 2d + 2T at worst. TODO."""
    raise NotImplementedError


def count_conflicts(a_times, b_times, W):
    """Number of claims in the sorted list a_times that have at least one claim in the
    sorted list b_times within W seconds (inclusive) on either side. Walk both lists once
    (two pointers); do not compare every pair. TODO."""
    raise NotImplementedError


def poisson_arrivals(lam, n, rng):
    """n claim times of a Poisson process with rate lam. Given."""
    t, out = 0.0, []
    for _ in range(n):
        t += rng.expovariate(lam)
        out.append(t)
    return out


def simulate(lam, W, claims=100_000, seed=10):
    """Continuous-time check of conflict_p. Given; uses your count_conflicts."""
    rng = random.Random(seed)
    a, b = poisson_arrivals(lam, claims, rng), poisson_arrivals(lam, claims, rng)
    return count_conflicts(a, b, W) / claims


def simulate_ticked(lam, t=T, d=D, claims=100_000, seed=10, phase_b=0.037):
    """Tick-aligned check. Given.

    Each click is granted the moment it happens. A server sends news of its grants in the
    update it sends at its next tick (A ticks at k*t, B at k*t + phase_b); the update spends
    d on the wire and is applied at the receiver's next tick. Grants x on A and y on B
    conflict if y happened before B applied x, and x happened before A applied y.
    Returns the share of A's grants that conflict."""
    rng = random.Random(seed)

    def next_tick(x, phase):
        return phase + math.ceil((x - phase) / t) * t

    a = poisson_arrivals(lam, claims, rng)
    b = poisson_arrivals(lam, claims, rng)
    a_known = [next_tick(next_tick(x, 0.0) + d, phase_b) for x in a]   # when B applies it
    b_known = [next_tick(next_tick(y, phase_b) + d, 0.0) for y in b]   # when A applies it
    j = hits = 0
    for x, x_known in zip(a, a_known):
        while j < len(b) and b_known[j] <= x:     # A already knew about these
            j += 1
        k = j
        while k < len(b) and b[k] < x_known:
            if b_known[k] > x:
                hits += 1
                break
            k += 1
    return hits / claims


# ---------------------------------------------------------------- part B: convergence

class DamageCounter:
    """Boss damage split by server. Each server only ever raises its own entry."""

    def __init__(self, me, max_hp):
        self.me, self.max_hp, self.parts = me, max_hp, {}

    def hit(self, damage):
        """Add damage dealt by this server's players. TODO."""
        raise NotImplementedError

    def snapshot(self):
        """A copy of the parts to send to other servers. Given."""
        return dict(self.parts)

    def merge(self, remote_parts):
        """Merge another server's snapshot. Must give the same result whatever the order,
        and when a snapshot arrives twice or late. TODO."""
        raise NotImplementedError

    def hp(self):
        """max_hp minus all damage this server knows about. TODO."""
        raise NotImplementedError


class VectorClock:
    """One counter per server. Section 4 of the lecture."""

    def __init__(self, me, servers):
        self.me, self.v = me, {s: 0 for s in servers}

    def event(self):
        """A local event: increment own entry and return a copy of the vector. TODO."""
        raise NotImplementedError

    def receive(self, stamp):
        """A message stamped with `stamp` arrives: take the entry-wise max, then count the
        receive as a local event. Return a copy of the vector. TODO."""
        raise NotImplementedError


def happened_before(x, y):
    """True if vector x happened before vector y: every entry <= and at least one <. TODO."""
    raise NotImplementedError


def concurrent(x, y):
    """True if neither happened before the other and they differ. TODO."""
    raise NotImplementedError


# ---------------------------------------------------------------- tests and tools

def check():
    W = T + D
    assert abs(conflict_p(0.5, W) - 0.0961) < 5e-5, conflict_p(0.5, W)
    assert abs(conflict_p(5, W) - 0.6358) < 5e-5, conflict_p(5, W)
    assert abs(conflict_p(5, D) - 0.0100) < 5e-5
    avg, worst = forward_latency(D, T)
    assert abs(avg - 0.102) < 1e-9 and abs(worst - 0.202) < 1e-9, (avg, worst)

    assert count_conflicts([1.0, 2.0, 3.0], [1.05, 2.5, 3.2], 0.1) == 1
    assert count_conflicts([1.0, 2.0], [0.9, 2.1], 0.1) == 2, "the window is inclusive"
    assert count_conflicts([1.0], [], 0.1) == 0
    rng = random.Random(3)
    a = sorted(rng.uniform(0, 100) for _ in range(300))
    b = sorted(rng.uniform(0, 100) for _ in range(300))
    brute = sum(1 for x in a if any(abs(x - y) <= 0.2 for y in b))
    assert count_conflicts(a, b, 0.2) == brute, "count_conflicts disagrees with brute force"
    for lam in (0.1, 0.5, 2):
        got = simulate(lam, W)
        assert abs(got - conflict_p(lam, W)) < 0.01, f"simulate({lam}) = {got:.4f}"

    a_, b_ = DamageCounter("A", 10_000), DamageCounter("B", 10_000)
    a_.hit(300); s1 = a_.snapshot()
    b_.hit(500); t1 = b_.snapshot()
    a_.hit(200); s2 = a_.snapshot()
    b_.merge(s2); b_.merge(s1); b_.merge(s2)
    a_.merge(t1)
    assert a_.hp() == b_.hp() == 9000, (a_.hp(), b_.hp())
    rng = random.Random(7)
    servers = [DamageCounter(s, 1_000_000) for s in "ABC"]
    mailbox = []
    for _ in range(500):
        s = rng.choice(servers)
        s.hit(rng.randint(1, 900))
        mailbox.append(s.snapshot())
    for s in servers:
        for snap in rng.sample(mailbox, len(mailbox)) + mailbox[:50]:   # shuffled, some twice
            s.merge(snap)
    assert len({s.hp() for s in servers}) == 1, "counters did not converge"

    a_c, b_c, c_c = (VectorClock(s, "ABC") for s in "ABC")
    x = a_c.event()                  # A asks in chat
    b_c.receive(x)
    y = b_c.event()                  # B replies
    z = c_c.event()                  # C does something unrelated
    assert x == {"A": 1, "B": 0, "C": 0} and y == {"A": 1, "B": 2, "C": 0}, (x, y)
    assert happened_before(x, y) and not happened_before(y, x)
    assert concurrent(x, z) and concurrent(y, z) and not concurrent(x, y)
    assert not happened_before(x, x) and not concurrent(x, x)
    print("all checks passed")


def compare():
    print("  lam   formula   continuous   tick-aligned")
    for lam in (0.01, 0.1, 0.5, 2, 5):
        f = conflict_p(lam, T + D)
        n = 200_000 if lam < 0.05 else 100_000
        print(f"{lam:5}   {100 * f:6.2f}%   {100 * simulate(lam, T + D, n):8.2f}%"
              f"   {100 * simulate_ticked(lam, claims=n):10.2f}%")


def sweep(path):
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["lam", "p_tick_aligned", "p_flushed", "p_30hz"])
        for k in range(-20, 11):
            lam = 10 ** (k / 10)
            w.writerow([round(lam, 4), round(conflict_p(lam, T + D), 5),
                        round(conflict_p(lam, D), 5), round(conflict_p(lam, 1 / 30 + D), 5)])
    print("wrote", path)


if __name__ == "__main__":
    if "--check" in sys.argv:
        check()
    elif "--compare" in sys.argv:
        compare()
    elif "--sweep" in sys.argv:
        sweep(sys.argv[sys.argv.index("--sweep") + 1])
    else:
        print(__doc__)
