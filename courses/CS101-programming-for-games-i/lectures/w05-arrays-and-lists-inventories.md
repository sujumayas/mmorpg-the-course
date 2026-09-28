# CS101 · Week 05 — Arrays and Lists: Inventories

**Why this matters:** Every game that lets you carry things keeps them in a list: slots in a backpack, cards in a hand, units in a squad. The rules for how that list fills decide what "inventory full" means, and players notice those rules the moment they break. Writing them yourself is the first time you'll manage many values with one variable and a loop.

**You will be able to:**
- Create, index, slice and loop over Python lists, and predict the result of `append`, `insert`, `pop` and `remove`.
- Implement a slot-based inventory with stack limits and compute its capacity for any item.
- Trace a two-pass "add item" algorithm by hand and explain why the pass order matters.
- Spot the aliasing bug, where two variables share one list, and fix it with a copy.

**Before class:** Python tutorial, sections 3.1.3 "Lists" and 5.1 "More on Lists" (docs.python.org). Nystrom, *Game Programming Patterns* (2014), "Game Loop" chapter, the first half, for how a loop visits every object each frame.

**Prerequisites from earlier courses:** [CS101 week 4, functions and decomposition](w04-functions-and-decomposition.md) (every inventory operation in this lecture is a function you can test). [CS101 week 3, loops and the game loop](w03-loops-and-the-game-loop.md) (`for` and `while`). Section 2 uses `min` as a cap and explains it where it appears; [MA101 week 7, piecewise functions, caps and floors](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w07-piecewise-caps-and-floors.md) covers caps in depth later this semester.

**Interactive:** [w05-inventory-stacking.html](../examples/w05-inventory-stacking.html). Use it during section 2.

---

## 1. Lists: many values, one name

Until now, each variable held one value. A text adventure with a sword, a torch and a key needed three variables, and a fourth item meant new code. A **list** holds any number of values in order under one name.

```python
backpack = ["sword", "torch", "key"]
```

In Python the word is "list." Other languages (and the syllabus title) say **array**, which usually means a fixed-size block of same-type values in memory. Godot's GDScript calls its version `Array`, and it behaves like a Python list. For this course the ideas are the same.

### Indexing

Each value in a list sits at a numbered position called its **index**. Indexes start at 0.

```python
backpack[0]      # "sword"
backpack[2]      # "key"
backpack[-1]     # "key"   (negative counts from the end)
len(backpack)    # 3
backpack[3]      # IndexError: list index out of range
```

The last valid index is always `len(backpack) - 1`. That "minus one" is the most common off-by-one in all of programming. When you see `IndexError`, check the loop bound first.

You can replace an item by assigning to its index:

```python
backpack[1] = "lantern"     # ["sword", "lantern", "key"]
```

### Growing and shrinking

| Operation | What it does | `backpack` after, from `["sword", "torch", "key"]` |
|---|---|---|
| `backpack.append("rope")` | add at the end | `["sword", "torch", "key", "rope"]` |
| `backpack.insert(0, "map")` | add at index 0, shifting the rest right | `["map", "sword", "torch", "key"]` |
| `backpack.pop()` | remove and return the last item | `["sword", "torch"]`, returns `"key"` |
| `backpack.pop(0)` | remove and return item 0 | `["torch", "key"]`, returns `"sword"` |
| `backpack.remove("torch")` | remove the first `"torch"` found | `["sword", "key"]` |
| `"key" in backpack` | is it there? | unchanged, returns `True` |
| `backpack.index("key")` | where is it? | unchanged, returns `2` |

Two details matter. `remove` and `index` raise `ValueError` if the item isn't there, so check with `in` first. And `insert(0, ...)` and `pop(0)` shift every other item along by one position. On a 3-item list you'll never notice. The Python wiki lists both as taking time proportional to the list's length, which is why a later course ([CS102 week 6](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w06-queues-and-stacks-undo-and-command-buffers.md)) introduces a queue for jobs like "the first enemy in line."

### Looping over a list

```python
for item in backpack:
    print(item)

for i, item in enumerate(backpack):
    print(i, item)          # 0 sword, 1 lantern, 2 key
```

Use the first form when you only need the values. Use `enumerate` when you also need the index, for example to change the item at that position.

