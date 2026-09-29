# MMO304 · Week 05 — Deflation and Hoarding

**Why this matters:** Most of the gold on a mature server isn't moving. It sits in a few veterans' banks, and it only affects prices when it starts to move. If you size your sinks by how much gold they remove, without asking whose gold, you'll hit the players who were spending and miss the hoards you were aiming at.

**You will be able to:**
- Compute a server's spending flow and effective velocity from a table of balances and spending rates, and predict the price level from them.
- Explain the three causes of deflation in a game economy and identify which one a telemetry pattern points to.
- Compare flat, proportional and luxury sinks by their effect on prices and on each group of players, not only by the gold they remove.
- Design a hoard-targeted sink and predict what happens to prices when a hoard is released instead of destroyed.

**Before class:** Lehdonvirta & Castronova, *Virtual Economies: Design and Analysis* (2014), chapter 10, "Money". Find the money velocity chart in CCP's Monthly Economic Report for January 2024 and note whether velocity moves with the money supply chart.

**Prerequisites from earlier courses:** [MMO304 week 4, money supply per capita and inflation](w04-money-supply-per-capita-and-inflation.md) (the quantity equation `M × V = P × Q` and real value). [MMO304 week 3, faucets, sinks and transformations](w03-faucets-sinks-and-transformations.md) (flow sinks and stock sinks). [GD102 week 3, positive feedback loops](../../GD102-systems-design-and-game-mechanics/lectures/w03-positive-feedback-loops-snowballing.md). [MA102 week 12, descriptive statistics](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w12-descriptive-statistics-for-playtests.md) (skew, mean and median). [MA102 week 4, expected value](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md) (weighted averages).

**Interactive:** [Hoards and sink targeting](../examples/w05-hoard-and-sink-targeting.html). Keep it open during section 2.

---

## 1. Deflation, and why games get it differently

**Deflation** is a sustained fall in the price level. The currency gains real value: the same gold buys more next week than it does today. In week 4 you used the quantity equation, `M × V = P × Q`, and fixed velocity so that prices followed money per player. Hold that equation in front of you and ask what makes `P` fall. There are only three answers.

**1. Money per player falls.** Sinks remove more than faucets add, so `n < 0` in week 4's notation. On a young server this can happen by accident, when repair costs and consumables are tuned for players who don't yet earn endgame gold. With `n = −10` a day, a player who starts at 2,000 gold is at zero after 200 days, and prices fall with them. Designers usually catch this one early, because it's loud. Players complain they can't afford to play.

**2. Goods pile up.** `Q` counts goods bought per day, but behind it sits the stock of goods that exist. Most MMO items never wear out or leave the game. Every sword crafted today is still for sale next year, next to the swords crafted since. Supply of durable goods grows while demand for them doesn't, so their prices fall. This is why many MMOs show two price levels at once: consumables inflating with money per player, and durable gear falling in price toward what it costs to vendor it. Week 8 turns item decay and destruction into a design tool for exactly this problem.

**3. Velocity falls.** Gold that nobody spends doesn't bid up prices. If players start saving instead of spending, `V` drops, and `P` drops with it even though `M` hasn't changed. Saving gold for later is called **hoarding** when it runs for a long time and involves large balances. This is the cause game designers most often misread, and it's the subject of this lecture.

### Why deflation feels worse than inflation

Players tolerate mild inflation. They hate deflation, even though it sounds like good news, because it changes what the smart move is.

If prices fall 1% a day, holding gold earns you a 1% real return per day for doing nothing. Buying a crafting material today, when it will be cheaper next week, is a loss. So players who notice deflation stop spending. That lowers `V`, which lowers prices further, which rewards holding even more. This is a positive feedback loop of the kind you met in GD102 week 3. Economists call it a deflationary spiral. In a game it shows up as an auction house full of listings and empty of buyers. Crafters, who need buyers, feel it first.

## 2. Worked example: the money that isn't moving

### The hook

On 25 December 2001, RuneScape's first Christmas event dropped Christmas crackers that gave partyhats. At the time, the RuneScape Wiki notes, partyhats and crackers were close to worthless, while some rune armour pieces were worth several hundred thousand coins. Crackers were never released again. Today a partyhat trades on the Grand Exchange for billions of coins.

