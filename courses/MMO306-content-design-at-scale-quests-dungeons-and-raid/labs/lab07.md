# MMO306 · Lab 07: Tuning a boss from its logs

**Week:** 7, tuning encounters with logs ([lecture](../lectures/w07-tuning-encounters-with-logs.md)).
**Time:** 2 hours in the lab, plus up to 2 hours at home.
**Work mode:** pairs.
**Counts toward:** encounter designs (40%). The tuning memo format here is the one your encounter designs use.

## Objective

Read a week of logs for an invented Mythic boss, the Warden (440,000,000 health, 400-second enrage). Find out which check is failing, fit the kill-rate model to the field of groups, correct it for upload bias, and recommend one hotfix with a predicted effect.

## Starter materials

All in [`lab07-starter/`](lab07-starter/). Python 3, standard library only.

- [`tuning.py`](lab07-starter/tuning.py): nine functions to write, each with a docstring that states its exact rule, plus a `report()` that prints the numbers you need once they work.
- [`test_lab07.py`](lab07-starter/test_lab07.py): nine checks. All fail on the starter. Run `python test_lab07.py` from inside the folder.
- [`encounter_log.csv`](lab07-starter/encounter_log.csv): 60 pulls by one progression group. Columns `pull, t, event, source, target, ability, amount`. Events are `ENCOUNTER_START`, `CAST` (amount = players targeted), `DAMAGE` (amount = raid damage in that chunk), `DEATH`, and `ENCOUNTER_END` (amount 1 for a kill, 0 for a wipe).
- [`best_pulls.csv`](lab07-starter/best_pulls.csv): 300 groups' best raid DPS on the Warden, from server telemetry, with an `uploaded` flag (1 if the group also uploaded to a public log site).
- The [kill-rate interactive](../examples/w07-kill-rate-curve.html) for checking your model.
- Spreadsheet option: both CSVs open in any spreadsheet. You can do steps 2 to 7 with pivot tables and `NORM.S.DIST`, but the checks in step 1 only run against the Python file.

## Steps

### Part A: read the logs (45 min)

1. Implement `read_pulls`, `wipe_causes`, `deaths_per_100` and `survival`. Run the checks. The four that use the tiny inline log must pass before you continue.
2. Run `python tuning.py`. You should see 60 pulls with 1 kill, and wipe causes of Cinder Wave 57.6%, Enrage 27.1%, Falling Glass 13.6%, Shard Rain 1.7%.
3. Compare the wipe causes with deaths per 100 exposures. You should see Cinder Wave at 3.88 and Falling Glass at 7.41. Write two sentences: which mechanic leads the wipe table, which one is actually deadlier per exposure, and why they differ (look at when and how often each is cast in the log).
4. Print the survival curve at every 20 seconds and sketch or plot it. You should get 1.0 at 100 s, 0.867 at 200 s, 0.55 at 300 s and 0.267 at 400 s. Mark where the curve drops fastest.

### Part B: fit the field (45 min)

5. Implement `kill_rate`, `fit_lognormal`, `model_kill_rate` and `health_for_target`. The lecture checks (25%, 40%, 50% on the twenty-group sample; 26.3% and 38.5% in the smooth model; 423.8M for a 35% target) must pass.
6. On all 300 groups, the kill rate at 440M is 0.230 and the fitted model gives `m ≈ 988,811`, `σ ≈ 0.1448`, model kill rate 0.231. On the uploaded groups only, the kill rate is 0.405. Explain the gap in one sentence.
7. Implement `weighted_kill_rate`. Your telemetry team reports that groups at or above 984,000 DPS upload at a rate of 0.8 and groups below upload at 0.2. Reweight the uploaded groups and report the corrected kill rate (you should get about 0.279). Explain why it lands between 0.230 and 0.405 rather than on 0.230.

### Part C: recommend a hotfix (30 min)

8. Your target is a 35% kill rate on the damage check. Use the population fit to find the health that reaches it (about 418.2M, a 5% cut). Using the lecture's slope rule, predict the kill-rate gain of that cut before you compute it exactly, then compare.
9. Decide whether the progression group from Part A would benefit from that cut. Use its wipe causes and survival curve, not its DPS alone.
10. Propose one mechanic change for the ability you think is holding groups back most. Say how it changes deaths per 100 exposures (for example "halving targets from 3 to 2 should cut deaths per cast by about a third") and which pulls in the log it would have saved.

## Deliverable

- `tuning.py` passing all nine checks.
- A tuning memo of at most 500 words, written to the encounter lead. It must contain: the wipe-cause table and deaths per 100 exposures, the survival curve (one image), the three kill rates (population, logged, reweighted), your health recommendation with its predicted and computed effect, your mechanic recommendation, and one sentence on what next week's logs should show if you are right.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Log analysis | All four Part A functions correct; the exposure argument in step 3 is specific and uses the cast timing | Functions correct, explanation vague | Checks failing or no explanation | 25% |
| Kill-rate model | Model functions correct; fitted values reproduced; slope prediction within 2 points of the exact change | Minor numeric slip | Model not fitted or not used | 25% |
| Upload bias | Correct reweighted rate and a correct reason it does not recover 0.230 (coarse two-band rates) | Rate correct, reason missing | Bias ignored | 15% |
| Recommendation | Health and mechanic changes each tied to the failing check, with numbers and a testable prediction | Changes reasonable but one lacks numbers | Recommendation not supported by the data | 25% |
| Memo writing | Plain, numeric, within the word limit | Some vague claims | Hard to act on | 10% |
