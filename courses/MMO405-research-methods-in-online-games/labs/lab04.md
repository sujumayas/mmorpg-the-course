# MMO405 · Lab 04: Reliability and structure of a player survey

**Week:** 4 ([Survey design and validated scales](../lectures/w04-survey-design-and-validated-scales.md))
**Time:** 2 hours in lab plus up to 2 hours at home
**Counts toward:** methods labs (30%); the measurement report feeds the methods section of your proposal (20%)
**Work:** individually; you may discuss results with one partner, but write your own code and report

## Objective

You will write the reliability functions a survey researcher uses every week, run them on a 10-item guild scale, and decide from the numbers how the scale should be scored. The scale's published codebook contains one scoring error and the scale is not measuring what its name claims. Your job is to find both and say what to report instead.

## Starter materials

All in [`lab04-starter/`](lab04-starter/README.md). Python 3.10 or later, standard library only.

- `gen_survey.py` writes `survey.csv` from seed 404: 400 invented players' answers to items `g1` to `g10` on a 1-to-7 agreement scale.
- `codebook.md` gives each item's wording and whether it is scored normally or in reverse, as the scale's (invented) authors published it.
- `scale.py` holds eight functions to write: `reverse_code`, `variance`, `pearson`, `cronbach_alpha`, `standardized_alpha`, `mean_interitem_r`, `corrected_item_total` and `alpha_if_deleted`. Each docstring states the formula. `load_survey` is written for you.
- `check_lab04.py` prints PASS, FAIL or TODO per function and exits non-zero until all pass.

```
python gen_survey.py
python scale.py
python check_lab04.py
```

## Steps

1. **Functions (40 min).** Write the eight functions until `check_lab04.py` passes. Don't import numpy or pandas. The point is to see each formula work.
2. **Raw alpha (10 min).** Run `scale.py`. Record alpha for the data as given, the mean inter-item correlation, and each item's corrected item-total correlation and alpha-if-deleted in `RESULTS.md`.
3. **Follow the codebook (10 min).** Reverse-code the items the codebook marks as reverse and recompute alpha. Record it.
4. **Find the scoring error (15 min).** One item still has a strongly negative item-total correlation. Name it, read its wording in `codebook.md`, and explain in two sentences why it should have been reverse-coded. This is content evidence. Recode it too and record the new alpha and mean inter-item correlation. Use `standardized_alpha` with your mean inter-item correlation and compare the result with the raw alpha.
5. **Look for structure (25 min).** Write a short function (in a separate file, `structure.py`) that prints the 10 × 10 correlation matrix of the recoded items, rounded to two decimals. Describe the pattern you see. Then compute alpha separately for `g1`-`g5` and `g6`-`g10`, and the Pearson correlation between the two half-scale sums. Put the three numbers in a table.
6. **Decide (at home).** Write a one-page measurement report (400 to 600 words) addressed to a research team who planned to use "guild commitment" as one score. It must include the alpha for the whole scale, the evidence that it is two constructs, a recommendation for scoring, and a proposed name for each part that fits the item wording. Say what criterion evidence from telemetry would support each part (one behavioral measure per part, with the expected direction).

## Deliverable

One folder named `lab04-<name>` containing `scale.py` (passing `check_lab04.py`), `structure.py`, `RESULTS.md` with steps 2 to 5, and `report.md` from step 6.

## Rubric (20 points)

| Criterion | Excellent (full) | Adequate (half) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Code passes the checker | All eight PASS | Six or seven PASS | Five or fewer | 4 |
| Scoring error found (steps 3 and 4) | Item named, wording-based reason given, alpha before and after both reported | Item named without a content reason | Missing or wrong item | 4 |
| Structure evidence (step 5) | Matrix pattern described in terms of blocks; both half alphas and the between-halves correlation reported and interpreted | Numbers without interpretation | Missing | 4 |
| Recommendation and naming (step 6) | Clear scoring decision justified by the numbers; names match the item wording | Decision given but weakly justified | Missing | 4 |
| Criterion evidence plan (step 6) | One plausible telemetry measure per part with an expected direction, and a note that linking needs consent | Measures named without direction or consent | Missing | 4 |
