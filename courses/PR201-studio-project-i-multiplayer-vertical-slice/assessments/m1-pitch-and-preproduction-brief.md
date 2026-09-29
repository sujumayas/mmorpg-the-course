# PR201 · Milestone 1 brief: pitch and pre-production

**Weight:** 8% of the course grade, inside the milestones component (50%).
**Assigned:** week 1. **Due:** end of week 2, before the week 3 studio session. **Reviewed:** at the start of week 3.
**Work mode:** team of five to seven. One team mark, adjusted per person by the [peer assessment](peer-assessment-brief.md).
**Session guides and labs:** [week 1, pitch and team formation](../lectures/w01-pitch-and-team-formation.md) with [lab 01](../labs/lab01.md), and [week 2, pillars and scope](../lectures/w02-pre-production-pillars-and-scope.md) with [lab 02](../labs/lab02.md).
**Builds on:** [PR101 week 1, roles on a game team](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w01-roles-on-a-game-team.md), [PR101 week 4, scope, MVP and cut lists](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w04-scope-mvp-vertical-slice-cut-lists.md), [PR101 week 6, estimation](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w06-estimation-and-why-it-fails.md) and [CS202 week 3, topologies](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w03-topologies-peer-to-peer-client-server-relay.md).

## What this milestone proves

That your team picked a game it can build. Most PR201 teams that miss the final milestone chose a pitch that needed more of one discipline than the team had. This milestone asks you to show the numbers that rule that out, and to write the design limits that follow from them before anyone opens the engine.

It does not mark how exciting the idea is. A modest pitch whose worst discipline load is 0.8 scores higher than a bold one at 1.3.

## Deliverables

Everything goes in `docs/` in the team repository. The lab 01 and lab 02 rubrics are used as feedback in the studio. This brief gives the milestone mark.

1. **Team charter**, one page. RACI for the pre-production milestones, the build owner, the product owner, meeting times, a lateness rule and how disagreements are settled. Use the charter from [PR101 week 1, section 5](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w01-roles-on-a-game-team.md).
2. **Skill matrix** (`team.csv`, lab 01 format). Every discipline has a primary and a different backup. Each member's weekly hours `H_i` are stated.
3. **Pitch one-pager** with the moment, the "why together" paragraph, one minute of play, the biggest unknown and a "full game" section you will not build.
4. **Fit sheet** (`pitch_demand.csv`) and the saved output of `check_fit.py` printing `PASS`. Every change made to reach `PASS` is written as a decision.
5. **Pillars** (`pillars.md`), each with the playtest question that tests it and one thing it rules out. One pillar is about players together.
6. **Scope sheet** (`features.csv`, lab 02 format) with the output of `check_scope.py` printing `PASS`, and `scope.md` with the must tier as player steps, overrides, dependencies, cut triggers and the player timeline of the slice.

## Evidence required

| Evidence | Format | How the instructor checks it |
|---|---|---|
| Fit check | `check_fit.py` output file | Reruns the checker on your CSV files and compares output |
| Scope check | `check_scope.py` output in `scope.md` | Reruns it and reads the cut line against the loads |
| Decisions | Numbered list in the one-pager | Picks two and finds each one in `features.csv` as a limit |
| Estimates | Every discipline's column filled in `features.csv` by that discipline's primary | Asks the primary to explain one estimate |
| Charter sign-off | Every member's name and date in the charter | Counts names against the team list |

No build is required at this milestone.

## How it is marked

The instructor runs both checkers, reads the documents and meets the team for 10 minutes at the start of week 3. In the meeting any member may be asked to explain a load, a cut trigger or a pillar. If only one person can answer, the "team ownership" row loses marks.

## Rubric

| Criterion | Points | Full marks when | Low marks when |
|---|---|---|---|
| Fit to team | 20 | `PASS` on rerun; largest load at or below 1 with stated `H`, `c`, `W`, `b`; every discipline has supply | Checker fails, or a discipline has zero supply and no plan |
| Decisions from the fit test | 10 | Each change to reach `PASS` appears as a limit in the one-pager and the feature list | Loads were fixed by editing numbers with no design change |
| "Why together" | 15 | A concrete moment where one player needs another, which a single player cannot reproduce | "You can play with friends" |
| Slice size and timeline | 10 | One zone, one encounter, one progression step; the timeline reaches every kept feature; "full game" parked separately | Several zones, classes or systems in the slice |
| Pillars | 10 | Each pillar has a playtest question and rules something out | Pillars as adjectives or genre labels |
| Scope sheet and cut line | 15 | `check_scope.py` passes; no kept feature depends on a cut one; overrides explained | Checker fails, or dependencies cross the cut line |
| Cut triggers | 10 | At least three, each with a date, a measurable condition and the cut it fires | Triggers without dates or conditions |
| Charter and roles | 5 | Build owner, product owner, backups and lateness rule named; all members signed | Missing roles or signatures |
| Team ownership | 5 | Any member explains any number in the meeting | One member answers everything |
| **Total** | **100** | | |

## Late and missing work

A milestone handed in up to 48 hours late is capped at 70. After that it scores 0 but must still be handed in, because the TDD depends on it. Extensions follow the university's mitigating circumstances process.