### Slicing

A **slice** takes a piece of a list and returns a new list.

```python
hotbar = slots[0:9]     # indexes 0 to 8. The end index is excluded.
storage = slots[9:]     # index 9 to the end
```

The rule "start included, end excluded" means `slots[0:9]` has exactly `9 − 0 = 9` items. You'll use slices in section 2 to split a 36-slot inventory into a 9-slot hotbar and 27 storage slots.

## 2. Worked example: "inventory full," except it isn't

### The hook

In Minecraft, your inventory can have no empty slot at all, and you'll still pick up cobblestone when you walk over it. Walk over dirt instead and it stays on the ground. The game isn't being inconsistent. "Full" has two meanings, and the pickup code checks them in a specific order.

The Minecraft Wiki describes the rules for Java Edition. The player inventory has 27 storage slots and 9 hotbar slots, plus four armour slots and an off-hand slot. Most items stack to 64 per slot, some stack only to 16, and items with durability (tools, weapons, armour) don't stack at all. When you pick items up, the game fills existing partial stacks of that item before it uses an empty slot.

### The model

Represent the 36 main slots as a Python list. Each slot is either `None` (empty) or a **tuple** `(item, count)`. A tuple is like a list you can't change after creating it; to update a slot you replace the whole tuple.

```python
def make_inventory(n_slots):
    return [None] * n_slots

def add_item(inventory, item, count, stack_size):
    """Put count of item into inventory. Return how many did not fit."""
    # Pass 1: top up stacks of the same item that are not full.
    for i in range(len(inventory)):
        slot = inventory[i]
        if slot is not None and slot[0] == item and slot[1] < stack_size:
            moved = min(stack_size - slot[1], count)
            inventory[i] = (item, slot[1] + moved)
            count -= moved
            if count == 0:
                return 0
    # Pass 2: start new stacks in empty slots.
    for i in range(len(inventory)):
        if inventory[i] is None:
            moved = min(stack_size, count)
            inventory[i] = (item, moved)
            count -= moved
            if count == 0:
                return 0
    return count
```

Every name, defined:

- `inventory` is the list of slots. `add_item` changes it **in place**. It doesn't return a new list. It returns the leftover count, the number that stays on the ground.
- `stack_size` is the most of this item one slot can hold: 64, 16 or 1 in Minecraft.
- `min(stack_size - slot[1], count)` is a cap: `min` returns the smaller of its two arguments, so you move whichever is smaller, the free space in the slot or what you still carry.
- The two `for` loops are the two passes. Pass 1 only looks at matching, non-full stacks. Pass 2 only looks at empty slots.

The whole idea fits in one sentence. **An item fits if some slot with the same item has room, or some slot is empty.** "No empty slots" only rules out the second.

### Numbers you can check

First, a small trace you can do by hand. Five slots, stack size 64. Slot 1 holds 60 arrows, slot 3 holds 10. Add 70 arrows.

| Step | Slot looked at | Before | Moved | After | Still to place |
|---|---|---|---|---|---|
| Pass 1 | 1 | `("arrow", 60)` | `min(4, 70) = 4` | `("arrow", 64)` | 66 |
| Pass 1 | 3 | `("arrow", 10)` | `min(54, 66) = 54` | `("arrow", 64)` | 12 |
| Pass 2 | 0 | `None` | `min(64, 12) = 12` | `("arrow", 12)` | 0 |

Final list: `[("arrow", 12), ("arrow", 64), None, ("arrow", 64), None]`. Returned leftover: 0.

Notice slot 0 now holds 12 while slots 1 and 3 are full. If pass 2 ran first, the 70 arrows would land in slots 0 and 2 as 64 and 6, leaving three partial stacks where the real algorithm leaves one. Pass order is a design decision with a visible result.

Now the hook scenario. Slots 0 to 34 hold full stacks of dirt and single pickaxes, alternating. Slot 35 holds 50 cobblestone. There is no `None` anywhere.

```python
inv = make_inventory(36)
for i in range(35):
    inv[i] = ("dirt", 64) if i % 2 == 0 else ("pickaxe", 1)
inv[35] = ("cobblestone", 50)

print(None in inv)                              # False: "full"
print(add_item(inv, "cobblestone", 20, 64))     # 6 left on the ground
print(inv[35])                                  # ('cobblestone', 64)
print(add_item(inv, "cobblestone", 5, 64))      # 5: now truly full for cobblestone
print(add_item(inv, "dirt", 3, 64))             # 3: every dirt stack is at 64
```

