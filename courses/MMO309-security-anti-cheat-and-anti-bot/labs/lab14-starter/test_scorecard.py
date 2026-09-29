"""Run with: python test_scorecard.py   (all checks must print PASS)."""
import math

import scorecard as sc

failures = 0
L = sc.load()["levers"]


def check(name, got, want, tol=1e-3):
    global failures
    try:
        ok = abs(got - want) <= tol or (math.isinf(want) and got == want)
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


def t_uptime():
    check("instant bans uptime", sc.uptime(**L["instant bans"]), 0.75)
    check("wave uptime", sc.uptime(**L["delayed wave"]), 0.4)
    check("no response uptime", sc.uptime(**L["no response"]), 1.0)
    check("detect 5 uptime", sc.uptime(5, 0, 2), 5 / 7)


def t_one_year():
    check("instant bans saving", sc.one_year(L["instant bans"], 1000)[2], 41250)
    check("wave harm left", sc.one_year(L["delayed wave"], 1000)[1], 146000)
    check("structural saving", sc.one_year(L["structural fix"], 1000)[2], 365000 - 365000 * 96 / 461 - 150000)
    check("close free account saving", sc.one_year(L["close free account"], 1000)[2], 365000 - 365000 * 6 / 66 - 30000)
    check("no response saving", sc.one_year(L["no response"], 1000)[2], 0)


def t_rules():
    check("day worth, instant bans", sc.day_worth(**L["instant bans"]), 3.0)
    check("day worth, no downtime", sc.day_worth(**L["no response"]), math.inf)
    check("lawsuit break-even", sc.lawsuit_breakeven(500000, 0.75, 0.10), 500000 / (365 * 0.65))
    check("lawsuit that changes nothing", sc.lawsuit_breakeven(500000, 0.5, 0.5), math.inf)


def t_years():
    s = 365000 - 365000 * 96 / 461 - 30000
    check("structural 2 years", sc.saving_over(L["structural fix"], 1000, 2), 2 * s - 140000)
    check("wave 2 years", sc.saving_over(L["delayed wave"], 1000, 2), 338000)
    check("1 year equals one_year", sc.saving_over(L["delayed wave"], 1000, 1), 169000)
    order = sc.rank(L, 1000, 1)
    check("rank year 1 top", order[0], "close free account")
    check("rank year 1 second", order[1], "delayed wave")
    check("rank year 2 structural beats wave",
          sc.rank(L, 1000, 2).index("structural fix") < sc.rank(L, 1000, 2).index("delayed wave"), True)


for n, f in [("uptime", t_uptime), ("one_year", t_one_year), ("rules", t_rules), ("years", t_years)]:
    run(n, f)
print("ALL PASS" if failures == 0 else f"{failures} FAILED")
raise SystemExit(1 if failures else 0)
