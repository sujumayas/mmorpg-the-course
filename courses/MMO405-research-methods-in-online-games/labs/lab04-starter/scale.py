"""MMO405 Lab 04: reliability and structure of a player survey.

Run:  python gen_survey.py      # once, writes survey.csv
      python scale.py           # prints the measurement report from your functions
      python check_lab04.py     # PASS / FAIL / TODO per function

Standard library only. Fill in every function that raises NotImplementedError.
An "items" argument is always a list of columns: items[j] is the list of all
respondents' answers to item j, and every column has the same length.
"""
import csv
from math import sqrt
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load_survey(path=HERE / "survey.csv"):
    """Return (names, items): item names and a list of integer columns."""
    with open(path, newline="") as f:
        rows = list(csv.reader(f))
    names = rows[0][1:]
    items = [[int(r[j + 1]) for r in rows[1:]] for j in range(len(names))]
    return names, items


def reverse_code(values, lo=1, hi=7):
    """Return a new list with each x replaced by lo + hi - x."""
    raise NotImplementedError


def variance(xs):
    """Sample variance with n - 1 in the denominator."""
    raise NotImplementedError


def pearson(x, y):
    """Pearson correlation of two equal-length lists."""
    raise NotImplementedError


def cronbach_alpha(items):
    """alpha = k/(k-1) * (1 - sum of item variances / variance of the total score),
    where the total score of a respondent is the sum of their answers."""
    raise NotImplementedError


def standardized_alpha(k, rbar):
    """alpha = k * rbar / (1 + (k - 1) * rbar)."""
    raise NotImplementedError


def mean_interitem_r(items):
    """Average Pearson correlation over all distinct pairs of items."""
    raise NotImplementedError


def corrected_item_total(items):
    """For each item j, the Pearson correlation between item j and the sum of
    all OTHER items. Return a list of k floats."""
    raise NotImplementedError


def alpha_if_deleted(items):
    """For each item j, cronbach_alpha of the scale without item j. Return a list."""
    raise NotImplementedError


def main():
    try:
        report()
    except NotImplementedError:
        print("Some functions still raise NotImplementedError. Run check_lab04.py to see which.")


def report():
    names, raw = load_survey()
    print(f"{len(raw[0])} respondents, {len(raw)} items")
    print(f"alpha, raw data as given:       {cronbach_alpha(raw):.3f}")
    print(f"mean inter-item r:              {mean_interitem_r(raw):.3f}")
    print("\nitem  corrected item-total  alpha if deleted")
    for name, r, a in zip(names, corrected_item_total(raw), alpha_if_deleted(raw)):
        print(f"{name:>4}  {r:20.3f}  {a:16.3f}")


if __name__ == "__main__":
    main()
