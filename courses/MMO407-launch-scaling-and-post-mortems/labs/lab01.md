# MMO407 · Lab 01: Launch funnel and readiness review

**Week:** 1 ([lecture](../lectures/w01-launch-day-anatomy.md))
**Time:** 2 hours in the lab, plus up to 2 hours to finish.
**Work mode:** pairs.
**Counts toward:** the launch plan (50% of the course grade). The readiness review becomes the first page of your week 13 launch plan.

## Objective

Model a launch as a serial pipeline, find its bottleneck, show why a rejecting stage collapses under retries, and turn the numbers into a readiness review with go/no-go criteria that a war room could use on the night.

## Starter materials

- [`lab01-starter/launch_funnel.py`](lab01-starter/launch_funnel.py), Python 3, standard library only. It holds the lecture's stages, arrivals and four plans, a working `backlog` and `apply_kill_switches`, and three stubs:
  - `throughput` (TODO 1), which returns the narrowest stage and the pipeline's throughput.
  - `simulate_retries` (TODO 2), the minute-by-minute retry model from lecture section 3.
  - `availability` (TODO 3), the product of service availabilities from section 4.
- [`lab01-starter/test_launch_funnel.py`](lab01-starter/test_launch_funnel.py) has six tests. All fail on the starter and pass on a correct solution. Run them from inside `lab01-starter/` with `python -m unittest test_launch_funnel.py` (from the repository root, `.venv/bin/python` is the course Python).
- `python launch_funnel.py` prints the lecture's plan table once TODO 1 is done.
- The interactive `examples/w01-launch-funnel.html`, once it is built.

## Steps

### Part A: the pipeline (40 min)

1. Implement `throughput` (TODO 1). Run the tests. `test_lecture_plans` must reproduce the lecture's four-row table exactly.
2. Write a function `best_upgrade(stages, arrivals, costs, budget)` that tries every way to spend a budget on doubling stages (each stage at most once) and returns the plan with the smallest 60-minute backlog, breaking ties by lowest cost. Use these costs, in thousands of dollars per doubling: patch check 20, authentication 60, character select 90, world entry 120. Report the best plan for budgets of 60, 120, 180 and 300 at the lecture's arrivals of 1,000 per minute.
3. Repeat step 2 at arrivals of 1,500 per minute. Explain in three sentences why the best plan changes, naming the bottleneck before and after each upgrade.

### Part B: retries and collapse (40 min)

4. Implement `simulate_retries` (TODO 2) and run all tests. Your minutes 1, 3, 5 and 6 must match the lecture's table.
5. Plot successes per minute for 30 minutes for rejection costs 0, 0.02, 0.05 and 0.1 (any plotting tool, or a text table). For each cost, record the first minute at which successes fall below 300 per minute. Explain why a cost of 0 never collapses and why even a small positive cost eventually does while arrivals exceed capacity.
6. Clients can back off. Use the `retry_s` argument to find the smallest retry interval for which successes stay above 500 per minute for all 30 minutes with rejection cost 0.1. Then run the same interval for 120 minutes and describe what happens. Explain in three sentences why no retry interval rescues a stage whose capacity is below the arrival rate, and what replacing the error with a queue changes (MMO302 week 9 covers the jitter that spreads the retries themselves).

### Part C: the readiness review (40 min)

7. Implement `availability` (TODO 3). Your game depends on these services on launch night: patch CDN 0.999, authentication 0.998, entitlement 0.997, character select 0.998, world servers 0.995, store 0.99, friends 0.99, voice chat 0.98, achievements 0.99, anti-cheat handshake 0.997. Compute the chance all are up, and the expected minutes of a 12-hour launch night when at least one is down.
8. Choose which services go behind kill switches and recompute. Justify every service you leave in the required set.
9. Write the readiness review (one page). It must contain the capacity table with the expected bottleneck marked, your chosen upgrade plan with its cost, the kill-switch list with a named owner role for each, and at least four go/no-go criteria written as measurable conditions (for example "authentication p99 under 500 ms at 1.2 × forecast arrivals in the final rehearsal").

## Deliverable

- `launch_funnel.py` passing all six tests, plus your code for steps 2, 3, 5, 6 and 8.
- A short results sheet with the tables and plots from steps 2 to 8.
- The one-page readiness review from step 9.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Pipeline model (steps 1 to 3) | Tests pass; best plans correct at both arrival rates; bottleneck migration explained with numbers | Tests pass; plans partly correct or explanation vague | Tests fail | 25 |
| Retry model (steps 4 to 6) | Tests pass; rejection-cost threshold found; jitter result correct and its limit explained | Tests pass; one of steps 5 or 6 missing or unexplained | Tests fail | 25 |
| Availability and kill switches (steps 7 and 8) | Correct figures; every required service justified | Correct figures, weak justification | Missing or wrong | 15 |
| Readiness review (step 9) | All four parts present; go/no-go criteria measurable; owners named by role | Parts present but criteria vague | Missing | 30 |
| Code quality | Readable, runs first time | Runs with minor fixes | Does not run | 5 |
| **Total** | | | | **100** |
