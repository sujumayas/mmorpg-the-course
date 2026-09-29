"""MMO405 lab 02: effect sizes, intervals and the four verdicts.

Python 3, standard library only. Fill in the four TODOs, then run
    python -m unittest test_effects.py
from inside this folder (from the repository root, .venv/bin/python is the course Python).
Running this file directly prints the report once the TODOs are done.
"""
import csv
from math import atanh, erf, sqrt, tanh
from pathlib import Path
from statistics import mean, variance

HERE = Path(__file__).parent
VERDICTS = ("meaningful", "no meaningful effect", "real but trivial", "inconclusive")


def phi(z):
    """Standard normal cumulative probability."""
    return 0.5 * (1 + erf(z / sqrt(2)))


def load(path=HERE / "wellbeing.csv"):
    with open(path, newline="") as f:
        return [{"player_id": r["player_id"], "server": r["server"],
                 "voice_chat": int(r["voice_chat"]), "wellbeing": float(r["wellbeing"])}
                for r in csv.DictReader(f)]


def cohens_d(a, b):
    """TODO 1. Standardized difference (mean(b) - mean(a)) / pooled SD.

    Pooled SD = sqrt(((na-1)*var(a) + (nb-1)*var(b)) / (na + nb - 2)),
    with var the sample variance (statistics.variance).
    """
    raise NotImplementedError("TODO 1")


def se_d(d, n1, n2):
    """Standard error of d for unequal groups (Hedges and Olkin's large-sample form).

    For equal groups and small d this is close to the lecture's sqrt(2/n).
    """
    return sqrt((n1 + n2) / (n1 * n2) + d * d / (2 * (n1 + n2)))


def verdict(d, se, sesoi):
    """TODO 2. Return one of VERDICTS, using the lecture's rules.

    different  = the 95% interval d +/- 1.96*se excludes 0
    equivalent = the 90% interval d +/- 1.645*se lies strictly inside (-sesoi, +sesoi)
    """
    raise NotImplementedError("TODO 2")


def fisher_ci(r, n, level_z=1.96):
    """TODO 3. Confidence interval for a correlation via Fisher's z.

    z = atanh(r), SE = 1/sqrt(n - 3); return (tanh(z - level_z*SE), tanh(z + level_z*SE)).
    """
    raise NotImplementedError("TODO 3")


def by_server(rows):
    """TODO 4. For each server, return (d, se) comparing voice_chat 1 (b) with 0 (a).

    Return a dict server -> (d, se), servers sorted A, B, C.
    """
    raise NotImplementedError("TODO 4")


if __name__ == "__main__":
    rows = load()
    a = [r["wellbeing"] for r in rows if r["voice_chat"] == 0]
    b = [r["wellbeing"] for r in rows if r["voice_chat"] == 1]
    d = cohens_d(a, b)
    se = se_d(d, len(a), len(b))
    print(f"pooled: n={len(a)}+{len(b)}  d={d:.3f}  95% CI [{d - 1.96 * se:.3f}, {d + 1.96 * se:.3f}]"
          f"  verdict at SESOI 0.20: {verdict(d, se, 0.20)}")
    for s, (ds, ses) in by_server(rows).items():
        print(f"server {s}: d={ds:.3f}  95% CI [{ds - 1.96 * ses:.3f}, {ds + 1.96 * ses:.3f}]"
              f"  verdict: {verdict(ds, ses, 0.20)}")
    print("Fisher CI for r=0.10, n=2500:", tuple(round(x, 4) for x in fisher_ci(0.10, 2500)))
