# CS101 · Week 06 — Dictionaries: Item Databases

**Why this matters:** A game with 300 items can't have 300 variables, and a list makes you search for the one you want. A dictionary finds a record by its name in one step, however big the table gets. The choice of what that name is (a number, a position, a readable string) decides whether your save files survive the next content update.

**You will be able to:**
- Create, read, update and loop over Python dictionaries, and handle a missing key with `in` or `.get`.
- Build an item database as a dictionary of dictionaries and load it from a JSON file.
- Compute how many comparisons a list search needs for `n` records and explain why a dictionary lookup does not grow with `n`.
- Choose stable keys for game data and explain what breaks when IDs are positions in a list.

**Before class:** Python tutorial, section 5.5 "Dictionaries" and section 7.2.2 "Saving structured data with json" (docs.python.org). Skim the Minecraft Wiki page "Java Edition 1.13/Flattening", only the opening summary.

**Prerequisites from earlier courses:** [CS101 week 5, arrays and lists](w05-arrays-and-lists-inventories.md) (lists, tuples, aliasing and the cost of `in` on a list). [CS101 week 4, functions and decomposition](w04-functions-and-decomposition.md) (the `EXITS` and `DESCRIPTIONS` dictionaries you used without a full explanation). Looking ahead, [GD203 week 9, item budgets and stat weights](../../GD203-combat-and-progression-design/lectures/w09-item-budgets-and-stat-weights.md) covers the design side of the item records you store today. You don't need it for this lecture.

**Interactive:** [w06-ids-vs-keys.html](../examples/w06-ids-vs-keys.html). Use it during section 2.

---

## 1. Dictionaries: look it up by name

A **dictionary** (Python type `dict`) stores **key-value pairs**. You give it a key and it gives you the value filed under that key. Think of a real dictionary: you don't read every page to find "sword," you go straight to it.

```python
prices = {"sword": 120, "potion": 15, "torch": 3}

prices["potion"]          # 15
prices["shield"] = 90     # add a new pair
prices["torch"] = 4       # replace the value for an existing key
del prices["sword"]       # remove a pair
len(prices)               # 3
```

The key goes in square brackets, just like a list index. The difference is what can go there. A list index must be a position, 0 to `len − 1`. A dictionary key can be any **immutable** value: a string, a number, or a tuple of those. Lists can't be keys, because they can change after you use them.

### Missing keys

Ask for a key that isn't there and Python raises `KeyError`.

```python
prices["bow"]             # KeyError: 'bow'
```

Two ways to avoid the crash, and they mean different things.

```python
if "bow" in prices:                   # "is it there?"
    print(prices["bow"])

cost = prices.get("bow", 0)           # "give me the value, or 0 if missing"
```

Use `in` when a missing key is a situation your code must handle differently. Use `.get` with a default when missing has a sensible meaning, like "you have 0 of that." Don't use `.get` to hide a key that should always exist. If your item database has no entry for `"iron_sword"`, that's a data bug, and a `KeyError` telling you so is a gift.

### Looping

```python
for name in prices:                  # keys
    print(name)

for name, cost in prices.items():    # key and value together
    print(f"{name}: {cost} gold")
```

Since Python 3.7, dictionaries remember the order in which keys were inserted, and loops follow that order. That's handy for display, but don't make game rules depend on it. Treat a dictionary as a lookup table, not a sequence.

### Counting with a dictionary

A very common game job is "how many of each?" A dictionary keyed by item name does it in three lines.

```python
drops = ["coin", "bone", "coin", "gem", "coin", "bone"]
counts = {}
for item in drops:
    counts[item] = counts.get(item, 0) + 1
print(counts)       # {'coin': 3, 'bone': 2, 'gem': 1}
```

`counts.get(item, 0)` is the "you have 0 of that" default, used exactly as intended. Compare with week 5's slot list. For a bank or a crafting-materials pouch where only the totals matter, a dictionary `{item: count}` replaces the whole two-pass `add_item` with one line.

## 2. Worked example: from "diamond sword = 276" to `minecraft:diamond_sword`

### The hook

