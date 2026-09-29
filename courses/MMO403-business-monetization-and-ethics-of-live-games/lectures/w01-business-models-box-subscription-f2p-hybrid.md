# MMO403 · Week 01 — Business Models: Box, Subscription, F2P, Hybrid

**Why this matters:** A persistent world costs money every month it stays online, whether or not its players pay every month. The business model decides how many people come through the door, how much each one pays and when, and whether a player who stays another month earns you money or costs you money. Pick it by habit and you can build a good game that loses money for exactly the reason it is good.

**You will be able to:**
- Compute the contribution (revenue minus cost to serve) of box, subscription, free-to-play and hybrid models for one audience over any horizon.
- Derive the retention level at which a subscription overtakes a box price, and explain why a box-only MMO loses money on every month a player stays.
- Compare models by the value of one extra point of monthly retention, and say which KPI each model's revenue is exposed to.
- Critique a real model change (The Elder Scrolls Online, Guild Wars 2, Final Fantasy XIV) by naming which term of the model it moved.

**Before class:** Fields & Cotton, *Social Game Design: Monetization Methods and Mechanics* (Morgan Kaufmann, 2011), the opening chapters on business models and the economics of free games (the course reader lists the pages). Reread the section "Three ways to sell a game" in GS101 week 11.

**Prerequisites from earlier courses:** [GS101 week 11, free-to-play, mobile and live service](../../GS101-history-and-critical-study-of-games/lectures/w11-free-to-play-mobile-and-live-service.md) (the revenue product `N × p × A`, ARPU versus ARPPU, and expected lifetime `1 / (1 − r)`; this lecture assumes all three). [MMO308 week 1, what live ops is](../../MMO308-live-operations-analytics-and-experimentation/lectures/w01-what-live-ops-is.md) (cohorts, stayers and tourists). [MMO404 week 13, cost engineering](../../MMO404-advanced-networked-simulation/lectures/w13-cost-engineering.md) (the cost of a player-hour).

**Interactive:** [Business model race](../examples/w01-business-model-race.html), built from the spec at the end of this lecture. Keep it open during section 2.

---

## 1. Three questions every business model answers

GS101 week 11 described the box, the subscription and free-to-play as three ways to sell a game, and gave you the monthly revenue product `R = N × p × A`. This course treats those models as engineering choices with numbers attached. Every business model, however it is dressed, answers three questions.

**How wide is the door?** Of all the people who hear about your game and would try it for free, what share actually starts playing? A $60 price turns most of them away. A free download turns almost none away. Call this share `d`.

**What does the meter charge?** Some money arrives once, at the door (a box price, an expansion). Some arrives every month the player stays (a subscription fee, store purchases). Call the one-time amount `U` (upfront) and the monthly amount per active player `m`. For a free-to-play game `m` is the ARPU from GS101, averaged over payers and non-payers alike.

**What does a player cost to keep?** This is the question single-player games never ask. An MMO player uses servers, bandwidth, database writes, customer support, anti-cheat, moderation and payment processing every month they play. Call it `c`, the **cost to serve** one active player for one month. MMO404 (taken this semester) prices the server part in its week 13 at about $2.09 per 1,000 player-hours with invented round numbers. At that rate a player who logs 40 hours a month costs about 8 cents in infrastructure. Support, moderation and the rest are usually larger than that. This lecture uses `c = $0.50` per active month, an invented round number you should replace with your own studio's figure.

The term that separates an MMO from a boxed single-player game is `m − c`. If it is positive, a player who stays is income. If it is negative, a player who stays is a cost. The rest of this lecture follows that sign.

## 2. Worked example: four models, one audience

### The hook

The Elder Scrolls Online launched for Windows and Mac on 4 April 2014 with a box price and a mandatory monthly subscription, the model World of Warcraft had used since 2004. Nine months later, in January 2015, ZeniMax announced it would drop the requirement. From 17 March 2015 the game became *The Elder Scrolls Online: Tamriel Unlimited*. You bought the game once and played without a monthly fee. An optional subscription, ESO Plus, gave access to the downloadable content, a monthly allowance of the premium currency (crowns) and faster progress, and a Crown Store sold items directly.

On its face, that is a company giving up a monthly fee from every player. Players at the time read it as a sign the game was failing. Yet by 2020 ESO had sold over 15 million units, and by 2024 its revenue passed $2 billion, according to figures the publisher reported and Wikipedia collects. How can charging most players less earn more? The model below answers with four numbers per business model.

