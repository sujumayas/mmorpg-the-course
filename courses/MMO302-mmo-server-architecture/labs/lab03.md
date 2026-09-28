# MMO302 · Lab 03: Build interest management

**Week:** 3 · **Time:** 2 hours in lab plus about 3 hours at home · **Weight:** part of the labs (40%)

## Objective

Build the grid interest management from the [week 3 lecture](../lectures/w03-area-of-interest-grids-radius-hysteresis.md), prove it gives exactly the same answer as brute force, measure how much faster it is, and add hysteresis. You finish with an interest design for a crowded hub, backed by your own measurements.

## Starter materials

Folder [`lab03-starter/`](lab03-starter/README.md). Standard library Python only.

- `aoi.py`: `mulberry32` and `make_world` (seed 302, the same worlds as the lecture and the interactive), `brute_sets` (exact radius by checking every pair), the pacing test `boundary_run`, and printers for the lecture's tables. Stubs for `build_grid`, `candidates`, `grid_count`, `grid_radius_sets` and `Hysteresis.step`.
- `test_aoi.py`: the lecture's numbers as tests, plus exact equality with brute force.

## Steps

1. **The hash.** Implement `build_grid` (cell key `(floor(x / c), floor(y / c))`) and `candidates` (the `(2k + 1) × (2k + 1)` block). Work the four-player example in the test by hand first. Write down each player's block and check that the grid count is 8.
2. **Grid count.** Implement `grid_count`. Run `python aoi.py --table` once `grid_radius_sets` is also done (step 3), and check the grid column against the lecture.
3. **Broad and narrow phase.** Implement `grid_radius_sets`, the grid as a broad phase followed by an exact distance test. Run the tests until they pass. The key test compares your sets with `brute_sets` player by player. Explain in two sentences why the answer is exact when `k × c ≥ r` and give a small example where it is wrong when `k × c < r`.
4. **Time it.** Run `python aoi.py --bench`. Record the times at 1,000, 2,000 and 5,000 players. Compute how the brute-force time grows from 1,000 to 2,000 and how the grid time grows. Relate both to `N²` and `N × density`. Then repeat the benchmark with `make_world(n, 0.5)` (edit `bench`) and explain why the grid's advantage shrinks.
5. **Cell size.** For the uniform 1,000-player world, measure candidates scanned (the grid count) and wall time for `c = 50, k = 1`, `c = 25, k = 2` and `c = 50/3, k = 3`. Check that all three give the brute-force sets. Recommend a cell size and justify it with your numbers.
6. **Hysteresis.** Implement `Hysteresis.step`. Run `python aoi.py --boundary` and check it against the lecture's table. Then set the pacing amplitude to 7 m and find the smallest `r_out` (to 0.5 m) with a single enter and no leaves. State the rule that links amplitude and margin.
7. **Design.** For the in-class hub (600 players in a 200 m plaza, 400 spread over the 2 km zone), write a one-page interest design. Give the view radius, cell size, block size, rebuild interval (use the fastest mount speed you assume), `r_in` and `r_out`, and the plaza's deliveries per tick from `make_world`-style numbers or your own generator. Say what you do when the plaza exceeds the budget, citing week 1 or CS202 week 13.

## Deliverable

Your finished `aoi.py`, the outputs of steps 2, 4 and 6, the cell-size table from step 5, a plot of time against `N` for brute force and grid (log axes), and the design from step 7, in one Markdown or PDF file plus the code.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Grid and narrow phase | All tests pass, including exact equality with brute force; the `k × c ≥ r` condition explained with a counterexample | Tests pass, explanation missing or vague | Tests fail | 30% |
| Measurement | Timings at three sizes and two densities; growth rates related to `N²` and `N × density`; log-log plot | Timings present, growth not analysed | No timings | 20% |
| Cell size | Three settings measured, all exact, a recommendation backed by numbers | Measured but no recommendation | Missing | 10% |
| Hysteresis | Implementation passes; the 7 m case solved; amplitude-margin rule stated | Implementation passes, rule missing | Fails | 15% |
| Design | Every parameter justified with a number; the crowd case handled with a named technique | Parameters given, some unjustified | Opinion without numbers | 25% |
