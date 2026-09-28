# CS102 · Week 13 — Data-Driven Design: Stats in JSON and CSV

**Why this matters:** Every number a designer wants to tune will be tuned dozens of times before launch. If that number sits inside your code, each change costs a programmer, a rebuild and a restart. If it sits in a data file, the designer changes it alone and sees the result in seconds. The price is a new kind of bug, the bad row, and this week you learn to catch it at the door.

**You will be able to:**
- Load a CSV table and a nested JSON file into typed Python objects keyed by id.
- Write a validator that reports every bad row with its line number before the game starts.
- Decide, for a given piece of game content, whether it belongs in code, a flat table or a nested document.
- Compute how much faster a tuning loop becomes when numbers move from code to data, and reload a table safely while the game runs.

**Before class:** Nystrom, *Game Programming Patterns* (2014), the "Type Object" chapter (gameprogrammingpatterns.com). Python documentation, the `csv` module (read `DictReader`) and the `json` module (read `load` and `loads`). Skim the Minecraft Wiki page "Loot table", sections "Definition" and "Tags".

**Prerequisites from earlier courses:** Dictionaries as item databases, [CS101 week 6](../../CS101-programming-for-games-i/lectures/w06-dictionaries-item-databases.md). Lists and loops over rows, [CS101 week 5, arrays and lists](../../CS101-programming-for-games-i/lectures/w05-arrays-and-lists-inventories.md). Functions with one job and boundary tests, [CS101 week 4, functions and decomposition](../../CS101-programming-for-games-i/lectures/w04-functions-and-decomposition.md). From this course, classes and dataclasses ([week 1](w01-classes-objects-encapsulation.md)), composition ([week 2](w02-inheritance-vs-composition.md)), and hash-map lookup cost ([weeks 4](w04-big-o-intuition-for-game-developers.md) and [5](w05-arrays-linked-lists-and-hash-maps.md)). Weighted loot tables, [MA102 week 9](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w09-weighted-tables-and-loot-table-design.md). One source of truth per number, [GD102 week 13, systems documentation](../../GD102-systems-design-and-game-mechanics/lectures/w13-systems-documentation.md).

**Interactive:** [Edit the table](../examples/w13-edit-the-table.html). Keep it open during section 2.

---

## 1. The number that lives in the wrong place

Here is how a first-year programmer usually writes a weapon.

```python
class LongSword:
    def roll_damage(self, rng):
        return rng.randint(3, 19)

    def attacks_per_sec(self):
        return 1.2
```

It works. Then the designer plays it and says the Long Sword feels weak, could the top end be 25? You open the file, change 19 to 25, save, restart the game, walk back to the training dummy and swing. The designer says 25 is too much, try 22. Again.

Nystrom describes this exact day in the "Type Object" chapter: a programmer who spends the day receiving emails that say "change the troll's health from 48 to 52," editing a class, recompiling, checking in and replying. He calls it turning into a data monkey. The designer is unhappy too, because every small idea waits on someone else.

The problem is not the class. The problem is that two different things are mixed in it.

- A **rule** is how the game computes something. "Damage is a random whole number between the weapon's minimum and maximum." Rules change rarely, and a change needs a programmer and a test.
- A **number** is a parameter that a rule uses. "The Long Sword's maximum is 19." Numbers change constantly during tuning, and a change needs a designer and a playtest.

**Data-driven design** means keeping rules in code and numbers (and content: names, lists of items, which monster drops what) in data files that the game reads at startup. The code then describes weapons in general, and a file describes each particular weapon.

### What a tuning change costs

Put numbers on the loop. One tuning iteration is the time from "I want to try 22" to "I have seen 22 in the game":

```
T = t_edit + t_build + t_restart + t_reach + t_observe
tweaks per hour = 60 / T        (T in minutes)
```

- `t_edit` is the time to make the change.
- `t_build` is the time to recompile. Zero if nothing is compiled.
- `t_restart` is the time to relaunch the game.
- `t_reach` is the time to get back to the situation you are testing (walk to the dummy, reload the save).
- `t_observe` is the time to actually play and judge.

The timings below are illustrative. Measure your own project; the shape of the result is what matters.

| Setup | edit | build | restart | reach | observe | T (min) | Tweaks per hour |
|---|---|---|---|---|---|---|---|
| Number in compiled code | 0.5 | 3 | 1 | 1.5 | 1 | 7.0 | 8.6 |
| Number in a data file, restart to see it | 0.5 | 0 | 1 | 1.5 | 1 | 4.0 | 15 |
| Number in a data file, reloaded while running | 0.5 | 0 | 0 | 0 | 1 | 1.5 | 40 |

