"""MMO406 Lab 14: the lore desk and the question test.

Run:   .venv/bin/python lore_desk.py thornmere_questions.csv --lam 48 --mu 20
Tests: .venv/bin/python test_lore_desk.py   (or pytest)

Model (week 14 lecture, sections 2 and 3):
    lam_e   = (1 - a) * lam                    questions per week reaching the lead
    W_days  = days_per_week / (mu - lam_e)     if lam_e < mu, else infinite
    a_min   = max(0, 1 - mu / lam)
    a_wait  = 1 - (mu - days_per_week / target_days) / lam
    a       = (answered + derivable) / total   from a question test
    margin  = 1.96 * sqrt(a * (1 - a) / total) (95% margin of error)
    gap     = missing + 2 * contradicted       per chapter

A question log (see thornmere_questions.csv) is a CSV with the columns
id, asker, chapter, question, status. Status is one of STATUSES.
"""
import argparse
import csv
import math
import sys

STATUSES = ("answered", "derivable", "missing", "contradicted", "reserved")


def escalated_rate(lam, a):
    """Questions per week that the bible does not answer."""
    raise NotImplementedError("escalated_rate")


def wait_days(lam, mu, a, days_per_week=5):
    """Average working days from question to answer; math.inf if the desk never clears."""
    raise NotImplementedError("wait_days")


def min_answer_rate(lam, mu):
    """Smallest answer rate at which the desk is stable (never below 0)."""
    raise NotImplementedError("min_answer_rate")


def answer_rate_for_wait(lam, mu, target_days, days_per_week=5):
    """Smallest answer rate that gives an average wait of target_days.
    Return None if even a perfect bible cannot reach it (mu too small),
    and 0.0 if no bible at all is needed."""
    raise NotImplementedError("answer_rate_for_wait")


def load_log(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def score_questions(rows):
    """Return {"counts": {status: n for every status in STATUSES},
               "total": n, "a": answer rate, "margin": 95% margin}.
    Raise ValueError on a status not in STATUSES or an empty log."""
    raise NotImplementedError("score_questions")


def gap_ranking(rows):
    """Return [(chapter, score)] for chapters with score > 0, where
    score = missing + 2 * contradicted, sorted by score (high first),
    then chapter name (A to Z)."""
    raise NotImplementedError("gap_ranking")


def report(rows, lam, mu):
    sc = score_questions(rows)
    a, m = sc["a"], sc["margin"]
    print(f"{sc['total']} questions: " + ", ".join(f"{k} {v}" for k, v in sc["counts"].items()))
    print(f"Answer rate a = {a:.1%} (95% margin {m:.1%}, so {max(0, a - m):.1%} to {min(1, a + m):.1%})")
    print("\nGaps to fix first:")
    for chapter, score in gap_ranking(rows):
        print(f"  {chapter:<12} {score}")
    print(f"\nDesk: lam = {lam:g}/week, mu = {mu:g}/week, a_min = {min_answer_rate(lam, mu):.1%}")
    t = answer_rate_for_wait(lam, mu, 1)
    print("Answer rate for a one-day wait: " + ("not reachable" if t is None else f"{t:.1%}"))
    for label, rate in (("low end", max(0, a - m)), ("estimate", a), ("high end", min(1, a + m))):
        w = wait_days(lam, mu, rate)
        print(f"  {label:<9} a = {rate:5.1%}  wait " + ("never clears" if w == math.inf else f"{w:.2f} days"))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("log", nargs="?", default="thornmere_questions.csv")
    p.add_argument("--lam", type=float, default=48)
    p.add_argument("--mu", type=float, default=20)
    args = p.parse_args()
    try:
        report(load_log(args.log), args.lam, args.mu)
    except NotImplementedError as e:
        print(f"TODO: implement {e}")
        sys.exit(1)
