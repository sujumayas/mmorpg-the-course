"""MMO405 Lab 04 checker. Run after gen_survey.py:  python check_lab04.py"""
import sys

import scale as s

TOL = 1e-9


def close(a, b, tol=TOL):
    return abs(a - b) <= tol


def survey():
    return s.load_survey()[1]


TESTS = {
    "reverse_code": lambda: s.reverse_code([1, 4, 7, 2]) == [7, 4, 1, 6]
        and s.reverse_code([0, 4], lo=0, hi=4) == [4, 0],
    "variance": lambda: close(s.variance([2, 4, 4, 4, 5, 5, 7, 9]), 32 / 7),
    "pearson": lambda: close(s.pearson([1, 2, 3], [2, 4, 6]), 1.0)
        and close(s.pearson([1, 2, 3], [3, 2, 1]), -1.0)
        and close(s.pearson([1, 2, 3, 4], [1, 3, 2, 4]), 0.8),
    "cronbach_alpha": lambda: close(s.cronbach_alpha([[1, 2, 3, 4], [2, 3, 4, 5]]), 1.0)
        and close(s.cronbach_alpha(survey()), 0.44022980275935397),
    "standardized_alpha": lambda: close(s.standardized_alpha(10, 0.3), 3 / 3.7)
        and close(s.standardized_alpha(12, 0.6 * 30 / 66), 0.8181818181818182),
    "mean_interitem_r": lambda: close(s.mean_interitem_r(survey()), 0.07182530699730189),
    "corrected_item_total": lambda: close(
        s.corrected_item_total(survey())[3], -0.5211020112504727)
        and close(s.corrected_item_total(survey())[0], 0.37861242364073155),
    "alpha_if_deleted": lambda: close(s.alpha_if_deleted(survey())[3], 0.6263668887378901),
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