| Pick up | Matching stack with room? | Empty slot? | Result |
|---|---|---|---|
| 20 cobblestone | slot 35, 14 free | no | 14 taken, 6 left |
| 5 more cobblestone | no (slot 35 now 64) | no | 0 taken, 5 left |
| 3 dirt | no (all dirt stacks at 64) | no | 0 taken, 3 left |

Finally, capacity. How much of one item can an empty inventory hold? `slots × stack_size`. How many slots does `n` of an item need? `ceil(n / stack_size)`, rounding up because a half-full slot is still a slot.

| Inventory | Slots | Stack size | Capacity for one item | Slots for 200 of it |
|---|---|---|---|---|
| Minecraft main inventory, 64-stack item | 36 | 64 | 2,304 | 4 |
| Minecraft main inventory, 16-stack item | 36 | 16 | 576 | 13 |
| Minecraft main inventory, tool | 36 | 1 | 36 | does not fit |

Check the middle row: `200 / 16 = 12.5`, round up, 13 slots.

### Move it

Open the interactive. The left view is the slot grid, drawn as a 9-slot hotbar under 27 storage slots. The right view is the same inventory printed as a Python list, exactly what `print(inventory)` would show. Pick an item, set a count, press "Pick up," and watch each pass run: pass 1 highlights the matching slots it tops up, pass 2 highlights the empty slots it fills, and anything left over drops into a "ground" box.

Load the preset "No empty slots." The grid looks full. Pick up cobblestone and 14 of them still go in. Pick up dirt and none do. The status line under the grid says two things at once: "Empty slots: 0 · Room for cobblestone: 14". The "Room for" table beside it lists every item, and dirt shows 0. The room number is what the player actually needs, and it's different for every item.

### The same idea in other games

Change two parameters, the number of slots and the stack rule, and the same function describes very different inventories.

**Old School RuneScape (current).** The backpack has 28 slots. Stackable items, such as coins, runes and arrows, take one slot no matter how many you hold. Everything else takes one slot per item. In our model that is `add_item(inv, item, count, stack_size)` with `n_slots = 28`, a stack size of 1 for most items, and a stack size so large it never fills for stackables. So 28 slots hold 28 swords or 28 different stackables of any size. Players plan trips around that 28, because the limit falls on distinct non-stacking things.

**Pokémon Red and Blue (Generation I, 1998 English release).** Bulbapedia describes the Bag as a list of up to 20 kinds of item, with no pockets, and up to 99 of each. In our model, 20 slots with a stack size of 99. The limit players hit is kinds of item, not quantity. Twenty different items fill the bag even if you hold one of each.

**Your own week 1 text adventure.** A plain Python list with `append` is an inventory with unlimited slots and a stack size of 1. Every design above is that list plus two rules.

| Game | Slots | Stack rule | What the player runs out of |
|---|---|---|---|
| Minecraft (Java) | 36 main | 64, 16 or 1 per item | slots, for mixed loot |
| Old School RuneScape | 28 | unlimited or 1 | slots, for non-stackables |
| Pokémon Red/Blue | 20 | 99 | kinds of item |
| Week 1 text adventure | unlimited | 1 | nothing |

### Design judgment

The algorithm is small. The choices around it shape how the game feels.

- **Slots versus stack size.** Few slots and big stacks (Pokémon) makes variety the limit, so players carry one of everything and never think about quantity. Many slots and small stacks pushes players to sort and throw things away. Decide which pressure you want before you pick the numbers.
- **Which items stack.** Making an item non-stackable is the strongest limit you have. RuneScape's 28 non-stackable slots make food a real trade-off against loot. Tools with durability can't stack in Minecraft because each one carries its own remaining uses, so a stack would have to hold many different values in one slot.
- **Fill order.** Topping up partial stacks first keeps stacks consolidated. Filling left to right means new items appear in predictable places, which matters when the first nine slots are a hotbar the player uses in combat. If your game auto-equips from the hotbar, a pickup that lands in slot 0 can change what the player is holding. Decide this on purpose and test it.
- **Tell the player what they need to know.** "Inventory full" is misleading when a matching stack still has room. A better message names the item: "No room for dirt."

