"""Tests for MMO403 Lab 13. Values come from the week 13 lecture.
Run with `python3 test_budget.py` (or `pytest test_budget.py`) from this folder."""
from budget import (burn_series, cash_out_month, contingency_months, crash_vs_slip,
                    load_plan, phase_burn, runway, slip, slip_cost)

PLAN = load_plan()
C, F = 10_000, 50_000
TOL = 1e-6


def test_phase_burn():
    assert phase_burn(45, C, F) == 500_000
    assert phase_burn(12, C, F) == 170_000
    assert phase_burn(0, C, F) == 50_000


def test_series_flat():
    s = burn_series(PLAN, C, F)
    assert len(s) == 30
    assert sum(s) == 13_920_000
    assert s[0] == 170_000 and s[6] == 500_000 and s[-1] == 650_000


def test_cash_out():
    assert cash_out_month(burn_series(PLAN, C, F), 15_000_000) is None
    assert cash_out_month(burn_series(slip(PLAN, "production", 3), C, F), 15_000_000) == 33
    assert cash_out_month(burn_series(slip(PLAN, "beta and launch", 3), C, F), 15_000_000) == 32
    assert cash_out_month([100, 100], 100) == 2   # spend must EXCEED cash


def test_slip_does_not_mutate():
    before = [tuple(r) for r in PLAN]
    slip(PLAN, "production", 3)
    assert [tuple(r) for r in PLAN] == before


def test_slip_cost():
    got = [slip_cost(PLAN, p, 3, C, F) for p in ("pre-production", "production", "beta and launch")]
    assert got == [510_000, 1_500_000, 1_950_000]


def test_ramp():
    s = burn_series(PLAN, C, F, ramp=3)
    heads = [round((b - F) / C, 6) for b in s[:12]]
    assert heads == [4, 8, 12, 12, 12, 12, 23, 34, 45, 45, 45, 45]
    assert abs(sum(s) - 13_320_000) < TOL
    assert len(s) == 30


def test_contingency_and_runway():
    assert abs(contingency_months(13_920_000, 0.20, 500_000) - 5.568) < TOL
    assert abs(contingency_months(13_920_000, 0.20, 650_000) - 4.2830769) < 1e-6
    series = [220_000] * 5 + [310_000] * 40      # check-yourself question 1
    assert abs(runway(6_000_000, series) - (5 + 4_900_000 / 310_000)) < TOL
    assert abs(runway(6_000_000, [220_000] * 40) - 6_000_000 / 220_000) < TOL


def test_crash_vs_slip():
    net, crash, slipped = crash_vs_slip(hires=15, months_left=12, ramp_months=3, ramp_eff=0.5,
                                        mentor_share=0.2, cost=C, phase_burn_now=500_000,
                                        slip_months=3)
    assert abs(net - 148.5) < TOL
    assert crash == 1_800_000 and slipped == 1_500_000


if __name__ == "__main__":
    import sys
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print("PASS", t.__name__)
        except Exception as e:  # noqa: BLE001
            failed += 1
            print("FAIL", t.__name__, "-", type(e).__name__, e)
    print(f"{len(tests) - failed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)
