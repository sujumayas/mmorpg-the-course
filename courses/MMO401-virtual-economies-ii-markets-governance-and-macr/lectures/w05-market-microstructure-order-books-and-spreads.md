# MMO401 · Week 05 — Market Microstructure: Order Books and Spreads

**Why this matters:** "The price" of an item is a fiction. There is a price to buy one right now, a price to sell one right now, and a different price again for buying two hundred. Those gaps decide who can make a living trading, how much a raider pays for consumables, and how easy your market is to push around. Microstructure is the study of those gaps, and you set most of them when you choose fees, tick sizes and matching rules.

**You will be able to:**
- Read an order book and compute best bid, best ask, mid price, spread and depth.
- Compute the average fill price and slippage of a market order by walking the book, and approximate it with a linear depth model.
- Derive the break-even spread for a market maker under a two-sided fee schedule, and compute it for EVE Online's current fees.
- Critique a market's microstructure (matching rule, fees, tick size, order limits) by predicting who it favors.

**Before class:** Lehdonvirta & Castronova, *Virtual Economies: Design and Analysis* (MIT Press, 2014), the market-design material within the course's assigned range, ch. 9-12. Demsetz, "The Cost of Transacting" (1968), sections I and II, on the spread as the price of immediacy.

**Prerequisites from earlier courses:** [MMO304 week 10, market design](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w10-market-design-auction-houses-vendors-barter.md) (posted prices vs order books, round-trip fees). [MMO304 week 6, supply, demand and equilibrium in auction houses](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w06-supply-demand-and-equilibrium-in-auction-houses.md). [MA101 week 2, linear functions and rates](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w02-linear-functions-and-rates.md). [MMO401 week 4](w04-monetary-policy-tools-in-games.md) for transaction taxes as sinks.

**Interactive:** [Order book depth](../examples/w05-order-book-depth.html). Keep it open during sections 2 and 3.

---

## 1. Anatomy of an order book

MMO304 week 10 introduced the two basic market shapes. In a **posted-price** market, sellers list items at a price and buyers take them. In an **order book**, buyers can also post standing offers, and the exchange matches the two sides. This week we zoom in on the order book, because that is where the interesting design decisions live.

An order book is two sorted lists.

- **Bids** are standing buy orders. "I will pay 9.8 for up to 50." They are sorted from highest price down.
- **Asks** (also called offers) are standing sell orders. "I will sell 40 at 10.0." They are sorted from lowest price up.

The top of each list gives you the numbers traders watch.

- The **best bid** is the highest price anyone will pay right now.
- The **best ask** is the lowest price anyone will sell at right now.
- The **spread** is best ask minus best bid. It is often quoted as a percentage of the mid price.
- The **mid price** is the average of best bid and best ask. It is the closest thing to "the price."
- **Depth** is the quantity available at or near the best prices. A deep book has lots of units close to the top. A thin book has few.

Orders come in two kinds. A **limit order** names a price and waits in the book until someone trades against it. A **market order** says "fill me now at whatever the book offers." In most games the distinction is implicit. If you place a buy order priced at or above the best ask, it behaves like a market order and fills at once. If you price it below, it rests in the book as a bid.

### Who gets filled, and at what price

A **matching rule** decides which resting order trades first and at what price. The usual rule in real exchanges is **price-time priority**. Better prices trade first, and among orders at the same price, older orders trade first.

Old School RuneScape's Grand Exchange documents its rule clearly. According to the Old School RuneScape Wiki, if you place a buy offer above existing sell offers, you trade with the lowest sell offer at that seller's price and the difference comes back to you. If you place a sell offer below existing buy offers, you trade with the highest buy offer at the buyer's price. Among offers at the same price, older offers go first. So the resting order sets the price, and the newcomer gets the benefit. That is standard price-time priority.

The rule matters because it decides who is paid for patience. The trader who rests an order in the book provides **liquidity**, meaning a standing chance for others to trade immediately. The trader who crosses the spread takes that liquidity. Under price-time priority, patient traders get their chosen price. Impatient ones pay the spread.

### A book you can compute with

Here is an invented book for a crafting herb. Every number in this lecture uses it.

| Bids (price, quantity) | Asks (price, quantity) |
|---|---|
| 9.8 × 50 | 10.0 × 40 |
| 9.5 × 120 | 10.2 × 60 |
| 9.0 × 200 | 10.5 × 100 |
| 8.0 × 300 | 11.0 × 150 |
| | 12.0 × 200 |
| | 14.0 × 300 |

