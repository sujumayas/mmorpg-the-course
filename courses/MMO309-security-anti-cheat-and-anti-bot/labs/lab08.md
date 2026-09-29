# MMO309 · Lab 08: From detector scores to decisions

Assigned in week 8 ([lecture](../lectures/w08-machine-learning-for-detection-overview.md)). Due at the start of week 9. Part of the labs component (30% of the course).

## Objective

Take a detector's scores on a labelled validation set and turn them into a detection policy: an automatic-action threshold with a precision guarantee, a review band sized to your team's capacity, and a prediction of how both will behave after the next ban wave changes the share of bots.

## Starter materials

- [`lab08-starter/make_scores.py`](lab08-starter/make_scores.py). Generates `scores.csv` with seed 3098: 20,000 accounts from a fictional MMO's validation sample, each with a detector score between 0 and 1 and a reviewed label (1 = bot, 0 = human). About 3% are bots. The data is synthetic.
- [`lab08-starter/detect.py`](lab08-starter/detect.py). The file you edit. Six functions marked TODO: `confusion`, `precision_recall`, `threshold_for_precision`, `expected_cost`, `precision_at_prevalence` and `review_band`. Their docstrings state exactly what to return.
- [`lab08-starter/check_lab08.py`](lab08-starter/check_lab08.py). Tests each function on a ten-account example you can check by hand, then checks your thresholds on the full dataset. Run it from inside `lab08-starter/` with `../../../../.venv/bin/python check_lab08.py`. Every check fails on the starter and passes on a correct solution.
- The week 8 interactive, `examples/w08-base-rate-threshold.html`.

## Steps

1. **By hand first (15 minutes).** On the ten-account example at the top of `check_lab08.py`, compute the confusion matrix, precision and recall at thresholds 0.9, 0.7 and 0.3 on paper. Keep the sheet; you will hand it in.
2. **Implement the functions.** Fill in `detect.py` until the first six checks pass.
3. **The precision guarantee.** On the full dataset, find the lowest threshold with precision of at least 0.99, 0.95 and 0.90. Record the threshold, recall and number of humans flagged for each. Plot precision and recall against the threshold, and mark the three points.
4. **Costs.** Using `expected_cost`, find the cost-minimizing threshold for three cost ratios: a wrongful ban costs 10, 40 and 200 times a missed bot. Compare with the thresholds from step 3 and explain the relationship in two sentences.
5. **Triage.** Use the 0.99-precision threshold as `t_act`. Your review team can clear 400 cases per run. Compute `t_review` with `review_band`, then count how many bots are caught automatically, how many land in the review band and how many are missed. The last check in the checker confirms your numbers.
6. **The next ban wave.** Measure the detector's recall and false positive rate at `t_act` and at `t_review`. Use `precision_at_prevalence` to predict precision at both thresholds if prevalence falls from 3% to 1% and to 0.3%. How many reviewer hours per bot found does the review band cost at each prevalence, if one review takes 6 minutes?
7. **Policy.** Write the policy described in the deliverable.

## Deliverable

Your completed `detect.py` (checker prints `ALL PASS`), the hand sheet from step 1, the plot from step 3, and a one-page detection policy (at most 400 words plus one table) addressed to your community and live-ops leads. The policy states `t_act`, `t_review`, the measured precision and recall in each band, the predicted precision after the next ban wave, how often prevalence will be re-measured and how, and what an accused player can do.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Correct implementation | All checks pass; hand sheet matches the code | Checks pass, hand sheet has small errors | Checks failing | 25% |
| Threshold analysis | Step 3 and 4 tables complete; plot labelled; cost-threshold relationship explained correctly | Minor gaps | Thresholds chosen without evidence | 20% |
| Triage design | Band counts correct; capacity respected; the share of bots handled by each band stated and interpreted | Counts correct, little interpretation | Missing or wrong | 20% |
| Base-rate prediction | Precision after the ban wave computed for both thresholds, with a concrete process change that follows from it | Computed, weak consequence | Missing | 20% |
| Policy page | Numbers first, within length, readable by non-specialists, covers re-measurement and appeals | Complete but padded or vague on appeals | Missing parts | 15% |
