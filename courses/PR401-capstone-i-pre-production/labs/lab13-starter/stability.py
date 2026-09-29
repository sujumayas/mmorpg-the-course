#!/usr/bin/env python3
"""PR401 lab 13: stability evidence for the review build. Standard library only.

Usage: python stability.py sessions.csv review.csv

sessions.csv  session,build,kind,hours,players,min_concurrent,client_crashes,server_crashes
              kind is playtest or soak; min_concurrent is the lowest number of connected
              players or bots while the session ran (use the steady part of the session)
review.csv    key,value rows: build, demo_players, demo_minutes, target,
              reconnect_tested (yes/no), longest_session_hours

Counts client exposure (player-hours, playtests only; headless bots don't exercise
the client) and server exposure (hours with min_concurrent >= demo_players), on the
review build only. Prints point estimates, 95% upper bounds and the pessimistic
chance of a clean demo, then PASS or NOT READY. Exits 1 when anything fails.
"""
import csv
import math
import sys


def poisson_upper(k, conf=0.95):
    """One-sided upper limit: mu with P(X <= k | mu) = 1 - conf (exact, by bisection)."""
    def cdf(mu):
        term = total = math.exp(-mu)
        for i in range(1, k + 1):
            term *= mu / i
            total += term
        return total
    lo, hi = 0.0, 10.0 + 5 * k
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if cdf(mid) > 1 - conf else (lo, mid)
    return (lo + hi) / 2


def read(path):
    with open(path, newline="") as f:
        return [{k.strip(): (v or "").strip() for k, v in r.items()} for r in csv.DictReader(f)]


def main(sessions_path, review_path):
    cfg = {r["key"]: r["value"] for r in read(review_path)}
    problems = []
    build = cfg.get("build", "")
    n_demo = float(cfg.get("demo_players", 8))
    t_demo = float(cfg.get("demo_minutes", 30)) / 60
    target = float(cfg.get("target", 0.9))
    longest = float(cfg.get("longest_session_hours", 3))
    reconnect = cfg.get("reconnect_tested", "no").lower() == "yes"
    Ec = Es = 0.0
    kc = ks = 0
    long_soak = False
    for r in read(sessions_path):
        sid = r.get("session", "?")
        if r.get("kind") not in ("playtest", "soak"):
            problems.append(f"session {sid}: kind must be playtest or soak")
            continue
        try:
            h, p, mc = float(r["hours"]), float(r["players"]), float(r["min_concurrent"])
            cc, sc = int(r["client_crashes"]), int(r["server_crashes"])
        except (KeyError, ValueError):
            problems.append(f"session {sid}: a numeric field is missing or not a number")
            continue
        if r.get("build") != build:
            print(f"session {sid}: build {r.get('build')} is not the review build {build}; not counted")
            continue
        if r["kind"] == "playtest":
            Ec += p * h
            kc += cc
        if mc >= n_demo:
            Es += h
            ks += sc
        if r["kind"] == "soak" and h >= longest:
            long_soak = True
    print(f"review build {build}: client {Ec:.1f} player-hours, {kc} crashes; "
          f"server {Es:.1f} h at load >= {n_demo:.0f}, {ks} crashes")
    if Ec == 0 or Es == 0:
        problems.append("no client or no server exposure on the review build")
        lc_up = ls_up = float("inf")
    else:
        lc_up, ls_up = poisson_upper(kc) / Ec, poisson_upper(ks) / Es
        print(f"client rate: point {kc / Ec:.3f}, upper {lc_up:.3f} per player-hour")
        print(f"server rate: point {ks / Es:.3f}, upper {ls_up:.3f} per hour")
    p_client = math.exp(-n_demo * lc_up * t_demo)
    p_server = math.exp(-ls_up * t_demo)
    print(f"pessimistic chance of no client crash in the demo: {p_client:.2f}")
    print(f"pessimistic chance the server survives the demo:  {p_server:.2f}")
    print(f"pessimistic chance of a fully clean demo:          {p_client * p_server:.2f}")
    if p_server < target:
        need = poisson_upper(0) / (-math.log(target) / t_demo)
        problems.append(f"server chance {p_server:.2f} below target {target}; "
                        f"with zero crashes you need about {need:.0f} server-hours at load")
    if p_client < target and not reconnect:
        problems.append(f"client chance {p_client:.2f} below target {target} and reconnect not tested")
    if not long_soak:
        problems.append(f"no soak of at least {longest} h on the review build")
    for p in dict.fromkeys(problems):
        print("  -", p)
    print("PASS" if not problems else "NOT READY")
    return 0 if not problems else 1


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    sys.exit(main(*sys.argv[1:]))
