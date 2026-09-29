# MMO403 · Lab 05: Tune a battle pass

**Week:** 5 ([Battle passes](../lectures/w05-battle-passes.md))
**Time:** 2 hours in lab plus up to 3 hours at home
**Counts toward:** models (40%); the memo's finish-line section is reused in the final business plan
**Work:** in pairs; submit one folder per pair

## Objective

You will implement the lecture's battle pass model, fit it to a season of pass-owner play time, find the finish line that maximizes tier sales, and choose a finish line, rebate and pressure-reducing rule that you can defend in numbers.

## Starter materials

All in [`lab05-starter/`](lab05-starter/README.md). Python 3.10 or later, standard library only.

- `gen_owners.py` writes `owners.csv` from seed 405: the season play time in hours of 5,000 pass owners. The data include a small group who stopped playing in the first week, as real data do.
- `battlepass.py` holds seven functions to write: `share_playing_at_least`, `tier_reached`, `tier_distribution`, `stats_from_distribution`, `empirical_distribution`, `fit_lognormal` and `best_h_star`. Each docstring gives the exact formula. `main()` prints the lecture's table and a data-versus-model table once they work.
- `check_lab05.py` prints PASS, FAIL or TODO per function.
- `memo-template.md`, the design memo you hand in.

```
python gen_owners.py
python battlepass.py
python check_lab05.py
```

## Steps

1. **The model (30 min).** Write `share_playing_at_least`, `tier_reached`, `tier_distribution` and `stats_from_distribution`. Run `battlepass.py`. The first table must match lecture 05 section 2 exactly. In `RESULTS.md`, check the `H* = 50` row by hand (show `z` and the finish share).
2. **The data (20 min).** Write `empirical_distribution` and `fit_lognormal`. Run `battlepass.py` again and copy the second table. Where does the model fit the data well, and where not? Plot or sketch a histogram of `ln(season_hours)` and find the early leavers.
3. **Clean the fit (15 min).** Refit the lognormal to owners with at least 5 hours only. Report the new `m` and `s`. Rerun the data-versus-model comparison with the new fit. Explain in two sentences why a handful of early leavers moved the fitted spread so much, and why you should still count them when you report finish share to the producer.
4. **The revenue peak (15 min).** Write `best_h_star`. Report the revenue-peak `H*` and its finish share for the lecture's model, for your step 2 fit and for your step 3 fit. Confirm with `empirical_distribution` that the data's own peak is close. How far is each peak from the fitted median?
5. **Rebate placement (15 min).** For `H*` at your step 3 median, compare a 1,500-coin rebate spread evenly with one placed entirely at the final tier, using the data. Report the average rebate back and the share of owners who get nothing under each. Which placement makes the pass "pay for itself" for the median owner at a 950-coin price?
6. **The memo (at home).** Fill in `memo-template.md`. Choose `H*` with a stated finish-share target, report how much tier revenue your choice gives up relative to the peak, choose a rebate amount and placement, and propose one rule from lecture 05 section 4 with a numerical estimate of what it changes (for example, catch-up XP modeled as a 10% increase in the hours of owners below 60% of `H*` in the final two weeks). End with the sentence players will see about how long the pass takes.

## Deliverable

One folder named `lab05-<name1>-<name2>` containing your `battlepass.py` (passing `check_lab05.py`), `RESULTS.md` with steps 1 to 5, and `memo.md` from step 6.

## Rubric (20 points)

| Criterion | Excellent (full) | Adequate (half) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Code passes the checker | All seven PASS | Five or six PASS | Four or fewer | 4 |
| Model and data (steps 1 to 3) | Hand check right; misfit located and explained by early leavers; cleaned fit reported with a reason to still count leavers in finish share | Numbers right, explanation thin | Missing or wrong | 4 |
| Peak and rebate (steps 4 and 5) | Three peaks reported and related to the median; rebate comparison with share getting nothing; correct "pays for itself" answer | Values right without interpretation | Missing | 4 |
| Memo: finish line and rebate | Target stated before `H*`; revenue given up in coins and percent; rebate choice justified by who receives it | Choice made, trade-off not quantified | Missing | 4 |
| Memo: pressure rule and player text | Rule modeled with a stated assumption and its effect on a table column; player-facing sentence accurate and plain | Rule named without estimate | Missing | 4 |
