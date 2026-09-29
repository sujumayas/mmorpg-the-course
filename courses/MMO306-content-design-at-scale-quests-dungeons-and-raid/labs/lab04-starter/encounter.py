"""MMO306 Lab 04: the enrage line.

Finish every function marked TODO. Run `python test_encounter.py` until every test passes.
Standard-library Python only. Times are in seconds, damage in hit points.

A mechanic is a tuple (first, every, cost):
    first  the time of its first cast
    every  its cycle c (seconds between casts)
    cost   the seconds of attacking it costs a damage dealer who resolves it cleanly (d)
A group is described by its paper DPS P and its execution factor x (1.0 = clean).
"""
from dataclasses import dataclass, field


@dataclass
class Boss:
    name: str
    H: float                                      # health
    T: float                                      # enrage time, seconds
    mechanics: list = field(default_factory=list)  # list of (first, every, cost)


@dataclass
class Group:
    name: str
    P: float        # paper DPS
    x: float = 1.0  # execution factor
    dps_players: int = 14


QUAKEMAW = Boss("Quakemaw", 5_000_000, 300, [(10, 20, 2), (15, 30, 3)])
STITCHGUT = Boss("Stitchgut", 6_900_000, 300, [])
GROUP_A = Group("A", 24_000, 1.6)
GROUP_B = Group("B", 22_000, 1.0)


def tax(boss):
    """Mechanic tax: sum of cost / every over the boss's mechanics."""
    raise NotImplementedError("tax")


def uptime(boss, group):
    """Average-model uptime u = 1 - x * tax, never below 0."""
    raise NotImplementedError("uptime")


def kill_time(boss, group):
    """Average-model kill time H / (P * u). Return None if u is 0."""
    raise NotImplementedError("kill_time")


def passes(boss, group):
    """True if the average-model kill time is at or before the enrage."""
    raise NotImplementedError("passes")


def hidden_health(boss, group):
    """The tank-and-spank health equivalent H / u for this group."""
    raise NotImplementedError("hidden_health")


def required_paper_dps(boss, group):
    """Paper DPS this group needs to kill exactly at the enrage: H / (u * T)."""
    raise NotImplementedError("required_paper_dps")


def simulate(boss, group, deaths=(), limit_s=None):
    """Tick simulation in tenths of a second (lecture section 3).

    deaths is a list of (time_s, count): count damage dealers die at time_s.
    Each dead damage dealer removes 1 / group.dps_players of P from that tick on.
    A mechanic window lasts x * cost seconds. Use integer ticks.
    Return the kill time in seconds (tick + 1) / 10, or None if the boss is not dead
    by limit_s (default: the enrage time T).
    """
    raise NotImplementedError("simulate")


def max_deaths(boss, group, when_s):
    """Largest number of damage dealers that can die at when_s and the group still
    kills the boss by the enrage, using simulate(). Return -1 if it fails with 0 deaths."""
    raise NotImplementedError("max_deaths")


if __name__ == "__main__":
    for b in (STITCHGUT, QUAKEMAW):
        for g in (GROUP_A, GROUP_B):
            print(b.name, g.name, round(uptime(b, g), 3), kill_time(b, g), simulate(b, g))