Best bid 9.8, best ask 10.0. The spread is 0.2, the mid price is 9.9, and the spread is about 2% of the mid. By the usual reading, this is a healthy market. The next section shows why that reading is incomplete.

## 2. Worked example: walking the book

### The hook

In World of Warcraft's patch 8.3.0 (January 2020), Blizzard changed how stackable goods, which it calls commodities, sell on the auction house. You no longer pick a stack. You type how many you want and the auction house fills the order from the cheapest listings available. Buy five herbs and you pay about the listed price. Buy five hundred before raid night and the total is much more than five hundred times the price at the top of the list.

Nothing is wrong with the auction house. You have just walked the book. The price at the top only applies to the units at the top.

### The model

A market buy order for `Q` units fills against the asks in order, cheapest first. Write the ask side as levels `(p_1, q_1), (p_2, q_2), ...` with `p_1 < p_2 < ...`. Then:

```
C(Q)       = sum of p_i × (units taken from level i)      total cost
avg(Q)     = C(Q) / Q                                      average fill price
marginal(Q) = price of the level the last unit came from
slippage(Q) = avg(Q) / p_1 − 1                             cost above the best ask
```

- `C(Q)` is what you pay in total.
- `avg(Q)` is the per-unit price you actually got.
- The **marginal price** is the price of the last unit, which is where the best ask sits after your order.
- **Slippage** is how much worse your average was than the best ask. Some traders call the same thing price impact.

A market sell order works the same way against the bids, highest first.

### Numbers you can check

Walk the ask side of the herb book for increasing orders.

| Order size `Q` | Total cost `C(Q)` | Average price | Marginal price | Slippage |
|---|---|---|---|---|
| 40 | 400 | 10.00 | 10.0 | 0.0% |
| 100 | 1,012 | 10.12 | 10.2 | 1.2% |
| 200 | 2,062 | 10.31 | 10.5 | 3.1% |
| 350 | 3,712 | 10.61 | 11.0 | 6.1% |
| 550 | 6,112 | 11.11 | 12.0 | 11.1% |
| 850 | 10,312 | 12.13 | 14.0 | 21.3% |

Check the 200 row. You take all 40 at 10.0 (400), all 60 at 10.2 (612), and all 100 at 10.5 (1,050). The total is 2,062, so the average is 10.31. The next buyer now sees a best ask of 11.0.

Two things to notice. The 2% spread said nothing about what a 550-unit buyer pays, which is 11% more than the best ask. And the average price always trails the marginal price. After the 850-unit order, the book's best ask has moved from 10.0 to 14.0, a 40% jump, but the buyer's average is only 21% above where they started. Half the move, roughly. That "roughly half" has a reason.

### A linear approximation

Real books are lumpy, but on average depth is often spread fairly evenly across prices. Suppose there are `d` units for sale per 1 gold of price above the best ask `a`. Then the marginal price after buying `Q` units is a straight line, and the cost is the area under it.

```
marginal(Q) = a + Q / d
C(Q)        = a × Q + Q² / (2d)
avg(Q)      = a + Q / (2d)
```

The average price moves exactly half as far as the marginal price. The quantity `1 / d` is how many gold the price moves per unit bought. Finance calls it **Kyle's lambda**, after Albert Kyle's 1985 paper on how prices absorb orders. A market with small lambda is deep. A market with big lambda is thin.

Try it. With `a = 10` and `d = 100`, buying 300 units moves the marginal price to `10 + 3 = 13` and the average to `10 + 1.5 = 11.5`. Slippage is 15%, and it grows linearly with `Q / d`. Double the order, double the slippage. Double the depth, halve it.

### The visual

Open the interactive. The main view is a **depth chart**. The x axis is price. Two staircases rise away from the middle. The ask staircase climbs to the right, counting how many units you could buy up to each price. The bid staircase climbs to the left, counting how many you could sell. The gap between them at the bottom is the spread.

Drag the order-size slider. A shaded region fills the ask staircase from the left, and a vertical marker shows the new best ask. The readouts show total cost, average price and slippage, matching the table. Now switch the book preset to "thin" (the same spread, a tenth of the depth) and drag again. The spread looks identical. The slippage is ten times worse. That contrast is the lesson. The spread tells you the cost of trading one unit. The depth tells you the cost of trading many.

### Cross-game recognition

**World of Warcraft (retail, commodity auction house since patch 8.3.0).** A one-sided book. There are asks but no bids, so every buyer uses a market order and walks the ask side. The patch notes describe the rule plainly. You enter a quantity and the house takes the cheapest listings. Since patch 9.2.7 (August 2022), commodity listings are shared across all realms in a region, which made each book far deeper and cut slippage for large raid orders.

