# MA102 · Week 12 — Descriptive statistics for playtests

**Why this matters:** After a playtest you hold a pile of numbers: clear times, deaths, survey ratings. The one number you put on the slide decides what the team changes next. Pick the wrong summary and one tester who went to answer the door can make your dungeon look 25% too long.

**You will be able to:**
- Compute the mean, median, mode, standard deviation, quartiles, interquartile range and percentiles of a small playtest dataset by hand and in code.
- Choose a measure of center and spread that fits the shape of the data, and justify the choice in one sentence.
- Detect outliers with the 1.5 × IQR rule and decide, with a reason, whether to keep, investigate or exclude them.
- Critique a playtest summary that reports a single average.

**Before class:** OpenIntro Statistics, 4th edition (Diez, Çetinkaya-Rundel & Barr, 2019, free online), chapter 2, section 2.1 "Examining numerical data". Skim the Wired article on Microsoft's Halo 3 playtest lab (Thompson, 2007), listed in Sources.

**Prerequisites from earlier courses:** [MA102 week 4, expected value](w04-expected-value-comparing-weapons.md), [week 5, variance and standard deviation](w05-variance-and-swingy-designs.md), [week 7, median and percentile waits](w07-geometric-distribution-kills-until-the-drop.md), [week 8, the normal curve](w08-dice-sums-and-the-normal-curve.md), and [week 10, the gacha mean and median](w10-pseudo-random-distribution-and-pity-timers.md). Reading plots from [MA101 week 1](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w01-functions-as-machines.md).

**Interactive:** [examples/w12-playtest-spread.html](../examples/w12-playtest-spread.html) (built from the spec at the end of this lecture). Keep it open during section 2.

---

## 1. From a known distribution to a pile of numbers

Until now, you started from a model and computed. A 25% crit, a 1% drop, 2d6. You knew the distribution, so the mean and standard deviation followed by algebra. Those were properties of a **random variable**.

A playtest turns that around. You do not know the distribution. You have a **sample**, a list of observed values, one per tester or per attempt. **Descriptive statistics** are numbers that summarize a sample: where its center is, how spread out it is, and what shape it has. They describe the data you have. They do not, by themselves, tell you how the next thousand players will behave. That leap is week 13's topic.

Playtest data comes in a few kinds, and the kind limits which summaries make sense.

- **Continuous measurements.** Clear time, time to first kill, session length. Any value in a range.
- **Counts.** Deaths, attempts, items crafted. Whole numbers, never negative, often with a long right tail.
- **Ordinal ratings.** "How difficult was the boss? 1 to 7." The order is meaningful. The gaps between numbers are not guaranteed to be equal.
- **Categories.** Class chosen, route taken, cause of death. Only counts and shares make sense.

Studios collect all four at scale. Microsoft's user research group, profiled by Wired in 2007, logged weapon choices, causes of death and death locations while testers played *Halo 3*, and turned those logs into maps of where players died. Behind every such map are the summaries in this lecture.

## 2. Worked example: the dungeon that "takes 25 minutes"

### The hook

Raiders in *World of Warcraft* live by percentiles. The third-party site Warcraft Logs scores each boss kill as a **parse**, a percentile that compares your damage with every other logged player of the same specialization on the same boss and difficulty. A parse of 50 means you beat half of them. Now suppose your raid leader shows a chart of the raid's DPS against "the average DPS for your spec". Many players with a parse of 50 will find themselves below that average. They are not bad and the numbers are not wrong. In a spread with a long tail of very high values, the middle player sits below the mean. The same thing will happen in your playtest data, and it will mislead your team unless you know why.

### The model

For a sample of `n` values `x_1 … x_n`:

```
mean                 x̄ = (x_1 + … + x_n) / n
median               the middle value of the sorted list (average the two middle values when n is even)
p-th percentile      sort the list; position h = (n − 1) × p + 1;
                     value = x_⌊h⌋ + (h − ⌊h⌋) × (x_⌊h⌋+1 − x_⌊h⌋)
quartiles            Q1 = 25th percentile, Q3 = 75th percentile
IQR                  Q3 − Q1   (the range of the middle half)
sample SD            s = sqrt( Σ (x_i − x̄)² / (n − 1) )
outlier fences       below Q1 − 1.5 × IQR or above Q3 + 1.5 × IQR
```

