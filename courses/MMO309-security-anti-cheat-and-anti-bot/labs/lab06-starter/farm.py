"""MMO309 Lab 06: the bot farm ledger. Fill in every function marked TODO.

The model from the week 6 lecture:
    revenue per day  = gold_per_hour * hours * price / 100_000     (price is $ per 100,000 gold)
    margin m         = revenue - run_cost
    lifetime L       = 1/d + W/2          (d: daily detection chance, W: days between waves)
    profit           = m * L - setup
    break-even life  = setup / m

bots.csv columns: account, created_day, detected_day, banned_day. Empty cells mean
"not yet" by the end of the log (END_DAY). Days are integers.
"""
import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent
END_DAY = 120


def load(path=HERE / "bots.csv"):
    """Return a list of dicts with int values, or None for empty cells."""
    with open(path) as f:
        return [{k: (int(v) if v not in ("", None) and k != "account" else (v or None))
                 for k, v in row.items()} for row in csv.DictReader(f)]


def margin(gold_per_hour, hours, price, run_cost):
    """Dollars per day a bot earns after running costs."""
    raise NotImplementedError("TODO step 1")


def profit(d, W, gold_per_hour=20_000, hours=20, price=1.50, run_cost=1.00, setup=35.0):
    """Expected profit per bot account, in dollars."""
    raise NotImplementedError("TODO step 1")


def breakeven_d(W, gold_per_hour=20_000, hours=20, price=1.50, run_cost=1.00, setup=35.0):
    """Smallest daily detection chance at which profit is <= 0, for wave interval W.
    Return 0.0 if m <= 0: the farm never pays, so any detection rate closes it.
    Return None if no detection rate is enough, which happens when setup/m <= W/2."""
    raise NotImplementedError("TODO step 1")


def estimate_d(rows, end_day=END_DAY):
    """Estimate the daily detection chance from the log, allowing for censoring.
    Each account is at risk from created_day. A detected account contributes
    (detected_day - created_day) days at risk and one detection. An account not
    detected by end_day contributes (end_day - created_day) days and no detection.
    Return detections / total days at risk."""
    raise NotImplementedError("TODO step 2")


def mean_wave_lag(rows):
    """Mean of (banned_day - detected_day) over accounts that have both."""
    raise NotImplementedError("TODO step 3")


if __name__ == "__main__":
    rows = load()
    d = estimate_d(rows)
    lag = mean_wave_lag(rows)
    print(f"accounts {len(rows)}, estimated d = {d:.4f}, mean wave lag = {lag:.2f} days")
    print(f"model lifetime with W = 7: {1 / d + 3.5:.2f} days; measured-lag lifetime: {1 / d + lag:.2f}")
    print(f"profit per account at W = 7: ${profit(d, 7):.2f}")
    print(f"break-even d at W = 7: {breakeven_d(7)}")
