#!/usr/bin/env python3
"""PR401 lab 08: economy check against the live window.

Usage: python economy_check.py flows.csv prices.csv players.csv [players_at_launch]
Computes the net rate (faucets minus recurring sinks; scaling sinks are optional
spending and are not subtracted), hours to afford every priced item, the week each target
player type reaches it, and the split of money created across player types.
Prints PASS or NOT READY. Standard library only.
"""
import csv
import sys

LIVE_WEEKS = 4
TOL = 0.02


def rows(path):
    with open(path, newline="") as f:
        return [{k.strip(): (v or "").strip() for k, v in r.items()} for r in csv.DictReader(f)]


def fnum(v):
    try:
        return float(v)
    except ValueError:
        return None


def main(flows_p, prices_p, players_p, launch=100):
    problems = []
    faucet = sink = 0.0
    scaling = 0
    for r in rows(flows_p):
        rate = fnum(r.get("marks_per_hour", ""))
        if rate is None:
            problems.append(f"flows {r['name']}: marks_per_hour is not a number")
            continue
        if r["type"] == "faucet":
            faucet += rate
        elif r["type"] == "sink":
            sink += rate
        elif r["type"] != "scaling_sink":
            problems.append(f"flows {r['name']}: type must be faucet, sink or scaling_sink")
        if r["type"] == "scaling_sink":
            scaling += 1
        if not r.get("source"):
            problems.append(f"flows {r['name']}: no source label (prototype data or 'assumed')")
        if not r.get("event"):
            problems.append(f"flows {r['name']}: no telemetry event name")
    n = faucet - sink
    print(f"faucets {faucet:.0f}/h  recurring sinks {sink:.0f}/h  net n = {n:.0f}/h")
    if n <= 0:
        problems.append("net rate is not positive; nothing can be bought")
    if scaling == 0:
        problems.append("no scaling_sink: add a sink that grows with activity, or explain in docs/economy.md and list it as scaling_sink with rate 0")

    players = {}
    for r in rows(players_p):
        h, share = fnum(r.get("hours_per_week", "")), fnum(r.get("share", ""))
        if h is None or share is None:
            problems.append(f"players {r.get('type')}: hours_per_week and share must be numbers")
            continue
        players[r["type"].lower()] = (h, share)
    if players and abs(sum(s for _, s in players.values()) - 1) > 0.001:
        problems.append("players: shares do not sum to 1")

    for r in rows(prices_p):
        item = r["item"]
        price = fnum(r.get("price", ""))
        target = r.get("target_type", "").lower()
        tweek = fnum(r.get("target_week", ""))
        if price is None or tweek is None or target not in players or n <= 0:
            problems.append(f"prices {item}: needs a numeric price, target_week and a target_type from players.csv")
            continue
        T = price / n
        week = T / players[target][0]
        print(f"{item:<24} T = {T:6.1f} h   {target} reaches it in week {week:5.2f}")
        for col, val in (("declared_hours", T), ("declared_week", week)):
            d = fnum(r.get(col, ""))
            if d is None:
                problems.append(f"prices {item}: {col} is blank")
            elif abs(d - val) > TOL * max(val, 1):
                problems.append(f"prices {item}: {col} {d} does not match computed {val:.2f}")
        if (week > tweek or week > LIVE_WEEKS) and not r.get("response"):
            problems.append(f"prices {item}: target player reaches it in week {week:.2f}, after target week {tweek:g} or the live period; change the price or write a response")

    total = sum(launch * s * h * LIVE_WEEKS for h, s in players.values())
    if total and n > 0:
        print(f"money created in {LIVE_WEEKS} weeks by {launch} players: {total * n:,.0f}")
        for t, (h, s) in players.items():
            print(f"  {t:<8} {100 * s:5.1f}% of players hold {100 * launch * s * h * LIVE_WEEKS / total:5.1f}% of the money")
    for p in problems:
        print("  -", p)
    print("PASS" if not problems else "NOT READY")
    return 0 if not problems else 1


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) not in (3, 4):
        print(__doc__)
        sys.exit(2)
    sys.exit(main(*args[:3], launch=int(args[3]) if len(args) == 4 else 100))
