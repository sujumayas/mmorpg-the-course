"""MMO307 Lab 01: gear chase simulator.

Standard-library Python. Fill in every function marked TODO, then run
    python test_gear_chase.py
until all tests pass. Notation follows the week 1 lecture:
S slots, k filled, m options per reward, q tokens per item, c tokens per run,
d chance that a run gives a random drop.
"""
import math
import random


def upgrade_chance(k, S, m=1):
    """Chance that a reward offering m random items (uniform over S slots,
    independent) holds at least one item for an empty slot, when k slots
    are filled. Lecture section 2: 1 - (k/S)^m."""
    raise NotImplementedError("upgrade_chance")


def expected_runs(S, m=1):
    """Expected runs to fill all S slots: sum over k of 1 / upgrade_chance(k, S, m)."""
    raise NotImplementedError("expected_runs")


def finish_cdf(S, m=1, n_max=200):
    """Exact distribution of the finish run as a list: element n-1 is the
    probability that the set is complete after n runs.
    Hint: keep a probability vector over k = 0..S and update it once per run."""
    raise NotImplementedError("finish_cdf")


def percentile_run(S, q, m=1, n_max=500):
    """Smallest n with P(done by run n) >= q (use a tolerance of 1e-12)."""
    raise NotImplementedError("percentile_run")


def token_runs(S, q, c):
    """Runs to fill S slots when each run pays c tokens and each item costs q."""
    raise NotImplementedError("token_runs")


def simulate_hybrid(S, q, c, d=1.0, players=10_000, seed=7):
    """Return a list with each simulated player's finish run.

    Each run: with probability d the player gets a random slot's item
    (useful only if that slot is empty); then the player gains c tokens
    and, while holding at least q tokens with a slot still empty, buys an
    empty slot. Use random.Random(seed) so results are reproducible."""
    raise NotImplementedError("simulate_hybrid")


if __name__ == "__main__":
    S = 10
    print("expected runs, single drops:", round(expected_runs(S), 2))
    print("median / 90th / 99th:", [percentile_run(S, x) for x in (0.5, 0.9, 0.99)])
