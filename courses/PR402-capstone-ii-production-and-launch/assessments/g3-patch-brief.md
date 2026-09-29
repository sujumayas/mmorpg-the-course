# PR402 · Launched game brief 3: patch

**Weight:** 6% of the course grade, inside the launched game component (40%).
**Assigned:** week 11. **Due:** the release plan (lab 12 parts A to C) before feature freeze; the patch live, or a recorded no-go, by the end of week 12; all records in `production/week12/` before the week 13 meeting.
**Work mode:** team. One team mark, adjusted per person by the [peer assessment](peer-assessment-brief.md).
**Session guide:** [week 12, patch](../lectures/w12-patch.md). **Lab:** [12](../labs/lab12.md).

## What this milestone proves

That the team ships a planned update to live players on a date it announced, with scope sized from its own track record and a cut order written before anything went wrong. Live games choose a fixed date and variable scope ([week 12, section 2](../lectures/w12-patch.md)). The patch is marked on whether the plan fitted with room to spare, whether the release followed the plan, and whether each item names the number it should move.

Cutting an item on schedule by the cut order is success, not failure. A patch that ships four of six planned items on the announced day, with the cuts in the order written before feature freeze, can score full marks.

## Gates

- **G1. Versioned and rolled back once.** The patch has a version and build number, and a rollback to the previous build was tested on staging before code freeze.
- **G2. Criteria before freeze.** Go or no-go criteria and the cut order are committed before code freeze.

## Deliverables

1. **Lab 12 worksheet**, parts A to D: `H`, `X`, `A`, the sprint table and `R` with the reason for the subset used, `E`; the candidate table and selection; expected actual hours and slack; exceptions; cut order; freeze dates; go or no-go criteria; rollout steps; post-release records.
2. **The patch**, tagged, live for all players by the end of week 12, or held by a recorded no-go decision against a named criterion.
3. **Release record**: go or no-go with each criterion marked, rollout steps with times and the metric watched at each, any cut with its date and reason.
4. **Patch notes** as published, in player terms.
5. **Expected-number list**: for each shipped item, the metric expected to move, its value before, the expected value after and the check date.

## Evidence required

| Evidence | Format | How the instructor checks it |
|---|---|---|
| Sprint records | Estimated and actual hours for sprints 1 to 4 | Recomputes `R` and `E` |
| Planned hours | Lab 11 planned hours for weeks 11 and 12 | Checks `H` matches lab 11 |
| Candidate data | Queries or ticket counts behind "players affected per week" | Checks one count against its query |
| Build | Tag, deploy log, staged rollout log | Checks the tag matches the version in the patch notes and that rollout expanded only after its watch period |
| Rollback | Staging log with date and person | Confirms it predates code freeze |
| Telemetry | Crash rate and error log during rollout; before values for each expected number | Compares the rollout decision with the crash rate at each step |
| Commit history | Cut order, criteria, freeze dates | Checks they were committed before feature freeze and code freeze |

## How it is marked

The instructor marks the plan before feature freeze with a short written note, and the full folder before the week 13 meeting. The expected numbers are checked a week later as evidence for the [post-mortem](post-mortem-brief.md). The lab 12 rubric is the detailed scoring guide for rows 1 to 4.

## Rubric

| Criterion | Points | Full marks when | Low marks when |
|---|---|---|---|
| Budget arithmetic | 15 | `A`, `R`, `E`, expected actual and slack recompute; release work `X` taken from the launch build's log | Estimates compared with hours as if `R` were 1; release work forgotten |
| Selection by rule | 20 | Must-fix items first; the rest by players per estimated hour with sourced counts; exceptions written with reasons | Items picked by preference with no rule |
| Cut order and freezes | 15 | Cut order written before feature freeze and followed; feature freeze three days and code freeze one day before release | Items added after feature freeze "because it's tiny" |
| Release plan and go or no-go | 15 | Four or more checkable criteria; staged rollout with a metric and wait at each step; two people online four hours after deploy | Friday-night deploy with nobody watching |
| Shipped on the date | 15 | Live by the end of week 12 with a tag and go record, or a no-go tied to a criterion and a new date announced | Late with no decision on record; silent slip |
| Patch notes | 10 | Written in player terms, grouped by what players do, reporters credited where they agreed | "Refactored inventory sync" |
| Expected numbers | 10 | Every shipped item has a metric, before value, expected value and check date | Items with no measurable effect named |
| **Total** | **100** | | |

## Builds on

- [PR401 week 11, production plan](../../PR401-capstone-i-pre-production/lectures/w11-production-plan.md) (the post-launch list the candidates come from).
- [PR101 week 6, estimation and why it fails](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w06-estimation-and-why-it-fails.md) (the plan ratio `R` and buffer), [week 4, cut lists](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w04-scope-mvp-vertical-slice-cut-lists.md) and [week 13, builds and release checklists](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w13-builds-and-release-checklists.md).
- [MMO302 week 14, observability](../../MMO302-mmo-server-architecture/lectures/w14-observability-logs-metrics-traces.md) (what you watch during rollout).
- [MMO308 week 9, patch management and hotfixes](../../MMO308-live-operations-analytics-and-experimentation/lectures/w09-patch-management-and-hotfixes.md) and its [staged rollout model](../../MMO308-live-operations-analytics-and-experimentation/examples/w09-staged-rollout.html); [week 10, feedback loops](../../MMO308-live-operations-analytics-and-experimentation/lectures/w10-player-feedback-loops-forums-surveys-polls.md).
- [MMO407 week 10, recovery strategies](../../MMO407-launch-scaling-and-post-mortems/lectures/w10-recovery-strategies.md) (trust and a moved date).