### The model

Take an **audience** of `A` people who would try the game if it were free. Follow them for `T` months. Each month, a share `r` of last month's players is still playing (**monthly retention**, constant for now; MMO308 week 1 showed why real curves bend, and week 2 of this course uses the bent version).

```
S(T)            = 1 + r + r² + ... + r^(T−1)          expected active months per player in T months
contribution(T) = A × d × ( U + (m − c) × S(T) )
```

- `d` is the share of the audience that comes through the door.
- `U` is the one-time price paid at the door, in dollars.
- `m` is the revenue per active player-month.
- `c` is the cost to serve one active player-month.
- `S(T)` counts month 1, the month players come through the door, as 1, because everyone who came through the door plays that month. As `T` grows, `S(T)` approaches `1 / (1 − r)`, the expected lifetime from GS101 week 11.

**Contribution** is revenue minus the cost to serve, before development, marketing and overheads. It is the money the live game produces to pay for everything else.

Here are four invented but plausible models for the same audience of 1,000,000 people:

| Model | `d` | `U` | `m` | What it stands for |
|---|---|---|---|---|
| Box | 0.20 | $60 | $0 | Buy once, play forever, no store |
| Subscription | 0.10 | $40 | $15 | Box plus a monthly fee, as WoW and ESO at launch |
| Free-to-play | 1.00 | $0 | $2.00 | Free door, store revenue averaged over everyone |
| Hybrid | 0.25 | $30 | $3.50 | Cheaper box, store, and an optional subscription |

The hybrid's `m = $3.50` is $2.00 of store spending per active player plus 10% of players choosing a $15 optional subscription ($1.50). Every number in this table is a teaching assumption. The shape of the result does not depend on the exact values, and the lab asks you to break it.

### Numbers you can check

Set `r = 0.80`. Then `S(1) = 1`, `S(3) = 1 + 0.8 + 0.64 = 2.44`, `S(12) = 4.656` and `S(36) = 4.998`.

Check the box at `T = 1` by hand: `1,000,000 × 0.20 × (60 + (0 − 0.50) × 1) = 200,000 × 59.50 = $11.90 million`. Check the subscription at `T = 3`: `1,000,000 × 0.10 × (40 + 14.50 × 2.44) = 100,000 × 75.38 = $7.54 million`.

Cumulative contribution in millions of dollars, `r = 0.80`:

| Model | Month 1 | Month 3 | Month 12 | Month 36 |
|---|---|---|---|---|
| Box | 11.90 | 11.76 | 11.53 | 11.50 |
| Subscription | 5.45 | 7.54 | 10.75 | 11.25 |
| Free-to-play | 1.50 | 3.66 | 6.98 | 7.50 |
| Hybrid | 8.25 | 9.33 | 10.99 | 11.25 |

Three things to read off it.

**The box shrinks.** The box model's contribution goes *down* every month, from $11.90 million to $11.50 million. Its players keep playing and keep costing 50 cents a month, and none of them pays again. For a box MMO, retention is a cost.

**The recurring models back-load their money.** The subscription earns less than half the box's contribution in month 1 and nearly catches up by month 36. Free-to-play collects under half of its 36-month total in the first three months.

**At 80% retention they almost tie.** After three years, box, subscription and hybrid sit within $0.25 million of each other. That is a coincidence of the numbers chosen, and it is also the point. Change `r` and the ranking changes completely:

| Monthly retention `r` | Box | Subscription | Free-to-play | Hybrid |
|---|---|---|---|---|
| 0.70 | **11.67** | 8.83 | 5.00 | 10.00 |
| 0.80 | **11.50** | 11.25 | 7.50 | 11.25 |
| 0.90 | 11.02 | **18.17** | 14.66 | 14.83 |

(36-month contribution, millions of dollars, best model in bold.)

The subscription overtakes the box when `0.10 × (40 + 14.5 S) > 0.20 × (60 − 0.5 S)`, which simplifies to `S > 5.16` active months. At `r = 0.80` the lifetime is 5 months, so the subscription never catches up. At `r = 0.90` it passes the box in month 7.

This code reproduces the first table. It runs as shown with `.venv/bin/python`:

