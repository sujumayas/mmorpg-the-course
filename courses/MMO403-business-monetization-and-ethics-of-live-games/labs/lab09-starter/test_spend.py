"""Tests for MMO403 Lab 09. Values come from the week 9 lecture and spend_month.csv.

Run with `.venv/bin/python test_spend.py` (exits 1 while any test fails)
or with pytest if you have it.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from spend import (alpha_from_top_share, cap_effect, gini, gini_identity, load,  # noqa: E402
                   lorenz, pareto_top_share, payer_rate, top_share)

TOY = [0] * 15 + [1, 2, 5, 12, 80]


def close(x, y, tol=1e-3):
    return abs(x - y) < tol


def test_toy_server():
    assert close(payer_rate(TOY), 0.25, 1e-12)
    assert close(gini([1, 2, 5, 12, 80]), 0.672)
    assert close(gini(TOY), 0.918)
    assert close(gini_identity(TOY), gini(TOY), 1e-12)
    assert gini([5, 5, 5]) == 0.0 and gini([0, 0]) == 0.0


def test_toy_lorenz_and_top():
    pts = lorenz(TOY)
    assert pts[0] == (0.0, 0.0) and close(pts[-1][1], 1.0, 1e-12) and len(pts) == 21
    assert close(pts[19][1], 0.20, 1e-12) and close(pts[18][1], 0.08, 1e-12)
    assert close(top_share(TOY, 0.05), 0.80, 1e-12)
    assert close(top_share(TOY, 0.10), 0.92, 1e-12)


def test_pareto_helpers():
    assert close(alpha_from_top_share(0.1, 0.5), 1.431, 1e-3)
    assert close(alpha_from_top_share(0.05, 0.5), 1.301, 1e-3)
    assert close(pareto_top_share(0.2, 2.0), 0.447, 1e-3)
    assert close(alpha_from_top_share(0.1, 0.6), 1.285, 1e-3)


def test_cap_effect():
    affected, lost = cap_effect([1, 2, 5, 12, 80], 10)
    assert close(affected, 0.4, 1e-12) and close(lost, 0.72, 1e-12)


def test_csv():
    s = load()
    pay = [x for x in s if x > 0]
    assert len(s) == 20_000 and close(payer_rate(s), 0.04, 1e-12)
    assert close(sum(pay), 12_870.79, 1e-6)
    assert close(gini(pay), 0.6322)
    assert close(gini(s), 0.9853)
    assert close(top_share(pay, 0.10), 0.5006)
    assert close(top_share(pay, 0.01), 0.1193)
    affected, lost = cap_effect(pay, 100)
    assert close(affected, 0.025) and close(lost, 0.0712)


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
