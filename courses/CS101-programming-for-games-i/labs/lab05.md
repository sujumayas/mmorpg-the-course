# CS101 · Lab 05: A stacking inventory

**Week:** 5, arrays and lists ([lecture](../lectures/w05-arrays-and-lists-inventories.md)).
**Time:** 2 hours in lab, plus up to 2 hours at home.
**Weight:** part of the weekly exercises (40%). Lab 06 replaces the hard-coded stack sizes with an item database.

## Objective

Implement a 36-slot inventory with a 9-slot hotbar and stack limits: count, measure room, add with the two-pass rule, remove, and sort. Make the provided tests pass, including the "no empty slots but still room" case from the lecture. Then connect it to your lab 04 fight so the potion count comes from the inventory.

## Starter materials

All in [`lab05-starter/`](lab05-starter/). Standard-library Python 3.10 or later.

- [`inventory.py`](lab05-starter/inventory.py) with `make_inventory` done for you and five empty functions, each with a docstring that is the spec: `count_item`, `room_for`, `add_item`, `remove_item`, `sort_inventory`. It also defines `HOTBAR`, `STORAGE` and a small `STACK_SIZES` dictionary (you'll learn dictionaries properly in week 6; here, read `STACK_SIZES["potion"]` as "the stack size for potions").
- [`test_lab05.py`](lab05-starter/test_lab05.py) with eight tests. Run `python test_lab05.py`. The starter reports `0/8 tests passed`.

One rule differs from the lecture on purpose. Pass 2 fills **storage first** (index 9 to the end), then the hotbar (0 to 8), so pickups don't land in the player's hand. `test_add_tops_up_before_new_stacks` uses a 12-slot inventory, so your code must work for any length, not only 36.

## Steps

1. **Read-only functions first.** Write `count_item` and `room_for`. Neither may change the list; the tests check this. `room_for` is the lecture's status-line number: free space in matching stacks plus `stack_size` per empty slot.
2. **`add_item`.** Implement the two passes. For pass 2's order, build a list of indexes: storage indexes, then hotbar indexes. Before running the tests, trace `test_add_tops_up_before_new_stacks` on paper and write the expected list. Then run the tests.
3. **Cross-check.** For any inventory and item, `add_item` must return `max(0, count − room_for(...))`. Write a loop that tries 200 random inventories and counts and asserts this. It's a cheap way to catch a bug the fixed tests miss.
4. **`remove_item`.** Take from the highest index first, so the hotbar is emptied last. Slots that reach 0 become `None`, never `("potion", 0)`.
5. **`sort_inventory`.** Return a new list: items A to Z, larger stacks first within an item, `None` at the end. Use `sorted` with a `key=` function. Do not change the original (aliasing, lecture section 3).
6. **Connect to lab 04.** In your lab 04 `play()`, replace the `potions` variable with an inventory. Drinking calls `remove_item(inv, "potion", 1)` and only heals if it returned 1. The rat drops 1 to 3 potions when defeated; add them with `add_item` and print what didn't fit.
7. **Stretch.** Write `merge_stacks(inventory, stack_sizes)` that consolidates partial stacks of the same item. For example, three 10-potion stacks with stack size 16 become 16, 14 and an empty slot. Write three tests first.

## Deliverable

`inventory.py` with `python test_lab05.py` reporting `8/8 tests passed`, your cross-check loop from step 3, your updated lab 04 file, and a note of at most 200 words: why storage-first is or isn't the right fill order for your game, and one case your cross-check caught (or a sentence on why it caught nothing).

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Tests pass | 8/8 | 6-7 | 5 or fewer | 35% |
| Cross-check loop | Random inventories, asserts the `room_for` identity, runs 200+ cases | Runs a few fixed cases | Missing | 15% |
| Aliasing and in-place rules | Read-only functions and `sort_inventory` never modify input; `add_item`/`remove_item` do, and say so | One function breaks its contract | Several do | 15% |
| Lab 04 integration | Potions come only from the inventory; drops respect `add_item` leftovers | Works with shortcuts (e.g. ignores leftovers) | Missing | 20% |
| Fill-order note | Argues from how the hotbar is used, with a concrete example | States a preference without reasons | Missing | 15% |
