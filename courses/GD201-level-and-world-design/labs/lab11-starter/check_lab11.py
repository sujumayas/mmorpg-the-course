"""Checker for GD201 Lab 11. Do not edit. Run: python check_lab11.py"""
import sys

import crowd

Z = crowd.TEACHING_ZONE
A, H, f, r = Z["A"], Z["H"], Z["f"], Z["r"]


def near(want, tol):
    return lambda got: abs(got - want) <= tol


CHECKS = [
    ("camp_neighbours(100) == 6.5", lambda: crowd.camp_neighbours(100, H, f), near(6.5, 1e-9)),
    ("camp_neighbours(300, H=10, f=0.5) == 14", lambda: crowd.camp_neighbours(300, 10, 0.5), near(14, 1e-9)),
    ("open_neighbours(100) == 0.201", lambda: crowd.open_neighbours(100, f, r, A), near(0.2011, 0.0005)),
    ("open_neighbours(300, f=0.5, r=50, A=2e6) == 0.589",
     lambda: crowd.open_neighbours(300, 0.5, 50, 2_000_000), near(0.589, 0.001)),
    ("capacity teaching zone == (40.0, 146)", lambda: crowd.capacity(H, f, 2, 10), lambda g: tuple(g) == (40.0, 146)),
    ("copies_needed(3000, 146) == 21", lambda: crowd.copies_needed(3000, 146), lambda g: g == 21),
    ("copies_needed(10, 146) == 1", lambda: crowd.copies_needed(10, 146), lambda g: g == 1),
    ("simulate P=400 even camps: camp mean == 29", lambda: crowd.simulate(400, H, f, r, A)[0], near(29.0, 1e-9)),
    ("simulate P=1000: open mean within 0.2 of 2.01", lambda: crowd.simulate(1000, H, f, r, A)[1], near(2.011, 0.2)),
    ("simulate P=400 random camps: camp mean near (m - 1) / H = 29.875",
     lambda: crowd.simulate(400, H, f, r, A, random_camps=True, trials=40)[0], near(29.875, 0.6)),
]


def main():
    passed = 0
    for label, fn, test in CHECKS:
        try:
            got = fn()
            ok = bool(test(got))
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
