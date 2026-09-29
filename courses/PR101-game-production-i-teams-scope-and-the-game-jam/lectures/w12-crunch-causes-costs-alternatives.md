# PR101 · Week 12 — Crunch: causes, costs, alternatives

**Why this matters:** In three weeks your team hits the final deadline, and someone will suggest pulling a few all-nighters. The game industry has done that for decades and called it crunch. This week you put numbers on what an extra hour of work actually buys when people are tired, and on when the bill arrives. Then you learn what to do instead, because "just don't crunch" is not a plan.

**You will be able to:**
- Compute week-by-week and cumulative output for a team working long hours under a fatigue-and-recovery model, and find the week where crunch falls behind a normal schedule.
- Explain, using the model and the historical output-hours data, why crunch looks effective at the deadline and costs more after it.
- Identify the production causes of a crunch (fixed dates, optimistic estimates, missing cut lists, scope growth) in a post-mortem and name the earlier decision that would have prevented it.
- Design a recovery plan for a late project that uses scope cuts, date moves and a bounded overtime policy, and defend it with numbers.

**Before class:** Clinton Keith, *Agile Game Development: Build, Play, Repeat* (2nd ed., 2020), chapter 1, "The Crisis Facing Game Development", and chapter 9, "Agile Release Planning". John Pencavel, "The Productivity of Working Hours", IZA Discussion Paper 8129 (2014), sections I to III (about 15 pages; skip the regression tables if you have not met them yet). Pick one post-mortem from the Game Developer post-mortem archive that mentions overtime and note what caused it.

