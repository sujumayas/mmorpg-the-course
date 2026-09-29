# MMO401 · Week 07 — Taxes and Fees as Policy

**Why this matters:** A market tax is the one sink that scales with how much your players trade, and it is the lever live teams pull most often. Set it by instinct and you can double the rate, halve the market, and remove less money than before. This week you learn to predict what a rate change does to volume, prices and the sink before you ship it.

**You will be able to:**
- Compute the buyer price, seller price, volume, sink revenue and deadweight loss of a sales tax in a linear market, and read the same numbers off an order book.
- Explain tax incidence and predict which side of a market ends up paying a fee from the slopes of supply and demand.
- Model leakage to an untaxed channel and find the tax rate that maximizes the sink once players can trade around the market.
- Compare sale taxes, listing fees and broker fees, and design a fee schedule for a stated policy goal.

**Before class:** Lehdonvirta & Castronova, *Virtual Economies: Design and Analysis* (MIT Press, 2014), the chapters 9-12 block, reading for how the authors treat fees and taxes as policy instruments (about 30 pages). Reread the fee section of MMO304 week 10. Skim the sinks and faucets chart in any 2025 CCP Monthly Economic Report for EVE Online.

**Prerequisites from earlier courses:** [MMO304 week 10, market design](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w10-market-design-auction-houses-vendors-barter.md) (fee schedules of four games, the break-even rule `s > b / (1 − f)`, order books and spreads). [MMO304 week 3, faucets, sinks and transformations](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w03-faucets-sinks-and-transformations.md) (a trade tax as a stock sink `τ × v × M`). [MMO304 week 4, money supply per capita](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w04-money-supply-per-capita-and-inflation.md) (proportional sinks set a ceiling). [MMO304 week 6, supply and demand in auction houses](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w06-supply-demand-and-equilibrium-in-auction-houses.md) (linear supply and demand, equilibrium). [MA101 week 6, rational functions](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w06-rational-functions-and-asymptotes.md). This course: [week 5, order books and spreads](w05-market-microstructure-order-books-and-spreads.md), [week 4, monetary policy tools](w04-monetary-policy-tools-in-games.md) (the sink `σ = τ × v`), and [week 2, agent-based modeling](w02-agent-based-modeling-i.md).

**Interactive:** [Tax order book](../examples/w07-tax-order-book.html). Drag the tax rate and bypass cost to see the order book and the sink curve move together.

---

## 1. A tax is two prices

In MMO304 you treated a market tax as a sink. Money goes in, a share disappears. That view is right about the money supply and incomplete about everything else. This week you look at what a tax does to the market it sits on.

Start with one sale. A buyer pays 100 gold. With a 5% cut, the seller receives 95. The 5 gold is deleted. There are now two prices for the same trade:

- The **buyer price** `P_b` is what the buyer hands over.
- The **seller price** `P_s` is what the seller keeps.

For a sales tax at rate `t` taken from the seller, `P_s = (1 − t) × P_b`. The gap between the two prices is called the **tax wedge**. Economists use the word because the tax is driven between buyer and seller like a wedge into a log. Every trade whose value to the buyer is smaller than the seller's cost plus the wedge no longer happens.

That last sentence is the whole problem. A tax collects money from the trades that survive it and destroys the trades that don't. The first part is your sink. The second part is lost play. Think of gatherers who stop gathering because the price they keep is too low, crafters who skip a batch, buyers who make do. Economists call the value of the destroyed trades **deadweight loss**. Nobody receives it. It just stops existing.

Week 4 wrote a trade tax's sink as `σ = τ × v` and warned that `v` responds to `τ`. This week's `t` is that `τ`, and the rest of the lecture measures how `v` responds.

The designer's question is never "is a tax good". It is "how much sink do I get per unit of trade I destroy, and at what rate does that ratio turn against me".

## 2. Worked example: tuning a transaction tax on an order book

### The hook

On 12 March 2025, in release 22.02, CCP raised the base sales tax on EVE Online's regional markets from 4% to 7.5%. Training the Accounting skill to level V cuts it by 55%, to about 3.4%. An NPC corporation collects the tax, so the ISK leaves the player economy. It is one of the sinks CCP reports every month.

