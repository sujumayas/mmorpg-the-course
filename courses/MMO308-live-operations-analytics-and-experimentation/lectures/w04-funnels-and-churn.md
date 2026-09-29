# MMO308 · Week 04 — Funnels and churn

**Why this matters:** A funnel tells you where players stop, and a churn number tells you how many stopped. Both look like plain counts, and both are easy to misread in a live game, where new players arrive every day and nobody presses a "quit" button. Read them wrong and you rewrite a story chapter that was fine, or celebrate "returning players" who never left.

**You will be able to:**
- Compute step conversion and end-to-end conversion for a funnel, and predict how a change at one step moves the end.
- Explain why a snapshot funnel understates late steps while players are still progressing, and compute the correction with a closed, time-boxed cohort funnel.
- Define churn for a free-to-play game with an inactivity window, and compute the share of "churned" players who are still playing for a given window and play cadence.
- Critique a churn or funnel figure for missing denominators, mixed cohorts and net-versus-gross confusion.

**Before class:** Seif El-Nasr, Drachen & Canossa (eds.), *Game Analytics* (2013), chapter 4 on game telemetry and the section on metrics and key performance indicators in chapter 2. Reread your notes on the geometric distribution from MA102 week 7.

**Prerequisites from earlier courses:** [UX201 week 3, flow and difficulty](../../UX201-game-ux-and-player-psychology/lectures/w03-flow-and-difficulty.md) (turning Steam achievement percentages into retention per step, with Celeste and Cuphead). [DB201 week 12, dashboards and KPIs](../../DB201-data-persistence-and-telemetry/lectures/w12-dashboards-and-kpis.md) (a KPI is a definition; complete cohorts only). [MA102 week 7, the geometric distribution](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w07-geometric-distribution-kills-until-the-drop.md) (constant per-trial chance, mean `1/p`). [GD102 week 2, stocks and flows](../../GD102-systems-design-and-game-mechanics/lectures/w02-stocks-and-flows.md) and [MMO301 week 13, worlds that died](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w13-worlds-that-died-shutdowns-and-their-lessons.md) (a population as a stock with an inflow and a churn outflow). Cohorts and retention curves come from [MMO308 week 3](w03-cohorts-and-retention-curves.md).

**Interactive:** [w04-snapshot-funnel.html](../examples/w04-snapshot-funnel.html), built from the spec at the end of this lecture. Keep it open during section 2.

---

## 1. Funnels, and what UX201 already gave you

A **funnel** is an ordered list of steps that a player passes through, with the number of players who reach each step. Install, finish the tutorial, reach level 10, join a guild. Chapter 1, chapter 2, chapter 3. Open the shop, look at an item, buy it.

Two ratios describe a funnel.

- **Step conversion** `s_k` is the share of players who reached step `k − 1` and went on to reach step `k`. It is `N_k / N_(k−1)`.
- **End-to-end conversion** is the share of players at the top who reach step `k`. It is `N_k / N_0`, and it equals the product of the step conversions: `s_1 × s_2 × ... × s_k`.

In UX201 week 3 you computed step conversion from Steam achievement percentages for Celeste and Cuphead and saw that single-player games lose most players early. That skill is assumed here. This week asks the questions an analyst on a live game has to ask before trusting those ratios. Who counts at the top? When were they counted? Have they had time to reach the bottom?

### Three definitions to decide before you count

- **Open or closed.** An **open funnel** counts anyone who reached step `k`, whether or not you saw them at step `k − 1`. A **closed funnel** counts a player at step `k` only if they also passed every earlier step, in order. Open funnels can show step conversion above 100% when players can enter mid-way (a returning player who skips the tutorial, a guild invite before level 10). Closed funnels cannot.
- **Time-boxed or not.** A **time-boxed funnel** counts step `k` only if it happened within `T` days of the player's entry. Without a box, the funnel keeps changing as long as the players keep playing.
- **Snapshot or cohort.** A **snapshot funnel** counts everyone who has ever entered, at one moment. A **cohort funnel** counts only players who entered in a given window, usually an install week, and compares them at the same age.

