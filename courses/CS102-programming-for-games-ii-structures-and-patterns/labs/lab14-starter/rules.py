"""CS102 Lab 14: six gameplay rules. Each one has exactly one planted bug.

Do not fix anything until a test of yours fails because of it (regression discipline).
Every rule is a pure function: randomness comes in through an `rng` argument.
"""


def damage_after_armor(raw, armor):
    """Subtractive armor. Every hit that lands deals at least 1 damage."""
    if raw > armor:
        return raw - armor
    if raw == armor:
        return 0
    return 1


def is_crit(rng, chance):
    """True if this hit is a critical hit. chance is from 0.0 (never) to 1.0 (always)."""
    return rng.random() <= chance


def rage_bonus(stacks):
    """Damage multiplier from Rage stacks: +5% per stack, up to 10 stacks (+50%).
    Stacks above 10 are allowed on the character but give no extra bonus."""
    return 1 + (stacks % 11) * 0.05


XP_TABLE = [round(100 * level ** 1.5) for level in range(1, 60)]   # levels 1..59
MAX_LEVEL = 60


def xp_to_next(level):
    """XP needed to go from `level` to `level + 1`. Returns None at MAX_LEVEL."""
    if level >= MAX_LEVEL:
        return None
    return XP_TABLE[level]


def split_gold(total, players):
    """Split `total` gold between `players` people. The party leader (index 0)
    gets any remainder. No gold is created or destroyed."""
    share = total // players
    return [share] * players


def regen(hp, max_hp, rate, dt):
    """Health after regenerating at `rate` HP per second for `dt` seconds.
    Never exceeds max_hp. Dead characters (hp <= 0) do not regenerate."""
    if hp <= 0:
        return hp
    if hp < max_hp:
        return hp + rate * dt
    return max_hp
