# MMO304 · Week 03 — Faucets, Sinks and Transformations

**Why this matters:** Every monster that drops gold is printing money, and every repair bill is burning it. If you do not track the two, prices on your servers will drift for months before anyone notices, and by then the fix will hurt. This week you learn to write an MMO economy as a set of flows and to predict where money per player will end up.

**You will be able to:**
- Classify every rule in an economy as a faucet, a sink, a transformation or a transfer, for both money and items.
- Write a stock-and-flow model of money supply and simulate it day by day.
- Derive the steady-state money per player from faucet, sink, tax and churn rates, and explain why sinks that scale with play cannot stop drift on their own.
- Design a sink package that holds money per player near a target, and critique its effect on players.

**Before class:** Lehdonvirta & Castronova, *Virtual Economies: Design and Analysis* (MIT Press, 2014), chapter 10, "Money". Skim one CCP *Monthly Economic Report* for EVE Online (any month from 2024 on) and find its chart of faucets and sinks.

**Prerequisites from earlier courses:** GD102 [week 2, stocks and flows](../../GD102-systems-design-and-game-mechanics/lectures/w02-stocks-and-flows.md) and [week 7, sources, drains and converters](../../GD102-systems-design-and-game-mechanics/lectures/w07-internal-economies-sources-drains-converters.md), including Machinations notation. [MA101 week 4, exponentials](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w04-exponentials-and-the-xp-curve.md) (repeated multiplication by `1 − k`). [MA101 week 2, linear functions and rates](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w02-linear-functions-and-rates.md). [Week 1 of this course](w01-why-virtual-economies-exist-artificial-scarcity.md) (the farming wage).

**Interactive:** [Faucet and sink simulator](../examples/w03-faucet-sink-simulator.html)

---

## 1. Four kinds of rule

In week 1 you saw that every price in a virtual economy traces back to rules the designer wrote. This week you sort those rules by what they do to the total amount of stuff in the world.

The **money supply**, `M`, is the total currency held by active players. It is a **stock**: a quantity that exists at a moment in time, like water in a bathtub. The rules that change it are **flows**: amounts per hour or per day, like water through a tap or a drain. You met this language in GD102 as stocks and flows, and in Machinations as sources, drains and converters. Virtual-economy designers use their own names:

- A **faucet** creates currency from nothing. Gold dropped by monsters, quest rewards, selling loot to a vendor.
- A **sink** destroys currency. Repair bills, vendor purchases, travel fees, auction-house cuts, taxes.
- A **transformation** converts one thing into another. Crafting turns ore into a sword. Buying from a vendor turns gold into an item, which is a money sink and an item faucet at once.
- A **transfer** moves currency or items between players without changing the total. Trading, gifting, mail.

The same four labels apply to items as well as money. Each item type has its own faucets (drops, crafting outputs), sinks (consumption, decay, deletion) and stock.

| Rule | Money | Items |
|---|---|---|
| Monster drops gold | Faucet | — |
| Monster drops a sword | — | Faucet |
| Sell sword to vendor | Faucet | Sink |
| Buy potion from vendor | Sink | Faucet |
| Repair armour | Sink | — |
| Craft sword from ore | — | Transformation (ore sink, sword faucet) |
| Player sells sword to player | Transfer | Transfer |
| Auction house takes 5% of the sale | Sink (the 5%) | Transfer |

The last two rows matter most for this week. Trade between players changes who holds the money, not how much exists. A market can only affect the money supply through fees and taxes. When players say "the economy is inflated", they are describing the total, and the total is set entirely by faucets and sinks.

### Why the balance matters

If faucets pour in more money than sinks remove, `M` grows. If the number of players does not grow as fast, each player holds more gold. More gold chasing the same goods means sellers can ask more, so prices rise. Week 4 builds that link in full, as the quantity theory of money. For this week we use the simplest version:

```
price of a traded good ∝ money per active player
```

In words, if money per player doubles and nothing else changes, player-set prices roughly double. That is enough to see where prices drift.

## 2. Worked example: the faucet/sink simulator

### The hook

EVE Online's developer, CCP, hired an economist in 2007, Eyjólfur Guðmundsson, to watch its in-game economy. CCP now publishes a monthly economic report, and one of its standard charts is simply a list of every faucet and every sink with the amount of currency each moved that month. A large studio treats the balance of these flows as a number worth publishing every month. Let's see why, by building the smallest possible server and watching its prices.

### The model

