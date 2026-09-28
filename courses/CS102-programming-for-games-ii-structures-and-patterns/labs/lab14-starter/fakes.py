"""Test doubles for injecting randomness."""


class ScriptedRng:
    """Stands in for random.Random. Returns pre-chosen values, in order."""

    def __init__(self, values):
        self._values = iter(values)

    def random(self):
        return next(self._values)

    def randint(self, a, b):
        v = next(self._values)
        if not a <= v <= b:
            raise ValueError(f"scripted value {v} outside randint({a}, {b})")
        return v