Moving the number out of code nearly doubles the loop rate. Reloading it while the game runs (section 5) multiplies it by about 4.7 over the original, because the two biggest costs, getting back to the test situation and rebuilding, disappear. A designer with 40 tries per hour tunes by feel. A designer with 9 tries per hour tunes by guessing, because each try is too expensive to waste.

## 2. Worked example: Diablo II's weapon table

### The hook

Diablo II: Resurrected (2021) keeps its item, monster and skill definitions as tab-separated text tables inside its game archive, and the fan project blizzhackers/d2data publishes them after each patch. The weapons table has 306 rows. Each row is one weapon base: a name, a three-letter code, a type, minimum and maximum damage, a speed modifier, strength and dexterity requirements, and more than a hundred other columns.

Here are four rows from the May 2026 extraction, trimmed to the columns we need. Blank cells are blank in the file too.

| name | code | type | mindam | maxdam | speed | reqstr | ubercode |
|---|---|---|---|---|---|---|---|
| Short Sword | ssd | swor | 2 | 7 | | | 9ss |
| Scimitar | scm | swor | 2 | 6 | -20 | | 9sm |
| Long Sword | lsd | swor | 3 | 19 | -10 | 55 | 9ls |
| Gladius | 9ss | swor | 8 | 22 | | 25 | 9ss |

Look at what is and is not in there. The Short Sword and the Gladius differ only in their numbers. There is no `class Gladius` anywhere; the Gladius is a row. The `ubercode` column says "the stronger version of the Short Sword is the row with code `9ss`," which is the Gladius. The `type` column holds `swor`, which is itself a key into a second table, `itemtypes.txt`, where `swor` is defined as "Sword." Rows point at other rows by id, across files.

That is the whole idea of this lecture, shipped in a game people have played for 25 years: the code knows what a weapon *is*, and a table says what each weapon *has*.

### The model

We now build the same structure for our own game. We keep Diablo II's idea and simplify the columns. Our game does not use Diablo II's attack-speed frame system, so instead of a `speed` modifier we store attacks per second directly.

```
table   = { id: Weapon, ... }          loaded once, at startup
weapon  = table[id]                     every lookup is by id
avg_hit = (min_dmg + max_dmg) / 2
dps     = avg_hit × attacks_per_sec
```

- `id` is a short, stable, lowercase name like `long_sword`. Code and other files refer to weapons only by id, never by position in the file.
- `Weapon` is a class with one field per column. Its fields hold numbers, not behaviour.
- `table` is a dictionary from id to `Weapon`. Week 5 showed why: a lookup by key in a hash map costs the same whether the table has 5 rows or 5,000.
- `min_dmg`, `max_dmg` are the damage range for one hit. `attacks_per_sec` is how many hits per second.
- `avg_hit` and `dps` are the rule. They live in code, once, and apply to every row.

The loader has three steps, and the order matters: **parse** each row from text into typed values, **validate** every row and every reference, then **index** the rows by id. Only a table that passes all three reaches the game.

### The code

Our data file, `weapons.csv`:

```
id,name,type,min_dmg,max_dmg,attacks_per_sec,req_str,upgrade
short_sword,Short Sword,sword,2,7,1.5,0,gladius
gladius,Gladius,sword,8,22,1.5,25,
long_sword,Long Sword,sword,3,19,1.2,55,
hand_axe,Hand Axe,axe,3,6,1.6,0,
war_hammer,War Hammer,mace,10,20,0.8,60,
```

The loader, `weapons_loader.py`. Read it top to bottom once; each function has one job.

```python
import csv
from dataclasses import dataclass

VALID_TYPES = {"sword", "axe", "mace", "knife"}

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
    text = row[key].strip()
    if text == "" and default is not None:
        return default
    try:
        return kind(text)
    except ValueError:
        raise ValueError(f"{key}: '{text}' is not a valid {kind.__name__}") from None

def parse_row(row, line, errors):
    """Turn one dict of strings into a Weapon, or record errors and return None."""
    try:
        w = Weapon(
            id=row["id"].strip(),
            name=row["name"].strip(),
            type=row["type"].strip(),
            min_dmg=number(row, "min_dmg", int),
            max_dmg=number(row, "max_dmg", int),
            attacks_per_sec=number(row, "attacks_per_sec", float),
            req_str=number(row, "req_str", int, default=0),
            upgrade=row["upgrade"].strip() or None,
        )
    except ValueError as e:
        errors.append(f"line {line}: {e}")
        return None
    if w.type not in VALID_TYPES:
        errors.append(f"line {line}: unknown type '{w.type}'")
    if not 0 <= w.min_dmg <= w.max_dmg:
        errors.append(f"line {line}: need 0 <= min_dmg <= max_dmg, got {w.min_dmg}..{w.max_dmg}")
    if w.attacks_per_sec <= 0:
        errors.append(f"line {line}: attacks_per_sec must be > 0")
    return w

def load_weapons(path):
    errors, table = [], {}
    with open(path, newline="") as f:
        for line, row in enumerate(csv.DictReader(f), start=2):
            w = parse_row(row, line, errors)
            if w is None:
                continue
            if w.id in table:
                errors.append(f"line {line}: duplicate id '{w.id}'")
            else:
                table[w.id] = w
    for w in table.values():
        if w.upgrade is not None and w.upgrade not in table:
            errors.append(f"{w.id}: upgrade '{w.upgrade}' is not a weapon id")
    if errors:
        raise ValueError(f"{path}: {len(errors)} problem(s)\n  " + "\n  ".join(errors))
    return table

def average_hit(w):
    return (w.min_dmg + w.max_dmg) / 2

def dps(w):
    return average_hit(w) * w.attacks_per_sec
```

