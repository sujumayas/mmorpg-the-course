"""CS102 Lab 01 starter: gated stats.

Fill in every method marked TODO. Do not change method names or signatures;
the tests in test_stats.py call them exactly as written.

Run the tests from this folder with:
    python -m unittest -v
"""
from fractions import Fraction


class StatStages:
    """A stat stage that always stays in [MIN, MAX].

    Invariant: MIN <= stage <= MAX, after the constructor and after every method.
    """

    MIN, MAX = -6, 6

    def __init__(self, ability=None):
        # ability is None, "simple" (doubles every change) or "contrary" (reverses it).
        self._stage = 0
        self._ability = ability

    @property
    def stage(self):
        return self._stage

    @property
    def multiplier(self):
        """Gen III+ multiplier: max(2, 2 + n) / max(2, 2 - n), as a Fraction."""
        # TODO: return the exact multiplier for self._stage as a Fraction.
        raise NotImplementedError

    def change(self, delta):
        """Apply a requested change and return the change that actually happened.

        Order of rules: ability first (simple doubles, contrary reverses), then clamp.
        """
        # TODO: implement the ability modifier, the clamp and the return value.
        raise NotImplementedError

    def reset(self):
        """Return the stage to 0 (a switch-out clears stages)."""
        # TODO
        raise NotImplementedError


class Fighter:
    """A combatant with health and two stat stages.

    Invariant: 0 <= hp <= max_hp.
    """

    def __init__(self, name, max_hp, base_attack, ability=None):
        if max_hp <= 0:
            raise ValueError("max_hp must be positive")
        self.name = name
        self._max_hp = max_hp
        self._hp = max_hp
        self._base_attack = base_attack
        self.attack = StatStages(ability)
        self.defense = StatStages(ability)

    @property
    def hp(self):
        return self._hp

    @property
    def max_hp(self):
        return self._max_hp

    @property
    def is_alive(self):
        return self._hp > 0

    def effective_attack(self):
        """base_attack x attack stage multiplier, as a Fraction."""
        # TODO
        raise NotImplementedError

    def take_damage(self, amount):
        """Reduce hp, never below 0. Return the damage actually taken.

        Negative amounts are a programming error: raise ValueError.
        """
        # TODO
        raise NotImplementedError

    def heal(self, amount):
        """Raise hp, never above max_hp. Return the healing actually applied.

        A fighter at 0 hp cannot be healed (return 0). Negative amounts raise ValueError.
        """
        # TODO
        raise NotImplementedError
