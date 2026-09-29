# MMO308 · Lab 13: Incident analysis and a blameless postmortem

**Week:** 13 ([lecture](../lectures/w13-incident-response.md))
**Time:** 2 hours in the lab, plus up to 2 hours to finish.
**Work mode:** pairs.
**Counts toward:** analytics labs (40% of the course grade).

## Objective

Measure what a synthetic Saturday-evening incident cost in player-hours, implement the lecture's revert-first versus fix-forward model, confirm it by simulation, and turn the result into a blameless postmortem whose action items are ranked by player-hours saved per engineer-day.

## Starter materials

- [`lab13-starter.py`](lab13-starter.py): Python 3, standard library only. It contains a data generator `make_evening()` that returns last week's and today's concurrent users every 15 minutes from 18:00, with a patch at 19:15 that breaks logins. It also has stubs for every function you write and nine tests that print PASS or FAIL. Run it first: all nine fail.
- The [revert-or-fix interactive](../examples/w13-revert-or-fix.html) to check your curves.
- The lecture's default parameters: `r = 30`, `p = 0.25`, `F = 45`, `R = 20`, `q = 0.6`, `N = 40,000`.

Run with `.venv/bin/python courses/MMO308-live-operations-analytics-and-experimentation/labs/lab13-starter.py` from the repository root. The script exits with status 0 only when every test passes.

## Steps

### Part A: measure the damage (35 min)

1. Implement `scaled_baseline`. Scale last week's series by today's total over last week's total in a pre-incident window. Test A1 checks it against the lecture's 30-minute table.
2. Implement `lost_player_hours`, returning gross loss, rebound and net loss from the incident start to the end of the series. Test A2 checks the lecture's 59,195 / 2,246 / 56,949.
3. Run both on `make_evening()` with the pre-incident window 18:00 to 19:15 (samples 0 to 4). Report gross, rebound and net loss. Then redo it with no scaling (scale factor 1) and report how much the unscaled baseline over- or understates the loss, in player-hours and percent.
4. Plot baseline and today on one chart and shade the gap. Mark the patch time and the rebound.

### Part B: the decision model (30 min)

5. Implement `expected_fix_forward`, `expected_revert_first`, `q_star` and `still_down`. Tests B1 to B4 use the lecture's numbers.
6. Make a table of `q*` for `p` in {0.5, 0.25, 0.1, 0.05} and `R` in {2, 20, 90}. In two sentences, say which cell describes a team with a kill switch and a hard bug, and what it should do at `q = 0.2`.
7. Suppose the incident in Part A had a revert available with `R = 20`, and the on-call engineer believed `q = 0.3`. Using `p = 0.25`, `r = 30` and `F = 45`, compute the expected player-hours saved by reverting first, with `N` equal to the average of the scaled baseline during the outage.

### Part C: simulate (25 min)

8. Implement `simulate`. Test C1 checks that 20,000 simulated incidents match the expected outages and the four-hour tail.
9. Plot the empirical survival curve of each strategy over the formula's step curve for the default parameters. Report the simulated 90th-percentile outage for each strategy.
10. The model assumes each diagnosis round succeeds with the same `p`. Change `simulate` (in a copy, not the tested function) so that `p` rises by 0.05 each round, capped at 0.6, as if the team learns. Report how the gap between the two strategies changes, and explain why in two sentences.

### Part D: postmortem (30 min)

11. Implement `rank_actions` (test D1).
12. Write a one-page blameless postmortem for the Part A incident. Invent the cause yourself (the patch or something else), and keep it consistent with the data. Include a timeline with the four clocks from lecture section 1, the measured impact, what was tried with the `q` held at each step, contributing causes with no person blamed, and five action items. For each action item give the model parameter it moves, your estimate of player-hours saved per year and engineer-days, then rank them with your function.

## Deliverable

- The completed `lab13-starter.py` with all nine tests passing, plus any copies you made for step 10.
- A PDF of at most 4 pages: the Part A numbers and chart, the Part B table and answers, the Part C plot and step 10 result, and the postmortem.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Impact measurement (Part A) | Tests A1 to A3 pass; scaled and unscaled losses reported with the difference explained; clear chart | Numbers correct but no comparison or chart | Tests fail | 20 |
| Decision model (Part B) | Tests B1 to B4 pass; `q*` table correct; step 7 answered in player-hours with the method shown | Table or step 7 incomplete | Tests fail | 25 |
| Simulation (Part C) | Test C1 passes; overlay plot; 90th percentiles; learning-team variant explained | Simulation runs, analysis thin | Missing | 20 |
| Postmortem (Part D) | Blameless, timeline with four clocks, action items each mapped to a parameter and ranked with numbers | Postmortem present but blames a person or has vague actions | Missing | 25 |
| Clarity | Every number has a unit and a source cell or function | Some numbers unexplained | Unreadable | 10 |
| **Total** | | | | **100** |
