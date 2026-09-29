"""Tests for MMO403 Lab 08. Values come from the week 8 lecture.

Run with `.venv/bin/python test_friction.py` (exits 1 while any test fails)
or with pytest if you have it.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from friction import (DEFAULTS, accidental, arpu, asymmetry, best_wait,  # noqa: E402
                      completion, lifetime, lifetime_lost, ltv, pay, retention, sweep)


def close(x, y, tol=1e-2):
    return abs(x - y) < tol


def test_components_at_two_hours():
    assert close(pay(2), 0.05, 1e-9)
    assert close(retention(2), 0.86, 1e-9)
    assert close(arpu(2), 1.50, 1e-9)
    assert close(lifetime(2), 1 / 0.14, 1e-9)


def test_table():
    expected = {0: (5.00, 10.00), 1: (9.55, 8.18), 2: (10.71, 7.14), 3.5: (11.02, 6.22),
                6: (10.77, 5.38), 12: (10.06, 4.55), 24: (9.38, 4.00)}
    for w, (v, life) in expected.items():
        assert close(ltv(w), v, 0.006) and close(lifetime(w), life, 0.006), w


def test_peak():
    w, v = best_wait()
    assert close(w, 3.46, 1e-9) and close(v, 11.02, 0.005)
    assert close(lifetime_lost(), 0.376, 0.001)


def test_sensitivity():
    q = dict(DEFAULTS, d=0.10)
    w, v = best_wait(q)
    assert close(w, 6.90, 0.02) and close(v, 14.02, 0.01)
    q = dict(DEFAULTS, A0=1.00)
    w, _ = best_wait(q)
    assert close(w, 2.31, 0.02)
    rows = sweep("s", [1.0, 2.0])
    assert close(rows[1][1], 4.32, 0.02) and close(rows[1][2], 19.01, 0.01)


def test_asymmetry():
    assert close(completion(0.85, 6), 0.377, 1e-3)
    assert close(asymmetry(0.85, 1, 6), 2.25, 1e-2)
    assert close(asymmetry(0.9, 2, 7), 0.9 ** -5, 1e-9)
    assert close(accidental(1000, 0.02, 0.0), 20, 1e-9)
    assert close(accidental(1000, 0.02, 0.9), 2, 1e-9)


TESTS = [v for k, v in dict(globals()).items() if k.startswith("test_")]

if __name__ == "__main__":
    failed = 0
    for t in TESTS:
        try:
            t()
            print("PASS", t.__name__)
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print("FAIL", t.__name__, type(exc).__name__, exc)
    print(f"{len(TESTS) - failed}/{len(TESTS)} passed")
    sys.exit(1 if failed else 0)
