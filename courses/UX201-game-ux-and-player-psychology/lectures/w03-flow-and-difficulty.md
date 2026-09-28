# UX201 · Week 03 — Flow and Difficulty

**Why this matters:** Most players who stop playing your game don't send feedback. They just don't come back. A difficulty curve that looks fine in a design document can bore one tester out in ten minutes and frustrate another out in twenty, while the team's summary slide says the game is "well tuned." This week you learn to see the players who leave, where they leave and why, before launch.

**You will be able to:**
- Explain flow and its conditions, and place a player's state on the eight-channel model from their challenge and skill.
- Compute each tester's challenge ratio level by level, apply a dropout rule, and predict who quits and where.
- Estimate a challenge ratio from playtest death counts, and say how many testers you need before the estimate means anything.
- Critique a difficulty design by its effect on the players who leave, not the average of those who stay, and choose a fix that targets the right group.

**Before class:** Mihaly Csikszentmihalyi, *Flow: The Psychology of Optimal Experience* (1990), chapter 4, "The Conditions of Flow." Jenova Chen, "Flow in Games (and Everything Else)," *Communications of the ACM* 50(4), 31-34 (2007), four pages. Celia Hodent, *The Gamer's Brain* (2017), the chapter "Engage-Ability" (pp. 135-172).

**Prerequisites from earlier courses:** [GD101 week 5, player experience goals](../../GD101-introduction-to-game-design/lectures/w05-player-experience-goals-and-the-8-kinds-of-fun.md). This week reuses its challenge ratio `R = C / S` and its flow band from 0.8 to 1.25 without re-deriving them, so reread its section 3. [GD101 week 7, playtesting](../../GD101-introduction-to-game-design/lectures/w07-playtesting-observe-dont-explain.md). [MA102 week 7, the geometric distribution](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w07-geometric-distribution-kills-until-the-drop.md), used in section 3 to read `R` from death counts. [MA102 week 12, descriptive statistics for playtests](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w12-descriptive-statistics-for-playtests.md), on why one average misleads. Looking ahead, [GD203 week 13, difficulty modes and scaling](../../GD203-combat-and-progression-design/lectures/w13-difficulty-modes-and-scaling.md) (next semester) gives the numeric levers behind the fixes in section 4. You don't need it for this week. From this course, [week 1](w01-perception-attention-memory.md) and [week 2](w02-cognitive-load-and-ui.md). Extraneous load from week 2 counts as challenge the player didn't sign up for.

**Interactive:** [Flow channel dropouts: who quits and where](../examples/w03-flow-dropout.html). Use it during section 2.

---

## 1. What flow is, and what it isn't

Psychologist Mihaly Csikszentmihalyi first described flow in *Beyond Boredom and Anxiety* (1975) and developed it for a general audience in *Flow* (1990). He studied people doing things they found deeply rewarding, such as rock climbing, chess, surgery and dance, and found that they described their best moments in similar terms. Later work with Jeanne Nakamura summarised flow as six linked experiences:

- intense, focused concentration on the present moment;
- action and awareness merging, so you stop watching yourself act;
- loss of reflective self-consciousness;
- a sense of control over what you are doing;
- distorted time, usually hours that feel like minutes;
- the activity feeling rewarding in itself.

Games designers care most about the conditions that make flow likely. The task has **clear goals**, it gives **immediate feedback**, and its **challenge matches the person's skill**. You already design the first two. Week 1 and GD101 week 12 were about feedback you can perceive in time, and quest markers and objectives are clear goals. The third condition is the subject of this lecture.

### From one channel to eight

GD101 week 5 drew flow as a band on a chart of challenge against skill. Above it lies anxiety, below it boredom. That three-zone picture is the one you'll use for the arithmetic this week. It helps to know it has a more detailed cousin.

In 1987 Fausto Massimini, Csikszentmihalyi and Massimo Carli published an **eight-channel model**, which splits the chart into eight regions by challenge and skill relative to the person's own average. Going round the chart:

| Challenge | Skill | State |
|---|---|---|
| High | Low | Anxiety |
| High | Moderate | Arousal |
| High | High | Flow |
| Moderate | High | Control |
| Low | High | Relaxation |
| Low | Moderate | Boredom |
| Low | Low | Apathy |
| Moderate | Low | Worry |

Two things in this table matter for games.

First, **not every state outside flow is bad.** Relaxation and control are what a cozy game or a victory lap is for. Arousal, where challenge slightly outruns skill, is where players learn fastest, because the gap pushes them. A well-paced game moves players through several channels on purpose, as GD101 week 5 showed with Left 4 Dead's build-up and relax cycle.

Second, **apathy sits at low challenge and low skill.** A new player facing a trivially easy tutorial they don't yet care about isn't bored in the "too good for this" sense. They are apathetic, and that is a different problem with a different fix, usually a reason to care rather than more difficulty.

### Flow is perceived, and it is personal

Challenge and skill in the model are the player's perception of them, not numbers in your spreadsheet. A player who misreads a boss's tell experiences the fight as harder than it is. A player who doesn't know a mechanic exists experiences its puzzle as impossible. That is why the extraneous load from week 2 matters here. A menu that fights the player adds challenge the player never agreed to, and it pushes them toward anxiety without making the game any more interesting.

And the band is personal. Chen's article makes the point that different players have different skills and different flow zones, so one fixed difficulty curve can't hold everyone inside theirs. The worked example puts numbers on who gets left out.

## 2. Worked example: three testers, one channel, two dropouts

### The hook

Celeste (2018) is a hard platformer that openly tells players to fail. At the start of Chapter 3, a postcard encourages players to "be proud of your death count" and says that the more you die, the more you are learning. The game counts deaths on every chapter's summary screen.

It still loses most of its players before the end. Steam records the share of the game's players who have unlocked each achievement. As of September 2026:

| Achievement (Celeste on Steam) | Share of players |
|---|---|
| Complete Chapter 1 | 70.7% |
| Complete Chapter 2 | 61.7% |
| Complete Chapter 3 | 50.6% |
| Complete Chapter 4 | 43.1% |
| Complete Chapter 5 | 38.6% |
| Complete Chapter 6 | 36.7% |
| Climb Celeste Mountain (Chapter 7) | 34.6% |

About half of the players who finish Chapter 1 never reach the summit. Some ran out of time or interest for reasons unrelated to difficulty. Achievement data can't tell you why anyone stopped. But the shape is common across games, and a UX researcher's job is to find the "why" before launch, with a handful of testers. The question is how to see, in a playtest of three people, the funnel that a million players will produce.

### The model

We reuse GD101 week 5's ratio and add one rule for quitting.

- `C_k` is the **challenge** of level `k`, on the designer's 0 to 10 scale.
- `S_k` is the tester's **skill** when they reach level `k`, on the same scale. In a real study you estimate it from play (section 3). Here it is given.
- `R_k = C_k / S_k` is the **challenge ratio**. Zones, as in GD101 week 5: **bored** below 0.8, **flow** from 0.8 to 1.25, **anxious** above 1.25.
- **Strain** is a counter that starts at 0. After each level, a level outside the band adds 1, and a level inside the band subtracts 1 (never below 0). The tester **quits** after the level where strain reaches the **quit threshold** `Q`. We use `Q = 3`.

The strain rule captures one idea. A single bad level doesn't lose a player, but a run of them does, and a good level buys some patience back. The threshold of 3 and the one-for-one recovery are teaching choices, not measured constants. You'll test how much the conclusions depend on them.

### Numbers you can check

A ten-level game. The designer's ramp:

| Level `k` | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| `C_k` | 2 | 3 | 3.5 | 4 | 5 | 5.5 | 6 | 7 | 7.5 | 8 |

Three testers, all invented.

- **Ana** has played many platformers. She starts at skill 6.0.
- **Ben** plays a few games a year. He starts at 2.2 and learns steadily.
- **Cai** has never played the genre. He starts at 1.8 and learns slowly.

Level by level. The arrow shows strain after the level.