**Prerequisites from earlier courses:** [GD102 week 2, stocks and flows](../../GD102-systems-design-and-game-mechanics/lectures/w02-stocks-and-flows.md) (a stock that drains and refills, which is what the model does to a team's energy). From this course, [week 4, scope and cut lists](w04-scope-mvp-vertical-slice-cut-lists.md) (the main alternative to crunch), [week 10, bug tracking](w10-bug-tracking-and-qa-basics.md) (the regression rate `r`, which fatigue raises) and [week 11, communication and conflict](w11-communication-and-conflict-in-teams.md) (the working agreement, where your overtime policy goes). [Week 6 on estimation](w06-estimation-and-why-it-fails.md) explains why the plans that lead to crunch are usually optimistic.

**Interactive:** [w12-crunch-ledger.html](../examples/w12-crunch-ledger.html). Keep it open during section 2.

---

## 1. What crunch is, and how common it is

**Crunch** is a period of mandatory or expected overtime, usually in the weeks or months before a milestone or release. The word covers anything from a few late evenings to months of 60-hour weeks. Two features separate it from ordinary overtime. It is expected rather than chosen, and it is usually the result of a plan that was never going to fit in normal hours.

It is common. The International Game Developers Association's 2019 Developer Satisfaction Survey asked employed developers about their working hours:

- 41% said their job involves crunch time, down from 51% in the 2017 survey.
- A further 35% reported long or extended hours that they did not call crunch.
- 36% had been in crunch more than twice in the previous two years, and 42% said crunch was expected at their workplace.
- During crunch, 38% worked 50 to 59 hours a week, 19% worked 60 to 69, and 13% worked more than 70.
- Of employees who worked beyond normal hours, only 8% received paid overtime, and 34% received no extra compensation at all.

The survey is self-selected (people choose to answer), so treat the exact numbers with care. The pattern is clear, though. Crunch is a normal part of many developers' working lives, and most of them are not paid for the extra hours.

### Three well-documented cases

**EA Spouse (2004).** In November 2004 Erin Hoffman, writing anonymously as "EA Spouse", published an account of her partner's working hours at Electronic Arts, where crunch planned for a short final phase had become a standing requirement. The post spread widely. Class-action lawsuits over unpaid overtime followed, and EA settled them by 2006, reclassifying some developers as hourly workers eligible for overtime pay.

**Red Dead Redemption 2 (2018).** In an interview published by *Vulture* on 14 October 2018, Rockstar co-founder Dan Houser said the team had been working 100-hour weeks several times that year. The next day Rockstar clarified that this referred to four senior writers, Houser among them, for three weeks, and that the company would never expect or force any employee to work that long. On 23 October 2018 Kotaku published reporting based on interviews with 77 current and former employees. None described 100-hour weeks. Many described weeks of around 55 to 60 hours sustained for long periods, and pressure to work nights and weekends. The game was made by roughly 1,600 developers.

**Cyberpunk 2077 (2019-2020).** In June 2019 CD Projekt's leadership said crunch on Cyberpunk 2077 would be non-obligatory. On 29 September 2020, after two delays, the studio told its developers that six-day weeks were mandatory for the final stretch. The game moved once more, launched on 10 December 2020, and, as week 10 described, was pulled from the PlayStation Store eight days later over the state of its console versions.

Keep these cases in their lane. They show that crunch happens at large, successful, well-funded studios, and that the public account of it is often disputed. They do not by themselves prove that crunch made those games worse. For that argument you need a model and some data.

## 2. Worked example: the crunch ledger

### The hook

During the First World War, British munitions factories suspended their limits on working hours. Weeks of 70 to 90 hours were common for men, and Sunday work came back. The government's Health of Munition Workers Committee studied the results. Its reports concluded that longer hours did not produce more output except over short, isolated periods, and it noted that seven days of work produced only six days' output. In 2014 the economist John Pencavel reanalysed the committee's data on munitions workers. Below about 49 hours a week, output rose in proportion to hours. Above that, each extra hour added less, output peaked at about 63 hours, and output at 70 hours was little different from output at 56. A 48-hour, six-day week produced slightly more than a 70-hour, seven-day week.

That is one week at a time. Game crunch lasts for weeks or months, and tiredness carries over from one week to the next. So the question for your team is not only "does hour 55 produce anything?" It is also "what does week 6 of long hours do to week 7?"

### The model

Track two things for each week `w`. One is the hours worked, `h_w`. The other is the team's **efficiency**, `e_w`, the fraction of a fresh hour's work that one hour now produces. Fresh, rested people have `e = 1`.

```
output_w = h_w × e_w

if h_w > 40:   e_(w+1) = max(e_min, e_w − f × (h_w − 40))
otherwise:     e_(w+1) = min(1, e_w + g)
```

- `h_w` is hours per person in week `w`. 40 is the normal week.
- `e_w` is efficiency at the start of week `w`, starting at `e_1 = 1`.
- `f` is the **fatigue rate**: efficiency lost per overtime hour. With `f = 0.005`, one 60-hour week (20 overtime hours) costs 0.10 of efficiency.
- `g` is the **recovery rate**: efficiency regained per normal week, up to 1. With `g = 0.10`, it takes four normal weeks to recover from four 60-hour weeks.
- `e_min` is a floor, so the model never predicts zero output. Use 0.3.

Efficiency is a stock, like the gold in GD102 week 2. Overtime drains it, rest refills it, and the refill is slower than people assume. The model counts output in "fresh hours": 60 hours at `e = 0.9` produce 54 fresh hours of work.

The values of `f` and `g` are **teaching values**, not measurements. They are chosen to give round numbers and a shape consistent with the historical data, with returns that shrink with long hours, and a cost that lingers. You will vary them in the interactive and in the lab. The shape of the result survives a wide range of values. The exact week it crosses does not.

This model is also generous to crunch in one way. It counts every hour of the first crunch week at full value, while Pencavel's data says hours beyond about 49 already add less within a single week. The real picture is somewhat worse for long hours than the table below.

### Numbers you can check

A four-person team is behind. Its plan is four weeks at 60 hours per person, then back to 40. Compare with a team that stays at 40 throughout. Use `f = 0.005`, `g = 0.10`, `e_min = 0.3`. Output is per person, in fresh hours.

| Week | Hours | Efficiency | Output | Cumulative (crunch) | Cumulative (40 h) |
|---|---|---|---|---|---|
| 1 | 60 | 1.0 | 60 | 60 | 40 |
| 2 | 60 | 0.9 | 54 | 114 | 80 |
| 3 | 60 | 0.8 | 48 | 162 | 120 |
| 4 | 60 | 0.7 | 42 | 204 | 160 |
| 5 | 40 | 0.6 | 24 | 228 | 200 |
| 6 | 40 | 0.7 | 28 | 256 | 240 |
| 7 | 40 | 0.8 | 32 | 288 | 280 |
| 8 | 40 | 0.9 | 36 | 324 | 320 |
| 9 | 40 | 1.0 | 40 | 364 | 360 |
| 12 | 40 | 1.0 | 40 | 484 | 480 |

Check week 3. Efficiency starts at `1.0 − 0.1 − 0.1 = 0.8`, so `60 × 0.8 = 48`. After week 4, efficiency is 0.6, and week 5 at 40 hours produces only `40 × 0.6 = 24`.

Read the ledger from two dates.

**At the deadline (end of week 4)** crunch looks like a clear win: 204 fresh hours against 160, 27.5% more. If you only measure until the ship date, crunch works. This is why it keeps happening.

**At the end of week 12** the crunch team is 4 fresh hours ahead. Each person worked 80 extra hours and got 4 hours of output for them. Almost all of the week 4 lead went on weeks 5 to 8, when the team came back to normal hours and did not come back to normal output.

The cost did not disappear. It moved to after the deadline. In a studio, that is the launch patch, the next project and the people who quit. In your course, it is your other exams.

Now make the crunch longer:

| Crunch length at 60 h | Lead at end of crunch | Lead at week 12 |
|---|---|---|
| 4 weeks | +44 | +4 |
| 6 weeks | +30 | −54 |
| 8 weeks | −8 | −96 |

Longer crunch makes things worse in both columns. A six-week crunch still leads at its own deadline, but it ends the quarter 54 fresh hours behind. By eight weeks the crunch team is behind *before the deadline arrives*. Its lead peaked after week 4 and shrank from there, because every crunch week from week 5 on produces less than a normal week (`60 × 0.6 = 36 < 40`).

A general rule falls out. A crunch week beats a normal rested week only while `h × e > 40`. At 60 hours, that means while `e > 0.67`. With `f = 0.005` that is the first four weeks. Working longer each week, say 70 hours, does not help. It drains `e` faster (0.15 a week), and the fifth week of 70-hour weeks produces 28 fresh hours.

This code prints the tables above. Run it with `.venv/bin/python`:

```python
from itertools import accumulate

def ledger(hours, crunch_weeks, weeks=12, f=0.005, g=0.10, e_min=0.3):
    e, out = 1.0, []
    for w in range(1, weeks + 1):
        h = hours if w <= crunch_weeks else 40
        out.append(round(h * e, 2))
        e = max(e_min, e - f * (h - 40)) if h > 40 else min(1.0, e + g)
        e = round(e, 6)
    return out

out = ledger(60, 4)
print(out[:5], list(accumulate(out))[-1])
for cw in (4, 6, 8):
    cum = list(accumulate(ledger(60, cw)))
    print(cw, round(cum[cw - 1] - 40 * cw), round(cum[-1] - 480))
print(ledger(70, 5)[4])
```

It prints:

```
[60.0, 54.0, 48.0, 42.0, 24.0] 484.0
4 44 4
6 30 -54
8 -8 -96
28.0
```

Open the interactive. The top chart shows weekly output as bars for both schedules, with a line at 40. The bottom chart shows the two cumulative lines. Drag the crunch length from 0 to 12 weeks and watch the crunch line pull ahead, then fall back and cross. Drag the deadline marker and see how different the verdict looks depending on where you stop counting. Then set `g` to 0.05 and watch the hangover stretch.

### Cross-game recognition

**British munitions factories (1915-1918), via Pencavel.** Within a single week, output stops rising with hours in the mid-60s, and 70 hours produce little more than 56. The committee's reports added the carry-over effect this model captures, finding that long hours helped only over short, isolated periods. Same shape, measured on real output.

**Red Dead Redemption 2 (2018).** The disputed 100-hour figure drew the headlines, but the model is more concerned with what Kotaku's sources described: 55 to 60 hours sustained for a long time. In the model, 55-hour weeks drain 0.075 of efficiency per week. From the fifth week on, each one produces less than a rested 40-hour week. Long, moderate crunch is the version the ledger punishes most, because it never stops long enough for `g` to act.

**Your week 10 backlog.** Fatigue does not only cut output. It raises the regression rate `r`, the share of fixes that break something else. Week 10 showed that raising `r` from 0 to 0.25 pushed the zero-bug day out by five days, more than adding 25% fix capacity pulled it in. A team that crunches through the bug-fixing phase lowers its effective fix rate twice, through lower `e` and through higher `r`. This is one reason studios that crunch at the end often ship with more bugs than planned. Cyberpunk 2077's mandatory six-day weeks in late 2020 were followed by a launch with serious console problems. The model predicts that combination, though it cannot prove the link in that case.

### Eyes-open judgment

- **Short, rare, chosen and paid overtime is different.** One 50-hour week before a milestone, agreed by the team and followed by a normal week, costs little in this model (`e` drops to 0.95 and recovers the next week). The ledger argues against sustained crunch, not against ever staying late.
- **The model ignores people leaving.** Its worst cost is not in the table. Burned-out developers leave, and a studio loses their knowledge and pays to hire and train replacements. Week 1's ramp-up cost from Brooks applies to every replacement.
- **Output is not value.** Fresh hours spent on the wrong feature are worth nothing. Crunch often goes on features that should have been cut, which is the real failure. See section 3.
- **Parameters differ by person and task.** Mechanical work tolerates long hours better than design or debugging, which need a clear head. People with caring duties or health conditions have far less room. A team policy should protect them, not average them away.
- **"We are more passionate than factory workers."** Motivation raises the willingness to work long hours. It does not change the fact that tired people make more mistakes. The regression rate cares about sleep, not passion.

## 3. Why crunch happens: it is decided early

Crunch is almost never decided in the last month. The last month is when a much earlier decision comes due. Post-mortems name the same causes again and again.

**A fixed date with flexible scope assumptions.** The date is set by a holiday release, a platform launch or a publisher contract. The scope is set by the pitch. Nobody forces the two to agree until late. The honest version of this is week 4's cut list. Decide in advance which features go if you run out of time, so the date and the scope can meet.

**Optimistic estimates.** Week 6 showed that estimates are uncertain and usually low, especially early. A plan that assumes every task takes its best-case time will run over. If the plan has no buffer, the overrun becomes overtime.

**Scope growth.** A feature is added mid-project because it would be cool, a competitor has it, or a stakeholder asked. Each addition is small. Together they overflow the schedule. The defence is a rule. Anything added must come with something removed of the same size, logged in the decision log from week 11.

**Integration debt.** Parts built separately meet for the first time near the end and do not fit. Week 2's frequent merges and week 13's regular builds are anti-crunch tools, because they bring integration pain forward, while there is still time to deal with it.

**Culture and incentives.** "Shipping heroics" get praised in all-hands meetings. Overtime is unpaid, so it looks free to whoever sets the schedule. The survey figure that only 8% of employees working beyond normal hours received paid overtime matters here. If overtime cost the studio money, planners would budget for it and see its price. If it is unpaid, the cost lands on the developers and their health, where no budget shows it.

## 4. Alternatives: what to do when you are late

Every late project has four levers. Crunch is only one of them, and the ledger shows it is the weakest once you look past the deadline.

| Lever | What it costs | When to use it |
|---|---|---|
| Cut scope | Features, polish, content | First, and early. A cut in week 10 saves work; a cut in week 14 only saves the unfinished part. |
| Move the date | Money, marketing, sometimes a missed window | When the core game is not yet fun or stable, and the date can move. |
| Add people | Ramp-up and channels (week 1) | Only early, and only for separable work such as QA or content with clear specs. |
| Add hours | Efficiency, bugs, health, attrition | Short, bounded bursts before a hard, immovable date, followed by recovery. |

For your final project, a sensible policy has four parts. Write it into your working agreement from week 11.

1. **Cut first.** At every sprint review, compare remaining work (in hours, from your task board) against remaining capacity. If it does not fit, cut from the bottom of the cut list the same day.
2. **Bound overtime.** For example, no more than one 50-hour week per person in the last three weeks, never two in a row, and no all-nighters. The ledger says one such week costs almost nothing. The rule is there to keep it to one.
3. **Protect the recovery.** Plan the week after the deadline as a light week. For you, that is your other exams, and the model says that is when you will pay.
4. **Make overtime visible.** Log it in the contribution record from week 11. Hours that nobody sees cannot be planned around.

## In-class activity (25 min)

In your final-project team, with your task board open.

1. **Measure the gap (7 min).** Sum the estimates of all remaining tasks for the final game. Compute your remaining capacity: members × hours per week × weeks left. How big is the gap, in hours?
2. **Two plans (10 min).** Plan A closes the gap with overtime only. Use the interactive to find the hours and weeks it needs, and read off the ledger for the three weeks after the deadline. Plan B closes it with cuts from your week 4 cut list, and at most one 50-hour week per person. List exactly which features Plan B cuts.
3. **Choose (5 min).** Pick a plan and write two sentences defending it with numbers from step 2.
4. **Swap (3 min).** Give your plan to another team. They name one risk you missed.

Expected output: the gap in hours, both plans on one page, your choice with its two-sentence defence, and the other team's risk. This page is the start of lab 12.

## Common misconceptions

- **"Crunch works, we shipped on time."** Measured at the deadline, it can. Measured over the following weeks, sustained crunch loses output, because recovery takes longer than the crunch that caused it. Always ask when the counting stopped.
- **"Twice the hours means twice the work."** Even within one week, the munitions data shows output stops rising with hours in the 60s. Over several weeks, fatigue lowers output per hour further.
- **"We'll crunch now and rest after launch."** For a studio, after launch is the patch cycle and the next project. For you, it is exam week. The recovery weeks are already booked.
- **"The alternative to crunch is failing."** The alternative is cutting scope early, which feels like failing but produces a finished, smaller game. Week 4's cut list exists so that this decision is made calmly.

## Check yourself

1. Using the model with `f = 0.005`, `g = 0.10`, compute the output of a 50-hour week that follows two 60-hour weeks. What is efficiency at the start of the following week?
2. A team works 55-hour weeks. With `f = 0.005`, in which crunch week does their weekly output first fall below 40 fresh hours?
3. A producer says, "Our four-week crunch gave us 27% more output before the milestone, so it paid off." Using the ledger, write two sentences in reply.
4. Your team is 60 hours short with three weeks left. Four members, and your cut list has three features estimated at 25, 20 and 30 hours. Propose a plan that uses no more than one 50-hour week per person, and show that it closes the gap.

<details>
<summary>Answers</summary>

1. Efficiency after two 60-hour weeks is `1.0 − 0.1 − 0.1 = 0.8`. The 50-hour week produces `50 × 0.8 = 40` fresh hours, exactly one normal week's output for 10 extra hours. Efficiency next week is `0.8 − 0.005 × 10 = 0.75`.
2. Each 55-hour week drains `0.005 × 15 = 0.075`. Week `w` starts at `e = 1 − 0.075 (w − 1)`. Output `55 × e < 40` needs `e < 0.727`, so `0.075 (w − 1) > 0.273`, `w − 1 > 3.64`, `w = 5`. Check: week 5 has `e = 0.70`, output 38.5. Week 4 has `e = 0.775`, output 42.6.
3. The 27% is real at the end of week 4 (204 against 160). But the team then produces 24, 28, 32 and 36 in the next four weeks, and by week 12 the crunch has returned 4 fresh hours for 80 extra hours per person. The cost moved past the milestone, it did not vanish.
4. One option: one 50-hour week per person adds `4 × 10 = 40` hours on paper. At `e = 1` in the first overtime week it is worth about 40 fresh hours. Cut the 20-hour feature and the gap closes (`40 + 20 = 60`). A safer option cuts the 30-hour and 20-hour features (50 hours) and uses overtime only for the remaining 10. Either answer must state which features go and keep the overtime within the rule.

</details>

## Lab / assignment hook

[Lab 12, recovery plan](../labs/lab12.md). Your team takes its real remaining work for the final game, runs the ledger model on a crunch-only plan with the provided script, builds a cut-first alternative from the week 4 cut list, and adds a bounded overtime policy to the week 11 working agreement. Deliverable: the model output, the two plans, the chosen plan with a 400-word justification, and the updated agreement.

## Sources

- Pencavel, J. (2014). "The Productivity of Working Hours". IZA Discussion Paper 8129, April 2014. Munitions workers in Britain during the First World War; output proportional to hours below about 49 per week, maximum near 63 hours, 70 hours little different from 56; the 48-hour six-day week slightly above the 70-hour seven-day week; the Health of Munition Workers Committee's findings on Sunday work and long hours.
- International Game Developers Association (2019). *Developer Satisfaction Survey 2019: Summary Report* (November 2019). Crunch prevalence among employees (41%, against 51% in 2017), long hours not called crunch (35%), expected crunch (42%), hours during crunch, and compensation (8% paid overtime, 34% no extra compensation).
- Wikipedia, "Crunch (video games)" (accessed September 2026). EA Spouse (Erin Hoffman, 2004) and the resulting class actions settled by 2006.
- Wikipedia, "Development of Red Dead Redemption 2" (accessed September 2026). Houser's *Vulture* interview (14 October 2018), Rockstar's clarification (15 October 2018: four senior writers, three weeks), Kotaku's reporting (23 October 2018, 77 current and former employees, weeks around 55-60 hours), team size about 1,600.
- Wikipedia, "CD Projekt" and "Cyberpunk 2077" (accessed September 2026). The June 2019 non-obligatory crunch statement, mandatory six-day weeks reported 29 September 2020, release on 10 December 2020 and PlayStation Store removal on 18 December 2020.
- Beck, K. et al. (2001). "Principles behind the Agile Manifesto", agilemanifesto.org. Agile processes promote sustainable development at a pace the team can keep indefinitely.
- Keith, C. (2020). *Agile Game Development: Build, Play, Repeat* (2nd ed.). Addison-Wesley. Chapters 1 and 9.
- The fatigue and recovery model and its parameters `f`, `g` and `e_min` are this course's teaching model. They are chosen to match the qualitative shape of the historical data, not fitted to it.

## Interactive spec: examples/w12-crunch-ledger.html

**The one insight.** Crunch pulls ahead at the deadline and falls behind afterwards. The cumulative lines cross, and where you stop counting decides whether crunch looks like it worked.

**Layout.** Two stacked charts sharing one x-axis (weeks 1 to the horizon): top "Output each week", bottom "Total output so far". Controls to the right on desktop, below on mobile. A verdict line above the charts.

**Model (exact).**
- For `w = 1..W`: `h_w = H` if `w ≤ C` else 40.
- `output_w = h_w × e_w`, with `e_1 = 1`.
- If `h_w > 40`: `e_(w+1) = max(e_min, e_w − f × (h_w − 40))`; else `e_(w+1) = min(1, e_w + g)`.
- Baseline: 40 hours every week, `e = 1`, output 40 per week.
- Lead at week `w` = crunch cumulative − `40 × w`.
- Crossover week = first week after the lead has been positive in which the lead becomes ≤ 0 (display "none within horizon" if it never happens).
- Round displayed values to one decimal; compute in full precision (round efficiency to 6 decimals each step to avoid float drift).

**Top chart.** Paired bars per week: crunch schedule (primary color) and 40-hour baseline (neutral). Horizontal reference line at 40 labelled "a rested normal week". Bars from crunch weeks whose output falls below 40 get a warning outline. Small efficiency value printed above each crunch bar (e.g. "0.7").

**Bottom chart.** Two lines: cumulative crunch and cumulative baseline. Shade the area between them green where crunch leads and red where it trails. A draggable vertical deadline marker `D` (default at the end of crunch), labelled with the lead at that week. A second fixed marker at the horizon with the lead there.

**Controls.**
- Crunch hours per week `H`: slider 40 to 80, step 1, default 60.
- Crunch length `C`: slider 0 to 12 weeks, step 1, default 4.
- Fatigue rate `f`: slider 0 to 0.015, step 0.001, default 0.005.
- Recovery rate `g`: slider 0.02 to 0.30, step 0.01, default 0.10.
- Efficiency floor `e_min`: slider 0.1 to 0.8, step 0.05, default 0.3.
- Horizon `W`: segmented 8 / 12 / 16 / 24 weeks, default 12.
- Deadline `D`: slider 1 to `W`, default equal to `C` (clamped to at least 1); also draggable on the chart and keyboard-movable.
- Reset.

**Verdict line (live).** Example: "At the deadline (week 4) crunch leads by 44 fresh hours. By week 12 it leads by 4. Each extra hour returned 0.05 hours." The last figure is `lead at W / (C × (H − 40))`, shown only when `C > 0` and `H > 40`.

**Table (collapsible).** Columns Week, Hours, Efficiency, Output, Cumulative crunch, Cumulative baseline, Lead.

**Test values (must match exactly).**
- Defaults (`H = 60, C = 4, f = 0.005, g = 0.10, e_min = 0.3, W = 12`): outputs weeks 1-9 `60, 54, 48, 42, 24, 28, 32, 36, 40`; cumulative at week 4 = 204, at week 12 = 484; lead at deadline +44, at horizon +4.
- `C = 6`: lead at week 6 = +30, week 7 = +6 (286 vs 280), week 8 = −14 (306 vs 320), week 12 = −54; crossover week = 8.
- `C = 8`: lead at week 8 = −8, at week 12 = −96.
- `H = 70, C = 5`: week-5 output 28.
- `H = 50, C = 1`: week-1 output 50, week-2 output 38 (`e = 0.95`), week-3 output 40.

**Accessibility and behaviour.** All controls keyboard operable with visible values; the deadline marker is a focusable slider with arrow-key steps. The verdict line is an ARIA live region. Respect `prefers-reduced-motion` and `prefers-color-scheme`. Red and green shading must also differ in pattern or label ("ahead" / "behind") for colour-blind readers. Use `templates/interactive-tokens.css` inline. No game art or logos.
