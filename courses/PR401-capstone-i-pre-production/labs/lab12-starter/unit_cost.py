#!/usr/bin/env python3
"""PR401 lab 12: per-unit cost and tool break-even. Standard library only.

Usage: python unit_cost.py timelog.csv units.csv tools.csv

timelog.csv  date,person,discipline,task,tag,unit_type,hours
             tag is one_time, per_unit, fix or overhead; unit_type is required for per_unit
units.csv    unit_type,discipline,units_built
tools.csv    tool,unit_type,manual_discipline,F,u_m,u_t,n_remaining,decision,note
             u_m is checked against the measured per-unit cost of manual_discipline
             decision is build_now, build_later or never

Prints hours by tag, per-unit cost per unit type and discipline, break-even for
each tool, then PASS or NOT READY. Exits 1 when anything fails.
"""
import csv
import sys
from collections import defaultdict

TAGS = {"one_time", "per_unit", "fix", "overhead"}
DECISIONS = {"build_now", "build_later", "never"}


def read(path):
    with open(path, newline="") as f:
        return [{k.strip(): (v or "").strip() for k, v in r.items()} for r in csv.DictReader(f)]


def main(log_path, units_path, tools_path):
    problems = []
    by_tag = defaultdict(float)
    per_unit = defaultdict(float)          # (unit_type, discipline) -> hours
    for i, r in enumerate(read(log_path), start=2):
        tag, h = r.get("tag", ""), float(r.get("hours") or 0)
        if tag not in TAGS:
            problems.append(f"timelog line {i}: tag '{tag}' is not one of {sorted(TAGS)}")
            continue
        by_tag[tag] += h
        if tag == "per_unit":
            if not r.get("unit_type"):
                problems.append(f"timelog line {i}: per_unit hours need a unit_type")
                continue
            per_unit[(r["unit_type"], r["discipline"])] += h
    total = sum(by_tag.values()) or 1
    print("hours by tag: " + ", ".join(f"{t} {by_tag[t]:.1f} ({by_tag[t] / total:.0%})" for t in sorted(TAGS)))
    built = {(r["unit_type"], r["discipline"]): float(r["units_built"]) for r in read(units_path)}
    cost = {}   # (unit_type, discipline) -> hours per unit
    print(f"{'unit_type':<16}{'discipline':<22}{'hours':>7}{'built':>7}{'per unit':>10}")
    for key, h in sorted(per_unit.items()):
        n = built.get(key)
        if not n:
            problems.append(f"{key[0]}/{key[1]}: per-unit hours logged but no units_built row")
            continue
        cost[key] = h / n
        print(f"{key[0]:<16}{key[1]:<22}{h:>7.1f}{n:>7.0f}{h / n:>10.2f}")
    for r in read(tools_path):
        name = r["tool"]
        F, um, ut, n = (float(r[k]) for k in ("F", "u_m", "u_t", "n_remaining"))
        if r.get("decision") not in DECISIONS:
            problems.append(f"{name}: decision must be one of {sorted(DECISIONS)}")
        measured = cost.get((r["unit_type"], r.get("manual_discipline", "")))
        if measured is None:
            problems.append(f"{name}: no measured per-unit cost for {r['unit_type']}/{r.get('manual_discipline')}; build some units by hand first")
        elif abs(um - measured) > 0.1 * measured and not r.get("note"):
            problems.append(f"{name}: u_m {um} differs from measured {measured:.2f} by more than 10% with no note")
        if um <= ut:
            print(f"{name}: tool never pays (u_t >= u_m)")
            if r.get("decision") == "build_now":
                problems.append(f"{name}: build_now although the tool never saves per-unit time")
            continue
        be = F / (um - ut)
        saved = n * um - (F + n * ut)
        print(f"{name}: break-even {be:.1f} units, {n:.0f} remaining, saves {saved:.1f} h in total")
        if r.get("decision") == "build_now" and n < be and not r.get("note"):
            problems.append(f"{name}: build_now below break-even needs a note (live ops, load shift)")
        if r.get("decision") == "never" and n > 2 * be and not r.get("note"):
            problems.append(f"{name}: never, with more than twice break-even remaining, needs a note")
        if not r.get("note"):
            problems.append(f"{name}: note must state the effect on each discipline's load")
    for p in dict.fromkeys(problems):
        print("  -", p)
    print("PASS" if not problems else "NOT READY")
    return 0 if not problems else 1


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    sys.exit(main(*sys.argv[1:]))
