"""Run with: python test_bounty.py   (all checks must print PASS)."""
import bounty as b

TOL = 1e-6
failures = 0


def check(name, got, want, tol=TOL):
    global failures
    try:
        ok = abs(got - want) <= tol
    except TypeError:
        ok = got == want
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else f"  got {got!r}, want {want!r}"))
    failures += not ok


def run(name, fn):
    global failures
    try:
        fn()
    except NotImplementedError:
        print(f"FAIL {name}  (not implemented)")
        failures += 1


def t_model():
    # Lecture section 2 numbers.
    check("exploit_value h=0.10", b.exploit_value(150, 0.10, 0.6, 300), 1320)
    check("bounty_needed h=0.10", b.bounty_needed(150, 0.10, 0.6, 300, 0.8), 1650)
    check("bounty_needed h=0.02", b.bounty_needed(150, 0.02, 0.6, 300, 0.8), 9150)
    check("bounty_needed never negative", b.bounty_needed(150, 1.0, 0.6, 300, 0.8), 0)
    check("studio_cost h=0.05", b.studio_cost(4000, 0.05, 20000), 100000)


def t_double_dip():
    # Lecture section 5: no audit gives 750 + 1320 = 2070.
    check("double_dip p=0", b.double_dip_value(150, 5, 0.0, 0.8, 1650, 300), 2070)
    check("double_dip p=0.9", b.double_dip_value(150, 5, 0.9, 0.8, 1650, 300), 750 + 0.1 * 1320 - 270)


def t_table():
    rows = b.load_classes()
    table = {r["name"]: r for r in b.price_table(rows, mean_detection_days=10)}
    check("table has 5 rows", len(table), 5)
    check("currency_dupe b_star", table["currency_dupe"]["b_star"], (3000 - 240) / 0.8)
    check("currency_dupe payout", table["currency_dupe"]["payout"], 3450)
    check("out_of_bounds payout floor", table["out_of_bounds_teleport"]["payout"], 100)
    check("item_dupe share", table["item_dupe"]["share"], 1650 / 40000)


def t_afford():
    rows = b.load_classes()
    # currency_dupe binds: 300 D - 240 <= 0.8 * 5000  ->  D <= 14.13
    check("longest affordable at $5,000", b.longest_affordable_detection(rows, 5000), 14)
    check("unaffordable returns 0", b.longest_affordable_detection(rows, 10), 0)


for n, f in [("model", t_model), ("double dip", t_double_dip), ("table", t_table), ("afford", t_afford)]:
    run(n, f)
print("ALL PASS" if failures == 0 else f"{failures} FAILED")
raise SystemExit(1 if failures else 0)
