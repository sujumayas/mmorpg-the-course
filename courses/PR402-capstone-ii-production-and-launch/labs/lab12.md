# PR402 Lab 12: Patch sizing and release plan

**Week:** 12 (Patch). **Guide:** [week 12](../lectures/w12-patch.md). **Team lab**, submitted once per team.

## Objective

Size your first live patch from your own track record, choose its contents by a written rule, and fix the release plan (freezes, go/no-go, rollout, cut order) before the code freeze. Every number in the sheet must be reproducible by the instructor from the inputs in the sheet.

## Starter materials

Copy this template into `production/week12/lab12.md`. The selection script from section 3 of the guide can be adapted to check your arithmetic; save your version as `production/week12/select.py` if you use it.

```markdown
## Part A. Budget
Planned hours to code freeze, by week (from lab 11): __ + __ = H = __
Release work X (list the tasks and hours): __
A = H − X = __

| Sprint | Estimated h | Actual h | Ratio |
|---|---|---|---|
| | | | |
| Total | | | R = |

Which R you use (all sprints, last two, other) and why: __
E = A / R = __

## Part B. Selection
| Item | Must-fix? | Estimate h | Players affected per week | Source of that number | Players per h | In/Cut | Running total |
|---|---|---|---|---|---|---|---|

Selected estimate total: __   Expected actual R × total: __   Slack A − expected: __
Exceptions to the rule (item, reason): __
Cut order (first to leave at the top): __

## Part C. Release plan
Feature freeze (date, time): __   Code freeze: __   Release: __ (who is online for 4 h after)
Go/no-go criteria (at least four, each checkable): __
Rollout steps with the metric watched and the wait at each step: __
Rollback tested on staging (date, by whom): __

## Part D. After the release
Go/no-go record (each criterion: pass/fail): __
Cuts made on the way (item, date, reason): __
Patch notes link: __
| Item | Metric expected to move | Before | Expected after | Check date |
|---|---|---|---|---|
```

## Steps

1. **Warm-up (10 minutes).** Enter the Emberfall numbers from the guide and confirm `E = 43.2`, a plan of 39 estimated hours and 5.6 hours of slack. Delete them.
2. **Part A.** Take `H` from lab 11. List your release work from your launch build's actual log, not from memory. Compute `R` from your sprint records. If you use a subset of sprints, say why.
3. **Part B.** List every candidate. Mark must-fix items (SEV1 and SEV2, by the week 4 mapping). For every other item, give players affected per week and where the number came from (a query, a ticket count, a cohort). Run the rule. Write the cut order.
4. **Part C.** Set the freezes and release slot. Write go/no-go criteria that someone outside the team could check. Test the rollback on your staging server and record it.
5. **Ship.** Follow the plan. Record every cut and the go/no-go outcome in Part D as it happens.
6. **Part D.** Publish player-facing patch notes. For every shipped item, write the metric you expect to move and when you will check it.

## Deliverable

`production/week12/lab12.md` complete, the tagged build, and the patch notes.

**Checkable output:** the instructor recomputes `A`, `R`, `E`, the selection (applying your stated rule to your table), the expected actual hours and the slack. The recomputed selection must match your In/Cut column except for exceptions you listed. The build tag in the repository must match the version in the patch notes.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Budget arithmetic | 4 | `A`, `R`, `E`, expected actual and slack all recompute |
| Selection | 4 | Rule applied correctly; every exception written with a reason; every player count sourced |
| Cut order | 2 | Written before feature freeze; followed if cuts were needed |
| Release plan | 5 | Freezes set; four or more checkable go/no-go criteria; staged rollout with metrics and waits; rollback tested |
| Shipped and recorded | 3 | Patch live with a tag and a go/no-go record, or a no-go decision tied to a criterion |
| Patch notes and metrics | 2 | Player-facing notes; every shipped item has an expected metric and a check date |
