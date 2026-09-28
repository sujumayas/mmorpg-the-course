# MA102 · Lab 13: How many kills until you trust a drop rate?

**Week:** 13 ([Sampling, confidence and why n=5 lies](../lectures/w13-sampling-confidence-and-why-n5-lies.md))
**Time:** 2 hours in lab plus up to 2 hours at home
**Counts toward:** problem sets (35% of the course grade)
**Work:** individually; you may discuss methods with a partner but submit your own files

## Objective

You will measure, by simulation, how often confidence intervals for a rate contain the truth, and turn what you find into a reporting guideline your team could follow. By the end you should be able to state, with numbers from your own runs, how many trials a playtest or drop log needs before its rate is worth quoting.

## Starter materials

The files are in [`lab13-starter/`](lab13-starter/README.md). Each item is described well enough to rebuild in 15 minutes if you work without the repository.

- [`drops.csv`](lab13-starter/drops.csv). A drop log of 3,000 simulated boss kills (150 players, 20 kills each), one row per kill, with columns `kill_id`, `player_id`, `dropped` (0 or 1). The hidden drop rate is set by the instructor with `make_drops.py` and revealed after submission.
- [`intervals_template.py`](lab13-starter/intervals_template.py). Functions to fill in for the Wald and Wilson intervals, the growing sample and the coverage simulation. Spreadsheet users build columns `n`, `k`, `p_hat`, `se`, `wald_low`, `wald_high`, `wilson_low`, `wilson_high` instead.
- [`coverage_template.csv`](lab13-starter/coverage_template.csv). The `coverage` grid: rows for `p` in {0.02, 0.10, 0.50, 0.80} and `n` in {5, 20, 100, 1000}, with empty columns for each method.
- [`mulberry32.py`](lab13-starter/mulberry32.py). The seeded random generator the course interactives use, so your results are reproducible. Use seed 13 for the main runs. `RAND()` in a spreadsheet cannot be seeded, so paste a fixed column of values generated once.
- The interactive [`examples/w13-sampling-intervals.html`](../examples/w13-sampling-intervals.html) for checking your numbers.

## Steps

1. **Warm up by hand (15 min).** Using the formulas from the lecture, compute the simple (Wald) and Wilson 95% intervals for 4 of 5, 16 of 20 and 0 of 30. Check them against the interactive's test values. Write one sentence on why 0 of 30 breaks the simple formula, then give the rule-of-three bound.
2. **Growing sample (25 min).** Read `drops.csv` in order. For the first `n` kills with `n` in {10, 30, 100, 300, 1000, 3000}, compute `k`, `p̂`, the Wald interval and the Wilson interval. Plot both intervals against `n` on one chart (log x axis). Mark where the Wilson interval first becomes narrower than ±25% of `p̂`.
3. **Coverage by simulation (35 min).** For each cell of the `coverage` tab, simulate 2,000 studies of size `n` at true rate `p`, build both intervals for each, and record the fraction that contain `p`. Fill the table for both methods. Compare three of your cells with the exact values in the lecture (for example `p = 0.8, n = 5`). Your simulated values should be within about 1.5 points.
4. **Sample size planning (15 min).** Using `n = 1.96² × p(1 − p) / m²` and the relative version, compute the kills needed to measure: a 50% clear rate to ±5 points; a 2% drop rate to ±0.5 points; a 0.5% drop rate to ±20% of itself. Then run one simulated study of each size and report whether your interval achieved the planned width.
5. **Bias experiment (20 min).** Add a biased "fan site" sample. Simulate 1,000 players who each kill the boss 20 times, but only players who got at least one drop submit their log. Compute the interval from submitted logs only. Compare it with the interval from all logs. Explain in three sentences why collecting more of the biased logs would not fix the result.
6. **Guideline (at home).** Write a one-page reporting guideline for your team titled "How we report rates from playtests and logs". It must include: the minimum `n` at which you will quote a percentage, which interval method you use and why, how to report zero-success results, and one rule about bias. Every rule must cite a number from your steps 2 to 5.

## Deliverable

Submit one folder named `lab13-<yourname>` containing:

- Your completed spreadsheet or Python script, runnable with seed 13 to reproduce every number.
- `chart.png` from step 2.
- `guideline.pdf`, one page, from step 6.

## Rubric (20 points)

| Criterion | Excellent (full) | Adequate (half) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Hand calculations (step 1) | All six intervals and the rule-of-three bound correct to 0.1 point | One or two arithmetic slips | Three or more wrong, or Wald used where Wilson required | 3 |
| Growing-sample chart (step 2) | Both methods plotted, log axis, threshold `n` marked and stated | Chart present but threshold missing or unclear | No chart | 3 |
| Coverage table (step 3) | All 32 cells filled, three cells checked against exact values, pattern described correctly | Table complete but no comparison or description | Table incomplete | 5 |
| Sample size planning (step 4) | Three sizes correct and one simulated study each confirms the width | Sizes correct, no simulation check | Sizes wrong | 3 |
| Bias experiment (step 5) | Biased and unbiased intervals computed; explanation names self-selection and why `n` cannot fix it | Computed but explanation vague | Missing | 3 |
| Guideline (step 6) | Four required rules, each backed by a number from the lab, readable by a non-statistician | Rules present but some unsupported by numbers | Missing or generic | 3 |
