"""MA102 lab 09 starter: loot table from targets.

Run it as a script (python lab09_starter.py) or paste the sections into a
notebook. The design brief is below as BRIEF and in lab09_brief.csv. The
empty two-tier table is below as TABLE. lab09_table_template.csv has the
columns of the spreadsheet "Table" sheet.

What is done for you:
    pick(table, rng)      one pick using the cumulative walk from the lecture

What you write:
    the weights in TABLE (steps 1 and 2) and GOLD_PER_DROP (step 3)
    simulate_kills(table, kills, rolls, rng)   (step 4)
"""
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(102)

ROLLS_PER_KILL = 2
TOKENS_PER_KILL = 3  # always drops, not part of the weighted table

# The brief. Targets are per player, one kill per week.
BRIEF = [
    {"reward": "Raid tokens", "job": "Income",
     "target": "Always drops 3 per kill (not part of the weighted table)"},
    {"reward": "Gold", "job": "Income",
     "target": "Expected 120 gold per kill from the table"},
    {"reward": "Tier armour piece", "job": "Progression",
     "target": "95% of players have at least one within 12 kills"},
    {"reward": "Raid weapon", "job": "Progression",
     "target": "95% of players have it within 30 kills"},
    {"reward": "Mount", "job": "Trophy",
     "target": "Median player gets it around kill 150 (within ±10)"},
]

# Two tiers. An entry is (name, weight) or (name, weight, sub_table).
# Replace each None with an integer weight. Top-table total at least 1,000.
GEAR_TABLE = [
    ("Tier armour piece", None),
    ("Raid weapon", None),
]
TROPHY_TABLE = [
    ("Mount", 1),  # the only trophy, so its in-tier share is 1
]
TABLE = [
    ("Nothing", None),
    ("Gold", None),
    ("Gear tier", None, GEAR_TABLE),
    ("Trophy tier", None, TROPHY_TABLE),
]
GOLD_PER_DROP = None  # step 3

# The lecture's one-tier boss table, for trying pick() before TABLE is filled.
LECTURE_TABLE = [
    ("Nothing", 600),
    ("Gold", 250),
    ("Potion", 100),
    ("Sword", 40),
    ("Ring", 10),
]


def pick(table, rng):
    """Pick one entry by the cumulative walk and return its name.

    roll = random integer in [0, W - 1]
    for each entry: if roll < weight, return it; else roll -= weight.
    If the chosen entry has a sub-table, pick again inside it.
    """
    total = sum(entry[1] for entry in table)
    roll = int(rng.integers(0, total))
    for entry in table:
        name, weight = entry[0], entry[1]
        if roll < weight:
            if len(entry) == 3:
                return pick(entry[2], rng)
            return name
        roll -= weight
    raise ValueError("roll fell off the end of the table")


def simulate_kills(table, kills, rolls, rng):
    """Simulate one player for `kills` kills, rolling `table` `rolls` times each.

    Return a dict mapping each item name to the kill number (1-based) of
    its first drop, or None if it never dropped. Also include the key
    "gold" with the total gold earned. Use pick() and `rng` for every draw.
    Call it 10,000 times to get percentiles for step 4.
    """
    raise NotImplementedError("Write simulate_kills (step 4).")


if __name__ == "__main__":
    counts = {}
    for _ in range(100_000):
        name = pick(LECTURE_TABLE, rng)
        counts[name] = counts.get(name, 0) + 1
    print("pick() on the lecture table, 100,000 picks (expect weight / 1000):")
    for name, weight in LECTURE_TABLE:
        print(f"  {name:<8} {counts.get(name, 0) / 100_000:.4f}  exact {weight / 1000:.4f}")

    if any(entry[1] is None for entry in TABLE + GEAR_TABLE):
        print("TODO: fill the weights in TABLE and GEAR_TABLE (steps 1 and 2).")
    else:
        try:
            result = simulate_kills(TABLE, 200, ROLLS_PER_KILL, rng)
            print(result)
        except NotImplementedError as e:
            print(f"TODO: {e}")
