"""MMO306 Lab 02 starter: a zone's XP budget and hub coverage. Standard library only.

Fill in the TODO functions, then run the tests from this folder:

    ../../../../.venv/bin/python test_zone.py

Notation follows the week 2 lecture.
    X      XP demand of the zone (sum of XP to next level over its range)
    q      XP one quest pays at the zone's level
    k      kill XP earned during one quest, as a share of q
    o      share of X that comes from outside the zone's quests
    n      quests the player completes before outlevelling the zone
    hubs   list of hub sizes (quest counts), done in order
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load_xp_table(path=os.path.join(HERE, "xp_table.csv")):
    """{level: xp_to_next} from xp_table.csv."""
    with open(path, newline="") as f:
        return {int(r["level"]): int(r["xp_to_next"]) for r in csv.DictReader(f)}


def zone_demand(table, lo, hi):
    """TODO step 1. XP to go from level lo to level hi: sum of table[L] for lo <= L < hi.
    Raise KeyError if a level in the range is missing from the table."""
    raise NotImplementedError("zone_demand() is yours to write")


def quests_needed(X, q, k, o):
    """TODO step 1. n = X x (1 - o) / (q x (1 + k))."""
    raise NotImplementedError("quests_needed() is yours to write")


def hub_seen(n, hubs):
    """TODO step 2. Share (0 to 1) of each hub the player completes when they do
    n quests in hub order. Returns a list with one share per hub."""
    raise NotImplementedError("hub_seen() is yours to write")


def hub_seen_skipping(n, hubs, s):
    """TODO step 3. The player does a share s of the quests they meet, so they walk
    past n / s quests to complete n. Return two lists, (walked, played):
    walked[i] is the share of hub i the player walks through (hub_seen of n / s),
    played[i] is the share they actually complete (walked[i] x s)."""
    raise NotImplementedError("hub_seen_skipping() is yours to write")


def level_minutes(table, lo, hi, q, k, t_q):
    """TODO step 4. Minutes spent on each level from lo to hi - 1, as a dict
    {level: minutes}, when the player earns q x (1 + k) XP every t_q minutes."""
    raise NotImplementedError("level_minutes() is yours to write")


if __name__ == "__main__":
    table = load_xp_table()
    X = zone_demand(table, 10, 15)
    hubs = [10, 10, 10]
    for label, k, o in (("solo", 0.25, 0), ("rested", 0.5, 0),
                        ("some dungeons", 0.25, 0.2), ("dungeon heavy", 0.25, 0.5)):
        n = quests_needed(X, 400, k, o)
        print(f"{label:14s} n={n:5.1f} c={sum(hubs) / n:.2f} "
              f"hubs={[round(s, 2) for s in hub_seen(n, hubs)]}")
    print(level_minutes(table, 10, 15, 400, 0.25, 6))