Until 2018, every item in Minecraft: Java Edition had a number. The iron shovel was 256, the apple 260, the bow 261, the diamond sword 276. Blocks had their own numbers below 256, which is how the game told blocks and items apart. Colours and variants were a second number stuck on the end, so red wool was `35:14`. Players typed these numbers into commands and map makers memorised them.

Then Java Edition 1.13, released in July 2018, removed numeric IDs. In "The Flattening," every block and item got a readable, namespaced string ID like `minecraft:stone`, and variants that used to share a number became items of their own: "planks" with a variant number became `oak_planks`, `spruce_planks` and so on.

A game already years past launch rewrote the way it names every item. This section shows the two data structures behind the two eras, and why the second one is what you should build from day one.

### The model

There are two ways to store an item database.

**As a list, where the ID is a position (or found by searching).**

```python
ITEM_LIST = [
    {"id": "iron_shovel", "name": "Iron Shovel", "damage": 4},
    {"id": "apple",       "name": "Apple",       "heal": 4},
    # ... hundreds more
]

def find_in_list(items, item_id):
    """Scan from the front. Return (record, comparisons)."""
    steps = 0
    for record in items:
        steps += 1
        if record["id"] == item_id:
            return record, steps
    return None, steps
```

**As a dictionary, where the ID is the key.**

```python
ITEM_DB = {
    "iron_shovel": {"name": "Iron Shovel", "damage": 4},
    "apple":       {"name": "Apple",       "heal": 4},
    # ... hundreds more
}

record = ITEM_DB["apple"]     # no loop
```

Two quantities describe the difference.

- **Lookup cost.** For a list of `n` records, `find_in_list` compares one record per step. If the item is equally likely to be anywhere, the average number of comparisons for an item that exists is `(n + 1) / 2`. For an item that doesn't exist it is `n`, because you must check everything to be sure. For a dictionary, the Python wiki lists the average cost of `d[key]` as constant: it doesn't grow with `n`.
- **ID stability.** If an item's ID is its position in a list, inserting or removing an item changes the ID of every item after it. If the ID is a key, adding or removing an item changes nothing else.

How can a dictionary skip the search? Python runs the key through a **hash function**, which turns it into a number, and uses that number to jump straight to a small area of memory where the value lives. You don't need the details in this course ([CS102 week 4](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w04-big-o-intuition-for-game-developers.md) gives you the vocabulary for how costs grow). You only need the consequence: finding `"apple"` among 10 items and among 100,000 takes about the same time.

### Numbers you can check

Comparisons are exact and you can verify them with the formula. The times were measured with Python 3.13 on an Apple M4 Pro laptop, looking up the last item, which is the worst case for the list. Your times will differ. The shape won't.

| Records `n` | List: average comparisons, item present `(n+1)/2` | List: comparisons, item missing `n` | List: time, last item | Dict: time |
|---|---|---|---|---|
| 10 | 5.5 | 10 | 0.28 µs | 23 ns |
| 100 | 50.5 | 100 | 2.25 µs | 22 ns |
| 1,000 | 500.5 | 1,000 | 24 µs | 23 ns |
| 10,000 | 5,000.5 | 10,000 | 260 µs | 24 ns |
| 100,000 | 50,000.5 | 100,000 | 2,658 µs | 24 ns |

The list column grows ten times each row. The dictionary column doesn't move. At 60 frames per second a frame lasts about 16,700 µs, so a single worst-case list lookup in a 100,000-record table uses about 16% of a frame. Do that for every item on screen and the game stutters. The dictionary lookup uses about 0.0001%.

To time it on your own machine, build both structures with `n` made-up records and look up the last one:

```python
import timeit

n = 10_000
items = [{"id": f"item_{i}"} for i in range(n)]
db = {f"item_{i}": {} for i in range(n)}
last = f"item_{n - 1}"

t_list = timeit.timeit(lambda: find_in_list(items, last), number=1_000) / 1_000
t_dict = timeit.timeit(lambda: db[last], number=100_000) / 100_000
print(f"list {t_list * 1e6:.1f} us, dict {t_dict * 1e9:.0f} ns")
```

For a 30-item text adventure, both are instant. Speed is a reason to prefer dictionaries that grows with your game. The next reason matters from the first day.

Now the stability view. Take a five-item list where the ID is `256 + index`. The starting number copies the pre-1.13 scheme, which began item IDs at 256.

