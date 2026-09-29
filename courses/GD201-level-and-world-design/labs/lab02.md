# GD201 · Lab 02: Blockout and critical path

**Week:** 2 · **Time:** 2 hours in the lab plus about 4 hours at home over the week · **Weight:** first of the graded blockouts (the blockouts component is 40% of the course). Lab 03 adds pacing to this same blockout.

**Lecture:** [Week 02, blockout and greyboxing](../lectures/w02-blockout-and-greyboxing.md). **Interactive:** [w02-greybox-budget.html](../examples/w02-greybox-budget.html), for planning your rounds.

## Objective

Finish a small tool that measures critical-path distance and time on a text-grid blockout, check it against a sample level, then build your Lab 01 paper level as a playable blockout in a game engine. Run three test rounds, keep a revision log, and compare the tool's predicted timings with your stopwatch.

## Starter materials

- [`lab02-starter/blockout.py`](lab02-starter/blockout.py). Loads a text grid, finds marker letters, and prints a report. Four functions are left for you: `shortest_steps` (breadth-first search), `path_seconds`, `critical_path` and `problems_at_ship` (the lecture's budget model).
- [`lab02-starter/sample_mill.txt`](lab02-starter/sample_mill.txt). A 28 × 12 cell sample blockout. `#` is wall, `.` is floor, capital letters are markers: `S` start, `A` to `D` beats, `G` goal. One cell is one metre.
- [`lab02-starter/check_lab02.py`](lab02-starter/check_lab02.py). A checker with 12 checks. Do not edit it.
- An engine of your choice: Unity (ProBuilder), Unreal (modeling tools or BSP brushes), Godot (CSG nodes) or TrenchBroom for a Quake-family engine. Use the engine's default first-person or third-person controller and write down its run speed.

Run from inside `lab02-starter`:

```
python blockout.py sample_mill.txt
python check_lab02.py
```

The starter prints the map size and markers, then reports what isn't implemented yet.

## Steps

1. **Part A, the tool (30 min).** Implement `shortest_steps` with a queue and a dictionary of distances. Moves are up, down, left and right only. Then implement `path_seconds` and `critical_path`. Check: the sample's `SABCDG` path is 64 cells, 10.7 s at 6 m/s.
2. **Part B, the budget (10 min).** Implement `problems_at_ship`. Run the checker until it prints `12/12 checks pass`.
3. **Part C, your level on a grid (20 min).** Convert the Lab 01 paper level to a text grid with markers for each beat. Use room sizes that are whole multiples of one base size, as section 3 of the lecture requires. Run `blockout.py` on it and record the critical path and each leg.
4. **Part D, the blockout (at home, about 2 hours).** Build the level in your engine with the Level Design Book checklist from the lecture: gridded floor, a scale figure the size of the player, walls at 150 to 200% of its height, doorways at least twice its width, and labelled placeholder boxes for enemies and pickups. No final art.
5. **Part E, three rounds (at home, about 2 hours in total).** Run three short test rounds with at least two testers each who haven't played it. Before each round, time the critical path yourself. During each round, observe without coaching. After each round, make changes and log them.
6. **Compare (15 min).** For each round, put the tool's predicted critical-path time (grid length divided by your controller's run speed) next to your stopwatch time. Where they differ by more than 20%, find the cause in the level.
7. **Plan the art switch (10 min).** From your log, estimate your own `f` (fraction of problems found per round) and `c_g` (hours per round). Estimate what an art round would cost you. Use the interactive or `problems_at_ship` to say when you would switch to art if you had 40 more hours.

## Deliverable

Submit a zip with:
- Your completed `blockout.py` and your level's text grid.
- The engine project or an exported build, plus four screenshots: overview from above, the scale figure beside a doorway, and two views at player eye height.
- A revision log with one row per round: date, testers, stopwatch critical-path time, problems observed (behaviour, not interpretation), change made for each, hours spent.
- A half-page note with the predicted-versus-measured comparison from step 6 and the art-switch plan from step 7, including your estimated `f`, `c_g` and `c_a`.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Checker | 12/12 checks pass | 8-11 pass | 0-7 pass | 20% |
| Blockout quality | Playable, correct scale throughout, grid-consistent sizes, checklist complete, placeholders labelled | Playable with one or two scale or checklist gaps | Not playable, or decorated instead of measured | 30% |
| Revision log | Three rounds, observations separated from interpretation, each change tied to an observation | Three rounds but changes not tied to observations | Fewer than three rounds | 25% |
| Prediction vs measurement | Every round compared, each large gap explained by a named place in the level | Comparison present, causes vague | Missing | 15% |
| Art-switch plan | Uses own `f` and costs, states a switch point and the art-only problems expected | Switch point stated without numbers | Missing | 10% |
