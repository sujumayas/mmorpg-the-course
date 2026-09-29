# MMO405 · Week 05 — Experiments and Quasi-Experiments

**Why this matters:** Many of the most important questions about online games can't be answered with an A/B test. You can't randomize a government's playtime law, an expansion that changes the whole world at once, or the end of a beta. Researchers still publish causal claims about all three. This week teaches you to tell which of those claims the design can support, and to build designs that can.

**You will be able to:**
- Name the threat to internal validity (history, maturation, selection, regression to the mean, instrumentation, attrition) behind a flawed before-and-after claim about an online game.
- Compute a difference-in-differences estimate from four group means and explain the parallel-trends assumption it rests on.
- Show with numbers how pooling treated and untreated players can hide or reverse an effect, and run a placebo test on pre-period data.
- Choose between a randomized experiment, difference-in-differences, an interrupted time series and a regression discontinuity for a given research question, and justify the choice.

**Before class:** Zendle, Flick, Gordon-Petrovskaya, Ballou, Xiao and Drachen (2023), "No evidence that Chinese playtime mandates reduced heavy gaming in one segment of the video games industry", *Nature Human Behaviour* 7, 1753-1766, read the introduction, methods and limitations (open access). Karhulahti, Huntington-Klein, Ballou and Ropovik (2026), the reply in *Collabra: Psychology* 12(1), read the abstract and the main argument. Choi, Cho, Lee, Kim and Park (2018), "Effect of the Online Game Shutdown Policy on Internet Use, Internet Addiction, and Sleeping Hours in Korean Adolescents", *Journal of Adolescent Health* 62(5), 548-555, read the abstract and methods.

**Prerequisites from earlier courses:** [MA102 week 14, hypothesis testing and A/B](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w14-intro-to-hypothesis-testing-ab.md) (the two-proportion test and power). [MMO308 week 5, A/B testing design](../../MMO308-live-operations-analytics-and-experimentation/lectures/w05-ab-testing-design.md) (units, triggering, clustering) and [week 6, statistics and pitfalls](../../MMO308-live-operations-analytics-and-experimentation/lectures/w06-ab-testing-statistics-and-pitfalls.md) (peeking, novelty effects). [MMO308 week 3, cohorts and retention curves](../../MMO308-live-operations-analytics-and-experimentation/lectures/w03-cohorts-and-retention-curves.md). [MMO402 week 12, research ethics in online worlds](../../MMO402-emergent-society-governance-and-ethics/lectures/w12-research-ethics-in-online-worlds.md) (Corrupted Blood, the Facebook experiment, and when product testing becomes research).

**Interactive:** [examples/w05-did-parallel-trends.html](../examples/w05-did-parallel-trends.html). Keep it open during section 2.

---

## 1. Why you can't always randomize

In MA102 week 14 and MMO308 weeks 5 and 6 you learned the randomized experiment: assign players to A or B by a coin (or a hash), and any difference in outcome beyond chance is caused by the change. Randomization works because it makes the two groups alike in everything, measured or not, except the change.

A **quasi-experiment** is a study that tries to estimate a causal effect without random assignment. You need one whenever randomization is impossible, unethical or too late:

- **Impossible.** A law applies to all minors in a country. An expansion changes one shared world for everyone. A server merge happens to a server, not to players on it.
- **Unethical.** You would not randomly assign players to harassment or to a spending trap to measure harm (MMO402 week 12).
- **Too late.** The change shipped last month and nobody held out a control group.

