"""Checker for GD201 Lab 13. Do not edit. Run: python check_lab13.py"""
import sys

import metrics as M

Q = M.QUAKE_RUN
HL2 = {"v0": 160, "g": 600, "v": 190, "w": 32, "step": 18}
H = 270 ** 2 / 1600

CHECKS = [
    ("jump_height(270, 800) == 45.5625", lambda: M.jump_height(270, 800), 45.5625),
    ("time_to_apex(270, 800) == 0.3375", lambda: M.time_to_apex(270, 800), 0.3375),
    ("max_gap(0, Quake) == 248.0", lambda: M.max_gap(0, Q), 248.0),
    ("max_gap(h, Quake) == 140.0", lambda: M.max_gap(H, Q), 140.0),
    ("max_gap(-h, Quake) == 292.7", lambda: M.max_gap(-H, Q), 292.73),
    ("max_gap(18, HL2 run) == 102.7", lambda: M.max_gap(18, HL2), 102.70),
    ("max_gap above apex is None", lambda: M.max_gap(50, Q), None),
    ("classify crate hop == walk", lambda: M.classify(M.SAMPLE_ROUTE[0], Q), "walk"),
    ("classify pit == comfortable", lambda: M.classify(M.SAMPLE_ROUTE[2], Q), "comfortable"),
    ("classify high ledge == skill", lambda: M.classify(M.SAMPLE_ROUTE[5], Q), "skill"),
    ("classify tower top == impossible", lambda: M.classify(M.SAMPLE_ROUTE[7], Q), "impossible"),
    ("audit verdicts for the sample route",
     lambda: [v for _, v, _ in M.audit(M.SAMPLE_ROUTE, Q)],
     ["walk", "comfortable", "comfortable", "skill", "comfortable", "skill", "comfortable", "impossible"]),
    ("audit percent for broken bridge == 92.7",
     lambda: M.audit(M.SAMPLE_ROUTE, Q)[3][2], 92.7),
]


def same(got, want):
    if want is None or isinstance(want, (list, str)):
        return got == want
    return got is not None and abs(got - want) < 0.05


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
