# MMO407 · Week 12 — Writing a post-mortem

**Why this matters:** A post-mortem is the one document from a launch that the next team will actually read. Most of them list what hurt, and a list of what hurt is not a list of what to change. The things that hurt a troubled launch often happened in smooth launches too. This week you learn to write a launch post-mortem whose lessons survive that test, and to read other teams' post-mortems without copying their accidents.

**You will be able to:**
- Compute how often a factor appears in troubled and in smooth launches, and the contrast ratio between them, and rank candidate lessons by it.
- Explain, with the contrast model, why the most-mentioned problem in a pile of post-mortems can carry no lesson at all, and name the survivorship and hindsight biases that produce such piles.
- Write a launch post-mortem with a plan-against-actual table, a timeline, contributing factors that pass a counterfactual test, and lessons graded by the evidence behind them.
- Critique a published post-mortem by naming its missing comparison and rewriting one of its lessons as a testable claim.

**Before class:** Read two post-mortems from the Game Developer (formerly Gamasutra) archive, one for an online game, and list every item in their "what went wrong" sections. Read Politowski, Petrillo, Ullmann and Guéhéneuc, "Game Industry Problems: An Extensive Analysis of the Gray Literature" (preprint, arXiv 2009.02440), sections 1, 3 and 7 (about 25 minutes). Reread MMO308 week 13, section 5, on the blameless incident postmortem; it is not repeated here.

**Prerequisites from earlier courses:** [MMO308 week 13, incident response](../../MMO308-live-operations-analytics-and-experimentation/lectures/w13-incident-response.md) (the blameless postmortem and action items that move a parameter). [MA102 week 13, sampling and confidence](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md) (why 20 cases is a small sample). [MMO302 week 14, observability](../../MMO302-mmo-server-architecture/lectures/w14-observability-logs-metrics-traces.md) (where the timeline comes from). Weeks [1](w01-launch-day-anatomy.md), [2](w02-capacity-planning-and-login-queues.md) and [3](w03-beta-strategies.md) of this course (the forecasts a launch post-mortem checks), and [week 10](w10-recovery-strategies.md).

**Interactive:** [examples/w12-post-mortem-contrast.html](../examples/w12-post-mortem-contrast.html). Keep it open during section 2.

---

## 1. Two documents with the same name

The word "post-mortem" covers two different documents, and mixing them up is the first mistake teams make.

An **incident postmortem** covers one event: an outage, a bad patch, a duplication bug. It is written within days, it follows a fixed template, and its action items change a number in the response model. MMO308 week 13 taught it, including why it must be blameless. You will still write those after every launch-night incident.

A **project post-mortem** covers a whole project or phase, such as the development of a game or its launch month. It is written weeks or months later, by people who were there, and it is meant for the next project. The best-known examples are the post-mortems published for decades in the print magazine Game Developer (closed in 2013) and on its sister website Gamasutra, renamed Game Developer in 2021. Each one describes a game's development in a standard shape, a short introduction, a list of "what went right," a list of "what went wrong," and a closing section. This week is about the project post-mortem, and specifically about the **launch post-mortem**, which covers the weeks from the final beta to the end of the first month live.

Researchers have treated that archive as data. Politowski and colleagues coded 200 post-mortems published between 1997 and 2019 and extracted 927 problems, which they grouped into 20 types. Technical problems (116) and game design problems (112) were the most common types. They also concluded that most of the main root causes were about people rather than technology. [PR101 week 14](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w14-post-mortems-as-a-practice.md) works through all 20 type counts as a Pareto table and opens the largest buckets by root cause, so this lecture uses only the headline. Earlier, Edholm and colleagues reviewed 78 post-mortems and found that 45% mentioned crunch time.

Those are useful facts about what developers write. Hold on to one question, though. Every number in that paragraph counts how often something appears in the "what went wrong" lists. None of them says how often it appeared in projects that went fine. That missing number is this week's subject.

## 2. Worked example: the lesson every launch shares

### The hook

