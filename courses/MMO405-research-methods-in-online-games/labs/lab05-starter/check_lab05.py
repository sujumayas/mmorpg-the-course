"""MMO405 Lab 05 checker. Run after gen_panel.py:  python check_lab05.py"""
import sys

import did as d

TOL = 1e-9
_cache = {}


def close(a, b, tol=TOL):
    return abs(a - b) <= tol


def series():
    if not _cache:
        rows = d.load_panel()
        _cache["m"] = d.weekly_share(rows, {"under18"})
        _cache["y"] = d.weekly_share(rows, {"18-24"})
        _cache["o"] = d.weekly_share(rows, {"25plus"})
        _cache["p"] = d.weekly_share(rows, {"under18", "18-24", "25plus"})
    return _cache


TOY_T = {-8: 5.0, -7: 5.0, -6: 5.0, -5: 5.0, -4: 6.0, -3: 6.0, -2: 6.0, -1: 6.0,
         0: 4.0, 1: 4.0, 2: 4.0, 3: 4.0}
TOY_C = {w: 2.0 + (1.0 if w >= 0 else 0.0) for w in range(-8, 4)}

TESTS = {
    "weekly_share": lambda: d.weekly_share(
        [(1, "a", 0, 1), (2, "a", 0, 0), (3, "b", 0, 1), (1, "a", 1, 0), (2, "a", 1, 0)],
        {"a"}) == {0: 50.0, 1: 0.0}
        and close(series()["m"][-8], 3.7446424543198735)
        and close(series()["o"][0], 3.883436326184418),
    "window_mean": lambda: close(d.window_mean({1: 2.0, 2: 4.0, 3: 9.0}, [1, 2]), 3.0)
        and close(d.window_mean(series()["p"], d.PRE), 3.0433333333333334),
    "did": lambda: close(d.did(TOY_T, TOY_C), -3.0)
        and close(d.did(series()["m"], series()["o"]), -1.958322054973126)
        and close(d.did(series()["m"], series()["y"]), -2.8271885470941327),
    "placebo_did": lambda: close(d.placebo_did(TOY_T, TOY_C), 1.0)
        and close(d.placebo_did(series()["m"], series()["y"]), -1.0028194372388386),
    "odds_ratio": lambda: close(d.odds_ratio(0.0077, 0.0088), 1.144125446788885)
        and close(d.odds_ratio(0.5, 0.5), 1.0),
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