Time moves in days. Players join, farm gold, pay for repairs, trade with a tax, and sometimes quit.

```
N(d+1) = N(d) + J − c × N(d)

M(d+1) = M(d) + N(d) × h × (g − r) − τ × v × M(d) − c × M(d)

m(d) = M(d) / N(d)          price index P(d) = 100 × m(d) / 1,000
```

- `N` is the number of active players. `J` is new players joining per day. `c` is the share of players who quit each day.
- `M` is the money held by active players. `m = M / N` is money per player.
- `h` is hours played per player per day.
- `g` is the faucet: gold earned per hour of play (drops, quests, vendor sales).
- `r` is the **flow sink**: gold spent per hour of play (repairs, consumables, travel). It scales with play time, like the faucet.
- `τ` is the tax rate on player trades, and `v` is the share of all money that changes hands in a day. Together `τ × v × M` is a **stock sink**: it scales with the amount of money in the world, not with play time.
- The term `c × M` says quitting players take their average wealth with them. Their gold does not vanish from the database, but it leaves active circulation. New players join with zero gold.
- `P` is a price index, set to 100 when each player holds 1,000 gold.

The simulator runs these two lines for as many days as you like.

### Numbers you can check

Base server: `N = 1,000`, `J = 5` per day, `c = 0.5%` per day, so the population stays at exactly 1,000 (5 join, 5 quit). Each player plays `h = 2` hours a day, earns `g = 100` gold per hour and spends `r = 60` on repairs. So each player's net income is `2 × (100 − 60) = 80` gold a day. Everyone starts with 1,000 gold, so `P = 100` on day 0. Trade volume is `v = 5%` of all money a day.

Check day 1 by hand, with no tax. `M(0) = 1,000,000`. Add `1,000 × 80 = 80,000`. Remove `0.005 × 1,000,000 = 5,000` for quitters. `M(1) = 1,075,000` and `m(1) = 1,075`. Prices are up 7.5% after one day.

Money per player `m` (and price index `P`) at selected days, rounded:

| Scenario | Day 30 | Day 90 | Day 180 | Day 365 | Day 730 | Long-run `m*` |
|---|---|---|---|---|---|---|
| A. Base, no tax | 3,094 (309) | 6,446 (645) | 9,915 (992) | 13,593 (1,359) | 15,614 (1,561) | 16,000 |
| B. Base, 5% trade tax | 2,954 (295) | 5,757 (576) | 8,173 (817) | 10,047 (1,005) | 10,627 (1,063) | 10,667 |
| C. Repair raised to `r = 80`, no tax | 1,977 (198) | 3,542 (354) | 5,160 (516) | 6,877 (688) | 7,820 (782) | 8,000 |
| D. No new players (`J = 0`), no tax | 3,412 (341) | 8,236 (824) | 15,472 (1,547) | 30,347 (3,035) | 59,693 (5,969) | none |
| E. No new players, 5% trade tax | 3,254 (325) | 7,281 (728) | 12,289 (1,229) | 19,624 (1,962) | 27,059 (2,706) | 32,000 |

In every scenario prices rise, because each player earns more than they spend. The interesting question is where they stop.

### Where money per player stops: the steady state

When the population is constant, you can divide the money line by `N` and get one line for money per player:

```
m(d+1) = m(d) × (1 − c − τ × v) + h × (g − r)
```

Each day, a fixed amount `h × (g − r)` flows in, and a fixed *share* `c + τ × v` of the existing stock flows out. The stock stops growing when inflow equals outflow:

```
m* = h × (g − r) / (c + τ × v)
```

Check scenario A: `80 / 0.005 = 16,000`. Scenario B: `τ × v = 0.05 × 0.05 = 0.0025`, so `m* = 80 / 0.0075 = 10,667`. Scenario C halves the numerator: `40 / 0.005 = 8,000`.

The path toward `m*` is the same shape you met in MA101 week 4, run backwards. The gap between `m` and `m*` shrinks by a factor `(1 − c − τv)` each day:

```
m(d) = m* − (m* − m(0)) × (1 − c − τ × v)^d
```

For scenario A on day 365, `16,000 − 15,000 × 0.995^365 = 16,000 − 15,000 × 0.1606 ≈ 13,590`, matching the table to rounding.

### The insight: two kinds of sink

