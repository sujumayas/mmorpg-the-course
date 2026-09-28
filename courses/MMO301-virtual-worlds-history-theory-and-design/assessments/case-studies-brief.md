# MMO301 · Case studies brief

**Weight:** 40% of the course grade, in three case studies.
**Case study 1:** Worlds that run themselves (weeks 1 to 3). 15% of the course. Fed by [Lab 01](../labs/lab01.md) and [Lab 03](../labs/lab03.md).
**Case study 2:** The endgame and the price of risk (weeks 4 to 6). 15% of the course. Fed by [Lab 04](../labs/lab04.md) and [Lab 05](../labs/lab05.md).
**Case study 3:** A world that died (week 13). 10% of the course. Fed by [Lab 13](../labs/lab13.md).

## What this component is for

The third course outcome is "analyze design lessons from landmark MMOs and their failures." A lesson is only worth something if you can show where it comes from. Each case study asks you to take one historical world, state one model from the lectures, run it on numbers you built in a lab, check it against the dated record, and say what a designer should decide differently because of it. Then say what the model cannot see.

That is the same shape as a worked example in this course's lectures. A case study is a worked example you write yourself, about a real world, with the evidence cited.

## How each case study is marked

Each case study is marked out of 100.

- **Labs, 40 points.** The feeding labs are submitted on their own dates and marked with the rubric printed in each lab. Their percentage scores are scaled to 40 points. Where two labs feed one case study, each is worth 20.
- **Case essay, 60 points.** Marked with the rubric at the end of this brief. The same rubric is used for all three essays, so feedback on the first one tells you what to fix in the second.

After each essay is returned, you have a 5-minute spot check with a marker in the next lab session. The marker picks one number from your essay and asks you to recompute or explain it, in the style of the [exam bank](exam-bank.md). The spot check is not graded on its own. If you cannot explain a number you submitted, the marker can move your "Numbers" line down one band.

## The case essay

### Length and structure

1,500 to 1,800 words, plus tables, charts and a source list. Use these headings in this order.

1. **The observation.** One surprising, checkable fact from the case that players or developers noticed, with its date and source. This is the hook.
2. **The model.** One model from the lectures, stated once, with every symbol named. Say which lab you built it in.
3. **The numbers.** A table from your lab sheet, with your parameter values and which of them are assumptions. At least one row must be checkable by hand in the essay.
4. **The record.** A dated timeline of at least five events from the case, each with a source. Show where the model's prediction matches the record and where it does not.
5. **Other worlds.** At least two other games or contexts rewritten into the same model, so the reader sees it is one idea.
6. **Design judgment.** What a designer should decide on purpose because of this case, with the cost of each choice named. "Players hated it" is not a cost. "Hoarders pay 12 units a day and casual players 3" is.
7. **What the model leaves out.** At least two things, and which way each would move your numbers.

### Rules for facts

- Every claim about a real game, company or person needs a source in your list, with the version, patch or era it describes. The lecture's Sources section counts as a source for the facts it lists. New facts need their own citation.
- Prefer official sources (developer posts, patch notes, GDC talks, papers), then well-maintained wikis, then press from the time.
- Say which numbers are invented. The lecture models all use invented parameters, and so will yours. That is fine if you label them.
- Paraphrase. Quote at most one short phrase per source.

## Case study 1: Worlds that run themselves

**Weeks:** [1](../lectures/w01-what-is-a-virtual-world-bartles-definition.md), [2](../lectures/w02-mud1-muds-moos-and-the-text-era.md), [3](../lectures/w03-ultima-online-the-simulation-dream-and-its-limits.md). **Labs:** [01](../labs/lab01.md) (world audit and density sheet) and [03](../labs/lab03.md) (the closed loop and the faucet).

Choose one prompt.

- **1A. The resource bank (recommended).** Why did Ultima Online's planned resource ecology empty out, and why did adding resources not fix it? Use the closed-loop model `s* = d × R` and your Lab 03 runs, including the hoarding minority. Place Ultima Online on Bartle's persistence ladder and explain why MUD1's reset was not available to it. Your design-judgment section must compare the closed loop with the faucet/drain that replaced it and size the stored stock `σ(1 − d)/d` the faucet leaves behind.
- **1B. Who builds the world.** Why did TinyMUD-style worlds run through a cycle of boom and collapse while LPMud-style worlds lasted, and what did LambdaMOO's governance crisis add? Use the content-race model from week 2 with your own parameter set, and the persistence-versus-change grid from week 1 as your Lab 01 audit applied it. Your design-judgment section must propose a content drain and a governance mechanism and name who each one angers.

Whichever prompt you choose, the "Other worlds" section must include the game you audited in Lab 01.

## Case study 2: The endgame and the price of risk

**Weeks:** [4](../lectures/w04-everquest-the-treadmill-and-the-raid.md), [5](../lectures/w05-world-of-warcraft-accessibility-and-the-themepark.md), [6](../lectures/w06-eve-online-the-single-shard-sandbox.md). **Labs:** [04](../labs/lab04.md) (contested versus instanced loot) and [05](../labs/lab05.md) (auditing a death rule).

