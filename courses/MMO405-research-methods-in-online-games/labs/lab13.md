# MMO405 · Lab 13: A replication audit

**Week:** 13 ([lecture](../lectures/w13-replication.md))
**Time:** 2 hours in the lab, plus up to 2 hours to finish.
**Work mode:** individual code; the replication plan in Part C may be drafted with your paper partner, but each student submits their own.
**Counts toward:** methods labs (30% of the course grade). The replication plan can go into the limitations or future-work section of your final paper.

## Objective

Predict how much a published effect should shrink from the original study's power, judge 12 invented replications with the five criteria from the lecture, separate shrinkage the significance filter explains from shrinkage that points to a changed game, and plan a replication of a study you cite.

## Starter materials

- [`lab13-starter/replication.py`](lab13-starter/replication.py), Python 3, standard library only. It has `se_d`, `d33` and a CSV loader ready, and three stubs:
  - `power` and `expected_published` (TODO 1), the lecture's filter model.
  - `verdicts` (TODO 2), the five criteria of lecture section 3, returned as a dict.
  - `replication_n` (TODO 3), the small-telescopes planning rule.
- [`lab13-starter/pairs.csv`](lab13-starter/pairs.csv), 12 invented original and replication pairs from fictional online-game studies. Columns: `study`, `topic`, `d_orig`, `n_orig`, `d_rep`, `n_rep` (players per group) and `patch_changed` (1 if the game's relevant system was changed between the two studies). [`make_pairs.py`](lab13-starter/make_pairs.py) regenerates it. Do not read its true effects until step 6.
- [`lab13-starter/test_replication.py`](lab13-starter/test_replication.py) has ten tests. All fail on the starter and pass on a correct solution. Run them from inside `lab13-starter/` with `python -m unittest test_replication.py` (from the repository root, `.venv/bin/python` is the course Python).
- The interactive [`examples/w13-significance-filter.html`](../examples/w13-significance-filter.html), once it is built.

## Steps

### Part A: the filter model (35 min)

1. Implement `power` and `expected_published` (TODO 1). Run the `TestFilter` tests. Reproduce the lecture's table for `δ = 0.20`, then make the same table for `δ = 0.10` and `δ = 0.40`.
2. For each of the three tables, find the smallest `n` per group at which the exaggeration ratio drops below 1.2. Write one sentence on how that `n` depends on `δ`, and one on what it means for a field whose typical true effect is 0.1.

### Part B: judging 12 replications (50 min)

3. Implement `verdicts` (TODO 2) and run all tests. Run `python replication.py` and paste its table into your results sheet.
4. Count how many of the 12 pairs "replicated" under each of criteria 1 (significance and sign), 2 (interval capture) and 3 (small telescopes, counting "not too small" as a success). Report the three counts side by side, as the Open Science Collaboration did, and explain in three sentences why they differ.
5. For every pair, compute the expected shrinkage from the filter alone. Assume the true effect is the replication estimate (clamped at 0.05 if smaller), compute `expected_published(δ, n_orig)`, and compare it with `d_orig`. Flag pairs where the original is much larger than the filter predicts from a truth near the replication estimate.
6. Look at the `patch_changed` column. For the three patched pairs, decide whether the filter alone could explain the gap. Pay special attention to S10: its original had 1,500 players per group. Write one paragraph per patched pair saying which story (filter or changed game) fits better, and what descriptive statistics you would ask for to check. Only then open `make_pairs.py`, read the true effects and the patch shift, and say in two sentences where your stories were right or wrong.

### Part C: plan a replication (35 min)

7. Pick one quantitative study you cite in your final paper. From its reported sample size, compute `d33` and `replication_n` (TODO 3) for 80% and 95% power. If the study reports only a total N or unequal groups, say how you converted it.
8. Write a one-page replication plan with these headings: claim being replicated; what must stay the same (measure, population, game system) and what cannot (game version, platform); sample size with the calculation from step 7; the criterion you will use to call it a success, stated before any data exist; data sharing (what you can publish, and how a reviewer could reproduce your main table if the telemetry cannot be released); ethics (which parts of the week 10 ethics review change for a replication, such as consent wording for data sharing).

## Deliverable

- `replication.py` passing all ten tests, plus your code for steps 1, 2 and 5.
- A results sheet (two pages at most) with the tables and answers for steps 1 to 6.
- The one-page replication plan from step 8.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Code (TODOs 1-3) | All tests pass; tables for three values of δ correct | Tests pass, one table has errors | Tests fail | 20 |
| Filter reasoning (steps 1, 2, 5) | Thresholds found; dependence on δ explained; filter predictions computed for all pairs and outliers flagged | Numbers right, explanation thin | Missing or wrong | 20 |
| Criteria comparison (steps 3, 4) | Three counts correct; disagreement explained by what each criterion asks | Counts right, explanation vague | Missing | 15 |
| Changed-game analysis (step 6) | Each patched pair argued with numbers; S10 recognized as unexplained by the filter; concrete descriptives named | Stories chosen without numbers | Missing | 20 |
| Replication plan (steps 7, 8) | Sample size computed and justified; success criterion fixed in advance; realistic data-sharing and ethics sections | Plan complete but criterion or data plan vague | Missing sections | 20 |
| Code quality | Readable, runs first time | Runs with minor fixes | Does not run | 5 |
| **Total** | | | | **100** |
