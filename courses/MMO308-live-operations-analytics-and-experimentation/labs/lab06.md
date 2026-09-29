# MMO308 · Lab 06: Peeking, boundaries and a broken split

**Week:** 6 ([A/B testing: statistics and pitfalls](../lectures/w06-ab-testing-statistics-and-pitfalls.md))
**Time:** 2 hours in lab plus up to 3 hours at home
**Counts toward:** analytics labs (40%); the write-up in step 6 is the analysis section of the A/B report (20%)
**Work:** in pairs; submit one folder per pair

## Objective

You will measure by simulation how peeking inflates the false-positive rate, find sequential stopping boundaries that fix it, and then analyse a real-looking 14-day experiment day by day. The experiment will look like a win if you peek. Your job is to show whether it is one.

## Starter materials

All in [`lab06-starter/`](lab06-starter/README.md). Python 3.10 or later, standard library only.

- `gen_experiment.py` writes `experiment_daily.csv` (seed 735): 14 rows, one per day, with newly exposed players and conversions in each arm of a test of a new crafting-station screen. The plan said 50/50 by hashed account id, primary metric "crafted an item within 3 days of first exposure", one analysis at day 14. Read the generator only after step 5.
- `peeking.py` holds six functions to write: `z_two_proportion`, `cumulative_z`, `srm_pvalue`, `obf_boundaries`, `stop_rate` and `find_constant`. Docstrings give exact definitions. `main()` prints the simulation and a day-by-day table once they work.
- `check_lab06.py` prints PASS, FAIL or TODO per function. Simulated functions are checked against ranges, so any correct implementation passes.

```
python gen_experiment.py
python peeking.py
python check_lab06.py
```

## Steps

1. **The z-test and the split check (15 min).** Write `z_two_proportion` (reuse MA102 lab 14) and `srm_pvalue`. Check `srm_pvalue` by hand on the lecture's 50,500 against 49,500.
2. **Peeking by simulation (25 min).** Write `stop_rate`. Tabulate the false-positive rate of the naive 1.96 rule for 1, 2, 5, 10, 14 and 30 looks. Compare with the lecture's table. How far apart may your numbers and the table's be with 20,000 runs? Use MA102 week 13's margin of error for a rate.
3. **Boundaries (25 min).** Write `obf_boundaries` and `find_constant`. Find the Pocock and O'Brien-Fleming constants for `K = 5` and `K = 14`. Then use `stop_rate` with `theta = 2.8016` to fill in the lecture's power table for `K = 5` (one look, peeking, Pocock, O'Brien-Fleming). Add a column for average share of the sample used, which needs a small change to your function or a copy of it.
4. **Day by day (15 min).** Write `cumulative_z` and run `peeking.py`. On which day would a team that peeks with the naive rule have stopped and shipped? Would the O'Brien-Fleming rule have stopped at any look? What does the planned single analysis at day 14 say?
5. **The split (15 min).** Run the SRM check on the 14-day totals, and then day by day. Is the mismatch a single bad day or steady? Only now, read `gen_experiment.py` and explain in three sentences how the mismatch created the apparent lift. Why did the missing players make B look better rather than worse?
6. **Analysis write-up (at home).** Two pages to the producer who asked "B was significant on day 4, why haven't we shipped it?" Include the day-by-day chart of `z` with both the 1.96 line and the O'Brien-Fleming boundary, the SRM result, the planned-analysis result, and your recommendation. State what you would change in the experiment plan and the client before rerunning the test.

## Deliverable

One folder named `lab06-<name1>-<name2>` containing your `peeking.py` (passing `check_lab06.py`), `RESULTS.md` with the tables and answers from steps 1 to 5, and `analysis.pdf` from step 6.

## Rubric (20 points)

| Criterion | Excellent (full) | Adequate (half) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Code passes the checker | All six PASS | Four or five PASS | Three or fewer | 4 |
| Peeking and boundaries (steps 2 and 3) | Full table with a correct margin of error; constants found for both K; power table with sample use, and the trade-off stated in numbers | Tables present, no margin or no trade-off | Missing | 5 |
| Day-by-day reading (step 4) | Naive stop day, OBF decision and planned result all correct and contrasted | Two of three correct | Missing | 3 |
| SRM diagnosis (step 5) | Overall and daily SRM computed; mechanism explained, including why the bias favors B | SRM computed, mechanism vague | Missing | 3 |
| Write-up (step 6) | Clear chart with both boundaries; recommendation follows from SRM and planned analysis; concrete plan and client changes | Correct but the producer would not follow it, or chart missing | Missing | 5 |