A few details deserve a sentence each.

- `csv.DictReader` turns each line into a dictionary from column name to **string**. CSV has no types. `"7"` is text until you convert it, which is why `number` exists.
- `enumerate(..., start=2)` gives each row its line number in the file. Line 1 is the header. A designer who reads "line 4" can open the file and go straight there.
- `frozen=True` makes a `Weapon` read-only after loading. Game code can read a weapon's numbers but cannot change the shared definition by accident. If a sword gets an enchantment, that belongs to the *item instance*, a separate object that points at the definition (Nystrom's Type Object pattern: the row is the type, the thing in your inventory is the object).
- `errors` is a list, and the loader keeps going after a problem. A designer who made five mistakes should see five messages in one run, not fix one, restart, and meet the next.
- The reference check for `upgrade` runs after every row is loaded, because a row may point at a weapon further down the file.

### Numbers you can check

Run `load_weapons("weapons.csv")` and print `average_hit` and `dps` for each row.

| id | min_dmg | max_dmg | attacks_per_sec | avg_hit | dps |
|---|---|---|---|---|---|
| short_sword | 2 | 7 | 1.5 | 4.5 | 6.75 |
| gladius | 8 | 22 | 1.5 | 15.0 | 22.50 |
| long_sword | 3 | 19 | 1.2 | 11.0 | 13.20 |
| hand_axe | 3 | 6 | 1.6 | 4.5 | 7.20 |
| war_hammer | 10 | 20 | 0.8 | 15.0 | 12.00 |

Check one by hand. Long Sword: `(3 + 19) / 2 = 11`, and `11 × 1.2 = 13.2`. Notice that the War Hammer hits as hard as the Gladius on average but has barely half its DPS, because it swings at 0.8 per second instead of 1.5.

Now do what the designer asked. Change one cell, the Long Sword's `max_dmg`, from 19 to 25. Do not touch the Python file. Run again.

| id | max_dmg | avg_hit | dps |
|---|---|---|---|
| long_sword (before) | 19 | 11.0 | 13.20 |
| long_sword (after) | 25 | 14.0 | 16.80 |

One cell moved, one row's output moved, and nothing else in the game changed. The rule `dps = avg_hit × attacks_per_sec` was written once and was never edited.

### What the validator buys you

Here is a file with five mistakes of the kind designers really make: a letter O typed for a zero, two numbers swapped, a misspelled type, a pasted row that duplicates an id, and a misspelled reference.

```
id,name,type,min_dmg,max_dmg,attacks_per_sec,req_str,upgrade
short_sword,Short Sword,sword,2,7,1.5,0,gladus
dagger,Dagger,knife,1,4O,2.0,0,
club,Club,mace,6,1,1.4,0,
long_sword,Long Sword,sowrd,3,19,1.2,55,
short_sword,Short Sword,sword,2,7,1.5,0,
```

Our loader refuses to start and prints:

```
broken.csv: 5 problem(s)
  line 3: max_dmg: '4O' is not a valid int
  line 4: need 0 <= min_dmg <= max_dmg, got 6..1
  line 5: unknown type 'sowrd'
  line 6: duplicate id 'short_sword'
  short_sword: upgrade 'gladus' is not a weapon id
```

Compare that with a naive loader that just calls `int()` on each cell and stores rows in a dictionary. When would each mistake show up?

| Mistake | Naive loader | Validating loader |
|---|---|---|
| `4O` for 40 | Crashes at load with `invalid literal for int() with base 10: '4O'`, no file line | Line 3, at load |
| min 6, max 1 | Loads fine. Crashes on the Club's first swing: `random.randint(6, 1)` raises `ValueError: empty range in randrange(6, 2)`, because `randint(a, b)` calls `randrange(a, b + 1)` | Line 4, at load |
| type `sowrd` | Never crashes. Every sword-type bonus silently skips the Long Sword | Line 5, at load |
| duplicate `short_sword` | Never crashes. The second row silently replaces the first, and its upgrade link is gone | Line 6, at load |
| upgrade `gladus` | In this file, never: the duplicate row on line 6 replaced the row that held the typo. On its own, it crashes with `KeyError: 'gladus'` the first time a player upgrades a Short Sword, maybe hours into a session | At load |

