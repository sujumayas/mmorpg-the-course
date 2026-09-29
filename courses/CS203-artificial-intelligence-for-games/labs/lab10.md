# CS203 · Lab 10: The awareness meter

**Week:** 10 ([Perception systems](../lectures/w10-perception-systems.md))
**Time:** one 2-hour lab session plus up to 2 hours at home
**Work:** individually; compare tuning tables with a neighbor at the end

## Objective

Build the perception layer for a stealth guard: a fill-and-drain awareness meter with suspicious and alert states, the break-even exposure formula, and hearing measured along a path instead of through walls. Then use it as a designer would. Tune one number, the forget time, so that a careful player who peeks from cover survives and a careless one is caught, and explain the trade-off in numbers.

## Starter materials

- Python 3.10 or later, no packages. In this repository, `.venv/bin/python`.
- [`labs/lab10-starter/perception.py`](lab10-starter/perception.py). It has the lecture's constants, a provided `simulate()` that runs a route through your `Awareness` class, a grid loader, and two scripted routes past one guard, `CAREFUL` and `CARELESS`. You fill in `detect_time()`, `break_even()`, `Awareness.update()`, `path_distance()` and `heard()`. Run `python perception.py` to print a table of first-alert times for several forget times; until your code is written it prints a dash.
- [`labs/lab10-starter/check_lab10.py`](lab10-starter/check_lab10.py). Run `python check_lab10.py` from inside the starter folder. It prints PASS or FAIL for seven checks and exits with status 1 until all pass. On the untouched starter all seven fail.
- The interactive [`examples/w10-detection-meter.html`](../examples/w10-detection-meter.html) for building intuition. It uses the same fill times and forget time as the lab.

## Steps

### Part A: the meter (50 minutes)

1. Write `detect_time(d, light)` and `break_even(d, light, forget)` from lecture section 2. Distances beyond 20 m use the 20 m fill time; light 0 returns infinity. Before running the checker, confirm by hand that `detect_time(10, 0.5)` is 5.0 and `break_even(20)` is 0.4.
2. Write `Awareness.update(sensed, d, light)`. Fill while sensed, drain while not, cap at 1 and floor at 0. Run the checker until the step 2 check passes.
3. Add the state transitions listed in the docstring. Suspicious starts at 0.5 and ends only when the meter falls below 0.3. Alert starts at 1 and ends only when the meter drains to 0. The step 3 checks test both thresholds and confirm that your meter reproduces the lecture's peeking result of 8.2 s.

### Part B: hearing (30 minutes)

4. Write `path_distance(grid, a, b)` as a breadth-first search over 1 m cells with 4-way moves, returning `None` when there is no path. Then write `heard(radius, distance, offscreen_far)` with Blacklist's half-radius rule for far, off-screen listeners. The step 4 checks use a map with a wall where the straight-line distance is 4 m and the path is 8 m.
5. Build a map of your own, at most 15 × 15, where a sound of radius 8 is heard by straight-line distance but not by path distance. Record both distances.

### Part C: tune the guard (at home)

6. Run `python perception.py`. For each forget time `F`, the table shows when each route first makes the guard alert, or "safe". Find, to the nearest 0.5 s, the largest `F` for which `CAREFUL` stays safe and the smallest `F` for which it does not. Explain the boundary with the break-even formula: `CAREFUL` peeks for 1 s out of every 4 s at 12 m, then spends its last 4 s in half light at 18 m.
7. Change one thing about the guard (not the routes) so that `CARELESS` takes at least 6 s to be caught while `CAREFUL` stays safe at your chosen `F`. You may change `T_NEAR`, `T_FAR` or the thresholds. Record the before-and-after first-alert times.
8. Write a note of at most 300 words to the level designer. State your chosen `F` and the change from step 7, give the break-even exposure at 5, 12 and 18 m under your settings, and say what a player who peeks at 12 m can get away with. Name one player behavior your tuning makes too easy and how you would detect it in a playtest.

## Deliverable

Your completed `perception.py` with `check_lab10.py` passing (paste its output), your step 5 map file, and a PDF with the step 5 distances, the step 6 boundary with its explanation, the step 7 before-and-after table, and the designer note.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Meter and states (30%) | All five meter and state checks pass; update logic is short and in the documented order | All pass, code hard to follow | Meter works, one state check fails | Meter missing or wrong |
| Hearing (20%) | Both hearing checks pass; the step 5 map works and both distances are reported | Checks pass, map missing or not demonstrated | BFS works, `heard()` wrong | Missing |
| Forget-time boundary (20%) | Boundary found to 0.5 s and explained with `f* = T / (T + F)` including the final half-light segment | Boundary found, explanation partial | Table copied, no boundary | Missing |
| Guard change (10%) | One change, both routes measured before and after, targets met | Targets met, measurements incomplete | Change made, a target missed | Missing |
| Designer note (20%) | Numbers for three distances, a concrete exploit and a concrete playtest measure | Numbers present, exploit vague | No numbers | Missing |
