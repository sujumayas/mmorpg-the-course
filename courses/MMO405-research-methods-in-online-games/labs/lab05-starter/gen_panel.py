"""MMO405 Lab 05: writes panel.csv, 16 weeks of synthetic telemetry from an
invented MMO. One row per account per week: account, age_band, week, heavy.
heavy = 1 if the account played more than 4 hours a day on 6 days that week.
A playtime rule for under-18 accounts starts in week 0, the same week as an
expansion that everyone gets. Seed 505. Standard library only.

Run:  python gen_panel.py
"""
import csv
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
SEED = 505
N_ACCOUNTS = 60_000
WEEKS = range(-8, 8)
BANDS = [("under18", 0.15), ("18-24", 0.30), ("25plus", 0.55)]


def prob(band, week):
    """Weekly probability (in %) that an account in this band plays heavily."""
    after = 1 if week >= 0 else 0
    if band == "under18":
        return 4.0 + 1.0 * after - 2.0 * after
    if band == "18-24":
        return 3.5 + 0.25 * week + 1.0 * after
    return 3.0 + 1.0 * after


def main():
    rng = random.Random(SEED)
    rows = []
    for acc in range(1, N_ACCOUNTS + 1):
        u, band = rng.random(), None
        cum = 0.0
        for name, share in BANDS:
            cum += share
            if u < cum:
                band = name
                break
        for week in WEEKS:
            heavy = 1 if rng.random() * 100 < prob(band, week) else 0
            rows.append((acc, band, week, heavy))
    with open(HERE / "panel.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["account", "age_band", "week", "heavy"])
        w.writerows(rows)
    print(f"wrote panel.csv: {N_ACCOUNTS} accounts x {len(WEEKS)} weeks")


if __name__ == "__main__":
    main()