Read the launch stories from this course and you will find a queue in almost every one. World of Warcraft Classic opened worldwide at midnight CEST on 27 August 2019 (26 August in the Americas) to long login queues, and Blizzard added servers. New World opened on 28 September 2021 with 2,000 players per world and queues on the most popular worlds that reached their 25,000-player limit. Week 1 and week 2 modelled both.

So should the next team's post-mortem template say "avoid long day-one queues"? Look again at those two launches. Both drew some of the largest crowds of their year. A queue is what a big crowd looks like at the door. If long queues also show up at launches that went well afterwards, then "we had long queues" is a description of a popular launch, not a cause of a troubled one. Whether it is a lesson depends on a number the post-mortem does not contain.

### The model

Take a set of launches you can compare, and sort them into two groups by outcome. **Troubled** launches failed a target you set in advance (for example, day-30 players below 60% of forecast, or a severity-1 incident lasting more than four hours). **Smooth** launches met it. For each candidate factor, count how many launches in each group had it.

- `n_T` and `n_S` are the numbers of troubled and smooth launches.
- `a` is the number of troubled launches with the factor, `b` the number of smooth launches with it.
- `f_T = a / n_T` is the factor's frequency in troubled launches. It is what a pile of "what went wrong" lists measures.
- `f_S = b / n_S` is its frequency in smooth launches. It is the missing column.
- `L` is the **contrast ratio**:

```
f_T = a / n_T
f_S = b / n_S
L   = f_T / f_S
```

Read `L` like this. At `L = 1`, the factor is as common in smooth launches as in troubled ones, so its presence tells you nothing about the outcome. At `L = 4`, it is four times as common among the troubled. Below 1, it is more common among the smooth. `L` does not prove the factor caused anything, but a factor with `L` near 1 cannot be the difference between the groups. That is enough to strike a lesson off the list.

Two warnings come with the formula. First, `L` is unstable when counts are small. With 20 launches per group, one launch moves a frequency by 5 points. Always report `a`, `b`, `n_T` and `n_S` next to `L`, and read MA102 week 13 before trusting a difference of a few launches. Second, if `b = 0`, `L` is infinite. A common fix is to add one half to every count before dividing, and to say that you did.

### Numbers you can check

Take an invented set of 40 MMO launches, 20 troubled and 20 smooth, and four factors from their post-mortems and launch plans. The numbers are made up for teaching.

| Factor | Troubled with it `a` | Smooth with it `b` | `f_T` | `f_S` | `L` |
|---|---|---|---|---|---|
| Day-one queue over an hour | 14 | 13 | 70% | 65% | 1.08 |
| No full-scale load test | 12 | 3 | 60% | 15% | 4.00 |
| Paid head start | 11 | 9 | 55% | 45% | 1.22 |
| Beta under 5% of launch CCU | 10 | 4 | 50% | 20% | 2.50 |

Check the load-test row by hand. `f_T = 12 / 20 = 0.60`. `f_S = 3 / 20 = 0.15`. `L = 0.60 / 0.15 = 4.00`.

Now rank them two ways. By `f_T`, which is all a pile of troubled post-mortems gives you, the order is queue (70%), load test (60%), head start (55%), beta size (50%). By `L`, the order is load test (4.00), beta size (2.50), head start (1.22), queue (1.08). The factor mentioned most often is the one with the least to teach. The two factors that separate the groups are both from week 3's list: tests that did not reach launch scale.

This script prints both rankings:

```python
TROUBLED, SMOOTH = 20, 20          # launches in each group
factors = {                        # (troubled launches with it, smooth launches with it)
    "day-one queue over an hour": (14, 13),
    "no full-scale load test": (12, 3),
    "paid head start": (11, 9),
    "beta under 5% of launch CCU": (10, 4),
}
rows = [(name, a / TROUBLED, b / SMOOTH) for name, (a, b) in factors.items()]

print("ranked by how often the troubled post-mortems mention it:")
for name, t, s in sorted(rows, key=lambda r: r[1], reverse=True):
    print(f"  {name:28} troubled {t:4.0%}")
print("ranked by the contrast L = troubled share / smooth share:")
for name, t, s in sorted(rows, key=lambda r: r[1] / r[2], reverse=True):
    print(f"  {name:28} troubled {t:4.0%}  smooth {s:4.0%}  L {t / s:4.2f}")
```

