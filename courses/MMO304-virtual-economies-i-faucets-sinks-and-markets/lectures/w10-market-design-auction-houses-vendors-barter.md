# MMO304 · Week 10 — Market Design: Auction Houses vs Player Vendors vs Barter

**Why this matters:** The trading interface you ship decides how far apart prices can drift, who gets rich from trade, and whether "merchant" is a way to play your game or a spreadsheet job. Changing it later is one of the most disruptive patches an MMO can make, so you should choose it on purpose.

**You will be able to:**
- Compute the expected price a buyer pays after checking `k` sellers, and the number of sellers a buyer should check for a given search cost.
- Predict how price dispersion and seller pricing change when a game moves from barter to player vendors to a central auction house.
- Compute the round-trip cost of a trade under a fee schedule and use it to predict the smallest price gap traders will close.
- Critique a market design for a specific game, naming what it gains and what it gives up.

**Before class:** Lehdonvirta & Castronova, *Virtual Economies: Design and Analysis* (2014), the chapter on market design and the chapter on money. Skim Stigler (1961), "The Economics of Information", sections I and II (the first eight pages are enough).

**Prerequisites from earlier courses:** [MA102 week 4, expected value](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md) (the expected price you pay is an expected value). [MA102 week 11, Monte Carlo simulation](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w11-monte-carlo-simulation.md) (the lab checks this week's formula by simulation). [MMO303 week 10, payoff matrices and Nash equilibria](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w10-game-theory-payoff-matrices-and-nash-equilibria.md) (undercutting is a game between sellers). [GD102 week 7 on internal economies](../../GD102-systems-design-and-game-mechanics/lectures/w07-internal-economies-sources-drains-converters.md). From this course, [week 9 on commodity money](w09-commodity-money-when-an-item-becomes-currency.md) (the Stone of Jordan and the barter search count) and [week 6 on supply, demand and equilibrium](w06-supply-demand-and-equilibrium-in-auction-houses.md).

**Interactive:** [Search cost and the price spread](../examples/w10-search-cost-market.html). Keep it open during section 2.

---

## 1. Three ways to put buyers and sellers together

Every MMO with trade has to decide how a player who wants something finds a player who has it. The answer is the game's **market design**, the set of rules and interfaces that match buyers with sellers and set the terms of a trade. There are three families.

**Barter.** Players trade goods for goods directly, face to face, with no in-game price list. The original Diablo II had a trade window and chat channels and nothing else. If you wanted a rune, you had to find someone who had it and who also wanted something you had.

**Player vendors.** Sellers set up shops, and buyers travel to them. In Ultima Online a player hires a vendor with a contract of employment and places it in a player-owned house, where it sells items at the owner's prices while the owner is offline. Buyers walk from house to house.

**Central exchange.** One interface lists every offer, and a buyer sees them all at once. World of Warcraft's auction house, Guild Wars 2's Trading Post, the Grand Exchange in RuneScape and Old School RuneScape, and EVE Online's regional markets are all versions of this.

The three differ in many ways, but one variable drives most of the differences, and you can measure it. That variable is **search cost**, the time and effort a buyer spends finding and comparing offers. Barter has the highest search cost, vendors sit in the middle, and a central exchange drives it close to zero. The rest of this lecture shows what search cost does to prices, and then what else changes when you remove it.

## 2. Worked example: why the auction house flattens prices

### The hook

Before Ultima Online had a vendor search tool, the same item could carry very different prices on different player vendors. UOGuide notes that vendor prices "fluctuate wildly" and were generally highest on vendors around Luna, the busiest town. A vendor in a high-traffic spot sold quickly at a premium, while the same item sat longer at a lower price on a remote vendor.

Compare that with World of Warcraft after patch 9.2.7 (August 2022). From that patch on, every realm in a region shares one listing for commodities such as herbs, gems, flasks and other stackables. A player buying an herb sees the cheapest offers from the whole region at once. Few buyers will pay 20% over the cheapest ask when the cheapest ask is on the same screen, so the model below predicts that prices for one herb in one region should bunch into a narrow band.

Same kind of good, two markets, very different price behavior. Why do prices spread out in one and collapse in the other? The seller didn't change. The buyer's search cost did.

### The model

Take one good. Sellers have posted asks spread evenly between a low price `L` and a high price `H`. A buyer checks `k` sellers, chosen at random, and buys from the cheapest one they saw. Each check costs the buyer `c` gold, which stands for the value of their time spent walking, whispering or waiting.

- `L` is the lowest ask in the market, usually close to what the good costs to produce.
- `H` is the highest ask.
- `k` is the number of sellers the buyer checks.
- `c` is the search cost per seller checked, in gold.

The expected lowest of `k` evenly spread prices is a standard result about the minimum of uniform random draws:

```
E[price paid] = L + (H − L) / (k + 1)
```

The buyer's total expected cost is the price plus the search:

```
total cost(k) = L + (H − L) / (k + 1) + k × c
```

Checking one more seller lowers the expected price by

```
gain from seller k+1 = (H − L) / ((k + 1)(k + 2))
```

A sensible buyer keeps searching while that gain is bigger than `c`, and stops at the first `k` where it is not.

This is George Stigler's 1961 search model, cut down to one good and one formula. Stigler's point was that price dispersion is not a sign of a broken market. It is what a market looks like when finding prices costs something.

### Numbers you can check

Take an herb whose asks run from `L = 80` to `H = 120` gold. First, the price a buyer expects to pay after `k` checks.

| Sellers checked `k` | Expected price paid | Gain from checking one more |
|---|---|---|
| 1 | 100.00 | 6.67 |
| 2 | 93.33 | 3.33 |
| 3 | 90.00 | 2.00 |
| 4 | 88.00 | 1.33 |
| 5 | 86.67 | 0.95 |
| 9 | 84.00 | — |
| 39 | 81.00 | — |
| 200 (every listing) | 80.20 | — |

Check the second row by hand. `80 + 40 / 3 = 93.33`. The first extra check is worth 6.67 gold. The fifth is worth less than one.

Now add search cost and find the best `k` for each value of `c`.

| Search cost `c` per check | Best `k` | Expected price paid | Total cost including search |
|---|---|---|---|
| 0 (central exchange) | all listings | about 80 | about 80 |
| 1 | 5 | 86.67 | 91.67 |
| 3 | 3 | 90.00 | 99.00 |
| 6 | 2 | 93.33 | 105.33 |

With `c = 3`, the third check gains 3.33 and the fourth would gain only 2.00, so the buyer stops at three. At `c = 6`, the buyer checks two sellers. A buyer in a barter world, where each "check" means finding a stranger in chat, pays about 13 gold more than a buyer at a central exchange before counting their time, and about 25 gold more once you do.

### The seller's side

The buyer table is only half the story. Sellers react. A seller who asks price `p` only makes the sale if every other seller the buyer checked asked more. With asks spread evenly between `L` and `H`, the chance of that is

```
P(sale | buyer checked you) = ((H − p) / (H − L)) ^ (k − 1)
```

| Ask `p` | `k = 1` | `k = 2` | `k = 3` | `k = 10` |
|---|---|---|---|---|
| 80 | 100% | 100% | 100% | 100% |
| 90 | 100% | 75% | 56.3% | 7.5% |
| 100 | 100% | 50% | 25% | 0.2% |
| 110 | 100% | 25% | 6.3% | 0.0004% |

Read down the `k = 1` column. When buyers check only one seller, a high ask sells as often as a low one, so every seller should ask the most they can. The economist Peter Diamond showed in 1971 that, taken to its limit, any positive search cost can push every seller to the monopoly price. Now read the `k = 10` column. An ask of 100 almost never sells. Sellers who want to sell must cut toward `L`.

Multiply price by chance of sale and you get the seller's expected revenue per buyer who checks them. At `k = 1` the 110 ask earns 110. At `k = 3` it earns 6.9, and the 80 ask earns 80. So the auction house has a second effect on top of helping buyers find the low price. It removes the reason for anyone to post a high one. That is why you see the undercutting wars familiar to every auction house player, where sellers relist one copper below the lowest ask. The spread closes until the lowest asks sit near what the good costs to make.

### The visual

Open `examples/w10-search-cost-market.html`. The left panel shows a strip of seller asks and marks the ones a buyer checked, with the price they paid. The right panel plots total cost against `k`, with the best `k` marked. Drag the search-cost slider from 6 down to 0. On the right, the best `k` climbs and the total cost falls. On the left, press "Let sellers respond" and watch the asks bunch up against `L`. The same slider moves both the buyer's behavior and the whole price distribution.

### Cross-game recognition

**EVE Online (current, 2026 era).** EVE has one market per region, not one market for the whole game. A buyer in one region sees every order in that region at zero search cost, but buying in a different region means flying a hauler through space, which costs time and risks losing the cargo. Inside a region, `c` is near zero and prices are tight. Between regions, `c` is large, and the EVE University wiki describes the result directly. The same item has different prices in different places, and traders earn a living by buying where it is cheap and hauling it to where it is dear. EVE is the search model with geography put back in.

**World of Warcraft (1.9 to 9.2.7).** WoW has moved its own `c` down in steps. Patch 1.9.0 (January 2006) linked each faction's city auction houses. Patch 6.0.2 (October 2014) merged the Alliance, Horde and neutral houses on each realm. Patch 9.2.7 (August 2022) made commodity listings region-wide while leaving gear realm-specific. Each step widened the pool a buyer sees in one search, which is the same as raising `k` at zero extra cost.

**Diablo II (original release and Lord of Destruction).** Diablo II had no exchange at all, so it sits at the high-`c` end. Barter has an extra cost that vendors don't. You must find someone who has what you want *and* wants what you have. The economist William Stanley Jevons called this the "double coincidence of wants" in 1875. Suppose each player holds one of `G` kinds of goods and wants one of the others, at random. A random partner has what you want with probability `1 / (G − 1)` and wants what you have with the same probability, so you expect to meet `(G − 1)²` partners before a trade works. With 10 kinds of goods, that is 81 meetings. With a money that everyone accepts, each half of the trade needs only one match. You meet about `G − 1 = 9` partners to sell your good for money and 9 more to buy what you want, `2(G − 1) = 18` in all, the same count as week 9. The search-cost gap between barter and money grows with the square of the number of goods. That is the pressure that turned the Stone of Jordan into Diablo II's currency, which you studied in week 9.

Three games, three values of `c`, one curve. When you look at any trading system, ask what one more price check costs a buyer. That number predicts the price spread you'll see.

### Eyes-open design judgment

Low search cost is efficient, and efficiency is not the only goal of a game market.

- **What a central exchange gives you.** Fair prices for casual players, fast clearing of gathered goods, and a single price per good that players and designers can read. It also gives you a place to put a fee, which counts as a sink in the week 3 ledger.
- **What it takes away.** The merchant career. When everyone sees every price, the only remaining trading skill is spotting trends, and bots can do that faster than people. Geography stops mattering, so a remote town has no reason to have a market. Social trading, haggling and the reputation of a trusted seller all disappear.
- **What vendors and barter cost.** New players pay the spread. In the table above, a buyer who checks one seller pays 20 gold more than one who sees them all. Players who know the prices profit from those who don't, which some games want and many don't.
- **The middle options.** You can keep one central market per region (EVE), centralize only commodities (WoW since 9.2.7), or add a search tool to vendors while keeping travel to buy (Ultima Online's later vendor search). Each is a choice of `c` per good, not one number for the whole game.

So the real decision is which goods should be cheap to find, and which should keep a price spread that rewards knowledge, travel or social ties. "Auction house or not" is too coarse a question.

## 3. Fees: the price of a round trip

Every central exchange charges fees, and fees matter twice. They remove money, which makes them a sink. They also set how large a price gap has to be before a trader bothers to close it.

Here are four fee schedules, each cited in Sources:

| Market (era) | Fee on a sale |
|---|---|
| World of Warcraft auction house (current retail) | 5% of the winning bid, plus a deposit based on the item's vendor price that is kept if the item doesn't sell |
| Guild Wars 2 Trading Post (current) | 5% listing fee paid up front, plus a 10% exchange fee on sale, 15% in total |
| Old School RuneScape Grand Exchange (since 29 May 2025) | 2% on the seller, capped at 5 million coins per item. It was 1% from December 2021. |
| EVE Online NPC station markets (current) | Sales tax of 7.5% base, cut by the Accounting skill, plus a broker's fee of 3% base on placed orders |

A trader who buys at price `b` and resells at price `s`, paying a total fee rate `f` on the sale, profits only if

```
s × (1 − f) > b      so      s > b / (1 − f)
```

With Guild Wars 2's 15%, an item bought at 100 must resell above `100 / 0.85 = 117.6` to break even. With Old School RuneScape's 2%, the break-even is 102.04. A price gap of 10% between two listings is free money in Old School RuneScape and a loss in Guild Wars 2. The fee is a band around the price inside which nobody trades. Wider band, fewer flippers, more price noise, and more gold removed per trade. Narrower band, tighter prices and more speculation.

The Old School RuneScape case shows a second use. The Old School RuneScape Wiki reports that most of the tax is deleted outright, and part funds an "item sink" that buys selected items from players and deletes them. The tax is a gold sink that also controls item supply. You'll meet the telemetry used to size such a sink in week 12.

## 4. Order books and posted prices

Central exchanges differ in one more way that changes player behavior. Some show only sellers' asks. Others let buyers post standing offers too.

In a **posted-price** market, sellers list items at fixed prices and buyers take them. Only the sell side is visible. In an **order book**, buyers can also post "I will pay 90 for up to 50 of these," and the exchange matches a new sell order against the best standing buy order. EVE's markets, the Guild Wars 2 Trading Post and the RuneScape Grand Exchange all take buy offers as well as sell offers.

An order book has two visible prices, the highest bid and the lowest ask. The gap between them is the **bid-ask spread**. It is a direct reading of how thin a market is. A spread of 1% means lots of traders compete on both sides. A spread of 30% means few people trade this good, and a patient seller can earn most of that gap.

Order books change what "selling" feels like. A gatherer can sell instantly into the highest bid and get on with the game, or list at the ask and wait. That choice is a trade-off between time and money, and it lets players with different amounts of patience coexist. Posted-price markets offer only the waiting option, or a steep undercut to jump the queue.

## 5. Choosing a design

When you pick a market design, you are choosing values for a few variables. Write them down before you write any code.

1. **Search cost per good class.** Commodities and gear can have different values. WoW's 2022 split is a real example.
2. **Scope.** One market per server, per region of the world map, or for the whole game. A larger scope gives tighter prices and fewer local opportunities.
3. **Fees and where they sit.** Up front (listing), on sale, or both. Up-front fees punish relisting wars. Sale fees punish flipping.
4. **Visibility.** Asks only, or asks and bids. Price history shown or hidden. Showing history makes prices tighter and makes bots easier to write.
5. **Access.** Is the market reachable from anywhere, only from towns, or only from certain towns? Access is search cost in another form.

A useful exercise is to describe a new game's market in the language of this lecture. "Commodities: one region-wide order book, reachable from any town, 5% fee on sale. Gear: player vendors in housing districts, no search tool, 60 gold daily upkeep." You can predict the price spread each part will produce before a single player logs in.

## In-class activity (25 minutes)

Work in groups of three. One person is the buyer, two are sellers with a hand of cards.

1. Each seller writes five asks for "Iron Bar" between 80 and 120 on slips of paper, face down.
2. **Round 1 (vendors).** The buyer may flip up to three slips. Each flip costs the buyer 3 gold. The buyer buys the cheapest flipped slip. Record the price and the total cost. Repeat five times with fresh slips.
3. **Round 2 (auction house).** All ten slips face up. The buyer buys the cheapest. Sellers then rewrite their asks for the next round, knowing only the cheapest sells. Play three rounds and record the lowest and highest asks each round.
4. Compare your averages with the tables in section 2.

Expected output: a small table of five vendor-round prices and three auction-house rounds, the spread in each auction round, and one sentence on how sellers changed their asks.

## Common misconceptions

- **"Price differences between sellers mean the market is broken."** Dispersion is the normal result of positive search cost. It becomes a problem only if you didn't intend it or players can't learn to exploit it.
- **"The auction house lowers prices because it adds competition."** It adds information. The number of sellers can be the same. What changes is how many of them each buyer can compare at once.
- **"Fees are just a gold sink."** They are also a band inside which nobody trades. A 15% fee kills arbitrage on gaps under 17.6%. That shapes who can make a living trading.
- **"Barter is just trading without money."** Barter's cost grows with the square of the number of goods. Players answer by inventing a money, whether you planned one or not.

## Check yourself

1. Asks are spread evenly between 50 and 110 gold. What price does a buyer expect to pay after checking four sellers?
2. Same market, with a search cost of 4 gold per check. How many sellers should the buyer check, and what is their total expected cost?
3. A Guild Wars 2 trader sees an item listed at 200 silver and a standing buy order elsewhere at 230 silver for the same item. Should they buy and resell? Show the numbers.
4. A game has 16 kinds of tradable goods and no common money. How many trading partners should a player expect to meet before finding a double coincidence of wants? How many with money?
5. A designer wants a "merchant" class whose players earn by knowing prices. Name two changes to a central auction house that would give them room, and one cost of each.

<details>
<summary>Answers</summary>

1. `50 + 60 / 5 = 62` gold.
2. The gain from check `k + 1` is `60 / ((k + 1)(k + 2))`. From 1 to 2 it is 10, 2 to 3 is 5, 3 to 4 is 3. Stop at `k = 3` since 3 < 4. Expected price `50 + 60 / 4 = 65`, total cost `65 + 3 × 4 = 77`.
3. Selling at 230 with 15% fees returns `230 × 0.85 = 195.5`, less than the 200 paid. The trade loses 4.5 silver. The break-even resale price is `200 / 0.85 = 235.3`.
4. `(16 − 1)² = 225` partners without money. With money, `2 × (16 − 1) = 30`: 15 to sell and 15 to buy.
5. Examples: limit the auction house to certain towns (raises `c`, players pay more and complain about travel); hide price history (traders who track prices win, bots and add-ons can rebuild the history, so the edge may not last); raise fees (fewer flippers, but prices for casual players spread out); split commodities from gear (only gear keeps a spread, which is complex to explain).

</details>

## Lab / assignment hook

[Lab 10, search cost and market design](../labs/lab10.md). You will check the expected-minimum formula by simulation, find the best number of checks for a range of search costs, simulate sellers undercutting in an auction house, and write a market design for a small MMO. The market design counts toward the models assessment (30%).

## Sources

- UOGuide, "Vendors" (Ultima Online, current shards). Player vendors are placed in public player houses with a contract of employment. Standard vendors charge 60 gold per day plus commission. Prices vary widely and were highest around Luna before Vendor Search.
- Warcraft Wiki, "Auction House" (World of Warcraft retail). The 5% cut and the deposit table. Patch 1.9.0 (3 January 2006) linked faction auction houses. Patch 6.0.2 (14 October 2014) merged them per realm. Patch 9.2.7 (16 August 2022) made commodities region-wide while gear stayed realm-specific.
- Guild Wars 2 Wiki, "Trading Post" (current). 5% listing fee and 10% exchange fee. One market shared by all worlds.
- Old School RuneScape Wiki, "Grand Exchange" (current). The Grand Exchange was added to Old School on 26 February 2015. The tax was 1% from 9 December 2021 and 2% from 29 May 2025, capped at 5 million coins per item. Most tax is deleted and part funds an item sink.
- RuneScape Wiki, "Grand Exchange". The original RuneScape Grand Exchange launched on 26 November 2007.
- EVE University Wiki, "Trading" (2025-26 era). Markets are regional. Sales tax 7.5% base, broker's fee 3% base, both reduced by skills and standings. Cross-region price differences and hauling.
- Stigler, G. J. (1961). "The Economics of Information." *Journal of Political Economy* 69(3), 213-225. The search model and price dispersion.
- Diamond, P. A. (1971). "A Model of Price Adjustment." *Journal of Economic Theory* 3(2), 156-168. Search cost and monopoly pricing.
- Jevons, W. S. (1875). *Money and the Mechanism of Exchange*. The double coincidence of wants.
- Lehdonvirta, V. & Castronova, E. (2014). *Virtual Economies: Design and Analysis*. MIT Press.

## Interactive spec: examples/w10-search-cost-market.html

**Insight the visual must make obvious:** lowering the buyer's search cost raises the number of sellers checked, and once sellers respond, the whole spread of asks collapses toward the lowest price. The spread is caused by search cost, not by sellers.

**Layout:** two linked panels, side by side on desktop, stacked on mobile (left panel first).

- **Left panel, "The market":** a horizontal price axis from `L` to `H`. Draw N = 40 seller asks as small ticks or dots along it (jitter vertically so they don't overlap). Highlight the `k*` sellers the most recent simulated buyer checked, and mark the price paid with a larger dot and label "Paid: X". Below the axis, a small text line: "Spread of asks: min A, max B, width B − A".
- **Right panel, "How far should a buyer look?":** x-axis `k` from 1 to 20 (integer). Plot three series: expected price `L + (H − L)/(k + 1)` (line), search spend `k × c` (line), and total cost (thicker line). Mark the minimum of total cost with a dot and label "Best k = k*, total = T". When `c = 0`, show a note "Central exchange: buyer sees all N listings" and set `k* = N`.

**Controls (keyboard accessible, sliders with visible numeric value):**
- Search cost `c`: 0 to 10 gold, step 0.5, default 3.
- Low ask `L`: 10 to 200, default 80. High ask `H`: `L + 5` to 400, default 120.
- Buttons: "Simulate 1 buyer", "Simulate 100 buyers" (shows the mean paid price next to the formula value), "Let sellers respond (10 rounds)", "Reset asks".
- Presets: "Barter-like (c = 6)", "Player vendors (c = 3)", "Auction house (c = 0)".

**Seller response rule (for "Let sellers respond"):** each round, simulate 200 buyers who each check `k*` random sellers and buy from the cheapest. Then every seller who made zero sales moves their ask to `max(L, ask − 0.25 × (ask − L) − 1)`. Sellers who sold keep their ask. Redraw after each round (animate unless `prefers-reduced-motion`, then jump to the last round). Asks start uniformly spread with a seeded PRNG (mulberry32, seed 10).

**Readout next to the visual:** `k*`, expected price at `k*`, total cost at `k*`, the gain from one more check `(H − L)/((k* + 1)(k* + 2))`, and a small table of `P(sale)` for asks at L, L + 25%, L + 50%, L + 75% of the range, using `((H − p)/(H − L))^(k* − 1)`.

**Formulas:**
- `E[min] = L + (H − L)/(k + 1)`
- `total(k) = E[min] + k c`; `k* = argmin over k in 1..N`, first minimum if tied.
- `P(sale | checked) = ((H − p)/(H − L))^(k − 1)`

**Test values (L = 80, H = 120):**
- `k = 1`: 100.00; `k = 2`: 93.33; `k = 3`: 90.00; `k = 5`: 86.67; `k = 200`: 80.20.
- `c = 1`: `k* = 5`, total 91.67. `c = 3`: `k* = 3`, total 99.00. `c = 6`: `k* = 2`, total 105.33.
- `P(sale)` at `k = 3`: ask 90 → 56.25%, ask 100 → 25%, ask 110 → 6.25%.
- 100 simulated buyers at `c = 3` should show a mean paid price within about ±2 of 90.
