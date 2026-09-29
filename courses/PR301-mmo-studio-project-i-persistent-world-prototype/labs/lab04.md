# PR301 Lab 04: Login soak test and sprint 1 focus factor

**Week:** 4 (sprint 1 mid-sprint session), finished at the sprint 1 review at the start of week 5. **Guide:** [week 4](../lectures/w04-sprint-1-review.md). **Team lab**, submitted once per team.

## Objective

Decide whether your login path is done, with numbers. You will set a failure-rate threshold from the alpha weekend's exposure before running any test, run the login soak under at least two separate conditions, compute a 95% upper bound for each, and measure the focus factor that sprint 2 will plan with.

## Starter materials

In [`labs/lab04-starter/`](lab04-starter/):

- `check_soak.py`. Standard library only. Run it with `.venv/bin/python check_soak.py soak.csv --threshold 0.01`. It prints the attempts a clean run needs, then each condition's 95% upper bound (the rule of three when there are no failures, the Wilson upper limit otherwise) and `DONE` or `NOT DONE`. It ends with `PASS` or `NOT READY` and exits with code 1 unless every condition is done.
- `soak.csv`. The three *Saltmarsh* conditions from the guide: `condition`, `attempts`, `failures`.

## Steps

1. **Warm-up (10 minutes).** Run the checker on the starter file and confirm 5.99%, 1.80% and 1.50%, all `NOT DONE`. Replace the rows with the rerun from the guide (cycled 400 and 0, burst 300 and 0) and confirm `PASS`.
2. **Threshold first.** Estimate the alpha's login attempts `E` (players times logins each) and the failures you can tolerate `k`. Write `p* = k / E` into your definition of done before running anything.
3. **Soak.** Run at least a cycled condition (bots log in and out repeatedly, with overlap) and a burst condition (all bots at once). Add a "restart, then all reconnect" condition if you can. Keep each condition's counts separate.
4. **Check.** Run the checker at your threshold. For every failure, find the cause in the logs and file a defect with the bot condition that reproduces it.
5. **Focus factor.** Compute sprint 1's `f` from the estimated hours of stories that met the definition of done and the hours people actually had. Forecast sprint 2's team and per-person capacity.

## Deliverable

In `production/sprint1/`. The midpoint soak and its defects are due at the end of the week 4 session. The final soak on the tagged build and `review.md` are due at the sprint 1 review at the start of week 5.

- `soak.csv` and the checker output saved as `soak-output.txt`, with the threshold and its exposure calculation at the top.
- `review.md`: goal answered yes or no, the restart result against the persistence map, done and not-done stories, the focus factor and the sprint 2 forecast.
- Defect tickets linked from `review.md`.

**Checkable output:** the instructor reruns `check_soak.py` at your stated threshold. A `NOT READY` result is acceptable for this lab if `review.md` answers the goal "no" and every failing condition has a linked defect. A `PASS` must match the logs.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Threshold | 4 | Set from exposure before the soak ran, and written in the definition of done |
| Conditions | 4 | At least cycled and burst, counted separately, never pooled |
| Checker and logs | 4 | Rerun matches; counts can be traced to the bot logs |
| Defects | 3 | Every failure has a cause or a named investigation, and a reproducing condition |
| Focus factor | 3 | Uses only stories that met the definition of done in sprint 1, and actual available hours |
| Review record | 2 | Goal answered yes or no; restart result recorded |