Look at scenarios C and D together. Raising repair costs (a flow sink) cut the long-run level in half in scenario C, which looks like a fix. It is not a brake. It only shrank the numerator. What stopped money per player from growing forever in scenarios A to C was the denominator, and in scenario A the only thing in it is churn `c`: new players arriving with zero gold keep diluting the average.

Scenario D removes new players. Every day the richest players remain and the population shrinks. With no stock sink, money per player grows forever, by about 80 gold a day. By day 730 prices are 60 times their starting level. A server that stops attracting new players inflates even if you changed nothing, because the dilution that was hiding the imbalance has stopped.

Scenario E adds back a stock sink, the trade tax. Now the denominator has a term that does not depend on newcomers. On a closed server the population and the wealth of quitters shrink together, so churn cancels out and the steady state becomes `m* = h × (g − r) / (τ × v) = 80 / 0.0025 = 32,000`. High, but finite.

So the rule is:

- **Flow sinks** (repairs, consumables, fees per action) scale with play, like faucets. They change the net income per hour, the numerator. As long as net income stays positive, they cannot create a ceiling alone.
- **Stock sinks** (taxes on trade, upkeep on property, anything proportional to wealth) scale with the money that exists. They create a ceiling, because they grow as the stock grows.
- **Dilution by new players** acts like a stock sink while the game is growing, and disappears when growth stops.

### The visual

Open the interactive. The top view plots `N(d)` and `m(d)` over two years. The bottom view is the price of a reference item (100 gold on day 0) and, next to it, a bar chart of today's daily flows: faucet in, flow sink out, tax out, quitters out. Start with scenario A. Drag the repair slider up and watch the whole price curve flatten, but still rise. Then set `J = 0`. The population line falls and the price line turns into a straight ramp with no top. Now raise the tax slider. The ramp bends into a curve that levels off, and the dashed line for `m*` appears. The bars show why: at the steady state the tax bar exactly matches the net faucet bar.

### Cross-game recognition

Every live MMO has these terms. The skill is recognising them under their local names and writing them in the model's form.

**World of Warcraft (long-standing rules, as documented on Warcraft Wiki).** Faucets `g`: gold from monsters, quest rewards and vendor sales. Flow sinks `r`: repairs, since equipped items lose 10% of their maximum durability when you die and more when you use a spirit healer, plus training, travel and consumables. Stock sink `τ v`: the auction house keeps a 5% cut of each winning bid, and it keeps the listing deposit when an item fails to sell. So `τ = 0.05` on the share of trade that goes through the auction house. Trades made face to face pay no tax at all, which means `v` counts only auction-house volume.

**EVE Online (market fees from 12 March 2025).** Sales tax on the market starts at 7.5% and falls by 11% of that per level of the Accounting skill, so a fully trained seller pays about 3.4%. A broker's fee of 3% at NPC stations (lower with skills and standings) applies when an order is placed. Together these form the `τ` of EVE's market, somewhere between about 4.4% and 10.5% depending on the trader's skills and standings. CCP's monthly reports chart ISK faucets (for example the bounties paid for destroying NPC pirates) against sinks like these taxes and fees, month by month. They are publishing the numerator and the stock sink of this model.

**Old School RuneScape (Grand Exchange tax, from 9 December 2021).** For years the Grand Exchange, the game's central market, charged no tax, so `τ = 0`. Jagex introduced a 1% tax on sales on 9 December 2021 and raised it to 2% on 29 May 2025, capped at 5 million coins per item, with some low-level items exempt. In our model that is a new stock sink switched on in a mature game with a large money stock, the move from scenario A to B, or D to E. Jagex also turned the tax into a transformation. Part of the collected tax funds an item sink that buys selected high-value items from players and deletes them. A sample Jagex posted on 29 May 2025, reproduced on the Old School RuneScape Wiki, lists 38,000 Bandos godswords and 399 twisted bows among the items deleted so far. That is a money sink feeding an item sink.

**Path of Exile (2013 onward).** Path of Exile's trade runs on currency items rather than gold, and those items have their own uses, such as upgrading an item's rarity or rerolling its properties. Every time a player uses one, a unit of the currency is destroyed. The currency is its own sink. In our model that puts a use-based sink directly on the money stock.

Four games, one model. For any economy, find its `g`, its `r`, its `τ` and `v`, and its population trend, and you can say whether money per player has a ceiling.

### Eyes-open design judgment

