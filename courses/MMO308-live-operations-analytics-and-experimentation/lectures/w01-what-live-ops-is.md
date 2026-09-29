# MMO308 · Week 01 — What Live Ops Is

**Why this matters:** Every online game you have played lost most of its launch crowd within months, and most of them kept running anyway. Live operations is the job of keeping a world alive after that first rush, and it starts with one uncomfortable fact. The size of your game next year is set far more by what you do every week than by how big the launch was.

**You will be able to:**
- Define live operations and name the recurring work it covers, from content cadence to incident response.
- Compute a game's weekly active players as a stack of install cohorts, and its long-run plateau from installs and expected lifetime.
- Explain, with numbers, why a launch cohort dominates the player count for months and then vanishes from it.
- Compare live-ops levers (acquisition, onboarding, endgame retention) by how much each moves the plateau.

**Before class:** Seif El-Nasr, Drachen and Canossa (eds.), *Game Analytics: Maximizing the Value of Player Data* (Springer, 2013), chapter 1, "Introduction" (pp. 3-12), and chapter 3, "Benefits of Game Analytics: Stakeholders, Contexts and Domains" (pp. 41-52). Skim Jorge Mazal, "How Duolingo reignited user growth" (Lenny's Newsletter, 28 February 2023).

**Prerequisites from earlier courses:** [DB201 week 12, dashboards and KPIs](../../DB201-data-persistence-and-telemetry/lectures/w12-dashboards-and-kpis.md) (DAU, WAU, retention and why each is a definition). [GD102 week 2, stocks and flows](../../GD102-systems-design-and-game-mechanics/lectures/w02-stocks-and-flows.md) (the bathtub rule). [MMO301 week 12, persistence and time](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w12-persistence-and-time-what-should-last.md) (Little's law, `S = λ × W`). [GS101 week 11, free-to-play and live service](../../GS101-history-and-critical-study-of-games/lectures/w11-free-to-play-mobile-and-live-service.md) (expected lifetime under constant retention).

**Interactive:** [w01-layer-cake.html](../examples/w01-layer-cake.html), built from the spec at the end of this lecture. Keep it open during section 2.

---

## 1. A game that is never finished

A boxed game ships once. The team fixes a few bugs, maybe sells an expansion, and moves on. An MMO ships on launch day and then keeps shipping for as long as the servers stay up. The work of running the game after launch is called **live operations**, usually shortened to **live ops**.

Live ops covers every recurring decision a team makes about a game that players are already inside:

- **Content cadence.** How often new quests, zones, items or seasons arrive, and how big each drop is. Old School RuneScape, for example, pushes game updates on Wednesdays at 11:30 UK time, most weeks of the year.
- **Events.** Time-limited activities that give players a reason to log in this week rather than next (week 8).
- **Patches and hotfixes.** Balance changes and bug fixes, planned or emergency (week 9).
- **Economy monitoring.** Watching faucets, sinks and prices so that a bug or an exploit does not wreck the currency (week 12, building on MMO304).
- **Community and feedback.** Reading forums, running surveys and, in some games, letting players vote on changes (weeks 10 and 11).
- **Incidents.** Outages, exploits and data problems handled while the world is running (week 13).
- **Measurement.** The telemetry, KPIs and experiments that tell the team whether any of the above worked (weeks 2 to 7).

What ties these together is a loop. You **measure** what players are doing, **decide** what to change, **change** it in the live game, and **measure** again. The loop never ends, and it has two properties that make it harder than pre-launch development.

First, every change lands on real people with real investments. You cannot "undo" a nerf to a weapon someone spent a month earning, and you cannot delete gold that is already in circulation without a riot. Second, the loop runs on data the team did not design for this exact question. Most live-ops analysis is reading a signal out of a player count that many things move at once.

This course is about running that loop well. This week sets up the one picture every later week refers back to, the picture of what a player count is made of.

## 2. Worked example: the launch cliff and the layer cake

### The hook

New World launched on Steam on 28 September 2021. SteamCharts, which samples Steam's concurrent player counts, records an average of about 410,000 concurrent players in October 2021 and a peak of 913,027. By June 2022 the monthly average was about 13,600, roughly 3% of October's.

Lost Ark launched in Europe and the Americas on 11 February 2022, published by Amazon Games. SteamCharts records a February 2022 average of about 699,000 concurrent players and a peak of about 1.32 million. By September 2022 the average was about 149,000, roughly 21% of February's.

Players and journalists read charts like these as verdicts. One game "died" and one "held on." Both charts share a shape, a cliff followed by a long, low shelf. Here is the question for this week. Suppose a game has nothing wrong with it at all. Its new players like it exactly as much in month six as in week one. What does its player chart look like? The answer surprises most people. It looks like a cliff.

Keep in mind what these numbers are. They are concurrent players on Steam only, averaged per month. DB201 week 12 warned you that a concurrent count and an active-user count are different KPIs, so we will compare shapes, never levels.

### The model

Split players by the week they installed. Each group of players who started in the same week is a **cohort**. A **retention curve** `R(a)` gives the share of a cohort still active `a` weeks after install, with `R(0) = 1` (everyone is active in their install week).

The weekly active players (WAU) in week `t` are the sum of what is left of every cohort:

```
WAU(t) = Σ over s ≤ t of  I(s) × R(t − s)
```

- `I(s)` is the number of installs in week `s`.
- `t − s` is the cohort's **age** in weeks.
- Each term is one **layer**: the players from cohort `s` who are still around in week `t`.

Stack the layers and you get the player count. That is why this picture is called a **layer cake** (some teams say a cohort stack chart).

For the retention curve, use the simplest shape that behaves like real data. Real retention curves drop steeply at first and then flatten, because each cohort mixes people who were never going to stay with people who will play for years. So model a cohort as two kinds of player:

```
R(a) = w × qs^a + (1 − w) × qt^a
```

- `w` is the share of **stayers** in each cohort.
- `qs` is the weekly survival of a stayer: the chance a stayer active this week is active next week.
- `qt` is the weekly survival of a **tourist**, someone who came to look around.

If every week brings the same number of installs `I`, the cake stops changing height once the old layers have worn away. That height is the **plateau**:

```
plateau = I × L,   where   L = Σ over a ≥ 0 of R(a) = w / (1 − qs) + (1 − w) / (1 − qt)
```

`L` is the expected number of active weeks per install. The plateau formula is Little's law from MMO301 week 12, with players in place of world objects. The stock equals the arrival rate times the average time each arrival stays. The closed form for `L` is the geometric-lifetime result from GS101 week 11 (`1 / (1 − r)`) applied to each type of player and weighted by its share.

Notice what is missing from the plateau formula. **The launch is not in it.** The launch sets how high the cake starts and how long the cliff lasts. It has no say in where the shelf ends up.

### Numbers you can check

Take a reference game with `w = 0.30`, `qs = 0.90`, `qt = 0.30`. Its launch week brings 200,000 installs. Every week after that brings 10,000.

First the retention curve. Check each entry by hand.

| Age `a` (weeks) | Stayers `0.3 × 0.9^a` | Tourists `0.7 × 0.3^a` | `R(a)` |
|---|---|---|---|
| 0 | 0.300 | 0.700 | 1.000 |
| 1 | 0.270 | 0.210 | 0.480 |
| 2 | 0.243 | 0.063 | 0.306 |
| 3 | 0.219 | 0.019 | 0.238 |
| 4 | 0.197 | 0.006 | 0.203 |

Half the cohort is gone after one week, but by week 4 almost everyone left is a stayer, and the curve falls only 10% a week from then on.

The expected lifetime is `L = 0.3 / 0.1 + 0.7 / 0.7 = 3 + 1 = 4` weeks. So the plateau is `10,000 × 4 = 40,000` WAU.

Now the cake. Week 1 has the launch cohort at age 1 (`200,000 × 0.48 = 96,000`) plus the brand-new week-1 cohort (10,000), so WAU is 106,000. Week 2 has `200,000 × 0.306 = 61,200` from launch, `10,000 × 0.48 = 4,800` from week 1 and 10,000 new, so 76,000.

| Week | Launch layer | All later layers | WAU | Share of WAU from launch cohort | WAU as % of launch week |
|---|---|---|---|---|---|
| 0 | 200,000 | 0 | 200,000 | 100% | 100% |
| 1 | 96,000 | 10,000 | 106,000 | 91% | 53% |
| 2 | 61,200 | 14,800 | 76,000 | 81% | 38% |
| 4 | 40,500 | 20,236 | 60,736 | 67% | 30% |
| 8 | 25,837 | 27,085 | 52,923 | 49% | 26% |
| 12 | 16,946 | 31,527 | 48,473 | 35% | 24% |
| 26 | 3,877 | 38,062 | 41,938 | 9% | 21% |
| 52 | 250 | 39,875 | 40,125 | 1% | 20% |

Read the last column. A game with nothing wrong with it lost 62% of its players in two weeks and 76% in three months. Its retention never changed. Its installs never changed after launch week. The cliff is pure arithmetic: a huge layer at the bottom of the cake wearing away at the rate every cohort wears away.

Read the second-to-last column too. At week 8, half of all active players are still from launch week. Any dashboard number averaged over "active players" in the first two months mostly describes launch players, the most enthusiastic people the game will ever get. By week 26 they are 9% of the player base, and the game's typical player is someone who arrived later, through a different door.

This code reproduces the table. It runs as shown with `.venv/bin/python`:

```python
def R(a, w=0.30, qs=0.90, qt=0.30):
    return w * qs**a + (1 - w) * qt**a

installs = [200_000] + [10_000] * 52
for t in (0, 1, 2, 4, 8, 12, 26, 52):
    launch = installs[0] * R(t)
    total = sum(installs[s] * R(t - s) for s in range(t + 1))
    print(f"week {t:2d}: WAU {total:8,.0f}  launch share {launch / total:4.0%}")
```

It prints `week 12: WAU   48,473  launch share  35%` and `week 52: WAU   40,125  launch share   1%`, matching the table.

### The visual

Open `examples/w01-layer-cake.html`. The top view is a single line, total WAU by week, the way a dashboard or SteamCharts shows it. The bottom view is the same numbers as a stacked area: the launch cohort in one color at the bottom and later cohorts stacked above it in bands.

Drag the launch-installs slider from 50,000 to 500,000. The top line gets a taller spike and a steeper cliff. Now look at the right edge of the chart. Every setting lands on the same shelf at 40,000, marked by a dashed line. Then drag the ongoing-installs slider or the stayer-share slider. The shelf itself moves. The picture to take away is this. The top view makes the launch look like the most important number in the game's life, and the bottom view shows it is a layer that wears away.

### Cross-game recognition

**New World and Lost Ark (Steam, 2021-2022).** Put the hook into the model's terms. The ratio of the shelf to the launch month is roughly `I × L / launch`, the ongoing inflow times the lifetime divided by the launch size. New World's June 2022 average was about 3% of its October 2021 average. Lost Ark's September 2022 average was about 21% of February's, close to our reference game's 20%. The model does not tell you why the two differ. It tells you where to look: at how many players each game kept attracting after launch (`I`), and how long those players stayed (`L`). A shelf at 3% of launch means `I × L` is small next to the launch, which can come from few new players, short lifetimes, or an enormous launch. Both charts also show later bumps, with Lost Ark's average rising again in May and June 2022 and New World's rising in autumn 2022. In the model, a bump is a new thick layer: a week when `I(s)` jumped because something brought new or returning players in at once. Week 3 shows how to tell such a layer apart from a change that hits every layer.

**Duolingo's growth model (described in 2023).** Duolingo is a learning app, but it runs the same loop as a live game, with streaks, leagues and daily goals. Jorge Mazal, writing about his years at Duolingo, described how the company split its users into states (new, current, reactivated, resurrected, at risk, dormant) and modeled daily active users as flows between them. When they tested which transition rate moved DAU the most, the retention rate of **current** users, people already active in the past week, beat the runner-up by about five times. Rewrite that in our form. Current users are the stayers, and their retention is `qs`. Because `L` contains the term `w / (1 − qs)`, a small change in `qs` near 1 moves `L` a lot. Mazal reports that Duolingo's DAU grew about 4.5 times over four years after they made that rate their main target.

**Objects in a world (MMO301 week 12) and players in a login queue (MMO302 week 9).** The plateau `I × L` is the same equation as the clutter law `S = λ × W` for dropped items and houses, and the queue-length rule for a login queue. Items spawn and despawn. Players queue and get in. Players install and leave. In each case the long-run stock is inflow times average stay, and the starting stock only decides how long the system takes to get there.

Three contexts: two MMO launches on Steam, a learning app's growth model, and the stock of objects in a world. One idea. A population is a stack of arrivals minus departures, and its long-run size is set by the inflow and the stay, not by the first wave.

### Eyes-open design judgment

- **Judge a launch by its layers, not its peak.** A launch cohort that is five times the ongoing inflow will produce a cliff to about 20% even if every player is treated perfectly. Before you panic about a drop, compute what the drop would be with unchanged retention. The gap between that and reality is the real signal.
- **Buy capacity for the launch, staff for the shelf.** Servers can scale down after a launch cliff (MMO302 week 13 covers autoscaling). Teams, budgets and content plans should be sized for the plateau, because that is the game you will run for years.
- **The top line lags.** For the first months, most active players are launch players. A problem that affects only new players (a broken tutorial, a confusing first zone) will barely move WAU until the launch layer has worn away. Week 3 builds the chart that catches it early.
- **The same two-type idea comes back.** Week 4 turns the stayers' weekly survival into a churn rate, and week 14 uses a mixture of fast and slow leavers to forecast when a declining game stops paying.
- **The model is a baseline, not a forecast.** It assumes installs are steady, retention does not depend on the calendar, and every cohort is alike. Real games break all three. Events change retention on specific dates, cohorts from a marketing campaign differ from organic ones, and updates bring back lapsed players. Use the model to set expectations, then study where reality departs from it.

## 3. Four levers, and what each is worth

The plateau formula tells you what live ops can change. There are only two terms, the inflow `I` and the lifetime `L`, and `L` has three parameters. Here is what a plausible improvement to each is worth for the reference game.

| Lever | Change | New `L` (weeks) | New plateau | Change |
|---|---|---|---|---|
| Acquisition: marketing, platforms, referrals | `I` from 10,000 to 12,000 per week | 4.00 | 48,000 | +20% |
| Onboarding: tutorial, first zone, first group | `w` from 0.30 to 0.36 | 4.51 | 45,143 | +13% |
| Endgame: content, social ties, progression | `qs` from 0.90 to 0.92 | 4.75 | 47,500 | +19% |
| First impression for tourists | `qt` from 0.30 to 0.40 | 4.17 | 41,667 | +4% |

Check one. With `qs = 0.92`, `L = 0.3 / 0.08 + 0.7 / 0.7 = 3.75 + 1 = 4.75`.

Three lessons come out of this table.

The first is that making tourists stay a little longer is worth little. Tourists leave fast whatever you do, and a 0.3 to 0.4 change in their weekly survival adds a sixth of a week to each one. The large gains come from turning more arrivals into stayers (`w`) or keeping stayers longer (`qs`).

The second is that the levers are not free and not equal in cost. A 20% rise in installs usually costs marketing money every single week, and stops when the money stops. A two-point rise in stayer survival comes from content and systems that keep working once built. Live-ops teams argue about this trade-off constantly. The table gives the argument a common unit, players at the plateau.

The third is that the `qs` lever gets stronger as `qs` rises. Going from 0.90 to 0.92 cuts stayer churn from 10% to 8% a week, a fifth of it. Going from 0.95 to 0.97 cuts it by two fifths. This is why Duolingo's current-user retention dominated its model, and why MMO teams spend most of their content budget on players who are already at the level cap.

## 4. The loop in practice

A live-ops team turns the loop from section 1 into a schedule. A typical week for a mid-sized MMO might look like this:

- **Daily.** Check the dashboard, with DB201 week 12's rules (definitions on every tile, like-for-like comparisons). Triage bugs and exploit reports. Watch the economy's money supply.
- **Weekly.** Ship a small update or hotfix. Review the last week's cohorts. Decide which experiments to start or stop.
- **Per season or patch (every 2 to 4 months in many MMOs).** Ship a content drop, run an event, review the retention of cohorts that arrived since the last drop.
- **Yearly.** Plan the calendar (week 8), set KPI targets, decide what to sunset (week 14).

Each item on that schedule is a bet on one of the four levers. A new raid is a bet on `qs`. A tutorial rework is a bet on `w`. A free weekend is a bet on `I`, usually with a spike of tourists who have a low `w`. The discipline of live ops is naming the lever before you ship, predicting the size of the effect in plateau terms, and checking afterwards. A team that cannot say which lever a piece of work pulls cannot tell whether it worked.

That check is harder than it sounds, because the player count moves for many reasons at once. The next five weeks give you the tools. Week 2 separates KPIs that count touches, such as MAU, from KPIs that count play. Week 3 builds the cohort charts that separate "new players are having a worse time" from "everyone had a bad Tuesday." Week 4 finds where players leave within their first sessions. Weeks 5 and 6 cover the controlled experiment, the only method that tells you a change caused an effect rather than arriving alongside it.

## In-class activity (25 minutes)

Groups of three. Each group gets one invented game card:

- **A.** Launch week 400,000 installs, then 5,000 per week. `w = 0.20`, `qs = 0.92`, `qt = 0.25`.
- **B.** Launch week 60,000 installs, then 8,000 per week. `w = 0.35`, `qs = 0.88`, `qt = 0.30`.
- **C.** Launch week 150,000 installs, then 12,000 per week. `w = 0.15`, `qs = 0.95`, `qt = 0.20`.

1. **Plateau (5 min).** Compute `L` and the plateau by hand. Express the plateau as a percentage of launch-week WAU.
2. **Cliff (5 min).** Using the interactive's custom mode, read off WAU in weeks 4, 12 and 26, and the week in which the launch cohort falls below half of WAU.
3. **Levers (10 min).** Your studio can afford exactly one of: +25% ongoing installs, `w` up by 0.05, or `qs` up by 0.02. Compute each one's plateau. Pick one and justify it in two sentences, including what it would cost to sustain.
4. **Report (5 min).** One sentence to a producer who says "we lost 70% of our players, the game is failing." Use your numbers.

Expected output: a filled card with `L`, plateau, three WAU values, the lever table and the one-sentence reply.

## Common misconceptions

- **"The drop after launch means players didn't like the game."** A cliff appears even when retention is constant and healthy. In the reference game WAU falls 76% in 12 weeks with nothing wrong. Compare the real drop with the drop the model predicts from your own retention curve before you conclude anything.
- **"A bigger launch means a bigger game."** The plateau is `I × L`. The launch size is not in it. A bigger launch buys a taller spike and a longer cliff, plus the chance that some launch players tell their friends, which shows up as a higher `I` later.
- **"Average player behavior in month one describes our players."** In month one most active players are launch players. In the reference game they are still 49% of WAU in week 8 and 9% in week 26.
- **"Live ops means events."** Events are one tool. Live ops is the whole measure-decide-change-measure loop, including patches, economy monitoring, community work and incident response.

## Check yourself

1. A game gets 15,000 installs per week after launch. Its retention has `w = 0.25`, `qs = 0.94`, `qt = 0.30`. Compute `L` and the plateau.
2. In the reference game, what is WAU in week 3? Show the three layers you add (launch, week 1, week 2) plus the new week-3 cohort.
3. A producer proposes a free-to-play weekend that brings a one-off extra 50,000 installs in week 30, with the same retention curve as everyone else. How much does it add to WAU in week 31 and in week 60? What does it do to the plateau?
4. For the reference game, which is worth more at the plateau: raising `w` from 0.30 to 0.40, or raising `qs` from 0.90 to 0.93? Show both `L` values.
5. A game's WAU is flat at 60,000 and its ongoing installs are 12,000 a week. What is its expected lifetime? If a tutorial fix raises `L` by 10%, where will WAU settle, and why does it take months to get there?

<details>
<summary>Answers</summary>

1. `L = 0.25 / 0.06 + 0.75 / 0.70 = 4.167 + 1.071 = 5.238` weeks. Plateau `= 15,000 × 5.238 ≈ 78,571`.
2. Launch layer `200,000 × R(3) = 200,000 × 0.2376 = 47,520`. Week-1 cohort at age 2: `10,000 × 0.306 = 3,060`. Week-2 cohort at age 1: `10,000 × 0.48 = 4,800`. New week-3 cohort: 10,000. WAU `= 65,380`.
3. Week 31 (age 1): `50,000 × 0.48 = 24,000`. Week 60 (age 30): `50,000 × (0.3 × 0.9^30 + 0.7 × 0.3^30) ≈ 50,000 × 0.0127 ≈ 636`. The plateau is unchanged, because it depends only on the steady inflow and `L`. The weekend adds a layer that wears away.
4. `w = 0.40`: `L = 0.4 / 0.1 + 0.6 / 0.7 = 4 + 0.857 = 4.857`. `qs = 0.93`: `L = 0.3 / 0.07 + 1 = 4.286 + 1 = 5.286`. The `qs` change is worth more, 52,857 against 48,571 at 10,000 installs a week.
5. At the plateau, `L = WAU / I = 60,000 / 12,000 = 5` weeks. After the fix, `L = 5.5` and WAU settles at 66,000. It takes months because only new cohorts get the better tutorial. The old layers keep their old retention and must wear away first, at the stayers' slow rate.

</details>

## Lab / assignment hook

[Lab 01, the layer cake](../labs/lab01.md). You implement the cohort-stack model in Python, reproduce this lecture's table, compare the model's cliff with the New World and Lost Ark monthly averages, and write a lever memo for a studio choosing between a marketing push and an endgame update. Deliverable: passing tests, a stacked-area chart and a 400-word memo.

## Sources

- SteamCharts, "New World: Aeternum" (app 1063730) and "Lost Ark" (app 1599340), monthly average and peak concurrent Steam players, read September 2026. New World: October 2021 average 410,171, peak 913,027; June 2022 average 13,615. Lost Ark: February 2022 average 699,094, peak 1,324,761; September 2022 average 149,088; May and June 2022 averages 489,020 and 465,789. Steam only; concurrent players, not active users.
- Wikipedia, "New World: Aeternum" (read September 2026). Windows release on 28 September 2021.
- Wikipedia, "Lost Ark (video game)" (read September 2026). Release in Europe, North America and South America on 11 February 2022 by Amazon Games.
- Old School RuneScape Wiki, "Game updates" (read September 2026). Game updates occur on Wednesdays at 11:30 UK time.
- Mazal, J. (28 February 2023). "How Duolingo reignited user growth." Lenny's Newsletter. User states, the finding that current-user retention had about five times the DAU impact of the next rate, and DAU growth of about 4.5 times over four years. Paraphrased.
- Little, J. D. C. (1961). "A Proof for the Queuing Formula L = λW." *Operations Research* 9(3), 383-387.
- Seif El-Nasr, M., Drachen, A. & Canossa, A. (eds.) (2013). *Game Analytics: Maximizing the Value of Player Data*. Springer. Chapter 1 (pp. 3-12) and chapter 3 (pp. 41-52).

## Interactive spec: examples/w01-layer-cake.html

**The one insight.** The launch sets the height of the spike and the length of the cliff, but the long-run player count (the shelf) is `I × L` and does not depend on the launch at all. The top view makes the launch look decisive; the bottom view shows it is a layer that wears away.

**Layout.** Two linked views stacked vertically on all widths. Top: "What the dashboard shows", a single line of total WAU by week (weeks 0 to 78). Bottom: "What it is made of", the same total as a stacked area of cohort layers. Both share the x-axis. A control panel sits beside the views on wide screens and between them on narrow screens. A number panel shows the key readouts at all times.

**Model (exact).**
- `R(a) = w × qs^a + (1 − w) × qt^a` for integer `a ≥ 0`.
- Installs: `I(0) = launch`, `I(s) = ongoing` for `s ≥ 1`. Optional one-off bump: if the bump toggle is on, `I(bumpWeek) += bumpSize`.
- `layer(s, t) = I(s) × R(t − s)` for `s ≤ t`; `WAU(t) = Σ layer(s, t)`.
- `L = w / (1 − qs) + (1 − w) / (1 − qt)`; `plateau = ongoing × L`.
- Launch share at week `t` = `layer(0, t) / WAU(t)`.

**Controls.**
- Launch installs: 0 to 500,000, step 10,000, default 200,000.
- Ongoing installs per week: 1,000 to 30,000, step 500, default 10,000.
- Stayer share `w`: 0.05 to 0.60, step 0.01, default 0.30.
- Stayer weekly survival `qs`: 0.80 to 0.98, step 0.01, default 0.90.
- Tourist weekly survival `qt`: 0.05 to 0.60, step 0.01, default 0.30.
- Bump toggle (default off), with bump week 1 to 78 (default 30) and bump size 0 to 200,000 (default 50,000).
- Preset buttons: "Reference game" (the defaults), and the in-class cards A, B and C (A: 400,000 / 5,000 / 0.20 / 0.92 / 0.25; B: 60,000 / 8,000 / 0.35 / 0.88 / 0.30; C: 150,000 / 12,000 / 0.15 / 0.95 / 0.20).
- A week scrubber (slider 0 to 78, default 12) that draws a vertical rule on both views.

**Top view.** Line of `WAU(t)`. Dashed horizontal line at the plateau, labeled "shelf = I × L = 40,000". Ghost line of the reference-game WAU stays faintly visible when parameters change, so the student sees what moved.

**Bottom view.** Stacked areas, bottom to top: launch cohort (ochre), cohorts 1-4, 5-12, 13-26, 27+ (four steel tints from dark to light). A one-off bump cohort, when on, is its own band in blood red. Hovering or focusing a band shows its name and value at the scrubbed week.

**Number panel (at the scrubbed week).** WAU; launch layer; launch share (%); WAU as % of launch-week WAU; `L` in weeks (2 decimals); plateau; plateau as % of launch-week WAU; first week in which launch share drops below 50%.

**Secondary panel, "levers".** A four-row table recomputed live from the current parameters: plateau after +20% ongoing installs; after `w + 0.06`; after `qs + 0.02` (capped at 0.99); after `qt + 0.10`. Each row shows the new `L`, the new plateau and the percent change.

**Test values (reference game).**
- `R(0..4) = 1.000, 0.480, 0.306, 0.2376, 0.2025`.
- `L = 4.000`, plateau 40,000.
- WAU at weeks 0, 1, 2, 4, 8, 12, 26, 52: 200,000; 106,000; 76,000; 60,736; 52,923; 48,473; 41,938; 40,125.
- Launch share at weeks 8, 12, 26: 48.8%, 35.0%, 9.2%. First week below 50%: week 8.
- Levers: +20% installs gives 48,000 (+20.0%); `w = 0.36` gives `L = 4.514`, 45,143 (+12.9%); `qs = 0.92` gives `L = 4.750`, 47,500 (+18.8%); `qt = 0.40` gives `L = 4.167`, 41,667 (+4.2%).
- Launch 500,000 with everything else default: week 52 WAU 40,501 (the shelf is unchanged; at default launch it is 40,125).
- Bump on (week 30, 50,000): WAU at week 31 is higher than without the bump by 24,000.

**Accessibility and style.** Sliders are native range inputs with visible labels and live numeric values; all controls keyboard-operable with visible focus. The number panel is an `aria-live="polite"` region. Respect `prefers-reduced-motion` (no transitions) and `prefers-color-scheme`. Palette from `templates/interactive-tokens.css`, copied inline. No game names in the graphics, no logos or art; the caption says "Invented game. The New World and Lost Ark shapes are discussed in the lecture."
