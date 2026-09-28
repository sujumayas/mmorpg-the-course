# UX201 · Week 04 — Self-Determination Theory: Competence, Autonomy, Relatedness

**Why this matters:** Every game hands out rewards, and most teams judge a reward by the spike it causes on the dashboard. Self-Determination Theory predicts something the dashboard can't show. Some rewards raise play while they run and leave players playing less than before once they stop. This week you learn to tell those rewards from the ones that build lasting motivation, and to put a number on the difference.

**You will be able to:**
- Name the three needs of Self-Determination Theory and identify which one a given game feature supports or thwarts.
- Classify a reward as engagement-, completion- or performance-contingent, or as informational feedback, and predict its effect on later free play.
- Compute the post-reward change in play from a published effect size, and the break-even point of a reward event.
- Critique a reward or social feature by the need it serves, and propose a change that keeps the uplift without the undermining.

**Before class:** Richard Ryan, Scott Rigby and Andrew Przybylski, "The Motivational Pull of Video Games: A Self-Determination Theory Approach," *Motivation and Emotion* 30 (2006), 347-363. Read the introduction and studies 1 and 4. Celia Hodent, *The Gamer's Brain* (CRC Press, 2017), the chapter "Motivation" (pp. 59-72). Skim the abstract of Deci, Koestner and Ryan (1999), listed in Sources.

**Prerequisites from earlier courses:** [UX201 week 3, flow and difficulty](w03-flow-and-difficulty.md). Optimal challenge is how a game feeds competence, and this week builds on it. [GD101 week 5, player experience goals](../../GD101-introduction-to-game-design/lectures/w05-player-experience-goals-and-the-8-kinds-of-fun.md), for the difference between what a game offers and what a player seeks. [GD101 week 9, choice and meaningful decisions](../../GD101-introduction-to-game-design/lectures/w09-choice-and-meaningful-decisions.md), which is the design side of autonomy. [MA102 week 8, dice sums and the normal curve](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w08-dice-sums-and-the-normal-curve.md), for reading an effect size as a shift of a bell curve. [MA102 week 14, hypothesis testing and A/B](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w14-intro-to-hypothesis-testing-ab.md), for the control group you need to see any of this in live data.

**Interactive:** [Reward crowding-out: dashboard vs cumulative view](../examples/w04-reward-crowding.html). Use it during section 2.

---

## 1. Three needs and two kinds of motivation

Psychologists Edward Deci and Richard Ryan built **Self-Determination Theory (SDT)** from the 1970s onward. It starts from a claim about people in general, not about games. People have three basic psychological needs, and activities that satisfy them are pursued willingly and feel good. Activities that thwart them are avoided, or pursued only under pressure.

- **Competence** is the need to feel effective, to act on the world and see that you are getting better at it. Clear goals, readable feedback and a challenge that matches skill feed it. That is flow from week 3, seen from the motivation side.
- **Autonomy** is the need to feel that your actions are your own choice. It is not the same as independence or having many options. A player who chooses to follow a guide is autonomous. A player forced through the one viable build is not, however many buttons the build uses.
- **Relatedness** is the need to feel connected to others, to matter to them and have them matter to you.

### Intrinsic and extrinsic

**Intrinsic motivation** means doing something because the activity itself is satisfying. **Extrinsic motivation** means doing it for a separable outcome, such as a reward, a grade, or avoiding a penalty. SDT does not treat extrinsic motivation as one thing. It arranges it on a continuum by how much the person has taken the reason on as their own.

| Regulation | The player's reason, in their words | How autonomous |
|---|---|---|
| External | "I log in because the daily reward resets if I don't." | Least |
| Introjected | "I'd feel guilty letting my guild down." | Low |
| Identified | "Farming this is dull, but I want to be ready for the raid." | High |
| Integrated | "Being the guild's crafter is part of who I am in this game." | Higher |
| Intrinsic | "I just like crafting." | Most |

Designers often talk as if extrinsic rewards were fake motivation and intrinsic enjoyment the real kind. SDT's picture is more useful. An extrinsic reason can be fully autonomous. The raider who farms because they value the raid has an extrinsic reason and no sense of being pushed. The question to ask about any system is where it sits on this table for the players who use it.

### Cognitive evaluation theory: the same reward, two meanings

