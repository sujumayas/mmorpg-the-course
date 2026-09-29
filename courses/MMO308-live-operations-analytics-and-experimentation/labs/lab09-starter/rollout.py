"""MMO308 Lab 09 starter: a rollout planner and a hotfix triage rule.

Standard library only (Python 3.12 or later, for random.binomialvariate).
Fill in every function marked TODO, then run
    .venv/bin/python courses/MMO308-live-operations-analytics-and-experimentation/labs/lab09-starter/test_rollout.py
from the repository root.

Notation follows the week 9 lecture:
    N       players who will take the patch
    p       bug rate, chance a player who takes the patch is hit
    d       detection rate, chance a hit player's problem reaches you in time
    stages  cumulative shares, strictly increasing, last one 1.0
"""
import csv
import math
import random
from pathlib import Path

BUGS = Path(__file__).with_name("bugs.csv")


def reach_probs(N, p, d, stages):
    """List of P(reach stage i) for each stage. The first is always 1.0.
    P(reach stage i+1) = P(reach stage i) * (1 - p*d) ** (players newly exposed in stage i).
    TODO"""
    raise NotImplementedError


def expected_harm(N, p, d, stages):
    """Expected players hit: sum over stages of P(reach) * newly exposed * p. TODO"""
    raise NotImplementedError


def simulate_rollout(N, p, d, stages, rng):
    """One simulated rollout. For each stage in order:
      exposed = players newly exposed in this stage (round to int)
      hit      = rng.binomialvariate(exposed, p)
      detected = rng.binomialvariate(hit, d)
      add hit to the total; if detected > 0, stop (halt before the next stage).
    Return the total players hit. TODO"""
    raise NotImplementedError


def canary_size(p, d, conf=0.95):
    """Smallest integer n with 1 - (1 - p*d) ** n >= conf. TODO"""
    raise NotImplementedError


def rollout_hours(stages, soak_hours):
    """Hours from the first stage to full release: one soak per stage
    before the last. TODO"""
    raise NotImplementedError


def best_plan(N, p, d, candidates, soak_hours, max_hours):
    """Among candidate stage lists whose rollout_hours <= max_hours, return the
    one with the lowest expected_harm (the first one on a tie). TODO"""
    raise NotImplementedError


def hotfix_decision(harm_per_hour, hours_to_patch, restart_minutes, ccu, risk, risk_harm):
    """Return (decision, wait_cost, hotfix_cost) in player-hours, where
    wait_cost = harm_per_hour * hours_to_patch,
    hotfix_cost = ccu * restart_minutes / 60 + risk * risk_harm,
    and decision is "hotfix" if wait_cost > hotfix_cost, otherwise "wait". TODO"""
    raise NotImplementedError


def load_bugs(path=BUGS):
    """Rows of bugs.csv with numeric fields converted. Provided."""
    with open(path, newline="") as fh:
        rows = list(csv.DictReader(fh))
    for r in rows:
        for k in ("harm_per_hour", "hours_to_patch", "restart_minutes", "ccu", "risk", "risk_harm"):
            r[k] = float(r[k])
    return rows


if __name__ == "__main__":
    print(expected_harm(200_000, 1 / 2_000, 1.0, [0.01, 0.10, 1.0]))
    for bug in load_bugs():
        args = [bug[k] for k in ("harm_per_hour", "hours_to_patch", "restart_minutes",
                                 "ccu", "risk", "risk_harm")]
        print(bug["bug_id"], hotfix_decision(*args))
