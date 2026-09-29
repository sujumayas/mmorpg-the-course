# MMO407 · Lab 09: The crisis communications kit

**Week:** 9 ([lecture](../lectures/w09-communication-during-crises.md))
**Time:** 2 hours in the lab, plus up to 3 hours to finish.
**Work mode:** pairs.
**Counts toward:** the launch plan (50% of the course grade). Your kit becomes the "communications" section of your final launch plan.

## Objective

Build the lecture's ETA forecaster, test extension policies on a larger outage log split by kind of incident, and write the communications kit a small live team needs before launch: a signed-off cost ratio, update templates for four kinds of crisis, and a channel plan.

## Starter materials

- [`lab09-starter/eta.py`](lab09-starter/eta.py), Python 3, standard library only. It provides `load`, `quantile`, `misses` and the lecture's log, and five stubs:
  - `cost` (TODO 1) and `best_eta` (TODO 2), the expected cost of an announcement and the critical-ratio pick.
  - `mean_left` (TODO 3), the average time still to go for outages that have lasted `t`.
  - `fixed_extensions` (TODO 4), Policy A: the median, then a fixed step after each miss.
  - `reforecast` (TODO 5), Policy B: the critical-ratio quantile of the outages still running.
- [`lab09-starter/outages.csv`](lab09-starter/outages.csv), an invented log of 200 unplanned outages with a `kind` column (`deploy`, `database`, `network`). The numbers are synthetic, drawn to resemble the shapes real incident logs have.
- [`lab09-starter/test_eta.py`](lab09-starter/test_eta.py) has seven tests. All fail on the starter and pass on a correct solution. Run them from inside `lab09-starter/` with `python -m unittest test_eta.py`.
- The interactive `examples/w09-eta-announcer.html`, once it is built.

## Steps

### Part A: the forecaster (35 min)

1. Implement TODOs 1 to 3 and run the tests. `best_eta` must return 105 for the lecture log at 2:1, and `mean_left` must give 116.5, 153.3 and 240.0 at 0, 60 and 240 minutes.
2. Plot `cost(T)` for `T` from 0 to 600 on the lecture log for ratios 1:1, 2:1 and 4:1, and mark each minimum. Confirm each minimum equals `best_eta`.
3. Show numerically why the minimum sits at the critical ratio. For `T = 100` and `T = 101`, compute the change in cost and compare it with `c_early × P(D ≤ 100) − c_late × P(D > 100)`.

### Part B: policies on a real-sized log (40 min)

4. Implement TODOs 4 and 5 and run all tests.
5. Load `outages.csv`. For each kind and for the whole log, report the median, the 2:1 announcement, and `mean_left` at 0, 30, 60, 120 and 240 minutes. Which kinds have a growing time-to-go and which a shrinking one? What does that mean for the size of the first extension?
6. Evaluate three policies on every outage in the CSV: Policy A with steps of 30 and 60 minutes, and Policy B. Forecast each kind from its own log (split by kind), then repeat forecasting every outage from the whole log. Report the average and the worst number of broken promises for each, and the average minutes by which the final announcement overshoots the real end.
7. Split the CSV in half by `id` (odd and even). Fit the announcement on one half and evaluate it on the other. How much worse is the miss rate out of sample? What does this tell you about using a log of 20 incidents?

### Part C: the kit (45 min)

8. Choose your team's cost ratio for three situations (weekday evening outage, weekend launch-night outage, planned maintenance) and justify each in one sentence. Compute the announcement each implies for a database incident.
9. Write four update templates with the five parts from the lecture's section 3, one each for an outage, a rollback, an economy exploit and a suspected security breach. Mark the fields a person fills in on the night, and include the next-update line in every one.
10. Write a channel plan: the source of truth, every other channel that links to it, which of them survive if your own domain is down, and who may post.
11. Run the kit on the lecture's in-class scenario (European login failure, Friday 19:10 UTC). Produce the three updates it generates, using your code for any times.

## Deliverable

- `eta.py` passing all seven tests, plus your code for steps 2, 3 and 5 to 8.
- The plot from step 2 and the tables from steps 5 and 6.
- The communications kit (at most three pages): cost ratios with justifications, the four templates, the channel plan and the three scenario updates.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Forecaster (steps 1 to 3) | Tests pass; plot correct; marginal-cost check matches the critical ratio | Tests pass; check missing | Tests fail | 20 |
| Policies (steps 4 to 7) | All policies evaluated by kind and pooled; residual shapes explained; out-of-sample drop measured and interpreted | Policies evaluated without the by-kind split or the out-of-sample test | Missing | 30 |
| Cost ratios (step 8) | Three ratios justified, announcements computed | Ratios without justification | Missing | 10 |
| Templates and channel plan (steps 9 and 10) | All four templates have all five parts, with no promise the log says is likely to break; channel plan survives a domain outage | Templates complete but channel plan shares a failure with the game | Missing | 25 |
| Scenario run (step 11) | Three updates generated from the kit with computed times | Updates written without the model | Missing | 10 |
| Code quality | Readable, runs first time | Runs with minor fixes | Does not run | 5 |
| **Total** | | | | **100** |
