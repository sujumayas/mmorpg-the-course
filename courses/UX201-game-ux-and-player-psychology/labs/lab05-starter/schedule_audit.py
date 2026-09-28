#!/usr/bin/env python3
"""UX201 Lab 05 starter: audit the reward schedules in a play session.

Standard library only (matplotlib is used for plots if it is installed; otherwise the script
writes CSV files you can chart in a spreadsheet). Run:
    python3 schedule_audit.py reward_log.csv
    python3 schedule_audit.py reward_log.csv --k 0.5 --theta 15 --plots

Input CSV columns (one row per reward event you observed):
    time_s, stream, trigger, actions_since_last, paid, notes
    - time_s: seconds since the start of the session when the reward arrived
    - stream: a short name for the reward source ("wolf quest", "chest drops", "daily reset")
    - trigger: "count" if it depends on how many actions you did, "time" if on time passing
    - actions_since_last: how many relevant actions (kills, pulls, harvests) since the last
      reward in this stream; leave blank for time-triggered streams
    - paid: 1 if a draw can be bought with real money or a currency that money buys, else 0
    - notes: free text

For each stream the script prints:
    - count, mean gap (actions or seconds), coefficient of variation (CV = sd / mean)
    - a schedule label: FR / VR for count triggers, FI / VI for time triggers
      (fixed if CV < 0.2, otherwise variable; with fewer than 4 gaps it says "too few events")
    - for ratio streams, the UX201 week 5 model with N = the mean gap:
        FR value right after a reward   = A / (1 + k N)
        VR value (every action)         = sum_d p (1-p)^(d-1) A / (1 + k d), p = 1/N
        whether a player with threshold theta stops after rewards on each schedule
        the dry streak (actions) with under 5% probability on the random version
"""
import argparse
import csv
import math
import statistics as st
from collections import defaultdict

A = 100.0


def fr_values(n, k):
    return [A / (1 + k * (n - j)) for j in range(n)]


def vr_value(n, k):
    p = 1.0 / n
    total, d = 0.0, 1
    while d < 100000:
        term = p * (1 - p) ** (d - 1) * A / (1 + k * d)
        total += term
        if term < 1e-9:
            break
        d += 1
    return total


def dry_streak(n):
    p = 1.0 / n
    if p >= 1:
        return 1
    return math.ceil(math.log(0.05) / math.log(1 - p))


def label(trigger, cv, gaps):
    if gaps < 4:
        return "too few events"
    fixed = cv < 0.2
    if trigger == "count":
        return "FR (fixed ratio)" if fixed else "VR (variable ratio)"
    return "FI (fixed interval)" if fixed else "VI (variable interval)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--k", type=float, default=1.0, help="discount per action (default 1)")
    ap.add_argument("--theta", type=float, default=12.0, help="stop threshold (default 12)")
    ap.add_argument("--plots", action="store_true", help="save PNGs if matplotlib is available")
    args = ap.parse_args()

    streams = defaultdict(list)
    for r in csv.DictReader(open(args.csv, newline="")):
        streams[r["stream"].strip()].append(r)

    cumulative_rows = []
    for name, rows in streams.items():
        rows.sort(key=lambda r: float(r["time_s"]))
        trigger = rows[0]["trigger"].strip().lower()
        paid = any(r.get("paid", "0").strip() == "1" for r in rows)
        if trigger == "count":
            gaps = [float(r["actions_since_last"]) for r in rows if r["actions_since_last"].strip()]
            unit = "actions"
        else:
            times = [float(r["time_s"]) for r in rows]
            gaps = [b - a for a, b in zip(times, times[1:])]
            unit = "s"
        print(f"\n== {name}  ({trigger}-triggered{', PAID DRAWS' if paid else ''})")
        print(f"  rewards logged: {len(rows)}")
        if len(gaps) >= 2:
            m, sd = st.mean(gaps), st.stdev(gaps)
            cv = sd / m if m else float("nan")
            print(f"  mean gap {m:.1f} {unit}, sd {sd:.1f}, CV {cv:.2f} -> {label(trigger, cv, len(gaps))}")
        else:
            m, cv = (gaps[0] if gaps else float("nan")), float("nan")
            print("  fewer than 2 gaps: log more of this stream or treat it as unknown")
        if trigger == "count" and gaps and m >= 1:
            n = max(1, round(m))
            fr = fr_values(n, args.k)
            vr = vr_value(n, args.k)
            print(f"  model with N = {n}, k = {args.k}, theta = {args.theta}:")
            print(f"    FR value after reward {fr[0]:.2f}, before reward {fr[-1]:.2f}; VR value {vr:.2f}")
            print(f"    FR player stops after rewards: {'yes' if fr[0] < args.theta else 'no'}; "
                  f"VR player stops: {'yes' if vr < args.theta else 'no'}")
            print(f"    random version: dry streak under 5% after {dry_streak(n)} actions")
        count = 0
        for r in rows:
            count += 1
            cumulative_rows.append((name, float(r["time_s"]), count))

    with open("cumulative_rewards.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["stream", "time_s", "rewards_so_far"])
        w.writerows(cumulative_rows)
    print("\nWrote cumulative_rewards.csv (rewards over time per stream).")

    if args.plots:
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print("matplotlib not installed; chart cumulative_rewards.csv in a spreadsheet instead.")
            return
        fig, ax = plt.subplots(figsize=(8, 4))
        for name in streams:
            pts = [(t, c) for s, t, c in cumulative_rows if s == name]
            ax.step([p[0] for p in pts], [p[1] for p in pts], where="post", label=name)
        ax.set_xlabel("time (s)")
        ax.set_ylabel("rewards so far")
        ax.legend()
        fig.tight_layout()
        fig.savefig("cumulative_rewards.png", dpi=150)
        print("Wrote cumulative_rewards.png.")


if __name__ == "__main__":
    main()
