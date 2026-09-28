"""CS101 Lab 05 starter: a slot inventory with stacks.

An inventory is a list of slots. Each slot is None (empty) or a tuple
(item, count). Slots 0-8 are the hotbar, slots 9-35 are storage.

Run the tests:  python test_lab05.py
Run the demo:   python inventory.py
"""

HOTBAR = range(0, 9)
STORAGE = range(9, 36)

STACK_SIZES = {"cobblestone": 64, "dirt": 64, "arrow": 64,
               "potion": 16, "pearl": 16, "pickaxe": 1, "sword": 1}


def make_inventory(n_slots=36):
    """Return a list of n_slots empty slots. Done for you."""
    return [None] * n_slots


def count_item(inventory, item):
    """Total count of item across all slots. Must not change the inventory."""
    raise NotImplementedError


def room_for(inventory, item, stack_size):
    """How many more of item would fit: free space in matching stacks
    plus stack_size for every empty slot."""
    raise NotImplementedError


def add_item(inventory, item, count, stack_size):
    """Add count of item in place, using the two-pass rule from the lecture:
    pass 1 tops up matching non-full stacks from index 0 upward,
    pass 2 starts new stacks in empty slots, storage first (index 9 to the end),
    then the hotbar (0-8). Return how many did not fit."""
    raise NotImplementedError


def remove_item(inventory, item, count):
    """Remove up to count of item in place, taking from the highest index
    first. A slot that reaches 0 becomes None. Return how many were removed."""
    raise NotImplementedError


def sort_inventory(inventory):
    """Return a NEW list with the same slots sorted by item name (A to Z),
    larger stacks first within a name, and all None slots at the end.
    The original list must not change."""
    raise NotImplementedError


if __name__ == "__main__":
    inv = make_inventory()
    print(add_item(inv, "arrow", 100, STACK_SIZES["arrow"]))
    print(inv)
