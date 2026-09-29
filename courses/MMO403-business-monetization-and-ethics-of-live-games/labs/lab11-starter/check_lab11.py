"""MMO403 Lab 11 checker. Run after gen_players.py:  python check_lab11.py

Prints PASS, FAIL or TODO for each function. Values are checked to 1e-9.
"""
import sys

import tokens as t

TOL = 1e-9


def close(a, b, tol=TOL):
    return abs(a - b) <= tol * max(1.0, abs(b))


TINY = [(20.0, 300_000), (10.0, 300_000), (20.0, 1_000), (5.0, 1_000)]


def simulate_ok():
    small = t.simulate(TINY, 15.0, 20.0, 100_000)
    want = {"cash": 1, "token": 2, "churn": 1, "cash_off": 2, "churn_off": 2,
            "k": 0.5, "revenue_on": 55.0, "revenue_off": 30.0, "gain": 25.0}
    if any(not close(small[key], val) for key, val in want.items()):
        return False
    big = t.simulate(t.load_players(), 15.0, 20.0, 100_000, 0.5, 0.3)
    return (big["token"] == 5576 and big["cash"] == 25254 and big["churn_off"] == 23620
            and close(big["k"], 0.20193687230989957) and close(big["gain"], 61174.0))


TESTS = {
    "token_gain": lambda: close(t.token_gain(100_000, 20.0, 15.0, 0.5, 0.3), 650_000.0)
        and close(t.token_gain(100_000, 20.0, 15.0, 1.0, 0.6), -700_000.0),
    "breakeven_sigma": lambda: close(t.breakeven_sigma(20.0, 15.0, 0.5), 0.625)
        and close(t.breakeven_sigma(20.0, 15.0, 0.0), 1.0),
    "blended_rate": lambda: close(t.blended_rate(900_000, 15.0, 100_000, 20.0), 15.5)
        and t.blended_rate(0, 15.0, 0, 20.0) == 0.0,
    "classify": lambda: t.classify(20.0, 300_000, 15.0, 100_000, 0.5, True) == "token"
        and t.classify(20.0, 300_000, 15.0, 100_000, 0.5, False) == "cash"
        and t.classify(10.0, 150_000, 15.0, 100_000, 0.5, True) == "churn"
        and t.classify(15.0, 0, 15.0, 100_000, 0.5, True) == "cash",
    "simulate": simulate_ok,
}


def main():
    ok = True
    for name, test in TESTS.items():
        try:
            passed = bool(test())
        except NotImplementedError:
            print(f"TODO {name}")
            ok = False
            continue
        except Exception as e:  # noqa: BLE001
            print(f"FAIL {name}: {type(e).__name__}: {e}")
            ok = False
            continue
        print(("PASS " if passed else "FAIL ") + name)
        ok = ok and passed
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