Put that next to week 4's quantity equation and something looks wrong. Billions of coins are sitting in, and bid against, a few thousand hats. If `P` follows money per player, why doesn't all that wealth push up the price of food and runes? And if a designer deleted a large chunk of that wealth, would the price of food fall?

The answer is that most of that money isn't moving. To see it, split the server into groups and follow the spending, not the balances.

### The model

Divide players into groups `i`. Each group has a number of players, a total balance `B_i`, and a daily spending rate `v_i`, the share of its balance it spends per day. Then:

```
spending per day  S = Σ B_i × v_i
money supply      M = Σ B_i
effective velocity V = S / M
price level       P = S / Q
```

This is the quantity equation again, with the velocity computed from the groups instead of assumed. `V` is a weighted average of the groups' spending rates, weighted by how much money each group holds. That's the weighted average from MA102 week 4, and it's the whole point. **If the group that holds most of the money spends slowly, most of the money supply barely affects prices.**

We keep `Q = 1,000` potions a day on a server of 1,000 players, as in week 4.

### Numbers you can check

A mature server with 1,000 active players and 2,000,000 gold, so `m = 2,000`:

| Group | Players | Total balance `B` | Each holds | Spends per day `v` | Spending `B × v` |
|---|---|---|---|---|---|
| Newcomers | 500 | 200,000 (10%) | 400 | 20% | 40,000 |
| Regulars | 400 | 600,000 (30%) | 1,500 | 5% | 30,000 |
| Veterans | 100 | 1,200,000 (60%) | 12,000 | 0.5% | 6,000 |
| Server | 1,000 | 2,000,000 | mean 2,000 | `V = 3.8%` | 76,000 |

So `P = 76,000 / 1,000 = 76` gold per potion. Week 4's rule, which assumed `V = 5%` for everyone, would have predicted `P = 2,000 / 20 = 100`. The veterans hold 60% of the gold and produce 8% of the spending. Notice also that the median player, a newcomer, holds 400 gold, a fifth of the mean.

Now run four events and recompute. Each row starts from the table above.

| Event | Gold removed | `M` after | Spending `S` | `P` | Change in `P` |
|---|---|---|---|---|---|
| (a) New raid gives veterans something to buy: `v` rises to 2.5% | 0 | 2,000,000 | 100,000 | 100 | +32% |
| (b) Flat fee: every player pays 200 gold once | 200,000 | 1,800,000 | 51,900 | 51.9 | −32% |
| (c) Luxury sink: 20 veterans buy a 10,000-gold mount | 200,000 | 1,800,000 | 75,000 | 75 | −1.3% |
| (d) Luxury sink: 60 veterans buy the mount | 600,000 | 1,400,000 | 73,000 | 73 | −3.9% |

Check (b) by hand. Newcomers go from 400 to 200 each, so their balance is 100,000 and they spend 20,000. Regulars go to 1,300 each, 520,000 total, spending 26,000. Veterans go to 11,800 each, 1,180,000 total, spending 5,900. Total `S = 51,900`.

Check (c). Only the veterans' balance changes, from 1,200,000 to 1,000,000, so their spending falls from 6,000 to 5,000. Total `S = 75,000`.

Read rows (b) and (c) together. **The same 200,000 gold leaves the economy. One way cuts prices by a third. The other cuts them by 1.3%.** Row (b) also halves every newcomer's savings. Row (d) removes 30% of all the money on the server, and prices fall under 4%.

Row (a) is the mirror image. No gold enters the economy, yet prices jump 32%, because hoarded money starts moving. A hoard is inflation that hasn't happened yet.

### The visual

Open the interactive. The left panel is a stacked bar of the money supply, split into newcomers, regulars and veterans. The right panel is a stacked bar of the day's spending in the same colours, with the potion price printed above it. At the defaults, the left bar is mostly veteran colour and the right bar is mostly newcomer colour.

Use the sink controls. Set the sink size to 200,000 gold and switch its target between "every player pays the same," "proportional to balance" and "veterans only (luxury item)." The left bar shrinks by the same amount every time. The right bar, and the price, move by very different amounts. Then leave the sink at zero and drag the veterans' spending rate from 0.5% to 2.5%. The left bar doesn't change at all, and the price climbs from 76 to 100.

