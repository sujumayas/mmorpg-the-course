# MMO401 · Week 13 — Reading an Economic Report

**Why this matters:** A live economy team gets a report every month, and the producer wants one sentence back. Is the money growing too fast, and should we act? The charts rarely agree with each other at first glance. This week you learn to reconcile them with two identities, so the sentence you write is right.

**You will be able to:**
- Reconcile a money supply chart with a faucet and sink table and compute the unexplained residual.
- Decompose a change in the price level into money, velocity and volume using the quantity equation in growth form.
- Compute per-capita and concentration figures from report totals and explain what each total hides.
- Write a five-line reading of a report that states what changed, why, and whether it needs an intervention.

**Before class:** CCP Games, *Monthly Economic Report* for any recent month (download the charts; read the money supply, money velocity and price index charts closely). Lehdonvirta & Castronova, *Virtual Economies: Design and Analysis* (MIT Press, 2014), from the course reading list ch. 9-12, reread the material on money and on managing the economy. Fisher, *The Purchasing Power of Money* (1911), chapter 2 (the equation of exchange), skim.

**Prerequisites from earlier courses:** [GD102 week 2, stocks and flows](../../GD102-systems-design-and-game-mechanics/lectures/w02-stocks-and-flows.md) (a stock changes by inflow minus outflow). [MA102 week 12, descriptive statistics](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w12-descriptive-statistics-for-playtests.md) (mean versus median, and why skew matters). [MMO304 week 13, case studies](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w13-case-studies-eve-diablo-runescape-grand-exchange.md) (EVE's published data and Old School RuneScape's tax). [MMO304 week 4, money supply per capita and inflation](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w04-money-supply-per-capita-and-inflation.md). [MMO304 week 12, economic telemetry and dashboards](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w12-economic-telemetry-and-dashboards.md). From this course, [week 4, monetary policy tools](w04-monetary-policy-tools-in-games.md), and week 12 on exploits and rollbacks (see the [MMO401 syllabus](../syllabus.md)).

**Interactive:** [Report decomposition](../examples/w13-report-decomposition.html) (spec at the end of this lecture). Keep it open during section 2.

---

## 1. What a report is for

An economic report is a set of charts built from logs. Every coin the server creates, deletes or moves leaves a record, and the report sums those records by category and by month. CCP Games publishes one for EVE Online every month. The January 2024 edition has about 27 charts covering production, mining and destruction, regional trade, NPC bounties, money supply, money velocity, and four price indices (consumer, mineral, primary producer and secondary producer). CCP also releases the raw data behind them.

Most studios never publish theirs. Inside the studio, someone still reads one every month. In MMO304 you learned to build a dashboard. This week you are the reader, and the reader's job is harder than it looks, for three reasons.

**Charts are totals.** A money supply chart adds up every account. It cannot tell you whether a thousand players each got a little richer or one cartel got very rich.

**Charts use definitions you did not choose.** "Money supply" might count every coin in the database, or only coins held by players who logged in recently. "Velocity" might be monthly or daily. The same economy can produce different charts under different definitions, and a change in definition looks like a change in the economy.

**Charts disagree.** The money chart can go up while the price chart goes down. Readers who look at one chart at a time will tell the producer two opposite stories in the same meeting.

The fix is to stop reading charts one at a time. Read them against identities. An identity is an equation that holds by definition, whatever players do. If the numbers in a report break an identity, either the report has an error, or a definition changed, or money moved through a channel the report does not track. All three are worth finding. If the numbers satisfy the identities, the identities tell you which chart explains which.

You need two.

## 2. Worked example: money up, prices down

### The hook

Picture a month's report for a mid-size MMO. The money supply chart climbs 2.6%. A designer on the team sees it and says prices are about to rise, so the team should raise a sink. Two pages later, the consumer price index has fallen 3.5%. Players on the forums are complaining that their loot sells for less.

Both charts are correct. The designer's instinct is common and it is wrong here, and acting on it would push prices down further. The two identities below show why in about five minutes of arithmetic.

EVE's report has exactly this shape. It prints money supply, money velocity and price indices as separate charts, and it leaves the reconciliation to you.

### The model

**Identity 1, the stock-flow identity.** Money is a stock. Faucets add to it and sinks remove from it (GD102 week 2, MMO304 week 3).

```
M_end = M_start + F − S + R
```