The first row is the only one the naive version catches early, and only because Python's `int()` happens to be strict. The swapped range crashes later, in the middle of play, far from its cause. The misspelled type and the duplicate never crash at all; they just make the game quietly wrong, and someone files a balance complaint a month later. The bad upgrade is worse still. One mistake, the duplicate, hid another, so this file shows no upgrade crash until someone deletes the duplicate row and the old `KeyError` comes back. The validator moves all five to the one moment when the person who made the mistake is still looking at the file.

### Move it

Open the interactive. The left view is the CSV text, editable. The right view is the game's view of it: a bar per weapon showing DPS, with the numbers beside it. Change the Long Sword's 19 to 25 and watch one bar grow while the Python source, shown collapsed under the chart, stays unchanged.

Then type `4O` into a cell, or swap a min and max. With **validate at load** on, the chart keeps the last good table and a red panel lists the problem with its line number. Turn validation off and press **Fight** to swing every weapon once. The swap now shows up as a crash message in the combat log, attributed to the weapon, not the line. The misspelled type shows up as nothing at all, which is the scariest result on the screen. Neither does the bad upgrade, because the duplicate row replaced it.

### The same idea in other games

**Minecraft (Java Edition, loot tables since 1.9).** What a zombie drops, what a desert temple chest contains, and (since 1.14) what a mined block drops are all JSON files in a data pack, for example `data/minecraft/loot_table/entities/zombie.json`. A data pack that ships a file at that path replaces the zombie's drops for every zombie in the world, with no code. The shape is nested: a table has `pools`, each pool has `rolls` and a list of `entries`, and each entry has a `weight`. That is still our model. The game code knows what a loot table *is* (how to roll pools and pick weighted entries, the maths of MA102 week 9) and each file says what one table *has*. Items inside entries are referred to by id, like `minecraft:rotten_flesh`, exactly as our `upgrade` column refers to `gladius`.

**Factorio (2.x, prototype stage).** Every item, recipe, machine and enemy in Factorio is a *prototype* defined in a Lua table during a startup stage the documentation calls the data or prototype stage. Mods add or change prototypes by running `data.lua`, `data-updates.lua` and `data-final-fixes.lua` in turn, each able to edit what the previous ones built. Only after all mods finish does the game build its real objects. The documentation says that missing properties either fall back to a default or give an error, and that extra properties the game is not looking for are ignored. Read that last clause again with our validator in mind. A modder who misspells a property name gets no error; the misspelled key is dropped and the default applies. That is our `sowrd` row, in a shipped engine, made on purpose so that mods written for one version keep loading in the next.

**Godot 4 (the client engine for this program).** Godot's answer is the **Resource**: a script that extends `Resource` with `@export` fields, saved as a text `.tres` file and edited in the Inspector. The Godot 4.7 documentation lists the advantages over JSON or CSV. The file loads straight into a typed object, fields can have editor range hints, and resources can reference other resources. A `WeaponData` resource with `min_dmg`, `max_dmg` and `attacks_per_sec` is our `Weapon` dataclass, with the engine doing parsing and some validation for you.

Four systems, four file formats, one split. Rules in code, written once. Numbers and content in data, keyed by id, loaded before play. When you meet a new engine or mod system, ask three questions. Where is the table? What is the id? What happens to a misspelled key?

### Design judgment

Moving numbers into data is almost always right for content (items, monsters, spells, loot, dialogue) and for tuning constants. It creates decisions you should make deliberately.

- **Formulas stay in code.** When designers are happy editing numbers, someone always proposes putting the formula in the data too: a `damage_formula` column holding `"(min+max)/2*speed"`. Now you have a second, weaker programming language with no debugger, no tests and no type checks, living inside a spreadsheet. If a weapon needs a genuinely different rule, give the row a `rule` column that names one of a few rules implemented and tested in code (`"standard"`, `"charge_up"`), and validate that name like any other reference.
- **Strict or forgiving about unknown keys.** Factorio ignores unknown properties so old mods keep loading. That is right for a platform with thousands of third-party mods. For your own team's files, reject unknown columns and keys. A typo that silently does nothing costs more than a load error.
- **Required fields and defaults.** Diablo II leaves `reqstr` blank for "no requirement." Blank-means-default saves typing but hides mistakes: did the designer mean zero, or forget? Decide per column, and write the decision into the loader (our `req_str` has a default; `max_dmg` does not).
- **Ids are forever.** Save files, other tables and network messages store ids. Rename "Long Sword" to "Longsword" in the `name` column freely. Never rename `long_sword`, or every save that holds one breaks. Week 14's tests can check that no id disappears between versions.
- **Load once, not per frame.** Parsing text is slow compared with a dictionary lookup. Parse and validate at startup (or on reload), then the game reads only the finished `table`. A game that reads `weapons.csv` inside its update loop will show up in the profiler immediately.