Ask the obvious question. The rate nearly doubled. Did the ISK removed by the tax nearly double? A player's first guess is yes, because the rate is a multiplier. A designer's answer is "it depends on what the volume did", and this worked example gives you the tool to say by how much. We won't claim to know EVE's actual result. The model tells you what to look for in the next economic report.

### The model

Take one commodity on one server. Each day 100 buyers arrive, each wanting one unit, with limit prices spread evenly from 100 gold down to 1. Each day 100 sellers arrive, each with one unit, with reservation prices (the lowest price they will accept) spread evenly from 1 to 100. On an order book the buyers become **bids** and the sellers become **asks**.

With no tax, the bids sorted high to low and the asks sorted low to high cross somewhere in the middle. In the continuous version:

```
demand:   Q = 100 − P_b          (buyers willing to pay at least P_b)
supply:   Q = P_s                (sellers willing to sell at P_s or more)
tax:      P_s = (1 − t) × P_b    (the seller pays rate t on the sale price)
```

Solve by setting demand equal to supply:

```
100 − P_b = (1 − t) × P_b
P_b = 100 / (2 − t)
Q   = 100 × (1 − t) / (2 − t)
R   = t × P_b × Q = 10,000 × t × (1 − t) / (2 − t)²
```

- `t` is the tax rate on the sale price.
- `P_b` and `P_s` are the buyer and seller prices.
- `Q` is the number of units traded per day.
- `R` is the sink, the gold deleted per day.

Deadweight loss needs one more line. The total value a trade creates is the buyer's limit price minus the seller's reservation price. Summing over the `Q` trades that happen gives `100Q − Q²`. With no tax, `Q = 50` and the market creates 2,500 gold of value a day. So:

```
DWL = 2,500 − (100 × Q − Q²)
```

You met `P_b = 100 / (2 − t)` in MA101 week 6 as a rational function. It rises slowly at first and then steeply as `t` approaches 1.

### Numbers you can check

| Tax `t` | Buyer price `P_b` | Seller keeps `P_s` | Volume `Q` (continuous) | Trades on the discrete book | Sink `R` per day | Deadweight loss |
|---|---|---|---|---|---|---|
| 0% | 50.00 | 50.00 | 50.00 | 50 | 0 | 0 |
| 2% | 50.51 | 49.49 | 49.49 | 49 | 50.0 | 0.3 |
| 5% | 51.28 | 48.72 | 48.72 | 49 | 124.9 | 1.6 |
| 10% | 52.63 | 47.37 | 47.37 | 47 | 249.3 | 6.9 |
| 20% | 55.56 | 44.44 | 44.44 | 44 | 493.8 | 30.9 |
| 50% | 66.67 | 33.33 | 33.33 | 33 | 1,111.1 | 277.8 |
| 66.7% | 75.00 | 25.00 | 25.00 | 25 | 1,250.0 | 625.0 |

Check one row by hand. At `t = 0.10`, `P_b = 100 / 1.9 = 52.63`, `P_s = 0.9 × 52.63 = 47.37`, and `Q = 100 − 52.63 = 47.37`. The sink is `0.1 × 52.63 × 47.37 = 249.3`. The discrete book column counts bid-ask pairs where the `k`-th highest bid `101 − k` is at least the `k`-th lowest ask grossed up for tax, `k / (1 − t)`. At 10% that holds up to `k = 47`.

Read the table two ways. Down the sink column, revenue climbs almost in proportion to the rate at first. Down the deadweight column, the loss grows much faster than the rate. It goes roughly with `t²`. At 5%, you delete 125 gold a day and destroy 1.6 gold of trade value. That is a very cheap sink. At 50% you delete 1,111 and destroy 278. Revenue peaks at `t = 2/3`, where it is 1,250, but by then a quarter of the market's value is gone. (Setting the derivative of `t(1 − t) / (2 − t)²` to zero gives `2 − 3t = 0`.)

So far this is a textbook tax. If you stopped here you would conclude that a game can run a 20% or 30% market tax, collect a large sink and lose little. That conclusion is wrong for most MMOs, and the reason is the part of the model that textbooks leave out.

### The part games add: the untaxed channel