```python
MODELS = {                 # door d, upfront U ($), monthly m ($ per active month)
    "box":          (0.20, 60.0, 0.0),
    "subscription": (0.10, 40.0, 15.0),
    "free-to-play": (1.00, 0.0, 2.0),
    "hybrid":       (0.25, 30.0, 3.5),
}
AUDIENCE, COST = 1_000_000, 0.50   # people reached; cost to serve per active month

def months_active(r, T):
    """Expected active months in the first T months: 1 + r + ... + r^(T-1)."""
    return sum(r**t for t in range(T))

def contribution(model, r, T):
    d, U, m = MODELS[model]
    return AUDIENCE * d * (U + (m - COST) * months_active(r, T))

for name in MODELS:
    row = [contribution(name, 0.80, T) / 1e6 for T in (1, 3, 12, 36)]
    print(f"{name:13s}" + "".join(f"{v:8.2f}" for v in row))
```

It prints `box             11.90   11.76   11.53   11.50` and `free-to-play     1.50    3.66    6.98    7.50`, matching the table.

### The visual

Open `examples/w01-business-model-race.html`. The left view is **monthly** contribution, the way a finance report shows a single month. The box line spikes at month 1 and then drops to small negative values. The subscription and free-to-play lines start low and decay. On this view the box looks like the obvious winner, because it wins the only month anyone remembers.

The right view is **cumulative** contribution, the same numbers added up. Drag the retention slider from 0.70 to 0.90. The box line barely moves (it even sinks a little). The subscription and free-to-play lines swing up and cross it. The picture to take away is that the business model decides which slider your revenue listens to. A box listens to launch sales. A subscription listens to retention. Free-to-play listens to retention and to how wide the door is.

### Cross-game recognition

Rewrite each real case as a change to `d`, `U`, `m` or `c`.

**The Elder Scrolls Online (April 2014 to March 2015).** Launch was the subscription row: a box price and `m` equal to the fee for everyone. Tamriel Unlimited lowered the effective `U` for the long run (no fee required), which widened `d`, and replaced a fee-for-all `m` with store spending plus an optional subscription taken by some players. That is the hybrid row. The model says this pays off when the wider door and store spending outweigh the fee lost from players who would have subscribed anyway. ESO's later sales figures fit that reading, though a public company never shows you the counterfactual.

**Guild Wars 2 (August 2012 to August 2015 and after).** ArenaNet sold GW2 with no subscription from day one, a box price plus a gem store. That is the hybrid row without the optional subscription. In August 2015 the core game became free to download, while expansions stayed paid. In model terms, `U` for the base game fell to zero and `d` rose toward 1, and the upfront revenue moved to the expansion, which a player buys only after the free game has retained them. The door and the meter were re-cut so that the price arrives after retention, not before.

**Final Fantasy XIV (relaunched August 2013, current).** Square Enix kept the subscription row and widened the door a different way. The official free trial, as of September 2026, lets anyone play the base game and three expansions up to level 80 with no playtime limit. Optional items in the online store are priced directly in real money and cannot be traded to other players. Producer Naoki Yoshida has repeatedly credited the subscription for the game's recovery and described free-to-play as an unreliable income that pulls development time toward store items. In model terms, the free trial raises `d` for the *trial*, and the subscription `m` applies only to players who have already chosen to stay. The door is free and the meter starts after retention has done its sorting.

**World of Warcraft (2004 to today).** The one-month subscription price in the US has been $15 since launch (GS101 week 11), and each expansion is sold separately. That is a subscription with a periodic second `U`. Expansions are how a subscription game raises revenue per player without raising the monthly fee.

Four games, one model. Each change either widened the door, moved the price later in the player's life, or changed what the meter charges.

### Eyes-open design judgment

- **Match the model to the retention you can deliver.** A subscription needs lifetimes long enough to beat the box. In this example that means more than 5.16 active months. If your honest retention forecast is 0.70, the subscription row loses to a box, and no marketing fixes that.
- **Never run a pure box MMO.** With `m = 0` and `c > 0`, every retained month costs money. Box-priced online games survive by adding a recurring term (expansions, a store, a subscription) or by keeping `c` near zero (peer-to-peer hosting, no support). Name the recurring term before launch.
- **Free-to-play is a bet on the tail.** It has the smallest early contribution and the steepest response to retention. It works when the game keeps people for years, and fails painfully when it doesn't.
- **Cash timing is a design constraint.** The box's money arrives in month 1. The subscription's arrives over years. A studio that must repay a loan or a publisher advance next year may prefer the front-loaded model even when the back-loaded one earns more in total. Week 13 returns to this.
- **Each model creates an incentive you must decide to resist.** A subscription is paid per month, which rewards stretching content with grinds. Free-to-play is paid per purchase, which rewards selling relief from friction the game itself adds. A box is paid once, which rewards promising more at launch than the live game will deliver. None of the three is neutral, and none is inherently exploitative. Section 4 treats this in detail.

