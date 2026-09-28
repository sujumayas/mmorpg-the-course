"""The old way. Part A step 3 and Part B step 6: move these numbers into the data files,
then delete this file's classes and make combat.py read them from the tables."""
import random


class Crossbow:
    name = "Crossbow"
    weapon_type = "bow"
    min_dmg, max_dmg = 6, 14
    attacks_per_sec = 0.7
    req_str = 40


class Skeleton:
    name = "Skeleton"
    hp = 40
    armor = 4
    weapon = Crossbow
    loot = [("gold", 70), ("nothing", 30)]


def swing(weapon, rng):
    return rng.randint(weapon.min_dmg, weapon.max_dmg)


if __name__ == "__main__":
    rng = random.Random(13)
    print([swing(Skeleton.weapon, rng) for _ in range(5)])
