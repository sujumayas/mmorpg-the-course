"""MMO308 Lab 06: peeking, stopping boundaries and a sample ratio check.

Run:  python gen_experiment.py   # once, writes experiment_daily.csv
      python peeking.py          # prints your analysis
      python check_lab06.py      # PASS / FAIL / TODO per function

Standard library only. Fill in every function that raises NotImplementedError.
"""
import csv
import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent


def z_two_proportion(k_a, n_a, k_b, n_b):
    """Pooled two-proportion z for B minus A (MA102 week 14). Return 0.0 if SE is 0."""
    raise NotImplementedError


def cumulative_z(rows):
    """rows: list of (day, n_a, conv_a, n_b, conv_b), one per day, in day order.
    Return the list of z values computed on the CUMULATIVE counts after each day."""
    raise NotImplementedError


def srm_pvalue(n_a, n_b, share_b=0.5):
    """Chi-square goodness-of-fit p-value (1 degree of freedom) for the observed
    split against the planned share of B. Use p = math.erfc(math.sqrt(chi2 / 2))."""
    raise NotImplementedError


def obf_boundaries(c, K):
    """O'Brien-Fleming boundaries for K equally spaced looks: c * sqrt(K / k), k = 1..K."""
    raise NotImplementedError


def stop_rate(boundaries, sims=20_000, seed=6, theta=0.0):
    """Simulate `sims` tests with len(boundaries) equally spaced looks.
    Each look adds random.gauss(0, 1) + theta / sqrt(K) to a running total S;
    z_k = S / sqrt(k). A test stops at the first k with |z_k| > boundaries[k-1].
    Use one random.Random(seed) for the whole run.
    Return the share of tests that stopped (the false-positive rate when theta = 0,
    the power otherwise)."""
    raise NotImplementedError


def find_constant(K, kind, sims=20_000, seed=6, alpha=0.05):
    """Find the constant c that gives stop_rate = alpha under theta = 0, by bisection
    on [1.5, 6.0] for 30 steps, reusing the same seed at every step.
    kind 'pocock': boundaries [c] * K.  kind 'obf': obf_boundaries(c, K)."""
    raise NotImplementedError


def load_rows():
    with open(HERE / "experiment_daily.csv") as f:
        return [(int(r["day"]), int(r["n_a"]), int(r["conv_a"]), int(r["n_b"]), int(r["conv_b"]))
                for r in csv.DictReader(f)]


def main():
    try:
        for K in (1, 5, 14):
            print(f"peeking with {K:>2} looks: false-positive rate {stop_rate([1.96] * K):.1%}")
        rows = load_rows()
        zs = cumulative_z(rows)
        c = find_constant(len(rows), "obf")
        bounds = obf_boundaries(c, len(rows))
        for (day, *_), z, b in zip(rows, zs, bounds):
            flag = " naive stop" if abs(z) > 1.96 else ""
            flag += " OBF stop" if abs(z) > b else ""
            print(f"day {day:>2}: z {z:6.2f}  OBF bound {b:5.2f}{flag}")
        na = sum(r[1] for r in rows)
        nb = sum(r[3] for r in rows)
        print(f"split A {na} / B {nb}: SRM p = {srm_pvalue(na, nb):.5f}")
    except NotImplementedError:
        print("TODO: finish the functions, then rerun")


if __name__ == "__main__":
    main()
