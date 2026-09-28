"""CS102 Lab 03 starter: a tiny chemistry engine (Design B, polymorphism).

Rules, after the three rules reported from the Breath of the Wild GDC 2017 talk:
  1. Elements change the state of materials.
  2. Elements change each other (here: water undoes fire's effect on a material).
  3. Materials never change each other directly.

Contract for Material.react(element):
  - returns a short description (str) of what happened, or None if nothing happened;
  - never raises, for any element string, including ones it has never heard of;
  - may change self.state, which must always be one of STATES.
"""

ELEMENTS = ["fire", "water", "electric"]
STATES = {"normal", "burning", "wet", "charged", "melted"}


class Material:
    def __init__(self, name):
        self.name = name
        self.state = "normal"

    def react(self, element):
        return None                       # default: ignore everything


class Grass(Material):
    def react(self, element):
        if element == "fire" and self.state != "wet":
            self.state = "burning"
            return "catches fire and spreads"
        if element == "water":
            self.state = "wet"
            return "gets wet"
        return None


class Wood(Material):
    def react(self, element):
        if element == "fire" and self.state != "wet":
            self.state = "burning"
            return "burns"
        if element == "water" and self.state == "burning":
            self.state = "normal"
            return "is put out"
        return None


class Metal(Material):
    def react(self, element):
        if element == "electric":
            self.state = "charged"
            return "conducts, shocks nearby"
        return None


class Stone(Material):
    pass


def all_material_classes():
    """Every concrete subclass of Material defined so far, found by walking the tree."""
    found, stack = [], list(Material.__subclasses__())
    while stack:
        cls = stack.pop()
        found.append(cls)
        stack.extend(cls.__subclasses__())
    return sorted(found, key=lambda c: c.__name__)


def apply(element, targets):
    """Apply one element to every target. This function must never need editing."""
    return [(t.name, t.react(element)) for t in targets]
