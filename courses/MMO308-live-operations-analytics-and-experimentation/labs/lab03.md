# MMO308 · Lab 03: The retention triangle

**Week:** 3, cohorts and retention curves ([lecture](../lectures/w03-cohorts-and-retention-curves.md)).
**Time:** 2 hours in lab, plus up to 3 hours at home.
**Weight:** one of the analytics labs (analytics labs are 40% of the course). The cohort table you build is reused in weeks 4, 6 and 8.

## Objective

Build a retention triangle from a raw activity log, then act as the live team's analyst. Three changes are hidden in 90 days of data from an invented MMO. Find each one, date it, and say whether it is a cohort effect, a one-day period effect or a lasting period effect. Then write the note that tells the team what broke onboarding and what it has cost so far.

## Starter materials

All in [`lab03-starter/`](lab03-starter/). Standard-library Python 3.10 or later, no packages to install.

- [`gen_cohorts.py`](lab03-starter/gen_cohorts.py). Writes `installs.csv` (about 45,000 players, about 500 installs a day for days 0 to 89) and `activity.csv` (one row per active player per day, about 284,000 rows). Seed 303. The planted effects are in a block marked `SECRET`. Do not read it until you have written your answers to step 5.
- [`retention.py`](lab03-starter/retention.py). Loaders and a short report are provided. Six functions are marked `TODO`: `cohort_sizes`, `cohort_table`, `checkpoint`, `pooled`, `find_step` and `calendar_index`. The module docstring fixes the conventions, including the rule that incomplete cells are left out rather than set to zero.
- [`test_retention.py`](lab03-starter/test_retention.py). Tests on a seven-player log you can check by hand, the lecture's D7 series (a −9.0 point step at install day 20), the lecture's outage (calendar index below 0.5 on day 40 only), and shape checks on the generated data. On the starter every test prints `TODO` and the script exits with status 1.

From the `lab03-starter` folder:

```
python gen_cohorts.py
python test_retention.py
python retention.py
```

## Steps

1. **Build the table (30 min).** Implement `cohort_sizes`, `cohort_table` and `checkpoint`. Work the seven-player test log by hand first. Run the tests.
2. **Draw it (20 min).** Plot the triangle as a heat map (install day down, age 0 to 30 across) and the D1, D7 and D30 series against install day, in any tool. Add DAU by calendar day from `activity.csv` as a third chart.
3. **Look before you compute (10 min).** Write down, without code, every seam and diagonal you can see and your guess of its date and type.
4. **Detect (30 min).** Implement `pooled`, `find_step` and `calendar_index`. Run `retention.py`. For the step it reports, compute pooled D1, D7 and D30 for the five cohorts before and the five from the step, and the standard error of each difference (lecture section 3). Is the step at the same install day in all three series?
5. **The third change (25 min).** `calendar_index` finds the one-day effect easily, but its values also drift downward over the last weeks of data. Two things could cause that drift: the cohort effect leaking into the column means, or a lasting period effect. Improve the index so it compares each cell only with cells from cohorts on the same side of the step you found in step 4 (or divides out a per-cohort level). Use the improved index and the D1, D7 and D30 series to decide whether there is a lasting period effect, and date it. Explain the pattern you expect in each Dn series for a lasting effect starting on day `P` (lecture, the "endgame" mode), and check it.
6. **Check (5 min).** Now read the `SECRET` block. Compare with your answers. Where you were off, say why.
7. **Incident note (at home).** Write the note to the live team.

## Deliverable

A zip or repository link with:

- your `retention.py`, passing `test_retention.py`, plus your improved index from step 5;
- `RESULTS.md` with your step 3 guesses, the step 4 table (pooled rates, differences, standard errors), your step 5 reasoning and dates, and the step 6 comparison;
- the three charts from step 2, with every effect you found marked on each;
- an incident note of at most 400 words that dates the onboarding break, states its size in D1, D7 and D30 with uncertainty, estimates the DAU it has cost by day 89 (use the week 1 layer-cake reasoning, or simulate the counterfactual with your own estimate of the normal curve), explains why the DAU chart did not show it, and names the one chart the team should check the morning after every future onboarding patch.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Code correctness | All tests pass; incomplete cells handled; readable | Tests pass, code hard to follow | Tests fail | 25% |
| Onboarding break | Correct install day, same in D1/D7/D30; pooled differences with standard errors | Correct day, uncertainty missing | Wrong day or type | 20% |
| One-day effect | Correct calendar day, and its appearance at `t − 1`, `t − 7`, `t − 30` shown in the Dn series | Correct day, not traced in the series | Missing | 15% |
| Lasting effect | Leak diagnosed, index improved, date within 3 days, expected Dn pattern stated and checked | Effect found, reasoning thin | Missing, or the leak mistaken for it | 20% |
| Charts | Triangle, Dn series and DAU charts labeled, effects marked | Charts present, marks missing | Missing | 5% |
| Incident note | Size with uncertainty, DAU cost estimated with method, the DAU blind spot explained, chart named; within 400 words | Most parts present | Missing or unsupported | 15% |
