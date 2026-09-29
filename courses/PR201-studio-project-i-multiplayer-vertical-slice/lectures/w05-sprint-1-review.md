# PR201 · Week 05 — Sprint 1 Review

**Why this matters:** Sprint 1 is the first time your plan meets measured data. You now know how many estimated hours your team actually finishes in a sprint, and that number is almost certainly lower than the one you planned with. The review is where you show what works on real machines, and then use the measurement to redraw the road to alpha. Teams that skip that second part find out in week 10.

**You will be able to:**
- Run a sprint review that demonstrates the sprint goal from a clean build on two machines, and record what the demo showed.
- Compute focus factor and estimate ratio from sprint 1, and explain what each one measures.
- Forecast how much estimated work sprints 2 and 3 will finish, with a range, and compute the gap to the alpha list.
- Close the gap with cuts made now and cuts triggered later, checking each against your pillars.

**Before class:** The Scrum Guide (November 2020), sections "Sprint Review" and "Sprint Retrospective" (about 10 minutes). [PR101 week 6](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w06-estimation-and-why-it-fails.md), sections 1 and 4 (estimate ratios and turning estimates into ranges). Bring the tagged `sprint-1` build, your daily log and your spike answers.

**Prerequisites from earlier courses:** [PR101 week 5](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w05-agile-and-scrum-adapted-for-games.md), section 5, for retrospectives that end in a decision. [PR101 week 4](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w04-scope-mvp-vertical-slice-cut-lists.md), section 5, for cut triggers. [PR101 week 14](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w14-post-mortems-as-a-practice.md) for blameless review. [GD101 week 7](../../GD101-introduction-to-game-design/lectures/w07-playtesting-observe-dont-explain.md) for watching a demo without explaining it.

**Interactive:** [Velocity forecast to alpha](../examples/w05-velocity-forecast.html), built from the spec at the end of this guide.

---

## 1. What a sprint review is, and what it isn't

The Scrum Guide describes the sprint review as a working session. The team shows what it finished, and the team and its stakeholders decide what to do next. It is capped at four hours for a one-month sprint. Yours gets about an hour of the studio session. The Guide asks for two things, inspecting the result and adapting the plan. Student teams usually do only the first.

The review is **not a presentation**. Slides about what you built are worth less than 30 seconds of the build running. It is also not a grade. The instructor is a stakeholder in the review, and the milestone rubric is applied separately against the review checklist below.

In this course a sprint review has four parts:

1. **The goal demo.** A team member who did not write the networking code runs the tagged build from a clean checkout on two lab machines and performs the sprint goal. Everyone watches. Nobody explains.
2. **What didn't get done.** Each carried-over task, how many hours remain, and why it was carried.
3. **The numbers.** Focus factor, estimate ratio and the forecast to alpha (section 2).
4. **The new plan.** Which cuts the team makes now, and which cuts are triggered by sprint 2's numbers.

The **retrospective** follows the review and is for the team alone. It looks at how the team worked, not at what it built, and it ends with one change the team will try in sprint 2.

## 2. Worked example: redrawing the road to alpha

### The hook

In 2017 the *Anthem* team built a demo in about six weeks for a visit from Patrick Söderlund, then a senior EA executive, according to Jason Schreier's 2019 *Kotaku* report as summarized on Wikipedia. A demo built for a review shows what a team can do with focus and a narrow target. It says little about the pace of normal production. A sprint review is meant to show the pace. The build you demo should be the build you made while working normally. The numbers you bring should describe that same sprint, including the parts that went badly.

### The model

From the sprint just finished, take the useful capacity `U` (available hours minus coordination, as in week 4), the estimated hours of tasks actually finished `E_done`, and the actual hours logged on those tasks `A_done`.

```
focus f  = E_done / U            estimated hours finished per useful hour
ratio r  = A_done / E_done       real hours per estimated hour on finished tasks
forecast = f × Σ U_s              estimate-hours the next sprints will finish
range    = forecast × (1 − β) … forecast × (1 + β)
gap      = remaining − forecast
```

