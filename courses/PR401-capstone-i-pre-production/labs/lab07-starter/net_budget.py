#!/usr/bin/env python3
"""PR401 lab 07: network and replication budget checker.

Usage: python net_budget.py budget.csv
Each row is one load case. The checker recomputes client kbit/s, egress Mbit/s,
entity updates per second and replication ms per tick, compares them with your
declared values, applies the course budget lines, and prints PASS or NOT READY.
Standard library only.
"""
import csv
import sys

CLIENT_KBPS_LINE = 128.0      # client downstream budget
TICK_SHARE_LINE = 0.5         # replication may use at most half of each tick
REQUIRED_CASES = {"spread", "hub", "loadtest"}
TOL = 0.02                    # 2% relative tolerance on declared values


def close(declared, computed):
    return abs(declared - computed) <= TOL * max(abs(computed), 1e-9)


def main(path):
    problems, seen = [], set()
    with open(path, newline="") as f:
        rows = [{k.strip(): (v or "").strip() for k, v in r.items()} for r in csv.DictReader(f)]
    for r in rows:
        name = r.get("case", "?")
        kind = r.get("kind", "").lower()
        seen.add(kind)
        try:
            N = int(r["ccu"]); cap = r["aoi_cap"]
            s = float(r["bytes_per_entity"]); o = float(r["overhead_bytes"])
            hz = float(r["update_hz"]); t_us = float(r["us_per_update"])
        except (KeyError, ValueError) as exc:
            problems.append(f"{name}: missing or non-numeric input ({exc})")
            continue
        e = N - 1 if cap in ("", "none") else min(N - 1, int(cap))
        u = e * s + o
        kbps = u * hz * 8 / 1000
        egress = N * u * hz * 8 / 1e6
        U = N * e * hz
        ms_tick = (U / hz) * t_us / 1000
        tick_ms = 1000 / hz
        print(f"{name:<22} e={e:<4} u={u:>6.0f} B  client={kbps:7.1f} kbit/s  egress={egress:7.1f} Mbit/s  "
              f"U={U:>8.0f}/s  repl={ms_tick:6.1f} of {tick_ms:.0f} ms")
        for col, val in (("declared_client_kbps", kbps), ("declared_egress_mbps", egress),
                         ("declared_repl_ms", ms_tick)):
            try:
                d = float(r.get(col, ""))
            except ValueError:
                problems.append(f"{name}: {col} is blank or not a number")
                continue
            if not close(d, val):
                problems.append(f"{name}: {col} {d} does not match computed {val:.1f}")
        over = []
        if kbps > CLIENT_KBPS_LINE:
            over.append("client downstream above 128 kbit/s")
        if kind == "loadtest" and ms_tick > TICK_SHARE_LINE * tick_ms:
            over.append("replication above half a tick at load test")
        if over and not r.get("response"):
            problems.append(f"{name}: over budget ({'; '.join(over)}) and no design change or accepted risk in 'response'")
        if r.get("source", "").lower() not in ("measured", "spike planned"):
            problems.append(f"{name}: source must be 'measured' or 'spike planned'")
    missing = REQUIRED_CASES - seen
    if missing:
        problems.append(f"missing load case kinds: {', '.join(sorted(missing))}")
    for p in problems:
        print("  -", p)
    print("PASS" if not problems else "NOT READY")
    return 0 if not problems else 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
