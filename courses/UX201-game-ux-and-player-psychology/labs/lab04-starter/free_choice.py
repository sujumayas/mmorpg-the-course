#!/usr/bin/env python3
"""UX201 Lab 04 starter: analyse a small free-choice experiment.

Standard library only. Run:
    python3 free_choice.py free_choice_data.csv
    python3 free_choice.py free_choice_data.csv --boot 5000 --seed 3

Input CSV columns (one row per participant):
    participant, group, baseline_s, free_choice_s, interest_1to7
    - group: "reward" or "control"
    - baseline_s: seconds spent on the puzzle game in the first (unrewarded) free period
    - free_choice_s: seconds spent on it in the final free period, after any reward was withdrawn
    - interest_1to7: the participant's answer to "How interesting did you find the puzzles?" (1-7)

What it prints (UX201 week 4, section 2):
    - group means and standard deviations of free_choice_s and of the change (free_choice_s - baseline_s)
    - Cohen's d for the change, reward minus control, using the pooled standard deviation
    - a bootstrap 95% interval for d (resampling participants within each group)
    - the same for self-reported interest
    - the meta-analysis values to compare against (Deci, Koestner & Ryan 1999)
"""
import argparse
import csv
import math
import random
import statistics as st

META = {
    "engagement-contingent": -0.40,
    "completion-contingent": -0.36,
    "performance-contingent": -0.28,
    "positive feedback": 0.33,
}


def cohen_d(a, b):
    """Standardised mean difference a - b with pooled SD. Returns nan if undefined."""
    if len(a) < 2 or len(b) < 2:
        return float("nan")
    va, vb = st.variance(a), st.variance(b)
    pooled = math.sqrt(((len(a) - 1) * va + (len(b) - 1) * vb) / (len(a) + len(b) - 2))
    if pooled == 0:
        return float("nan")
    return (st.mean(a) - st.mean(b)) / pooled


def boot_ci(a, b, n, rng):
    ds = []
    for _ in range(n):
        ra = [rng.choice(a) for _ in a]
        rb = [rng.choice(b) for _ in b]
        d = cohen_d(ra, rb)
        if not math.isnan(d):
            ds.append(d)
    ds.sort()
    if not ds:
        return float("nan"), float("nan")
    return ds[int(0.025 * len(ds))], ds[int(0.975 * len(ds)) - 1]


def describe(label, xs):
    sd = st.stdev(xs) if len(xs) > 1 else float("nan")
    return f"{label:<10} n={len(xs):<3} mean={st.mean(xs):8.1f}  sd={sd:8.1f}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--boot", type=int, default=2000, help="bootstrap resamples")
    ap.add_argument("--seed", type=int, default=1)
    args = ap.parse_args()
    rng = random.Random(args.seed)

    rows = list(csv.DictReader(open(args.csv, newline="")))
    groups = {"reward": [], "control": []}
    for r in rows:
        g = r["group"].strip().lower()
        if g not in groups:
            raise SystemExit(f"unknown group {g!r} for participant {r['participant']}")
        groups[g].append(r)

    for field, label in [("free_choice_s", "Final free-choice time (s)"), ("change", "Change from baseline (s)"),
                         ("interest_1to7", "Self-reported interest (1-7)")]:
        vals = {}
        for g, rs in groups.items():
            if field == "change":
                vals[g] = [float(r["free_choice_s"]) - float(r["baseline_s"]) for r in rs]
            else:
                vals[g] = [float(r[field]) for r in rs]
        print(f"\n== {label}")
        for g in ("reward", "control"):
            print("  " + describe(g, vals[g]))
        d = cohen_d(vals["reward"], vals["control"])
        lo, hi = boot_ci(vals["reward"], vals["control"], args.boot, rng)
        print(f"  Cohen's d (reward - control) = {d:+.2f}   bootstrap 95% interval [{lo:+.2f}, {hi:+.2f}]")

    print("\n== Meta-analysis free-choice effect sizes for comparison (Deci, Koestner & Ryan 1999)")
    for k, v in META.items():
        print(f"  {k:<24} d = {v:+.2f}")
    print("\nRead the interval, not only d. With about 6 people per group the interval is usually wider than 1.")


if __name__ == "__main__":
    main()
