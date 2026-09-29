# MMO403 · Lab 10: Reading a three-arm price test

**Week:** 10 ([Pricing experiments](../lectures/w10-pricing-experiments.md))
**Time:** 2 hours in lab plus up to 2 hours at home
**Counts toward:** models (40%)
**Work:** in pairs; submit one folder per pair

## Objective

You will analyse a finished price test on a new-player starter bundle shown at US$3.99, US$4.99 and US$6.99. The conversion readout and the revenue readout point in different directions, the store-wide numbers are noisy, and one arm quietly takes revenue from another item. Your job is to say which price to ship, how sure you are, and what the test could not tell you.

## Starter materials

All in [`lab10-starter/`](lab10-starter/README.md). Python 3.10 or later, standard library only.

- `gen_price_test.py` writes `price_test.csv` (seed 1129): 36,000 exposed players, one row each, with `arm`, `price`, `bought` (0 or 1, the bundle within 14 days) and `other_spend` (US$ spent on the rest of the store in the same 14 days). Arm A is the current price. Read the generator only in step 5.
- `pricing.py` holds eight functions to write: `rpe`, `breakeven_conversion`, `arc_elasticity`, `n_per_arm_rate`, `n_per_arm_revenue`, `welch_z`, `cap_values` and `summarize`. Docstrings give exact definitions. `main()` prints the readout once they work.
- `check_lab10.py` prints PASS, FAIL or TODO per function. It fails on the starter and passes on a correct solution.

```
python gen_price_test.py
python pricing.py
python check_lab10.py
```

## Steps

1. **The formulas (20 min).** Write the first five functions. Check them by hand on the lecture's US$4.99 and US$6.99 example: `RPE` 0.2796, break-even 3.57%, elasticity −0.67, about 6,742 and 26,501 players per arm.
2. **The readout (20 min).** Write `summarize` and `welch_z`, then run `pricing.py`. For arms B and C against A, report conversion, bundle `RPE`, break-even conversion and arc elasticity. Which arm would a conversion dashboard call the winner? Which would a bundle-revenue dashboard call the winner?
3. **Is it real? (20 min).** Report the z statistics for conversion and bundle `RPE`. B's revenue gain is not significant at 12,000 players per arm. Use `n_per_arm_revenue` with the observed rates to say how many players per arm the test needed, and how many weeks that is at 12,000 new players a week in total.
4. **The whole store (20 min).** Compare store-wide `RPE` (bundle plus `other_spend`) across arms, first raw and then capped at US$20 per player with `cap_values`. Explain why the raw z statistics are so small and what capping hides. Which arm loses store-wide revenue, and is that loss significant after capping?
5. **The mechanism (15 min).** Only now, read `gen_price_test.py`. Explain in three sentences how arm C lost store revenue even though more players bought its bundle. How would you have detected this without reading the generator?
6. **Recommendation (at home).** One page to the monetization lead who asked "B cut purchases by 20%, why should we ship it?" State the price you recommend, the evidence for and against, what the test could not answer (with the sample size it would have needed), and one change to the next test's plan. Include one sentence on how many players own the bundle under each price, and whether that matters for this game.

## Deliverable

One folder named `lab10-<name1>-<name2>` containing your `pricing.py` (passing `check_lab10.py`), `RESULTS.md` with the tables and answers from steps 1 to 5, and `recommendation.pdf` from step 6.

## Rubric (20 points)

| Criterion | Excellent (full) | Adequate (half) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Code passes the checker | All eight PASS | Six or seven PASS | Five or fewer | 4 |
| Readout and break-even (step 2) | Both arms placed correctly against the break-even line; the two dashboards' verdicts contrasted | Numbers right, no contrast | Missing | 3 |
| Significance and sample size (step 3) | z values correct; required sample and weeks computed from observed rates; conclusion stated as "could not tell" rather than "no effect" | Sample size computed, conclusion muddled | Missing | 4 |
| Store-wide analysis (steps 4 and 5) | Raw and capped results, the cost of capping named, cannibalization found and explained, a detection method proposed | Capped result without explanation | Missing | 4 |
| Recommendation (step 6) | A clear price; evidence and limits stated in numbers; ownership trade-off addressed; a concrete plan change | Clear price, weak on limits | Missing or no decision | 5 |
