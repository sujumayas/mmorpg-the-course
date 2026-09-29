# MMO407 · Week 14 — Presentations

**Why this matters:** In week 15 you present your launch plan and your post-mortem analysis to a panel that acts as a launch readiness review. This week you rehearse for it. In a studio, that review decides whether the game ships on the date. Most review panels add up a scorecard, and an added-up scorecard can rate a plan at 92% while one of its criteria sits at zero. This week you learn how a panel should combine criteria, how to present a plan so a failing criterion cannot hide, and how to show that a lesson from a post-mortem transfers to your launch.

**You will be able to:**
- Compute a weighted readiness score, a weighted geometric score and a gate check for a launch plan, and explain why they can disagree.
- Compute the highest weighted score a plan can reach with one criterion at zero, and use it to critique a scorecard.
- Design a readiness scorecard with gates and weights for a given launch, and defend which criteria are gates.
- Structure a 12-minute launch plan presentation and a post-mortem analysis so that the decision, the ranges and the closest-to-failing gate come first.

**Before class:** Finish your launch plan draft (sections 1 to 7 from week 13). Read the Wikipedia article "Launch commit criteria", the introduction and the Space Shuttle section (10 minutes). Reread [MMO404 week 14](../../MMO404-advanced-networked-simulation/lectures/w14-case-study-presentations.md), sections 3 to 5, on presentation structure, evidence and questions; this lecture uses them and does not repeat them.