## 3. CSV or JSON: pick by the shape of the data

Both formats are plain text, both work with version control, both load in two lines of Python. Choose by the shape of what you are storing.

**CSV (comma-separated values)** is a table: every row has the same columns. It is the right choice when your content is a list of things with the same fields, like weapons, monsters or level-up thresholds. Designers can edit it in any spreadsheet program, sort it, and add a column of formulas beside it for their own checks, as in [GD102 week 14](../../GD102-systems-design-and-game-mechanics/lectures/w14-tuning-with-spreadsheets.md). Its weaknesses:

- Every cell is a string. You must convert and check types yourself.
- Nesting is awkward. A weapon with a list of three on-hit effects either needs three columns (`effect1`, `effect2`, `effect3`, mostly blank), a second table keyed by weapon id, or a string you split, like `"burn;slow"`.
- Spreadsheet programs "help." Depending on the program and locale, a cell containing `1-2` may be turned into a date, `007` into `7`, and `1.5` saved as `1,5`. Save as CSV from the spreadsheet, then let the validator catch what the program changed.

**JSON (JavaScript Object Notation)** is a tree of objects (key-value maps), arrays (lists), strings, numbers, booleans and `null`. It is the right choice when entries have different shapes or contain lists, like loot tables, dialogue trees and quests. Numbers are numbers and strings are strings after parsing, so you get basic types for free. Its weaknesses:

- No comments in standard JSON, so designers cannot annotate why a value is what it is.
- One misplaced comma breaks the whole file. Python's `json.loads('{"a": 1,}')` fails with `Illegal trailing comma before end of object: line 1 column 8`. At least it gives a position.
- Large nested files are hard to review in a diff, and two designers editing the same file conflict more often than two designers editing different rows of a CSV.

Here is a small loot table in JSON, shaped like Minecraft's, for the goblin in our game.

```json
{
  "id": "goblin",
  "pools": [
    {
      "rolls": 1,
      "entries": [
        {"item": "gold", "weight": 60},
        {"item": "short_sword", "weight": 30},
        {"item": "nothing", "weight": 10}
      ]
    }
  ]
}
```

Loading and validating it, with a cross-file check against the weapons table:

```python
import json

SPECIAL_ITEMS = {"gold", "nothing"}

def load_loot(path, weapons):
    with open(path) as f:
        data = json.load(f)
    errors = []
    for p, pool in enumerate(data.get("pools", [])):
        if not isinstance(pool.get("rolls"), int) or pool["rolls"] < 1:
            errors.append(f"pools[{p}].rolls must be a whole number >= 1")
        total = 0
        for e, entry in enumerate(pool.get("entries", [])):
            where = f"pools[{p}].entries[{e}]"
            item, weight = entry.get("item"), entry.get("weight")
            if item not in weapons and item not in SPECIAL_ITEMS:
                errors.append(f"{where}: unknown item '{item}'")
            if not isinstance(weight, int) or weight <= 0:
                errors.append(f"{where}: weight must be a whole number > 0")
            else:
                total += weight
        if total == 0:
            errors.append(f"pools[{p}] has no valid entries")
    if errors:
        raise ValueError(f"{path}: " + "; ".join(errors))
    return data
```

JSON has no line numbers after parsing, so the error names a **path** into the tree instead: `pools[0].entries[1]`. That is just as precise for a designer, as long as you print it. The goblin's short sword chance is `30 / (60 + 30 + 10) = 30%`, by the weight rule from MA102 week 9. Rename `short_sword` in the weapons file and this loader fails at startup with `unknown item 'short_sword'`, instead of the goblin dropping nothing forever.

A rule of thumb. If you would draw it as a grid, use CSV. If you would draw it as boxes inside boxes, use JSON. If it is both (a list of monsters, each with a nested loot table), keep the grid in CSV and point from each row to a JSON file by id.

## 4. Validation: fail early, fail loudly, say where

Section 2's validator checks five kinds of problem. Every data loader you write should check all five, and they come in a natural order.

1. **Syntax.** Can the file be parsed at all? A JSON trailing comma, a CSV row with the wrong number of commas.
2. **Types.** Is `max_dmg` a whole number? Is `rolls` an integer, not the string `"1"`?
3. **Ranges and relations inside a row.** `min_dmg ≤ max_dmg`, `attacks_per_sec > 0`, a probability between 0 and 1.
4. **Uniqueness.** No two rows share an id.
5. **References.** Every id mentioned (`upgrade`, a loot entry's `item`, a monster's `loot_table`) exists in the table it points at.

