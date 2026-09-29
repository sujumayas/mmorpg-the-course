#!/usr/bin/env python3
"""PR301 lab 05: do the mob camps feed the players who will stand in them? Standard library only.

Usage: python check_camps.py camps.csv [--target 0.8] [--tmin 20] [--tmax 90]

camps.csv columns: camp, spawns, respawn_s, ttk_s, travel_s, players (comma-free list of player
counts to test, separated by spaces), dynamic (y or n).
Model (PR301 week 5, section 2):
  k      = 60 / (ttk_s + travel_s)            kills per minute one player wants
  lambda = players * k                        kills per minute the camp is asked for
  mu     = spawns * 60 / respawn_s            kills per minute the camp can supply
  rho    = lambda / mu                        PASS needs rho <= target at every tested count
  idle   = max(0, 1 - mu / lambda)            share of time players wait for a spawn
  dynamic respawn: respawn_s(P) = clamp(spawns * 60 * target / lambda, tmin, tmax)
"""
import argparse
import csv
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("camps")
    ap.add_argument("--target", type=float, default=0.8)
    ap.add_argument("--tmin", type=float, default=20)
    ap.add_argument("--tmax", type=float, default=90)
    a = ap.parse_args()
    with open(a.camps, newline="") as f:
        rows = list(csv.DictReader(f))
    ok = bool(rows)
    print(f"{'camp':<12}{'P':>4}{'respawn s':>10}{'demand/min':>11}{'supply/min':>11}{'rho':>7}{'idle':>7}")
    for r in rows:
        M = float(r["spawns"])
        T0 = float(r["respawn_s"])
        k = 60 / (float(r["ttk_s"]) + float(r["travel_s"]))
        dyn = r["dynamic"].strip().lower() == "y"
        for P in [int(x) for x in r["players"].split()]:
            lam = P * k
            T = T0
            if dyn and lam > 0:
                T = min(max(M * 60 * a.target / lam, a.tmin), a.tmax)
            mu = M * 60 / T
            rho = lam / mu
            idle = max(0.0, 1 - mu / lam) if lam else 0.0
            flag = "" if rho <= a.target else "  OVER"
            ok = ok and rho <= a.target
            print(f"{r['camp']:<12}{P:>4}{T:>10.1f}{lam:>11.1f}{mu:>11.1f}{rho:>7.2f}{idle:>7.0%}{flag}")
    print("PASS" if ok else "NOT READY")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
