"""MMO308 Lab 04 checker. Run after gen_log.py:  python check_lab04.py

Prints PASS, FAIL or TODO per function and exits non-zero unless all pass.
Expected values come from the seed-404 files; regenerate them with gen_log.py
if you edited the CSVs.
"""
import sys

import funnel as f

TOL = 1e-9
# numbers of players reaching chapters 1..8 (shares x n), from the seed-404 data
SNAP = (6000, [5774, 5014, 3712, 3148, 2670, 2270, 1928, 1674])
C30 = (4805, [4646, 3915, 2511, 1921, 1413, 929, 581, 340])
C60 = (3721, [3626, 3298, 2505, 2166, 1867, 1570, 1332, 1089])
CHURNED = {7: (3229, 9695651), 30: (2019, 6033324)}          # (count, sum of ids)
FALSE = {(7, "daily"): 0.005702066999287242, (7, "regular"): 0.10321324245374879,
         (7, "occasional"): 0.6420525657071339, (7, None): 0.19417776401362652,
         (14, "regular"): 0.008149010477299184, (14, "occasional"): 0.4723320158102767}


def close(a, b):
    return abs(a - b) <= TOL


def funnel_ok(got, want):
    n, shares = got
    return n == want[0] and len(shares) == len(want[1]) and all(
        close(s, c / want[0]) for s, c in zip(shares, want[1]))


def main():
    P, S, C = f.load()
    tests = {
        "step_conversions": lambda: (
            f.step_conversions([200, 150, 75, 60]) == [0.75, 0.5, 0.8]
            and f.step_conversions([10, 0, 0]) == [0.0, 0.0]),
        "snapshot_funnel": lambda: funnel_ok(f.snapshot_funnel(P, C), SNAP),
        "cohort_funnel (30-day box)": lambda: funnel_ok(f.cohort_funnel(P, C, 30), C30),
        "cohort_funnel (60-day box)": lambda: funnel_ok(f.cohort_funnel(P, C, 60), C60),
        "churned": lambda: all(
            (len(s := f.churned(P, S, W)), sum(s)) == want for W, want in CHURNED.items()),
        "false_churn_share": lambda: all(
            close(f.false_churn_share(P, S, W, cadence=c), v) for (W, c), v in FALSE.items()),
    }
    ok = True
    for name, test in tests.items():
        try:
            passed = test()
        except NotImplementedError:
            print(f"TODO {name}")
            ok = False
            continue
        except Exception as e:  # a crash is a failure, with the reason shown
            print(f"FAIL {name}: {type(e).__name__}: {e}")
            ok = False
            continue
        print(("PASS " if passed else "FAIL ") + name)
        ok = ok and passed
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
