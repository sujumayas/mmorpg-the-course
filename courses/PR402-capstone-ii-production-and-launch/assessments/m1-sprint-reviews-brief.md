# PR402 · Milestone 1 brief: sprint reviews

**Weight:** 10% of the course grade, inside the milestones component (40%). The full weight map is in the [peer assessment brief](peer-assessment-brief.md#how-the-grade-is-built).
**Assigned:** week 1. **Due:** four reviews, each at the start of the studio meeting after the sprint ends. Sprint 1 at the start of week 2, sprint 2 at the start of week 3, sprint 3 at the start of week 4 (with the tagged alpha build), sprint 4 at the week 8 meeting.
**Work mode:** team. One team mark, adjusted per person by the [peer assessment](peer-assessment-brief.md).
**Session guides:** [week 1](../lectures/w01-production-sprint-1-the-ops-tax.md), [week 2](../lectures/w02-production-sprint-2-content-pipeline.md), [week 3](../lectures/w03-production-sprint-3-feature-complete-and-server-budget.md), [week 7](../lectures/w07-production-sprint-4.md). **Labs:** [01](../labs/lab01.md), [02](../labs/lab02.md), [03](../labs/lab03.md), [07](../labs/lab07.md).

## What this milestone proves

That the team plans from its own measured numbers and replans when they change. PR402 has four production sprints. Each ends in a review where the instructor checks the plan the team made against what the team did. Three questions run through all four reviews.

1. Did the team commit to what its measured rate and its ops tax allow, and no more?
2. Did it measure the ops tax honestly and replan when the measured value missed the planned one by more than 0.1 ([week 1, section 5](../lectures/w01-production-sprint-1-the-ops-tax.md))?
3. Is every cut written down, owned and agreed, so that nothing comes back as "we'll squeeze it in"?

A sprint that misses its forecast can still score well here. A sprint that hits its forecast with half-done stories counted as done cannot.

## Deliverables

Each review has its own deliverables, taken from the session guide's "Deliverables" section. All of them live in the team repository.

| Review | Due | Deliverables |
|---|---|---|
| Sprint 1 | Start of week 2 | Lab 01 capacity plan passing `check_capacity.py`; signed cut memo; sprint 1 board export with `feature`, `content`, `ops` tags; measured week 1 ops tax in `plan.csv`; sprint 1 increment deployed to the team server |
| Sprint 2 | Start of week 3 | Lab 02 pipeline sheet passing `check_pipeline.py`, with `run-1.txt` and `run-2.txt`; updated content plan; sprint 2 board with pipeline columns and a WIP limit; one content item through every stage and playable on the server, with measured touch hours |
| Sprint 3 | Start of week 4 | Alpha exit criteria (10 to 20 checkable lines, each marked pass or fail); lab 03 hosting budget passing `check_budget.py`; capacity plan for spikes; budget alert screenshot; alpha build tagged, deployed from the release pipeline and joinable from outside the team |
| Sprint 4 | Week 8 meeting | Lab 07 sprint plan (capacity at two velocities, buffer with its data source, commitment, ranked backlog with both lines); daily burn-down with bug points separate and the day-3 decision; post-launch list and cut list; open-beta readiness checklist with evidence; dated content-lock statement |

From sprint 2 on, every review also includes the lab 01 checker rerun with the measured tax for each week so far.

## Evidence required

| Evidence | Format | How the instructor checks it |
|---|---|---|
| Rate and velocity | PR401 slice board exports, PR402 board exports | Recomputes `r` for sprint 1 and planning velocity for sprint 4 from the exports; counts done items only |
| Ops tax | Time log with `feature`, `content`, `ops` tags | Recomputes one week's measured `t` from the log, and checks that bugs in a story's own code are not tagged `ops` |
| Checker outputs | `check_capacity.py`, `check_pipeline.py`, `check_budget.py` outputs saved in the lab folders | Reruns each checker on the committed files; the output must match and print `PASS` |
| Builds | Tags and deploy logs for the sprint 1 increment, the week 3 content item and the alpha candidate | Joins the alpha build from a machine outside the team; checks the tag matches the deploy log |
| Hosting spend | Provider billing page, `spend-log.md` | Compares actual spend to date with the lab 03 plan |
| Cuts | `cut-memo.md`, `cut-list.md`, `post-launch.md`, commit messages on `backlog.csv` | Picks one cut and asks two team members who agreed it and when |
| Burn-down | Tracker history for sprint 4 | Checks the day-3 row against the threshold written before the sprint started |

## How it is marked

Each review takes 10 minutes in the first part of the studio meeting and is scored on the day by the instructor. The lab rubric for that week (20 points each) is the detailed scoring guide for the "plan" row of the matching review. Its score is scaled to the row's points. Labs are not weighted separately, because the course's assessment line has no lab component.

A review missed without an agreed extension scores 0 for its 25 points. Documents handed in within 48 hours after the review are capped at 70% for their rows.

## Rubric

| Review | Criterion | Points | Full marks when | Low marks when |
|---|---|---|---|---|
| Sprint 1 | Capacity plan (lab 01) | 10 | Rate from done points and available hours; tax set and justified for weeks 1 to 7; both budgets fit; triggers cover the 80% band | Checker fails, or the rate counts unfinished stories |
| Sprint 1 | Cuts and ops-reducing work | 8 | Five largest cuts with the pillar each touches, signed by everyone; at least one ops-reducing story above the line and done | Cuts unsigned or unowned; the deploy script cut first |
| Sprint 1 | Measured tax and increment | 7 | Tags used on every ticket; week 1 `t` measured and entered; increment runs on the server | No tags, or the increment only runs on a laptop |
| Sprint 2 | Pipeline (lab 02) | 10 | Every stage has an owner, `h_s` and a measured `k_s`; the chosen fix raises throughput `X`; WIP limit keeps lead time at two weeks or less | The fix only raises a non-bottleneck stage |
| Sprint 2 | Scope decision | 7 | The gap to the content target is closed by a written decision that matches the updated content plan | Gap left as "we'll work harder" |
| Sprint 2 | Replanning and content item | 8 | Lab 01 rerun with measured tax, line moved if needed; one item through every stage and playable, with touch hours recorded | No rerun, or no item finished end to end |
| Sprint 3 | Alpha exit criteria | 10 | 10 to 20 lines a stranger could test, covering every kept feature, each marked pass or fail on the current build | "Parties work" style lines, or features missing from the list |
| Sprint 3 | Hosting budget (lab 03) | 8 | Every environment scheduled; real dated prices; checker `PASS` with a reserve; alerts set; teardown on the load-test checklist | Staging dropped to save money, or prices invented |
| Sprint 3 | Alpha build | 7 | Tagged on the last working day, deployed from the release pipeline, joinable from outside the team | Built by hand, or only reachable on the studio network |
| Sprint 4 | Plan and buffer (lab 07) | 10 | Completed points only; both capacities rounded down; buffer sized from a named tracker query; readiness items above the conservative line | Buffer missing, or planned points used as velocity |
| Sprint 4 | Burn-down and cuts | 8 | Daily rows with bug points separate; day-3 check run and recorded; any cut logged with day and reason | Cuts made on day 5, or no day-3 record |
| Sprint 4 | Content lock | 7 | Lock dated in the changelog; no new system or content item in the week 8 build; post-launch and cut lists with reasons | A new system appears in the open-beta build |
| **Total** | | **100** | | |

## Builds on

- [PR401 week 11, production plan](../../PR401-capstone-i-pre-production/lectures/w11-production-plan.md) and [PR401 weeks 12](../../PR401-capstone-i-pre-production/lectures/w12-vertical-slice-sprint-1.md) and [13](../../PR401-capstone-i-pre-production/lectures/w13-vertical-slice-sprint-2.md) (the plan and slice sprints the rate comes from); [PR401 week 9, content plan](../../PR401-capstone-i-pre-production/lectures/w09-content-plan.md).
- [PR101 week 4, scope and cut lists](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w04-scope-mvp-vertical-slice-cut-lists.md), [week 5, Scrum for games](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w05-agile-and-scrum-adapted-for-games.md), [week 6, estimation](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w06-estimation-and-why-it-fails.md), [week 7, task tracking and WIP](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w07-task-tracking-and-definitions-of-done.md), [week 13, builds and release checklists](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w13-builds-and-release-checklists.md).
- [MMO302 week 11, load testing with bots](../../MMO302-mmo-server-architecture/lectures/w11-load-testing-with-bots.md) and [week 13, cloud deployment and autoscaling](../../MMO302-mmo-server-architecture/lectures/w13-cloud-deployment-and-autoscaling.md) (the knee and headroom behind the budget).
- [MMO308 week 1, what live ops is](../../MMO308-live-operations-analytics-and-experimentation/lectures/w01-what-live-ops-is.md) (why the ops tax exists).
- [MMO407 week 2, capacity planning and login queues](../../MMO407-launch-scaling-and-post-mortems/lectures/w02-capacity-planning-and-login-queues.md) (the spike plan).
