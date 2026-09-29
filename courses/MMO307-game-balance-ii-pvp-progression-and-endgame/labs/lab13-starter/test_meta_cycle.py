"""Lab 13 tests. Run with `pytest test_meta_cycle.py` or `python test_meta_cycle.py`.
All tests fail on the starter and pass on a correct solution."""
import math

from meta_cycle import (cycle_average, diversity_at, effective_number,
                        fit_tau, longest_period)

TOL = 1e-6


def test_effective_number():
    assert abs(effective_number([0.25] * 4) - 4) < TOL
    assert abs(effective_number([50, 50]) - 2) < TOL      # counts work too
    assert abs(effective_number([0.5, 0.3, 0.2]) - 1 / 0.38) < TOL
    assert effective_number([]) == 0.0


def test_diversity_at_lecture_table():
    # Lecture section 2: D_0 = 12, D_s = 4, tau = 7 days.
    assert abs(diversity_at(0, 12, 4, 7) - 12) < TOL
    assert abs(diversity_at(7, 12, 4, 7) - (4 + 8 / math.e)) < TOL
    assert abs(diversity_at(14, 12, 4, 7) - 5.0827) < 1e-4


def test_fit_tau_recovers_exact_model():
    days = [0, 3, 7, 14, 21, 28]
    div = [diversity_at(t, 12, 4, 7) for t in days]
    assert abs(fit_tau(days, div, 4) - 7) < TOL


def test_fit_tau_skips_points_at_or_below_ds():
    days = [0, 7, 14, 60]
    div = [diversity_at(t, 10, 3, 5) for t in days[:3]] + [2.9]
    assert abs(fit_tau(days, div, 3) - 5) < TOL


def test_cycle_average_lecture_values():
    assert abs(cycle_average(12, 4, 7, 14) - 7.4587) < 1e-4
    assert abs(cycle_average(12, 4, 7, 28) - 5.9634) < 1e-4
    # Very short cycles approach D_0, very long ones approach D_s.
    assert abs(cycle_average(12, 4, 7, 0.001) - 12) < 1e-3
    assert abs(cycle_average(12, 4, 7, 1e6) - 4) < 1e-3


def test_scale_invariance():
    # Only T / tau matters: halving tau is the same as doubling T.
    assert abs(cycle_average(12, 4, 3.5, 14) - cycle_average(12, 4, 7, 28)) < TOL


def test_longest_period():
    assert longest_period(12, 4, 7, 7.0) == 17
    assert longest_period(12, 4, 7, 12.5) == 0
    assert longest_period(12, 4, 7, 3.0) == 365


if __name__ == "__main__":
    failed = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print(f"PASS {name}")
            except Exception as exc:  # NotImplementedError counts as a failure
                failed += 1
                print(f"FAIL {name}: {type(exc).__name__} {exc}")
    raise SystemExit(1 if failed else 0)
