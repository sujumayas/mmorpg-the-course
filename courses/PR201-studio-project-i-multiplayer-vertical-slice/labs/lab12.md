# PR201 Lab 12: Sprint 4 polish budget and cut line

**Week:** 12 (Sprint 4: polish). **Guide:** [week 12](../lectures/w12-sprint-4-polish.md). **Team lab**, submitted once per team.

## Objective

Plan sprint 4 from measured numbers. Every hour is an estimated hour, the unit of every sprint so far. You will pull your fix-load inputs from the tracker, convert logged fix hours to estimated hours, compute how much of the sprint forecast `f × U` remains for polish after the beta bug bar, and fill that budget from your week 11 input list in value-per-hour order. The output is a sprint plan whose cut line anyone can recompute.

## Starter materials

In [`labs/lab12-starter/`](lab12-starter/):

- `plan_polish.py`. Standard library only. Run `.venv/bin/python plan_polish.py sprint4.csv polish.csv`. It prints the forecast, the fix load in estimated hours, the polish budget and the greedy fill, then `PASS` or `NOT READY`, and exits with code 1 when anything is missing or inconsistent.
- `sprint4.csv`. The eight inputs (`U`, `f`, `O`, `B`, `N`, `r`, `h`, `q`) with Hollowmarch's values from the guide and the `source` column empty.
- `polish.csv`. Hollowmarch's eight polish items with `evidence`, `done_test` and `decision` empty.

## Steps

### Part A: inputs (30 minutes)

1. **Warm-up.** Fill the starter files with placeholder sources and evidence, set the decisions the guide's table gives, and run the script until it passes. You should see a forecast of 39.9, a polish budget of 9.5 hours and 9.0 planned.
2. **Your inputs.** Replace every value in `sprint4.csv` with your team's own. For each, the `source` column names the query or record it came from, for example "tracker: bugs created in sprint 3, 20 rows" or "sprint 3 board: 5 of 25 fixes reopened". If you have no record, write `guess` and the reason.
   - `U`: useful hours for the sprint: available hours after known absences, minus coordination (week 4).
   - `f`: focus over sprints 1 to 3, estimated hours done divided by useful hours (week 5).
   - `O`: overhead tasks at their estimates: the beta build and its checklist, the internal playtest.
   - `B`: open P1 and P2 bugs now.
   - `N`: expected new P1 and P2 bugs during the sprint (bugs found per sprint since week 7 × P1/P2 share).
   - `r`: regression rate (fixes reopened or causing a new ticket, divided by fixes, since week 7).
   - `h`: mean logged hours per fix since week 7. These are actual hours; the script divides them by `q`.
   - `q`: sprint 3 actual hours ÷ estimated hours.

### Part B: the polish list (40 minutes)

3. **Items.** Replace the rows in `polish.csv` with your own candidates from the week 11 input list. Every row's `evidence` names the week 11 finding ID. Items with no finding behind them don't belong in this file.
4. **Value.** Score each item from 1 to 10 against written anchors. Put the anchors at the top of `plan.md`.
5. **Run the script without decisions.** Read the model column, then write the same decisions into `decision`. If the team disagrees with the model on an item, change the value score and write one sentence in `plan.md` saying why. Don't overrule the cut line by hand.
6. **Definitions of done.** For every item marked `in`, write a `done_test` a tester who did not make the change can run, including a second client and network conditions where the item is networked.
7. **Run the script** until it prints `PASS`. Save the output as `plan-output.txt`.

### Part C: the lever (10 minutes)

8. In `plan.md`, compute the polish budget twice more: once with `U + 10` and once with `r` lowered by 0.1. Explain in one sentence why the extra 10 hours add only `f × 10` to the budget. Name one concrete practice your team will adopt to lower `r` this sprint, and the person who owns it.

## Deliverable

In `production/week12/`: `sprint4.csv`, `polish.csv`, `plan-output.txt`, and `plan.md` (value anchors, any value changes with reasons, the two lever calculations and the `r` practice).

**Checkable output:** the instructor reruns `plan_polish.py` on your two CSV files. It must print `PASS` and exit with code 0, and the budget must match `plan-output.txt`.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Checker passes | 4 | `PASS` on rerun, output matches the saved file |
| Inputs sourced | 5 | Every input cites a tracker query or record; guesses are labelled with a reason; no polish estimate is multiplied by the ratio |
| Evidence trail | 3 | Every item names a week 11 finding |
| Definitions of done | 4 | Every item above the line has a test a non-author can run; networked items name the second client and conditions |
| Lever analysis | 2 | Both recomputed budgets correct; a named practice and owner for lowering `r` |
| Value anchors | 2 | Written before scoring; any change to fit the team's preference is explained |

<details>
<summary>Instructor notes</summary>

- Warm-up: forecast 39.9, 13.8 fixes, 25.4 fix estimate-hours, polish budget 9.5, planned 9.0 (revive prompt, tutorial, loot sparkle). With `U = 85`: 14.8. With `r = 0.1`: 12.3.
- A team that multiplies polish estimates by its ratio, or plans against calendar hours, has counted the overrun twice or not at all. Ask which unit each number is in.

</details>
