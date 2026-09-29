# MMO406 · Lab 09: The realm clock

**Week:** 9 ([lecture](../lectures/w09-living-world-events.md))
**Time:** 2 hours in the lab, plus up to 3 hours to finish.
**Work mode:** pairs.
**Counts toward:** exercises (40%). The event brief goes into the events section of your world bible.

## Objective

Implement the realm clock with fatigue, add a loop in which realms that fall behind lose participants, and design a collective-goal event for your setting that lands every realm inside its narrative window.

## Starter materials

All in [`lab09-starter/`](lab09-starter/). Standard-library Python 3, run with `.venv/bin/python` from the repository root or any Python 3.9+.

- [`realm_clock.py`](lab09-starter/realm_clock.py), a skeleton with seven functions to write: `daily_rate`, `finish_day`, `ceiling_per_player`, `largest_g`, `simulate`, `load_realms` and `plan`. The `simulate` docstring gives the exact order of the daily update, including the discouragement rule.
- [`realms.csv`](lab09-starter/realms.csv), the lecture's four invented realms. Replace them in Part C.
- [`test_realm_clock.py`](lab09-starter/test_realm_clock.py), six tests using the lecture's numbers. All fail on the starter. Run them from the starter folder with `../../../../.venv/bin/python test_realm_clock.py`.
- The [interactive](../examples/w09-realm-clock.html) for spot checks.

## Steps

### Part A: the clock (35 min)

1. Implement `daily_rate`, `finish_day`, `ceiling_per_player`, `largest_g`, `load_realms` and `plan`. Running `python realm_clock.py` must print the lecture's three plans.
2. With the lecture's realms, `q = 0.2`, `u = 10`, `d = 0.97` and a window of day 14 to day 42, find the fixed goal `G` that puts the largest number of realms in the window. Report `G` and each realm's status. Compare with the scaled goal from `largest_g`.

### Part B: the discouragement loop (40 min)

3. Implement `simulate` and run all tests.
4. The loop models a realm whose players see that they are behind schedule and stop turning up. With `target_day = 30`, `behind = 0.8` and `penalty = 0.9`, run the fixed goal of 300,000 with and without fatigue for all four realms. Report the finish days next to the formula's.
5. Explain in at most 100 words why the loop turns a late realm into one that never finishes, and why it doesn't affect the huge realm.
6. Design one countermeasure and implement it as an option in `simulate`: a catch-up bonus (contributions worth more when behind), a goal that shrinks after a set day, or a studio fallback on `D_max`. Rerun step 4 with it and report the finish days. Say which realms it helps and what it costs the story.

### Part C: your event (45 min)

7. Replace `realms.csv` with realm sizes that fit your game concept (at least three realms, with at least a 5x spread between smallest and largest). Justify the sizes in one line.
8. Pick an event from your setting's tension ledger that players could push forward. Choose `q`, `u` and `d` with a one-line justification each, and a narrative window.
9. Choose a goal rule and value. Run `plan` and `simulate` with the discouragement loop and your countermeasure. Adjust until every realm finishes inside the window, or document why a realm may miss it and what the fallback does.
10. Write the event brief from section 4 of the lecture (kind, story, clock, fallback, states, legacy, canon), at most one page.
11. Swap briefs with another pair. Each pair names the realm size at which the other's plan fails first, using your code. Revise if needed.

## Deliverable

- The completed `realm_clock.py` with all tests passing, your countermeasure option and your `realms.csv`.
- A report of at most 3 pages: the step 2 result, the step 4 table and step 5 explanation, the step 6 results, your finish-day table from step 9, the event brief, and the other pair's failure point with your response.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Model (Part A) | Tests for the clock pass; step 2 goal and statuses correct and compared with the scaled rule | Tests pass, comparison missing | Tests fail | 20 |
| Discouragement loop (Part B) | Simulation passes; explanation correct; a working countermeasure with results and a named story cost | Simulation passes, countermeasure missing or untested | Missing | 30 |
| Event plan (Part C, steps 7-9) | Justified parameters; every realm in window or a documented fallback; loop included | Plan works only without the loop | Missing | 25 |
| Event brief and peer check | All seven brief parts; legacy and canon choices tied to weeks 7 and 8; failure point recorded and answered | Brief complete, peer check missing | Missing | 25 |
| **Total** | | | | **100** |
