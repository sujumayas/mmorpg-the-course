# PR101 · Week 06 — Estimation and Why It Fails

**Why this matters:** Every plan you made in week 4 rests on estimates, and estimates are almost always wrong in the same direction. You can't make them right. You can measure how wrong your team usually is, understand why "most of our tasks were on time" and "we finished late" are both true, and set your buffer and your cut line from that measurement instead of from hope.

**You will be able to:**
- Compute estimate ratios for a plan and summarize them with the median, the mean, percentiles and the whole-plan ratio.
- Explain, with the skew penalty `e^(σ²/2)`, why a team whose typical task is on time can still finish a plan 50% late.
- Compare two ways of writing a plan by their spread and their plan ratio, and compute the buffer each one needs.
- Turn a point estimate into a range from past data, and critique an estimate that has no range.

**Before class:** Clinton Keith, *Agile Game Development* (2nd ed., 2020), the chapters on estimation and planning (about 25 pages). Steve McConnell, *Software Estimation: Demystifying the Black Art* (2006), chapter 4 on where estimation error comes from (about 20 pages, library copy). Bring your lab 04 scope sheet with its estimates and your MVP actuals.

**Prerequisites from earlier courses:** [PR101 week 4, scope and cut lists](w04-scope-mvp-vertical-slice-cut-lists.md) (the buffer `b`, the cut line and the overrun `m`, which this week replaces with data). [PR101 week 1, team capacity](w01-roles-on-a-game-team.md) (coordination hours, one reason estimates run long). [MA101 week 5, logarithms](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w05-logarithms-how-many-levels-until.md) (why ratios belong on a log scale). MA102 runs alongside this course. Its [week 12, descriptive statistics](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w12-descriptive-statistics-for-playtests.md) covers medians, percentiles and skew in full, and its [week 5, variance](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w05-variance-and-swingy-designs.md) defines the standard deviation. This lecture explains the parts it needs.

**Interactive:** [examples/w06-skewed-estimates.html](../examples/w06-skewed-estimates.html). Keep it open during section 2. It loads an invented earlier cohort's plans by default and accepts your own.

---

## 1. What an estimate is, and how to score one

