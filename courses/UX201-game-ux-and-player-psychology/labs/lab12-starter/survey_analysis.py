"""UX201 Lab 12 starter: raw vs weighted survey results, with Wilson intervals.

Usage:
    python survey_analysis.py responses.csv population.csv [item]

responses.csv  one row per respondent: respondent_id, group, then one column
               per Likert item scored 1-7 (7 = strongly agree). Reverse-coded
               items must have names ending in "_r"; the script flips them
               (8 - score) before any analysis.
population.csv group, players  (group sizes from telemetry, or from the
               invitation list if you invited a random sample).
item           the item to analyse (default: first item column). "Satisfied"
               means a score of 5, 6 or 7 (top-3-box on a 7-point scale).

Output: per-group counts and satisfaction, the raw share satisfied with its
Wilson 95% interval, the weighted share, and the response-rate ratio k
between the most- and least-responsive groups. Also prints how many
interviews give an 80% chance of hearing a problem held by 10-30% of players.
"""
import csv
import math
import sys
from collections import defaultdict

Z = 1.96


def wilson(k, n, z=Z):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    den = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return centre - half, centre + half


def main(resp_path, pop_path, item=None):
    rows = list(csv.DictReader(open(resp_path, newline="")))
    items = [c for c in rows[0] if c not in ("respondent_id", "group")]
    item = item or items[0]
    for r in rows:
        for c in items:
            if c.endswith("_r"):
                r[c] = str(8 - int(r[c]))
    pop = {r["group"]: float(r["players"]) for r in csv.DictReader(open(pop_path, newline=""))}
    total_players = sum(pop.values())

    n_g, sat_g = defaultdict(int), defaultdict(int)
    for r in rows:
        n_g[r["group"]] += 1
        sat_g[r["group"]] += int(r[item]) >= 5
    n = sum(n_g.values())
    k_sat = sum(sat_g.values())

    print(f"Item: {item}   respondents: {n}")
    print(f"{'group':<10}{'players':>9}{'resp':>6}{'resp rate':>11}{'sat %':>8}")
    rates = {}
    for g in pop:
        rate = n_g[g] / pop[g]
        rates[g] = rate
        s = 100 * sat_g[g] / n_g[g] if n_g[g] else float("nan")
        print(f"{g:<10}{pop[g]:9.0f}{n_g[g]:6d}{100*rate:10.2f}%{s:8.1f}")

    lo, hi = wilson(k_sat, n)
    raw = k_sat / n
    weighted = sum(pop[g] / total_players * sat_g[g] / n_g[g] for g in pop if n_g[g])
    g_hi, g_lo = max(rates, key=rates.get), min(rates, key=rates.get)
    print(f"\nRaw satisfied:      {100*raw:.1f}%  (Wilson 95%: {100*lo:.1f}% to {100*hi:.1f}%)")
    print(f"Weighted satisfied: {100*weighted:.1f}%")
    print(f"Response-rate ratio {g_hi}/{g_lo}: {rates[g_hi]/rates[g_lo]:.2f}")

    print("\nInterviews for an 80% chance of hearing a problem at least once:")
    for p in (0.10, 0.15, 0.20, 0.30):
        print(f"  p = {p:.2f}: n >= {math.ceil(math.log(0.2) / math.log(1 - p))}")


if __name__ == "__main__":
    a = sys.argv[1:]
    main(a[0] if a else "responses.csv", a[1] if len(a) > 1 else "population.csv",
         a[2] if len(a) > 2 else None)
