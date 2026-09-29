# MMO308 · Week 02 — KPIs: DAU, MAU, Stickiness, ARPDAU

**Why this matters:** MAU is the number studios put in press releases, and it is the KPI most easily moved by people who barely played. A launch, a free weekend or a sale can double it for a month and halve it the next, while the players who carry your game hardly change. This week you learn which KPI counts touches, which counts play, and how to read the two together.

**You will be able to:**
- Build a KPI tree that links revenue, DAU, MAU, stickiness, payer rate, ARPPU and ARPDAU, and state which factors multiply.
- Compute DAU, MAU, stickiness and player-days for a population of regulars and tourists, and predict how each responds to a spike of tourists.
- Explain the 30-day echo in a rolling MAU and compute when it happens and how large it is.
- Critique a KPI report that compares MAU across a launch quarter without an engagement-weighted measure beside it.

**Before class:** Seif El-Nasr, Drachen and Canossa (eds.), *Game Analytics* (Springer, 2013), chapter 4, Tim Fields, "Game Industry Metrics Terminology and Analytics Case Study" (pp. 53-71). Skim the "Monthly Active Users" table and its footnote in Activision Blizzard's Q4 2022 results release (SEC EDGAR, exhibit 99.1 to Form 8-K, 6 February 2023).

**Prerequisites from earlier courses:** [DB201 week 12, dashboards and KPIs](../../DB201-data-persistence-and-telemetry/lectures/w12-dashboards-and-kpis.md). This lecture assumes its definitions of DAU, WAU, MAU, stickiness and ARPDAU, its identity "stickiness = mean active days / window length", and its rule that distinct counts do not add. It does not repeat them. [GS101 week 11, free-to-play and live service](../../GS101-history-and-critical-study-of-games/lectures/w11-free-to-play-mobile-and-live-service.md) (ARPU as payer rate times average spend per payer). From this course, [week 1, what live ops is](w01-what-live-ops-is.md) (cohorts, tourists and stayers).

**Interactive:** [w02-mau-window.html](../examples/w02-mau-window.html), built from the spec at the end of this lecture. Keep it open during section 2.

---

## 1. KPIs form a tree

DB201 week 12 taught you that every KPI is a definition, with a threshold, a day boundary and a counting unit. This week takes the definitions as settled and asks how the KPIs relate to each other, and what each one is sensitive to.

Start from the number the business watches, revenue per day, and keep splitting it:

```
revenue per day = DAU × ARPDAU
ARPDAU          = payer rate × ARPPU
DAU             = MAU × stickiness       (mean DAU over the month)
```

- **Payer rate** is the share of a day's active users who spent money that day.
- **ARPPU** is average revenue per paying user: revenue divided by the number of payers. GS101 week 11 used the monthly version of this split, `ARPU = p × A`.
- **Stickiness** is mean DAU divided by MAU, as in DB201 week 12.

Drawn as a tree:

```
revenue/day
├── DAU
│   ├── MAU
│   └── stickiness
└── ARPDAU
    ├── payer rate
    └── ARPPU
```

Every link in the tree is a product. That has two consequences you will use all course.

**Growth rates multiply, they do not add.** Roblox's letter to shareholders for the fourth quarter of 2022 reported full-year 2022 average DAU of 56.0 million, up 23% on 2021, and average bookings per DAU (ABPDAU) of $51.29, down 14%. Bookings were $2.9 billion, up 5%. Check it with the tree: `1.23 × 0.86 = 1.058`, close to the reported 5% given that each percentage is rounded. A 23% gain and a 14% loss do not make a 9% gain.

**Units hide in the tree.** Roblox defines ABPDAU as bookings in a period divided by the average DAU of that period. For a year, that is a yearly number. Per day, $51.29 is about `51.29 / 365 = $0.14`. A studio that compares its own daily ARPDAU of $0.20 with Roblox's $51.29 has made a 365-fold error before doing any analysis. Always write the time unit next to a "per user" KPI.

Every node in the tree is a count (players, payers, dollars) or a ratio of counts. Ratios over a mixed population are weighted averages, and they move when the mix moves. Week 7 builds the full mix-and-rate decomposition for that problem. This week looks at a different trap, one that lives in the MAU node itself.

## 2. Worked example: the MAU that doubled and halved

### The hook

Activision Blizzard reported monthly active users (MAUs) for each of its three business units every quarter. For Blizzard, the unit that makes World of Warcraft, Overwatch and Diablo, the reported average MAU was 31 million for the quarter ending September 2022, **45 million** for the quarter ending December 2022 and **27 million** for the quarter ending March 2023.