- The **mean** is the sample's balance point. It is the sample version of the expected value from week 4.
- The **median** splits the sorted data in half. It is the 50th percentile.
- The **standard deviation** is the typical distance from the mean, the sample version of week 5's SD. Dividing by `n − 1` instead of `n` corrects a small downward bias when you estimate a population's spread from a sample. Week 13 explains why. For now, use `n − 1` for playtest samples.
- The **interquartile range (IQR)** measures spread using only the middle half of the data.
- The **1.5 × IQR rule** is a convention, proposed by the statistician John Tukey, for flagging values far enough out to deserve a second look.

The percentile rule above is the "inclusive" linear-interpolation method. It is the default in numpy and matches `PERCENTILE.INC` in spreadsheets. Other tools use slightly different rules, so on small samples two tools can report quartiles that differ by a fraction of a unit. Always state which rule you used.

### Numbers you can check

Twelve testers ran a new five-room dungeon. Here are their clear times in minutes, sorted:

```
14  16  17  18  19  19  21  22  24  27  31  68
```

**Center.** The sum is 296, so the mean is `296 / 12 ≈ 24.67` minutes. With 12 values, the median is the average of the 6th and 7th: `(19 + 21) / 2 = 20` minutes.

**Spread.** Each value's deviation from the mean, and its square:

| Time | Deviation from 24.67 | Squared |
|---|---|---|
| 14 | −10.67 | 113.78 |
| 16 | −8.67 | 75.11 |
| 17 | −7.67 | 58.78 |
| 18 | −6.67 | 44.44 |
| 19 | −5.67 | 32.11 |
| 19 | −5.67 | 32.11 |
| 21 | −3.67 | 13.44 |
| 22 | −2.67 | 7.11 |
| 24 | −0.67 | 0.44 |
| 27 | 2.33 | 5.44 |
| 31 | 6.33 | 40.11 |
| 68 | 43.33 | 1,877.78 |
| **Sum** | 0 | 2,300.67 |

`s = sqrt(2300.67 / 11) = sqrt(209.15) ≈ 14.46` minutes.

**Quartiles.** For Q1, `h = 11 × 0.25 + 1 = 3.75`, so Q1 is three quarters of the way from the 3rd value (17) to the 4th (18): 17.75. For Q3, `h = 9.25`, a quarter of the way from 24 to 27: 24.75. So `IQR = 7` minutes.

**Fences.** `Q3 + 1.5 × IQR = 24.75 + 10.5 = 35.25`. The 68-minute run is far outside. The lower fence is 7.25, and nobody is below it.

Now compare the summaries with and without that single run:

| Summary | All 12 testers | Without the 68 | 68 replaced by 31 |
|---|---|---|---|
| Mean | 24.67 | 20.73 | 21.58 |
| Median | 20 | 19 | 20 |
| SD | 14.46 | 5.02 | 5.63 |
| IQR | 7.0 | 5.5 | 7.0 |

One tester in twelve moved the mean by almost 4 minutes and nearly tripled the SD. The median moved by 1 minute or not at all. The IQR did not move when the outlier was merely made less extreme. Look back at the squared-deviation column. The 68 alone contributes 1,877.78 of the 2,300.67 total, 82% of the variance from one row. That is how squaring works. It gives far points enormous weight.

Here is the sentence to remember from this dataset. **Nine of twelve testers finished faster than the mean.** A slide that says "the dungeon takes about 25 minutes" describes almost nobody.

The session notes explain the 68. That tester left the controller for about 40 minutes mid-run. The value is real but it does not measure the dungeon. A reasonable report reads: "Median clear time 20 minutes (IQR 17.75 to 24.75, n = 12). One run of 68 minutes excluded from timing because of a 40-minute idle period, noted in the log."

### Move it yourself

Open `examples/w12-playtest-spread.html`. The top view is a dot plot of the 12 clear times on a minutes axis, with a box plot drawn under it (box from Q1 to Q3, line at the median, whiskers to the most extreme non-outlier values, outliers as separate dots). Two markers ride above the axis, a solid one for the mean and a hollow one for the median. Drag any dot. Drag the 68 toward the pack and watch the mean marker slide left while the median barely twitches. Drag one of the middle dots and the median jumps while the mean shifts a little. The side panel shows the numbers live: mean, median, SD, Q1, Q3, IQR, fences, and "testers faster than the mean". The insight to take away is that the mean listens to every value in proportion to its distance, the median only to the order.

### Same idea elsewhere

Each case below asks the same question. *Which center describes the typical player, given the shape of the tail?*

**HowLongToBeat.** The completion-time site publishes more than an average for each game. Its detailed statistics show average and median times, plus separate "rushed" and "leisure" figures based on how submitters describe their own pace. Completion times have exactly the right tail our dungeon had: a few players who idle, explore everything, or leave the game running. Reporting the median alongside the mean is the site's defense against them.