Real governments tax almost every channel a sale can take. Game designers usually don't. Most MMOs give players at least one way to trade that skips the market cut: a trade window, the mail, a contract or a guild bank. Using that channel has a cost. You have to find a partner, agree on a price, meet, and trust them. Call that cost `e`, in gold per trade.

A trader bypasses the market when the tax on the trade is larger than their bypass cost, `t × P_b > e`. Players differ. Someone in a large guild with a trade channel has `e` near zero. A new solo player has a high `e`. Assume bypass costs are spread evenly from 0 to a maximum `E`. Then the share of trades that leave the market is

```
b = min(1, t × P_b / E)
```

and the market keeps `Q_m = Q × (1 − b)` trades. The sink becomes

```
R_m = t × P_b × Q × (1 − b)
```

This is a first-order model. It keeps the price and the total number of trades from the wedge model and asks only which channel each trade uses. Your agent-based model in the lab relaxes that.

Take `E = 20` gold, a plausible cost for arranging a face-to-face trade on a 50-gold item.

| Tax `t` | Tax per trade `t × P_b` | Share bypassing `b` | Trades on the market `Q_m` | Sink with bypass `R_m` | Sink without bypass `R` |
|---|---|---|---|---|---|
| 0% | 0.00 | 0% | 50.0 | 0 | 0 |
| 2% | 1.01 | 5.1% | 47.0 | 47.5 | 50.0 |
| 5% | 2.56 | 12.8% | 42.5 | 108.9 | 124.9 |
| 10% | 5.26 | 26.3% | 34.9 | 183.7 | 249.3 |
| 15% | 8.11 | 40.5% | 27.3 | 221.5 | 372.5 |
| 20% | 11.11 | 55.6% | 19.8 | 219.5 | 493.8 |
| 30% | 17.65 | 88.2% | 4.8 | 85.5 | 726.6 |

The peak has moved. Without bypass, revenue keeps rising until 67%. With bypass at `E = 20`, it peaks near **17%**, at about 226 gold a day, and then falls. At 30%, the market has almost emptied. The trades haven't vanished. Of the 41 trades a day that the price still supports, about 36 happen off the book, where you can't see them, can't tax them, and can't protect the players doing them.

That is the volume against sink trade-off in one table. Below the peak, each point of tax buys more sink and pushes some trade off the market. Above the peak, each point of tax loses sink *and* market volume. No designer should ever set a rate above the peak, and you should usually stay well below it, because the market's other jobs (price discovery, safety, telemetry) depend on its volume.

### Where the peak sits

The peak depends on `E`. Rerun the search for other bypass costs:

| Maximum bypass cost `E` | Revenue-maximizing tax | Sink at the peak |
|---|---|---|
| 10 (trading around the market is easy) | 9.3% | 118.8 |
| 20 | 17.3% | 225.7 |
| 40 | 29.9% | 406.1 |
| 100 (trading around the market is hard) | 50% | 740.7 |

This is the design insight worth remembering. **How high you can tax the market is set by how hard you make it to trade around the market.** The rate and the bypass rules are one decision, not two.

### The visual

Open the interactive. The left panel is the order book for one day. Bids form a staircase going down, asks a staircase going up. A dashed ask staircase shows each seller's reservation price grossed up for tax, `c / (1 − t)`. The trades are the shaded steps where the bid staircase is above the dashed one. Drag the tax slider and watch the dashed staircase lift and the crossing slide left.

The right panel plots sink revenue against the tax rate, one curve without bypass and one with it, plus market volume. A marker shows your current rate. On the left, a 20% tax looks mild. Only six trades fail to cross. On the right, with bypass switched on, 20% sits just past the top of the hump, and more than half the book is gone. The left view shows the textbook. The right view shows your game.

### Cross-game recognition

Every market cut you meet can be written as a wedge `t` on the seller plus some rule about orders and bypass. Rewrite each one into that form.

**EVE Online (current, since release 22.02 on 12 March 2025).** Sales tax `s` is 7.5% at base, reduced 11% per level of Accounting, so `s = 7.5% × (1 − 0.11 × level)`, which is 3.375% at level V. A seller who places a sell order at an NPC station also pays a broker's fee of 3% at base, reduced by Broker Relations and standings. So `t = s + f` for a seller who lists, and `t = s` for one who sells straight into a standing buy order. In a player-owned Upwell structure the broker's fee is a 0.5% surcharge to the NPC commission plus a rate the owner sets, which can be 0%. That owner's share is paid to a player, so it is a **transfer** between players, not a sink. Same fee on the screen, different macro effect.