The December quarter was crowded. The company's results release lists Wrath of the Lich King Classic (September 2022), the free-to-play launch of Overwatch 2 (October 2022) and World of Warcraft's Dragonflight expansion (November 2022). The release for the next quarter says Overwatch engagement "moderated" after the launch quarter, but that hours played were still about twice the level seen before the free-to-play launch.

Read the MAU line alone and it says Blizzard gained 14 million players in one quarter and lost 18 million the next, ending below where it started. Read the hours statement and the game that drove the spike doubled its engagement. Both can be true at once. The reason is what MAU counts.

Two details of Activision Blizzard's definition matter here. MAU is the number of individuals who accessed a particular game in a month, and a quarter's figure is the average of its three monthly values. Someone who plays two of the company's games counts twice. Nothing in that definition asks how much anyone played.

### The model

Split a game's monthly players into two kinds, as week 1 did with cohorts.

- **Regulars**: `R` players who each play on a share `p` of the days in the month.
- **Tourists**: `T` players who each play on `k` days of the month, where `k` is small.

Over a month of `D` days (use 30):

```
MAU          = R + T
player-days  = R × p × D + T × k
mean DAU     = player-days / D = R × p + T × k / D
stickiness   = mean DAU / MAU
```

A **player-day** is one player active on one day. Summed over a month, player-days is the same number as the sum of the daily DAUs, which DB201 called user-days. It weights each player by how often they played.

Now look at what a tourist does to each KPI. A tourist adds **1** to MAU, the same as a regular who played every day. A tourist adds `k / D` to mean DAU, which is `2 / 30 = 0.067` for someone who played twice. So MAU is a count of **touches**, and DAU is a measure of **play**. A month with many tourists pumps MAU far more than DAU, and pushes stickiness down.

### Numbers you can check

An invented MMO has three quarters. Before its big update, 1,000,000 regulars play 40% of days, and 200,000 tourists drift through, each playing 2 days. In the update quarter, tourists rise to 700,000 and 100,000 newcomers become regulars. The quarter after, the new regulars stay, and tourists fall back to 100,000.

| Quarter | Regulars `R` | Tourists `T` | MAU | Mean DAU | Stickiness | Player-days per month | Tourist share of MAU | Tourist share of player-days |
|---|---|---|---|---|---|---|---|---|
| Before | 1,000,000 | 200,000 | 1,200,000 | 413,333 | 0.344 | 12,400,000 | 16.7% | 3.2% |
| Update | 1,100,000 | 700,000 | 1,800,000 | 486,667 | 0.270 | 14,600,000 | 38.9% | 9.6% |
| After | 1,100,000 | 100,000 | 1,200,000 | 446,667 | 0.372 | 13,400,000 | 8.3% | 1.5% |

Check the update row by hand. MAU is `1,100,000 + 700,000 = 1,800,000`. Mean DAU is `1,100,000 × 0.4 + 700,000 × 2 / 30 = 440,000 + 46,667 = 486,667`. Stickiness is `486,667 / 1,800,000 = 0.270`.

Now read the table as a producer would.

- MAU went up 50%, then down 33%, back exactly to where it started. The headline says "all the new players left".
- Mean DAU went up 18%, then down 8%. It ended 8% **above** where it started.
- The regular base, the players who carry the game, grew 10% and stayed grown.
- Stickiness fell in the update quarter and then rose above its old level, because the new regulars stayed and the tourists left.

The tourists were 39% of MAU in the update quarter and under 10% of the play. MAU let the least engaged people in the game write the headline.

The same numbers in code, which runs as shown with `.venv/bin/python`:

```python
D = 30
quarters = {"before": (1_000_000, 0.40, 200_000, 2),
            "update": (1_100_000, 0.40, 700_000, 2),
            "after":  (1_100_000, 0.40, 100_000, 2)}
for name, (R, p, T, k) in quarters.items():
    mau = R + T
    dau = R * p + T * k / D
    print(f"{name:6s} MAU {mau:9,}  DAU {dau:9,.0f}  stickiness {dau / mau:.3f}")
```

It prints `update MAU 1,800,000  DAU   486,667  stickiness 0.270` on its middle line.

### The visual

Open `examples/w02-mau-window.html`. The top view is the dashboard: two lines, MAU and mean DAU, by month, each indexed to 100 in the first month so they share an axis. The bottom view is the population itself, one small square per 10,000 players, arranged by how many days each played that month: regulars as a tall column on the right, tourists as a wide spread on the left.

