# MMO304 · Week 06 — Supply, Demand and Equilibrium in Auction Houses

**Why this matters:** Every patch you ship moves a supply curve or a demand curve, and the auction house reports the result within hours. If you can draw the two curves, you can predict the new price before the patch goes live, say who pays your market fees, and spot when an NPC price is quietly printing gold.

**You will be able to:**
- Build supply and demand curves from players' values and costs, and compute the equilibrium price and quantity, both from a list and from straight-line curves.
- Compute how a seller-side market fee splits between buyers and sellers, the gold it removes, and the trades it prevents.
- Predict the new equilibrium after a patch shifts demand or supply, using elasticity to say which side moves the price more.
- Identify NPC buy and sell prices as floors and ceilings, and compute the gold they add or remove each day.

**Before class:** Lehdonvirta & Castronova, *Virtual Economies: Design and Analysis* (2014), chapter 4, "Supply and Demand". Read the Old School RuneScape Wiki page "Grand Exchange," sections on offers and the tax.

**Prerequisites from earlier courses:** [MMO304 week 2, functional, hedonic and social value](w02-functional-hedonic-and-social-value.md) (willingness to pay). [MMO304 week 4, money supply per capita and inflation](w04-money-supply-per-capita-and-inflation.md) (percentage sinks and faucets). [MMO304 week 5, deflation and hoarding](w05-deflation-and-hoarding.md) (items piling up toward an NPC floor). [MA101 week 2, linear functions and rates](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w02-linear-functions-and-rates.md) (slopes and where two lines cross). [GD102 week 7, converters and traders in an internal economy](../../GD102-systems-design-and-game-mechanics/lectures/w07-internal-economies-sources-drains-converters.md).

**Interactive:** [Who pays the auction house fee?](../examples/w06-market-tax-incidence.html) Keep it open during section 2.

---

## 1. From players to curves

In week 2 you met **willingness to pay**, the most gold a player would give up for an item. Every buyer on the auction house has one. Every seller has the mirror image, a **reservation price**, the least they would accept. For a gatherer it's roughly what the time was worth. For a player clearing their bags, it may be the NPC vendor price.

### Demand from a list of buyers

Line up ten buyers for a healing flask, each wanting one, by willingness to pay: 150, 140, 130, 120, 110, 100, 90, 80, 70, 60 gold.

At a price of 125, four buyers want one (150, 140, 130 and 120 are above 125). At 95, six want one. Plot "number of buyers who want one" against price and you get a staircase that steps down to the right. That staircase is the **demand curve**. It slopes down because lower prices bring in buyers who value the item less.

### Supply from a list of sellers

Now ten sellers, each with one flask, by reservation price: 45, 55, 65, 75, 85, 95, 105, 115, 125, 135.

At 100, six sellers are willing (45 through 95). At 120, eight are. Plot it and you get a staircase that steps up to the right. That's the **supply curve**. It slopes up because higher prices bring in sellers with higher costs.

### Equilibrium

The **equilibrium** is the price where the number of willing buyers equals the number of willing sellers. Walk the price down from the top:

| Price | Buyers willing | Sellers willing | Result |
|---|---|---|---|
| 120 | 4 | 8 | Too many listings. Sellers undercut. |
| 105 | 5 | 7 | Still too many listings. |
| 98 | 6 | 6 | Balanced. |
| 92 | 6 | 5 | Buyers can't find a flask. Price rises. |

Any price from 95 to 100 clears this market with six trades. Below 95, the sixth seller walks away. Above 100, the sixth buyer walks away.

The six trades that happen are the right six, in a precise sense. They pair the six buyers who value flasks most with the six sellers who can supply them most cheaply. The gain from each trade is the buyer's value minus the seller's cost. Summed over the six trades, it's `(150 + 140 + 130 + 120 + 110 + 100) − (45 + 55 + 65 + 75 + 85 + 95) = 750 − 420 = 330` gold. Economists call this **total surplus**. No other set of trades between these twenty players produces more. The auction house finds the best outcome without anyone planning it, as long as buyers and sellers can see each other's prices.

