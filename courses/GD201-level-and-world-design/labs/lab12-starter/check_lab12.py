"""Checker for GD201 Lab 12. Do not edit. Run: python check_lab12.py"""
import sys

import spawns as s

T, AR = s.TEACHING_MAP, s.ARENA
ROOM_B = {(x, y) for x in (1, 2, 3) for y in (9, 10, 11)}
ONE_DOOR = list(T)
ONE_DOOR[8] = "#####..###..#####"

CHECKS = [
    ("los: arena corners see each other, A and C do not",
     lambda: [s.los(AR, (1, 1), (9, 9)), s.los(T, (8, 3), (15, 9))], [True, False]),
    ("los is symmetric for B and (5, 11)", lambda: [s.los(T, (1, 9), (5, 11)), s.los(T, (5, 11), (1, 9))],
     None),
    ("exposure: open arena, R = 4 == 48", lambda: s.exposure(AR, (5, 5), 4), 48),
    ("exposure: open arena, R = 3 == 28", lambda: s.exposure(AR, (5, 5), 3), 28),
    ("exposure: teaching map A, C == [90, 2]", lambda: [s.exposure(T, (8, 3), 8), s.exposure(T, (15, 9), 8)], [90, 2]),
    ("heatmap: max 90 at (8, 2)", lambda: [max(s.heatmap(T, 8).values()), s.heatmap(T, 8)[(8, 2)]], [90, 90]),
    ("camp_positions: B with two exits == [(1, 7), (5, 11)]",
     lambda: list(s.camp_positions(T, [(4, 10), (2, 8)], ROOM_B, 8)), [(1, 7), (5, 11)]),
    ("camp_positions: B with north gap walled == 28 cells",
     lambda: len(s.camp_positions(ONE_DOOR, [(4, 10)], ROOM_B, 8)), 28),
    ("p_star(6, 20, 60) == 2 and p_star(4, 15, 90) ~ 0.667",
     lambda: [round(s.p_star(6, 20, 60), 3), round(s.p_star(4, 15, 90), 3)], [2.0, 0.667]),
    ("quest_time: lecture P = 11 and check-yourself 3",
     lambda: [s.quest_time(10, 20, 6, 60, 11), s.quest_time(8, 15, 4, 90, 5)], [1100.0, 900.0]),
]


def main():
    passed = 0
    for label, fn, want in CHECKS:
        try:
            got = fn()
            if want is None:  # symmetry check: both directions must agree
                ok = isinstance(got, list) and len(got) == 2 and got[0] == got[1] and isinstance(got[0], bool)
            elif isinstance(got, list) and isinstance(want, list):
                ok = len(got) == len(want) and all(
                    abs(g - w) < 1e-6 if isinstance(w, float) else g == w for g, w in zip(got, want))
            else:
                ok = got == want
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
