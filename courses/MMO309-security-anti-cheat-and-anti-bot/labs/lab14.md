# MMO309 · Lab 14: Response scorecard

Assigned in week 14 ([lecture](../lectures/w14-case-studies.md)). Due at the start of week 15. Part of the labs component (30% of the course). The scorecard is a useful appendix for the final threat model.

## Objective

Build the week 14 response scorecard as code, extend it to several years, and use it to recommend which anti-bot lever each of three invented games should fund first.

## Starter materials

- [`lab14-starter/scorecard.py`](lab14-starter/scorecard.py). The model, the multi-year rule and the lawsuit break-even are written out in the module docstring. It has a loader and six stub functions marked TODO: `uptime`, `one_year`, `day_worth`, `lawsuit_breakeven`, `saving_over` and `rank`. Running it as a script prints the best lever per game over one and three years once the stubs are filled.
- [`lab14-starter/levers.json`](lab14-starter/levers.json). The six levers from the lecture (`detect`, `act`, `down`, first-year cost `K_first`, later-year cost `K_later`, collateral `C`), three invented games that differ in harm per live day `h` ("farm_mmo" at $1,000, "pvp_arena" at $3,000, "small_indie" at $150), and the lecture's lawsuit numbers. All values are teaching assumptions.
- [`lab14-starter/test_scorecard.py`](lab14-starter/test_scorecard.py). Checks against the lecture's numbers. Run it from inside `lab14-starter/` with `../../../../.venv/bin/python test_scorecard.py`. Every check group fails on the starter and passes on a correct solution.

## Steps

1. **Implement the one-year card.** Fill in `uptime`, `one_year` and `day_worth`. Reproduce the lecture's table at `h = 1,000` and confirm that at instant-ban defaults a day of downtime is worth three days of detection.
2. **Add the lawsuit.** Implement `lawsuit_breakeven`. Report the break-even `h` for the lecture's numbers, then for a ruling that only cuts uptime to 0.4. Say in two sentences which of the three games could justify suing a supplier.
3. **Go multi-year.** Implement `saving_over` and `rank`. Find the first year in which the structural fix beats the delayed wave for "farm_mmo".
4. **Score the three games.** For each game, print the full ranking over one and three years. For "small_indie", list every lever whose saving is negative and explain why with `K + C` against `365 × h × (1 − uptime)`.
5. **Remove the easy win.** Suppose the games have no free account path to close. Delete that lever and rank again. Report the new winner per game and the value of one extra day of `down` for it, using `day_worth`.
6. **Recommend.** For each game, name the lever to fund first, the number you would measure after launch to check the card's `down` assumption, and the collateral you would watch.

## Deliverable

Your completed `scorecard.py` (tests passing), a table of the three games' rankings over one and three years, and a one-page recommendation (at most 500 words plus tables) to your live-ops lead covering steps 4 to 6.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Model correctness | All tests pass; lecture table reproduced | One-year card right, multi-year or lawsuit has a small error | Tests fail | 30% |
| Lawsuit and multi-year analysis | Break-even and crossover year reported with working | One of the two reported | Missing | 15% |
| Game rankings | Rankings for all three games, negative levers explained with the card's terms | Rankings without explanations | Missing | 20% |
| Sensitivity | Step 5 run, new winner justified with `live / down` | Step 5 run, justification thin | Missing | 20% |
| Recommendation | Lever, check metric and collateral named per game, each tied to a number | Levers named without links to numbers | No recommendation | 15% |