**SteamSpy playtime.** SteamSpy's public API reports both `average_forever` and `median_forever` playtime (in minutes) for each game. Players who leave a game running for weeks (idling for trading-card drops or achievements) pull the average far above what a typical owner plays. The pair of numbers exists because the average alone is misleading for playtime.

**Genshin Impact pulls, from week 10.** The tail runs the other way here. Under the community soft-pity model, the pull that gives a 5-star has a mean of 62.3 and a median of 76. A long run of lucky early pulls drags the mean *below* the typical player, and soft pity piles everyone else up around 74 to 80. A **left-skewed** distribution (long tail to the left) has mean below median. A **right-skewed** one, like clear times or DPS, has mean above median. The direction of the tail tells you which way the mean lies.

**Warcraft Logs, again.** A percentile is a rank, so it ignores how far above you the top players are. That is why the parse is stable and the "average DPS" line is not. A single player with an extreme kill moves the average and leaves everyone's percentile almost unchanged.

### Design judgment

No summary is correct in general. Each answers a different question, and you should pick deliberately.

- **For "what will a typical player experience?"**, report the median and IQR. Times, counts and playtimes are almost always right-skewed.
- **For "how much in total?"**, the mean is the right number, because `total = mean × n`. Server load, gold entering the economy per hour, and support tickets per day all scale with the mean. The idle player who logs 68 minutes still occupies a server instance for 68 minutes. Economy designers in [MMO304](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/syllabus.md) care about means for this reason.
- **For "how bad is it for the unlucky or struggling?"**, report a high percentile. The 90th percentile clear time here is 30.6 minutes. If your design target says "nobody should need more than 35 minutes", check the percentile, not the mean.
- **Never drop an outlier silently.** Investigate it. An idle tester is noise. A tester who was lost for 40 minutes because a door was unreadable is the most important data point you collected. The fence flags the value. You decide what it means, and you write down the decision.
- **Always report n.** "Median 20 minutes" from 12 testers and from 12,000 players are different claims. Week 13 makes the difference precise.

### Check this example

1. Add a 13th tester with a time of 20 minutes to the original 12. What are the new median and mean?
2. A designer wants to report "mean ± SD" for this dungeon: `24.67 ± 14.46`. What does the lower end of that range suggest, and why is the summary a poor fit here?

<details>
<summary>Answers</summary>

1. The sorted list now has 13 values, and the 7th is 20, so the median is 20. The mean is `316 / 13 ≈ 24.31`.
2. The lower end is about 10 minutes, faster than any tester ran, while the upper end (39) sits between the 11th and 12th values. Mean ± SD fits symmetric, bell-shaped data (week 8). This data is right-skewed with one extreme value, so the range is both too wide on the left and uninformative on the right. Median and IQR describe it better.

</details>

## 3. Shape: histograms, skew and two humps

Center and spread are two numbers. The shape of the data can break both. Before you trust any summary, draw the data.

A **histogram** groups values into equal-width bins and draws a bar for how many fall in each. For small playtests, a dot plot (one dot per tester) is better, because it hides nothing. For hundreds of values, a histogram is the only readable choice. Bin width matters. Too wide and you hide features, too narrow and you see noise. Try two or three widths and keep the one that shows the same shape consistently.

Three shapes cover most playtest data.

- **Roughly symmetric.** Mean and median close together. Mean ± SD is a fair summary. Sums of many small random effects look like this (the central limit idea from week 8).
- **Right-skewed.** A long tail of high values. Mean above median. Times, deaths, playtime, gold earned. Use the median and IQR, and a high percentile for the tail.
- **Bimodal.** Two humps. Neither the mean nor the median describes anyone.

The bimodal case is the one that fools teams most. Twenty testers rated a boss's difficulty from 1 (far too easy) to 7 (far too hard), where 4 means "about right":

| Rating | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| Testers | 1 | 6 | 2 | 1 | 2 | 7 | 1 |

The mean is `82 / 20 = 4.1`. The median is 4.5. Both say "about right". Exactly one tester chose 4. The data says the boss is too easy for one group and too hard for another. That is a very different design problem. You might find the split lines up with class choice, prior experience or whether the tester found an optional item. The **mode**, the most common value (6 here), hints at the problem, but only the picture shows it.

A note on ratings. A 1-to-7 scale is ordinal. The distance from 1 to 2 may not feel the same as from 4 to 5. Many teams still report a mean rating because it is convenient. That is acceptable when you also show the distribution, and risky when the mean is the only number on the slide.

