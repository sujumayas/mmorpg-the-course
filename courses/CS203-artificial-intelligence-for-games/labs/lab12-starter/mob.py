"""CS203 Lab 12 starter: an MMO mob with aggro radius, a threat table and a leash.

Run:   python mob.py             prints the raid-tier table
Check: python check_lab12.py     exits 0 only when your work is complete

You edit the places marked TODO. flicker(), the raid tiers and the table
printer are provided and use your code. Threat is stored as whole numbers and
thresholds as tenths, so every comparison is exact.
"""
from math import dist

MELEE_K, RANGED_K = 11, 13      # 110% and 130%, in tenths


def aggro_radius(mob_level, player_level):
    """Yards: 20 at equal level, +1 per level the mob is above the player
    (-1 per level below), never below 5, never above 45."""
    raise NotImplementedError("aggro_radius")  # TODO


class ThreatTable:
    def __init__(self, thresholds=True):
        self.threat = {}            # unit -> int threat
        self.target = None
        self.thresholds = thresholds
        self.forced_until = -1      # while now < forced_until, the target is locked

    def add_damage(self, who, damage, multiplier=1.0):
        """Damage adds damage x multiplier threat (rounded to a whole number)."""
        raise NotImplementedError("add_damage")  # TODO

    def add_heal(self, who, healing, mobs_in_combat=1):
        """Healing adds 0.5 x healing / mobs_in_combat threat (rounded) to THIS table.
        The caller adds the same amount to every mob in combat."""
        raise NotImplementedError("add_heal")  # TODO

    def taunt(self, who, now, duration=3):
        """Set who's threat equal to the current maximum, make who the target,
        and lock the target until now + duration."""
        raise NotImplementedError("taunt")  # TODO

    def remove(self, who):
        """who dies or leaves combat: drop the entry. If it was the target,
        the target becomes None so choose() picks the highest remaining."""
        raise NotImplementedError("remove")  # TODO

    def choose(self, in_melee, now=0):
        """Return the target.

        - Empty table: None.
        - No target: the highest threat (no threshold).
        - Locked by a taunt (now < forced_until): keep the target.
        - Otherwise a challenger replaces the target if
          10 x its threat > k x target threat, k = 11 in melee, 13 at range,
          or k = 10 when thresholds are off. Several challengers: highest wins.
        """
        raise NotImplementedError("choose")  # TODO


def healer_pull(multiplier, boss_dps, tank_dps, mobs=1, seconds=600):
    """Lecture section 2 with your table: the tank hits from second 1, the healer
    heals boss_dps per second from second 2 (split over mobs). Return the first
    second the boss targets the healer, or None."""
    raise NotImplementedError("healer_pull")  # TODO


def min_safe_multiplier(boss_dps, tank_dps, mobs=1, step=0.01, seconds=600):
    """Smallest multiplier on the grid 1.00, 1.01, 1.02, ... (up to 10) for which
    healer_pull returns None. Build each candidate as round(1 + i * step, 2)."""
    raise NotImplementedError("min_safe_multiplier")  # TODO


class Mob:
    """IDLE -> COMBAT -> EVADE -> IDLE."""

    def __init__(self, level, spawn, leash=40.0, max_hp=1000):
        self.level, self.spawn, self.pos = level, spawn, spawn
        self.leash, self.max_hp, self.hp = leash, max_hp, max_hp
        self.state = "IDLE"
        self.table = ThreatTable()

    def take_damage(self, who, amount):
        """Provided. Evading mobs ignore damage; idle mobs enter combat."""
        if self.state == "EVADE":
            return
        self.hp -= amount
        self.table.add_damage(who, amount)
        self.state = "COMBAT"

    def update(self, players):
        """players: dict name -> (position, level). One tick.

        IDLE:   if any player is within aggro_radius(self.level, their level)
                of self.pos, add each such player with 0 threat (add_damage(name, 0))
                and go to COMBAT.
        COMBAT: if dist(self.pos, self.spawn) > self.leash, go to EVADE:
                clear the table (a new ThreatTable), restore hp to max_hp.
        EVADE:  move straight home (set pos = spawn) and go to IDLE.
        Return the new state.
        """
        raise NotImplementedError("Mob.update")  # TODO


def flicker(thresholds, seconds=60):
    """Provided: lecture section 3. Tank and rogue both average 300 threat/s."""
    table, switches = ThreatTable(thresholds), 0
    table.add_damage("tank", 100)
    table.add_damage("rogue", 0)
    table.choose({"tank", "rogue"})
    for t in range(1, seconds + 1):
        table.add_damage("tank", 150 if t % 2 else 450)
        table.add_damage("rogue", 400 if t % 2 else 200)
        before = table.target
        if table.choose({"tank", "rogue"}, now=t) != before:
            switches += 1
    return switches


# Three raid tiers: (name, boss damage per second on the tank, tank damage per second)
TIERS = [("tier 1", 500, 180), ("tier 2", 800, 210), ("tier 3", 1300, 240)]

if __name__ == "__main__":
    print(f"{'tier':<8} {'B':>5} {'d':>4} {'m* formula':>11} {'m* simulated':>13}")
    for name, b, d in TIERS:
        formula = b / (2.6 * d)
        try:
            sim = min_safe_multiplier(b, d)
            print(f"{name:<8} {b:>5} {d:>4} {formula:>11.3f} {sim:>13.2f}")
        except NotImplementedError as exc:
            print(f"{name:<8} {b:>5} {d:>4} {formula:>11.3f} {'-':>13}   ({exc} not written yet)")
            break