Steam's global achievement percentages are an open, unboxed snapshot. That is fine for a finished single-player game years after release. It is a trap for a live game, as the worked example shows.

## 2. Worked example: the funnel that is still filling

### The hook

Throne and Liberty is a free-to-play MMO developed by NCSOFT and published on Steam by Amazon Games, released there on 1 October 2024. Its main story is split into chapters called Codex adventures, and each chapter has a Steam achievement. On 28 September 2026, Steam reported these shares of players for the first eleven:

| Codex chapter | Share of players | Step conversion |
|---|---|---|
| 1. Island of the Star-Born | 71.0% | — |
| 2. The Tragedy of the Casill Family | 57.1% | 80.4% |
| 3. The Demise of the Gray-Fanged | 49.5% | 86.7% |
| 4. Veterans Never Die | 42.8% | 86.5% |
| 5. The Terrific Trio of Carmine Forest | 38.6% | 90.2% |
| 6. A Sacred Pledge of Blood | 35.8% | 92.7% |
| 7. The Song of the Vienta Dwarves | 32.4% | 90.5% |
| 8. The Sandstorm Overlord | 29.7% | 91.7% |
| 9. The Demon's Smile | 26.8% | 90.2% |
| 10. A Pact of Fire and Darkness | 24.7% | 92.2% |
| 11. Nightmare Déjà Vu | 22.7% | 91.9% |

After chapter 4 the story loses 8% to 10% of its remaining readers at every chapter, and the rate barely moves. A narrative lead reading this table might conclude that every chapter from 5 onward is equally weak. Is that what the table says?

Two things are hidden in it. First, the percentages have no count behind them. The page does not say how many players the 100% stands for. Second, this is a snapshot of everyone who has ever played the Steam version, from launch-week players to someone who installed yesterday. The newest players have not had time to reach chapter 11. They are counted at the top and missing at the bottom, not because they quit, but because they have not got there yet. To see how much that matters, you need a model of players moving through a funnel over time.

### The model

Each day, a player who is still playing and has not finished the story does one of three things.

```
progress to the next step     probability q per day
quit for good                 probability h per day
neither (plays, or skips a day, but stays)   probability 1 − q − h
```

- `q` is the **daily progress rate**. With `q = 0.18`, a player finishes a step about every 5 to 6 days on average.
- `h` is the **daily hazard**, the chance of leaving for good on any given day. It is the churn rate measured per day.

Race the two. From any step, the player either progresses first or quits first. The chance they progress first is:

```
eventual step conversion   c = q / (q + h)
eventual end-to-end        c^k   for step k
```

This is the same race you saw in MA102 week 7, where each trial has a fixed chance and the waiting time is geometric. Here two events compete, and only the ratio of their rates decides who wins. The expected number of days until something happens at a step is `1 / (q + h)`.

With `q = 0.18` and `h = 0.02`, `c = 0.18 / 0.20 = 0.90`. Every step keeps 90% of the players who reach it, forever, and each step takes 5 days on average to resolve.

The eventual funnel is the one you would see if you waited until every player had either finished or quit. A snapshot taken earlier shows something else.

### Numbers you can check

Take one install cohort and look at it at different ages. The eventual row follows from `c^k` with `c = 0.9`. You can check it by hand: `0.9, 0.81, 0.729, ...`. The rows for younger ages come from stepping the three-way daily choice forward day by day, which the interactive does and which you will code in the lab.

| Cohort age | Step 1 | Step 2 | Step 4 | Step 6 | Step 8 | Step 10 | Step 10 ÷ step 9 |
|---|---|---|---|---|---|---|---|
| 14 days | 86.0% | 65.0% | 19.8% | 2.3% | 0.1% | 0.0% | 10.9% |
| 30 days | 89.9% | 80.1% | 57.6% | 30.4% | 10.3% | 2.1% | 42.7% |
| 60 days | 90.0% | 81.0% | 65.5% | 52.5% | 40.2% | 27.4% | 81.1% |
| 180 days | 90.0% | 81.0% | 65.6% | 53.1% | 43.0% | 34.9% | 90.0% |
| Eventual | 90.0% | 81.0% | 65.6% | 53.1% | 43.0% | 34.9% | 90.0% |

