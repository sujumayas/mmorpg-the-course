# PR402 Lab 6: Balance review sheet

**Week:** 6 (Telemetry and balance review). **Guide:** [week 6](../lectures/w06-telemetry-and-balance-review.md). **Team lab**, submitted once per team.

## Objective

Turn your cleaned closed-beta telemetry into a balance review sheet in which every verdict follows from its numbers, and a change log in which every change predicts a value you can test in open beta.

## Starter materials

Create `production/week06/balance-review.csv` with these columns, in this order:

```
id,question,metric,unit,n,mean,sd,t,lo,hi,band_lo,band_hi,band_set,verdict,note
```

- `unit` is `player` or `party`. `n` counts units, never events.
- `t` is the two-sided 95% t value for `n − 1` degrees of freedom, from any t table (for `n` above 30, 2.05 is close enough; for 60 and above, 2.00).
- `lo` and `hi` are `mean ± t × sd / √n`, rounded to two decimals.
- `band_set` is the date the band was written, from your PR401 balance document, or `after-beta` if you set it this week.
- `verdict` is `act`, `leave` or `cant_decide`, by the rule in guide section 5.

Create `production/week06/change-log.md` with one block per `act` row:

```
Row: B2   Lever: Hexer base damage   Old: 100%   New: 77%
Model: (8.9 - 2.0) / (11.0 - 2.0) = 0.767
Simulator: run id / commit, predicted kill time 11.0 s (sim result: ___ s)
Predicted metric for open beta: 11.0 s, band 10.2-13.8
```

## Steps

1. **Warm-up (15 minutes).** Enter the four classes from the guide's worked example as rows W1 to W4. Your `lo`, `hi` and verdicts must match the guide's table to two decimals. Add row W5 for the Warden with kills as `n` (`n = 400`, `sd = 4.0`, `t = 1.96`) and write in `note` why this row is wrong. Delete W1 to W5 before you submit, or move them to a `warmup.csv`.
2. **Clean.** Run your filter script on the raw export. Record in `cleaning-log.md` the event counts before and after removing internal accounts, and the build numbers present. If more than one build is present, use only the last one and say how many events that dropped.
3. **Targets.** List every numeric target in your PR401 balance document that the closed beta could have touched. Each becomes a row. Add at least one party-level row for your first group encounter.
4. **Compute.** For each row, compute the per-unit values first (per-player median, or per-party first-attempt result), then `mean`, `sd`, `lo`, `hi`. For a party clear rate, use a Wilson interval instead (PR201 week 11) and put the rate and bounds in `mean`, `lo`, `hi`, with `t` left blank.
5. **Verdicts.** Apply the rule. Do not adjust a band after seeing the interval. If you think a band is wrong, add a new row with the new band, `band_set = after-beta`, and keep the original.
6. **Size the changes.** For every `act` row, write a change-log block. Use the section 4 formula or a simulator run, and state the predicted metric value. One lever per class.
7. **Targeted tests.** For every `cant_decide` row, compute the units needed, `n ≈ (1.96 × sd / gap)²`, where `gap` is the distance from the mean to the nearer band edge. Add it to `open-beta-tests.md` with the telemetry event it needs and an owner.

## Deliverable

In `production/week06/`: `cleaning-log.md`, `balance-review.csv`, `change-log.md`, `open-beta-tests.md`.

**Checkable output:** the instructor picks two rows of `balance-review.csv` and recomputes `lo`, `hi` and the verdict from `n`, `mean`, `sd`, `t` and the band. Both must match to two decimals. The instructor also recomputes one change-log prediction from its formula.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Warm-up | 2 | W1 to W4 match the guide; W5's note names the unit error |
| Cleaning | 3 | Counts before and after, builds listed, script in the repository |
| Units and arithmetic | 5 | Every `n` counts players or parties; two random rows recompute exactly |
| Bands and verdicts | 4 | Bands dated, no band moved after the data, verdicts follow the rule |
| Change log | 4 | Every `act` row sized with a stated model and a predicted value; one lever per class |
| Targeted tests | 2 | Every `cant_decide` row has units needed, the event, and an owner |
