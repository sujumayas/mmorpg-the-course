# PR401 · Milestone 13 brief: pre-production review and final package

**Weight:** 6% of the course grade, inside the pre-production package component (50%).
**Assigned:** week 14. **Due:** replan and review decision record at the end of the week 14 meeting, in `preproduction/week14/`. The full pre-production package, with every review condition addressed, at week 15. **Reviewed:** at the week 14 review; the package is marked at week 15.
**Work mode:** team. One team mark, adjusted per person by the [peer assessment](peer-assessment-brief.md). Each member also sits the individual viva described in the [exam bank](exam-bank.md).
**Session guide and lab:** [week 14, pre-production review](../lectures/w14-pre-production-review.md) with [lab 14](../labs/lab14.md).
**Builds on:** [MMO403 week 14](../../MMO403-business-monetization-and-ethics-of-live-games/lectures/w14-pitching-to-publishers-and-investors.md), section 2 (stage gates and kill rules), [PR101 week 14, post-mortems as a practice](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w14-post-mortems-as-a-practice.md), section 4 (checkable action items), [MMO405 week 2](../../MMO405-research-methods-in-online-games/lectures/w02-quantitative-methods-overview.md), section 5 (deciding in advance what would change your mind), and [MMO406 week 14, bible workshop](../../MMO406-worldbuilding-and-lore-for-persistent-worlds/lectures/w14-bible-workshop.md) (the world bible the package carries).

## What this milestone proves

That the team replanned PR402 from what the slice measured, and brought the plan and the evidence to a panel that could say no. *Emberfall*'s slice town cost 10 hours against 6.5 planned. At a planned learning rate of 0.95, three more towns put art at 1.05. The team planned two, held the fourth town on the cut list behind a trigger on unit 2's hours, and said so on its first slide before the panel asked. That is what this milestone rewards.

The mark does not depend on the panel's decision. A team that receives "rework" and turns every condition into a checkable action item can score full marks.

## Deliverables

At the end of the week 14 meeting:

1. **Replanned production plan**: `team.csv`, `backlog.csv`, `replan.csv`, `replan-log.md`, the flat-rate output (`flat-output.txt`) and `reconcile.py` printing `PASS`, plus the updated `production-plan.md` with the new load table and learning-rate triggers.
2. **Review decision record** (`review-decision.md`): the panel's decision, each condition as an action item with an owner, a date and an observable result, and the peer panel's questions with your answers.

At week 15, the **pre-production package**, one folder with an index page linking each part (week 14 section 2):

3. The greenlit pitch from week 6, updated with anything the slice changed.
4. Pillars and vision (week 3), with the setting lines and a short world bible in the MMO406 week 14 form.
5. Technical design (week 7), updated with what the slice taught about the server and data.
6. Economy and balance design (week 8), content plan (week 9) and social systems plan (week 10), each with a "changed since" note.
7. The replanned production plan and risk register.
8. The vertical slice tag, the stability statement and the tagged time log.
9. A conditions table showing each review condition, its action item and the evidence it is met.

## Evidence required

| Evidence | Format | How the instructor checks it |
|---|---|---|
| Measured costs | `replan.csv` | Every content type the slice built uses `u_1` from tagged per-unit hours, one-time hours removed |
| Learning rate | `replan.csv` and log | 0.95 or flat, unless two measured units or written evidence support lower |
| Loads | `reconcile.py` output | Reruns it; every discipline at or below 1.0 at every milestone |
| Triggers | Risk register | Each changed assumption (learning rate, tool `u_t`, crash bound) has a trigger and a response for each direction |
| Conditions | Conditions table | Each has an owner, a date, an observable result, and evidence it was met by week 15 |
| Safety minimums | `safety.csv` and the replanned backlog | Each week 10 minimum is in the slice or scheduled before PR402's closed beta, with an owner |
| Package consistency | Index page | Numbers match across documents: CCU, towns, prices, hours |

## How it is marked

The panel runs the review as in week 14 section 4: play, plan, questions, decision. The instructor marks the replan and the decision record from the week 14 files, and the package from the week 15 folder. The instructor checks three numbers across documents; a mismatch costs marks on the consistency row.

## Rubric

| Criterion | Points | Full marks when | Low marks when |
|---|---|---|---|
| Replan from measured costs | 20 | `PASS` on rerun; every slice-built type replaced with measured `u_1`; flat run saved and discussed | The week 11 plan brought unchanged |
| Learning-rate judgment | 15 | Planned rate defended with evidence; triggers on unit 2 with a response each way | 0.8 planned from one unit |
| Replan log | 10 | Every change with hours and the pillar touched; units cut before quality | Quality bar lowered to fit |
| Presentation | 10 | States what changed since week 11 before the panel asks; answers with numbers or "we did not measure that, and here is how we will" | Reads the package aloud, or guesses |
| Decision record | 15 | Decision and every condition recorded, read back, and turned into action items with owner, date and observable result | Conditions paraphrased or missing dates |
| Package completeness | 15 | All parts present with "changed since" notes; every condition met or its status evidenced | Parts missing, or conditions ignored |
| Consistency across documents | 15 | Spot-checked numbers agree across pitch, TDD, economy, content, social and production plan | The TDD says 60 CCU and the social plan plans for 120 |
| **Total** | **100** | | |

## Late and missing work

The week 14 files cannot be late: the decision record is written at the meeting. A package handed in up to 48 hours after the week 15 deadline is capped at 70. After that it scores 0, and PR402 cannot start production without it.
