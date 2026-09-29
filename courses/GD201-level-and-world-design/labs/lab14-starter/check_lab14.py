"""Checker for GD201 Lab 14. Do not edit. Run: python check_lab14.py"""
import sys

import heatmap as H


def ev(player, kind, x, y, run=0, t=0):
    return {"player": player, "run": run, "t": t, "kind": kind, "x": x, "y": y}


# A small hand-made playtest, 4 m cells. p1 leaves cell (0, 0), comes back and dies there.
TINY = [ev("p1", "pos", 1, 1), ev("p1", "pos", 2, 2), ev("p1", "pos", 5, 1),
        ev("p1", "pos", 1, 3), ev("p1", "death", 1, 3),
        ev("p2", "pos", 5, 5), ev("p2", "death", 5, 6)]


def csv_events():
    return H.load_events("telemetry.csv")


CHECKS = [
    ("cell_of(9.9, 4.0, 4) == (2, 1)", lambda: H.cell_of(9.9, 4.0, 4), (2, 1)),
    ("count_deaths tiny", lambda: H.count_deaths(TINY, 4), {(0, 0): 1, (1, 1): 1}),
    ("count_visits tiny (a return is a new visit)", lambda: H.count_visits(TINY, 4),
     {(0, 0): 2, (1, 0): 1, (1, 1): 1}),
    ("heat(25, 100, 0.1, 20) == 0.225", lambda: H.heat(25, 100, 0.1, 20), 0.225),
    ("heat(2, 4, 0.1, 20) == 0.1667", lambda: H.heat(2, 4, 0.1, 20), 0.16667),
    ("heat_map tiny, k = 2", lambda: H.heat_map(TINY, 4, 2),
     {(0, 0): 0.5, (1, 0): 1 / 3, (1, 1): 2 / 3}),
    ("top_cells breaks ties by the smaller cell",
     lambda: H.top_cells({(2, 0): 1.0, (1, 5): 1.0, (0, 0): 0.5}, 2), [(1, 5), (2, 0)]),
    ("telemetry.csv: 39 deaths in total",
     lambda: sum(H.count_deaths(csv_events(), 4).values()), 39),
    ("telemetry.csv: 1080 visits in total at 4 m",
     lambda: sum(H.count_visits(csv_events(), 4).values()), 1080),
    ("telemetry.csv: hottest cell by count is (7, 2), the bridge",
     lambda: H.top_cells(H.count_deaths(csv_events(), 4), 1), [(7, 2)]),
    ("telemetry.csv: hottest cell by shrunk rate (k = 20) is (4, 3), the sniper yard",
     lambda: H.top_cells(H.heat_map(csv_events(), 4, 20), 1), [(4, 3)]),
]


def same(got, want):
    if isinstance(want, float):
        return abs(got - want) < 1e-3
    if isinstance(want, dict):
        return (isinstance(got, dict) and set(got) == set(want)
                and all(abs(got[c] - want[c]) < 1e-3 for c in want))
    return got == want


def main():
    passed = 0
    for label, fn, want in CHECKS:
        try:
            got = fn()
            ok = same(got, want)
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
