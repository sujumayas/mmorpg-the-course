"""MMO308 Lab 02: touches and play.

Fill in every function marked TODO, then run `python test_kpis.py`.
Run `python gen_activity.py` first so activity.csv and payments.csv exist.
Standard-library Python 3.10+ only.

Conventions (from the week 2 lecture):
  * days_map is {day: set(player_id)} for every day that has activity.
  * A window [first, last] includes both ends.
  * Player-days = sum of DAU over the window. Mean DAU = player-days / number of days.
  * MAU over a window = distinct players active on any day of the window.
  * Stickiness = mean DAU / MAU.
  * A payer-day is a (day, player) pair with at least one purchase.
"""
import csv
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent


# ---------------------------------------------------------------- provided

def load_activity(path=HERE / "activity.csv"):
    days = defaultdict(set)
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            days[int(r["day"])].add(r["player_id"])
    return dict(days)


def load_payments(path=HERE / "payments.csv"):
    """Return a list of (day, player_id, amount)."""
    with open(path, newline="") as f:
        return [(int(r["day"]), r["player_id"], float(r["amount"])) for r in csv.DictReader(f)]


# ---------------------------------------------------------------- TODO

def month_model(R, p, T, k, D=30):
    """The lecture's regulars-and-tourists model for one month.
    Return a dict with mau, player_days, mean_dau and stickiness."""
    raise NotImplementedError("month_model: MAU, player-days, mean DAU, stickiness")


def dau_series(days_map, first, last):
    """List of DAU for each day first..last (0 for a day with no activity)."""
    raise NotImplementedError("dau_series: DAU per day")


def window_mau(days_map, first, last):
    """Distinct players active on any day in [first, last]."""
    raise NotImplementedError("window_mau: distinct players in a window")


def rolling_mau(days_map, t, window=30):
    """Distinct players active in the `window` days ending on day t."""
    raise NotImplementedError("rolling_mau: window ending on day t")


def regulars(days_map, t, min_days=8, window=28):
    """Players active on at least `min_days` of the `window` days ending on day t."""
    raise NotImplementedError("regulars: count of players with min_days in window")


def kpi_tree(days_map, payments, first, last):
    """Return a dict with: days, player_days, mean_dau, mau, stickiness, revenue,
    revenue_per_day, payer_days, payer_rate (payer_days / player_days),
    arppu (revenue / payer_days), arpdau (revenue / player_days).
    Only payments with first <= day <= last count. Return 0.0 for any ratio
    whose denominator is 0."""
    raise NotImplementedError("kpi_tree: the week 2 KPI tree for one window")


def revenue_factors(tree0, tree1):
    """Return (mean_dau_ratio, arpdau_ratio, revenue_per_day_ratio), each tree1 / tree0.
    The first two multiply to the third."""
    raise NotImplementedError("revenue_factors: DAU and ARPDAU factors")


# ---------------------------------------------------------------- report

if __name__ == "__main__":
    act, pay = load_activity(), load_payments()
    months = [(0, 29), (30, 59), (60, 89)]
    trees = [kpi_tree(act, pay, a, b) for a, b in months]
    print("month        MAU   mean DAU  stickiness  ARPDAU  revenue/day")
    for i, t in enumerate(trees, 1):
        print(f"{i:5d} {t['mau']:10,} {t['mean_dau']:10,.0f} {t['stickiness']:11.3f} "
              f"{t['arpdau']:7.4f} {t['revenue_per_day']:12,.2f}")
    for i in (1, 2):
        d, a, r = revenue_factors(trees[i - 1], trees[i])
        print(f"month {i} -> {i + 1}: revenue/day x{r:.3f} = DAU x{d:.3f} * ARPDAU x{a:.3f}")
    print("day  DAU  rolling30  stickiness  regulars")
    for t in (35, 39, 40, 41, 45, 69, 70, 71, 72, 89):
        mean_dau = sum(dau_series(act, t - 29, t)) / 30
        m = rolling_mau(act, t)
        print(f"{t:3d} {len(act.get(t, ())):5d} {m:9,d} {mean_dau / m:11.3f} {regulars(act, t):9,d}")
