"""Tests for MMO406 Lab 10. Values come from the week 10 lecture and lab10.md.
Run with `.venv/bin/python test_foreshadow.py` (from any folder) or pytest.
Every test fails on the starter and passes on a correct foreshadow.py."""
import copy
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from foreshadow import audit, best_horizon, best_whole, expected_value  # noqa: E402


def close(a, b, tol=1e-6):
    return abs(a - b) <= tol


def load_plan():
    with open(os.path.join(HERE, "thornmere_plan.json")) as f:
        return json.load(f)


def test_expected_value_lecture_table():
    assert close(expected_value(0, 1, 2, 0.2), 0.0)
    assert close(expected_value(2, 1, 2, 0.2), 0.56)
    assert close(expected_value(8, 1, 2, 0.1), 2.30467, 1e-4)
    assert close(expected_value(1, 1, 2, 0.3), 0.10)
    assert close(expected_value(4, 1, 0.5, 0.2), 1.3432, 1e-6)


def test_best_horizon():
    assert close(best_horizon(1, 2, 0.1), 7.4910, 1e-3)
    assert close(best_horizon(1, 2, 0.2), 2.4814, 1e-3)
    assert close(best_horizon(2, 2, 0.2), 3.4814, 1e-3)
    assert best_horizon(1, 4, 0.3) == 0.0  # floored at zero


def test_best_whole_breaks_ties_low():
    d, e = best_whole(1, 2, 0.2)
    assert d == 2 and close(e, 0.56)
    d, e = best_whole(1, 0, 0.25)       # E(3) == E(4) == 1.265625
    assert d == 3 and close(e, 1.265625)
    d, e = best_whole(1, 4, 0.2)        # E(0) == E(1) == 0
    assert d == 0 and close(e, 0.0)


def test_audit_statuses_on_thornmere():
    rows = {r["id"]: r for r in audit(load_plan())}
    expected = {"H1": "ok", "H2": "too early", "H3": "too early", "H4": "too late",
                "H5": "ok", "H6": "ok", "H7": "too late"}
    assert {k: rows[k]["status"] for k in expected} == expected
    assert [r["id"] for r in audit(load_plan())] == sorted(expected)


def test_audit_numbers_and_negative_flag():
    rows = {r["id"]: r for r in audit(load_plan())}
    assert rows["H3"]["d"] == 3 and close(rows["H3"]["D"], 4.0)
    assert close(rows["H3"]["E"], 0.512 * 3 - 0.488 * 4)
    assert rows["H3"]["negative"] is True
    assert rows["H1"]["negative"] is False
    assert close(rows["H4"]["E"], 0.0) and rows["H4"]["d"] == 0


def test_audit_rejects_bad_plans():
    for mutate in (
        lambda p: p.update(rho=0),
        lambda p: p.update(rho=1),
        lambda p: p.update(v=0),
        lambda p: p["hooks"][0].update(type="whispered"),
        lambda p: p["hooks"][0].update(planted=3, payoff=1),
    ):
        plan = load_plan()
        mutate(plan)
        try:
            audit(plan)
        except ValueError:
            continue
        raise AssertionError("audit accepted a bad plan")


def test_audit_does_not_modify_plan():
    plan = load_plan()
    before = copy.deepcopy(plan)
    audit(plan)
    assert plan == before


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
