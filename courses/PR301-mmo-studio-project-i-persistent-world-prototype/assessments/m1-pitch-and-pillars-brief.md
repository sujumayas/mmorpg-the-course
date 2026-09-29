# PR301 · Milestone 1 brief: pitch and world pillars

**Weight:** 4% of the course grade, inside the milestones component (50%).
**Assigned:** week 1. **Due:** before the week 2 studio session, in `docs/pitch/` in the team repository.
**Work mode:** team. One team mark, adjusted per person by the [peer assessment](peer-assessment-brief.md).
**Session guide:** [week 1, pitch and world pillars](../lectures/w01-pitch-and-world-pillars.md). **Lab:** [lab 01](../labs/lab01.md).
**Builds on:** [PR201 week 1](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w01-pitch-and-team-formation.md) (supply, load and the skill matrix), [PR201 week 2](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w02-pre-production-pillars-and-scope.md) (pillars that decide things), [MMO304 week 3](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w03-faucets-sinks-and-transformations.md) (faucets and sinks), [MMO302 week 1](../../MMO302-mmo-server-architecture/lectures/w01-scale-targets-ccu-messages-and-n-squared.md) (what 50 concurrent players cost) and [MMO302 week 7](../../MMO302-mmo-server-architecture/lectures/w07-persistence-strategies-write-through-periodic-event-sourcing.md) (what each loss window costs to build).

## How the course is assessed

The course's assessment line is "Milestones (50%), final world (30%), post-mortem and peer review (20%)". The briefs in this folder split it like this.

| Component | Brief | Due | Course weight |
|---|---|---|---|
| M1 Pitch and pillars | this brief | before week 2 | 4% |
| M2 Architecture review | [m2](m2-architecture-review-brief.md) | before week 3 | 6% |
| M3 Sprint reviews 1 to 5 | [m3](m3-sprint-reviews-brief.md) | starts of weeks 5, 7, 9, 12, 13 | 14% |
| M4 Alpha persistent weekend | [m4](m4-alpha-persistent-weekend-brief.md) | week 9 freeze and the Monday after | 10% |
| M5 Telemetry review | [m5](m5-telemetry-review-brief.md) | 48 hours after week 10 | 7% |
| M6 Beta open class playtest | [m6](m6-beta-open-class-playtest-brief.md) | start of week 14 | 9% |
| **Milestones** | | | **50%** |
| Final world (stabilization and showcase) | [final](final-world-brief.md) | week 15 | 30% |
| Post-mortem and viva | [post-mortem](post-mortem-brief.md) | week 15 | 10% |
| Peer review | [peer assessment](peer-assessment-brief.md) | weeks 10 and 15 | 10% |
| **Total** | | | **100%** |

Labs are marked on their own 20-point rubrics as feedback, and they carry no separate weight. Their checker outputs are evidence for the milestone that uses them. The [exam bank](exam-bank.md) supplies the viva questions for the post-mortem.

## What this milestone proves

That the team has picked a world it can afford, and has written down the promises the architecture review will test. PR201 asked for fifteen minutes of game played once. PR301 asks for a world 50 people live in for a weekend. A pitch passes when its load against team supply is at or below 0.9, every change made to get there is a written design constraint, and the world names what it keeps, where its money goes and why players stand near each other.

## Deliverables

1. **World one-pager.** The pitch, the loop in one sentence, and the "why come back tomorrow" paragraph.
2. **Three pillars.** Each with its statement, what it rules in and at least one named feature it rules out.
3. **Budget sheet.** `pitches.csv` and the saved `check_budget.py` output showing `PASS`, with the team parameters at the top of `budget-notes.md`.
4. **Constraints list.** Every change made to reach `PASS`, written so a designer could apply it.
5. **Persistence promise.** The week 1 section 4 table covering character level, items, currency, position, market state and anything else the world saves, with the acceptable loss in a crash for each.
6. **Updated `team.csv`.** A primary and a different backup for every discipline.
7. **Economy and grouping lines.** At least one named faucet, one named sink and one reason for players to group.

## Evidence required

| Evidence | Format | How the instructor checks it |
|---|---|---|
| Budget | `pitches.csv`, `budget-output.txt`, `budget-notes.md` | Reruns `check_budget.py` with the stated parameters; it must print `PASS` and exit 0 |
| Measured `k` | Calculation from PR201 sprint records | Traces the hours and minutes of play to the PR201 repository, or accepts the stated default of 45 |
| Replay factor | Loop sentence for any `r` above 3 | Checks that the loop connects at least two systems |
| Persistence promise | Table in `docs/pitch/` | Checks that every "None" row names something a player would complain about losing |
| Pillar test | Neighbour team's ruling on two backlog features | Reads the ruling sheet from the week 1 session |
| Skill cover | `team.csv` and the PR201 discipline check | Reruns the PR201 lab 01 checker for the largest discipline load |

No server logs, telemetry or soak data exist yet. The evidence for this milestone is the arithmetic and the session records.

## How it is marked

The instructor reads the pack before the week 2 session and gives written feedback at its start, so the architecture review uses a signed-off promise. The sample team *Saltmarsh* from the week 1 guide would score well on the budget rows. Its first sheet loaded at 0.99, it cut crafting to two tiers, reached 0.88, and wrote the cut into the one-pager as a constraint.

## Rubric

| Criterion | Points | Full marks when | Low marks when |
|---|---|---|---|
| Budget passes | 15 | `PASS` on rerun at load 0.9 or less; output file matches | Fails on rerun, or parameters changed without a written reason |
| Honest estimates | 15 | `P` includes login, persistence, grouping and the encounter; `F` estimated by each discipline's primary; `k` measured or honestly defaulted | Platform at zero, or estimates made by one person |
| Replay and sensitivity | 10 | Every `r` above 3 has a loop sentence; load at `r − 1` reported with the cut that would follow | `r` asserted; no sensitivity check |
| Constraints | 10 | Each change to pass is a rule a designer can apply ("crafting has two tiers") | Changes left as numbers in a spreadsheet |
| Pillars | 15 | Three pillars, each ruling out a named feature; the neighbour team ruled as the team would | Pillars that rule out nothing |
| Persistence promise | 15 | Covers characters, items, currency, position and market; "None" kept for what players would miss | Missing rows, or "None" for everything including mob health |
| Economy and grouping | 10 | One faucet, one sink and one grouping reason named and tied to a pillar | Any of the three missing |
| Team cover | 10 | Primary and different backup for every discipline; largest discipline load at or below 1 | One person covering two disciplines alone |
| **Total** | **100** | | |

## Late and missing work

The pack is due before week 2 because the review depends on it. A pack up to 48 hours late is capped at 70. A team that arrives at week 2 without a persistence promise takes part in the review with a draft, and the missing rows score 0.
