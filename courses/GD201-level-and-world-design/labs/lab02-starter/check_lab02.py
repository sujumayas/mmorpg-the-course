"""Checker for GD201 Lab 02. Do not edit. Run: python check_lab02.py"""
import sys

import blockout as b

GRID = b.load("sample_mill.txt")
M = b.markers(GRID)
BLOCKED = list(GRID)
BLOCKED[6] = BLOCKED[6][:12] + "#" + BLOCKED[6][13:]   # wall off the only link between west and east

CHECKS = [
    ("shortest_steps S -> A == 5", lambda: b.shortest_steps(GRID, M["S"], M["A"]), 5),
    ("shortest_steps A -> D == 19", lambda: b.shortest_steps(GRID, M["A"], M["D"]), 19),
    ("shortest_steps across a wall-off is None", lambda: b.shortest_steps(BLOCKED, M["S"], M["G"]), None),
    ("path_seconds(64) == 10.667", lambda: b.path_seconds(64), 10.667),
    ("path_seconds(30, 2.0, 5.0) == 12.0", lambda: b.path_seconds(30, 2.0, 5.0), 12.0),
    ("critical_path SABCDG == (64, [5, 14, 17, 12, 16])", lambda: b.critical_path(GRID, "SABCDG"),
     (64, [5, 14, 17, 12, 16])),
    ("critical_path SG == (34, [34])", lambda: b.critical_path(GRID, "SG"), (34, [34])),
    ("critical_path on the walled-off map is None", lambda: b.critical_path(BLOCKED, "SABCDG"), None),
    ("problems_at_ship(16) == 2.125", lambda: b.problems_at_ship(16), 2.125),
    ("problems_at_ship(0) == 5.75", lambda: b.problems_at_ship(0), 5.75),
    ("problems_at_ship(48, M=0) == 0.0098", lambda: b.problems_at_ship(48, M=0), 0.0098),
    ("problems_at_ship(8, c_a=8) == 0.5", lambda: b.problems_at_ship(8, c_a=8), 0.5),
]


def same(got, want):
    if isinstance(want, float):
        return isinstance(got, (int, float)) and abs(got - want) < 0.001
    if isinstance(want, tuple):
        return got is not None and tuple(got[:1]) == want[:1] and list(got[1]) == want[1]
    return got == want


def main():
    passed = 0
    for label, fn, want in CHECKS:
        try:
            got = fn()
            ok = same(got, want)
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