Three habits make validators useful rather than annoying.

**Collect, then report.** Append each problem to a list and raise once at the end. The student version of a loader raises at the first error, and the designer fixes errors one restart at a time.

**Say where, in the designer's terms.** "line 4" or `pools[0].entries[1]`, plus the column name and the bad value. Never just `KeyError: 'gladus'`, which tells a designer nothing about which file to open.

**Refuse to start on bad data.** It is tempting to skip a bad row and carry on. Do that in a shipped game with player mods, and log it. During development, refuse. A game that starts with one weapon missing will be playtested for an hour before anyone notices the missing weapon, and the playtest is wasted.

Validation also catches a class of problem that is not a typo: a design that is legal but surprising. A check like "no weapon's DPS is more than twice the median of its tier" is not a rule of the file format. It is a **sanity check** that flags rows for a human to look at. Keep these as warnings, not errors, so a designer can make an outlier on purpose.

## 5. Templates and live reload

### Rows that inherit from rows

Twelve kinds of goblin that differ only in health and name make a table full of copied cells. Nystrom's "Type Object" chapter handles this with a `parent` field: a breed names another breed, and any value it leaves out is taken from the parent. His JSON example gives a Troll Archer a `parent` of `Troll` and marks its health as inherited by writing `0`.

That `0` is worth a warning. It works in his example because no troll should have zero health. Use the same trick for `armor` and a designer can no longer make an unarmored troll, because `0` means "inherit." Use a *missing key* for "inherit" instead. Missing and zero are different in JSON and in a Python dictionary, so keep them different.

```python
def resolve(rows):
    """rows: dict id -> dict of fields, some with a 'parent' id. Returns flat dicts."""
    done = {}
    def flat(rid, seen=()):
        if rid in done:
            return done[rid]
        if rid in seen:
            raise ValueError(f"parent cycle: {' -> '.join(seen + (rid,))}")
        row = rows[rid]
        base = flat(row["parent"], seen + (rid,)) if "parent" in row else {}
        merged = {**base, **{k: v for k, v in row.items() if k != "parent"}}
        done[rid] = merged
        return merged
    for rid in rows:
        flat(rid)
    return done
```

`{**base, **own}` builds a new dictionary with the parent's values first and the child's own values on top. The `seen` tuple catches a designer who makes A the parent of B and B the parent of A, which would otherwise recurse forever. Run `resolve` before the validator, so the validator sees each row as the game will.

### Reloading while the game runs

The last row of the section 1 table, 40 tweaks per hour, needs the game to notice a changed file and reload it without restarting. The minimum version checks the file's modification time once a second.

```python
import os

class LiveTable:
    def __init__(self, path, loader):
        self.path, self.loader = path, loader
        self.table = loader(path)                 # must succeed at startup
        self.mtime = os.path.getmtime(path)

    def poll(self):
        m = os.path.getmtime(self.path)
        if m == self.mtime:
            return
        self.mtime = m
        try:
            self.table = self.loader(self.path)   # swap only if it validates
            print(f"reloaded {self.path}")
        except ValueError as e:
            print(f"kept previous {self.path}:\n{e}")
```

The important line is the `try`. A designer saves a half-typed file, the new table fails validation, and the game keeps running on the last good table while printing what is wrong. They finish typing, save again, and the new numbers appear. Live reload without validation is worse than no live reload: one half-typed save crashes the session they were tuning.

Live reload has a subtle trap. Objects created before the reload may hold a reference to an old `Weapon`. If an item instance stores the whole `Weapon` object, it keeps the old numbers until it is recreated. If it stores the weapon's *id* and looks it up in `live.table` when needed, it sees the new numbers immediately. This is one more reason to pass ids around, not copies.

## In-class activity (25 minutes)

Pairs, one laptop. Materials: `weapons_loader.py`, `weapons.csv` and `broken.csv` copied from section 2 of these notes.

1. (5 min) Run the loader on `weapons.csv`. Then bring the War Hammer's DPS as close as you can to the Gladius's (22.5) by changing **one cell**. Try `attacks_per_sec` (1.5 gives exactly 22.5) and `max_dmg` (46 gives 22.4). Write down which one keeps its slow, heavy feel and what that choice does to the size of each hit.
2. (10 min) Add a column `crit_chance` (a number from 0 to 1, default 0.05 when blank). Extend `Weapon`, `parse_row` and the validator. Add one row to `broken.csv` that breaks your new rule, and confirm the loader reports it with the right line.
3. (10 min) Swap files with the pair next to you. Try to write a row that their loader accepts but that would crash or misbehave in a fight. Report what you found.

