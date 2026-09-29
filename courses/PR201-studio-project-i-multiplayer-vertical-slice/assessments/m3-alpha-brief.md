# PR201 · Milestone 3 brief: alpha

**Weight:** 14% of the course grade, inside the milestones component (50%).
**Assigned:** week 4. **Due:** the week 10 alpha review. The alpha playtest runs between the review and week 11, and its evidence is marked at beta.
**Work mode:** team. One team mark, adjusted per person by the [peer assessment](peer-assessment-brief.md).
**Session guides:** [week 4](../lectures/w04-sprint-1-networking-skeleton.md), [week 5](../lectures/w05-sprint-1-review.md), [week 6](../lectures/w06-sprint-2-core-combat.md), [week 7](../lectures/w07-sprint-2-review-and-playtest.md), [week 8](../lectures/w08-sprint-3-content-and-progression.md), [week 9](../lectures/w09-sprint-3-review.md) and [week 10, alpha milestone](../lectures/w10-alpha-milestone.md). **Labs:** [04](../labs/lab04.md) to [10](../labs/lab10.md).

## What this milestone proves

That the whole slice exists and runs over a network, and that the team can run its own process. Alpha in this course is defined by the seven criteria A1 to A7 in [week 10, section 1](../lectures/w10-alpha-milestone.md). In short, everything that will ship exists and works: feature complete, playable end to end on three machines with progress kept across logout, built by script from a tag, zero open P1 and P2 bugs, the network matrix passing, telemetry landing, and placeholders listed. Art and audio may still be rough.

The pass or fail decision on the day follows the week 10 rule. A conditional pass lists the failed criteria and a date within one week to meet them. Two failed criteria, or any failed A2 or A3, is a fail. This brief turns that decision and the three sprints before it into a mark.

## Deliverables

Due at the start of the week 10 review, in the team repository.

1. **Alpha criteria sheet** (lab 10 format), A1 to A7, each with owner, evidence and pass or fail.
2. **Bug tracker export and alpha forecast**, checked with `check_alpha.py`.
3. **Alpha candidate build**, tagged, made by the build script, with the build log.
4. **Network matrix report** from the overnight run, in [CS202 week 14](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w14-testing-under-bad-networks-netem-clumsy.md) format.
5. **Placeholder list** for the playtest.
6. **Alpha playtest plan**: questions, unit of analysis, tracked event and threshold for each, dated before any session runs. Method from [week 7](../lectures/w07-sprint-2-review-and-playtest.md) and [UX201 week 8](../../UX201-game-ux-and-player-psychology/lectures/w08-usability-testing-methods.md).
7. **Sprint records for sprints 1 to 3**: labs 04 to 09 with their checker outputs, and for each sprint the forecast, estimated hours committed, estimated hours done, goal met yes or no, and the retrospective change with its owner. Method from [PR101 week 5](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w05-agile-and-scrum-adapted-for-games.md) and [week 7](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w07-task-tracking-and-definitions-of-done.md).
8. **Updated TDD**: the week 6 feedback table, the week 8 progression acceptance criteria, and version 2 of sections 11 and 12. Section 11 v2 replaces the week 3 file save with the database design: the schema for characters, inventory and progression ([DB201 week 2](../../DB201-data-persistence-and-telemetry/lectures/w02-relational-modeling-characters-inventories-items.md)), level-up and loot grant as single transactions ([week 5](../../DB201-data-persistence-and-telemetry/lectures/w05-transactions-and-acid.md)) and unique grant ids against duplicates ([week 6](../../DB201-data-persistence-and-telemetry/lectures/w06-race-conditions-and-the-duplication-bug.md)). Section 12 v2 gives every tracked event its properties and where it is stored ([week 10](../../DB201-data-persistence-and-telemetry/lectures/w10-telemetry-design-events-and-properties.md)).

## Evidence required

| Evidence | Format | How the instructor checks it |
|---|---|---|
| Build | Tag, build script and log | A3 is run live: the build is made from the tag on a non-developer machine during the review |
| End to end | Three fresh accounts, three lab machines | A2 is run live: entrance to boss kill, logout, login, level and XP intact |
| Persistence integrity | Level-up and loot grants as single transactions with grant ids ([DB201 week 5](../../DB201-data-persistence-and-telemetry/lectures/w05-transactions-and-acid.md), [week 6](../../DB201-data-persistence-and-telemetry/lectures/w06-race-conditions-and-the-duplication-bug.md)) | Reviewer reads the code path and kills the server during a level-up |
| Bugs | Tracker export and `check_alpha.py` output | Reruns the checker; compares priorities with the [PR101 week 10](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w10-bug-tracking-and-qa-basics.md) matrix |
| Network matrix | Report with four profiles, five seeds each | Reads the report and reruns one cell |
| Telemetry | Query output from the A2 run | Reruns the query ([DB201 week 11](../../DB201-data-persistence-and-telemetry/lectures/w11-pipelines-collect-store-query.md)) |
| Sprint records | Board exports and lab checker outputs | Recomputes velocity for one sprint from the export |
| Playtest plan | Committed file | Checks the commit date is before the first session |

## How it is marked

The review lasts 20 minutes per team and follows the week 10 session plan. The team does not demo from the editor. The instructor and a second reviewer score alone and agree a mark.

Each criterion row below is scored on the review day. A criterion met within the conditional week earns at most half its points. A criterion still failing after the conditional week scores 0, and the team keeps working toward beta.

## Rubric

| Criterion | Points | Full marks when | Low marks when |
|---|---|---|---|
| A1 Feature complete | 12 | Every story above the week 9 line meets the definition of done; cuts marked with reasons | Features missing and not recorded as cut |
| A2 End to end | 15 | Three fresh accounts reach the boss kill on three machines and keep level and XP across logout | Needs a developer's machine, or progress is lost |
| A3 Reproducible build | 10 | Made from the tag by script on a non-developer machine during the review | Only the build owner can build, or it needs the editor |
| A4 No gate bugs and forecast | 10 | Zero open P1 and P2; priorities match the matrix; forecast made Monday and tracked daily | Gate bugs open, or priorities lowered to pass |
| A5 Network matrix | 12 | Four profiles with five seeds each; LAN, Good broadband and Evening Wi-Fi pass; Mobile recorded | Profiles missing, or failures not filed |
| A6 Telemetry | 8 | TDD section 12 v2 lists each event's properties; every tracked event fires in the A2 run and is queryable | Events missing, client-only or not queryable |
| A7 Content marked | 3 | Placeholder list complete | Placeholders unlisted |
| Server authority and persistence integrity | 10 | Damage, loot and XP decided on the server; TDD section 11 v2 gives a normalised schema and names the transactions; grants atomic and idempotent; survives a server kill mid level-up | Client-decided results, no schema or transactions, or duplicates possible |
| Sprint process | 12 | Forecasts from measured velocity; only done stories counted; goals answered; retrospective changes owned and checked | Velocity counts unfinished work; no retrospectives |
| Alpha playtest plan | 8 | Every question has a unit, an event and a threshold, dated before the first session | Thresholds missing or written after |
| **Total** | **100** | | |

## Late and missing work

The review happens in the session and cannot be moved without an agreed extension. Documents handed in up to 48 hours late are capped at 70 for their rows.