Drag the tourist slider for the update month from 0 to 2,000,000. On the top view the MAU line leaps and the DAU line barely moves. On the bottom view the new squares all land in the 1-day and 2-day columns. Then drag the regular-share-of-days slider `p` down from 0.40 to 0.30 with tourists held fixed. Now MAU does not move at all while DAU falls a quarter. The two situations are opposite. In the first, reach grew and engagement stood still. In the second, reach stood still and engagement fell. A MAU tile shows you only the first.

### Cross-game recognition

**Blizzard, fiscal 2022 to 2023.** Write the hook in the model's terms. MAU rose from 31 million to 45 million and fell to 27 million. The release says Overwatch's hours played in the first quarter of 2023 were about twice their level before the free-to-play launch. Hours played is an engagement-weighted measure, like player-days. So the model's pattern fits: a launch quarter full of tourists, which inflates `T` and therefore MAU, followed by a quarter in which `T` shrinks while the engaged base (`R × p`) stays larger than before. We cannot split Blizzard's numbers into `R` and `T`, because the company did not publish DAU or hours by quarter. That is exactly the lesson: a reported MAU without an engagement measure beside it cannot be interpreted.

**Roblox (fiscal 2022).** Roblox reports the opposite pair. It publishes average DAU and **hours engaged**, 49.3 billion hours in 2022, or about 2.4 hours per DAU per day, and does not publish MAU. In the model's terms, Roblox reports `mean DAU` and `player-days × hours per player-day`, the two numbers that weight people by play. Its definition also counts a user who plays across midnight only once, for the first day (DB201 week 12). That is a company choosing engagement-weighted KPIs for its main public figures.

**Steam concurrent players (week 1).** SteamCharts samples the number of players in a game at regular intervals and averages the samples over the month. Up to sampling error, that average equals the total hours played in the month divided by the hours in the month. Rewrite it in the model's form: `average CCU = Σ over players of hours played / (24 × D)`. A tourist who plays for two hours adds almost nothing to it. That is why the New World and Lost Ark charts in week 1 fall so steeply after launch. The average concurrent count weights each player by time played, and the tourists who pumped launch week contribute almost no hours after it.

**Stickiness rising while a game shrinks (DB201 week 12).** DB201 listed "high stickiness means the game is healthy" as a misconception. The model shows why. Set `T` to fall from 200,000 to 0 with `R` fixed: MAU drops 17% while stickiness rises from 0.344 to 0.400. Losing tourists raises stickiness, just as gaining them lowers it.

Four contexts: a publisher's MAU line, a platform that reports DAU and hours instead, Steam's concurrent-player averages and a DB201 misconception. One idea. MAU counts touches. DAU, player-days, hours and concurrent players count play. Read them together, or a wave of tourists will write your story.

### Eyes-open design judgment

- **Pair MAU with an engagement-weighted KPI, always.** Mean DAU, player-days or hours. If MAU moves and player-days does not, you gained or lost reach, not play. If player-days moves and MAU does not, your existing players changed their behavior, which is usually the more important news.
- **MAU is the right KPI for some questions.** How many people did the free weekend reach? How many potential payers saw the new shop? Reach matters for acquisition and for the top of the funnel in week 4. Use MAU for those questions and say so on the tile.
- **Count regulars directly.** Define a regular in advance (for example, active on 8 or more days of the last 28) and report the count. It is a cleaner health KPI than stickiness, because it does not move when tourists come and go. It moves when your core moves.
- **Do not set MAU as a team target.** A team rewarded for MAU will buy tourists with free weekends, re-engagement emails that bring people back for one login, cross-promotions. Each raises MAU for a month at the cost of lower stickiness and no durable change. Pair any reach target with a player-days or regulars guardrail, a metric that must not get worse while you chase the target.

## 3. Rolling windows remember for thirty days

Section 2 used calendar months. Many dashboards instead show a **rolling** MAU: on each day `t`, the number of distinct players active on any of the 30 days ending at `t`. A rolling window has a memory, and the memory produces an artifact every live team eventually sees.

Take a game with 1,000,000 regulars who each play 40% of days, and no tourists. Almost every regular plays at least once in any 30 days (the chance of missing all 30 is `0.6^30`, about 2 in 10 million), so rolling MAU is 1,000,000. DAU is 400,000. Stickiness, computed daily as `DAU / rolling MAU`, is 0.40.