## 3. The value of one point of retention

The retention table shows the ranking flipping. A sharper way to see it is to ask how much one extra percentage point of monthly retention is worth under each model. Raise `r` from 0.80 to 0.81 and recompute the 36-month contribution:

| Model | Change in 36-month contribution for +1 point of `r` |
|---|---|
| Box | −$26,000 |
| Subscription | +$380,000 |
| Free-to-play | +$393,000 |
| Hybrid | +$197,000 |

Where do these come from? Over a long horizon, `S` is close to `1 / (1 − r)`, whose derivative is `1 / (1 − r)²`. At `r = 0.80` that is 25. So one point of `r` adds about `A × d × (m − c) × 25 × 0.01`. For free-to-play, `1,000,000 × 1 × 1.50 × 0.25 = $375,000`. The exact 36-month figure is a little higher because the step from 0.80 to 0.81 is not infinitesimal.

This table is the budget argument for a live-ops team. If a retention feature moves `r` by one point, it is worth $380,000 to a subscription game and costs a box game $26,000 in server and support time. The same feature, built by the same people, is a good investment in one business model and a loss in another. When MMO308 week 1 showed that stayers' retention was the most powerful lever in a live game, it assumed a business model where `m > c`.

Notice also what the table does not say. It does not say players are better served by one model. Retention measures that people keep playing. It does not measure why, and a model that pays for retention will be tempted to buy it with obligations rather than enjoyment. Week 8 (dark patterns) looks at that line.

## 4. Hybrids, and whose experience pays for whose

Pure models are rare in 2026. Most MMOs combine at least two meters:

| Game (era) | Door | One-time | Recurring |
|---|---|---|---|
| World of Warcraft (retail, current) | Paid | Expansions | Subscription |
| Final Fantasy XIV (current) | Free trial to level 80 | Expansions | Subscription, plus optional items in the online store |
| The Elder Scrolls Online (since March 2015) | Paid | Game and chapters | Crown Store, optional ESO Plus |
| Guild Wars 2 (since August 2015) | Free core game | Expansions | Gem store |

A hybrid is not automatically better. It lets you tune `d`, `U` and `m` separately, and it adds a question pure models do not face: **which players are paying for which other players?**

In a subscription game, every active player pays the same `m`. Everyone covers their own `c`, and the surplus pays for development. In free-to-play, most players pay nothing, so their `c` is covered by the minority who spend. GS101 week 11 showed that spending is concentrated, so a small share of payers funds the servers for everyone else. That can be a fair deal, since keen players get a game full of other people and casual players get a free game. It can also turn into a design that serves the heaviest spenders first. Week 9 measures the concentration, and the week 7 and 8 lectures cover where regulators and critics have drawn lines.

For this week, keep three questions for any hybrid you design or critique:

1. Does the player who never pays still have a complete game? If not, what exactly is missing, and is that disclosed before they invest time?
2. Does the recurring meter charge for things the game makes worse on purpose? A subscription that sells time and a store that sells shortcuts both have this temptation.
3. If the game went back to one pure model tomorrow, which group of players would lose the most? That group is the one your hybrid currently favours.

## In-class activity (25 minutes)

In groups of three. Materials: the interactive, a laptop per group, and one MMO each group has played (or pick one from the hybrid table).

1. (8 min) Estimate `d`, `U`, `m` and `r` for your game from what you know and from its store page. Write each as a range, not a point. Be honest that `r` is a guess.
2. (7 min) Enter the middle of each range into the interactive's custom model. Record the 12- and 36-month contribution for an audience of 1,000,000. Then find the smallest `r` at which your game beats a $60 box.
3. (5 min) Propose one change to the business model (a free trial, a cheaper box, an optional subscription, removing the store). Enter it and record the new contribution and the new value of one point of retention.
4. (5 min) Write one sentence naming which players gain and which lose from your change.