### Straight-line curves

With thousands of players, the staircase smooths into a line. Week 7 already used this form of demand:

```
Q_d = a − b × P        (quantity demanded per day)
Q_s = c + d × P        (quantity supplied per day)
```

- `a` is how many players would take one if it were free, and `b` is how many fewer want one per gold of price.
- `c` is how many would be supplied at a price of zero (items people would dump anyway), and `d` is how many more are supplied per gold of price.

Set `Q_d = Q_s` and solve, which is finding where two lines cross from MA101 week 2:

```
P* = (a − c) / (b + d)
Q* = a − b × P*
```

For the rest of the lecture we use `a = 1,000`, `b = 5`, `c = 100`, `d = 4`. Then `P* = 900 / 9 = 100` gold and `Q* = 500` flasks a day.

## 2. Worked example: who pays the auction house cut?

### The hook

World of Warcraft's auction house takes 5% of every winning bid, and the money comes out of the seller's payment. In 2025 two other big games raised their market taxes. Old School RuneScape doubled its Grand Exchange tax from 1% to 2% on 29 May 2025, and EVE Online raised its base sales tax from 4% to 7.5% on 12 March 2025. In all three games the fee is charged to the seller.

So the question sounds simple. When the seller's fee doubles, do sellers lose the whole increase? Most players assume so. The model says no. Part of the fee lands on buyers, through a higher price, and the size of that part has nothing to do with who the game charges.

### The model

A seller-side fee at rate `t` means a sale at price `P` pays the seller `P × (1 − t)`. Sellers decide how much to supply based on what they receive, so the supply curve becomes:

```
Q_s = c + d × P × (1 − t)
```

Buyers still pay `P`, so demand is unchanged. Set them equal:

```
P(t)     = (a − c) / (b + d × (1 − t))       price buyers pay
P_s(t)   = P(t) × (1 − t)                    price sellers receive
Q(t)     = a − b × P(t)                      trades per day
sink(t)  = t × P(t) × Q(t)                   gold removed per day
```

The fee opens a **wedge** of `t × P` between what the buyer pays and what the seller receives. Compare both prices with the no-fee price `P*` to see who bears it. The buyer bears `P(t) − P*`. The seller bears `P* − P_s(t)`. Economists call this split the **incidence** of the tax.

With straight-line curves the split comes out in a very clean form. The buyer's share of the wedge is

```
buyer share = d / (b + d)
seller share = b / (b + d)
```

Look at what isn't in that formula: the letter `t`, and any mention of who the fee is charged to. **The side that is less flexible pays more.** If buyers barely respond to price (small `b`), they pay most of the fee. If sellers barely respond (small `d`), sellers do.

The fee also costs something beyond the gold it collects. Trades that were worth making at `P*` no longer happen, because the wedge makes them unprofitable. The surplus those trades would have created is lost to everyone. Economists call it **deadweight loss**. For small fees it's close to the triangle `½ × wedge × (Q* − Q(t))`.

### Numbers you can check

With `a = 1,000`, `b = 5`, `c = 100`, `d = 4`:

| Fee `t` | Buyer pays `P` | Seller gets `P_s` | Trades `Q` | Buyer's part of wedge | Seller's part | Gold removed per day | Deadweight loss per day |
|---|---|---|---|---|---|---|---|
| 0% | 100.00 | 100.00 | 500.0 | — | — | 0 | 0 |
| 2% | 100.90 | 98.88 | 495.5 | 0.90 | 1.12 | 1,000 | 4.5 |
| 5% | 102.27 | 97.16 | 488.6 | 2.27 | 2.84 | 2,499 | 29.1 |
| 10% | 104.65 | 94.19 | 476.7 | 4.65 | 5.81 | 4,989 | 121.7 |

Check the 5% row by hand. `P = 900 / (5 + 4 × 0.95) = 900 / 8.8 = 102.27`. `P_s = 102.27 × 0.95 = 97.16`. `Q = 1,000 − 5 × 102.27 = 488.6`. The wedge is `102.27 − 97.16 = 5.11`, and the buyer's part is `2.27 / 5.11 = 44.4%`, which is `4 / 9`. Gold removed is `0.05 × 102.27 × 488.6 ≈ 2,499`.

