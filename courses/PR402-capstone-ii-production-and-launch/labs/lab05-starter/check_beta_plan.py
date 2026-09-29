#!/usr/bin/env python3
"""PR402 lab 05: closed beta funnel, invite batches and stress windows.

Usage: python check_beta_plan.py beta.csv batches.csv windows.csv

Model (PR402 week 5, section 4):
  active needed  = ceil(target_ccu / p_window)
  invites needed = ceil(active needed / p_start)
  no-window CCU  = active * sessions * hours / 168   (peak about 3x)
  exposure E     = active * sessions * hours;  clean beta => rate < 3 / E
Rules: planned invites >= invites needed; first batch is 40-70% of the total; at least two
       windows on different days, each 60-120 minutes and announced in the invite;
       friends_share <= 0.5; consent_notice_live is yes; every input has a source.
"""
import csv
import math
import sys


def read(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def main():
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    rows = read(sys.argv[1])
    b = {r["key"]: r["value"].strip() for r in rows}
    batches, windows = read(sys.argv[2]), read(sys.argv[3])
    problems = [f"input {r['key']} has no source" for r in rows
                if r["key"] != "consent_notice_live" and not r["source"].strip()]

    target, ps, pw = float(b["target_ccu"]), float(b["p_start"]), float(b["p_window"])
    sess, hrs = float(b["sessions_per_tester"]), float(b["hours_per_session"])
    active = math.ceil(target / pw - 1e-9)
    need = math.ceil(active / ps - 1e-9)
    planned = sum(int(x["invites"]) for x in batches)
    print(f"active testers needed {active}, invites needed {need}, planned {planned}")
    spread = active * sess * hrs / 168
    print(f"without windows: average CCU {spread:.1f}, evening peak about {3 * spread:.0f}")
    e = active * sess * hrs
    launch = float(b["launch_week_player_hours"])
    print(f"exposure {e:.0f} player-hours; clean beta bound: rate < 1 per {e / 3:.0f} h; "
          f"launch week may still see up to {3 * launch / e:.1f} firings of an unseen bug")

    if planned < need:
        problems.append(f"planned invites {planned} are below the {need} needed")
    if batches and planned:
        first = int(batches[0]["invites"]) / planned
        if not 0.4 <= first <= 0.7:
            problems.append(f"first batch is {first:.0%} of invites; send 40-70% first and size the rest from p_start")
        if len(batches) < 2:
            problems.append("only one invite batch; plan at least two")
    days = {w["day"] for w in windows}
    if len(windows) < 2 or len(days) < 2:
        problems.append("need at least two stress windows on different days")
    for w in windows:
        if not 60 <= int(w["minutes"]) <= 120:
            problems.append(f"{w['window']}: {w['minutes']} minutes; keep windows 60-120 minutes")
        if w["announced_in_invite"].strip().lower() != "yes":
            problems.append(f"{w['window']}: not announced in the invite")
    if float(b["friends_share"]) > 0.5:
        problems.append(f"friends_share {float(b['friends_share']):.0%} is over 50%")
    if b["consent_notice_live"].lower() != "yes":
        problems.append("consent notice is not live")

    for p in problems:
        print("FAIL:", p)
    print("PASS" if not problems else "NOT READY")
    sys.exit(0 if not problems else 1)


if __name__ == "__main__":
    main()
