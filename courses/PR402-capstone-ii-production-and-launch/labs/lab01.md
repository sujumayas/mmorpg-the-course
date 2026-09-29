# PR402 Lab 01: Capacity plan under the ops tax

**Week:** 1 (Production sprint 1). **Guide:** [week 1](../lectures/w01-production-sprint-1-the-ops-tax.md). **Team lab**, submitted once per team.

## Objective

Turn your PR401 production plan into a capacity plan that survives contact with a live build. You will measure your rate from the vertical slice sprints, set an ops tax for every week to content lock, split the backlog into a feature budget and a content budget, and mark every item keep, trigger or cut. A checker script tells you whether the plan fits.

## Starter materials

In [`labs/lab01-starter/`](lab01-starter/):

- `check_capacity.py`. Standard library only. Run it with `.venv/bin/python check_capacity.py history.csv plan.csv backlog.csv`. It prints the rate, each week's backlog points, both budgets with their low values, then `PASS` or `NOT READY`. It exits with code 1 when the plan does not fit.
- `history.csv`. The Emberfall slice sprints from the week 1 guide.
- `plan.csv`. The Emberfall tax schedule. The `measured_tax` column stays empty until each week's review.
- `backlog.csv`. An Emberfall backlog with every item marked `keep`. It fails the checker on purpose.

## Steps

1. **Warm-up (15 minutes).** Run the checker on the starter files and read the four failures. Mark items in `backlog.csv` as `trigger` or `cut` until it prints `PASS`. Write a pillar check for each. Compare budgets with the guide's table (74.5 and 59.9).
2. **Your history.** Replace `history.csv` with your PR401 slice sprints. Count done points only. Commit the board exports next to the file.
3. **Your tax schedule.** Fill `plan.csv` with your available hours per week and a planned tax for weeks 1 to 7. Write one sentence in `note` for each phase explaining the number.
4. **Your backlog.** Put every remaining item from your PR401 production plan in `backlog.csv`, typed `feature` or `content`, with points. Include at least one ops-reducing feature (deploy script, crash reporter, admin tools).
5. **Cut and trigger.** Mark items until the checker prints `PASS`. Trigger items are what you cut first if a sprint comes in slow. They must cover the gap between each budget and its low value.
6. **Cut memo.** Write `cut-memo.md`: the five largest cuts or triggers, the pillar each touches, and what the player loses. Every team member signs with their name and the date.
7. **Weekly update.** At each sprint review from week 2 to week 7, enter the measured tax for the week just finished and rerun the checker. If it fails, move the line and commit the new `backlog.csv` with a one-line reason in the commit message.

## Deliverable

In `production/week01/` in the team repository:

- `history.csv`, `plan.csv`, `backlog.csv` that pass `check_capacity.py`, and the output saved as `check-output.txt`.
- `cut-memo.md`, signed.
- The PR401 board exports used for `history.csv`.

**Checkable output:** the instructor reruns `check_capacity.py` on your three files. It must print `PASS` and exit with code 0. From week 2 on, the instructor reruns it with your measured taxes, and it must still pass.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Checker passes | 4 | `PASS` on rerun, output file matches |
| Honest rate | 4 | Done points only; hours match the board exports; no half-finished stories counted |
| Tax schedule | 3 | Every week set, justified per phase, within the checker's floors |
| Two budgets | 3 | Features and content split correctly; no content item disguised as a feature or the reverse |
| Cuts and triggers | 4 | Pillar check on every row; triggers cover the band; at least one ops-reducing story kept |
| Cut memo | 2 | Five cuts named with player impact; signed by the whole team |