Three things to notice:

- **The split is the same in every row.** Buyers always pay 4/9 of the wedge and sellers 5/9, at 2%, 5% or 10%.
- **The gold removed grows almost in proportion to `t`.** Double the fee from 5% to 10% and the sink roughly doubles, from 2,499 to 4,989 gold a day.
- **The lost trades grow much faster.** Deadweight loss goes from 29 to 122 gold a day, roughly four times. It grows with the square of the fee, because both the wedge and the missing quantity grow with `t`.

Now change who is flexible. Take a raid flask that raiders must have, with `a = 600`, `b = 1` (demand barely responds to price), and the same supply. At a 5% fee the price rises from 100 to 104.17 and sellers get 98.96. Buyers pay `d / (b + d) = 4/5 = 80%` of the wedge. Take a cosmetic dye that nobody needs, with `a = 2,500`, `b = 20`. The price rises only to 100.84 and sellers get 95.80. Buyers pay `4 / 24 = 16.7%`.

The same 5% fee, charged to the same side, falls mostly on raiders in one market and mostly on sellers in the other.

### The visual

Open the interactive. The left panel is the market: the demand line, the supply line before the fee (faded) and after it (solid), and a vertical bar at the new quantity showing the wedge between `P` and `P_s`. The right panel is a single bar split into two colours, the buyer's part and the seller's part of the wedge, with the gold removed and the deadweight loss printed below.

Drag the fee from 0% to 20%. On the left, the solid supply line swings up and the wedge grows. On the right, the bar grows, but the split between the colours doesn't move at all. Now drag the demand slope `b` down toward 1. The left panel's demand line turns steep, and on the right the buyer's colour takes over the bar. The fee rate controls how big the wedge is. The slopes control who pays it.

Finally, flip the switch "charge the fee to buyers instead." The curves on the left redraw, but `P`, `P_s`, `Q` and the split on the right stay exactly the same. Who the game charges changes the label on the receipt, not the outcome.

### Cross-game recognition

Rewrite each game's fee as a seller wedge `t` and the analysis carries over.

**World of Warcraft (retail).** The auction house keeps 5% of the winning bid, so `t = 0.05`. A deposit is also charged when listing, based on the item's vendor price and the listing length (15%, 30% or 60% of vendor price for 12, 24 or 48 hours), and the seller gets it back if the item sells. The deposit only bites on unsold listings, so it acts on listing behaviour, not on completed trades.

**Old School RuneScape (current).** The Grand Exchange tax is 2% since 29 May 2025, so `t = 0.02`. It rounds down, which means items under 50 coins pay nothing, and it's capped at 5 million coins per item, so for a very expensive item the effective `t` is lower than 2%. The wiki notes that most of the tax is removed from the game, which makes the "gold removed" column a true sink.

**EVE Online (current).** A seller in an NPC station pays the sales tax, 7.5% base since 12 March 2025, plus a broker's fee on the order, 3% base. At base skills the wedge is about `t = 0.105`. With Accounting V and Broker Relations V it falls to `0.03375 + 0.015 ≈ 0.049`, before standings. Because training changes `t` per player, EVE's sellers don't all face the same wedge, so the most skilled traders can undercut everyone else and still net more.

**Real economies.** Economists separate the **statutory incidence** of a tax (who the law says pays) from its **economic incidence** (who ends up poorer). The standard result, which you just derived, is that economic incidence depends on the slopes, not on the statute. Sales taxes, payroll taxes and tariffs all follow it.

### Eyes-open design judgment