Expected output: a filled table (four parameters, two contributions, the break-even `r`), the proposed change with its numbers, and the one-sentence judgment.

## Common misconceptions

- **"A subscription always earns more than a box because it keeps paying."** Only if lifetimes are long enough. In the example the subscription needs more than 5.16 active months to beat a $60 box. Below that, the box wins.
- **"Retention is always good for the business."** Under a pure box model with a live service, every retained month costs money. Retention is income only when `m > c`.
- **"Free-to-play means low revenue per player."** Low revenue per player per month, yes. Over a long lifetime, free-to-play can earn more per person reached than any other row, because its door is widest and its revenue has no ceiling.
- **"A model change is a verdict on the game's quality."** ESO and Guild Wars 2 changed their doors while continuing to grow. A model change moves `d`, `U` and `m`. It says nothing by itself about whether players liked the game.

## Check yourself

1. Using the lecture's box and subscription rows and `c = $0.50`, what 36-month contribution does each earn at `r = 0.85`? Which is larger?
2. A studio proposes a free trial for its subscription game. It raises `d` from 0.10 to 0.12 (more people end up subscribing after trying) but the trial players cost `c` for one free month each, and 300,000 people try it. Is the trial worth it over 36 months at `r = 0.80`? Show the two numbers you compare.
3. For the free-to-play row, what value of `m` makes 36-month contribution equal to the box's at `r = 0.80`?
4. Explain in two sentences why a live-ops team at a box-priced MMO might be asked to *reduce* play time, and why that request is a sign of a missing recurring meter rather than a bad team.

<details>
<summary>Answers</summary>

1. `S(36)` at 0.85 is `(1 − 0.85^36) / 0.15 ≈ 6.647`. Box: `200,000 × (60 − 0.5 × 6.647) = 200,000 × 56.68 ≈ $11.34 million`. Subscription: `100,000 × (40 + 14.5 × 6.647) = 100,000 × 136.39 ≈ $13.64 million`. The subscription is larger, because 6.65 active months exceeds the 5.16 break-even.
2. Extra subscribers: 20,000, each worth `40 + 14.5 × 4.998 = $112.47`, so about $2.25 million. Cost of the trial: `300,000 × $0.50 = $150,000`. The trial is worth about $2.1 million net. (If trial players who do not convert stay more than one month, add their extra cost.)
3. Box 36-month is $11.50 million. Free-to-play needs `1,000,000 × (m − 0.5) × 4.998 = 11,500,000`, so `m − 0.5 = 2.301` and `m ≈ $2.80`.
4. With `m = 0`, every hour a player stays costs server and support money and earns nothing, so the only financial lever left is to shorten play. The fix is a recurring meter (expansions, a store, a subscription) that makes `m − c` positive, not a team that makes the game less engaging.

</details>

## Lab / assignment hook

[Lab 01, business model race](../labs/lab01.md). You implement the model in Python from a starter with tests, reproduce the tables in section 2, then fit the four parameters for one real MMO from public information and argue which model it should use. This lab starts the "Models" strand (40%) of the course assessment.

## Sources

- Wikipedia, "The Elder Scrolls Online" (retrieved September 2026). Released 4 April 2014 for Windows and Mac with a mandatory subscription; January 2015 announcement that the subscription requirement would end on 17 March 2015; rebrand as *Tamriel Unlimited*; optional ESO Plus with DLC access, a monthly crown allowance and faster progress; console release 9 June 2015; over 15 million units sold by January 2020 and over $2 billion revenue by 2024 as reported.
- Hines, P. (Bethesda), post on X/Twitter, 10 January 2020: more than 15 million people had bought ESO. Jones, A., "After making $2 billion in 10 years, The Elder Scrolls Online's director wants you to know..." (GamesRadar+, 6 April 2024): the $2 billion revenue figure, as reported from the studio.
- Wikipedia, "Guild Wars 2" (retrieved September 2026). No subscription fee; a purchase was required to install the game until August 2015; six expansion packs from *Heart of Thorns* (2015) to *Visions of Eternity* (2025); content updates add items to the gem store.
- Square Enix, "FINAL FANTASY XIV Free Trial" (freetrial.finalfantasyxiv.com, accessed September 2026). Free trial up to level 80, covering *A Realm Reborn*, *Heavensward*, *Stormblood* and *Shadowbringers*, with no playtime restriction.
- Square Enix, "FINAL FANTASY XIV Online Store" (store.finalfantasyxiv.com, accessed September 2026). Optional items priced in real money; optional items cannot be sold or traded to other players.
- Wikipedia, "Final Fantasy XIV" (retrieved September 2026), section "Sales and subscriptions". Subscription-based since the August 2013 relaunch; Yoshida's statements crediting the subscription model and his view of free-to-play as unreliable income.
- GS101 week 11 and its sources. World of Warcraft's US one-month price of $15, unchanged since the 2004 launch.
- MMO404 week 13. Invented baseline of about $2.09 per 1,000 player-hours for infrastructure.
- Fields, T. & Cotton, B. (2011). *Social Game Design: Monetization Methods and Mechanics*. Morgan Kaufmann.

