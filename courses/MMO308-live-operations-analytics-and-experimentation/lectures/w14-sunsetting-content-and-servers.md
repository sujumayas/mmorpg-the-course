# MMO308 · Week 14 — Sunsetting Content and Servers

**Why this matters:** Every live game eventually removes things: an old raid, a quiet realm, the whole world. Players take each removal personally, and they are right to, because they paid for those things in time or money. The date you pick is a forecast, and a forecast from the wrong curve can close a world with years of life left, or keep one running at a loss long after it should have ended.

**You will be able to:**
- Compute month-over-month ratios from a population series and use them to tell a single-rate decline from a mixture of fast and slow leavers.
- Forecast the month at which a declining game stops covering its costs under both models, and the announcement month that a notice period forces.
- Compute what each forecasting mistake costs, closing too early or running too long.
- Design a sunset plan for content or a whole game, with cost steps, sales cut-off, notice, data handling and a final event.

**Before class:** Bungie's Destiny 2 "Year 4" announcement of the Destiny Content Vault (June 2020), or the "Destiny Content Vault" section of the Wikipedia article on *Destiny 2: Beyond Light* (10 minutes). Amazon Games, "The Future of New World: Aeternum - What to Expect" (15 January 2026, 5 minutes). Reread MMO301 week 13 section 4, "Designing the ending".