The two views disagree on purpose. The money supply chart tells you how much gold exists. The spending chart tells you which gold matters for prices.

### Cross-game recognition

**RuneScape, partyhats (2001 to today).** Partyhats have a fixed supply, because crackers were a one-time drop. Wealthy players park wealth in them. Buying a partyhat moves coins from one rich player to another. No coins leave the game, and none of them reach the food market. In our model, a large part of the veterans' balance is locked in trades among veterans with `v` near zero for everyone else's goods. A fixed-supply rare is a store of value, a place for hoards to live. Week 9 follows the same path to the point where an item becomes a currency.

**EVE Online (Monthly Economic Reports).** CCP publishes money velocity as its own chart next to money supply. It would only need one chart if velocity were stable. Publishing both lets players and staff see when the money supply keeps rising but the share of it being spent falls, which is row (a) of our table running backwards.

**World of Warcraft, the Brutosaur (Battle for Azeroth, patch 8.0.1).** The Mighty Caravan Brutosaur sold for 5,000,000 gold from vendors, a price only players with very large balances could pay. In our terms it's row (c) and (d), a sink aimed at veterans' hoards. From patch 9.0.1 it moved to the Black Market Auction House with a starting bid of 5,000,000 gold, and the Warcraft Wiki notes it usually sells at the 9,999,999 gold cap. An auction makes hoards bid against each other, which pulls out more of the gold that isn't moving for every copy sold.

**Old School RuneScape, Death's Coffer (from 25 June 2020).** Players can sacrifice tradeable items worth at least 10,000 coins and get credit worth 105% of the item's Grand Exchange price. The credit can only be spent on item reclaim fees after death and on private boss instances. The 5% bonus is a bribe to hoarders: take the valuable item you are sitting on, destroy it, and get slightly more than its market value in a currency that can only be burned on fees. It deletes both the item and, later, the fee money.

**Real economies.** Keynes described the paradox of thrift in 1936. Each household saving more is prudent, but if everyone does it at once, spending falls and so do incomes. The quantity equation shows the same effect through `V`.

### Eyes-open design judgment

