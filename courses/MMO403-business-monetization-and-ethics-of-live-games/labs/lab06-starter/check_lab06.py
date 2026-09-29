"""MMO403 Lab 06 checker:  python check_lab06.py   (takes about 10 seconds)"""
import sys

import lootbox as lb


def close(a, b, tol):
    return abs(a - b) <= tol


def t_sim():
    ok = True
    for prot, pity, target in ((False, None, 120.55), (True, None, 103.22),
                               (False, 40, 69.70), (True, 40, 36.61)):
        s = lb.simulate(lb.SET, prot, pity, trials=10_000, seed=406)
        ok = ok and len(s) == 10_000 and close(sum(s) / len(s), target, 0.03 * target)
    s = lb.simulate(lb.SET, True, 40, trials=2_000, seed=1)
    return ok and lb.summarize(s)[2] == 40


TESTS = {
    "expected_boxes": lambda: close(lb.expected_boxes([(20, 0.05)]), 71.9548, 1e-3)
        and close(lb.expected_boxes(lb.SET), 120.5453, 1e-3),
    "p_complete": lambda: close(lb.p_complete(90, lb.SET), 0.5, 0.02)
        and lb.p_complete(89, lb.SET) < 0.5 <= lb.p_complete(90, lb.SET)
        and close(lb.p_complete(0, lb.SET), 0.0, 1e-9),
    "protected_cdf": lambda: (lambda c: len(c) == 3001 and close(c[19], 0.0, 1e-12)
        and c[70] >= 0.5 > c[69] and c[230] >= 0.9 > c[229])(lb.protected_cdf(lb.SET, 3000)),
    "mean_from_cdf": lambda: close(lb.mean_from_cdf([0, 0, 1]), 2.0, 1e-12)
        and close(lb.mean_from_cdf([0, 0.5, 1]), 1.5, 1e-12),
    "percentile_from_cdf": lambda: lb.percentile_from_cdf([0, 0.2, 0.6, 0.95, 1], 0.5) == 2
        and lb.percentile_from_cdf([0, 0.2, 0.6, 0.95, 1], 0.9) == 3,
    "summarize": lambda: lb.summarize([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) == (5.5, 5, 9),
    "box_price_in_money": lambda: close(lb.box_price_in_money(150, 1000, 9.99), 1.4985, 1e-9),
    "simulate": t_sim,
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
