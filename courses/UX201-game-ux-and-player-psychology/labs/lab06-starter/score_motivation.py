#!/usr/bin/env python3
"""UX201 Lab 06 starter: score one audience with two instruments.

Standard library only. Run:
    python3 score_motivation.py motivation_data.csv
    python3 score_motivation.py motivation_data.csv --factor 0.75

Input: see item_bank.md. Columns respondent, age_band, R_A1..R_K4 (1-5), FC01..FC12 (A/E/S/K).

Prints (UX201 week 6, section 2):
    - per respondent: rating means per type (1-5), forced-choice % per type (wins / 6), their sum,
      and the primary motivation from Yee's rule (top x factor > second) applied to the rating means
    - per format: Pearson correlations between every pair of types across respondents
    - the share of respondents with no primary motivation, and the forced-choice "type" count
"""
import argparse
import csv
import itertools
import math
import statistics as st

TYPES = ["A", "E", "S", "K"]
NAMES = {"A": "Achieve", "E": "Explore", "S": "Social", "K": "Compete"}
FC_ITEMS = [f"FC{i:02d}" for i in range(1, 13)]
FC_PER_TYPE = 6


def pearson(x, y):
    if len(x) < 3:
        return float("nan")
    mx, my = st.mean(x), st.mean(y)
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    if sxx == 0 or syy == 0:
        return float("nan")
    return sxy / math.sqrt(sxx * syy)


def primary(scores, factor):
    order = sorted(TYPES, key=lambda t: -scores[t])
    top, second = scores[order[0]], scores[order[1]]
    return NAMES[order[0]] if top * factor > second else "none"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--factor", type=float, default=0.75)
    args = ap.parse_args()

    rows = list(csv.DictReader(open(args.csv, newline="")))
    rating, forced = [], []
    print(f"{'resp':<6}" + "".join(f"R_{t:<6}" for t in TYPES) + "".join(f"FC_{t:<6}" for t in TYPES)
          + "FC_sum  primary(rating)  top FC type")
    no_primary = 0
    fc_types = {t: 0 for t in TYPES}
    for r in rows:
        rm = {t: st.mean(float(r[f"R_{t}{i}"]) for i in range(1, 5)) for t in TYPES}
        wins = {t: 0 for t in TYPES}
        for item in FC_ITEMS:
            choice = r[item].strip().upper()
            if choice not in wins:
                raise SystemExit(f"{r['respondent']}: {item} has {choice!r}, expected A, E, S or K")
            wins[choice] += 1
        fc = {t: 100.0 * wins[t] / FC_PER_TYPE for t in TYPES}
        rating.append(rm)
        forced.append(fc)
        p = primary(rm, args.factor)
        no_primary += p == "none"
        top_fc = max(TYPES, key=lambda t: fc[t])
        fc_types[top_fc] += 1
        print(f"{r['respondent']:<6}" + "".join(f"{rm[t]:<8.2f}" for t in TYPES)
              + "".join(f"{fc[t]:<9.1f}" for t in TYPES) + f"{sum(fc.values()):<8.0f}{p:<17}{NAMES[top_fc]}")

    for label, data in [("Rating scale", rating), ("Forced choice", forced)]:
        print(f"\n== Correlations between types, {label} (n = {len(data)})")
        rs = []
        for a, b in itertools.combinations(TYPES, 2):
            r = pearson([d[a] for d in data], [d[b] for d in data])
            rs.append(r)
            print(f"  {NAMES[a]:<8} x {NAMES[b]:<8} r = {r:+.2f}")
        valid = [x for x in rs if not math.isnan(x)]
        if valid:
            print(f"  mean r = {st.mean(valid):+.2f}" + ("   (forced choice: theory -0.33 when interests are unrelated)"
                                                       if label == "Forced choice" else ""))

    n = len(rows)
    print(f"\nNo primary motivation (rating means, factor {args.factor}): {no_primary} of {n} "
          f"({100 * no_primary / n:.0f}%). Yee's MMO sample: 43% on three components.")
    print("Top forced-choice type (ties go to the first in A, E, S, K order): "
          + ", ".join(f"{NAMES[t]} {c}" for t, c in fc_types.items()))


if __name__ == "__main__":
    main()
