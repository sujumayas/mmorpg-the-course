# MMO308 · Lab 12: Faucet alarms

**Week:** 12, economy monitoring ([lecture](../lectures/w12-economy-monitoring.md)).
**Time:** 2 hours in the lab, plus up to 2 hours to finish.
**Work mode:** pairs.
**Counts toward:** analytics labs (40% of the course grade).

## Objective

You are the new economy analyst on a live server. You get 24 weeks of daily faucet, sink and reconciliation data, plus the team's list of planned events. Somewhere in the second half, things went wrong that nobody planned. Build the alarm layer from the week 12 lecture, show that a naive version drowns in false alarms, find and date every incident, and write the alarm specification the team will run from now on.

## Starter materials

All in [`lab12-starter/`](lab12-starter/). Standard-library Python 3.12 or later (the repository's `.venv` has 3.13). Use a spreadsheet for charts if you prefer.

- [`economy.csv`](lab12-starter/economy.csv): 168 days, day 1 is a Monday. Columns `day`, `weekday`, `active_players`, two faucets (`mob_loot`, `quest_reward`), two sinks (`repair`, `auction_fee`), all in millions of gold per day, and `residual`, the daily reconciliation gap from MMO304 week 12 (snapshot supply minus ledger-predicted supply), which should sit near zero.
- [`events.csv`](lab12-starter/events.csv): what the team planned and announced, with the expected multiplier where there is one. Anything not listed was not planned.
- [`alarms.py`](lab12-starter/alarms.py): loaders plus five stubs, `weekday_baseline`, `robust_sigma`, `spike_alarms`, `cusum` and `zscores`. Its main block runs a deliberately naive pipeline on `mob_loot`.
- [`test_lab12.py`](lab12-starter/test_lab12.py): four checks. One reproduces the lecture's 14-day CUSUM table (alarm on day 13), one checks the mirror score and the effect of `k`, one checks the baseline with skipped days, and one checks the robust `σ`, spike and z-score helpers. Run it from inside `lab12-starter/` with `../../../../.venv/bin/python test_lab12.py`. All four fail on the starter.
- [`make_faucet.py`](lab12-starter/make_faucet.py): the generator, seed 12. Don't read it until you have submitted. It contains the answers.

## Steps

**A. The tools (25 min)**

1. Implement the five stubs and run the tests until all four pass.

**B. The naive pipeline (15 min)**

2. Run `alarms.py`. It builds a same-weekday baseline on raw `mob_loot`, measures `σ` on days 29 to 56, and runs CUSUM from day 57. Note the day it fires and look it up in `events.csv`. Then add the spike rule to the naive run and list every day it fires. Sort the firings into "planned" and "unexplained".

**C. A pipeline you can trust (40 min)**

3. **Per player.** Divide each faucet and sink by `active_players` (and multiply by 1,000 to get thousands of gold per player). Explain in two sentences what this does to the expansion days.
4. **Planned changes.** Multiply the baseline by the expected multiplier on planned event days, and skip those days when computing later baselines. For the patch on day 85, divide `quest_reward` from day 85 onward by the expected 1.06 before computing baselines. Show, with the naive and adjusted runs side by side, what the patch does to an unadjusted alarm.
5. **Noise.** Measure `σ` for each series with `robust_sigma` on days 29 to 56. Explain why the robust version matters if an incident had happened in that window.
6. **Rules.** From day 57, run an upward CUSUM (`k = 0.5`, `h = 5`) and the spike rule on the faucets and the residual, and the mirror CUSUM and a downward spike rule on the sinks. The residual's baseline is zero. Collect every alarm in one table with the series, day, rule and `z` or `S`.

**D. The incidents (25 min)**

7. Label every alarm as an incident, a planned change you failed to adjust for, or a false alarm. For each incident, estimate the day it began by reading the CUSUM path backwards to the last day the score was zero, and estimate the gold involved up to the alarm day.
8. For each incident, say which rule caught it first and whether the other rule would have caught it at all. Relate your answer to the lecture's run-length table.

**E. The budget and the spec (at home)**

9. The full team will watch 40 series like these. Using your `cusum` function on simulated standard-normal `z` (a few thousand runs per setting, seeded), find the smallest `h` with `k = 0.5` that gives no more than 6 false alarms a year across 40 series. Report the detection delay for a 1σ leak at that `h`.
10. Write a one-page alarm specification. For each of the five series give the rule, `k`, `h`, direction, baseline method, and who gets paged or ticketed. Include the procedure for planned events and patches, and a rule for when to reset or freeze a baseline.

## Deliverable

1. Your completed `alarms.py`, with all four tests passing, and the script that runs your step 3 to 9 pipeline.
2. A chart per series (value with baseline on top, `z` and CUSUM below, alarms marked) and the alarm table from steps 6 and 7.
3. The one-page alarm specification from step 10.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Implementation | All tests pass; pipeline code is short, readable and reproducible | Tests pass, pipeline hard to follow | Tests fail | 20% |
| Baseline design (steps 3-5) | Per-player normalisation, event and patch adjustments and robust `σ` all applied and each justified with a before/after comparison | Adjustments applied, weak justification | Adjustments missing | 25% |
| Incident finding (steps 6-8) | Every alarm labelled; all three incidents found and dated from the CUSUM path; gold estimated; rule comparison tied to run lengths | Incidents found, dating or labelling incomplete | Incidents missed | 30% |
| Budget and specification (steps 9-10) | `h` chosen by simulation to meet the budget, delay cost stated, spec complete with owners and reset rules | Spec complete, `h` chosen by feel | Spec incomplete | 25% |

<details>
<summary>Instructor check values</summary>

Reference pipeline as described in steps 3 to 6 (absolute residuals per player, 4-week same-weekday baselines, robust `σ` from days 29 to 56, monitoring from day 57, alarms listed with a reset after each), checked with Python 3.13.

- Naive run in `alarms.py`: first CUSUM alarm on day 62, the planned double-gold Saturday. The naive spike rule also fires on day 63 (planned) and on every day from 155 (expansion), plus days 127, 132 and 138 (the real leak).
- Without the patch adjustment, `quest_reward` alarms on day 87. With it, `quest_reward` raises no alarm.
- Incident 1, `mob_loot` leak of 1.2 million gold a day from day 120 (about 1σ of the daily total): upward CUSUM alarm on day 127 (per player), spike rule also on day 127, further CUSUM alarms on 132 and 138 after resets. Gold leaked by day 127 is about 9.6 million.
- Incident 2, `repair` sink charging 4.5% less from day 100: mirror CUSUM and downward spike both on day 104.
- Incident 3, `residual` jump of about 6 million on day 140 only: spike and CUSUM both on day 140.
- One false alarm in the reference pipeline: mirror CUSUM on `repair`, day 75. It persists at `h = 6`. Students who label it correctly and explain it as noise (5 series over 112 days at an in-control run length near 930 days predict about 0.6 false alarms) deserve full marks for step 7.
- Step 9: with `k = 0.5`, the budget needs an in-control run length of about `40 × 365 / 6 ≈ 2,430` days, which `h = 6` meets (about 2,500 days in simulation), at a 1σ detection delay of about 12 days instead of 10.

</details>
