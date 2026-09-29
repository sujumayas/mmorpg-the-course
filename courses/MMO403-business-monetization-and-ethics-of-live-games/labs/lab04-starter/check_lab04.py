"""MMO403 Lab 04 checker:  python check_lab04.py"""
import sys

import edge as e

TOL = 1e-3


def close(a, b, tol=TOL):
    return abs(a - b) <= tol


TESTS = {
    "win_prob": lambda: close(e.win_prob(0.10, 0.25), 0.60630, 1e-4)
        and close(e.win_prob(0.05, 0.10), 0.63499, 1e-4)
        and close(e.win_prob(0.0, 0.3), 0.5, 1e-12),
    "rating_gap": lambda: close(e.rating_gap(0.75), 190.849, 1e-2)
        and close(e.rating_gap(0.5), 0.0, 1e-12),
    "top_cutoff": lambda: close(e.top_cutoff(0.0, 0.2), 256.31, 0.05)
        and close(e.top_cutoff(75.0, 0.2), 274.29, 0.05),
    "payer_share_on_top": lambda: close(e.payer_share_on_top(0.0, 0.2), 0.2, 1e-6)
        and close(e.payer_share_on_top(74.99, 0.2), 0.3189, 1e-3)
        and close(e.payer_share_on_top(74.99, 0.2, top=0.01), 0.3979, 1e-3),
    "unranked_win_rates": lambda: all(close(x, y, 1e-4) for x, y in
        zip(e.unranked_win_rates(0.6063, 0.2), (0.58504, 0.47874))),
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
        except Exception as ex:
            print(f"FAIL {name}: {type(ex).__name__}: {ex}")
            ok = False
            continue
        print(("PASS " if passed else "FAIL ") + name)
        ok = ok and passed
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
