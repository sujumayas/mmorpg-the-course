"""Checker for GD201 Lab 03. Do not edit. Run: python check_lab03.py"""
import sys

import intensity as m

B = [0, 5, 10, 15, 20, 30, 40, 0, 0, 0, 0, 5, 10, 15, 30, 0, 0, 0]


def close(got, want, tol=0.01):
    if isinstance(want, dict):
        return all(close(got[k], v, tol) for k, v in want.items())
    if isinstance(want, list):
        return len(got) == len(want) and all(close(g, w, tol) for g, w in zip(got, want))
    return abs(got - want) <= tol


CHECKS = [
    ("intensity_curve([30, 0, 0, 30]) == [30, 15, 7.5, 33.75]",
     lambda: m.intensity_curve([30, 0, 0, 30]), [30, 15, 7.5, 33.75]),
    ("drip of 10 settles at 20.0", lambda: m.intensity_curve([10] * 18)[-1], 20.0),
    ("intensity_curve with d=0.8: [10, 0] -> [10, 8]", lambda: m.intensity_curve([10, 0], d=0.8), [10, 8]),
    ("measure(design B)", lambda: m.measure(m.intensity_curve(B)),
     {"max": 62.66, "peak_s": 30, "calm_s": 60, "peaks": 2}),
    ("measure(drip)", lambda: m.measure(m.intensity_curve([10] * 18)),
     {"max": 20.0, "peak_s": 0, "calm_s": 0, "peaks": 0}),
    ("director(18) == [20, 20, 20, 0, 0, 0] x 3", lambda: m.director(18), [20, 20, 20, 0, 0, 0] * 3),
    ("director(6, full=30) == [30, 30, 0, 0, 0, 30]", lambda: m.director(6, full=30), [30, 30, 0, 0, 0, 30]),
    ("events_from_beats([('x', 25, 5)]) == [5, 5, 5]", lambda: m.events_from_beats([("x", 25, 5)]), [5, 5, 5]),
    ("sample beats: 34 steps", lambda: len(m.events_from_beats(m.SAMPLE_BEATS)), 34),
    ("sample beats: total threat 395", lambda: sum(m.events_from_beats(m.SAMPLE_BEATS)), 395),
    ("measure(sample beats)", lambda: m.measure(m.intensity_curve(m.events_from_beats(m.SAMPLE_BEATS))),
     {"max": 49.37, "peak_s": 100, "calm_s": 140, "peaks": 2}),
    ("half_life(0.5) == 10 s and half_life(0.7) == 19.43 s",
     lambda: [m.half_life(0.5), m.half_life(0.7)], [10.0, 19.43]),
]


def main():
    passed = 0
    for label, fn, want in CHECKS:
        try:
            got = fn()
            ok = close(got, want)
        except NotImplementedError as e:
            got, ok = f"not implemented ({e})", False
        except Exception as e:
            got, ok = f"{type(e).__name__}: {e}", False
        passed += ok
        print(f"[{'PASS' if ok else 'FAIL'}] {label}" + ("" if ok else f"   got {got}"))
    print(f"{passed}/{len(CHECKS)} checks pass")
    sys.exit(0 if passed == len(CHECKS) else 1)


if __name__ == "__main__":
    main()