Read the last column. At 30 days the snapshot says only 43% of players who reach step 9 go on to step 10. The true figure is 90% at every step. Nothing about step 10 is worse. The cohort is simply too young. At 60 days the gap has shrunk to 81% versus 90%. By 180 days it is gone.

Now blend cohorts, the way Steam does. If players install at a steady rate for `L` days and you take one snapshot of all of them, each step's share is the average over cohorts of ages 1 to `L`. With the same `q` and `h`:

| Installs spread over | Reported step conversion, steps 2 to 10 | True |
|---|---|---|
| 90 days | falls from 84.8% to 80.3% | 90% |
| 365 days | 88.6% to 88.8% | 90% |
| 730 days | 89.3% to 89.4% | 90% |

A game three months old shows every step as worse than it is, and late steps as worse still. A game two years old is close to the truth. Throne and Liberty's Steam version was almost exactly two years old when these figures were taken, so its late chapters are probably close to their eventual conversion. The flat 90% after chapter 4 looks like a steady daily hazard racing a steady pace. It does not point at any single chapter.

### A visual you can move

Open `examples/w04-snapshot-funnel.html`. The left view is the funnel a dashboard would show you, bars for steps 1 to 10 at the cohort age you pick. The right view is the eventual funnel for the same `q` and `h`, drawn as ghost bars behind the same axes, with the step conversion printed on each bar.

Drag the age slider from 7 to 180 days. At 14 days the left funnel collapses after step 4 and looks like a story that loses everyone mid-way. Slide on and the bars fill in from the top down until they match the ghosts. Then switch the view to "all installs since launch" and move the launch-age slider. The step conversions sit below 90% until the game is about a year old.

Now change `h` while leaving `q` alone. The eventual funnel moves. Change `q` alone. The eventual step conversion moves too, because it is a ratio. A faster pace is as good as a lower hazard. This is the design lever the model exposes. Shortening a chapter raises `q` and lifts every later step without changing why anyone quits.

### Cross-game recognition

Each of these is the same object: an ordered list of steps, a snapshot of shares, and a pace racing a hazard.

**New World: Aeternum (Amazon Games, Steam, released 28 September 2021).** Its "Progress" achievements I to V read 86.9%, 70.2%, 53.5%, 40.6% and 31.5% on 28 September 2026. Step conversions are 80.8%, 76.2%, 75.9% and 77.6%. The same shape as Throne and Liberty, a roughly constant loss per step, but the constant is lower, about 77%. In the model that means `q / (q + h) ≈ 0.77`. Either each milestone takes longer or the daily hazard is higher. The snapshot alone cannot say which, but a cohort funnel with timestamps can, because it measures how long players take between steps.

**Albion Online (Sandbox Interactive, on Steam since May 2018).** Fixing the tutorial ship reads 56.7% and "Tutorial completed" reads 49.0%, a step conversion of 86.4% for a short step inside the first session. Further down the same list, "One Year of Service", awarded for being part of the game for a year, reads 14.9%. That is a funnel with one step measured in time instead of content. It is a crude one-year retention figure for Steam players, and it has the same age problem as every snapshot. Players who installed eleven months ago cannot have it yet.

**Celeste and Cuphead (UX201 week 3).** Both are finished single-player games, many years past release. Their snapshots are the eventual funnels, which is why the UX201 analysis could read step conversion straight off them. Put a live MMO next to them and the difference is age. A single-player game's funnel stops filling. A live game's never does.

**A shop funnel.** Open the shop, view an item, buy it. The steps take seconds, so `q` is huge relative to `h`, and a snapshot taken a day later is already the eventual funnel. The age problem only bites when steps take days.

### Eyes-open design judgment