- `M_start`, `M_end` are the money supply at the start and end of the month.
- `F` is the total of all faucets in the report (NPC bounties, quest rewards, sales to NPC vendors).
- `S` is the total of all sinks (market taxes, fees, repairs, NPC purchases).
- `R` is the residual, everything the other terms miss. In a perfect report `R = 0`.

**Identity 2, the equation of exchange.** Irving Fisher wrote it down in 1911 for national economies, and it holds in any economy with money.

```
M × V = P × Q
```

- `M` is the money supply.
- `V` is velocity, how many times the average coin changes hands per period. Compute it as `V = T / M`, where `T` is the total value of trades in the period.
- `P` is the price level, an index of what things cost.
- `Q` is the real volume of trade, how many goods changed hands, measured at fixed prices.

Since `T = M × V` and also `T = P × Q`, this is an identity. It says nothing about causes. Its use is bookkeeping. If you know three of the four, the fourth is fixed.

Take the ratio of two months and you get the growth form. For small changes the growth rates add:

```
(1 + gP) = (1 + gM)(1 + gV) / (1 + gQ)
gP ≈ gM + gV − gQ
```

Each `g` is a growth rate for the month, so `gM = +0.026` means the money supply rose 2.6%. In words, **prices rise with money and velocity and fall with volume.** A money chart alone predicts prices only if velocity and volume held still.

### Numbers you can check

Here is the month. The game and its currency (crowns) are invented, so the numbers are easy to check by hand. All money figures are in billions of crowns.

| Faucets | Amount | Sinks | Amount |
|---|---|---|---|
| NPC bounties | 85 | Sales tax (2% of market trades) | 78 |
| Quest rewards | 35 | Repairs | 20 |
| Sales to NPC vendors | 20 | Other fees | 12 |
| **Total F** | **140** | **Total S** | **110** |

The money supply chart reads 1,000 at the start and 1,026 at the end.

**Step 1, reconcile the stock.** Net flow is `F − S = 140 − 110 = +30`. The identity predicts `M_end = 1,030`. The chart shows 1,026. So `R = 1,026 − 1,030 = −4`, which is 0.4% of the stock and 13% of the net flow. Hold that thought.

**Step 2, check the sink against its own rule.** The sales tax is 2% of market trades. Market trade value this month was `T = 3,900`, and `0.02 × 3,900 = 78`. The tax line matches. When a sink is a rate times a base, check it. A mismatch here means some trades avoided the tax, or the rate is not what the patch notes say.

**Step 3, decompose the price change.**

| Quantity | Last month | This month | Growth |
|---|---|---|---|
| Money supply `M` | 1,000 | 1,026 | +2.60% |
| Trade value `T` | 4,000 | 3,900 | −2.50% |
| Velocity `V = T / M` | 4.000 | 3.801 | −4.97% |
| Volume index `Q` | 100 | 101 | +1.00% |
| Price level `P = T / Q` | 40.00 | 38.61 | −3.47% |

The growth form gives `gP ≈ 2.60 − 4.97 − 1.00 = −3.37%`. The exact product gives `1.026 × 0.950292 / 1.01 = 0.965347`, a fall of 3.47%. Keep the digits. Round the velocity factor to 0.9503 first and you get a fall of 3.46%. Round `P` to 38.61 first and you get 3.48%. Compute growth rates from unrounded values. The approximation is off by 0.1 point, which is fine for a meeting and not fine for a chart label.

Now the story is clear. Money grew 2.6%. The average coin changed hands 5% less often. Slightly more goods traded. The velocity drop was twice as big as the money growth, so prices fell.

**Step 4, per capita.** Active players rose from 50,000 to 54,000, up 8%, perhaps because of a content patch. Money per player went from `1,000 / 50,000 = 20.0` million to `1,026 / 54,000 = 19.0` million crowns, down 5%. New players arrive with almost nothing. They add to the head count faster than they add to the money stock. That is one plausible reason velocity fell, since new players trade less than veterans. The report cannot prove it. It tells you where to look next, which is velocity split by account age.

**Step 5, the residual.** Four billion crowns went missing. Candidates, in the order to check them:

1. A definition. If the money supply counts only accounts active in the last N days, a veteran who quits takes their balance out of the chart without any sink firing. An 8% rise in players suggests churn at the same time.
2. A flow the report does not categorise, such as GM refunds or a new fee added in a patch after the report's category list was written.
3. An exploit or a logging bug (week 12). These usually show up as a positive residual, money appearing with no faucet.

