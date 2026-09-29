# PR402 · Week 14 — Post-mortem: What Your Launched Game Can Teach the Next Team

**Why this matters:** The post-mortem is 20% of this course, and it is the last document your team writes together. It is also the first post-mortem you have written about a game that real players used for weeks. You have more evidence than in any earlier project: sprint records, a patch sized from your own track record, a live ledger, incident logs, a cohort table. A good post-mortem uses that evidence to test what the team believes it learned. A weak one lists what hurt. This week you do the first kind.

**You will be able to:**
- Compute your team's estimate ratio and commitment rate for every sprint and the patch, and test the claim "we got better at planning" against them.
- Build a plan-against-actual table for dates and scope, from the PR401 production plan to launch and the patch.
- Compute the recurrence and closure rates of the lessons from your PR401 pre-production review, and write this project's lessons as action items someone can check.
- Assemble a launch post-mortem that follows the structure from MMO407 week 12 and passes the blameless standard.

**Before class:** Collect every production record from this course in one folder: sprint boards with estimates and actuals, labs 11 to 13, the patch release record, incident postmortems, the cohort table and the economy review. Find your PR401 pre-production review and its action items. Reread MMO407 week 12, sections 3 and 4, on the anatomy of a launch post-mortem and the biases that spoil it (25 minutes), and PR101 week 14, sections 3 and 4, on blameless writing and recurrence (20 minutes).

**Prerequisites from earlier courses:** [PR101 week 9, jam post-mortem](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w09-jam-post-mortem.md) (your first post-mortem and the cone of uncertainty). [PR101 week 14, post-mortems as a practice](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w14-post-mortems-as-a-practice.md) (Pareto coding, blameless writing, action items, the recurrence rate `R = |C1 ∩ C2| / |C1|`, all used here without re-teaching). [PR101 week 6, estimation and why it fails](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w06-estimation-and-why-it-fails.md) (the estimate ratio). [MMO407 week 12, writing a post-mortem](../../MMO407-launch-scaling-and-post-mortems/lectures/w12-writing-a-post-mortem.md) (the launch post-mortem, the contrast ratio, survivorship and hindsight bias). [MMO308 week 13, incident response](../../MMO308-live-operations-analytics-and-experimentation/lectures/w13-incident-response.md) (incident postmortems, which feed the timeline). [MMO403 week 14, pitching to publishers and investors](../../MMO403-business-monetization-and-ethics-of-live-games/lectures/w14-pitching-to-publishers-and-investors.md) (the showcase in week 15 is partly a pitch for what the game could become). From this course, [week 12](w12-patch.md) (the patch forecast tested below) and [week 13](w13-economy-review.md).

---

## 1. What this post-mortem is for

MMO407 week 12 separated two documents. An **incident postmortem** covers one event. A **project post-mortem** covers a whole project and is written for the next one. This week's document is the second kind, with a launch section inside it. It covers your project from the PR401 production plan to the end of week 13.

It has two readers. The first is the next team, which could be you, on your first job. The second is the instructor, who marks it against the rubric in the assessment brief. Both want the same thing: claims tied to evidence, and lessons someone can act on.

Two biases from MMO407 week 12 will pull at you. **Hindsight bias** makes the causes of what happened look obvious now, so the post-mortem says "we should have known". **Survivorship** means you only see what went wrong on your project, with nothing to compare it against, so everything that hurt looks like a lesson. The worked example shows one way to push back. Use your own records to test a lesson before you write it down.

## 2. The evidence you already have

Most teams arrive at the post-mortem with memories and a few screenshots. You have more than that, if you kept the course's worksheets.

- **Sprint records.** Estimated and actual hours, items committed and delivered, for sprints 1 to 4 and the patch.
- **Milestone dates.** Planned in PR401, actual in this course.
- **The scope list.** The PR401 production plan's feature list against what shipped at launch and in the patch.
- **Labs 11 to 13.** Interrupt hours, queue waits, the patch budget and forecast, the economy table and decision.
- **Incident postmortems.** One per SEV1 or SEV2 incident since launch, with timelines.
- **The cohort table.** Retention by install day, with incident dates marked.
- **The PR401 pre-production review.** Its "what went wrong" list and action items.

A claim in your post-mortem should point at one of these. "Our estimates improved" points at the sprint records. "The economy inflated" points at lab 13. "Players liked the patch" points at, for example, the tutorial D1 before and after, from the week 12 expected-number list.

## 3. Worked example: did we get better at planning?

### The hook

