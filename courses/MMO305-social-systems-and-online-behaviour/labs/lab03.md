# MMO305 · Lab 03: Simulating strangers

**Week:** 3 · **Time:** 2 hours in lab plus about 2 hours at home · **Weight:** part of the reading responses (20%); the model feeds the final social system design (50%)

## Objective

Check the week 3 binomial model against a simulated matchmaker, then add the cheapest bonding feature a matchmaker can have, a "queue again with this group" option, and measure how much of it you need before a player in a large pool makes acquaintances again. You will use the formulas from [week 3](../lectures/w03-forced-vs-voluntary-grouping.md), section 3.

## Starter materials

- [`lab03-starter/matchmaker.py`](lab03-starter/matchmaker.py): Python 3, standard library only. `simulate(N, r, m=4, k=3, s=0.0, seed=305)` shuffles the whole pool of `N` players into groups of `m + 1` each run, counts how often each pair meets, and returns the mean distinct people met and the mean acquaintances (partners met at least `k` times) per player. Two parts are left for you, marked TODO: the binomial `formula` and the requeue rule for `s > 0`.
- Running `python3 matchmaker.py` prints the baseline for `N = 60, 200, 1000` with `r = 20`. `python3 matchmaker.py 500 30` runs one case.
- `N` must be a multiple of `m + 1` (the script checks). Use 60, 200, 500, 1000, 2000 and 5000 for 5-player groups.
- A spreadsheet or plotting library for one chart.

## Steps

1. **Run the baseline.** Record the output for the three default pool sizes.
2. **Write the formula.** Implement `formula(N, r, m, k)` returning `D` and `A` from week 3. Compare it with the simulation for `N = 60, 200, 1000` and `r = 20`. Where they differ, run the simulation with 10 different seeds and average. Explain in two sentences why a single seed at `N = 60` can be further from the formula than a single seed at `N = 1000`.
3. **Sweep.** For `N` in {60, 200, 500, 1000, 2000, 5000} and `r` in {20, 60}, tabulate `D` and `A` from the formula. Plot `A` against `N` on a log x-axis, one line per `r`.
4. **Requeue.** Implement the requeue rule. At the start of each run after the first, each group from the previous run is kept intact with probability `s` (they chose "queue again together"); everyone else is shuffled into new groups. Run `N = 200` and `N = 5000` with `s = 0.25` and `s = 0.5`, `r = 20`.
5. **Find the threshold.** For `N = 5000` and `r = 20`, find the smallest `s` (to two decimal places, averaging 5 seeds) at which the mean player makes at least 3 acquaintances.
6. **Cost.** Requeued groups meet fewer new people. Report `D` alongside `A` for your threshold `s`, and say how many fewer distinct people a player meets than with `s = 0`.

## Deliverable

Your completed `matchmaker.py`, the tables from steps 1 to 6, the chart from step 3, and a recommendation of about 300 words to a producer who wants cross-server matchmaking for a weekly dungeon "without killing guild recruitment." State the pool size, the requeue feature and the target `s` you would aim for, with numbers, and one risk (for example, cliques that never admit newcomers).

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Formula | Correct `D` and `A`, matches simulation averages, seed variance explained | Correct formula, no explanation | Wrong or missing | 25% |
| Sweep and chart | Full table, labelled log-scale chart, cliff identified | Table complete, chart unclear | Incomplete | 15% |
| Requeue rule | Implemented correctly, results for both `N` and both `s` | Implemented, one case missing | Not working | 20% |
| Threshold and cost | Threshold `s` found with averaging, cost in `D` reported | Threshold found from one seed | Missing | 15% |
| Recommendation | Specific pool, feature and target `s` with numbers, a real risk named | Recommendation with few numbers | Opinion without numbers | 25% |

<details>
<summary>Instructor check values</summary>

- Baseline, seed 305: `N = 60`: `D` 44.43, `A` 8.30. `N = 200`: 66.81, 1.35. `N = 1000`: 77.02, 0.07. `N = 500, r = 30`: 106.75, 0.93.
- Formula (`r = 20`): `N = 60`: `D` 44.51, `A` 8.87. `N = 200`: 66.42, 1.43. `N = 1000`: 77.02, 0.07. `N = 500, r = 30`: `D` 107.04, `A` 0.89. Averaging 20 seeds gives 44.42 and 9.01 at `N = 60`, and 66.37 and 1.44 at `N = 200`.
- Why seeds matter more at small `N`: the mean is taken over only 60 players, and their meetings are linked (if A meets B often, B meets A often), so one seed is a small, correlated sample. At `N = 1000` there are many more nearly independent players.
- Requeue, seed 305, `r = 20`: `N = 200`, `s = 0.25`: `D` 52.27, `A` 6.37; `s = 0.5`: 38.64, 10.38. `N = 5000`, `s = 0.25`: 61.08, 3.38; `s = 0.5`: 41.80, 9.62. With requeue, acquaintances depend far less on `N`.
- Threshold at `N = 5000`, `r = 20`, 5 seeds: `s = 0.22` gives 2.85, `s = 0.23` gives 3.10, so about `s = 0.23`. Its `D` is about 62, against about 79 with `s = 0`, so a player meets roughly 17 fewer new people a month.

</details>
