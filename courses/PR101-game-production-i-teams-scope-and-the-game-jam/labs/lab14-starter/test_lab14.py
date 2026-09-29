"""PR101 lab 14 tests. Run: python test_lab14.py

Plain asserts, no packages. Each test prints PASS or FAIL with a reason.
"""
from pathlib import Path

import postmortem_tools as T

HERE = Path(__file__).resolve().parent
TYPES = T.load_counts(HERE / "politowski_types.csv")
TEAM = T.load_problems(HERE / "example_team.csv")


def close(a, b, tol=1e-3):
    return abs(a - b) < tol


def test_count_by_category():
    jam = T.count_by_category(TEAM, "jam")
    assert jam == {"scope": 2, "planning": 1, "communication": 1, "bugs": 1, "crunch time": 1}, jam
    final = T.count_by_category(TEAM, "final")
    assert final == {"planning": 2, "testing": 1, "communication": 1, "tools": 1}, final


def test_pareto_order_and_shares():
    rows = T.pareto(TYPES)
    assert len(rows) == 20, len(rows)
    assert rows[0][0] == "technical" and close(rows[0][2], 0.1251), rows[0]
    assert close(rows[3][3], 0.4164), f"cumulative after 4 should be 41.6%, got {rows[3][3]}"
    assert close(rows[-1][3], 1.0), rows[-1]
    names = [r[0] for r in rows]
    assert names.index("bugs") < names.index("scope"), "ties must be broken alphabetically"


def test_pareto_small_and_ties():
    rows = T.pareto({"tools": 3, "scope": 3, "communication": 2, "testing": 1, "bugs": 1, "art": 0})
    assert [r[0] for r in rows] == ["scope", "tools", "communication", "bugs", "testing"], rows
    assert [round(r[3], 2) for r in rows] == [0.3, 0.6, 0.8, 0.9, 1.0], rows
    assert T.pareto({}) == [], "empty counts should give no rows"


def test_vital_few():
    assert T.vital_few(T.pareto(TYPES)) == 12, T.vital_few(T.pareto(TYPES))
    team = {"scope": 12, "communication": 9, "tools": 6, "bugs": 5,
            "planning": 4, "audio": 2, "documentation": 2}
    assert T.vital_few(T.pareto(team)) == 4, "exactly 80% must count as reaching 80%"
    assert T.vital_few(T.pareto(team), 0.5) == 2, T.vital_few(T.pareto(team), 0.5)
    assert T.vital_few([]) == 0


def test_recurrence():
    r, repeated = T.recurrence(TEAM, "jam", "final")
    assert close(r, 0.4), r
    assert repeated == ["communication", "planning"], repeated
    r2, rep2 = T.recurrence(TEAM, "final", "jam")
    assert close(r2, 0.5), f"final -> jam: 2 of 4 categories, got {r2}"
    assert T.recurrence(TEAM, "nope", "final") == (0.0, [])


def test_closure():
    rate, still_open = T.closure(TEAM, "jam")
    assert close(rate, 0.6), f"3 of 5 distinct items are done, got {rate}"
    assert still_open == ["Estimate better", "Talk more"], still_open
    assert T.closure(TEAM, "final") == (0.0, []), "no action items yet in final"


TESTS = [v for k, v in dict(globals()).items() if k.startswith("test_")]

if __name__ == "__main__":
    passed = 0
    for t in TESTS:
        try:
            t()
            print(f"PASS {t.__name__}")
            passed += 1
        except Exception as err:  # report and keep going
            print(f"FAIL {t.__name__}: {type(err).__name__}: {err}")
    print(f"{passed}/{len(TESTS)} tests passed")
    raise SystemExit(0 if passed == len(TESTS) else 1)
