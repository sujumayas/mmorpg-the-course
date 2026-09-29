# MMO304 · Week 04 — Money Supply per Capita and Inflation

**Why this matters:** Every gold number you type into a design document, from a quest reward to a mount price to a hard cap, is written in a currency that loses value while the server runs. If you can't turn money per player into prices and inflation rates, you'll learn that your 20,000-gold luxury item has become pocket change from the forums, not from your own dashboard.

**You will be able to:**
- Compute a price level from money per player with the quantity equation `M × V = P × Q`, and state the assumptions it needs.
- Compute daily inflation from a money-per-player series and explain why a falling inflation rate can hide a growing problem.
- Convert any fixed gold amount (a reward, a price, a cap) into real terms and predict how fast it loses its effect.
- Build a price index from telemetry and use its gap from money per player to diagnose what changed.

**Before class:** Lehdonvirta & Castronova, *Virtual Economies: Design and Analysis* (2014), chapter 10, "Money". Open one CCP Monthly Economic Report for EVE Online (January 2024 is a good one) and find three charts: money supply, money velocity and a price index.

**Prerequisites from earlier courses:** [MMO304 week 3, faucets, sinks and transformations](w03-faucets-sinks-and-transformations.md) (the stock-and-flow model, flow sinks versus stock sinks and the steady state `m*`). GD102 [week 2, stocks and flows](../../GD102-systems-design-and-game-mechanics/lectures/w02-stocks-and-flows.md), [week 3, positive feedback](../../GD102-systems-design-and-game-mechanics/lectures/w03-positive-feedback-loops-snowballing.md) and [week 4, negative feedback](../../GD102-systems-design-and-game-mechanics/lectures/w04-negative-feedback-loops-rubber-banding.md). [MA101 week 2, linear functions and rates](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w02-linear-functions-and-rates.md) (why a constant slope looks like it slows down in percent). [MA102 week 12, descriptive statistics](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w12-descriptive-statistics-for-playtests.md) (mean versus median on skewed data).

**Interactive:** [Real value drift](../examples/w04-real-value-drift.html). Keep it open during section 2.

---

## 1. From money per player to prices

Last week you built a model that predicts `m`, money per player, day by day. You saw that a flow sink such as repairs only slows the growth of `m`, while a stock sink such as a trade tax gives it a ceiling. You also saw that new players arriving with empty pockets hold `m` down, and that this dilution stops when arrivals stop.

This week asks the next question. Players never see `m`. They see prices. How does money per player turn into the price of a healing potion, and how should you measure the change?

### Three stocks, three definitions

**Money supply**, `M`, is all the currency held by active players right now. In a real economy that's hard to measure. In a game it's one database query, and a good live team runs it daily.

**Active players**, `N`, needs a definition you stick to, such as "logged in during the last 14 days." Change the definition and every per-player number jumps, so write it down and keep it.

**Money per player**, `m = M / N`, is the average balance of an active player. Economists call it money per capita.

### The quantity equation

Economists have a bookkeeping identity, published in its best-known form by Irving Fisher in 1911:

```
M × V = P × Q
```

- `M` is the money supply.
- `V` is **velocity**, the share of the money supply spent per day. If `V = 0.05`, the average coin changes hands once every 20 days.
- `P` is the **price level**, the price of a typical good.
- `Q` is the number of goods bought per day.

The left side is gold spent per day. The right side is the value of goods bought per day. Every purchase counts on both sides, so the two are always equal. As written, it's an identity. It becomes a model when you assume some letters hold still.

In an MMO, a reasonable first assumption is that each player produces and buys a fixed amount of stuff per day, so `Q = q × N`, where `q` is goods per player per day. Divide both sides by `N`:

```
P = (M / N) × V / q = m × V / q
```

If velocity and output per player hold still, **the price level is proportional to money per player**. Double `m` and prices double. Double `M` while `N` also doubles and nothing happens. That's why week 3 divided by `N`.

Throughout this lecture we fix `V = 0.05` and `q = 1` (each player sells one potion a day), so:

```
P = m / 20
```

A server where the average player holds 2,000 gold sells potions at 100 gold. Week 3's price index, `100 × m / 1,000`, is the same idea with a different constant. Next week you will drop the fixed-velocity assumption, because hoarding makes `V` fall.

### Inflation and real value

**Inflation** is a sustained rise in the price level. The **daily inflation rate** is

```
π(t) = P(t) / P(t − 1) − 1
```

If potions cost 100 gold on Monday and 102 on Tuesday, `π = 2%`.

Any amount written in gold is a **nominal** amount. Its **real** value is what it buys, which is the nominal amount divided by the price level. A 100-gold quest reward is worth one potion when `P = 100` and half a potion when `P = 200`. The designer typed the same number both times. The player got half as much.

## 2. Worked example: every fixed number shrinks

### The hook

In World of Warcraft, the most gold one character could hold was 214,748 gold, 36 silver and 47 copper for the game's first six years. That odd number is 2³¹ − 1 copper, the largest value a signed 32-bit integer can store. Blizzard raised the cap to 999,999 gold in patch 4.0.1 (October 2010) and to 9,999,999 gold in patch 7.0.3 (July 2016).

Now look at the game's flagship luxury purchase, a three-seat mount with vendors riding on its back:

| Mount | Added | Vendor price |
|---|---|---|
| Traveler's Tundra Mammoth | Patch 3.0.2 (2008) | 20,000 gold |
| Grand Expedition Yak | Patch 5.0.4 (2012) | 120,000 gold |
| Mighty Caravan Brutosaur | Patch 8.0.1 (2018) | 5,000,000 gold |

That's 250 times the price in ten years. Blizzard doesn't publish WoW's money supply, so you can't read an inflation rate straight off these numbers. What you can read is that a fixed technical limit had to be raised twice, and that designers priced each new luxury sink far above the last one. A 20,000-gold price that meant something in 2008 would not have worked in 2018.

The question for this example: if money per player grows at a steady rate, how fast does a fixed gold number lose its meaning, and why does it feel like the problem is fading when it isn't?

### The model

Take the week 3 server after new players have stopped arriving. Each active player gains a net `n` gold a day from faucets minus flow sinks (in week 3's notation, `n = h(g − r)`). A stock sink removes a share `σ` of all money each day (week 3's `τ × v`). Churn at average wealth doesn't change `m`, so leave it out.

```
m(t + 1) = m(t) + n − σ × m(t)
P(t)     = m(t) × V / q = m(t) / 20
π(t)     = P(t) / P(t − 1) − 1
```

To see what a fixed number is worth, measure it against the economy:

```
real value of a fixed amount X  =  X / P(t)          (in potions)
weight of a fixed price L       =  L / m(t)           (in "average balances")
```

The second measure answers the designer's question: is this price still large compared with what players hold? A luxury mount priced at 10 times the average balance is a serious sink. Priced at one average balance, it's an impulse purchase.

With `σ = 0` the model is a straight line, `m(t) = m(0) + n t`. The daily inflation rate is then

```
π(t) = n / m(t − 1) = n / (m(0) + n (t − 1))
```

The numerator is fixed and the denominator grows, so the rate falls toward zero. Prices never stop rising.

With `σ > 0`, week 3's steady state applies: `m* = n / σ`. Prices level off at `m* / 20`.

### Numbers you can check

Start at `m(0) = 2,000` (potions at 100), with `n = 40` and no stock sink. A newcomer earns a fixed 100 gold a day from level-appropriate quests. The luxury mount costs a fixed 20,000 gold.

| Day | `m` | Potion `P` | Daily inflation `π` | Newcomer's day buys (potions) | Mount price ÷ `m` |
|---|---|---|---|---|---|
| 0 | 2,000 | 100 | — | 1.00 | 10.0 |
| 1 | 2,040 | 102 | 2.00% | 0.98 | 9.8 |
| 30 | 3,200 | 160 | 1.27% | 0.63 | 6.3 |
| 60 | 4,400 | 220 | 0.92% | 0.45 | 4.5 |
| 180 | 9,200 | 460 | 0.44% | 0.22 | 2.2 |
| 365 | 16,600 | 830 | 0.24% | 0.12 | 1.2 |
| 730 | 31,200 | 1,560 | 0.13% | 0.06 | 0.6 |

