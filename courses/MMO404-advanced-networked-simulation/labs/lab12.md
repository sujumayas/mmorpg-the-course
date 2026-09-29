# MMO404 · Lab 12: AI budget

**Week:** 12 · **Time:** 2 hours in lab plus about 3 hours at home · **Weight:** part of the labs (40%)

## Objective

Turn the [week 12 lecture](../lectures/w12-ai-at-scale.md) into a tool that prices a zone's AI before launch. You implement tiered think rates and the coverage model, find each monster's nearest player with a grid and time it against brute force, then build the two schedulers from section 3: phasing by id, which flattens the steady state, and a budgeted accumulator, which survives a sudden rush. You finish with an AI budget for a zone whose players spread out on quest nights and gather once a week for a world boss.

## Starter materials

Folder [`lab12-starter/`](lab12-starter/README.md). Standard library Python only. Run with `.venv/bin/python` from the repository root or any Python 3.10+.

- `ai_budget.py`: the lecture's zone (4 km square, 10,000 monsters, tiers of 50, 150 and 400 m at 10, 2 and 0.2 thinks per second, 20 µs per think), a seeded world builder `make_world` and a brute-force `nearest_brute` (given), and TODOs for `tier_rate`, `model_tier_counts`, `cost_ms_per_s`, `nearest_grid`, `thinks_per_tick` and `budgeted_tick`. It has `--check`, `--measure` and `--sweep` modes.

## Steps

1. **By hand first.** Before coding, compute the tier counts and cost for one isolated player from density and ring areas, and for 100 spread players from the coverage formula. Keep both for your report.
2. **The model.** Implement `tier_rate`, `model_tier_counts` and `cost_ms_per_s`. Run `--check` until it stops at `nearest_grid`. Explain in two sentences why `model_tier_counts(1)` gives 265 far-tier monsters where the ring area gives 270.
3. **Nearest player on a grid.** Implement `nearest_grid` with cells of side 400 m, checking only the 3 × 3 block around each monster. Run `--measure` and report both timings. Then time both again with 1,000 spread players (edit `measure` or write a short script) and explain the change with Big-O.
4. **Where players stand.** Run `--sweep ai.csv` and plot cost against player count, with the 250 ms/s budget line. Find the largest number of spread players the default tiers can afford. Then use `simulated_counts` to fill in a table of cost for 200 players in 1, 2, 5, 10, 20 and 50 groups. In three sentences, explain why grouping helps AI and hurts replication (week 1).
5. **Flatten the ticks.** Implement `thinks_per_tick`. For the 200-spread layout, build the list of periods (1 tick for near, 5 for mid, 50 for far, 0 for dormant) and plot 100 ticks in step and phased. Report the worst tick in ms both ways.
6. **Survive a rush.** Implement `budgeted_tick`. Simulate a raid teleporting into a dormant area: 500 monsters jump to the near tier on tick 0, on top of the 2,019 phased thinks per tick you already have, with a budget of 2,500 thinks per tick. Give near-tier monsters weight 10, mid 2 and far 0.2. Report how many ticks it takes until every promoted monster has thought at least once, and the longest any far-tier monster waited.
7. **Your AI budget.** A 3 km × 3 km zone holds 6,000 monsters and a budget of 150 ms/s at 20 µs per think. On quest nights 150 players spread over it. Once a week, 300 players gather at a world boss. Write a one-page budget: the tiers you choose (near radius at least 40 m), the cost on both nights, the worst tick with phasing, the reaction delay of each tier and the distance a player running at 7 m/s covers in one think interval, and how often tiers are recomputed.

## Deliverable

Your finished `ai_budget.py`, `ai.csv` with the chart from step 4, the grouping table, the tick plots from step 5, the rush script from step 6, and a report (PDF or Markdown, at most three pages) with the hand calculations from step 1, the answers to steps 2 to 6 and the budget from step 7. Submit before the week 13 lecture.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Cost model | `--check` passes; hand numbers match; the 265 against 270 gap explained by the exponential's overlap term | Passes, explanation missing | Fails the check | 20% |
| Nearest player | Grid agrees with brute force; timings for 200 and 1,000 players explained with Big-O | Correct, timing or explanation missing | Brute force only | 15% |
| Player layout analysis | Chart with budget line and affordable player count; grouping table; replication contrast stated with week 1's pair term | Chart and table, explanation thin | Step skipped | 15% |
| Scheduling | Worst tick in step and phased reported in ms; rush simulated with catch-up ticks and longest far-tier wait | One scheduler analysed | Fails the check | 20% |
| AI budget | Tiers fit both nights with numbers; delays and running distances per tier; recompute rule stated and justified | Numbers present, choices unjustified | Budget missing or copied from the lecture | 25% |
| Writing | Plain, one idea per paragraph, units everywhere | Mostly clear | Hard to follow | 5% |
