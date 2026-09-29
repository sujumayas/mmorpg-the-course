"""Tests for MMO308 Lab 03. Values come from the week 3 lecture and a tiny log.
Run `python gen_cohorts.py` once, then `python test_retention.py`."""
from pathlib import Path

from retention import (calendar_index, checkpoint, cohort_sizes, cohort_table,
                       find_step, load_activity, load_installs, pooled)

HERE = Path(__file__).resolve().parent


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


# Tiny game: A, B, C, D install on day 0; E, F on day 1; G on day 2. Last day is 3.
INSTALLS = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 1, "F": 1, "G": 2}
ACTIVITY = {0: {"A", "B", "C", "D"}, 1: {"A", "B", "E", "F"},
            2: {"A", "E", "G"}, 3: {"A", "C", "F"}}


def test_sizes():
    assert cohort_sizes(INSTALLS) == {0: 4, 1: 2, 2: 1}


def test_table_by_hand():
    t = cohort_table(INSTALLS, ACTIVITY, last_day=3, max_age=3)
    assert t[0] == {0: 1.0, 1: 0.5, 2: 0.25, 3: 0.5}
    assert t[1] == {0: 1.0, 1: 0.5, 2: 0.5}
    assert t[2] == {0: 1.0, 1: 0.0}          # G missed day 3: a real zero, and complete
    assert 3 not in t                         # nobody installed on day 3


def test_incomplete_cells_left_out():
    t = cohort_table(INSTALLS, ACTIVITY, last_day=2, max_age=3)
    assert set(t[0]) == {0, 1, 2} and set(t[2]) == {0}


def test_checkpoint_and_pooled():
    t = cohort_table(INSTALLS, ACTIVITY, last_day=3, max_age=3)
    assert checkpoint(t, 1) == {0: 0.5, 1: 0.5, 2: 0.0}
    assert checkpoint(t, 3) == {0: 0.5}
    sizes = cohort_sizes(INSTALLS)
    assert close(pooled(t, sizes, 1, 0, 2), (2 + 1 + 0) / 7)
    assert pooled(t, sizes, 3, 1, 2) is None


def test_find_step_lecture_series():
    d7 = {c: (0.2251 if c < 20 else 0.1351) for c in range(0, 40)}
    c, diff = find_step(d7, window=5)
    assert c == 20 and abs(diff - (-0.09)) < 1e-9


def test_calendar_index_finds_outage():
    # the lecture's model, cohorts 0-50, ages 0-10, outage on day 40
    def R(c, a):
        if a == 0:
            return 1.0
        w = 0.15 if c >= 20 else 0.25
        r = w * 0.985 ** a + (1 - w) * 0.30 ** a
        return r * 0.4 if c + a == 40 else r
    table = {c: {a: R(c, a) for a in range(0, 11) if c + a <= 50} for c in range(0, 51)}
    idx = calendar_index(table)
    worst = min(idx, key=idx.get)
    assert worst == 40 and idx[40] < 0.5
    assert all(0.7 < v < 1.3 for t, v in idx.items() if t != 40)


def test_generated_data_shape():
    if not (HERE / "activity.csv").exists():
        raise AssertionError("run gen_cohorts.py first")
    installs, activity = load_installs(), load_activity()
    t = cohort_table(installs, activity)
    assert all(v[0] == 1.0 for v in t.values())
    assert max(c + max(v) for c, v in t.items()) == 89
    assert len(checkpoint(t, 30)) == 60


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
            except AssertionError as e:
                failed += 1
                print(f"FAIL {name} {e}")
    print("all tests pass" if not failed else f"{failed} test(s) not passing yet")
    raise SystemExit(1 if failed else 0)
