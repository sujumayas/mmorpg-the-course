"""MA102 lab 10 starter: design a bad-luck protection rule.

Run it as a script (python lab10_starter.py) or paste the sections into a
notebook. Keep this file: the week 11 Monte Carlo lab reuses it.

What you write:
    prd_gap_dist(C)
    pity_gap_dist(base, soft_start, step, hard)
    mean_sd(dist)
    solve_C(p)

Spreadsheet version: build it yourself with one row per attempt and
columns for the per-attempt chance, survival and landing probability.
Do the bisection by hand with a goal-seek cell on C.
"""
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(1010)  # step 5


def prd_gap_dist(C):
    """Exact gap distribution under PRD, p_n = min(1, C * n).

    Return a list whose entry n - 1 is P(first proc on attempt n).
    The list ends at the first attempt where C * n >= 1, so it sums to 1.
    """
    raise NotImplementedError("Write prd_gap_dist (step 1).")


def pity_gap_dist(base, soft_start, step, hard):
    """Exact gap distribution under a soft-and-hard pity rule.

    p_n = base                                  for n < soft_start
    p_n = base + step * (n - soft_start + 1)    for soft_start <= n < hard
    p_hard = 1
    (cap p_n at 1). With step = 0 this is hard pity only.
    Return a list whose entry n - 1 is P(first success on attempt n),
    of length `hard`.
    """
    raise NotImplementedError("Write pity_gap_dist (step 4).")


def mean_sd(dist):
    """Mean and standard deviation of a gap distribution.

    `dist` is a list where entry n - 1 is P(gap = n). Return (mean, sd).
    """
    raise NotImplementedError("Write mean_sd (step 1).")


def solve_C(p):
    """Find the PRD constant C for nominal rate p by bisection on [0, p].

    Choose C so that the mean gap of prd_gap_dist(C) equals 1 / p.
    Return C. Count your bisection steps for step 2.
    """
    raise NotImplementedError("Write solve_C (step 2).")


if __name__ == "__main__":
    try:
        dist = prd_gap_dist(0.084744)
        m, s = mean_sd(dist)
        print(f"PRD 25%: mean {m:.2f} (4.00), SD {s:.2f} (1.90), longest gap {len(dist)} (12)")
        for p in (0.10, 0.20, 0.30, 0.50):
            print(f"p = {p:.2f}  C = {solve_C(p):.6f}")
        hard = pity_gap_dist(0.006, 90, 0, 90)
        soft = pity_gap_dist(0.006, 74, 0.06, 90)
        print(f"Hard pity 90: {mean_sd(hard)[0]:.2f} (69.70)  "
              f"Soft 74 +6%: {mean_sd(soft)[0]:.2f} (62.30)")
        plt.bar(range(1, len(dist) + 1), dist)
        plt.xlabel("gap n")
        plt.ylabel("P(gap = n)")
        plt.show()
    except NotImplementedError as e:
        print(f"TODO: {e}")