**Old School RuneScape Grand Exchange (2% since 29 May 2025, 1% from 9 December 2021).** `t = 0.02`, rounded down to whole coins, capped at 5 million coins per item, with a list of exempt items. The tax is a per-unit wedge `min(0.02 × P, 5,000,000)`. Most of it is deleted, and part funds an item sink that buys selected items and deletes them. The trade window between players is a separate channel. Old School RuneScape's Code of Conduct bans scamming, which lowers `e` for honest trades by reducing the risk of meeting a stranger.

**Guild Wars 2 Trading Post (current).** A 5% listing fee is taken when the item is listed and is not refunded. A 10% exchange fee is taken from the sale. For an item that sells, `t = 0.15`. For one that never sells, the seller has still paid 5%. The market is shared by all worlds in North America and Europe. With `t = 15%`, the wedge model predicts a larger share of trades that don't happen at all than in a 2% market, and the bypass model predicts strong pressure to trade outside the post wherever that is possible.

**World of Warcraft (current retail).** The auction house keeps 5% of the winning bid, so `t = 0.05`. The seller also pays a deposit based on the item's vendor price and the auction length, lost if the item doesn't sell. Face-to-face trades pay no cut. That makes WoW's rule the cleanest case of the bypass model, with a low `t` on the market and an untaxed channel beside it.

Four games, four presentations. In each, ask the same three questions. What is `t` for a trade that happens? What does a listing cost if the trade doesn't happen? How cheap is it to trade around the market?

### Eyes-open design judgment

- **Low rates are cheap sinks.** Deadweight loss grows with the square of the rate. Between 2% and 5%, a tax removes a lot of money per unit of lost trade. This is why so many games land there.
- **The revenue peak is lower than you think, and you should stay below it anyway.** With an easy bypass the peak can be under 10%. Near the peak, volume is already falling fast, and a market with thin volume has wide spreads and poor price discovery.
- **Taxing the market taxes safety.** Trades pushed into the trade window or the mail lose the market's escrow. That is where scams live, which is next week's topic. A high tax is an indirect subsidy to scammers.
- **Decide the bypass rules deliberately.** You can raise `e` (remove the trade window, add a mail fee, bind items on trade) to protect a higher rate. Each of those costs players something too. Guild Wars 2 at 15% and Old School RuneScape at 2% are two ends of that choice.
- **Watch who receives the fee.** A fee paid to an NPC is a sink. A fee paid to a structure owner or a guild is a transfer that concentrates wealth. Both are policy, but they do different things to the money supply.

## 3. Who really pays: tax incidence

The legal rule says who hands over the tax. It does not decide who bears it. Look back at the 20% row. The buyer price rose from 50 to 55.56 and the seller price fell from 50 to 44.44. Buyers and sellers each lost 5.56 per unit, even though the game took the tax only from the seller. Charge the same wedge to the buyer instead and the final prices are the same. **Tax incidence** is the share of the wedge each side ends up bearing.

For a per-unit tax `T` in a linear market with demand `Q = a − b × P` and supply `Q = c + d × P`, the buyer's share is `d / (b + d)` and the seller's share is `b / (b + d)`. The side that is less able to walk away pays more.

Work it with `T = 10` and the same demand, `Q = 100 − P`:

| Supply | Who is it | Buyer price | Seller keeps | Volume | Buyers bear | Sellers bear |
|---|---|---|---|---|---|---|
| `Q = P` | Balanced market | 55.0 | 45.0 | 45.0 | 5.0 | 5.0 |
| `Q = 3P − 100` | Sellers with good alternatives (crafters who can switch recipes) | 57.5 | 47.5 | 42.5 | 7.5 | 2.5 |
| `Q = 0.25P + 37.5` | Sellers who farm anyway (gatherers, bots, drops from content players run for other reasons) | 52.0 | 42.0 | 48.0 | 2.0 | 8.0 |