## 3. Lists as values: the aliasing trap

Here is a bug that catches almost everyone once.

```python
starting_kit = ["sword", "potion"]
player_one = starting_kit
player_two = starting_kit
player_one.append("shield")
print(player_two)       # ['sword', 'potion', 'shield']  ???
```

Assignment with `=` does not copy a list. It makes a second name for the **same** list. `starting_kit`, `player_one` and `player_two` are three labels on one box. Change the box through any label and all three see it. This is called **aliasing**.

Numbers and strings don't show this, because you can't change them in place. `hp = hp - 5` makes a new number and moves the label. Lists (and week 6's dictionaries) can be changed in place, so aliasing matters.

The fix is to copy when you mean "a separate list with the same contents":

```python
player_one = starting_kit.copy()     # or list(starting_kit), or starting_kit[:]
```

The same thing happens with functions, and this is where week 4's "parameters are local" rule gets a footnote. When you pass a list to a function, the parameter is another label on the same list. `add_item` changes `inventory[i]`, and the caller sees the change. That is exactly what we want there. It is not what you want in a function that is supposed to only look.

```python
def count_items(inventory):
    total = 0
    for slot in inventory:
        if slot is not None:
            total += slot[1]
    return total          # reads, never writes: safe
```

A good habit: a function either changes a list it was given (and says so in its docstring, and usually returns `None` or a small result like the leftover count) or leaves it alone and returns something new. Mixing both surprises the caller.

### A copy trap inside the trap

`[None] * 36` is safe because `None` can't be changed. But `[[]] * 3` builds a list of three labels on **one** empty inner list:

```python
bags = [[]] * 3
bags[0].append("apple")
print(bags)       # [['apple'], ['apple'], ['apple']]
```

Build nested lists with a loop or a comprehension instead: `bags = [[] for _ in range(3)]`. This is why the inventory in section 2 stores tuples, which can't be changed in place, and replaces the whole slot on every update.

## 4. Changing a list while you loop over it

Another classic. You want to drop every broken item:

```python
items = ["sword", "broken_bow", "broken_axe", "torch"]
for item in items:
    if item.startswith("broken"):
        items.remove(item)
print(items)      # ['sword', 'broken_axe', 'torch']  one survived
```

Removing `"broken_bow"` at index 1 shifts `"broken_axe"` into index 1, and the loop moves on to index 2, skipping it. Don't change a list's length while a `for` loop walks it. Build a new list instead:

```python
items = [item for item in items if not item.startswith("broken")]
```

That line is a **list comprehension**: "a list of `item` for each `item` in `items`, if it doesn't start with 'broken'." It reads like the sentence you'd say out loud, and it never skips anything because it never modifies the list it's reading.

### Sorting

Players love a "sort" button. `sorted` returns a new sorted list; `.sort()` sorts in place.

```python
loot = [("gem", 3), ("arrow", 40), ("bread", 7)]
sorted(loot)                                  # by name: arrow, bread, gem
sorted(loot, key=lambda s: s[1], reverse=True)  # by count: arrow, bread, gem
```

The `key=` argument takes a function (here a small unnamed one, a **lambda**) that turns each item into the value to sort by. You'll write a real "sort inventory" function in the lab, and you'll need to decide where `None` slots go.

### How long does it take?

`"key" in backpack` checks each item from the start until it finds a match. On a 36-slot inventory that's at most 36 comparisons, far too quick to measure. But `add_item` scans the list twice on every pickup, and a game with 5,000 items in a bank or 10,000 entries in an item database will start to feel it. Week 6 introduces the structure that finds things without scanning.

## In-class activity (25 minutes)

In pairs. Materials: the `add_item` function from section 2 (copy it into a file) and a sheet of paper.

1. (8 min) On paper, trace `add_item` on a 4-slot inventory `[("gem", 8), None, ("gem", 3), None]` with stack size 10, adding 12 gems. Write the list after each slot is touched and the leftover. Then run it and compare.
2. (7 min) Change the design so the hotbar (slots 0 to 8 of a 36-slot inventory) is filled only after storage (9 to 35) in pass 2. You may only change the order in which pass 2 visits indexes. Write the one-line change. Hint: a slice or `list(range(...))` concatenation.
3. (10 min) Design an inventory for a survival game where water is critical. Pick the number of slots, the stack sizes for water, food and wood, and one item that doesn't stack. Use the capacity formula to state how many water units a player can carry if they carry nothing else, and how many if they also carry 100 wood.

Expected output: the trace table from step 1, the changed line from step 2, and three numbers with one sentence of reasoning from step 3.

## Common misconceptions

- **"No empty slots means I can't pick anything up."** A matching stack with room still accepts that item. Fullness depends on the item.
- **"`b = a` makes a copy of the list."** It makes a second name for the same list. Use `a.copy()` when you need a separate list.
- **"`remove` inside a `for` loop over the same list is fine."** It skips the item after each removal. Build a new list with a comprehension instead.
- **"Index 36 is the last slot of a 36-slot inventory."** The last index is 35. Indexes run from 0 to `len − 1`.

## Check yourself

1. A game has 24 slots and a stack size of 20 for potions. The player holds 3 slots of potions at 20, 20 and 7, and 21 other slots are full of other items. How many potions can they pick up? How many if one of the other slots were empty?
2. Trace `add_item` on `[None, ("ore", 30), None]` with stack size 32, adding 70 ore. Give the final list and the return value.
3. What does this print, and why?

```python
row = [0] * 3
grid = [row] * 2
grid[0][1] = 5
print(grid)
```

4. A designer wants to make a 16-stack item carry as much as a 64-stack item. How many slots does a player need to carry 256 of each? Is the designer's goal about slots or about stack size?
5. Rewrite this loop as one list comprehension: keep only slots that are not `None` and have a count above 1.

```python
kept = []
for slot in inventory:
    if slot is not None and slot[1] > 1:
        kept.append(slot)
```

<details>
<summary>Answers</summary>

1. Pass 1 only: the stack at 7 has 13 free, the two at 20 have none. They can pick up 13. With one empty slot, pass 2 adds another 20, so 33.
2. Pass 1: slot 1 goes from 30 to 32 (2 moved, 68 left). Pass 2: slot 0 gets 32 (36 left), slot 2 gets 32 (4 left). No slots remain. Final list `[("ore", 32), ("ore", 32), ("ore", 32)]`, returns 4.
3. `[[0, 5, 0], [0, 5, 0]]`. `[row] * 2` puts the same inner list in both positions (aliasing), so changing one row changes "both." Build it with `[[0] * 3 for _ in range(2)]`.
4. 256 of the 64-stack item needs 4 slots; 256 of the 16-stack item needs 16. Carrying the same amount means using 4 times as many slots, so the stack size is what makes them unequal. To make them equal per slot, the stack sizes must be equal.
5. `kept = [slot for slot in inventory if slot is not None and slot[1] > 1]`

</details>

## Lab / assignment hook

[Lab 05, a stacking inventory](../labs/lab05.md). Implement `add_item`, `remove_item`, `count_item` and `sort_inventory` for a 36-slot inventory with a hotbar, pass the provided tests (several of them at the "full but not full" edge), and connect it to your lab 04 fight so potions come from the inventory. Deliverable: the module with passing tests and a 200-word note on your fill-order choice.

## Sources

- Minecraft Wiki, "Inventory" (Java Edition, current). 27 storage slots, 9 hotbar slots, 4 armour slots and an off-hand slot; most items stack to 64, some to 16, items with durability do not stack; picked-up items fill existing partial stacks before empty slots. https://minecraft.wiki/w/Inventory
- Old School RuneScape Wiki, "Inventory" (current game). 28 slots; stackable items such as coins, runes and arrows take a single slot however many are held; each non-stackable item takes one slot. https://oldschool.runescape.wiki/w/Inventory
- Bulbapedia, "Bag", Generation I section (Pokémon Red, Blue and Yellow). The Bag is a single list of up to 20 kinds of item, up to 99 of each.
- Python Software Foundation, *The Python Tutorial*, sections 3.1.3 "Lists" and 5.1 "More on Lists" (Python 3.12 documentation).
- Python Wiki, "TimeComplexity". List `insert` and `pop` from the middle, and `x in s`, take time proportional to the list's length; `append` and `pop()` from the end take constant time on average. https://wiki.python.org/moin/TimeComplexity
- Nystrom, R. (2014). *Game Programming Patterns*, "Game Loop". gameprogrammingpatterns.com.

## Interactive spec: examples/w05-inventory-stacking.html

**Purpose.** Show that "no empty slots" and "can't pick up this item" are different conditions, by running the two-pass `add_item` visibly on a slot grid linked to its Python list printout.

**Layout.** Two linked views, side by side on desktop, stacked on mobile (grid first).

- **Left: the slot grid.** 27 storage slots (3 rows of 9) above a separated row of 9 hotbar slots, so slots are numbered 9-35 for storage and 0-8 for the hotbar, matching `hotbar = slots[0:9]`. Each slot shows a generic coloured shape per item type (circle, square, triangle, diamond, bar; no game art) and its count in the corner. Slot index shown on hover/focus. A "ground" box below holds leftovers with their count.
- **Right: the list view.** A monospace block showing `inventory = [` followed by one line per slot, `  ('cobblestone', 64),  # 35` or `  None,  # 2`, scrolling, with the lines for slots touched by the last operation highlighted in the same colour as the grid highlight.
- **Status line** under the grid: `Empty slots: N · Room for <selected item>: M`, where `M = sum over slots of (stack_size − count) for matching slots + (empty slots × stack_size)`. Also a small table "Room for each item type" listing M for all five item types.

**Controls.**
- Item picker: cobblestone (stack 64), dirt (64), arrow (64), pearl (16), pickaxe (1). Stack sizes shown next to names.
- Count input, 1 to 500, default 20.
- "Pick up" button runs `add_item`. Animation: pass 1 highlights each matching non-full slot in order and fills it; then pass 2 highlights each empty slot in order. 150 ms per slot; instant when `prefers-reduced-motion` is set or when a "Skip animation" checkbox is ticked. A "Pass 1 / Pass 2 / Leftover" readout shows the counts moved in each pass.
- "Fill order" toggle: `partial stacks first` (default, the two-pass algorithm) versus `empty slots first` (pass 2 runs before pass 1). Changing it does not alter the current state; it affects the next pickup.
- Pass 2 order selector: `0 → 35` (default) or `storage first (9 → 35, then 0 → 8)`.
- Presets: "Empty", "Arrow trace" (5-slot mode: only slots 0-4 enabled, slot 1 = arrow 60, slot 3 = arrow 10), "No empty slots" (slots 0-34 alternating dirt 64 and pickaxe 1 starting with dirt at slot 0, slot 35 = cobblestone 50), and "Reset".
- Click a slot (or Enter when focused) to empty it.

**Formulas.** Exactly the `add_item` in lecture section 2. `leftover = count − moved_pass1 − moved_pass2`. Capacity of an empty inventory for an item: `n_slots × stack_size`.

**Test values (must match exactly).**
- Arrow trace, add 70 arrows, partial first: final slots `[('arrow', 12), ('arrow', 64), None, ('arrow', 64), None]`, pass 1 moved 58, pass 2 moved 12, leftover 0.
- Arrow trace, add 70 arrows, empty first: slot 0 gets 64, slot 2 gets 6, pass 1 moves 0, final `[('arrow', 64), ('arrow', 60), ('arrow', 6), ('arrow', 10), None]`, leftover 0. Three partial stacks remain; the readout says so.
- No empty slots: status `Empty slots: 0 · Room for cobblestone: 14`, room for dirt 0. Pick up 20 cobblestone: 14 in, 6 to ground. Then 5 cobblestone: 0 in, 5 to ground. Then 3 dirt: 0 in, 3 to ground.
- Empty inventory: room for cobblestone 2,304, pearl 576, pickaxe 36.

**The one insight.** Load "No empty slots": the status line shows `Empty slots: 0` next to `Room for cobblestone: 14`. Two different numbers for "full" on the first screen.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css` inline. Every slot is a focusable button with `aria-label` like "Slot 35, cobblestone, 50 of 64". Item shapes differ in shape as well as colour. Works at 390px width with the grid at 9 columns of at least 36px.
