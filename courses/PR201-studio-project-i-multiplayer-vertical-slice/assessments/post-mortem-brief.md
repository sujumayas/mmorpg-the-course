# PR201 · Post-mortem and viva brief

**Weight:** 10% of the course grade, inside the post-mortem and peer review component (20%). The other 10% is the [peer assessment](peer-assessment-brief.md).
**Assigned:** week 12. **Due:** team post-mortem and individual reflections at the end of week 15. Vivas run in week 15 and the exam period.
**Work mode:** mixed. The team post-mortem gets one team mark (not peer-adjusted). The reflection and viva are individual.
**Builds on:** [PR101 week 14, post-mortems as a practice](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w14-post-mortems-as-a-practice.md), [PR101 week 12, crunch](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w12-crunch-causes-costs-alternatives.md) and [UX201 week 14, UX research reporting](../../UX201-game-ux-and-player-psychology/lectures/w14-ux-research-reporting.md).

## What this component is for

A post-mortem is useful when it changes what the team does next time. PR301 teams will read yours before they pitch. So it has to be specific, blameless and checkable. The individual reflection and viva test that each member understands the slice's production and networking decisions, not only the part they built.

## Deliverables

### Team post-mortem (40 points)

`docs/post-mortem.md`, 2,000 to 3,500 words, built from the exports frozen in `production/postmortem-data/` at the end of [week 14](../lectures/w14-release-candidate.md).

1. **Timeline.** Planned and actual dates for every milestone, and the velocity per sprint.
2. **Estimate accuracy.** Planned against actual hours per discipline, using the week 1 fit sheet as the plan. Which discipline load was most wrong, and by how much.
3. **What went right and what went wrong.** Each item coded with a category from PR101 week 14, supported by an artefact (a board export, a telemetry row, a playtest note, a commit).
4. **Recurrence check.** The PR101 jam post-mortem categories against these ones, with the recurrence rate `R` and the closure rate.
5. **Action items.** At most five, each with an owner, a change and a check that a PR301 team could run.

### Individual reflection (30 points)

`docs/reflections/<your-id>.md`, 800 to 1,200 words, written alone.

1. Two decisions you made or argued for, what evidence you had, and whether it held up.
2. One networking or persistence decision you did not own. Explain it well enough that the owner would agree.
3. Your planned hours against your logged hours, and what changed.
4. One thing you would do differently, as a checkable action item.

### Viva (30 points)

15 minutes, one student and two examiners, with the build and the repository open. Examiners pick five or six questions from the [exam bank](exam-bank.md), rewritten with your team's numbers. At least two are about parts of the slice you did not build.

## Rubric

| Criterion | Points | Full marks when | Low marks when |
|---|---|---|---|
| Team: evidence | 15 | Every claim backed by a named artefact; estimate accuracy computed per discipline | Claims without artefacts; no numbers |
| Team: blameless analysis | 10 | Causes named as process or system; no individual blamed | Named blame, or vague "communication was bad" |
| Team: action items and recurrence | 15 | `R` and closure rate computed; five or fewer items, each owned and checkable | Items like "plan better"; no recurrence check |
| Individual: decisions and evidence | 12 | Two decisions with evidence and an honest outcome | Narrative of tasks done, no decisions |
| Individual: others' decisions | 10 | A decision owned by someone else explained correctly with its trade-off | Wrong or vague explanation |
| Individual: hours and action item | 8 | Planned against logged hours with a reason; one checkable change | No numbers, or a generic resolution |
| Viva | 30 | Answers use the team's real numbers, explain trade-offs and cover parts the student did not build | Answers limited to own tasks, or cannot explain the slice's architecture |
| **Total** | **100** | | |

The viva mark uses the marking guidance in the exam bank. A student who does not attend a viva without mitigating circumstances scores 0 on that row.
