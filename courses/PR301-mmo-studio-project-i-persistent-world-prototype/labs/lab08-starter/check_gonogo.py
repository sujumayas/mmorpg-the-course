#!/usr/bin/env python3
"""PR301 lab 08: check a freeze plan (bug forecast, cuts, kill switches).

Usage: .venv/bin/python check_gonogo.py tracker.csv plan.txt killswitches.csv

tracker.csv       columns: severity,open,arrivals_per_week,fix_hours,allowed_open,flagged_off
                  allowed_open blank = no limit (that severity is not forecast);
                  flagged_off = bugs of that severity removed by feature flags
plan.txt          key=value: people, hours_per_week (available), weeks, focus_factor,
                  reserved_ops_hours, feature_hours, flag_cost_hours, arrival_multiplier,
                  bad_case_response
killswitches.csv  columns: system,flag,owner,tested_on

Standard library only. Prints the forecast and PASS or NOT READY (exit code 1).
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


def bug_hours(rows, weeks, mult):
    total, flagged = 0.0, 0
    for r in rows:
        if not r["allowed_open"].strip():
            continue
        flag = int(r.get("flagged_off", "0") or 0)
        must = float(r["open"]) + mult * float(r["arrivals_per_week"]) * weeks - float(r["allowed_open"]) - flag
        must = max(must, 0.0)
        flagged += flag
        total += must * float(r["fix_hours"])
    return total, flagged


def main(tracker_path, plan_path, ks_path):
    problems = []
    rows = list(csv.DictReader(open(tracker_path)))
    p = load_kv(plan_path)
    for key in ("people", "hours_per_week", "weeks", "focus_factor", "reserved_ops_hours", "feature_hours",
                "flag_cost_hours", "arrival_multiplier"):
        if not p.get(key):
            problems.append(f"plan.txt: '{key}' is empty")
    if problems:
        for x in problems:
            print("  -", x)
        print("NOT READY")
        return 1
    weeks = float(p["weeks"])
    cap = (float(p["people"]) * float(p["hours_per_week"]) * weeks * float(p["focus_factor"])
           - float(p["reserved_ops_hours"]))
    feat = float(p["feature_hours"])
    fcost = float(p["flag_cost_hours"])
    for mult, label in ((float(p["arrival_multiplier"]), "expected"), (1.5, "arrivals x1.5")):
        bugs, flagged = bug_hours(rows, weeks, mult)
        work = bugs + feat + flagged * fcost
        slack = cap - work
        print(f"{label:>14}: bugs {bugs:.1f} h + features {feat:.1f} h + flags {flagged * fcost:.1f} h"
              f" = {work:.1f} h vs capacity {cap:.1f} h -> slack {slack:+.1f} h ({slack / cap:+.0%})")
        if label == "expected" and slack < 0:
            problems.append("expected case does not fit: cut scope, do not add effort")
    if not p.get("bad_case_response"):
        problems.append("plan.txt: 'bad_case_response' is empty: say what happens if arrivals run at x1.5")
    s1 = [r for r in rows if r["severity"].strip().upper() == "S1"]
    if s1 and s1[0]["allowed_open"].strip() not in ("0", ""):
        problems.append("S1 allowed_open must be 0")
    if s1 and int(s1[0].get("flagged_off", "0") or 0) > 0:
        problems.append("S1 bugs cannot be flagged off in the forecast; use the kill-switch list")
    ks = list(csv.DictReader(open(ks_path)))
    if not ks:
        problems.append("no kill switches listed")
    for k in ks:
        if not k.get("tested_on", "").strip():
            problems.append(f"kill switch '{k['flag']}' ({k['system']}) has never been tested")
        if not k.get("owner", "").strip():
            problems.append(f"kill switch '{k['flag']}' has no owner")
    for x in problems:
        print("  -", x)
    print("PASS" if not problems else "NOT READY")
    return 0 if not problems else 1


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(*sys.argv[1:]))
