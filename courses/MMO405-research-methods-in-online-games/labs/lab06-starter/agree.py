"""MMO405 Lab 06: agreement statistics for two coders and one yes/no code.

Run:  python agree.py            # prints the agreement report for prior_codes.csv
      python agree.py mine.csv   # the same for your own file with the same columns
      python check_lab06.py      # PASS / FAIL / TODO per function

Standard library only. Fill in every function that raises NotImplementedError.
A "codes" argument is a list of 0/1 integers, one per excerpt, in excerpt order.
"""
import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load_codes(path=HERE / "prior_codes.csv"):
    """Return {column name: list of 0/1 ints} for every column except id."""
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    return {k: [int(r[k]) for r in rows] for k in rows[0] if k != "id"}


def table_2x2(codes_a, codes_b):
    """Return (a, b, c, d): a both 1, b A=1 B=0, c A=0 B=1, d both 0."""
    raise NotImplementedError


def percent_agreement(a, b, c, d):
    """p_o = (a + d) / n, as a proportion from 0 to 1."""
    raise NotImplementedError


def cohen_kappa(a, b, c, d):
    """kappa = (p_o - p_e) / (1 - p_e), with
    p_e = p_A * p_B + (1 - p_A) * (1 - p_B), p_A = (a + b) / n, p_B = (a + c) / n.
    Return 1.0 if p_e == 1 (both coders gave one answer to everything and agreed)."""
    raise NotImplementedError


def specific_agreement(a, b, c, d):
    """Return (p_pos, p_neg) with p_pos = 2a / (2a + b + c) and
    p_neg = 2d / (2d + b + c). Use None for a value whose denominator is 0."""
    raise NotImplementedError


def pabak(a, b, c, d):
    """Prevalence-adjusted bias-adjusted kappa: 2 * p_o - 1."""
    raise NotImplementedError


def main():
    try:
        report(sys.argv[1] if len(sys.argv) > 1 else HERE / "prior_codes.csv")
    except NotImplementedError:
        print("Some functions still raise NotImplementedError. Run check_lab06.py to see which.")


def fmt(x):
    return "  n/a" if x is None else f"{x:5.2f}"


def report(path):
    codes = load_codes(path)
    stems = sorted({k.rsplit("_", 1)[0] for k in codes})
    print("code          a   b   c   d   p_o  kappa  p_pos  p_neg  PABAK")
    for s in stems:
        t = table_2x2(codes[s + "_a"], codes[s + "_b"])
        pp, pn = specific_agreement(*t)
        print(f"{s:<12} {t[0]:>2}  {t[1]:>2}  {t[2]:>2}  {t[3]:>2}  "
              f"{percent_agreement(*t):.2f}  {cohen_kappa(*t):+.2f}  {fmt(pp)}  {fmt(pn)}  {pabak(*t):.2f}")


if __name__ == "__main__":
    main()
