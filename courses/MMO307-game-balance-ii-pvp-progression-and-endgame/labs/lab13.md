# MMO307 · Lab 13: Settling time and patch cadence

**Assigned:** week 13 ([lecture](../lectures/w13-meta-game-and-patch-cycles.md), [interactive](../examples/w13-patch-cadence.html)). **Due:** start of week 14 class. **Time:** 2 hours in lab, plus up to 2 hours at home. **Feeds:** the final season design (40%), which needs a patch calendar with a stated settling time.

## Objective

Measure how fast an invented game's meta settles after a patch, check whether the exponential settling model fits, and use the fitted model to recommend a patch calendar for one 16-week season. You should finish able to defend every date on the calendar with a number.

## Starter materials

All in [`lab13-starter/`](lab13-starter/). Standard-library Python, run with `.venv/bin/python` from the repository root or any Python 3.10+.

- [`meta_cycle.py`](lab13-starter/meta_cycle.py), a skeleton with five functions to complete: `effective_number`, `diversity_at`, `fit_tau`, `cycle_average` and `longest_period`. A working `load_pick_log` reads the CSV and turns each day's pick counts into `N_eff`. Running the file prints `N_eff` per day once `effective_number` works.
- [`pick_log.csv`](lab13-starter/pick_log.csv), 29 days of pick counts (days 0 to 28 after a patch, 4,000 picks per day) for the eight classes of an invented ladder.
- [`test_meta_cycle.py`](lab13-starter/test_meta_cycle.py), seven tests using the lecture's values. All fail on the starter. Run `python test_meta_cycle.py` or `pytest test_meta_cycle.py` inside the folder.
- The [interactive](../examples/w13-patch-cadence.html) for spot checks.

## Steps

1. **Complete the functions (40 min).** Implement the five functions until all seven tests pass. `fit_tau` fits a least-squares line to `ln(D − D_s)` against `t` and returns `−1/slope`, skipping points where `D ≤ D_s`. `longest_period` returns the largest whole number of days whose cycle average still meets a target.
2. **Describe the data (15 min).** Run `meta_cycle.py`. Plot `N_eff` against day, in any tool. Estimate `D_0` from day 0 and `D_s` from the mean of days 22 to 28.
3. **Fit `τ` (20 min).** Fit `τ` using days 0 to 14 and your `D_s`. Then refit with `D_s` raised and lowered by 0.3. Report all three values of `τ` in a table and explain in two sentences why the direction of each change makes sense.
4. **Check the fit (15 min).** Plot `ln(N_eff − D_s)` against day for days 0 to 14, with your fitted line. Say whether the points follow a straight line, and name any day that departs from it by more than you would expect from noise.
5. **Sensitivity to the window (10 min).** Refit using days 0 to 7 only, and then days 0 to 21. Explain which window you trust and why.
6. **Recommend a calendar (30 min).** Your team can ship at most 10 balance patches in a 16-week season (112 days), and it wants a season-average `N_eff` of at least 6.0. Use `cycle_average` and `longest_period` with your fitted `D_0`, `D_s` and `τ`. Give the interval you recommend, the number of patches, the average `N_eff` and the settled share of each cycle. If the target cannot be met within the budget, say how far short you fall, and propose one non-patch change (scheduled perturbation, counter design) that raises `D_s`. Estimate the `D_s` it would need.
7. **Judgment dates (10 min).** For each patch on your calendar, give the first day on which you would judge it from pick data (`2τ` after release). Flag every patch you would have to finalize before its predecessor is readable.

## Deliverable

A zip or repository link containing:

- Your completed `meta_cycle.py`, with the test output pasted into the report showing all seven tests passing.
- The two plots from steps 2 and 4.
- `report.md` (600 to 900 words) with the `D_s` and `τ` estimates, the sensitivity tables from steps 3 and 5, the calendar from step 6 (a table of patch days and judgment days), and one closing paragraph that names the settling time your calendar assumes and says what you would do if next season's `τ` came out half as long.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Weight |
|---|---|---|---|---|
| Correct functions | All seven tests pass; code is readable | Five or six tests pass | Four or fewer pass | 25% |
| Fitting and fit checking | `τ` reported with the `D_s` and window sensitivity; log plot shows the fit and any departures are named | `τ` reported with one sensitivity check | Single `τ` with no check | 25% |
| Calendar recommendation | Meets or clearly explains the target; interval, count, average, settled share all correct; non-patch option quantified if needed | Calendar given with some numbers missing or unjustified | No calendar, or numbers contradict the model | 25% |
| Judgment dates | Every patch has a judgment date; conflicts flagged and a policy proposed for them | Dates given, conflicts not discussed | Missing | 10% |
| Writing | Plain, numbered claims tied to tables; within word limit | Mostly clear, some claims without numbers | Hard to follow or over length | 15% |
