"""MMO405 Lab 07 checker. Run after gen_focal.py:  python check_lab07.py"""
import sys

import recording as r

TOL = 1e-9
LECTURE = [(3, 9), (31, 37), (58, 64), (95, 101)]


def close(a, b, tol=TOL):
    return abs(a - b) <= tol


TESTS = {
    "continuous_share": lambda: close(r.continuous_share(LECTURE, 120), 0.2)
        and close(r.continuous_share([], 60), 0.0),
    "scan_share": lambda: close(r.scan_share(LECTURE, 120, 5), 5 / 24)
        and close(r.scan_share(LECTURE, 120, 15), 1 / 8)
        and close(r.scan_share(LECTURE, 120, 15, offset=5), 3 / 8)
        and close(r.scan_share([(0, 1)], 10, 3, offset=1), 0.0),
    "scan_average": lambda: close(r.scan_average(LECTURE, 120, 15), 0.2)
        and close(r.scan_average(LECTURE, 120, 8), 0.2),
    "one_zero_share": lambda: close(r.one_zero_share(LECTURE, 120, 5), 8 / 24)
        and close(r.one_zero_share(LECTURE, 120, 15), 5 / 8)
        and close(r.one_zero_share([(14, 15)], 20, 15), 0.5)
        and close(r.one_zero_share([(15, 16)], 20, 15), 0.5)
        and close(r.one_zero_share([(10, 12)], 25, 10), 1 / 3),
    "one_zero_expected": lambda: close(r.one_zero_expected(4, 6, 15, 120), 0.7)
        and close(r.one_zero_expected(4, 6, 10, 120), 64 / 120)
        and close(r.one_zero_expected(10, 10, 15, 100), 1.0),
    "bias_factor": lambda: close(r.bias_factor(6, 15), 3.5)
        and close(r.bias_factor(20, 30), 2.5),
    "focal_log": lambda: close(
        sum(r.one_zero_share(b, r.L, 15) for b in r.load_log().values()), 3.5),
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
        except FileNotFoundError:
            print(f"FAIL {name}: run gen_focal.py first")
            ok = False
            continue
        except Exception as e:
            print(f"FAIL {name}: {type(e).__name__}: {e}")
            ok = False
            continue
        print(("PASS " if passed else "FAIL ") + name)
        ok = ok and passed
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