It prints:

```
ranked by how often the troubled post-mortems mention it:
  day-one queue over an hour   troubled  70%
  no full-scale load test      troubled  60%
  paid head start              troubled  55%
  beta under 5% of launch CCU  troubled  50%
ranked by the contrast L = troubled share / smooth share:
  no full-scale load test      troubled  60%  smooth  15%  L 4.00
  beta under 5% of launch CCU  troubled  50%  smooth  20%  L 2.50
  paid head start              troubled  55%  smooth  45%  L 1.22
  day-one queue over an hour   troubled  70%  smooth  65%  L 1.08
```

One more thing hides in the queue row. A queue is partly an outcome. It happens because many players arrived, and many players arriving is also what a smooth launch looks like. A factor that is a symptom of the launch's size will appear in both groups. Before you list something as a cause, ask whether it happened before the launch (a plan, a test, a decision) or during it (a consequence). Causes live in the first group.

### Move it yourself

Open the interactive. The left view shows only the troubled launches, as a grid of 20 tiles, with the factor you pick lit up in each tile that had it. This is the view a pile of post-mortems gives you. Pick "day-one queue" and 14 of 20 tiles light up. It looks damning. Now switch on the right view, which adds the 20 smooth launches beside them. Thirteen of those light up too. The bar under the grids shows `L = 1.08`. Pick "no full-scale load test" and the picture reverses. Twelve troubled tiles light, but only three smooth ones. Then drag the smooth-group counts yourself and watch `L` move, and watch how much one tile changes it when the groups are small.

### Cross-game recognition

The missing column shows up wherever people learn from the cases that reached them.

**The post-mortem archive.** Politowski and colleagues counted 927 problems in 200 post-mortems. Edholm and colleagues found crunch mentioned in 45% of 78. In the model's terms these are `f_T`-style counts, frequencies inside the "what went wrong" lists. The archive has a second gap as well. It is made almost entirely of games that shipped, because cancelled projects rarely publish post-mortems. So even the "troubled" group is a group of survivors. None of this makes the counts useless. They are the right tool for "what do developers struggle with most often?" They are the wrong tool for "what separates a troubled project from a fine one?" (For crunch, that second question is also not the main one. Its cost to the people doing it is a reason to avoid it on its own.)

**Bombers in the Second World War.** The statistician Abraham Wald, working in Columbia University's Statistical Research Group, wrote memoranda on how to estimate the vulnerability of an aircraft's parts from damage on the planes that came back. The data came only from surviving aircraft. The damage on returning planes shows where a plane can be hit and still come home, which says little about where the lost planes were hit. In the model's terms, the returning planes are one group and the lost planes are the missing one. A post-mortem archive of shipped games is the same kind of sample.

**Case-control studies in medicine.** Epidemiologists who suspect a risk factor compare people who have a disease (cases) with similar people who do not (controls), and ask how often the factor is present in each group. That is our `f_T` and `f_S`, with troubled launches as cases and smooth launches as controls. Such studies usually report an odds ratio, a close relative of `L`. They are cheaper than an experiment and give weaker evidence of cause, which is exactly the standing of a well-built post-mortem comparison.

**Fan revivals (week 11).** Nostalrius's team wrote a post-mortem of their World of Warcraft fan server and presented it to Blizzard. A single-project post-mortem like that is a record of one case. Its lessons become transferable only when someone lines them up against other fan servers that did and did not survive.

Four settings, one missing column. Whenever you read a lesson drawn from failures, ask where the comparison group is.

### Eyes-open design judgment

