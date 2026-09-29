# PR101 · Week 09 — Jam Post-Mortem

**Why this matters:** You just made a game in 48 hours, and every team in the room has a story about what went wrong. Stories are cheap and they flatter the teller. This week you replace the story with your own data: how far your estimates were off, whether they got better as the jam went on, and what that means for the plan of your final project. The chart you'll draw has a famous shape, and your data will show why that shape misleads most people who look at it.

**You will be able to:**
- Compute the total-view and remaining-view estimate ratios for every task in a jam log, and explain why the first must narrow while the second need not.
- Draw the cone of uncertainty from your class's own jam data, in two views, and read its p10, p50 and p90 bands.
- Critique the claim that estimates improve as a project progresses, using your data, one shipped game and one published study.
- Run a blameless post-mortem that ends in three changes, each with an owner and a check.

**Before class:** Todd Little, "Schedule Estimation and Uncertainty Surrounding the Cone of Uncertainty," *IEEE Software* 23(3), May/June 2006, pages 48-54 (7 pages; read the figures and the section on the cone closely). Steve McConnell's short article "The Cone of Uncertainty" on the Construx site. From the Game Developer (Gamasutra) post-mortem archive, pick any one post-mortem of a small-team game and note how many of its "what went wrong" items are about time.

**Prerequisites from earlier courses:** [PR101 week 4, scope](w04-scope-mvp-vertical-slice-cut-lists.md) (the overrun factor `m`, which you now measure), [week 6, estimation](w06-estimation-and-why-it-fails.md) (the ratio `r`, percentiles, the plan ratio `R` and the skew penalty, which this week follows through time), [week 7, task tracking](w07-task-tracking-and-definitions-of-done.md) (the ninety-ninety rule and the definition of done) and [week 8, the jam](w08-48-hour-game-jam.md) (the jam log). [MA102 week 12, descriptive statistics](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w12-descriptive-statistics-for-playtests.md) (percentiles and the median; we use the same inclusive percentile rule). [MA101 week 5, logarithms](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w05-logarithms-how-many-levels-until.md) (why ratios go on a log scale). [MA102 week 13, sampling](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md) (why one team's numbers prove little).

**Interactive:** [`examples/w09-cone-of-uncertainty.html`](../examples/w09-cone-of-uncertainty.html). Paste your team's jam log into it during section 2.

---

## 1. What a post-mortem is for

A **post-mortem** is a structured look back at a finished project, written by the team, to decide what to do differently next time. The name comes from medicine, where it means an examination after death. Games borrowed it for projects that are finished rather than dead, though both happen.

Gamasutra, the website of the print magazine Game Developer (which closed in 2013), built up a collection of more than 150 post-mortems of shipped games, going back to 1997 and written by the games' own developers under two headings: what went right and what went wrong. The site itself was renamed Game Developer in August 2021. That archive is one of your course readings. In 2016, Michael Washburn and colleagues at Microsoft Research analysed 155 of the Gamasutra post-mortems to find which practices went with good and bad project experiences, and named their paper after the two headings. The format worked well enough to be studied as data.

Most post-mortems share three weaknesses, and this week's method is built against each.

1. **Memory rewrites the jam.** By Monday, "we ran out of time" has replaced "the save system was estimated at 2 hours and took 9." You logged the second version during the jam so you wouldn't have to remember it.
2. **Stories blame people.** "Sam's level was late" is a story about Sam. "Level cards were estimated before anyone had built a level" is a fact about the process, and it can be fixed. Google's *Site Reliability Engineering* book (2016, chapter 15) calls this a **blameless** post-mortem: assume everyone acted in good faith with the information they had, and look for the process that let the problem happen. Week 14 goes further into how to write one.
3. **Lessons don't turn into changes.** A list of ten lessons changes nothing. Three changes, each owned by a named person, with a way to tell next time whether it happened, change something.

So the order is: data first, then the story, then the changes.

## 2. Worked example: your cone, drawn two ways

### The hook

CD Projekt Red announced four release dates for Cyberpunk 2077. At E3 on 9 June 2019 it said 16 April 2020. On 16 January 2020 it moved to 17 September. On 18 June 2020 it moved to 19 November. On 27 October 2020 it moved to 10 December, and the game launched that day.

Score each announcement with week 6's ratio, `actual / estimate`, applied to the time that was left. On 9 June 2019 the studio implied 312 days remained. In fact 550 did, a ratio of `550 / 312 = 1.76`. In January it implied 245 days and 329 remained: 1.34. In June it implied 154 and 175 remained: 1.14. In October it implied 44 and 44 remained: 1.00. The ratios fall 1.76, 1.34, 1.14, 1.00. Estimates that start far off and close in on the truth as the project goes on have a name, the **cone of uncertainty**, and this looks like one.

Now score the same four dates a second way. Instead of the days *left*, compare the *total* time from E3 to launch, 550 days, with the total the studio was implying at each moment. In January 2020 the implied total (9 June 2019 to 17 September 2020) was 466 days: a ratio of `550 / 466 = 1.18`. In June 2020 it was 529 days: 1.04. By this measure the June estimate was within 4 percent. By the first measure, on the same day, the date was still 14 percent short of the time that remained.

Same game, same announcements, two different answers to "how good was the estimate?" One of them flatters. This week you find out which, using the jam log your team kept in week 8, and whether the cone survives contact with your own data.

(A public release date is a business decision, not an engineer's estimate. Treat these ratios as a picture of how the dates moved.)

### The textbook cone

The cone is older than games. Barry Boehm drew it in *Software Engineering Economics* (1981), and Steve McConnell popularized it in *Software Estimation* (2006). McConnell's version puts the project's milestones along the bottom and the estimate's error up the side. At the initial concept, an estimate by a skilled estimator can be off by a factor of 4 either way: the truth lies anywhere from 0.25 to 4 times the estimate. Once the product is defined, the range is 0.5 to 2. Once the requirements and the interface design are settled, about 30% of the way through the calendar, it is about 0.8 to 1.25. The cone says estimates get better as you go. The rest of this section tests that claim.

### The model

Take one task from your jam log. It has an actual total effort `A`, known once it's done. At each checkpoint before that, the log recorded:

- `s`, the person-hours **spent** so far;
- `R̂` (R-hat), the person-hours the owner **estimated remain**.

From these, compute three numbers per checkpoint:

```
x               = s / A                 how far through the task you were (0 = start, 1 = done)
total ratio     = A / (s + R̂)           actual total ÷ estimated total
remaining ratio = (A − s) / R̂           actual remaining ÷ estimated remaining
```

Both are week 6's ratio `r = actual / estimate`, applied to different quantities, and both go on a log scale for the reason week 6 gave: 2 and 0.5 are equally bad misses. The Cyberpunk hook used them on calendar days. Here they apply to person-hours on one task. You could group checkpoints by the clock hour of the jam, but at hour 30 a task started at hour 28 is at its beginning while one started at hour 0 is nearly done. So group by `x`, how far through its own task each estimate was made, and the two are compared at the same stage.

At the first checkpoint `s = 0`, so both ratios are the same number: actual ÷ original estimate. After that they come apart, and that difference is the point of the lesson.

### Numbers you can check

Here is task T01 from lab 8's template log, an enemy spawner, estimated at 3 hours. It actually took 8.

| Hour | Spent `s` | Remaining estimate `R̂` | Estimated total `s + R̂` | `x = s/A` | Total ratio `A/(s + R̂)` | Remaining ratio `(A − s)/R̂` |
|---|---|---|---|---|---|---|
| 0 | 0 | 3 | 3 | 0.00 | 2.67 | 2.67 |
| 6 | 2 | 2 | 4 | 0.25 | 2.00 | 3.00 |
| 12 | 5 | 1 | 6 | 0.63 | 1.33 | 3.00 |
| 18 | 7 | 1.5 | 8.5 | 0.88 | 0.94 | 0.67 |
| 24 | 8 (done) | 0 | | 1.00 | | |

Check the hour 12 row. The owner had spent 5 and thought 1 hour remained, so the estimated total was 6. The actual was 8: total ratio `8/6 = 1.33`. But the actual remaining work was `8 − 5 = 3` hours against an estimate of 1: remaining ratio 3.00. The owner was *three times* too optimistic about what was left, exactly as optimistic as at hour 6. The total view says they'd nearly got it right.

Look at the total ratio column: 2.67, 2.00, 1.33, 0.94. It marches toward 1. The remaining ratio column: 2.67, 3.00, 3.00, 0.67. It doesn't march anywhere.

### Why the total view has to narrow

Write the remaining ratio as `ρ` (rho), so the actual remaining work is `ρ × R̂`. Then:

```
total ratio = (s + ρ × R̂) / (s + R̂)
```

That's a weighted average of 1 (with weight `s`) and `ρ` (with weight `R̂`). As the task goes on, `s` grows and `R̂` usually shrinks, so the average is dragged toward 1 **whatever `ρ` is**. At hour 12 in the table, `s = 5` and `R̂ = 1`, so the total ratio is five parts 1 and one part 3: `(5 + 3) / 6 = 1.33`.

This means the cone in the total view is bookkeeping. The hours already spent are known exactly, and as they become most of the total, the error in the total shrinks, even if the person estimating learns nothing at all. The honest question for a producer is the remaining view: *when someone tells me how much is left, how far off are they?*

### The class's jam, pooled

One task proves nothing. To draw both views for many tasks you need the hours spent at every checkpoint, which is why lab 8's log records `spent` as well as the remaining estimate. The lab gives you a sample log in that format: 8 teams, 52 tasks, 184 rows. It is invented, like week 6's cohort, but built to follow the pattern in Todd Little's published data (below) rather than the textbook cone. Pool every checkpoint of every finished task, sort them into four bins by `x`, and take the 10th, 50th and 90th percentiles of each ratio in each bin (week 6's percentile rule). The **spread** is p90 ÷ p10: how many times bigger a bad miss is than a good one.

| `x` bin | Points | Total ratio p10 / p50 / p90 | Total spread | Remaining ratio p10 / p50 / p90 | Remaining spread |
|---|---|---|---|---|---|
| 0.00-0.25 | 58 | 0.82 / 1.50 / 2.50 | 3.04 | 0.79 / 1.50 / 2.73 | 3.45 |
| 0.25-0.50 | 14 | 1.01 / 1.15 / 1.55 | 1.53 | 1.02 / 1.27 / 2.33 | 2.28 |
| 0.50-0.75 | 24 | 1.00 / 1.25 / 1.38 | 1.38 | 1.00 / 2.00 / 3.00 | 3.00 |
| 0.75-1.00 | 15 | 0.94 / 1.05 / 1.18 | 1.25 | 0.78 / 1.50 / 3.00 | 3.83 |

(Spreads are computed from unrounded percentiles, so the last digit can differ from dividing the rounded ones.)

The total view is a cone: spread 3.04, then 1.53, 1.38, 1.25. The remaining view is a pipe: 3.45, 2.28, 3.00, 3.83. No trend at all. At the end of a task, when the owner says "about an hour left," the truth in this sample ranges from under an hour to three hours, just as widely as at the start. The textbook cone predicts the remaining view should narrow too. This sample was built to follow Little's published data, which didn't, so it can't settle which shape is real for students. Your class's pooled log is the first real evidence you'll have, and the in-class activity looks at it.

Three more numbers from the same log. The median of actual ÷ original estimate across the 47 finished tasks is **1.50**: the typical task took half again as long as first estimated. The plan ratio, week 6's `R = Σ actual ÷ Σ original estimate` over the same tasks, is `222.5 / 132` ≈ **1.69**. It sits above the median for the reason week 6 gave: the tail of long overruns adds hours that the early tasks can't give back. And **6** open rows claim 0 hours remaining on a task that wasn't done yet. That is week 7's ninety-ninety rule, counted.

### The visual

Open the interactive. The left panel is the total view: every checkpoint as a dot, `x` along the bottom, total ratio up the side on a log scale, with the p10, p50 and p90 lines per bin. It is a cone, narrowing to the right. The right panel is the remaining view of the same dots. It is a pipe.

Hover over any dot and the same checkpoint lights up in the other panel. Pick task C02 at hour 12, the dot at `x = 0.80` in the left panel sitting just above the 1.0 line at 1.15. Its owner had spent 6 hours and said half an hour was left. The task took 7.5. Watch its twin in the right panel sit at 3.0. The same moment looks like a 15 percent miss in one view and a three-fold miss in the other.

Then paste your own team's log into the box below the charts. Your cone will be noisier than the sample, because you have fewer tasks. Toggle "Cyberpunk 2077" to overlay the four announcements from the hook, and "cut tasks" to see where the tasks you abandoned would sit.

### Cross-game recognition

**Cyberpunk 2077, both views.** In this lecture's form, with the clock starting at E3 2019, the remaining ratios from the hook are 1.76, 1.34, 1.14, 1.00 and the total ratios are 1.76, 1.18, 1.04, 1.00. The total view narrows faster, for the reason in the formula above: by June 2020 more than two thirds of the calendar from E3 to launch had passed (`x = 0.68`), so the known part swamped the error. In this one project the remaining view narrowed too. But the last date was held while the work was not finished: the console versions launched with so many problems that Sony removed the game from the PlayStation Store eight days later (week 10 returns to this). One project can't settle whether the narrowing came from better estimating or from a date that stopped moving.

**Landmark Graphics, 1999-2002 (Todd Little, *IEEE Software*, 2006).** Little had weekly estimates of the delivery date for all 106 software projects at his company over three years, from experienced teams. The actual ÷ initial estimate followed a skewed distribution, a lognormal, with a median of about 1.8 and a mean of about 2.0, and p90 ÷ p10 was 3.25. That's close to your sample's first-bin numbers. When he plotted actual total ÷ estimated total against time, he got a cone. When he plotted actual remaining ÷ estimated remaining at each project phase, the distributions were nearly identical at every phase, a factor of about 3 to 4 between p10 and p90 throughout. His data showed a pipe where everyone expected a cone.

**McConnell's own warning.** The textbook cone above is a factor of 4 either way at the initial concept, narrowing as the project is defined. McConnell adds a condition that is easy to miss. The cone is the *best case*, the accuracy skilled estimators can reach, and it narrows only when the team makes decisions that remove variability: fixing the scope, saying what they won't do, designing the interface. A project that doesn't make those decisions keeps its uncertainty to the end. He calls that a cloud rather than a cone. Little's pipe is what a cloud looks like in data.

Your jam, a AAA launch and 106 business software projects, drawn two ways each. In every case, the total view narrows by arithmetic, and the remaining view narrows only if something about the work changes.

### Eyes-open judgment

What should a producer do with this?

- **Ask which view someone is quoting.** "We're 90 percent sure of the total" and "we're sure it's an hour left" are different claims. When a teammate says "an hour left", the remaining view's band for your class is the honest range. In the sample, at `x` above 0.75, that is 0.78 to 3.0 hours.
- **Update week 6's numbers with your own.** Week 6 set your buffer from an invented cohort's plan ratio. Replace it with your team's jam plan ratio, and use the right number for each job, as week 6 did. For a whole plan, multiply the total by the plan ratio `R`: in the sample, an MVP estimated at 30 person-hours needs `30 × 1.69 ≈ 51`, and the buffer that absorbs it is `b = 1 − 1/1.69 ≈ 0.41`. The median (1.50 here) would have planned 45 and run out. For one card, use the median for the most likely value and the class's p10 to p90 for its range.
- **Narrow the cone on purpose.** Tasks don't become predictable by getting older. They become predictable when you split them (week 7), prototype the risky part first, and decide what you won't do. A card that is still "about an hour left" for the third checkpoint in a row isn't converging. Split it or cut it.
- **Beware survivorship.** Cut tasks never finished, so they have no actual and drop out of the table. In the sample, all five cut tasks had been estimated at 4 hours and had already used between 4.5 and 8.5 hours when they were cut. They were the worst overruns in the log, and the table doesn't see them. Every chart of finished work flatters the estimates. The interactive draws cut tasks as lower bounds for that reason.
- **Small samples lie.** A four-person team logs perhaps 15 tasks. The p90 of 15 values rests on one or two tasks (MA102 week 13). Pool the class's logs for the bands, and use your team's own numbers only for the median and the plan ratio.
- **Don't punish the log.** The moment estimates are graded on accuracy, people pad them, and the data stops telling you anything. That is why the jam log is graded on completeness only.

## 3. Running the post-mortem

Hold it within a week of the jam, while the build still runs on everyone's machine. Budget 90 minutes for a four-person team. The producer runs it, and someone else takes notes.

| Time | Step | Output |
|---|---|---|
| 15 min | **Data.** Run lab 9's script on your log. Put the cone table, the median ratio, the plan ratio, the zero-remaining count and the freeze record on screen. | The numbers everyone agrees on |
| 15 min | **Timeline.** Walk the checkpoints (0, 12, 24, 36, 42, 48) using the board photos. At each one: what was playable, what was cut, what surprised us. | A one-line entry per checkpoint |
| 30 min | **Went right, went wrong.** Each person writes up to three of each on sticky notes, silently, for 5 minutes. Then group them. Each item must point to evidence: a log row, a commit, a board photo. | 3-5 of each, with evidence |
| 20 min | **Three changes.** For the final project, pick three changes. Each has an owner and a check: how you'll know in week 13 whether it happened. | Three changes |
| 10 min | **Check the changes against the data.** Does each change address something the numbers show, or something one person felt? | Revised changes |

### What counts as evidence

"We ran out of time" is a feeling. Here's the same feeling as evidence, from a team whose log looks like the sample:

- Our plan ratio was 1.69 (median 1.5), and our cut line was drawn with no buffer.
- The MVP loop was first playable at hour 18, six hours after the hour-12 trigger; we didn't stop slice work as the trigger said.
- Two of our cards were at "1 hour left" for three checkpoints in a row.
- Four changes went in after the feature freeze; one broke the export, found at hour 45.

Each of these points to a change. Draw the cut line with a buffer sized from the measured plan ratio. Obey the hour-12 trigger, with a named person who calls it. Split any card that reports the same remaining estimate twice. Tag every working build from hour 30 on.

### Blameless, in practice

Write every item about the work, not the person. Compare:

| Blame | Blameless |
|---|---|
| "Ana's save system was late." | "The save card was estimated at 2 h before anyone had tested the engine's file API; it took 9 h." |
| "Ben broke the build at hour 45." | "A change went into main after content lock without the build owner playing it; nothing stopped it." |

The blameless version is longer and more useful. The first one tells Ana to feel bad. The second tells the team to prototype unfamiliar APIs before estimating them, and it applies to everyone.

### Changes that can be checked

A change needs a verb and a check. "Communicate better" has neither. Compare:

- "Hold back a buffer of `b = 1 − 1/R` from our jam plan ratio (`R = 1.69`, so 41% of capacity) when drawing the cut line. Owner: producer. Check: the week 13 cut line sits at 59% of capacity, and the calculation is written on the board."
- "Any card with the same remaining estimate at two checkpoints in a row gets split at the next check-in. Owner: producer. Check: count of such cards in the final project's log is zero at week 13."
- "From content lock on, main is changed only by the build owner. Owner: build owner. Check: `git log` after the lock shows one author."

Week 14 looks at what happens to these changes across projects, and how to tell if a lesson was learned or just written down twice.

## In-class activity (30 minutes)

In your jam teams, with your laptops and your jam log.

1. **Run the numbers (10 min).** Run lab 9's script on your team's log. Paste the log into the interactive. Write down your median ratio, your plan ratio (lab 9 step 10), the spread in your first and last bins in both views, and your zero-remaining count.
2. **Find your worst task (5 min).** Find the finished task with the highest ratio of actual to original estimate. Using the board and Git history, write one sentence on why it ran over, without naming a person.
3. **Cut tasks (5 min).** List every task you cut, with its spent hours at the time. For each, write the lower bound on its ratio (spent ÷ original estimate). How would including them change your median?
4. **Pool (10 min).** Each team adds its log to the class folder. The lecturer runs the script on the pooled log and shows the class cone. Is the class's remaining view a pipe, like Little's, or does it narrow? Discuss one reason your class might differ from the sample.

Expected output: your team's five numbers, one blameless sentence about your worst task, a lower-bound list for cut tasks, and a class-level observation about the pooled cone.

## Common misconceptions

- **"Estimates get more accurate as the project goes on."** The *total* estimate does, by arithmetic, because the spent part is known. The estimate of what *remains* improves only if the team does something that removes uncertainty. In Little's data it stayed about as wide at every phase.
- **"Our estimates were bad, so we should estimate more carefully."** Careful estimating doesn't remove the spread. Calibrating (scaling the plan by your plan ratio) removes the bias, and splitting and prototyping reduce the spread.
- **"We cut the tasks that were going badly, so our estimates look fine."** That's survivorship. The cut tasks were the misses. A table without them flatters you.
- **"A post-mortem is where we say what went wrong."** A post-mortem is where you decide what to change. The list of what went wrong is an input.

## Check yourself

1. A task has `A = 6`. At a checkpoint, `s = 4` and `R̂ = 0.5`. Compute `x`, the total ratio and the remaining ratio. Which one should a producer believe when deciding whether to cut the task's follow-up work?
2. Show that if the remaining ratio is exactly 2 at every checkpoint, the total ratio still approaches 1 as `s` grows. Compute the total ratio for `s = 1, 5, 20` with `R̂ = 1`.
3. Your team's jam log gives a median actual ÷ estimate of 1.4, a plan ratio of 1.7 and a p90 of 2.6. Your final project's MVP cards add up to 50 person-hours. How many person-hours should you plan for the MVP, and what buffer does that imply? One MVP card is estimated at 4 hours. What is its most likely actual, and how bad could it reasonably get?
4. A team cut three tasks, each estimated at 3 hours, after spending 3.5, 5 and 6 hours on them. What is the smallest possible ratio for each? What does that do to the team's median if its finished tasks had ratios 0.8, 1.0, 1.2, 1.3, 1.6?
5. Rewrite "Communication was bad and the art was late" as a blameless went-wrong item with evidence, and one change with an owner and a check.

<details>
<summary>Answers</summary>

1. `x = 4/6 = 0.67`. Total ratio `6 / (4 + 0.5) = 1.33`. Remaining ratio `(6 − 4) / 0.5 = 4.0`. The producer should believe the remaining view: the owner said half an hour and it took two, a four-fold miss. The total view makes it look like a 33% miss because two thirds of the work was already done.
2. Total ratio `= (s + 2 × 1) / (s + 1)`. For `s = 1`: `3/2 = 1.5`. For `s = 5`: `7/6 ≈ 1.17`. For `s = 20`: `22/21 ≈ 1.05`. The owner is always twice too optimistic about what's left, yet the total ratio heads to 1.
3. Plan for `50 × 1.7 = 85` person-hours, using the plan ratio because the deadline cares about total hours. The buffer is `b = 1 − 1/1.7 ≈ 0.41`. Scaling by the median would give 70 and leave you 15 hours short, because the median ignores the tail that the total inherits (week 6). For the single card, the median gives the most likely actual, `4 × 1.4 = 5.6` hours, and the p90 gives a bad but plausible case, `4 × 2.6 = 10.4` hours.
4. Lower bounds `3.5/3 = 1.17`, `5/3 = 1.67`, `6/3 = 2.0`. Their true ratios are at least these, since the tasks weren't finished. Finished only: median of 0.8, 1.0, 1.2, 1.3, 1.6 is 1.2. With the three cut tasks at no less than their lower bounds, the eight values sorted are at least 0.8, 1.0, 1.17, 1.2, 1.3, 1.6, 1.67, 2.0, so the median is at least `(1.2 + 1.3)/2 = 1.25`, and higher if the cut tasks would have run longer. Leaving them out understates the bias.
5. Example. Went wrong: "Art cards for level 2 were estimated at hour 0 before the art pipeline was tested; the first sprite reached the engine at hour 20 after two import problems (board photo at hour 24; commits `a1b2`, `c3d4`)." Change: "Import one placeholder asset of each type through the full pipeline in the first two hours, before estimating art cards. Owner: art lead. Check: the final project log shows art cards created after the pipeline test commit."

</details>

## Lab / assignment hook

[Lab 09, your cone and your post-mortem](../labs/lab09.md). You write the functions that turn a jam log into the cone table, test them against the lecture's numbers, run them on your team's log and the pooled class log, and write your team's jam post-mortem with the data section, evidence-based went right and went wrong, and three checkable changes. The post-mortem is the first draft of the course's post-mortem assessment (20%); week 14 returns to it.

## Sources

- Wikipedia, "Cyberpunk 2077" (read September 2026). Release date of 16 April 2020 announced at E3 2019; delays to 17 September, 19 November and 10 December 2020; released 10 December 2020; removed from the PlayStation Store later that month and returned in June 2021. Dates of the announcements from the cited reports: Adi Robertson, The Verge, 9 June 2019 (April date); CD Projekt Red's post of 16 January 2020, reproduced by GameSpot (September date); Chaim Gartenberg, The Verge, 18 June 2020 (November date); Andy Chalk, PC Gamer, 27 October 2020 (December date).
- Little, T. (2006). "Schedule Estimation and Uncertainty Surrounding the Cone of Uncertainty." *IEEE Software* 23(3), 48-54. doi:10.1109/MS.2006.82. Landmark Graphics data, 106 projects, 1999-2002, weekly estimates; lognormal ratio of actual to initial estimate with median about 1.8 and mean about 2.0; p90/p10 of 3.25; remaining-duration ratios nearly identical at every phase, about a factor of 3 to 4 between p10 and p90.
- McConnell, S., "The Cone of Uncertainty," Construx website (Wayback Machine copy from 2023, read September 2026). 4× to 0.25× at initial concept; the cone as best-case accuracy; narrowing only through decisions that remove variability; the "cloud of uncertainty."
- Boehm, B. (1981). *Software Engineering Economics*. Prentice Hall. Original cone (as cited by Little and McConnell).
- McConnell, S. (2006). *Software Estimation: Demystifying the Black Art*. Microsoft Press. The cone's ranges by milestone as reproduced in the Construx article: 0.25x to 4x at initial concept, 0.5x to 2x at approved product definition, about 0.8x to 1.25x at user interface design complete, about 30% into the calendar.
- Washburn, M., Sathiyanarayanan, P., Nagappan, M., Zimmermann, T. & Bird, C. (2016). "'What Went Right and What Went Wrong': An Analysis of 155 Postmortems from Game Development." *Proceedings of the 38th International Conference on Software Engineering Companion*, 280-289. doi:10.1145/2889160.2889253.
- Wikipedia, "Game Developer (website)" (read September 2026). Online sister publication of the print magazine *Game Developer*, which closed in 2013; more than 150 collected post-mortems dating back to 1997; renamed from Gamasutra to Game Developer in August 2021.
- Beyer, B., Jones, C., Petoff, J. & Murphy, N. R. (eds.) (2016). *Site Reliability Engineering*. O'Reilly. Chapter 15, "Postmortem Culture: Learning from Failure." https://sre.google/sre-book/postmortem-culture/

## Interactive spec: examples/w09-cone-of-uncertainty.html

**The one insight.** The same checkpoints drawn two ways: actual total ÷ estimated total forms a cone that narrows toward 1 by arithmetic, while actual remaining ÷ estimated remaining stays about as wide from start to finish. The cone in the total view is not evidence that estimating improved.

**Data.** Embed the exact contents of `labs/lab09-starter/jam_log_sample.csv` (184 rows plus header) as the default dataset. A textarea "Paste your jam log (CSV)" below the charts replaces it on a "Use my log" button; a "Back to sample" button restores it. Parse errors are shown in text, naming the line.

**Computation** (identical to lab 09's `cone.py`).

```
for each task whose last row (by hour) has status "done":
    A = spent on the done row
    for each row with status "open" and remaining_est > 0:
        x = spent / A
        total = A / (spent + remaining_est)
        remaining = (A − spent) / remaining_est
bins by x: [0, 0.25), [0.25, 0.5), [0.5, 0.75), [0.75, 1.0)
per bin, if at least 2 points: p10, p50, p90 with the inclusive rule
    (sorted values v[0..n−1]; position h = (n − 1) × p; interpolate between v[floor(h)] and v[ceil(h)])
spread = p90 / p10
zero claims = count of open rows with remaining_est = 0
bias = median over finished tasks of A / (remaining_est on the task's first row)
plan ratio = Σ A / Σ (first-row remaining_est) over finished tasks
cut tasks: last row status "cut"; lower bound = last spent / first remaining_est
```

**Layout.** Two scatter plots side by side on desktop, stacked on mobile. Both have x from 0 to 1 and a log-scaled y from 0.1 to 10 with gridlines at 0.25, 0.5, 1, 2, 4 and a heavier line at 1.

1. **Left, total view.** Dots at (x, total). Per bin, horizontal segments for p10, p50, p90, and a shaded band between p10 and p90. Title "Actual total ÷ estimated total".
2. **Right, remaining view.** Dots at (x, remaining), same bands. Title "Actual remaining ÷ estimated remaining".

Hovering or focusing a dot highlights the same checkpoint in both views and shows task, hour, spent, remaining_est, A and both ratios. Dots must be reachable by keyboard (arrow keys step through points in task and hour order).

**Controls.**

- "Show Cyberpunk 2077" checkbox: overlays four diamond markers on both views at (x, total, remaining) = (0.00, 1.76, 1.76), (0.40, 1.18, 1.34), (0.68, 1.04, 1.14), (0.92, 1.00, 1.00). Label them with the announcement month.
- "Show cut tasks as lower bounds" checkbox: draws each cut task as an upward arrow at x = 0 from its lower-bound ratio, on both views.
- Team filter: a select with "All teams" plus one entry per team in the data.

**Readout.** A table matching lab 09's printout: bin, n, total p10/p50/p90/spread, remaining p10/p50/p90/spread, plus bias, plan ratio and zero-claims counts above it.

**Test values** (sample data, all teams; must match lecture section 2).

- Bias 1.50. Plan ratio 1.69 (222.5 / 132). Zero claims 6. 52 tasks, 5 cut (B07, C07, E06, F07, G06, each first estimate 4, lower bounds 2.125, 2.125, 2.0, 1.5, 1.125).
- Bin 0.00-0.25: n = 58; total 0.82 / 1.50 / 2.50, spread 3.04; remaining 0.79 / 1.50 / 2.73, spread 3.45.
- Bin 0.25-0.50: n = 14; total 1.01 / 1.15 / 1.55, spread 1.53; remaining 1.02 / 1.27 / 2.33, spread 2.28.
- Bin 0.50-0.75: n = 24; total 1.00 / 1.25 / 1.38, spread 1.38; remaining 1.00 / 2.00 / 3.00, spread 3.00.
- Bin 0.75-1.00: n = 15; total 0.94 / 1.05 / 1.18, spread 1.25; remaining 0.78 / 1.50 / 3.00, spread 3.83.
- Pasting lab 08's `jam_log_template.csv` gives the lecture's T01 rows: (0, 2.67, 2.67), (0.25, 2.00, 3.00), (0.625, 1.33, 3.00), (0.875, 0.94, 0.67); T02 is cut and gives no points; T03 gives one point, (0, 1.25, 1.25).

**Behaviour.** No animation. Colours from `templates/interactive-tokens.css`; the two views use the same colour per team when the team filter is "All teams". No studio logos or game art; Cyberpunk 2077 appears as a text label only.