Check the last row. `100 − P = 0.25 × (P − 10) + 37.5` gives `1.25P = 65`, so `P = 52`. Sellers keep 42 and bear 8 of the 10.

This matters for games because a lot of supply is inelastic. Materials that drop from raids arrive whether or not the price is good, so the people selling them pay most of any tax. If your goal is to tax rich buyers of luxury goods, a flat sales cut on raid materials does the opposite. It lands on the players farming them.

## 4. Taxing orders instead of trades

A sale tax charges trades that happen. A listing fee charges orders whether or not they fill. Those are different instruments, and they target different behavior.

**Sale tax.** Charged only on success. It widens the gap between buyer and seller price and removes marginal trades. It does not care how many times you relist.

**Listing fee or deposit.** Charged when an order is placed, or kept when it fails. It taxes *attempts*. Guild Wars 2's 5% listing fee and World of Warcraft's forfeited deposit are this kind. A player who lists at an absurd price and relists every hour pays each time. So listing fees discourage speculative listings, undercutting wars and the practice of listing everything at silly prices to see what sticks.

**Broker fee on both sides.** EVE charges its broker's fee on placed orders, buy or sell. That hits **market makers**, the players who post both a buy order and a sell order and earn the spread between them (EVE players call this station trading; week 5 covers the mechanics). A market maker who buys at bid `B` and sells at ask `A`, paying broker fee `f` on both orders and sales tax `s` on the sale, profits only if

```
A × (1 − f − s) > B × (1 + f)
A / B > (1 + f) / (1 − f − s)
```

| Fee schedule | Minimum profitable spread `A/B − 1` |
|---|---|
| EVE, base skills (`f` = 3%, `s` = 7.5%) | 15.1% |
| EVE, Broker Relations V and Accounting V (`f` = 1.5%, `s` = 3.375%) | 6.7% |
| EVE, base skills, sales tax before 12 March 2025 (`f` = 3%, `s` = 4%) | 10.8% |
| Guild Wars 2 (no buy-side fee, 15% on sell side) | 17.6% |
| Old School RuneScape (2%, no buy-side fee) | 2.0% |

Fees set a floor under the spread. No market maker will quote tighter than the floor, so the posted spread in a thin market settles at or above it. The 2025 EVE change moved the base-skill floor from about 11% to about 15%. The model predicts wider spreads for new traders and more of the market-making business going to fully skilled characters, because their floor sits at 6.7%. Whether you want that is a policy question. Skill-reduced fees are a reward for investing in a trading career. They are also a moat that protects veterans from newcomers.

## 5. Designing a fee schedule from a goal

Start from the goal, then pick the instrument.

