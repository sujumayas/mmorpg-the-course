# PR201 · Lab 05: Sprint review note and forecast to alpha

**Week:** 5 · **Time:** 90 minutes in the studio session · **Weight:** a sprint record for [milestone 3, alpha](../assessments/m3-alpha-brief.md) (sprint process row)

## Objective

Measure how much estimated work your team actually finishes per useful hour, forecast what sprints 2 and 3 will deliver, and close the gap to the alpha list with cuts made now and cuts triggered later. The model is in section 2 of the [week 5 guide](../lectures/w05-sprint-1-review.md).

## Starter materials

Folder `lab05-starter/`. Standard library Python only.

- `sprint_result.csv`: per finished sprint, `useful_capacity_h`, `done_estimate_h` and `done_actual_h`.
- `plan.csv`: useful capacity of each future sprint before the milestone.
- `cuts.csv`: `id`, `item`, `hours`, `when` (`now` or `trigger: …`) and `pillar_check`.
- `forecast.py`: prints `f`, `r`, the naive view and the forecast range, and with `--cuts` checks that cuts now close the mid gap and cuts now plus trigger cuts close the low gap. Options `--remaining` (required) and `--band` (default 0.2).
- `review-template.md`: the one-page review note.

## Steps

1. **Reproduce the guide.** Run `python forecast.py sprint_result.csv plan.csv --remaining 120 --cuts cuts.csv`. Confirm `f = 0.573`, `r = 1.28`, the mid gap of 27.1 and the `FAIL` on the low gap.
2. **Fix the starter.** Add the loot rarity cut from the guide (rarity tiers from four to two, 10 hours, same trigger as revive) and confirm `PASS`.
3. **Your numbers.** Fill `sprint_result.csv` from your sprint 1 log. `done_estimate_h` counts only tasks that met the definition of done. `done_actual_h` is hours logged on those tasks.
4. **Your remaining work.** Re-estimate every task still on your alpha list, including carry-over, and total it.
5. **Forecast.** Fill `plan.csv` from next sprints' availability and run the forecast.
6. **Cuts.** Write cuts now and trigger cuts until the check passes. For each, rerun lab 02's `check_scope.py` on the reduced tiers and write the pillar result in `pillar_check`.
7. **Term check.** Rerun `check_scope.py` on your whole scope sheet with `--plannable` set to your measured `f` times your team's useful hours for the term (week 1). *Hollowmarch*: `0.573 × 445.5 = 255`. If it fails, cut or re-scope should features until it passes, and keep the before-and-after table for week 9.
8. **Split `f` and `r`.** In two sentences, say whether your shortfall is mostly estimation (`r` well above 1) or flow (`r` near 1, `f` low), and what the retrospective should look at.
9. **Review note.** Fill in `review-template.md`.

## Deliverable

In `docs/sprint-1/`: the three CSV files, the `forecast.py` output at `PASS`, the step 2 result, the step 8 sentences, the updated `features.csv` with its term-check output, and `review.md`.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Measurement | `f` and `r` from logged data, only done tasks counted | Minor counting errors | Planned numbers used | 25% |
| Forecast | Range and gaps correct, remaining re-estimated including carry-over | Carry-over at old estimates | Naive capacity used | 20% |
| Cuts | `forecast.py` passes; every cut names a sprint or trigger | Passes, triggers vague | Does not pass | 25% |
| Pillar check | Scope checker still passes after cuts | Checked by hand | Not checked | 15% |
| Diagnosis and note | Step 7 names estimation or flow with evidence; review note complete | One weak | Missing | 15% |