A sub-theory of SDT, **cognitive evaluation theory (CET)**, explains when a reward helps or hurts. Every reward has what Deci and Ryan call a *functional significance*, which is roughly what the reward tells the person.

- An **informational** reward tells you about your competence. "New personal best" or a skill rank that tracks your play. It tends to raise intrinsic motivation, because it feeds competence without taking autonomy.
- A **controlling** reward tells you what you must do. "Log in 7 days in a row or lose your streak." It tends to lower intrinsic motivation, because the reason for acting moves from inside the activity to outside it.

The same object can be either. A trophy you earned by beating a hard boss informs. A trophy you are chasing because a checklist tells you to controls. Players, not designers, decide which one it is, and the framing the designer chooses tips them.

## 2. Worked example: same numbers, opposite feeling

### The hook

During the beta of the original World of Warcraft, the game had no rest bonus. Instead it cut experience gain by half after a few hours of continuous play, to push players to stop. Testers hated it. Blizzard replaced it with **rested experience**, which gives double experience for a while after time away from the game. The Warcraft Wiki reports that the developers later described the change as the same numbers seen from the opposite point of view. The ratio between tired and fresh play barely moved. What changed was the message. The first version said "you are being punished for playing." The second said "here is a gift for coming back." Rested experience is still in the game two decades later, and the wiki describes it as a bonus, a reason to log out in an inn and take breaks.

Two questions follow. Why should a label change how people feel about identical arithmetic? And can we say how much a controlling reward costs, in minutes of play, once it stops?

### The model

CET gives the first answer. The penalty version was controlling. The bonus version was closer to informational, or at least not contingent on playing more. For the second question we need numbers, and the best available come from a meta-analysis by Deci, Richard Koestner and Ryan (1999). It pooled 128 laboratory experiments that all used some version of the **free-choice paradigm**. Participants do an interesting task, some of them for a reward. Then the reward is withdrawn, the experimenter leaves the room, and the researcher measures how long each person keeps doing the task when nobody asks them to. That free-choice time is the measure of intrinsic motivation.

The original was Deci's 1971 study with Soma cube puzzles. Students who were paid a dollar per solved puzzle in the second session spent more free time on the puzzles during that session, and less than their own starting level in the third session, after the pay stopped. An unpaid control group showed no such drop.

The meta-analysis reports results as **effect sizes** `d`, the difference between the rewarded group and the control group in free-choice behaviour, measured in standard deviations. From MA102 week 8, a standard deviation is the natural unit of spread in a bell curve, so `d = −0.36` means the rewarded group's whole distribution sits 0.36 standard deviations to the left of the control group's.

The model has two lines. Let `μ` be players' mean voluntary time in an activity before any reward, `σ` its standard deviation, and `d` the effect size for the reward type.

```
play while the reward runs   = μ + X
play after the reward stops  = μ + d × σ
```

- `X` is the extra play the reward buys while it runs. It depends on the reward's size and you measure it. The meta-analysis doesn't give it to you.
- `d` depends on the reward's contingency, taken from the meta-analysis.

The share of players who end up below the old average is `Φ(−d)`, where `Φ` is the standard normal cumulative distribution. For a negative `d`, that share is above one half.

The meta-analysis classified rewards by what they were contingent on. Each category has an everyday game equivalent.

| Contingency | Lab version | Game version | `d` on free-choice play |
|---|---|---|---|
| Engagement-contingent | Paid for doing the task at all | "Play 3 matches today," login rewards | −0.40 |
| Completion-contingent | Paid for finishing the task | "Complete 3 dungeons this week" | −0.36 |
| Performance-contingent | Paid for meeting a standard | "Win 5 matches," "reach the top 10%" | −0.28 |
| Positive feedback | Told you did well | "New personal best," a rank that reflects skill | +0.33 |

These are small-to-moderate effects, pooled from lab tasks chosen to be interesting, with children and college students. On self-reported interest, as opposed to free-choice time, the same meta-analysis found smaller undermining (`d = −0.15` for engagement-contingent and `−0.17` for completion-contingent rewards). Treat the table as the best available estimate of direction and rough size, not as a measured property of your game.

### Numbers you can check

Take an optional activity in an invented MMO, say fishing. Before any change, players who fish spend a mean `μ = 30` minutes a week on it, with `σ = 20`. The team adds a four-week "Angler's Contract" event. It is completion-contingent: catch 20 fish a week for a reward. The event raises fishing by `X = 15` minutes a week while it runs. That is a 50% uplift, and it will be on a slide.

