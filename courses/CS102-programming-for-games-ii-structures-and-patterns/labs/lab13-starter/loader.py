"""CS102 Lab 13: a validated data loader.

Fill in every function marked TODO. Run `python check_lab13.py` after each part.
Standard library only. Python 3.10 or later.
"""
import csv
import json
import os
from dataclasses import dataclass

VALID_TYPES = {"sword", "axe", "mace", "knife"}   # Part A step 3: you will add one
SPECIAL_ITEMS = {"gold", "nothing"}               # loot items that are not weapons
MONSTER_FIELDS = {"name", "hp", "armor", "weapon", "loot"}


@dataclass(frozen=True)
class Weapon:
    id: str
    name: str
    type: str
    min_dmg: int
    max_dmg: int
    attacks_per_sec: float
    req_str: int
    upgrade: str | None


def number(row, key, kind, default=None):
    """Convert row[key] (a string) to int or float. Blank uses default if one is given."""
    text = row[key].strip()
    if text == "" and default is not None:
        return default
    try:
        return kind(text)
    except ValueError:
        raise ValueError(f"{key}: '{text}' is not a valid {kind.__name__}") from None


def average_hit(w):
    return (w.min_dmg + w.max_dmg) / 2


def dps(w):
    return average_hit(w) * w.attacks_per_sec


# ---------------------------------------------------------------- Part A: weapons

def parse_row(row, line, errors):
    """Return a Weapon built from one CSV row (a dict of strings), appending any
    problems to errors as 'line N: ...'. Return None if the row cannot be built.
    Checks: numbers parse; req_str blank means 0; type in VALID_TYPES;
    0 <= min_dmg <= max_dmg; attacks_per_sec > 0. Report every problem, not just the first."""
    raise NotImplementedError("TODO Part A")


def load_weapons(path):
    """Return {id: Weapon}. Collect every problem (including duplicate ids and upgrade
    ids that do not exist) and raise ONE ValueError listing them all, one per line."""
    raise NotImplementedError("TODO Part A")


# ---------------------------------------------------------------- Part B: monsters

def resolve(rows):
    """rows: {id: dict}. A row may name a 'parent' id. Return {id: flat dict} where
    each row's missing keys come from its parent (recursively). A key that is present,
    even with value 0 or an empty list, is NOT inherited. Raise ValueError naming the
    ids involved if parents form a cycle, or if a parent id does not exist."""
    raise NotImplementedError("TODO Part B")


def load_monsters(path, weapons):
    """Load monsters.json, resolve parents, then validate every monster:
    - exactly the keys in MONSTER_FIELDS after resolving (report missing and unknown keys)
    - name is a non-empty str; hp is an int > 0; armor is an int >= 0
      (bool is not an int here: reject True/False)
    - weapon is an id in weapons
    - loot is a list; each entry has an item in weapons or SPECIAL_ITEMS and an
      int weight > 0; the loot list has at least one valid entry
    Name each problem by monster id and path, e.g. "goblin.loot[1]: unknown item 'x'".
    Collect everything, raise one ValueError, or return {id: dict}.
    Tip: resolve each monster's own parent chain separately (a small dict of just the
    rows it reaches), so that one cycle does not hide every other problem in the file."""
    raise NotImplementedError("TODO Part B")


# ---------------------------------------------------------------- Part C: live reload

class LiveTable:
    """Holds a loaded table and reloads it when the file changes on disk."""

    def __init__(self, path, loader):
        self.path = path
        self.loader = loader
        self.table = loader(path)          # must succeed at startup
        self.mtime = os.path.getmtime(path)
        self.last_error = None

    def poll(self):
        """If the file's modification time changed, try to reload it.
        On success replace self.table and set self.last_error = None, return True.
        On ValueError keep the old table, store the message in self.last_error,
        return False. If nothing changed return None."""
        raise NotImplementedError("TODO Part C")