A small negative residual in a month with high churn is probably definitional. A positive residual of this size would go straight to the security team.

### The visual

Open the interactive. The left panel shows the money supply as a waterfall. Start at 1,000, add each faucet, subtract each sink, add the residual, and land at 1,026. The right panel shows the price change as three bars (money, velocity, volume) that sum to the price bar.

Drag the velocity slider from −5% to 0%. The left panel barely moves. Velocity is not in the stock identity, and the only link is the sales tax, which grows with trade, so the money supply ends at 1,022 instead of 1,026. The right panel's price bar flips from −3.5% to +1.2%. The money chart looked almost the same in both worlds, and the price outcome was opposite. Then drag the player-count slider and watch money per player fall while the total rises.

### Cross-game recognition

**EVE Online (monthly reports, current format).** Map each chart to a term. Money supply is `M`. Money velocity is `V`. The consumer price index is a `P`. Production, mining and trade volume charts stand in for `Q`. The bounty chart is one line of `F`. With four charts you can check the equation of exchange yourself. When two of CCP's charts seem to contradict each other, the third usually resolves it. Note that CCP computes its own velocity and price index, and the report pages do not state the formula or period for either (checked for the October 2024 report). The raw data file shows only that money supply is split into character and corporation ISK. Before you combine them, check whether the periods match, because a daily velocity and a monthly money supply do not multiply into anything meaningful.

**Old School RuneScape (Grand Exchange tax since December 2021).** The tax is a sink written as a rate times a base, like step 2. From May 29, 2025 it is 2% of each sale, capped at 5 million coins per item. Two reading lessons come out of it. First, the cap breaks the rate-times-base check for expensive items. Above 250 million coins per item, the tax is flat, so `S_tax / T` drops below 2% whenever high-value items trade more. A falling effective rate does not mean evasion. It may mean the mix of trades shifted upward. Second, Jagex announced in May 2025 that the item sink funded by the tax had removed about 5.7 trillion coins' worth of items since launch. That figure is priced in coins, but it describes items leaving the game, which is a change on the `Q` side. The coins used to buy those items went to the players who sold them, so that part of the spending stays in circulation. Most of the tax is simply deleted. Always ask which side of the identity a reported number lives on.

**National statistics (any central bank).** Real economies split the same data across agencies. One publishes the money stock. Another publishes a consumer price index. Economists who want to know why prices moved do the same decomposition you just did, and they hit the same problem you will. Velocity is not measured directly. It is whatever makes the identity balance. In a game you have the trade logs, so you can compute `T` from records and velocity becomes a measurement instead of a leftover. That is a genuine advantage the in-house economist has over a central banker.

Three settings, one reading habit. Put each number into an identity, find the term it belongs to, and check that the terms add up.

### Eyes-open design judgment

- **Identities do not tell you causes.** The decomposition says velocity fell. It does not say why. New players, a patch that made crafting less profitable, a holiday week, or traders waiting for an announced tax change all lower velocity. You need a second cut of the data (by account age, by region, by item category) to choose between them.
- **The growth form is an approximation.** For monthly changes of a few percent it is within a tenth of a point. For an event month, such as an exploit that doubles the money supply, use the exact ratio. `gM = +100%, gV = −40%` gives `+60%` by addition and `+20%` exactly.
- **Price indices are baskets someone chose.** A consumer price index built from ammunition and ships moves with combat. One built from crafting inputs moves with gathering. Know the basket before you trust the index, and prefer several indices to one.
- **Do not act on one month.** A month is a noisy sample (MA102 week 13). Look for three months in the same direction, or one month with a known cause, before you move a lever. Next week's lecture covers how to size the lever once you decide.

## 3. Totals hide distributions

Everything above treats "the economy" as one account. Players do not live in the average.

### Money per player is a mean

Money per player, 19.0 million crowns, is a mean. Wealth in online economies is usually highly skewed, and the mean sits far above what a typical player holds (MA102 week 12). If the top 1% of accounts hold half the money, then the other 99% hold the other half, and the median player may have a tenth of the mean.