In 1994, Roger Buehler, Dale Griffin and Michael Ross asked 37 psychology students to predict when they would finish their senior honours thesis. The average prediction was 33.9 days. The average actual time was 55.5 days, a ratio of about 1.64. Only about 30% finished by the date they had predicted. The researchers also asked for a pessimistic estimate, "if everything goes as poorly as it possibly could". The average pessimistic estimate was 48.6 days, still a week short of what actually happened.

The students were not new to their own work habits. They had written papers before. They still planned from the best case. The study gave the effect its name, the **planning fallacy**, and PR101 week 14 noted that underestimation is among the most-cited root causes in published game post-mortems.

Almost every student post-mortem says "we got better at planning over the project". It is the easiest lesson to claim and one of the hardest to check without data. You have the data.

### The model

For each sprint `k`, from the sprint board:

```
r_k = A_k / E_k            estimate ratio: actual hours over estimated hours for committed items
q_k = D_k / C_k            commitment rate: items delivered over items committed
```

If the team's hours are fixed and it works through the committed items at the real pace, it finishes about `E_k / A_k` of the planned work. So the model predicts:

```
q_k ≈ 1 / r_k
```

A team that improves at planning should show `r_k` falling toward 1, `q_k` rising toward 1, and the two tracking each other. If `q_k` rises while `r_k` does not fall, the team did not get better at estimating. It got better at committing less, which is also a skill, but a different lesson.

For a single forecast, the **forecast error** is `actual / predicted − 1`. Week 12 predicted the patch's actual hours using the four-sprint `R`. Now you can check that prediction.

### Numbers you can check

The Emberfall team's records, with one-week sprints as in [week 12](w12-patch.md):

| Sprint | Estimated `E` | Actual `A` | `r` | Committed `C` | Delivered `D` | `q` | `1 / r` |
|---|---|---|---|---|---|---|---|
| 1 | 36 | 54 | 1.50 | 18 | 11 | 61% | 67% |
| 2 | 39 | 54 | 1.38 | 17 | 12 | 71% | 72% |
| 3 | 35.5 | 46 | 1.30 | 16 | 12 | 75% | 77% |
| 4 | 33.5 | 40.5 | 1.21 | 14 | 12 | 86% | 83% |
| Patch | 39 | 50 | 1.28 | 6 | 6 | 100% | 78% |

Check sprint 3. `r = 46 / 35.5 = 1.296`. `q = 12 / 16 = 0.75`. `1 / r = 0.772`.

Read it in three steps.

**Sprints 1 to 4.** The ratio fell from 1.50 to 1.21 in four steps, and `q` rose from 61% to 86%. The two columns `q` and `1 / r` stay within 6 points of each other in every sprint. The team really did get better at estimating, and it shows up in delivery. Four points are a small sample, and part of the improvement may come from later sprints having more familiar work. Say so in the post-mortem. But the direction is clear, and it is supported by two independent measures.

**The patch.** Its ratio, 1.28, is worse than sprint 4's. Live bug fixing is harder to estimate than feature work, as week 12 predicted. Yet `q = 100%`, far above `1 / r = 78%`. That gap is the week 12 method at work. The team sized the patch with a 26% buffer, `b = 1 − 1/1.35`, so it committed only what fit after the ratio. The patch shows better commitment, not better estimation.

**The forecast.** Week 12 predicted `39 × 1.3507 = 52.7` actual hours. The patch took 50, a forecast error of `50 / 52.7 − 1 = −5.1%`. Had the team used sprint 4's ratio, 1.21, it would have predicted `39 × 40.5 / 33.5 = 47.1` and been 6.0% under. Both are close. The four-sprint ratio erred on the safe side, and the post-mortem can say so with a number.

The post-mortem line that follows from this is not "we got better at planning". It is two lines. "Our estimate ratio fell from 1.50 to 1.21 over four feature sprints, and delivery tracked it." And "for live work, we still underestimate by about 28%; sizing the patch with the four-sprint ratio delivered every item with 8 hours to spare."

This script reproduces the table and the forecast check. Run it with `.venv/bin/python`.

```python
rows = [("1", 36, 54, 18, 11), ("2", 39, 54, 17, 12), ("3", 35.5, 46, 16, 12),
        ("4", 33.5, 40.5, 14, 12), ("patch", 39, 50, 6, 6)]
for name, E, A, C, D in rows:
    r, q = A / E, D / C
    print(f"sprint {name:5} r={r:.3f}  q={q:.0%}  1/r={1 / r:.0%}  gap={q - 1 / r:+.0%}")
R4 = sum(A for _, E, A, _, _ in rows[:4]) / sum(E for _, E, A, _, _ in rows[:4])
for label, ratio in (("four-sprint R", R4), ("sprint 4 r", 40.5 / 33.5)):
    pred = 39 * ratio
    print(f"{label}: predicted {pred:.1f} h, actual 50 h, error {50 / pred - 1:+.1%}")
```

