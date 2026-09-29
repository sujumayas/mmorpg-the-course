# PR401 · Milestone 12 brief: vertical slice

**Weight:** 10% of the course grade, inside the pre-production package component (50%).
**Assigned:** week 12. **Due:** in two parts. Sprint 1 plan, quality bar and tool decisions at the end of the week 12 meeting, in `preproduction/week12/`. Tagged review build, stability evidence and the updated time log at the start of the week 14 meeting, in `preproduction/week13/`. **Reviewed:** the panel plays the slice at the week 14 review.
**Work mode:** team. One team mark, adjusted per person by the [peer assessment](peer-assessment-brief.md).
**Session guides and labs:** [week 12, vertical slice sprint 1](../lectures/w12-vertical-slice-sprint-1.md) with [lab 12](../labs/lab12.md), and [week 13, vertical slice sprint 2](../lectures/w13-vertical-slice-sprint-2.md) with [lab 13](../labs/lab13.md).
**Builds on:** [PR101 week 4](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w04-scope-mvp-vertical-slice-cut-lists.md), section 4 (the vertical slice), [PR201 week 11](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w11-playtest-and-telemetry-review.md) (playtest evidence), [PR301 week 9, the first persistent weekend](../../PR301-mmo-studio-project-i-persistent-world-prototype/lectures/w09-alpha-first-persistent-weekend.md), [PR301 week 14, stabilization](../../PR301-mmo-studio-project-i-persistent-world-prototype/lectures/w14-stabilization.md), and [MMO406 week 1, setting as system](../../MMO406-worldbuilding-and-lore-for-persistent-worlds/lectures/w01-setting-as-system.md) (the slice town should explain its own rules).

## What this milestone proves

Two things. That a small piece of the game plays at the quality the team promised, including the persistent loop across a logout. And that the team measured what one unit of the game costs to make, with one-time work separated out. *Emberfall*'s artist logged 14 hours on the slice town, 4 of them one-time, so `u_1 = 10`. The week 11 plan had carried 6.5. Without the tagged log, week 14 could not have found that.

The slice is marked on meeting its own signed quality bar and on the evidence behind it, not on its size. A small slice that plays cleanly from the tag and has an honest stability statement beats a large one that crashes in the demo.

## Deliverables

Sprint 1, end of the week 12 meeting:

1. **Slice plan** (`slice-plan.md`): the sprint 1 goal as one testable sentence that includes the persistent loop, the per-discipline sprint plan, and the quality bar with one line per discipline, signed by every member.
2. **Tool decisions** (`tools.csv` and notes) in the lab 12 format, with `unit_cost.py` printing `PASS`: each candidate tool with `F`, `u_m`, `u_t`, `n`, break-even, the effect on discipline loads, and the decision.

Sprint 2, start of the week 14 meeting:

3. **Tagged review build**, with the tag, demo script and fallback plan in `review-build.md`. The tag is at least 48 hours old at the review; later commits are crash fixes with a second reviewer.
4. **Stability evidence** in the lab 13 format: `sessions.csv` covering every playtest and soak on the tagged build, and the `stability.py` report printing `PASS`, or `NOT READY` with the shortfall and a matching demo plan.
5. **Tagged time log** (`timelog.csv`, `units.csv`) with every slice unit and every tool-made unit, and the per-unit cost report.

The slice itself contains the five elements in week 12 section 1: one town at final quality, one quest chain (the tutorial quest chain from the week 9 plan, for *Emberfall*), one group encounter, the persistent loop on the real server, and one social system from week 10 working end to end.

## Evidence required

| Evidence | Format | How the instructor checks it |
|---|---|---|
| Quality bar | Signed `slice-plan.md` | The panel plays against it line by line |
| Daily build | Smoke-test results in the tracker | Main playable every day from day 2 of sprint 1 |
| Tagging | `timelog.csv` and `tag-rules.md` | Every hour has one of four tags; five or more edge-case rules; spot check of ten rows |
| Tool decisions | `unit_cost.py` output | Reruns it; every `build_now` tool has made at least one logged unit |
| Stability | `stability.py` output and `stability.md` | Reruns it; client and server exposure counted separately; upper bounds and the pessimistic clean-demo chance reported |
| Long soak | A row in `sessions.csv` | At least one soak on the tagged build longer than the longest expected PR402 session |
| Recovery | Rehearsal note | Database restore rehearsed; reconnect test logged if the plan relies on it |

## How it is marked

The panel plays the slice for 15 minutes at the week 14 review from the tag, following the demo script loosely. The instructor reruns both checkers and reads the time log. The panel's notes on the quality bar feed the first row.

## Rubric

| Criterion | Points | Full marks when | Low marks when |
|---|---|---|---|
| Slice meets its quality bar | 25 | Every line of the signed bar holds in play; all five slice elements present | Placeholder content in camera view, or an element missing |
| Persistent loop | 10 | Logout and login on the real server with progress, items and currency intact, including after a server restart | Local saves, or items lost on restart |
| Sprint plan and build health | 10 | One testable goal; per-discipline plan at or below 1.0; main playable daily with smoke tests logged | Integration left to the last day |
| Tagged time log | 15 | Every hour tagged; rules written; one-time and per-unit split plausible on spot check | Tags added after the fact, or hours missing |
| Tool decisions | 10 | `PASS` on rerun; break-even at the plan ratio; load effect per discipline; decision followed | Tools built with no break-even, or not used |
| Stability evidence | 20 | `PASS`, or an honest `NOT READY` with a matching demo plan; exposures separate; upper bounds and clean-demo chance reported; long soak done | Stability claimed from "it hasn't crashed" |
| Review build discipline | 10 | Tag 48 hours old; demo script and fallback exist; restore rehearsed | Built the night before, or no fallback |
| **Total** | **100** | | |

## Late and missing work

Sprint 1 files more than 48 hours late are capped at 70 for their rows. The review build cannot be late: the panel plays whatever is tagged at the start of the week 14 meeting.