An **estimate** is a prediction of how much work a task will take, in person-hours. A person-hour is one person working for one hour. (Week 4 added these up for the whole team and called the total team-hours. It's the same unit.) An estimate is not a promise and it's not a target. A **target** is what you'd like ("the title screen should take an hour"). A **commitment** is what you agree to deliver. Teams get into trouble when a target is written down in the estimate column and then treated as a prediction.

### The ratio

After a task is done, you know its **actual**, the hours it really took. Score the estimate with one number:

```
r = actual / estimate
```

`r = 1` means the estimate was exact. `r = 2` means the task took twice as long. `r = 0.5` means it took half as long.

Use a ratio, not a difference. Being 2 hours off on a 1-hour task is a disaster, but on a 20-hour task it's excellent. The ratio treats both fairly.

### Ratios live on a log scale

Here's a subtlety that matters later. On an ordinary number line, `r = 0.5` sits 0.5 below 1 and `r = 2` sits 1 above it. But they're the same size of mistake: one is "half as long", the other "twice as long". A log scale fixes this. On a log scale, 0.5, 1, 2 and 4 are equally spaced, because each is double the one before. MA101 week 5 showed that logarithms turn multiplying into adding, and that's what you want here, since estimate errors multiply.

The ratio also can't go below 0, but it has no upper limit. A task can't take less than no time. It can take five times as long as you thought. This lopsidedness is called **skew**, and it is the main reason plans run late even when most tasks don't. Section 2 shows how.

## 2. Worked example: most tasks on time, the plan 50% late

### The hook

Players learn to read a game's announced release date as a lower bound. Two famous cases, scored as ratios:

- **The Last Guardian.** Sony announced it at E3 in June 2009 with a planned release in 2011. It shipped on 6 December 2016. Even if you read "2011" as the last day of that year, the game took about 2.9 times as long as announced, and about 4.7 times if you read it as 1 January 2011.
- **Duke Nukem Forever.** When Take-Two bought the publishing rights in December 2000, it hoped to release the game the following year. It shipped in June 2011. From Take-Two's purchase, that is a ratio of about 10.

Now try the other direction. A game that shipped in a third of its announced time would have a ratio of 0.33. One that shipped in a tenth would have 0.1. Try to name one. You'll struggle, and the reason isn't only that studios announce late. A task can't take less than no time, but it can take ten times as long as planned. Ratios pile up just under 1 and trail off far above it.

That asymmetry does something that surprises almost every team the first time they measure it. It makes plans run late even when most of the tasks in them don't. This worked example shows how, with numbers you can check.

### The model

Score every finished task with its ratio, then summarize the list of ratios in four ways:

```
r = actual / estimate                     one task's ratio
median = middle ratio when sorted         the typical task
p10, p90 = 10th and 90th percentile       a range covering 80% of tasks
plan ratio R = Σ actual / Σ estimate      the whole plan
mean r ≈ G × e^(σ²/2)                     why R sits above the median
buffer needed  b = 1 − 1/R                from week 4's P = (1 − b) × C
```

- A **percentile** is a position in the sorted list. The 90th percentile, p90, is the value that 90% of ratios fall below. To compute the `p`-th percentile of `n` sorted values, set `h = (n − 1) × p` and move the fraction `h − floor(h)` of the way from the value at position `floor(h)` to the next one, counting positions from 0. This is the same linear method MA102 uses.
- The **plan ratio** `R` weights each task by its size. It's the one that decides whether you finish, because your deadline cares about total hours, not about how many tasks were on time. Week 4's single overrun `m` was a guess at `R`.
- `G` is the **geometric mean**: take the natural log of every ratio, average the logs, and convert back with `e^x`. For skewed ratios it sits near the median.
- `σ` (sigma) is the standard deviation of the logs of the ratios, a measure of how wide the spread is on the log scale.
- `e^(σ²/2)` is the **skew penalty**. When ratios spread evenly on a log scale (a shape called **log-normal**), the ordinary mean equals the geometric mean times this factor. It's always at least 1, and it grows fast as the spread grows: 1.02 at `σ = 0.2`, 1.13 at `σ = 0.5`, 1.38 at `σ = 0.8`.
- `b` is the buffer that would have exactly absorbed `R`. You need `(1 − b) × R = 1`.

The line to remember is the fifth. **A team can be exactly right about the typical task and still be badly late on the plan**, because the plan adds up hours, and adding rewards the rare task that takes four times as long far more than it rewards the task that takes half as long. The plan ratio tracks the mean, and the mean sits above the median by the skew penalty.

### Numbers you can check, first by hand

Here is one team's first-evening plan: ten tasks, with what they actually took.

| Task | Estimate (h) | Actual (h) | Ratio r |
|---|---|---|---|
| a | 2 | 1 | 0.5 |
| b | 4 | 3 | 0.75 |
| c | 5 | 4 | 0.8 |
| d | 1 | 1 | 1.0 |
| e | 6 | 6 | 1.0 |
| f | 3 | 3 | 1.0 |
| g | 2 | 3 | 1.5 |
| h | 3 | 6 | 2.0 |
| i | 2 | 5 | 2.5 |
| j | 2 | 8 | 4.0 |
| **Total** | **30** | **40** | |

- Six of ten tasks took their estimate or less.
- The median is the average of the 5th and 6th ratios, `(1.0 + 1.0) / 2 = 1.0`. The typical task was exactly on time.
- The mean ratio is `15.05 / 10 ≈ 1.51`. Three late tasks pull it up.
- The plan ratio is `R = 40 / 30 ≈ 1.33`. The plan ran a third over.

Ask the team how estimating went and they'll say "pretty well, most things were on time or early". They're right. They also finished 10 hours late on a 30-hour plan. The early tasks saved 3 hours in total (tasks a, b and c). The late tasks cost 13 (tasks g to j). The savings are capped, because a 2-hour task can save at most 2 hours. The losses aren't.

### Numbers you can check, from a whole cohort

Now a bigger dataset. It's **invented** for teaching, but shaped like real jam plans: twelve teams from a fictional earlier cohort, each with its first-evening plan and what every task actually took. Teams A to F wrote plans with no rule on task size, so tasks ranged from 1 to 10 hours. Teams G to L followed the rule week 7 will give you: split every task until it is 4 hours or less. Cut tasks have no actual, so they drop out. The full data is in [`labs/lab06-starter/jam_plans_example.csv`](../labs/lab06-starter/jam_plans_example.csv).

| Plan rule | Tasks finished | Cut | p10 | Median | p90 | Mean r | `σ` | `G` | `G × e^(σ²/2)` | Plan ratio `R` | Buffer `b` |
|---|---|---|---|---|---|---|---|---|---|---|---|
| No size rule (A-F) | 44 | 4 | 0.500 | 1.000 | 3.308 | 1.49 | 0.66 | 1.20 | 1.49 | 1.48 (302.5 / 204) | 0.33 |
| Split to 4 h (G-L) | 69 | 3 | 0.658 | 1.000 | 1.667 | 1.07 | 0.35 | 1.01 | 1.08 | 1.06 (187 / 176.5) | 0.06 |

Read it column by column.

**The median is identical.** In both groups the typical task was estimated exactly right. If you only asked "was the typical task on time?", you'd rate the two groups the same.

**The spread is not.** For teams without a size rule, one task in ten took at least 3.3 times its estimate. For the split-rule teams, the p90 is 1.67. The early side barely differs (0.50 against 0.66). The whole difference is in the tail.

**The skew penalty accounts for the gap.** For the no-rule teams, `σ = 0.66`, so the penalty is `e^(0.66²/2) = e^0.218 ≈ 1.24`, and `1.20 × 1.24 ≈ 1.49`. That matches the mean ratio, and the plan ratio of 1.48 lands right beside it. For the split-rule teams, `σ = 0.35`, the penalty is about 1.06, and the plan ratio is 1.06.

**The buffer follows.** A no-rule team needed `b = 1 − 1/1.48 ≈ 0.33`, a third of its capacity held back. Week 4's `b = 0.25` would not have been enough. A split-rule team needed only 0.06.

Check the hours too. Across teams A to F, tasks that came in early saved 30.5 hours in total, and tasks that ran late cost 129. Across teams G to L, early tasks saved 19 hours and late ones cost 29.5. Splitting didn't make the team better at guessing the typical task. It cut off the tail.

### Move it yourself

Open the interactive. The top view is a strip of dots, one per finished task, placed by ratio on a log scale, with the median marked and the p10 and p90 shown as brackets. The bottom view turns the same tasks into hours: a bar of estimated hours beside a bar of actual hours, and under them two bars for "hours saved by early tasks" and "hours lost to late tasks". Start with teams A to F. In the top view the dots look balanced around 1, about as many on each side. In the bottom view, the "lost" bar is four times the "saved" bar. On the log scale the dots look even. In hours they aren't.

Switch to teams G to L and watch the right-hand tail of the strip pull in and the two hour bars nearly match. Then open the spread explorer. It generates synthetic tasks with a median of exactly 1 and a spread `σ` you choose. Drag `σ` from 0 to 1 and watch the plan ratio climb along the curve `e^(σ²/2)` while the median never moves. After the jam, paste your own team's plan into the box.

### Cross-game recognition

The same shape, a ratio with a floor near zero and a long tail above, shows up wherever people predict how long something takes.

**Game release dates (2000s).** Rewrite the hook's cases as ratios: The Last Guardian at least 2.9, Duke Nukem Forever about 10. These are single points from the far tail, not a sample, so they can't give you a p90. What they show is that the tail exists and is very long. Nobody has an equally famous game at 0.1.

**Game completion times (HowLongToBeat).** MA102 week 12 met the same skew from the player's side. HowLongToBeat publishes both an average and a median completion time for each game, because a few players who idle or explore everything pull the average far above what a typical player takes. That is our mean-above-median gap, measured on players instead of tasks. Rewritten in our form, a player's time divided by the median time is a ratio with a floor and a tail, and the site reports the median precisely because the mean overstates the typical case.

**Student theses (Buehler, Griffin and Ross, 1994).** Psychologists asked 37 students to predict when they'd finish their senior theses. The average prediction was 33.9 days. The average actual was 55.5 days, a ratio of `55.5 / 33.9 ≈ 1.64`. Only about 30% finished by their own predicted date. The students also gave a "worst case" estimate, and the average worst case, 48.6 days, was still shorter than the average actual. Their idea of a bad outcome sat inside the typical one. This is the **planning fallacy**, a term Daniel Kahneman and Amos Tversky proposed in 1979 for the tendency to underestimate your own task times even when you know similar tasks ran long.

**Your own jam (weeks 8 and 9).** In week 8 you will log estimates and hours at every check-in. In week 9 you will load them, compute your team's plan ratio, and look at how estimates behaved as tasks progressed. That is the version of this example that counts.

Four settings, one pattern. The typical estimate is roughly right, the spread is skewed toward late, and totals inherit the skew.

### Eyes-open design judgment

The model tells you what to measure. These decisions are still yours.

- **Plan with the plan ratio, not the median.** Multiplying by the median corrects a single typical task. For a whole plan, multiply by `R`, which is at least as big whenever ratios are skewed. For a no-rule team, a 60-hour plan really needs about 89 hours.
- **Cut the tail, not the median.** Nagging people to "estimate better" moves the median, which is often already fine. Splitting tasks, prototyping the risky part first and listing hidden work (section 3) shrink `σ`, and the penalty falls with the square of `σ`.
- **Give ranges for single tasks.** For one task, the band is the honest answer. A 4-hour task under a no-rule history is really "2 to 13 hours, most likely 4". Saying "4" hides the part your teammates need to plan around.
- **Invented data teaches the shape, not your numbers.** The cohort above was built to show the pattern cleanly. Your team's median may not be 1, and your tail may be shorter or longer. Only your own log tells you, and with 10 or 20 tasks it will be noisy ([MA102 week 13](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md) explains why small samples mislead).
- **A date that can't move pushes error into scope.** If a jam deadline is fixed and `R` comes in at 1.48, the extra 48% has to come from somewhere. Week 4's cut list is where it should come from, in the order you chose while calm.

## 3. Why estimates fail

Section 2 measured *how much* estimates miss. Here is *why*, in the order you'll meet the causes in a jam.

### Optimism

When you estimate a task, you picture yourself doing it: open the file, write the function, test it, done. This is the **inside view**. It leaves out everything that isn't the task itself: the engine update that breaks your import, the teammate who needs help, the half hour you spend finding the bug in someone else's code. The thesis students knew that past theses ran late. They still pictured their own thesis going smoothly. The fix is the **outside view**: ask how long tasks *like this one* took, on average, and start from that.

### Skew

A task has more ways to go long than to go short. The best case is "it works first time", and you can't beat that by much. The worst case has no floor: a bug that takes a day to find, an art style that needs redoing. Even a perfectly unbiased estimator, whose median ratio is exactly 1, will run late on a plan, because the skew penalty `e^(σ²/2)` is always above 1. The only cure is a narrower spread. Section 2's split-rule teams show where that comes from: smaller tasks.

### Missing tasks

Your task list covers the work you thought of. It doesn't cover the work you didn't. Look at section 2's invented cohort. Not one team put bug fixing or exporting a build on its first-evening plan, and every jam team has to do both. Work nobody listed is not in any single task's ratio at all. It only shows up in the project total. Week 7's definition of done exists to drag some of it into view early.

### Coordination and interruption

Week 1's channel model charged every teammate `c` hours per channel for talking, waiting and redoing. Those hours come out of the same day as your task. If your estimate assumes four uninterrupted hours and you get three, the ratio is already 1.33 before anything goes wrong. Estimate in the hours you'll really have, not in clock hours.

### Waiting for other people

When a task needs two other tasks finished first, it can only start when the slower of the two is done. If each has a 50% chance of running late, the chance that at least one does is `1 − 0.5 × 0.5 = 75%`. Dependencies turn individual coin flips into likely delays. This is the complement rule from [MA102 week 3](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md), applied to a schedule.

### Hofstadter's law

The writer Douglas Hofstadter put the whole problem into one self-referential joke in *Gödel, Escher, Bach* (1979). His law says a task always takes longer than you expect, even when you account for the law itself. It's a joke with a real point. Knowing about the planning fallacy doesn't cure it. Measuring your own ratios does, a little.

## 4. Estimating better

None of these methods makes estimates right. Each makes them less wrong, or makes the wrongness visible early.

**Estimate small tasks.** Spread grows with task size and with how vague a task is. Split anything above 4 person-hours into pieces. Week 7 makes this a rule for your task board. Small tasks also finish often, which gives you ratios to learn from during the jam, not only after it.

**Estimate alone, then compare.** If one person says a number out loud first, everyone else anchors on it. **Planning poker**, which James Grenning described and named in 2002 and Mike Cohn later popularized, has every estimator choose a card privately and reveal at the same time. When the numbers disagree widely, the highest and lowest estimators explain their reasoning. The disagreement is the useful part. It usually means one person knows about a problem the others don't.

**Give ranges, and say what they mean.** "2 to 6 hours, most likely 3" is more honest than "3". Say what the range is: "I'd be surprised if it took less than 2 or more than 6" is roughly a p10-to-p90 range. Keep a record of how often actuals fall outside your ranges. If it's much more than one time in five, your ranges are too narrow.

**Correct with your own history.** Once you have a log, multiply new estimates by your team's ratios. For a single task, your band from p10 to p90 gives the range. For a whole plan, multiply the total by the project ratio. This is the outside view with your own team as the reference.

**Re-estimate on a schedule.** Use every checkpoint to re-estimate what's left as well as report what's done. Week 7 sets the jam logging schedule (every six hours) and lab 8 fixes the log format. This week scored each estimate once, at the start. Week 9 follows estimates through time. It introduces the **cone of uncertainty**, the textbook claim that estimates narrow toward the truth as a project goes on, and tests it on your own jam log. Do re-estimates made late in a task really get better, or does the arithmetic only make them look better?

## In-class activity (25 minutes)

Everyone, individually at first, then as a class.

1. **(5 min) Estimate.** Your lecturer lists three short in-class tasks, for example sorting a shuffled deck of cards into suits and ranks, writing the alphabet backwards from memory, and drawing a 6 × 6 maze on grid paper that a neighbour can solve. Write your estimate for each in minutes, privately. No discussion.
2. **(10 min) Do them.** Time yourself on each, in pairs, one person timing the other and then swapping.
3. **(5 min) Score.** Compute your three ratios, their median and your project ratio (sum of actuals over sum of estimates).
4. **(5 min) Class strip.** Everyone adds their three ratios as dots to one log-scale strip on the board (lines at 0.25, 0.5, 1, 2 and 4). Count dots above and below 1. Then compute the class project ratio from the sums.

Expected output: your three ratios, your median and project ratio, and a photo of the class strip. Discuss: was the class median near 1? Was the class project ratio above it? Which task had the widest spread, and why?

## Common misconceptions

- **"Most of our tasks were on time, so our estimates are fine."** The count of on-time tasks tells you about the median. Finishing depends on the plan ratio, which skew pushes above the median. In the ten-task example, six of ten tasks were on time and the plan ran 33% over.
- **"If we just try harder we'll estimate correctly."** Effort mostly moves the median, and the median is often fine already. The lateness lives in the tail. Smaller tasks and earlier prototypes of risky work shrink the tail. Trying harder doesn't.
- **"Padding every task is the same as a buffer."** Padding each task gets spent inside the task, because people work to the time they're given. A shared buffer at the end of the plan, used only when needed, protects the deadline better.
- **"The early tasks will cancel out the late ones."** They can't, in hours. A 2-hour task can come in at most 2 hours early. It can come in 6 hours late. Cancelling needs symmetry, and ratios don't have it.

## Check yourself

1. A team's five tasks have estimates 2, 2, 4, 1 and 3 hours and actuals 1, 3, 4, 3 and 3 hours. Compute each ratio, the median ratio and the plan ratio. Were "most tasks on time"? Was the plan?
2. Using the split-rule band from section 2 (p10 0.658, median 1.000, p90 1.667), give a range for a task estimated at 3 hours. Then give a corrected total for a 40-hour plan written under the same rule.
3. Your team's plan ratio last semester was 1.25. What buffer `b` would have absorbed it? With `C = 84`, what's `P`?
4. The logs of a team's ratios have `σ = 0.8` and a geometric mean of 1.0. Estimate their mean ratio. What does that say about a 50-hour plan? What would the same plan need if splitting tasks brought `σ` down to 0.4?
5. Two tasks must both finish before the build can be exported. Each has a 40% chance of running late. What's the chance the export starts late?

<details>
<summary>Answers</summary>

1. Ratios: 0.5, 1.5, 1.0, 3.0, 1.0. Sorted: 0.5, 1.0, 1.0, 1.5, 3.0, so the median is 1.0. Three of five were on time or early. The plan ratio is `14 / 12 ≈ 1.17`, so the plan ran 17% over, mostly because of the 1-hour task that took 3.
2. `3 × 0.658 ≈ 2.0` to `3 × 1.667 = 5.0` hours, most likely 3. For the plan, use the split-rule plan ratio: `40 × 1.06 ≈ 42.4` hours.
3. `b = 1 − 1/1.25 = 0.2`. `P = 0.8 × 84 = 67.2` hours.
4. `e^(0.8²/2) = e^0.32 ≈ 1.38`, so the mean ratio is about 1.38 and a 50-hour plan will likely need about 69 hours, even though the typical task is on time. At `σ = 0.4`, `e^(0.08) ≈ 1.08`, so the plan needs about 54 hours. Halving the spread cut the expected overrun from 19 hours to 4.
5. The chance neither runs late is `0.6 × 0.6 = 0.36`, so the chance the export starts late is `1 − 0.36 = 0.64`, or 64%.

</details>

## Lab / assignment hook

[Lab 06, your estimate log](../labs/lab06.md). You complete a small Python module that computes ratios, percentiles, the plan ratio and the skew penalty, test it on the invented cohort until your numbers match this lecture's table, run it on your lab 04 MVP estimates, and then re-estimate your jam task list as ranges with a buffer set from data.

## Sources

- Wikipedia, "The Last Guardian" (accessed September 2026). Announced by Sony at E3 2009 with a planned 2011 release on PlayStation 3; moved to PlayStation 4; released 6 December 2016.
- Wikipedia, "Duke Nukem Forever" (accessed September 2026). Take-Two bought the publishing rights in December 2000 and hoped to release the game the following year; released 10 June 2011 in Europe and Australia and 14 June 2011 in North America.
- HowLongToBeat, per-game statistics pages (accessed September 2026), as used in MA102 week 12. Average and median completion times reported side by side.
- Buehler, R., Griffin, D. and Ross, M. (1994). Exploring the "planning fallacy": why people underestimate their task completion times. *Journal of Personality and Social Psychology*, 67(3), 366-381. doi:10.1037/0022-3514.67.3.366 (volume, issue and pages checked against the Crossref record, September 2026). Figures as summarized in Wikipedia, "Planning fallacy" (accessed September 2026): 37 students; predicted 33.9 days, best case 27.4, worst case 48.6, actual 55.5; about 30% finished within their prediction. The same article gives the 1979 origin of the term with Kahneman and Tversky.
- McConnell, S. (2006). *Software Estimation: Demystifying the Black Art*. Microsoft Press. Background on estimates, targets and commitments.
- Wikipedia, "Planning poker" (accessed September 2026). Defined and named by James Grenning in 2002; popularized by Mike Cohn in *Agile Estimating and Planning*.
- Wikipedia, "Hofstadter's law" (accessed September 2026). From *Gödel, Escher, Bach* (1979).
- Keith, C. (2020). *Agile Game Development: Build, Play, Repeat* (2nd ed.). Addison-Wesley.
- The twelve-team plan data in `labs/lab06-starter/jam_plans_example.csv` is invented for teaching and describes no real cohort.

## Interactive spec: examples/w06-skewed-estimates.html

**The one insight.** On a log scale, estimate ratios look balanced around a median of 1, yet the plan's total runs long, because a task can come in only a little early but a lot late. The plan ratio tracks `G × e^(σ²/2)`, so shrinking the spread `σ` (by splitting tasks) does more than moving the median.

**Layout.** Two linked views, stacked on mobile (strip first), side by side above 900px, plus a data panel and a collapsible spread explorer below.

1. **Top view, the ratio strip.** A horizontal log2 axis from 0.25 to 8, gridlines and labels at 0.25, 0.5, 1, 2, 4, 8. One dot per finished task at its ratio, stacked vertically in columns when values coincide (beeswarm with deterministic placement by sorted order, no randomness). A vertical line at the median labelled "median", brackets at p10 and p90, and a dashed line at 1 labelled "on estimate". A caption counts "k of n tasks on or under estimate".
2. **Bottom view, hours.** Four horizontal bars on one linear hours scale: "Estimated" (Σ estimate), "Actual" (Σ actual), "Saved by early tasks" (Σ (estimate − actual) over tasks with actual < estimate), "Lost to late tasks" (Σ (actual − estimate) over tasks with actual > estimate). Print beside them: plan ratio `R`, mean r, median, `σ`, `G`, `G × e^(σ²/2)`, and "buffer needed b = 1 − 1/R" (0 when R ≤ 1). Linked: focusing or hovering a dot in the top view highlights that task's contribution in the saved or lost bar.
3. **Data panel.** Group selector: "Teams A-F (no size rule)" (default), "Teams G-L (split to 4 h)", "All", "Pasted". A textarea preloaded with the invented data (the 120 rows of `labs/lab06-starter/jam_plans_example.csv`, embedded inline in a `<script type="text/csv">` block). Columns `team,rule,task,estimate_h,actual_h`; blank `actual_h` means cut, and cut rows are listed as a count ("4 cut, not scored"). An "Apply" button parses pasted data into the "Pasted" group. A line of text states the default data is invented.
4. **Spread explorer.** Slider `σ` 0 to 1.2, step 0.05, default 0.6; slider n 10 to 200, default 50; reroll button. Generates `r_i = exp(σ × z_i)` with `z_i` from a seeded standard normal (Box-Muller on a fixed-seed PRNG such as mulberry32) and estimates all 2 h. Shows the synthetic strip in the top view and its numbers in the bottom view, and adds a small inset chart of `e^(σ²/2)` against `σ` (0 to 1.2) with a dot for the current synthetic plan ratio.

**Controls.** Group selector, textarea and Apply, `σ` and n sliders, reroll. All native inputs with visible labels and current values; keyboard: Tab through dots in the strip (each dot focusable with a label "task, estimate, actual, ratio").

**Formulas.**
- `r = actual / estimate`, finished rows only.
- Percentile `p`: sort; `h = (n − 1) × p`; `s[floor(h)] + (h − floor(h)) × (s[floor(h)+1] − s[floor(h)])`, using `s[n−1]` when `floor(h) = n − 1`. Median is `p = 0.5`.
- `R = Σ actual / Σ estimate`. Mean r is the arithmetic mean. `σ` is the population standard deviation of `ln r`. `G = exp(mean of ln r)`. Penalty `exp(σ²/2)`.

**Test values (default data; must match the lecture).**
- Teams A-F: n 44, cut 4, p10 0.500, median 1.000, p90 3.308, mean 1.494, `σ` 0.662, `G` 1.201, `G × e^(σ²/2)` 1.495, `R` 1.483 (302.5 / 204), b 0.326, on or under estimate 23 of 44, saved 30.5 h, lost 129.0 h.
- Teams G-L: n 69, cut 3, p10 0.658, median 1.000, p90 1.667, mean 1.074, `σ` 0.353, `G` 1.011, `R` 1.059 (187 / 176.5), b 0.056, saved 19.0 h, lost 29.5 h.
- Pasting the ten-task table from section 2 gives median 1.0, mean 1.505, `R` 1.333, saved 3 h, lost 13 h.

**Insight on first screen.** Default group A-F, so the first view shows a strip centred on 1 above a "lost" bar four times the "saved" bar.

**Accessibility and style.** Saved and lost bars use pattern as well as color; respects `prefers-reduced-motion` and `prefers-color-scheme`; palette from `templates/interactive-tokens.css`. No game names or art in the graphics.
