#!/usr/bin/env python3
"""PR301 lab 07: check an economy budget and a recipe list.

Usage: .venv/bin/python check_budget.py budget.csv recipes.csv targets.txt

budget.csv   columns: code,kind,per_player_hour,basis,logged_event
             kind is faucet or sink; basis is "bot run" or "estimate"; logged_event names the
             ledger reason code the server writes (normally the same as code)
recipes.csv  columns: recipe,fee,inputs_vendor_value,output_vendor_price
             output_vendor_price is blank if the output cannot be sold to a vendor
targets.txt  key=value lines: goal_price, band_min_hours, band_max_hours, players, hours_per_player

Standard library only. Prints the budget summary and PASS or NOT READY (exit code 1).
"""
import csv
import sys


def load_kv(path):
    out = {}
    for line in open(path):
        line = line.split("#", 1)[0].strip()
        if "=" in line:
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip()
    return out


def main(budget_path, recipes_path, targets_path):
    problems = []
    lines = list(csv.DictReader(open(budget_path)))
    t = load_kv(targets_path)
    for key in ("goal_price", "band_min_hours", "band_max_hours", "players", "hours_per_player"):
        if not t.get(key):
            problems.append(f"targets.txt: '{key}' is empty")
    faucet = sink = 0.0
    for row in lines:
        code = row["code"].strip()
        kind = row["kind"].strip().lower()
        try:
            rate = float(row["per_player_hour"])
        except ValueError:
            problems.append(f"{code}: per_player_hour is not a number")
            continue
        if kind == "faucet":
            faucet += rate
        elif kind == "sink":
            sink += rate
        else:
            problems.append(f"{code}: kind must be faucet or sink")
        if not row.get("basis", "").strip():
            problems.append(f"{code}: basis is empty (bot run or estimate)")
        if not row.get("logged_event", "").strip():
            problems.append(f"{code}: no logged ledger event")
    if problems and any("targets.txt" in p for p in problems):
        for p in problems:
            print("  -", p)
        print("NOT READY")
        return 1

    net = faucet - sink
    goal = float(t["goal_price"])
    lo, hi = float(t["band_min_hours"]), float(t["band_max_hours"])
    H = float(t["players"]) * float(t["hours_per_player"])
    print(f"faucets {faucet:.1f}/h  sinks {sink:.1f}/h  net {net:.1f}/h  sink ratio {sink / faucet:.0%}")
    if net <= 0:
        problems.append("net income is zero or negative: players can never afford the goal")
    else:
        hg = goal / net
        print(f"hours to {goal:.0f} currency: {hg:.1f} (band {lo}-{hi})")
        print(f"weekend: {H:.0f} player-hours -> money supply {H * net:,.0f}, per player {net * float(t['hours_per_player']):,.0f}")
        if not lo <= hg <= hi:
            problems.append(f"hours to goal {hg:.1f} is outside the band {lo}-{hi}")

    for r in csv.DictReader(open(recipes_path)):
        out = r["output_vendor_price"].strip()
        if not out:
            print(f"recipe {r['recipe']}: output not vendor-sellable, ok")
            continue
        cost = float(r["fee"]) + float(r["inputs_vendor_value"])
        gain = float(out) - cost
        verdict = "LEAKS" if gain > 0 else "ok"
        print(f"recipe {r['recipe']}: sells {float(out):.0f}, fee + inputs {cost:.0f} -> {verdict}")
        if gain > 0:
            problems.append(f"recipe {r['recipe']} creates {gain:.0f} currency per craft")
    for p in problems:
        print("  -", p)
    print("PASS" if not problems else "NOT READY")
    return 0 if not problems else 1


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(*sys.argv[1:]))
