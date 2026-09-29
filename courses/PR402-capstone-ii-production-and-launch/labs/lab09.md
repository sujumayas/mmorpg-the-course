# PR402 Lab 9: Launch capacity plan and go or no-go record

**Week:** 9 (Launch). **Guide:** [week 9](../lectures/w09-launch.md). **Team lab**, submitted once per team.

## Objective

Make the launch decisions on paper before the doors open: a go or no-go record with evidence, a corrected demand forecast, a shard plan that balances the launch queue against the day-7 population, and a merge trigger you can test.

## Starter materials

Copy this template to `production/week09/launch-plan.md`.

```
## A. Forecast
Open-beta forecast peak ___   actual peak ___   error ratio ___
Launch audience ___ / beta audience ___ = scale ___
Arrival phases (attempts per minute, whole game):
  phase 1: ___ /min for ___ min
  phase 2: ___ /min for ___ min
  phase 3: ___ /min after
Day-7 evening peak forecast (total): ___ CCU   (method ___)

## B. Shard plan
Load-test knee ___ CCU (report ___)  headroom ___  cap per shard ___
Entry rate per shard ___ /min   Session length ___ min   Full admission rate = cap / session = ___
Alive threshold (PR401 social plan) ___ CCU   Wait limit ___ min
| Plan | Worst queue | At minute | Wait at back | Day-7 peak per shard | Passes? |
Chosen plan: ___
Merge trigger: ___   Staging merge tested on ___ (log ___)

## C. Go or no-go
| Criterion | Threshold | Evidence link | Owner | Pass/fail | If fail, then |
Decision: ___   Time: ___   Signed by: ___

## D. First 48 hours
Peak CCU ___   Worst queue observed ___   Crashes per 100 player-hours ___
Launch cohort n ___   returned day 1 ___   day-1 retention ___
```

A minute-by-minute queue script is in the guide's worked example. Copy it to `production/week09/queue.py`, replace the constants and the `arrivals` function with your values, and run it with `.venv/bin/python queue.py`.

## Steps

1. **Warm-up (10 minutes).** Run the guide's script unchanged. It must print a worst queue of 40.0 at minute 180 for one shard and 0.9 at minute 83 for two. Save the output as `warmup.txt`.
2. **Forecast.** Fill section A. Apply the open-beta error ratio to every phase. State the day-7 method in one line (for example open-beta day-3 peak times launch scale).
3. **Plans.** Run your script for one, two and (if relevant) three shards. Fill the table in section B for each.
4. **Choose.** Pick the plan and justify it in three sentences or fewer. If it uses a temporary shard, write a merge trigger in measurable terms and run the merge on staging with open-beta character data. Link the log.
5. **Go or no-go.** Fill section C with at least the seven criteria from guide section 2. The "if fail, then" column must be filled before the review. Commit it before the review starts.
6. **Launch.** Follow the run sheet. Fill section D at T+48 hours.

## Deliverable

In `production/week09/`: `warmup.txt`, `launch-plan.md` with all four sections, `queue.py` with your values and its output as `queue-output.txt`.

**Checkable output:** the instructor runs your `queue.py` and checks the output matches `queue-output.txt` and the table in section B. The instructor checks from the commit history that section C's thresholds and "if fail, then" column were committed before the decision time.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Warm-up | 2 | Output matches the guide |
| Forecast | 4 | Error ratio applied to every phase; day-7 method stated |
| Shard plan | 5 | At least two plans computed; script reproduces the table; choice justified against both limits |
| Merge trigger | 3 | Measurable; staging merge logged before launch (or no temporary shard) |
| Go or no-go | 4 | Seven or more criteria with evidence and owners; fallbacks written before the review |
| First 48 hours | 2 | All section D values reported with `n` |
