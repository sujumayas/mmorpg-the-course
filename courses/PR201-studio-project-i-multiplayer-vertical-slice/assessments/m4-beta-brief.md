# PR201 · Milestone 4 brief: beta

**Weight:** 12% of the course grade, inside the milestones component (50%).
**Assigned:** week 10. **Due:** the beta build and exit criteria sheet at the week 13 review. The soak plan and log, and the known issues list, at the start of the week 14 meeting.
**Work mode:** team. One team mark, adjusted per person by the [peer assessment](peer-assessment-brief.md).
**Session guides and labs:** [week 11, playtest and telemetry review](../lectures/w11-playtest-and-telemetry-review.md) with [lab 11](../labs/lab11.md), [week 12, sprint 4 polish](../lectures/w12-sprint-4-polish.md) with [lab 12](../labs/lab12.md), and [week 13, beta milestone](../lectures/w13-beta-milestone.md) with [lab 13](../labs/lab13.md).

## What this milestone proves

That the slice is complete, has been changed by evidence, and is stable enough to survive the showcase. Beta in this course is defined in [week 13, section 1](../lectures/w13-beta-milestone.md): feature and content complete, no open P1 bugs with every open P2 owned and planned, and a stability target met by a soak test. After beta every change is a fix or a removal.

This milestone also marks the work between alpha and beta: the week 11 evidence review, and whether sprint 4 spent its hours on what the evidence said.

## Deliverables

Due at the week 13 review:

1. **Beta build**, tagged `v0.9.0-beta` or the team's equivalent, built from a clean checkout, uploaded before the meeting, with a README a stranger can follow.
2. **Exit criteria sheet** (lab 13, part A). The course's minimum rows from week 13 section 2, plus the team's own, each with evidence from the beta build.
3. **Alpha evidence pack** from week 11 in `production/week11/`: `evidence.csv` and `counts.csv` passing `check_evidence.py`, and the ranked `input-list.md`.
4. **Sprint 4 record** (lab 12 format), with a before-and-after capture for every completed polish item and a line tracing each item to the input list or labelling it a judgment call.
5. **UX pass.** A heuristic evaluation of the HUD and onboarding by two team members, following [UX201 week 9](../../UX201-game-ux-and-player-psychology/lectures/w09-heuristic-evaluation-for-games.md) and [week 10](../../UX201-game-ux-and-player-psychology/lectures/w10-hud-and-information-design.md), and an accessibility checklist per [UX201 week 11](../../UX201-game-ux-and-player-psychology/lectures/w11-accessibility-guidelines.md) with each item done, planned or not applicable with a reason.

Due at the start of the week 14 meeting, in `production/week13/`:

6. **Soak plan and log** (lab 13 format). `soak_target.py` prints `PASS` or `ON TRACK`, with the reliability target `R` recorded before the first soak.
7. **Known issues list** with every open P2, P3 and P4 bug and its planned outcome.

## Evidence required

| Evidence | Format | How the instructor checks it |
|---|---|---|
| Build | Tag, script log, README | Starts it from a clean download on a lab machine using only the README |
| Content route | Route checklist signed by a tester who did not build it | A full party, including a player from another team, plays the showcase route under the campus Wi-Fi profile |
| Performance | Profiler capture: server tick time and client frame time against budget ([CS202 week 13](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w13-tick-rate-and-bandwidth-budgets.md)) | Reads one line per measure; checks it came from the beta build |
| Telemetry | The week 11 count checks rerun on the beta build | Recomputes one count from the raw export ([DB201 week 12](../../DB201-data-persistence-and-telemetry/lectures/w12-dashboards-and-kpis.md)) |
| Evidence trace | Sprint 4 items with evidence IDs | Picks three and traces each to `evidence.csv` or the observation notes |
| Soak | Soak log and checker output | Reruns `soak_target.py` |
| Bugs | Dated tracker export | Checks zero open P1 and an owner and target build on every P2 |

## How it is marked

At the week 13 review two markers score alone and agree a mark. If they differ by more than 10 points, a third marker reviews the evidence and the median counts. Evidence from an earlier build than the beta tag does not count.

## Rubric

| Criterion | Points | Full marks when | Low marks when |
|---|---|---|---|
| Content complete | 15 | Every showcase area, enemy and quest step reachable in a normal playthrough; route signed by a non-builder | Content behind a debug key, or missing |
| Bugs | 10 | Zero open P1; every P2 owned with a target build; bug bash findings filed | Open P1, or P2s without owners |
| Build | 8 | Starts from a clean download with only the README | Needs team help to start |
| Network | 12 | Full party including an outside player finishes the route under campus Wi-Fi conditions | Party cannot finish, or results differ between clients |
| Performance | 8 | Server tick and client frame time under budget, measured on the beta build | No measurements, or old build |
| Telemetry | 7 | Count checks balance on the beta build | Checks not rerun, or imbalances unexplained |
| Stability | 12 | `R` set before the first soak; checker prints `PASS` or `ON TRACK`; the bot route covers every showcase system or gaps have human tests | No soak, or target set after the data |
| Evidence-driven changes | 15 | Lab 11 passes; sprint 4 spent on the ranked list; judgment calls labelled; top alpha findings addressed or explained | Changes cannot be traced, or top findings ignored |
| UX and accessibility | 8 | Heuristic findings acted on or scheduled; accessibility items decided with reasons | No evaluation; checklist copied without decisions |
| Sprint 4 process | 5 | Polish budget and cut line from lab 12 held, or changes recorded | Scope added after the cut line |
| **Total** | **100** | | |

## Late and missing work

As for alpha. A team that misses beta still enters the fix-or-remove rule on the date. Features added after week 13 are removed from the release candidate by the build owner.
