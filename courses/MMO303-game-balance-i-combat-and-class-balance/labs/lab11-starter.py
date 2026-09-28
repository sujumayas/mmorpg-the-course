"""MMO303 Lab 11 starter: a discrete group-combat simulator.

Run it as-is to see the checks fail politely. Fill in `simulate` (Part A),
then the area-fire rule (Part B) and healing (Part C). Standard library only.

    python3 lab11-starter.py
"""
import csv
from dataclasses import dataclass

DT = 0.01        # seconds per step (lecture rule)
MAX_TIME = 300.0 # fight ends here if nobody has won


@dataclass
class Unit:
    hp: float = 1000.0      # maximum health
    dps: float = 100.0      # damage per second (0 for a pure healer)
    hps: float = 0.0        # healing per second (heals the lowest-health living ally)
    role: str = "dps"       # "dps" or "healer"
    cur: float = None       # current health, set in __post_init__

    def __post_init__(self):
        if self.cur is None:
            self.cur = self.hp

    @property
    def alive(self):
        return self.cur > 1e-7


def make_side(n_dps, n_healers=0, hp=1000.0, dps=100.0, hps=0.0):
    """List order is target order: damage dealers first, healers at the back."""
    side = [Unit(hp=hp, dps=dps) for _ in range(n_dps)]
    side += [Unit(hp=hp, dps=0.0, hps=hps, role="healer") for _ in range(n_healers)]
    return side


def simulate(side_a, side_b, rules):
    """Run one fight. Return a dict with keys:
        t          fight length in seconds
        a, b       survivors on each side
    `rules` is a dict, for example
        {"target_a": "focus", "target_b": "spread", "area_cap": None, "healers_first": False}

    TODO Part A. Each step:
      1. Sum each side's living damage dealers' DPS x DT.
      2. "focus": all of it on the first living enemy in list order.
         "spread": divide it equally among living enemies.
      3. Apply both sides' damage at once (deaths are simultaneous), overkill is lost.
      4. Stop when a side is empty or at MAX_TIME.
    TODO Part B: if rules["area_cap"] is a number k, each attacker applies
      10% of its DPS x DT in full to each of up to k living enemies.
    TODO Part C: after damage, each living healer heals the lowest-health
      living ally by hps x DT, not above max hp. If rules["healers_first"],
      side A targets side B's healers before its damage dealers.
    """
    raise NotImplementedError("simulate() is yours to write")


def write_csv(path, rows):
    """rows: list of dicts with the same keys. Opens in any spreadsheet."""
    if not rows:
        return
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


# Reference results from the week 11 lecture: 10 against 8, 1,000 HP, 100 DPS.
REFERENCE = [
    ("focus", "focus", "A", 6, 10.5),
    ("focus", "spread", "A", 10, 8.0),
    ("spread", "spread", "A", 10, 8.0),
    ("spread", "focus", "B", 8, 12.5),
]


def check_part_a():
    for ta, tb, winner, survivors, t_ref in REFERENCE:
        try:
            r = simulate(make_side(10), make_side(8), {"target_a": ta, "target_b": tb})
        except NotImplementedError as e:
            print(f"A {ta:6} vs B {tb:6}: not run yet ({e})")
            continue
        won = "A" if r["b"] == 0 else "B"
        left = r["a"] if won == "A" else r["b"]
        ok = won == winner and left == survivors and abs(r["t"] - t_ref) <= 0.2
        print(f"A {ta:6} vs B {tb:6}: {won} wins with {left} in {r['t']:.1f} s "
              f"(lecture: {winner}, {survivors}, {t_ref} s) {'OK' if ok else 'CHECK'}")


if __name__ == "__main__":
    check_part_a()
