"""MMO307 Lab 13: meta settling time and patch cadence.

Standard-library Python only. Run the tests with:
    .venv/bin/python test_meta_cycle.py        (or: pytest test_meta_cycle.py)

The model (lecture week 13, section 2):
    D(t)  = D_s + (D_0 - D_s) * exp(-t / tau)           diversity t days after a patch
    D_bar = D_s + (D_0 - D_s) * (tau / T) * (1 - exp(-T / tau))   average over a T-day cycle

Fill in every function marked TODO. Do not change the signatures; the tests call them.
"""
import csv
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent


def effective_number(shares):
    """Effective number of strategies, 1 / sum(p_i^2) (MMO303 week 1).

    `shares` may be counts or fractions; normalise them first.
    Return 0.0 for an empty or all-zero list.
    """
    # TODO: implement
    raise NotImplementedError


def diversity_at(t, d0, ds, tau):
    """D(t) from the settling model."""
    # TODO: implement
    raise NotImplementedError


def fit_tau(days, diversity, ds):
    """Estimate the settling time tau from post-patch observations.

    Fit a straight line to ln(D - ds) against t by least squares and return
    tau = -1 / slope. Ignore any point where D - ds <= 0 (the log is undefined).
    Raise ValueError if fewer than two usable points remain.
    """
    # TODO: implement
    raise NotImplementedError


def cycle_average(d0, ds, tau, period):
    """Average diversity over one patch cycle of `period` days (D_bar above)."""
    # TODO: implement
    raise NotImplementedError


def longest_period(d0, ds, tau, target, max_days=365):
    """Largest whole number of days T (1..max_days) with cycle_average >= target.

    Return 0 if even T = 1 misses the target.
    """
    # TODO: implement
    raise NotImplementedError


def load_pick_log(path=HERE / "pick_log.csv"):
    """Return (days, diversity) from the pick log: one N_eff value per day."""
    days, diversity = [], []
    with open(path, newline="") as fh:
        reader = csv.DictReader(fh)
        classes = [c for c in reader.fieldnames if c != "day"]
        for row in reader:
            days.append(int(row["day"]))
            diversity.append(effective_number([int(row[c]) for c in classes]))
    return days, diversity


if __name__ == "__main__":
    days, div = load_pick_log()
    for t, d in zip(days, div):
        print(f"day {t:2d}  N_eff {d:6.3f}")
