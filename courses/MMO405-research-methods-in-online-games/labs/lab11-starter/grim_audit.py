"""MMO405 lab 11: check that reported numbers can exist.

Python 3, standard library only. Fill in the four TODOs, then run
    python -m unittest test_grim_audit.py
from inside this folder (from the repository root, .venv/bin/python is the course Python).
Running this file prints the audit of manuscript_means.csv and manuscript_tests.csv
once the TODOs are done.
"""
import csv
import math
from pathlib import Path

HERE = Path(__file__).parent


# ---------- provided: exact two-sided p-value for a t statistic ----------

def _betacf(a, b, x, eps=1e-14, max_iter=500):
    """Continued fraction for the regularized incomplete beta function."""
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    d = 1.0 / (d if abs(d) > 1e-300 else 1e-300)
    h = d
    for m in range(1, max_iter + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        d = 1.0 / (d if abs(d) > 1e-300 else 1e-300)
        c = 1.0 + aa / c if abs(1.0 + aa / c) > 1e-300 else 1e-300
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        d = 1.0 / (d if abs(d) > 1e-300 else 1e-300)
        c = 1.0 + aa / c if abs(1.0 + aa / c) > 1e-300 else 1e-300
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < eps:
            break
    return h


def _betai(a, b, x):
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    lbeta = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
    front = math.exp(lbeta + a * math.log(x) + b * math.log(1.0 - x))
    if x < (a + 1.0) / (a + b + 2.0):
        return front * _betacf(a, b, x) / a
    return 1.0 - front * _betacf(b, a, 1.0 - x) / b


def t_two_sided_p(t, df):
    """Two-sided p-value of Student's t with df degrees of freedom."""
    return _betai(df / 2.0, 0.5, df / (df + t * t))


# ---------- loaders ----------

def load_means(path=HERE / "manuscript_means.csv"):
    with open(path, newline="") as f:
        return [{"id": r["id"], "label": r["label"], "mean": float(r["mean"]), "n": int(r["n"]),
                 "items": int(r["items"]), "decimals": int(r["decimals"])} for r in csv.DictReader(f)]


def load_tests(path=HERE / "manuscript_tests.csv"):
    with open(path, newline="") as f:
        return [{"id": r["id"], "label": r["label"], "t": float(r["t"]), "df": int(r["df"]),
                 "relation": r["relation"], "p": float(r["p"]), "decimals": int(r["decimals"])}
                for r in csv.DictReader(f)]


# ---------- your work ----------

def grim(mean, n, items=1, decimals=2):
    """TODO 1. True if some whole-number sum k gives k / (n * items) that rounds
    (half up) to `mean` at `decimals` places. Use integer arithmetic, as in the
    lecture's code, so that floating-point error cannot flip the answer."""
    raise NotImplementedError("TODO 1")


def nearest_possible(mean, n, items=1, decimals=2):
    """TODO 2. Return (below, above): the largest possible reported mean strictly
    below `mean` and the smallest strictly above it, each rounded to `decimals`."""
    raise NotImplementedError("TODO 2")


def p_consistent(t, df, relation, reported, decimals):
    """TODO 3. Recompute p = t_two_sided_p(t, df) and compare with the report.

    relation "=": consistent if p rounded to `decimals` equals `reported`.
    relation "<": consistent if p < reported.
    """
    raise NotImplementedError("TODO 3")


def audit_means(rows):
    """TODO 4. Return a list of (id, status) with status one of
    "untestable" (n * items >= 10**decimals), "consistent" or "inconsistent"."""
    raise NotImplementedError("TODO 4")


def report():
    means = load_means()
    status = dict(audit_means(means))
    print("Means")
    for r in means:
        extra = ""
        if status[r["id"]] == "inconsistent":
            lo, hi = nearest_possible(r["mean"], r["n"], r["items"], r["decimals"])
            extra = f"  (nearest possible: {lo} or {hi})"
        print(f"  {r['id']:4s} {r['label']:38s} M={r['mean']:<6} n={r['n']:<4} items={r['items']}  {status[r['id']]}{extra}")
    print("Tests")
    for r in load_tests():
        p = t_two_sided_p(r["t"], r["df"])
        ok = p_consistent(r["t"], r["df"], r["relation"], r["p"], r["decimals"])
        print(f"  {r['id']:4s} {r['label']:38s} t({r['df']})={r['t']}  reported p {r['relation']} {r['p']}  "
              f"recomputed {p:.4f}  {'consistent' if ok else 'INCONSISTENT'}")


if __name__ == "__main__":
    report()
