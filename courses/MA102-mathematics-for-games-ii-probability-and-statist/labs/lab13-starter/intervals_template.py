"""Lab 13 template. Fill in the TODOs; run with `python intervals_template.py`.

Every number you report must be reproducible with seed 13.
"""
import csv
import math

from mulberry32 import Mulberry32

Z = 1.96
SEED = 13


def wald(k: int, n: int) -> tuple[float, float]:
    """Simple 95% interval p_hat +/- 1.96 * SE. Do not clamp to [0, 1]."""
    # TODO: lecture week 13, section 2
    raise NotImplementedError


def wilson(k: int, n: int) -> tuple[float, float]:
    """Wilson score 95% interval."""
    # TODO: lecture week 13, section 3
    raise NotImplementedError


def read_drops(path: str = "drops.csv") -> list[int]:
    with open(path, newline="") as f:
        return [int(row["dropped"]) for row in csv.DictReader(f)]


def growing_sample(drops: list[int]) -> None:
    """Step 2: print n, k, p_hat, se, wald_low, wald_high, wilson_low, wilson_high."""
    for n in (10, 30, 100, 300, 1000, 3000):
        k = sum(drops[:n])
        # TODO: compute and print the row, then plot both intervals against n
        print(n, k)


def coverage(p: float, n: int, method, studies: int, rng: Mulberry32) -> float:
    """Step 3: fraction of simulated studies whose interval contains p."""
    # TODO: simulate `studies` studies of size n at rate p
    raise NotImplementedError


if __name__ == "__main__":
    drops = read_drops()
    growing_sample(drops)
    rng = Mulberry32(SEED)
    # Step 3 grid (the `coverage` tab):
    # for p in (0.02, 0.10, 0.50, 0.80):
    #     for n in (5, 20, 100, 1000):
    #         print(p, n, coverage(p, n, wald, 2000, rng), coverage(p, n, wilson, 2000, rng))
