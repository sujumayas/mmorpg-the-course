"""MMO405 Lab 05: difference-in-differences on a synthetic policy change.

Run:  python gen_panel.py       # once, writes panel.csv
      python did.py             # prints the estimates table from your functions
      python check_lab05.py     # PASS / FAIL / TODO per function

Standard library only. Fill in every function that raises NotImplementedError.
A "series" is a dict {week: percent of accounts playing heavily that week}.
"""
import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent
EARLY = range(-8, -4)   # weeks -8 to -5
PRE = range(-4, 0)      # weeks -4 to -1
POST = range(0, 4)      # weeks 0 to 3


def load_panel(path=HERE / "panel.csv"):
    """Return a list of (account, age_band, week, heavy) tuples with int fields."""
    with open(path, newline="") as f:
        r = csv.reader(f)
        next(r)
        return [(int(a), band, int(w), int(h)) for a, band, w, h in r]


def weekly_share(rows, bands):
    """Series for accounts whose age_band is in `bands` (a set of strings):
    for each week, 100 * (heavy rows) / (all rows) among those accounts."""
    raise NotImplementedError


def window_mean(series, weeks):
    """Mean of series[w] over the weeks in `weeks`."""
    raise NotImplementedError


def did(treated, comparison, pre=PRE, post=POST):
    """(treated post - treated pre) - (comparison post - comparison pre),
    each term a window_mean over the given weeks."""
    raise NotImplementedError


def placebo_did(treated, comparison, early=EARLY, pre=PRE):
    """The same DiD computed only on pre-rule weeks: `early` plays the role of
    'before' and `pre` the role of 'after'. Near zero if trends are parallel."""
    raise NotImplementedError


def odds_ratio(p_before, p_after):
    """Odds ratio of two proportions (0 to 1): odds(after) / odds(before)."""
    raise NotImplementedError


def main():
    try:
        report()
    except NotImplementedError:
        print("Some functions still raise NotImplementedError. Run check_lab05.py to see which.")


def report():
    rows = load_panel()
    pooled = weekly_share(rows, {"under18", "18-24", "25plus"})
    minors = weekly_share(rows, {"under18"})
    young = weekly_share(rows, {"18-24"})
    older = weekly_share(rows, {"25plus"})
    pb, pa = window_mean(pooled, PRE), window_mean(pooled, POST)
    print(f"pooled heavy play:  {pb:.2f}% -> {pa:.2f}%  change {pa - pb:+.2f}  "
          f"odds ratio {odds_ratio(pb / 100, pa / 100):.2f}")
    print(f"minors only change: {window_mean(minors, POST) - window_mean(minors, PRE):+.2f}")
    for name, comp in (("18-24", young), ("25plus", older)):
        print(f"DiD vs {name:>6}: {did(minors, comp):+.2f}   placebo {placebo_did(minors, comp):+.2f}")


if __name__ == "__main__":
    main()
