"""MMO402 Lab 14 starter: find the crux of a design debate.

Usage:  python3 lab14-starter.py lab14-criteria.csv [criterion]

Criteria file: CSV with header `criterion,weight,<optionA>,<optionB>`. Each row is
one criterion, its weight (weights must sum to 1) and each option's score from
0 to 10, where higher is always better for that criterion (so a cost criterion
scores cheaper options higher).

Model (week 14, section 2). Each option's value is the weighted sum of its
scores. The gap D = U_A - U_B decides the debate. The crux weight of a
criterion is the weight at which D becomes 0 when that criterion's weight
changes and the other weights keep their proportions. The crux score is the
change in option A's score on one criterion that would make D = 0.

Pure standard library. Python 3.8+.
"""
import csv
import sys


def load(path):
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        a, b = reader.fieldnames[2], reader.fieldnames[3]
        rows = [(r["criterion"], float(r["weight"]), float(r[a]), float(r[b])) for r in reader]
    total = sum(w for _, w, _, _ in rows)
    if abs(total - 1.0) > 1e-6:
        raise SystemExit(f"weights sum to {total}, not 1")
    return a, b, rows


def values(rows):
    ua = sum(w * sa for _, w, sa, _ in rows)
    ub = sum(w * sb for _, w, _, sb in rows)
    return ua, ub


def crux_weight(rows, name):
    """Weight of criterion `name` at which the two options tie, with the other
    weights scaled to keep their proportions. None if no tie in [0, 1]."""
    wj = next(w for c, w, _, _ in rows if c == name)
    dj = next(sa - sb for c, _, sa, sb in rows if c == name)
    rest = sum(w * (sa - sb) for c, w, sa, sb in rows if c != name)
    if wj >= 1:
        return None
    d_rest = rest / (1 - wj)          # gap if this criterion had weight 0
    if d_rest == dj:
        return None
    t = d_rest / (d_rest - dj)
    return t if 0 <= t <= 1 else None


def crux_score(rows, name):
    """TODO (step 3): return the change x to option A's score on criterion
    `name` that makes the two options tie (D = 0), holding every weight fixed.
    Return None if the criterion has weight 0."""
    raise NotImplementedError


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    a, b, rows = load(sys.argv[1])
    ua, ub = values(rows)
    print(f"{a}: {ua:.3f}   {b}: {ub:.3f}   gap D = {ua - ub:+.3f}")
    names = [sys.argv[2]] if len(sys.argv) > 2 else [c for c, _, _, _ in rows]
    for name in names:
        t = crux_weight(rows, name)
        tw = "no tie in [0, 1]" if t is None else f"{t:.4f}"
        try:
            x = crux_score(rows, name)
            xs = "n/a" if x is None else f"{x:+.3f}"
        except NotImplementedError:
            xs = "TODO"
        print(f"  {name:<18} crux weight {tw:<18} crux score change for {a}: {xs}")


if __name__ == "__main__":
    main()
