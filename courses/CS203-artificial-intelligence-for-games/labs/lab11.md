# CS203 · Lab 11: The stage manager

**Week:** 11 ([Group tactics and formations](../lectures/w11-group-tactics-and-formations.md))
**Time:** one 2-hour lab session plus up to 2 hours at home
**Work:** pairs for Parts A and B; the designer note is individual

## Objective

Build the central coordinator that decides which melee enemies may close in on the player and which attacks they may use, in the style of Kingdoms of Amalur: Reckoning's grid. Make it rotate attackers fairly. Add formation slot assignment that avoids crossing paths. Then use the provided fight simulation to set difficulty with two capacities instead of changing any enemy.

## Starter materials

- Python 3.10 or later, no packages. In this repository, `.venv/bin/python`.
- [`labs/lab11-starter/stage.py`](lab11-starter/stage.py). It defines two creature types with the lecture's grid and attack weights (plus a damage value per attack), a provided `run_rounds()` that admits enemies from a waiting queue, lets them attack and rotates them to the back, and a provided `fight()` that counts rounds until the player has taken 600 damage. You fill in `StageManager.request_slot()`, `choose_attack()` and `release()`, then `damage_taken()`, `assign_greedy()` and `assign_best()`. Run `python stage.py` to print rounds-to-600-damage at three difficulty settings; until your code works it prints a dash.
- [`labs/lab11-starter/check_lab11.py`](lab11-starter/check_lab11.py). Run `python check_lab11.py` from inside the starter folder. It prints PASS or FAIL for seven checks and exits with status 1 until all pass. On the untouched starter all seven fail.
- The interactive [`examples/w11-attack-grid.html`](../examples/w11-attack-grid.html). Its Step button uses the same weights and capacities as `run_rounds()`, with two differences. On the grid, the heaviest enemy picks its attack first (ties in admission order), which is how Dawe's example has the troll charge before the soldier. And its admission skips over an enemy that does not fit and keeps admitting, where `run_rounds()` stops at the first one. Step 7 asks you about that second difference.

## Steps

### Part A: the manager (50 minutes)

1. Write `request_slot()` and `choose_attack()`. Admission and attack choice follow lecture section 2: admit when the grid weight fits in what is left, choose the first affordable attack in strongest-first order. An enemy may hold only one attack at a time, and only enemies on the grid may attack. Before running the checker, predict on paper what Dawe's example (soldier, troll, soldier; capacities 12 and 10) should return.
2. Write `release()`. It frees both the attack weight and the grid weight. The step 2 checks then run six soldiers through eight rounds and expect exactly four attacks each and 42 damage every round. If your rotation is unfair, read `run_rounds()` and find which of your methods leaves state behind.

### Part B: numbers and slots (40 minutes)

3. Write `damage_taken()` so it reproduces the lecture's table. Then extend the table in your report to packs of 12 for caps of 3 and 4, and give the pack size at which each cap first exceeds 2,000 total damage.
4. Write `assign_greedy()` and `assign_best()`. The checker uses the lecture's four units and then 200 random five-unit cases to confirm that the best assignment is never longer than greedy. Add a line of your own that counts how many of those 200 greedy assignments contain at least one crossing pair of paths (the lecture's `crosses()` function is a good start). Report the count.

### Part C: tune the fight (at home)

5. Run `python stage.py`. The pack is one troll followed by six soldiers. Record rounds-to-600 for the three settings. Then run `fight()` on a grid of your own: grid capacity 8 to 24 in steps of 4, attack capacity 6 to 18 in steps of 4. Put the results in a table.
6. Find the settings in your table where raising grid capacity changes nothing. Explain, with the attack weights, which capacity is binding there.
7. The first round with grid capacity 12 admits only the troll and one soldier. Explain why admission stops at the first enemy that does not fit, and describe what a player sees when a troll is at the front of the queue and the grid is almost full. Propose one change to the admission rule and say what it costs.
8. Write a note of at most 300 words to the combat designer. Recommend grid and attack capacities for easy, normal and hard so that this pack takes about 35, 20 and 12 rounds to deal 600 damage. Say which enemies the player sees attacking at each setting, and name one pack composition your settings would make too easy.

## Deliverable

Your completed `stage.py` with `check_lab11.py` passing (paste its output), and a PDF with the step 3 table, the step 4 crossing count, the step 5 grid table, the explanations for steps 6 and 7, and the designer note.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Stage manager (30%) | All four manager checks pass; methods are short and keep `grid_used` and `attack_used` consistent | All pass, code hard to follow | Admission works, rotation fails | Missing or wrong |
| Damage and assignment (20%) | Both checks pass; step 3 table to 12 with thresholds; step 4 crossing count reported | Checks pass, one extra missing | One check fails | Missing |
| Capacity analysis (20%) | Full grid table; binding capacity identified with the weights | Table complete, explanation vague | Partial table | Missing |
| Queue behavior (10%) | Head-of-line blocking explained; a concrete alternative with its cost | Explained, no alternative | Described only | Missing |
| Designer note (20%) | Three settings that hit the targets within 2 rounds, what the player sees, and a concrete weak composition | Settings given, one target missed | No numbers | Missing |
