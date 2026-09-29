"""MMO405 Lab 07: writes focal_log.csv, a structured focal observation of six
characters in a public hub, one 180-minute session each (seed 707).

Each row is one bout of the behaviour "in conversation" (a chat exchange or
emote exchange with another character): focal_id, start_min, end_min.
Run:  python gen_focal.py
"""
import csv
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
L = 180
# (focal id, number of bouts, mean bout length in minutes)
PROFILES = [("C1", 3, 20.0), ("C2", 6, 8.0), ("C3", 12, 3.0),
            ("C4", 2, 30.0), ("C5", 9, 4.0), ("C6", 18, 1.5)]


def bouts_for(rng, n, mean_len):
    """Place n non-overlapping bouts in [0, L) with gaps of at least 1 minute."""
    while True:
        lengths = [max(1, round(rng.expovariate(1 / mean_len))) for _ in range(n)]
        free = L - sum(lengths) - n
        if free <= 0:
            continue
        cuts = sorted(rng.randint(0, free) for _ in range(n))
        out, t, prev = [], 0, 0
        for length, c in zip(lengths, cuts):
            t += c - prev + 1
            prev = c
            out.append((t, t + length))
            t += length
        if out[-1][1] <= L:
            return out


def main():
    rng = random.Random(707)
    with open(HERE / "focal_log.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["focal_id", "start_min", "end_min"])
        for fid, n, mean_len in PROFILES:
            for s, e in bouts_for(rng, n, mean_len):
                w.writerow([fid, s, e])
    print("wrote focal_log.csv")


if __name__ == "__main__":
    main()
