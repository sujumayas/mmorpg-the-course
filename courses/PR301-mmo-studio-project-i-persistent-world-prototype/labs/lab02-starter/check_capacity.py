#!/usr/bin/env python3
"""PR301 lab 02: does the architecture carry the test load? Standard library only.

Usage: python check_capacity.py capacity.csv

capacity.csv has two columns, key and value. Model (PR301 week 2, section 2; MMO302 weeks 1, 5, 7, 11):
  N          = headroom * target_ccu                     players in the load test
  deliveries = u * N * (N - 1) + mobs * u_mob * N        worst case: everyone in one crowd
  cpu        = deliveries * cost_us / 1e6                 share of one core spent on deliveries
  out_bytes  = deliveries * bytes_per_delivery + N * tick_hz * header_bytes   per second
  commits    = N * changes_per_player_s                   write-through database commits per second
  n_max      = largest N whose cpu stays at or below cpu_budget
  PASS when cpu <= cpu_budget, out_mbit <= uplink_mbit and commits <= db_commits_budget
"""
import csv
import sys

KEYS = ["target_ccu", "headroom", "u", "mobs", "u_mob", "cost_us", "cpu_budget",
        "bytes_per_delivery", "header_bytes", "tick_hz", "uplink_mbit",
        "changes_per_player_s", "db_commits_budget"]


def deliveries(n, p):
    return p["u"] * n * (n - 1) + p["mobs"] * p["u_mob"] * n


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    with open(sys.argv[1], newline="") as f:
        p = {}
        for row in csv.DictReader(f):
            v = (row.get("value") or "").strip()
            if v:
                p[row["key"].strip()] = float(v)
    missing = [k for k in KEYS if k not in p]
    if missing:
        print("NOT READY: missing " + ", ".join(missing))
        sys.exit(1)

    N = round(p["headroom"] * p["target_ccu"])
    d = deliveries(N, p)
    cpu = d * p["cost_us"] / 1e6
    out_bytes = d * p["bytes_per_delivery"] + N * p["tick_hz"] * p["header_bytes"]
    out_mbit = out_bytes * 8 / 1e6
    commits = N * p["changes_per_player_s"]
    n_max = 1
    while deliveries(n_max + 1, p) * p["cost_us"] / 1e6 <= p["cpu_budget"]:
        n_max += 1

    print(f"Load-test players N        {N}")
    print(f"Deliveries per second      {d:,.0f}")
    print(f"CPU on deliveries          {cpu:.1%} of one core (budget {p['cpu_budget']:.0%})")
    print(f"Outbound                   {out_bytes / 1000:,.1f} kB/s = {out_mbit:.2f} Mbit/s "
          f"(budget {p['uplink_mbit']:g})")
    print(f"Per client outbound        {out_bytes / N / 1000:.1f} kB/s")
    print(f"Database commits           {commits:.1f} per second (budget {p['db_commits_budget']:g})")
    print(f"Largest crowd within budget {n_max} players")
    ok = cpu <= p["cpu_budget"] and out_mbit <= p["uplink_mbit"] and commits <= p["db_commits_budget"]
    print("PASS" if ok else "NOT READY: a budget is exceeded")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
