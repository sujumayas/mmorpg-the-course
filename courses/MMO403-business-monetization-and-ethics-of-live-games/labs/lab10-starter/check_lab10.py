"""MMO403 Lab 10 checker. Run after gen_price_test.py:  python check_lab10.py

Prints PASS, FAIL or TODO for each function. Values are checked to 1e-9.
"""
import sys

import pricing as p

TOL = 1e-9


def close(a, b, tol=TOL):
    return abs(a - b) <= tol * max(1.0, abs(b))


def summary_ok():
    s = p.summarize(p.load_rows())
    return (sorted(s) == ["A", "B", "C"] and s["A"]["buyers"] == 603 and s["B"]["n"] == 11937
            and close(s["B"]["rpe"], 0.27756220155818045)
            and close(s["C"]["store_rpe"], 0.7259239130434783))


TESTS = {
    "rpe": lambda: close(p.rpe(6.99, 0.04), 0.2796),
    "breakeven_conversion": lambda: close(p.breakeven_conversion(4.99, 0.05, 6.99), 0.035693848354792564),
    "arc_elasticity": lambda: close(p.arc_elasticity(9.99, 0.02, 7.99, 0.024), -0.8172727272727274),
    "n_per_arm_rate": lambda: close(p.n_per_arm_rate(0.05, 0.04), 6742.258839039998),
    "n_per_arm_revenue": lambda: close(p.n_per_arm_revenue(4.99, 0.05, 6.99, 0.04), 26500.63445282265),
    "welch_z": lambda: close(p.welch_z([1.0, 2.0, 3.0], [2.0, 4.0, 6.0, 8.0]), 2.1213203435596424)
        and close(p.welch_z([0, 1, 0, 1], [1, 1, 0, 1]), 0.6546536707079772)
        and p.welch_z([1.0, 1.0], [1.0, 1.0]) == 0.0,
    "cap_values": lambda: p.cap_values([5.0, 25.0, 99.99, 0.0], 20.0) == [5.0, 20.0, 20.0, 0.0],
    "summarize": summary_ok,
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
