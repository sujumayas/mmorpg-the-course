# MMO304 · Week 12 — Economic Telemetry and Dashboards

**Why this matters:** An MMO economy changes every hour, and players will tell you it is broken long before it is. The only defense is measurement you set up before launch. The wrong number on a dashboard is worse than no number, because a team will patch the game in response to it.

**You will be able to:**
- Design a currency ledger that tags every faucet and sink, and reconcile it against balance snapshots to find untracked gold.
- Compute a fixed-basket (Laspeyres) price index and a Paasche index from market data, and explain why the average transaction price misleads.
- Compute money supply per active player and show how the choice of denominator changes the conclusion.
- Specify an economy dashboard for a live game, with each panel's metric, cadence and alert rule.

**Before class:** Lehdonvirta & Castronova, *Virtual Economies: Design and Analysis* (2014), chapter 12, "Macroeconomic Management". Browse one recent EVE Online Monthly Economic Report on eveonline.com and list the charts it contains.

**Prerequisites from earlier courses:** [MA102 week 12, descriptive statistics](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w12-descriptive-statistics-for-playtests.md) (mean vs median, percentiles). [MA102 week 13, sampling and confidence](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md) (why a thin market's weekly price is noisy). DB201 [week 10](../../DB201-data-persistence-and-telemetry/lectures/w10-telemetry-design-events-and-properties.md) and [week 11](../../DB201-data-persistence-and-telemetry/lectures/w11-pipelines-collect-store-query.md) (how events get logged and stored). From this course, [week 3 on faucets, sinks and transformations](w03-faucets-sinks-and-transformations.md), [week 4 on money supply per capita and inflation](w04-money-supply-per-capita-and-inflation.md), and [week 11 on real-money trade](w11-real-money-trade-and-gold-farming.md) (bots show up in telemetry first).

**Interactive:** [Price index dashboard](../examples/w12-price-index-dashboard.html). Keep it open during section 2.

---

## 1. The ledger: measure flows, derive stocks

Economic telemetry starts with one rule. **Every change to any player's currency is logged as an event with a reason code.** A quest reward, a loot pickup, a repair bill, an auction fee, a trade between players. Each gets a row with a timestamp, the account, the amount, and a tag that says which faucet or sink it came from.

This event log is the **ledger**. From it you derive everything else. The ledger gives you **flows**, the gold entering and leaving per day by source. The game database separately holds **stocks**, the balance each character holds right now. Week 3 gave you the vocabulary. This week makes it measurable.

Player-to-player trades are logged too, but they are neither faucets nor sinks. They move gold between players without changing the total. Tag them as transfers so they don't pollute your faucet and sink totals.

### Reconciliation: the check that finds bugs

Flows and stocks must agree. If `M` is the total gold held by all characters,

```
M(tomorrow) = M(today) + faucets(today) − sinks(today)
```

Run this every day against a snapshot of all balances. Suppose today's snapshot shows 400,000,000 gold, the ledger logs 38,000,000 of faucets and 34,900,000 of sinks, and tomorrow's snapshot shows 403,600,000. The ledger predicts `400.0M + 38.0M − 34.9M = 403.1M`. There are 500,000 gold that nobody logged.

That gap has three possible causes, and each is urgent.

- **An untagged faucet.** Some code path creates gold without writing a ledger event. Common with new content and hotfixes.
- **A duplication exploit.** Players have found a way to copy gold or items that sell for gold. Duplication gaps grow fast and are often concentrated in few accounts.
- **A logging failure.** Events were dropped. The economy is fine, your pipeline isn't.

A reconciliation gap is the single most valuable alert in economic telemetry. It costs one query a day and catches problems no player report will describe correctly.

## 2. Worked example: the price index and the average-price trap

### The hook

CCP's Monthly Economic Report for EVE Online is a detailed economic dashboard that a studio publishes for its players every month. It shows money supply, money velocity, faucets and sinks, production, mining and destruction, and regional trade. For prices, it does not show "average sale price." It shows a set of **indices**: a Consumer Price Index, a Mineral Price Index, and primary and secondary Producer Price Indices.

Why would a studio with every transaction on record publish a constructed index instead of the plain average? Because the plain average answers the wrong question, and it can be badly wrong in the week you most need it.

### The model

A **price index** measures how much a fixed shopping list costs today compared with a base period. Pick a **basket**: the goods and the quantity `q0` of each bought in the base period. The **Laspeyres index** prices that same basket at today's prices:

```
Laspeyres(t) = 100 × Σ p_t × q_0  /  Σ p_0 × q_0
```

- `p_0`, `q_0` are each good's price and quantity in the base period.
- `p_t` is each good's price in period `t`.
- The sum runs over the goods in the basket.

The **Paasche index** does the same with today's quantities as the basket:

```
Paasche(t) = 100 × Σ p_t × q_t  /  Σ p_0 × q_t
```

The **average transaction price**, the number people reach for first, is total gold spent divided by items sold:

```
average price(t) = Σ p_t × q_t  /  Σ q_t
```

Notice the difference. Both indices hold the mix of goods fixed and let only prices move. The average lets both move. If players start buying more expensive things, the average rises even when no price changed.

### Numbers you can check

A small game's market has three goods. In the base week, potions sell for 10 gold (1,000 sold), ore for 5 gold (2,000 sold) and a crafted sword for 1,000 gold (10 sold). Total spending is 30,000 gold on 3,010 items, so the average price is 9.97.

Three things can happen next week.

| Scenario | What changed | Average price | Change | Laspeyres | Paasche |
|---|---|---|---|---|---|
| Base | — | 9.97 | — | 100.0 | 100.0 |
| A. Mix shift | A new raid needs swords. 40 swords sell instead of 10. No price changes. | 19.74 | +98% | 100.0 | 100.0 |
| B. Real inflation | Every price rises 10%. Quantities unchanged. | 10.96 | +10% | 110.0 | 110.0 |
| C. Hidden inflation | Potions rise to 15. Only 5 swords sell. | 9.98 | +0.2% | 116.7 | 120.0 |

Check scenario A by hand. Spending is `10,000 + 10,000 + 40,000 = 60,000` on 3,040 items, so the average is 19.74. The basket from the base week still costs `10 × 1,000 + 5 × 2,000 + 1,000 × 10 = 30,000`, so Laspeyres is 100.

Check scenario C. The base basket now costs `15 × 1,000 + 5 × 2,000 + 1,000 × 10 = 35,000`, and `35,000 / 30,000 = 116.7`. Spending is `15,000 + 10,000 + 5,000 = 30,000` on 3,005 items, so the average is 9.98. The average shows no inflation at all while the price of the most-bought item rose 50%.

Scenario A is the one that causes panic. A producer sees "average price doubled" on a dashboard the week a raid launches, and someone proposes a new gold sink. Nothing got more expensive. Players spent more because they wanted different things. Scenario C is the one that causes damage by silence. The average stays flat while new players, who spend most of their gold on potions, find their money buys a third less.

### The visual

Open `examples/w12-price-index-dashboard.html`. The left chart shows the average transaction price over twelve weeks. The right chart shows the Laspeyres and Paasche indices over the same weeks. Press "Scenario A" and watch the left chart spike while the right stays flat. Press "Scenario C" and the opposite happens. Then drag the sword-quantity slider on its own. Only the left chart moves.

### Cross-game recognition

**EVE Online (Monthly Economic Report, current).** EVE's indices split the market into groups of goods. The Mineral Price Index covers raw materials, which matter to miners and industrialists, while the consumer and producer indices cover goods further along the production chain. Publishing several indices instead of one admits a fact your dashboard should admit too. Inflation depends on what you buy.

**World of Warcraft Token (since patch 6.1.2, 2015).** The WoW Token costs a fixed US$20, and its gold price is set by supply and demand. That makes the token's gold price a one-item index. The good never changes and neither does its real-money price, so when its gold price climbs, gold is losing value against real money, or more players want game time for gold. A single-item index is noisy and has its own supply and demand, but it is free, public and comparable across years.

**The US Consumer Price Index (Bureau of Labor Statistics).** The real-world CPI prices a market basket of consumer goods and services. Its weights come from spending surveys of thousands of households. It is the same fixed-basket idea you just computed, with one refinement. Since January 1999, the BLS uses a geometric mean inside most item categories, so the index allows for some shopping around when relative prices change. Economists studying virtual worlds borrowed these tools early. Edward Castronova's 2001 study of EverQuest's world, Norrath, measured its output and currency from auction data and concluded that Norrath's GNP per capita sat between Russia's and Bulgaria's, and that its currency was worth more than the yen or the lira at the time.

Three contexts, one formula. Fix the basket, move only the prices.

### Eyes-open design judgment

- **Choosing the basket is a design decision.** A basket of raid consumables tracks endgame players. A basket of repair costs and starter gear tracks new players. Build at least two, and say whose prices each one follows.
- **Laspeyres runs high, Paasche runs low.** When a price rises, players buy less of it. Laspeyres ignores that and overstates the cost increase. Paasche uses the new, smaller quantities and understates it. If the two diverge a lot, as in scenario C, players are substituting, which is itself worth knowing.
- **Baskets go stale.** A basket from launch week says nothing about goods added by an expansion. Reset the basket on a schedule (each major patch is a natural point) and chain the index across resets.
- **Thin goods are noise.** A good that sells 12 times a week has a weekly average price with a wide margin of error (MA102 week 13). Weight by spending, not item count, and don't alert on a single thin good.
- **Public indices change behavior.** EVE publishes its indices. Speculators use them. A public index is a gift to transparency and to traders. Decide which you want before you publish.

## 3. Money supply per player: pick the denominator deliberately

Week 4 showed that inflation follows money supply per capita, not money supply. The telemetry question is which capita to divide by.

| | Month 1 | Month 2 | Change |
|---|---|---|---|
| Total gold held | 1.20 billion | 1.30 billion | +8.3% |
| Monthly active players | 60,000 | 50,000 | −16.7% |
| Gold per monthly active player | 20,000 | 26,000 | +30% |

The team saw +8% money supply and relaxed. Per active player it rose 30%, because the players who left kept their gold on their characters. That gold is "held," but it can't bid on anything until they return. Inactive gold is not spending pressure today. It is spending pressure the day a returning-player event brings those accounts back.

So track three numbers, not one:

1. **Total supply**, from the ledger and reconciliation.
2. **Active supply**, gold held by characters that logged in during the period.
3. **Active supply per active player**, the number that best predicts price pressure.

Each denominator has traps. Bots count as active players. In the lab dataset you will see a bot wave raise the active count, which makes per-player sink spending appear to fall even though real players changed nothing. Alt characters multiply "players" if you count characters instead of accounts. Choose accounts, exclude flagged bots, and say so on the dashboard.

### Velocity

The last money-supply number is **velocity**, the number of times the average gold piece changes hands per period:

```
velocity = gold spent in trades and sinks in the period / active supply
```

It comes from the equation of exchange you met in week 4, `M × V = P × Q`. A rise in velocity with flat supply can push prices up just as well as new gold can. EVE's report tracks it too.

## 4. Distribution: the mean player doesn't exist

A dashboard that shows mean gold per player hides the shape of wealth. MMO wealth is heavily skewed, with a few players holding a large share. With a skewed distribution, the mean is pulled up by the richest accounts and says little about a typical player (MA102 week 12).

Report the median, the 90th and 99th percentiles, and the **top 1% share**, the fraction of all gold held by the richest 1% of active accounts. These answer different questions.

- The **median** tells you what a typical player can afford. Price your sinks for new players against it.
- The **99th percentile** tells you what the market's top buyers can pay. Price luxury sinks against it.
- The **top 1% share** tells you about concentration. A sudden jump means gold is flowing to few accounts. Traders cornering a market, a duplication exploit and bots feeding a seller all look like this.

The same logic applies to faucets. Log, for each faucet source, what share of its gold went to the top 1% of earners that day. A healthy mob-loot faucet pays many players a little each. A mob-loot faucet whose top 1% share jumps from 6% to 37% is almost certainly being farmed by bots. You will find exactly that in the lab.

## 5. Designing the dashboard

A good economy dashboard has few panels, each answering a question someone will act on. Here is a starting layout. Adapt it, but write down for each panel the metric, the cadence and the alert rule.

| Panel | Metric | Cadence | Alert when |
|---|---|---|---|
| Reconciliation | Snapshot supply minus ledger-predicted supply | Daily | Any gap above 0.1% of supply |
| Faucets and sinks | Gold per day by source, stacked; sink/faucet ratio | Daily, 7-day average | Any source moves more than 25% week on week without a patch note |
| Supply per active player | Active supply / active accounts, bots excluded | Daily | 30-day growth above the target inflation band |
| Price indices | Laspeyres for two or more baskets, plus Paasche | Weekly | Index moves more than 5% in a week |
| Wealth distribution | Median, p90, p99, top 1% share | Weekly | Top 1% share jumps more than 5 points |
| Faucet concentration | Top 1% share per faucet source | Daily | Share doubles against its 28-day average |
| Market health | Volume and bid-ask spread for key goods | Daily | Volume falls by half, or the spread doubles |

Three rules keep a dashboard useful.

1. **Every alert names an owner and an action.** "Top 1% share of mob loot doubled" should page the anti-bot team, not the whole studio.
2. **Annotate patches.** Put every patch, event and ban wave on the time axis. Half of all "anomalies" are content you shipped.
3. **Show the uncertainty.** Weekly prices of thin goods deserve an error bar. A panel without one invites overreaction.

MMO308 goes deeper into live-ops analytics and experiments. This week's goal is narrower. Know which economic numbers to log from day one, because you can't reconstruct a ledger you never wrote.

## In-class activity (25 minutes)

Pairs. You are the economist for a new MMO launching next month. You get a list of 12 faucets and sinks from the design document (on the handout: quest rewards, mob loot, vendor sales, crafting sales to NPCs, daily login gold, repairs, auction fees, fast travel, NPC consumables, housing rent, guild upkeep, respec cost).

1. Write the ledger event schema: field names and types, and the reason-code list.
2. Choose two price baskets of four goods each, one for new players and one for the endgame. Justify each choice in one sentence.
3. Pick the three dashboard panels you would build first and give each an alert rule with a number.
4. Swap with another pair. Invent one incident (a dupe, a bot wave, a bugged fee) and check whether their dashboard would catch it within a day.

Expected output: the schema, two baskets, three panels with alert rules, and one incident that their dashboard missed (if any).

## Common misconceptions

- **"Average price is the inflation rate."** The average moves when the mix of goods changes. Use a fixed-basket index.
- **"Money supply went up 8%, so prices will rise about 8%."** Divide by active players, account for inactive gold, and watch velocity. The per-player number can move very differently.
- **"If the ledger balances, the economy is fine."** Reconciliation catches untracked gold. It doesn't catch tracked gold flowing to bots. That takes the concentration panels.
- **"More metrics make a better dashboard."** A panel with no owner and no alert rule is decoration. It trains people to ignore the screen.

## Check yourself

1. A snapshot shows 812,000,000 gold. The ledger logs 51,400,000 of faucets and 47,900,000 of sinks for the day. The next snapshot shows 816,100,000. What is the reconciliation gap, and what are two possible causes?
2. Base week: bread 4 gold (500 sold), arrows 1 gold (3,000 sold), cloaks 200 gold (20 sold). Next week: bread 5, arrows 1, cloaks 200, with 400 bread, 3,000 arrows and 30 cloaks sold. Compute the Laspeyres index, the Paasche index and the change in the average price.
3. Total supply rises from 500 million to 540 million in a month, while active accounts rise from 25,000 to 30,000. What happened to gold per active account? Would you add a sink?
4. The mob-loot faucet's daily total rose 40%, active accounts rose 7% and its top 1% share went from 6% to 35%. What is the most likely cause, and which team do you call?

<details>
<summary>Answers</summary>

1. Predicted `812.0 + 51.4 − 47.9 = 815.5` million. The gap is 600,000 gold (about 0.07% of supply), close to the 0.1% alert line. Causes include an untagged faucet (new content or a hotfix), a duplication exploit, or dropped log events.
2. Base basket cost: `4 × 500 + 1 × 3,000 + 200 × 20 = 9,000`. At new prices: `5 × 500 + 3,000 + 4,000 = 9,500`, so Laspeyres is 105.6. Paasche: new spending `5 × 400 + 3,000 + 200 × 30 = 11,000`; new quantities at old prices `4 × 400 + 3,000 + 6,000 = 10,600`; Paasche is 103.8. Average price: base `9,000 / 3,520 = 2.56`, next `11,000 / 3,430 = 3.21`, a rise of 25%. The average overstates inflation because more cloaks were sold.
3. From 20,000 to 18,000 per active account, a fall of 10%. Supply per active player dropped, so a new sink would push toward deflation. Check the price index before acting.
4. Bots farming mob loot. A 40% faucet rise with only 7% more accounts, concentrated in few accounts, is a bot signature. Call the anti-bot or security team, and remember that the bots also inflate your active-account denominator.

</details>

## Lab / assignment hook

[Lab 12, economy telemetry](../labs/lab12.md). You get 56 days of ledger data and 8 weeks of market data from a fictional server. You will reconcile the supply, build the dashboard panels from section 5, and find three incidents hidden in the data. This lab is the course's telemetry lab (20% of the grade).

## Sources

- CCP Games, "Monthly Economic Report" (EVE Online, June 2024 edition as an example of the current format). Sections include production, mining and destruction, money supply, money velocity, economy indices (Consumer Price Index, Mineral Price Index, primary and secondary Producer Price Indices), sinks and faucets, and regional trade.
- Warcraft Wiki, "WoW Token". Fixed US$20 price, gold value set by supply and demand, introduced in patch 6.1.2 (Americas from 7 April 2015).
- US Bureau of Labor Statistics, "Consumer Price Index: Frequently Asked Questions". Market basket, weights from expenditure diaries and interviews, geometric mean formula for most basic indexes since January 1999.
- Castronova, E. (2001). "Virtual Worlds: A First-Hand Account of Market and Society on the Cyberian Frontier." CESifo Working Paper 618. Abstract checked on RePEc/IDEAS (September 2026): GNP per capita "somewhere between that of Russia and Bulgaria", currency traded at USD 0.0107, "higher than the Yen and the Lira".
- Lehdonvirta, V. & Castronova, E. (2014). *Virtual Economies: Design and Analysis*. MIT Press.

## Interactive spec: examples/w12-price-index-dashboard.html

**Insight the visual must make obvious:** the average transaction price moves when players buy a different mix of goods, even when no price changes. A fixed-basket index moves only when prices do.

**Layout:** two linked line charts over 12 weeks, side by side on desktop, stacked on mobile. Below them, an editable table of the three goods.

- **Left chart, "Average price paid":** `Σ p q / Σ q` per week, as a line. y-axis starts at 0.
- **Right chart, "Price index (week 1 = 100)":** Laspeyres (solid, steel token) and Paasche (dashed, gold token). y-axis from 80 to 140, extending if needed.
- **Table:** rows potion, ore, sword. Columns base price, base quantity, and for the currently selected week, price and quantity. Selecting a week (click a point or use left/right arrow keys) loads that week into the table.

**Controls:**
- Scenario buttons: "Base", "A. Mix shift", "B. Real inflation", "C. Hidden inflation", "Custom".
- Scenario timeline: weeks 1-4 are base. The scenario applies from week 5 to week 12, ramping linearly over weeks 5-8 and holding from week 9. Example for A: sword quantity goes 10, 17.5, 25, 32.5, 40 over weeks 4-8 and stays 40.
- In Custom mode, three price-multiplier sliders (0.5 to 2.0, step 0.05) and three quantity-multiplier sliders (0.25 to 5, step 0.25), one per good, applied at week 12 with the same ramp.
- Toggle "Show average on index scale" that rescales the average to 100 at week 1 and overlays it on the right chart as a thin line, so the gap is visible on one axis.

**Readout:** for the selected week, average price and its change from week 1, Laspeyres, Paasche, and a one-line verdict: "Prices moved" if Laspeyres differs from 100 by more than 1, "Mix moved" if the average differs from its week-1 value by more than 1% while Laspeyres is within 1, "Both" otherwise.

**Formulas:**
- `avg(t) = Σ p_t q_t / Σ q_t`
- `L(t) = 100 × Σ p_t q_0 / Σ p_0 q_0`
- `P(t) = 100 × Σ p_t q_t / Σ p_0 q_t`

**Base data:** potion 10 gold × 1,000; ore 5 × 2,000; sword 1,000 × 10.

**Test values (week 12):**
- Base: average 9.97, L 100.0, P 100.0.
- A (sword quantity 40): average 19.74, L 100.0, P 100.0.
- B (all prices × 1.10): average 10.96, L 110.0, P 110.0.
- C (potion price 15, sword quantity 5): average 9.98, L 116.7, P 120.0.
