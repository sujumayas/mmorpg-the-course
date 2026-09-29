# PR301 Lab 06: Tick budget worksheet

**Week:** 6 (sprint 2 mid-sprint session; the sprint 2 review is at the start of week 7). **Guide:** [week 6](../lectures/w06-sprint-2-review.md). **Team lab**, submitted once per team.

## Objective

Find out how many mobs your world server can hold at the load-test crowd from week 2, and decide what to do about it before sprint 3 starts. You run four bot configurations, fit the tick cost model from the guide, compute the largest mob count that meets both week 2 limits (the CPU budget on the mean tick and your decision record's p99 trigger), and compare a content option with an engineering option before touching the architecture.

## Starter materials

In [`labs/lab06-starter/`](lab06-starter/):

- `check_tick.py`. Standard library only. Run it with `.venv/bin/python check_tick.py runs.csv claims.txt`. It fits `t = a + g + cM + dPM` from runs A to D at the load-test crowd, prints the coefficients, the two mean-tick limits, the planned world's mean and p99 and `M_max`, then `PASS` or `NOT READY` (exit code 1).
- `runs.csv`. The four *Saltmarsh* runs from the guide's worked example.
- `claims.txt`. Tick rate, CPU budget, p99 limit, planned mob count, your computed `M_max`, the chosen option, its fallback, and `option_mean_ms`, the mean tick the chosen option is modelled to give at the planned mobs. Four lines are blank. The checker prints `NOT READY` unless the planned mobs are at or below `M_max` or `option_mean_ms` meets both limits.

## Steps

1. **Warm-up (10 minutes).** Fill in the blank lines of `claims.txt` using the guide's numbers (option 2, the grid, modelled at 56.0 ms) and run the checker until it prints `PASS`. Your `M_max` must match the guide's 178. Then try the world-boss row's 60.0 ms and read the error.
2. **Tick logging.** Make sure your server writes one line per tick: tick number, duration in ms, players online, mobs spawned. Add a script (any language) that reads a log, drops the first two minutes and prints the mean and the 99th percentile.
3. **Four runs.** Run your bots through the real client protocol in the 2 × 2 design: A (no bots, no mobs), B (your week 2 load-test crowd, no mobs), C (no bots, your planned mob count), D (both). Use week 2's worst-case layout for B and D. At least ten minutes each after warm-up.
4. **Fit.** Replace `runs.csv` with your four rows. Fill `claims.txt` with your tick rate, the CPU budget and p99 trigger from your week 2 decision record, and your planned mobs. Run the checker and copy `M_max` into the claims. In `tick-budget.md`, compare the fitted `g` with your week 2 prediction for player deliveries at that crowd.
5. **Options table.** Model at least two options in `tick-budget.md`, one that changes content (fewer mobs, fewer spawn points) and one that changes the simulation (grid-limited wake checks, a slower AI tick for idle mobs). For each, give the assumption it depends on and how you will measure it. Model an architecture change (more processes) only if both fail.
6. **Spread run.** Run a fifth configuration with the same players and mobs as D but bots spread evenly over the zone. Add it to `runs.csv` as run `E`. The checker prints it but does not fit it. Say in one sentence whether it changes your decision.
7. **Decision.** Fill `chosen_option`, `fallback` and, if your planned mobs exceed `M_max`, the chosen option's modelled mean in `option_mean_ms`. Add the chosen story to the sprint 3 backlog with a size in hours and a done condition that names a load and a percentile. Update your week 2 decision record with the trigger result.

## Deliverable

In `production/week06/` in the team repository:

- `runs.csv` and `claims.txt` that pass `check_tick.py`, with its output saved as `check-output.txt`.
- The five raw tick logs, or a link to where they are stored.
- `tick-budget.md`: the options table, the assumptions, the spread-run result, the decision and the backlog item ID.

**Checkable output:** the instructor reruns `check_tick.py` on your two files. It must print `PASS` and exit with code 0, and the numbers in `tick-budget.md` must match its output.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Checker passes | 4 | `PASS` on rerun, output file matches |
| Measurement quality | 4 | Real protocol, moving bots, ten-minute runs, warm-up dropped, p99 from per-tick data |
| Options modelled | 4 | One content and one engineering option, each with the arithmetic shown and its assumption named |
| Spread run | 3 | Run E present and its effect on the decision stated |
| Decision | 3 | Chosen option and fallback recorded; backlog item with size and a measurable done condition |
| Honesty about limits | 2 | Notes where the model may not hold (other crowd sizes, near the budget, the p99 ratio) and compares `g` with week 2 |
