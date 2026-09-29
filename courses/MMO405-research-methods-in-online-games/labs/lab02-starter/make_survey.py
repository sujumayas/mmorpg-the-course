"""Writes wellbeing.csv, the invented 6,000-player dataset for MMO405 lab 02.
Run: python make_survey.py   (already run once; the CSV ships with the starter)

Columns: player_id, server (A/B/C), voice_chat (1 if the player used voice chat
in the survey fortnight), wellbeing (a 0-10 scale score, one decimal).
Values are drawn once with a fixed seed and stored, so the CSV, not this script,
is the lab's data.
"""
import csv
import random

SERVERS = {  # server: (players, share using voice chat, mean wellbeing without voice)
    "A": (2000, 0.20, 4.8),
    "B": (2000, 0.40, 5.0),
    "C": (2000, 0.60, 5.3),
}
EFFECT = 0.10   # points added for voice-chat users, on a scale with SD 1.2
SD = 1.2


def build(seed=4052):
    rng = random.Random(seed)
    rows, pid = [], 1
    for server, (n, share, mean) in SERVERS.items():
        for _ in range(n):
            voice = 1 if rng.random() < share else 0
            score = rng.gauss(mean + EFFECT * voice, SD)
            score = min(10.0, max(0.0, score))
            rows.append({"player_id": f"P{pid:05d}", "server": server,
                         "voice_chat": voice, "wellbeing": f"{score:.1f}"})
            pid += 1
    return rows


if __name__ == "__main__":
    with open("wellbeing.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["player_id", "server", "voice_chat", "wellbeing"])
        w.writeheader()
        w.writerows(build())
    print("wrote wellbeing.csv")
