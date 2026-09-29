#!/usr/bin/env python3
"""PR401 lab 10: social liquidity and safety checker.

Usage: python social_check.py liquidity.csv safety.csv
For each system that needs m of M players online at once, computes the online
probability p in the window and off-peak, and P(at least m online) with any NPC
fill applied. Checks declared values, requires a response for any window value
under 0.80 and a decision for off-peak, and checks the safety minimums.
Prints PASS or NOT READY. Standard library only.
"""
import csv
import sys
from math import comb

LINE = 0.80
TOL = 0.01
SAFETY = ["code of conduct", "report", "block and mute", "chat filter",
          "moderation rota", "sanctions", "age policy", "data and consent"]


def rows(path):
    with open(path, newline="") as f:
        return [{k.strip(): (v or "").strip() for k, v in r.items()} for r in csv.DictReader(f)]


def at_least(M, p, m):
    if m <= 0:
        return 1.0
    return 1 - sum(comb(M, j) * p ** j * (1 - p) ** (M - j) for j in range(min(m, M + 1)))


def main(liq_p, safety_p):
    problems = []
    for r in rows(liq_p):
        name = r.get("system", "?")
        try:
            M, m, fill = int(r["members"]), int(r["needed"]), int(r.get("npc_fill") or 0)
            h, e, W = float(r["hours_per_week"]), float(r["window_share"]), float(r["window_hours"])
        except (KeyError, ValueError) as exc:
            problems.append(f"{name}: missing or non-numeric input ({exc})")
            continue
        m_eff = max(1, m - fill)
        p_win = e * h / W
        p_off = (1 - e) * h / (168 - W)
        P_win, P_off = at_least(M, p_win, m_eff), at_least(M, p_off, m_eff)
        print(f"{name:<28} M={M:<3} m={m} fill={fill}  p_window={p_win:.3f}  P_window={P_win:.3f}  "
              f"p_off={p_off:.4f}  P_off={P_off:.5f}")
        for col, val in (("declared_p_window", p_win), ("declared_P_window", P_win)):
            try:
                if abs(float(r.get(col, "")) - val) > TOL:
                    problems.append(f"{name}: {col} does not match computed {val:.3f}")
            except ValueError:
                problems.append(f"{name}: {col} is blank")
        if P_win < LINE and not r.get("response"):
            problems.append(f"{name}: P_window {P_win:.2f} is under {LINE}; choose a lever or accept it in 'response'")
        if not r.get("off_peak_rule"):
            problems.append(f"{name}: no off_peak_rule (what happens outside the window?)")
    have = {}
    for r in rows(safety_p):
        have[r.get("feature", "").lower()] = r
    for feat in SAFETY:
        r = have.get(feat)
        if not r:
            problems.append(f"safety: '{feat}' missing")
        elif not r.get("owner") or r.get("status", "").lower() not in ("done", "planned"):
            problems.append(f"safety: '{feat}' needs an owner and status done or planned")
        elif r["status"].lower() == "planned" and not r.get("due_week"):
            problems.append(f"safety: '{feat}' is planned but has no due_week")
    for p in problems:
        print("  -", p)
    print("PASS" if not problems else "NOT READY")
    return 0 if not problems else 1


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(*sys.argv[1:]))