## Interactive spec: examples/w01-business-model-race.html

**Purpose.** Show that the business model decides which parameter revenue depends on. Insight on first load: *on the monthly view the box wins month 1 by a mile, while on the cumulative view the four models finish within $4 million of each other, and dragging retention reorders them.*

**Layout.** Two linked charts side by side on desktop, stacked on mobile (monthly first). Controls under the charts, then a numbers table. Generic shapes and colors only. No game names inside the charts; game names appear only as preset labels.

**Left chart, monthly contribution.** x: month 1 to `T` (default 36). y: contribution in that month, millions of dollars, with a zero line. Month 1 for each model is `A × d × (U + m − c)`; month `t ≥ 2` is `A × d × (m − c) × r^(t − 1)`. Draw each model as a line with markers (box's month 1 will dwarf the rest, so use a y-axis break or a toggle "clip month 1" defaulting to on, with the clipped value printed above the chart).

**Right chart, cumulative contribution.** Same x. y: after month `t`, `A × d × (U + (m − c) × S(t))`, with `S(n) = (1 − r^n) / (1 − r)` (and `S(n) = n` when `r = 1`). Mark every crossover between two lines with a dot and the month number. Label each line at its right end with its final value.

**Controls.**
- Retention `r`: slider 0.50 to 0.98, step 0.01, default 0.80. This is the main control and sits first.
- Cost to serve `c`: 0 to 3.00, step 0.05, default 0.50.
- Horizon `T`: 6 to 120 months, step 1, default 36.
- Audience `A`: fixed at 1,000,000 (display only).
- Per model, editable `d`, `U`, `m` (collapsed panel "Edit models"), defaults from the lecture table: box (0.20, 60, 0), subscription (0.10, 40, 15), free-to-play (1.00, 0, 2.00), hybrid (0.25, 30, 3.50). A fifth "custom" model, hidden until enabled, defaults to (0.15, 20, 5).
- Presets: "Lecture default", "Low retention (0.70)", "High retention (0.90)", "Expensive servers (c = 2.00)".

**Numbers panel.** For each model at the current settings: contribution at months 1, 3, 12 and `T`; the value of one extra point of retention, `contribution(r + 0.01, T) − contribution(r, T)`; the break-even `S` against the box, `S* = (d_box U_box − d U) / (d (m − c) − d_box (m_box − c))` when defined, and the first month the model passes the box (or "never within T").

**Test values** (A = 1,000,000, c = 0.50, T = 36 unless stated).
- r = 0.80: box 11.90 / 11.76 / 11.53 / 11.50 million at months 1, 3, 12, 36; subscription 5.45 / 7.54 / 10.75 / 11.25; free-to-play 1.50 / 3.66 / 6.98 / 7.50; hybrid 8.25 / 9.33 / 10.99 / 11.25.
- 36-month at r = 0.70: 11.67, 8.83, 5.00, 10.00. At r = 0.90: 11.02, 18.17, 14.66, 14.83.
- Value of +1 point at r = 0.80: box −26,200; subscription +380,100; free-to-play +393,200; hybrid +196,600 (±100 for rounding).
- Subscription vs box: break-even S* = 5.16; at r = 0.80 "never within 36"; at r = 0.90 first passes in month 7.
- With c = 2.00 and r = 0.80, free-to-play's monthly contribution is exactly zero every month, so its line is flat at 0.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`. Each model has a distinct color and a distinct marker shape (circle, square, triangle, diamond) so lines are readable without color. Sliders are native range inputs with visible numeric values and keyboard steps. Crossover dots have text labels. Respect reduced motion (no animated line drawing).
