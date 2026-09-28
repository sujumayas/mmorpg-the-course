# GD102 · Week 07 — Internal economies: sources, drains and converters

**Why this matters:** Every game that hands out a resource has an economy, whether or not anyone designed it. If you only count what comes in and forget to ask how things leave, your players will find the answer for you, and it usually looks like prices that climb every week until new players cannot afford anything.

**You will be able to:**
- Classify every mechanic that touches a resource as a source, a drain, a converter or a trader, and say which stock it changes.
- Compute the equilibrium money stock of an economy with flat and proportional drains, and predict how long it takes to get there.
- Predict whether a change to a faucet will cause a one-time price rise or ongoing inflation, and explain the difference with numbers.
- Critique a shipped game's sinks by rewriting them in the same model.

**Before class:** Adams & Dormans, *Game Mechanics: Advanced Game Design* (2012), chapter 4 "Internal Economy" and chapter 9 "Building Economies". Meadows, *Thinking in Systems: A Primer* (2008), chapter 1 (the bathtub and dynamic equilibrium sections) and chapter 2 (the one-stock systems).

**Prerequisites from earlier courses:** GD101 [week 3](../../GD101-introduction-to-game-design/lectures/w03-resources-conflict-boundaries-outcome.md) (resources as a formal element). From this course, [week 2, stocks and flows](w02-stocks-and-flows.md) (the bathtub rule and flows that depend on the stock), [week 4, negative feedback loops](w04-negative-feedback-loops-rubber-banding.md), [week 5, Machinations diagrams I](w05-machinations-diagrams-i.md) (sources, drains, pools) and [week 6](w06-machinations-diagrams-ii-converters-traders-gates.md) (converters and traders). The decay formula in section 2 is the exponential from MA101 [week 4, exponentials and the XP curve](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w04-exponentials-and-the-xp-curve.md), run downhill.

**Interactive:** [Two towns, one patch](../examples/w07-town-economy.html). Keep it open during section 2.

---

## 1. What an internal economy is

In week 2 you drew stocks and flows. A **stock** is an amount of something that can be counted at a moment in time: gold in wallets, potions in bags, health in a health bar. A **flow** is a rate that changes a stock: gold per hour from monsters, potions per day drunk in dungeons.

Adams and Dormans call the whole web of stocks and flows in a game its **internal economy**. The word "economy" can mislead you. It does not have to involve money. Ammunition in a shooter is an internal economy: you pick it up (inflow), you fire it (outflow), and the stock in your magazine decides what you can do next. Mana in an MMO is an internal economy that runs inside a single fight. You will study that one in detail in MMO303 [week 7, healing throughput and mana economy](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w07-healing-throughput-and-mana-economy.md). Today we use money because money is where mistakes are most visible, and because every later economy course in this degree builds on it.

Adams and Dormans name four kinds of mechanic that act on resources. You met their Machinations symbols in weeks 5 and 6. Here they are as questions you can ask about any rule.

- **Source.** Does this rule create a resource from nothing? A monster that drops gold is a source. The gold did not exist before the kill. Economists who study online games call a money source a **faucet**.
- **Drain.** Does this rule destroy a resource? Paying an NPC blacksmith to repair your sword is a drain. The gold leaves the game. Money drains are called **sinks**.
- **Converter.** Does this rule turn one resource into another? A crafting recipe that turns three herbs into one potion is a converter. Herbs are drained, potions are created.
- **Trader.** Does this rule move a resource between players or stocks without creating or destroying it? A player-to-player trade is a trader. Total gold in the world does not change when you pay another player.

The last distinction is the one designers get wrong most often. A player market feels like the center of the economy, but by itself it creates and destroys nothing. It only moves gold around. Prices on that market are decided by what the sources, drains and converters do to the total stock. Keep that in mind, because the worked example turns on it.

### Why the total matters

Imagine a town where every player earns 100 gold a day from monsters and spends nothing. After a month, everyone has 3,000 gold more than they started with. Nothing in the world is more plentiful, so the potions crafters sell have not multiplied. What happens to the price of a potion?