| Level | `C` | Ana `S` | Ana `R` | Ana strain | Ben `S` | Ben `R` | Ben strain | Cai `S` | Cai `R` | Cai strain |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 2.0 | 6.0 | 0.33 bored | → 1 | 2.2 | 0.91 flow | → 0 | 1.8 | 1.11 flow | → 0 |
| 2 | 3.0 | 6.5 | 0.46 bored | → 2 | 2.9 | 1.03 flow | → 0 | 2.2 | 1.36 anxious | → 1 |
| 3 | 3.5 | 7.0 | 0.50 bored | → 3, quits | 3.6 | 0.97 flow | → 0 | 3.0 | 1.17 flow | → 0 |
| 4 | 4.0 | — | — | — | 4.2 | 0.95 flow | → 0 | 3.1 | 1.29 anxious | → 1 |
| 5 | 5.0 | — | — | — | 4.6 | 1.09 flow | → 0 | 3.4 | 1.47 anxious | → 2 |
| 6 | 5.5 | — | — | — | 5.2 | 1.06 flow | → 0 | 3.7 | 1.49 anxious | → 3, quits |
| 7 | 6.0 | — | — | — | 5.8 | 1.03 flow | → 0 | — | — | — |
| 8 | 7.0 | — | — | — | 6.4 | 1.09 flow | → 0 | — | — | — |
| 9 | 7.5 | — | — | — | 6.8 | 1.10 flow | → 0 | — | — | — |
| 10 | 8.0 | — | — | — | 7.3 | 1.10 flow | → 0 | — | — | — |

Check two cells by hand. Cai at level 5: `5.0 / 3.4 = 1.47`, above 1.25, so anxious and strain goes from 1 to 2. Ana at level 3: `3.5 / 7.0 = 0.50`, below 0.8, so strain reaches 3 and she quits.

Two of three testers quit, for opposite reasons. Ana leaves bored after level 3. Cai leaves anxious after level 6. Ben, the tester the ramp was implicitly built for, spends all ten levels in flow.

Now look at the numbers a busy team would put on a slide.

- **Pooled mean `R`.** Average all 19 ratios the three testers produced (3 from Ana, 10 from Ben, 6 from Cai). The sum is `1.29 + 10.34 + 7.89 = 19.52`, and `19.52 / 19 = 1.03`. That's the centre of the flow band. By this number, the game is perfectly tuned.
- **Late-level tuning.** Levels 7 to 10 show `R` between 1.03 and 1.10, all flow. By this number, the second half is flawless. But only Ben played it.

Both summaries are true and both mislead. Ana's boredom and Cai's anxiety cancel in the pooled mean. The late levels look good because the only tester left is the one they fit. The players the curve failed are not in the data for the levels that failed them. Statisticians call this **survivorship bias**. You met the "one average hides the shape" problem in MA102 week 12. Here it hides whole people.

One more thing, and it's the most useful line in the example. Had Ana kept playing, her skill would have reached about 8.5 by level 8, giving `R = 7.0 / 8.5 = 0.82`, inside the band. **The game got good for Ana at level 8. She left at level 3.**

### A visual you can move

Open `examples/w03-flow-dropout.html`. On the left is the familiar time chart. The designer's ramp `C` and the three testers' skill curves are drawn over levels 1 to 10, and they look like a reasonable family of lines around the ramp. On the right is the flow channel, skill on the horizontal axis and challenge on the vertical, with the band shaded. Each tester is a path of dots, one per level, and each path ends in a cross where the tester quits. The numbers panel shows each tester's strain and the pooled mean `R`.

On first load, the right chart shows Ana's path below the band ending at level 3 and Cai's above it ending at level 6, while the pooled mean reads 1.03. The left chart shows nothing alarming. Turn on "show where they would have gone." Faded dots continue each path past the cross, and Ana's path drifts into the band at level 8. Then try the fixes in section 4. Set a start level for Ana, or an assist multiplier for Cai, and watch the crosses disappear.

### Cross-game recognition

The model gives you a way to read any funnel. Turn a list of "share of players who reached step `k`" into **retention per step**, the share of players who reached step `k − 1` and then went on to reach `k`.