| Index | ID | Item, before | Item, after inserting "copper shovel" at index 1 |
|---|---|---|---|
| 0 | 256 | iron shovel | iron shovel |
| 1 | 257 | iron pickaxe | **copper shovel** |
| 2 | 258 | iron axe | iron pickaxe |
| 3 | 259 | flint and steel | iron axe |
| 4 | 260 | apple | flint and steel |
| 5 | 261 | — | apple |

A save file that says "slot 3 holds item 259" held flint and steel yesterday and an iron axe today. Four of the five old items changed ID, and every save file, every command block and every mod that wrote a number now points at the wrong thing. With string keys, the save says `"flint_and_steel"`, and inserting `"copper_shovel"` anywhere changes nothing that already existed.

Old Minecraft survived with numbers because its developers only ever appended new IDs and never reused or reordered old ones. That discipline works, but it's a rule every future programmer must remember, and the compiler won't remind them. A string key makes the rule unnecessary.

### Move it

Open the interactive. The left view is a lookup race. Drag the slider for `n` from 10 to 100,000 (logarithmic) and pick which item to find. Three bars compare the cost. "List, this lookup" and "List, average (n+1)/2" grow with the number of comparisons; "Dictionary" stays at one hash plus about one comparison. Set the target to "missing item" to see the list at its worst, `n` comparisons.

The right view is a tiny item table and a save file with three slots. Press "Insert copper shovel at position 1" with the ID scheme set to "ID = 256 + position". Watch the save file's slots change meaning while its numbers stay the same. Press "Reset", switch the scheme to "ID = string key" and insert again. The save file doesn't flinch.

The insight to leave with: **a list makes you pay for a lookup with a search, and makes an item's identity depend on its neighbours. A dictionary does neither.**

### The same idea in other games

**Minecraft's old variant numbers were a compound key.** `35:14` means "item 35, variant 14." In Python that is a tuple key.

```python
OLD_BLOCKS = {(35, 0): "white wool", (35, 14): "red wool", (5, 0): "oak planks"}
OLD_BLOCKS[(35, 14)]            # "red wool"

NEW_BLOCKS = {"minecraft:red_wool": {...}, "minecraft:oak_planks": {...}}
```

Tuples work as keys because they're immutable. The Flattening replaced the tuple with a single readable string, so the key alone says what the thing is.

**World of Warcraft keeps numeric item IDs, and they're sparse.** The Hearthstone, the item every character starts with, is item 6948 in Classic WoW, and fan databases like Wowhead use that number in the item's web address. A list indexed by that number would need 6,949 positions before the Hearthstone, most of them unused. A dictionary keyed by integer stores only the items that exist.

```python
WOW_ITEMS = {6948: {"name": "Hearthstone"}}      # int keys, no gaps to fill
```

This is the other half of the lesson. Numbers aren't the problem. Positions are. WoW's IDs are keys that never change meaning, so they're safe. Old Minecraft's were also keys in practice, kept safe by never reordering. The danger is only when the number is where the thing sits in a list.

**Save files and data files everywhere.** JSON, the format you'll use in section 3 and in the lab, has only one kind of key: a string. Any tool that reads your item file, whether a Python script, a web page or a game engine, gets a table of string keys. Designing your keys as readable strings from the start means the data file, the save file and the code all use the same names. When you move to Godot in [week 7](w07-engine-intro-scenes-nodes-scripts.md), you'll look items up by these same keys.

| Context | Key type | Example key | Stable if you add items? |
|---|---|---|---|
| Minecraft Java before 1.13 | int, or (int, int) | `276`, `(35, 14)` | yes, only because IDs were never reordered |
| Minecraft Java 1.13 on | namespaced string | `"minecraft:diamond_sword"` | yes, by design |
| Classic World of Warcraft | int (sparse) | `6948` | yes, by design |
| A list where ID = index | position | `3` | no |

### Design judgment

