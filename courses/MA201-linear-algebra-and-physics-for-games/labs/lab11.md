# MA201 · Lab 11: Grids, quadtrees and a world boss

**Week:** 11 ([Spatial partitioning: grids and quadtrees](../lectures/w11-spatial-partitioning-grids-and-quadtrees.md))
**Time:** one 2-hour lab session plus up to 2 hours at home
**Work:** pairs for Parts A and B, individual report for Part C
**Counts toward:** problem sets (40%)

## Objective

Turn the lecture's work-counting grid and quadtree into real spatial indexes that return exact neighbors and survive moving entities. Measure how well the lecture's unit-cost model predicts wall-clock time on your machine, fix the model with a measured weight, and then choose an index for a zone whose crowd walks across the map to a world boss.

## Starter materials

- Python 3.10 or later, standard library only. In this repository, `.venv/bin/python`.
- [`labs/lab11-starter/partition.py`](lab11-starter/partition.py). It provides the lecture's scene (`make_scene()`, 2,000 city players and 2,000 wilderness monsters, same seed), a brute-force `brute_neighbors()` to test against, a `boss_session()` generator that walks the city crowd to a world boss at `(200, 800)` over 60 frames, and a timing helper. You write `best_cell_size()`, `Grid.query()`, `Grid.move()`, `QuadTree.insert()` and `QuadTree.query()`. `python partition.py` times each index on the lecture scene once your code runs.
- [`labs/lab11-starter/check_lab11.py`](lab11-starter/check_lab11.py). Run `python check_lab11.py` inside the starter folder. It prints PASS or FAIL for seven checks and exits with status 1 until all pass. On the untouched starter all seven fail.
- The interactive [`examples/w11-cell-size-tradeoff.html`](../examples/w11-cell-size-tradeoff.html) for checking `W(s)` by eye.

## Steps

### Part A: exact queries (60 minutes)

1. Derive the best cell size when visiting a cell costs `k` times as much as testing an entity, `W(s) = k (2r/s + 1)² + ρ (2r + s)²`. Show the derivative on paper, then write `best_cell_size(r, rho, k)`. Confirm by hand that `k = 1` gives the lecture's 2.54 m for the city.
2. Write `Grid.query(i, r)`. Visit the same cells as the lecture's `work()`, but test each entity with squared distance (MA101 week 14) and return the sorted ids within `r`, never `i` itself. Keep the two counters. The checks compare your answers with brute force at cell sizes 2.5, 8 and 40 m.
3. Write `Grid.move(i, x, y)`. Only touch cell lists when the cell changes. The check makes 3,000 small random moves and then requires every id to appear exactly once and every query to still match brute force. Count how many of the 3,000 moves changed cell at `s = 8` and explain the number with a one-line estimate.
4. Write `QuadTree.insert(i)` and `QuadTree.query(i, r)` with capacity 8 and maximum depth 10. The checks test leaf capacity, exact answers, and 50 entities stacked on one point, which must stop splitting at depth 10 instead of recursing forever.

### Part B: from work to milliseconds (30 minutes)

5. Run `python partition.py`. For the three grids, you now have two counts and a time each. Fit the time as `a × cells + b × tested` (three equations, two unknowns; least squares or a careful eyeball is fine). Report `k = a / b` for your machine and recompute `s*` for the city and the wilderness with it. Does the order of the lecture's table change?
6. Time the quadtree. Report its build time separately. Explain why the quadtree's time is closer to the best grid than the lecture's work table suggests, using your `k`.

### Part C: the world boss (at home)

7. Use `boss_session()` to replay 60 frames. For each frame, bring each index up to date and then run every entity's query. Compare at least three strategies:
   - one grid with your chosen cell size, updated with `move()`;
   - the same grid rebuilt from scratch every frame;
   - a quadtree rebuilt every frame.
   Record the per-frame time (update plus queries) and plot it against the frame number for all three.
8. Find the frame where each strategy is slowest and explain why with `W(s)`: what are `ρ` and `s*` for the gathered crowd, which is 2,000 players in a circle of radius 10 m?
9. Write a recommendation of at most 300 words for the zone's server programmer. Name one structure and its settings, give its worst-frame time and the frame it happens on, compare it with the runner-up in numbers, and say what you would monitor on the live server to know when the choice stops being right.

## Deliverable

Your completed `partition.py` with `check_lab11.py` passing (paste the output), the step 1 derivation, the step 3 estimate, the step 5 fit and recomputed `s*` values, the step 7 plot, and the recommendation.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Correct indexes (35%) | All seven checks pass; move touches lists only on cell change; quadtree counts are kept at the root | All pass, with extra rebuilds or duplicated code | Grid passes, quadtree fails | Fewer than three checks pass |
| Derivation and model fit (20%) | Correct derivative, measured `k`, `s*` recomputed and the table-order question answered | Derivation right, fit rough | Formula stated without derivation | Missing |
| Boss replay (25%) | Three strategies timed per frame and plotted; worst frames explained with the crowd's `ρ` and `s*` | Plot present, explanation partial | One strategy only | Missing |
| Recommendation (20%) | One named structure with settings, worst-frame numbers against the runner-up, a concrete live metric | Numbers present, metric vague | No numbers | Missing |
