"""Regenerate pairs.csv: 12 invented original/replication pairs from online-game research.

Every study here is fictional. The numbers were drawn so that some pairs show the
significance filter, some show a changed game, and some replicate cleanly.
Run: python make_pairs.py
"""
import csv
import random
from math import sqrt
from pathlib import Path

TOPICS = [
    ("mentor NPC and guild joining", 0.20, 50, 250, 0),
    ("voice chat and raid success", 0.10, 40, 200, 0),
    ("daily login rewards and D30 retention", 0.05, 800, 2000, 0),
    ("toxicity warning and repeat reports", 0.30, 60, 150, 0),
    ("cosmetic shop and perceived fairness", 0.00, 35, 180, 0),
    ("tutorial length and first-session quits", 0.25, 400, 400, 0),
    ("guild size and weekly play hours", 0.15, 120, 300, 1),
    ("PvP ladder resets and churn", 0.20, 30, 120, 1),
    ("housing system and social ties", 0.40, 25, 100, 0),
    ("matchmaking wait and abandonment", 0.35, 1500, 1500, 1),
    ("loot pity timer and spending", 0.00, 45, 250, 0),
    ("crafting depth and economy participation", 0.12, 70, 350, 0),
]


def main(seed=405):
    rng = random.Random(seed)
    rows = []
    for i, (topic, delta, n_o, n_r, patched) in enumerate(TOPICS, start=1):
        se_o = sqrt(2 / n_o)
        while True:  # the original passed the significance filter in the predicted direction
            d_o = rng.gauss(delta, se_o)
            if d_o > 1.96 * se_o:
                break
        shift = -0.15 if patched else 0.0  # the game changed between the two studies
        d_r = rng.gauss(delta + shift, sqrt(2 / n_r))
        rows.append({"study": f"S{i:02d}", "topic": topic, "d_orig": f"{d_o:.3f}",
                     "n_orig": n_o, "d_rep": f"{d_r:.3f}", "n_rep": n_r,
                     "patch_changed": patched})
    with open(Path(__file__).parent / "pairs.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()