After the event, the model predicts:

| Reward type | `d` | Weekly fishing after the event | Share of players below the old mean |
|---|---|---|---|
| Engagement-contingent | −0.40 | 30 − 0.40 × 20 = 22.0 min | Φ(0.40) = 65.5% |
| Completion-contingent | −0.36 | 30 − 0.36 × 20 = 22.8 min | Φ(0.36) = 64.1% |
| Performance-contingent | −0.28 | 30 − 0.28 × 20 = 24.4 min | Φ(0.28) = 61.0% |
| Positive feedback | +0.33 | 30 + 0.33 × 20 = 36.6 min | Φ(−0.33) = 37.1% |

Now the question a producer should ask. Did the event gain or lose fishing overall? The event added `4 × 15 = 60` minutes per player. The undermining costs `0.36 × 20 = 7.2` minutes a week for as long as it lasts. The break-even point is

```
weeks to break even = (event weeks × X) / (|d| × σ) = 60 / 7.2 = 8.3 weeks
```

If the lower level lasts longer than about eight weeks, the event cost more fishing than it bought. If it lasts twelve weeks, the net is `60 − 12 × 7.2 = −26.4` minutes per player. That is a loss, from an event whose dashboard showed +50%.

Check one row by hand. Performance-contingent, `d = −0.28`: `0.28 × 20 = 5.6` minutes lost a week, break-even at `60 / 5.6 = 10.7` weeks. Performance rewards undermine less than engagement rewards in the meta-analysis because they carry some information about competence. Doing well is part of what is rewarded.

One number here is an assumption, and you should say so whenever you use the model. The meta-analysis measured free-choice time minutes after the reward stopped, in a lab. How long the drop lasts in a live game, weeks or days, is not known from those studies. The persistence `R` is a slider in the interactive for that reason. The direction of the effect is well supported. Its duration in your game is something you measure.

### A visual you can move

Open `examples/w04-reward-crowding.html`. The left chart is the dashboard view, weekly fishing minutes over 20 weeks, with the event in weeks 5 to 8. The bars jump during the event and dip after it. They look like a normal post-event settle. The right chart is the cumulative difference from a control group that never saw the event. It climbs to +60 at week 8, falls through zero during week 17 and ends at −26.4 at week 20. Same numbers, two views. One says the event worked. The other says it cost you.

Switch the reward type to positive feedback and the right curve never comes back down. Set the persistence to 4 weeks and the event stays in profit. Drag the uplift `X` and watch how large an uplift has to be before a controlling reward pays for itself over 12 weeks. That turns out to be `12 × 7.2 / 4 = 21.6` minutes a week.

### Cross-game recognition

**World of Warcraft rest (beta to today).** The hook in model terms. The penalty version was a controlling contingency on play length, like an engagement-contingent reward turned upside down. The bonus version is not contingent on doing more. It rewards coming back, and the wiki's own description of it as a reason to take breaks shows it read as a gift. The arithmetic between fresh and tired play barely changed. The functional significance did.

**Deci's newspaper field study (1971).** The same paper included a field version. Student staff writing headlines for a college newspaper were paid 50 cents a headline for a period, then told the money had run out. Their pace afterwards fell relative to an unpaid comparison group. Nothing about it is a game, which is the point. The effect comes from people, not from a genre.

**Gamification badges.** Points and badges bolted onto non-game activities, such as check-ins in the location app Foursquare, drew criticism grounded in SDT. Critics argued that expected rewards for activities that don't meet competence, autonomy or relatedness would crowd out whatever interest was there. Rewrite it in this week's form. A badge for checking in is engagement-contingent, `d` around −0.40 if the lab result transfers. A badge that reports something you actually achieved leans informational.

Three settings, one principle. What a reward tells the player matters as much as what it gives them.

### Eyes-open design judgment

