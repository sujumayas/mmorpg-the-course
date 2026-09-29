# MMO403 · Lab 02: LTV curve and payback

**Week:** 2, unit economics ([lecture](../lectures/w02-unit-economics-ltv-cac-arppu.md)).
**Time:** 2 hours in lab, plus up to 3 hours at home.
**Weight:** part of the Models strand (40%). The LTV code is reused in the final business plan.

## Objective

Implement the LTV curve as retention times net ARPDAU summed over days, find the payback day for a given CAC, and use both to price four acquisition channels. Then write an acquisition plan in which every LTV states its horizon, its fee basis and its cohort.

## Starter materials

All in [`lab02-starter/`](lab02-starter/). Standard-library Python 3.10 or later.

- [`ltv.py`](lab02-starter/ltv.py), with a `Game` dataclass holding the lecture's defaults (`w = 0.25`, `qs = 0.98`, `qt = 0.40`, ARPDAU $0.20, fee 30%), a CSV loader and five empty functions: `retention`, `ltv`, `lifetime_ltv`, `payback_day` and `channel_report`.
- [`channels.csv`](lab02-starter/channels.csv), four invented acquisition channels (organic referral, video ads, incentivized installs, an influencer campaign), each with its own CAC, retention parameters and ARPDAU.
- [`test_ltv.py`](lab02-starter/test_ltv.py), the lecture's test values: `R(1) = 0.545`, LTV through day 30 of $0.989, lifetime $1.925, payback on day 70 at a $1.50 CAC and never at $2.00, and the effect of removing the platform fee. Every test fails on the starter.
- The interactive `examples/w02-ltv-curve.html` for spot checks.

Run the tests from inside the folder with `python3 test_ltv.py` (or `pytest`).

## Steps

1. **Retention.** Implement `retention(g, d)`. Check `R(1)` by hand.
2. **LTV curve.** Implement `ltv(g, T)` as net ARPDAU times the sum of `R(0) .. R(T − 1)`.
3. **Lifetime.** Implement `lifetime_ltv(g)` from the closed form, and confirm it matches `ltv(g, 5000)`.
4. **Payback.** Implement `payback_day(g, cac)`, returning `None` when the curve never reaches CAC.
5. **Channels.** Implement `channel_report(rows)` and run it on `channels.csv`. Treat organic installs as CAC 0 (their ratio is infinite, so report them separately).
6. **Tests.** Run until all six tests pass.
7. **Sensitivity.** For the video-ads channel, find the smallest change to each of `w`, `qs`, `qt` and ARPDAU (one at a time) that brings LTV/CAC to 3. Report which parameter needs the smallest relative change, and relate it to the lecture's claim about the tail.
8. **ARPDAU by type.** Extend `ltv` with an optional tourist ARPDAU `t`, computing the stayer ARPDAU that keeps the lifetime average equal to `a` (formula in the interactive spec). Reproduce the lecture's section 3 table and the day-73 payback.
9. **Plan.** You have $100,000 for one month and a 120-day payback requirement. Allocate it across the paid channels, and state for each the net LTV you used, its horizon, and the cohort it describes.

## Deliverable

Your completed `ltv.py` with passing tests and the step 8 extension, the channel table from step 5, the sensitivity result from step 7, and an acquisition plan of at most 600 words (step 9).

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Implementation | All tests pass; closed form and sum agree | Tests pass | Tests fail | 25% |
| Channel report | Correct LTV, ratio and payback for all four, organic handled sensibly | One channel wrong or organic mishandled | Missing | 15% |
| Sensitivity | All four parameters solved, conclusion tied to the tail | Some parameters solved | Missing | 20% |
| ARPDAU by type | Table and day-73 payback reproduced | Extension runs, numbers off | Missing | 15% |
| Acquisition plan | Every LTV states horizon, fee basis and cohort; budget respects payback | One of the three labels missing | LTV used without labels | 25% |
