# MMO402 · Week 06 — Moderation at Scale

**Why this matters:** A popular online game gets more reports in a day than a team of humans could read in a month. So someone has to decide which reports a machine acts on alone, which ones a person reads, and which ones nobody ever looks at. Those thresholds are the real moderation policy, whatever the code of conduct says. If you set them without doing the arithmetic, the queue will set them for you.

**You will be able to:**
- Compute the reviewer hours a report volume needs and the growth of a backlog when inflow exceeds capacity.
- Design a three-tier triage (automatic action, human review, dismissal) from score bands and a staffing budget, and compute its correct actions, wrong actions and missed violations.
- Read a platform transparency report and turn its figures into daily volumes, automation shares and appeal outcomes.
- Critique a moderation plan for its hidden costs: wait times, wrong punishments, missed harm, report abuse and moderator exposure.

**Before class:** Microsoft, *Xbox Platform and Game Studios Transparency Report, January to December 2025*, the "Sharing our safety data" section (about 20 minutes). Gillespie, T. (2018), *Custodians of the Internet*, chapter 4 ("Three imperfect solutions to the problem of scale"). Reread MMO305 week 9, section 2, on the precision of punishment.

**Prerequisites from earlier courses:** [MMO305 week 9, toxicity research and interventions](../../MMO305-social-systems-and-online-behaviour/lectures/w09-toxicity-research-and-interventions.md) (precision and false-positive rate of a detection system; the League of Legends Tribunal). [MMO305 week 8, griefing](../../MMO305-social-systems-and-online-behaviour/lectures/w08-griefing-typology-and-design-responses.md) (what is being reported). [MA102 week 14, hypothesis testing](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w14-intro-to-hypothesis-testing-ab.md) (false positives and false negatives as a trade-off). [GD102 week 2, stocks and flows](../../GD102-systems-design-and-game-mechanics/lectures/w02-stocks-and-flows.md) (a backlog is a stock). This course: [week 4, wars, betrayals and meta-gaming](w04-wars-betrayals-and-meta-gaming.md) (what counts as a violation) and [week 5, rules and terms of service](w05-rules-eulas-and-terms-of-service.md) (the published rules moderation enforces). Next: [week 7, justice systems](w07-justice-systems-reports-reviews-appeals.md).

**Interactive:** [w06-moderation-queue.html](../examples/w06-moderation-queue.html)

---

## 1. What "at scale" changes

**Content moderation** is the work of finding and acting on behavior and content that break a platform's rules: chat, voice, names, images, cheating, scams. In a small game, moderation looks like justice. A game master reads a report, looks at the logs, decides, and maybe talks to both players. At scale it looks like logistics.

Four terms are used throughout this lecture.

- **Reactive moderation** starts from a player report. **Proactive moderation** starts from the platform's own scanning, such as filters on names and chat, or cheat detection.
- A **score** is a number, usually between 0 and 1, that an automated system assigns to a report or a piece of content. It estimates how likely the item is to break the rules. Real scores are imperfect, and they are more useful when they are **calibrated**, meaning that items scored around 0.8 turn out to break the rules about 80% of the time.
- **Triage** means sorting cases by urgency and certainty before anyone handles them, as in an emergency department.
- **Throughput** is how many cases a team can close per day. **Backlog** is the stock of cases waiting.

MMO305 week 9 gave you the precision formula. If a detection system flags a group in which violations are rare, even a small false-positive rate produces many wrong punishments. This week adds the constraint MMO305 left out, which is capacity. You cannot fix precision by "having a human check" if the humans cannot keep up.

## 2. Worked example: who reads 107,000 reports a day?

### The hook

Microsoft's transparency report for Xbox covers the whole of 2025. Players filed 39 million reports that year, which is about 107,000 a day. Only 9.6% of those reports, 3.7 million, led to a restriction on content or an account. Microsoft says 65% of user reports and 97% of all reports were processed by automated systems. It handled more than 332,000 appeals and reinstated 26% of the accounts that appealed, about 85,000 of them.

