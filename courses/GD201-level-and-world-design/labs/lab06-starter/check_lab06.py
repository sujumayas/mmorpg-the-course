"""Checker for GD201 Lab 06. Do not edit. Run: python check_lab06.py"""
import sys

import choke_sim as cs

A = 0.1  # kill rate for a 10-second time-to-kill


def close(tol):
    return lambda got, want: abs(got - want) <= tol


def same(got, want):
    return got == want


CHECKS = [
    ("kill_rate(10) == 0.1", lambda: cs.kill_rate(10), 0.1, close(1e-12)),
    ("square_law(30, 10) attackers win with 28.28",
     lambda: (cs.square_law(30, 10, A, A)[0], round(cs.square_law(30, 10, A, A)[1], 2)), ("attackers", 28.28), same),
    ("square_law(20, 12, b = 2a) attackers win with 10.58",
     lambda: (cs.square_law(20, 12, A, 2 * A)[0], round(cs.square_law(20, 12, A, 2 * A)[1], 2)), ("attackers", 10.58), same),
    ("square_law(10, 30) defenders win with 28.28",
     lambda: (cs.square_law(10, 30, A, A)[0], round(cs.square_law(10, 30, A, A)[1], 2)), ("defenders", 28.28), same),
    ("choke_losses(10, w=2) == 25", lambda: cs.choke_losses(10, A, A, 2), 25.0, close(1e-9)),
    ("choke_losses(20, w=2) == 100", lambda: cs.choke_losses(20, A, A, 2), 100.0, close(1e-9)),
    ("fall_time(8, w=2) == 40", lambda: cs.fall_time(8, A, 2), 40.0, close(1e-9)),
    ("fight open field 30 v 10 leaves 28.28", lambda: cs.fight(30, 10, A, A)[0], 28.28, close(0.01)),
    ("fight w=2 leaves 5.00 attackers", lambda: cs.fight(30, 10, A, A, width=2)[0], 5.0, close(0.01)),
    ("fight w=2 lasts 50.0 s", lambda: cs.fight(30, 10, A, A, width=2)[2], 50.0, close(0.05)),
    ("fight w=1 leaves 6.40 defenders", lambda: cs.fight(30, 10, A, A, width=1)[1], 6.40, close(0.01)),
    ("fight w=1 attackers clamp to 0.0", lambda: cs.fight(30, 10, A, A, width=1)[0], 0.0, close(0.0)),
    ("cover_factor(65, 20) == 45/65", lambda: cs.cover_factor(65, 20), 45 / 65, close(1e-12)),
    ("cover_factor(30, 40) == 0", lambda: cs.cover_factor(30, 40), 0.0, close(0.0)),
    ("half cover w=4: fight leaves 11.94", lambda: cs.fight(30, 10, A * cs.cover_factor(65, 20), A, width=4)[0], 11.94, close(0.01)),
    ("weakest_lane([4,3,3], w=2, rot 20) == (1, 15.0, False)",
     lambda: tuple(round(x, 6) if isinstance(x, float) else x for x in cs.weakest_lane([4, 3, 3], A, 2, 20)), (1, 15.0, False), same),
    ("weakest_lane([4,4,4], w=3, rot 12) holds",
     lambda: cs.weakest_lane([4, 4, 4], A, 3, 12)[2], True, same),
]


def main():
    passed = 0
    for label, fn, want, cmp in CHECKS:
        try:
            got = fn()
            ok = bool(cmp(got, want))
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