Expected output: the changed cell and its new value, your updated loader, and one row that got past the other pair's validator (or a statement that none did, with the three attempts you made).

## Common misconceptions

- **"Data-driven means no code."** The rules are still code, and they need to be better code, because every row now depends on them. Data-driven moves the *numbers* out.
- **"If the file parses, the data is fine."** Parsing checks syntax only. `min_dmg` of 6 with `max_dmg` of 1 is valid CSV and valid JSON. Ranges, uniqueness and references need your validator.
- **"Skipping bad rows is safer than refusing to start."** During development it hides the problem until a playtest trips over the gap. Refuse to start and list every problem.
- **"JSON is better than CSV because it's more powerful."** It is better for nested shapes and worse for flat tables that designers edit in spreadsheets. Pick by shape.

## Check yourself

1. A designer wants the Hand Axe to have the same DPS as the Short Sword without changing its damage range. What `attacks_per_sec` gives that? Is the change in code or data?
2. The loot pool in section 3 gets a new entry, `{"item": "gladius", "weight": 20}`. What is the chance of a short sword per goblin kill now? What does the loader do if the entry says `"gladuis"` instead?
3. Using the section 1 model, your project's build takes 8 minutes and restart plus reaching the test takes 3 minutes. Editing and observing take 1.5 minutes together. How many tweaks per hour with numbers in code? With numbers in data and live reload?
4. In Factorio, a modder writes a property name with a typo. Using the documentation's rule, what happens, and why might the engine designers have chosen that behaviour?
5. A row uses `"armor": 0` to mean "inherit from parent." Give a design that this makes impossible and propose a fix.

<details>
<summary>Answers</summary>

1. The Short Sword's DPS is 6.75 and the Hand Axe's average hit is 4.5, so `attacks_per_sec = 6.75 / 4.5 = 1.5`. It is a one-cell change in `weapons.csv`; no code changes.
2. Total weight is `60 + 30 + 10 + 20 = 120`, so short sword chance is `30 / 120 = 25%`, down from 30%. Adding an entry changed every other entry's chance, as in MA102 week 9. With `"gladuis"`, the loader raises at startup with `pools[0].entries[3]: unknown item 'gladuis'`.
3. In code: `T = 1.5 + 8 + 3 = 12.5` minutes, so `60 / 12.5 = 4.8` tweaks per hour. Data with live reload removes build and restart-and-reach: `T = 1.5` minutes, 40 tweaks per hour, about 8.3 times as many.
4. The misspelled property is ignored and the property it was meant to set takes its default (or, if that property is required, the game reports it as missing). Ignoring unknown properties lets mods written for one version load in a later version that dropped or renamed a field, which matters for a platform with a large mod ecosystem.
5. An unarmored creature (armor 0) that has an armored parent can no longer be written, because 0 means "inherit." Use a missing key for "inherit" and let 0 mean zero, as `resolve` does.

</details>

## Lab / assignment hook

[Lab 13, a validated data loader](../labs/lab13.md). You get weapon and monster files, two broken copies of them, and a combat script that still hard-codes a Crossbow and a Skeleton as classes. Move those two into the data files, write a loader (with `parent` inheritance for monsters) that reports every problem in the broken files with a location, and add live reload that keeps the last good table. The loader becomes the data layer of the final data-driven combat module, and next week you write its tests.

## Sources

- blizzhackers, `d2data` repository, "Diablo 2 Resurrected 3.0 JSON Data", `json/weapons.json` and `json/itemtypes.json`, commit of 23 May 2026 ("Updated for newest patch"). The README states the files are the data from the `.txt` files in the D2R game archive. Rows used: Short Sword (ssd) 2-7, ubercode 9ss; Scimitar (scm) 2-6, speed -20; Long Sword (lsd) 3-19, speed -10, reqstr 55; Gladius (9ss) 8-22, reqstr 25; type `swor` defined as "Sword"; 306 weapon rows. https://github.com/blizzhackers/d2data
- Nystrom, R. (2014). *Game Programming Patterns*, "Type Object". The "change the troll's health from 48 to 52" workday, the data-monkey remark, loading breeds from JSON, and a `parent` breed with 0 used to mean "inherit." Paraphrased. https://gameprogrammingpatterns.com/type-object.html
- Minecraft Wiki, "Loot table" (Java Edition, accessed September 2026). JSON files in the data pack directory `loot_table`, the zombie example path, pools, rolls, entries and weights; introduced in 1.9 (snapshot 15w43a); block drops moved to loot tables in 1.14 (18w43a). https://minecraft.wiki/w/Loot_table
- Factorio Lua API documentation, Auxiliary Docs, "Data lifecycle" (version 2.1.20). Settings and prototype stages; `data.lua`, `data-updates.lua`, `data-final-fixes.lua`; missing properties fall back to a default or give an error; extra properties are ignored. https://lua-api.factorio.com/latest/auxiliary/data-lifecycle.html
- Godot Engine documentation (4.7, stable), "Resources", section "Creating your own resources". Resource scripts serialize to `.tres`/`.res`; comparison with JSON, CSV and TXT. https://docs.godotengine.org/en/stable/tutorials/scripting/resources.html
- Python Software Foundation, *The Python Standard Library*, `csv` (`DictReader`), `json`, `dataclasses` (`frozen=True`) and `os.path.getmtime` (Python 3.13 documentation). Error messages in the tables were produced with Python 3.13.5.

