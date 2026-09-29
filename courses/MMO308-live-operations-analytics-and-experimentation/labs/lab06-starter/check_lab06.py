"""MMO308 Lab 06 checker. Run after gen_experiment.py:  python check_lab06.py

Exact functions are checked to 1e-9. Simulated ones are checked against ranges
wide enough for any correct implementation with 20,000 runs.
"""
import sys

import peeking as p

TOL = 1e-9


def close(a, b, tol=TOL):
    return abs(a - b) <= tol


def between(x, lo, hi):
    return lo <= x <= hi


TESTS = {
    "z_two_proportion": lambda: close(p.z_two_proportion(400, 1000, 440, 1000), 1.8122009407318735)
        and p.z_two_proportion(0, 10, 0, 10) == 0.0,
    "cumulative_z": lambda: (lambda z: len(z) == 14 and close(z[3], 2.2160043277966404)
                             and close(z[-1], 1.7957591814582545))(p.cumulative_z(p.load_rows())),
    "srm_pvalue": lambda: close(p.srm_pvalue(21055, 20280), 0.00013789663305392415)
        and close(p.srm_pvalue(90450, 9550, 0.1), 2.101435956012439e-06)
        and close(p.srm_pvalue(50000, 50000), 1.0),
    "obf_boundaries": lambda: all(close(a, b) for a, b in zip(
        p.obf_boundaries(2.024, 4), [4.048, 2.8623682502431445, 2.337113889679605, 2.024])),
    "stop_rate": lambda: between(p.stop_rate([1.96]), 0.043, 0.057)
        and between(p.stop_rate([1.96] * 14), 0.205, 0.237)
        and between(p.stop_rate([1.96], theta=2.8016), 0.785, 0.815),
    "find_constant": lambda: between(p.find_constant(5, "pocock"), 2.37, 2.46)
        and between(p.find_constant(5, "obf"), 1.99, 2.09),
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