- **Players feel sinks differently.** A repair bill feels like punishment for playing. A trade tax feels fair to most players and painful to traders. A wealth or upkeep tax (EVE-style structure upkeep, housing rent) hits hoarders and can feel like theft. Voluntary luxury sinks, such as expensive cosmetics, mounts and housing items, are the friendliest because players choose them. A healthy package usually mixes several.
- **Flow sinks are for pacing, stock sinks are for the level.** Use repairs and consumables to set how fast a typical player gets richer. Use taxes, upkeep and luxury goods aimed at the rich to set where money per player levels off.
- **Plan for the end of growth.** Launch-period dilution hides imbalances. When new-player numbers fall, the same rules inflate faster. Size your stock sinks for the mature game, not the launch month.
- **Churned money is not destroyed.** Quitters' gold sits in the database. When they return, often for a new expansion, it re-enters circulation at the worst moment. Model it as a delayed faucet.
- **Beware of sinks that punish new players.** Flat fees hit a new player's 50 gold much harder than a veteran's 50,000. A percentage tax on trade falls mostly on those who trade the most, which is usually richer players.

## 3. Transformations and item economies

Money is only half of the ledger. Every item type has its own stock and flows, and transformations connect them. Four patterns matter.

### Vendors connect money to items

A vendor that buys loot is a money faucet and an item sink. A vendor that sells potions is a money sink and an item faucet. Vendor prices therefore set **floors and ceilings** on player prices. No one sells a sword to a player for less than a vendor pays for it, and no one buys a potion from a player for more than a vendor charges. In the language of week 1, the vendor fixes a price for goods the designer supplies without scarcity.

A common mistake is to treat vendor sales of loot as harmless because "the item leaves the game". The item does leave. The gold it creates stays, and adds to `g`.

### Crafting destroys inputs

Crafting is a transformation. Ten ore become one sword, so ore leaves the world. Crafting is how most games keep common materials from piling up: players keep gathering because crafting keeps consuming. Week 7 models crafting chains in detail. For now note that if the sword itself never leaves, crafting has just moved the pile-up from ore to swords. Every item stock needs a sink somewhere downstream: consumption, decay, or obsolescence (weeks 2 and 8).

### Items that behave like money

When an item is durable, easy to trade and wanted by many players, it can start to act like currency. Path of Exile designed its economy around this. Diablo II's players did it on their own, using a ring as money (week 9). Once an item is money, its faucets and sinks are part of your money supply, whether you planned it or not.

### Converting a money sink into an item sink

The Old School RuneScape item sink shows a newer pattern. The tax removes coins, and then the studio spends part of that value to buy and delete rare items, whose own stock had no natural sink. It is one rule doing two jobs: holding down money per player and propping up the price of rare drops by removing surplus copies.

## 4. Reading an economy as a ledger

To audit a real or proposed economy, write every rule into one table with its expected daily amount on a typical server. Then add up each column.

| Rule | Type | Scales with | Gold per player per day |
|---|---|---|---|
| Monster gold | Faucet | Play time | +150 |
| Quest rewards | Faucet | Play time | +50 |
| Repairs | Flow sink | Play time | −90 |
| Consumables from vendors | Flow sink | Play time | −30 |
| Auction cut, 5% on 5% of money a day | Stock sink | Money held | −0.0025 × `m` |
| New players at zero gold | Dilution | Growth | −`c` × `m` |

Here net flow per player is `150 + 50 − 90 − 30 = 80` gold a day, the same as the simulator's base case. With 0.5% daily churn, the steady state is `80 / (0.005 + 0.0025) = 10,667` gold per player, scenario B. If you want a different target, the formula tells you what to change. For example, to hold `m*` at 5,000 with the same faucets and churn, you need `c + τv = 80 / 5,000 = 0.016`, so `τv = 0.011`. At 5% daily volume that is a 22% trade tax, which players would hate. A better answer is to cut net income or add a stock sink that does not depend on trade, such as upkeep on housing.

This ledger is also the start of telemetry. In week 12 you will log each row from real servers and watch the totals.

## In-class activity (25 minutes)

In groups of three, audit an economy you know. Choose one MMO or online game the group has played.

1. List at least eight rules that create, destroy or move money. Label each as faucet, flow sink, stock sink, transformation or transfer.
2. Estimate the daily amount of each for a typical mid-level player. Guesses are fine, but write down how you guessed.
3. Compute net income per player per day, and the steady state `m*` if churn is 0.5% a day and your stock sinks are as you estimated.
4. The game's new-player numbers fall to zero next year. Recompute `m*`. If it no longer exists, propose one stock sink and the rate that gives a ceiling of 20 days of a typical player's income.

