#!/usr/bin/env python3
"""PR401 lab 09: content plan checker.

Usage: python content_yield.py content.csv params.csv
Computes effective hours E = c x r and yield E / cost for every unit, checks the
included units against the budget, must-haves and yield order, computes the
median drought and the drought if your most important assumed replay value
halves, and prints PASS or NOT READY. Standard library only.
"""
import csv
import sys

TOL = 0.05


def rows(path):
    with open(path, newline="") as f:
        return [{k.strip(): (v or "").strip() for k, v in r.items()} for r in csv.DictReader(f)]


def main(content_p, params_p):
    problems = []
    prm = {r["key"]: r["value"] for r in rows(params_p)}
    try:
        budget = float(prm["budget_h"]); h = float(prm["median_hours_per_week"]); weeks = float(prm["weeks"])
    except (KeyError, ValueError):
        print("params.csv needs numeric budget_h, median_hours_per_week and weeks")
        print("NOT READY")
        return 1
    units = []
    for r in rows(content_p):
        try:
            u = dict(name=r["unit"], cost=float(r["cost_h"]), c=float(r["first_pass_h"]), r=float(r["replay"]),
                     evidence=r.get("evidence", ""), must=r.get("must_have", "").lower() == "yes",
                     inc=r.get("include", "").lower() == "yes", note=r.get("note", ""))
        except (KeyError, ValueError) as exc:
            problems.append(f"content row {r.get('unit')}: bad number ({exc})")
            continue
        u["E"] = u["c"] * u["r"]
        u["y"] = u["E"] / u["cost"] if u["cost"] else 0
        if not u["evidence"]:
            problems.append(f"{u['name']}: no evidence for c and r (write 'assumed' if none)")
        if u["must"] and not u["inc"]:
            problems.append(f"{u['name']}: must-have unit is not included")
        units.append(u)

    inc = [u for u in units if u["inc"]]
    spent = sum(u["cost"] for u in inc)
    E = sum(u["E"] for u in inc)
    need = h * weeks
    drought_days = max(0.0, need - E) / h * 7
    for u in sorted(units, key=lambda u: -u["y"]):
        print(f"{'IN ' if u['inc'] else '   '}{u['name']:<34} cost {u['cost']:5.0f}  E {u['E']:5.2f}  yield {u['y']:.3f}")
    print(f"budget {budget:.0f} h, spent {spent:.0f} h; E total {E:.2f} h; median needs {need:.1f} h; "
          f"median drought {drought_days:.1f} days")
    if spent > budget:
        problems.append(f"included units cost {spent:.0f} h, over the {budget:.0f} h budget")

    # yield order: an excluded unit that fits and beats an included optional unit needs a note
    left = budget - spent
    for x in units:
        if x["inc"]:
            continue
        beaten = [u for u in inc if not u["must"] and u["y"] < x["y"]]
        if (beaten or x["cost"] <= left) and not x["note"]:
            problems.append(f"{x['name']}: excluded although it {'outranks ' + beaten[0]['name'] if beaten else 'fits the remaining budget'}; include it or write a note")

    # sensitivity on the included assumed unit with the largest E
    assumed = [u for u in inc if u["evidence"].lower().startswith("assumed") and u["r"] > 1]
    if assumed:
        key = max(assumed, key=lambda u: u["E"])
        E_half = E - key["E"] / 2
        sens = max(0.0, need - E_half) / h * 7
        print(f"sensitivity: {key['name']} r halved -> E {E_half:.2f} h, median drought {sens:.1f} days")
        if prm.get("sensitivity_unit", "") != key["name"]:
            problems.append(f"sensitivity_unit should be '{key['name']}' (largest E among assumed replay values)")
        try:
            if abs(float(prm.get("declared_sensitivity_drought_days", "")) - sens) > TOL * max(sens, 1):
                problems.append(f"declared_sensitivity_drought_days does not match {sens:.1f}")
        except ValueError:
            problems.append("declared_sensitivity_drought_days is blank")
    for col, val in (("declared_effective_h", E), ("declared_median_drought_days", drought_days)):
        try:
            if abs(float(prm.get(col, "")) - val) > TOL * max(val, 1):
                problems.append(f"{col} does not match computed {val:.2f}")
        except ValueError:
            problems.append(f"{col} is blank")
    for p in problems:
        print("  -", p)
    print("PASS" if not problems else "NOT READY")
    return 0 if not problems else 1


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(*sys.argv[1:]))