**Old School RuneScape (Grand Exchange, current).** A two-sided book with price-time priority, as described in section 1. It adds a **buy limit**. Each item can only be bought in a set quantity per account every four hours. In our model the buy limit caps `Q` for a single account. That caps how far one player can walk the book in one go, which protects thin items from being swept (next week's topic) and slows down bulk buyers, including bots.

**EVE Online (regional markets, current).** Each region has its own order book, and stations and market-enabled structures in the region see it. A buyer's order range, set by the Visibility skill, decides how far away a resting order can be. For a large buyer, walking the book in one region may cost more than hauling goods in from another, so the depth that matters includes the travel time to other regions' books (week 9 covers regional economies).

**Stock markets.** Kyle's 1985 model was written for a stock exchange. The same staircase appears in every exchange's depth chart. Large institutional orders are split into many small ones over time for exactly the reason in the table. Small orders pay the spread, large orders pay the slope.

Four markets, one staircase. When you look at a new market, ask two questions. How wide is the gap at the top, and how steep is the staircase?

### Design judgment, eyes open

- **Deep books favor casual players.** A raider who buys 200 flasks the night before a raid wants low slippage. Pooling markets (region-wide, cross-server) is the most powerful depth lever you have. WoW's 9.2.7 change pooled whole realms.
- **Deep books also weaken local economies.** Depth pooled from everywhere removes the reason to trade locally. That is a real cost if your world design depends on regional prices (week 9).
- **Order limits cap `Q` directly.** Buy limits like Old School RuneScape's protect thin books but annoy legitimate bulk buyers. Set them per item, from each item's typical depth, not as one global number.
- **A one-sided book pushes all waiting onto sellers.** Without bids, a seller who wants to sell now must undercut the lowest ask. With bids, they can sell into the best bid. Decide which side should carry the patience in your economy.

### Check yourself (worked example)

1. Using the herb book, what does a market order for 250 units cost in total and on average? What is the slippage?
2. In a linear book with best ask 20 and depth `d = 50` units per gold, what are the marginal price, average price and slippage for a 200-unit order?

<details>
<summary>Answers</summary>

1. `40 × 10.0 + 60 × 10.2 + 100 × 10.5 + 50 × 11.0 = 400 + 612 + 1,050 + 550 = 2,612`. Average `2,612 / 250 = 10.448`. Slippage `10.448 / 10 − 1 ≈ 4.5%`.
2. Marginal `20 + 200/50 = 24`. Average `20 + 200/100 = 22`. Slippage `22/20 − 1 = 10%`.

</details>

## 3. What the spread pays for

Why would anyone pay the spread? Harold Demsetz answered this in 1968. The spread is the price of **immediacy**. A buyer who wants the herb now pays the best ask. A buyer who can wait posts a bid and hopes a seller comes along. The spread is what the patient side earns for standing ready.

The patient traders who stand ready on both sides are **market makers**. In EVE Online they are called station traders. They post a bid and an ask on the same item in the same station, buy from impatient sellers, sell to impatient buyers, and keep the gap. In Old School RuneScape, players call the same activity flipping or merchanting.

### The break-even spread

A market maker does not keep the whole spread. Fees take a cut. Suppose placing any order costs a **broker fee** `b` as a share of the order's value, and every sale pays a **sales tax** `t` as a share of the sale. The market maker buys one unit at their bid `B` and sells it at their ask `A`.

```
cost of buying   = B × (1 + b)
revenue of selling = A × (1 − b − t)
profit per unit  = A × (1 − b − t) − B × (1 + b)
```

Profit is zero when

```
A / B = (1 + b) / (1 − b − t)
```

That ratio minus one is the **break-even spread**. No market maker can quote a tighter spread for long without losing money. Fees put a floor under the spread.

### Numbers you can check

EVE Online charges both fees at NPC stations. The broker fee has a 3% base, reduced by 0.3 points per level of Broker Relations and a little further by standings. The sales tax has had a 7.5% base since release 22.02 (12 March 2025), reduced by 11% per level of Accounting. We ignore standings here.

| Market and trader | Broker fee `b` | Sales tax `t` | Break-even `A / B` | Break-even spread |
|---|---|---|---|---|
| EVE, no trade skills | 3.0% | 7.5% | `1.03 / 0.895 = 1.1508` | 15.1% |
| EVE, Broker Relations V only | 1.5% | 7.5% | `1.015 / 0.91 = 1.1154` | 11.5% |
| EVE, Accounting V only | 3.0% | 3.375% | `1.03 / 0.93625 = 1.1001` | 10.0% |
| EVE, both at V | 1.5% | 3.375% | `1.015 / 0.95125 = 1.0670` | 6.7% |
| Old School RuneScape, 2% tax on the seller | 0% | 2% | `1 / 0.98 = 1.0204` | 2.0% |
| World of Warcraft, 5% cut (no bids, so this is a flip of listings) | 0% | 5% | `1 / 0.95 = 1.0526` | 5.3% |

Check the EVE "both at V" row. `b = 3% − 5 × 0.3% = 1.5%`. `t = 7.5% × (1 − 5 × 0.11) = 3.375%`. So `A / B = 1.015 / (1 − 0.015 − 0.03375) = 1.015 / 0.95125 ≈ 1.0670`.

The table tells a story about who trades. A fully skilled EVE trader can profit on any spread above 6.7%. An unskilled one needs more than 15%. In any item with lots of skilled traders, competition pushes spreads down toward 6.7%, and the unskilled trader cannot make money there at all. The fee schedule plus a skill tree creates a profession with a barrier to entry. That is a design choice, whether or not it was made on purpose.

Compare Old School RuneScape. A 2% seller tax lets anyone flip items with spreads above 2%, so competition squeezes spreads much tighter. Tight spreads are good for ordinary players who buy and sell once. They also leave much less room for a merchant career.

### Spreads and thinness

The fee floor is the minimum spread. Actual spreads are wider in thin items for two reasons. A market maker in a thin item waits longer between fills, so they hold stock longer and take more risk that the price moves against them. And fewer market makers compete, so nobody undercuts them down to the floor. That is why the spread is a direct readout of how liquid an item is. On your dashboards (week 13), a spread that suddenly widens usually means traders left the item or expect a price move.

## 4. Queues, ticks and undercut wars

Price-time priority creates a race. If you want your ask filled first, you must beat the best ask by the smallest allowed price step, called the **tick size**. Then someone beats you by one tick, and so on. Players in every game with an order book know this as undercutting.

The tick size sets how cheap it is to jump the queue. In a game where prices are in whole gold and a typical item costs 20, one tick is 5% of the price, a big step. Nobody undercuts by a tick for fun. In a game where prices run to two decimal places on items worth millions, one tick is effectively free. The queue becomes a pure reaction-time contest, and whoever updates their order most often wins, which rewards people who check the market constantly and invites automation.

Games answer with **modification costs**. EVE Online charges a fee to modify an order's price. EVE University's wiki describes it as a broker fee reduced by a relist discount, 50% at base and larger with the Advanced Broker Relations skill, and notes that in some cases modifying an old order costs more than cancelling and placing a new one. A modification fee makes each undercut cost a share of the order's value, so it only pays to undercut when you expect the fill to earn more than the fee.

You have four levers against undercut wars. Each has a cost.

| Lever | Effect on undercutting | Cost |
|---|---|---|
| Larger tick size | Each undercut gives up more margin | Coarser prices on cheap items |
| Fee on modification | Each undercut costs a share of value | Honest repricing costs too |
| Cooldown on modification | Limits how often a player can reprice | Slow response to real news |
| Hidden or delayed book | Traders cannot see the exact best price | Less transparency for everyone |

None of these is free. Pick the one whose cost your players will notice least.

## 5. Designing a market's microstructure

When you specify a market, you now have a vocabulary for its microstructure. Write each choice down.

1. **Book shape.** One-sided (asks only) or two-sided (bids and asks). One-sided is simpler and pushes the waiting onto sellers.
2. **Matching rule.** Price-time priority is the default. State who gets the price improvement when a new order crosses the book. Old School RuneScape gives it to the newcomer.
3. **Fees.** On placing, on selling, on modifying. Each fee raises the break-even spread. Use the formula in section 3 to see the floor your fees create for market makers.
4. **Tick size.** Absolute (1 gold) or relative (a share of price). Relative ticks keep undercut cost constant across cheap and expensive items.
5. **Order limits.** Per-item buy limits cap `Q` and slippage for a single account.
6. **Scope.** Which players see which book. Scope sets depth.

Each choice favors someone. Deep, tight, low-fee books favor casual buyers and sellers. Thin, fee-heavy books favor skilled market makers and whoever can afford to wait. Week 7 adds the other side of the fee question. Each fee is a sink, and raising it trades market volume for money removed. There you will run an order-book simulation that measures exactly that trade-off.

## In-class activity (25 minutes)

Pairs play a paper order book. The instructor hands out cards: six "impatient buyer" cards (buy `n` units now), six "impatient seller" cards, and two "market maker" roles per pair.

1. Start from the herb book in section 1, written on the whiteboard. Market makers may post one bid and one ask each, at any price in ticks of 0.1.
2. The instructor draws cards one at a time. Impatient orders walk the book. Market makers may repost after each card, paying a 2% broker fee on each posted order's value and a 2% sales tax on each sale.
3. After twelve cards, each market maker reports profit, inventory, and the tightest spread they quoted that made money.
4. Compare the tightest profitable spread with the break-even formula in section 3 with `b = 2%`, `t = 2%`.

Expected output: each pair's profit and inventory, and a one-sentence explanation of any gap between the tightest profitable spread and the formula (usually inventory left unsold).

## Common misconceptions

- **"A small spread means a liquid market."** A small spread says the first unit is cheap to trade. Depth says whether the hundredth is. Check both.
- **"Market makers are parasites taking a cut."** They sell immediacy. Without them, a seller who wants to sell now has to wait for a buyer, or cut the price until one appears. The fee floor decides how much they can charge.
- **"Fees only matter as a sink."** Fees also set the minimum spread and so decide which players can profit from trading. The same fee schedule with a skill discount creates a profession.
- **"Undercutting by one tick is harmless."** When ticks are tiny compared with prices, the queue turns into a reaction-time race that rewards constant monitoring and automation.

## Check yourself

1. Using the herb book, a gatherer sells 200 herbs with a market order. What do they receive before fees, and what is their average price?
2. An EVE trader has Broker Relations V and Accounting III. What is their break-even spread? (Ignore standings.)
3. A designer proposes cutting a game's sales tax from 5% to 1% to "help traders." Use the break-even formula to predict what happens to spreads in busy items and to the income of existing market makers.
4. A book has best ask 50 and depth `d = 20` units per gold. A buy limit of 100 units per four hours applies. What is the worst average price one account can get in a single four-hour window? What if the buyer uses five accounts, one after another, and nobody refills the book?

<details>
<summary>Answers</summary>

1. `50 × 9.8 + 120 × 9.5 + 30 × 9.0 = 490 + 1,140 + 270 = 1,900`. Average `1,900 / 200 = 9.5`, which is 3.1% below the best bid.
2. `b = 1.5%`. `t = 7.5% × (1 − 0.33) = 5.025%`. `A / B = 1.015 / (1 − 0.015 − 0.05025) = 1.015 / 0.93475 ≈ 1.0859`. Break-even spread about 8.6%.
3. With `b = 0`, the floor falls from `1/0.95 − 1 ≈ 5.3%` to `1/0.99 − 1 ≈ 1.0%`. More players can profit from flipping, competition pushes spreads in busy items toward 1%, and the existing market makers' margin per trade shrinks. Ordinary buyers and sellers gain. Traders do not, even though the change was pitched as helping them. The game also removes less money per trade.
4. One account: `avg = 50 + 100/(2 × 20) = 52.5`. Five accounts in a row walk 500 units in total. The last account buys units 401 to 500, whose average price is `50 + 450/20 = 72.5`. The buy limit per account does nothing against multiple accounts, which is why buy limits usually come with rules or detection aimed at alts.

</details>

## Lab / assignment hook

[Lab 05, build a matching engine](../labs/lab05.md). You implement a price-time priority order book in Python from the starter file, fill it with simple agent traders (impatient buyers, impatient sellers and one market maker), and measure spread, depth and slippage as you change the fee schedule. Lab 06 reuses the engine. Week 7's transaction-tax lab uses its own simpler clearing model, and you can check its results against this engine.

## Sources

- World of Warcraft, patch 8.3.0 notes (14 January 2020), as recorded on Warcraft Wiki. Commodities are bought by entering a quantity, and the auction house selects the cheapest listings. Warcraft Wiki, "Auction House": patch 9.2.7 (16 August 2022) made commodity listings shared across realms in a region; 5% cut.
- Old School RuneScape Wiki, "Grand Exchange" (accessed September 2026). Matching at the existing offer's price with the difference returned, older offers first at equal prices, buy limits per four hours, the 2% tax since 29 May 2025.
- EVE University Wiki, "Trading" and "Accounting" (current). Broker fee 3% base at NPC stations, minus 0.3% per Broker Relations level and small standings reductions; sales tax 7.5% base, minus 11% per Accounting level; relist discount of 50% at base, raised by Advanced Broker Relations; regional markets and order ranges set by Visibility. EVE Online, "Patch notes, version 22.02" (12 March 2025) for the sales tax rise from 4% to 7.5%.
- Demsetz, H. (1968). "The Cost of Transacting." *Quarterly Journal of Economics* 82(1).
- Kyle, A. S. (1985). "Continuous Auctions and Insider Trading." *Econometrica* 53(6).
- Lehdonvirta, V. & Castronova, E. (2014). *Virtual Economies: Design and Analysis*. MIT Press.
- The herb book and all linear-depth numbers are invented for teaching.

## Interactive spec: examples/w05-order-book-depth.html

**The one insight:** the spread tells you the cost of trading one unit, the depth tells you the cost of trading many. Two books with the same 2% spread can have slippage that differs by a factor of ten.

**Layout.** Two panels. Panel A "Walk the book" on top (or left on desktop), panel B "Break-even spread" below (or right).

**Panel A, depth chart.**
- X axis: price from 7.5 to 15. Y axis: cumulative quantity. Ask staircase (cumulative units available at or below each price) drawn to the right of the best ask. Bid staircase (cumulative units at or above each price) drawn to the left of the best bid. The spread gap is labelled with its value and percentage of mid.
- Book presets (radio buttons): "Lecture book" (bids 9.8×50, 9.5×120, 9.0×200, 8.0×300; asks 10.0×40, 10.2×60, 10.5×100, 11.0×150, 12.0×200, 14.0×300), "Thin" (same prices, every quantity divided by 10, rounded to whole units: bids 5, 12, 20, 30; asks 4, 6, 10, 15, 20, 30), "Wall" (lecture book plus an extra ask of 1,000 at 10.5).
- Controls: side toggle (buy / sell); order size slider 0 to the total depth of the chosen side, step 10 (keyboard arrows move by 10, PageUp/PageDown by 100).
- On change: shade the portion of the staircase consumed; draw a vertical line at the new best price; readouts for total cost (or proceeds), average price, marginal price, slippage relative to best price. If the order exceeds the book, show "book exhausted" and fill only what exists.
- Algorithm: iterate levels in priority order; take `min(remaining, q_i)` from each; sum `p_i × taken`.
- Test values (lecture book, buy): Q = 40 gives 400 / 10.00 / 10.0 / 0.0%. Q = 100 gives 1,012 / 10.12 / 10.2 / 1.2%. Q = 200 gives 2,062 / 10.31 / 10.5 / 3.1%. Q = 250 gives 2,612 / 10.448 / 11.0 / 4.5%. Q = 550 gives 6,112 / 11.11 / 12.0 / 11.1%. Q = 850 gives 10,312 / 12.13 / 14.0 / 21.3%. Sell Q = 200 gives proceeds 1,900 / average 9.50 / marginal 9.0 / 3.1% below best bid. Thin book, buy Q = 55 gives `4×10 + 6×10.2 + 10×10.5 + 15×11 + 20×12 = 40 + 61.2 + 105 + 165 + 240 = 611.2`, average 11.11, slippage 11.1% (same slippage as 550 units in the lecture book, which is the point).
- An optional "linear model" overlay: a straight line `a + Q/d` fitted with `a` = best ask and `d` entered by a small input (default 100), with its `avg = a + Q/(2d)` readout next to the exact one.

**Panel B, break-even spread.**
- Controls: broker fee `b` 0% to 5% step 0.1%; sales tax `t` 0% to 10% step 0.025% (to allow 3.375%); preset buttons "EVE no skills" (3, 7.5), "EVE BR V" (1.5, 7.5), "EVE Acc V" (3, 3.375), "EVE both V" (1.5, 3.375), "OSRS" (0, 2), "WoW" (0, 5).
- Readout: `A/B = (1 + b)/(1 − b − t)` to four decimals and break-even spread as a percentage to one decimal. A small bar showing the herb book's actual spread (2.0%) against the break-even value, coloured by whether a market maker profits.
- Test values: 1.1508 / 15.1%; 1.1154 / 11.5%; 1.1001 / 10.0%; 1.0670 / 6.7%; 1.0204 / 2.0%; 1.0526 / 5.3%.

**Accessibility and style.** Shared palette from `templates/interactive-tokens.css`. All staircase values also available in a collapsible table. Respect `prefers-reduced-motion`. No logos or game art; the item is a generic "herb".