On day 0 the studio runs a one-day free event. 300,000 tourists log in that day and never return.

| Day | DAU | Rolling 30-day MAU | Daily stickiness |
|---|---|---|---|
| −1 | 400,000 | 1,000,000 | 0.400 |
| 0 | 700,000 | 1,300,000 | 0.538 |
| 1 | 400,000 | 1,300,000 | 0.308 |
| 15 | 400,000 | 1,300,000 | 0.308 |
| 29 | 400,000 | 1,300,000 | 0.308 |
| 30 | 400,000 | 1,000,000 | 0.400 |

Day 0 is the last day of the first window that contains the tourists. Day 29 is the last day of the last one. On day 30 the event falls out of the window, and rolling MAU drops by 300,000 overnight. Stickiness "jumps 30%" from 0.308 to 0.400. No player did anything different on day 30. It is an echo of day 0.

Two practical rules follow.

- **Annotate the echo.** Every spike in the log produces a cliff in the rolling MAU exactly one window length later. Put the event's date on the dashboard, and the date it leaves the window beside it. A team that does not do this will hold a meeting about day 30.
- **Know which window you are reading.** A calendar MAU for a month containing the event and a rolling MAU on any day within 29 days after it both include the tourists. A rolling MAU on day 30 does not. When two reports disagree about MAU by exactly the size of an event, this is almost always the reason.

The same memory affects stickiness computed with a rolling WAU (7-day echo) and D30 retention charts (week 3), where an event on one calendar day shows up in different cohorts' curves at different ages.

## 4. Reading a KPI report

Put the three sections together into a checklist you run on any KPI change before you believe it. Use it in the lab and on every dashboard you inherit.

1. **Units and definition.** Per day or per period? Which DAU and MAU definitions (DB201 week 12)? Calendar or rolling window? Did any of these change between the two periods?
2. **Touches or play?** If the KPI counts people (MAU, reach, "players"), find the engagement-weighted KPI beside it (DAU, player-days, hours). Do they move together?
3. **Factors.** For a product (revenue = DAU × ARPDAU), report each factor's change. Do they move together or against each other?
4. **Windows.** Is there an event, launch or outage within one window length before the date? Is the change an echo?
5. **Mix.** Could the change come from who is playing rather than how they play? Week 7 gives you the decomposition.
6. **Noise.** Is the change larger than the normal movement of the same weekday? MA102 week 13's intervals apply to rates such as payer rate. Revenue per user is skewed by a few big spenders, so its noise is larger than intuition suggests. Week 6 returns to this.

A change that survives all six checks is worth a meeting. Many changes do not survive step 2.

## In-class activity (25 minutes)

Pairs. Each pair gets this monthly report from an invented MMO that ran a free weekend in March:

| Month | MAU | Mean DAU | Revenue per day | Payers per day |
|---|---|---|---|---|
| February | 250,000 | 90,000 | $27,000 | 3,600 |
| March | 400,000 | 97,500 | $28,275 | 3,900 |
| April | 240,000 | 92,000 | $28,520 | 3,680 |

1. **Tree (8 min).** For each month compute stickiness, ARPDAU, payer rate and ARPPU. Check that revenue per day equals mean DAU times ARPDAU, and that ARPDAU equals payer rate times ARPPU.
2. **Model (7 min).** Treat every month as 30 days. Assume February has no tourists, and March's extra MAU are tourists who each played `k` days. Solve for `k` from March's mean DAU, assuming regulars played as in February. Is the answer plausible for a free weekend?
3. **Headlines (5 min).** Write the careless headline for April ("MAU fell X%"). Then write two sentences a producer can act on, using DAU, stickiness and ARPDAU.
4. **Echo (5 min).** The free weekend was 14 and 15 March. On which day will a 30-day rolling MAU drop the tourists? What will daily stickiness do that day?

Expected output: a filled table, the value of `k`, both headlines and the echo date.

## Common misconceptions

- **"MAU fell a third, so we lost a third of our players."** In the worked example MAU returned from 1.8 million to 1.2 million while the regular base stayed 10% larger than before the update. MAU counts touches. Check player-days.
- **"A tourist and a regular count the same, so they matter the same."** Each adds 1 to MAU. A regular playing 12 days adds 6 times as much play as a tourist playing 2 days, and far more revenue.
- **"23% more users and 14% less per user is 9% growth."** Factors multiply: `1.23 × 0.86 = 1.058`, about 6%.
- **"Stickiness jumped on the 30th, the new patch worked."** Check whether an event fell out of the rolling window that day. In section 3, stickiness rises 30% on day 30 with nothing changed.

