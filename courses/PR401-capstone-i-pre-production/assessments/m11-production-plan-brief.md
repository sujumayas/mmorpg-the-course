# PR401 · Milestone 11 brief: production plan

**Weight:** 7% of the course grade, inside the pre-production package component (50%).
**Assigned:** week 11. **Due:** at the start of the week 12 meeting, in `preproduction/week11/`. **Reviewed:** at the end of the week 11 meeting (draft) and again at the week 14 review.
**Work mode:** team. One team mark, adjusted per person by the [peer assessment](peer-assessment-brief.md).
**Session guide and lab:** [week 11, production plan](../lectures/w11-production-plan.md) with [lab 11](../labs/lab11.md).
**Builds on:** [PR101 week 4](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w04-scope-mvp-vertical-slice-cut-lists.md), section 5 (ordered cut lists and triggers), [PR101 week 12, crunch](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w12-crunch-causes-costs-alternatives.md) (why "the artist will work more" is not a move), [PR101 week 7, task tracking](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w07-task-tracking-and-definitions-of-done.md), and [MMO403 week 13, team and budget planning](../../MMO403-business-monetization-and-ethics-of-live-games/lectures/w13-team-and-budget-planning.md).

## What this milestone proves

That the plan fits in every discipline, not only in total. *Emberfall*'s backlog was at 0.80 for the whole team and 1.44 for its one artist, which would have left towns grey at launch. Moving work to the tech-art student and buying a prop kit brought art to 0.94, with a boss-model cut held in reserve behind a trigger. The plan is marked on finding the constraint and relieving it with a move whose cost someone agreed to pay.

## Deliverables

1. **Production plan** (`production-plan.md`) with the parts from week 11 section 5: the calendar mapped to PR402 weeks with milestone definitions, the capacity table with sourced inputs, the load table per discipline for the whole window and per milestone, the staffed backlog as a linked export, the ordered cut list, and the risk register with triggers and pre-chosen responses.
2. **`team.csv` and `backlog.csv`** in the lab 11 format, with `check_plan.py` printing `PASS`.
3. **Constraint log** (`constraint-log.md`), half a page: the starting load table, each move, who paid for it, and the final table.

## Evidence required

| Evidence | Format | How the instructor checks it |
|---|---|---|
| Loads | Checker output | Reruns `check_plan.py`; every discipline at or below 1.0 for the window and each milestone |
| Sourced inputs | `inputs.md` | Hours from the charter; `f` and `R` from the week 6 fit sheet, or a stated reason |
| Constraint moves | `constraint-log.md` | Each move has hours, conversion factor, who pays and any pillar touched |
| Order | `backlog.csv` | No forward dependencies; alpha items in PR402 sprints 1 to 3 |
| Cut list | Plan section | Ordered, hours freed, pillar touched |
| Triggers | Risk register | Each risk has an observable trigger and a pre-chosen response |

## How it is marked

The instructor reruns the checker at the end of the week 11 meeting as feedback, and marks the version submitted at the start of week 12. At the week 14 review the panel reads the replanned version, which is marked in [milestone 13](m13-pre-production-review-and-package-brief.md).

## Rubric

| Criterion | Points | Full marks when | Low marks when |
|---|---|---|---|
| Checker passes | 10 | `PASS` on rerun, output matches | Fails |
| Capacity per discipline | 15 | Every input sourced; people who split disciplines counted as fractions; absences subtracted | Whole-team capacity only |
| Constraint found and relieved | 20 | Starting table saved; constraint named; each move states hours, conversion, who pays; the new constraint checked | Loads fixed by editing estimates |
| Slack where it matters | 10 | Programming at or below 0.90 by alpha, or a stated reason | Every discipline at exactly 1.00 |
| Milestone mapping and dependencies | 15 | Alpha items in sprints 1 to 3; no forward dependency; one long chain broken with a named stub | Items after the things they depend on |
| Cut list | 10 | Ordered, hours per cut, pillar touched, first cut ready to take | Unordered, or cuts that remove a pillar |
| Risk triggers | 15 | Each risk has an observable trigger and a pre-chosen response | "If art falls behind" |
| Team ownership | 5 | Any member explains the constraint and the move | Only the producer can |
| **Total** | **100** | | |

## Late and missing work

Up to 48 hours late is capped at 70. The slice sprints are planned from this file, so it must exist before week 12 even if it scores 0.
