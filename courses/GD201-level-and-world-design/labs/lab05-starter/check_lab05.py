"""Checker for GD201 Lab 05. Do not edit. Run: python check_lab05.py"""
import sys

import signposts as sp

LOG = sp.load_log
G = [(0.7, 0.5), (0.3, 0.05)]

CHECKS = [
    ("find_chance(0.3, 9) == 0.9596", lambda: sp.find_chance(0.3, 9), 0.9596, 1e-4),
    ("signposts_needed(0.3, 0.95) == 9", lambda: sp.signposts_needed(0.3, 0.95), 9, 0),
    ("signposts_needed(0.2, 0.36) == 2 (exact boundary)", lambda: sp.signposts_needed(0.2, 0.36), 2, 0),
    ("signposts_needed(0.25, 0.95) == 11", lambda: sp.signposts_needed(0.25, 0.95), 11, 0),
    ("mixture(9, lecture groups) == 0.8096", lambda: sp.mixture(9, G), 0.8096, 1e-4),
    ("mixture(40, lecture groups) == 0.9614", lambda: sp.mixture(40, G), 0.9614, 1e-4),
    ("route_find(3 subtle + 1 loud) == 0.9655",
     lambda: sp.route_find([sp.SUBTLE] * 3 + [sp.LOUD], sp.LECTURE_GROUPS), 0.9655, 1e-4),
    ("route_find(sample route) == 0.7685",
     lambda: sp.route_find(sp.SAMPLE_ROUTE, sp.LECTURE_GROUPS), 0.7685, 1e-4),
    ("lost_by_group check-yourself 2: tunnelers == 0.865",
     lambda: sp.lost_by_group([{"s": 0.6, "t": 0.1}] * 4, {"s": 0.8, "t": 0.2})["t"], 0.865, 1e-3),
    ("signpost_rates(log)['S3'] == 0.5", lambda: sp.signpost_rates(LOG())["S3"], 0.5, 1e-9),
    ("signpost_rates(log)['S6'] == 0.5833", lambda: sp.signpost_rates(LOG())["S6"], 0.5833, 1e-4),
    ("tester_rates(log)['T04'] == 0.6667", lambda: sp.tester_rates(LOG())["T04"], 0.6667, 1e-4),
    ("fit_two_groups scanner share == 0.6667", lambda: sp.fit_two_groups(LOG())["scanner"][0], 0.6667, 1e-4),
    ("fit_two_groups scanner p == 0.8333", lambda: sp.fit_two_groups(LOG())["scanner"][1], 0.8333, 1e-4),
    ("fit_two_groups tunneler p == 0.125", lambda: sp.fit_two_groups(LOG())["tunneler"][1], 0.125, 1e-4),
    ("simulate(sample route, 50k players) within 0.01 of 0.7685",
     lambda: sp.simulate(sp.SAMPLE_ROUTE, sp.LECTURE_GROUPS, players=50_000, seed=3), 0.7685, 0.01),
]


def main():
    passed = 0
    for label, fn, want, tol in CHECKS:
        try:
            got = fn()
            ok = abs(got - want) <= tol
        except NotImplementedError as e:
            got, ok = f"not implemented ({e})", False
        except Exception as e:  # show the student what broke
            got, ok = f"{type(e).__name__}: {e}", False
        passed += ok
        print(f"[{'PASS' if ok else 'FAIL'}] {label}" + ("" if ok else f"   got {got}"))
    print(f"{passed}/{len(CHECKS)} checks pass")
    sys.exit(0 if passed == len(CHECKS) else 1)


if __name__ == "__main__":
    main()