- **Choose keys a human can read.** `"iron_sword"` in a save file or a bug report tells you what's wrong. `276` sends you to a lookup table. Readable keys cost a few bytes each, which nothing in this course will notice.
- **Never reuse or rename a key once it ships.** Players' save files, other people's mods and your own quest scripts will refer to it. If you must rename, keep the old key as an alias that maps to the new one, and convert old saves when they load.
- **Numbers are fine when you need them.** Network messages and tight save formats sometimes want small integers. Keep a dictionary from string key to number, generated once, and never let the number be a list position.
- **One source of truth.** Store every item once in the database, keyed by ID, and refer to it everywhere else by key. An inventory slot should hold `("iron_sword", 1)`, not a full copy of the sword's stats. Otherwise a balance patch changes the database and leaves thousands of stale copies in players' bags.

## 3. Building a real item database

### A dictionary of dictionaries

Each item is a record with several fields. A dictionary is a good record too, so the database is a dictionary whose values are dictionaries.

```python
ITEM_DB = {
    "wooden_sword": {"name": "Wooden Sword", "type": "weapon", "damage": 4, "stack": 1, "price": 10},
    "iron_sword":   {"name": "Iron Sword",   "type": "weapon", "damage": 6, "stack": 1, "price": 60},
    "potion":       {"name": "Potion",       "type": "consumable", "heal": 12, "stack": 16, "price": 15},
    "arrow":        {"name": "Arrow",        "type": "ammo", "stack": 64, "price": 1},
}

ITEM_DB["iron_sword"]["damage"]        # 6
ITEM_DB["potion"].get("damage", 0)     # 0: potions have no damage field
```

Read `ITEM_DB["iron_sword"]["damage"]` left to right: find the sword's record, then find the damage in it. Notice that records don't all have the same fields. A potion has `heal`, a sword has `damage`. That's normal for game data, and `.get` with a default is how you read an optional field.

Now week 5's inventory gets simpler. `add_item` no longer needs a `stack_size` argument, because it can look it up: `stack_size = ITEM_DB[item]["stack"]`. The inventory stores keys; the database stores facts about them.

### Loading from a file

Item data belongs in a data file, not in code, so a designer can edit prices without touching Python. **JSON** (JavaScript Object Notation) is a text format that maps almost exactly onto Python dictionaries and lists.

`items.json`:

```json
{
  "wooden_sword": {"name": "Wooden Sword", "type": "weapon", "damage": 4, "stack": 1, "price": 10},
  "potion":       {"name": "Potion", "type": "consumable", "heal": 12, "stack": 16, "price": 15}
}
```

```python
import json

def load_items(path):
    with open(path) as f:
        return json.load(f)

ITEM_DB = load_items("items.json")
```

JSON has only a few types: objects (become `dict`), arrays (become `list`), strings, numbers, `true`/`false` and `null` (become `True`, `False`, `None`). Its keys are always strings. That suits the "readable key" advice perfectly.

### Validating the data

A data file can be wrong in ways Python won't notice until a player equips the broken item. Write a function that checks the whole database when the game starts.

```python
REQUIRED = ["name", "type", "stack", "price"]

def validate(db):
    """Return a list of problems. An empty list means the data is fine."""
    problems = []
    for key, record in db.items():
        for field in REQUIRED:
            if field not in record:
                problems.append(f"{key}: missing {field}")
        if record.get("stack", 1) < 1:
            problems.append(f"{key}: stack must be at least 1")
        if record.get("type") == "weapon" and "damage" not in record:
            problems.append(f"{key}: weapon without damage")
    return problems
```

This is week 4's decomposition again. `validate` is pure: data in, list of problems out. You can test it with a small bad dictionary without opening a file.

### Querying: building views from the database

The database is keyed by ID, but sometimes you need a different question answered: "all weapons," "everything under 20 gold." Loop and filter. A **dictionary comprehension** is the dictionary version of week 5's list comprehension.

```python
weapons = {k: v for k, v in ITEM_DB.items() if v["type"] == "weapon"}
cheap = [k for k, v in ITEM_DB.items() if v["price"] < 20]     # ['potion', 'arrow']
```

These scans are fine when they run once, for a shop screen. If your game asks "all weapons" every frame, build the `weapons` dictionary once at load time and keep it.

### Choosing between a list and a dictionary

| Question you ask most | Use |
|---|---|
| "What is at position 3?" or "what comes next?" | list |
| "What is the record for `iron_sword`?" | dictionary |
| "How many of each?" | dictionary `{key: count}` |
| "In what order did these happen?" | list |
| Fixed slots that the player arranges by hand | list of slots holding keys |

