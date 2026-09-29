# PR402 · Launched game brief 1: launch

**Weight:** 10% of the course grade, inside the launched game component (40%).
**Assigned:** week 8. **Due:** the go or no-go record and launch plan at the week 9 meeting, about 24 hours before the doors open; the as-run records and first numbers at the week 10 meeting, in `production/week09/`.
**Work mode:** team. One team mark, adjusted per person by the [peer assessment](peer-assessment-brief.md).
**Session guide:** [week 9, launch](../lectures/w09-launch.md). **Lab:** [09](../labs/lab09.md).

## What this milestone proves

That the team makes its launch decisions on paper before the doors open, and then runs the first 48 hours by those decisions. Launch in this course means the game becomes available to anyone, with no end date, on the platform your PR401 plan named, with player progress kept from then on ([week 9, section 1](../lectures/w09-launch.md)).

What is marked is the quality of the decisions and records, not the size of the crowd. A launch with 40 players, a queue plan that was never needed and a clean incident log can score full marks. So can a launch that went badly, if the team followed its triggers, told players the truth on time and wrote it all down.

## Gates

- **G1. Public and persistent.** The game is reachable by anyone from the store or site named in the plan, and character data survives a server restart. A launch that is not public by the end of week 9 scores 0 on rows 3 to 7 until it is, and the team meets the instructor to agree a date.
- **G2. Rollback drilled.** A rollback to the previous build with data intact was run on staging before launch, with its time recorded. Without it the go or no-go record cannot pass ([week 9, section 2](../lectures/w09-launch.md)).
- **G3. Status channel off the game's servers.** Player updates go out through a channel that stays up when the game is down.

## Deliverables

1. **Go or no-go record**: criteria, owners, evidence links, results, the decision and its time. The criteria and each "if fail, then" line are committed before the review starts.
2. **Launch capacity plan** (lab 09): forecast corrected by the open-beta error ratio, arrival phases, the shard plan with worst queue, wait at the back and day-7 peak per shard, the chosen plan, and a measurable merge trigger with a staging merge log if a temporary shard is used. `queue.py` and its output.
3. **Run sheet** from T−24 h to T+48 h with owners and checks, and the as-run version with actual times and deviations.
4. **Message templates** drafted before launch, and the **incident and message log** for the first 48 hours: every incident with severity and times, every player-facing message with its time and the promised next-update time.
5. **First numbers**: peak CCU, worst queue observed, crashes per 100 player-hours, and day-1 retention of the launch cohort with its `n`.

## Evidence required

| Evidence | Format | How the instructor checks it |
|---|---|---|
| Build | Release candidate tag, production deploy log | Confirms the launch build is the open-beta build plus fixes, with no new system |
| Load test | Report on the release candidate at forecast peak times 1.5 | Checks the cap per shard comes from this knee with stated headroom |
| Commit history | Go or no-go criteria, lab 09 section C | Checks thresholds and fallbacks were committed before the decision time |
| Queue model | `queue.py` and `queue-output.txt` | Runs the script; output must match the table |
| Incident log | Timestamped log, server logs | Matches one incident's start, mitigation and messages against server logs and the status channel |
| Player messages | Status channel history | Checks the first message after each incident went out within 15 minutes and every promised update time was kept or its miss explained |
| Telemetry | Queries for peak CCU, queue length, crash rate, launch cohort | Recomputes day-1 retention from the cohort query |
| Staging merge | Merge log with open-beta character data | Required only if a temporary shard was opened |

## How it is marked

The instructor observes the go or no-go review in the week 9 meeting and signs the record. The as-run material is marked at the week 10 meeting. The lab 09 rubric is the detailed scoring guide for rows 1 to 3.

## Rubric

| Criterion | Points | Full marks when | Low marks when |
|---|---|---|---|
| Go or no-go | 20 | At least seven criteria with evidence and owners; fallbacks decided in advance (lower cap, feature switched off, delay); decision follows the record | Criteria written during the review; "the team feels ready" |
| Demand forecast | 10 | Open-beta error ratio applied to every arrival phase; day-7 method stated | Forecast from the pitch deck |
| Shard plan and merge trigger | 15 | At least two plans computed; choice justified against wait limit and alive threshold; merge trigger measurable and tested on staging, or one shard with a cap and honest queue message | Temporary shard with no tested merge |
| Run sheet as run | 10 | Every step has an owner and check; deviations recorded with times | Run sheet written after launch |
| Incident handling | 15 | Each incident has severity, roles as in MMO308 week 13, mitigation first, times recorded; rollback used by its trigger if needed | Debugging on production with no commander; triggers ignored |
| Player communication | 15 | Templates ready before T; first message within 15 minutes; next-update times promised and kept; no fix times promised | Silence for hours; fix times promised and missed |
| Rota and sustainability | 5 | Roles covered in blocks for 72 hours; nobody on duty past their block | Whole team awake at T+20 hours |
| First numbers | 10 | Peak CCU, worst queue, crash rate and day-1 retention reported with `n` and compared with the forecast | Numbers missing or reported without `n` |
| **Total** | **100** | | |

## Builds on

- [PR401 week 11, production plan](../../PR401-capstone-i-pre-production/lectures/w11-production-plan.md) (launch platform and date) and the [PR401 week 10 social systems plan](../../PR401-capstone-i-pre-production/lectures/w10-social-systems-plan.md) (the alive threshold).
- [PR101 week 13, builds and release checklists](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w13-builds-and-release-checklists.md) and [week 12, crunch](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w12-crunch-causes-costs-alternatives.md).
- [MMO302 week 2, shards and layers](../../MMO302-mmo-server-architecture/lectures/w02-shards-realms-zones-instances-layers.md) and [week 9, login and gateway services](../../MMO302-mmo-server-architecture/lectures/w09-login-character-select-gateway-services.md).
- [MMO308 week 9, patch management and hotfixes](../../MMO308-live-operations-analytics-and-experimentation/lectures/w09-patch-management-and-hotfixes.md) (rollback triggers) and [week 13, incident response](../../MMO308-live-operations-analytics-and-experimentation/lectures/w13-incident-response.md).
- [MMO407 week 1, launch day anatomy](../../MMO407-launch-scaling-and-post-mortems/lectures/w01-launch-day-anatomy.md), [week 2, capacity planning and login queues](../../MMO407-launch-scaling-and-post-mortems/lectures/w02-capacity-planning-and-login-queues.md), [week 9, communication during crises](../../MMO407-launch-scaling-and-post-mortems/lectures/w09-communication-during-crises.md) and [week 13, launch plan workshop](../../MMO407-launch-scaling-and-post-mortems/lectures/w13-launch-plan-workshop.md).
