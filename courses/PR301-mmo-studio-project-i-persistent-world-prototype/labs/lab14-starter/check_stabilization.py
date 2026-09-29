#!/usr/bin/env python3
"""PR301 lab 14: check the stabilization triage and fix budget. Standard library only.

Usage: python check_stabilization.py bugs.csv params.csv

Model (PR301 week 14, sections 2 to 4, extending the week 8 budget):
  Must-fix = every bug triaged S1 or S2. Each needs a decision:
    fix         counted at the mean hours for its severity
    disable     removed by a week 8 kill switch; each distinct switch adds flag_hours once
                (the time to re-check it on the release candidate)
    reclassify  moved to S3 or S4; needs evidence, and only allowed for S2 bugs that
                neither lose data nor crash (data_loss = no, crash = no)
  q                = reopened / closed
  effective demand = (fix hours + new_mustfix x h_new) / (1 - q) + flags x flag_hours
  capacity         = team_hours - reserved_hours + extra_hours
  PASS when every must-fix bug has a valid decision and demand <= capacity.
"""
import csv
import sys


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    problems = []
    with open(sys.argv[2], newline="") as f:
        P = {r["key"].strip(): float(r["value"]) for r in csv.DictReader(f) if r["value"].strip()}
    need = ["h_S1", "h_S2", "reopened", "closed", "new_mustfix", "h_new", "flag_hours",
            "team_hours", "reserved_hours", "extra_hours"]
    missing = [k for k in need if k not in P]
    if missing:
        sys.exit(f"params.csv: missing {missing}\nNOT READY")
    q = P["reopened"] / P["closed"]
    with open(sys.argv[1], newline="") as f:
        bugs = list(csv.DictReader(f))
    fix_h, flags, counts = 0.0, set(), {}
    for b in bugs:
        sev, dec = b["severity"].strip().upper(), b["decision"].strip().lower()
        if sev not in ("S1", "S2"):
            continue
        counts[dec] = counts.get(dec, 0) + 1
        yes = lambda k: b[k].strip().lower() == "yes"
        if sev == "S1" and not (yes("data_loss") or yes("crash")):
            problems.append(f"{b['id']}: S1 needs data_loss or crash = yes (week 8 scale)")
        if dec == "fix":
            fix_h += P["h_" + sev]
        elif dec == "disable":
            if not b["flag"].strip():
                problems.append(f"{b['id']}: disable needs a flag name")
            flags.add(b["flag"].strip())
        elif dec == "reclassify":
            if sev == "S1" or yes("data_loss") or yes("crash"):
                problems.append(f"{b['id']}: data-loss, crash or S1 bugs cannot be reclassified")
            if b["new_severity"].strip().upper() not in ("S3", "S4"):
                problems.append(f"{b['id']}: reclassify needs new_severity S3 or S4")
            if not b["evidence"].strip():
                problems.append(f"{b['id']}: reclassify needs evidence from beta telemetry")
        else:
            problems.append(f"{b['id']}: {sev} needs a decision of fix, disable or reclassify")
    flags.discard("")
    demand = (fix_h + P["new_mustfix"] * P["h_new"]) / (1 - q) + len(flags) * P["flag_hours"]
    cap = P["team_hours"] - P["reserved_hours"] + P["extra_hours"]
    print(f"decisions {counts}  flags {sorted(flags)}")
    print(f"q {q:.3f}  fix hours {fix_h:g}  demand {demand:.1f} h  capacity {cap:g} h  "
          f"margin {cap - demand:.1f} h ({(cap - demand) / cap:.0%})")
    if demand > cap + 1e-9:
        problems.append(f"demand {demand:.1f} h exceeds capacity {cap:g} h")
    for p in problems:
        print("  -", p)
    print("PASS" if not problems else "NOT READY")
    sys.exit(0 if not problems else 1)


if __name__ == "__main__":
    main()
