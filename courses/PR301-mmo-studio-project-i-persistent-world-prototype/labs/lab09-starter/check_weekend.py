#!/usr/bin/env python3
"""PR301 lab 09: check sign-up sizing, the on-call rota and the runbook headings.

Usage: .venv/bin/python check_weekend.py sizing.txt rota.csv runbook.md

sizing.txt  key=value: target, show_rate, sessions_per_player, session_hours, event_attendance,
            evening_weight, total_weight, signups_planned, signups_claimed
rota.csv    columns: primary,backup,start,end   times as "Fri 18:00", "Sat 00:00", "Sun 18:00"
            (whole hours; the weekend runs from Fri 18:00 to Sun 18:00)
runbook.md  must contain a heading for each required action (see REQUIRED below)

Standard library only. Uses the week 9 guide's hand model (Little's law plus the event).
Prints PASS or NOT READY (exit code 1).
"""
import csv
import math
import re
import sys

DAYS = {"fri": 0, "sat": 1, "sun": 2}
REQUIRED = ["start", "stop", "restart", "restore", "kill switch", "hotfix", "roll back", "contacts"]
MAX_SHIFT = 6


def load_kv(path):
    out = {}
    for line in open(path):
        line = line.split("#", 1)[0].strip()
        if "=" in line:
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip()
    return out


def hour_index(text):
    m = re.fullmatch(r"\s*(fri|sat|sun)\w*\s+(\d{1,2}):00\s*", text.lower())
    if not m:
        raise ValueError(f"bad time '{text}' (use e.g. 'Sat 02:00')")
    return DAYS[m.group(1)] * 24 + int(m.group(2)) - 18


def main(sizing_path, rota_path, runbook_path):
    problems = []
    z = load_kv(sizing_path)
    keys = ("target", "show_rate", "sessions_per_player", "session_hours", "event_attendance",
            "evening_weight", "total_weight", "signups_planned", "signups_claimed")
    missing = [k for k in keys if not z.get(k)]
    if missing:
        problems += [f"sizing.txt: '{k}' is empty" for k in missing]
    else:
        s, k, W, e = (float(z[x]) for x in ("show_rate", "sessions_per_player", "session_hours", "event_attendance"))
        share = float(z["evening_weight"]) / float(z["total_weight"])
        l_over_p = k * share * W
        per_signup = s * (e + (1 - e) * l_over_p)
        need = math.ceil(float(z["target"]) / per_signup)
        planned = float(z["signups_planned"])
        print(f"evening share {share:.2%}, L/P {l_over_p:.3f}, online per sign-up {per_signup:.3f}")
        print(f"sign-ups needed for {z['target']}: {need}; planned {planned:.0f} -> "
              f"{planned * per_signup:.1f} humans at the event, normal evening {planned * s * l_over_p:.1f}")
        if abs(int(float(z["signups_claimed"])) - need) > 1:
            problems.append(f"signups_claimed {z['signups_claimed']} but the model gives {need}")
        if planned < need:
            print(f"  note: planned sign-ups are {need - planned:.0f} short; the plan must say how bots or a"
                  f" higher attendance cover the gap")

    covered = [0] * 48
    for row in csv.DictReader(open(rota_path)):
        try:
            a, b = hour_index(row["start"]), hour_index(row["end"])
        except ValueError as err:
            problems.append(str(err))
            continue
        who, backup = row["primary"].strip(), row["backup"].strip()
        if not who or not backup:
            problems.append(f"shift {row['start']}-{row['end']}: needs a primary and a backup")
        if who and who == backup:
            problems.append(f"shift {row['start']}-{row['end']}: backup must be a different person")
        if b - a > MAX_SHIFT:
            problems.append(f"shift {row['start']}-{row['end']} for {who}: {b - a} h (max {MAX_SHIFT})")
        for h in range(max(a, 0), min(b, 48)):
            covered[h] += 1
    gaps = [h for h in range(48) if not covered[h]]
    if gaps:
        names = ", ".join(f"{['Fri', 'Sat', 'Sun'][(h + 18) // 24]} {(h + 18) % 24:02d}:00" for h in gaps[:6])
        problems.append(f"{len(gaps)} uncovered hour(s), first: {names}")
    else:
        print("rota covers all 48 hours")

    text = open(runbook_path).read().lower()
    heads = " ".join(re.findall(r"^#+\s*(.+)$", text, re.M))
    for req in REQUIRED:
        if req not in heads:
            problems.append(f"runbook has no heading for '{req}'")
    for p in problems:
        print("  -", p)
    print("PASS" if not problems else "NOT READY")
    return 0 if not problems else 1


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(*sys.argv[1:]))
