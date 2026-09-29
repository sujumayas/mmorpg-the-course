"""CS203 Lab 11 starter: a stage manager for melee attackers, and formation slots.

Run:   python stage.py           prints a fight table for three difficulty settings
Check: python check_lab11.py     exits 0 only when your work is complete

You edit the six places marked TODO. run_rounds() and fight() are provided and
use your methods, so they start working as soon as yours do.
"""
from collections import deque
from itertools import permutations
from math import dist

# creature type -> (grid weight, attacks strongest first as (name, attack weight, damage))
CREATURES = {
    "soldier": (4, [("lunge", 5, 14), ("swing", 3, 8)]),
    "troll": (8, [("charge", 6, 30), ("club", 4, 18)]),
}


class StageManager:
    """Grants grid slots and attacks around one player (Dawe, Game AI Pro ch. 28)."""

    def __init__(self, grid_capacity, attack_capacity):
        self.grid_capacity = grid_capacity
        self.attack_capacity = attack_capacity
        self.grid_used = 0
        self.attack_used = 0
        self.on_grid = {}        # enemy name -> grid weight
        self.attacking = {}      # enemy name -> attack weight in progress

    def request_slot(self, name, weight):
        """Admit if weight fits in the free grid capacity. Return True or False.

        An enemy already on the grid is not admitted twice (return True, no change).
        """
        raise NotImplementedError("request_slot")  # TODO

    def choose_attack(self, name, attacks):
        """attacks: list of (attack name, attack weight, damage), strongest first.

        Only an enemy on the grid and not already attacking may attack. Take the
        first attack whose weight fits in the free attack capacity, record it in
        self.attacking and return the (name, weight, damage) tuple, else None.
        """
        raise NotImplementedError("choose_attack")  # TODO

    def release(self, name):
        """The enemy's attack (if any) ends and it gives its slot back.

        Free both its attack weight and its grid weight. Unknown names do nothing.
        """
        raise NotImplementedError("release")  # TODO


def run_rounds(pack, grid_capacity, attack_capacity, rounds):
    """pack: list of (enemy name, creature type), in request order.

    Each round: admit from the front of the waiting queue while enemies fit
    (an enemy that does not fit stays at the front and admission stops),
    then every enemy on the grid, in admission order, chooses an attack,
    then every enemy that attacked releases and goes to the back of the queue.
    Returns (damage per round list, attacks per enemy dict).
    """
    stage = StageManager(grid_capacity, attack_capacity)
    queue = deque(pack)
    kinds = dict(pack)
    per_round, count = [], {name: 0 for name, _ in pack}
    for _ in range(rounds):
        while queue and stage.request_slot(queue[0][0], CREATURES[queue[0][1]][0]):
            queue.popleft()
        damage, attackers = 0, []
        for name in list(stage.on_grid):
            chosen = stage.choose_attack(name, CREATURES[kinds[name]][1])
            if chosen:
                damage += chosen[2]
                count[name] += 1
                attackers.append(name)
        for name in attackers:
            stage.release(name)
            queue.append((name, kinds[name]))
        per_round.append(damage)
    return per_round, count


def damage_taken(pack_size, max_attackers, dps=10, kill_time=5):
    """Lecture section 2: total damage while the player kills one enemy per kill_time.

    max_attackers None means no cap.
    """
    raise NotImplementedError("damage_taken")  # TODO


def assign_greedy(units, slots):
    """Each unit, in list order, takes its nearest free slot. Return a tuple of slot indices."""
    raise NotImplementedError("assign_greedy")  # TODO


def assign_best(units, slots):
    """Assignment with the smallest total straight-line distance (try every order).

    Break ties by taking the first order that permutations() yields.
    """
    raise NotImplementedError("assign_best")  # TODO


def total_distance(units, slots, order):
    return sum(dist(units[i], slots[s]) for i, s in enumerate(order))


def fight(pack, grid_capacity, attack_capacity, health=600, rounds=40):
    """Rounds until the player's health is used up, or None if they last all rounds."""
    per_round, _ = run_rounds(pack, grid_capacity, attack_capacity, rounds)
    total = 0
    for i, dmg in enumerate(per_round, start=1):
        total += dmg
        if total >= health:
            return i
    return None


PACK = [("T1", "troll")] + [(f"S{i}", "soldier") for i in range(1, 7)]

if __name__ == "__main__":
    print(f"{'setting':<8} {'C_g':>4} {'C_a':>4} {'rounds to 600 damage':>22}")
    for label, cg, ca in (("easy", 8, 6), ("normal", 12, 10), ("hard", 16, 14)):
        try:
            r = fight(PACK, cg, ca)
            print(f"{label:<8} {cg:>4} {ca:>4} {'never' if r is None else r:>22}")
        except NotImplementedError as exc:
            print(f"{label:<8} {cg:>4} {ca:>4} {'-':>22}   ({exc} not written yet)")
            break
