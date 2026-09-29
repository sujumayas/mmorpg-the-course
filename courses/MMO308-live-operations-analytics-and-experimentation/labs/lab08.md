# MMO308 · Lab 08: Measure an event and plan a calendar

**Week:** 8, event design and calendars ([lecture](../lectures/w08-event-design-and-calendars.md)).
**Time:** 2 hours in the lab, plus up to 2 hours to finish.
**Work mode:** pairs.
**Counts toward:** analytics labs (40% of the course grade).

## Objective

Measure what a ten-day announced event added to a game's player-hours, show how much a lazy baseline inflates the report, and use the recovery model to plan a 12-week calendar you can defend in numbers.

## Starter materials

All in [`lab08-starter/`](lab08-starter/). Standard-library Python.

- [`daily_hours.csv`](lab08-starter/daily_hours.csv): 120 days of synthetic player-hours (`day`, `weekday`, `player_hours`). Day 0 is a Monday. Weekends run higher. The event was announced on day 70, ran on days 84 to 93, and play had settled by day 108.
- [`event_lift.py`](lab08-starter/event_lift.py): a loader, the phase ranges as constants, and stubs for `weekday_medians`, `baseline_series`, `flat_baseline`, `lift_summary`, `recovery_lift` and `yearly_lift_days`.
- [`test_event_lift.py`](lab08-starter/test_event_lift.py): seven tests from the lecture's example and the CSV. All seven fail on the starter.

```
.venv/bin/python courses/MMO308-live-operations-analytics-and-experimentation/labs/lab08-starter/test_event_lift.py
```

- The event interactive, `examples/w08-event-pull-forward.html`, to check flat-phase cases.

## Steps

### Part A: measure (60 min)

1. **Baseline.** Implement `weekday_medians` over the four clean weeks (days 42 to 69) and `baseline_series`. Explain in one sentence why a median per weekday beats one mean over all 28 days for this data.
2. **Lift.** Implement `lift_summary`. The lecture test must give gross 60,000, borrowed 35,000 and net 25,000.
3. **The event.** Run it on the CSV. Report gross, borrowed, net and the incrementality ratio. Plot the actual series, the baseline and the cumulative lift from day 70 on one figure (any plotting tool).
4. **The lazy baseline.** Implement `flat_baseline` and compute the gross lift against the mean of days 77 to 83. By what percent does it overstate the gross? Repeat with days 63 to 69 (the week before the announcement) and explain why that shortcut lands much closer.
5. **Window length.** Recompute net lift with the post window cut at day 97 instead of 108. How much hangover does a three-day window miss?

### Part B: plan (45 min)

6. **Spacing.** Implement `recovery_lift` and `yearly_lift_days` and reproduce the lecture's table for `L_max = 60%`, `τ = 30`, ten-day events.
7. **Fit your own τ.** A previous season had four events of the same kind with these gaps and measured lifts: 20 days, 30%; 40 days, 45%; 60 days, 52%; 100 days, 58%. Find the `L_max` and `τ` that fit best (a grid search over `L_max` from 50% to 70% and `τ` from 10 to 60 is enough). Report the fit and its largest error.
8. **Calendar.** Using your fitted model and this lab's incrementality ratio, plan 12 weeks with four events for three segments (new, established, lapsed). Give each event a goal as "metric, segment, target" and an expected gross and net lift. No two events for the same segment may overlap.

## Deliverable

Your `event_lift.py` with all tests passing, the figure from step 3, and a one-page event report: the measured lift with the baseline method named, the size of the lazy-baseline error, your fitted `L_max` and `τ`, and the 12-week calendar table.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Code correctness | All seven tests pass; ranges handled without off-by-one errors | Tests pass with hard-coded cases | Tests fail | 25% |
| Measurement | Gross, borrowed, net and ratio correct; figure shows the cumulative lift settling | One quantity wrong or figure unclear | Spike reported as the effect | 25% |
| Baseline critique | Both lazy baselines quantified and the difference explained; window-length effect sized | Quantified without explanation | Missing | 20% |
| Calendar | Fitted model used; goals measurable; overlap rule respected; lifts shown | Calendar sound but not tied to the model | No numbers | 20% |
| Report writing | Plain, numeric, fits on one page | Some vague claims | Hard to act on | 10% |