- **Controlling rewards are not forbidden.** They are the right tool for activities with little intrinsic interest to begin with. The critics of the meta-analysis (Cameron, Pierce and colleagues) showed that rewards can raise interest in tasks people initially found dull. The damage is concentrated where interest was already high. So a daily bounty on a chore is cheap. A daily bounty on the activity your players already love is expensive.
- **Measure with a holdout.** The dashboard view can't show the cost, because the "before" level is gone by the time you look for it. Keep a small control group that never sees the event, as MA102 week 14 describes, and compare the two groups for weeks after the event ends.
- **Framing is design, not marketing.** The rest system shows that the same numbers can be controlling or not depending on the frame. Put the frame on the design review checklist. Does this reward say "you must" or "you did"?
- **Performance rewards sit in the middle.** They undermine less, but they also exclude. Only players who meet the standard get the information. For players who miss it, a performance reward reports incompetence, which is worse than no reward.
- **Streaks are a special case.** A streak adds a loss on top of an engagement-contingent reward, so it is the most controlling kind. If you ship one, give it a grace day or a freeze, which turns part of the threat back into a choice.

### Check yourself (worked example)

1. A team adds an engagement-contingent "play 30 minutes a day" reward to a crafting system with `μ = 50` and `σ = 25` minutes a week. What weekly crafting time does the model predict after the reward ends, and what share of crafters end up below the old mean?
2. For the Angler's Contract with `d = −0.36`, what weekly uplift `X` makes the event break even if the undermining lasts exactly 10 weeks?
3. A designer says, "Our positive-feedback system raised play by 0.33 standard deviations, so it's worth the same as the event's uplift." What is wrong with comparing those two numbers directly?

<details>
<summary>Answers</summary>

1. `50 − 0.40 × 25 = 40` minutes a week. The share below the old mean is `Φ(0.40) = 65.5%`.
2. The loss is `10 × 7.2 = 72` minutes, spread over a four-week event, so `X = 72 / 4 = 18` minutes a week.
3. The event's `X` is measured while the reward runs. The `d` for positive feedback is measured after the feedback stops. They answer different questions. To compare them you need both the during and after effects of each design, which is what the cumulative view shows.

</details>

## 3. Measuring need satisfaction in play

The effect sizes above come from labs. For games you need a way to ask players about competence, autonomy and relatedness directly. Rigby and Ryan developed the **Player Experience of Need Satisfaction (PENS)** questionnaire for this. It has short subscales, each a few statements rated on a scale from "do not agree" to "strongly agree." There are subscales for in-game competence, in-game autonomy and in-game relatedness, plus two that describe how the game gets there, intuitive controls and presence.

Ryan, Rigby and Przybylski (2006) used it in four studies, and the design of the first one is worth copying.

- **Study 1.** Undergraduates played Super Mario 64 for 20 minutes and then filled in PENS and measures of enjoyment and future play. After the session, each was offered a free choice of playing more of the same game or an alternative popular game. Of the 88 participants, 31 chose Mario, 54 chose the alternative, 2 withdrew and 1 went unrecorded. Competence and autonomy predicted enjoyment and the preference for future play. Intuitive controls predicted competence and autonomy, so a clunky control scheme costs motivation through the needs.
- **Study 2.** Participants played two 3D adventure games, The Legend of Zelda: Ocarina of Time and A Bug's Life, chosen because the first ranked near the top of popularity surveys and the second near the bottom. Zelda scored higher on enjoyment (mean 4.56 against 3.60) and on preference for future play (3.21 against 2.24). The difference in intuitive controls was not significant, because both used simple controls. The difference in competence and autonomy was.
- **Study 4.** An online survey of people who played MMOs. Here relatedness joined competence and autonomy, and the paper reports that the three needs independently predicted enjoyment and future play. It also compared PENS with Nick Yee's motivation components, which you meet in week 6.

Two lessons for your own tests.

First, pair self-report with behaviour. The free choice at the end of study 1 is the same idea as Deci's free-choice period. People will tell you a game was fun. Whether they keep playing when they could stop is a harder measure to fake.

Second, a need score is a diagnosis, not a verdict. If players report low autonomy, you still have to find the feature that takes it away. The PENS pattern points you to the right need. The playtest methods from week 3 and GD101 week 7 find the feature.

## 4. Designing for each need

Each need can be supported or thwarted, and most features do some of each. A **need audit** lists a game's major systems and marks, for each need, what the system gives and what it takes.

### Competence

Support comes from optimal challenge (week 3), clear and immediate feedback (GD101 week 12), and visible growth. Thwarting comes from feedback that arrives late or can't be read, difficulty spikes, and, less obviously, rewards that report failure. A leaderboard where 90% of players see themselves in the bottom half reports incompetence to most of the people who look at it. A personal-best display reports growth to all of them.

