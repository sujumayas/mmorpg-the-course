# PR402 · Launched game brief 2: live-ops operation

**Weight:** 10% of the course grade, inside the launched game component (40%).
**Assigned:** week 9. **Due:** week 10 records before the week 11 meeting, in `production/week10/`; week 11 records before the week 12 meeting, in `production/week11/`. Marked once, at the week 12 meeting.
**Work mode:** team. One team mark, adjusted per person by the [peer assessment](peer-assessment-brief.md).
**Session guides:** [week 10, live-ops week 1](../lectures/w10-live-ops-week-1.md) and [week 11, operating rhythm](../lectures/w11-live-ops-week-2-operating-rhythm.md). **Labs:** [10](../labs/lab10.md), [11](../labs/lab11.md).

## What this milestone proves

That the team runs a live game by written rules it can sustain, and moves from launch mode to operating mode on evidence. Two weeks are marked together because they are one arc. Week 10 sets the routine: a daily review, triage in player-hours, a hotfix decision you can defend and an on-call load within limits. Week 11 measures what that routine cost, buys some of the cost back, and fixes the rhythm the team keeps until the showcase.

The instructor is not marking how many incidents you had. A team with five incidents, all mitigated first by a switch or a revert, each announced within 15 minutes and followed by a postmortem, can score full marks.

## Deliverables

**Week 10** ([lab 10](../labs/lab10.md)):

1. **Daily review log**: one entry per day, with dashboard values (health, first cohort, new players, bug queue, economy, incidents) and decisions. Each review 30 minutes or less.
2. **Triage sheet** (`triage.csv`) and **`capacity.md`**: break-even harm, fix capacity net of incident follow-up, every issue with severity, `h` and its basis, rank and decision.
3. **Hotfix and patch records**: build number, issues closed, restart time, regressions.
4. **Rota and capacity** for weeks 10 and 11 with on-call hours per person.
5. **Player-facing posts**: known-issues post history and patch notes.
6. **Retention report**: launch cohort day-1, day-3 and day-7 with `n` and Wilson intervals.
7. **Incident postmortems**: one per SEV1 or SEV2 incident, in the MMO308 week 13 format.

**Week 11** ([lab 11](../labs/lab11.md)):

8. **Lab 11 worksheet**, parts A to D: interrupt budget `C`, `I`, `i`, `P`; support queue `L`, `λ`, `W`, `L_target` and ticket causes; buy-back plan with costs, hours removed and payback; operating rhythm.
9. **Buy-back tickets** in the tracker with owners.
10. **Rhythm sheet**: on-call rota to the end of week 14, triage slot, weekly live review agenda, the interrupt line set before the log was analysed.
11. **Cohort table** for every install day since launch, with incident dates marked.

## Evidence required

| Evidence | Format | How the instructor checks it |
|---|---|---|
| Dashboard | Live dashboard and its history | Compares one day's review log entry with the dashboard for that day |
| Incident logs | Log, postmortems, server logs, status channel | Picks one incident and checks mitigation came before the fix, with times |
| Builds | Hotfix tags and deploy logs | Checks every `hotfix` row in `triage.csv` shipped in one bundled build |
| Telemetry | Queries behind `h` estimates and the cohort table | Recomputes break-even, one rank and one Wilson interval |
| Time log | Week 10 entries tagged planned or one of five interrupt categories | Recomputes `i` and `P`; checks category totals add up to `I` |
| Ticket system | Open-ticket counts at a fixed time each day, ticket log | Recomputes `W = L / λ` and checks cause counts sum to arrivals |
| Rota | Calendar or rota file | Asks a random team member who is on call today |

## How it is marked

The instructor observes one timed daily review during the week 10 meeting, checks the week 10 folder at the week 11 meeting, and marks both weeks together at the week 12 meeting. The lab 10 and lab 11 rubrics are the detailed scoring guides for rows 2 and 5.

## Rubric

| Criterion | Points | Full marks when | Low marks when |
|---|---|---|---|
| Daily review | 10 | Ran every day in 30 minutes or less from a one-screen dashboard; decisions logged | Reviews skipped, or an hour of scrolling with no decisions |
| Triage and hotfix decisions (lab 10) | 20 | SEV1 mitigated first; `h` with a basis on every row; break-even and capacity applied; fixes bundled; three rows recompute | Fixes in arrival order; one restart per fix |
| Incident response | 15 | Roles, severity and times recorded; mitigation first; player message within 15 minutes; a blameless postmortem per SEV1 or SEV2 | No postmortems, or postmortems that name a culprit |
| Sustainable load | 10 | Fix capacity from the rota net of six hours follow-up per incident; nobody above the agreed on-call limit | Two people on call every night |
| Interrupt budget and queue (lab 11) | 20 | `i`, `P` and `W` from honest logs; interrupt line set in advance; top ticket cause named with its share | Interrupts logged as planned work; tickets timed by hand and abandoned |
| Buy-back plan | 10 | At least three one-off fixes tied to Part A rows, with cost, hours removed, payback and owners; the top cause addressed in the patch or deferred with a reason | Queue cleared without fixing its source |
| Retention and cohorts | 10 | Day-1, day-3 and day-7 reported with `n` and intervals; low cohorts checked against incident dates; no trend claimed that the intervals cannot carry | "Retention dropped 4 points" from one small cohort |
| Player communication | 5 | Known-issues post updated after each review; fixed reports closed where they were reported | Stale post; reporters never told |
| **Total** | **100** | | |

## Builds on

- [PR401 week 11, production plan](../../PR401-capstone-i-pre-production/lectures/w11-production-plan.md) (the capacity model the interrupt budget refines).
- [PR101 week 10, bug tracking](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w10-bug-tracking-and-qa-basics.md), [week 7, WIP and Little's law](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w07-task-tracking-and-definitions-of-done.md) and [week 12, crunch](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w12-crunch-causes-costs-alternatives.md).
- [MMO302 week 9, login and gateway services](../../MMO302-mmo-server-architecture/lectures/w09-login-character-select-gateway-services.md) and [week 14, observability](../../MMO302-mmo-server-architecture/lectures/w14-observability-logs-metrics-traces.md).
- [MMO308 week 1](../../MMO308-live-operations-analytics-and-experimentation/lectures/w01-what-live-ops-is.md), [week 3, cohorts and retention](../../MMO308-live-operations-analytics-and-experimentation/lectures/w03-cohorts-and-retention-curves.md), [week 9, hotfixes](../../MMO308-live-operations-analytics-and-experimentation/lectures/w09-patch-management-and-hotfixes.md), [week 10, feedback loops](../../MMO308-live-operations-analytics-and-experimentation/lectures/w10-player-feedback-loops-forums-surveys-polls.md), [week 12, economy monitoring](../../MMO308-live-operations-analytics-and-experimentation/lectures/w12-economy-monitoring.md) and [week 13, incident response](../../MMO308-live-operations-analytics-and-experimentation/lectures/w13-incident-response.md).
- [MMO407 week 9, communication during crises](../../MMO407-launch-scaling-and-post-mortems/lectures/w09-communication-during-crises.md) and [week 10, recovery strategies](../../MMO407-launch-scaling-and-post-mortems/lectures/w10-recovery-strategies.md).
