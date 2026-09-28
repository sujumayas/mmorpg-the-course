# MMO402 · Case analyses brief

**Weight:** 30% of the course grade.
**Covers:** labs 01 to 10, 12 and 13, plus the week 11 case analysis specified in this brief. Thirteen items in all.
**Related briefs:** [debate-brief.md](debate-brief.md) (lab 14 counts there) and [final-paper-brief.md](final-paper-brief.md) (most case analyses are reused there). Practice questions for every week are in the [exam bank](exam-bank.md).

## What this component is for

The course outcomes behind this component are "analyze emergent player governance" and "design moderation and justice systems". Each case analysis asks you to take one lecture model, apply it to a case or a dataset you have not seen worked, and say what a studio should do, with numbers. The habit being built is the same every week: model, numbers, verdict, recommendation, cost.

Most items reappear in the final governance design paper. Do them well once and you will reuse them.

## The items

| Item | Topic | Assigned | Due | Can be dropped? |
|---|---|---|---|---|
| [Lab 01](../labs/lab01.md) | Governance audit of a live world | Week 1 | Start of week 2 | Yes |
| [Lab 02](../labs/lab02.md) | Keys to the vault | Week 2 | Start of week 3 | Yes |
| [Lab 03](../labs/lab03.md) | Count the council | Week 3 | Start of week 4 | Yes |
| [Lab 04](../labs/lab04.md) | The allowed-play brief | Week 4 | Start of week 5 | **No** |
| [Lab 05](../labs/lab05.md) | Terms-of-service audit | Week 5 | Start of week 6 | Yes |
| [Lab 06](../labs/lab06.md) | Triage the queue | Week 6 | Start of week 7 | Yes |
| [Lab 07](../labs/lab07.md) | Tune a review panel | Week 7 | Start of week 8 | Yes |
| [Lab 08](../labs/lab08.md) | A player charter | Week 8 | Start of week 9 | Yes |
| [Lab 09](../labs/lab09.md) | Case briefs with the layer test | Week 9 | Start of week 10 | **No** |
| [Lab 10](../labs/lab10.md) | Pacing audit | Week 10 | Start of week 11 | Yes |
| Case analysis 11 (below) | Gate, default and fallback | Week 11 | Start of week 12 | Yes |
| [Lab 12](../labs/lab12.md) | Release audit | Week 12 | Start of week 13 | Yes |
| [Lab 13](../labs/lab13.md) | Shutdown policy memo | Week 13 | Start of week 14 class | Yes |

"Start of week N" means before the first class session of that week.

Labs 04 and 09 always count. Together they carry the course's signature case, the Bank of EVE and the question of when in-world fraud is allowed play, through the two tests the course builds for it (week 4's allowed-play test and week 9's layer test).

Lab 14 is not a case analysis. It is the debate case file and counts in the [debate brief](debate-brief.md).

## How the grade is computed

1. Each item is marked out of 100 with the rubric printed in that lab, or with the rubric below for case analysis 11.
2. Labs 01 to 09 print four bands with percentage weights: Excellent (4), Adequate (2 or 3) and Missing or wrong (0 or 1). The marker records the band score for each criterion. A criterion's points are `weight × band score / 4`. For example, an Adequate (3) on a 20% criterion earns `20 × 3/4 = 15` points.
3. Labs 10 and 12 print points directly with full, half and zero marks. Lab 13 prints percentage weights with the same three levels. Full marks earn the whole weight, half marks earn half, and missing earns 0.
4. Your three lowest item scores are dropped, except labs 04 and 09.
5. The ten remaining items are averaged with equal weight. Each counted item is worth 3% of the course grade.

A missing item scores 0 and is a candidate for dropping like any other score.

### Quality descriptors across all items

Markers use these descriptors to keep marks consistent across the thirteen rubrics, and to moderate a sample of each item across markers.

| Band | Item score | What the work looks like |
|---|---|---|
| Excellent | 85-100 | The model is applied correctly to the case. Every check value reproduces. Every claim about a real game is cited with its version or date. The recommendation follows from the numbers and names its cost and who bears it. |
| Good | 70-84 | Correct model and numbers, with one gap: a thin justification, a missing sensitivity check, or a recommendation whose cost is only partly named. |
| Adequate | 55-69 | The model is used, but with errors a careful reader would catch, or the recommendation does not follow from the numbers. |
| Weak | 40-54 | The model is misapplied or used only as decoration, and conclusions rest on opinion. |
| Missing | 0-39 | Required parts absent, numbers wrong throughout, or unsourced claims about real games. |

## Case analysis 11: gate, default and fallback

Week 11 has no lab session. This case analysis replaces it. The task is the one set in the [week 11 lecture](../lectures/w11-minors-in-online-worlds.md), "Lab / assignment hook".

**Objective.** Write a two-page case analysis of one real world from section 2 of the week 11 lecture: Club Penguin, Toontown Online, Fortnite after the 2022 FTC order, or Roblox from 2025. State its gate, default and fallback in the lecture's model. Estimate plausible values for each rate, with your reasoning. Recommend one change and compute its effect.

**Starter materials.**