- **A market fee is two tools at once.** It's a sink (weeks 3 and 4) and a tax on trading. Size it for the sink you need, then check the trades it prevents. At game-sized rates of 2% to 10%, the lost trades are small next to the gold removed. Past 20% or so they grow fast.
- **Decide who you want to pay, then check the slopes.** If your sink is meant to fall on high-income raiders, fees on must-have raid consumables do that automatically. If you meant to tax crafters, a fee on the same goods mostly misses them.
- **Charging buyers or sellers is a presentation choice.** Pick the side that makes the fee easier to understand in the interface. Players complain about the fee they see. The math doesn't care.
- **Caps and rounding change the effective rate.** A capped fee like the Grand Exchange's 5 million coins is regressive at the top: the richest trades pay the lowest percentage. That may be deliberate, to keep rare-item trading on the exchange, but decide it knowingly.
- **Different fees for different players create a hierarchy.** EVE's skill-reduced taxes reward traders who invest in the profession. A flat fee for everyone makes trading a side activity. Neither is wrong. They produce different games.

### Check yourself (worked example)

1. With `a = 1,000`, `b = 5`, `c = 100`, `d = 4`, compute `P`, `P_s`, `Q` and the gold removed at a 20% fee. What share of the wedge do buyers pay?
2. A designer wants a potion market to remove 3,000 gold a day with the curves above. Estimate the fee rate needed, and say whether the lost trades are a concern.
3. Supply of an ore is very rigid (`d = 1`) because only a few players can mine it, and demand is `b = 5`. At a 10% fee, what share of the wedge falls on the miners?

<details>
<summary>Answers</summary>

1. `P = 900 / (5 + 3.2) = 109.76`, `P_s = 87.80`, `Q = 451.2`, removed `0.2 × 109.76 × 451.2 ≈ 9,905` gold. Buyers still pay `4/9 ≈ 44%`.
2. Removal is about `2,500 × t / 5%`, so 3,000 needs about 6%. Check: `P = 900 / (5 + 3.76) = 102.74`, `Q = 486.3`, removed `0.06 × 102.74 × 486.3 ≈ 2,998`. Deadweight loss is about `½ × 6.16 × 13.7 ≈ 42` gold a day, small next to the 3,000 removed.
3. Seller share `= b / (b + d) = 5/6 ≈ 83%`. The miners bear most of it.

</details>

## 3. Patch day: shifting the curves

Most price changes in an MMO don't come from fees. They come from patches that move a whole curve.

A **demand shift** changes how many players want the item at every price. A new raid that requires a flask adds buyers at every price, so `a` rises. A **supply shift** changes how many are offered at every price. A drop-rate buff to the herb in the flask recipe lowers costs, so `c` rises.

| Patch | Change | New `P*` | New `Q*` |
|---|---|---|---|
| Baseline | `a = 1,000`, `c = 100` | 100 | 500 |
| New raid needs the flask | `a = 1,180` | 120 | 580 |
| Herb drop rate buffed | `c = 280` | 80 | 600 |
| Both in the same patch | `a = 1,180`, `c = 280` | 100 | 680 |

Check the raid row: `P* = (1,180 − 100) / 9 = 120`. The last row is a useful lesson for patch notes. If you ship a new raid and a herb buff together, the flask price may not move at all, while trading volume rises 36%. A dashboard that only watches price would report "no effect."

### Elasticity: which side moves the price

How far a shift moves the price depends on the slopes. The **price elasticity** of demand at a point is the percentage change in quantity for a 1% change in price. For a straight line, it's `b × P / Q`. At our baseline, demand elasticity is `5 × 100 / 500 = 1.0` and supply elasticity is `d × P / Q = 4 × 100 / 500 = 0.8`.

- Goods with **inelastic** demand (elasticity well below 1), like must-have raid consumables, show large price swings when supply shifts. Nerf the herb and flask prices spike.
- Goods with **elastic** demand, like cosmetics and convenience items, show small price changes and large volume changes.

This is the same pair of slopes that decided who pays the fee in section 2. The flexible side absorbs shocks by changing quantity. The rigid side absorbs them through price.

## 4. NPC prices: floors and ceilings

Many MMOs put an NPC on one side of the market. That NPC changes the supply and demand picture in a way that matters for the money supply.

### An NPC buyer is a price floor, and a faucet

If an NPC buys flasks for 90 gold without limit, no player will sell below 90. The market price can't fall below the NPC's price. That's a **price floor**.

