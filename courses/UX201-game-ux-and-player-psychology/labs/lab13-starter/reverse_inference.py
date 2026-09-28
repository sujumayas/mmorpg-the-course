"""UX201 Lab 13: what does a peak mean?

Usage:
  python3 reverse_inference.py session_T2.csv
  python3 reverse_inference.py session_T2.csv --context scare
  python3 reverse_inference.py session_T2.csv --blind-rule fear

For the chosen windows (all, or one context), prints per coded state:
windows n_s, peaks, observed hit rate h_s = peaks / n_s, and P(state | peak).
--blind-rule S reports how often a rule that reads every peak as state S is right.
Standard-library Python 3 only.
"""
import argparse
import csv
from collections import Counter

STATES = ["neutral", "fear", "frustration", "excitement"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--context", default="all",
                    help="all, none, scare, death or solve (default all)")
    ap.add_argument("--blind-rule", default=None, choices=STATES)
    a = ap.parse_args()

    with open(a.csv, newline="") as f:
        rows = list(csv.DictReader(f))
    if a.context != "all":
        rows = [r for r in rows if r["context"] == a.context]
    if not rows:
        raise SystemExit("no windows match that context")

    windows = Counter(r["coded_state"] for r in rows)
    peaks = Counter(r["coded_state"] for r in rows if r["peak"] == "1")
    total_peaks = sum(peaks.values())

    print(f"context = {a.context}: {len(rows)} windows, {total_peaks} peaks")
    print(f"{'state':<12}{'windows':>8}{'peaks':>7}{'hit rate':>10}{'P(s|peak)':>11}")
    for s in STATES:
        n, k = windows[s], peaks[s]
        h = k / n if n else float("nan")
        post = k / total_peaks if total_peaks else float("nan")
        print(f"{s:<12}{n:>8}{k:>7}{h:>10.2f}{post:>11.1%}")
    aroused = total_peaks - peaks["neutral"]
    if total_peaks:
        print(f"share of peaks from an aroused state: {aroused / total_peaks:.1%}")
    if a.blind_rule and total_peaks:
        print(f"rule 'every peak = {a.blind_rule}' is right "
              f"{peaks[a.blind_rule] / total_peaks:.1%} of the time")


if __name__ == "__main__":
    main()