Players with more gold are willing to pay more for the same potion, and crafters notice. Prices rise. That rise is **inflation**: a sustained increase in prices across the economy. It is not a moral failing of players. It is arithmetic. More money chasing the same goods buys less per coin.

Inflation hurts two groups most. New players arrive with little gold and find every player-made item priced for veterans. Players who saved gold find their savings buy less each week. Both groups leave. This is why the question "where does the money go?" deserves as much design time as "how much do we pay for this quest?"

## 2. Worked example: faucets and drains in a tiny town

### The hook: a game that taxes its own market

On 9 December 2021, Old School RuneScape started charging a 1% fee on items sold through the Grand Exchange, its central player market. On 29 May 2025 it doubled the fee to 2%. The fee is capped at 5 million coins per item, and a list of everyday goods (low-level food, basic tools, some teleports) is exempt. According to the OSRS Wiki, most of the coins collected are simply removed from the game, and a small part is used to buy certain items from players and delete them.

Players pay this fee on every taxed sale, forever. Why would a developer add a cost to trading, the most social activity in its economy, and then raise it? The OSRS Wiki's page on money sinks gives the stated reason in one phrase: sinks exist "to control inflation rates". The rest of this section shows why a fee on trades does that job better than almost any other kind of sink, using a town small enough to compute by hand.

### The model

Our town has `N = 100` players. Time moves in days. Every quantity is either a stock or a flow per day.

```
M(t+1) = M(t) + N × (F − D) − s × M(t)
s      = τ × v
P(t)   = v × M(t) / (N × q)
```

- `M` is the **money stock**: all gold held by all players.
- `F` is the **faucet**: gold each player earns per day from monsters and quests.
- `D` is the **flat drain**: gold each player pays per day to NPCs whatever their wealth (repairs, NPC potions, rent).
- `v` is the **velocity**: the fraction of the money stock spent on the player market each day. We use `v = 0.30`.
- `τ` (tau) is the **market cut**: the fraction of each sale the market deletes.
- `s = τ × v` is the **proportional drain rate**: the fraction of all gold that disappears through the cut each day.
- `q` is the number of potions each player crafts and sells per day. We use `q = 10`, so the town sells 1,000 potions a day.
- `P` is the **market price of a potion**. It is the gold spent on the market per day divided by the potions sold per day.

The price rule is the one bold assumption in the model. It says the market spends a fixed share of all gold, and that spending is shared across a fixed number of potions. Real markets are messier. But the core of it (prices track money per player divided by goods per player) is the standard starting point for game economies, and it is enough to see the effect.

Notice what the formula for `P` contains. `M / N` is **money per player**. Prices follow money per player, not total money. A town that doubles its population and its money stock at the same time sees no inflation.

### Two towns that look identical today

We build two towns with the same faucet, `F = 100` gold per player per day, and the same starting stock of 200,000 gold (2,000 per player).

- **Town A (flat drains only).** Players pay 100 gold a day in flat drains (repairs plus a daily rent). The market has no cut, so `τ = 0` and `s = 0`.
- **Town B (flat plus proportional).** Players pay 40 gold a day in flat drains. The market takes a 10% cut, so `s = 0.10 × 0.30 = 0.03`. Three percent of all gold disappears through trading each day.

Check that both towns are stable. In town A, each player earns 100 and pays 100, so `M` never moves. In town B, the town earns `100 × (100 − 40) = 6,000` a day net of flat drains, and the cut removes `0.03 × 200,000 = 6,000` a day. Inflow equals outflow. Both towns have a potion price of

```
P = 0.30 × 200,000 / (100 × 10) = 60 gold
```

Now make one change to both towns. A patch adds a richer hunting ground, and the faucet rises 10%, from 100 to 110 gold per player per day. Nothing else changes.

### Numbers you can check

Town A is easy. Each player now nets 10 gold a day, so the town gains 1,000 gold a day, every day.

Town B needs one step at a time. On day 1:

```
M(1) = 200,000 + 100 × (110 − 40) − 0.03 × 200,000
     = 200,000 + 7,000 − 6,000
     = 201,000
```