It prints:

```
sprint 1     r=1.500  q=61%  1/r=67%  gap=-6%
sprint 2     r=1.385  q=71%  1/r=72%  gap=-2%
sprint 3     r=1.296  q=75%  1/r=77%  gap=-2%
sprint 4     r=1.209  q=86%  1/r=83%  gap=+3%
sprint patch r=1.282  q=100%  1/r=78%  gap=+22%
four-sprint R: predicted 52.7 h, actual 50 h, error -5.1%
sprint 4 r: predicted 47.1 h, actual 50 h, error +6.0%
```

### Cross-game recognition

**Buehler, Griffin and Ross (1994).** The thesis students' average ratio of 1.64 sits just above your sprint 1 ratio of 1.50. Their pessimistic estimates, 1.43 times their ordinary predictions, were still short. A buffer set by feeling ("let's add some slack") is a pessimistic estimate. A buffer set from your own ratio is a measurement.

**Announced release dates.** PR101 week 6 scored The Last Guardian's announced date at a ratio of about 2.9 and Duke Nukem Forever's at about 10. Those are whole projects, where ratios compound across years. Your sprints are one-week slices of the same curve. The shape, heavy on the late side, is the same.

**Published post-mortems.** The Politowski dataset in PR101 week 14 lists underestimation among the ten most frequent root causes across 200 published game post-mortems. MMO407 week 12 warns that a problem found in many post-mortems is not automatically a lesson. Your table is the missing comparison for your own team. It shows whether underestimation shrank when you measured it.

### Eyes-open design judgment

- **Two measures beat one.** A falling ratio could come from padded estimates. A rising commitment rate could come from committing less. When both move together and `q ≈ 1 / r` holds, the improvement is real.
- **Say how small the sample is.** Five points cannot prove a trend. Write the direction, the numbers and the caveat. Do not write a percentage improvement as if it were a law.
- **Separate kinds of work.** Feature work and live work had different ratios. A single project-wide ratio (here 1.35 over everything) would hide the difference, and the next team would plan live work too tightly.
- **The measure changes behaviour.** Once the team knew its ratio was tracked, estimates may have been padded. Check whether the estimates for similar items grew over time before crediting the improvement to skill.

### Check this example

1. A team's sprint records show `r` = 1.4, 1.4, 1.4, 1.4 and `q` = 70%, 80%, 90%, 100%. What did they get better at?
2. For Emberfall, what fraction of the patch's committed items would you expect to deliver if the patch had been planned with all 64 estimated hours of the first draft?
3. Why is "we got better at planning" a weaker post-mortem line than the two lines in the example, even if it is true?

<details>
<summary>Answers</summary>

1. Not estimating: the ratio never moved. They got better at committing, sizing each sprint to fit after the ratio. Report it as that. It is a real skill, and the next team can copy it.
2. With `A = 58.3` hours and `64 × 1.35 = 86.4` needed, about `58.3 / 86.4 = 67%` of the estimated work, so roughly two-thirds of the items, and very likely not the event, which was the largest.
3. It cannot be checked, it gives the next team nothing to do, and it hides the difference between feature and live work. The two lines state measured values that the next team can use to size its own plans.

</details>

## 4. Plan against actual

MMO407 week 12 made the **plan-against-actual table** the spine of a launch post-mortem. Build two.

**Dates.** One row per milestone from the PR401 production plan: planned week, actual week, and a one-line reason for any slip. Emberfall's shows alpha in week 4 as planned, closed beta in week 5 as planned but a day late after the week 4 no-go, and open beta, launch and the patch all on their planned weeks (8, 9 and 12). The lost day came out of the closed beta's first day, not out of any later milestone.

**Scope.** Every feature in the PR401 plan, marked shipped at launch, shipped in the patch, or cut, plus every unplanned item that shipped. Emberfall planned 30 features for launch. It shipped 21 (70%), cut 9, and shipped 7 items that were in no plan: a login queue, a kill switch, the in-client bug report button and a chat rate limiter before launch, and the watchdog, the alert rule and the item-loss fix after it. Every one of the 7 was operations tooling or a live fix. The PR401 plan had no line for any of them.

That last fact is the kind of lesson a plan-against-actual table finds and memory misses. It turns into a specific action: the next production plan budgets operations tooling as a feature, sized from lab 11's interrupt hours.

## 5. Lessons, recurrence and action items

Code this project's "what went wrong" items into categories with the PR101 week 14 method, then compare them with your PR401 pre-production review.