- `U_s` is the useful capacity of each future sprint `s` before the milestone, from the team's availability.
- `remaining` is the estimated hours still on the milestone's list, re-estimated at the review, including carried-over tasks.
- `β` is the width of the range. With one sprint of data you have no measured spread. Use `β = 0.2` as a placeholder and replace it with the spread of your own `f` values after sprint 3.

`f` is sometimes called **velocity per hour**. Scrum doesn't define velocity. It comes from wider agile practice, such as Mike Cohn's *Agile Estimating and Planning* (2005). The forecast is in **estimate-hours**, the same unit as the backlog. That's the point. You compare the backlog's estimates with the rate at which your team burns estimates, and you never mix estimated and real hours in one sum.

### Numbers you can check

*Hollowmarch* sprint 1 from week 4: useful capacity `U = 75` hours (90 available minus 15 coordination). Tasks finished had estimates totalling `E_done = 43` hours. The team logged `A_done = 55` hours on them.

```
f = 43 / 75 = 0.573
r = 55 / 43 = 1.28
```

The team planned with `f = 0.7`. It achieved 0.573. Part of the difference is the estimate ratio: finished tasks took 28% longer than estimated. The rest is the 10 hours of discovered work and the time spent on tasks that were started and carried over.

Alpha is at week 10. Before it come sprint 2 (weeks 6 and 7) and sprint 3 (weeks 8 and 9). The artist's exam is over, so each has useful capacity `U = 6 × 16 − 15 = 81` hours. At the review the team re-estimated the alpha list: the 15 carried-over hours plus 105 hours of must-tier and early should-tier features, so `remaining = 120`.

| View | What it assumes | Hours available for the alpha list | Gap |
|---|---|---|---|
| Naive capacity | Every useful hour finishes an estimated hour | 162 | 42 to spare |
| Planned focus 0.7 | The week 4 plan was right | 113.4 | 6.6 short |
| Measured focus, mid | `f = 0.573` holds | 92.9 | 27.1 short |
| Measured focus, low | `f` 20% worse | 74.3 | 45.7 short |
| Measured focus, high | `f` 20% better | 111.5 | 8.5 short |

The naive row is the one teams use without thinking, and it says the team has 42 hours to spare. The measured row says they are 27 hours short. That 69-hour swing, from one division, is the most important number of the review.

### Closing the gap

The team closed the mid gap with cuts now and covered the low gap with cuts that fire only if sprint 2 comes in low. Each cut was checked against the week 2 pillar support.

| Cut | Hours | When | Pillar check |
|---|---|---|---|
| F1 tank taunt, moved to sprint 4 (after alpha) | 18 | Now | P1 support falls from 4 to 3 (telegraphs, revive, boss) |
| F4 boss second phase, moved to sprint 4 | 15 | Now | Boss keeps phase 1, so P1 and P2 keep their support |
| F7 revive, moved to sprint 4 | 12 | Trigger: sprint 2 finishes under 40 estimate-hours | P1 support would fall to 2 (telegraphs, boss) |

Cuts now total 33 hours, which covers the mid gap of 27.1. Now plus trigger total 45 hours. That is 0.7 short of the low gap of 45.7. Lab 05's `forecast.py` prints `FAIL` on exactly this plan. The team added a fourth line: loot rarity tiers reduced from four to two, 10 hours, same trigger, and P3 support unchanged because loot still drops. Now plus trigger is 55 hours, and the check passes.

"Moved to sprint 4" is a real cut for alpha, not a disguised promise. Sprint 4 (week 12) is polish, and these features would compete there with every bug found at alpha. Write them on the cut list with their player-loses line, exactly as in week 2. The term check below decides whether they can come back at all.

### Feeding the number back

Rerun lab 01's fit test with the measured focus in place of `1 − b = 0.7`. Plannable hours per person over the remaining sprints fall by the ratio `0.573 / 0.7 = 0.82`. If a discipline's load was 0.92 in week 1, it is now about 1.12. The week 1 bottleneck check is only as good as its focus number, and you have a better one now.

The same number reopens the week 2 scope sheet, and this is the step teams skip. Week 2 set plannable hours at `P = 0.7 × 445.5 = 312` and filled them: must 150 plus should 161 is 311. With the measured focus, the whole term holds `P' = 0.573 × 445.5 = 255` estimate-hours, so `room = 255 − 150 = 105` for a should tier of 161. The alpha forecast above only covers two sprints, so it can't show this gap. The term check can.

