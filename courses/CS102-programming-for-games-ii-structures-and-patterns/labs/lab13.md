# CS102 · Lab 13: A validated data loader

**Week:** 13 ([lecture](../lectures/w13-data-driven-design-stats-in-json-and-csv.md))
**Time:** 2 hours in the lab, plus up to 2 hours to finish.
**Work mode:** pairs (one keyboard, swap every 20 minutes).
**Counts toward:** labs (40% of the course grade). The loader you write here is the data layer of the final data-driven combat module, and lab 14 tests it.

## Objective

Move a combat module's weapon and monster numbers out of code and into a CSV and a JSON file. Write a loader that reports every problem in a broken file with a location a designer can act on. Add live reload that never replaces a good table with a bad one.

## Starter materials

All in [`lab13-starter/`](lab13-starter/). Standard library only, Python 3.10 or later.

- `loader.py`: the `Weapon` dataclass, the `number()` helper and `dps()` from the lecture, and five stubs to fill in: `parse_row`, `load_weapons`, `resolve`, `load_monsters` and `LiveTable.poll`. Each docstring states exactly what the checker expects.
- `weapons.csv` (6 weapons) and `monsters.json` (4 monsters, two of which inherit from `goblin`).
- `broken_weapons.csv` (7 problems) and `broken_monsters.json` (several problems, including a parent cycle). Do not fix these files. They are the test inputs.
- `combat_hardcoded.py`: a Crossbow and a Skeleton written the old way, as classes with numbers inside.
- `combat.py`: a tiny time-to-kill script that reads everything from the tables. It works once Parts A and B pass.
- `check_lab13.py`: eight checks. Run `python check_lab13.py` from inside the folder. Every check prints `TODO` until you write the function it needs, then `PASS` or `FAIL` with a reason.

## Steps

### Part A: weapons (40 min)

1. Implement `parse_row` and `load_weapons`. You may start from the lecture's code, but read each line and be ready to explain it. Checks A1 and A2 must pass. A2 needs **seven** messages from `broken_weapons.csv`, including both problems on line 7.
2. Run `combat.py`. It will fail because Part B is missing. Read the traceback and note which function it stopped in.
3. Move the Crossbow from `combat_hardcoded.py` into `weapons.csv` with id `crossbow`. Its type is `bow`, which is not yet valid. Decide where the list of valid types should live, change it, and write one sentence in your README on why you put it there. Check A3 must pass.

### Part B: monsters (45 min)

4. Implement `resolve`. The rule is the one from lecture section 5: a missing key is inherited, a present key is not, even if its value is `0` or `[]`. Check B1 must pass. `goblin_scout` in `monsters.json` sets `armor` to 0 on purpose to catch the classic mistake.
5. Implement `load_monsters`. Validate every rule in its docstring, name every problem by monster id and path (`goblin.loot[1]`), and collect them all before raising. Checks B2 and B3 must pass. Count how many problems your loader reports for `broken_monsters.json` and explain in your README why `goblin_brute` reports loot problems that are not written in its own entry.
6. Move the Skeleton into `monsters.json` with id `skeleton`, then delete the two classes from `combat_hardcoded.py`. Check B4 must pass. Run `python combat.py` and `python combat.py crossbow`, and copy both outputs into your README.

### Part C: live reload (25 min)

7. Implement `LiveTable.poll` as described in its docstring. Check C1 must pass.
8. Write a 15-line script `watch.py` that creates a `LiveTable` for `weapons.csv`, then loops forever: poll once a second and, after each successful reload, print the DPS of every weapon. Run it, edit `weapons.csv` in a text editor, and save three times: once with a valid change, once with a typo, once fixing the typo. Paste the terminal output into your README.

### Part D: break your partner's loader (10 min)

9. Swap loaders with another pair. Write one new broken file (CSV or JSON) that their loader accepts but that would crash or misbehave in `combat.py`. If you can't, write down the three attempts you made. Give them the file.

## Deliverable

A zip of your `lab13-starter/` folder containing:

- `loader.py` with all eight checks passing, and your updated `weapons.csv`, `monsters.json` and `watch.py`.
- `README.md` (at most one page): how to run the checks, the two `combat.py` outputs, the `watch.py` session, your answers to steps 3 and 5, and the file from step 9 with what it did to the other pair's loader (or the file you received and whether it got past yours).

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Weapon loading and validation (A1-A3) | All three checks pass; messages name line and column | Checks pass but messages are hard for a designer to act on | Checks fail | 25 |
| Monster loading, inheritance and validation (B1-B4) | All four pass; every problem named by id and path; cycle does not hide other problems | Checks pass except B3, or cycle stops all other reporting | Two or more checks fail | 30 |
| Live reload (C1 and `watch.py`) | C1 passes; session shows reload, kept table with message, and recovery | C1 passes, session incomplete | C1 fails | 20 |
| Design answers (steps 3 and 5) | Correct, specific, refer to the code | Plausible but vague | Missing | 10 |
| Part D and README | Attack file is a real gap (or three honest attempts); README complete and runs as described | README incomplete | Missing | 15 |
| **Total** | | | | **100** |

<details>
<summary>Instructor notes</summary>

A reference solution reports 9 problems for `broken_monsters.json`: the cycle once from each of `ghost` and `wraith`, two loot problems on `goblin`, the string `"55"` for `goblin_brute.hp`, `goblin_brute` repeating goblin's two loot problems because it inherits the list, and two problems on `troll` (weapon `club`, empty loot). Students who report the inherited loot problems only once, under `goblin`, have made a defensible choice if they explain it. Common Part D gaps: a negative `armor` accepted by a loader that checks only the type, `hp` as a float (`30.5`), `True` as an int, and loot weights that are floats.

</details>