| Goal | Instrument | Why |
|---|---|---|
| Remove money in proportion to trade | Low sale tax, 2% to 5% | Cheap in deadweight loss, scales with activity |
| Stop undercutting wars and listing spam | Listing fee or deposit forfeited on expiry | Taxes attempts, not success |
| Remove items, not only money | Tax revenue spent on an item sink (Old School RuneScape) | Holds up prices of chosen goods |
| Reward trader specialization | Skill-reduced fees (EVE) | Veterans quote tighter spreads |
| Keep rich trades inside the market | A per-item cap (Old School RuneScape's 5 million coins) | Caps `t × P` so bypass never pays for expensive items |
| Let players build market infrastructure | Owner-set fees paid to players (EVE structures) | Turns a sink into income for an institution |

The cap deserves one more sentence, because it is the bypass model at work. At 2%, the tax on a 250-million-coin item is exactly 5 million. Above that, the tax stops growing, so `t × P` stays below any large player's bypass cost and the richest trades stay on the market where they are visible.

## In-class activity (25 minutes)

Groups of three. Your game has a single commodity market with demand `Q = 100 − P` and supply `Q = P`, and a trade window with bypass cost spread evenly up to `E = 20`. The monetary team (week 4) says the economy needs a sink of 200 gold a day from this market.

1. Using the tables, find the lowest tax that reaches 200 a day with bypass. Report the market volume at that rate.
2. Propose one change to the bypass channel that would let you reach 200 a day at a 10% tax. State the new `E` you need. (Hint: find `E` such that `R_m(0.10) = 200`.)
3. Name the player group that pays for your change and say how they will react.
4. Swap with another group. Critique their answer to step 3.

Expected output: a rate, a volume, a proposed `E` with its number, and one paragraph on who pays.

## Common misconceptions

- **"Doubling the rate doubles the sink."** Only if volume holds. Volume falls with the rate, and falls faster when players can trade around the market. Past the peak, a higher rate collects less.
- **"The seller pays the sales tax."** The seller hands it over. Who bears it depends on who can walk away. Gatherers of drops that arrive anyway bear most of it.
- **"A listing fee is just a smaller sales tax."** It taxes a different thing. It punishes relisting and speculative orders, and it keeps working when nothing sells.
- **"Trades that leave the market are gone."** They moved to a channel with no escrow, no price data and no tax. They are still there, and they now carry scam risk.

## Check yourself

1. In the wedge model with `E` very large (no bypass), what are `P_b`, `P_s`, `Q` and `R` at `t = 25%`?
2. With `E = 20`, what share of trades bypasses the market at `t = 25%`? What is `R_m`?
3. An EVE trader has Broker Relations IV (`f` = 1.8%) and Accounting III (`s` = 7.5% × 0.67). What minimum spread do they need?
4. Supply of a raid material is `Q = 0.25P + 37.5` and demand is `Q = 100 − P`. The designer adds a per-unit tax of 20. What do buyers and sellers each bear?
5. A designer wants to raise a 5% auction house cut to 12% and asks you to estimate the sink change. What two numbers do you need from telemetry before you answer?

<details>
<summary>Answers</summary>

1. `P_b = 100 / 1.75 = 57.14`, `P_s = 0.75 × 57.14 = 42.86`, `Q = 42.86`, `R = 0.25 × 57.14 × 42.86 ≈ 612.2`.
2. Tax per trade `0.25 × 57.14 = 14.29`, so `b = 14.29 / 20 = 71.4%`. `Q_m = 42.86 × 0.286 = 12.24` and `R_m = 14.29 × 12.24 ≈ 174.9`. That is below the 17% peak and the rate is past it.
3. `s = 7.5% × (1 − 0.33) = 5.025%`. Minimum spread `(1.018) / (1 − 0.018 − 0.05025) − 1 = 1.018 / 0.93175 − 1 ≈ 9.3%`.
4. Buyer share `d / (b + d) = 0.25 / 1.25 = 20%`, so buyers bear 4 and sellers bear 16. Check: `100 − P = 0.25(P − 20) + 37.5` gives `P = 54`, sellers keep 34.
5. How volume responds to the price (the slopes of supply and demand, or a past rate change) and how much trade already goes through untaxed channels (a proxy for `E`, such as trade-window and mail volume). Without them you can't tell which side of the peak 12% lands on.

</details>

## Lab / assignment hook

[Lab 07, tuning a transaction tax on an order-book simulation](../labs/lab07.md). You will extend a Python agent-based order book with a bypass channel, sweep the tax rate, find the revenue peak for three bypass costs, and write a one-page recommendation. It counts toward the ABM labs (40%).

## Sources

- EVE University Wiki, "Trading" (checked September 2026, describing version 22.02 onward). Sales tax 7.5% base since 12 March 2025, formula `7.5% × (1 − 11% × Accounting level)`, 3.37% at Accounting V; broker's fee 3% base reduced 0.3 points per Broker Relations level and by standings; Upwell structure broker fee is a 0.5% commission surcharge plus an owner-set rate with a 0% minimum; sales tax paid to the NPC Secure Commerce Commission; regional markets. The earlier 4% base rate is from MMO304 week 4's citation of the same page.
- Old School RuneScape Wiki, "Grand Exchange" (current). Tax 1% from 9 December 2021, 2% from 29 May 2025, capped at 5 million coins per item, rounded down, exempt list, most revenue removed and part used to buy and delete items.
- Old School RuneScape Wiki, "Scams". Rule 2 of the Code of Conduct prohibits scamming; trade window guidance.
- Guild Wars 2 Wiki, "Trading Post" (current). 5% non-refundable listing fee, 10% exchange fee on sale, shared by all NA and EU worlds.
- Warcraft Wiki, "Auction House" (current retail). 5% cut of the winning bid, deposit by vendor price and duration, kept if the item does not sell.
- Lehdonvirta, V. & Castronova, E. (2014). *Virtual Economies: Design and Analysis*. MIT Press. Chapters 9-12: 9 "Institutions and Nonmarket Allocation", 10 "Money", 11 "Macroeconomic Design", 12 "Macroeconomic Management" (titles and order from the MIT Press chapter DOIs 10.7551/mitpress/9525.003.0010 to .0013 on Crossref, checked September 2026).
- Tax incidence and deadweight loss in linear markets follow any intermediate microeconomics text, for example Varian, H. *Intermediate Microeconomics*, the chapter on taxes in equilibrium.

## Interactive spec: examples/w07-tax-order-book.html

**The one insight:** on the order book a moderate tax looks harmless because only a few trades fail to cross, but once players can trade around the market the sink peaks at a low rate and falls after it. The rate you can charge is set by how hard bypass is.

**Layout.** Two linked panels, side by side on desktop, stacked on mobile (order book first).

- Left panel, "Today's order book": 100 bids at limit prices `101 − k` for `k = 1..100`, drawn as a descending staircase, and 100 asks at reservation prices `k`, drawn as an ascending staircase. A dashed ascending staircase shows grossed-up asks `k / (1 − t)`. Shade the steps where `101 − k ≥ k / (1 − t)` (trades that happen). When bypass is on, shade the last `round(Q_book × b)` of those trades in a second, hatched fill labelled "traded off-market". Print trades on book, trades off-market and trades lost to the tax.
- Right panel, "Sink and volume against tax rate": x-axis tax 0% to 80%. Plot `R(t)` (no bypass, solid), `R_m(t)` (with bypass, solid, second colour), and market volume `Q_m(t)` on a secondary axis (dashed). Vertical marker at the current `t`. Mark the peak of `R_m` with a dot and label its rate and value.

**Formulas** (continuous, used for the right panel and the readout):

```
P_b = 100 / (2 − t)
P_s = (1 − t) × P_b
Q   = 100 × (1 − t) / (2 − t)
R   = t × P_b × Q
DWL = 2500 − (100 × Q − Q²)
b   = min(1, t × P_b / E)      (b = 0 when bypass is off)
Q_m = Q × (1 − b)
R_m = t × P_b × Q_m
```

Discrete book trades: `k* = count of k in 1..100 with 101 − k ≥ k / (1 − t)`.

**Controls.**

- Tax rate `t`: slider 0% to 80%, step 0.5%, default 5%.
- Bypass toggle, default on.
- Maximum bypass cost `E`: slider 1 to 100 gold, default 20. Disabled when bypass is off.
- Preset buttons: "Old School RuneScape 2%", "World of Warcraft 5%", "EVE base seller who lists 10.5%", "Guild Wars 2 15%". Presets set `t` only and leave `E` alone.

**Readout table** (copyable): `t`, `P_b`, `P_s`, `Q`, discrete `k*`, `b`, `Q_m`, `R`, `R_m`, `DWL`, and the current revenue-maximizing rate for `E` (found by scanning `t` in steps of 0.001).

**Test values** (must match, rounded as shown):

- `t` = 10%, `E` = 20: `P_b` 52.63, `P_s` 47.37, `Q` 47.37, `k*` 47, `b` 26.3%, `Q_m` 34.90, `R` 249.3, `R_m` 183.7, `DWL` 6.9.
- `t` = 20%, `E` = 20: `P_b` 55.56, `Q` 44.44, `k*` 44, `b` 55.6%, `Q_m` 19.75, `R` 493.8, `R_m` 219.5, `DWL` 30.9.
- `t` = 66.7% bypass off: `R` 1,250.0, `Q` 25.00, `k*` 25.
- Peak of `R_m`: `E` = 10 at 9.3% (118.8); `E` = 20 at 17.3% (225.7); `E` = 40 at 29.9% (406.1); `E` = 100 at 50.0% (740.7).

**Accessibility.** Sliders and toggles keyboard operable with visible focus. Distinguish curves by line style and direct labels, not colour alone. Respect `prefers-reduced-motion` by disabling staircase transitions. No game logos or art; games are named in preset labels only.
