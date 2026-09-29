"""MMO308 Lab 05: experiment design helpers.

Run:  python gen_servers.py     # once
      python design.py          # prints the design table from your functions
      python check_lab05.py     # PASS / FAIL / TODO per function

Standard library only. Fill in every function that raises NotImplementedError.
"""
import csv
import hashlib
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
Z_ALPHA = 1.96        # two-sided, alpha = 0.05
Z_BETA = 0.8416       # 80% power


def bucket(unit_id, experiment):
    """SHA-256 of the UTF-8 string f"{experiment}:{unit_id}". Take the first
    8 bytes of the digest as a big-endian unsigned integer and divide by 2**64.
    Return a float in [0, 1)."""
    raise NotImplementedError


def variant(unit_id, experiment, share_b=0.5):
    """'B' if bucket(unit_id, experiment) < share_b, else 'A'."""
    raise NotImplementedError


def design_effect(m, rho):
    """Kish design effect for clusters of average size m and intraclass correlation rho."""
    raise NotImplementedError


def effective_n(n, m, rho):
    """Effective number of independent players in an arm of n players in clusters of size m."""
    raise NotImplementedError


def mde(p, n_eff):
    """Minimum detectable difference in a rate (as a proportion, not points) for
    baseline p, n_eff effective players per arm, alpha 0.05 two-sided, 80% power:
    (Z_ALPHA + Z_BETA) * sqrt(2 p (1 - p) / n_eff)."""
    raise NotImplementedError


def icc_from_clusters(sizes, successes):
    """Estimate the intraclass correlation of a 0/1 metric from per-cluster counts.
    p_bar  = sum(successes) / sum(sizes)
    rates  = successes[i] / sizes[i]
    var_r  = sample variance of the rates (divide by k - 1)
    noise  = mean over clusters of p_bar (1 - p_bar) / sizes[i]
    sig_b2 = max(0, var_r - noise)
    rho    = sig_b2 / (sig_b2 + p_bar (1 - p_bar))"""
    raise NotImplementedError


def load_history():
    sizes, succ = [], []
    with open(HERE / "server_history.csv") as f:
        for r in csv.DictReader(f):
            sizes.append(int(r["new_players"]))
            succ.append(int(r["d7_retained"]))
    return sizes, succ


def main():
    try:
        sizes, succ = load_history()
        rho = icc_from_clusters(sizes, succ)
        p = sum(succ) / sum(sizes)
        print(f"baseline D7 {p:.4f}, estimated ICC {rho:.5f}")
        n = 100_000
        for unit, m, r in (("player", 1, 0.0), ("guild", 20, 0.05), ("server", 5000, rho)):
            ne = effective_n(n, m, r)
            print(f"{unit:>7}: deff {design_effect(m, r):8.2f}  n_eff {ne:9.0f}  "
                  f"MDE {100 * mde(p, ne):5.2f} points")
    except NotImplementedError:
        print("TODO: finish the functions, then rerun")


if __name__ == "__main__":
    main()
