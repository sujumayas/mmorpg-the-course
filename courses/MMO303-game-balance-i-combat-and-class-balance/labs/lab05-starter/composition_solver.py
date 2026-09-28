"""MMO303 Lab 05 starter: composition solver. Standard library only.

Fill in the three TODO functions, then run the tests:

    python3 test_solver.py        (or: pytest test_solver.py)

Units follow the week 5 lecture: p is damage per second, q is healing per
second, m is mitigation as a fraction, HP is health.
"""
import csv
import os
from dataclasses import dataclass

HERE = os.path.dirname(os.path.abspath(__file__))


@dataclass
class Role:
    name: str
    p: float   # damage per second
    q: float   # healing per second
    m: float   # mitigation, 0.60 means 60%
    hp: float  # health


@dataclass
class Encounter:
    H: float   # boss health
    T: float   # enrage time in seconds
    B: float   # boss sustained raw damage per second on its target
    R: float   # raid damage per second after mitigation, spread across the group
    S: float   # largest single raw hit the target must survive


DEFAULT = Encounter(H=600_000, T=180, B=1_000, R=200, S=5_000)


def load_roles(path=os.path.join(HERE, "roles.csv")):
    """Return {"tank": Role, "healer": Role, "dps": Role} from roles.csv."""
    roles = {}
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            roles[row["role"]] = Role(row["role"], float(row["p"]), float(row["q"]),
                                      float(row["m"]), float(row["HP"]))
    return roles


def compositions(n):
    """TODO step 1. Return every (t, h, d) with t + h + d = n, as a list of tuples."""
    raise NotImplementedError("compositions() is yours to write")


def target(group, roles):
    """TODO step 2. Return the Role the boss attacks for group = (t, h, d).
    A tank if there is one; otherwise the non-tank with the highest HP,
    ties broken by the higher mitigation."""
    raise NotImplementedError("target() is yours to write")


def check(group, encounter, roles):
    """TODO step 3. Return a dict with the margin of each check (value minus
    requirement) and whether the group passes all three:

        {"damage": float, "healing": float, "spike": float, "passes": bool}

    Damage passes when its margin is >= 0, healing when its margin is >= 0.
    The spike check is strict: it passes only when HP > S x (1 - m), so a
    margin of exactly 0 fails.
    """
    raise NotImplementedError("check() is yours to write")


def passing(encounter, roles, n=5):
    """Every composition of size n that passes all three checks."""
    return [g for g in compositions(n) if check(g, encounter, roles)["passes"]]


if __name__ == "__main__":
    roles = load_roles()
    for g in compositions(5):
        r = check(g, DEFAULT, roles)
        print(g, {k: (round(v, 1) if not isinstance(v, bool) else v) for k, v in r.items()})
