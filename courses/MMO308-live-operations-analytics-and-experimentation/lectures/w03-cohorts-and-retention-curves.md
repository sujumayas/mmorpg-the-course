# MMO308 · Week 03 — Cohorts and Retention Curves

**Why this matters:** A patch that breaks the first hour of your game can leave DAU rising for weeks, while an outage that changes nothing lasting makes DAU crater for a day. A team that reads only the calendar chart will fix the wrong thing. Cohorts sort every player by when they arrived, and that one change of axis shows which kind of problem you have and when it started.

**You will be able to:**
- Build a cohort retention table from an activity log and read D1, D7 and D30 by install date.
- Classify a change as a cohort effect, a one-day period effect or a lasting period effect from the pattern it leaves in the table.
- Date a patch that broke onboarding from D1, D7 and D30 series, and explain why the break is nearly invisible in DAU.
- Choose which retention checkpoint to watch by trading signal size against delay, using the standard error of a rate.

**Before class:** Seif El-Nasr, Drachen and Canossa (eds.), *Game Analytics* (Springer, 2013), chapter 2, "Game Analytics – The Basics" (pp. 13-40), and skim chapter 19, "Visual Analytics Tools – A Lens into Player's Temporal Progression and Behavior" (pp. 435-470). Read the "Destiny Content Vault" section of the Wikipedia article on *Destiny 2: Beyond Light* (10 minutes).

**Prerequisites from earlier courses:** [DB201 week 12, dashboards and KPIs](../../DB201-data-persistence-and-telemetry/lectures/w12-dashboards-and-kpis.md) (the definition of Dn retention, exact-day versus rolling retention, and why only complete cohorts belong on a chart; this week assumes all three). [MA102 week 13, sampling and confidence](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md) (the standard error of a rate). From this course, [week 1, what live ops is](w01-what-live-ops-is.md) (cohorts, the layer cake and the two-type retention curve) and [week 2, KPIs](w02-kpis-dau-mau-stickiness-arpdau.md) (why rolling windows echo events).

**Interactive:** [w03-retention-triangle.html](../examples/w03-retention-triangle.html), built from the spec at the end of this lecture. Keep it open during section 2.

---

## 1. From one curve to a table

In week 1 every cohort shared one retention curve `R(a)`. Real cohorts do not. Players who install in the week of a big update meet a busier world than players who install in a quiet month. Players who install after a tutorial rewrite meet a different first hour. To see those differences, you keep one curve per cohort.

Put them in a table. Each row is a cohort, labeled by its **install day** `c`. Each column is an **age** `a`, the number of days since install. Each cell holds the exact-day retention `R(c, a)`: the share of cohort `c` that was active on day `c + a`, as DB201 week 12 defined it. The result is called a **cohort table**, and because the newest cohorts have not reached the older ages yet, its filled cells form a triangle. Analysts often call it the **retention triangle**.

Every cell sits on three clocks at once:

- its **age** `a`, the column;
- its **cohort** `c`, the row;
- its **calendar day** `t = c + a`, a diagonal running from top right to bottom left.

That gives three kinds of effect, and each leaves its own shape in the table.

- An **age effect** is the normal shape of the curve: every cohort loses players fast in the first days and slowly after. It shows as the same pattern repeated along every row.
- A **cohort effect** changes the players who arrived at a certain time, for all of their ages. A new tutorial, a marketing campaign that brings a different audience, a store feature on one day. It shows as a **horizontal** boundary: every row below some install day looks different.
- A **period effect** changes what happens on certain calendar days, for everyone. An outage, a holiday, a double-XP weekend, a patch that changes the endgame. It shows as a **diagonal**: every cell with the same `c + a`.

