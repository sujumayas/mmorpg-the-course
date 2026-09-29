# CS203 · Lab 12: The mob brain

**Week:** 12 ([MMO mob AI: leashing, aggro, threat tables](../lectures/w12-mmo-mob-ai-leashing-aggro-threat-tables.md))
**Time:** one 2-hour lab session plus up to 2 hours at home
**Work:** individually; compare tier tables with a neighbor at the end

## Objective

Build the three rules every MMO mob needs: when to start a fight (a level-scaled aggro radius), whom to attack (a threat table with multipliers, split healing, taunts and the 110% and 130% switch rule), and when to give up (a leash with an evade reset). Then use the table the way a raid designer would, to find the smallest tank threat multiplier that keeps each tier's boss off the healer, and check the simulation against the lecture's formula `m* = B / (2.6 d N)`.

## Starter materials

- Python 3.10 or later, no packages. In this repository, `.venv/bin/python`.
- [`labs/lab12-starter/mob.py`](lab12-starter/mob.py). It has the `ThreatTable` and `Mob` classes with docstrings that state every rule, a provided `Mob.take_damage()`, a provided `flicker()` that reproduces the lecture's tank-and-rogue test with your table, and three raid tiers. You fill in `aggro_radius()`, the five `ThreatTable` methods, `healer_pull()`, `min_safe_multiplier()` and `Mob.update()`. Run `python mob.py` to print the tier table; until your code works the simulated column shows a dash.
- [`labs/lab12-starter/check_lab12.py`](lab12-starter/check_lab12.py). Run `python check_lab12.py` from inside the starter folder. It prints PASS or FAIL for eight checks and exits with status 1 until all pass. On the untouched starter all eight fail.
- The interactive [`examples/w12-threat-table.html`](../examples/w12-threat-table.html). Its table follows the same integer rules as the lab.

## Steps

### Part A: the table (55 minutes)

1. Write `aggro_radius()`. Before running the checker, work out by hand the radius of a level 38 mob for a level 42 player.
2. Write `add_damage()`, `add_heal()` and `choose()`. Keep threat as whole numbers by rounding each addition, and compare `10 × challenger > k × current` with `k` in tenths, exactly as in the lecture. The step 2 checks include two exact ties (a rogue at exactly 110% and a healer just under 130%) that must not switch.
3. Write `taunt()` and `remove()`. A taunt sets the taunter's threat to the current maximum and locks the target for three seconds. Removing the current target lets `choose()` pick the highest remaining unit with no threshold. The step 3 checks also run `flicker()` and expect the lecture's 60 switches without thresholds and 3 with them.

### Part B: the healer and the leash (35 minutes)

4. Write `healer_pull()` using your table, then `min_safe_multiplier()`, which searches multipliers 1.00, 1.01, 1.02 and upward for the first one that never lets the healer pull within 600 seconds. The checker expects the lecture's 8, 22 and 301 seconds, and 1.16 for a 600 DPS boss and a 200 DPS tank.
5. Write `Mob.update()` for the IDLE, COMBAT and EVADE states. The checker walks a mob through a player outside and then inside its radius, a chase past the leash, damage while evading, and the return home.

### Part C: the raid designer's table (at home)

6. Run `python mob.py`. Copy the tier table. For each tier, explain in one line why the simulated value is the formula value rounded up to the next 0.01, and say what would change if the fight were only 120 seconds long. Rerun `min_safe_multiplier` with `seconds=120` to check.
7. The designer wants one multiplier for all three tiers with a healer margin of at least 1.5 on every boss. Compute it from the formula, then confirm with `healer_pull` that the healer never pulls in any tier at that value.
8. Tier 3 adds two adds that stay in combat all fight, so `N = 3` for healing threat. Recompute the tier 3 `m*` from the formula and with `min_safe_multiplier(..., mobs=3)`. Then write two sentences on what happens to the adds if the tank does not also build threat on them, using the rules in `ThreatTable` to justify it.
9. Write a note of at most 300 words to the raid team. Recommend a multiplier, state the margin `S` it gives on each tier, and name one thing players will stop doing (or start doing) at that margin. Add one leash rule for the tier 3 boss room and the exploit it prevents.

## Deliverable

Your completed `mob.py` with `check_lab12.py` passing (paste its output), and a PDF with the step 6 table and explanations, the step 7 multiplier with its confirmation, the step 8 values and sentences, and the note.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Threat table (35%) | All five table checks pass; `choose()` handles no target, lock, thresholds and several challengers in a clear order | All pass, code hard to follow | Damage and healing work, a switching or taunt check fails | Missing or wrong |
| Healer search and FSM (20%) | Both checks pass; `min_safe_multiplier` builds candidates without float drift | Both pass, search inefficient or fragile | One of the two fails | Missing |
| Formula versus simulation (20%) | Step 6 rounding and the 120 s case explained with the pull-time formula; step 7 value confirmed in all tiers | Values right, explanations thin | Table copied, no explanation | Missing |
| Adds and splitting (10%) | Step 8 value from formula and simulation, and a correct account of add targeting | Values right, add behavior vague | One value | Missing |
| Raid note (15%) | Multiplier with `S` per tier, a concrete player behavior change, a leash rule with its exploit | Numbers present, behavior vague | No numbers | Missing |