**Celeste (Steam, September 2026).** Chapter to chapter, retention is 87.3%, 82.0%, 85.2%, 89.6%, 95.1% and 94.3%. The losses are largest early, around Chapters 2 and 3, and then retention climbs above 94% for the last two chapters, which are harder.

**Cuphead (Steam, September 2026).** 76.6% of players have defeated a boss, 53.4% have defeated every boss on Inkwell Isle I, 31.4% on Isle II, 22.0% on Isle III, 18.6% have completed the casino, and 17.6% have finished the game on Normal. Retention per step is 69.7%, 58.8%, 70.1%, 84.5% and 94.6%. The heaviest losses come in the early and middle isles. The final steps keep almost everyone who reaches them.

Both funnels have the shape the three-tester table predicts. Retention *improves* as the game gets harder, because the players still present are increasingly the Bens, the people whose channel matches the curve. The Anas and Cais have already left. Read a late-game retention number as a statement about who is left, not about how well tuned the late game is.

**Designed responses.** GD101 week 5 compared four answers to "whose flow channel do we aim at?" Tetris lets players choose their starting level. flOw lets them move deeper or shallower by what they eat. Left 4 Dead's AI Director varies intensity on its own. Celeste's Assist Mode lets players slow the game. Rewritten in this week's terms, each one is a way to stop strain from accumulating for a particular kind of tester. A start level fixes Ana. Assist fixes Cai. An adaptive director tries to fix both without asking.

### Eyes-open design judgment

- **Design for the players who leave.** The testers who finish tell you the curve works for people like them. The testers who quit tell you who else you're losing. Report dropouts and their reasons first, averages second.
- **Bored and anxious need opposite fixes.** Lowering difficulty to save Cai makes Ana's problem worse. Raising it for Ana loses Cai sooner. When dropouts come from both sides, one curve can't fix it. You need entry points, options or adaptation.
- **The strain rule is a lens.** `Q = 3` and one-for-one recovery are ours. Try `Q = 5` in the interactive. Ana then quits after level 5 and Cai after level 8. The *when* moves and the *who* doesn't. That's the kind of conclusion you can trust from a toy model.
- **Leaving the band is sometimes the goal.** A hard platformer's climactic level should push into anxiety for a moment, and a reward room should sit in relaxation. The dropout rule punishes runs outside the band, not single moments. Design the runs deliberately.
- **Achievement funnels don't explain themselves.** A 30% drop at Chapter 1 might be difficulty, might be a boring opening, or might be people who bought the game in a sale and never really started. Use funnels to find where to look, and playtests to find why.

### Check yourself (worked example)

1. Add a fourth tester, Dee, with skill 3.0, 3.2, 3.4, 3.8, 4.4, 5.0, 5.6, 6.2, 6.8, 7.4 at levels 1 to 10. Compute her `R` and strain for each level. Does she quit?
2. Using the Celeste percentages, what share of the players who completed Chapter 1 went on to climb the mountain in Chapter 7?
3. The team decides to "fix the curve" by lowering every `C` by 10%. Recompute Ana's first three levels and Cai's levels 4 to 6. Who does it help, and is it enough?

<details>
<summary>Answers</summary>

1. `R`: 0.67 bored (strain 1), 0.94 flow (0), 1.03 flow (0), 1.05 flow (0), 1.14 flow (0), 1.10 flow (0), 1.07 flow (0), 1.13 flow (0), 1.10 flow (0), 1.08 flow (0). Dee finishes. Her only bored level is the first, and flow levels pay it back.
2. `34.6 / 70.7 = 0.489`, just under half.
3. Ana: `1.8/6.0 = 0.30`, `2.7/6.5 = 0.42`, `3.15/7.0 = 0.45`. Still bored, still quits after level 3, so it helps her not at all. It makes things worse for her. Cai: level 4 `3.6/3.1 = 1.16` flow, level 5 `4.5/3.4 = 1.32` anxious, level 6 `4.95/3.7 = 1.34` anxious. Tracking his strain from the start with the new values: level 1 `1.8/1.8 = 1.00` flow (0), level 2 `2.7/2.2 = 1.23` flow (0), level 3 `3.15/3.0 = 1.05` flow (0), level 4 flow (0), level 5 (1), level 6 (2), level 7 `5.4/4.0 = 1.35` (3), so he quits after level 7 instead of 6. One more level, not a fix. A flat cut is the wrong tool for a two-sided problem.