That is the same as town A. On day 1 the towns are indistinguishable. Keep stepping and they separate:

| Day | Town A money | Town A potion price | Town B money | Town B potion price |
|---|---|---|---|---|
| 0 | 200,000 | 60.0 | 200,000 | 60.0 |
| 1 | 201,000 | 60.3 | 201,000 | 60.3 |
| 10 | 210,000 | 63.0 | 208,753 | 62.6 |
| 30 | 230,000 | 69.0 | 219,966 | 66.0 |
| 100 | 300,000 | 90.0 | 231,748 | 69.5 |
| 365 | 565,000 | 169.5 | 233,333 | 70.0 |

Town A's price climbs by 0.3 gold every day and never stops. After a year a potion costs almost three times what it did at launch. Town B's price rises too, but it settles at 70 gold and stays there. The same 10% faucet change raised town B's price by 16.7% once, and then nothing more. Town A's price rose 182.5% in the same year and is still rising.

Open the interactive. The left chart shows both towns' money stock over a year. The right chart shows the potion price. Drag the faucet slider from 100 to 110. Town A's line tilts upward and keeps going off the top of the chart. Town B's line bends and flattens. Drag the faucet back to 100 and town A stops climbing but never comes back down, because nothing in town A removes the extra gold.

### Why town B settles: a drain that grows with the stock

Town B has a **proportional drain**. The cut removes a fixed share of the money stock, so the more gold there is, the more gold it removes. That is a negative feedback loop, exactly the shape you studied in [week 4](w04-negative-feedback-loops-rubber-banding.md), and the stock-dependent outflow from section 4 of [week 2](w02-stocks-and-flows.md). Too much money makes the drain bigger, which pulls the stock back down.

The stock stops changing when inflow equals outflow:

```
N × (F − D) = s × M*
M* = N × (F − D) / s
```

`M*` is the **equilibrium money stock**. For town B after the patch:

```
M* = 100 × (110 − 40) / 0.03 = 233,333 gold
P* = 0.30 × 233,333 / 1,000 = 70.0 gold
```

That matches the last row of the table. The approach to `M*` is exponential decay of the gap. Each day, 3% of the remaining gap closes:

```
M(t) = M* + (M(0) − M*) × (1 − s)^t
```

Check day 30: `233,333 − 33,333 × 0.97^30 = 233,333 − 33,333 × 0.401 = 219,966`. The gap halves every `ln 0.5 / ln 0.97 ≈ 22.8` days. After about three months the town has effectively arrived. This is the MA101 week 4 exponential with a growth factor below 1.

Town A has only flat drains. A flat drain removes the same gold whether the town is poor or rich. It cannot push back. The equilibrium formula has `s = 0` in the denominator, which is the algebra's way of saying there is no equilibrium unless `F = D` exactly. Any imbalance, in either direction, accumulates forever. Meadows calls this the bathtub: with the drain opening fixed, the water level only stays put if the tap matches it exactly.

This gives you the lecture's main rule.

> A faucet change in an economy with a proportional drain causes a one-time shift in the price level. The same change in an economy with only flat drains causes inflation that never ends.

Economists distinguish a higher **price level** (potions now cost 70 instead of 60) from ongoing **inflation** (potions cost more every week). Players can adapt to the first. The second grinds them down.

### Two more sliders worth moving

The interactive has two more controls. Try them before reading on.

**The market cut.** In town B with `F = 110`, set the cut to 5%. Then `s = 0.015`, `M* = 466,667` and the price settles at 140 gold. Set it to 20% and the price settles at 35. The cut sets the price level. Halving the cut doubles the equilibrium money stock. A designer can use the cut to aim prices at a target, which is exactly the lever the OSRS team pulled in 2025.

**The flat drain.** In town A, set the flat drain to 110 to match the new faucet. Inflation stops, but the price stays wherever it had reached. Now set it to 111. The money stock starts falling and never stops, because a flat drain has no floor. In a real game that means players slowly go broke, which is called **deflation**, and it is just as damaging. A flat-only economy has to be tuned exactly and retuned every time anything changes. A proportional drain tunes itself.

### Cross-game recognition

