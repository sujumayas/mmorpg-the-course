"""Tests for Lab 07, from the week 7 lecture.
Run with `python test_split_tuning.py` or `pytest test_split_tuning.py`."""
from split_tuning import (ROSTER, audit, burst_multiplier, clone, pve_dps,
                          pvp_ttk, sustain_multiplier)


def near(a, b, tol=1e-6):
    return abs(a - b) <= tol


def test_lecture_table():
    assert near(pve_dps(900, 12_000), 1_100)
    assert near(pve_dps(700, 18_000), 1_000)
    assert round(pvp_ttk(900, 12_000), 1) == 20.0
    assert round(pvp_ttk(700, 24_000), 1) == 8.6
    assert round(pvp_ttk(1_050, 3_000), 1) == 25.7


def test_burst_can_one_shot():
    assert pvp_ttk(600, 30_000) == 0
    assert pvp_ttk(600, 40_000) == 0


def test_multipliers_in_ttk():
    assert round(pvp_ttk(700, 24_000, p=0.8), 1) == 15.4
    assert round(pvp_ttk(1_050, 3_000, q=1.2), 1) == 21.4
    assert round(pvp_ttk(700, 24_000, h=4.35), 1) == 152.1


def test_clone():
    s, B = clone(1_100, 20)
    assert near(s, 900) and near(B, 12_000)
    s, B = clone(1_100, 22)
    assert round(s, 1) == 947.4 and round(B) == 9_158


def test_inverse_multipliers():
    assert near(burst_multiplier(700, 24_000, 15), 0.8125)
    assert near(sustain_multiplier(1_050, 3_000, 22), 27_000 / 23_100)
    p = burst_multiplier(600, 30_000, 15)
    assert near(pvp_ttk(600, 30_000, p=p), 15)


def test_audit():
    report = audit(ROSTER)
    assert report["Duelist"] == []
    assert report["Ravager"] == ["pvp"]
    assert report["Channeler"] == ["pvp"]
    fixed = audit({"Ravager": (700, 24_000)}, splits={"Ravager": {"p": 0.8}})
    assert fixed["Ravager"] == []
    worse = audit({"Ravager": (700, 18_000)})
    assert worse["Ravager"] == ["pve"]


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
    raise SystemExit(1 if failed else 0)
