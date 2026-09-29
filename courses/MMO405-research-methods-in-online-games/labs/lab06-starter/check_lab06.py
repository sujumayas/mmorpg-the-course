"""MMO405 Lab 06 checker:  python check_lab06.py"""
import sys

import agree as g

TOL = 1e-9


def close(a, b, tol=TOL):
    return abs(a - b) <= tol


def prior(stem):
    c = g.load_codes()
    return g.table_2x2(c[stem + "_a"], c[stem + "_b"])


TESTS = {
    "table_2x2": lambda: g.table_2x2([1, 1, 0, 0, 1], [1, 0, 1, 0, 1]) == (2, 1, 1, 1)
        and prior("harassment") == (1, 2, 1, 36) and prior("schedule") == (12, 2, 1, 25),
    "percent_agreement": lambda: close(g.percent_agreement(45, 5, 5, 45), 0.9)
        and close(g.percent_agreement(*prior("harassment")), 0.925),
    "cohen_kappa": lambda: close(g.cohen_kappa(45, 5, 5, 45), 0.8)
        and close(g.cohen_kappa(0, 5, 5, 90), -0.05263157894736842)
        and close(g.cohen_kappa(75, 15, 5, 5), 0.23076923076923078)
        and close(g.cohen_kappa(*prior("schedule")), 0.8324022346368716)
        and g.cohen_kappa(0, 0, 0, 10) == 1.0,
    "specific_agreement": lambda: g.specific_agreement(0, 5, 5, 90)[0] == 0.0
        and close(g.specific_agreement(0, 5, 5, 90)[1], 180 / 190)
        and close(g.specific_agreement(*prior("harassment"))[0], 0.4)
        and g.specific_agreement(0, 0, 0, 10)[0] is None,
    "pabak": lambda: close(g.pabak(0, 5, 5, 90), 0.8)
        and close(g.pabak(*prior("schedule")), 0.85),
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
        except Exception as e:
            print(f"FAIL {name}: {type(e).__name__}: {e}")
            ok = False
            continue
        print(("PASS " if passed else "FAIL ") + name)
        ok = ok and passed
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
