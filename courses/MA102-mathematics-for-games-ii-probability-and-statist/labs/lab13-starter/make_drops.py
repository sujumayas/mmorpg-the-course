"""Instructor script: regenerate drops.csv with a new hidden rate before release.

    python make_drops.py 0.0xx

3,000 kills by 150 players (20 kills each), seed 13.
"""
import csv
import sys

from mulberry32 import Mulberry32

rate = float(sys.argv[1])
rng = Mulberry32(13)
with open("drops.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["kill_id", "player_id", "dropped"])
    for i in range(3000):
        w.writerow([i + 1, f"p{i // 20 + 1:03d}", rng.bernoulli(rate)])