Expected output: the ledger table, two `m*` values (or "none"), and one proposed sink with its rate and a sentence on how players will feel about it.

## Common misconceptions

- **"The auction house is a big sink because huge sums move through it."** Only the fee is a sink. The rest is a transfer from buyer to seller and leaves the money supply unchanged.
- **"Selling loot to vendors removes things from the economy."** It removes the item and creates gold. For the money supply it is a faucet.
- **"If sinks match faucets at launch, the economy is stable."** Flow sinks and faucets can match while stock sinks and dilution are doing the real work. When growth stops, the balance changes without any rule changing.
- **"Raising repair costs will stop inflation."** Raising a flow sink lowers net income per hour. Unless it pushes net income to zero or below, money per player still rises; only the speed and the ceiling change, and on a closed server there is still no ceiling.

## Check yourself

1. A server has constant population, net income of 120 gold per player per day, churn 1% a day and no taxes. What is `m*`? A 4% auction cut is added and 10% of all money trades through the auction house each day. What is the new `m*`?
2. Using the base simulator (scenario A), how many days does it take for `m` to get halfway from 1,000 to 16,000?
3. A designer doubles every monster's gold drop from `g = 100` to `g = 200`, keeping `r = 60`. In scenario B, what is the new `m*`? By what factor do long-run prices change?
4. A closed server has net income of 50 gold per player per day and a 3% trade tax on a daily volume of 4% of money. What is `m*`? If the tax is removed, what happens?
5. Classify these for money and for items: (a) a player buys a mount from a vendor for 5,000 gold; (b) a player sells 20 wolf pelts to another player for 100 gold; (c) a player crafts a cloak from 20 wolf pelts; (d) the auction house keeps 5 gold from that pelt sale.

<details>
<summary>Answers</summary>

1. `m* = 120 / 0.01 = 12,000`. With the cut, `τv = 0.04 × 0.10 = 0.004`, so `m* = 120 / 0.014 ≈ 8,571`.
2. Halfway means the gap has halved: `0.995^d = 0.5`, so `d = ln 0.5 / ln 0.995 = 138.3`. The gap is not yet halved after 138 whole days, so `m` first passes 8,500 on day 139.
3. Net income becomes `2 × (200 − 60) = 280` gold a day. `m* = 280 / 0.0075 ≈ 37,333`. That is `280 / 80 = 3.5` times scenario B's 10,667, so long-run prices rise 3.5-fold. The doubled faucet more than doubled the net, because the flow sink stayed fixed.
4. On a closed server, `m* = h(g − r) / (τv) = 50 / (0.03 × 0.04) = 50 / 0.0012 ≈ 41,667`. Without the tax there is no stock sink, and money per player rises by about 50 gold a day (a little more, since quitters also leave) forever.
5. (a) Money sink, item faucet (a transformation from gold to mount). (b) Transfer of both money and items. (c) Item transformation, pelts sink and cloak faucet, no money effect. (d) Money sink of 5 gold.

</details>

## Lab / assignment hook

[Lab 03, build the faucet/sink simulator](../labs/lab03.md). You will implement the model in a spreadsheet or Python, reproduce the five scenarios in this lecture, and design a sink package that holds prices within a target band for two years while new-player numbers fall. It feeds the Models assignment (30%) and prepares the telemetry lab in week 12.

## Sources

- Wikipedia, "Eve Online" (article as of 2026). CCP hired economist Eyjólfur Guðmundsson in 2007 to oversee the game's economy.
- CCP Dr.EyjoG (Eyjólfur Guðmundsson), "Econ Dev Blog - Market Overview For Mineral Markets", eveonline.com, 3 September 2007 (re-read September 2026). His first economics dev blog as CCP's economist, which confirms the 2007 date.
- CCP Games, *Monthly Economic Report*, January 2024 (eveonline.com news). Includes the standard charts of ISK sinks and faucets and their history.
- EVE University Wiki, "Trading". Sales tax 7.5% base from 12 March 2025, reduced by 11% per Accounting level; broker's fee 3% base at NPC stations, reduced by Broker Relations and standings.
- Warcraft Wiki, "Auction House" (5% cut of the winning bid, deposits as a share of vendor price) and "Repair" (10% loss of maximum durability on death, more with a spirit healer). Checked September 2026: the page states the 5% cut for the faction auction houses and flags only missing information on the old neutral auction houses (15% cut) and the patch 8.3 revamp.
- Old School RuneScape Wiki, "Grand Exchange". Tax of 1% from 9 December 2021, 2% from 29 May 2025, capped at 5 million coins per item, with exemptions; item sink funded by the tax; a sample of deleted items posted by Mod Ash on 29 May 2025 (38,000 Bandos godswords, 399 twisted bows, among others). The wiki values that list at current prices, so it gives no fixed total.
- Wikipedia, "Path of Exile" (article as of 2026). Barter economy of currency items with their own crafting uses.
- Lehdonvirta, V. & Castronova, E. (2014). *Virtual Economies: Design and Analysis*. MIT Press.