- **Build the smooth column on purpose.** Nobody hands it to you. Keep a one-page record of every launch your studio does, troubled or not, with the same factor checklist, filled in before the outcome is known. After five years you have a comparison set. Without it, every post-mortem lesson is an anecdote.
- **Fix the outcome definition first.** Decide what counts as troubled before you look at factors. If you choose the definition afterwards, you will choose one that makes your favourite lesson look strong.
- **Separate causes from symptoms.** Queues, error rates and angry reviews are how a launch looked. Load tests, beta size and capacity plans are what the team chose. Only choices can become lessons.
- **Report the counts.** "`L = 4.0` (12 of 20 against 3 of 20)" lets a reader judge the noise. "`L = 4.0`" alone does not.
- **`L` is a filter, not a verdict.** A high `L` makes a factor worth a closer look. The mechanism (week 1's bottleneck, week 3's exposure model) is what turns it into a lesson you can act on.

### Check this example

1. A factor appears in 9 of 15 troubled launches and 6 of 25 smooth launches. Compute `f_T`, `f_S` and `L`.
2. A studio's archive holds only its 12 troubled launches. The factor "shipped a new account system in the last month" appears in 8. What can you conclude, and what would you need?
3. In the section 2 table, how many smooth launches would need a paid head start for its `L` to equal 1?

<details>
<summary>Answers</summary>

1. `f_T = 9 / 15 = 60%`, `f_S = 6 / 25 = 24%`, `L = 2.5`.
2. Only that the factor is common among troubled launches (67%). You need the same count for comparable smooth launches. If it appears in about two thirds of those too, it is not a lesson.
3. `L = 1` needs `f_S = f_T = 55%`, which is 11 of 20.

</details>

## 3. The anatomy of a launch post-mortem

The contrast model decides which lessons are worth keeping. The rest of the document decides whether anyone can check them. Here is the template this course uses, and the reason for each part.

**1. Scope and sources.** One paragraph. The dates covered (for example, from the final beta to day 30), the systems in scope, and where the evidence comes from: dashboards, incident postmortems, player surveys, interviews. A reader should know what you could and could not see.

**2. Plan against actual.** A table of every forecast the launch plan made, beside what happened. This is the heart of a launch post-mortem, because it checks the models from weeks 1 to 3 against reality.

| Forecast | Plan | Actual | Error | Model it came from |
|---|---|---|---|---|
| Peak arrivals, first hour | 1,000/min | 1,650/min | +65% | marketing forecast |
| Bottleneck stage | world entry | authentication | wrong stage | week 1 capacity table |
| Peak world queue, hour 3 | 18,000 | 31,000 | +72% | week 2 queue model |
| Mean session length, day 1 | 180 min | 260 min | +44% | beta telemetry |
| Severity-1 bugs in week 1 | ≤ 2 | 5 | +3 | week 3 exposure model |
| Day-30 active players | 200,000 | 150,000 | −25% | retention forecast |

(The rows above are invented for illustration.) Each large error is a finding. Notice that the queue error is roughly explained by the arrivals error and the session-length error together. Week 2 showed that the queue grows with arrivals and falls with the logout rate, so both errors push it the same way. Trace errors back to their inputs before you call anything a surprise.

**3. Timeline.** Times in UTC, from logs and incident channels (MMO302 week 14), not from memory. Include the decisions: when the war room chose to open extra worlds, when a kill switch was used, when the team posted to players.

**4. What went right, what went wrong.** Keep the traditional lists. They are the raw material, the `f_T` column. Write each item as something that happened, with a number where possible.

**5. Contributing factors.** For each "went wrong" item, list the choices made before the launch that contributed to it. Apply a **counterfactual test** to each. If this choice had gone the other way, and everything else had stayed the same, would the outcome have changed, and by how much? Use a model where one exists. "Had we doubled authentication, week 1's funnel says throughput would have risen from 600 to 900 per minute and world entry would have become the bottleneck." That is a counterfactual with a number. "Had we been more careful" is not a counterfactual.

**6. Lessons, graded.** Write each lesson as a conditional claim that could be wrong, then grade the evidence behind it.