The calendar charts you already know (DAU, rolling MAU, Steam's concurrent players) add up each diagonal of the layer cake. They are period views. They cannot tell a cohort effect from a period effect, because they have already mixed all the rows. That is the whole reason to build the table.

### Why the curve bends

Before looking for breaks, know the shape of a healthy curve. Week 1's two-type model in daily form is:

```
R(a) = w × qs^a + (1 − w) × qt^a        for a ≥ 1, with R(0) = 1
```

with `w` the share of stayers, `qs` a stayer's daily survival and `qt` a tourist's. Tourists vanish within a few days, so the early curve is dominated by them and falls steeply. After that only stayers remain, and the curve falls at the slow rate `1 − qs`. On a chart with a log scale on the retention axis, the tail of the curve becomes a straight line, and its slope tells you `qs`. Week 4 turns that slope into a churn rate.

## 2. Worked example: the patch that broke onboarding

### The hook

On 10 November 2020 Bungie released Destiny 2: Beyond Light. The same day changed the game in two different ways.

For existing players, it added a new destination, Europa, and new seasonal content. It also moved five older destinations (Titan, Io, Mars, Mercury and the Leviathan) and the campaigns and activities tied to them into what Bungie called the Destiny Content Vault, removing them from the game. For brand-new players, it replaced the start of the game. Earth's Cosmodrome, an area from the first Destiny, returned as the introductory destination for first-time players of the free-to-play base game, with a new opening questline.

Week 14 looks at the vault as a content sunset. This week asks a measurement question. One calendar date carried a change for everyone (new content, fewer destinations) and a change for new players only (a different first hour). A DAU chart sees one date. How would Bungie's analysts, or yours, tell the two changes apart, and see whether the new first hour kept more or fewer new players? Bungie has not published retention figures, and the numbers below are invented. The method is what transfers.

### The model

Take an invented MMO. Every day, 2,000 players install. Its daily retention follows the two-type curve with `qs = 0.985` and `qt = 0.30`. Normally a quarter of each cohort are stayers, `w = 0.25`.

Two things go wrong, one after the other:

1. **The onboarding break.** A patch on day 20 introduces a bug in the tutorial's group quest. Players who install on day 20 or later are much less likely to find a group, and fewer become stayers: `w` drops to 0.15 **for cohorts `c ≥ 20` only**. Nothing changes for players already past the tutorial.
2. **The outage.** On day 40 a login fault keeps 60% of returning players out for the whole day. Every cell with `c + a = 40` (and `a ≥ 1`) is multiplied by 0.4. Nothing changes on any other day.

So:

```
R(c, a) = w(c) × 0.985^a + (1 − w(c)) × 0.30^a      for a ≥ 1
w(c)    = 0.25 if c < 20, else 0.15
R(c, a) × 0.4                                       if c + a = 40
DAU(t)  = Σ over c ≤ t of 2,000 × R(c, t − c)       with R(c, 0) = 1
```

The first change is a cohort effect. The second is a one-day period effect.

### Numbers you can check

Start with the checkpoints. `D1 = R(c, 1)` for a normal cohort is `0.25 × 0.985 + 0.75 × 0.30 = 0.2463 + 0.2250 = 0.471`. Work the others the same way.

| Install day `c` | D1 | D7 | D30 | What happened |
|---|---|---|---|---|
| 9 | 47.1% | 22.5% | 15.9% | normal |
| 10 | 47.1% | 22.5% | **6.4%** | day 30 of this cohort is day 40, the outage |
| 18 | 47.1% | 22.5% | 15.9% | normal |
| 19 | 47.1% | 22.5% | 15.9% | normal, last cohort before the patch |
| **20** | **40.3%** | **13.5%** | **9.5%** | first broken cohort |
| 21 | 40.3% | 13.5% | 9.5% | broken |
| 33 | 40.3% | **5.4%** | 9.5% | day 7 of this cohort is day 40 |
| 39 | **16.1%** | 13.5% | 9.5% | day 1 of this cohort is day 40 |

Read the table two ways.

**Down the rows**, the onboarding break is a **step**: all three checkpoints change at install day 20 and stay changed. D1 falls 6.9 points (−15%), D7 9.0 points (−40%) and D30 6.4 points (−40%). The step sits at the same install date in all three series. That alignment is the signature of a cohort effect, and the install date where it lands is the patch date.

**Along the diagonals**, the outage is a **single dip** that lands on a different install date in each series: cohort 39 in D1, cohort 33 in D7, cohort 10 in D30. Each is `40 − n` for Dn. A one-day problem on calendar day `t` always shows up at install day `t − n` in the Dn series. That staggering is the signature of a period effect.

Now look at what the dashboard showed. DAU with the break and the outage, next to what DAU would have been without either:

| Day | DAU | DAU without the break or outage | Gap |
|---|---|---|---|
| 19 | 10,838 | 10,838 | 0% |
| 25 | 12,104 | 12,974 | −7% |
| 30 | 12,855 | 14,612 | −12% |
| 39 | 14,073 | 17,265 | −18% |
| **40** | **6,879** | 17,539 | −61% |
| 41 | 14,322 | 17,808 | −20% |
| 60 | 16,345 | 22,218 | −26% |
| 70 | 17,199 | 24,078 | −29% |

The team never sees the middle column. What they see is DAU **rising** every day except one, from 10,838 on day 19 to 17,199 on day 70. The game is young and every day adds a new layer, so growth hides the damage. The one day that screams is day 40, a problem that cost a day of play and then vanished. The problem that will cost 29% of DAU by day 70 and keep growing never produces a visible event on the calendar chart at all.

Here is the model in code. It runs as shown with `.venv/bin/python`:

```python
QS, QT, INSTALLS = 0.985, 0.30, 2_000

def R(c, a):
    if a == 0:
        return 1.0
    w = 0.15 if c >= 20 else 0.25          # onboarding break for cohorts from day 20
    r = w * QS**a + (1 - w) * QT**a
    return r * 0.4 if c + a == 40 else r   # outage on calendar day 40

for c in (19, 20, 33, 39):
    print(c, [f"{100 * R(c, a):.1f}%" for a in (1, 7, 30)])
dau = lambda t: sum(INSTALLS * R(c, t - c) for c in range(t + 1))
print([round(dau(t)) for t in (19, 30, 40, 70)])
```

It prints `20 ['40.3%', '13.5%', '9.5%']` for the first broken cohort and `[10838, 12855, 6879, 17199]` for DAU.

### The visual

Open `examples/w03-retention-triangle.html`. It has three linked views.

- **Top, "What the dashboard shows":** DAU by calendar day. It climbs, with one deep notch at day 40.
- **Middle, "The triangle":** the cohort table as a heat map, install day down the side and age across the top, darker for higher retention. The onboarding break is a horizontal seam at row 20. The outage is a thin pale diagonal.
- **Bottom, "Checkpoints by install day":** D1, D7 and D30 as three lines against install day. All three step down together at install day 20. Each has one dip at a different place.

Hover any cell in the triangle and the views highlight its row, its column and its diagonal, with the calendar day it belongs to. Then use the "patch type" control. Switch the break from "onboarding (cohorts from day P)" to "endgame (calendar days from P)". Now a patch on day 45 lowers the stayers' daily survival from 0.985 to 0.97 for everyone. The seam in the triangle turns from horizontal into a diagonal boundary with everything below and to the right of it paler. On the checkpoint chart, D30 bends first (from install day 16), D7 later (from install day 39) and D1 last (from install day 45), because each checkpoint passes calendar day 45 at a different install date. Same date, same size of change, opposite shape.

### Cross-game recognition

**Destiny 2: Beyond Light (10 November 2020).** Rewrite the hook in the model's terms. The new Cosmodrome opening is a cohort effect: it changed `w(c)` for players whose install day was 10 November or later, and nothing for anyone else. The vaulting of five destinations and the arrival of Europa are period effects: they changed what every player could do from that calendar date. In the triangle the first appears as a horizontal seam at the row for 10 November. The second appears as a boundary along the diagonal `c + a = 10 November`. An analyst who wants to know whether the new opening helped compares rows just after the seam with rows just before it, at the same ages, and checks that the period effect has hit both groups at matching ages before reading anything into the difference.

**Old School RuneScape's weekly updates (current).** OSRS ships game updates on Wednesdays at 11:30 UK time most weeks. Each update is a small period effect. In a triangle of daily cohorts, a week of such updates shows as parallel diagonal stripes seven days apart. A team that expects the stripes can subtract them. A team that does not may read a Wednesday bump in D7 for the cohort that installed the previous Wednesday as a feature of that cohort. It is the update, reaching that cohort at age 7.

**Week 2's rolling-window echo.** In week 2 a one-day event made a rolling MAU drop exactly 30 days later. That is the same diagonal geometry seen from another angle. An event on calendar day `t` affects the cell `(c, a)` with `c + a = t`, and a 30-day window carries it until it slides out at `t + 30`. Diagonals are what calendar events look like in any chart that tracks age.

**Age-period-cohort analysis in demography and epidemiology.** Researchers who study mortality, disease or voting use the same three clocks. A person's age, the calendar year and their birth year (their cohort) are tied by `year = birth year + age`, exactly our `t = c + a`. A drug introduced in 1995 is a period effect. A childhood vaccine given only to people born after 1960 is a cohort effect. Yang and Land's textbook on age-period-cohort analysis is built around the same triangle, which demographers call a Lexis diagram when drawn as a chart. They also prove a warning that applies to you: because `t = c + a` exactly, a steady trend along one clock can always be rewritten as trends along the other two. You can separate sharp changes (a step, a dip, a seam) from each other. You cannot separate slow, straight-line drifts without an outside assumption.

Four contexts: a shooter's expansion day, an MMO's weekly updates, week 2's MAU echo and a demographer's triangle. One idea. Every cell has an age, a cohort and a date. Changes that belong to a cohort draw horizontal lines, changes that belong to a date draw diagonals, and a calendar chart cannot tell them apart.

### Eyes-open design judgment

- **Ship every onboarding change with a cohort chart already open.** The only way to see an onboarding effect early is the checkpoint-by-install-day chart. Mark the patch date on it before you deploy, and look for a step in D1 from the next morning.
- **Read three checkpoints, not one.** A step that appears at the same install day in D1, D7 and D30 is a cohort effect. A dip at `t − 1`, `t − 7` and `t − 30` is a period effect on day `t`. With only one checkpoint you cannot tell the two apart.
- **Watch the diagonals when you judge a cohort.** A cohort that looks weak at D7 may simply have hit an outage or a holiday at age 7. Before you blame onboarding, check whether the cohorts on either side hit the same calendar day at other ages.
- **Growth hides cohort damage.** In the worked example DAU rose on every day but one for 50 days after onboarding broke. In a young or growing game, never read "DAU up" as "new players are fine". The layer cake from week 1 explains why: new layers are thin, but old ones still carry the total.
- **Define install carefully.** Account creation, first login and first completed tutorial step give different cohorts. A client update that adds an extra launcher screen before account creation moves players out of your cohorts entirely, and your D1 can rise while fewer people start the game. Keep a funnel for the steps before install (week 4).

## 3. Signal or speed: which checkpoint to watch

The worked example shows D1 changing by 15% and D7 by 40%. So why not just watch D30, which also changed by 40%? Because of time. The table below uses daily cohorts of 2,000 players and the standard error of a rate from MA102 week 13, `sqrt(p(1 − p) / n)`. For the difference between one normal and one broken cohort, add the two variances.

| Checkpoint | Normal | Broken | Difference | Standard error of the difference | Difference in standard errors | First readable after the patch |
|---|---|---|---|---|---|---|
| D1 | 47.1% | 40.3% | 6.9 points | 1.56 points | 4.4 | 1 day |
| D7 | 22.5% | 13.5% | 9.0 points | 1.21 points | 7.5 | 7 days |
| D30 | 15.9% | 9.5% | 6.4 points | 1.05 points | 6.1 | 30 days |

Check the D7 row. Normal `p = 0.2251`, broken `p = 0.1351`. The variances are `0.2251 × 0.7749 / 2,000 = 0.0000872` and `0.1351 × 0.8649 / 2,000 = 0.0000584`. Their sum is `0.0001456`, whose square root is `0.0121`, 1.21 points. The difference, 8.99 points, is 7.4 to 7.5 standard errors depending on rounding.

Three lessons.

**D1 is fast and noisy.** A break that only changes stayers barely moves D1, because D1 is dominated by tourists who were never going to stay. Here the D1 step is 4.4 standard errors, visible from one cohort but easy to lose among real day-to-day noise from weekdays, marketing and holidays. Pool several cohorts on each side of the date before you trust it.

**D7 is the workhorse.** By day 7 the tourists have gone, so D7 measures mostly stayers, which is what an onboarding change affects. It gives the biggest signal per cohort and arrives in a week.

**D30 confirms, but late.** It is the closest to "did they become long-term players?", and it is the only checkpoint that catches effects which appear late in the first month. But a team that waits for D30 on every change ships a month of broken onboarding before it knows.

The general rule is to watch the earliest checkpoint where the change you expect has had time to act. For a tutorial, that is D1 to D7. For a new level-cap system that players reach after two weeks, D1 and D7 will show nothing, and D30 is the first place to look.

## 4. Reading real triangles

The model is clean. Real triangles are not. Four habits make them readable.

**Use enough rows.** One day's cohort is noisy. Group cohorts by week for anything slower than D7, or plot a 7-day moving average of the checkpoint series. Weekly grouping also removes the weekday pattern, since weekend installers often behave differently from weekday ones.

**Only complete cells.** DB201 week 12 showed that a cohort whose day 7 has not happened must not appear with a D7 of zero. The same rule covers the whole triangle. Blank out cells in the future, never fill them with zeros.

**Compare at equal age.** When you compare two cohorts, compare them at the same ages. Comparing this week's cohort's D7 with last month's cohort's D30 is comparing ages, not cohorts.

**Label the calendar.** Draw every known period event (patches, events, outages, holidays) as a diagonal on the triangle and a vertical rule on the DAU chart. A diagonal you can explain is not a finding. A horizontal seam you cannot explain is the most important thing on the page.

## In-class activity (25 minutes)

Groups of three. Each group gets a printed triangle (install days 0 to 34, ages 0 to 30) from an invented game with 1,500 installs a day. It contains exactly three planted effects, chosen from: an onboarding break or fix, a one-day outage, a weekend event lasting two calendar days, and an endgame patch that lowers stayers' daily survival from a given day.

1. **Find the shapes (10 min).** Mark every horizontal seam, single diagonal and diagonal boundary you can see. For each, write whether it is a cohort effect, a one-day period effect or a lasting period effect, and the date.
2. **Confirm with checkpoints (8 min).** From the triangle, read off the D1, D7 and D30 series by install day. Check that each effect lands where the rules predict: the same install day in all three series, or install days `t − 1`, `t − 7` and `t − 30`.
3. **Size the worst one (7 min).** For the effect you think matters most, estimate its size in D7 points and its cost in DAU by day 60, using the layer-cake reasoning from week 1.

Expected output: an annotated triangle, a three-row table (effect, type, date) and one sentence with the size estimate.

## Common misconceptions

- **"DAU is rising, so new players are fine."** In the worked example DAU rose from 10,838 to 17,199 over the 50 days after onboarding broke, while D7 for new cohorts fell 40%. Growth in a young game hides cohort damage.
- **"A drop in D7 for one cohort means that cohort was worse."** It may be a period effect on the calendar day that cohort reached age 7. In the example cohort 33's D7 of 5.4% comes from the day-40 outage, not from anything about cohort 33.
- **"D1 is the best early warning."** D1 is the fastest, but when a change affects stayers rather than tourists, D7 gives a larger and cleaner signal a week later. In the example D7 shows 7.5 standard errors against D1's 4.4.
- **"With enough data you can separate age, period and cohort trends."** Because calendar day equals install day plus age, steady linear trends cannot be separated without an extra assumption. Sharp changes can.

## Check yourself

1. Using the model, compute D7 for a normal cohort and for a broken one by hand. Which of the two terms (stayers or tourists) makes up most of the difference?
2. An outage hits calendar day 55. On which install days does it show up in the D1, D7 and D30 series?
3. The team fixes the tutorial bug on day 50, restoring `w = 0.25` for new cohorts. Where does the fix appear in the triangle, and on which calendar day can the D7 chart first show it?
4. An endgame patch on day 45 lowers stayers' daily survival from 0.985 to 0.97 for everyone. For a normal cohort installed on day 10, what is its retention at age 40, with and without the patch? (Ignore the outage.)
5. With daily cohorts of 500 instead of 2,000, what is the standard error of the difference in D7 between one normal and one broken cohort? How many standard errors is the break now, and what would you do about it?

<details>
<summary>Answers</summary>

1. `0.985^7 = 0.8997` and `0.3^7 = 0.000219`. Normal: `0.25 × 0.8997 + 0.75 × 0.000219 = 0.2249 + 0.0002 = 0.2251`. Broken: `0.15 × 0.8997 + 0.85 × 0.000219 = 0.1350 + 0.0002 = 0.1351`. The stayer term makes up essentially all the difference: by day 7 the tourists are gone.
2. D1 at install day 54, D7 at install day 48, D30 at install day 25. Each is `55 − n`.
3. A second horizontal seam at row 50, with rows below it back to normal. The D7 chart shows it on calendar day 57, when cohort 50 reaches age 7.
4. Without the patch: `0.25 × 0.985^40 + 0.75 × 0.3^40 ≈ 0.25 × 0.5463 = 0.1366`. With it, the cohort spends 35 days at 0.985 and the last 5 (calendar days 46 to 50) at 0.97: `0.25 × 0.985^35 × 0.97^5 ≈ 0.25 × 0.5892 × 0.8587 ≈ 0.1265`. So 13.7% becomes 12.6%.
5. Each variance is four times larger, so the standard error doubles: `sqrt(0.2251 × 0.7749 / 500 + 0.1351 × 0.8649 / 500) ≈ 0.0241`, 2.41 points. The break is `8.99 / 2.41 ≈ 3.7` standard errors. Pool several cohorts on each side of the patch date (five days on each side gives 2,500 players per group and brings it back to about 8 standard errors), at the cost of waiting longer.

</details>

## Lab / assignment hook

[Lab 03, the retention triangle](../labs/lab03.md). You build a cohort table from a raw activity log in Python, plot D1, D7 and D30 by install day, and find the dates and types of three planted effects, including a patch that broke onboarding. Deliverable: passing tests, the triangle and checkpoint charts, and a 400-word incident note that dates the break and estimates its cost.

## Sources

- Wikipedia, "Destiny 2: Beyond Light" (read September 2026). Release on 10 November 2020; the Destiny Content Vault removing Titan, Io, Mars, Mercury and the Leviathan with their campaigns and activities; the return of Earth's Cosmodrome as the introductory destination for first-time New Light players with a new questline; Europa as the new destination.
- Old School RuneScape Wiki, "Game updates" (read September 2026). Game updates occur on Wednesdays at 11:30 UK time.
- Yang, Y. & Land, K. C. (2013). *Age-Period-Cohort Analysis: New Models, Methods, and Empirical Applications*. Chapman and Hall/CRC. DOI 10.1201/b13902. The age-period-cohort framework and the identification problem created by `period = cohort + age`.
- Seif El-Nasr, M., Drachen, A. & Canossa, A. (eds.) (2013). *Game Analytics: Maximizing the Value of Player Data*. Springer. Chapter 2, Drachen, Seif El-Nasr & Canossa, "Game Analytics – The Basics" (pp. 13-40); chapter 19, Seif El-Nasr, Gagné, Moura et al., "Visual Analytics Tools – A Lens into Player's Temporal Progression and Behavior" (pp. 435-470).

## Interactive spec: examples/w03-retention-triangle.html

**The one insight.** An onboarding break (cohort effect) draws a horizontal seam in the retention triangle and a step at the same install date in D1, D7 and D30, while DAU keeps rising. An outage (one-day period effect) draws a single diagonal and makes DAU crater for a day. The calendar view shouts about the harmless one and whispers about the lasting one; the triangle shows which is which.

**Layout.** Three linked views stacked vertically on all widths. Top: "What the dashboard shows", DAU by calendar day 0 to 70. Middle: "The triangle", heat map with install day `c = 0..60` as rows (top to bottom) and age `a = 0..30` as columns; cells with `c + a > 70` are blank (future). Bottom: "Checkpoints by install day", D1, D7 and D30 against install day, each drawn only for complete cohorts (`c + n ≤ 70`). Controls sit in a bar between the top and middle views on narrow screens and in a side panel on wide screens.

**Model (exact).**
- `QS = 0.985`, `QT = 0.30`, installs per day `I` (default 2,000).
- Onboarding mode (default): `w(c) = wBroken if breakOn and c ≥ P else wNormal`. Defaults `wNormal = 0.25`, `wBroken = 0.15`, `P = 20`.
- Endgame mode: `w(c) = wNormal` for all `c`; stayers' survival is `QS` on calendar days `≤ P` and `qsAfter` (default 0.97) after. For `a ≥ 1`: `after = max(0, min(a, c + a − P))`; `R(c, a) = w × QS^(a − after) × qsAfter^after + (1 − w) × QT^a`.
- Onboarding mode for `a ≥ 1`: `R(c, a) = w(c) × QS^a + (1 − w(c)) × QT^a`.
- Outage: if `outageOn` and `c + a = O` and `a ≥ 1`, multiply by `m`. Defaults `O = 40`, `m = 0.4`.
- `R(c, 0) = 1`. `DAU(t) = Σ over c = 0..t of I × R(c, t − c)`.
- Optional noise toggle (default off): each cell becomes `Binomial(I, R(c, a)) / I`, drawn from a seeded generator (seed shown, with a "reroll" button). DAU uses the noisy cells.
- Counterfactual ghost: DAU with `breakOn = false` and `outageOn = false`, drawn faintly on the top view.

**Controls.** Patch type radio: "Onboarding (cohorts from day P)" or "Endgame (calendar days from P)". Break toggle (default on), `P` 5 to 60 (default 20 for onboarding, 45 when switching to endgame), `wBroken` 0.05 to 0.35 step 0.01, `qsAfter` 0.90 to 0.995 step 0.005. Outage toggle (default on), `O` 5 to 70, `m` 0 to 1 step 0.05. Installs per day 250 to 5,000. Noise toggle and seed. Presets: "Lecture example", "Outage only", "Break only", "Endgame patch", "Break then fix" (a second step at `c = 50` restoring `wNormal`).

**Linking.** Hovering or keyboard-focusing a triangle cell highlights its row, its column and its diagonal, marks calendar day `c + a` on the DAU chart and the three checkpoint points of cohort `c` on the bottom chart. A readout shows `cohort c, age a, calendar day c + a, retention x%`. Clicking a DAU day highlights its diagonal in the triangle.

**Readouts.** For the default scenario: step size at `P` for D1, D7 and D30 in points and percent; the three install days where the outage appears (`O − 1`, `O − 7`, `O − 30`); DAU on day 70 and its gap to the counterfactual; the standard error of the D7 difference for one cohort, `sqrt(p1(1 − p1)/I + p2(1 − p2)/I)`, and the difference in standard errors.

**Test values (defaults).**
- D1, D7, D30 for cohorts 9, 10, 19, 20, 33, 39: 47.1/22.5/15.9; 47.1/22.5/6.4; 47.1/22.5/15.9; 40.3/13.5/9.5; 40.3/5.4/9.5; 16.1/13.5/9.5 (percent).
- Triangle rows 18 to 22, ages 0 to 3: rows 18 and 19 are 100, 47.1, 31.0, 25.9; rows 20 to 22 are 100, 40.3, 22.2, 16.6.
- Outage diagonal, rows 36 to 40, ages 0 to 4: row 36 is 100, 40.3, 22.2, 16.6, 5.9; row 37 is 100, 40.3, 22.2, 6.7, 14.8; row 38 is 100, 40.3, 8.9, 16.6, 14.8; row 39 is 100, 16.1, 22.2, 16.6, 14.8; row 40 is 100, 40.3, 22.2, 16.6, 14.8.
- DAU on days 19, 25, 30, 39, 40, 41, 60, 70: 10,838; 12,104; 12,855; 14,073; 6,879; 14,322; 16,345; 17,199. Counterfactual on the same days: 10,838; 12,974; 14,612; 17,265; 17,539; 17,808; 22,218; 24,078.
- Signal: D1 difference 6.85 points, SE 1.56, 4.4 SE; D7 8.99 points, SE 1.21, 7.5 SE; D30 6.35 points, SE 1.05, 6.1 SE.
- Endgame preset (`P = 45`, `qsAfter = 0.97`, outage off): `R(10, 40) = 12.65%` (13.66% without the patch); `R(50, 7) = 20.22%` against 22.51% unpatched. D30 first differs from install day 16, D7 from 39, D1 from 45.

**Accessibility and style.** Heat map cells are focusable in a grid with arrow-key navigation and announce their readout. A color legend with numeric stops; the heat map uses a single-hue sequential ramp (ochre) that works in both color schemes. Controls are native inputs with labels. Readouts in an `aria-live="polite"` region. Respect `prefers-reduced-motion` and `prefers-color-scheme`. Palette from `templates/interactive-tokens.css`. No game names, logos or art in the graphic; the caption says "Invented game. The Destiny 2 case is discussed in the lecture."
