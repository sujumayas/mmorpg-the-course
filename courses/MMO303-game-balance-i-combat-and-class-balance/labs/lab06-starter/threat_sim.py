"""MMO303 Lab 06 starter: tick-based threat simulator. Standard library only.

Model (week 6 lecture, classic WoW rules):
  - damage adds damage x threat modifier to the enemy's table;
  - healing adds 0.5 x healing, split equally across all enemies in combat;
  - the enemy switches when a melee player exceeds 110% of the current
    target's threat, or a ranged player exceeds 130%.

Fill in the TODOs, then run `python3 test_threat.py` (or pytest).
"""
from dataclasses import dataclass, field

DT = 0.1           # seconds per tick
MELEE_K = 1.1
RANGED_K = 1.3


@dataclass
class Combatant:
    name: str
    dps: float = 0.0            # raw damage per second on this enemy
    threat_mod: float = 1.0     # 1.3 for a warrior in Defensive Stance
    ranged: bool = False
    hps: float = 0.0            # effective healing per second

    @property
    def k(self):
        return RANGED_K if self.ranged else MELEE_K


@dataclass
class ThreatTable:
    """One enemy's threat table. `threat` maps a combatant name to its threat."""
    threat: dict = field(default_factory=dict)
    target: str = None

    def add(self, name, amount):
        """TODO: add threat for one combatant."""
        raise NotImplementedError("ThreatTable.add is yours to write")

    def check_switch(self, combatants, t):
        """TODO: switch target if any non-target exceeds k x the target's
        threat (k from that combatant). Return the new target's name if the
        target changed at time t, else None."""
        raise NotImplementedError("ThreatTable.check_switch is yours to write")


def pull_time_closed_form(tau_t, tau_d, head_start, k):
    """TODO: the lecture's closed form. Return k L / (tau_d - k tau_t),
    or None if the DPS never pulls (tau_d <= k tau_t)."""
    raise NotImplementedError("pull_time_closed_form is yours to write")


def simulate(tank, others, head_start, duration=60.0, taunt_on_pull=False,
             taunt_cooldown=10.0, n_enemies=1):
    """TODO: run one enemy for `duration` seconds in ticks of DT.

    The tank starts with `head_start` threat and is the target at t = 0.
    Each tick, every combatant adds its threat (damage x modifier, plus
    0.5 x healing / n_enemies). Then check for a switch.
    If `taunt_on_pull` and the taunt is off cooldown, a switch away from the
    tank is followed at once by a taunt: the tank's threat becomes equal to
    the highest threat on the table and the tank is the target again.

    Return a list of (time, new_target_name) for every switch away from
    the tank, in time order.
    """
    raise NotImplementedError("simulate is yours to write")