Emberfall's PR401 review had six categories: scope, planning, communication, tools, testing and documentation. The team closed four action items (a cut list, a ratio-based buffer from sprint 2, a daily stand-up, a regression checklist). The tools and documentation items were never made checkable. This project's list has tools, documentation, planning and operations.

The recurrence rate is `3 / 6 = 50%` (tools, documentation, planning), and the closure rate is `4 / 6 = 67%`. The two open items both came back, as PR101 week 14 would predict. Planning came back even though its action item was closed. The worked example explains why: the buffer fixed feature sprints, but live work had its own ratio. That is a better lesson than "planning was hard again". Operations is new, and it is the lesson from section 4.

Every lesson ends in at most one action item with an owner, a change and a check. Write them for the team you will be on next, not for a team that no longer exists.

## Studio session plan

The studio meeting runs 180 minutes with one break.

| Time | Activity | Output |
|---|---|---|
| 0:00-0:15 | Instructor briefing: evidence before lessons; `r`, `q` and `1 / r`; the two plan-against-actual tables | Notes |
| 0:15-0:55 | Fill the sprint table and the forecast check from your boards (lab 14, part A) | Sprint table |
| 0:55-1:25 | Build the date and scope plan-against-actual tables (part B) | Two tables |
| 1:25-1:35 | Break | |
| 1:35-2:05 | Code "what went wrong" items; compute recurrence and closure against PR401 (part C) | Coded list, rates |
| 2:05-2:35 | Pair critique with another team: each reads the other's three lessons and asks "what evidence, and what would have to be true for this to be wrong?" | Critique notes |
| 2:35-3:00 | Write action items; assign sections of the final document; instructor sign-off on the outline | Outline and owners |

## Deliverables

Due at the week 15 showcase, in `production/postmortem/` in the team repository, as part of the post-mortem assessment (20% of the course).

1. **Lab 14 worksheet**, parts A to D. Checked by recomputing two sprint rows and the forecast error.
2. **The post-mortem document**, at the length set in the post-mortem assessment brief, with the sections of MMO407 week 12 section 3: summary, plan-against-actual tables, timeline with incidents, contributing factors, lessons graded by evidence, and action items. Checked against the assessment brief's rubric.
3. **Individual reflection** per student, as the assessment brief sets it, on one decision you made and what the evidence now says about it. Checked for a specific decision and a specific piece of evidence.

## Common failure modes

- **A diary instead of a post-mortem.** A chronological account of feelings. Start from the tables, then explain them.
- **Lessons with no evidence.** "Communication improved" with nothing behind it. Point at a record or cut the line.
- **Blame.** "The back-end lead was slow." Rewrite blamelessly, per PR101 week 14: what in the process let the delay go unseen?
- **One ratio for everything.** Mixing feature and live work hides the lesson the next team most needs.
- **Hindsight.** "We should have known the economy would inflate." Did lab 13's data exist when you designed the rewards? If not, the lesson is about monitoring, not foresight.
- **Action items without owners or checks.** They will not close, and they will come back.

## Review checklist

The instructor checks, at the week 15 showcase:

- [ ] The sprint table covers every sprint and the patch with `E`, `A`, `r`, `C`, `D`, `q`, and two rows recompute.
- [ ] The week-12 patch forecast is checked against the actual hours, with the error stated.
- [ ] The date and scope plan-against-actual tables start from the PR401 plan and list every unplanned item.
- [ ] Recurrence and closure rates are computed against the PR401 review, and every recurring item is discussed.
- [ ] Every lesson cites a record from section 2 of the guide and states how small the sample is where it matters.
- [ ] The document is blameless and passes one random line-by-line check.
- [ ] Every action item has one owner, a change and a check.

## Sources

- Buehler, R., Griffin, D. & Ross, M. (1994). "Exploring the 'planning fallacy': Why people underestimate their task completion times." *Journal of Personality and Social Psychology* 67(3), 366-381. Study 1: 37 students; average predicted thesis completion 33.9 days against 55.5 actual; about 30% finished by their predicted time; average pessimistic estimate 48.6 days. Figures as summarised in the Wikipedia article "Planning fallacy" (read September 2026).
- Politowski, C., Petrillo, F., Ullmann, G. C. & Guéhéneuc, Y.-G. "Game Industry Problems: An Extensive Analysis of the Gray Literature." arXiv:2009.02440v3 (2020, revised 2021). Underestimation among the top ten root causes across 200 post-mortems, as used in PR101 week 14.
- The Emberfall team's sprint records, scope counts and review categories are a constructed example for teaching. They are not data from any real team.