**Prerequisites from earlier courses:** [MMO404 week 14, case study presentations](../../MMO404-advanced-networked-simulation/lectures/w14-case-study-presentations.md) (separating sourced facts, model results and judgment; bracketing each assumption). [MMO308 week 13, incident response](../../MMO308-live-operations-analytics-and-experimentation/lectures/w13-incident-response.md) (blameless postmortems and action items that move a model's numbers). [MMO308 week 14, sunsetting content and servers](../../MMO308-live-operations-analytics-and-experimentation/lectures/w14-sunsetting-content-and-servers.md) and [MMO301 week 13, worlds that died](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w13-worlds-that-died-shutdowns-and-their-lessons.md) (models for shutdown cases, if your post-mortem analysis covers one). [MA102 week 4, expected value](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md) (weighted averages). In this course, [week 1](w01-launch-day-anatomy.md) (go/no-go criteria for the unlock), [week 2](w02-capacity-planning-and-login-queues.md) (queue forecasts as ranges) and [week 13](w13-launch-plan-workshop.md) (the disaster line and the exceedance curve). [Week 12](w12-writing-a-post-mortem.md) (writing a post-mortem).

**Interactive:** [examples/w14-readiness-gates.html](../examples/w14-readiness-gates.html). Keep it open during section 2.

---

## 1. The panel is a readiness review

Your final assessment has two parts, and you present both at the week 15 panel. This week you rehearse, with a mock review in class and a timed dry run in the lab.

- **The launch plan** (50% of the course grade). The seven sections from week 13, presented as if to the studio's launch readiness review.
- **The post-mortem analysis**, part of the case analyses (50% of the course grade). One published launch, relaunch or shutdown, read through a model from this course, ending in a lesson your launch plan uses.

A **launch readiness review** is the meeting, usually one to three weeks before the date, where the people who own the launch decide whether it goes ahead. The panel hears each area (capacity, testing, operations, communications, platform) and ends with one of three answers: go, go with conditions, or no-go. Week 1 gave you go/no-go criteria for the last hours before the unlock. The readiness review applies the same idea weeks earlier, to the whole plan.

Your week 15 panel plays that role. It is made of the instructor, one guest from industry where possible, and one student from another group. Everyone on it will ask the same underlying question: is there anything in this plan that should stop the launch? The rest of this lecture is about making the answer to that question visible, first with a model and then with how you present.

## 2. Worked example: the plan that scores 92% and should not ship

### The hook

Cyberpunk 2077 released on 10 December 2020 on PC, PlayStation 4, Xbox One and Stadia. On Metacritic, the PC version scored 86 out of 100. The PlayStation 4 version scored 57 and the Xbox One version 61. Before release, CD Projekt had given reviewers copies for PC only, and not for the last-generation consoles. Within days, Sony announced refunds and removed the game from the PlayStation Store "until further notice". It returned in June 2021 with a store warning that purchase for PS4 was not recommended. Class-action suits followed, and CD Projekt settled one for US$1.85 million, approved in January 2023.

It is not an MMO, but it is the clearest recent case of a launch where the average looked good and one platform was failing. Every view of the game that most people saw before release was an aggregate of mostly strong parts. The part that sank the launch was either given little weight or no evidence at all. Here is the question for your panel. If a plan is excellent on five criteria and zero on the sixth, what score should it get?

### The model

A readiness scorecard has criteria `i = 1 … n`. Each has:

- a score `sᵢ` between 0 and 1, the share of its target the plan meets (1 = met, 0 = nothing in place),
- a weight `wᵢ`, how much the panel says it matters, with `W = Σ wᵢ`,
- optionally a **gate** `gᵢ`, a minimum score below which the plan cannot launch, whatever else it does.

There are three common ways to combine them.

```
weighted average      S = Σ wᵢ sᵢ / W
weighted geometric    G = Π sᵢ^(wᵢ / W)
gate check            pass if sᵢ ≥ gᵢ for every gated criterion
```

The weighted average is **compensatory**: a high score on one criterion makes up for a low score on another, point for point. The gate check is **non-compensatory**: nothing makes up for a failed gate. The geometric score sits in between. It punishes low scores harder than the average, and a score of exactly zero anywhere makes `G` zero.

One number tells you how much a compensatory scorecard can hide. If criterion `k` scores zero and everything else is perfect, the average is

```
S_max with one zero = 1 − wₖ / W
```

With six equally weighted criteria, that is 83%. With the zero on a criterion that carries 1 of 12 weight points, it is 92%.

### Numbers you can check

Take a readiness scorecard with six criteria. The weights and gates are invented teaching values, but every row comes from a week of this course.

| Criterion | Weight | Gate | From |
|---|---|---|---|
| Capacity: queue forecast within target | 3 | 0.7 | Week 2 |
| Beta exposure for crash-class bugs | 2 | none | Week 3 |
| Restore drill run and timed | 2 | 0.7 | Week 13, DB201 week 14 |
| Kill switches built and flipped in test | 2 | 0.7 | Week 13 |
| Player communication plan | 2 | none | [Week 9](w09-communication-during-crises.md) |
| Low-end platform performance | 1 | 0.7 | This lecture |
| **Total `W`** | **12** | | |

Three groups present plans. Plan A is excellent everywhere except the low-end platform, where it has nothing. Plan B is solid and even. Plan C is strong with a thin beta.

| Criterion | A | B | C |
|---|---|---|---|
| Capacity | 1.0 | 0.85 | 0.9 |
| Beta exposure | 1.0 | 0.85 | 0.7 |
| Restore drill | 1.0 | 0.85 | 0.9 |
| Kill switches | 1.0 | 0.85 | 0.9 |
| Player comms | 1.0 | 0.85 | 0.9 |
| Low-end platform | 0.0 | 0.85 | 0.9 |

This code scores all three.

```python
from math import prod

# Launch readiness criteria: name -> (weight, gate). Gate None means "no minimum".
CRITERIA = {"capacity": (3, 0.7), "beta exposure": (2, None), "restore drill": (2, 0.7),
            "kill switches": (2, 0.7), "player comms": (2, None), "low-end platform": (1, 0.7)}
PLANS = {"A": [1.0, 1.0, 1.0, 1.0, 1.0, 0.0],   # scores in CRITERIA order, 1.0 = target met
         "B": [0.85] * 6,
         "C": [0.9, 0.7, 0.9, 0.9, 0.9, 0.9]}

W = sum(w for w, _ in CRITERIA.values())
for name, scores in PLANS.items():
    avg = sum(w * s for (w, _), s in zip(CRITERIA.values(), scores)) / W
    geo = prod(s ** (w / W) for (w, _), s in zip(CRITERIA.values(), scores))
    failed = [c for (c, (_, g)), s in zip(CRITERIA.items(), scores) if g is not None and s < g]
    print(f"plan {name}: average {avg:.3f}  geometric {geo:.3f}  failed gates: {', '.join(failed) or 'none'}")
```

It prints:

```
plan A: average 0.917  geometric 0.000  failed gates: low-end platform
plan B: average 0.850  geometric 0.850  failed gates: none
plan C: average 0.867  geometric 0.863  failed gates: none
```

Check plan A by hand. `S = (3 + 2 + 2 + 2 + 2 + 0) / 12 = 11 / 12 ≈ 0.917`, exactly `1 − 1/12`. Plan A tops the weighted average and fails the gate check. Plan C by hand: `S = (2.7 + 1.4 + 1.8 + 1.8 + 1.8 + 0.9) / 12 = 10.4 / 12 ≈ 0.867`.

The three rules give three rankings.

| Rule | Ranking | Plan A |
|---|---|---|
| Weighted average, launch at 0.8 or above | A, C, B | launches first |
| Weighted geometric, launch at 0.8 or above | C, B, then A at 0 | does not launch |
| Gates first, then weighted average | C, B | does not launch |

Now change one number. Suppose plan A has a rough low-end build that reaches 0.1 of its target instead of nothing. The average rises to 0.925. The geometric score jumps from 0 to `0.1^(1/12) ≈ 0.825`, above the launch line. Only the gate still says no. The geometric score catches a true zero and almost nothing else, because a criterion with weight 1 of 12 enters as a twelfth root.

### Move it yourself

Open the interactive. The left view is the scorecard most dashboards show: one horizontal gauge for the weighted average, with a launch line at 0.8, and a stacked bar showing how much each criterion contributes. With plan A loaded, the gauge sits at 91.7% and is green. The right view is the gate view: one row per criterion, its score as a bar, and its gate as a notch. The low-end platform row is empty and red, and the verdict at the top reads "no-go: 1 gate failed". Drag the low-end score from 0 to 0.1. The gauge barely moves, the geometric readout jumps from 0 to 0.825, and the gate row stays red until the score reaches 0.7. Then raise that criterion's weight from 1 to 3 and watch plan A's average fall to 0.786. A scorecard only notices a failing criterion if you gave it weight, which is the problem gates solve.

### Cross-game recognition

Averages and gates appear wherever games or engineers have to decide whether something is ready.

**Final Fantasy XIV (current patches).** Duties in the Duty Finder can require a minimum average item level. The game computes the average as the sum of the item levels of all equipped pieces divided by the number of slots, and when no shield is equipped the main-hand weapon counts twice, once for each hand. The community wiki draws the obvious conclusion: to reach a required minimum, upgrade the weapon first. That is a gate placed on a compensatory score. One old piece of armour can hide behind a strong weapon, exactly as plan A's zero hid behind five strong criteria.

**World of Warcraft (retail).** Warcraft Wiki records that item level is used as a gating requirement when queueing for dungeons, raids and scenarios, and that every character sheet shows an average item level. The shape is the same as in FFXIV: one summary number for a whole set of gear, and a hard minimum on that number. Both games chose it because a single number is easy to show players and hard to argue with. Both accept that a player can meet it with uneven gear.

**Rocket launches.** Launch commit criteria are conditions that must hold before a countdown proceeds. The Wikipedia article's examples include rules that forbid launch outright, such as not launching through disturbed weather, and rules that only delay the count, such as a 15-minute hold when electric field meters read above a limit. There is no average. Each rule is a gate, and each gate has its own consequence: scrub or hold.

**Cyberpunk 2077 (December 2020).** Rewritten in this week's terms, the pre-release evidence covered five strong criteria and gave the last-generation console criterion either no weight or no score. Reviews then scored platforms separately and the aggregate split: 86 on PC, 57 on PS4. A readiness review with a gate on every shipping platform would have had to say "no-go" or "go with conditions: PC and new consoles only". That is a business decision, and it should be made with the gate in plain view.

Four settings, one idea. A weighted average answers "how good is this overall?" A gate answers "is anything here bad enough to stop us?" A launch review has to ask the second question first.

### Eyes-open design judgment

- **Gate only what can sink the launch.** If every criterion is a gate, one weak comms plan blocks a strong launch, and teams learn to inflate scores. Gate the criteria whose failure lands above week 13's disaster line (capacity, data safety, containment, every platform you sell on). Weight the rest.
- **A gate needs a measured score.** "Restore drill: 0.9" means nothing unless 0.9 of something was measured, such as the restore running in 54 minutes against a 60-minute target. A gate on an opinion is a vote.
- **Missing evidence scores zero, not blank.** Cyberpunk's reviewers had no console copies. A scorecard that drops a criterion when its evidence is missing turns "we did not test it" into "it does not count". Make "no evidence" score zero.
- **Weights are where arguments hide.** Plan A's 92% came from giving the low-end platform 1 point in 12. Ask who set the weights, and when. As with week 13's disaster line, set them before anyone sees the scores.
- **"Go with conditions" is a real answer.** It means the plan launches with a gate removed from scope: a platform held back, a region delayed, trading disabled until the ledger alarm is proven. Write the conditions as week 13 triggers, with owners and stand-downs.

### Check this example

1. A scorecard has five criteria with weights 4, 3, 3, 2 and 2. What is the highest weighted average a plan can reach with the weight-2 criterion at zero? With the weight-4 criterion at zero?
2. Plan C's beta score falls from 0.7 to 0.4. Compute its new weighted average and geometric score. Does it pass the gates?
3. A reviewer proposes replacing the gates with the weighted geometric score and a launch line of 0.8. Give a plan, using this example's weights, that has no zero, passes the geometric line and should still not launch.

<details>
<summary>Answers</summary>

1. `W = 14`. With the weight-2 criterion at zero, `1 − 2/14 ≈ 0.857`. With the weight-4 criterion at zero, `1 − 4/14 ≈ 0.714`.
2. `S = (2.7 + 0.8 + 1.8 + 1.8 + 1.8 + 0.9) / 12 = 9.8 / 12 ≈ 0.817`. `G = 0.9^(10/12) × 0.4^(2/12) = exp((10 ln 0.9 + 2 ln 0.4) / 12) = exp((−1.054 − 1.833) / 12) = exp(−0.2406) ≈ 0.786`. Beta exposure has no gate, so plan C still passes the gates, now with a lower score than B. The geometric score would stop it at the 0.8 line.
3. Plan A with the low-end platform at 0.1: `G ≈ 0.825`, above 0.8, and a platform that reaches a tenth of its target. Any criterion with a small weight can sit near zero with little effect on `G`, because it enters as the `w/W`-th root.

</details>

## 3. Presenting a launch plan

MMO404 week 14 gave you the structure for a technical case study: facts, model results and judgment kept apart, each assumption bracketed, questions handled by naming what would change your answer. A launch plan presentation uses the same discipline, in an order set by the panel's question.

You have 12 minutes and 8 minutes of questions. Use this order.

1. **The decision (1 minute).** Your recommendation (go, go with conditions, or no-go) and the date. If conditions, list them.
2. **The gate table (2 minutes).** Every gated criterion, its measured score, its gate and the evidence. Put the one closest to its gate at the top, not the bottom. The panel will look for it anyway, and it is better that you show it than they find it.
3. **Capacity as a range (2 minutes).** Week 2's queue forecast at hours 1 to 6, as a range across session-length models, with the layers and head start that produce it. One number with no range invites the question "what if you are wrong?", and you will spend your question time on it.
4. **The tail (3 minutes).** Week 13's register, the disaster line, the exceedance curve for your chosen plan and for the expected-loss plan, and the rule you used to choose. Show both curves. The panel should see what you gave up.
5. **Triggers and roles (2 minutes).** The four triggers most likely to fire, each with its lead-time check, and the war room roles by name.
6. **The lesson you borrowed (1 minute).** One lesson from your post-mortem analysis and the line of the plan it changed. This links the two halves of the assessment.
7. **What would change your recommendation (1 minute).** The one assumption, if wrong, that turns go into no-go. MMO404 week 14 called this bracketing. Here it is the last slide because it is the panel's first question.

Three presentation habits matter more for a launch plan than for a case study.

- **Numbers with their unit and source on the slide.** "Queue 750 to 1,125 per world at hour 3 (lab 2, three session models)" can be checked. "Manageable queues" cannot.
- **Show the red.** A plan with every criterion green looks untested. The panel trusts a plan more when you show where it is weak and what you did about it.
- **Say who decides.** For every trigger and every condition, a role owns the call. A plan where "the team" decides is a plan where no one does.

## 4. Presenting a post-mortem analysis

The second half of the assessment is an analysis of a published case, from weeks 4 to 11 or from the reading list of Game Developer post-mortems. [Week 12](w12-writing-a-post-mortem.md) covered how to write a post-mortem of your own. Reading someone else's is a different skill, because the authors chose what to tell you.

Structure the 8-minute analysis in four parts.

1. **What happened, with dates (2 minutes).** A timeline from sources, cited with dates and versions. Keep facts and interpretation separate, as MMO404 week 14 requires.
2. **The model that explains it (3 minutes).** Pick one model from this program and rewrite the case in its terms: week 1's narrowest stage, week 2's cumulative curves, week 3's beta exposure, week 13's register, MMO308 week 13's revert-or-fix, or, for a shutdown, MMO308 week 14's forecast or MMO301 week 13's empty-shard spiral. Show which parameter moved and by roughly how much. If you cannot find a parameter that moved, you have a story, not an analysis.
3. **What the team could have seen, and when (2 minutes).** The evidence that existed before the failure, and the gate or trigger that would have acted on it. Be fair. Judge the decision by what was known then, the blameless rule from MMO308 week 13.
4. **The transferable lesson (1 minute).** A lesson transfers if it changes a number or a rule in a launch plan for a different game. "Test more" does not transfer. "Gate every platform you sell on, with a measured score" does. So does "treat the shoulder, not the spike, as the capacity target".

A good test is to state the lesson as a row in your own scorecard or register. If it fits as a criterion with a weight or gate, or as a risk with a `p` and an `I`, it transfers. If it does not fit anywhere, rewrite it until it does.

## 5. The panel, and how you are assessed

The panel's rubric is built the way section 2 recommends. It has gates first, then weighted points.

**Gates (a presentation that fails one is returned for resubmission within a week, and its marks are capped at 50):**

- The capacity numbers reproduce from your lab 2 code when the panel runs it.
- Every real-game fact on a slide has a source with a date or version.
- The plan has a disaster line agreed before costing, and states the rule used to choose mitigations.
- The post-mortem analysis uses a model and names a parameter that moved.

**Weighted criteria (100 points):** the launch plan's content (40), the post-mortem analysis (25), the link between them (10), the handling of questions (15) and the clarity of the slides (10). The detailed descriptors are in the [launch plan brief](../assessments/launch-plan-brief.md).

Peer panellists use the same sheet. Their job is to ask one question from each of these three kinds.

- **The gate question.** "Which gate is closest to failing, and what happens if it does?"
- **The tail question.** "What is the worst week this plan allows, and why is that acceptable?"
- **The transfer question.** "Which line of your plan would be different if you had not read your case?"

Groups that answer each with a number and a slide reference score well. Groups that answer with reassurance do not.

## In-class activity (30 minutes)

Run a mock readiness review in groups of three pairs. Each pair has its own launch plan.

1. **Score (10 minutes).** Each pair fills in the section 2 scorecard for its own plan, with a measured score and one line of evidence for each criterion. Write "no evidence" as 0.
2. **Review (15 minutes).** Pairs swap plans. The reviewing pair has 5 minutes to find the criterion closest to its gate, and 5 minutes to ask the gate, tail and transfer questions. The presenting pair answers without slides, then the pairs rotate once.
3. **Decide (5 minutes).** Each reviewing pair writes a verdict: go, go with conditions (listed as triggers), or no-go, with the rule that produced it.

Expected output: three filled scorecards, each with a weighted average, a geometric score and a gate result; three written verdicts; and, for each plan, the one criterion the reviewers would fix first. Keep the sheets. Revise your plan before your presentation slot.

## Common misconceptions

- **"A high overall score means the plan is ready."** A weighted average of 92% is compatible with one criterion at zero. Check the gates before you look at the total.
- **"The geometric mean solves that."** It solves a true zero. A criterion at 0.1 with a small weight barely moves it. Gates are the only rule that stops a failing criterion whatever its weight.
- **"Showing weaknesses loses marks."** Panels look for them. Hiding the weakest gate means the panel finds it during questions, where you have no slide to answer with.
- **"A lesson is anything the post-mortem authors said they learned."** Authors write lessons for their own next game. A lesson transfers to yours only if you can write it as a gate, a weight, a risk or a trigger in your own plan.

## Check yourself

1. A studio's scorecard has eight equally weighted criteria and launches at a weighted average of 0.85. What is the highest score a plan with one criterion at zero can reach? Could such a plan launch?
2. Using section 2's weights, a plan scores 0.8 on every criterion except the restore drill, which scores 0.5. Compute its weighted average and its geometric score, and say whether it passes the gates. What does a panel decide under each of the three rules?
3. You are designing a scorecard for an MMO that sells on PC and one console. Which of these would you make gates, and which weighted criteria: tested restore, console performance, launch trailer quality, trading kill switch, beta survey satisfaction? Justify each in one line.
4. A group's post-mortem analysis of a launch concludes "communicate better with players". Rewrite it as a transferable lesson in one of the forms from section 4.

<details>
<summary>Answers</summary>

1. `1 − 1/8 = 0.875`, above 0.85. A plan can launch with one criterion at zero if the others are perfect or near it. With two at zero, `1 − 2/8 = 0.75` and it cannot.
2. `S = (3 × 0.8 + 2 × 0.8 + 2 × 0.5 + 2 × 0.8 + 2 × 0.8 + 1 × 0.8) / 12 = 9.0 / 12 = 0.75`. `G = 0.8^(10/12) × 0.5^(2/12) = exp((10 ln 0.8 + 2 ln 0.5)/12) = exp((−2.231 − 1.386)/12) = exp(−0.3014) ≈ 0.740`. The restore drill's 0.5 is below its 0.7 gate. Average rule: no-go (0.75 is below 0.8). Geometric rule: no-go (0.74). Gates: no-go. All three agree here, because every score is mediocre, not one hidden zero.
3. Gates: tested restore (data loss is above any disaster line), console performance (you sell there, and Cyberpunk shows the cost), trading kill switch (containment for dupes, week 13). Weighted: launch trailer quality (affects demand, cannot sink the launch), beta survey satisfaction (useful, but a weak survey should not block a sound plan).
4. For example: "Post a status update on a fixed cadence (every 30 minutes during a SEV1) from launch minute 1, owned by the communications lead" as a trigger or gate, or "Communication plan with first-message drafts: gate 0.7, measured as the share of week 13 risks with a drafted message". Either can be scored and checked.

</details>

## Lab / assignment hook

[Lab 14, readiness review](../labs/lab14.md). You implement the three scoring rules and a gate report, score three invented launch plans and your own, compute the smallest score changes that flip each verdict, and run a timed dry run of your presentation with a peer panel. The final launch plan and post-mortem analysis are assessed in week 15.

## Sources

- Wikipedia, "Cyberpunk 2077" (read September 2026). Release on 10 December 2020 for PlayStation 4, Stadia, Windows and Xbox One; Metacritic scores of 86 (PC), 57 (PS4) and 61 (Xbox One); review copies for PC only; Sony's refunds and removal from the PlayStation Store in December 2020 "until further notice"; return in June 2021 with a warning against purchase for PS4; class actions from 24 December 2020 and a US$1.85 million settlement approved in January 2023.
- Consolegameswiki, "Item Level" (Final Fantasy XIV, current patches, read September 2026). Average item level as the sum over equipped slots divided by the number of slots; main-hand counted twice when no shield is equipped; minimum item level requirements for duties; advice to upgrade the weapon first to reach a minimum.
- Warcraft Wiki, "Item level" (retail World of Warcraft, read September 2026). Item level used as a gating requirement when queueing for dungeons, raids and scenarios; average item level shown on the character sheet.
- Wikipedia, "Launch commit criteria" (read September 2026). Criteria that must be satisfied before a countdown proceeds; examples that forbid launch (disturbed weather) and that delay it (a 15-minute hold on field mill readings).
- MMO404 week 14, MMO308 weeks 13 and 14, and MMO301 week 13 (this program) for presentation structure, blameless postmortems and shutdown models, with their sources.
- Scorecard criteria, weights, gates, plan scores and the panel rubric weights in sections 2 and 5 and the activity are teaching values. The authoritative rubric is the course's assessment brief.

## Interactive spec: examples/w14-readiness-gates.html

**The one insight:** a weighted average can rate a plan at 92% while one criterion sits at zero. The average gauge is green while the gate view shows a red row and a no-go verdict. The geometric score catches an exact zero and very little else.

**Layout (two linked views, stacked on mobile, side by side at 900px and wider):**

- View A, "the scorecard": a horizontal gauge from 0 to 1 for the weighted average `S`, with a launch line at the chosen threshold (default 0.8), coloured `--moss` above the line and `--ochre` below. Under it, one stacked bar of width `S`, split into segments of width `wᵢ sᵢ / W`, each labelled with the criterion; a dotted outline shows each criterion's full `wᵢ / W` so a missing segment is visible as an empty outline. Readout of `G` beside the gauge.
- View B, "the gates": one row per criterion, a bar for `sᵢ` from 0 to 1, a notch at `gᵢ` for gated rows ("no gate" label otherwise). A row whose score is below its gate is drawn in `--blood` with the text "below gate". At the top, a verdict: "go" (all gates pass and `S` above the line), "no-go: N gate(s) failed", or "no-go: score below line".
- Below both, a comparison table of the three rules for plans A, B and C and the custom plan: `S`, `G`, gates passed, verdict under each rule.

**Controls:**

- Plan selector: A, B, C, custom (default A).
- For each of the six criteria: score slider (0 to 1, step 0.05), weight stepper (0 to 5, step 1), gate toggle and gate value (0 to 1, step 0.05). Defaults from the lecture tables.
- Launch threshold for `S` and `G` (0.5 to 1, step 0.01, default 0.8).
- "Missing evidence" checkbox per criterion that forces its score to 0 and labels the row "no evidence".

**Readout (always visible, `aria-live="polite"`):** `S`, `G`, `1 − wₖ/W` for the lowest-scoring criterion `k`, number of failed gates, and the verdict under each rule.

**Formulas:**

```
W = Σ wᵢ
S = Σ wᵢ sᵢ / W
G = Π sᵢ^(wᵢ / W)          (G = 0 if any sᵢ = 0 with wᵢ > 0)
gates pass ⇔ sᵢ ≥ gᵢ for every gated i
verdict (average rule)   = go if S ≥ threshold
verdict (geometric rule) = go if G ≥ threshold
verdict (gated rule)     = go if gates pass and S ≥ threshold
```

**Test values (must match):**

- Weights 3, 2, 2, 2, 2, 1; gates 0.7 on capacity, restore drill, kill switches, low-end platform.
- Plan A (1, 1, 1, 1, 1, 0): `S = 0.917`, `G = 0.000`, 1 gate failed (low-end platform). Average rule go, geometric no-go, gated no-go.
- Plan A with low-end at 0.1: `S = 0.925`, `G = 0.825`, gate failed; average go, geometric go, gated no-go.
- Plan A with low-end weight 3 (`W = 14`): `S = 11/14 = 0.786`, below 0.8.
- Plan B (0.85 × 6): `S = 0.850`, `G = 0.850`, all gates pass, go under every rule.
- Plan C (0.9, 0.7, 0.9, 0.9, 0.9, 0.9): `S = 0.867`, `G = 0.863`, go under every rule.
- Plan C with beta 0.4: `S = 0.817`, `G = 0.786`; average go, geometric no-go, gated go.
- All 0.8 except restore drill 0.5: `S = 0.750`, `G = 0.740`, restore gate failed; no-go under every rule.

**First screen:** plan A loaded. Caption: "91.7% ready. One criterion has nothing in it. Should this launch?"

**Accessibility:** all controls keyboard operable with visible focus; every slider labelled with criterion name and current value; readout in `aria-live="polite"`; verdict colours paired with text so colour is never the only signal; respects `prefers-reduced-motion` and `prefers-color-scheme`; tokens from `templates/interactive-tokens.css` inline. Generic shapes only, no game art or logos.
