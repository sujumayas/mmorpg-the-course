# PR401 · Milestone 9 brief: content plan

**Weight:** 5% of the course grade, inside the pre-production package component (50%).
**Assigned:** week 9. **Due:** at the start of week 10, in `docs/content-plan.md` and `preproduction/week09/`. **Reviewed:** at the week 10 stand-up.
**Work mode:** team. One team mark, adjusted per person by the [peer assessment](peer-assessment-brief.md).
**Session guide and lab:** [week 9, content plan](../lectures/w09-content-plan.md) with [lab 09](../labs/lab09.md).
**Builds on:** [PR101 week 6, estimation](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w06-estimation-and-why-it-fails.md) (why measured costs beat estimates), [MMO406 week 7, lore delivery](../../MMO406-worldbuilding-and-lore-for-persistent-worlds/lectures/w07-lore-delivery-in-mmos.md) (lore for a population that turns over), and [MMO406 week 9, living world events](../../MMO406-worldbuilding-and-lore-for-persistent-worlds/lectures/w09-living-world-events.md) (the patch-week event).

## What this milestone proves

That "enough content" is a costed list with measured authoring ratios, filled in yield order, and that the team knows which single claim the live period depends on. In *Emberfall*'s plan the recipe set carries 8 of 19.2 hours of median play on an assumed `r = 8`. If it is 4, the median player has almost a week with nothing new. The plan is marked on whether it finds that claim and schedules its test, not on how much content it promises.

## Deliverables

1. **Content inventory and plan** (`content.csv`, `params.csv`) in the lab 09 format, with `content_yield.py` printing `PASS`.
2. **Measured `k` table** for every content type prototyped, from real hours and tester play times.
3. **Sensitivity paragraph**: the claim that carries the most of `Σ E`, the drought if it halves, and the vertical slice sprint 1 test that will settle it.
4. **Content calendar** across the build window with dependencies, and one unit held for the PR402 patch week.

## Evidence required

| Evidence | Format | How the instructor checks it |
|---|---|---|
| Measured `k` | Table in `content-plan.md` | Hours trace to the prototype time logs; play times to tester notes |
| Unit fields | `content.csv` | Every unit has cost, `c`, `r`, evidence and a must-have flag |
| Selection | Checker output | Reruns `content_yield.py`; must-haves in, rest in yield order or departures explained |
| Drought | Checker output and paragraph | Median drought and the case for the largest assumed `r` |
| Test scheduled | Sprint 1 backlog | The load-bearing `r` test is an item in slice sprint 1 |
| Calendar | Calendar table | Every unit in a sprint with its dependencies; patch-week unit named |

## How it is marked

The instructor reruns the checker and asks one member to recompute a unit's yield and one to say what happens to the median drought if the load-bearing claim halves.

## Rubric

| Criterion | Points | Full marks when | Low marks when |
|---|---|---|---|
| Checker passes | 10 | `PASS` on rerun, declared totals match | Fails |
| Measured `k` | 20 | Every prototyped type measured from real hours and tester medians | Week 1's `k = 20` reused |
| Inventory | 15 | All candidates listed, costed as shipped, honest evidence labels | Only the units the team already chose |
| Selection by yield | 15 | Must-haves in, the rest in yield order within budget, departures explained | Chosen by what the team likes to build |
| Sensitivity and test | 20 | Load-bearing claim named; drought if it halves; a specific test scheduled in sprint 1 | No sensitivity case, or a test with no date |
| Calendar | 10 | Every unit in a sprint with dependencies; one unit held for the patch week | Content with no dates |
| Lore fit | 5 | Content that carries lore works for players who arrive late, as in MMO406 week 7 | Lore only in a one-time intro |
| Team ownership | 5 | Any member recomputes a yield | Only the content designer can |
| **Total** | **100** | | |

## Late and missing work

Up to 48 hours late is capped at 70. The production plan needs the calendar, so late work must still be handed in.
