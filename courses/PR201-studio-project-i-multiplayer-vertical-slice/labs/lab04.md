# PR201 · Lab 04: Sprint 1 plan and daily log

**Week:** 4 (runs through the sprint) · **Time:** 90 minutes of planning in the studio session plus 5 minutes a day · **Weight:** a sprint record for [milestone 3, alpha](../assessments/m3-alpha-brief.md) (sprint process row)

## Objective

Plan sprint 1 so that nobody is committed past their limit, then keep a daily log that lets you draw a burn-down and a burn-up and forecast the end of the sprint from either. The model is in section 2 of the [week 4 guide](../lectures/w04-sprint-1-networking-skeleton.md).

## Starter materials

Folder `lab04-starter/`. Standard library Python only.

- `availability.csv`: `member` and `hours_available` for this sprint.
- `backlog.csv`: `id`, `task`, `owner`, `estimate_h`, `goal` (`y` or `n`) and `acceptance`. The starter holds the 16 *Hollowmarch* tasks, with one assignment wrong.
- `daily.csv`: `day`, `remaining_h` and `scope_h`, one row per working day, from day 0.
- `check_sprint.py`: checks task size, owners, acceptance lines, and per-person and team limits, and with a daily log prints the done column and both forecasts at `--day` (default 6). Options `--weeks`, `--c`, `--focus`, `--max-task` and `--days` default to 2, 0.25, 0.7, 4 and 10.

## Steps

1. **Read a failure.** Run `python check_sprint.py availability.csv backlog.csv daily.csv`. It prints `NOT READY`: the starter gives T9 to Ben, who is then committed 12 hours against a limit of 9.45. Write one sentence on why the team total of 48 against 52.5 still passed.
2. **Reproduce the guide.** Move T9 back to Ana, as in the guide's table, and rerun. Confirm `PASS`, the team limit of 52.5, the 48 committed hours, the 27 goal hours and the two day-6 forecasts (29.7 and 23.0).
3. **Your sprint goal.** Write it so a stranger can test it on two machines in five minutes.
4. **Your backlog.** Split the must-tier skeleton and your funded spikes into tasks of 4 hours or less, each with an owner and an acceptance line. Mark goal tasks. Run the checker until `PASS`.
5. **Daily log.** Each working day before the standup, every owner updates remaining hours. The chart owner adds one row to `daily.csv`. A discovered task gets a card and raises `scope_h` the same day.
6. **Mid-sprint forecast.** On day 5 or 6, run the checker with `--day` set to that day. Write both forecasts, which one you believe, and the decision you took (for example, no new non-goal tasks).
7. **Charts.** At the end of the sprint, draw both charts from `daily.csv` in any tool, with the scope line visible.

## Deliverable

`availability.csv`, `backlog.csv`, `daily.csv`, the planning-day checker output, the step 1 sentence, the step 6 forecast note and both charts, in `docs/sprint-1/`. Bring them to the week 5 review.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Sprint goal | Testable on two machines in five minutes by a stranger | Testable with explanation | Vague | 15% |
| Backlog | Checker passes on planning day; acceptance lines checkable by someone else | Passes, acceptance vague | Does not pass | 25% |
| Daily log | A row for every working day; scope changes on the day found | One or two gaps | Reconstructed at the end | 25% |
| Forecast and decision | Both forecasts computed mid-sprint, one chosen with a reason, decision recorded | Forecasts without decision | Missing | 20% |
| Charts | Both charts correct, scope line visible, goal tasks marked | One chart | Missing | 15% |
