"""MMO405 lab 13: power, the significance filter, and five replication criteria.

Python 3, standard library only. Fill in the three TODOs, then run
    python -m unittest test_replication.py
from inside this folder (from the repository root, .venv/bin/python is the course Python).
Running this file directly prints the audit table for pairs.csv once the TODOs are done.

Conventions (lecture week 13): d is Cohen's d, n is players PER GROUP, SE(d) = sqrt(2/n),
the filter publishes d_hat > 1.96 * SE, and all tests are normal approximations.
"""
import csv
from math import ceil, sqrt
from pathlib import Path
from statistics import NormalDist

HERE = Path(__file__).parent
Z = NormalDist()


def se_d(n):
    """Standard error of d with n players per group."""
    return sqrt(2 / n)


def load_pairs(path=HERE / "pairs.csv"):
    with open(path, newline="") as f:
        return [{"study": r["study"], "topic": r["topic"],
                 "d_orig": float(r["d_orig"]), "n_orig": int(r["n_orig"]),
                 "d_rep": float(r["d_rep"]), "n_rep": int(r["n_rep"]),
                 "patch_changed": int(r["patch_changed"])} for r in csv.DictReader(f)]


def power(delta, n):
    """TODO 1a. Chance that a study with n per group finds d_hat > 1.96 * SE
    when the true effect is delta (one direction only, as in the lecture)."""
    raise NotImplementedError("TODO 1a")


def expected_published(delta, n):
    """TODO 1b. Mean d_hat among studies that pass the filter:
    delta + SE * pdf(a) / (1 - cdf(a)) with a = 1.96 - delta / SE.
    Use Z.pdf and Z.cdf."""
    raise NotImplementedError("TODO 1b")


def d33(n_orig):
    """The effect size that would have given the original study 33% power."""
    return (1.96 - Z.inv_cdf(0.67)) * se_d(n_orig)


def verdicts(d_o, n_o, d_r, n_r, sesoi=0.20):
    """TODO 2. Apply the five criteria of lecture section 3. Return a dict with keys:

    "sig_same_sign"  True if the replication is two-sided significant (p < .05) with the
                     same sign as the original.
    "captured"       True if d_o lies inside the replication's 95% interval d_r +/- 1.96*SE_r.
    "telescope_p"    one-sided p for "the replication is below d33(n_o)":
                     Z.cdf((d_r - d33(n_o)) / SE_r).
    "too_small"      True if telescope_p < 0.05.
    "equivalent"     True if the 90% interval d_r +/- 1.645*SE_r lies strictly inside
                     (-sesoi, +sesoi).
    "pooled_d"       inverse-variance weighted mean of d_o and d_r (weights 1/SE^2).
    "pooled_p"       two-sided p of pooled_d, with SE = 1/sqrt(sum of weights).
    """
    raise NotImplementedError("TODO 2")


def replication_n(n_orig, target_power=0.80):
    """TODO 3. Players per group a replication needs so that, if the true effect is 0,
    a one-sided test at alpha = .05 rejects d33(n_orig) with probability target_power.
    Solve d33 = (z_.95 + z_power) * sqrt(2 / n) for n and round UP to a whole player.
    Use Z.inv_cdf for both z values."""
    raise NotImplementedError("TODO 3")


if __name__ == "__main__":
    print("study  d_orig n_orig  d_rep n_rep | sig capt  tel_p small equiv pooled | patch")
    for p in load_pairs():
        v = verdicts(p["d_orig"], p["n_orig"], p["d_rep"], p["n_rep"])
        yn = lambda b: "yes" if b else "no"
        print(f"{p['study']:>5} {p['d_orig']:7.3f} {p['n_orig']:6d} {p['d_rep']:6.3f} {p['n_rep']:5d} |"
              f" {yn(v['sig_same_sign']):>3} {yn(v['captured']):>4} {v['telescope_p']:6.3f}"
              f" {yn(v['too_small']):>5} {yn(v['equivalent']):>5} {v['pooled_d']:6.3f} |"
              f" {p['patch_changed']}")
