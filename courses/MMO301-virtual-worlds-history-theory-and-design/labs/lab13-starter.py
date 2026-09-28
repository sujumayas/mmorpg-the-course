#!/usr/bin/env python3
"""MMO301 Lab 13 starter: the density-churn model from week 13.

Standard library only. Run:
    python3 lab13-starter.py                      # default launch plan, 40 shards, no merge
    python3 lab13-starter.py --merge 12 --after 10
    python3 lab13-starter.py --shards 20 --arrivals 4000 --csv run.csv

All parameters are invented for teaching. See the week 13 lecture, section 2.
"""
import argparse
import csv


def churn(d, c0, c1, H):
    """Monthly churn rate for a shard with d players."""
    return c0 + c1 * H / (H + d)


def break_even(S, p, F, k):
    """Population at which revenue p*N equals cost F + k*S."""
    return (F + k * S) / p


def simulate(N0, S, A, months, c0, c1, H, p, F, k, merge=None, after=None):
    """Return one dict per month 0..months."""
    rows = []
    N = N0
    for t in range(months + 1):
        s = after if (merge is not None and t >= merge) else S
        d = N / s
        c = churn(d, c0, c1, H)
        rows.append({
            "month": t, "shards": s, "players": round(N), "per_shard": round(d),
            "churn": round(c, 4), "revenue": round(p * N),
            "cost": F + k * s, "break_even": round(break_even(s, p, F, k)),
        })
        N = N * (1 - c) + A
    return rows


def resting_population(S, A, c0, c1, H):
    """Solve N * churn(N/S) = A by bisection."""
    lo, hi = 0.0, 1e7
    for _ in range(200):
        mid = (lo + hi) / 2
        if mid * churn(mid / S, c0, c1, H) < A:
            lo = mid
        else:
            hi = mid
    return mid


# TODO (step 3): write fit_to_timeline(points, ...) that tries a grid of A and S
# values and returns the pair whose simulated players are closest (sum of squared
# relative errors) to your case's public data points [(month, players), ...].

# TODO (step 4): write sunset_month(rows, months_below=6) that returns the first
# month the world has been below break-even for `months_below` months in a row.


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--players", type=float, default=200_000)
    ap.add_argument("--shards", type=int, default=40)
    ap.add_argument("--arrivals", type=float, default=6_000)
    ap.add_argument("--months", type=int, default=60)
    ap.add_argument("--c0", type=float, default=0.03)
    ap.add_argument("--c1", type=float, default=0.20)
    ap.add_argument("--H", type=float, default=2_000)
    ap.add_argument("--price", type=float, default=15)
    ap.add_argument("--fixed", type=float, default=900_000)
    ap.add_argument("--per-shard", type=float, default=10_000)
    ap.add_argument("--merge", type=int, default=None, help="month of merge")
    ap.add_argument("--after", type=int, default=10, help="shards after merge")
    ap.add_argument("--csv", default=None)
    a = ap.parse_args()

    rows = simulate(a.players, a.shards, a.arrivals, a.months, a.c0, a.c1, a.H,
                    a.price, a.fixed, a.per_shard, a.merge, a.after)
    for r in rows[:4] + rows[6::6]:
        print(r)
    below = [r["month"] for r in rows if r["players"] < r["break_even"]]
    print("months below break-even:", len(below), "first:", below[0] if below else None)
    final_S = a.after if a.merge is not None else a.shards
    print("resting population:", round(resting_population(final_S, a.arrivals, a.c0, a.c1, a.H)))
    if a.csv:
        with open(a.csv, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)


if __name__ == "__main__":
    main()
