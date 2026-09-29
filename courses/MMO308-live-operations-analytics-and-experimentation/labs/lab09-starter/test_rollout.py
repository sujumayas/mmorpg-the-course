"""Tests for MMO308 Lab 09. Values come from the week 9 lecture and bugs.csv.

Run with `.venv/bin/python test_rollout.py` (exits 1 while any test fails)
or with pytest if you have it.
"""
import random
import statistics
import sys

from rollout import (best_plan, canary_size, expected_harm, hotfix_decision, load_bugs,
                     reach_probs, rollout_hours, simulate_rollout)

N, P = 200_000, 1 / 2_000


def close(a, b, tol=1e-6):
    return abs(a - b) < tol


def test_reach():
    r = reach_probs(N, P, 1.0, [0.01, 0.10, 1.0])
    assert close(r[0], 1.0) and close(r[1], 0.36779, 1e-4) and close(r[2], 4.5287e-5, 1e-7)


def test_lecture_harm():
    assert close(expected_harm(N, P, 1.0, [1.0]), 100)
    assert close(expected_harm(N, P, 1.0, [0.01, 0.10, 1.0]), 4.3149, 1e-3)
    assert close(expected_harm(N, P, 0.2, [0.01, 0.10, 1.0]), 20.548, 1e-2)
    assert close(expected_harm(N, P, 1.0, [0.01, 0.05, 0.25, 1.0]), 2.6057, 1e-3)
    assert close(expected_harm(100_000, 1 / 1_000, 1.0, [0.02, 0.2, 1.0]), 4.4336, 1e-3)


def test_simulation_matches_model():
    rng = random.Random(9)
    runs = [simulate_rollout(N, P, 0.2, [0.01, 0.10, 1.0], rng) for _ in range(4_000)]
    mean = statistics.fmean(runs)
    se = statistics.stdev(runs) / len(runs) ** 0.5
    assert abs(mean - 20.548) < 4 * se, (mean, se)


def test_simulation_big_bang():
    rng = random.Random(1)
    runs = [simulate_rollout(20_000, 0.01, 1.0, [1.0], rng) for _ in range(500)]
    assert 195 < statistics.fmean(runs) < 205


def test_canary():
    assert canary_size(1 / 5_000, 1.0) == 14_978
    assert canary_size(1 / 10_000, 0.5) == 59_914


def test_rollout_hours_and_best_plan():
    assert rollout_hours([1.0], 4) == 0 and rollout_hours([0.01, 0.1, 1.0], 4) == 8
    cands = [[1.0], [0.01, 0.10, 1.0], [0.01, 0.05, 0.25, 1.0], [0.01, 0.04, 0.15, 0.5, 1.0]]
    assert best_plan(N, P, 1.0, cands, 4, 8) == [0.01, 0.10, 1.0]
    assert best_plan(N, P, 1.0, cands, 4, 16) == [0.01, 0.04, 0.15, 0.5, 1.0]
    assert best_plan(N, P, 1.0, cands, 4, 0) == [1.0]


def test_hotfix_lecture():
    decision, wait, fix = hotfix_decision(400, 60, 10, 30_000, 0.10, 20_000)
    assert decision == "hotfix" and close(wait, 24_000) and close(fix, 7_000)
    assert hotfix_decision(20, 60, 10, 30_000, 0.10, 20_000)[0] == "wait"


def test_bug_queue():
    keys = ("harm_per_hour", "hours_to_patch", "restart_minutes", "ccu", "risk", "risk_harm")
    got = {b["bug_id"]: hotfix_decision(*[b[k] for k in keys])[0] for b in load_bugs()}
    assert got == {"B1": "hotfix", "B2": "wait", "B3": "hotfix",
                   "B4": "hotfix", "B5": "hotfix", "B6": "wait"}


TESTS = [test_reach, test_lecture_harm, test_simulation_matches_model, test_simulation_big_bang,
         test_canary, test_rollout_hours_and_best_plan, test_hotfix_lecture, test_bug_queue]

if __name__ == "__main__":
    failed = 0
    for t in TESTS:
        try:
            t()
            print(f"PASS {t.__name__}")
        except Exception as e:  # NotImplementedError, AssertionError, ...
            failed += 1
            print(f"FAIL {t.__name__}: {type(e).__name__} {e}")
    print(f"{len(TESTS) - failed}/{len(TESTS)} passed")
    sys.exit(1 if failed else 0)