### Autonomy

Support comes from meaningful choice, the kind GD101 week 9 defined, where options differ in ways the player cares about and more than one is viable. It also comes from volition over when and how long to play. Thwarting comes from dominant strategies that make choice fake, from schedules the game sets for the player (daily resets, timed events you must attend), and from controlling language. "You must complete" and "don't miss out" push the reason for play outside the player.

A useful test is to ask what happens if the player says no. If the answer is "nothing, they just don't get the bonus," the feature is probably not controlling. If it's "they fall behind, lose a streak or let down their group," it is.

### Relatedness

Support comes from reasons to help, from shared goals, and from signals that others noticed you. Thwarting comes from forced grouping with strangers who have no reason to care, from toxic chat, and from systems that make other players into obstacles.

Journey (2012) shows how little it can take. Two players who meet in the desert can travel together and help each other. They can't talk, type, or see each other's names until the credits. Their only signal is a musical chime. The developers set out to build an emotional connection between anonymous strangers. The design bets that relatedness can come from a shared goal, the chance to help, and the removal of most of what goes wrong in online talk. MMO305 goes further, covering [forced and voluntary grouping in week 3](../../MMO305-social-systems-and-online-behaviour/lectures/w03-forced-vs-voluntary-grouping.md) and [designing for positive social play in week 14](../../MMO305-social-systems-and-online-behaviour/lectures/w14-designing-for-positive-social-play.md).

### A worked need audit

| System (invented MMO) | Competence | Autonomy | Relatedness |
|---|---|---|---|
| Daily login calendar | — | Thwarts: reward for showing up, a missed day costs | — |
| Personal-best dungeon timer | Supports: informational | Supports: optional | — |
| Weekly guild objective | Supports if progress is visible | Mixed: chosen group, set schedule | Supports: shared goal |
| Random-group dungeon finder | Supports: steady challenge | Supports: play when you like | Weak: strangers, no reason to care |
| "Complete 20 fishing catches" event | Weak: reports quantity, not skill | Thwarts: completion-contingent | — |

Read down a column to find the need your game leaves hungry. Read across a row to see what a change would cost. Turning the fishing event into "log your biggest catch" moves it from the completion row towards the personal-best row. You lose some of the uplift and most of the undermining.

## In-class activity (25 minutes)

Pairs. Pick a game both of you have played for at least ten hours.

1. **Audit (10 min).** List five systems that give rewards. For each, classify the contingency (engagement, completion, performance, informational) and mark each need as supported, thwarted or not involved.
2. **Price one (5 min).** Choose the most controlling reward. Make a reasonable guess at `μ` and `σ` for the activity it rewards, in minutes a week, and use the section 2 table to predict play after the reward stops.
3. **Redesign (10 min).** Rewrite that reward so it becomes informational, or so saying no costs nothing. State what you expect to lose in uplift and what you expect to keep.

Expected output: a five-row audit table, one priced reward with its predicted post-reward time, and a one-paragraph redesign with its trade-off.

## Common misconceptions

- **"Extrinsic rewards are bad."** They are fine for low-interest tasks and for rewards that read as information. The meta-analysis's negative effects are for expected, tangible, contingent rewards on activities people already found interesting.
- **"Autonomy means lots of options."** Autonomy is the sense that you chose. Thirty weapons with one viable choice give less autonomy than three weapons that all work.
- **"If the event raised engagement, it worked."** The event's effect includes what happens after it ends. Without a holdout group you only see the first half.
- **"Relatedness means chat and guilds."** Journey supports relatedness with no chat at all. Chat can thwart relatedness when it is mostly hostile.

## Check yourself

1. Classify each as engagement-, completion- or performance-contingent, or informational: (a) 50 gold for every hour online; (b) a badge for finishing every quest in a zone; (c) a title for reaching the top 1,000 in the ladder; (d) a post-match screen showing your accuracy compared with your last ten matches.
2. A rhythm game's players spend `μ = 40` minutes a week in free play, `σ = 30`. The team adds a performance-contingent weekly reward for scoring A on five songs. Predict free play after the reward is removed. How many weeks of undermining would a four-week event with `X = 10` survive before losing time overall?
3. A PENS survey of your beta testers shows high competence, high relatedness and low autonomy. Name two kinds of feature you would inspect first, and why.
4. Using the continuum table in section 1, place this player's reason: "I run the weekly dungeon with my friends because I'd feel bad if they had to find a replacement." What would move the same behaviour one row towards autonomy?