Check two rows by hand. Day 30: `m = 2,000 + 30 × 40 = 3,200`, so `P = 160`, and `π = 40 / 3,160 = 1.27%`. Day 365: `m = 2,000 + 365 × 40 = 16,600`, so the mount is `20,000 / 16,600 = 1.2` average balances.

Read the columns side by side. The inflation rate falls by a factor of 15 over two years. Anyone watching that column alone would say inflation is under control. Meanwhile, a newcomer's day of questing buys one sixteenth of what it bought at the start, and the "luxury" mount costs less than the average player holds.

Now add a stock sink, `σ = 1%` a day:

| Day | `m` | Potion `P` | `π` | Newcomer's day buys | Mount price ÷ `m` |
|---|---|---|---|---|---|
| 0 | 2,000 | 100 | — | 1.00 | 10.0 |
| 30 | 2,521 | 126 | 0.60% | 0.79 | 7.9 |
| 180 | 3,672 | 184 | 0.09% | 0.54 | 5.4 |
| 365 | 3,949 | 197 | 0.01% | 0.51 | 5.1 |
| steady state | `40 / 0.01 = 4,000` | 200 | 0% | 0.50 | 5.0 |

Every fixed number still loses value, but only once. Prices double and then stop. After that, a designer can set rewards and prices knowing they will hold.

### The visual

Open the interactive. It starts on the **1% stock sink** preset. The left panel shows the potion price over two years, bending over and flattening at `m* / 20 = 200`. The right panel shows the daily inflation rate, plus two "real" lines: what the newcomer's 100 gold buys, and the mount's price in average balances. All three start at 1.0. The inflation line drops to zero within a few months, and the two real lines level off at 0.5. With a stock sink, a calm rate and stable real values go together.

Now press **No stock sink** (`σ = 0`). The left line becomes a straight ramp, climbing by the same 2 gold every day. On the right, the inflation rate still sinks toward zero and looks just as reassuring, but the two real lines no longer level off. They keep sliding down, almost on top of the inflation line. One view says the problem is fading. The other shows it getting worse in the only terms players feel.

Drag the day marker along with each preset and compare the readouts at day 365: 0.51 potions and 5.1 balances with the sink, 0.12 potions and 1.2 balances without it. Finally, switch on **Index the mount price**. The mount's price becomes `10 × m(t)`, and its weight line stays at 10.0 whatever you do to the other sliders. When you can't stop drift, move the price with it.

### Cross-game recognition

The principle is general. Any quantity fixed in currency shrinks at the inflation rate. Here it is in three more places, each read as `X / P(t)`.

**World of Warcraft, the gold cap and the token (retail).** A cap is a fixed nominal `X`. While `m` grows, the richest players' balances approach it, and the cap starts to bind on real behaviour, such as saving for an expensive purchase. Raising it in patches 4.0.1 and 7.0.3 restored its real value. The WoW Token, sold in the Americas from 7 April 2015 at a launch price of 30,000 gold, works the other way. Its gold price floats with supply and demand, so it tracks the value of gold against a fixed real-world bundle (30 days of play). You can read it as a one-item price index. It also moves when demand for gold shifts relative to demand for real money, for example at the start of an expansion, so treat it as evidence of inflation, not a measurement.

**Old School RuneScape (current).** High Level Alchemy turns an item into 60% of its fixed listed value in new coins. That payout is a fixed nominal amount per item. When coin prices rise, alching pays less in real terms and props up fewer items' prices. The Grand Exchange tax, raised from 1% to 2% on 29 May 2025, is capped at 5 million coins per item. A cap written in coins shrinks in real terms, so each year it limits the tax on a smaller real amount of trade. Ask the same question of each rule: is this number fixed in coins, or does it move with the economy?

