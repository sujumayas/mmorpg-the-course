"""Tests for MMO406 Lab 14. Values come from the week 14 lecture and lab14.md.
Run with `.venv/bin/python test_lore_desk.py` (from any folder) or pytest.
Every test fails on the starter and passes on a correct lore_desk.py."""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from lore_desk import (answer_rate_for_wait, escalated_rate, gap_ranking,  # noqa: E402
                       load_log, min_answer_rate, score_questions, wait_days)


def close(a, b, tol=1e-3):
    return abs(a - b) < tol


def log():
    return load_log(os.path.join(HERE, "thornmere_questions.csv"))


def test_lecture_wait_table():
    assert close(escalated_rate(48, 0.7), 14.4)
    expected = {0.60: 6.25, 0.65: 1.5625, 0.70: 0.8929, 0.80: 0.4808, 0.85: 0.3906, 0.90: 0.3289}
    for a, days in expected.items():
        assert close(wait_days(48, 20, a), days), a
    assert wait_days(48, 20, 0.55) == math.inf
    assert wait_days(48, 20, 0.50) == math.inf


def test_expansion_doubles_team():
    assert wait_days(96, 20, 0.70) == math.inf
    assert close(wait_days(96, 20, 0.85), 0.8929)
    assert close(min_answer_rate(96, 20), 0.7917)
    assert close(answer_rate_for_wait(96, 20, 1), 0.84375)


def test_thresholds():
    assert close(min_answer_rate(48, 20), 0.5833)
    assert close(answer_rate_for_wait(48, 20, 1), 0.6875)
    assert close(answer_rate_for_wait(40, 15, 1), 0.75)
    assert min_answer_rate(10, 20) == 0.0
    assert answer_rate_for_wait(10, 20, 1) == 0.0
    assert answer_rate_for_wait(48, 4, 1) is None
    assert close(wait_days(48, 20, 0.7, days_per_week=7), 1.25)


def test_score_thornmere_log():
    s = score_questions(log())
    assert s["total"] == 40
    assert s["counts"] == {"answered": 20, "derivable": 6, "missing": 8,
                           "contradicted": 3, "reserved": 3}
    assert close(s["a"], 0.65)
    assert close(s["margin"], 0.1478)


def test_score_rejects_bad_input():
    bad = [{"id": "X1", "chapter": "history", "status": "maybe"}]
    for rows in (bad, []):
        try:
            score_questions(rows)
        except ValueError:
            continue
        raise AssertionError("score_questions accepted bad input")


def test_gap_ranking():
    assert gap_ranking(log()) == [("religion", 5), ("factions", 3), ("history", 3),
                                  ("geography", 2), ("community", 1)]
    rows = [{"chapter": "b", "status": "reserved"}, {"chapter": "a", "status": "answered"}]
    assert gap_ranking(rows) == []


if __name__ == "__main__":
    failed = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print(f"PASS {name}")
            except NotImplementedError as e:
                failed += 1
                print(f"TODO {name}: {e}")
            except AssertionError:
                failed += 1
                print(f"FAIL {name}")
    print(f"\n{failed} test(s) not passing" if failed else "\nAll tests pass.")
    sys.exit(1 if failed else 0)
