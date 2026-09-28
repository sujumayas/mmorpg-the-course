# MA101 · Lab 14: Range queries

Assigned in week 14 ([lecture](../lectures/w14-distances-ranges-and-squared-distance.md)). Due at the start of week 15. Counts toward the problem-set grade.

## Objective

Classify thousands of objects by distance using squared distance only, prove on real data that the answers match the square-root version, reproduce and fix an integer-overflow range bug, and build an aggro and leash state machine with hysteresis.

## Starter materials

- [`starter/lab14_starter.py`](starter/lab14_starter.py). Python 3 with the standard library. It loads the data files below and has empty functions:
  - `sq_dist(a, b)` returns `dx² + dy² + dz²`.
  - `despawn_zone(mob, players, r_near, r_far)` returns `"safe"`, `"random"` or `"despawn"` using the nearest player.
  - `metric(dx, dz, name)` returns Euclidean, Manhattan, Chebyshev or alternating-diagonal distance.
  - `MobBrain` class with `state`, `r_aggro`, `r_leash` and an empty `update(player_pos)` method.
- [`starter/mobs.csv`](starter/mobs.csv): 5,000 mob positions, columns `id, x, y, z`, integer blocks.
- [`starter/players.csv`](starter/players.csv): 3 player positions in the same world.
- [`starter/int32_sim.py`](starter/int32_sim.py): `wrap32(n)` wraps any integer to signed 32-bit, and `sq_dist_int32(a, b)` computes a squared distance with every step wrapped, to imitate a C# or C++ `int`.
- [`starter/chase.csv`](starter/chase.csv): a recorded player walk of 300 samples near one mob, columns `t, x, z`, 0.1 s apart.
- Spreadsheet route: import the CSV files into any spreadsheet. Steps 3 and 5 are easier in Python.
- The week 14 interactive, [`examples/w14-range-rings.html`](../examples/w14-range-rings.html), to spot-check individual positions.

## Steps

1. **Squared distance.** Implement `sq_dist`. Check it on the lecture's table: the mob at the origin and a player at (91, y, 91) with equal heights must give 16,562.
2. **Classify.** Implement `despawn_zone` with `r_near = 32` and `r_far = 128`, comparing squared distances against `r_near²` and `r_far²`. For each mob, use the nearest of the three players. Report how many mobs fall in each zone.
3. **Prove equivalence on data.** Write a second classifier that computes `sqrt` and compares with the unsquared radii. Run both on all 5,000 mobs and report the number of disagreements. It should be zero. Then time both over 100 repetitions and report the two times. Write one sentence on whether the difference matters at this scale.
4. **The box shortcut.** Classify again with the per-axis check `abs(dx) ≤ 128 and abs(dz) ≤ 128` (ignore y). Count the mobs the box check keeps that the true rule despawns. Give the coordinates of the one that is farthest from its nearest player.
5. **Overflow.** Convert all positions to centimeters (multiply by 100) and recompute each mob's squared distance to the nearest player you found in step 2 with `sq_dist_int32`. Count how many mobs now get a wrong zone. Find the smallest wrong-zone distance in blocks. Explain the result with the number 2,147,483,647, then fix it by using Python integers (or 64-bit) and confirm zero errors. Extension: if the nearest-player search itself runs in 32-bit, a far player's wrapped negative value can win. Find the smallest wrong-zone distance in that case and explain why it is so much smaller.
6. **Metrics.** For the offsets (10, 0), (3, 4), (6, 6) and (20, 15), compute all four metrics with `metric`. Then count how many mobs would be in the "despawn" zone under each metric with `r_far = 128`. Which metric keeps the most mobs alive, and why?
7. **Aggro and leash.** Implement `MobBrain.update` with states `IDLE`, `CHASE` and `RETURN`. `IDLE` becomes `CHASE` when `S ≤ r_aggro²`. `CHASE` becomes `RETURN` when `S > r_leash²`. `RETURN` becomes `IDLE` after 3 seconds. Use `r_aggro = 10`, `r_leash = 30`, and the mob fixed at the origin. Replay `chase.csv` and report every state change with its time. Then replay with a single radius (`r_leash = r_aggro = 10`) and count the state changes. Report both counts.

## Deliverable

Submit your completed `lab14_starter.py` (or spreadsheet) and a PDF memo of at most 400 words, addressed to an engine programmer. The memo must contain:

- Zone counts from step 2 and the disagreement count and timings from step 3.
- The box-check count and farthest example from step 4.
- The overflow finding from step 5, with the threshold distance and your fix.
- The metric table from step 6.
- The two state-change counts from step 7 and one sentence on what the leash band buys the player.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Squared-distance classification | Correct zone counts, zero disagreements shown, no square roots in the main classifier | Counts slightly off or a stray `sqrt` | Wrong or does not run | 25% |
| Box and overflow analysis | Correct counts, overflow explained with the int32 limit and fixed | One of the two analyses incomplete | Missing | 20% |
| Metric comparison | All four metrics correct for all offsets, correct explanation of which keeps most mobs | One metric wrong or explanation missing | Missing or mostly wrong | 20% |
| Hysteresis state machine | Correct transitions, both counts reported, clear comparison | Works with minor timing errors | Missing or flickers with the two-radius rule | 25% |
| Memo clarity | Under 400 words, numbers first, a programmer could act on it | Understandable but padded or missing a number | Hard to follow | 10% |