Now try it with people. Suppose a moderator needs 1.5 minutes per report and gets 7 productive hours a day. Reading every Xbox report would take

```
107,000 × 1.5 / 60 ≈ 2,675 moderator-hours per day
2,675 / 7 ≈ 382 moderators working every single day
```

That is before voice clips, cheating cases that take far longer than 1.5 minutes, and appeals. It also ignores the proactive side. Microsoft scanned 14.8 billion pieces of content in 2025, about 40 million a day. No human team reads that.

So every large platform triages. The question is how to set the triage, and what it costs.

### The model

Reports arrive at `Q` per day. An automated system gives each report a score, and the team picks two thresholds on it.

- Scores at or above `h` get **automatic action**, with no human involved.
- Scores from `l` up to `h` go to **human review**.
- Scores below `l` are **dismissed** with no action. In practice these may be logged, counted toward repeat-report patterns, or sampled for quality checks.

The team's review capacity is

```
C = M × H × 60 / a
```

- `M` is the number of moderators on shift per day.
- `H` is productive hours per moderator per day.
- `a` is the average handling time per report, in minutes.

If the review tier receives `q_r` reports a day, the backlog changes by `q_r − C` each day. When `q_r > C`, the backlog after `d` days is `d × (q_r − C)`, and a new report waits about `backlog / C` days.

The outcomes depend on how many true violations land in each tier. Assume, for now, that human reviewers decide correctly. Then:

```
correct actions   = violations in auto tier + violations in review tier (if reviewed)
wrong actions     = non-violations in auto tier
missed violations = violations in dismiss tier + violations stuck in the backlog
```

Three numbers, and you can only trade them against each other. Lowering `h` sends more cases to automatic action, which raises wrong actions. Raising `l` sends more to dismissal, which raises misses. Widening the review band, between `l` and `h`, is limited by `C`.

### Numbers you can check