Take the herb-buff patch, where the market price would fall to 80. With an NPC floor at 90:

```
Q_d at 90 = 1,000 − 5 × 90 = 550
Q_s at 90 = 280 + 4 × 90 = 640
sold to the NPC = 640 − 550 = 90 flasks a day
new gold = 90 × 90 = 8,100 gold a day
```

When a market sits on an NPC floor, the surplus goes to the NPC, and the NPC pays in freshly created gold. **An NPC buy price is a faucet that switches on when supply outruns demand.** Old School RuneScape's High Level Alchemy, which turns an item into 60% of its listed value in coins, works like this. When an item's market price falls below its alchemy value, players buy it and cast the spell. The OSRS Wiki's page on item sinks names alchemy as one of the inflation sources that coin sinks have to offset. Week 5 showed durable items drifting down toward such a floor. This is where they land, and where they start printing money.

### An NPC seller is a price ceiling, and a sink

The mirror case: an NPC sells flasks for 110 gold without limit. No player will pay more than 110, so the market price can't rise above it. That's a **price ceiling** backed by the NPC. If demand shifts up so far that the market price would pass 110, players buy the excess from the NPC and the gold they pay leaves the economy. **An NPC sell price is a sink that switches on when demand outruns supply.** Starter gear sold by vendors (week 4) is this kind of ceiling.

### A ceiling with no NPC behind it creates a shortage

Some games cap prices by rule rather than with an NPC. If the rule says no flask may trade above 90, but nobody stands ready to sell at 90:

```
Q_d at 90 = 550
Q_s at 90 = 460
shortage = 90 flasks a day
```

Ninety buyers a day can't find a flask. Sellers who know the item is worth more stop listing it on the exchange and trade it elsewhere, often through side deals that the exchange can't see. Week 13's Grand Exchange case study follows one such cap through its history.

## In-class activity (30 minutes)

A pit market, run by the instructor. You need a deck of 20 cards, printed or handwritten, and a whiteboard.

- Ten **buyer** cards, one value each: 150, 140, 130, 120, 110, 100, 90, 80, 70, 60.
- Ten **seller** cards, one cost each: 45, 55, 65, 75, 85, 95, 105, 115, 125, 135.

Each student draws one card and keeps it private. With more than 20 students, use two decks and two pits.

1. **Round 1, no fee (8 minutes).** Buyers and sellers walk around and make deals out loud. A buyer earns `value − price`. A seller earns `price − cost`. Nobody may trade at a loss. When a pair agrees, they report the price to the instructor, who writes it on the board.
2. **Round 2, a 10% seller fee (8 minutes).** Redraw cards and repeat. Sellers now earn `0.9 × price − cost`.
3. **Debrief (14 minutes).** Compare the number of trades and the average price in the two rounds with the predictions below. Which buyer and seller pairs dropped out? Who complained about the fee, and who actually paid it?

Expected output: a board with both rounds' prices, the count and average of each round, and one sentence per group explaining any gap from the prediction.

<details>
<summary>Instructor predictions</summary>

Round 1: six trades, prices converging to between 95 and 100, total surplus 330. Round 2: a seller with cost 95 needs `95 / 0.9 = 105.6` and no remaining buyer values the flask that highly, so five trades, prices between about 100 and 105.6. The lost trade is the buyer valuing 100 with the seller costing 95, a surplus of 5. The fee collects about 50 gold. Real rounds scatter around these numbers, and the first few trades are usually far off. Point out how quickly the price range narrows, and that the buyers paid part of the fee although only sellers were charged.

</details>

## Common misconceptions

- **"The seller pays the seller's fee."** The seller is charged. Buyers pay part of it through a higher price, and the split depends on the slopes.
- **"A higher fee means proportionally fewer trades."** Lost trades grow roughly with the square of the fee. Small fees cost almost nothing in trades. Large ones cost a lot.
- **"If the price didn't change after a patch, nothing changed."** Demand and supply can shift together. Watch volume as well as price.
- **"NPC vendors are neutral."** An NPC buyer creates gold whenever the market sits on its floor. An NPC seller removes gold whenever the market sits on its ceiling. Each is a faucet or a sink that turns on only under certain market conditions.

