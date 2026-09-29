# MMO306 · Lab 03: Pull planner and trash routes

**Week:** 3 · **Time:** 2 hours in the lab plus about 2 hours at home · **Weight:** part of the encounter designs component (40%). The wing you lay out here becomes the first wing of your final dungeon.

**Lecture:** [Week 03, dungeon design: trash, bosses, loot](../lectures/w03-dungeon-design-trash-bosses-loot.md). **Interactive:** [w03-pull-size.html](../examples/w03-pull-size.html), for checking single pulls by eye.

## Objective

Implement the lecture's pull model: kill time with a target cap, tank survival time, clear time and the fastest safe pull. Add a route planner that picks which packs to kill to reach a forces target in the least time. Then lay out the trash for the first wing of your final dungeon and show that the fastest route players can find passes through the packs you meant them to fight.

## Starter materials

- [`lab03-starter/pulls.py`](lab03-starter/pulls.py). Base numbers from the lecture, a pack loader and six functions to fill in: `kill_time`, `survive_time`, `pull_works`, `clear_minutes`, `best_pull` and `route`.
- [`lab03-starter/packs.csv`](lab03-starter/packs.csv). Eight invented packs for a sample wing, with enemy count, forces value (percent) and walking time to each.
- [`lab03-starter/test_pulls.py`](lab03-starter/test_pulls.py). Tests taken from the lecture's tables and the sample wing. Do not edit it.

Run from inside `lab03-starter`:

```
../../../../.venv/bin/python test_pulls.py
../../../../.venv/bin/python pulls.py
```

On the starter every test fails with `NotImplementedError`. When you are done, all four print `PASS`.

## Steps

1. **Part A, one pull (20 min).** Implement `kill_time`, `survive_time` and `pull_works`. Check them against the `N = 8` row of the lecture: 20 s to kill with cap 20, 32 s with cap 5, 35.6 s for the tank to drop.
2. **Part B, the run (15 min).** Implement `clear_minutes` and `best_pull`. Reproduce both columns of the lecture's clear-time table and the scaling table (10, 5 and 3 enemies at +0, +5 and +10 levels).
3. **Part C, routes (25 min).** Implement `route` by searching every subset of packs. Run the tests until all four pass. Run `pulls.py` and record the route to 30% forces. Then rerun with `d = 45` and explain in two sentences why the route now includes the far `side_vault`.
4. **Part D, crowd control (at home, 30 min).** Add an optional argument `cc` to `survive_time`: the number of enemies that are crowd-controlled (they deal no damage) for the whole pull. Show how one `cc` changes the largest safe pull at +5 levels. Keep the original tests passing.
5. **Part E, your wing (40 min).** Design the first wing of your final dungeon: 6 to 12 packs, their enemy counts, forces values and walking times, and a forces target for the wing. Choose at least one "must-see" pack that teaches the first boss's mechanic. Adjust distances, pack sizes or `d` until `route` includes the must-see pack at the base numbers and at +5 levels.
6. **Design note (at home, 45 min).** One page with your wing's pack table, the chosen route at both scalings, the forces slack, and a paragraph on the pull size you expect players to choose and why you want it.

## Deliverable

Submit a zip with:
- Your completed `pulls.py`, including the Part D `cc` option.
- Your wing as a `packs.csv` in the same format.
- A sketch of the wing (paper photo or drawing) with the route marked at both scalings.
- The one-page design note.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Tests | All 4 pass | 2-3 pass | 0-1 pass | 20% |
| Crowd control extension | `cc` implemented, original tests still pass, effect at +5 levels shown with numbers | Implemented without the +5 comparison | Missing | 15% |
| Wing design | Must-see pack on the fastest route at both scalings, forces slack stated and between 1.1 and 1.5, sketch matches the CSV | Must-see pack on the route at one scaling only | Must-see pack skipped, or numbers missing | 35% |
| Route explanation | Part C answer names the unsafe pull and the forces-per-second trade | Answer names the change without the reason | Missing | 10% |
| Design note | Expected pull size argued from `t_kill` and `t_surv`, with a stated design intent | Pull size stated without the model | Missing | 20% |
