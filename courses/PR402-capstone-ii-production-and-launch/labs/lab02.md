# PR402 Lab 02: Content pipeline sheet

**Week:** 2 (Production sprint 2). **Guide:** [week 2](../lectures/w02-production-sprint-2-content-pipeline.md). **Team lab**, submitted once per team.

## Objective

Find the stage that limits how much content you ship, set a WIP limit that keeps lead time short, and turn the remaining gap into a written scope decision. The checker computes each stage's capacity, the bottleneck, Little's law lead time and the forecast at content lock.

## Starter materials

In [`labs/lab02-starter/`](lab02-starter/):

- `check_pipeline.py`. Standard library only. Run it with `.venv/bin/python check_pipeline.py pipeline.csv params.csv`. It prints each stage's capacity, the bottleneck, lead time and forecast, then `PASS` or `NOT READY`, and exits with code 1 when a rule fails.
- `pipeline.csv`. Emberfall's plan A from the guide, with one source left blank.
- `params.csv`. Content production weeks to content lock (4, weeks 4 to 7), WIP limit, minutes per item, target minutes and the gap decision (blank).

## Steps

1. **Warm-up (10 minutes).** Run the checker on the starter files. Change them to plan C from the guide (write 10 hours, script 4 hours per item, WIP 3), fill the missing source and write a gap decision. The checker should report dress as the bottleneck, `X = 1.50`, 6 items and 90 minutes, then `PASS`.
2. **Your stages.** Replace `pipeline.csv` with your own content pipeline. Use one row per stage an item passes through, in order. If you have more than one content type (quests and dungeons, say), make one sheet per type.
3. **Your hours.** For each stage, enter the owner's content hours per week in weeks 4 to 7, after the ops tax from lab 01, and the touch hours per item from the item you timed before class. Write where each number came from in `source`.
4. **First run.** Record the bottleneck, throughput and forecast. Save the output as `run-1.txt`.
5. **One fix.** Design one change that raises throughput: a tool or template at the bottleneck, hours moved between adjacent skills, or a simpler item type. Save the output as `run-2.txt`. If your fix does not raise `X`, explain why in two sentences and try again.
6. **WIP limit.** Set `wip_limit` so the lead time is two weeks or less. Put the limit on your board.
7. **Gap decision.** If the forecast is short of your PR401 target, write in `gap_decision` what closes the gap: a cut to the target, repeatable content, or both. Update your content plan to match.
8. **Weekly update.** At each review until week 7, replace estimated touch hours with measured ones and rerun.

## Deliverable

In `production/week02/` in the team repository:

- `pipeline.csv` and `params.csv` for the chosen plan, passing `check_pipeline.py`, with `run-1.txt` and `run-2.txt`.
- The updated content plan, with each item marked build, template, repeatable or cut.

**Checkable output:** the instructor reruns `check_pipeline.py` on your files. It must print `PASS` and exit with code 0.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Checker passes | 4 | `PASS` on rerun; run files match |
| Measured inputs | 4 | Touch hours come from a timed item or logs, with sources; hours per week agree with lab 01 |
| Bottleneck fix | 4 | The fix raises `X`, and the team can say which stage becomes the next bottleneck |
| WIP limit | 3 | Lead time at most two weeks, and the limit is visible on the board |
| Scope decision | 3 | The gap is closed by a written decision that matches the updated content plan |
| Weekly remeasure | 2 | At least one later rerun with measured touch hours committed by week 4 |
