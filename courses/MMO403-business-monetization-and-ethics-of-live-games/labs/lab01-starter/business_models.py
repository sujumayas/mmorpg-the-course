"""MMO403 Lab 01 starter: four business models, one audience. Standard library only.

Fill in the four TODO functions, then run the tests:

    python3 test_business_models.py        (or: pytest test_business_models.py)

The model is the one from the week 1 lecture, section 2:

    contribution(T) = audience x d x (U + (m - c) x S(T))
    S(T) = 1 + r + r^2 + ... + r^(T-1)

d is the share of the audience that comes through the door, U the upfront price,
m the revenue per active player-month, c the cost to serve one active player-month,
r the monthly retention and T the horizon in months.
"""
import csv
import os
from dataclasses import dataclass

HERE = os.path.dirname(os.path.abspath(__file__))


@dataclass
class Model:
    name: str
    door: float      # d, share of the audience that plays
    upfront: float   # U, dollars paid once at the door
    monthly: float   # m, dollars per active player-month


def load_models(path=os.path.join(HERE, "models.csv")):
    """Return {name: Model} from models.csv."""
    models = {}
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            models[row["model"]] = Model(row["model"], float(row["door"]),
                                         float(row["upfront"]), float(row["monthly"]))
    return models


def months_active(r, T):
    """TODO step 1. Expected active months per player in the first T months.

    Month 1 counts as 1 (everyone who paid at the door plays in month 1).
    Return 1 + r + ... + r^(T-1). Return 0 for T = 0.
    """
    raise NotImplementedError("months_active() is yours to write")


def contribution(model, r, T, cost=0.50, audience=1_000_000):
    """TODO step 2. Revenue minus cost to serve over the first T months, in dollars."""
    raise NotImplementedError("contribution() is yours to write")


def crossover_month(a, b, r, cost=0.50, audience=1_000_000, horizon=120):
    """TODO step 3. First horizon T (1..horizon) where model b's contribution is at least
    model a's, given that it was strictly below at T = 1. Return None if b never catches up
    within the horizon, and 1 if b already leads or ties at T = 1."""
    raise NotImplementedError("crossover_month() is yours to write")


def retention_value(model, r, T=36, cost=0.50, audience=1_000_000, step=0.01):
    """TODO step 4. Change in contribution over T months when monthly retention rises
    from r to r + step. Negative means retention costs this model money."""
    raise NotImplementedError("retention_value() is yours to write")


if __name__ == "__main__":
    models = load_models()
    for r in (0.7, 0.8, 0.9):
        print(f"r = {r}")
        for m in models.values():
            print(f"  {m.name:13s} ${contribution(m, r, 36) / 1e6:6.2f}M over 36 months")
