# AU101 · Lab 12: The raid voice budget

**Week:** 12 ([lecture](../lectures/w12-audio-for-mmos-many-players-one-mix.md))
**Time:** 2 hours in the lab, plus up to 2 hours to finish.
**Work mode:** pairs.
**Counts toward:** the final sound pass (40%).

## Objective

Predict a raid's voice demand with Little's law, implement a flat and a tiered voice allocator, and use a provided raid simulator to measure what each policy does to your own sounds, your party's and everyone else's. Then find the burst peaks that averages hide and tune a budget for a world boss event.

## Starter materials

All in [`lab12-starter/`](lab12-starter/). Python 3, standard library only.

- [`raid_mix.py`](lab12-starter/raid_mix.py): stubs for `expected_voices` (Little's law), `crowd_gain_db` (`10 · log10(n)`), `allocate_flat` (first come, first served, week 10's "discard newest") and `allocate_tiered` (reservations per tier with spill-down in tier order, nearest first). Finished tools: `make_raid` (you, your party and the others at seeded random distances and phases), `requests_at` (every sound alive at time `t`, plus 4 permanent boss voices) and `kept_share` (the fraction of a tier's requests that got a voice over a run).
- [`test_raid_mix.py`](lab12-starter/test_raid_mix.py): seven tests from the lecture. They check 1.6, 32 and 64 voices from Little's law, +10.0 and +15.44 dB crowd gains, the first-come order, a hand-worked tiered allocation, that neither allocator exceeds the budget, that the simulator's average demand is within 5% of your Little's-law prediction, and that the tiered policy keeps 100% of your sounds and your party's. All seven fail on the starter.
- The [raid voice budget interactive](../examples/w12-raid-voice-budget.html) to compare with your numbers.

Run the tests with `python3 test_raid_mix.py` inside the folder. When they pass, `python3 raid_mix.py` prints the demand table and your own sounds' share under both policies (the lecture reports about 41% flat and 100% tiered).

## Steps

### Part A: predict (20 min)

1. Implement `expected_voices` and `crowd_gain_db`. Reproduce the lecture's demand table and crowd-bed table.
2. Before running any simulation, write down your prediction of the share of "others" sounds kept under the lecture's tiered reservations. Show the arithmetic.

### Part B: allocate (40 min)

3. Implement `allocate_flat`. Sort by `start` and keep the first `budget`. Python's `sorted` is stable, so ties keep input order.
4. Implement `allocate_tiered` exactly as the docstring describes. Work the test case by hand first, then make the test pass.
5. Run `kept_share` for every tier under both policies with the default raid. Put the eight numbers in a table next to your Part A predictions and explain any gap over 3 percentage points.

### Part C: bursts (30 min)

6. In your own file, write a variant of `make_raid` that gives every player phase 0 (do not edit the starter or the tests). This is a pull where everyone opens at once. Record the peak demand in the first 3 seconds and the share of your sounds kept under the tiered policy.
7. Find the smallest "self" reservation that keeps 100% of your sounds during the pull. Explain why it differs from the average-based answer.

### Part D: tune a world boss (30 min)

8. Scale the raid to 120 players with a 48-voice budget. Keep your party at 5.
9. Design reservations, an others' sound length (you may change `duration` for the others tier only, using your own variant of `requests_at`) and a crowd-bed threshold. Your targets: 100% of your sounds, at least 95% of your party's, the boss always, and at least 25% of the individual others' sounds for the nearest players.
10. Report the crowd-bed level at your threshold and at 120 players.

## Deliverable

- Completed `raid_mix.py` with all seven tests passing, plus `experiments.py` that reproduces every number in your report.
- A two-page PDF: the Part A predictions, the Part B table with explanations, the Part C burst result and reservation, and the Part D design with the numbers that show each target is met. End with a 100-word recommendation for which options-menu settings your world boss design needs, in the style of the lecture's section 5.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Code | All seven tests pass; experiments reproducible from one script | Five or six tests pass | Four or fewer pass | 25 |
| Prediction vs simulation | Predictions written before running, gaps explained with the model | Table present, gaps unexplained | Missing | 20 |
| Burst analysis | Peak and minimum reservation found, difference from the average explained | Numbers without explanation | Missing | 20 |
| World boss design | All four targets met and shown with numbers; crowd-bed rule stated with levels | Two or three targets met | Missing | 25 |
| Options recommendation | Settings mapped to tiers, each justified | Generic list | Missing | 10 |
| **Total** | | | | **100** |