## Interactive spec: examples/w13-edit-the-table.html

**Purpose.** Make visible that a data edit changes the game with no code change, and that validation moves a bad row's failure from "mid-fight, far from the cause, or never" to "at load, with a line number."

**Layout.** Two linked views side by side at widths ≥ 900px, stacked below that (editor first).

- **Left: the data file.** A monospace `<textarea>` (with visible line numbers in a gutter; 1-based, header is line 1) pre-filled with the exact `weapons.csv` from section 2. Below it, a row of preset buttons that replace the text: "Clean table", "Long Sword max 25", "Broken file" (the exact `broken.csv` from section 2). Edits re-run the pipeline 200 ms after the last keystroke.
- **Right: the game's view.** A horizontal bar chart, one bar per weapon in table order, bar length proportional to DPS, with the exact numbers at the end of each bar: `avg 11.0 · dps 13.20`. The x-axis runs from 0 to max(25, largest DPS × 1.1). Under the chart, a collapsed `<details>` labelled "Python rule (unchanged)" showing the `average_hit` and `dps` functions, with a small counter "code edits: 0" that never changes. This counter is the point: the student sees it stay at zero while bars move.
- **Validation panel** under the editor: green "Loaded 5 weapons" or red "N problem(s)" with one list item per problem, each clickable/Enter-able to move the textarea cursor to that line.
- **Controls:** toggle "Validate at load" (default on, `aria-pressed`); button "Fight" (swings every weapon once against a dummy and writes to a combat log); a seeded RNG (mulberry32, seed 13) so the log is reproducible.

**Behaviour with validation on.** Run the pipeline exactly as `load_weapons` does: parse header; for each row (line = index + 2) convert `min_dmg`, `max_dmg`, `req_str` with a strict integer parse (`/^-?\d+$/` after trim; `req_str` blank → 0), `attacks_per_sec` with a strict float parse (`/^-?\d+(\.\d+)?$/`); check type in {sword, axe, mace, knife}; `0 ≤ min ≤ max`; `attacks_per_sec > 0`; duplicate id keeps the first row; after all rows, check each non-blank `upgrade` is an id. If any problem, **keep the last good table on the chart** (grey it slightly and show "showing last good table") and list the problems. Message text must match the Python output exactly, for example `line 3: max_dmg: '4O' is not a valid int`.

**Behaviour with validation off (naive loader).** Parse numbers with `parseInt`/`parseFloat` (so `4O` becomes 4, which is itself a lesson: show it in the chart as a normal bar), no type, range, duplicate or reference checks, later duplicate rows overwrite earlier ones. Pressing Fight: for each weapon, if `min > max` write `Club: crash, empty range in randrange(6, 2)` in red (Python's own message, since `randint(a, b)` calls `randrange(a, b + 1)`); else roll `randint(min, max)` and write `Club hits for N`. If the weapon's type is not in the valid set, write `Long Sword hits for N (no sword bonus applied)` in amber. Then, for each weapon with a non-blank upgrade not in the table, write `Short Sword: crash on upgrade, KeyError 'gladus'`. With the "Broken file" preset this line does not appear, because the later duplicate `short_sword` row, which has a blank upgrade, overwrites the row holding `gladus`. Delete line 6 and it appears.

**Test values.** Clean table: DPS 6.75, 22.50, 13.20, 7.20, 12.00. "Long Sword max 25": long_sword avg 14.0, dps 16.80, all others unchanged. "Broken file", validation on: exactly five messages in this order: `line 3: max_dmg: '4O' is not a valid int`, `line 4: need 0 <= min_dmg <= max_dmg, got 6..1`, `line 5: unknown type 'sowrd'`, `line 6: duplicate id 'short_sword'`, `short_sword: upgrade 'gladus' is not a weapon id`.

**The one insight.** A cell edit moves one bar while "code edits: 0" never changes, and the same bad file is either five precise messages at load (validation on) or a mix of mid-fight crashes and silent wrongness (validation off).

**Accessibility.** All controls keyboard operable; chart bars have text labels, not colour alone; problem list is an `aria-live="polite"` region; no animation under `prefers-reduced-motion`.