- **Measure a sink by what it does to prices and to each group, not by gold removed.** The dashboard number "200,000 gold removed today" can describe row (b) or row (c). They are opposite policies.
- **Flat sinks fall on the players who spend.** Repair costs, travel fees and one-off charges are the same for everyone, so they take the largest share of the smallest balances. They're good at slowing `m` (week 3) and bad at touching hoards.
- **Luxury sinks are opt-in and mostly miss the price level.** That's good if you want to shrink the hoard, the "inflation that hasn't happened yet," without hurting current prices. It's useless if you want potion prices to fall today.
- **A hoard released is worse than a hoard kept.** Content that suddenly gives veterans something to buy is row (a). If you plan a patch with a big new gold sink, the gold spent on it disappears, which is fine. If you plan a patch that makes veterans' gold useful for player-made goods, expect a price jump on those goods.
- **Forced wealth taxes are rare for a reason.** A proportional sink on balances (week 3's stock sink applied to savings) targets hoards directly, but players experience it as losing gold for doing nothing. Most designers prefer to tax transactions and sell luxuries, and let hoarders choose to pay.
- **Hoarding isn't a bug.** Saving for a big goal is a satisfying long loop for many players. The designer's job is to give the hoard a destination that ends in a sink.

### Check yourself (worked example)

1. Using the base table, the veterans' spending rate falls from 0.5% to 0.1% a day. What happens to `P` and to effective velocity `V`?
2. A designer must remove 300,000 gold. Option A charges every player 300 gold (newcomers can pay at most what they hold). Option B sells 30 veterans a 10,000-gold housing plot. Compute `P` after each.
3. Starting from the base table, veterans spend 2.5% a day for a week because of a new raid, and a luxury sink removes 600,000 gold from them on the same day. Compute `P`.

<details>
<summary>Answers</summary>

1. Veteran spending falls from 6,000 to 1,200. `S = 71,200`, so `P = 71.2` (−6.3%). `V = 71,200 / 2,000,000 = 3.56%`.
2. Option A: newcomers have 400 each, pay 300, keep 100: balance 50,000, spending 10,000. Regulars keep 1,200 each: 480,000, spending 24,000. Veterans keep 11,700 each: 1,170,000, spending 5,850. `S = 39,850`, `P ≈ 39.9`. Option B: veterans' balance falls to 900,000, spending 4,500. `S = 74,500`, `P = 74.5`.
3. Veterans' balance is 600,000, spending at 2.5% is 15,000. `S = 40,000 + 30,000 + 15,000 = 85,000`, so `P = 85`. The sink cancels part of the raid's price jump.

</details>

## 3. Hoards over time: overhang and dormant gold

The table in section 2 is a snapshot. Over months, three things change the size and behaviour of hoards.

### Dormant accounts

A player who quits keeps their gold in the database. Week 3's model treated quitters as taking their money out of circulation, which is right for as long as they stay away. It isn't a sink. If 20% of your lifetime players are dormant and they held above-average balances, the gold outside circulation may be a large multiple of the gold inside it. Economists call a stock of money that could return to circulation an **overhang**.

A returning-player campaign pulls that overhang back in. Suppose 50 dormant veterans return, each with 12,000 gold, and spend at 2.5% a day while they catch up. They add `50 × 12,000 × 0.025 = 15,000` gold a day to spending. On our base server that moves `P` from 76 to 91, a 20% rise, from one marketing email.

### Measuring hoards

You can't read a hoard off total `M`. Track these instead:

- **Share of gold held by the top 10% of active players.** Rising share with flat `M` means gold is flowing toward savers.
- **Effective velocity** `V = S / M`, from logged spending. A falling `V` is the direct measure of hoarding.
- **Age of gold.** For each balance, the days since it last changed. A growing share of gold older than 90 days is a hoard, and it tells you how much could move at once.
- **Dormant gold.** The total held by accounts that are not active. This is your overhang.

### Hoarding and deflation together

When `V` falls, prices fall (section 1, cause 3). Falling prices reward holding (the spiral). Hoarding is therefore both a cause of deflation and a response to it. The designer's lever is to give savers a reason to spend that ends in a sink: a luxury item, a prestige cosmetic, a housing plot, a guild hall. Each of these moves gold from a low-`v` group to nowhere, which shrinks the overhang without raising anyone's prices.

## 4. Deflation in item prices

The same logic applies to items, with the roles swapped. Here the durable goods are the hoard.

Imagine a sword crafted at a rate of 50 a day. New players who need one arrive at 30 a day. Nobody destroys swords. Every day, 20 more swords exist than there are buyers for. Listings pile up on the auction house, sellers undercut each other, and the sword's price falls toward the highest guaranteed buyer, usually an NPC vendor price or a salvage value.

In Old School RuneScape, High Level Alchemy is that guaranteed buyer for many items. It pays 60% of an item's listed value in coins. When an item's market price falls below that, players buy it and cast the spell, so alchemy puts a floor under the price. Look at what that floor does to the money supply, though. Each alched item is new gold entering the game. A market that falls to an NPC floor turns surplus items into a faucet. Week 6 treats this floor with supply and demand curves, and week 8 covers the other fix, taking items out of the game.

## In-class activity (25 minutes)

In groups of three, you are the economy team for a server with this snapshot, `Q = 2,000` potions a day:

| Group | Players | Balance each | Spending rate |
|---|---|---|---|
| New | 1,200 | 300 | 25% |
| Regular | 600 | 2,000 | 6% |
| Veteran | 200 | 20,000 | 0.4% |

1. Compute `M`, `S`, effective `V` and `P`.
2. Your producer wants `M` down by 10% this quarter, with `P` falling by no more than 3%. Design a sink that does it. Name the in-game item or fee, who pays, and the exact amount. Show the new `P`.
3. A returning-player event is planned for the same quarter: 100 dormant veterans with 20,000 gold each, spending 2% a day. Compute the new `P` with your sink in place. Is your sink enough?
4. One sentence: what dashboard number would warn you, a week ahead, that step 3 is going badly?

Expected output: the numbers from steps 1 to 3, the sink design, and the metric.

<details>
<summary>Instructor check values</summary>

1. `M = 360,000 + 1,200,000 + 4,000,000 = 5,560,000`. `S = 90,000 + 72,000 + 16,000 = 178,000`. `V ≈ 3.2%`. `P = 89`.
2. Removing the 556,000 from veterans only (for example 56 veterans buying a 10,000-gold guild hall, 560,000) leaves veteran balance 3,440,000, spending 13,760, `S = 175,760`, `P ≈ 87.9` (−1.3%). A flat 278-gold fee on everyone would drop newcomers to 22 each and give `S ≈ 84,370`, `P ≈ 42`, a fall of more than half.
3. Returning veterans add `100 × 20,000 × 0.02 = 40,000` spending. With the step 2 sink, `S = 215,760`, `P ≈ 107.9`, about 21% above the starting 89. The luxury sink doesn't offset a hoard release. Pairing the event with a sink aimed at returning players (for example a catch-up vendor for gear) does.
4. Effective velocity, or spending by the returning cohort, rising faster than planned.

</details>

## Common misconceptions

- **"Removing gold always lowers prices."** Only gold that would have been spent. A sink on idle balances barely moves prices.
- **"If `M` is flat, prices are flat."** Prices follow spending. `M` can stay flat while velocity rises and prices jump, as in row (a).
- **"Deflation is good for players because things get cheaper."** It rewards holding over spending and starves crafters of buyers. The spiral can empty an auction house.
- **"Quitting players remove their gold."** Dormant gold is still in the database. It's an overhang that returns when they do.

## Check yourself

1. Two servers have the same `M = 3,000,000` and `Q = 1,500`. On server A, all players spend 4% a day. On server B, 70% of the gold is held by players who spend 0.5% a day and the rest by players who spend 12% a day. Compute `P` on each.
2. Explain, using `M × V = P × Q`, why a patch that adds a powerful new crafted item can raise prices across the auction house without any change to faucets or sinks.
3. A sword is crafted 80 times a day and bought 50 times a day, and swords never break. An NPC buys swords for 150 gold. What happens to the sword's price over time, and what does the NPC do to the money supply once the floor is reached?
4. Rank these sinks by how much they lower `P` per gold removed, from most to least: a 5% transaction tax on potion sales, a 10,000-gold guild hall, repair costs. Justify the ranking with the model.

<details>
<summary>Answers</summary>

1. A: `S = 120,000`, `P = 80`. B: `2,100,000 × 0.005 + 900,000 × 0.12 = 10,500 + 108,000 = 118,500`, `P = 79`. Similar prices, very different structures. On B a small rise in the hoarders' spending moves prices far more.
2. The new item gives savers something to buy, so `V` rises. With `M` and `Q` fixed, `P` rises. Hoarded gold enters circulation.
3. Supply exceeds demand by 30 a day, so the price falls until it reaches 150, where the NPC takes the surplus. At the floor, 30 swords a day turn into `30 × 150 = 4,500` new gold a day, a new faucet.
4. Repair costs first (paid by active players, including newcomers, out of gold that would be spent), then the transaction tax (paid by people who are spending, in proportion to spending), then the guild hall (paid by savers from idle gold). The ranking is the order of the payers' spending rates.

</details>

## Lab / assignment hook

[Lab 05, sink targeting](../labs/lab05.md). You build the group model in a spreadsheet, load a supplied snapshot of a server's balances, and compare four sink packages by their effect on prices and on each group. The lab counts toward the Models component (30%).

## Sources

- RuneScape Wiki, "Christmas cracker" (RuneScape). Released 25 December 2001; discontinued; notes that partyhats were near worthless at the time of the drop while some rune items were worth several hundred thousand coins; current Grand Exchange prices in the billions.
- CCP Games, "Monthly Economic Report, January 2024" (EVE Online). Separate money supply and money velocity charts.
- Warcraft Wiki, "Reins of the Mighty Caravan Brutosaur". 5,000,000 gold from vendors from patch 8.0.1 (2018); moved to the Black Market Auction House in patch 9.0.1 (13 October 2020) with a 5,000,000 gold starting bid, usually selling at 9,999,999 gold.
- Old School RuneScape Wiki, "Death's Coffer". Introduced 25 June 2020; items worth at least 10,000 coins give 105% of their Grand Exchange price as coffer value, usable only for reclaim fees and private boss instances.
- Old School RuneScape Wiki, "High Level Alchemy" (60% of item value) and "Item sink" (alchemy named as an inflation source).
- Keynes, J. M. (1936). *The General Theory of Employment, Interest and Money*. Macmillan. The paradox of thrift.
- Lehdonvirta, V. & Castronova, E. (2014). *Virtual Economies: Design and Analysis*. MIT Press.

## Interactive spec: examples/w05-hoard-and-sink-targeting.html

**The one insight the visual must make obvious:** the money supply and the spending flow respond to different things. The same gold removed can move prices by a third or by one percent, depending on whose gold it is, and prices can jump with no new gold at all.

**Model (static snapshot, recomputed on every control change).**
Three groups, each with `players_i`, `each_i` (balance per player) and `v_i` (share spent per day). `Q` = potions per day.
```
B_i = players_i × each_i
M = Σ B_i
S = Σ B_i × v_i
V = S / M
P = S / Q
```
Sink of size `X` gold with a target mode, applied before computing `S`:
- "Flat per player": each player pays `min(each_i, X / totalPlayers)`. If some players can't pay the full share, show the shortfall and do not redistribute it.
- "Proportional to balance": each balance is multiplied by `(1 − X / M)`.
- "Veterans only (luxury)": `B_vet` falls by `min(X, B_vet)`; other groups unchanged.
Returning players: `R` dormant veterans with balance `each_vet` each, spending `v_return`, added as a fourth group (default `R = 0`).

**Layout.** Two panels side by side on desktop, stacked on mobile, with shared group colours and a legend.
- Left: "Where the gold is." One stacked horizontal bar of `M` by group, before (outline) and after (filled) the sink.
- Right: "Where the spending is." One stacked bar of `S` by group, before and after, with `P` and its percent change printed large above it.
- Readout table: `M`, `S`, `V` (percent, 2 decimals), `P` (1 decimal), percent change in `P` against the no-sink baseline, and each group's balance per player after the sink.

**Controls.**
- Per group: players, balance each, spending rate (sliders with numeric inputs). Defaults: newcomers 500 / 400 / 20%; regulars 400 / 1,500 / 5%; veterans 100 / 12,000 / 0.5%. Spending-rate sliders from 0% to 30% (step 0.1%).
- Sink size `X`: 0 to 1,000,000, step 10,000, default 0.
- Sink target: three radio buttons (flat, proportional, veterans only).
- Returning veterans `R`: 0 to 200, default 0; their spending rate: 0% to 5%, default 2.5%.
- `Q`: fixed at 1,000 (show it).
- Presets reproducing each row of the lecture table: "Base", "(a) New raid", "(b) Flat fee 200k", "(c) Luxury 200k", "(d) Luxury 600k", "Returning 50".

**Test values.**
- Base: `M = 2,000,000`, `S = 76,000`, `V = 3.80%`, `P = 76.0`.
- (a) veteran `v = 2.5%`: `S = 100,000`, `P = 100.0` (+31.6%).
- (b) flat, `X = 200,000`: balances each 200 / 1,300 / 11,800; `S = 51,900`, `P = 51.9` (−31.7%).
- (c) veterans only, `X = 200,000`: `S = 75,000`, `P = 75.0` (−1.3%).
- (d) veterans only, `X = 600,000`: `S = 73,000`, `P = 73.0` (−3.9%).
- Proportional, `X = 600,000`: `S = 53,200`, `P = 53.2`.
- Returning 50 (no sink): extra spending 15,000, `S = 91,000`, `P = 91.0`.

**Accessibility and style.** Shared palette from `templates/interactive-tokens.css`, plus a pattern fill per group so the bars work without colour. All controls keyboard operable with visible focus. A live text summary, for example "Removed 200,000 gold (10% of money). Prices fell 1.3%. Veterans paid all of it." No game art or logos.