## Check yourself

1. Demand is `Q_d = 800 − 4P` and supply is `Q_s = 50 + 6P`. Find the equilibrium. A 5% seller fee is added. What share of the wedge do buyers pay, and what is the new price?
2. In the pit market, a buyer with value 100 and a seller with cost 95 are the sixth pair. Explain why the 5% fee leaves them able to trade but the 10% fee doesn't.
3. With the lecture's baseline curves, an NPC buys flasks at 105. What happens to the market, and how much gold does the NPC create per day?
4. A designer proposes lowering the auction house cut from 5% to 1% "to help crafters." Using the lecture's baseline curves, how much does the seller's received price change, and what happens to the sink?

<details>
<summary>Answers</summary>

1. `P* = (800 − 50) / 10 = 75`, `Q* = 500`. Buyer share `= d / (b + d) = 6/10 = 60%`. New `P = 750 / (4 + 6 × 0.95) = 750 / 9.7 ≈ 77.32`.
2. The seller needs `95 / 0.95 = 100` at a 5% fee, which the buyer can just pay. At 10% the seller needs `105.6`, above the buyer's value of 100, so no price works for both.
3. The market price would be 100, below the floor, so the price rises to 105. Buyers want `1,000 − 525 = 475`. Sellers offer `100 + 420 = 520`. The NPC takes 45 a day, creating `45 × 105 = 4,725` gold a day.
4. At 1%, `P = 900 / (5 + 3.96) = 100.45` and `P_s = 99.44`, against `97.16` at 5%. Sellers gain about 2.28 gold per flask, and buyers save `102.27 − 100.45 = 1.82`. The sink falls from about 2,499 to about 500 gold a day. Crafters gain, but so do buyers, and the economy loses 2,000 gold a day of sink that must be replaced elsewhere.

</details>

## Lab / assignment hook

[Lab 06, estimating a market from auction data](../labs/lab06.md). You fit straight-line supply and demand to a supplied week of auction listings and sales for one item, predict the effect of a fee change and a patch, and compare your prediction with the "after" data. The lab counts toward the Models component (30%).

## Sources

- Warcraft Wiki, "Auction House" (current retail). The house keeps 5% of the winning bid; deposits of 15%, 30% or 60% of vendor price for 12, 24 or 48 hours, returned on sale.
- Old School RuneScape Wiki, "Grand Exchange" (current). Tax 1% from 9 December 2021 and 2% from 29 May 2025, rounded down (no tax below 50 coins), capped at 5 million coins per item; most revenue removed from the game; offers matched against the best existing opposite offer.
- EVE University Wiki, "Trading" (current). Sales tax 7.5% base since version 22.02 (12 March 2025), up from 4%, 7.5% × (1 − 0.11 × 5) = 3.375% at Accounting V; broker's fee 3% base, 1.5% at Broker Relations V.
- Old School RuneScape Wiki, "High Level Alchemy" (60% of item value; players buy items below alchemy value and alch them) and "Item sink" (alchemy as an inflation source).
- Lehdonvirta, V. & Castronova, E. (2014). *Virtual Economies: Design and Analysis*. MIT Press.

## Interactive spec: examples/w06-market-tax-incidence.html

**The one insight the visual must make obvious:** the fee rate sets how big the wedge is, but the slopes of the two curves decide who pays it, and it makes no difference which side the game charges.

