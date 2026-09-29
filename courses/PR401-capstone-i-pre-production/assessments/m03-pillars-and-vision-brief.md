# PR401 · Milestone 3 brief: pillars and vision

**Weight:** 4% of the course grade, inside the pitch component (20%).
**Assigned:** week 3. **Due:** before the week 4 studio session, in `preproduction/week03/`, with the vision and art direction pages in `docs/`. The pillar thresholds must be committed before the week 4 session starts. **Reviewed:** at the start of week 4.
**Work mode:** team. One team mark, adjusted per person by the [peer assessment](peer-assessment-brief.md).
**Session guide and lab:** [week 3, pillars and vision](../lectures/w03-pillars-and-vision.md) with [lab 03](../labs/lab03.md).
**Builds on:** [PR201 week 2, pillars and scope](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w02-pre-production-pillars-and-scope.md), section 3, [PR301 week 1, pillars for a world](../../PR301-mmo-studio-project-i-persistent-world-prototype/lectures/w01-pitch-and-world-pillars.md), section 3, and [MMO406 week 1, setting as system](../../MMO406-worldbuilding-and-lore-for-persistent-worlds/lectures/w01-setting-as-system.md), sections 1 and 3.

## What this milestone proves

That your pillars decide where the hours go. The week 3 guide measured *Emberfall*'s first feature list and found P3 at 13% of feature hours and a quarter of the hours serving no pillar. A pillar you cannot see in the hours is a slogan. This milestone marks the audit and the revision more than the wording.

## Deliverables

In `preproduction/week03/` in the team repository, except the two pages in item 1, which go in `docs/vision.md` and `docs/art-direction.md`.

1. **Vision and pillars page**, one page: a one-sentence vision drawn from the week 2 positioning, two to four pillars, at least two anti-pillars, and one setting line per pillar. Beside it, the **art direction page** (one page, the start of the art bible): palette, shape language, scale reference, reference images the team may use and a readability rule, each tied to a pillar or setting line.
2. **Pillar sheet** (`pillars.csv`) with a question, an observable and a threshold for each pillar.
3. **Feature sheet** (`features.csv`) with hours and pillar weights, the foundation list kept separate, and the checker output before (`audit-before.txt`) and after (`audit-after.txt`) revision.
4. **Change log** (`changes.md`) listing each cut or addition, the hours moved, and where the freed hours went.
5. **Claims sheet update**: each pillar's test question appears as a claim.

## Evidence required

| Evidence | Format | How the instructor checks it |
|---|---|---|
| Hour audit | `audit-before.txt`, `audit-after.txt` | Reruns `check_pillars.py` with the `s_min` and `o_max` in `changes.md` |
| Thresholds in advance | Commit date of `pillars.csv` | Dated before the week 4 session |
| Revision | `changes.md` | Traces two cuts into `features.csv` |
| Setting ties | Setting lines on the vision page | Each pillar has one; no orphan lore |
| Art direction | `docs/art-direction.md` | Each choice names a pillar or setting line; a readability rule is stated |
| Capacity check | One paragraph | Revised total compared with week 1 capacity |

## How it is marked

The instructor reruns the checker, reads the vision page and asks one member to argue for the weight on the largest feature.

## Rubric

| Criterion | Points | Full marks when | Low marks when |
|---|---|---|---|
| Checker passes | 10 | `PASS` on rerun with the stated thresholds | Fails, or the thresholds were loosened with no reason |
| Vision | 10 | One sentence that follows from the week 2 positioning | A paragraph, or a genre label |
| Pillars | 20 | Two to four; each rules something out; one about players together; one that depends on persistence | Adjectives ("immersive"), or more than four |
| Anti-pillars | 10 | At least two, each ruling out something a comparable does | Anti-pillars nobody would want anyway |
| Test lines | 20 | Every pillar has a question, an observable a prototype can produce, and a threshold committed before week 4 | Thresholds added after prototype 1 |
| Revision and change log | 15 | Before and after shown, hours moved, freed hours placed; orphans at or under `o_max` | The audit was run once and nothing changed |
| Setting and art direction | 10 | One setting line per pillar, in the spirit of MMO406 week 1: the world explains the rules; the art direction page ties each choice to a pillar or setting line | Lore unconnected to any system, or no art direction page |
| Team ownership | 5 | Any member explains a weight | One member answers everything |
| **Total** | **100** | | |

## Late and missing work

Up to 48 hours late is capped at 70. Thresholds committed after the week 4 session starts score 0 on the test lines row, whatever the reason, because a threshold set after the data is not a test.
