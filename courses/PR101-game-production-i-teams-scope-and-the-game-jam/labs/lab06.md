# PR101 · Lab 06: Your estimate log

**Week:** 6, estimation ([lecture](../lectures/w06-estimation-and-why-it-fails.md)).
**Time:** 2 hours in lab, plus up to 2 hours at home.
**Weight:** part of the jam game component (30%). The buffer you set here goes into your jam plan, and the habit of scoring estimates feeds the week 9 post-mortem.

## Objective

Finish a small Python module that scores a plan's estimates: ratios, percentiles, the plan ratio, the skew penalty and the buffer the plan would have needed. Check it against the lecture's table for an invented cohort. Then run it on your own lab 04 MVP estimates and re-estimate your jam task list as ranges, with a buffer set from data.

## Starter materials

All in [`lab06-starter/`](lab06-starter/). Standard-library Python 3.10 or later, no packages. Run everything from inside that folder.

- [`estimates.py`](lab06-starter/estimates.py). `load_log`, `finished` and `report` are done for you. Seven functions are empty: `ratio`, `median`, `percentile`, `summary`, `skew_penalty`, `buffer_for` and `corrected_estimate`. Each docstring is the spec.
- [`jam_plans_example.csv`](lab06-starter/jam_plans_example.csv), the invented twelve-team cohort from lecture section 2 (120 tasks). Column `rule` is `none` for teams A to F and `split4` for teams G to L. A blank `actual_h` means the task was cut.
- [`our_plan.csv`](lab06-starter/our_plan.csv), an empty file with the same columns for your team.
- [`test_lab06.py`](lab06-starter/test_lab06.py), seven tests. On the starter, `python test_lab06.py` prints `0/7 tests passed` and exits with code 1.

## Steps

1. **Read the data (10 min).** Open `jam_plans_example.csv` in a spreadsheet. Pick one team and compute its ratios, median and plan ratio by hand. Is that team's plan ratio above its median?
2. **`ratio`, `median`, `percentile` (30 min).** Implement them. `percentile` must use the lecture's linear method, and `percentile(v, 0.5)` must equal `median(v)`. Don't sort the caller's list in place. Run the tests until `test_ratio`, `test_median` and `test_percentile` pass.
3. **`summary` (20 min).** Return the six numbers named in the docstring, skipping cut rows. `test_summary_matches_lecture` checks them against the lecture's table to three decimals.
4. **`skew_penalty`, `buffer_for`, `corrected_estimate` (15 min).** Implement them from the lecture's model: `e^(σ²/2)`, `b = 1 − 1/R`, and a range of `raw × p10` to `raw × p90`. Run the tests until you see `7/7 tests passed`.
5. **Report and check the model (15 min).** Run `python estimates.py`. Check every number against the lecture's table. Then write a short script that computes `σ` and `G` for each rule (the standard deviation and the mean of `math.log(r)`, with `G = e^(mean)`) and prints `G × skew_penalty(σ)` next to the mean ratio. How close are they for each rule?
6. **Your own history (at home, 30 min).** Put your lab 04 MVP estimates and actuals into `our_plan.csv`, with your team letter and `rule` set to `ours`. Run `python estimates.py our_plan.csv`. Record your median and plan ratio and the buffer it implies. Compare it with the 0.25 you used in lab 04.
7. **Re-estimate your jam plan (at home, 30 min).** If you have at least eight rows of your own, use your own p10 and p90. Otherwise use the cohort band that matches how your plan is written (split to 4 hours or not). Give a range for every task above your lab 04 cut line. Recompute `P` with the buffer from step 6 (or the matching cohort buffer) and redraw the cut line. Record which tasks moved below it.
8. **Split the biggest tasks (at home, 15 min).** Take the three largest tasks left above the line and split each into pieces of 4 hours or less, as week 7 will require. Re-estimate the pieces. Did the total go up? Write one sentence on why splitting often raises an estimate.

## Deliverable

In your team repository under `lab06/`:

- `estimates.py` with `python test_lab06.py` reporting `7/7 tests passed`.
- Your step 5 script and its output.
- `our_plan.csv` with your MVP rows, and the report output for it.
- A note of at most 400 words with: your plan ratio and implied buffer compared with lab 04's; the redrawn cut line and the tasks that moved; the split tasks from step 8 with their old and new estimates; and one sentence on how far `G × e^(σ²/2)` was from the mean ratio for each cohort rule and why it isn't exact.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Tests pass | 7/7 | 5-6 | 4 or fewer | 35% |
| Code quality | Functions follow their docstrings, raise the stated errors, don't mutate inputs; no statistics library used for the graded functions | Works with small deviations (mutates input, missing error) | Hard-coded answers or tests edited | 15% |
| Model check | Step 5 script correct; comparison of `G × e^(σ²/2)` and mean explained (sample, not a perfect log-normal) | Numbers right, no explanation | Missing | 10% |
| Own-data analysis | Correct plan ratio and buffer from your own MVP rows, compared with lab 04 | Computed but not compared | Missing | 15% |
| Re-estimated plan | Ranges for every planned task, `P` recomputed, cut line redrawn, moved tasks listed, three tasks split | Ranges given but plan not redrawn, or no splitting | Point estimates only | 25% |
