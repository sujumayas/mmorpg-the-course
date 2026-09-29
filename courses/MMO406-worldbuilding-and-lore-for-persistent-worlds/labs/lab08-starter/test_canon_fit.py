"""Tests for Lab 08. Values come from the week 8 lecture and its interactive spec.
Run with ../../../../.venv/bin/python test_canon_fit.py (or pytest)."""
from canon_fit import (best_honor_set, dissonance_bits, distribution, expected_contradictions,
                       fit, load_choices, mixture_distribution, mixture_fit, per_type_expected,
                       take_rates)

PS = [0.90, 0.75, 0.60, 0.55, 0.50]
LOYAL_REBEL = [(0.6, [0.9] * 5), (0.4, [0.3] * 5)]


def close(x, y, tol=1e-3):
    return abs(x - y) < tol


def test_fit_and_expected():
    assert close(fit(PS), 0.111375, 1e-9)
    assert close(expected_contradictions(PS), 1.70, 1e-9)
    assert close(fit(PS, (3, 4)), 0.405, 1e-9) and close(fit(PS, (0, 1)), 0.165, 1e-9)
    assert close(expected_contradictions(PS, (3, 4)), 0.75, 1e-9)
    assert fit(PS, range(5)) == 1.0 and expected_contradictions(PS, range(5)) == 0


def test_distribution():
    want = [0.111, 0.326, 0.353, 0.171, 0.035, 0.002]
    got = distribution(PS)
    assert len(got) == 6 and all(close(g, w) for g, w in zip(got, want))
    assert close(sum(got), 1.0, 1e-9)
    assert [round(x, 3) for x in distribution(PS, (0, 1))] == [0.165, 0.41, 0.335, 0.09]


def test_bits():
    assert close(dissonance_bits(PS), 3.1665)
    assert close(2 ** -dissonance_bits(PS), fit(PS), 1e-9)


def test_best_honor_set():
    assert best_honor_set(PS, 2) == (3, 4)
    assert best_honor_set([0.7, 0.6, 0.6, 0.9], 1) == (1,)
    assert best_honor_set(PS, 0) == ()


def test_mixture():
    assert all(close(p, 0.66, 1e-9) for p in take_rates(LOYAL_REBEL))
    assert close(mixture_fit(LOYAL_REBEL), 0.355266, 1e-6)
    assert close(fit(take_rates(LOYAL_REBEL)), 0.1252, 1e-4)
    d = mixture_distribution(LOYAL_REBEL)
    assert len(d) == 6 and close(sum(d), 1.0, 1e-9) and close(d[5], 0.0672)
    assert close(mixture_fit([(0.7, [0.8] * 3), (0.3, [0.2] * 3)]), 0.3608, 1e-6)


def test_per_type():
    assert [round(x, 6) for x in per_type_expected(LOYAL_REBEL)] == [0.5, 3.5]
    mixed = [(0.6, [0.9, 0.9, 0.9, 0.3, 0.3]), (0.4, [0.3, 0.3, 0.3, 0.9, 0.9])]
    assert [round(x, 6) for x in per_type_expected(mixed)] == [1.7, 2.3]
    assert close(mixture_fit(mixed), 0.048114, 1e-6)


def test_load_choices():
    rows = load_choices()
    assert len(rows) == 5 and rows[4] == ("Free the prisoner or not", 0.5)


if __name__ == "__main__":
    import sys
    failed = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print("PASS", name)
            except Exception as e:  # noqa: BLE001
                failed += 1
                print("FAIL", name, type(e).__name__, e)
    print(f"{failed} failed")
    sys.exit(1 if failed else 0)
