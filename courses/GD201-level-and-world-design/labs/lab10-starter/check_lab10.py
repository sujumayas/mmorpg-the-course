"""Checker for GD201 Lab 10. Do not edit. Run: python check_lab10.py"""
import sys

import hubs

Z, H, C = hubs.SAMPLE_ZONE, hubs.SAMPLE_HUB, hubs.CANDIDATE_SHORTCUTS
STAR = [("hub", f"d{i}", 100) for i in range(1, 9)]
CHAIN = [("hub" if i == 0 else f"d{i}", f"d{i + 1}", 100) for i in range(8)]

CHECKS = [
    ("errand_cost, hub and spoke n=8, L=100 == 200", lambda: hubs.errand_cost(STAR, "hub"), 200.0),
    ("errand_cost, chain n=8, L=100 == 900", lambda: hubs.errand_cost(CHAIN, "hub"), 900.0),
    ("errand_cost, chain + loop-back == 500",
     lambda: hubs.errand_cost(CHAIN + [("d8", "hub", 100)], "hub"), 500.0),
    ("pairwise_cost, chain n=8 == 300", lambda: hubs.pairwise_cost(CHAIN, "hub"), 300.0),
    ("errand_cost, sample zone == 942.9", lambda: hubs.errand_cost(Z, H), 942.857),
    ("pairwise_cost, sample zone == 321.9", lambda: hubs.pairwise_cost(Z, H), 321.905),
    ("best_shortcut, sample zone picks town-ruins",
     lambda: list(hubs.best_shortcut(Z, H, C)[0]), ["town", "ruins", 380]),
    ("best_shortcut, sample zone new E == 754.3", lambda: hubs.best_shortcut(Z, H, C)[1], 754.286),
    ("gate_slack, lecture table",
     lambda: [round(x, 2) for x in hubs.gate_slack(hubs.SAMPLE_SPOKES, hubs.SAMPLE_GATES)],
     [2.0, 1.33, 1.2, 1.14, 1.25]),
    ("gate_slack, check-yourself question 3",
     lambda: [round(x, 2) for x in hubs.gate_slack([8, 8, 8, 8], [0, 4, 10, 18, 24])],
     [2.0, 1.6, 1.33, 1.33]),
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
