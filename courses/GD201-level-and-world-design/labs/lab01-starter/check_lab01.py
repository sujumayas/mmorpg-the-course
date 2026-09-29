"""Checker for GD201 Lab 01. Do not edit. Run: python check_lab01.py"""
import sys

import retry

L = retry.SAMPLE_LEVEL
CHECKS = [
    ("expected_time(8, 0.2, 52) == 248.0", lambda: retry.expected_time(8, 0.2, 52), 248.0),
    ("expected_time(6, 0.25, 30) == 114.0", lambda: retry.expected_time(6, 0.25, 30), 114.0),
    ("penalty_ratio(8, 0.2, 52) == 6.2", lambda: retry.penalty_ratio(8, 0.2, 52), 6.2),
    ("segment_time 3 x (c=10, p=0.5), s=2 == 154.0",
     lambda: retry.segment_time([10, 10, 10], [0.5] * 3, 2), 154.0),
    ("segment_time hard first == 40.5", lambda: retry.segment_time([10, 10], [0.5, 0.8], 2), 40.5),
    ("level_time sample, checkpoints [0] == 1164.9", lambda: retry.level_time(L, [0], 2), 1164.9),
    ("level_time sample, checkpoints [0, 2, 4] == 234.4", lambda: retry.level_time(L, [0, 2, 4], 2), 234.4),
    ("level_time sample, every challenge == 178.8",
     lambda: retry.level_time(L, list(range(len(L))), 2), 178.8),
    ("best_checkpoints sample, k=2 == [0, 3]", lambda: list(retry.best_checkpoints(L, 2, 2)), [0, 3]),
    ("best_checkpoints sample, k=3 == [0, 2, 3]", lambda: list(retry.best_checkpoints(L, 3, 2)), [0, 2, 3]),
]


def main():
    passed = 0
    for label, fn, want in CHECKS:
        try:
            got = fn()
            ok = got == want if isinstance(want, list) else abs(got - want) < 0.05
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