Proportional drains on trade are everywhere. The skill is to rewrite each one as `s = τ × v` and find what `τ` is.

**Old School RuneScape (2021 onward).** The Grand Exchange tax is `τ = 1%` from December 2021 and `τ = 2%` from May 2025, taken from the seller, capped at 5 million coins per item. Because most of the tax is deleted, it is a proportional sink of exactly our kind. Doubling `τ` halves `M*`, all else equal. The exemptions for cheap food and tools are a deliberate choice to keep the drain off new players, whose trades are mostly in those goods. On the faucet side, the OSRS Wiki lists coins dropped by monsters and High Level Alchemy (casting a spell that turns an item into coins) among the ways new coins enter the game.

**EVE Online (current era).** When a sell order fills on the market, the seller pays a sales tax to an NPC corporation, the Secure Commerce Commission. The base rate is 7.5%, reduced by the Accounting skill to 3.37% at skill level 5. Players who place orders also pay a broker's fee, 3% at base in NPC stations. EVE University's wiki confirms that this ISK leaves circulation. So EVE runs two proportional sinks on every market sale. On the faucet side, most NPC pirates carry bounties that the game pays out in ISK when they are destroyed. CCP publishes a Monthly Economic Report with charts of ISK sinks and faucets, the telemetry you will learn to read in MMO304.

**World of Warcraft (current era).** When an auction sells, the auction house keeps 5% of the winning bid. The seller also pays a deposit when listing, sized from the item's vendor price and the auction length, and gets it back only if the item sells. Rewritten: `τ = 5%` on completed sales, plus a small drain on failed listings that punishes overpricing.

