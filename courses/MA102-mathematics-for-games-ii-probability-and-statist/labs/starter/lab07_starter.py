"""MA102 lab 07 starter: dry streaks at scale.

Run it as a script (python lab07_starter.py) or paste the sections into a
notebook. Every random draw goes through the one seeded generator `rng`,
so your results reproduce.

What you write:
    simulate_first_success(p, players, rng)
    dry_curve(samples, n_max)
    percentile_wait(samples, q)

Spreadsheet version: build it yourself with one row per kill n (0 to 500),
a column for (1 - p)^n, and a second sheet with 1,000 simulated players
using RAND().
"""
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(102)

P_DROP = 0.01      # steps 1 to 5
PLAYERS = 10_000   # use 1,000 in the spreadsheet
N_MAX = 500        # x-axis of the step 3 plot


def simulate_first_success(p, players, rng):
    """Simulate `players` players farming a drop with chance p per kill.

    Return a numpy int array of length `players`. Entry i is the kill
    number (1, 2, 3, ...) on which player i got their first drop.
    Use only `rng` for random draws.
    """
    raise NotImplementedError("Write simulate_first_success (steps 1 and 2).")


def dry_curve(samples, n_max):
    """Share of players still dry after n kills, for n = 0 .. n_max.

    `samples` is the array from simulate_first_success. Return a numpy
    float array of length n_max + 1. Entry n is the share of players whose
    first drop came after kill n (so entry 0 is 1.0).
    Compare it with the exact curve (1 - p)**n.
    """
    raise NotImplementedError("Write dry_curve (step 3).")


def percentile_wait(samples, q):
    """Kill count by which a share q of players have the drop.

    q is a share between 0 and 1 (0.5 for the median, 0.95, 0.99).
    Return the smallest kill count k such that at least q of the samples
    are <= k.
    """
    raise NotImplementedError("Write percentile_wait (step 4).")


if __name__ == "__main__":
    n = np.arange(N_MAX + 1)
    exact = (1 - P_DROP) ** n
    print(f"Exact dry share at n = 69, 100, 299: "
          f"{exact[69]:.4f}, {exact[100]:.4f}, {exact[299]:.4f}")

    try:
        samples = simulate_first_success(P_DROP, PLAYERS, rng)
        sim = dry_curve(samples, N_MAX)
        for k in (69, 100, 299):
            print(f"n = {k:>3}  simulated {sim[k]:.4f}  exact {exact[k]:.4f}")
        for q in (0.5, 0.95, 0.99):
            print(f"q = {q:.2f}  wait {percentile_wait(samples, q)}")
        plt.plot(n, sim, label="simulated")
        plt.plot(n, exact, "--", label="(1 - p)^n")
        plt.xlabel("kills n")
        plt.ylabel("share still dry")
        plt.legend()
        plt.show()
    except NotImplementedError as e:
        print(f"TODO: {e}")
