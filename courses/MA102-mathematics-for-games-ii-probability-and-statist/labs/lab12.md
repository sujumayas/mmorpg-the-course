# MA102 · Lab 12: Summarizing a playtest

Assigned in week 12 ([lecture](../lectures/w12-descriptive-statistics-for-playtests.md)). Due at the start of week 13. Counts toward the problem-set grade.

## Objective

Turn a raw playtest log into a one-page summary a lead designer can act on: choose the right center and spread for each measure, flag and investigate outliers, and show the shape of the data.

## Starter materials

- [`playtest_w12.csv`](lab12-starter/playtest_w12.csv) in [`lab12-starter/`](lab12-starter/README.md). One row per tester for 40 testers of a fictional dungeon, with columns `tester_id`, `experience` (new or returning), `clear_minutes` (entry to boss kill or quitting), `deaths`, `minutes_idle` (from the session log), `reached_boss` (yes or no), `beat_boss` (yes or no) and `difficulty_rating` (1 to 7, 4 = about right). The data is synthetic and built to contain one idle outlier, one genuinely lost tester and a two-group split in ratings.
- [`lab12_starter.py`](lab12-starter/lab12_starter.py), which loads the CSV and gives you `inclusive_percentile(values, p)`, the lecture's rule, so your quartiles match the answer key. It runs as a script or in a notebook; pandas and numpy also work.
- Spreadsheet users: open the CSV and use `PERCENTILE.INC`, which follows the same rule.
- The week 12 interactive, [`examples/w12-playtest-spread.html`](../examples/w12-playtest-spread.html). It has no import box, but you can load the "Boss attempts" preset, add testers and drag values to check a small subset of your numbers.

## Steps

1. **Check the data.** Count rows, missing values and impossible values (negative times, ratings outside 1 to 7). Write down anything you fix and why.
2. **Summaries.** For `clear_minutes` and `deaths`, compute n, mean, median, sample SD, Q1, Q3, IQR, 90th percentile, and the 1.5 × IQR fences. For `difficulty_rating`, compute the mean, median and mode and a count per rating.
3. **Plots.** Draw a dot plot or histogram plus a box plot for clear times, a histogram for deaths, and a bar chart of rating counts. Try two bin widths for the deaths histogram and keep the one that shows the shape honestly.
4. **Outliers.** List every value outside the fences. Use `minutes_idle` and the other columns to decide for each one whether to keep, exclude from timing, or flag as a design finding. Recompute the clear-time summaries with and without exclusions.
5. **Rates.** Compute deaths per hour for each tester, then the median deaths per hour. Compute the funnel: entered, reached the boss, beat the boss, with the drop at each step.
6. **Groups.** Split every summary by `experience`. Does the rating split line up with experience? Report the medians and IQRs for each group side by side.
7. **Summary.** Write the one-page summary described below.

## Deliverable

The notebook, script or spreadsheet plus a one-page PDF (at most 450 words and three figures) addressed to the lead designer. It must:

- Open with the three numbers you think matter most, each with n and the summary type named (in the form "median clear time 22 minutes, IQR 18 to 27, n = 39", with your own numbers).
- State each outlier decision in one line.
- Explain the rating distribution without using only its mean.
- End with one recommended design change supported by a number from your analysis.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Correct statistics | All summaries correct under the inclusive rule, with and without exclusions | One or two errors | Several errors or wrong percentile method | 30% |
| Choice of summary | Median and IQR for skewed measures, mean where totals matter, distribution shown for ratings, each choice justified | Mostly sensible choices, weak justification | Mean ± SD used everywhere | 20% |
| Outlier handling | Every flagged value investigated with the log, decisions documented, design finding separated from noise | Outliers flagged but decisions thin | Outliers ignored or silently dropped | 20% |
| Plots | Plots readable, honest bins, axis labels and n shown | Plots present with minor problems | Missing or misleading | 15% |
| Summary page | Numbers first, under 450 words, recommendation tied to evidence | Understandable but padded or missing n | Hard to follow or no recommendation | 15% |
