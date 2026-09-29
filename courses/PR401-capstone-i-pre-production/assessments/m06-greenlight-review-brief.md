# PR401 · Milestone 6 brief: greenlight review

**Weight:** 6% of the course grade, inside the pitch component (20%).
**Assigned:** week 5 (package template), presented in week 6. **Due:** package before the week 6 meeting; fit sheet, decision record and cut list 48 hours after it, in `preproduction/week06/`. **Reviewed:** at the week 6 greenlight meeting.
**Work mode:** team. One team mark, adjusted per person by the [peer assessment](peer-assessment-brief.md).
**Session guide and lab:** [week 6, greenlight review](../lectures/w06-greenlight-review.md) with [lab 06](../labs/lab06.md).
**Builds on:** [PR101 week 6, estimation and why it fails](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w06-estimation-and-why-it-fails.md), section 2 (the plan ratio `R` and the buffer), [PR101 week 4](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w04-scope-mvp-vertical-slice-cut-lists.md), section 5 (ordered cut lists), [MMO403 week 14](../../MMO403-business-monetization-and-ethics-of-live-games/lectures/w14-pitching-to-publishers-and-investors.md), section 2 (stage gates), and [MMO403 week 13, team and budget planning](../../MMO403-business-monetization-and-ethics-of-live-games/lectures/w13-team-and-budget-planning.md).

## What this milestone proves

That the pitch fits the team at the team's own measured estimating record, and that the team leaves the gate with a decision it can plan against. *Emberfall*'s pitch as written had a fit ratio of 1.35 and a tripwire below 1. Its cut plan reached 0.97 with a tripwire of 1.35. The panel's decision was a conditional go with that tripwire as the condition. That is a good outcome, and it scores well here.

The milestone mark is not the panel's decision. A team that receives "pivot" and records it properly can score full marks. What is marked is the quality of the package and the record.

## Deliverables

1. **Greenlight package**, six pages at most, with the seven parts from week 6 section 2: the pitch on one page, prototype evidence, market position, feature list with estimates and the MVP line, the capacity and fit calculation, the risk register, and the ordered cut list.
2. **Fit sheet** (`team.csv`, `plan.csv`, `risks.csv`) in the lab 06 format, with `greenlight_fit.py` printing `PASS`.
3. **Decision record** (`decision-record.md`): outcome, conditions with dates and owners, and the tripwire value `R*` that reverses the decision.
4. **Updated cut list** (`cut-list.md`), ordered, with hours per item, reflecting the decision.

## Evidence required

| Evidence | Format | How the instructor checks it |
|---|---|---|
| Capacity | `team.csv` | `C = N × H × f` with `H = 112` or a stated alternative; `f` from PR301 with totals shown |
| Plan ratio | `team.csv` source column | `R` from PR301 sprint estimates and actuals, totals shown |
| Fit and tripwire | Checker output | Reruns `greenlight_fit.py`; `F` and `R*` match |
| Risk register | `risks.csv` | Five or more risks, each with `p`, hours, owner and an observable trigger |
| Worst case | `cut-list.md` | The largest risk's full cost is covered by cuts, or named as a pivot risk |
| Decision | `decision-record.md` against the panel's notes | Every condition has a date and an owner |

## How it is marked

The panel scores the package live on the six weighted criteria in week 6 section 3. The instructor then marks this milestone from the panel's scores and the submitted files, using the rubric below. The two override rules from week 6 apply to the gate decision, not to this mark.

## Rubric

| Criterion | Points | Full marks when | Low marks when |
|---|---|---|---|
| Prototype evidence | 20 | Each prototype states its question, testers, threshold and a measured answer; the riskiest claim is addressed | Demos with no question |
| Fit calculation | 20 | `PASS` on rerun; `f` and `R` measured from PR301 with totals; `F` and `R*` correct | `R` assumed, or checker fails |
| Risk register | 15 | Five or more risks with probabilities, hours, owners and observable triggers | Vague triggers ("if it goes badly") |
| Pillars drive the feature list | 15 | Every must-have traces to a pillar or foundation; orphans on the cut list; no feature over 80 hours | Features with no pillar kept above the cut line |
| Cut list | 10 | Ordered by distance from the pillars; hours per cut; worst case covered | Unordered, or cuts that remove a pillar's only feature |
| MMO scope and market | 10 | Persistence and player interaction the design depends on; two comparables and a reason to switch | Scope that would work single-player |
| Decision record | 10 | Outcome, every condition with date and owner, tripwire stated, read back at the meeting | Conditions missing dates or owners |
| **Total** | **100** | | |

## Late and missing work

The package must be in the repository before the meeting starts; a late package is presented as is and the panel scores what it has. The decision record and fit sheet are capped at 70 if more than 48 hours late.