| Grade | Evidence | Example |
|---|---|---|
| A | A mechanism (a model that explains it) plus a contrast across launches | "Launches without a full-scale load test were four times as likely to be troubled in our 40-launch set (12/20 against 3/20), and week 1's model explains the path" |
| B | A mechanism, or a contrast, but not both | "Our bottleneck moved from authentication to world entry after the upgrade, as week 1 predicts" |
| C | One case, no comparison | "Our long queue made players angry" |

Grade C lessons are allowed. They must say they are grade C, so the next team treats them as questions rather than rules.

**7. Actions.** Each action has an owner, a date, and the metric that will show it worked, as in MMO308 week 13. A launch post-mortem's actions usually change the next launch plan, so name the section of the plan each action changes.

## 4. Two biases that write bad post-mortems

**Hindsight.** After the launch, the problem looks obvious. The load test that was skipped, the forecast that was low, the warning in a chat message. **Hindsight bias** is the tendency to believe, once you know the outcome, that it was predictable all along. It makes teams blame people for missing signals that were buried in noise at the time. The defence is to reconstruct what the team knew at each decision point, from the timeline and the documents dated before the outcome, and judge the decision against that. This is also why MMO308 insists incident postmortems are blameless. The same rule holds for a whole launch.

**Survivorship.** You learn from the cases that reach you. A studio's post-mortem folder holds the launches someone chose to write up, usually the painful ones. A public archive holds the games that shipped and whose developers were allowed to publish. Both are missing a group. Section 2's model makes that gap visible. Your comparison set, built on purpose and filled in before outcomes are known, closes it.

A small team will not have 40 launches. That is fine. Use what exists. Past launches in your studio, public data on other launches (the cases in weeks 4 to 8 of this course), and your own milestones (each beta phase is a small launch with its own forecast). Use a small comparison set with its counts reported, not no comparison at all.

## In-class activity (25 minutes)

Groups of four. Each group gets a one-page summary of an invented MMO launch (the instructor hands out four different ones) and a class-wide table of 30 earlier launches with outcome and six factors.

1. (8 min) From your launch summary, write the "what went wrong" list, at least five items. Mark each as a choice made before launch or a symptom during it.
2. (8 min) For the choices, look up `a`, `b`, `n_T` and `n_S` in the class table and compute `L`. Rank them.
3. (6 min) Write your top two lessons as conditional claims with a grade (A, B or C) and one action each, with owner and metric.
4. (3 min) Swap with another group. Find the weakest lesson in theirs and say which grade it really deserves.

Expected output: a half page with the list, the `L` table with counts, two graded lessons, and the other group's critique. At least one group should find that its most-mentioned problem has `L` close to 1.

## Common misconceptions

- **"The problem mentioned most often is the most important lesson."** Frequency in troubled launches (`f_T`) is not a contrast. A factor as common in smooth launches carries no lesson about the difference.
- **"Our launch post-mortem is the same as the incident postmortems."** Incident postmortems cover one event and change response parameters. A launch post-mortem checks the launch plan's forecasts and changes the next plan.
- **"A high `L` proves the factor caused the trouble."** It shows the factor goes with trouble in this set. Small counts, a biased outcome definition, or a hidden common cause can all produce it. A mechanism is what makes it a lesson.
- **"If it went wrong, someone should have seen it coming."** That is hindsight. Judge each decision against what was known when it was made.

## Check yourself

1. In a set of 18 troubled and 30 smooth launches, "launched in the same month as a big competitor" appears in 9 troubled and 12 smooth. Compute `L`. Would you keep it as a lesson?
2. A factor appears in 6 of 20 troubled launches and 0 of 20 smooth ones. What is `L` as written? Recompute it after adding one half to each of the four counts (with and without the factor, in each group).
3. A post-mortem says, "Our queue model was wrong. The peak queue was 72% above plan." Using week 2's model, name two inputs whose errors could explain it, and say how you would check each.
4. Rewrite "communication with players was poor" as a graded lesson with a condition, a number, and an action.
5. Your studio has run four launches, all of them troubled, all with the same publisher. What can a post-mortem of the fifth conclude about the publisher, and what would you need to know more?

