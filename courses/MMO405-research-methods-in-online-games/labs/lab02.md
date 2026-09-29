# MMO405 · Lab 02: Effect sizes and the four verdicts

**Week:** 2 ([lecture](../lectures/w02-quantitative-methods-overview.md))
**Time:** 2 hours in the lab, plus up to 2 hours to finish.
**Work mode:** individual.
**Counts toward:** methods labs (30% of the course grade).

## Objective

Compute effect sizes with intervals, classify them against a smallest effect size of interest chosen in advance, and find out what happens to a pooled estimate when players are nested in servers that differ.

## Starter materials

- [`lab02-starter/effects.py`](lab02-starter/effects.py), Python 3, standard library only. It loads the data and gives you `phi` and `se_d`, and has four stubs:
  - `cohens_d` (TODO 1), the standardized difference with a pooled SD.
  - `verdict` (TODO 2), the lecture's four-verdict rule.
  - `fisher_ci` (TODO 3), the interval for a correlation.
  - `by_server` (TODO 4), `d` and its standard error within each server.
- [`lab02-starter/wellbeing.csv`](lab02-starter/wellbeing.csv), an invented survey of 6,000 players on three servers: `player_id`, `server`, `voice_chat` (used voice chat in the survey fortnight) and `wellbeing` (0 to 10). [`make_survey.py`](lab02-starter/make_survey.py) shows how it was generated. **Do not read the generator until you have finished step 6.**
- [`lab02-starter/test_effects.py`](lab02-starter/test_effects.py) has eight tests. All fail on the starter and pass on a correct solution. Run them from inside `lab02-starter/` with `python -m unittest test_effects.py` (from the repository root, `.venv/bin/python` is the course Python).
- The interactive [`examples/w02-significant-vs-meaningful.html`](../examples/w02-significant-vs-meaningful.html), once it is built.

`se_d` uses the large-sample standard error for unequal groups, `sqrt((n1+n2)/(n1·n2) + d²/(2(n1+n2)))`. For equal groups and small `d` it is close to the lecture's `sqrt(2/n)`.

## Steps

### Part A: before you look (15 min)

1. Write down, in your results sheet and before running anything on the data, a SESOI for "voice-chat users have higher well-being" on this 0 to 10 scale. Justify it in two sentences, using one of the lecture's sources for a SESOI (perceptible change, value to the studio, or theory). If you cannot justify another value, use `Δ = 0.20` and say why that default is weak.

### Part B: the code (50 min)

2. Implement TODOs 1 to 3 and run the tests. The lecture's five rows must come out with the same verdicts.
3. Implement `by_server` (TODO 4). Run all eight tests, then `python effects.py`, and copy the report into your results sheet.

### Part C: reading the numbers (40 min)

4. Compare the pooled `d` with the three within-server estimates. Using week 1's selection term, explain in four sentences why the pooled estimate is larger than any of the server estimates. Name the two brackets of the term in this dataset and give their signs from the data (compute voice-chat share and non-voice mean well-being per server).
5. Combine the three server estimates into one with inverse-variance weights: `d̄ = Σ(d_s / se_s²) / Σ(1 / se_s²)` and `se(d̄) = 1 / sqrt(Σ 1/se_s²)`. Report `d̄`, its 95% interval and its verdict at your SESOI from step 1.
6. Server B's estimate has the opposite sign from A and C. Is that evidence that voice chat works differently on server B? Answer with the intervals, not the point estimates.
7. Now read `make_survey.py`. The true effect is 0.10 points on a scale with SD 1.2. Convert it to `d`, compare it with your step 5 estimate, and say in two sentences whether your conclusion from step 5 would have misled a designer.

### Part D: the paragraph (15 min)

8. Write a 300-word results paragraph for a paper about this dataset. It must state the design and its strongest claim type, the SESOI and where it came from, the pooled and within-server effects with intervals, the verdict, and one plain-language translation (probability of superiority or natural units). It must not use the word "significant" without an effect size next to it.

## Deliverable

- `effects.py` passing all eight tests, plus your code for step 5.
- A results sheet (two pages at most) with your pre-registered SESOI (step 1), the report, and answers to steps 4 to 7.
- The 300-word paragraph from step 8.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Code (steps 2 and 3) | All tests pass; report reproduced | Tests pass; report incomplete | Tests fail | 20 |
| SESOI (step 1) | Chosen before analysis with a real justification | Default used and its weakness named | Missing or chosen after the data | 10 |
| Nesting and selection (steps 4 and 5) | Both brackets computed with signs; combined estimate and verdict correct | Direction right, numbers incomplete | Missing or wrong | 25 |
| Interval reasoning (steps 6 and 7) | Uses intervals to judge server B; compares with the true `d` and states the practical consequence | Reasonable but based on point estimates | Missing | 20 |
| Results paragraph (step 8) | Every required element; claim type matches design; readable by a designer | One element missing or a causal overclaim | Missing | 20 |
| Code quality | Readable, runs first time | Runs with minor fixes | Does not run | 5 |
| **Total** | | | | **100** |
