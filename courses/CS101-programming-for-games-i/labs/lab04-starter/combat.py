"""CS101 Lab 04 starter: refactor a tangled combat turn into small functions.

Run the game:   python combat.py
Run the tests:  python test_lab04.py

Part A is the original tangled loop. Read it, play it, but do not edit it.
Part B is where you write your functions. Each one currently raises
NotImplementedError, so every test fails until you fill it in.
Part C is play(), which you rewrite to call your Part B functions.
"""
import random

# ---------------------------------------------------------------------------
# Part A: the original tangled fight (read only). It contains one boundary bug.
# ---------------------------------------------------------------------------

def fight_tangled(seed=None):
    rng = random.Random(seed)
    hero_hp, hero_max, hero_atk, hero_bonus, hero_armor, hero_def = 30, 30, 9, 4, 2, 12
    rat_hp, rat_atk, rat_bonus, rat_armor, rat_def = 16, 6, 2, 1, 11
    potions = 2
    turn = 1
    while hero_hp > 0:
        print(f"-- Turn {turn}. You: {hero_hp}/{hero_max} HP. Rat: {rat_hp} HP.")
        choice = input("(a)ttack or (d)rink potion? ").strip().lower()
        if choice == "d":
            if potions > 0:
                potions = potions - 1
                hero_hp = hero_hp + 12
                if hero_hp > hero_max:
                    hero_hp = hero_max
                print(f"You drink a potion. {potions} left.")
            else:
                print("No potions left!")
        else:
            roll = rng.randint(1, 20)
            if roll == 20 or (roll != 1 and roll + hero_bonus >= rat_def):
                dmg = hero_atk - rat_armor
                if dmg < 1:
                    dmg = 1
                if roll == 20:
                    dmg = dmg * 2
                rat_hp = rat_hp - dmg
                print(f"You roll {roll} and hit for {dmg}.")
            else:
                print(f"You roll {roll} and miss.")
        if rat_hp < 0:                      # look closely at this line
            print("The rat is defeated!")
            return True
        roll = rng.randint(1, 20)
        if roll == 20 or (roll != 1 and roll + rat_bonus >= hero_def):
            dmg = rat_atk - hero_armor
            if dmg < 1:
                dmg = 1
            if roll == 20:
                dmg = dmg * 2
            hero_hp = hero_hp - dmg
            if hero_hp < 0:
                hero_hp = 0
            print(f"The rat rolls {roll} and bites for {dmg}.")
        else:
            print(f"The rat rolls {roll} and misses.")
        turn = turn + 1
    print("You are defeated.")
    return False


# ---------------------------------------------------------------------------
# Part B: your functions. Replace each `raise NotImplementedError` with code.
# Keep them pure: no print, no input, no random calls inside them.
# ---------------------------------------------------------------------------

def attack_hits(roll, bonus, defense):
    """True if a d20 roll hits. A natural 20 always hits, a natural 1 always
    misses, otherwise hit when roll + bonus >= defense."""
    raise NotImplementedError


def damage(attack, armor, crit=False):
    """attack - armor, but never below 1. Doubled (after the floor) on a crit."""
    raise NotImplementedError


def apply_damage(hp, amount):
    """Return the new HP after taking `amount`, never below 0."""
    raise NotImplementedError


def drink_potion(hp, max_hp, potions, heal_amount=12):
    """Return (new_hp, potions_left). Heals up to max_hp and uses one potion.
    With no potions, nothing changes."""
    raise NotImplementedError


def is_defeated(hp):
    """True when a combatant is out of the fight."""
    raise NotImplementedError


def resolve_attack(roll, attacker, defender):
    """Return the damage dealt by one attack roll (0 on a miss).
    attacker and defender are dicts with keys 'atk', 'bonus', 'armor', 'def'."""
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Part C: rewrite the fight using Part B. Only this function may print,
# ask for input or roll dice.
# ---------------------------------------------------------------------------

def play(seed=None):
    rng = random.Random(seed)
    hero = {"hp": 30, "max": 30, "atk": 9, "bonus": 4, "armor": 2, "def": 12}
    rat = {"hp": 16, "atk": 6, "bonus": 2, "armor": 1, "def": 11}
    potions = 2
    # TODO: the same fight as fight_tangled, built from your functions.
    return fight_tangled(seed)   # delete this line when your version works


if __name__ == "__main__":
    play()
