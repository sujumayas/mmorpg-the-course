"""MMO403 Lab 05: tune a battle pass.

Run:  python gen_owners.py      # once, writes owners.csv
      python battlepass.py      # prints the lecture table and the data table
      python check_lab05.py     # PASS / FAIL / TODO per function

Standard library only. Fill in every function that raises NotImplementedError.
The model is in lecture 05, section 2.
"""
import csv
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load_hours():
    """Given. Season hours of every owner in owners.csv, in file order."""
    with open(HERE / "owners.csv") as fh:
        return [float(r["season_hours"]) for r in csv.DictReader(fh)]


def share_playing_at_least(h, m, s):
    """Lognormal model: share of owners with season hours >= h.
    1 - Phi(ln(h/m)/s), using math.erf. Return 1.0 when h <= 0."""
    raise NotImplementedError


def tier_reached(hours, h_star, tiers=100):
    """Final tier of one owner: min(tiers, floor(tiers * hours / h_star))."""
    raise NotImplementedError


def tier_distribution(h_star, m, s, tiers=100):
    """Model distribution of the final tier. Return a list d of length tiers + 1
    with d[k] = P(T = k). For k < tiers, d[k] = reach(k) - reach(k + 1), where
    reach(k) = share_playing_at_least(k * h_star / tiers, m, s).
    d[tiers] = reach(tiers)."""
    raise NotImplementedError


def stats_from_distribution(d, gap=10, buy_share=0.3, tier_price=150,
                            rebate=1500, placement="even"):
    """From a final-tier distribution d (length tiers + 1) return a dict with
    keys finish, mean_tier, near_miss, tier_revenue, rebate_back:
      finish       = d[tiers]
      mean_tier    = sum(k * d[k])
      near_miss    = sum of d[k] for tiers - gap <= k < tiers
      tier_revenue = 1000 * buy_share * tier_price * sum((tiers - k) * d[k])
                     over the same k   (coins per 1,000 owners)
      rebate_back  = rebate * mean_tier / tiers   if placement == "even"
                     rebate * finish               if placement == "final"
    """
    raise NotImplementedError


def empirical_distribution(hours, h_star, tiers=100):
    """Distribution of final tiers in real data: list of length tiers + 1,
    share of owners whose tier_reached(...) equals k."""
    raise NotImplementedError


def fit_lognormal(hours):
    """Return (m, s): m = exp(mean of ln hours), s = sample standard deviation
    (statistics.stdev) of ln hours."""
    raise NotImplementedError


def best_h_star(m, s, lo=10, hi=150, **kw):
    """Whole-hour h_star in [lo, hi] with the highest model tier_revenue.
    Ties go to the smaller h_star. kw is passed to stats_from_distribution."""
    raise NotImplementedError


def main():
    print("Lecture model (m = 40, s = 0.7)")
    for h in (20, 30, 40, 50, 60, 80, 100):
        r = stats_from_distribution(tier_distribution(h, 40, 0.7))
        print(f"{h:4}  finish {r['finish']:6.1%}  mean tier {r['mean_tier']:5.1f}"
              f"  revenue {r['tier_revenue']:8,.0f}  rebate {r['rebate_back']:5.0f}")
    hours = load_hours()
    m, s = fit_lognormal(hours)
    print(f"\nData: {len(hours)} owners, fitted m = {m:.2f} h, s = {s:.3f}")
    for h in (20, 30, 40, 50, 60, 80, 100):
        emp = stats_from_distribution(empirical_distribution(hours, h))
        mod = stats_from_distribution(tier_distribution(h, m, s))
        print(f"{h:4}  finish data {emp['finish']:6.1%} model {mod['finish']:6.1%}"
              f"  revenue data {emp['tier_revenue']:8,.0f} model {mod['tier_revenue']:8,.0f}")


if __name__ == "__main__":
    main()