This matters for policy. A flat sink, like a fixed repair cost, takes the same crowns from everyone. For the median player it is a large share of their wealth. For the top 1% it is invisible. A proportional sink, like a sales tax, falls on whoever trades most. Before you choose, you need to know the distribution, and a report of totals will not show it. Ask your data team for percentiles: the 10th, 50th, 90th and 99th percentile of balances, month by month. If only one wealth chart gets added to your report, make it that one.

### Concentration in space

EVE's markets are regional, and the report shows trade by region. The EVE University Wiki, citing the February 2025 report, lists the value of market offers at five trade hubs. Jita had about 687 trillion ISK, Amarr about 54 trillion, Dodixie about 17 trillion, Hek about 10 trillion and Rens about 8 trillion. Add them and Jita holds `687 / 776 = 88.5%` of the five-hub total.

A reader can take two lessons from one division. First, "EVE's market" mostly means Jita's market. A price index averaged over regions will track Jita whatever happens elsewhere. Second, a change that affects only the hub, such as a tax on NPC stations, touches most listed value while touching few systems. Week 9 covered why that concentration forms. This week the point is that you must look at shares, not totals, to see it.

### Ratios that travel well

A report's totals depend on how many players you have. Ratios let you compare months, and games, of different sizes. Compute these every month:

| Ratio | Formula | What it tells you |
|---|---|---|
| Sink coverage | `S / F` | Below 1, money grows. Above 1, it shrinks. Our month: `110 / 140 = 0.79`. |
| Money growth | `(M_end − M_start) / M_start` | Compare to player growth. |
| Money per active player | `M / N` | The number players feel. |
| Faucet per active player | `F / N` | Monthly income of the average account: `140 / 54,000 ≈ 2.6` million. |
| Effective tax rate | `S_tax / T` | Check against the patch notes. |
| Residual share | `R / (F − S)` | Above about 10%, find out why. Our month: 13%. |

A sink coverage of 0.79 does not say anything is wrong. A new game with a growing population should run below 1, because each new player needs a starting balance. A mature game with flat population and coverage well below 1 for a year has a money stock that will keep rising. The ratio is a speedometer, not a verdict.

## 4. Writing the reading

The report is input. Your output is a short reading that a producer can act on. Use five lines, in this order.

1. **What changed.** The one or two numbers that moved most, with sizes. "Consumer prices fell 3.5%; money supply rose 2.6%."
2. **Why, from the identities.** "Velocity fell 5%, more than offsetting money growth. Active players rose 8%, so money per player fell 5%."
3. **What does not add up.** "A residual of −4 billion (13% of net flow). Probably churn under the active-money definition; checking."
4. **What it means for players.** "Sellers get less per item. New players are poorer than last month's new players."
5. **Action.** Either "no action, watch velocity by account age next month" or a named intervention with a size. Most months the right answer is no action.

Resist the urge to add a sixth line. If the reading needs more, you have not yet found the main cause.

A good reading is also falsifiable. "Velocity fell because new players trade less" predicts that velocity among accounts older than 90 days did not fall. If next month's cut shows it did, you were wrong, and you say so. The in-house economist's credibility comes from predictions that sometimes fail in public, then get corrected.

## In-class activity (25 minutes)

Pairs. Each pair gets this second month for the same game (billions of crowns):

| Item | Value |
|---|---|
| Money supply start / end | 1,026 / 1,110 |
| Faucets: bounties / quests / NPC sales | 90 / 36 / 21 |
| Sinks: sales tax / repairs / other | 84 / 21 / 12 |
| Market trade value `T` | 4,200 |
| Volume index `Q` | 100 |
| Active players | 55,000 |