**Model (closed form, recomputed on every control change).**
```
Q_d = a − b × P
Q_s = c + d × P_s
Seller-charged fee:  P_s = P × (1 − t)
  P  = (a − c) / (b + d × (1 − t))
Buyer-charged fee:   buyer pays P_b = P_s / (1 − t) (same wedge definition, so results are identical)
Q  = a − b × P
P0 = (a − c) / (b + d),  Q0 = a − b × P0
buyerPart  = P − P0
sellerPart = P0 − P_s
buyerShare = buyerPart / (P − P_s)       (= d / (b + d); show both)
sink = t × P × Q
DWL  = 0.5 × (P − P_s) × (Q0 − Q)
Elasticities at equilibrium: e_d = b × P / Q, e_s = d × P_s / Q
```
Floor mode: if an NPC buy price `F` is set and `F > P`, the price becomes `F`; show `Q_d(F)`, `Q_s(F)`, NPC purchases `Q_s(F) − Q_d(F)` and gold created `F × (Q_s(F) − Q_d(F))` per day. Ceiling mode: if a rule caps price at `C < P` with no NPC seller, show the shortage `Q_d(C) − Q_s(C)`. If an NPC sells at `C`, show NPC sales and gold removed `C × (Q_d(C) − Q_s(C))`. Apply floor and ceiling modes with `t = 0` to keep the numbers simple (disable the fee slider while they are on and say so).

**Layout.** Two linked panels, side by side on desktop, stacked on mobile.
- Left "The market": price on the vertical axis (0 to 250), quantity on the horizontal (0 to 1,000). Demand line, supply line without fee (faded, dashed) and with fee (solid). A vertical wedge bar at `Q` from `P_s` to `P`, labelled with both values. Shade the deadweight-loss triangle. In floor or ceiling mode, draw the horizontal NPC line and shade the NPC quantity.
- Right "Who pays": a horizontal bar of length `P − P_s`, split into buyer part and seller part with percentages, then three numbers: gold removed per day, deadweight loss per day, and elasticities.
- Readout table: `P0`, `Q0`, `P`, `P_s`, `Q`, buyer share, sink, DWL (2 decimals).

**Controls.**
- Fee `t`: 0% to 30%, step 0.5%, default 5%.
- Switch "charge the fee to buyers instead" (default off).
- `a`: 200 to 3,000, step 10, default 1,000. `b`: 0.5 to 25, step 0.5, default 5.
- `c`: 0 to 500, step 10, default 100. `d`: 0.5 to 25, step 0.5, default 4.
- Floor/ceiling selector: none, NPC buyer at `F`, rule cap at `C`, NPC seller at `C`, with a price input (default 90).
- Presets: "Baseline", "Raid flask (b = 1, a = 600)", "Cosmetic dye (b = 20, a = 2,500)", "New raid (a = 1,180)", "Herb buff (c = 280)", "Herb buff with NPC floor 90", "Rule cap at 90".

**Test values.**
- Baseline, `t = 0`: `P = 100`, `Q = 500`, `e_d = 1.00`, `e_s = 0.80`.
- `t = 2%`: `P = 100.90`, `P_s = 98.88`, `Q = 495.5`, sink 1,000, DWL 4.5.
- `t = 5%`: `P = 102.27`, `P_s = 97.16`, `Q = 488.6`, buyer share 44.4%, sink 2,499, DWL 29.1.
- `t = 10%`: `P = 104.65`, `P_s = 94.19`, `Q = 476.7`, sink 4,989, DWL 121.7.
- `t = 20%`: `P = 109.76`, `P_s = 87.80`, `Q = 451.2`, sink 9,905.
- Raid flask, `t = 5%`: `P = 104.17`, `P_s = 98.96`, buyer share 80.0%.
- Cosmetic dye, `t = 5%`: `P = 100.84`, `P_s = 95.80`, buyer share 16.7%.
- New raid, `t = 0`: `P = 120`, `Q = 580`. Herb buff: `P = 80`, `Q = 600`.
- Herb buff with NPC floor 90: `Q_d = 550`, `Q_s = 640`, NPC buys 90, gold created 8,100 per day.
- Rule cap at 90 (baseline): `Q_d = 550`, `Q_s = 460`, shortage 90.
- Switching the fee to buyers leaves every number above unchanged.

**Accessibility and style.** Shared palette from `templates/interactive-tokens.css`. Buyer and seller parts use distinct colours and patterns. Every slider has a numeric input and is keyboard operable. A live text summary, for example "A 5% fee raises the price to 102.27. Buyers pay 44% of it, sellers 56%. It removes 2,499 gold a day and prevents 11 trades." Respect `prefers-color-scheme` and `prefers-reduced-motion`. No game art or logos.