Three games, three names (tax, sales tax plus broker's fee, cut plus deposit), one mechanism. Each is a drain that grows as the economy's trading grows.

### Eyes-open design judgment

Proportional drains are not free. Weigh these before you add one.

- **Strength: self-correction.** The economy finds its own equilibrium after every patch, so a faucet mistake costs you a price-level shift rather than a year of inflation.
- **Strength: it hits the rich harder.** A player who trades a lot pays the most. That is usually the player with the most gold, which is where the excess lives.
- **Cost: it taxes the social activity.** Every point of `τ` discourages trading. Push it too high and players trade outside the market (direct trades, which the cut does not see), and your sink drains nothing. EVE's 7.5% base rate is high, but it drops with a skill, which rewards dedicated traders instead of punishing them.
- **Cost: it only drains money that moves.** Gold hoarded in a bank never passes through the cut. If your richest players stop trading, a trade tax cannot touch their stock. That is one reason games also run flat and one-off sinks (expensive mounts, cosmetic vendors, housing).
- **Decide deliberately:** who pays. Exemptions for starter goods (as in OSRS) shift the drain onto veterans. A flat fee does the opposite and weighs most on the poor.

The general lesson is older than games. Meadows describes this structure as a stock with a balancing loop: the outflow depends on the stock, so the stock seeks a goal. If you want a stock to hold steady without constant retuning, give it a drain that depends on it.

## 3. Converters: the mechanics that hide sources and drains

Sources and drains are easy to spot when gold appears or disappears on screen. Converters are harder, because they turn one resource into another, and whether they act as a source or a drain depends on which stock you are watching.

### A converter can be a faucet in disguise

In Old School RuneScape, High Level Alchemy turns an item into a fixed number of coins. From the item's point of view it is a drain: the item is destroyed. From the money stock's point of view it is a faucet: new coins appear that no player paid. A designer who counts only "monster gold drops" as the faucet will underestimate how much money enters the game, because every monster drop that can be alchemized is also a coin drop one step removed.

The rule is: **track the resource, not the building.** For each converter, write down what it drains and what it creates. Then add each side to the ledger of the stock it touches.

### A converter can change prices without touching money

In our town, potions come from crafters. Suppose a crafting converter lets each player turn herbs into potions, and a patch makes the recipe twice as efficient. Now `q` doubles from 10 to 20 potions per player per day. The money stock does not move at all. But the price formula has `q` in the denominator:

```
P = 0.30 × 200,000 / (100 × 20) = 30 gold
```

The price halves. This is the other side of inflation. Prices depend on money per player divided by goods per player. A designer can fight rising prices by adding sinks (reduce the top) or by adding production (raise the bottom). The two feel very different to players. Sinks feel like costs. Production feels like abundance, but it also makes crafters' work worth less, and crafters are players too.

### Traders do not change the totals

A player-to-player trade moves gold from buyer to seller and a potion from seller to buyer. The total money stock and the total potion stock are unchanged. This is why "the market is broken" is almost never true in the literal sense. The market is a trader. It reports prices that the sources, drains and converters produced. When a designer adds a cut to the market, the market becomes a trader with a drain attached, and that attachment is what does the work.

## 4. Auditing an economy in five steps

When you meet a new game, or review your own design, run this audit. It turns the model above into a checklist.

1. **List the stocks.** Every resource players hold: currencies, materials, consumables, items. Do not forget stocks that hide in bank vaults and guild storage.
2. **List every source, drain and converter** for each stock. Include the ones that look like something else: vendor sales (a faucet), repair bills (a drain), crafting (a converter), item destruction on death (a drain).
3. **Classify each drain** as flat (a fixed amount per player or per action) or proportional (a share of wealth or of trade). Count at least one proportional drain per major currency. If there is none, you have built town A.
4. **Find the equilibrium.** With the numbers you have, compute `M* = N × (F − D) / s`. If `s` is zero, say so and state what will happen when `F` drifts.
5. **Divide by players.** Compute money per player at equilibrium. Then ask what happens to it if a large wave of new players arrives with no gold, or if half the population leaves.

MMO304 starts from this audit and adds the complications you have left out: many currencies, crafting chains, markets that set prices by supply and demand, and telemetry. See MMO304 [week 3](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w03-faucets-sinks-and-transformations.md) and [week 4](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w04-money-supply-per-capita-and-inflation.md).

## In-class activity (25 minutes)

Work in pairs with the interactive open. You are the economy designer for town B.

1. The content team wants to raise the monster faucet to 130 gold per day for a holiday event lasting 30 days, then return it to 110. Predict, before touching the sliders, the potion price at the end of the event and 60 days after it ends. Write your predictions down.
2. Run the event in the interactive using the "event" preset (faucet 130 for days 1 to 30, then 110). Record the price at day 30 and day 90. How close were you?
3. The community team says players hate the price spike. Propose one change to a drain that keeps the day-30 price under 75 gold. You may change `τ`, `D`, or both, for the duration of the event only. Test it.
4. Swap proposals with another pair. Find one group of players your partners' change hurts more than others (new players, traders, hoarders, crafters). Write one sentence explaining who and why.

Expected output: two predictions with the observed values, one drain change with its day-30 price, and one sentence of critique. With the default event, the price at day 30 is 78.0 gold, 73.2 at day 60 and 71.3 at day 90. Raising the cut to 12% for the event, or the flat drain to 55, keeps day 30 near 70.

## Common misconceptions

- **"The market sets prices, so a broken market causes inflation."** The market is a trader. It moves gold, it does not create it. Prices rise because sources outpace drains. Fixing the market's interface will not fix the money supply.
- **"Balance the faucet and the drain once and the economy is stable."** With only flat drains, it is stable only while nothing changes. Any later change to faucets, population or player behavior accumulates without limit. A proportional drain makes the balance self-correcting.
- **"Inflation means prices are high."** High prices are a price level. Inflation is prices that keep rising. Town B after the patch has higher prices and zero inflation.
- **"Crafting is neither a source nor a drain, so it doesn't affect the economy."** Crafting is a converter. It drains one stock and fills another, and a change to its rate moves prices as surely as a change to a faucet.

## Check yourself

1. Town C has 200 players, a faucet of 80 gold per player per day, flat drains of 50 gold per player per day, velocity `v = 0.25` and a market cut of 6%. Compute the proportional drain rate `s`, the equilibrium money stock `M*` and the equilibrium money per player.
2. In town B (`s = 0.03`, `N = 100`, flat drain 40), the faucet is 110 and the town sits at equilibrium. The team doubles the market cut to 20%. Compute the new equilibrium price. About how many days until the price is halfway to it?
3. A designer proposes removing the market cut and instead raising town B's flat drain by 60 gold per player per day, "because it removes the same amount of gold today". Use the model to explain what will happen the next time the faucet changes.
4. A new converter lets players melt unwanted potions into 20 gold each at an NPC. Is this a source or a drain for the money stock? For the potion stock? What happens to the potion price floor?

<details>
<summary>Answers</summary>

1. `s = 0.06 × 0.25 = 0.015`. `M* = 200 × (80 − 50) / 0.015 = 400,000`. Money per player is 2,000.
2. New `s = 0.20 × 0.30 = 0.06`. `M* = 100 × 70 / 0.06 = 116,667`, so `P* = 0.30 × 116,667 / 1,000 = 35` gold. The gap closes 6% per day, so it halves in `ln 0.5 / ln 0.94 ≈ 11.2` days.
3. Today both designs remove 6,000 gold a day, so nothing visible changes. But the flat drain cannot respond to the stock. The next faucet increase creates town A: the net surplus accumulates every day and prices rise without end. Any faucet decrease makes the money stock fall without end.
4. It is a source for money (20 new gold per potion) and a drain for potions. No player will sell a potion for less than 20 gold, because the NPC pays 20. It sets a price floor and also acts as a faucet whose size depends on how many surplus potions exist, which is the High Level Alchemy pattern.

</details>

## Lab hook

**Lab 07, town economy spreadsheet** ([labs/lab07.md](../labs/lab07.md)). You rebuild towns A and B in a spreadsheet, add a crafting converter and a population wave, and write a one-page recommendation for which sinks a small MMO should ship with. The lab is a direct input to the economy design assignment (30% of the course).

## Sources

- Old School RuneScape Wiki, "Grand Exchange" and "Grand Exchange item sink" (accessed September 2026): tax of 1% from 9 December 2021, raised to 2% on 29 May 2025, capped at 5 million coins per item, exempt item list, most taxed coins removed from the game with a small share used to buy and delete items.
- Old School RuneScape Wiki, "Money sink" (accessed September 2026): definition of sinks as a way to control inflation; coin sources including NPC coin drops and High Level Alchemy; examples of coin sinks (repairs, tolls, instance fees).
- EVE University Wiki, "Trading" (current rules, accessed September 2026): sales tax base 7.5%, reduced 11% per Accounting level to 3.37% at level 5; broker's fee base 3% in NPC stations; fees paid to the Secure Commerce Commission and removed from circulation.
- EVE University Wiki, "Ratting" (accessed September 2026): most NPC pirates carry bounties paid on destruction.
- CCP Games, "Monthly Economic Report, January 2024", eveonline.com: published sinks and faucets charts.
- Warcraft Wiki (warcraft.wiki.gg), "Auction House" (current retail rules, accessed September 2026): 5% cut of the winning bid; deposit of 15%, 30% or 60% of vendor sell price for 12, 24 or 48 hours, returned only when the item sells; faction auction houses merged per realm in patch 6.0.2.
- Adams, E. & Dormans, J. (2012). *Game Mechanics: Advanced Game Design*. New Riders. Chapter 4 (sources, drains, converters, traders) and chapter 9.
- Meadows, D. H. (2008). *Thinking in Systems: A Primer*. Chelsea Green. Chapters 1-2 (stocks, flows, dynamic equilibrium, balancing loops).

## Interactive spec: examples/w07-town-economy.html

**The one insight.** Move the faucet slider once. Town A (flat drains only) inflates forever. Town B (flat plus a proportional market cut) shifts to a new price and stops. On day 1 they are identical; the difference only shows over weeks.

**Layout.** Two linked charts side by side on desktop, stacked on mobile. Controls panel below (mobile) or to the right (desktop). A readout table under the charts.

**Left chart, "Money per player".** x = day 0 to horizon (default 365). y = `M(t) / N`. Two lines: town A (label "Flat drains only") and town B (label "Flat + market cut"). Dashed horizontal line at town B's equilibrium `M* / N`, labelled "Town B settles here". No equilibrium line for town A; when `F ≠ D_A`, show the text "Town A has no resting point" in the chart corner.

**Right chart, "Potion price".** x = day, y = `P(t)` for both towns, same colors. Horizontal guide at the starting price. A vertical cursor that follows the pointer or keyboard focus and shows both prices at that day in a tooltip.

**Controls.**
- Faucet `F` (shared by both towns): slider 80 to 140, step 1, default 100.
- Town A flat drain `D_A`: slider 60 to 140, step 1, default 100.
- Town B flat drain `D_B`: slider 0 to 100, step 1, default 40.
- Town B market cut `τ`: slider 0% to 30%, step 0.5%, default 10%.
- Velocity `v`: slider 0.05 to 0.60, step 0.01, default 0.30 (applies to both towns' prices and to town B's drain).
- Potions per player per day `q`: slider 5 to 40, step 1, default 10.
- Players `N`: fixed at 100 by default; an "Advanced" disclosure reveals a population slider 50 to 400 and a checkbox "New players join with 0 gold" (when `N` changes mid-run on the chosen day, add or remove players with zero gold for joiners; departing players take average wealth).
- Horizon: 90, 180, 365 days (segmented control).
- Change day: slider 0 to 60, default 0. The faucet slider value applies from this day on; before it the faucet is 100. This lets students see the "identical on day 1" moment.
- Presets: "Baseline" (all defaults), "Patch +10%" (F = 110), "Holiday event" (F = 130 for days 1-30, then 110; show a shaded band on both charts for the event window), "Deflation" (town A `D_A = 111` with F = 110).

**Formulas (step once per day, starting from `M(0) = 200,000`, `N = 100`).**
- Town A: `M(t+1) = M(t) + N × (F(t) − D_A)`. Clamp at 0 and show a "Town A is broke" badge if it hits 0.
- Town B: `M(t+1) = M(t) + N × (F(t) − D_B) − τ × v × M(t)`.
- Price: `P(t) = v × M(t) / (N × q)`.
- Equilibrium for B: `M* = N × (F − D_B) / (τ × v)`; if `τ = 0` show "no equilibrium".
- Half-life of B's gap: `ln 0.5 / ln (1 − τ v)` days.

**Readouts (copyable, in a table).** For each town: price at day 1, 10, 30, 100, 365; money per player at the same days; "30-day inflation" = `P(t)/P(t−30) − 1` at the cursor day. For town B also `M*`, `P*` and half-life in days.

**Test values (must match).**
- Defaults: both towns flat at `M = 200,000`, `P = 60.0` for all days.
- Patch +10% (F = 110 from day 0): Town A day 1 `201,000 / 60.3`, day 10 `210,000 / 63.0`, day 30 `230,000 / 69.0`, day 100 `300,000 / 90.0`, day 365 `565,000 / 169.5`. Town B day 1 `201,000 / 60.3`, day 10 `208,753 / 62.63`, day 30 `219,966 / 65.99`, day 100 `231,748 / 69.52`, day 365 `233,333 / 70.00`. `M* = 233,333`, half-life 22.8 days.
- F = 110, τ = 5%: `M* = 466,667`, `P* = 140`. τ = 20%: `M* = 116,667`, `P* = 35`.
- F = 110, q = 20, day 0: price 30.0 in both towns.
- Holiday event: town B price 77.97 at day 30, 73.20 at day 60, 71.28 at day 90, 70.08 at day 180. With τ = 12% during the event only, day 30 is 70.01. With `D_B = 55` during the event only, day 30 is 68.98.
- Event controls: add "event τ" and "event D_B" sliders, visible only with the Holiday event preset, that apply during days 1-30.

**Accessibility.** Every slider has a visible label and live numeric value, and works with arrow keys. The charts have a text summary in an `aria-live` region ("Town A price rising 0.3 gold per day; town B settles at 70.0 gold"). No animation when `prefers-reduced-motion` is set. Colors from `templates/interactive-tokens.css`, with the two towns also distinguished by line style (solid vs dashed) so the view works without color.
