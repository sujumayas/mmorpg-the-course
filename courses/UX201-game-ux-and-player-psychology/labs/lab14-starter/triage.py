"""UX201 Lab 14: findings triage.

Usage:
  python3 triage.py findings.csv
  python3 triage.py findings.csv --n 5 --weights 1,3,10,30 --bar 1 --z 1.96

findings.csv columns: id, title, testers_hit, r1, r2, r3, fix_cost
  testers_hit  number of testers (out of --n) who hit the problem
  r1..r3       independent severity ratings 1-4 (1 cosmetic, 2 minor, 3 major, 4 blocker)
  fix_cost     S, M or L (small, medium, large), from the owner's estimate

Severity = mean of r1..r3 rounded half up. Prints each finding with its Wilson interval,
P, L, U and tier, sorted fix now > investigate > backlog, then by U descending,
and flags findings whose three ratings differ by 2 or more.
Standard-library Python 3 only.
"""
import argparse
import csv
import math

TIERS = ["fix now", "investigate", "backlog"]


def wilson(x, n, z):
    if n == 0:
        return 0.0, 1.0
    p = x / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, centre - half), min(1.0, centre + half)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--n", type=int, default=5, help="number of testers (default 5)")
    ap.add_argument("--weights", default="1,3,10,30", help="w(1),w(2),w(3),w(4)")
    ap.add_argument("--bar", type=float, default=1.0, help="impact bar T (default 1)")
    ap.add_argument("--z", type=float, default=1.96, help="1.96 for 95%%, 1.645 for 90%%")
    a = ap.parse_args()
    w = [float(v) for v in a.weights.split(",")]
    if len(w) != 4:
        raise SystemExit("--weights needs four numbers")

    out = []
    with open(a.csv, newline="") as f:
        for r in csv.DictReader(f):
            x = int(r["testers_hit"])
            ratings = [int(r[k]) for k in ("r1", "r2", "r3")]
            sev = int(math.floor(sum(ratings) / 3 + 0.5))
            lo, hi = wilson(x, a.n, a.z)
            ws = w[sev - 1]
            L, U, P = lo * ws, hi * ws, x / a.n * ws
            tier = TIERS[0] if L >= a.bar else TIERS[1] if U >= a.bar else TIERS[2]
            split = max(ratings) - min(ratings) >= 2
            out.append((TIERS.index(tier), -U, r["id"], r["title"], x, sev, lo, hi,
                        P, L, U, tier, r.get("fix_cost", ""), split))

    out.sort()
    print(f"n = {a.n}, weights = {a.weights}, bar T = {a.bar}, z = {a.z}")
    print(f"{'id':<5}{'x/n':>6}{'sev':>4}{'interval':>16}{'P':>7}{'L':>7}{'U':>7}"
          f"  {'tier':<12}{'cost':<5}title")
    for (_, _, fid, title, x, sev, lo, hi, P, L, U, tier, cost, split) in out:
        flag = "  [raters split]" if split else ""
        print(f"{fid:<5}{f'{x}/{a.n}':>6}{sev:>4}{f'{lo:.1%}-{hi:.1%}':>16}"
              f"{P:>7.2f}{L:>7.2f}{U:>7.2f}  {tier:<12}{cost:<5}{title}{flag}")
    by_freq = sorted(out, key=lambda o: (-o[4], o[2]))
    print("frequency order:", ", ".join(o[2] for o in by_freq))


if __name__ == "__main__":
    main()
