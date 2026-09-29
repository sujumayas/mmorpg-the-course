"""MMO307 Lab 04 starter: the season ladder. Standard library only.

Fill in every function that raises NotImplementedError, then run the tests:

    python test_ladder.py        (or: pytest test_ladder.py)

Notation follows the week 4 lecture: E is a season's entry item level,
W its width (top minus entry), c the creep per season, g the power gained
per item level under an exponential budget.
"""
import csv
import math
import os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))


def load_tracks(path=os.path.join(HERE, "tracks.csv")):
    """Return {season: [(track, rank, ilvl), ...]} from tracks.csv."""
    seasons = defaultdict(list)
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            seasons[row["season"]].append((row["track"], int(row["rank"]), int(row["ilvl"])))
    return dict(seasons)


def ladder(rows, entry_track="Adventurer", top_track="Myth"):
    """Return (E, top): rank 1 of entry_track and the highest rank of top_track."""
    raise NotImplementedError("ladder() is yours to write")


def ranks_at(ilvl, rows):
    """Return every "Track rank" label at exactly this item level, sorted, e.g. ["Veteran 4"]."""
    raise NotImplementedError("ranks_at() is yours to write")


def landing(i, E_next, W):
    """Position x of an item at level i on a ladder that starts at E_next and is W wide."""
    raise NotImplementedError("landing() is yours to write")


def survival(i, E, c):
    """Number of later seasons an item at level i (from a season with entry E) stays at or
    above the entry, when every season moves up by c. Return math.inf when c == 0."""
    raise NotImplementedError("survival() is yours to write")


def gap_exp(d, g):
    """Power ratio of a d-item-level gap under an exponential budget (1 + g) per level."""
    raise NotImplementedError("gap_exp() is yours to write")


def gap_linear(i_high, i_low, a=0.6, b=15.5):
    """Power ratio between two item levels under a linear budget a*i + b."""
    raise NotImplementedError("gap_linear() is yours to write")


def creep_for_landing(x, W):
    """Creep c that makes the old top land at fraction x of the new ladder."""
    raise NotImplementedError("creep_for_landing() is yours to write")


def max_width(F, g):
    """Widest ladder whose top and entry still fit inside a sharing band F."""
    raise NotImplementedError("max_width() is yours to write")


if __name__ == "__main__":
    s = load_tracks()
    for name, rows in s.items():
        try:
            print(f"{name}: {len(rows)} track ranks, ladder {ladder(rows)}")
        except NotImplementedError:
            print(f"{name}: {len(rows)} track ranks (write ladder() to see entry and top)")