**Prompt.** World of Warcraft removed barriers that EverQuest had kept: contested raid bosses, experience lost on death, corpse runs, groups formed by hand. What did each removal buy and what did it cost the world? Use two models, the contested-loot model (`W = G × R / (s × d)` against `W = L × R / (7 × d)`) and the death-penalty model (`P = g × (1 − λt) − λx`), with the numbers from Labs 04 and 05. Your essay must answer one question with both models together. Which players did the older design serve better, and which did it push out?

EVE Online (week 6) is available as an "Other worlds" case. It keeps risk and prices it, which makes it a useful third point beside the two themepark answers.

## Case study 3: A world that died

**Week:** [13](../lectures/w13-worlds-that-died-shutdowns-and-their-lessons.md). **Lab:** [13](../labs/lab13.md) (sunset simulation and closure post-mortem).

**Prompt.** Extend your Lab 13 post-mortem into a full case essay. Your main case is the one you fitted in Lab 13. Add a second closed world whose main cause belongs to a *different* family of the four in the lecture (empty-world spiral, business decision, licence or partner, platform), and use it in the "Other worlds" section to show what the density-churn model can and cannot explain. Your design-judgment section must contain the five-question sunset plan from the lecture, rewritten for your main case one year before its closure, with a trigger that is a number.

The Lab 13 post-mortem (600 words) may be reused inside the essay. The essay must add the observation, the second world and the limits section, and revise the post-mortem in response to the lab feedback.

## Milestones

Labs are due at the start of the week after they are assigned unless the lab states another date.

| When | Milestone | Graded? |
|---|---|---|
| Start of week 2 | Lab 01 submitted | Case study 1, 20 points |
| Start of week 4 | Lab 03 submitted | Case study 1, 20 points |
| Week 4 lab session | **Prompt choice for case study 1** (1A or 1B) and a five-row draft timeline, checked by a marker in 5 minutes | No, but required |
| Start of week 5 | Lab 04 submitted | Case study 2, 20 points |
| Start of week 6 | Lab 05 submitted | Case study 2, 20 points |
| Start of week 6 | **Case study 1 essay** submitted | Case study 1, 60 points |
| Week 7 lab session | Case study 1 returned; spot check | No |
| Start of week 9 | **Case study 2 essay** submitted | Case study 2, 60 points |
| Week 10 lab session | Case study 2 returned; spot check | No |
| Start of week 14 | Lab 13 submitted, as the lab states | Case study 3, 40 points |
| End of week 14 | **Case study 3 essay** submitted | Case study 3, 60 points |
| Week 15 | Case study 3 returned; spot check folded into the world bible viva | No |

## Case essay rubric (60 points)

| Criterion | Points | Excellent | Good | Adequate | Weak or missing |
|---|---|---|---|---|---|
| Observation and record | 10 | 9-10: a sharp, dated hook; a timeline of five or more events, every row cited with era, sources of more than one kind | 7-8: timeline complete, one row uncited or one source type only | 5-6: fewer than five events, or several uncited | 0-4: no timeline, or claims without sources |
| Model | 10 | 9-10: stated once with every symbol named; applied to the case, not only described; the right model for the question | 7-8: stated and applied, one symbol vague | 5-6: described in words, applied loosely | 0-4: missing or misapplied |
| Numbers | 12 | 11-12: table from the lab sheet, one row checked by hand in the text, assumptions labelled, figures traceable | 8-10: numbers correct, one assumption unlabelled | 6-7: numbers present but not tied to the sheet, or one error that changes a conclusion | 0-5: no numbers, or several errors |
| Other worlds | 8 | 7-8: two or more cases rewritten into the model's symbols, with one that shows where the model strains | 5-6: two cases, rewritten loosely | 4: one case, or cases named without the model | 0-3: missing |
| Design judgment | 12 | 11-12: decisions a designer could act on, each with its cost and who pays it, argued against an alternative | 8-10: decisions and costs named, alternatives thin | 6-7: judgment generic, could fit any game | 0-5: summary instead of judgment |
| Limits | 4 | 4: two or more limits, each with the direction it moves the numbers | 3: limits named without direction | 2: one limit | 0-1: none |
| Writing | 4 | 4: plain, numbers first, within length, headings as specified | 3: readable, slightly long or padded | 2: hard to follow in places | 0-1: over length by more than 20% or unstructured |

## Late work and integrity

An essay submitted up to 48 hours late loses 6 of its 60 points. After that it is marked for feedback only and scores 0 on the essay part. A lab submitted up to 48 hours late loses 10% of its marks, and after that it scores 0. You may take one 48-hour extension on one lab in the whole course without penalty by telling your tutor before the deadline.

You may discuss the models and the historical record with classmates. Your sheets, runs and prose must be your own. If you use an AI tool, say where in a one-line note at the end. You are still responsible for every number and every source, and the spot check will test that.