<details>
<summary>Answers</summary>

1. (a) Engagement-contingent. (b) Completion-contingent. (c) Performance-contingent. (d) Informational.
2. `40 − 0.28 × 30 = 31.6` minutes a week. The loss is 8.4 minutes a week and the gain is `4 × 10 = 40` minutes, so it breaks even after `40 / 8.4 = 4.8` weeks.
3. Look at features that set schedules or impose a fixed path, such as daily resets, timed events and a single viable build, and at controlling language in quest and event text. Those take away autonomy while leaving competence and relatedness alone.
4. Introjected, because guilt drives it. It moves towards identified when the player values the outcome for themselves, for example because they enjoy the team's progress. Design can help by making it easy to skip a week without penalty to the group, which removes the guilt lever and leaves the reason that remains.

</details>

## Lab hook

[Lab 04, a free-choice experiment](../labs/lab04.md). In small groups you run a short version of Deci's free-choice paradigm on a browser puzzle game with classmates as participants. One group gets a points reward for each solved puzzle and one doesn't, and you time what everyone does in an unobserved free period afterwards. You compute the effect size with the starter script and compare it with the meta-analysis. Deliverable: the data, the script output and a two-page report on what your sample can and can't tell you.

## Sources

- Deci, E. L. (1971). "Effects of externally mediated rewards on intrinsic motivation." *Journal of Personality and Social Psychology*, 18(1), 105-115. The three-session Soma puzzle experiment (payment of one dollar per puzzle in session 2, free-choice period of eight minutes), the newspaper headline field experiment (50 cents per headline) and the verbal-praise experiment. Details checked against Wikipedia, "Self-determination theory" and "Overjustification effect" (accessed September 2026).
- Deci, E. L., Koestner, R. & Ryan, R. M. (1999). "A meta-analytic review of experiments examining the effects of extrinsic rewards on intrinsic motivation." *Psychological Bulletin*, 125(6), 627-668. Abstract via PubMed (PMID 10589297): 128 studies; free-choice effect sizes d = −0.40 (engagement-contingent), −0.36 (completion-contingent), −0.28 (performance-contingent), +0.33 (positive feedback); self-reported interest d = −0.15 (engagement), −0.17 (completion). Abstract checked September 2026.
- Cameron, Pierce and colleagues' critiques of the undermining effect, including Cameron, Banko & Pierce (2001) in *The Behavior Analyst*, which found rewards can raise interest in low-interest tasks. Via Wikipedia, "Overjustification effect."
- Ryan, R. M., Rigby, C. S. & Przybylski, A. (2006). "The Motivational Pull of Video Games: A Self-Determination Theory Approach." *Motivation and Emotion*, 30, 347-363. PENS subscales; study 1 (Super Mario 64, 88 participants, 31 chose the target game and 54 the alternative); study 2 (Zelda against A Bug's Life, enjoyment 4.56 against 3.60, future play 3.21 against 2.24); study 4 (MMO players, relatedness).
- Warcraft Wiki, "Rest" (warcraft.wiki.gg, accessed September 2026). Rested experience as a bonus of double experience; the beta design that halved experience after a few hours, replaced after tester complaints; the developers' description of it as the same numbers from the opposite point of view.
- Wikipedia, "Journey (2012 video game)" (accessed September 2026). Anonymous two-player meetings, no speech or text, names shown after the credits, communication by a musical chime.
- Wikipedia, "Overjustification effect," section on gamification (accessed September 2026). SDT-based critiques of points and badges, Foursquare as the example.
- Hodent, C. (2017). *The Gamer's Brain*. CRC Press. Chapter "Motivation" (pp. 59-72).
- The fishing example, its `μ`, `σ` and `X`, the persistence assumption and the need audit table are this course's own teaching models.

## Interactive spec: examples/w04-reward-crowding.html

**Purpose.** Show that a controlling reward can raise play while it runs and lower it afterwards, so that the event's net effect depends on the post-event period that a normal dashboard hides.

**The one insight the visual must make obvious.** At defaults, the left chart's bars jump during the event and settle a little lower afterwards, which looks harmless. The right chart's cumulative line climbs to +60, falls through zero during week 17 and ends at −26.4.

**Layout.** Two charts side by side at 1280px, stacked at 390px with the cumulative chart second. Controls and a numbers panel below. An optional third panel, collapsed by default, shows two bell curves (before and after).

- Left, "Weekly minutes (dashboard)": x axis weeks 1 to 20, y axis 0 to 60 minutes. Bars for the treated group. A dashed horizontal line at `μ` for the control group. Shade the event weeks.
- Right, "Cumulative difference from control": x axis weeks 1 to 20, y axis symmetric around 0 (auto range, at least ±80). Line of `Σ (treated − control)` up to each week. Mark the zero crossing with a labelled dot ("break-even, week N"). Positive area in one fill, negative area in another with a hatch pattern.
- Optional panel, "Where players end up": two normal curves with mean `μ` and `μ + dσ`, standard deviation `σ`, with the area of the after-curve below the old mean shaded and labelled with `Φ(−d)` as a percentage.

**Controls.**

- Reward type: segmented control with Engagement (d = −0.40), Completion (−0.36, default), Performance (−0.28), Positive feedback (+0.33), and Custom (enables a `d` slider from −0.6 to +0.6, step 0.01).
- `μ`: 0 to 120 minutes, default 30. `σ`: 5 to 60, default 20.
- Event start week: 2 to 10, default 5. Event length `E`: 1 to 8 weeks, default 4.
- Uplift `X`: 0 to 40 minutes a week, default 15.
- Persistence `R`: 0 to 20 weeks, default 12 (weeks after the event during which the `dσ` shift applies; afterwards treated returns to `μ`). Caption: "Unknown from lab studies. Measure it."
- Presets: "Default: completion event", "Positive feedback", "Short persistence (R = 4)", "Big uplift (X = 21.6)".
- Reset.

**Formulas.** For week `w`: control = `μ`. Treated = `μ` before the event; `μ + X` during the event; `μ + d × σ` for `R` weeks after the event; `μ` afterwards. Cumulative difference `C_w = Σ_{v ≤ w} (treated_v − μ)`. Break-even week = first week after the event where `C_w ≤ 0` (show "none" if never). Analytic break-even length = `E × X / (|d| × σ)` weeks after the event (show only when `d < 0`). Share below old mean = `Φ(−d)` with a standard normal CDF (use an erf approximation with error below 1e-4).

**Numbers panel.** Minutes gained during the event (`E × X`), minutes lost per week after (`|d| × σ`, or gained if `d > 0`), break-even length, break-even week, final cumulative difference at week 20, weekly minutes after the event, share below old mean. A sentence built from the data, for example "The event added 60 minutes per player, then cost 7.2 a week. It is in the red from week 17."

**Test values.**

- Defaults (completion, `μ = 30`, `σ = 20`, start 5, `E = 4`, `X = 15`, `R = 12`): treated weeks 5 to 8 = 45; weeks 9 to 20 = 22.8. `C_8 = 60`. `C_16 = 60 − 8 × 7.2 = 2.4`. `C_17 = −4.8`, so break-even week 17. `C_20 = −26.4`. Break-even length 8.33 weeks. Share below old mean 64.1%.
- Engagement: after = 22.0, loss 8.0 a week, break-even length 7.5 weeks, `C_20 = −36.0`, share 65.5%.
- Performance: after = 24.4, loss 5.6 a week, break-even length 10.71 weeks, `C_20 = −7.2`, share 61.0%.
- Positive feedback with `X = 5`: after = 36.6, `C_20 = 20 + 12 × 6.6 = 99.2`, break-even "none", share 37.1%.
- Completion with `R = 4`: `C_20 = 60 − 28.8 = 31.2`, break-even "none".
- Completion with `X = 21.6`: `C_20 = 86.4 − 86.4 = 0.0` (break-even exactly at week 20).
- Section 2 check-yourself: `μ = 50`, `σ = 25`, engagement: after = 40.0, share 65.5%.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`, light and dark. Positive and negative areas differ by pattern as well as colour. Every control keyboard operable with visible numeric values. The break-even marker has a text label, not only a colour. Respect reduced motion (no animated bar growth when set). No game art or logos; the activity is labelled "optional activity (e.g. fishing)".