## Check yourself

1. A game has 500,000 regulars playing 50% of days and 300,000 tourists playing 3 days each in a 30-day month. Compute MAU, mean DAU, stickiness and the tourist share of player-days.
2. In the worked example's update quarter, how many tourists could the game add before stickiness fell below 0.20, with everything else fixed?
3. A game's revenue per day went from $50,000 to $54,000 while mean DAU went from 200,000 to 240,000. What happened to ARPDAU, in percent? Write the answer as a product of factors.
4. A studio reports "D30 stickiness", mean DAU over the last 30 days divided by rolling MAU, every day. A three-day event starts on 1 June and brings 50,000 tourists who each play once, on one of the three days. On which dates does rolling MAU drop them? What does the stickiness chart look like?
5. A producer proposes a target of "MAU +20% by year end". Name one cheap way to hit it that leaves the game no better, and the guardrail that would catch it.

<details>
<summary>Answers</summary>

1. MAU `= 800,000`. Player-days `= 500,000 × 0.5 × 30 + 300,000 × 3 = 7,500,000 + 900,000 = 8,400,000`. Mean DAU `= 280,000`. Stickiness `= 0.35`. Tourist share of player-days `= 900,000 / 8,400,000 ≈ 10.7%`, while tourists are 37.5% of MAU.
2. Stickiness `= (440,000 + T × 2 / 30) / (1,100,000 + T) = 0.20` gives `440,000 + 0.0667T = 220,000 + 0.2T`, so `T = 220,000 / 0.1333 ≈ 1,650,000` tourists.
3. ARPDAU went from `50,000 / 200,000 = $0.25` to `54,000 / 240,000 = $0.225`, down 10%. Revenue ratio `1.08 = 1.20 × 0.90`.
4. A tourist who played on 1 June leaves the window on 1 July (the 30-day window ending 30 June still contains 1 June). Those from 2 June leave on 2 July, and 3 June on 3 July. Stickiness dips for about a month and then steps back up over three days, 1 to 3 July, in three steps. The numerator (mean DAU over the last 30 days) also carries the event's extra player-days until the same dates, but they are small next to the 50,000 in MAU.
5. Free weekends, one-login rewards for lapsed players, or cross-promotion that brings people in for a single session all raise MAU for a month. A guardrail on player-days, on the count of regulars (for example, active 8 or more of the last 28 days), or on stickiness would show that the game's engaged base did not grow.

</details>

## Lab / assignment hook

[Lab 02, touches and play](../labs/lab02.md). You implement DAU, calendar and rolling MAU, stickiness, player-days and the KPI tree in Python, run them on 90 days of generated activity from an MMO that ran a free weekend, find the rolling-window echo, and write the one-page KPI report a producer should have received instead of "MAU down 31%". Deliverable: passing tests, charts and a 400-word report.

## Sources

- Activision Blizzard, Inc., Q3 2022, Q4 2022 and Q1 2023 results releases, exhibits 99.1 to Form 8-K filed 7 November 2022, 6 February 2023 and 26 April 2023 (SEC EDGAR, accessions 0001628280-22-028634, 0001628280-23-002422, 0001628280-23-013097). Blizzard average MAUs of 31, 45 and 27 million for the quarters ending September 2022, December 2022 and March 2023; the MAU definition (individuals who accessed a particular game in a month; period value is the average of monthly values; an individual playing two games counts twice); the October 2022 free-to-play launch of Overwatch 2, the September 2022 release of Wrath of the Lich King Classic and the November 2022 launch of Dragonflight; Overwatch hours played in Q1 2023 about twice the level before the free-to-play launch. One short phrase quoted.
- Roblox Corporation, Q4 2022 letter to shareholders, exhibit 99.2 to Form 8-K filed 15 February 2023 (SEC EDGAR, accession 0001315098-23-000017). Full-year 2022 average DAU 56.0 million, up 23%; bookings $2.9 billion, up 5%; ABPDAU $51.29, down 14%.
- Roblox Corporation, Annual Report on Form 10-K for fiscal 2022, filed 28 February 2023 (SEC EDGAR, accession 0001315098-23-000035). Definitions of DAU, hours engaged and ABPDAU ("Key Metrics"); 49.3 billion hours engaged in 2022, an average of 2.4 hours per DAU each day.
- SteamCharts, "New World: Aeternum" and "Lost Ark", read September 2026 (see week 1).
- Fields, T. (2013). "Game Industry Metrics Terminology and Analytics Case Study." In Seif El-Nasr, Drachen & Canossa (eds.), *Game Analytics*, Springer, pp. 53-71.