</details>

## 3. Measuring the challenge ratio in a playtest

In the example, `S` was given. In a real playtest you don't see skill or challenge. You see behaviour: attempts, deaths, time, what testers say, and when they put the controller down. You need a bridge from what you can count to `R`.

### Deaths per clear

Suppose each attempt at a level succeeds with probability `p`, and that `p` depends only on the ratio. A simple choice with the right shape is

```
p = 1 / (1 + R)
```

At `R = 1`, a tester clears half their attempts. At `R = 0.5`, two thirds. At `R = 2`, one third. From MA102 week 7, the number of failures before the first success follows a geometric distribution with mean `(1 − p) / p`. Substitute:

```
mean deaths before clearing = (1 − p) / p = R
```

With this link, **the expected number of deaths on a level equals its challenge ratio.** A flow band from 0.8 to 1.25 means "about one death per clear." Count deaths per clear across testers and you have an estimate of `R` for that level.

The unit matters. In this model, `C` is calibrated so that `R = 1` means the death count you intend. In Celeste, where a single screen can cost many attempts and a retry costs a second, the intended count is much higher than in a game with long levels and slow reloads. In practice, divide observed deaths by your intended deaths, so `R ≈ observed / intended`. The postcard in the hook is Celeste telling players what its intended count is.

### How noisy is one tester?

The geometric distribution has standard deviation `√(1 − p) / p`. At `R = 1`, where `p = 0.5`, that is `√0.5 / 0.5 = 1.41` deaths. The spread is larger than the mean. One tester dying twice on a level (`R` estimate 2.0, "anxious") and another dying zero times (`R` estimate 0, "bored") is entirely consistent with a level sitting exactly at `R = 1` for both of them.

Average over `n` testers and the standard error shrinks by `√n`. At `R = 1`:

| Testers `n` | Standard error of mean deaths |
|---|---|
| 1 | 1.41 |
| 5 | 0.63 |
| 10 | 0.45 |
| 20 | 0.32 |

With five testers, a measured mean of 1.0 is consistent with true values anywhere from about 0 to 2.3 (two standard errors either side), which spans all three zones. You need around 20 testers before a single level's death count can separate "flow" from "anxious" with any confidence. That's why difficulty tuning moves to telemetry (MMO308) once a game has many players.

Small playtests can still do better than one level at a time. Pool levels. Watch the trend across a tester's whole session, which is what the strain rule does. And use more than one signal.

### Other signals