Take a mid-sized game with `Q = 100,000` reports a day, 10% of which are real violations (close to Xbox's 9.6% action rate). Its classifier sorts reports into four score bands.

| Band | Score range | Reports per day | Share violating | Violations | Non-violations |
|---|---|---|---|---|---|
| A | 0.9 and above | 6,000 | 90% | 5,400 | 600 |
| B | 0.5 to 0.9 | 8,000 | 40% | 3,200 | 4,800 |
| C | 0.2 to 0.5 | 16,000 | 5% | 800 | 15,200 |
| D | below 0.2 | 70,000 | about 0.9% | 600 | 69,400 |
| Total | | 100,000 | 10% | 10,000 | 90,000 |

The team has `M = 40` moderators, `H = 7` hours and `a = 1.5` minutes, so `C = 40 × 7 × 60 / 1.5 = 11,200` reviews per day.

Now compare five policies. Each row is one choice of thresholds.

| Policy | Auto-act | Review | Dismiss | Review load vs `C` | Correct actions/day | Wrong actions/day | Missed/day |
|---|---|---|---|---|---|---|---|
| 1. Humans review everything | — | A-D | — | 100,000 vs 11,200 | about 1,120 (10% of the 11,200 reviewed) | 0 | Most; the backlog grows by 88,800/day |
| 2. Auto A, review B and C | A | B, C | D | 24,000 vs 11,200 | about 7,270 (5,400 + 4,000 × 11,200 / 24,000) | 600 | 600 in D, plus violations stuck in a backlog growing by 12,800/day |
| 3. Auto A, review B | A | B | C, D | 8,000 vs 11,200 | 8,600 | 600 | 1,400 |
| 4. Auto A and B | A, B | — | C, D | 0 | 8,600 | 5,400 | 1,400 |
| 5. Policy 3, plus spare capacity on the top of C | A | B, part of C | rest | 11,200 vs 11,200 | at least 8,760 | 600 | at most 1,240 |

Work through the rows.

**Policy 1** looks the most careful. After a week the backlog is `7 × 88,800 = 621,600` reports, and a new report waits `621,600 / 11,200 ≈ 55` days. By then the offender has moved on, and the victim has learned that reporting does nothing. "Humans check everything" turns into "nobody checks anything in time".

**Policy 2** fails more slowly. The backlog grows by 12,800 a day. After 30 days it holds 384,000 reports, a wait of about 34 days.

**Policy 3** is stable. The team has 3,200 spare reviews a day. It catches `5,400 + 3,200 = 8,600` of 10,000 violations (86%). It wrongly acts on 600 players a day, and it misses the 1,400 violations in bands C and D.

**Policy 4** removes the humans entirely and catches the same 8,600 violations. But it wrongly punishes 5,400 players a day. Its precision is `8,600 / 14,000 = 61%`, so nearly two in five actions hit someone innocent.

**Policy 5** spends Policy 3's spare 3,200 reviews on the highest-scored reports in band C. Even if violations were spread evenly through the band, that catches `3,200 × 5% = 160` more. With a calibrated score they are concentrated at the top of the band, so the true gain is larger.

Policy 3 at 600 wrong actions a day adds up to 219,000 wrong actions a year. That is the same order of magnitude as the 332,000 appeals Xbox handled in 2025. Wrong actions do not disappear. They come back as appeals, support tickets and players who quit.

### The visual

Open the interactive. The left view, "Where reports go", is a flow diagram from the four bands to three tiers and then to outcomes (correct, wrong, missed, waiting), with widths in reports per day. The right view, "The queue", plots the backlog over 30 days. Drag `h` and `l`, or the number of moderators.

Watch the right view as you widen the review band. As long as the review load stays under `C`, the backlog line lies flat on zero. Push the load a few percent above `C` and the line starts to climb, and it never comes back. Now try to reduce wrong actions by raising `h`. The left view shows wrong actions falling, and the right view shows the queue taking off, because every case you take away from the machine lands on a person.

### The insight

The thresholds are the policy. A code of conduct says what is forbidden. The pair `(h, l)` and the staffing level decide what is actually enforced, how fast, and at whose expense. A team that has not chosen them explicitly has chosen them anyway, through whatever the queue does.

The model also shows the three-way trade in its sharpest form. Once capacity is fixed, you can buy fewer wrong punishments only with more missed harm or longer waits. You can escape the trade only by changing its terms: more moderators (raise `C`), faster tools (lower `a`), a better classifier (purer bands), or fewer reports to begin with (design that prevents harm, MMO305 week 9).

### Cross-game and cross-context recognition

**Xbox (2025 transparency report).** Rewrite the published numbers in the model's terms. `Q ≈ 107,000` user reports a day. The actioned share is 9.6%, so roughly one report in ten is a real violation, a base rate close to our example's. The 97% automation share for all reports means almost everything sits in the automatic tiers. The 26% reinstatement rate on appeals is a measure of wrong actions, but only among players who appealed. It is not the error rate of the whole system (see misconceptions). The report also notes that automation reduces how often human moderators are exposed to sensitive content, a cost the throughput model does not count.

**League of Legends, the Tribunal (early 2010s).** Riot raised `C` by recruiting players as reviewers. Reported cases went to a crowd that voted on punishment. Blackburn and Kwak (2014) studied more than 10 million reports about 1.46 million reported players. They trained a classifier to predict the crowd's verdicts, and it did well on clear-cut cases. In model terms, the crowd widened the review tier, and the classifier offered a way to move the clearest cases into the automatic tier and save reviewer time. MMO305 week 9 discusses what this did to toxicity. Here, notice that it is the same triage with a different workforce.

**Emergency-department triage.** A hospital sorts arrivals into "treat now", "wait for a doctor" and "send home with advice". The three tiers, the capacity limit and the trade between waiting and wrong sorting are the same. Hospitals also re-triage patients who wait too long, a lesson moderation queues can copy.

**Spam filtering in email.** Mail is delivered, sent to a spam folder that the user may check, or rejected outright. The spam folder is a review tier staffed by the recipient, and its capacity is the recipient's patience.

### Eyes-open design judgment

- **Choose the thresholds by harm type, not globally.** A wrong automatic mute for profanity costs little and is easy to undo. A wrong permanent ban for cheating costs a player years of progress. Use a high `h` or no automatic tier at all for severe penalties, and a low `h` for light, reversible ones.
- **Make automatic actions light and reversible.** Policy 4's 5,400 daily wrong actions are a disaster as bans and a nuisance as 10-minute chat restrictions. The penalty ladder is part of the triage.
- **Staff for the peak, not the average.** Launches, free weekends and major updates bring spikes in reports. A queue that sits at 90% of `C` on a normal day overflows at the first spike. Plan for surge capacity or a surge policy, such as temporarily raising `l`.
- **Audit the dismiss tier.** Band D in the example hid 600 real violations a day. Sample it every week, or you will never learn what your filter misses.
- **Count appeals as part of the cost.** Every wrong action is a future appeal. Week 7 builds the justice system that handles them.

## 3. What throughput leaves out

The model counts cases. Four problems do not show up in the counts.

### Consistency

Two moderators given the same case should reach the same decision. The share of cases on which reviewers agree, corrected for chance, is called **inter-rater agreement**. Low agreement means a player's outcome depends on who opened the ticket, which players experience as arbitrary. Common remedies include written decision guides with examples, calibration sessions where the team rules on the same cases and compares, and second reviews for severe penalties. Each of these lowers throughput, because it raises `a`.

### Context and language

Scores and reviewers both struggle with context. Banter between friends can look like harassment. Slang shifts faster than filters update. A reviewer who does not speak the language cannot judge the report. Global games need moderators, or at least classifiers, for every major language community, and the band shares in the example will differ by region.

### Report abuse

Reports are a tool, and tools get misused. Groups can mass-report a player they dislike, trying to push that player's score past `h`. The defenses are to score reports rather than simply count them. Weight each reporter by their past accuracy, discount reports from the same group or match, and never let the number of reports alone trigger an automatic penalty.

### The moderators

Reviewing harmful content hurts the people who do it. Throughput targets that push `a` down push exposure per hour up. Automation that takes the most graphic material out of human queues is a welfare measure as well as an efficiency measure. Staffing plans should include rotation, support and limits on exposure, and those plans raise the real cost of `C`.

## 4. Proactive moderation and the base rate

Proactive scanning faces the base-rate problem from MMO305 week 9 at an enormous scale. Xbox scanned 14.8 billion items in 2025 and found 2.5% of them in violation, 368 million. That is a much lower base rate than the roughly 10% among player reports, because players report things they have already judged to be bad. Reports are a pre-filtered stream.

Apply MMO305's formula with the Xbox base rate. A scanner with 90% recall and a 1% false-positive rate, run on 2.5% prevalence, has precision

```
0.9 × 0.025 / (0.9 × 0.025 + 0.01 × 0.975) = 0.0225 / 0.03225 ≈ 70%
```

At 40 million items a day, that 1% false-positive rate touches about 390,000 innocent items a day. This is why proactive systems mostly block or hide content, which is cheap to reverse, rather than penalizing accounts. The penalty ladder carries the ethical weight that the classifier cannot.

## In-class activity (25 minutes)

Groups of four. Your MMO launches next month. Community estimates: 30,000 reports a day at launch, falling to 12,000 after a month. A vendor classifier gives the band table below. Your budget is 12 moderators on 7-hour days, and a report takes 2 minutes on average.

| Band | Share of reports | Share violating |
|---|---|---|
| High (0.85 and above) | 5% | 85% |
| Middle (0.4 to 0.85) | 15% | 35% |
| Low (below 0.4) | 80% | 2% |

1. Compute `C` (3 minutes).
2. Choose thresholds for launch week and for month two. For each, compute review load, correct actions, wrong actions and misses per day (12 minutes).
3. Write the penalty that automatic actions will carry, and say why it is reversible (5 minutes).
4. Name the one thing you would spend money on first: moderators, tooling to lower `a`, or a better classifier. Justify it with a number from step 2 (5 minutes).

Expected output: `C = 2,520`, two threshold plans with their numbers, one penalty rule and one investment with its number.

## Common misconceptions

- **"If a human checks every case, moderation is fair."** Only if the humans keep up. Policy 1 in the example makes new reports wait 55 days after one week. Late justice for the victim is lost justice, and it teaches players that reporting does nothing.
- **"A 26% appeal reinstatement rate means the system is wrong 26% of the time."** It measures errors among players who appealed. Those who were rightly punished appeal less often, and some wrongly punished players never appeal, so the rate is neither the system's overall error rate nor a bound on it.
- **"Automation is the risky part; humans are the safe part."** Humans disagree with each other, get tired and misread context. Automation is consistent but blind to context. Match each to the cases it handles best, and measure both.
- **"More reports mean more toxicity."** Report volume also rises with player count, with how easy reporting is, and with report abuse. Track the actioned share and the share of matches with a confirmed violation, not raw reports.

## Check yourself

1. A game receives 50,000 reports a day. Moderators handle a report in 2 minutes and work 6 productive hours. How many moderators does reviewing every report need?
2. With the band table from section 2 and `C = 11,200`, a manager proposes auto-acting on band A and reviewing all of band C instead of band B, "because band C is where the hidden cases are". Compute review load, correct actions, wrong actions and misses. Is the queue stable?
3. A review tier receives 9,000 reports a day and `C = 8,500`. What is the backlog after 20 days, and how long does a new report wait?
4. A proactive name filter runs on 200,000 new names a day. 1% are offensive. The filter has 95% recall and a 0.5% false-positive rate. How many acceptable names does it block each day, and what is its precision?
5. Your team can either hire 10 more moderators (raising `C` from 11,200 to 14,000) or buy a tool that cuts `a` from 1.5 to 1.2 minutes. Which raises `C` more?

<details>
<summary>Answers</summary>

1. Hours needed `= 50,000 × 2 / 60 ≈ 1,667`. Divide by 6 hours per moderator, giving about 278 moderators a day.
2. Review load is 16,000, which is more than 11,200, so the queue is not stable. It grows by 4,800 a day. While it keeps up, humans can review 11,200 band-C reports and catch about `11,200 × 5% = 560` violations. Correct actions per day are therefore about `5,400 + 560 = 5,960`, against 8,600 under Policy 3. Wrong actions stay at 600, and band B's 3,200 violations are now missed. It is worse on every count.
3. The backlog grows by 500 a day, so after 20 days it holds 10,000. The wait is `10,000 / 8,500 ≈ 1.2` days, and it keeps growing.
4. Acceptable names are `198,000`, so wrong blocks `= 0.005 × 198,000 = 990` a day. True blocks `= 0.95 × 2,000 = 1,900`. Precision `= 1,900 / 2,890 ≈ 66%`.
5. The hires give 14,000. The tool gives `40 × 7 × 60 / 1.2 = 14,000`. They are equal. Compare costs, and note that the tool keeps helping as the team grows.

</details>

## Lab / assignment hook

[Lab 06, triage the queue](../labs/lab06.md). You get one day of 2,000 scored reports with ground-truth labels and handling times. Your job is to choose thresholds under a 720-minute review budget and a limit on wrong automatic actions, plot precision and recall, and write a one-page moderation policy that states your thresholds, penalty ladder and audit plan. It counts toward the case analyses (30%).

## Sources

- Microsoft. *Xbox Platform and Game Studios Transparency Report*, covering January to December 2025. https://www.xbox.com/en-US/legal/xbox-transparency-report (accessed September 2026). 39M player reports, 9.6% (3.7M) leading to restrictions; 65% of user reports and 97% of total reports processed with automation; 14.8B items proactively scanned, 2.5% (368M) violating; more than 332K appeals with a 26% reinstatement rate (85K); automation to reduce moderators' exposure to sensitive content.
- Blackburn, J. & Kwak, H. (2014). "STFU NOOB! Predicting Crowdsourced Decisions on Toxic Behavior in Online Games." *Proceedings of the 23rd International World Wide Web Conference (WWW 2014)*. arXiv:1404.5905. The League of Legends Tribunal as a two-stage crowdsourced system; more than 10 million reports on 1.46 million players; a classifier predicting crowd decisions to cut cost.
- Gillespie, T. (2018). *Custodians of the Internet: Platforms, Content Moderation, and the Hidden Decisions That Shape Social Media*. Yale University Press. Chapter 4.
- The band table, staffing and the policies in section 2 and the in-class activity are constructed for teaching. They are not data from any company.

## Interactive spec: examples/w06-moderation-queue.html

**The one insight:** once review capacity is fixed, thresholds trade wrong punishments against missed harm and waiting time. Any review load above capacity makes the backlog grow without limit, so "have a human check it" fails unless the numbers add up.

**Layout.** Controls at the top, then two linked views, side by side on desktop and stacked on mobile ("Where reports go" first).

- **Controls.** Reports per day `Q`: 10,000 to 200,000, default 100,000. Auto-action tier: checkboxes for bands A, B, C, D (default A). Review tier: checkboxes (default B). Any band in neither tier is dismissed. A band may not be in both tiers; checking one unchecks the other. "Spend spare capacity on the next band down" toggle (default off). Moderators `M`: 0 to 200, default 40. Hours `H`: 4 to 8, default 7. Handling time `a`: 0.5 to 5 minutes, step 0.1, default 1.5. Preset buttons "Policy 1" to "Policy 5" from the lecture.
- **Left view, "Where reports go".** A three-column flow: bands (A-D, heights by reports) to tiers (auto, review, dismiss) to outcomes (correct action, wrong action, missed, waiting in backlog). Each flow labelled with its count per day. Colours come from the shared palette, and every flow also carries a text label.
- **Right view, "The queue".** Backlog (reports) against day 0 to 30. A horizontal reference line at zero. Label at day 30 with backlog and wait in days. If the review load is at or below `C`, the line stays at 0 and the label reads "Stable, spare capacity N per day".
- **Readout table** (copyable): `C`, review load, correct/day, wrong/day, missed/day (day-one value, excluding backlog), precision of all actions, backlog at day 7 and day 30, wait at day 30.

**Band data (share of Q, share violating).** A: 6%, 90%. B: 8%, 40%. C: 16%, 5%. D: 70%, 600/70,000 = 0.857%.

**Formulas.**

```
C = M × H × 60 / a
for each band b: n_b = Q × share_b; v_b = n_b × viol_b
load = Σ n_b over review bands
reviewed_today = min(load, C)
correct = Σ v_b (auto) + Σ v_b (review) × reviewed_today / load   // proportional when overloaded
wrong = Σ (n_b − v_b) over auto bands
missed = Σ v_b over dismissed bands
backlog(d) = max(0, d × (load − C))
wait(d) = backlog(d) / C  (days)
if spare toggle and load < C: take (C − load) reports from the highest dismissed band,
   caught_extra = (C − load) × viol_of_that_band, add to correct, subtract from missed
precision = correct / (correct + wrong)
```

**Test values** (Q = 100,000, M = 40, H = 7, a = 1.5, so C = 11,200).

- Policy 3 (auto A, review B): load 8,000, stable, spare 3,200; correct 8,600, wrong 600, missed 1,400; precision 93.5%.
- Policy 4 (auto A and B): load 0; correct 8,600, wrong 5,400, missed 1,400; precision 61.4%.
- Policy 2 (auto A, review B and C): load 24,000; correct 7,266.7 (show 7,267); wrong 600; backlog day 7 = 89,600, day 30 = 384,000; wait at day 30 = 34.3 days.
- Policy 1 (review all): load 100,000; backlog day 7 = 621,600; wait at day 7 = 55.5 days.
- Policy 5 (Policy 3 plus spare on C): correct 8,760, missed 1,240.
- a = 1.2 with Policy 3: C = 14,000.

**Accessibility.** All controls keyboard-operable with visible focus and text values; flows and lines carry text labels, not colour alone; the readout table is a real table; `prefers-reduced-motion` disables flow animation. No game logos or art.
