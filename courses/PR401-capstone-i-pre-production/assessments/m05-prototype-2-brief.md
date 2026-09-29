# PR401 · Milestone 5 brief: prototype 2 and the greenlight evidence table

**Weight:** 15% of the course grade, half of the prototypes component (30%).
**Assigned:** week 5. **Due:** before the week 6 greenlight session, in `preproduction/week05/` and `prototypes/p2/`. **Reviewed:** at the week 6 greenlight.
**Work mode:** team. One team mark, adjusted per person by the [peer assessment](peer-assessment-brief.md).
**Session guide and lab:** [week 5, prototype 2](../lectures/w05-prototype-2.md) with [lab 05](../labs/lab05.md).
**Builds on:** [PR201 week 11, playtest and telemetry review](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w11-playtest-and-telemetry-review.md) (the unit of analysis in a group test), [MMO405 week 2, quantitative methods](../../MMO405-research-methods-in-online-games/lectures/w02-quantitative-methods-overview.md), sections 4 and 5 (nesting and preregistration), [MMO405 week 5, experiments](../../MMO405-research-methods-in-online-games/lectures/w05-experiments-and-quasi-experiments.md), and [MMO405 week 10, ethics](../../MMO405-research-methods-in-online-games/lectures/w10-ethics-and-irb.md).

## What this milestone proves

That the team knows the difference between seeing a problem and measuring a rate, and bought the answer it could afford. *Emberfall*'s prototype 1 found every major problem with its craft and trade loop and still could not say whether the loop held: 5 of 8 gives a Wilson interval from 31% to 86% against a threshold of 50%. Prototype 2 either settles a decision question with a sized test or states plainly that it could not, and why.

## Deliverables

1. **Updated risk sheet** and the rerun lab 04 checker output with prototype 1 results.
2. **Sizing sheet** (`sizing.csv`) and the `check_sizing.py` output.
3. **Options and brief**: `options.md` with at least two options costed against the budget, and `brief-p2.md` with the choice and, if sequential, the stop rule. Both committed before the first test group plays.
4. **Prototype 2 build** in `prototypes/p2/` with a README, and **result reports** with raw notes.
5. **Greenlight evidence table** (`evidence.md`): every load-bearing claim, its evidence level, `n`, `k`, the interval at effective sample size and the verdict, with an exposure total that matches the rerun burn-down.
6. **Time log** for prototype 2, and one line comparing prototype 1's actual hours with `c`.

## Evidence required

| Evidence | Format | How the instructor checks it |
|---|---|---|
| Question types | Label on every prototype question | Discovery or decision; no rate decided from a discovery sample |
| Sample size | `sizing.csv` and checker output | Reruns `check_sizing.py`; `n₀`, a stated `ρ` and the design effect are used |
| Stop rule in advance | Commit date of `brief-p2.md` | Predates the first test session |
| Results | `n`, `k`, interval, verdict per decision question | Recomputes one interval with the design effect |
| Evidence table | `evidence.md` | Exposure total equals the rerun burn-down |
| Iteration | Change list between prototypes | One kind of change at a time, each traced to a prototype 1 observation |

## How it is marked

The greenlight panel reads the evidence table at the week 6 meeting. The instructor marks this milestone from the submitted files and the panel's notes. A panel member may ask any team member to read an interval off the table and say what it means for the claim.

## Rubric

| Criterion | Points | Full marks when | Low marks when |
|---|---|---|---|
| Checker passes | 10 | `PASS` on rerun, output saved | Fails |
| Question types | 10 | Every question labelled; discovery samples used only to find problems | A rate claimed from five think-aloud users |
| Sizing | 15 | `p` from prototype 1; thresholds trace to earlier commits; `ρ`, group size and observer hours realistic | `ρ` of zero with players tested in groups, or thresholds moved |
| Options and choice | 15 | Two or more options with numbers; the choice argued against the budget; what was left open is stated | One option, or no costs |
| Stop rule | 10 | Written before the first group; covers every outcome at the look | Added after the first look, or missing for a sequential test |
| Iteration | 10 | Changes are one kind at a time, each traced to an observation | Several changes at once, so no result can be attributed |
| Results | 15 | `n`, `k`, interval at effective size and a verdict for each decision; `ρ` checked where possible | Point estimates only |
| Evidence table | 10 | Every load-bearing claim present; exposure reconciles with the burn-down | Claims missing, or totals that do not match |
| Team ownership | 5 | Any member reads an interval correctly | Only the analyst can |
| **Total** | **100** | | |

## Late and missing work

The evidence table must be in the repository before the greenlight session starts. A table added after the session scores 0 on the evidence table row. Other late work is capped at 70 for up to 48 hours.