## 4. Counts, rates and fair comparisons

Playtest counts need a denominator before they mean anything.

Suppose tester A died 6 times and tester B died 3 times. If A played for 60 minutes and B for 15, then A died 6 times per hour and B 12 times per hour. B had the harder time. Before you compare, divide by exposure: time played, attempts made or rooms reached. Choose the denominator that matches the design question. "Deaths per attempt" answers "is this boss too punishing per try?". "Deaths per hour" answers "how often does a session get interrupted?".

Completion is a rate too. "8 of 12 testers beat the boss" is a completion rate of 67%. A **funnel** tracks a rate at each step: 12 entered, 11 reached room 3, 9 reached the boss, 8 won. The biggest drop between steps shows where to look first. Live-game analytics ([MMO308 week 4](../../MMO308-live-operations-analytics-and-experimentation/lectures/w04-funnels-and-churn.md)) runs exactly this on millions of players. The arithmetic is the same.

When comparing two versions of a level, compare the same summary computed the same way on the same kind of player. Mixing experienced and new testers is the fastest way to invent a difference that is not there. Week 14's A/B tests formalize this.

## In-class activity (25 minutes)

Work in pairs. A boss was tested by 15 people. Here are the attempts each needed for a first kill, sorted:

```
1  2  2  3  3  3  4  4  5  6  7  9  12  15  31
```

1. Compute the mean, median, sample SD, Q1, Q3 and IQR, using the inclusive percentile rule. (Check with a spreadsheet or numpy afterwards.)
2. Apply the 1.5 × IQR rule. Which values, if any, are outliers?
3. Draw a dot plot and a box plot by hand on the same axis.
4. The lead asks, "How many attempts does this boss take?" Write a one-sentence answer that a designer could act on, including n.
5. Name one piece of information about the 31-attempt tester you would want before deciding whether to exclude them.

Expected output: the six numbers, the plots, the sentence and the question. Pairs then swap sentences and try to find a way the other pair's sentence could mislead.

## Common misconceptions

- **"The average is the typical value."** Only for roughly symmetric data. In right-skewed playtest data, most testers are below the mean. In the dungeon, 9 of 12 were.
- **"Outliers are errors, so delete them."** Some are errors, some are the most important observation you have. Flag with the fence, then investigate and document.
- **"A bigger SD means the design is worse."** SD measures spread, not quality. A dungeon with two valid routes of different lengths should have a large spread. Ask whether the spread is intended.
- **"Percentiles and averages measure the same thing."** A percentile is a rank. It ignores how far away the extreme values are. That is why a 50th-percentile parse can sit below the mean DPS.

## Check yourself

1. Seven testers took `3, 4, 4, 5, 6, 9, 30` minutes to solve a puzzle. Compute the mean, median, Q1, Q3 and IQR (inclusive rule). Is 30 an outlier?
2. Two versions of a tutorial. Version A: median 8 minutes, IQR 2. Version B: median 8 minutes, IQR 7. What design question does the difference raise?
3. A server team asks for the "median session length" to estimate total server hours for next month. What is wrong with the request, and what should they use instead?
4. Survey ratings on a 1-to-5 scale are `1, 1, 1, 2, 5, 5, 5, 5`. Report the mean, median and mode, and say which summary you would put on the slide.

<details>
<summary>Answers</summary>

1. Sum 61, mean `61/7 ≈ 8.71`. Median is the 4th value, 5. Q1: `h = 6 × 0.25 + 1 = 2.5`, halfway between 4 and 4, so 4. Q3: `h = 5.5`, halfway between 6 and 9, so 7.5. IQR 3.5. Upper fence `7.5 + 5.25 = 12.75`, so 30 is an outlier.
2. Both have the same typical time, but B's middle half is spread over 7 minutes, so players experience B very differently from each other. Find out who is slow in B and why. It may be a readability or onboarding problem for one group.
3. Total hours equal mean session length times the number of sessions. The median ignores long sessions, which use a lot of server time, so it underestimates. Use the mean (and check a high percentile for peak planning).
4. Mean `25/8 = 3.125`, median `(2 + 5)/2 = 3.5`, mode 5. None of them describes the data, which is split between strongly negative and strongly positive. Put the distribution itself on the slide (a bar chart of counts), with n = 8.

</details>

## Lab hook

**[Lab 12: Summarizing a playtest](../labs/lab12.md).** You receive a CSV of 40 testers' times, deaths and ratings from a dungeon playtest, compute every summary in this lecture, flag and investigate outliers, and write a one-page summary for the lead designer. The same dataset returns in week 13, when you put confidence intervals on it.