**EVE Online (current).** CCP's Monthly Economic Report publishes money supply, money velocity and several price indices, so players see `M`, `V` and `P` from the quantity equation in one document. EVE's main sinks are percentages, such as the sales tax on market trades, which is paid to an NPC. On 12 March 2025, CCP raised the base sales tax from 4% to 7.5% (Accounting V lowers it to 3.375%). A percentage sink scales with prices by construction, so it never needs re-indexing. That's week 3's stock sink, and it's also the answer to this week's problem.

**Real economies.** Governments index pensions and tax brackets to a consumer price index for the same reason. A tax bracket written in fixed currency pulls more people into higher rates as wages inflate. Economists call this bracket creep. Your quest rewards have the same problem in reverse.

### Eyes-open design judgment

- **Decide, for every gold number, whether it is nominal or indexed.** Fixed numbers are easy to read and to write guides about. Indexed numbers keep their meaning. A reasonable default is to keep newcomer-facing numbers fixed and stable, such as starter vendor prices, and to index or use percentages for endgame sinks.
- **Percentages are indexing you get for free.** A 5% fee needs no re-tuning as prices rise. A 500-gold fee does. That's one reason stock sinks are popular with live teams.
- **Don't read the inflation rate alone.** A falling rate with positive `n` and no stock sink means prices are still rising without limit. Report the price level and at least one real measure, such as potions per newcomer day, next to the rate.
- **Indexing hides the problem from players, not from the economy.** If you raise every luxury price with `m`, the sink keeps working, but newcomers still face rising market prices. Indexing repairs the sink, not the inflation.
- **Some drift is a choice.** Mild inflation erodes old hoards and makes fresh play matter more. The damage in the first table comes from drift with no ceiling, not from drift itself.

### Check yourself (worked example)

1. With `m(0) = 2,000`, `n = 40` and `σ = 0`, on which day does the daily inflation rate first fall below 0.5%? What is the potion price then?
2. A quest reward of 300 gold was designed to buy three potions at launch (`P = 100`). With `σ = 1%`, how many potions does it buy in the long run?
3. A designer wants the luxury mount to cost 10 average balances forever, with `σ = 1%`. What price should they set once the economy settles?

<details>
<summary>Answers</summary>

1. `π(t) = 40 / m(t − 1)` drops below 0.005 once `m(t − 1) > 8,000`. `m` reaches 8,000 on day 150, so `π(151)` is exactly 0.5% and day 152 is the first day below it. `m(152) = 8,080`, so `P ≈ 404`.
2. Long-run `P = 4,000 / 20 = 200`, so 300 gold buys 1.5 potions.
3. `10 × m* = 10 × 4,000 = 40,000` gold.

</details>

## 3. Reading inflation from telemetry

Your live dashboard (week 12 covers these in depth) shows data, not a model. Here is how to connect the two.

### Measure the flows, then check the stock

For each faucet and sink, log the gold that passes through it each day. Sum the faucets and subtract the sinks to get `ΔM`, the change in money supply per day. Then compare it with the day-to-day change in the database count of `M`. If they disagree, you have an unlogged faucet or sink. In practice that's often a bug, a duplication exploit, or a reward nobody tagged.

### Build a price index

A **price index** is the cost of a fixed basket of goods, divided by the basket's cost on a base day, times 100. Pick goods players buy to use, not to speculate on. Consumables and crafting materials work well. Rare cosmetics don't, because their prices move with fashion and scarcity. If your basket cost 5,000 gold on day 0 and 6,000 on day 30, the index is 120, and the average daily inflation over the month is `1.2^(1/30) − 1 ≈ 0.61%`.

### Use the gap as a diagnostic

The quantity equation says your index should move with `m` if `V` and `q` hold still. When they drift apart, one of the other letters changed:

| What you see | Likely cause | Which letter moved |
|---|---|---|
| `m` rising, index flat | Players are saving, not spending | `V` fell |
| `m` flat, index rising | Saved gold is being spent, often on new content | `V` rose |
| Index falls for one item group only | A drop-rate or recipe change raised supply | `q` for those goods rose |
| Index rises for one item group only | New content needs that consumable | demand shifted |

The last two rows aren't about money at all. They're about supply and demand for particular goods, which is week 6. The first two rows are about velocity, which is next week.

### Watch the distribution, not only the mean

Money per player is an average, and averages in game economies hide a lot. In MA102 week 12 you saw that on skewed data the mean sits far from the median. A server with `m = 2,000` may have a median balance of 300, because a few veterans hold most of the gold. Report the median balance and the share held by the top 10% next to `m`. The median player is the one who feels prices.

## 4. Who inflation hurts

Inflation isn't neutral. It moves real value from some players to others.

- **Newcomers lose most.** Their income is fixed in gold by the quest tables and they have no savings, so rising prices hit their whole budget. In the first table, their real wage fell from 1.00 to 0.12 potions a day in a year.
- **Savers lose ground.** A veteran holding 20,000 gold held 200 potions' worth at `P = 100` and 24 potions' worth at `P = 830`.
- **Sellers of goods gain.** Crafters and gatherers sell at market prices that rise with `m`, while their cost is their time. You'll study them in week 7.

That's why many MMOs scale quest gold with character level. Scaling protects newcomers' real income at their own level. It also raises `n` for veterans, which feeds the inflation it compensates for. Every faucet decision is also a decision about who gets richer.

The alternative for goods newcomers need is to take them out of the player market. Sell starter gear from an NPC at a fixed price. A fixed vendor price doesn't inflate, so newcomers know what they can afford, and the purchase is a flow sink.

Some designers go further and tie a faucet to the price level: "gold drops rise with the price index, so real income stays constant." Run that through the model. `n` rises with `P`, which rises with `m`, which rises with `n`. That's a positive feedback loop from GD102 week 3, and it turns linear drift into exponential inflation. Indexing a faucet is far more dangerous than indexing a sink.

## In-class activity (25 minutes)

In groups of three, audit the gold numbers in a design document for a small MMO. Use this table:

| Rule | Amount |
|---|---|
| Level 10 quest reward | 150 gold |
| Starter sword from NPC vendor | 400 gold |
| Auction house cut | 5% of sale price |
| Guild creation fee | 5,000 gold |
| Housing plot, sold by NPC | 250,000 gold |
| Fast-travel fee | 20 gold |

The live team expects `m` to grow from 2,000 to 6,000 over the first year, with `P = m / 20`.

1. For each rule, compute its real value at launch and after one year, in potions. For the auction cut, explain why no computation is needed.
2. Classify each rule as "keep fixed," "index to `m`" or "convert to a percentage." Justify each in one line, using who pays it.
3. Pick the housing plot. Propose an indexing rule and compute its price after one year so that it costs the same number of average balances as at launch.
4. Write one sentence for your community manager announcing the housing change without using the word "inflation."

Expected output: the table with two new columns, the classification, the housing rule with its number, and the sentence.

<details>
<summary>Instructor check values</summary>

Launch `P = 100`, after one year `P = 300`. Quest reward 1.5 then 0.5 potions; sword 4 then 1.33; guild fee 50 then 16.7; plot 2,500 then 833; travel 0.2 then 0.067. The auction cut is a percentage, so its real value moves with prices automatically. The plot costs `250,000 / 2,000 = 125` average balances at launch. To keep that, set it to `125 × m`, which is 750,000 gold after one year.

</details>

## Common misconceptions

- **"Total gold keeps rising, so we have inflation."** Not necessarily. If `N` grows as fast as `M`, `m` and prices stay flat. Always divide by `N`.
- **"Inflation is slowing down because the daily rate is falling."** With positive `n` and no stock sink, `m` rises by the same amount every day. The rate falls only because the base grows. Check a real measure before you relax.
- **"A price of 20,000 gold is a price of 20,000 gold."** It's 10 average balances on one day and 1.2 a year later. The number you typed doesn't change. What it means does.
- **"Indexing everything fixes inflation."** Indexing sinks keeps them working. Indexing faucets creates positive feedback and makes inflation worse.