- The model from lecture section 2: children missed `= N × π × (1 − se)`, older players wrongly restricted `= N × (1 − π)(1 − sp)`, precision of the child flag `= π se / (π se + (1 − π)(1 − sp))`, children exposed `= missed × k`.
- The week 11 interactive, `examples/w11-age-gate.html`, once it is built. Until then, a spreadsheet with the formulas above.
- The lecture's sources for your chosen world. You may add sources, and you must cite them with dates.

**Steps.**

1. **Facts (at most 200 words).** Describe the world's gate, its communication tiers and defaults, and its fallback for misclassified players, with dates and sources.
2. **Model mapping.** Write the world in the model's terms. Which of `π`, `se`, `sp` and `k` does each feature set? Say which features the model does not capture (for example, a code exchange that targets strangers rather than age).
3. **Estimates.** Give a value or a range for each rate with one sentence of reasoning. Label every value as your estimate. Do not present an estimate as a published figure.
4. **Numbers.** For `N = 100,000` sign-ups, compute children missed, older players wrongly restricted, precision and children exposed for the world as it is.
5. **Recommendation.** Propose one change: a different gate, a different default, an appeal route, or a change to a communication tier. Compute its effect on exposure and on wrongly restricted players. Name who bears the cost.
6. **Tension.** In one paragraph, name the tension from lecture section 3 your change makes worse (safety against privacy, protection against inclusion, protection against autonomy, or separation against community) and say why you accept it.

**Deliverable.** A PDF of two pages plus sources and a calculation sheet, named `ca11-<surname>.pdf`.

**Rubric (100 points).**

| Criterion | Points | Excellent | Good | Adequate | Weak or missing |
|---|---|---|---|---|---|
| Facts and sourcing | 15 | 13-15: gate, tiers, defaults and fallback all described, dated and cited | 10-12: one element undated or thinly cited | 7-9: facts partly unsourced | 0-6: unsourced or wrong |
| Model mapping | 20 | 17-20: every feature mapped to a rate, and what the model misses is named | 14-16: mapping correct, limits not named | 10-13: one feature mapped to the wrong rate | 0-9: model not used |
| Estimates and numbers | 25 | 22-25: every rate estimated with reasoning, labelled as an estimate, all four outputs computed correctly | 17-21: one estimate unreasoned or one arithmetic slip | 12-16: several estimates bare, or outputs incomplete | 0-11: no numbers or wrong model |
| Recommendation with computed effect | 25 | 22-25: one concrete change, its effect on exposure and on wrongful restriction computed, who pays named | 17-21: effect computed on one side only | 12-16: change proposed without numbers | 0-11: missing |
| Tension named | 10 | 9-10: a named tension, argued with reference to the chosen world | 7-8: tension named, argument generic | 5-6: tension implied | 0-4: missing |
| Writing | 5 | 5: two pages, plain, own words | 4: slightly over length or padded | 3: unclear in places | 0-2: unclear or copied |

## What to submit each week

- The document the lab asks for, as a PDF, named as the lab specifies.
- Any code or spreadsheet the lab asks for, runnable as submitted. Labs 02, 03, 06, 07, 10, 12 and 13 print check values. Reproduce them before you run your own experiments. If yours differ, say so and say which you trust and why. An honest mismatch loses fewer points than a silent one.
- Word counts are targets. Anything within 20% either way is fine. Page limits are firm.

### Rules that apply to every item

These are the habits the lectures teach. Markers apply them whatever the lab's rubric calls the criterion.

- **Name the model.** Every analysis says which lecture model it uses and states it once, with every symbol defined.
- **Label invented numbers.** Rates you estimate are labelled as estimates. Figures about real games are cited with their version or era.
- **One recommendation, with its cost.** A recommendation that costs nothing has not been thought through. Name who pays: the studio, the players, a subgroup of players, or moderators.
- **Paraphrase.** No long quotations from terms of service, policies or articles. At most one short quoted phrase per source.

## Milestones

| When | Milestone | Graded? |
|---|---|---|
| Weekly, start of weeks 2 to 14 | Item submitted (see the items table) | Yes |
| Week 5 | Feedback on labs 01 to 03 returned. Use it before lab 04. | No |
| Week 10 | Feedback on labs 04 to 07 returned, including the compulsory lab 04. | No |
| End of week 13 | All feedback on labs 01 to 12 and case analysis 11 returned, in time to reuse the work in the final paper | No |
| Week 15 | Case analyses grade released with the drop applied | Yes |

## Late work and extensions

- An item submitted up to 48 hours late loses 10 points out of 100. After that it scores 0 and becomes a candidate for dropping.
- You have two free 48-hour extensions over the semester, for any item except lab 13. Tell the course team before the deadline. Lab 13 has no extension, because the week 14 debate uses it as evidence.
- Documented illness or emergency is handled separately and does not use a free extension.

## Academic integrity

Discuss cases and methods with classmates. The numbers, tables and words you submit are yours. Labs 05, 06 and 10 are pair work; both names go on the submission and both partners receive the mark. Cite the source of every real-game fact, and do not introduce a game fact you cannot source. If you use a generative AI tool, say how, and check every number and source it gives you yourself.