<details>
<summary>Answers</summary>

1. `f_T = 9 / 18 = 50%`, `f_S = 12 / 30 = 40%`, `L = 1.25`. With these counts the difference is a couple of launches, well within noise. Do not keep it as a lesson; at most a grade C question.
2. As written, `L` is infinite (division by zero). With one half added: troubled with it `6.5`, troubled without `14.5`, so `f_T = 6.5 / 21 ≈ 0.310`. Smooth with it `0.5`, without `20.5`, so `f_S = 0.5 / 21 ≈ 0.024`. `L ≈ 13`. Report it with the raw counts.
3. Arrivals higher than forecast (check the first-hour arrival rate in the login logs) and sessions longer than forecast, which lower the logout rate (check mean session length on day 1 against the beta's). Also the number of worlds open, if it changed on the night.
4. For example, "When the status page was updated less often than every 60 minutes during the first 12 hours, support tickets per 1,000 players doubled (from our launch and two earlier ones). Grade B (contrast across three launches, no mechanism tested). Action: communications lead posts on a fixed 30-minute rhythm for launch night, owner named, metric tickets per 1,000 players." Any version with a condition, numbers, a grade and an owned action is fine.
5. Nothing that separates the publisher from anything else, because there is no launch without that publisher to compare with (`f_S` is undefined). You would need launches with other publishers, or smooth launches with this one.

</details>

## Lab / assignment hook

[Lab 12, launch post-mortem](../labs/lab12.md). You compute contrast ratios over a provided set of 40 invented launches with a small library, reproduce this lecture's table, find the factor whose ranking changes most between `f_T` and `L`, and write a full launch post-mortem for one of the launches in the set, using the section 3 template. The post-mortem counts toward the case analyses (50%), and the template is the one you will use for the final post-mortem analysis.

## Sources

- Politowski, C., Petrillo, F., Ullmann, G. C. & Guéhéneuc, Y.-G. "Game Industry Problems: An Extensive Analysis of the Gray Literature." Preprint submitted to Elsevier, arXiv:2009.02440v3 (first posted September 2020, read September 2026). 200 post-mortems from 1997 to 2019, 927 problems in 20 types; technical (116) and game design (112) the most common; most main root causes related to people; the paper's summary of Edholm et al. (2017), 78 post-mortems reviewed, 45% mentioning crunch time. Also its discussion of "what went right" and "what went wrong" sections.
- Politowski, C., Petrillo, F., Ullmann, G. C., de Andrade Werly, J. & Guéhéneuc, Y.-G. (2020). "Dataset of Video Game Development Problems." arXiv:2001.00491 (read September 2026). More than 200 post-mortems from 1998 to 2018, 1,035 problems in 20 types.
- Wikipedia, "Survivorship bias" (read September 2026). Abraham Wald and the Statistical Research Group at Columbia University; memoranda on estimating aircraft vulnerability from damage to returning aircraft.
- Wikipedia, "Case–control study" (read September 2026). Comparison of subjects with and without a condition on how often a suspected factor is present; usually reported as an odds ratio; weaker evidence of cause than a randomised trial.
- Wikipedia, "Game Developer (website)" (read September 2026). Known as Gamasutra until 2021; sister publication of the print magazine Game Developer, which closed in 2013.
- Wikipedia, "Nostalrius" (read September 2026). The team's post-mortem document presented to Blizzard after the server closed in 2016.
- Week 1 of this course for the WoW Classic (midnight CEST on 27 August 2019, 26 August in the Americas) and New World (28 September 2021, 2,000 players per world, queues reaching the 25,000 limit) launch facts, with their sources.
- Beyer, B., Jones, C., Petoff, J. & Murphy, N. R. (eds.) (2016). *Site Reliability Engineering*. O'Reilly. Chapter 15, "Postmortem Culture: Learning from Failure." https://sre.google/sre-book/
- The 40-launch set, its factor counts, the plan-against-actual rows and every example lesson are invented teaching values.

## Interactive spec: examples/w12-post-mortem-contrast.html

**The one insight:** a factor that lights up in most troubled launches can light up just as often in smooth ones. Only the comparison (`L`) tells you whether it is a lesson, and the most-mentioned factor is often the one with the least to teach.

**Layout (two linked views, stacked on mobile, side by side at 900px and wider):**

- View A, "the post-mortem pile": a 4 × 5 grid of 20 tiles for troubled launches. Tiles that had the selected factor are filled (`--blood`), the rest outlined. Above it, `f_T` as a large number. Below it, a small bar chart ranking all four factors by `f_T`.
- View B, "the comparison": hidden until the "show smooth launches" toggle is on (a button labelled "Add the smooth launches"). When on, a second grid of `n_S` tiles for smooth launches appears beside View A, with factor tiles filled (`--steel`). Below both grids, one horizontal bar for `L` on a log scale from 0.25 to 16 with a reference line at 1, and a second bar chart ranking the four factors by `L`. The two ranking charts sit side by side so the reordering is visible.

**Controls:**

- Factor selector (radio buttons): the four section 2 factors, plus "custom".
- For "custom": sliders `n_T` 5 to 50, `n_S` 5 to 50, `a` 0 to `n_T`, `b` 0 to `n_S` (all step 1). The grids resize to match (up to 50 tiles each).
- "Add one half to each count" checkbox (default off). When on, `f_T = (a + 0.5) / (n_T + 1)` and `f_S = (b + 0.5) / (n_S + 1)`.
- "Show smooth launches" toggle (default off on first load).
- "Move one launch" buttons beside `b`: −1 and +1, to show how much one tile changes `L` in a small group.

**Readout (always visible, `aria-live="polite"`):** `a / n_T`, `b / n_S`, `f_T`, `f_S`, `L` to two decimals (or "infinite: no smooth launch had it" when `b = 0` and the half-count option is off), and a sentence: "Mentioned in 70% of troubled post-mortems, and present in 65% of smooth launches. L = 1.08: not a lesson."

**Formulas:**

```
f_T = a / n_T;  f_S = b / n_S;  L = f_T / f_S
with half counts: f_T = (a + 0.5) / (n_T + 1);  f_S = (b + 0.5) / (n_S + 1)
verdict text: L < 1.5 "not a lesson on this evidence"; 1.5 ≤ L < 3 "worth a closer look";
              L ≥ 3 "strong contrast: find the mechanism"   (teaching thresholds, labelled as such)
```

**Test values (must match):**

- Queue: `a = 14, b = 13`, `f_T = 70%`, `f_S = 65%`, `L = 1.08`.
- Load test: `12, 3`, `60%`, `15%`, `L = 4.00`.
- Head start: `11, 9`, `55%`, `45%`, `L = 1.22`.
- Beta size: `10, 4`, `50%`, `20%`, `L = 2.50`.
- Ranking by `f_T`: queue, load test, head start, beta. Ranking by `L`: load test, beta, head start, queue.
- Custom `n_T = 20, n_S = 20, a = 6, b = 0`: "infinite" with half counts off; with half counts on, `f_T = 0.310`, `f_S = 0.024`, `L = 13.00`.
- Custom `n_T = 15, n_S = 25, a = 9, b = 6`: `L = 2.50`.

**First screen:** "Day-one queue" selected, smooth launches hidden, 14 of 20 tiles filled, and the caption "70% of troubled launches had a long queue. Is that a lesson? Add the smooth launches."

**Accessibility:** every control keyboard operable with visible focus; tiles also summarised as text ("14 of 20 filled"); readout in `aria-live="polite"`; `prefers-reduced-motion` disables tile animation; respects `prefers-color-scheme`; tokens from `templates/interactive-tokens.css` inline. Generic tiles only, no game art or logos.