Without randomization, the question becomes: what else could explain the difference? Methodologists (Shadish, Cook and Campbell's standard text is the usual reference) name the common alternative explanations **threats to internal validity**. Learn them as a checklist, with a game version of each:

- **History.** Something else happened at the same time. Your guild-finder launched the same week as a holiday event, and logins rose for both reasons.
- **Maturation.** Players change over time anyway. New players' session length falls in their second month whether or not you patch anything (MMO308 week 3).
- **Selection.** The groups differed before the change. Players who opted into the new voice chat were already more social.
- **Regression to the mean.** You picked a group because it was extreme, and it drifted back. You fix the three servers with the worst toxicity reports this month, and next month their reports fall, as they would have partly done anyway.
- **Instrumentation.** The measurement changed. A client update changed how session end is logged, and "average session" jumped overnight.
- **Attrition.** Different players left the groups. After a difficulty patch, the frustrated players quit, and the remaining ones report higher satisfaction.

Every quasi-experimental design is a way of ruling some of these out. None rules out all of them. The skill is to know which ones your design handles and to say so.

## 2. Worked example: the policy that seemed to increase heavy play

### The hook

From 1 November 2019, Chinese regulation required online game providers to stop players under 18 from playing more than 1.5 hours a day (3 hours on public holidays) and from playing between 22:00 and 08:00. In September 2021 the rule tightened to a single hour, 20:00 to 21:00, on Fridays, weekends and public holidays. Did the 2019 rule reduce heavy play?

In 2023, Zendle and colleagues analyzed Unity Analytics telemetry from Chinese users between 16 August 2019 and 16 January 2020: more than a million game identifiers, 7.04 billion hours of play and about 2.4 billion player profiles, mostly from mobile games. They defined **heavy play** as more than 4 hours a day on 6 days a week. The share of weekly profiles playing heavily went *up*, from 0.77% before the rule to 0.88% after, an odds ratio of 1.14. The title of the paper says there was no evidence the mandates reduced heavy gaming.

Then look at the data's limits, which the authors reported themselves: the telemetry had no age information. The rule applied only to minors. Citing Tencent, the authors noted that minors produced only 6.4% of playtime on Tencent's games in China in September 2020. In 2026 Karhulahti, Huntington-Klein, Ballou and Ropovik published a reply in *Collabra: Psychology* arguing that, without age data, the study could not in principle identify the effect of a policy aimed at minors.

Who is right is a design question, and you can answer it with four numbers.

### The model

Split players into a **treated group** that the change applies to and a **comparison group** that it doesn't. Measure the outcome in both groups before and after. The **difference-in-differences (DiD)** estimate is:

```
δ = (Y_T,post − Y_T,pre) − (Y_C,post − Y_C,pre)
```

- `Y_T,pre` and `Y_T,post` are the treated group's average outcome before and after.
- `Y_C,pre` and `Y_C,post` are the comparison group's average outcome before and after.
- `δ` is the estimated effect of the change on the treated group.

The first bracket is the treated group's change, which mixes the effect with everything else that happened (history, maturation). The second bracket estimates "everything else" from a group that saw everything else but not the change. Subtracting removes it.

That subtraction is only valid under one assumption, **parallel trends**. Without the change, the treated group's outcome would have moved by the same amount as the comparison group's. The groups can start at different levels. They must not be heading in different directions.

### Numbers you can check

Here is an invented MMO, but a realistic one. It has players in the regulated country, and it knows which accounts belong to minors because the regulation requires identity checks. Minors are 10% of accounts. The outcome is the weekly share of accounts playing heavily, in percent. In the same week the rule starts, a winter expansion launches for everyone.

| Group | Before | After | Change |
|---|---|---|---|
| Minors (treated), 10% of accounts | 4.0 | 3.0 | −1.0 |
| Adults (comparison), 90% | 3.0 | 4.0 | +1.0 |
| All accounts pooled | 3.1 | 3.9 | +0.8 |

Three analysts look at this game.

- **Analyst 1 has no age data.** They see only the pooled row. Heavy play rose by 0.8 points, an odds ratio of about 1.27. "The policy failed, and maybe backfired."
- **Analyst 2 has age data but no comparison group.** They look at minors only. Heavy play fell by 1.0 point. "The policy worked a little."
- **Analyst 3 uses DiD.** `δ = (3.0 − 4.0) − (4.0 − 3.0) = −1.0 − 1.0 = −2.0` points. The expansion pushed everyone up by 1 point. Minors went down anyway. The policy's effect is twice what analyst 2 reported, and in the opposite direction from what analyst 1 reported.

In this invented case the policy halved minors' heavy play (from the 4.0 they would have reached without it, 5.0, to 3.0), and the pooled data still showed an increase. Nothing in the pooled row could reveal that. The same odds ratio arithmetic reproduces the published figure:

```python
share = {("minor", "pre"): 4.0, ("minor", "post"): 3.0,
         ("adult", "pre"): 3.0, ("adult", "post"): 4.0}
w = 0.10  # minors' share of accounts

def pooled(period):
    return w * share["minor", period] + (1 - w) * share["adult", period]

def odds_ratio(p_pre, p_post):
    return (p_post / (1 - p_post)) / (p_pre / (1 - p_pre))

pooled_change = pooled("post") - pooled("pre")
minor_change = share["minor", "post"] - share["minor", "pre"]
adult_change = share["adult", "post"] - share["adult", "pre"]
print(f"pooled:        {pooled('pre'):.1f} -> {pooled('post'):.1f}  change {pooled_change:+.1f}")
print(f"minors only:   change {minor_change:+.1f}")
print(f"diff-in-diff:  {minor_change - adult_change:+.1f}")
print(f"pooled odds ratio:  {odds_ratio(pooled('pre') / 100, pooled('post') / 100):.2f}")
print(f"Zendle et al. 0.77% -> 0.88%:  {odds_ratio(0.0077, 0.0088):.2f}")
```

It prints:

```
pooled:        3.1 -> 3.9  change +0.8
minors only:   change -1.0
diff-in-diff:  -2.0
pooled odds ratio:  1.27
Zendle et al. 0.77% -> 0.88%:  1.14
```

This does not show that the real 2019 rule worked. The invented numbers show only that pooled data *could not tell*, which is the reply's point. Zendle and colleagues addressed part of this in their paper. They discussed dilution by adults, used a within-person model on a subsample, and argued that an ineffective policy was still the most plausible reading. Read both papers and decide for yourself how much weight the finding can carry.

### A visual you can move

Open the interactive. The top panel shows what analyst 1 sees: one weekly line for all accounts, from eight weeks before the rule to eight weeks after, with the rule date marked. The bottom panel splits that line into minors and adults, and draws a dashed "counterfactual" line for minors: where they would have gone if they had followed the adults' trend.

Start with the defaults (minors 10%, expansion shock +1.0, policy effect −2.0, no pre-trend gap). The top line steps up. The bottom panel shows minors stepping down while adults step up. The gap between the minors' line and their dashed counterfactual is the effect. Now drag the "minors' share of accounts" slider down to 6%, near the Tencent figure. The pooled step barely changes. Drag the policy effect to zero and back. The pooled line hardly notices, while the bottom panel changes completely.

Then break the assumption. Set "extra pre-trend for minors" to +0.25 points per week. The minors' line now rises faster than the adults' line even before the rule. The DiD readout moves away from the true effect by exactly `4 × 0.25 = 1.0` point, because each side of the comparison averages four weeks. The **placebo test** readout, a DiD computed only on pre-rule weeks (weeks −8 to −5 against −4 to −1), jumps from 0 to 1.0. A placebo estimate far from zero is your warning that trends were not parallel.

### Cross-game recognition

**Korea's shutdown law (2011).** From November 2011, South Korea blocked players aged 15 and under from online games between midnight and 6 a.m. Choi and colleagues (2018) used the national Korea Youth Risk Behavior Web-based Survey for 2011 to 2015, with about 142,000 respondents aged 15 or below and about 102,000 aged 16 or above. They used a DiD with exactly our structure: treated = 15 and under, comparison = 16 and over, outcome = daily internet use in minutes. The estimate was −3.6 minutes in 2012, −3.2 in 2013, −1.1 in 2014 (not significant) and +2.2 in 2015 (not significant). The policy did not change internet addiction scores or sleep. Rewritten in our form, `δ_2012 = (Δ ≤15) − (Δ ≥16) = −3.648 minutes`. The comparison group carries the parallel-trends assumption. Ask yourself whether 16- and 17-year-olds, heading into university entrance exams, are a good stand-in for younger teenagers.

**ArcheAge's closed beta wipe (2011-2012).** Kang, Blackburn, Kwak and Kim (2017) analyzed 270 million behavior records from the fourth closed beta test of the MMORPG ArcheAge, run by XLGames in Korea from 8 December 2011 to 20 February 2012. At the end of a closed beta, every character and item is deleted. That makes the last days of the test a natural experiment on how players behave when consequences stop mattering. The treatment is "the world is about to end" and it hits everyone at once, so there is no untreated group in the same period. The authors compared players who stayed to the end with players who left voluntarily earlier (churners), whose own final days are a comparison "ending" that was not forced. They found no system-wide collapse into antisocial behavior, more social activity near the end, and a sharp drop in progression (quests, leveling). Churners were more likely than stayers to kill other players. In DiD terms, this is `δ = (change near a forced ending) − (change near a chosen ending)`. The comparison group differs by selection, since churners chose to leave. Naming that threat is the first thing a reviewer will do.

Three cases, one structure. Every one of these studies answers "what would have happened without the change?" with a comparison group, and every one is only as good as the case that its comparison group would have followed the same path.

### Eyes-open design judgment

- **Get the treatment variable into the data before the change.** The age field is the difference between analyst 1 and analyst 3. If you work in a studio and know a policy or feature will hit one group, make sure the telemetry can identify that group, with the privacy and consent duties that brings (MMO402 week 12).
- **Choose the comparison group for its trend, not its level.** A comparison group that starts higher or lower is fine. One that is on a different trajectory, such as older teens heading into exams, is not. Show the pre-period weekly lines in every DiD you report.
- **Run the placebo test.** Pretend the change happened earlier and compute DiD on pre-period data only. A clearly non-zero result means the design is biased.
- **Remember dilution in both directions.** Pooling hides effects on small groups. It also hides harms. A change that hurts 5% of players badly can look neutral in the average.
- **Prefer randomization when you can get it.** If a studio can hold back a random 5% of accounts from a feature for two weeks, that beats any quasi-experiment. Quasi-experiments are for when you can't.

### Check yourself (worked example)

1. A studio adds a "reputation" system to the EU servers only. Weekly reports of verbal abuse per 1,000 matches: EU before 12.0, after 9.5; NA before 11.0, after 10.0. Compute naive before-and-after on EU and the DiD. Which threat does NA help rule out?
2. In the interactive's default setting, the minors' share falls to 5%. Compute the pooled before and after values. Does the pooled change get closer to or further from the true effect?

<details>
<summary>Answers</summary>

1. Naive: `9.5 − 12.0 = −2.5`. DiD: `(9.5 − 12.0) − (10.0 − 11.0) = −2.5 + 1.0 = −1.5` reports per 1,000 matches. NA helps rule out history, such as a season change or a global chat filter update that hit both regions.
2. Before: `0.05 × 4.0 + 0.95 × 3.0 = 3.05`. After: `0.05 × 3.0 + 0.95 × 4.0 = 3.95`. The pooled change is +0.90, further from the true −2.0 than the +0.8 at 10%. The smaller the treated group, the more the pooled number just tracks the adults.

</details>

## 3. Interrupted time series

Sometimes there is no comparison group at all. A whole-world expansion changes every server on the same day. An **interrupted time series (ITS)** uses many measurements before and after the change, and asks whether the series jumped or bent at the change point more than its own history predicts. The standard model is a segmented regression:

```
Y_t = β0 + β1 × t + β2 × D_t + β3 × (t − t0) × D_t + error
```

- `t` is time (week number), and `t0` is the week of the change.
- `D_t` is 0 before the change and 1 from `t0` on.
- `β1` is the pre-change trend, `β2` is the immediate jump at the change and `β3` is the change in slope after it.

ITS handles maturation well, because the pre-change trend is estimated and projected forward. It handles history badly, because anything else that happened in week `t0` looks like the change. In games, patch days are crowded. Content, fixes, store items and events often ship together, so an ITS on "the new matchmaker" is usually an ITS on "patch 4.2". Zendle and colleagues' second analysis was a model of this family: it predicted each profile's weekly heavy play from a smooth trend over weeks plus a before-or-after indicator for the regulation. It inherits the same weakness as the pooled comparison. The series was not restricted to the players the rule applied to.

Two practical rules. First, you need enough points: aim for at least eight before and eight after, and more if the outcome has a weekly cycle. Second, weekly game data is **autocorrelated**. This week's value is close to last week's, so ordinary regression standard errors are too small. Use a method that allows for autocorrelation, or be modest about precision.

A useful upgrade is a **comparative ITS**: add a comparison series (another region, another game from the same studio, or players who never touched the changed feature) and ask whether the treated series bent more than the comparison did. That is DiD with many time points.

## 4. Regression discontinuity

Games are full of thresholds. A feature unlocks at level 20. Players at 1,500 rating are promoted to a new league. Accounts with more than 30 days of play get access to trading. A **regression discontinuity (RD)** design uses the threshold as the experiment. Players just below and just above the cutoff are nearly identical, except that one group got the treatment. Compare outcomes in a narrow band around the cutoff, allowing for the trend in the running variable (level, rating, days), and the jump at the cutoff estimates the effect for players near it.

Take an invented example. A studio gives players who finish a season at 1,500 rating or above a cosmetic reward and a "Gold" badge, and wants to know whether the badge increases next-season play. Comparing Gold players with everyone else mixes in skill and dedication. Comparing players who finished at 1,490 to 1,499 with players at 1,500 to 1,509 nearly removes both.

RD rests on one assumption that games often break: players must not be able to place themselves precisely on one side of the cutoff. In games the number is on screen, and players grind to it. If far more players finish at 1,500 to 1,504 than at 1,495 to 1,499, players pushed themselves over the line, and the ones who made it differ in motivation from the ones who didn't. Always plot a histogram of the running variable around the cutoff. A spike just above it (bunching) is a warning sign.

Two limits. RD estimates the effect only near the cutoff, so it tells you nothing about a 2,200-rated player. And it needs a lot of players near the threshold, which a small game may not have.

## 5. Choosing a design

| Situation | Best available design | Main threat it leaves | What you must show |
|---|---|---|---|
| You control the rollout and can hold players out | Randomized experiment (MMO308 week 5) | Interference between players, novelty | Randomization check, unit choice |
| Change hits one identifiable group; another group is untouched | Difference-in-differences | Different trends | Pre-period lines, placebo test |
| Change hits everyone at once; long history available | Interrupted time series, ideally with a comparison series | History (other things on the same day) | Other events at `t0`, autocorrelation |
| Treatment assigned by a cutoff on a number | Regression discontinuity | Players sorting across the cutoff | Histogram around the cutoff |
| Treatment is an event nobody chose (a wipe, an outage, a bug) | Natural experiment, analyzed with one of the above | Whatever made the event happen where it did | Why the event is as good as random |

Two questions decide most cases. First, **who got the change, and do you know who they are?** If you can't identify the treated players in your data, no amount of statistics recovers the effect on them. That is the whole of the reply to Zendle and colleagues. Second, **what would the treated players have done otherwise, and which data stands in for that?** Every design in the table is a different answer.

### Experiments on players are research on people

Random assignment is the strongest design and also the one that raises the sharpest ethical questions, because you deliberately give some players a different experience. MMO402 week 12 covers the line between product testing and research, and the Facebook emotional-contagion study. In January 2012 Facebook altered what some users saw in their News Feeds for a week to study emotional contagion. After publication in *PNAS* in 2014, the journal's editor published an expression of concern about whether participants had given informed consent and had the chance to opt out. For your projects, the rules are simple. Any study you run as a student, whether an experiment or a quasi-experiment on data you collect, goes to your institution's ethics review before data collection (week 10 covers the process). Quasi-experiments on existing data avoid manipulation, but not privacy duties: the minors in our worked example are exactly the players whose data needs the most care.

## In-class activity (25 minutes)

In groups of three, each group gets one card describing a real-sounding change to an invented MMO:

- A. A new-player mentor system launched on two of eight servers, chosen because their communities asked for it.
- B. A chat filter enabled for everyone on 3 March, the same day as a seasonal event.
- C. A daily login bonus given only to accounts under 30 days old.
- D. A raid difficulty change that affected only guilds that had already cleared the raid.

For your card:

1. (8 min) Pick the best available design from section 5 and write the estimating formula with named groups and periods.
2. (7 min) Name the strongest threat to internal validity for your design and the check that tests it (placebo test, pre-period plot, histogram at the cutoff, list of other events).
3. (5 min) Could the studio have randomized instead? If yes, what unit? If no, why not?
4. (5 min) Swap cards with another group and find one weakness in their answer.

Expected output: one formula, one named threat with its check, and a yes or no on randomization with a reason.

## Common misconceptions

- **"No significant change in the overall numbers means the change had no effect."** Pooled data dilutes effects on small groups. In the worked example, a policy that cut minors' heavy play from 5.0% to 3.0% showed up as a rise in the pooled figure.
- **"DiD needs the two groups to be similar."** It needs them to be on parallel *trends*. They can start at very different levels.
- **"A big dataset makes the estimate trustworthy."** Size shrinks random error. It does nothing for bias. Billions of hours without an age field still can't isolate minors.
- **"Quasi-experiments are observational, so ethics review doesn't apply."** Using existing player data still raises privacy and consent questions, and at a university it still goes through review.

## Check yourself

1. A studio doubles the drop rate of a crafting material on 1 June. Crafting sessions per active player rose 18% in June. Name two threats to internal validity that could explain part of the rise, with a game-specific example of each.
2. Players aged 15 and under had daily internet use fall by 10 minutes after a policy; players 16 and over fell by 6 minutes. What is the DiD estimate? What would you need to believe about the two age groups for it to be the effect of the policy?
3. You run a placebo DiD on pre-period weeks and get +0.9 points, while the real DiD is −1.2 points. What does the placebo tell you, and how would you report the result?
4. A matchmaking change applies to all players on patch day. Which design would you choose, what else would you collect, and why is a comparison series valuable here?
5. In the rating example of section 4, 1,200 players finished at 1,500 to 1,504 and 450 finished at 1,495 to 1,499. What does that suggest, and how does it affect the RD estimate of the badge's effect?

<details>
<summary>Answers</summary>

1. Examples: history (a summer event or a patch launched the same month), maturation (players who joined in spring reach the crafting stage in June), instrumentation (a logging change to how crafting sessions are counted), selection through attrition (non-crafters quit, leaving a more crafting-heavy population).
2. `δ = (−10) − (−6) = −4` minutes. You need to believe that without the policy, both groups' daily use would have changed by the same amount, the parallel-trends assumption.
3. The groups' trends were already diverging before the change, so the design is biased by roughly the placebo amount. Report both numbers, show the pre-period plot, and say that the true effect is uncertain. Don't report −1.2 as the effect. Consider a different comparison group, or a comparative ITS that models each group's own trend.
4. An interrupted time series on weekly outcomes with many weeks before and after, plus a list of everything else that shipped in the same patch. A comparison series (a region that got the patch later, or a game mode the change didn't touch) helps separate the matchmaking change from other patch-day events (history).
5. Bunching above the cutoff: players pushed themselves over 1,500. Those just above differ in motivation from those just below, so the RD comparison mixes the badge's effect with that difference, likely overstating it. Narrowing the band doesn't fix it. Report the histogram and treat the estimate with caution, or find a threshold players can't see.

</details>

## Lab / assignment hook

[Lab 05, difference-in-differences on a synthetic policy change](../labs/lab05.md). You receive 16 weeks of synthetic telemetry from an invented MMO with an age field, compute the pooled change, the naive before-and-after and the DiD, run a placebo test, and then discover that one of two possible comparison groups breaks parallel trends. Deliverable: passing code and a one-page design critique that you will reuse in your proposal's threats-to-validity section.

## Sources

- Zendle, D., Flick, C., Gordon-Petrovskaya, E., Ballou, N., Xiao, L. Y. & Drachen, A. (2023). "No evidence that Chinese playtime mandates reduced heavy gaming in one segment of the video games industry." *Nature Human Behaviour*, 7(10), 1753-1766. https://doi.org/10.1038/s41562-023-01669-8. Full text checked in Europe PMC (PMC10593605, September 2026): the November 2019 rule (1.5 hours a day, 3 on holidays, no play 22:00 to 08:00), the September 2021 expansion, Unity Analytics data from 16 August 2019 to 16 January 2020, 7.04 billion hours and about 2.4 billion profiles, the heavy-play definition, 0.77% and 0.88% prevalence and odds ratio 1.14, the multilevel model with a smooth week term and a regulation indicator, the missing age data, and the Tencent figure of 6.4% of playtime from minors in September 2020 (as cited by the authors).
- Karhulahti, V.-M., Huntington-Klein, N., Ballou, N. & Ropovik, I. (2026). "'No Evidence That Chinese Playtime Mandates Reduced Heavy Gaming': Zendle et al. (2023) Cannot Support Its Claims Due to a Flawed Design." *Collabra: Psychology*, 12(1), 161080. https://doi.org/10.1525/collabra.161080. Metadata checked via Crossref; argument checked in the preprint abstract (PsyArXiv, https://doi.org/10.31234/osf.io/n2rka_v4).
- Choi, J., Cho, H., Lee, S., Kim, J. & Park, E.-C. (2018). "Effect of the Online Game Shutdown Policy on Internet Use, Internet Addiction, and Sleeping Hours in Korean Adolescents." *Journal of Adolescent Health*, 62(5), 548-555. https://doi.org/10.1016/j.jadohealth.2017.11.291. Abstract checked on PubMed (PMID 29434003): policy from November 2011, midnight to 6 a.m., ages 15 and below; Korea Youth Risk Behavior Web-based Survey 2011-2015; group sizes; DiD estimates by year; no change in addiction or sleep.
- Kang, A. R., Blackburn, J., Kwak, H. & Kim, H. K. (2017). "I Would Not Plant Apple Trees If the World Will Be Wiped: Analyzing Hundreds of Millions of Behavioral Records of Players During an MMORPG Beta Test." *Proceedings of WWW 2017*. https://doi.org/10.1145/3038912.3038914. Checked in the arXiv version (1703.01500): 4th closed beta of ArcheAge by XLGames, 8 December 2011 to 20 February 2012, 270 million records, comparison with voluntary churners, findings on progression, social activity and player killing.
- Kramer, A. D. I., Guillory, J. E. & Hancock, J. T. (2014). "Experimental evidence of massive-scale emotional contagion through social networks." *PNAS*, 111(24), 8788-8790. https://doi.org/10.1073/pnas.1320040111. Verma, I. M. (2014). "Editorial expression of concern." *PNAS*, 111(29), 10779. https://doi.org/10.1073/pnas.1412583111 (checked on PubMed, PMID 24994898). The January 2012 date is as given in MMO402 week 12's sources.
- Shadish, W. R., Cook, T. D. & Campbell, D. T. (2002). *Experimental and Quasi-Experimental Designs for Generalized Causal Inference*. Houghton Mifflin. The standard list of threats to internal validity.

## Interactive spec: examples/w05-did-parallel-trends.html

**Purpose.** Show that a pooled before-and-after series can hide or reverse a policy's effect on a small treated group, that DiD recovers it when trends are parallel, and that a placebo test exposes non-parallel trends.

**Layout.** Two vertically stacked line charts sharing an x-axis of weeks −8 to +7 (16 weeks, the change at week 0 drawn as a vertical dashed line labeled "rule starts"). On desktop, a readout column to the right; on mobile, readouts below the charts.

- **Top chart, "What pooled telemetry shows".** One line: `pooled(t)`.
- **Bottom chart, "Split by the group the rule applies to".** Minors line (accent color), adults line (neutral color), and a dashed minors counterfactual line from week 0 on, `minor_cf(t) = minor(t) − e` for `t ≥ 0`. Shade the gap between `minor(t)` and `minor_cf(t)` after week 0 and label it "effect".

**Controls.**
- `w`, minors' share of accounts: slider 0.02 to 0.50, step 0.01, default 0.10.
- `c`, common shock at week 0 (for example an expansion): slider −2.0 to +2.0, step 0.1, default +1.0.
- `e`, true policy effect on minors: slider −3.0 to +1.0, step 0.1, default −2.0.
- `g`, common weekly trend: slider −0.20 to +0.20, step 0.01, default 0.
- `d`, extra weekly pre-trend for minors (breaks parallel trends): slider −0.30 to +0.30, step 0.05, default 0.
- Buttons: "Reset", "Tencent-sized group" (sets `w = 0.064`), "Break parallel trends" (sets `d = 0.25`).

**Model (all values in percentage points of accounts playing heavily).**
- `adult(t) = 3.0 + g × t + c × [t ≥ 0]`
- `minor(t) = 4.0 + (g + d) × t + (c + e) × [t ≥ 0]`
- `pooled(t) = w × minor(t) + (1 − w) × adult(t)`
- Window means: pre = weeks −4 to −1, post = weeks 0 to 3, early-pre = weeks −8 to −5.

**Readouts (two decimals).**
- Pooled change = mean pooled(post) − mean pooled(pre).
- Pooled odds ratio = `odds(mean pooled post / 100) / odds(mean pooled pre / 100)`, with `odds(p) = p / (1 − p)`.
- Minors only change = mean minor(post) − mean minor(pre).
- DiD = (minor post − minor pre) − (adult post − adult pre), using window means.
- Placebo DiD = (minor pre − minor early-pre) − (adult pre − adult early-pre).
- True effect `e`, and "bias = DiD − e".

**Test values.**
- Defaults (`w = .10, c = 1, e = −2, g = 0, d = 0`): pooled means 3.10 before, 3.90 after, change +0.80, odds ratio 1.27; minors only −1.00; DiD −2.00; placebo 0.00; bias 0.00.
- `w = .05`, other defaults: pooled change +0.90.
- `d = .25`, other defaults: DiD −1.00; placebo +1.00; bias +1.00. (Each side of each comparison is four weeks apart, so the bias is `4 × d`.)
- `e = 0`, other defaults: pooled change +1.00, minors only +1.00, DiD 0.00.

**The one insight.** At the defaults, the top chart steps up while the bottom chart shows minors stepping down under the counterfactual. The student should see that no amount of staring at the top chart could reveal the bottom one.

**Accessibility and style.** Lines distinguished by dash pattern as well as color. Each chart has a text summary under it that updates with the readouts. Sliders keyboard operable with visible focus. Respect `prefers-reduced-motion` and `prefers-color-scheme`. Use `templates/interactive-tokens.css` inline. No game art or logos.