**Prerequisites from earlier courses:** [MMO301 week 13, worlds that died](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w13-worlds-that-died-shutdowns-and-their-lessons.md) (the empty-shard spiral, when to merge, and the history of Star Wars Galaxies, City of Heroes and others; this week does not repeat them). [MA101 week 4, exponentials](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w04-exponentials-and-the-xp-curve.md) and [MA101 week 5, logarithms](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w05-logarithms-how-many-levels-until.md) (half-lives and why a log axis turns exponentials into straight lines). [DB201 week 12, dashboards and KPIs](../../DB201-data-persistence-and-telemetry/lectures/w12-dashboards-and-kpis.md) (MAU as a definition). [DB201 week 13, privacy and data retention](../../DB201-data-persistence-and-telemetry/lectures/w13-privacy-gdpr-and-data-retention.md) (what you must still do with player data after the servers stop). [MMO308 week 4, funnels and churn](w04-funnels-and-churn.md) (the churn rate and why real churn is not constant; each group's `λ` below is a constant monthly hazard of that kind). Retention curves from [MMO308 week 3](w03-cohorts-and-retention-curves.md) are the cohort-level version of this week's population-level question.

**Interactive:** [`examples/w14-sunset-forecast.html`](../examples/w14-sunset-forecast.html). Keep it open during section 2.

---

## 1. Three things you can sunset

**Sunsetting** means removing something from a live game on purpose, with notice. There are three scales.

- **Content.** One activity, zone, raid or mode is retired while the game goes on. The game gets smaller so that it is cheaper to maintain.
- **Servers.** Realms or shards are merged or closed. MMO301 week 13 modeled why this matters: players feel the population of their own shard, not the total. That lecture covers when to merge. This one does not repeat it.
- **The game.** The servers are switched off and the world ends.

Between "fully live" and "off" sits a state most games pass through, **maintenance mode**. The servers run, bugs get fixed, but no new content ships. The content team moves to other projects, so the monthly cost drops sharply. Maintenance mode is itself a sunset decision, and it is often the most important one, because it changes the cost line for years.

Each scale uses the same question with different numbers. Does what this thing earns, or keeps players engaged with, cover what it costs to keep? The earning side declines over time. The question is how fast, and that is a forecasting problem.

## 2. Worked example: when will it stop paying?

### The hook

BioWare announced on 24 February 2021 that it was ending all future work on Anthem. The servers stayed on. Premium currency kept selling until 3 July 2025, when EA stopped the sales and announced the shutdown. The servers went off on 12 January 2026. That is almost five years of a game with no new content that was still worth running.

Later that year, Amazon took a different path with New World: Aeternum. It announced in October 2025 that no new content would come after Season 10. On 15 January 2026 it delisted the game, said players could buy Marks of Fortune (its premium currency) until 20 July 2026, and set the server switch-off for 31 January 2027, more than a year later.

Both studios had to answer the same question years or months in advance. When will what the remaining players spend stop covering what it costs to keep the world running? Players watching a population chart usually think they know. The chart often misleads them.

### The model

Let `M(t)` be monthly active users (MAU) `t` months after the decline begins. Suppose the players are of two kinds. A **core** that leaves slowly, and **casual** players who leave fast. Each group decays exponentially with its own half-life.

```
M(t) = M0 × [ w × e^(−λc t) + (1 − w) × e^(−λk t) ]      λ = ln 2 / half-life

revenue per month = a × M(t)
the game pays while a × M(t) > C
sunset month t*: a × M(t*) = C          announce by t* − notice
```

- `M0` is MAU when the decline starts.
- `w` is the share of those players in the slow core.
- `λc` and `λk` are the monthly leaving rates of core and casual players, set from their half-lives.
- `a` is the average revenue per MAU per month (ARPMAU, a sibling of the ARPDAU you met in week 2).
- `C` is the monthly cost of running the game. It drops when you enter maintenance mode.
- `notice` is how many months before switch-off you tell players.

The **single-rate model** is the special case with one group, `M(t) = M0 × e^(−λt)`. It is what you get if you fit one exponential to the first months of decline, and it is what most people picture when they say a game is "dying".

One diagnostic separates the two models. Take the ratio of MAU to MAU six months earlier. Under a single rate, that ratio is `e^(−6λ)` every time, a constant. Under a mixture, the ratio rises over time, because the fast leavers are gone and the survivors are increasingly core. On a log axis (MA101 week 5), a single rate is a straight line and a mixture is a line that bends toward flat.

### Numbers you can check

All numbers are invented for teaching, sized like a mid-sized MMO in its later years. `M0 = 100,000`. The core is `w = 30%` of players with a half-life of 36 months. Casual players have a half-life of 6 months. Revenue per MAU is `a = $4` a month. The live game costs `C = $150,000` a month. Maintenance mode costs `$50,000`. The studio promises six months' notice.

An analyst at month 12 fits a single exponential through month 0 and month 12, as you would by drawing a straight line on a log chart. Both models agree exactly at those two points.

```python
import math

M0, w = 100_000, 0.30          # MAU when the decline starts; share of players in the slow-leaving core
core_hl, casual_hl = 36, 6     # half-lives in months
a = 4.0                        # revenue per MAU per month, dollars
C_live, C_maint = 150_000, 50_000   # monthly cost with a content team, and in maintenance mode
notice = 6                     # months between announcing and switching off

lc, lk = math.log(2) / core_hl, math.log(2) / casual_hl

def mixture(t):
    """Two groups of players, each leaving at its own rate."""
    return M0 * (w * math.exp(-lc * t) + (1 - w) * math.exp(-lk * t))

lam = math.log(M0 / mixture(12)) / 12      # one rate through month 0 and month 12

def single(t):
    """One exponential fitted through month 0 and month 12."""
    return M0 * math.exp(-lam * t)

def crossing(model, cost):
    """First month, to 0.1, where revenue a x MAU is no longer above the cost."""
    k = 0
    while a * model(k / 10) > cost:
        k += 1
    return k / 10

def profit(model, t0, t1, cost):
    """Profit a x MAU - cost summed from month t0 to t1 in 0.1-month steps."""
    return sum((a * model(k / 10) - cost) * 0.1 for k in range(round(t0 * 10), round(t1 * 10)))

print(f"single-rate fit: {lam:.4f} per month, half-life {math.log(2) / lam:.1f} months")
print("month  mixture   single   6-month ratio: mixture  single")
for t in range(0, 49, 6):
    rm = "" if t == 0 else f"{mixture(t) / mixture(t - 6):.3f}"
    rs = "" if t == 0 else f"{single(t) / single(t - 6):.3f}"
    print(f"{t:5d} {mixture(t):8,.0f} {single(t):8,.0f}   {rm:>20s} {rs:>7s}")
for name, cost in (("live", C_live), ("maintenance", C_maint)):
    print(f"{name:11s} ${cost:,}/month: break-even MAU {cost / a:,.0f}; "
          f"single says month {crossing(single, cost)}, mixture says month {crossing(mixture, cost)}")
ts, tm = crossing(single, C_maint), crossing(mixture, C_maint)
print(f"announce by month {ts - notice:.1f} (single) or {tm - notice:.1f} (mixture)")
print(f"mixture is true, you close at month {ts}: profit forgone ${profit(mixture, ts, tm, C_maint):,.0f}")
print(f"single is true, you run to month {tm}: loss taken ${-profit(single, ts, tm, C_maint):,.0f}")
```

It prints:

```
single-rate fit: 0.0737 per month, half-life 9.4 months
month  mixture   single   6-month ratio: mixture  single
    0  100,000  100,000                               
    6   61,727   64,274                  0.617   0.643
   12   41,311   41,311                  0.669   0.643
   18   29,963   26,552                  0.725   0.643
   24   23,274   17,066                  0.777   0.643
   30   19,024   10,969                  0.817   0.643
   36   16,094    7,050                  0.846   0.643
   42   13,910    4,531                  0.864   0.643
   48   12,179    2,912                  0.876   0.643
live        $150,000/month: break-even MAU 37,500; single says month 13.4, mixture says month 13.7
maintenance $50,000/month: break-even MAU 12,500; single says month 28.3, mixture says month 46.8
announce by month 22.3 (single) or 40.8 (mixture)
mixture is true, you close at month 28.3: profit forgone $240,883
single is true, you run to month 46.8: loss taken $420,869
```

Check month 6 of the mixture by hand. The core is `30,000 × 2^(−6/36) = 30,000 × 0.891 = 26,727`. The casual group has lost exactly one half-life, `70,000 × 0.5 = 35,000`. Total 61,727.

Now read the table in three passes.

**The near term agrees.** Both models say the live game stops paying for its content team at about month 13.5. The break-even there is 37,500 MAU, and both curves pass through that region together because they were fitted to the same first year. So the decision to enter maintenance mode at around month 12 does not depend much on which model is right. Anthem's and New World's "no more new content" announcements are this decision.

**The long term does not.** Under maintenance costs the break-even is 12,500 MAU. The single-rate model reaches it at month 28.3. The mixture reaches it at month 46.8, eighteen and a half months later. With six months' notice, the single-rate model tells you to announce at month 22. The mixture says month 41.

**The notice period forces you to decide on the part where the models disagree.** You cannot wait to see the crossing. You must announce six months before it, and in this example you must choose at month 22, when the two forecasts are already years apart at the far end.

The ratio column tells you which world you are in. Under a single rate, every six-month ratio is 0.643. In the mixture world, the ratio at month 12 is already 0.669 and at month 18 it is 0.725. A rising ratio means a core is emerging. By month 18 you have three ratios, and a trend in them is visible long before month 22. Watch the ratios as well as the level.

Last, the two errors do not cost the same. Closing at month 28 when the mixture is true forgoes about $241,000 of profit, and ends a world that still has about 20,000 monthly players. Running to month 47 when the single rate is true loses about $421,000. With these numbers, a studio that cares only about money should lean slightly toward the earlier date. A studio that also weighs its players has a reason to wait for a third or fourth ratio. Neither lean is automatic, and the size of each error is what you put in front of the people who decide.

### Seeing it move

Open the interactive. The left panel plots MAU over 60 months on a linear axis, with both models and a horizontal break-even line for the current cost. The right panel plots the same curves on a log axis. Above them, a timeline strip marks the two sunset months and the two announcement months.

On the linear panel, both curves look like they are flattening, and the single-rate curve seems to be "finding a floor" too. That is how exponential decay always looks on a linear axis, because the absolute drop shrinks as the level shrinks. Switch your eyes to the log panel. The single rate is a dead-straight line going down forever. The mixture bends. Only the log view shows which curves have a real floor.

Drag the core share `w` down to 0.05. The two curves merge and the forecasts agree. Drag it to 0.5 and the maintenance crossing for the mixture moves past month 60. Then move the maintenance cost slider and watch both crossings slide. Lowering `C` buys more months under the mixture than under the single rate, because the mixture's tail is flat.

### Cross-game recognition

Studios do not publish MAU, so you cannot fit these curves to real games from outside. What you can see is which parameter each decision moved. Rewrite each case in terms of `C`, `a`, `notice` and the crossing.

**Anthem (BioWare and EA, 2021 to 2026).** On 24 February 2021 development stopped, which is a drop from `C_live` to something like `C_maint`. The world then ran for almost five years. On 3 July 2025 premium currency sales ended and the shutdown was announced, so `a` for new spending went to zero on the day of the announcement. Switch-off came on 12 January 2026, about six months of notice. EA has not published why it waited. One reading that fits the model is that the players who stayed left more slowly than the first year suggested, so the crossing kept moving later. That is what a core does.

**New World: Aeternum (Amazon Games, 2025 to 2027).** In October 2025, Amazon said no new content would come after Season 10: again `C_live` down to `C_maint`. The announcement of 15 January 2026 delisted the game, so new players stopped arriving. That removes the inflow the model ignores. Premium currency stayed on sale until 20 July 2026, so `a` fell in two steps rather than one. Switch-off is 31 January 2027, about twelve and a half months of notice, twice Anthem's. A longer notice means deciding further out on the forecast, where the uncertainty from section 2 is largest. Amazon chose that uncertainty in exchange for giving players a year.

**Star Wars: The Old Republic (June 2023).** EA moved development and operation from BioWare to Broadsword Online Games, a studio that already ran Ultima Online and Dark Age of Camelot. The stated reason was to let BioWare focus on Mass Effect and Dragon Age. In model terms, handing the game to a team built for long-running older MMOs lowers `C`. On a flat mixture tail, even a modest cost cut moves the crossing out by years. That is the opposite of a shutdown. It is a way to reach the core's long tail.

**Destiny 2, the Destiny Content Vault (10 November 2020).** Bungie removed five destinations (Io, Titan, Mars, Mercury and the Leviathan), Year 2 annual pass activities and all content from the first Destiny with the Beyond Light expansion. It said the game had grown too large to update and maintain efficiently, at about 115 GB, and the vault cut install size by about 30 to 40%. This is sunsetting at the content scale. The game keeps running, but each future update costs less to build and test, which is a lower `C` for the whole game bought by retiring its least-used parts.

Four studios, four moves on the same chart. Lower the cost line, change when revenue stops, pick a notice length. Each one moves where the curve and the line cross.

### Eyes-open design judgment

- **Two points fit anything.** The single-rate model here was drawn through two points, and a mixture model has four parameters. With 12 noisy months you can fit a mixture that says almost anything. Use the six-month ratios as the evidence, and do not trust a mixture fit until the ratios have risen at least twice in a row. The lab has you fit both and see how the answer moves with noise.
- **The model has no inflow.** Real games gain returning and new players, especially after updates and sales. In maintenance mode inflow is small, which is why the model is reasonable there. Delisting the game, as New World did, removes it entirely.
- **Announcements change the curve.** The model assumes players leave at the same rate after the announcement. In practice some leave at once and some come back for a last look. Measure the curve during the notice period and do not reuse pre-announcement ratios after it.
- **Money is not the only line.** A world with 20,000 monthly players is a community. The model tells you what keeping it costs. Whether that cost is worth paying is a decision the studio owns, and it should be made knowing both errors in the table, not only the cheaper one.

### Check yourself on the worked example

1. Under the single-rate fit, how many MAU remain at month 60? Under the mixture?
2. Maintenance cost falls from $50,000 to $40,000 a month. What is the new break-even MAU? Which model's crossing moves more, and why?
3. A game shows six-month ratios of 0.70, 0.70 and 0.71. What does this suggest about the core, and which forecast would you trust more?

<details>
<summary>Answers</summary>

1. Single rate: `100,000 × e^(−0.0737 × 60) ≈ 1,200`. Mixture: core `30,000 × 2^(−60/36) ≈ 9,450`, casual `70,000 × 2^(−10) ≈ 68`, total about 9,520.
2. `40,000 / 4 = 10,000` MAU. The mixture's crossing moves more (from month 46.8 to about 57.6, against 28.3 to about 31.3 for the single rate), because the mixture's curve is flatter there, so lowering the line shifts the crossing further along the time axis.
3. The ratios are nearly constant, so there is little sign of a slow core yet. A single-rate forecast is the honest one for now. Keep watching. If the ratios start rising, revise.

</details>

## 3. Sunsetting content

A game that ships content for years grows heavy. Every new patch must be tested against every live activity. Every activity keeps its rewards in the economy. And every activity splits the player base a little further. Retiring content trades something players value for a cheaper, more focused game.

Decide it with data, and show the data. For each activity, compute its share of play hours from telemetry (DB201 week 10), and estimate its share of maintenance cost: test hours per patch, bug reports, size on disk. An invented example:

| Activity | Share of play hours | Share of maintenance cost | Hours share ÷ cost share |
|---|---|---|---|
| Current raid | 31% | 14% | 2.21 |
| Open-world events | 24% | 10% | 2.40 |
| Old raid A | 3% | 12% | 0.25 |
| Old zone B | 1% | 9% | 0.11 |
| Everything else | 41% | 55% | 0.75 |

The last column is engagement bought per unit of cost. Old zone B gives the game 1% of its play for 9% of its maintenance. It is the candidate. But run three checks before you retire anything.

- **Who plays it?** A 1% share may be the whole of one kind of player: collectors, a role-play community, new players in their first week. Break the hours down by segment (week 7) before you decide.
- **What was bought?** If players paid money for an expansion that included the zone, removing it breaks a promise. Destiny 2's vault raised exactly this problem. Bungie's answer was to announce well ahead and plan to bring some content back later, as it had done with the Moon.
- **What leaves the economy?** Retiring an activity retires its faucets and sinks. Check the ledger (MMO304 week 12) for any item that becomes impossible to earn or impossible to spend.

## 4. The sunset plan

When the answer is "switch it off", the plan has five parts. MMO301 week 13 covered how to design the ending as an experience. Here is the operational list.

1. **Cost steps.** Enter maintenance mode first. It is often years before switch-off, as Anthem shows.
2. **The announcement and the notice.** Choose the notice length from the forecast's uncertainty and from what players need to finish things. MMO301 week 13 compared the notice given in earlier shutdowns, from under two months to nearly six. Anthem (six months) and New World (about a year) extend that record.
3. **Sales.** Stop selling the game or new premium currency at the announcement, or on a published date soon after. Selling currency to players who cannot use it before switch-off is the fastest way to turn a sad ending into an angry one. New World kept selling for six months after announcing, with the cut-off date public from day one.
4. **Data.** Switching off the servers does not end your duties toward the personal data you hold. Your retention schedule from DB201 week 13 still applies. Decide what you keep (financial records for tax law), what you delete and when, and what you hand players before the end (character exports, screenshots, a final record).
5. **Preservation.** Some studios release offline modes or license private servers. MMO301 week 13 tells the City of Heroes story. The pressure to plan for this is rising. The Stop Killing Games campaign's European Citizens' Initiative, "Stop Destroying Videogames", collected about 1.29 million valid signatures. On 16 June 2026 the European Commission answered that it could not propose a legal duty to keep games playable after they are discontinued, and committed to working with the industry on voluntary standards instead. For a designer, this means an end-of-life plan is not required by law in the EU as of 2026, and players increasingly expect one anyway.

## In-class activity (25 minutes)

Pairs get a card with 24 months of a game's MAU (the instructor hands out four different cards, generated from different values of `w`).

1. Compute the three six-month ratios. Decide single rate or mixture, and write one sentence of evidence.
2. Using `a = $4`, maintenance `C = $50,000` and six months' notice, give your announcement month. Show which model you used.
3. Swap cards with another pair. Without looking at their answer, do step 1 on their card. Compare.
4. The instructor reveals the next 24 months of each card. Which pairs would have closed a world that was still paying? Which would have run at a loss?

Expected output: ratios, a model choice with evidence, an announcement month, and a one-line reflection on the reveal.

## Common misconceptions

- **"The curve is flattening, so we've found our floor."** On a linear axis, every exponential looks like it is flattening. Only rising period-over-period ratios, or a bend on a log axis, show a real floor.
- **"We'll announce when revenue drops below cost."** With a notice period, by then you are already running at a loss for the whole notice. You must decide on the forecast, before the crossing.
- **"Maintenance mode is a slow shutdown."** It is a cost change. With a slow-leaving core, a game can run profitably in maintenance mode for years, as Anthem did.
- **"Removing unpopular content only affects the few who play it."** It affects the promise made to everyone who paid for it and the items that flow from it into the economy. Check segments, purchases and the ledger first.

## Check yourself

1. A game's MAU is 80,000 now and 52,000 six months later. Assuming a single rate, what is its half-life, and when will it reach 20,000?
2. For the same game, the next six-month ratio is 0.72. Does that support the single-rate model? What would you expect of the ratio after that if a core exists?
3. With `a = $5` and `C = $60,000` a month, what is the break-even MAU? If the game follows your single-rate model from question 1 and notice is 9 months, at which month must you announce?
4. Old raid A in section 3 has a 3% share of hours and 12% of cost. List the three checks you would run before retiring it and the telemetry each one needs.
5. A producer proposes keeping premium currency on sale until the last week "because some players still want to buy". Give two reasons from this lecture to stop sales earlier.

<details>
<summary>Answers</summary>

1. Ratio `0.65` per six months, so the monthly rate is `λ = −ln(0.65)/6 ≈ 0.0718` and the half-life is `ln 2 / 0.0718 ≈ 9.7` months. Reaching 20,000 from 80,000 is two half-lives, about 19.3 months from now.
2. No. A single rate predicts 0.65 again. A rising ratio suggests a slower-leaving core. If a core exists, expect the next ratio to rise again, toward the core's own six-month ratio.
3. `60,000 / 5 = 12,000` MAU. Under the single rate, `t = ln(80,000 / 12,000) / 0.0718 ≈ 26.4` months from now, so announce by about month 17.4.
4. Who plays it (hours by segment, including new players and particular communities), what was bought (purchase records linking the raid to paid content), and what leaves the economy (the ledger's faucets and sinks tagged by activity).
5. Players cannot use currency bought just before switch-off, so late sales turn an ending into a grievance and a refund problem. And the announcement already changes player behavior, so a published cut-off date gives everyone the same information and keeps trust.

</details>

## Lab / assignment hook

[Lab 14, sunset forecast](../labs/lab14.md). You fit a single-rate and a mixture model to a noisy 18-month MAU history, compute the six-month ratios, forecast both crossings and announcement months, and write a one-page sunset recommendation that states both errors. It also feeds the final live-ops plan, which must include an end-of-life section.

## Sources

- Wikipedia, "Anthem (video game)" (retrieved September 2026). BioWare ended future work on 24 February 2021; premium currency sales discontinued and shutdown announced on 3 July 2025; servers shut down on 12 January 2026.
- Amazon Games, "The Future of New World: Aeternum - What to Expect", newworld.com, 15 January 2026. Delisting on 15 January 2026; Marks of Fortune purchases until 20 July 2026; servers offline 31 January 2027; no content after the Nighthaven seasonal update. Wikipedia, "New World (video game)" (retrieved September 2026), for the October 2025 announcement that new content would end after Season 10.
- Wikipedia, "Star Wars: The Old Republic" (retrieved September 2026). June 2023 move of development and operation from BioWare to Broadsword Online Games, which maintains Ultima Online and Dark Age of Camelot, so BioWare could focus on Mass Effect and Dragon Age.
- Wikipedia, "Destiny 2: Beyond Light" (retrieved September 2026), section on the Destiny Content Vault, summarizing Bungie's June 2020 announcement. Content vaulted on 10 November 2020 (Io, Titan, Mars, Mercury, the Leviathan, Year 2 annual pass activities and the original Destiny content); game size about 115 GB; install size cut by about 30 to 40%; plans to remaster and return some content, as with the Moon.
- Wikipedia, "Stop Killing Games" (retrieved September 2026). Campaign founded by Ross Scott in 2024 after The Crew's shutdown; European Citizens' Initiative "Stop Destroying Videogames" closed 31 July 2025; about 1,294,188 valid signatures confirmed 26 January 2026; Commission response of 16 June 2026 declining to propose a legal obligation and committing to stakeholder work on voluntary standards.
- Seif El-Nasr, M., Drachen, A. and Canossa, A. (eds.) (2013). *Game Analytics: Maximizing the Value of Player Data*. Springer. Course reading for telemetry-based population measures.
- All population, revenue and cost figures, the mixture parameters and the content table in section 3 are teaching assumptions, not figures from any studio.

## Interactive spec: examples/w14-sunset-forecast.html

**Purpose.** Show that a single exponential and a core-plus-casual mixture look alike on a linear axis and in the first year, but differ on a log axis and in the far forecast, which is where a notice period forces the decision.

**Layout.** Controls strip on top. Below it a timeline strip, then two linked charts side by side on desktop (stacked on mobile, linear first). A results table under the charts.

**Controls (each with numeric readout, keyboard-operable):**
- `w`, core share: 0 to 0.8, step 0.01, default 0.30.
- Core half-life: 12 to 72 months, step 1, default 36.
- Casual half-life: 2 to 12 months, step 0.5, default 6.
- `a`, revenue per MAU per month: $1 to $10, step 0.5, default $4.
- Monthly cost `C`: $10,000 to $200,000, step $5,000, default $50,000. A toggle "Live ($150,000) / Maintenance ($50,000)" sets it quickly.
- Notice months: 0 to 18, step 1, default 6.
- Fit month `f` (the second point of the single-rate fit): 6 to 24, step 6, default 12.
- `M0` fixed at 100,000.

**Formulas.**
- Mixture: `M(t) = M0 × (w × 2^(−t/hc) + (1 − w) × 2^(−t/hk))`.
- Single rate through months 0 and `f`: `λ = ln(M0 / M(f)) / f`, `S(t) = M0 × e^(−λt)`.
- Break-even MAU: `C / a`. Crossing: first `t` on a 0.1-month grid with `a × model(t) ≤ C`. If none by month 120, show "after month 120".
- Announce month: crossing minus notice. If negative, show "announce now: already inside the notice window".
- Six-month ratios for both models at months 6 to 60.
- Error costs: profit forgone `Σ (a × M(t) − C) × 0.1` from the single crossing to the mixture crossing (on the mixture), and loss taken `−Σ (a × S(t) − C) × 0.1` over the same interval (on the single rate). Show "n/a" when the single crossing is later.

**Left chart.** Linear y axis 0 to 100,000, x axis 0 to 60 months. Both curves, the break-even line, observed-data dots for months 0 to `f` (from the mixture), vertical markers at both crossings.

**Right chart.** Same data with a log y axis from 1,000 to 100,000 (ticks at 1k, 2k, 5k, 10k, 20k, 50k, 100k). The single rate must draw as a straight line.

**Timeline strip.** A 0-to-60-month bar with four labeled markers: announce (single), sunset (single), announce (mixture), sunset (mixture).

**Results table.** Rows for months 0, 6, ..., 48 with mixture MAU, single MAU, and both six-month ratios. Then the two crossings, two announce months and two error costs.

**Test values (defaults, `C = $50,000`).** λ = 0.0737 per month (single half-life 9.4 months). Mixture at months 6, 12, 24, 48: 61,727; 41,311; 23,274; 12,179. Single at the same months: 64,274; 41,311; 17,066; 2,912. Six-month ratios `M(t)/M(t−6)`, mixture, at months 6, 12, 18, 24: 0.617, 0.669, 0.725, 0.777 (0.876 at month 48); single constant 0.643. Break-even 12,500 MAU. Crossings 28.3 (single) and 46.8 (mixture). Announce at 22.3 and 40.8. Profit forgone $240,883; loss taken $420,869. With `C = $150,000`: crossings 13.4 and 13.7.

**The one insight.** On the linear chart both curves appear to level off. On the log chart only the mixture bends, and the vertical gap between the two sunset markers on the timeline is largest exactly where the notice period forces the decision.

**Accessibility and style.** Shared palette tokens from `templates/interactive-tokens.css`. Mixture solid line, single rate dashed, so they differ without color. All numbers also shown as text. No game names, logos or art in the visual.
