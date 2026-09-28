"""MA101 Lab 14 starter: range queries.

Python 3, standard library only. Data files: mobs.csv, players.csv, chase.csv.
Helper: int32_sim.py. Fill in every TODO.
"""
import csv


def load_mobs(path="mobs.csv"):
    """List of (id, (x, y, z)) with integer block coordinates."""
    return [(int(r["id"]), (int(r["x"]), int(r["y"]), int(r["z"]))) for r in csv.DictReader(open(path))]


def load_players(path="players.csv"):
    """List of (x, y, z) integer tuples."""
    return [(int(r["x"]), int(r["y"]), int(r["z"])) for r in csv.DictReader(open(path))]


def load_chase(path="chase.csv"):
    """List of (t, x, z) samples 0.1 s apart. The mob stands at the origin."""
    return [(float(r["t"]), float(r["x"]), float(r["z"])) for r in csv.DictReader(open(path))]


def sq_dist(a, b):
    """dx^2 + dy^2 + dz^2 for two (x, y, z) tuples. No square root."""
    raise NotImplementedError("TODO")


def despawn_zone(mob, players, r_near, r_far):
    """"safe", "random" or "despawn", using the nearest player and squared distances only."""
    raise NotImplementedError("TODO")


def metric(dx, dz, name):
    """name is "euclidean", "manhattan", "chebyshev" or "alternating" (D&D 3.5 diagonals)."""
    raise NotImplementedError("TODO")


class MobBrain:
    """States IDLE, CHASE, RETURN. The mob stands at the origin."""

    def __init__(self, r_aggro=10.0, r_leash=30.0, return_time=3.0):
        self.state = "IDLE"
        self.r_aggro = r_aggro
        self.r_leash = r_leash
        self.return_time = return_time
        self.timer = 0.0

    def update(self, player_pos, dt=0.1):
        """player_pos is (x, z). Apply one step of the rules in the lab brief.
        Return the new state."""
        raise NotImplementedError("TODO")


if __name__ == "__main__":
    print("sq_dist check:", sq_dist((0, 64, 0), (91, 64, 91)), "(want 16562)")
