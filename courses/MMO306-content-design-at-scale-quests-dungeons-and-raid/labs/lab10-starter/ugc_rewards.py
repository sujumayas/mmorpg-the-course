"""MMO306 Lab 10 starter: the best-farm model for player-made content.

Fill in every function marked TODO. Standard library only.

    python ugc_rewards.py                       # prints the lecture table once done
    python -m unittest test_ugc_rewards.py      # all tests fail until you write the code

Reward rates are relative to studio content: 1.0 pays like your own
missions, 1.3 pays 30% more. A mission's rate is 1 + X, where X is its
overpay. The lecture uses X ~ Exponential(mean m).
"""
import math
import random


def harmonic(n):
    """H_n = 1 + 1/2 + ... + 1/n. harmonic(10) is about 2.928968."""
    raise NotImplementedError("TODO: harmonic")


def expected_best(n, m, cap=None):
    """Expected best reward rate among n missions with exponential overpay of mean m.

    Formula: 1 + m * H_n. If cap is not None, the best can't exceed cap.
    """
    raise NotImplementedError("TODO: expected_best")


def sample_overpay(m, rng, dist="exponential"):
    """Draw one mission's overpay X.

    "exponential": mean m (use rng.expovariate).
    "uniform":     uniform on [0, 2m], so the mean is also m but the tail is capped.
    Anything else: raise ValueError.
    """
    raise NotImplementedError("TODO: sample_overpay")


def simulate_best(n, m, trials=2000, seed=306, dist="exponential"):
    """Average, over `trials`, of the best rate 1 + max(X_1..X_n).

    Create one random.Random(seed) and use it for every draw, so the same
    seed always gives the same answer.
    """
    raise NotImplementedError("TODO: simulate_best")


def inflow_multiplier(phi, best):
    """Total reward inflow relative to plan when a share phi of play time
    moves to a mission paying `best`: 1 + phi * (best - 1)."""
    raise NotImplementedError("TODO: inflow_multiplier")


def funnel(submissions, pass_rates):
    """Creations left after each gate of a publication funnel.

    funnel(5000, [0.6, 0.3, 0.4]) returns [3000, 900, 360] (floats are fine).
    """
    raise NotImplementedError("TODO: funnel")


def largest_pool(m, target):
    """Largest number of paying missions N whose expected best 1 + m * H_N
    is at or under `target`. Use exact harmonic numbers, not ln N."""
    raise NotImplementedError("TODO: largest_pool")


if __name__ == "__main__":
    try:
        for n in (1, 10, 100, 1_000, 10_000, 100_000):
            print(f"N={n:>7,}  best {expected_best(n, 0.10):.3f}x")
        print("simulated N=1,000:", round(simulate_best(1_000, 0.10, trials=500), 3))
    except NotImplementedError as e:
        print("not done yet:", e)