*Hollowmarch* closed it in two moves:

| Change to the scope sheet | Should tier (h) | Pillar check |
|---|---|---|
| Week 2 lock | 161 | P1 4, P2 3, P3 2 |
| F1 tank taunt and F4's second phase, already out of alpha, leave the slice (−18, −15) | 128 | P1 3, P2 3, P3 2 |
| F6 talent choice becomes fixed stat gains at each level, re-estimated from 35 to 10 hours (−25) | 103 | P1 3, P2 3, P3 2 (loot, levels) |

The should tier is 103 inside a room of 105, and `check_scope.py --plannable 255` prints `PASS`. The scope sheet now holds `150 + 103 = 253` estimate-hours, 58 fewer than in week 2. Week 9's release burn-up starts from this sheet, so keep the table. It is how a reader gets from week 2's 311 to week 9's baseline.

### The same idea elsewhere

**Weather forecasting.** A forecaster who predicts tomorrow from what happened today is using persistence, a baseline that is hard to beat for short horizons and poor for long ones. Velocity forecasting is a persistence forecast. It works well for the next two sprints and badly for the next ten. That is one reason to forecast only to the next milestone.

**The planning fallacy.** PR101 week 6 cited Buehler, Griffin and Ross (1994). Students predicted about 34 days for a thesis that took about 56, and their "worst case" of about 49 days was still too short. Planning with 0.7 and measuring 0.573 is the same pattern at sprint scale. The fix is also the same: plan from what happened, not from what you expect.

**Hofstadter's law.** It always takes longer than you expect, even when you take Hofstadter's law into account. The measured `f` is how you take it into account with a number instead of a joke.

### Eyes-open judgment

One sprint is a thin sample. Sprint 1 carried spikes and setup that sprint 2 won't, so `f` may rise. It also had a stable team and no playtest, and sprint 2 has both, so `f` may fall. The range exists because you don't know which. Commit to the mid forecast, pre-agree cuts for the low one, and don't plan anything on the high one.

Don't "fix" the number by inflating estimates. If a team doubles every estimate, `f` halves and the forecast is the same. What changes is that nobody trusts the backlog any more. The honest move is to keep estimating the way you did, and let `f` carry the correction.

Watch `r` separately from `f`. A high `r` means tasks take longer than estimated, which is an estimation problem. A low `f` with `r` near 1 means hours go somewhere other than tasks: meetings, setup, blocked time, unlogged work. That is a flow problem, and the retrospective should look for it. For *Hollowmarch*, `r = 1.28` explains most of the gap from 0.7 to 0.573, so the retrospective focuses on estimation.

### Check yourself

1. Sprint 2 finishes 38 estimate-hours with `U = 81`. Does the trigger fire? Compute the new `f` for sprint 2 alone and for sprints 1 and 2 pooled.
2. A team finishes 50 estimate-hours in sprint 1 with `U = 75`, and `r = 1.0`. Another finishes 50 with `r = 1.5`. Both have the same `f`. What would you tell each team to work on?

<details><summary>Answers</summary>

1. Yes, 38 is under 40, so revive and the rarity tiers move to sprint 4. Sprint 2 alone gives `f = 38 / 81 = 0.469`. Pooled, `f = (43 + 38) / (75 + 81) = 81 / 156 = 0.519`. Forecast sprint 3 from the pooled value: `0.519 × 81 = 42.1` estimate-hours.
2. Both have `f = 50 / 75 = 0.667`. The first team's tasks took exactly as long as estimated, so the missing third of their hours went to something other than tasks. Look at meetings, waiting and unlogged work. The second team spent `1.5 × 50 = 75` hours, all their useful time, on tasks that were estimated at 50. They lose no time to flow, but they underestimate by half. Work on splitting tasks and estimating from past actuals.

</details>

## 3. Running the demo

The goal demo follows a script so that it tests the build, not the presenter.

