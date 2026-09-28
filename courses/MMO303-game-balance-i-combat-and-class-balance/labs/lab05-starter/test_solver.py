"""Tests for Lab 05. Values come from the week 5 lecture and lab05.md.
Run with `python3 test_solver.py` or `pytest test_solver.py`."""
from dataclasses import replace

from composition_solver import DEFAULT, check, compositions, load_roles, passing, target

ROLES = load_roles()


def test_count():
    assert len(compositions(5)) == 21
    assert len(set(compositions(5))) == 21
    assert all(sum(g) == 5 for g in compositions(5))


def test_target_rule():
    assert target((1, 1, 3), ROLES).name == "tank"
    assert target((0, 1, 4), ROLES).m == 0.20


def test_default_encounter():
    assert passing(DEFAULT, ROLES) == [(1, 1, 3)]


def test_default_margins():
    r = check((1, 1, 3), DEFAULT, ROLES)
    assert abs(r["damage"] - (3_500 - 600_000 / 180)) < 1e-6
    assert abs(r["healing"] - 100) < 1e-6   # 700 - (1,000 x 0.4 + 200)
    assert abs(r["spike"] - 4_000) < 1e-6   # 6,000 - 5,000 x 0.4


def test_lighter_boss():
    enc = replace(DEFAULT, B=500, S=3_500)
    assert sorted(passing(enc, ROLES)) == [(0, 1, 4), (1, 1, 3)]


def test_heavy_boss():
    assert passing(replace(DEFAULT, B=1_500), ROLES) == []


def test_spike_is_strict():
    # A DPS target with 3,000 health survives 3,749 raw but not exactly 3,750.
    enc = replace(DEFAULT, B=500)
    assert check((0, 1, 4), replace(enc, S=3_749), ROLES)["spike"] > 0
    r = check((0, 1, 4), replace(enc, S=3_750), ROLES)
    assert r["spike"] == 0 and r["passes"] is False


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
    print("all tests pass" if not failed else f"{failed} test(s) not passing yet")
