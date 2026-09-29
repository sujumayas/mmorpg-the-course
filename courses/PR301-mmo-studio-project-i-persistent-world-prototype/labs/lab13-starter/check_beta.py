#!/usr/bin/env python3
"""PR301 lab 13: check the beta invitation plan and the load-test headroom. Standard library only.

Usage: python check_beta.py turnout.csv loadtest.csv

Model (PR301 week 13, sections 2 and 3):
  s = alpha logins / alpha invitations, with a Wilson 95% interval
  e = alpha event attendees / alpha logins;  a = e + (1 - e) x LP  (weeks 9 and 10)
  p = s x a; humans online at the event ~ Binomial(invitations, p)
  I_needed = smallest I with P(online >= target) >= goal
  The planned invitations must reach I_needed at the LOW end of s with the planned e.
  A planned e above the alpha value needs a written e_assumption.
  Load test, the week 6 tick rule at the load-test crowd (headroom x target, 100 players):
  mean tick at that crowd must be <= mean_limit_ms (60 at 10 Hz, the 0.6 CPU budget).
  Capacity = players where p99 crosses p99_limit_ms (80, the D3 trigger), interpolated
  between the two measured steps around the crossing. Headroom = capacity / target must be
  >= headroom (2, week 2). If no step crosses the limit, capacity is "at least" the largest step.
"""
import csv
import sys
from math import exp, lgamma, log, sqrt


def wilson(k, n, z=1.96):
    p = k / n
    c = (p + z * z / (2 * n)) / (1 + z * z / n)
    h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return c - h, c + h


def p_at_least(S, p, T):
    if p <= 0:
        return 0.0
    if p >= 1:
        return 1.0 if S >= T else 0.0
    lp, lq = log(p), log(1 - p)
    return sum(exp(lgamma(S + 1) - lgamma(k + 1) - lgamma(S - k + 1) + k * lp + (S - k) * lq)
               for k in range(T, S + 1))


def s_needed(p, T, goal):
    S = T
    while p_at_least(S, p, T) < goal:
        S += 1
        if S > 5000:
            return None
    return S


def interp(steps, x):
    for (x0, y0), (x1, y1) in zip(steps, steps[1:]):
        if x0 <= x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return None


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    problems = []
    with open(sys.argv[1], newline="") as f:
        v = {r["key"].strip(): r["value"].strip() for r in csv.DictReader(f)}
    need = ["alpha_invited", "alpha_logged_in", "alpha_attended", "LP", "planned_e", "target",
            "goal", "planned_invitations", "mean_limit_ms", "p99_limit_ms", "headroom"]
    missing = [k for k in need if not v.get(k)]
    if missing:
        sys.exit(f"turnout.csv: missing {missing}\nNOT READY")
    n, k, ke = int(v["alpha_invited"]), int(v["alpha_logged_in"]), int(v["alpha_attended"])
    LP, e, T, goal = float(v["LP"]), float(v["planned_e"]), int(v["target"]), float(v["goal"])
    a = e + (1 - e) * LP
    inv = int(v["planned_invitations"])
    mean_lim, p99_lim, head = float(v["mean_limit_ms"]), float(v["p99_limit_ms"]), float(v["headroom"])
    s = k / n
    lo, hi = wilson(k, n)
    e_alpha = ke / k
    a_alpha = e_alpha + (1 - e_alpha) * LP
    elo, ehi = wilson(ke, k)
    print(f"show rate s {s:.3f} (Wilson {lo:.1%} to {hi:.1%})  "
          f"event attendance e {e_alpha:.3f} (Wilson {elo:.1%} to {ehi:.1%})  a {a_alpha:.3f}")
    for name, ss in (("alpha s", s), ("low-end s", lo)):
        for aname, aa in (("alpha e", a_alpha), ("planned e", a)):
            print(f"  {name:9} {aname:9} p={ss * aa:.3f}  I_needed={s_needed(ss * aa, T, goal)}"
                  f"  P(>={T} | I={inv})={p_at_least(inv, ss * aa, T):.1%}")
    i_low = s_needed(lo * a, T, goal)
    if i_low is None or inv < i_low:
        problems.append(f"planned invitations {inv} below {i_low} needed at low-end s with planned e")
    if e > e_alpha + 1e-9 and not v.get("e_assumption", ""):
        problems.append("planned e is above the alpha value: name the lever in e_assumption")
    with open(sys.argv[2], newline="") as f:
        rows = [r for r in csv.DictReader(f) if r["p99_ms"].strip()]
    steps = sorted((float(r["players"]), float(r["p99_ms"])) for r in rows)
    means = sorted((float(r["players"]), float(r["mean_ms"])) for r in rows if r["mean_ms"].strip())
    if len(steps) < 3:
        problems.append("need at least three load-test steps with p99 recorded")
    crowd = head * T
    at_target = interp(steps, T)
    if at_target is not None:
        print(f"p99 at {T} players: {at_target:.1f} ms (for information)")
    mean_crowd = interp(means, crowd)
    if mean_crowd is None:
        problems.append(f"load test must step to {crowd:g} players with the mean tick recorded")
    else:
        print(f"mean tick at {crowd:g} players: {mean_crowd:.1f} ms (limit {mean_lim:g} ms)")
        if mean_crowd > mean_lim:
            problems.append(f"mean tick {mean_crowd:.1f} ms at {crowd:g} players exceeds {mean_lim:g} ms")
    cap, exact = None, True
    for (x0, y0), (x1, y1) in zip(steps, steps[1:]):
        if y0 <= p99_lim < y1:
            cap = x0 + (p99_lim - y0) / (y1 - y0) * (x1 - x0)
            break
    if cap is None and steps:
        cap, exact = (0.0, True) if steps[0][1] > p99_lim else (steps[-1][0], False)
    if cap is not None:
        word = "" if exact else "at least "
        print(f"capacity (p99 crosses {p99_lim:g} ms) {word}{cap:.1f} players, "
              f"headroom {word}{cap / T:.2f} (need {head:g})")
        if cap / T < head - 1e-9:
            problems.append(f"headroom {cap / T:.2f} below {head:g}")
    for p in problems:
        print("  -", p)
    print("PASS" if not problems else "NOT READY")
    sys.exit(0 if not problems else 1)


if __name__ == "__main__":
    main()