- The **driver** is someone who did not write the networking code. If they can't run it from the README, that is a finding.
- **Clean checkout** on a lab machine: clone, build with the documented command, run. If it takes more than 10 minutes, record why.
- **Two machines**, not two windows. One runs the server (or hosts), the other joins by IP address.
- **Perform the goal exactly as written.** Join, move on both, hit the enemy, see it die on both.
- **Then break it gently.** Leave and rejoin. Join a third client if the design allows it. Add 100 ms of delay with the lab's network conditioner (CS202 week 14) and try again. Record what happens. You are not fixing anything now.

A scribe writes every surprise on a card. Those cards feed the sprint 2 backlog and the risk register.

## 4. The retrospective

Timebox it to 30 minutes. Use one format for the whole semester so the team gets fast at it. A good default has three steps:

1. **Data** (10 minutes). The charts from week 4, `f` and `r`, the demo cards, and the day-6 decision. What happened, without blame. PR101 week 14 covers why blameless review finds more.
2. **One cause** (10 minutes). Pick the biggest single reason `f` was below plan. For *Hollowmarch* it was estimates. Networking tasks took 1.28 times their estimate, and all of the overrun was on tasks the estimator had never done before.
3. **One change** (10 minutes). A specific experiment for sprint 2 with a check. "Any task of a kind nobody on the team has done before gets a pair estimate and a 1.5 multiplier, and we compare `r` on those tasks at the sprint 2 review."

One change, not five. Five changes can't be evaluated, and they won't all happen.

## Studio session plan

| Time | Activity | Output |
|---|---|---|
| 0:00 to 0:40 | Goal demos. Each team has 8 minutes on two lab machines. Other teams watch one demo each and fill in a surprise card | Demo cards per team |
| 0:40 to 1:10 | Numbers. Each team computes `f`, `r`, the forecast range and the gap with `forecast.py` | Forecast table |
| 1:10 to 1:20 | Break | |
| 1:20 to 1:50 | New plan. Cuts now and trigger cuts, pillar check, cut list updated. Instructor visits each team for 5 minutes as a stakeholder | `forecast.py` at `PASS`, updated `features.csv` |
| 1:50 to 2:20 | Retrospective, team only | One change for sprint 2, written down |
| 2:20 to 3:00 | Sprint 2 planning, first pass. Carry-over and the R2 prediction spike go at the top | Draft sprint 2 backlog |

## Deliverables

By the end of the studio session:

- **Sprint 1 review note** (one page, from the lab 05 template): goal met or not, demo findings, carry-over, `f`, `r`, forecast range and gap.
- **Forecast files** (`sprint_result.csv`, `plan.csv`, `cuts.csv`) and the `forecast.py` output showing `PASS`.
- **Updated scope sheet** with the cuts and their player-loses lines, and `check_scope.py` still passing with the reduced tiers at `--plannable` set to your measured `f` times your useful hours for the term (the term check in section 2).
- **Retrospective record**: one cause and one change with its check.
- **Updated risk register**, with the demo surprises added as risks where they fit.

See [lab 05](../labs/lab05.md).

## Common failure modes

- **The slide review.** The team presents the sprint instead of running it. Fix: no slides, and the build runs first.
- **The author drives.** The one person who knows the build's quirks runs the demo, so the quirks stay hidden. Fix: someone else drives, from the README.
- **Carry-over as a footnote.** Unfinished tasks quietly join sprint 2 at their original estimates. Fix: re-estimate every carried task and count it in `remaining`.
- **Forecast with the planned focus.** The team uses 0.7 again because 0.573 "was a bad sprint". Fix: use the measured number. If sprint 2 is better, the forecast will say so.
- **Cuts that aren't cuts.** Features "moved to later" with no sprint, no trigger and no pillar check. Fix: every move names its sprint or trigger, and the scope checker still passes.

## Review checklist

- [ ] Goal demo run by a non-author, from a clean checkout, on two machines. Result recorded as met, partly met or not met.
- [ ] Carry-over tasks listed and re-estimated.
- [ ] `f` and `r` computed from logged data, with the method shown.
- [ ] Forecast to alpha with a range, and the gap for low, mid and high.
- [ ] Cuts now close the mid gap. Cuts now plus trigger cuts close the low gap. `forecast.py` passes.
- [ ] Every cut keeps every pillar at support 2 or more.
- [ ] The scope sheet passes `check_scope.py` at the measured focus for the whole term, not only the alpha list.
- [ ] Retrospective produced one change with a check for the sprint 2 review.
- [ ] Sprint 2 backlog starts with the deferred R2 spike, and every carried task is re-estimated and placed in it (week 6 shows how).