## Sources

- Thompson, C. (2007). "Halo 3: How Microsoft Labs Invented a New Science of Play." *Wired* 15.09, published online 21 August 2007 (wired.com/2007/08/ff-halo-2/, re-read September 2026). Randy Pagulayan's team logged player locations, weapon fire and deaths, produced maps of where testers died and charts of how they died, and a death "heat map" of the Valhalla multiplayer level led Bungie to change its terrain.
- Warcraft Logs, rankings help page, and the third-party guide "What your WoW parse score means" (wowcoach.gg, accessed September 2026). Parse as a percentile against the same spec, boss and difficulty; colour bands at 25, 50, 75, 95, 99 and 100. Warcraft Logs is a community tool, not part of the game.
- HowLongToBeat, per-game statistics pages (accessed September 2026). Average, median, rushed and leisure completion times from user submissions.
- SteamSpy API documentation (steamspy.com/api.php, accessed September 2026). Fields `average_forever` and `median_forever`, in minutes, since March 2009. SteamSpy figures are estimates.
- Genshin Impact figures and the community soft-pity model: see the Sources section of [week 10](w10-pseudo-random-distribution-and-pity-timers.md).
- Diez, D., Çetinkaya-Rundel, M. & Barr, C. (2019). *OpenIntro Statistics*, 4th ed. Section 2.1. Definitions of mean, median, quartiles, IQR, box plots and the 1.5 × IQR outlier rule.
- Tukey, J. W. (1977). *Exploratory Data Analysis*. Addison-Wesley. Origin of the box plot and the 1.5 × IQR fences.

## Interactive spec: examples/w12-playtest-spread.html

**Insight the visual must make obvious:** dragging a single extreme value moves the mean and SD a lot and the median and IQR hardly at all, so for skewed playtest data the median describes the typical tester and the mean does not.

**Layout.** One main view plus a live number panel. On mobile the panel sits below the plot.

1. **Dot plot with box plot.** Horizontal axis in minutes, 0 to 80 (auto-extend if a dot is dragged past). Each tester is a draggable circle (pointer and keyboard: focus a dot with Tab, move with arrow keys by 1 minute, Shift+arrow by 5). Tied values stack vertically. Under the dots, a box plot: box from Q1 to Q3, a line at the median, whiskers to the most extreme values inside the fences, and any value outside the fences drawn as a hollow outlier marker. Above the axis, a solid triangle for the mean and a hollow triangle for the median, each labelled with its value. Shade the region "faster than the mean".
2. **Number panel.** n, mean, median, mode (or "none"), sample SD (n − 1), Q1, Q3, IQR, lower and upper fence, 90th percentile, and "testers faster than the mean: k of n". Values to 2 decimals.

**Controls.**
- Dataset selector: "Dungeon clear times" (default), "Boss attempts" (the in-class data), "Difficulty ratings" (the bimodal 1-7 data, with the axis switched to 1-7 and dots snapped to integers).
- Button "Add tester" (adds a dot at the median) and "Remove selected".
- Toggle "Exclude outliers from summaries" that greys outliers and recomputes the panel, showing both values side by side ("all / excluded").
- Button "Reset dataset".

**Formulas.** Mean `Σx/n`. Sample SD `sqrt(Σ(x − x̄)²/(n − 1))`. Percentile with the inclusive rule: sort, `h = (n − 1)p + 1`, interpolate between `x_⌊h⌋` and `x_⌊h⌋+1` (1-indexed). Fences `Q1 − 1.5 IQR`, `Q3 + 1.5 IQR`.

**Test values** (assert on load):
- Clear times `14 16 17 18 19 19 21 22 24 27 31 68`: mean 24.67, median 20, SD 14.46, Q1 17.75, Q3 24.75, IQR 7, upper fence 35.25, P90 30.6, faster than mean 9 of 12, outliers {68}.
- Same with 68 removed: mean 20.73, median 19, SD 5.02.
- Same with 68 changed to 31: mean 21.58, median 20, SD 5.63, IQR 7.
- Boss attempts `1 2 2 3 3 3 4 4 5 6 7 9 12 15 31`: mean 7.13, median 4, SD 7.68, Q1 3, Q3 8, IQR 5, upper fence 15.5, outliers {31}.
- Ratings (counts 1,6,2,1,2,7,1 for values 1-7): mean 4.10, median 4.5, mode 6, SD 1.97.

**First screen:** the dungeon dataset, with the mean and median triangles visibly apart and the 68 drawn as an outlier. A one-line caption states "9 of 12 testers were faster than the mean".