- **Time per level against the designer's target.** Long times with few deaths often mean confusion (extraneous load) rather than difficulty.
- **Voluntary breaks and the controller going down.** The most direct dropout signal a moderated test gives you. Log the level and the minute.
- **Think-aloud remarks.** "This is easy" and "I'll just try once more" are different states. Log them against the level (GD101 week 7's observation method).
- **A one-question rating after each level.** For example, "too easy / about right / too hard." It's crude, but it's cheap and it can be plotted next to deaths. [Week 12](w12-surveys-and-interviews.md) covers how to write such questions without leading the tester.

When deaths, time and remarks agree, trust the zone. When they disagree, the disagreement is itself a finding, and usually the level is hard to *understand* rather than hard to *do*.

## 4. Fixing the curve for the right player

Each fix changes one term in the model. GD203 week 13 gives the combat multipliers behind them. Here the question is which tester each fix serves.

### Entry point: fixing Ana

Let players start further along the ramp. Put Ana at level 6 with her starting skill of 6.0, and her `R` for levels 6 to 10 becomes `5.5/6.0 = 0.92`, `6.0/6.5 = 0.92`, `7.0/7.0 = 1.00`, `7.5/7.4 = 1.01`, `8.0/7.7 = 1.04`. That is five levels in flow and no strain. The cost is that she misses whatever levels 1 to 5 teach. The usual answer is a short skill check, or a skippable tutorial that confirms the player already knows the controls.

### Assist: fixing Cai

Let players scale challenge down. Multiply every `C` by 0.75 for Cai, and his ratios run 0.83, 1.02, 0.88, 0.97, 1.10, 1.11, 1.13, 1.22, 1.22, 1.22. That is all ten levels in flow, though the last three sit near the upper edge. The cost is a design question about identity. Some players feel an assist option cheapens the achievement, and others refuse to use one that's labelled as a crutch. Celeste presents its Assist Mode plainly as a set of options. How you name and place an option is part of its UX.

### Adaptation: fixing both without asking

Let the game estimate `R` from deaths and adjust. The measurement problem from section 3 is now the game's problem. With one player and a noisy signal, an adaptive system either reacts slowly or reacts to noise. And players who notice hidden adjustment can feel patronised, as GD101 week 5 discussed.

### Which fix, when

| Dropout pattern in your playtest | Likely fix |
|---|---|
| Experienced testers bored early | Entry point, skill check, skippable tutorial |
| New testers anxious in the middle | Assist options, a gentler ramp shape, better teaching (week 7) |
| Both at once | Several of the above; a single curve won't do it |
| Long times, few deaths, confused remarks | Not difficulty. Fix clarity and extraneous load (weeks 1 and 2) |

The last row matters. Difficulty is the lever designers reach for first, and often it is the wrong one.

## In-class activity (25 minutes)

Groups of three. Each group gets the three-tester table from section 2 and a blank copy of the ramp.

1. **Redesign (10 min).** Change the ramp (you may change any `C_k`) and add at most one option: a start level, an assist multiplier, or neither. Your goal is to keep all three testers to the end with `Q = 3`.
2. **Check (10 min).** Recompute `R` and strain for all three testers by hand. Then swap sheets with another group and check theirs.
3. **Report (5 min).** State your change in one sentence and name the tester it cost the most. Every change costs someone something.

Expected output: a modified ramp table, three strain columns showing no quits, and one sentence naming the trade-off.

## Common misconceptions

- **"Flow means the game should be hard."** Flow means challenge *matches* skill. For a skilled player that is hard. For a new player it is gentle. Cozy games aim deliberately at relaxation and control.
- **"If the average tester is in the band, the curve is fine."** Averages cancel boredom against anxiety and ignore the players who already left. Report each tester's path and every dropout.
- **"Late-game retention is high, so the late game is well tuned."** It is high because the players the curve failed have already gone. It tells you who is left.
- **"One tester died a lot on level 4, so level 4 is too hard."** At `R = 1`, the standard deviation of deaths is larger than the mean. One tester's count on one level is mostly noise. Pool levels and testers, and use more than one signal.

## Check yourself

1. A tester's skill is 4.0 at a level with challenge 6.0. What is `R`, and which zone is it? On the eight-channel model, if both their challenge and skill are low relative to their norms, which state is that, and what kind of fix does it suggest?
2. Eight testers die a total of 14 times while clearing level 5 once each. Estimate `R`. Assuming the true `R` is near your estimate, what is the standard error, and can you say the level is outside the flow band?
3. A game's Steam achievements show 80% beat level 1, 60% beat level 2 and 57% beat level 3. Compute retention per step. What would you look at first, and why can't the achievement data alone answer it?
4. With `Q = 2` instead of 3, recompute when Ana and Cai quit. Does Ben still finish?

<details>
<summary>Answers</summary>

1. `R = 6.0 / 4.0 = 1.5`, anxious. Low challenge with low skill is apathy. The fix is usually a reason to care, such as stakes or curiosity, rather than a change in difficulty.
2. Mean deaths `14 / 8 = 1.75`, so `R ≈ 1.75`. With `p = 1/2.75 = 0.364`, SD `= √0.636 / 0.364 = 2.19`, and SE `= 2.19 / √8 = 0.78`. Two standard errors below 1.75 is about 0.2, well inside the band, so no, you can't yet say it's outside. You need more testers or pooled levels.
3. 60/80 = 75% and 57/60 = 95%. Look at level 2 first, since a quarter of the players who beat level 1 never beat it. The data can't say whether level 2 is too hard, boring, confusing, or just where people who were never committed drifted away. A playtest of level 2 with think-aloud and death counts can.
4. Ana: strain 1, 2, so she quits after level 2. Cai: level 1 flow (0), level 2 anxious (1), level 3 flow (0), level 4 anxious (1), level 5 anxious (2), so he quits after level 5. Ben has zero strain throughout and finishes.

</details>

## Lab hook

[Lab 03, flow playtest and dropout report](../labs/lab03.md). You run a moderated playtest of a short game with three to five testers, log deaths, time and remarks per level, estimate each tester's `R` with the starter script, apply the strain rule, and compare its predicted quits with where your testers actually stopped or wanted to. Deliverable: the data file, the channel plot and a dropout report of two pages.

## Sources

- Csikszentmihalyi, M. (1975). *Beyond Boredom and Anxiety*. Jossey-Bass. Csikszentmihalyi, M. (1990). *Flow: The Psychology of Optimal Experience*. Harper & Row. Summary via Wikipedia, "Flow (psychology)."
- Nakamura, J. & Csikszentmihalyi, M., the six components of flow, via Wikipedia, "Flow (psychology)."
- Massimini, F., Csikszentmihalyi, M. & Carli, M. (1987). The eight-channel model (arousal, flow, control, relaxation, boredom, apathy, worry, anxiety), via Wikipedia, "Flow (psychology)."
- Chen, J. (2007). "Flow in games (and everything else)." *Communications of the ACM*, 50(4), 31-34. Different players have different flow zones; player choice over dynamic difficulty.
- Steam global achievement statistics for Celeste (app 504230), retrieved September 2026 from the Steam Web API and the Steam Community achievements page. Complete Chapter 1: 70.7%; Chapter 2: 61.7%; Chapter 3: 50.6%; Chapter 4: 43.1%; Chapter 5: 38.6%; Chapter 6: 36.7%; Climb Celeste Mountain: 34.6%. These figures drift over time.
- Celeste Wiki, "Achievements" and "Postcards" (celeste.ink, accessed September 2026). Chapter names and achievement conditions; the Chapter 3 postcard about being proud of your death count.
- Steam global achievement statistics for Cuphead (app 268910), retrieved September 2026. Defeat a boss: 76.6%; defeat every boss in Inkwell Isle I: 53.4%, II: 31.4%, III: 22.0%; complete the Casino: 18.6%; complete the game on Normal: 17.6%.
- Hodent, C. (2017). *The Gamer's Brain*. CRC Press. Chapter "Engage-Ability."
- The ramp, the three testers, the strain rule with `Q = 3`, the link `p = 1/(1 + R)` and the flow band edges (from GD101 week 5) are teaching models, not measurements of any game.

## Interactive spec: examples/w03-flow-dropout.html

**Purpose.** Plot challenge against skill for three testers, show who drops out and where, and show that pooled averages and late-level data hide the dropouts.

**The one insight the visual must make obvious.** On the flow-channel chart, two of the three tester paths leave the band and end in a cross, one below and one above, while the pooled mean `R` in the numbers panel sits at 1.03, inside the band.

**Layout.** Two charts side by side at 1280px, stacked at 390px (channel chart first on mobile). Controls and numbers panel below.

- Left, "Over levels": x axis level 1 to 10, y axis 0 to 10. The ramp `C_k` as a thick line with square markers (after multipliers). Each tester's `S` as a thin line with that tester's marker. Lines stop at the quit level; with "show where they would have gone" on, continue as dashed and faded.
- Right, "Flow channel": x axis skill 0 to 10, y axis challenge 0 to 10. Shade the band between `y = lo × x` and `y = hi × x` (defaults 0.8, 1.25). Label "anxious" above and "bored" below. Each tester is a path of dots at `(S_k, C_k)` joined in level order, with a number label on each dot. The quit level gets a cross marker and the label "quits after level k". With "show where they would have gone" on, continue the path in faded dots.

**Data (defaults).**

- `C = [2, 3, 3.5, 4, 5, 5.5, 6, 7, 7.5, 8]`.
- Ana `S = [6.0, 6.5, 7.0, 7.4, 7.7, 8.0, 8.3, 8.5, 8.7, 8.9]`.
- Ben `S = [2.2, 2.9, 3.6, 4.2, 4.6, 5.2, 5.8, 6.4, 6.8, 7.3]`.
- Cai `S = [1.8, 2.2, 3.0, 3.1, 3.4, 3.7, 4.0, 4.3, 4.6, 4.9]`.
- Skill is indexed by levels played, not by level number. A tester who starts at level `L` has `S` equal to their first value at level `L`, their second at `L + 1`, and so on.

**Controls.**

- Quit threshold `Q`: slider 1 to 8, default 3.
- Band edges: `lo` 0.5 to 1.0 (step 0.05, default 0.8), `hi` 1.0 to 2.0 (default 1.25), in an "advanced" section.
- Per tester: start level (1 to 10, default 1) and challenge multiplier (0.5 to 1.5, step 0.05, default 1.0), plus a visibility toggle.
- Global ramp editor: ten number inputs or draggable points for `C_k`, and a "scale all C" multiplier (0.5 to 1.5, default 1.0).
- Toggle "show where they would have gone."
- "Add tester" (up to 5): editable name and ten skill values; preload the Dee example from Check yourself as an option.
- Presets: "Default: two dropouts", "Start Ana at level 6", "Assist 0.75 for Cai", "Lower all C by 10%", "Q = 5".
- Reset.

**Formulas.**

- For each tester, for each level played `k` from their start level: `c = C_k × global × tester multiplier`; `R = c / S`; zone bored if `R < lo`, anxious if `R > hi`, else flow. Strain: `+1` outside the band, else `max(0, strain − 1)`. Stop after the level where strain first reaches `Q`.
- Pooled mean `R` = mean of all `R` values from levels actually played, all testers.
- Per-level mean `R` among testers still playing, shown as a small row of cells under the left chart (blank if nobody is playing).
- Survivors per level (count), shown in the same row.

**Numbers panel.** Per tester: levels played, quit level or "finished", zone counts, final strain. Global: pooled mean `R`, number of dropouts, and a sentence built from the data, for example "2 of 3 testers quit. Pooled mean R = 1.03 (flow)."

**Test values.**

- Defaults, `Q = 3`: Ana plays 3 levels, `R` 0.33, 0.46, 0.50, quits after level 3. Ben plays 10, `R` 0.91, 1.03, 0.97, 0.95, 1.09, 1.06, 1.03, 1.09, 1.10, 1.10, finishes. Cai plays 6, `R` 1.11, 1.36, 1.17, 1.29, 1.47, 1.49, strain 0, 1, 0, 1, 2, 3, quits after level 6. Pooled mean `R` over 19 levels = 1.03 (1.0276 unrounded, from a sum of 19.524).
- Ana with "show where they would have gone": `R` at level 8 = 7.0 / 8.5 = 0.82 (flow).
- Ana start level 6: `R` 0.92, 0.92, 1.00, 1.01, 1.04, finishes.
- Cai multiplier 0.75: `R` 0.83, 1.02, 0.88, 0.97, 1.10, 1.11, 1.13, 1.22, 1.22, 1.22, finishes.
- `Q = 5`: Ana quits after level 5, Cai after level 8, Ben finishes.
- `Q = 2`: Ana quits after level 2, Cai after level 5, Ben finishes.
- Global scale 0.9: Ana still quits after level 3; Cai quits after level 7.
- Dee `S = [3.0, 3.2, 3.4, 3.8, 4.4, 5.0, 5.6, 6.2, 6.8, 7.4]`: first `R` 0.67 (bored), then all flow, finishes.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`, light and dark. Testers differ by colour and marker shape (circle, triangle, square, diamond, star). Zones differ by fill pattern as well as colour. The quit cross is large and labelled in text. All controls keyboard operable. Respect reduced motion (no animated path drawing when it is set; otherwise a short draw-in on load is allowed but must not delay the first readable frame). No game art, logos or screenshots.