- **Use cohort funnels for decisions, snapshots for curiosity.** Compare install cohorts at the same age, with a time box longer than the slowest step you care about. A 30-day box on a funnel whose late steps take 50 days will always blame the late steps.
- **Decide open or closed on purpose.** A closed funnel answers "of players who took the path we designed, where did they leave?" An open funnel answers "how many reached this point by any route?" Returning players and alternate paths make these very different in an MMO.
- **A constant step conversion is a clue.** If every step loses the same share, the cause is probably something that acts every day (the game's overall pull against real life) rather than any one chapter. A single step well below its neighbors, like Throne and Liberty's chapter 2 at 80.4%, is where to look first.
- **Pace is a lever.** Since `c = q / (q + h)`, making steps shorter keeps more players even if the daily hazard does not change. That is a design choice with a cost. Short steps are less content per step, and players notice.
- **A funnel says where, not why.** It narrows your search. Playtests, surveys and session recordings (UX201 weeks 8 and 12) say why.

## 3. Where to push on a funnel

End-to-end conversion is a product of step conversions, so a change at one step moves the end in a predictable way.

- A **relative** improvement at any step moves the end by the same relative amount. Raise step 3 from 50% to 55% (10% relative) and the end rises 10% relative. Raise step 7 from 90% to 99% (also 10% relative) and the end also rises 10% relative.
- An improvement of a fixed number of **percentage points** is worth more at a weak step. Adding 5 points to a 50% step is +10% relative. Adding 5 points to a 90% step is +5.6% relative.

Take a five-step onboarding funnel with step conversions 80%, 50%, 90%, 90%, 95%. End-to-end is `0.8 × 0.5 × 0.9 × 0.9 × 0.95 = 0.308`, so 30.8% of installers finish.

| Change | New end-to-end | Gain |
|---|---|---|
| None | 30.8% | — |
| Step 2: 50% to 55% | 33.9% | +3.1 points |
| Step 4: 90% to 95% | 32.5% | +1.7 points |
| Step 1: 80% to 85% | 32.7% | +1.9 points |

The weakest step gives the biggest return per point. But points are not free, and they are not equally priced. Moving a 50% step to 55% might need a redesigned tutorial boss. Moving a 90% step to 95% might need one clearer quest marker. The funnel tells you the value of a point at each step. Your team must estimate the cost. Rank changes by value per unit of effort, and you will sometimes fix the strong step first.

## 4. Churn: when has a player left?

**Churn** is the set of players who have stopped playing, and the **churn rate** is the share of the active players at the start of a period who have left by its end. In a subscription game churn has a clean definition: the subscription lapsed. In a free-to-play game nobody tells you they have left. You must decide it from silence.

### The inactivity window

The usual rule is an **inactivity window** `W`. A player is labelled churned on the day their last session becomes `W` days old. Pick `W` too short and you label players who are merely between sessions. Pick it too long and you find out about churn weeks after it happened, which is too late to send the "we miss you" message or to connect a spike in churn to last month's patch.

You can compute the cost of a short window. Use the same kind of model as section 2. Each day, a player who is still playing returns with probability `a`. After each session, they quit for good with probability `h`. A player whose last session was `W` days ago is either still playing and on a long gap, or gone. The share who are still playing is:

```
still playing after W quiet days = (1 − h)(1 − a)^W
false-churn share = (1 − h)(1 − a)^W / ((1 − h)(1 − a)^W + h)
```

`(1 − a)^W` is the complement rule from MA102 week 3, the chance of `W` days in a row without a return.

```python
# Share of players labelled "churned" by an inactivity window W who are
# in fact still playing. Each day a still-playing player returns with
# probability a; after each session they quit for good with probability h.
def false_churn(a, h, W):
    still = (1 - h) * (1 - a) ** W   # kept playing, but W quiet days so far
    return still / (still + h)

types = {"daily (a=0.5)": 0.5, "3x a week (a=0.3)": 0.3, "occasional (a=0.1)": 0.1}
h = 0.03
print("W days" + "".join(f"{name:>22}" for name in types))
for W in (3, 7, 14, 30, 60):
    print(f"{W:>6}" + "".join(f"{false_churn(a, h, W):>22.1%}" for a in types.values()))
```

Output:

```
W days         daily (a=0.5)     3x a week (a=0.3)    occasional (a=0.1)
     3                 80.2%                 91.7%                 95.9%
     7                 20.2%                 72.7%                 93.9%
    14                  0.2%                 18.0%                 88.1%
    30                  0.0%                  0.1%                 57.8%
    60                  0.0%                  0.0%                  5.5%
```

A 7-day window works for daily players, since only 20% of those it labels are false alarms. For players who come back three times a week, 73% of the players it labels churned will be back. For occasional players, even a 30-day window is wrong more often than right. There is no single correct `W`. It depends on the cadence of the players you are labelling, which is one reason MMO308 week 7 splits players into segments before computing anything.

Two habits keep this honest.

- **Measure the false-churn share, do not assume it.** Take everyone labelled churned on a given date and count how many played again in the next 60 or 90 days. If it is high, your window is too short for that segment. Lab 04 does exactly this.
- **Do not count false churn as a win.** A "reactivation campaign" sent to players labelled churned by a 7-day window will "bring back" most of them, because most never left. Compare against a held-out group who got no message. Week 5 shows how to set that up.

### Net and gross: what a subscriber count hides

A population is a stock (GD102 week 2). Over a period:

```
end = start + new + returning − churned
net change = new + returning − churned
```

Published figures are usually the stock, so they give you only the net change. World of Warcraft had 10 million subscribers at the start of 2015, after the Warlords of Draenor expansion launched in November 2014. On 6 May 2015 Activision Blizzard reported 7.1 million at the end of March 2015. News coverage called this losing three million subscribers in three months, the largest quarterly drop the game had reported.

Three million is a net figure. The players who cancelled were at least 2.9 million, plus however many joined or returned during the quarter, which was not published. If a million new and returning subscriptions came in during those three months (an illustrative number, not a reported one), then 3.9 million cancelled, a quarterly churn rate of 39% of the starting 10 million. The same net drop is consistent with a small team of leavers and no arrivals, or a large churn masked by a large inflow. A dashboard that shows only the stock cannot tell these apart, and they call for opposite responses. The first says "the game lost its pull". The second says "the game still attracts players and cannot keep them". Always show new, returning and churned as three separate lines under the stock.

Activision Blizzard reported 5.6 million at the end of June 2015 and 5.5 million at the end of September 2015, then stopped publishing the figure.

### Churn rate and expected lifetime

If a constant share `c` of active players churn each month, the number of months a player stays is geometric, and the mean lifetime is `1 / c` (MA102 week 7). A 10% monthly churn means an average stay of 10 months. A 20% churn means 5. Halving churn doubles lifetime, and lifetime multiplies into everything a live game earns. That is why churn is watched more closely than almost any other number.

Real churn is rarely constant. It is highest in the first days, which is what the retention curves of MMO308 week 3 show, and it drops as players become invested. Using `1 / c` with a first-month churn rate will badly understate how long your veterans stay. Compute churn per cohort age, not for the whole population at once.

## In-class activity (25 minutes)

In groups of three, with a laptop and the interactive.

1. **Read a live snapshot (8 min).** Your MMO launched 90 days ago with steady installs. The story funnel shows step conversions of 85%, 84%, 84% and 84% for steps 2 to 5. Using the interactive in "all installs since launch" mode, find a `q` and `h` that reproduce these numbers. What is the eventual step conversion? Is any chapter weak?
2. **Pick a window (10 min).** Your game's players split into 50% daily (`a = 0.5`), 30% three-times-a-week (`a = 0.3`) and 20% occasional (`a = 0.1`), all with `h = 0.03`. Using the formula, choose one `W` for the whole game and compute the overall false-churn share among players labelled at that `W`, weighting each segment by how many of its players cross the window. Then propose a per-segment window and compute the improvement.
3. **Price a fix (7 min).** Using the five-step funnel of section 3, your team can afford one of: +8 points at step 1, +4 points at step 2, or +4 points at both steps 4 and 5. Which gives the highest end-to-end conversion?

Expected output: `q/(q+h)` near 0.9 in step 1 with no single weak chapter; a stated window with its false-churn share in step 2; for step 3, +4 at step 2 gives 33.2%, +8 at step 1 gives 33.9%, +4 at steps 4 and 5 gives 33.5%, so the step 1 change wins despite step 2 being the weakest.

## Common misconceptions

- **"The late chapters leak, look at the step conversion."** In a young game, or a young cohort, late steps are understated because players are still on their way. Compare cohorts at the same age before blaming content.
- **"Fix the weakest step first."** It gives the most per point, but points cost different amounts at different steps. Rank by gain per unit of effort.
- **"Churn is players who haven't logged in for a week."** That is one window, and its error rate depends on how often each player normally plays. For occasional players it mislabels most of them.
- **"The subscriber count fell by X, so X players left."** The fall is net. Gross churn is at least X and could be much larger.

## Check yourself

1. A funnel step has daily progress rate `q = 0.10` and daily hazard `h = 0.025`. What is its eventual step conversion? About how many days does a player spend at the step before it resolves?
2. A game's snapshot shows 60% at step 1 and 30% at step 5 for a cohort that has fully matured. If every step from 2 to 5 has the same conversion, what is it?
3. Using the false-churn formula with `a = 0.2` and `h = 0.04`, what share of players labelled churned by a 14-day window are still playing?
4. A studio reports 2.0 million monthly players in January and 1.8 million in February. It also says 400,000 players played for the first time in February and 100,000 returned after a long break. What was February's churn, and what was the churn rate?

<details>
<summary>Answers</summary>

1. `c = 0.10 / 0.125 = 0.80`. The step resolves after `1 / 0.125 = 8` days on average.
2. `0.30 / 0.60 = 0.5 = s^4`, so `s = 0.5^(1/4) ≈ 0.841`, about 84% per step.
3. `(1 − 0.04) × 0.8^14 = 0.96 × 0.04398 = 0.04222`. False-churn share `0.04222 / (0.04222 + 0.04) = 0.514`. Just over half are still playing.
4. `1.8 = 2.0 + 0.4 + 0.1 − churned`, so churned = 0.7 million, a churn rate of `0.7 / 2.0 = 35%` of January's players. The net drop of 0.2 million hides it.

</details>

## Lab / assignment hook

[Lab 04, funnels and churn from an event log](../labs/lab04.md). You compute a snapshot funnel and a closed, time-boxed cohort funnel from 120 days of simulated story progress, show how far apart they are, then label churn with several inactivity windows and measure each window's false-churn share against what players actually did in the following 60 days. Deliverable: your `funnel.py` passing the checker, and a one-page memo recommending a funnel definition and a churn window for each player segment.

## Sources

- Steam global achievement statistics, Throne and Liberty (app 2429640), retrieved 28 September 2026 from the Steam Web API (`GetGlobalAchievementPercentagesForApp`) and the Steam Community achievements page for chapter names. Codex chapters 1 to 11 as in the section 2 table. Step conversions computed by the author. Steam store page for the release date (1 October 2024), developer NC and FirstSpark Games, publisher Amazon Games. Figures drift daily.
- Steam global achievement statistics, New World: Aeternum (app 1063730), retrieved 28 September 2026. Progress I to V: 86.9%, 70.2%, 53.5%, 40.6%, 31.5%. Steam store page for the release date (28 September 2021) and publisher.
- Steam global achievement statistics, Albion Online (app 761890), retrieved 28 September 2026. "Whatever Floats Your Boat" 56.7%, "Cast Away" (tutorial completed) 49.0%, "One Year of Service" 14.9%. Steam store page for the Steam release date (16 May 2018).
- World of Warcraft subscriber figures. Business Insider, "World of Warcraft lost three million subscribers in three months" (Weinberger, 7 May 2015) and Kotaku, "Why World of Warcraft Lost So Many Subscribers" (Vas, 7 May 2015): 10 million at the start of 2015, 7.1 million at the end of March 2015, reported on Activision Blizzard's earnings call. Activision Blizzard results releases, exhibits to Form 8-K on SEC EDGAR (read September 2026): Q1 2015 (filed 6 May 2015), "Subscribers ended the quarter at 7.1 million"; Q2 2015 (filed 4 August 2015), 5.6 million at the end of June; Q3 2015 (filed 3 November 2015), 5.5 million at the end of September. Wikipedia, "World of Warcraft" (accessed September 2026), for the end of subscriber reporting after that quarter.
- Seif El-Nasr, M., Drachen, A. & Canossa, A. (eds.) (2013). *Game Analytics: Maximizing the Value of Player Data*. Springer.
- The snapshot and cohort funnel tables, the blended-snapshot figures and the false-churn table were computed by the author from the models stated in the lecture.

## Interactive spec: examples/w04-snapshot-funnel.html

**The one insight.** A funnel read from a snapshot shows late steps as leaky while players are still progressing. With a true 90% conversion at every step, a 30-day-old cohort shows only 43% from step 9 to step 10. The student drags cohort age and watches the bars fill in to the eventual funnel.

**Layout.** Two linked views side by side on desktop, stacked on mobile (snapshot first).

- **Left view, "What the dashboard shows".** Ten vertical bars, steps 1 to 10, height = share of the cohort (or blended population) that has reached each step at the chosen age. Label each bar with its share (one decimal) and, between bars, the step conversion `bar_k / bar_(k−1)` (one decimal). Color a step conversion in the accent color when it is more than 5 points below the eventual `c`.
- **Right view, "Where it ends up".** Same axes. Eventual bars `c^k` drawn solid, with the left view's current bars overlaid as outlines, so the gap is visible. Print `c = q/(q+h)` and the mean days per step `1/(q+h)` above the chart.
- **Readout row.** Age, mode, `q`, `h`, `c`, and for steps 2 to 10 a table of snapshot step conversion versus `c`.

**Controls (keyboard accessible, update immediately).**
- Mode toggle: "One cohort" (default) / "All installs since launch".
- Cohort age `t` in days: slider 1 to 365, default 30. In "all installs" mode the same slider is labelled "Days since launch" (`L`), runs 1 to 730, default 90.
- Daily progress rate `q`: slider 0.02 to 0.50, step 0.01, default 0.18.
- Daily hazard `h`: slider 0.00 to 0.10, step 0.005, default 0.02. Constrain `q + h ≤ 1`.
- Number of steps: fixed at 10.
- Presets: "Young game" (one cohort, t = 30), "Mature" (t = 180), "Launch + 90 days" (all installs, L = 90), "Launch + 2 years" (all installs, L = 730).

**Formulas.**
- Cohort state: `act[k]` = share still playing with exactly `k` steps done; `gone[k]` = share who quit with `k` done. Start `act[0] = 1`. Each day, for `k < 10`: `act'[k+1] += q·act[k]`, `gone[k] += h·act[k]`, `act'[k] += (1 − q − h)·act[k]`. For `k = 10`: `act'[10] += (1 − h)·act[10]`, `gone[10] += h·act[10]`. Run `t` days.
- Reached step `k` at age `t`: `R_t(k) = Σ_{j ≥ k} (act[j] + gone[j])`.
- Blended: `B_L(k) = (1/L) Σ_{a = 1..L} R_a(k)` (installs uniform over the `L` days, snapshot at day `L`). Compute incrementally by stepping one cohort forward and accumulating, which is `O(L × 10)`.
- Eventual: `c = q/(q+h)` (if `q + h = 0`, show "no movement"); `R_∞(k) = c^k`.

**Test values (q = 0.18, h = 0.02).**
- `c = 0.9`, mean days per step 5.
- One cohort, t = 14: steps 1, 2, 4, 6 = 86.0%, 65.0%, 19.8%, 2.3%.
- t = 30: steps 1, 2, 4, 6, 8, 9, 10 = 89.9%, 80.1%, 57.6%, 30.4%, 10.3%, 5.0%, 2.1%; step 10 ÷ step 9 = 42.7%.
- t = 60: step 10 = 27.4%, step 10 ÷ step 9 = 81.1%.
- t = 180: all steps within 0.1 point of `0.9^k`; step 10 = 34.9%.
- All installs, L = 90: step 1 = 86.0%, step 10 = 15.9%; step conversions 84.8% (step 2) falling to 80.3% (step 10).
- All installs, L = 365: step conversions 88.6% to 88.8%. L = 730: 89.3% to 89.4%.

**First screen.** "Young game" preset. The left funnel drops to 2.1% at step 10 with red step conversions from step 4 on (82.6% and below), while the right view's solid bars stand at 34.9%, so the gap is the first thing the student sees.
