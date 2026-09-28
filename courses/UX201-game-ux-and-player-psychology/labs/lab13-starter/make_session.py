"""Regenerate session_T2.csv, the invented EDA session used in UX201 Lab 13.

Standard-library Python 3. Deterministic (seed 1313), so every student gets the same file.
Each row is one 5-second window of a 30-minute session (360 windows).
Columns: window, start_s, context, coded_state, peak
  context      event in the game log that started 0-5 s before the window:
               scare, death, solve, or none
  coded_state  observer's coding from face video, think-aloud and replay interview:
               neutral, fear, frustration, excitement
  peak         1 if a skin-conductance response starts in the window (lag already shifted)
The numbers are a teaching data set, not a recording of a real player.
"""
import csv
import random

rng = random.Random(1313)
N = 360
HIT = {"neutral": 0.06, "fear": 0.85, "frustration": 0.75, "excitement": 0.80}
# (context, coded-state weights) for windows that follow each event type
CONTEXT_MIX = {
    "scare": {"neutral": 0.15, "fear": 0.65, "frustration": 0.05, "excitement": 0.15},
    "death": {"neutral": 0.20, "fear": 0.05, "frustration": 0.70, "excitement": 0.05},
    "solve": {"neutral": 0.25, "fear": 0.00, "frustration": 0.05, "excitement": 0.70},
    "none":  {"neutral": 0.88, "fear": 0.04, "frustration": 0.05, "excitement": 0.03},
}
EVENTS = {"scare": 10, "death": 8, "solve": 6}

context = ["none"] * N
for kind, count in EVENTS.items():
    placed = 0
    while placed < count:
        w = rng.randrange(6, N - 3)
        if all(c == "none" for c in context[w:w + 3]):
            for k in range(3):            # each event colours 3 windows (15 s)
                context[w + k] = kind
            placed += 1

rows = []
for w in range(N):
    mix = CONTEXT_MIX[context[w]]
    states, weights = zip(*mix.items())
    state = rng.choices(states, weights)[0]
    peak = 1 if rng.random() < HIT[state] else 0
    rows.append({"window": w + 1, "start_s": w * 5, "context": context[w],
                 "coded_state": state, "peak": peak})

with open("session_T2.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
print("wrote session_T2.csv,", N, "windows")