1. (8 min) Reconcile the stock and compute `R`. Check the sales tax against 2% of `T`.
2. (8 min) Compute `V`, `P` and the growth of each from last month (use this lecture's month as "last month"). Decompose `gP`.
3. (9 min) Write the five-line reading.

Expected output: the numbers, plus five lines. Hint for step 1: the residual is large and positive this time. Line 3 of your reading should say what you would check first, and why a positive residual is more alarming than last month's negative one.

## Common misconceptions

- **"Money supply up means inflation."** Only if velocity and volume hold still. The equation of exchange lets prices move opposite to money whenever velocity or volume move more than money does.
- **"The residual is rounding error; ignore it."** A residual of a few percent of net flow may be rounding. A residual that is a large share of net flow is a missing channel, a definition change or an exploit. Report it every month so you notice when it jumps.
- **"More money per player means players are richer."** A mean rises when the top gets richer, even if the median falls. Ask for percentiles.
- **"A falling effective tax rate means players are dodging the tax."** With a capped tax, the effective rate falls when the trade mix shifts to expensive items. Check the mix before blaming evasion.

## Check yourself

1. A report shows `M_start = 800`, faucets 120, sinks 95, and `M_end = 841`. Compute the residual and its share of net flow. Is this more likely definitional or an exploit? Explain.
2. Money grew 4%, velocity grew 2%, and volume grew 3%. Estimate the price change with the growth form, then compute it exactly.
3. A game with a 3% sales tax and no cap reports `T = 6,000` and a sales tax sink of 150. What effective rate does that imply, and name two explanations for the gap.
4. A new game's sink coverage `S / F` has been 0.6 for six months while active players grew 40%. A colleague wants to add a large sink right away. Using money per player, say what you would compute first and why.
5. In the Old School RuneScape Grand Exchange rules from May 2025, what tax is paid on one item selling for 600 million coins, and what effective rate is that?

<details>
<summary>Answers</summary>

1. Predicted `M_end = 800 + 120 − 95 = 825`. Residual `841 − 825 = +16`, which is `16 / 25 = 64%` of net flow. A large positive residual means money appeared without a recorded faucet. That points to an exploit, a logging gap or an untracked faucet, not to churn, which usually pushes the residual negative under an active-money definition.
2. Growth form: `4 + 2 − 3 = +3%`. Exact: `1.04 × 1.02 / 1.03 = 1.0299`, so +2.99%.
3. `150 / 6,000 = 2.5%`, below the 3% rate. Possible explanations: some trade in `T` is untaxed (direct trades, exempt items), skills or reductions lower some players' rate, or `T` is measured differently from the taxed base.
4. Compute money per active player over the six months. If it is flat or falling, the money growth is being absorbed by new players who need starting balances, and a large sink would hit them hardest. Only if money per player is rising steadily is there a per-player inflation problem to fix.
5. 2% of 600 million is 12 million, over the 5 million cap, so the tax is 5 million. That is `5 / 600 = 0.83%`.

</details>

## Lab / assignment hook

[Lab 13, reading a year of reports](../labs/lab13.md). You get twelve months of synthetic report data for the same invented game. You reconcile every month, decompose every price change, find the month with the exploit, and write a five-line reading for the three most important months. The lab's decomposition code becomes the diagnostic step of the policy memo in your final project, and [week 14](w14-intervention-design.md) turns the diagnosis into an intervention.

## Sources

- CCP Games, *Monthly Economic Report, January 2024*, eveonline.com (accessed September 2026). About 27 charts, including production, mining and destruction, regional trade and imports, NPC bounties, money supply, money velocity, and consumer, mineral, primary producer and secondary producer price indices; raw data offered for download.
- CCP Games, *Monthly Economic Report, October 2024*, eveonline.com (retrieved September 2026). Money supply and money velocity charts shown without a published definition or formula.
- EVE University Wiki, "Trade hubs" (accessed September 2026), citing the EVE Monthly Economic Report for February 2025. Market offer value at Jita (about 687 trillion ISK), Amarr (about 54 trillion), Dodixie (about 17 trillion), Hek (about 10 trillion) and Rens (about 8 trillion).
- Old School RuneScape Wiki, "Grand Exchange tax" (accessed September 2026). Tax of 1% from December 9, 2021, 2% from May 29, 2025, capped at 5 million coins per item; most revenue removed from the game, a small part used to buy selected items from players and delete them; Jagex's May 29, 2025 announcement of about 5.7 trillion coins' worth of items removed by the item sink since launch; exemptions for low-level supplies and bonds.
- Wikipedia, "Eve Online" (accessed September 2026). CCP hired economist Eyjólfur Guðmundsson in 2007; he left in 2014.
- Fisher, I. (1911). *The Purchasing Power of Money*. Macmillan. Chapter II, "Purchasing Power of Money as Related to the Equation of Exchange" (Library of Economics and Liberty edition, retrieved September 2026). The equation of exchange `MV = PT`, written here in its modern `MV = PQ` form.
- Lehdonvirta, V. & Castronova, E. (2014). *Virtual Economies: Design and Analysis*. MIT Press.

## Interactive spec: examples/w13-report-decomposition.html

**Purpose.** Show that the money supply chart and the price chart can point in opposite directions, and that velocity and volume, which never appear in the money chart, decide which way prices go.

**Layout.** Controls on top. Two panels side by side at desktop width, stacked on mobile (left panel first). A numbers strip under the panels. A "Load in-class month" button swaps all controls to the in-class activity values.

**Controls (all money in billions of crowns).**
- `M_start`: number input, default 1,000.
- Faucets: three sliders, bounties 0-200 (default 85), quests 0-100 (default 35), NPC sales 0-100 (default 20).
- Sinks: sales tax rate slider 0-10% step 0.5 (default 2%), repairs 0-100 (default 20), other fees 0-100 (default 12). The sales tax sink is computed as `rate × T`.
- Residual `R`: slider −50 to +50 (default −4).
- Last month's trade value `T_0`: fixed at 4,000. Last month's volume `Q_0`: fixed at 100.
- Velocity change `gV`: slider −20% to +20%, step 0.1 (default the exact lecture value `3,900 / 1,026 / 4 − 1 = −4.9708%`, displayed as −4.97%). With `gV` typed as exactly −4.97%, `gP` comes out −3.46%. The default must use the unrounded value so the interactive matches the lecture's −3.47%.
- Volume change `gQ`: slider −10% to +10%, step 0.5 (default +1%).
- Active players: last month fixed at 50,000; this month slider 30,000-80,000 step 1,000 (default 54,000).

**Computation.**
- `F = bounties + quests + npc`. `V_0 = T_0 / M_start`. `V_1 = V_0 × (1 + gV)`.
- The sales tax depends on `T_1`, which depends on `M_end`, which depends on the tax. Solve directly: `M_end = (M_start + F − repairs − other + R) / (1 + rate × V_1)`, then `T_1 = M_end × V_1`, `S_tax = rate × T_1`.
- `gM = M_end / M_start − 1`. `P_0 = T_0 / Q_0`. `Q_1 = Q_0 × (1 + gQ)`. `P_1 = T_1 / Q_1`. `gP = P_1 / P_0 − 1` (exact), and `gP_approx = gM + gV − gQ`.
- Money per player last month `M_start / 50,000`, this month `M_end / N_1`, shown in millions.

**Left panel, money waterfall.** Vertical waterfall from `M_start`: one green step per faucet, one red step per sink, a grey step for `R`, ending at `M_end`. Label each step with its value. Headline above: "Money supply +x.x%".

**Right panel, price decomposition.** Horizontal bars for `gM` (positive to the right), `gV`, and `−gQ`, then a thicker bar for `gP_approx` equal to their sum, and a marker on it for exact `gP`. Headline: "Price level ±x.x%". When `sign(gM) ≠ sign(gP)`, show the caption "Money and prices moved in opposite directions: look at velocity."

**Numbers strip.** `F`, `S`, `F − S`, `R`, `R / (F − S)`, `M_end`, `V_0`, `V_1`, `T_1`, `S_tax`, effective tax `S_tax / T_1`, `P_0`, `P_1`, `gP` exact and approximate, money per player both months, sink coverage `S / F`.

**The one insight.** Dragging `gV` barely changes the left panel (only through the sales tax) and flips the right panel. At defaults the money headline reads +2.6% and the price headline reads −3.5%.

**Test values.**
- Defaults: `F = 140`, `V_1 = 3.8012`, `M_end ≈ 1,026.0`, `T_1 ≈ 3,900`, `S_tax ≈ 78.0`, `S = 110`, `gM ≈ +2.60%`, `P_1 ≈ 38.61`, `gP ≈ −3.47%` exact (−3.4653%), `−3.37%` approximate, money per player 20.0M then 19.0M, `S / F = 0.786`.
- Defaults with `gV = 0`: `V_1 = 4.0`, `M_end = (1,000 + 140 − 32 − 4) / 1.08 = 1,022.2`, `T_1 = 4,088.9`, `S_tax = 81.8`, `gP = 1.0222 × 1 / 1.01 − 1 = +1.21%` exact. The price bar flips sign while the money headline barely moves.
- All faucets and sinks 0, `R = 0`, `gV = 0`, `gQ = 0`: every bar is 0 and `M_end = M_start`.

**Accessibility.** Faucet and sink steps differ by a pattern or a +/− label, not colour alone. Every slider shows its value as text and is keyboard operable. Colours from `templates/interactive-tokens.css`. No animation when `prefers-reduced-motion` is set.