Week 5's slot inventory stays a list, because the player cares where things are. But each slot holds a key into the item database, not a copy of the item.

## In-class activity (25 minutes)

In groups of three. Materials: a laptop, the `ITEM_DB` from section 3, and the `validate` function.

1. (8 min) Extend `ITEM_DB` to eight items for a small fantasy shop. Include one item with a deliberate data error that `validate` should catch, and one it can't catch (for example, a sword whose price is lower than a weaker sword's). Run `validate`.
2. (7 min) Write `total_value(inventory, db)` that takes a week 5 slot list like `[("potion", 3), None, ("iron_sword", 1)]` and returns the total price. Compute it by hand for that list first (it should be 105), then run it.
3. (10 min) Your game ships version 1.0 with items stored in a list where ID = index. Version 1.1 must add a "bronze sword" between the wooden and iron swords in the shop display. Write down, step by step, what breaks in players' save files, and propose a fix that doesn't require every player to start over.

Expected output: the extended database with `validate`'s output, `total_value` and its result, and a five-line migration plan for step 3.

## Common misconceptions

- **"A dictionary is just a list with names."** A list finds by position or by searching; a dictionary finds by key without searching. They answer different questions, and the cost difference grows with size.
- **"Use `.get` everywhere so the game never crashes."** Hiding a missing key turns a clear `KeyError` at startup into a wrong number in play. Use `.get` only where missing has a real meaning.
- **"Numeric IDs are the problem."** Positions are the problem. A number that is a permanent key (WoW's 6948) is as stable as a string. It's only less readable.
- **"Dictionaries are always sorted."** They keep insertion order, which isn't sorted order, and rules shouldn't depend on it. Use `sorted(db)` when you need an order.

## Check yourself

1. A list database has 2,400 items. On average, how many comparisons does `find_in_list` need for an item that exists? For one that doesn't? How many does a dictionary need, roughly?
2. What does this print?

```python
stock = {"arrow": 50, "potion": 3}
stock["potion"] = stock.get("potion", 0) - 1
stock["bomb"] = stock.get("bomb", 0) + 2
print(stock)
```

3. An items list uses `ID = 100 + index` for 40 items. A designer removes the item at index 10. How many existing items change ID? What is the ID of the item that used to be 125?
4. Why can `(35, 14)` be a dictionary key but `[35, 14]` cannot? What would go wrong if lists were allowed?
5. Write one line that builds `{item_id: price}` for every item in `ITEM_DB` whose `type` is `"consumable"`.

<details>
<summary>Answers</summary>

1. Present: `(2,400 + 1) / 2 = 1,200.5` comparisons on average. Missing: 2,400. A dictionary needs about one hash and about one comparison, whatever the size.
2. `{'arrow': 50, 'potion': 2, 'bomb': 2}`. The potion count drops from 3 to 2. `bomb` didn't exist, so `.get` gives 0 and the result is 2.
3. The items at indexes 11 to 39 each shift down by one, so 29 items change ID. The item that was 125 (index 25) moves to index 24, so its ID becomes 124.
4. Tuples are immutable, so their hash never changes. If you could change a list after using it as a key, its hash would change, and the dictionary would look in the wrong place and fail to find the entry.
5. `{k: v["price"] for k, v in ITEM_DB.items() if v["type"] == "consumable"}`

</details>

## Lab / assignment hook

[Lab 06, the item database](../labs/lab06.md). Load a provided `items.json`, write `validate`, `find`, `items_of_type` and `total_value`, make the tests pass, fix the three data errors the tests expose, then migrate an old save file that used list positions to string keys. Deliverable: the module with passing tests and the migrated save file.

## Sources

- Minecraft Wiki, "Java Edition data values/Pre-flattening" and "Pre-flattening/Item IDs" (Java Edition before 1.13). Item IDs start at 256 to separate them from block IDs; iron shovel 256, apple 260, bow 261, diamond sword 276; data values for variants such as wool colours (`35:14` for red wool); the change happened in snapshot 17w47a.
- Minecraft Wiki, "Java Edition 1.13/Flattening" (Java Edition 1.13, 18 July 2018). Numeric IDs removed in favour of namespaced resource locations such as `minecraft:stone`; variants such as planks split into separate IDs like `oak_planks`.
- Wowhead, "Hearthstone" (Classic World of Warcraft), item 6948. https://www.wowhead.com/classic/item=6948/hearthstone
- Python Wiki, "TimeComplexity". Dictionary get-item has constant average cost; list `x in s` is linear. https://wiki.python.org/moin/TimeComplexity
- Python Software Foundation, *The Python Tutorial*, sections 5.5 "Dictionaries" and 7.2.2 "Saving structured data with json"; *What's New in Python 3.7* (dictionaries keep insertion order as a language guarantee).
- Timing table: measured by the lecturer with `timeit`, Python 3.13.5, Apple M4 Pro, September 2026. Reproduce with the `timeit` snippet in section 2.

## Interactive spec: examples/w06-ids-vs-keys.html

**Purpose.** Make two things visible at once: list lookup cost grows with `n` while dictionary lookup does not, and position-based IDs change meaning when you insert an item while key-based IDs don't.

**Layout.** Two panels, side by side on desktop, stacked on mobile.

**Left panel: lookup race.**
- Slider `n`, logarithmic, positions 10, 30, 100, 300, 1,000, 3,000, 10,000, 30,000, 100,000 (keyboard arrows step between them). Default 1,000.
- Radio "Target": `first item`, `middle item`, `last item`, `random item` (re-rolls on each press of "Look up"), `missing item`.
- Three horizontal bars on a shared **logarithmic** axis from 1 to 100,000 comparisons: "List, this lookup", "List, average `(n+1)/2`", "Dictionary". The dictionary bar is fixed at 1 comparison (label: "1 hash + ~1 comparison"). Exact numbers printed at the end of each bar.
- Toggle "linear axis": switching to a linear axis makes the dictionary bar a sliver, which is the point; a caption says so.
- Below: a small line chart of comparisons vs `n` (log-log), list average as a line, dictionary as a flat line, current `n` marked with a dot.
- Formulas: list comparisons = target index + 1 (first = 1, middle = `floor(n/2) + 1`, last = `n`), missing = `n`, average = `(n + 1) / 2`. Dictionary = 1.
- A static note under the chart repeats the lecture's measured times (10: 0.28 µs vs 23 ns; 100,000: 2,658 µs vs 24 ns) labelled "measured, Python 3.13, one laptop". Do not measure in the browser.

**Right panel: IDs vs keys.**
- Mode toggle: `ID = 256 + position` (default) or `ID = string key`.
- An item table with columns Position, ID, Item. Start state: iron shovel, iron pickaxe, iron axe, flint and steel, apple (positions 0-4, IDs 256-260 in position mode; keys `iron_shovel`, `iron_pickaxe`, `iron_axe`, `flint_and_steel`, `apple` in key mode).
- A "save file" box with three slots that store IDs only: slot A = 259 / `flint_and_steel`, slot B = 260 / `apple`, slot C = 256 / `iron_shovel`. Next to each, the item the ID currently resolves to.
- Buttons: "Insert copper shovel at position 1", "Remove item at position 1", "Reset".
- After insert in position mode: table becomes iron shovel 256, copper shovel 257, iron pickaxe 258, iron axe 259, flint and steel 260, apple 261. Save resolves A = 259 to **iron axe** (was flint and steel), B = 260 to **flint and steel** (was apple), C = 256 to iron shovel (unchanged). Changed resolutions are highlighted with a warning style and the text "4 of 5 old items changed ID".
- After insert in key mode: table order changes the same way, but every save slot resolves to the same item as before; message "0 items changed ID".
- After remove at position 1 (from the start state) in position mode: iron axe 257, flint and steel 258, apple 259; save A = 259 resolves to apple, B = 260 resolves to "(nothing)" in an error style.

**The one insight.** First screen: the left panel at `n = 1,000` shows 500.5 vs 1 on a log axis, and the right panel's insert button is the only highlighted control. One click shows the save file pointing at the wrong items.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css` inline. Bars have text values, not colour alone. Changed save-slot rows use an icon-free text label ("changed") as well as colour. All controls keyboard operable; highlight transitions disabled under `prefers-reduced-motion`. Item names are generic text; no Minecraft or WoW art.