## Sources

- Schwaber, K. and Sutherland, J. (2020). *The Scrum Guide*, November 2020 edition. scrumguides.org. The Sprint Review as a working session to inspect the outcome and decide future adaptations, timeboxed to four hours for a one-month sprint; forecasting practices do not replace empiricism.
- Wikipedia, "Anthem (video game)" (accessed September 2026), summarizing Schreier, J., "How BioWare's Anthem Went Wrong", *Kotaku*, April 2019. The six-week demo for Patrick Söderlund's 2017 visit. As cited in PR101 week 5.
- Buehler, R., Griffin, D. and Ross, M. (1994). Exploring the "planning fallacy": why people underestimate their task completion times. *Journal of Personality and Social Psychology*, 67(3), 366-381. Figures (33.9 days predicted, 48.6 worst case, 55.5 actual) as summarized in Wikipedia, "Planning fallacy", and cited in PR101 week 6.
- Wikipedia, "Hofstadter's law" (accessed September 2026). From *Gödel, Escher, Bach* (1979).
- Cohn, M. (2005). *Agile Estimating and Planning*. Prentice Hall. Velocity-based release planning. As cited through Wikipedia, "Planning poker", in PR101 week 6.
- The *Hollowmarch* sprint data, capacities and cuts are invented for teaching. The ±20% range is a teaching placeholder, not a measured figure.

## Interactive spec: examples/w05-velocity-forecast.html

**Insight to make obvious:** planning with raw capacity hides the gap. The same backlog looks 42 hours early in capacity terms and 27 hours late in measured estimate-hours. The range, not the midpoint, decides how many cuts you pre-agree.

**Layout.** One horizontal bar chart per view, all on the same hours scale. Rows are "Naive capacity", "Planned focus", "Measured low", "Measured mid" and "Measured high". Each bar shows hours available for the milestone list. A vertical line marks `remaining`. The part of each bar short of the line is shaded as the gap, and the part beyond it as spare. Below it is a second strip, "cuts", with two stacked blocks: cuts now and trigger cuts, drawn from `remaining` leftwards, so students can see whether they reach the mid bar and the low bar.

**Model.**
- `f = E_done / U1`, `r = A_done / E_done`
- `future = Σ U_s` over the future sprints
- naive = `future`; planned = `f_plan × future`; mid = `f × future`; low = `mid × (1 − β)`; high = `mid × (1 + β)`
- gap for each view = `remaining − view`
- pass when `cuts_now ≥ gap_mid` and `cuts_now + cuts_trigger ≥ gap_low`

**Controls.**
- `U1` sprint 1 useful capacity (20 to 150, default 75)
- `E_done` (0 to `U1`, default 43) and `A_done` (0 to 200, default 55)
- Number of future sprints (1 to 5, default 2) and useful capacity per future sprint (20 to 150, default 81)
- `remaining` (0 to 300, default 120)
- `f_plan` (0.3 to 1.0, default 0.7)
- `β` (0 to 0.5, default 0.2)
- `cuts_now` (0 to 100, default 33) and `cuts_trigger` (0 to 100, default 12)

**Test values** (defaults): `f = 0.573`, `r = 1.28`; naive 162.0 (spare 42.0); planned 113.4 (gap 6.6); low 74.3 (gap 45.7); mid 92.9 (gap 27.1); high 111.5 (gap 8.5). Cuts now 33 covers mid. Now plus trigger 45 misses low by 0.7, so the page shows "not covered". Setting `cuts_trigger = 22` shows "covered" (55 ≥ 45.7).

**Display rules.** Show `f`, `r` and every bar's value and gap as text beside the chart, to one decimal. Colour gap and spare with the shared palette's warning and success tokens, and also label them with the words "short" and "spare" so colour is not the only cue. Keyboard-operable sliders, and a text table of the five views for screen readers.
