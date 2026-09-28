"""A tiny fight that reads everything from the data tables. Run after Parts A and B."""
import random
import sys
from loader import load_weapons, load_monsters, dps


def time_to_kill(attacker_weapon, defender_hp, defender_armor, rng, max_seconds=600):
    """Seconds until defender_hp reaches 0. Subtractive armor, floor 1 (GD203 week 2)."""
    hp, t, step = defender_hp, 0.0, 1 / attacker_weapon.attacks_per_sec
    while hp > 0 and t < max_seconds:
        t += step
        hp -= max(1, rng.randint(attacker_weapon.min_dmg, attacker_weapon.max_dmg) - defender_armor)
    return round(t, 2)


if __name__ == "__main__":
    weapons = load_weapons("weapons.csv")
    monsters = load_monsters("monsters.json", weapons)
    player_weapon = weapons[sys.argv[1] if len(sys.argv) > 1 else "long_sword"]
    print(f"Player uses {player_weapon.name} (dps {dps(player_weapon):.2f})")
    for mid, m in monsters.items():
        ttk = time_to_kill(player_weapon, m["hp"], m["armor"], random.Random(13))
        print(f"  {m['name']:14} hp {m['hp']:4}  armor {m['armor']:2}  killed in {ttk:6.2f} s")