## Check yourself

1. A server has `M = 90,000,000` gold and `N = 30,000` active players. With `P = m / 20`, what is the potion price? A month later `M = 99,000,000` and `N = 36,000`. Did prices rise or fall, and by how much?
2. A basket of goods costs 8,000 gold on day 0 and 10,000 gold on day 60. What is the index on day 60, and what is the average daily inflation rate?
3. Your index is flat for a month while `m` rises 15%. Using `M × V = P × Q`, give the most likely explanation, and say what you expect to happen if a big content patch then gives veterans something expensive to buy.
4. With `σ = 0.5%` and `n = 30`, what is the long-run potion price? A 600-gold reward was worth six potions at launch (`P = 100`). What is it worth in the long run?

<details>
<summary>Answers</summary>

1. `m = 3,000`, `P = 150`. A month later `m = 2,750`, `P = 137.5`, a fall of about 8.3%, because the population grew 20% while money grew 10%.
2. Index `= 100 × 10,000 / 8,000 = 125`. Average daily inflation `= 1.25^(1/60) − 1 ≈ 0.37%`.
3. Velocity fell by roughly 13% (`1 / 1.15 ≈ 0.87`), so spending stayed flat. Players are holding more gold without spending it. When new content gives them a reason to spend, `V` rises again and prices jump without any new gold entering. That's next week's topic.
4. `m* = 30 / 0.005 = 6,000`, `P = 300`. The reward buys 2 potions.

</details>

## Lab / assignment hook

[Lab 04, the real value of every gold number](../labs/lab04.md). You extend your week 3 spreadsheet with a price level, a daily inflation rate and a real-value column for each gold amount in a supplied design document, then propose a nominal-versus-indexed policy and defend it with numbers. The lab counts toward the Models component (30%).

## Sources

- Warcraft Wiki, "Gold cap" (retail). Original cap 214,748g 36s 47c (2³¹ − 1 copper); raised to 999,999g 99s 99c in patch 4.0.1 (12 October 2010) and to 9,999,999g in patch 7.0.3 (19 July 2016).
- Warcraft Wiki, "Reins of the Traveler's Tundra Mammoth" (20,000 gold, patch 3.0.2, 2008), "Reins of the Grand Expedition Yak" (120,000 gold, patch 5.0.4, 2012) and "Reins of the Mighty Caravan Brutosaur" (5,000,000 gold from vendors, patch 8.0.1, 2018).
- Warcraft Wiki, "WoW Token". Americas launch on 7 April 2015 (patch 6.1.2) at 30,000 gold; the gold price is set dynamically from supply and demand.
- CCP Games, "Monthly Economic Report, January 2024" (EVE Online). Includes money supply, money velocity, sinks and faucets, and price index charts.
- EVE University Wiki, "Trading" (current). Base sales tax 7.5% since version 22.02 (12 March 2025), up from 4%; 7.5% × (1 − 0.11 × 5) = 3.375% at Accounting V; paid to an NPC corporation.
- Old School RuneScape Wiki, "Grand Exchange" (current). Tax 1% from 9 December 2021 and 2% from 29 May 2025, capped at 5 million coins per item; most revenue removed from the game.
- Old School RuneScape Wiki, "High Level Alchemy" (60% of an item's value in coins).
- Fisher, I. (1911). *The Purchasing Power of Money*. Macmillan. The equation of exchange.
- Lehdonvirta, V. & Castronova, E. (2014). *Virtual Economies: Design and Analysis*. MIT Press.

## Interactive spec: examples/w04-real-value-drift.html

This example builds on week 3's `examples/w03-faucet-sink-simulator.html`, which owns the full faucet/sink simulation (the course's signature example). This one isolates the price side.

