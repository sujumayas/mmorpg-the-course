# MMO308 · Lab 01: The layer cake

**Week:** 1, what live ops is ([lecture](../lectures/w01-what-live-ops-is.md)).
**Time:** 2 hours in lab, plus up to 2 hours at home.
**Weight:** one of the analytics labs (analytics labs are 40% of the course). The model you build here is reused in weeks 3 and 8.

## Objective

Build the cohort-stack model of a live game's player count, reproduce the lecture's numbers, and use it to answer two questions a studio really asks. How much of our post-launch drop is just arithmetic? Which live-ops lever buys the most players at the plateau?

## Starter materials

All in [`lab01-starter/`](lab01-starter/). Standard-library Python 3.10 or later, no packages to install.

- [`layercake.py`](lab01-starter/layercake.py). The model skeleton. Six functions are marked `TODO`: `retention`, `lifetime`, `plateau`, `layers`, `wau_series` and `launch_share`. Helpers are provided: `launch_installs` (the lecture's install pattern), `load_steam` (reads the CSV below) and `write_layers_csv` (writes a stacked-area table from your `layers`).
- [`test_layercake.py`](lab01-starter/test_layercake.py). Tests with the lecture's values: `R(0..4)`, `L = 4`, plateau 40,000, WAU of 106,000, 76,000, 48,473, 41,938 and 40,125 in weeks 1, 2, 12, 26 and 52, and launch shares of 48.8% and 9.2% in weeks 8 and 26. On the starter, every test prints `TODO` and the script exits with status 1.
- [`steam_monthly.csv`](lab01-starter/steam_monthly.csv). Monthly average and peak concurrent Steam players for New World (October 2021 to December 2022) and Lost Ark (February 2022 to March 2023), copied from SteamCharts in September 2026.

From the `lab01-starter` folder:

```
python test_layercake.py
python layercake.py
```

When your functions are right, the first command prints `all tests pass` and the second prints the lecture's table and writes `layers.csv`.

## Steps

1. **Implement the model (40 min).** Fill in the six functions. `lifetime` must use the closed form `w / (1 − qs) + (1 − w) / (1 − qt)`; one test compares it with a 3,000-term sum. Run the tests until all pass.
2. **Plot the cake (15 min).** Run `layercake.py` and plot `layers.csv` as a stacked area in any tool (a spreadsheet is fine). Add the total as a line. Mark the plateau.
3. **How much of the drop is arithmetic? (25 min).** From `steam_monthly.csv`, compute each game's monthly average as a percentage of its first full month (October 2021 for New World, February 2022 for Lost Ark). Then choose model parameters so the reference model's monthly means (average WAU over each block of 4 or 5 weeks) match Lost Ark's percentages for the first four months as closely as you can, holding `qt = 0.30`. Report your `w`, `qs` and ongoing-installs-to-launch ratio. Now try the same for New World. Which parameters did you have to push to extreme values, and what does that suggest? Write one paragraph. Remember that Steam concurrent players are not WAU: compare shapes, and say so.
4. **Bumps (15 min).** Both games' averages rise again later (Lost Ark in May and June 2022, New World from September 2022). Add a one-off bump cohort to your installs list and find the bump size that reproduces Lost Ark's May 2022 percentage. Then describe in two sentences what else, other than new installs, could produce the same bump (hint: players returning from earlier cohorts), and why the layer cake as written cannot tell the two apart.
5. **Lever memo (at home).** Your studio runs the reference game and can fund one of three plans for a year: (a) marketing that raises ongoing installs by 25% at a cost of 40,000 currency units per week; (b) an onboarding rework that raises `w` from 0.30 to 0.36, one-off cost 900,000; (c) an endgame update every quarter that raises `qs` from 0.90 to 0.92, cost 500,000 per update. Using your model, compute WAU in week 104 for each plan starting at week 52, and the extra player-weeks each plan produces between weeks 52 and 104 (the area between the new WAU line and the baseline). Divide cost by extra player-weeks. You will need to extend the model, because parameters now change at week 52. Plan (b) changes `w` only for cohorts that install in week 52 or later. Plan (c) changes `qs` for every stayer from week 52 on, including those in old cohorts. Explain in `RESULTS.md` how you implemented each.

## Deliverable

A zip or repository link with:

- your `layercake.py`, passing `test_layercake.py`;
- the stacked-area chart from step 2;
- `RESULTS.md` with the step 3 table and paragraph and the step 4 bump size and explanation;
- a memo of at most 400 words (step 5) recommending one plan, with a table of week-104 WAU, extra player-weeks and cost per player-week for all three, and one sentence on the biggest assumption your model makes.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Model correctness | All tests pass; closed form used; code readable with parameters not hard-coded | Tests pass, code hard to modify | Tests fail | 30% |
| Fitting the Steam shapes | Parameters reported for both games, fit quality shown, CCU versus WAU caveat stated, extreme parameters interpreted | One game fitted, caveat missing | No fit or percentages wrong | 25% |
| Bump analysis | Bump size found; returning players identified as an alternative; limitation of the model explained | Bump size found, explanation thin | Missing | 15% |
| Lever memo | Three plans compared on week-104 WAU and cost per extra player-week, clear recommendation, key assumption named | Comparison made, cost analysis incomplete | Recommendation without numbers | 25% |
| Presentation | Chart labeled with units and plateau line | Chart present, labels missing | No chart | 5% |