## Interactive spec: examples/w02-mau-window.html

**The one insight.** MAU counts touches and DAU counts play. A wave of tourists moves MAU a lot and DAU a little, so the two lines can tell opposite stories. The top (dashboard) view shows the lines; the bottom view shows the players behind them, sorted by days played, and makes it obvious where the new MAU landed.

**Layout.** Two linked views stacked vertically. Top: "What the dashboard shows", two lines over 6 months (MAU and mean DAU, each indexed to 100 in month 1) plus stickiness in its own small chart underneath (0 to 0.6), not on a secondary axis, so the ratio never appears to cross the counts. Bottom: "Who is behind it", for the selected month, a histogram of players by days played (1 to 30), drawn as stacked unit squares (one square per 10,000 players; tourists in blood, regulars in steel). A tab switches the bottom view to "Rolling window" (section 3 mode).

**Model, monthly mode (exact).** For month `m`: `MAU = R_m + T_m`; `playerDays = R_m × p_m × 30 + T_m × k_m`; `meanDAU = playerDays / 30`; `stickiness = meanDAU / MAU`. Regulars' days played are drawn as a binomial(30, `p_m`) histogram scaled to `R_m` (compute exact binomial probabilities; do not simulate). Tourists all sit at `k_m` days.

**Controls, monthly mode.** Month selector 1 to 6. For the selected month: regulars `R` 0 to 3,000,000 step 50,000; regular share of days `p` 0.05 to 0.90 step 0.01; tourists `T` 0 to 3,000,000 step 50,000; tourist days `k` 1 to 5. Default six months: months 1-2 "before" (1,000,000, 0.40, 200,000, 2); month 3 "update" (1,100,000, 0.40, 700,000, 2); months 4-6 "after" (1,100,000, 0.40, 100,000, 2). Presets: "Lecture example" (the defaults), "Engagement drop" (all months as before, but `p = 0.30` from month 4), "Tourists leave" (`T` falls to 0 from month 4, `R` fixed at 1,000,000).

**Model, rolling mode (exact).** Days −10 to 45. Regulars `R = 1,000,000`, `p = 0.40`; a one-day event on day 0 with `E` tourists (slider 0 to 1,000,000, default 300,000) who play only that day; window length `W` (7 or 30, default 30). `DAU(t) = R × p + (t == 0 ? E : 0)`. `rollingMAU(t) = R × (1 − (1 − p)^W) + (0 ≤ t ≤ W − 1 ? E : 0)`. Daily stickiness `= DAU(t) / rollingMAU(t)`. Mark day 0 and day W with vertical rules labeled "event" and "event leaves window".

**Readouts.** Monthly mode: MAU, mean DAU, stickiness, player-days, tourist share of MAU and of player-days, and month-over-month percent change of MAU and mean DAU. Rolling mode: the values at a scrubbed day.

**Test values.**
- Month 1: MAU 1,200,000; mean DAU 413,333; stickiness 0.344; player-days 12,400,000; tourist shares 16.7% and 3.2%.
- Month 3: MAU 1,800,000; mean DAU 486,667; stickiness 0.270; player-days 14,600,000; tourist shares 38.9% and 9.6%. MAU +50.0%, DAU +17.7% versus month 2.
- Month 4: MAU 1,200,000; mean DAU 446,667; stickiness 0.372; tourist shares 8.3% and 1.5%. MAU −33.3%, DAU −8.2% versus month 3.
- "Tourists leave" preset, month 4: MAU 1,000,000; stickiness 0.400.
- Rolling mode defaults: day −1 stickiness 0.400; day 0 DAU 700,000, MAU 1,300,000, stickiness 0.538; days 1 to 29 stickiness 0.308; day 30 stickiness 0.400. With `W = 7`: the drop happens on day 7.

**Accessibility and style.** Native range inputs with labels and live values; keyboard operable with visible focus. Readouts in an `aria-live="polite"` region. The histogram has a text alternative listing counts per days-played bucket. Respect `prefers-reduced-motion` and `prefers-color-scheme`. Palette from `templates/interactive-tokens.css`: MAU in ochre, DAU in steel, stickiness in ink, tourists in blood. No game names, logos or art in the graphic; the caption says "Invented game. The Blizzard MAU figures are discussed in the lecture."
