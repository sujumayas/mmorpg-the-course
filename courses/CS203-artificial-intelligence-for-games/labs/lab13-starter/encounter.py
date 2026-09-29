"""CS203 Lab 13 starter: boss encounters as data, under three phase rules.

A boss is a dictionary (see WARDEN below). Each phase covers some of the boss's
health ("hp"), has a fixed length for time-gated fights ("seconds", None for the
last phase), and a list of abilities. An ability fires at first, first + period,
first + 2 * period, ... seconds after its phase starts.

Three phase rules (the "mode" argument):
    "hp"     a phase ends when the group has dealt its hp in damage.
    "time"   a phase starts at a fixed time; the fight ends at the kill.
    "guard"  like "hp", but a phase holding a signature ability cannot end before
             that ability's first cast has resolved (start + first + resolve).
             Damage dealt while the boss is held at the threshold is wasted.

All times are fractions.Fraction so that thresholds land exactly. The group deals
a constant `dps`. The fight ends at the kill or at the enrage, whichever is first.

Run:   python encounter.py         prints the lecture's comparison table
Check: python test_encounter.py    exits 0 only when your work is complete

You write the four functions marked TODO. Leave the data and helpers alone.
"""
from fractions import Fraction

WARDEN = {
    "name": "The Warden",
    "hp": 600_000,
    "enrage": 360,
    "phases": [
        {"name": "P1", "hp": 240_000, "seconds": 120,
         "abilities": [{"name": "Summon adds", "first": 20, "period": 45}]},
        {"name": "P2", "hp": 180_000, "seconds": 90,
         "abilities": [{"name": "Meteor", "first": 40, "period": 40,
                        "signature": True, "resolve": 5}]},
        {"name": "P3", "hp": 180_000, "seconds": None,
         "abilities": [{"name": "Firestorm", "first": 15, "period": 25}]},
    ],
}

# A second boss so your code cannot hard-wire the Warden.
FOUNDRY = {
    "name": "The Foundry Twins",
    "hp": 400_000,
    "enrage": 300,
    "phases": [
        {"name": "Split", "hp": 200_000, "seconds": 100,
         "abilities": [{"name": "Hammer", "first": 10, "period": 12},
                       {"name": "Bellows", "first": 30, "period": 30,
                        "signature": True, "resolve": 6}]},
        {"name": "Merged", "hp": 200_000, "seconds": None,
         "abilities": [{"name": "Slag wave", "first": 8, "period": 20},
                       {"name": "Crucible", "first": 50, "period": 60,
                        "signature": True, "resolve": 10}]},
    ],
}


def kill_time(enc, dps):
    """Seconds to deal the boss's full health at a constant dps (hp and time modes)."""
    return Fraction(enc["hp"], dps)


# ---------------------------------------------------------------- TODO 1
def phase_windows(enc, dps, mode):
    """Return a list of (start, end) Fractions, one per phase, ignoring the enrage.

    hp:    phase i lasts phase_hp / dps and starts where phase i-1 ended.
    time:  phase i starts at the sum of earlier "seconds"; it ends at start + seconds,
           or at None for a phase whose "seconds" is None (it runs until the kill).
    guard: like hp, but if the phase has a signature ability, its end is at least
           start + first + resolve of that ability.
    """
    raise NotImplementedError("phase_windows")


# ---------------------------------------------------------------- TODO 2
def cast_times(start, end, first, period, stop):
    """Absolute times start + first + k * period (k = 0, 1, ...) that are strictly
    before `end` (skip this test if end is None) and strictly before `stop`."""
    raise NotImplementedError("cast_times")


# ---------------------------------------------------------------- TODO 3
def run(enc, dps, mode):
    """Simulate one fight. Return a dict with
        "events":  list of (time, phase_name, ability_name) sorted by time, then phase
                   order, then ability order in the data,
        "end":     time the fight ends (the kill, or the enrage if it comes first),
        "outcome": "kill" or "enrage".
    The kill is at kill_time() in hp and time modes, and at the end of the last
    phase window in guard mode. A kill exactly at the enrage counts as a kill.
    """
    raise NotImplementedError("run")


# ---------------------------------------------------------------- TODO 4
def skip_threshold(enc, phase_name, ability_name):
    """Smallest dps (a Fraction) at which the ability's first cast never happens
    under HP gates: phase_hp / first."""
    raise NotImplementedError("skip_threshold")


# ---------------------------------------------------------------- helpers
def counts(enc, result):
    """Number of casts per ability, in data order."""
    names = [a["name"] for p in enc["phases"] for a in p["abilities"]]
    return [sum(1 for _, _, n in result["events"] if n == name) for name in names]


def table(enc=WARDEN, dps_values=(2_000, 3_200, 4_400, 4_600, 6_000)):
    print(f"{enc['name']}: minimum DPS to beat the enrage {enc['hp'] / enc['enrage']:,.1f}")
    print(f"{'DPS':>6} {'hp':>14} {'time':>14} {'guard':>14} {'guard end':>10}")
    for dps in dps_values:
        cells = []
        for mode in ("hp", "time", "guard"):
            try:
                cells.append(str(counts(enc, run(enc, dps, mode))))
            except NotImplementedError:
                cells.append("-")
        try:
            end = f"{float(run(enc, dps, 'guard')['end']):.1f}"
        except NotImplementedError:
            end = "-"
        print(f"{dps:>6,} {cells[0]:>14} {cells[1]:>14} {cells[2]:>14} {end:>10}")


if __name__ == "__main__":
    table()
    print()
    table(FOUNDRY, (1_500, 2_500, 4_000, 7_000))
