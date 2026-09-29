# MMO306 · Lab 13: A roadmap simulator

**Week:** 13 ([lecture](../lectures/w13-content-budgets-and-cadence-planning.md))
**Time:** 2 hours in the lab, plus up to 3 hours to finish.
**Work mode:** pairs.
**Counts toward:** final dungeon (60%). The roadmap and budget you produce here become the "cadence and budget" page of your final dungeon document.

## Objective

Implement the week 13 model for one drop, then simulate a whole two-year roadmap in which late teams start their next drop late and drops ship in order. Use the simulator to choose a team count and cadence for your final dungeon's studio, and defend the choice with numbers for both the team and the players.

## Starter materials

All in [`lab13-starter/`](lab13-starter/). Standard-library Python 3, run with `.venv/bin/python` from the repository root or any Python 3.9+.

- [`roadmap.py`](lab13-starter/roadmap.py), with seven functions to write: `pert`, `on_time_chance`, `mean_days_late`, `teams_needed`, `fastest_cadence`, `release_days` and `drought_days`, plus the Monte Carlo driver `simulate`. Each docstring gives the exact rule the tests expect.
- [`test_roadmap.py`](lab13-starter/test_roadmap.py), five tests. They check the lecture's table (on time 77.3% for two teams at 175 days, 16.0 days late for the mean plan), the staircase of teams needed, four hand-built release schedules (a late team starting late, a finished drop held behind a late one, early drops waiting for their date), drought totals, and that the simulator shows the cascade. All fail on the starter.
- The [interactive](../examples/w13-cadence-promise.html) for checking single-drop numbers.
- Your lab 01 `locust.py` (week 1) for exhaustion times.

## Steps

### Part A: one drop (25 min)

1. Implement `pert`, `on_time_chance` and `mean_days_late`. Check them against the section 2 table of the lecture.
2. Implement `teams_needed` and `fastest_cadence`. Print the staircase for cadences from 90 to 365 days in steps of 5, at 90% on time. Mark the cadences where adding one more day of `P` saves a whole team.

### Part B: the whole roadmap (45 min)

3. Implement `release_days`. Work the three small schedules in `test_release_days` by hand first, on paper, then make the code agree.
4. Implement `drought_days`. For the schedule `[160, 350, 480, 670]`, compute the drought for a player with `T = 140` by hand (answer: 120 days) before running it.
5. Implement `simulate` and run the file. For the mean plan (`n = 2, P = 160`) you should see about a third of drops on time and an average slip near 40 days, much worse than the single-drop 50% and 16 days. Explain the gap in two sentences using the two cascade rules from lecture section 4.
6. For `n` from 1 to 4 and the fastest 90% cadence of each, compare the single-drop on-time chance with the simulated roadmap share. Report the table.

### Part C: your studio (50 min)

7. Write a three-point estimate for one major drop of your final dungeon's game (a dungeon or raid tier with its surrounding content). Give one sentence of reasoning for each of `a`, `m` and `b`. Your `b` must be at least as far from `m` as your `a`, unless you can say why your project is different.
8. Your studio can fund up to 4 major-drop teams. Using `simulate`, find the plan (`n`, `P`) that reaches at least 90% of drops on time over a 12-drop roadmap with the fewest teams, and among those the shortest cadence.
9. Use the week 1 population from lab 01 (`players.csv`) and your drop's `C` and `r` to compute `T` for p50, p90 and p99. Using `release_days` on one simulated roadmap that includes at least one late drop, report each percentile's total drought over two years.
10. Place one minor drop per cycle on your roadmap. Say on which day of the cycle it lands, which percentile it serves, and what kind of content it is (week 8, 9 or 11).
11. Pick one late drop from step 9 and decide between slip and cut using the lecture's section 3 formulas. Report the extra drought for p50, p90 and p99 under each option and state your decision.

## Deliverable

- The completed `roadmap.py` with all tests passing, and a script `lab13_report.py` that prints every table in your report.
- A report of at most 2 pages: the staircase from step 2, the single-drop versus roadmap table from step 6, your estimate and chosen plan (steps 7 and 8), the drought table and minor-drop plan (steps 9 and 10), and your slip-or-cut decision with its numbers (step 11).
- A one-page roadmap drawing for two years: major drops with their on-time chance, minor drops, and the p50 and p90 drought lines.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Model and simulator (Parts A and B) | All five tests pass; hand checks shown; cascade gap explained with both rules | Tests pass, explanation vague | Tests fail | 30 |
| Estimate and plan (steps 7 and 8) | Estimate reasoned and lopsided for a stated reason; plan meets 90% with fewest teams, found by search | Plan meets target but not minimal, or estimate unreasoned | No simulation behind the plan | 25 |
| Players (steps 9 to 11) | Droughts per percentile from a real simulated roadmap; minor drops aimed at a named percentile; slip-or-cut decided with numbers | Numbers present, reasoning thin | Missing | 25 |
| Roadmap drawing and writing | Readable one-page roadmap; report under 2 pages, every claim backed by a printed number | Roadmap present but hard to read | Missing | 20 |
| **Total** | | | | **100** |