## Interactive spec: examples/w03-faucet-sink-simulator.html

**The one insight:** sinks that scale with play (repairs) only slow price drift, while sinks that scale with the money stock (trade tax) put a ceiling on it. Dilution by new players hides the difference until growth stops.

**Model** (daily steps, `d` = 0 to 730, all in double precision, update `M` using `N(d)` before updating `N`):

```
M(d+1) = M(d) + N(d) × h × (g − r) − τ × v × M(d) − c × M(d)
N(d+1) = N(d) + J − c × N(d)
m(d) = M(d) / N(d)
P(d) = 100 × m(d) / 1,000
Steady state (shown only when it exists):
  if J = c × N(0) (constant population):  m* = h(g − r) / (c + τv)
  if J = 0 and τv > 0:                    m* = h(g − r) / (τv)
  otherwise: run to day 730 and show "no closed form".
```

Start with `N(0) = 1,000` and `M(0) = 1,000 × m0`, `m0 = 1,000`.

**Layout.**

- Top view: two lines over days 0-730, `N(d)` on the left axis and `m(d)` on the right axis, with a dashed horizontal line at `m*` when it exists.
- Bottom-left view: price index `P(d)` over the same days, with the day-0 value of 100 marked.
- Bottom-right view: a bar chart of today's flows in gold per day at the scrubbed day: faucet `N h g` (up), flow sink `N h r` (down), tax `τ v M` (down), quitters `c M` (down), and the net. At a constant-population steady state (presets A to C) the up bar equals the sum of the down bars. On a closed server at its steady state (preset E) `M` still falls at the churn rate, so there the tax bar equals the faucet minus the flow sink, and the quitters bar is extra.
- Day scrubber (0-730) and a Play button (animates day by day; disabled animation under `prefers-reduced-motion`, which jumps to the end).

**Controls.** `J` new players per day (0-20, default 5), `c` churn per day (0-2%, default 0.5%), `h` hours per day (0.5-6, default 2), `g` faucet gold per hour (0-400, default 100), `r` repair per hour (0-400, default 60), `τ` trade tax (0-25%, default 0), `v` daily trade volume share (0-20%, default 5%). Preset buttons A to E matching the lecture's table.

**Readouts** (copyable): `m`, `P` and `N` at days 30, 90, 180, 365 and 730; `m*` or "none"; days until `m` is halfway to `m*`.

**Test values** (rounded to whole gold):

- Day 1, preset A: `M` = 1,075,000, `m` = 1,075.
- Preset A (`J` 5, `c` 0.5%, `h` 2, `g` 100, `r` 60, `τ` 0): `m` at days 30/90/180/365/730 = 3,094 / 6,446 / 9,915 / 13,593 / 15,614; `m*` = 16,000; halfway first reached on day 139 (closed form 138.3).
- Preset B (`τ` 5%): 2,954 / 5,757 / 8,173 / 10,047 / 10,627; `m*` = 10,667.
- Preset C (`r` 80): 1,977 / 3,542 / 5,160 / 6,877 / 7,820; `m*` = 8,000.
- Preset D (`J` 0): `N` at day 365 = 160.5, at day 730 = 25.8; `m` = 3,412 / 8,236 / 15,472 / 30,347 / 59,693; `m*` none.
- Preset E (`J` 0, `τ` 5%): 3,254 / 7,281 / 12,289 / 19,624 / 27,059; `m*` = 32,000.
- Setting `r = g` in any preset: net faucet zero, `m` only falls (or stays at 1,000 with no churn and no tax).

**Accessibility.** Lines distinguished by dash pattern and direct labels. Flow bars labelled with values. All sliders and buttons keyboard operable with visible focus. Respect `prefers-color-scheme` and `prefers-reduced-motion`.
