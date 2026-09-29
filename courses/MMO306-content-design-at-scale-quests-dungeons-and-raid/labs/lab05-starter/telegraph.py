"""MMO306 Lab 05: telegraph tuning from measured data.

Finish every function marked TODO, then run `python test_telegraph.py`.
Standard-library Python only (statistics.NormalDist is allowed and useful).
All times are in milliseconds.
"""
import csv
from pathlib import Path
from statistics import NormalDist

DATA = Path(__file__).with_name("reaction_times.csv")


def load_times(path=DATA):
    """Return the needed_ms column as a list of ints, in file order."""
    with open(path, newline="") as f:
        return [int(row["needed_ms"]) for row in csv.DictReader(f)]


def fit_normal(times):
    """Return (mean, sample standard deviation) of the times."""
    raise NotImplementedError("fit_normal")


def p_normal(T_tel, mu, sigma):
    """Chance one player responds in time under the normal model: Phi((T - mu) / sigma)."""
    raise NotImplementedError("p_normal")


def p_empirical(T_tel, times):
    """Share of measured responses that are at or below T_tel."""
    raise NotImplementedError("p_empirical")


def p_clean(p, N, k):
    """Chance of a clean pull: p ** (N * k)."""
    raise NotImplementedError("p_clean")


def expected_misses(p, N, k):
    """Expected failures per pull when a miss is not a wipe: N * k * (1 - p)."""
    raise NotImplementedError("expected_misses")


def required_normal(target, N, k, mu, sigma):
    """Telegraph length giving clean-pull chance `target` under the normal model."""
    raise NotImplementedError("required_normal")


def required_empirical(target, N, k, times):
    """Smallest measured value T such that p_empirical(T) >= target ** (1 / (N * k)).
    With few samples this is often the slowest value in the data set: 400 samples
    cannot tell you about a 1-in-2,000 response."""
    raise NotImplementedError("required_empirical")


def shift(times, rtt_ms):
    """Add a network round trip to every measured time (lecture section 4)."""
    raise NotImplementedError("shift")


if __name__ == "__main__":
    t = load_times()
    mu, sd = fit_normal(t)
    print(f"n={len(t)} mean={mu:.1f} sd={sd:.1f}")
    for T in (1000, 1100, 1200):
        print(T, round(p_normal(T, mu, sd), 4), p_empirical(T, t))
