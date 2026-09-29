# MMO404 · Lab 03: Partitioning a crowded world

**Week:** 3 · **Time:** 2 hours in lab plus about 4 hours at home · **Weight:** part of the labs (40%)

## Objective

Partition a seeded 3,000-player world across 16 servers and measure what each scheme costs, using the load model from the [week 3 lecture](../lectures/w03-spatial-partitioning-at-scale.md). You implement the crowd-split formula and two recursive bisection partitioners, reproduce the lecture's tables, and then write a rebalancing rule that follows moving crowds without handoff storms.

## Starter materials

Folder [`lab03-starter/`](lab03-starter/README.md). Standard library Python only. Run with `.venv/bin/python` from the repository root or any Python 3.10+.

- `partition.py`: the world generator `make_world`, a grid-based pair finder `pairs`, the static 4 × 4 partition `static_grid` and the load function `loads` are given. You implement `crowd_split_us`, `kd_headcount` and `kd_by_load`. It has `--check`, `--compare` and `--crowd` modes.

## Steps

1. **The crowd model.** Before coding, compute by hand the per-server load for a 300-player crowd split across 4 servers. Implement `crowd_split_us` and run `python partition.py --crowd 300`. Then find, with a short loop of your own, the smallest number of servers that fits crowds of 150, 200, 300 and 600 players in 50 ms. Compare with the lecture's table.
2. **Headcount bisection.** Implement `kd_headcount` exactly as its docstring says (x first, left gets `len × left // servers` players). `--check` requires a busiest server of 64.7 ms and 28.7% of pairs cut.
3. **Load bisection.** Implement `kd_by_load`. The check requires the busiest server under 50 ms and an imbalance under 2.5. Run `python partition.py --compare` and copy the three rows into your report.
4. **Slack.** Rerun `kd_by_load` with `slack` = 0.0, 0.05, 0.15 and 0.30. For each, report the busiest server, the mean load and the cut. Explain what slack buys and what it costs.
5. **Picture it.** Plot the world with each partition's region borders and colour each region by its load (any plotting tool; a scatter plot with rectangles is enough). Mark which regions are over budget.
6. **Moving crowds.** Write a function that moves each hot spot's centre 20 m per step in a fixed random direction and regenerates the world for 30 steps (keep the seed, move only the centres). At each step, rerun `kd_by_load` from scratch and count how many players changed owner since the previous step (the churn). Then write a rebalancing rule with hysteresis: keep the old partition while its imbalance stays under 2.0, and repartition only when it rises above that. Report total churn, the worst busiest-server load and the number of repartitions for both approaches.

## Deliverable

Your finished `partition.py` plus the code for step 6, the plots from step 5, and a report (PDF or Markdown, at most four pages) with the hand calculation and table from step 1, the compare output, the slack table and explanation from step 4, and the churn comparison from step 6 with a recommended rule. Submit before the week 4 lecture.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Crowd model | `crowd_split_us` correct; hand calculation agrees; servers-needed table matches the lecture | Correct with a small arithmetic slip in the report | Wrong formula | 15% |
| Partitioners | `--check` passes; both k-d functions follow their docstrings; no hard-coded results | One partitioner passes | Neither passes | 30% |
| Slack analysis | Four rows reported; trade-off between cut and balance explained with the numbers | Rows reported, explanation thin | Missing | 15% |
| Visualisation | Borders and load colours clear for all three partitions; over-budget regions marked | Plots present but hard to read | Missing | 10% |
| Rebalancing | Churn measured for both approaches; hysteresis rule reduces churn with the busiest server still reported; recommendation justified | Measured, recommendation unjustified | Missing | 25% |
| Writing | Plain, one idea per paragraph, units everywhere | Mostly clear | Hard to follow | 5% |
