"""CS101 Lab 06 starter: an item database as a dictionary of dictionaries.

Files:
  items.json           the database you will fix (it has three data errors)
  items_original.json  an untouched copy, used by the tests; do not edit it
  ids_v1.json          version 1 of the game stored items by position:
                       ID = 256 + index in this list
  save_v1.json         a version 1 save file that uses those numeric IDs

Run the tests:  python test_lab06.py
"""
import json

REQUIRED = ["name", "type", "stack", "price"]
FIRST_ID_V1 = 256
ALIASES = {"short_sword": "wooden_sword"}   # old key -> current key


def load_json(path):
    """Read a JSON file and return the Python value. Done for you."""
    with open(path) as f:
        return json.load(f)


def validate(db):
    """Return a list of problem strings, each starting with the item key,
    e.g. "arrow: stack must be at least 1". Check: every REQUIRED field is
    present; stack >= 1; every item of type "weapon" has "damage".
    Return [] when the data is fine."""
    raise NotImplementedError


def find(db, key, aliases=ALIASES):
    """Return the record for key. If key is an old name in aliases, follow it.
    If the key is still unknown, raise KeyError(key)."""
    raise NotImplementedError


def items_of_type(db, item_type):
    """Return the keys of all items of item_type, sorted A to Z."""
    raise NotImplementedError


def total_value(inventory, db):
    """inventory is a week 5 slot list: None or (key, count).
    Return the sum of price * count over all slots."""
    raise NotImplementedError


def migrate_save(old_save, ids_v1):
    """Convert a version 1 save to version 2. Return a NEW dict:
    same fields, "version": 2, and each non-null slot [id, count] replaced
    by [key, count], where key = ids_v1[id - FIRST_ID_V1]. Null slots stay None.
    Do not modify old_save."""
    raise NotImplementedError


if __name__ == "__main__":
    db = load_json("items.json")
    for problem in validate(db):
        print(problem)
