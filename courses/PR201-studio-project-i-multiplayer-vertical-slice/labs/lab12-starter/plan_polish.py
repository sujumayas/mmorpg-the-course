#!/usr/bin/env python3
"""PR201 lab 12: sprint 4 fix load, polish budget and cut line. Standard library only.

Usage: python plan_polish.py sprint4.csv polish.csv

Model (PR201 week 12, section 3). Every hour is an estimated hour.
  E     = f * U                    sprint forecast (useful hours times focus)
  F     = (B + N) / (1 - r)        fixes needed before beta
  H_fix = F * h / q                logged hours per fix converted to estimated hours
  H_pol = E - O - H_fix            polish budget
  Items go on at their raw estimates (f already carries the overrun); sort by
  value/estimate (ties keep file order); keep an item if it still fits,
  otherwise skip it and try the next.
sprint4.csv has one row per input (U, f, O, B, N, r, h, q) with a value and a source.
polish.csv needs, per item: estimate, value (1-10), evidence (week 11 finding),
decision (in or cut) matching the model, and a done_test for every item that is in.
"""
import csv
import sys

INPUTS = ("U", "f", "O", "B", "N", "r", "h", "q")


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    problems = []
    with open(sys.argv[1], newline="") as f:
        rows = {r["input"].strip(): r for r in csv.DictReader(f)}
    x = {}
    for k in INPUTS:
        r = rows.get(k)
        if r is None or not r["value"].strip():
            problems.append(f"input {k}: value missing")
            continue
        x[k] = float(r["value"])
        if not r["source"].strip():
            problems.append(f"input {k}: source missing (tracker query, or write 'guess')")
    if len(x) < len(INPUTS):
        for p in problems:
            print("FAIL:", p)
        print("NOT READY")
        sys.exit(1)
    if not 0 <= x["r"] < 1:
        problems.append("r must be at least 0 and below 1")
        x["r"] = 0.0
    if x["q"] <= 0 or not 0 < x["f"] <= 1:
        problems.append("q must be above 0 and f between 0 and 1")
        x["q"], x["f"] = 1.0, min(max(x["f"], 0.0), 1.0)
    forecast = x["f"] * x["U"]
    fixes = (x["B"] + x["N"]) / (1 - x["r"])
    h_fix = fixes * x["h"] / x["q"]
    budget = forecast - x["O"] - h_fix
    print(f"forecast {forecast:.1f}, fixes {fixes:.1f}, fix estimate-hours {h_fix:.1f}, polish budget {budget:.1f} h")
    with open(sys.argv[2], newline="") as f:
        items = list(csv.DictReader(f))
    for i in items:
        i["est"] = float(i["estimate"])
        i["val"] = float(i["value"])
    total = 0.0
    print(f"{'id':<5}{'v/h':>6}{'estimate':>9}{'running':>9}  model  yours")
    for i in sorted(items, key=lambda i: -i["val"] / i["est"]):
        h = i["est"]
        keep = total + h <= budget + 1e-9
        total += h if keep else 0
        model = "in" if keep else "cut"
        yours = i["decision"].strip()
        print(f"{i['id']:<5}{i['val'] / i['est']:6.2f}{h:9.1f}{total:9.1f}  {model:<5}  {yours or '-'}")
        if yours != model:
            problems.append(f"{i['id']}: decision '{yours}' but the model gives '{model}'")
        if not i["evidence"].strip():
            problems.append(f"{i['id']}: evidence missing (cite the week 11 finding)")
        if model == "in" and not i["done_test"].strip():
            problems.append(f"{i['id']}: an item above the line needs a done_test")
    print(f"planned {total:.1f} h of {budget:.1f} h")
    if budget <= 0:
        problems.append("no polish budget: the beta bar alone does not fit the sprint")
    for p in problems:
        print("FAIL:", p)
    print("PASS" if not problems else "NOT READY")
    sys.exit(0 if not problems else 1)


if __name__ == "__main__":
    main()
