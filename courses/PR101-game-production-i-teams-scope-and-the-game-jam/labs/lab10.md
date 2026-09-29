# PR101 · Lab 10: Bug triage and the backlog model

**Week:** 10, bug tracking and QA basics ([lecture](../lectures/w10-bug-tracking-and-qa-basics.md)).
**Time:** 2 hours in lab, plus up to 2 hours at home with your team.
**Work mode:** code in pairs; parts C and D with your final-project team.
**Weight:** labs feed the final team game (40%). The tracker and forecast you build here are checked again at the week 13 release review.

## Objective

Implement the week 10 triage rules and backlog model in Python so they pass a test suite. Then use them on your own final-project bugs. You finish with a working tracker, five reproducible bug reports and a written forecast of when your build will be stable enough to ship.

## Starter materials

All in [`lab10-starter/`](lab10-starter/). Standard-library Python 3.10 or later, no packages.

- [`triage.py`](lab10-starter/triage.py) holds seven functions. `load_bugs` works. The other six (`priority`, `find_rates`, `backlog`, `peak_days`, `zero_day`, `lincoln_petersen`, `ship_blockers`) raise `NotImplementedError`. Each docstring states the rule.
- [`test_triage.py`](lab10-starter/test_triage.py) has 11 tests built from the lecture's tables and check-yourself answers. On the starter all 11 fail.
- [`bugs_sample.csv`](lab10-starter/bugs_sample.csv) holds 12 bugs with severity, frequency and status, for the ship-blocker test.
- [`forecast.py`](lab10-starter/forecast.py) prints a day-by-day forecast from six numbers at the top of the file. It needs a working `triage.py`.
- Your merged, triaged bug sheet from the week 10 in-class activity.
- The [interactive](../examples/w10-bug-backlog.html), for checking your numbers by eye.

Run the tests from inside the folder:

```
cd lab10-starter
python -m unittest -v
```

## Steps

### Part A: triage rules (30 min)

1. Implement `priority(severity, frequency)` with `P = S + F − 1`, clamped to 1-4. Reject bad input with `ValueError`. Run the tests. `PriorityTests` should pass.
2. Implement `ship_blockers(bugs)`. Before you run the test, work out by hand which of the 12 sample bugs block release and write the list in your README. Then run the test. If your hand list and the test disagree, explain which one was wrong and why.

### Part B: the backlog model (40 min)

3. Implement `find_rates` with half-up rounding. The test includes a case where Python's built-in `round` gives the wrong answer. Find it and say in one sentence why.
4. Implement `backlog`, `peak_days` and `zero_day`. Watch the order. Regressions on day `t` come from fixes on day `t − 1`, and a team cannot fix more bugs than are open.
5. Implement `lincoln_petersen`. Duplicate ids on one tester's list count once.
6. Run the full suite until all 11 tests pass. Then run `python forecast.py` and confirm the defaults print a peak on days 4 and 5 and zero on day 16, as in the lecture.

### Part C: your team's tracker (30 min, team)

7. Move your in-class bug sheet into the tracker your team chose (GitHub Issues, your task board or a shared sheet). Every bug gets the eight fields from lecture section 1, a severity, a frequency band and a priority computed with your `priority` function.
8. Write five full bug reports for bugs in your current final-project build (not the jam build). At least one must be an S1 or S2. Swap with another team. Each team tries to reproduce the other's five bugs from the reports alone and marks each one "reproduced first try", "reproduced after guessing" or "could not reproduce". Revise any report that was not reproduced first try.
9. Export the tracker as a CSV with the columns of `bugs_sample.csv` and run `ship_blockers` on it.

### Part D: stability forecast (20 min, team)

10. Estimate your own inputs: `B0` (open P1 and P2 bugs today), `F0` and `DECAY` (from your first few days of finds, or from the in-class test pass), `CAPACITY` (fixes per day your team can realistically make on this project), and `REGRESSION` (count how many of your fixes so far were reopened or caused a new bug). Put them into `forecast.py` along with your real ship day.
11. Run it. Then run it again with `REGRESSION` raised by 0.15 and with `CAPACITY` raised by 2. Record all three results.

## Deliverable

A zip of `lab10-starter/` containing:

- `triage.py` with all tests passing.
- `forecast.py` with your team's inputs.
- `tracker.csv`, your exported tracker.
- `README.md`, at most two pages, with:
  - the hand-worked ship-blocker list from step 2 and any disagreement explained;
  - the rounding case from step 3;
  - the five revised bug reports and the other team's reproduction marks;
  - a one-page **stability forecast**: your inputs and where each came from, the three forecast runs, the predicted peak and zero days against your ship day, and a recommendation (what the team will cut, fix first or list as known issues). Name the input you trust least.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Tests pass | All 11 pass; code readable, no special cases for test values | 8-10 pass | Fewer than 8 | 25 |
| Hand checks (steps 2, 3) | Hand list correct or disagreement explained; rounding case found and explained | One of the two done well | Missing | 10 |
| Bug reports | Five reports, all eight fields, each reproduced first try after revision | Five reports, some fields thin or one not reproducible | Fewer than five, or not reproducible | 25 |
| Tracker | Every bug has severity, frequency and computed priority; ship blockers listed | Most fields present | Missing or unprioritized | 15 |
| Stability forecast | Inputs justified from data, three runs compared, recommendation follows from numbers, least-trusted input named | Runs present, reasoning thin | Missing or numbers not from the model | 25 |
| **Total** | | | | **100** |

<details>
<summary>Instructor notes</summary>

- Ship blockers in `bugs_sample.csv`: B-001 (S1 always, P1), B-004 (S2 always, P1), B-007 (S1 rare, P2), B-011 (S3 always, P2, reopened). B-003 is closed, B-009 is won't-fix, B-012 is P3 whatever its status.
- The rounding case is `find_rates(13, 0.5, 2)`: 6.5 must round to 7, while `round(6.5)` in Python gives 6.
- A common bug in `backlog` is adding regressions from the same day's fixes. The `r = 0.25` test catches it, because the peak moves.
- Teams usually overestimate `CAPACITY` and ignore `REGRESSION`. Ask them to justify capacity from their sprint velocity (week 7).

</details>
