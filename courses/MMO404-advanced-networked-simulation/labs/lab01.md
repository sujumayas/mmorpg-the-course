# MMO404 · Lab 01: Zone capacity

**Week:** 1 · **Time:** 2 hours in lab plus about 3 hours at home · **Weight:** part of the labs (40%)

## Objective

Turn the [week 1 lecture](../lectures/w01-limits-of-the-zone-model.md) tick-cost model into a tool you trust, then use it to plan a launch city. You implement the model, test it against interacting pairs counted on seeded zones, measure how capacity falls as players gather, and show with numbers why a faster server does not fix a crowd.

## Starter materials

Folder [`lab01-starter/`](lab01-starter/README.md). Standard library Python only. Run it with `.venv/bin/python` from the repository root or any Python 3.10+.

- `zone_capacity.py`: constants from the lecture, a seeded zone generator `make_zone`, a brute-force pair counter `brute_pairs`, and TODOs for `aoi_fraction`, `pair_fraction`, `tick_ms`, `capacity` and a grid-based `count_pairs`. It has `--check`, `--measure` and `--sweep` modes.

## Steps

1. **The model.** Before writing code, compute by hand `tick_ms(1000, 0.25)` and `capacity(1.0)` with the lecture's constants. Then implement the four model functions and run `python zone_capacity.py --check`. It will stop at `count_pairs` until step 2.
2. **Counting real pairs.** Implement `count_pairs` with a uniform grid whose cells have side `R`, checking only the 3 × 3 block of cells around each player. `--check` compares it with `brute_pairs`. Time both on `make_zone(2000, 0.1)` with `time.perf_counter()` and report the ratio.
3. **Is the model honest?** Run `--measure`. For each hot-spot share, report measured pairs, model pairs and the ratio. Explain in at most three sentences why the ratio is below 1 when players spread out and near 1 in a crowd. (Hint: where are players whose AOI circle hangs off the map?)
4. **The capacity curve.** Run `--sweep capacity.csv` and plot `capacity` and `capacity_2x_cpu` against `h` on one chart (any tool). Add a third series, the ratio of the two. Mark where the ratio falls below 1.5. What is the ratio at `h = 1`, and why is it close to `√2` rather than 2?
5. **Levers.** For `h = 0.25` and 1,000 players, compute the tick time under each change separately: AOI radius 100 → 60 m; two layers of 500; time dilation to 50% speed (`BUDGET` doubles, so compare tick time with the new budget); CPU twice as fast. Rank them by how far each brings the tick under its budget, and name each one's price for players.
6. **Your city plan.** A launch city is 1.2 km square with a 70 m AOI. Design expects 900 players at evening peak, and a daily event draws 40% of them into one square. Write a one-page plan: the city's capacity outside and during the event, which lever from step 5 you choose for the event, the tick time after your lever, and what players will notice.

## Deliverable

Your finished `zone_capacity.py`, `capacity.csv`, the chart from step 4, and a report (PDF or Markdown, at most three pages) with the hand calculations from step 1, the timing from step 2, the answers to steps 3 to 5 and the plan from step 6. Submit before the week 2 lecture.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Model code | `--check` passes; hand calculations agree with the code | Passes after patching a constant to fit a test | Fails the check | 20% |
| Pair counting | Grid matches brute force exactly; timing ratio reported and explained with `O(n²)` vs `O(n)` | Correct but timing or explanation missing | Brute force only, or counts differ | 15% |
| Model validation | Ratios reported; the edge effect named and explained | Ratios reported, explanation vague | Step skipped | 15% |
| Capacity analysis | Chart with three series; ratio of about 1.43 at `h = 1` explained with the square-root law | Chart present, explanation thin | No chart | 20% |
| Levers and plan | Every tick time computed with units; lever chosen for a stated reason; player-facing cost named | Numbers present, some unjustified | Plan missing or copied from the lecture | 25% |
| Writing | Plain, one idea per paragraph, units everywhere | Mostly clear | Hard to follow | 5% |