**The one insight the visual must make obvious:** the daily inflation rate falls toward zero while the real value of every fixed gold number keeps falling. Only a stock sink (or indexing a specific price) stops the real slide.

**Model (discrete daily update, days 0 to 730, recomputed on every control change).**
```
m(0) = m0
m(t+1) = m(t) + n − σ × m(t)
P(t) = m(t) × V / q                 (q fixed at 1)
π(t) = P(t) / P(t−1) − 1            (undefined at t = 0; show an em-dash placeholder)
realWage(t) = W / P(t)              (potions bought by a newcomer's fixed daily income W)
mountWeight(t) = L(t) / m(t),  where L(t) = L0 if indexing is off, L(t) = k × m(t) if on (k = L0 / m0)
m* = n / σ   (show only when σ > 0)
```
Clamp `m` at 0 if `n < 0` and show "Sinks exceed faucets: money per player falls."

**Layout.** Two linked panels, side by side on desktop, stacked on mobile.
- Left panel "What the price tag says": potion price `P(t)` against day. Dashed horizontal line at `m* × V / q` when `σ > 0`.
- Right panel "What it means": three lines, each normalised to 1.0 at its first defined day: `π(t) / π(1)`, `realWage(t) / realWage(0)`, `mountWeight(t) / mountWeight(0)`. Label each line directly. Under the chart, show the unnormalised values at the selected day.
- A day marker, draggable and keyboard-steppable (arrow keys ±1 day, Page Up/Down ±30), shared by both panels.
- Readout table at the selected day: `m`, `P`, `π` (percent, 2 decimals), `realWage` (2 decimals), `L`, `mountWeight` (1 decimal), `m*`.

**Controls (values shown next to each).**
- `m0`: 500 to 10,000, step 100, default 2,000.
- Net inflow `n`: −40 to 200 gold per player-day, step 5, default 40.
- Stock sink `σ`: 0% to 3%, step 0.05%, default 0%.
- Velocity `V`: 0.01 to 0.2, step 0.01, default 0.05.
- Newcomer income `W`: 10 to 500, step 10, default 100.
- Mount price `L0`: 1,000 to 100,000, step 1,000, default 20,000.
- Toggle "Index the mount price" (default off).
- Presets: "No stock sink" (defaults above), "1% stock sink" (`σ = 1%`), "Indexed mount" (defaults with toggle on).
- **Opening state:** the page loads on the "1% stock sink" preset, day marker at 365. With `σ = 0` the three normalised lines nearly overlap, so the contrast is clearest when the student starts with the sink and then switches it off.

**Test values (must match the lecture's tables).**
- No-stock-sink preset (the defaults listed under Controls): day 1 `m = 2,040`, `P = 102`, `π = 2.00%`; day 30 `m = 3,200`, `P = 160`, `π = 1.27%`, realWage 0.63, mountWeight 6.3; day 60 `P = 220`, `π = 0.92%`; day 180 `m = 9,200`, `π = 0.44%`; day 365 `m = 16,600`, `P = 830`, `π = 0.24%`, realWage 0.12, mountWeight 1.2; day 730 `m = 31,200`, `P = 1,560`, mountWeight 0.6.
- `σ = 1%`: day 30 `m = 2,520.6`, `P = 126.03`; day 180 `m = 3,672.4`; day 365 `m = 3,949.0`, `P = 197.45`, realWage 0.51, mountWeight 5.1; `m* = 4,000`.
- Indexed mount on, defaults: mountWeight stays 10.0 on every day; `L(365) = 166,000`.
- First day with `π < 0.5%` under defaults: day 152.

**Accessibility and style.** Shared palette from `templates/interactive-tokens.css`. Lines distinguished by colour and dash pattern. A one-line text summary updates live, for example "Day 365: potions cost 830 gold. Prices rose 0.24% today. A newcomer's day buys 0.12 potions. The mount costs 1.2 average balances." Respect `prefers-reduced-motion` and `prefers-color-scheme`. No game art or logos.
