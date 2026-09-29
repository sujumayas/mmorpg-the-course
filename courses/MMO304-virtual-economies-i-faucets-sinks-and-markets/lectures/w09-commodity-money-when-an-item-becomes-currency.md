# MMO304 · Week 09 — Commodity Money: When an Item Becomes Currency

**Why this matters:** You decide what your game's money is when you ship a gold coin. Your players decide again every day. If your gold fails at its job, they will pick an item and use that instead, and your drop table becomes their central bank. You need to recognize when that is happening, predict which item they will pick, and decide whether to fight it or design for it.

**You will be able to:**
- Compute how many trades and how many prices a barter market needs compared with a market that has money.
- Test a candidate item against the properties money needs, and predict whether players will adopt it as currency.
- Explain how a commodity money's supply (drops, duplication, sinks) sets its value, using the Stone of Jordan in Diablo II.
- Critique the choice between a designed commodity money (Path of Exile) and a conventional gold currency.

**Before class:** Lehdonvirta & Castronova, *Virtual Economies: Design and Analysis* (2014), chapter 10, "Money". Radford, R. A. (1945), "The Economic Organisation of a P.O.W. Camp", *Economica* 12(48), the sections on the cigarette currency.

**Prerequisites from earlier courses:** [MA102 week 7, the geometric distribution](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w07-geometric-distribution-kills-until-the-drop.md) (mean wait `1/p` for a chance `p` per try). [MA102 week 11, Monte Carlo simulation](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w11-monte-carlo-simulation.md) (checking a formula by simulation). [GD102 week 7, internal economies](../../GD102-systems-design-and-game-mechanics/lectures/w07-internal-economies-sources-drains-converters.md). From this course, [week 4, money supply per capita](w04-money-supply-per-capita-and-inflation.md) and [week 8, item stock and destruction](w08-item-decay-durability-and-destruction-as-sinks.md) (the steady stock `F / d`).

**Interactive:** [Barter vs money](../examples/w09-barter-vs-money.html). Drag the number of goods and switch the market to money.

---

## 1. What money does

Economists name three jobs that money does. A thing is money to the extent it does them.

- **Medium of exchange.** You accept it in trade, not because you want it, but because you know someone else will accept it from you.
- **Unit of account.** Prices are quoted in it. "That sword is worth 3 of these."
- **Store of value.** You can hold it for a while and it still buys roughly what it bought before.

Most games start with a **fiat currency**: gold coins created by the game's faucets, with no use except spending. Gold works as money only if players trust that it will keep doing those three jobs.

A **commodity money** is an item that has its own use and also does money's jobs. Gold coins in the real world were commodity money. So were cigarettes in prisoner-of-war camps, as you'll see below. In games, commodity money usually appears when the official currency fails at one of the three jobs and players need something that works.

Two terms used throughout:

- **Barter** is trading goods directly for goods, with no money in between.
- The **double coincidence of wants** is barter's central problem. For a trade to happen, your partner must have what you want *and* want what you have.

## 2. Worked example: a ring becomes Diablo II's money

### The hook

Blizzard ran an official strategy guide for Diablo II and its expansion Lord of Destruction, called *The Arreat Summit*. Its page on runes tells players not to fall for a common scam, trading one Stone of Jordan for one or two cheap runes. Its page on trading suggests example names for a trade game, and one of them is "Silks4TwoJordan", a game where someone wants to buy a set of armour for two Stones of Jordan.

The Stone of Jordan is a unique ring. Diablo II has gold. Yet the game's own guide quotes prices in rings. Somewhere along the way, players stopped pricing things in the currency the game gave them and started pricing them in jewelry.

This worked example explains why, in two steps. First, why a market that trades many kinds of goods needs *some* money. Then, why that money was a ring and not gold.

### The model: the cost of barter

Suppose players trade `G` kinds of goods. Each player holds one kind and wants one other kind, chosen at random. They meet trading partners one at a time. Assume each partner holds a kind different from yours and wants a kind different from theirs, each chosen at random.

**Barter.** A meeting produces a trade only if the partner has what you want (chance `1 / (G − 1)`) and wants what you have (another `1 / (G − 1)`, independent of the first). So the chance per meeting is:

```
p_barter = 1 / (G − 1)²
```

The number of meetings until the first success follows the geometric distribution from MA102 week 7, with mean `1 / p`:

```
meetings with barter = (G − 1)²
```

**With money.** Suppose one good is accepted by everyone. You make two half-trades instead of one whole one. First you sell your good to anyone who wants it (chance `1 / (G − 1)` per meeting, so `G − 1` meetings on average). Then you buy what you want from anyone who has it (another `G − 1`):

```
meetings with money = 2 × (G − 1)
```

**Prices.** Barter needs an exchange rate between every pair of goods. Money needs one price per good:

```
prices with barter = G × (G − 1) / 2
prices with money  = G − 1
```

Barter's costs grow with the square of the number of goods. Money's grow in a straight line. Week 10 reuses these counts when it compares market designs, always counting both halves of a money trade.

### Numbers you can check

| Kinds of goods `G` | Barter meetings `(G−1)²` | Money meetings `2(G−1)` | Barter prices `G(G−1)/2` | Money prices `G−1` |
|---|---|---|---|---|
| 5 | 16 | 8 | 10 | 4 |
| 10 | 81 | 18 | 45 | 9 |
| 20 | 361 | 38 | 190 | 19 |
| 50 | 2,401 | 98 | 1,225 | 49 |
| 100 | 9,801 | 198 | 4,950 | 99 |

With 5 kinds of goods, barter is a nuisance, twice as slow as money. With 100, it is 50 times as slow, and nobody can remember 4,950 exchange rates. Diablo II's trade economy covered many unique items, set items, runes, gems and charms, each with different rolls. Some money was going to emerge.

### A visual the student can move

Open the interactive. The left view draws the `G` goods as dots on a circle. In barter mode, a line joins every pair, one line per exchange rate. Switch on "money" and the tangle collapses into a star, with one line from each good to the money good in the centre. The right view runs a simulated market. Every trader looks for a partner, meeting after meeting, and the histogram shows how many meetings each trader needed. In barter mode, drag `G` from 5 to 20 and watch the histogram's mean slide from 16 to 361 while its long tail stretches off the chart. Switch on money and the whole histogram jumps back near zero.

The left view shows how complicated barter is to *think* about. The right view shows how slow it is to *do*. Both grow with the square of `G`.

### Why not gold?

The model says a Diablo II economy needs money. It does not say which. Gold was the obvious candidate, and it failed at two of money's jobs, for reasons the game's own rules explain.

**Gold was a poor store of value.** On Battle.net realms, dying cost a character a share of all their gold, both carried and in the stash, equal to their character level in percent, up to 20%. A high-level player who died carrying their savings lost a fifth of them. A ring on a corpse or in a stash lost nothing to that penalty.

**Gold could not express high values.** Non-player vendors capped what they paid for any item. The cap rose from 5,000 gold in Normal Act I to 35,000 gold in Hell, and 35,000 was the most any vendor ever paid. There was no way to turn a valuable item into more gold than that at a vendor, and the items players valued most came from monster drops, not from vendors. So gold had no reliable connection to the value of top items. A price of "five million gold" for a rare item meant little, because gold could not buy that item from anyone but another player, who then faced the same problem.

Now test the Stone of Jordan against the same jobs. Here are the properties an item needs to work as money, with the evidence from Blizzard's guide:

| Property money needs | Why it matters | Stone of Jordan (Lord of Destruction era) |
|---|---|---|
| Durable | Must not wear out while you hold it | Rings never need repair and are not subject to wear |
| Uniform | Every unit worth the same, so no inspection needed | Fixed stats with no random ranges: +1 to all skills, +25% maximum mana, adds 1-12 lightning damage, +20 mana |
| Widely wanted | Anyone will accept it, even if not for themselves | +1 to all skills helps every class; required level 29, so almost any character can wear one |
| Scarce, with steady supply | Holds value; new units arrive slowly | A unique ring from random drops |
| Small and easy to trade | Cheap to carry and hand over | A ring; fits any stash |
| Has sinks | Units leave, so the stock does not grow forever | Consumed by Horadric Cube recipes (for example, adding a socket to a rare item); linked to the realm-only Diablo clone event |

Gold failed "store of value" and "expresses high values". The Stone of Jordan passed every row. It became the unit of account, then the medium of exchange, then what players saved in.

### Cross-game recognition

The same pressure produces the same answer wherever an official currency is missing or weak.

**Prisoner-of-war camps (Second World War).** R. A. Radford, an economist who was himself a prisoner, described in 1945 how Red Cross parcels made each prisoner rich in some goods and short of others. Barter was clumsy, and cigarettes became the currency: prices of food and clothing were quoted and paid in cigarettes. Cigarettes were wanted by smokers (the use value), uniform, small and countable. They also had a sink, since smokers burned them. Radford documented inflation and deflation in the cigarette currency as supplies changed, the same supply effects you studied in week 4.

**Path of Exile (from the 2013 launch).** Grinding Gear Games decided before launch not to use gold for trade. A 2011 developer diary on the official site, "Rethinking Gold as a Currency", laid out the plan. Trade runs on currency items that have their own crafting uses. A Chaos Orb rerolls all the random properties of a rare item. It takes one inventory square and stacks to 20. The Path of Exile Wiki names it as one of the three orbs most used as currency between players, with the Divine Orb and the Mirror of Kalandra above it in value. Every Chaos Orb used for crafting is destroyed, so the money has a built-in sink. When gold was finally added in patch 3.25 (Settlers of Kalguur, July 2024), it could not be traded between players. Path of Exile is the Stone of Jordan done on purpose.

**United States prisons (from the 2000s).** Commodity money appears whenever the official one is banned. After many US prisons banned smoking in the early 2000s, inmates in many places switched from cigarettes to containers of mackerel as the unit of trade. The container is uniform, durable and wanted. The pattern is the same as the camp's.

Three settings, one test. When you see players quote prices in an item, check it against the properties table. The item that passes most rows, in a place where the official money fails one, becomes the money.

### Eyes-open design judgment

- **Your drop table is now monetary policy.** Once an item is money, its drop rate is the money supply. A patch that doubles the drop rate of the Stone of Jordan is a patch that doubles the money printing press. Treat drop changes to a money item like changes to gold faucets (week 4).
- **Balance changes become currency shocks.** If you weaken the item's use (say, the ring loses +1 to all skills), you cut its "widely wanted" row, and everyone's savings lose value overnight. Players will experience a stat change as a bank collapse.
- **Duplication is counterfeiting.** Diablo II's patch history includes fixes for item duplication exploits. A duplicated money item is identical to a real one, so every dupe adds to the money stock without a drop. The value of every honest player's savings falls. Duplication bugs in a money item are the most expensive bugs you can ship.
- **Designing it on purpose has costs too.** Path of Exile's currency items give money built-in sinks and make every orb useful. The price is complexity. New players must learn a dozen currencies and their exchange rates, the barter problem of section 2 at a smaller `G`. Path of Exile's later additions (a currency exchange market, untradeable gold for non-player services) are fixes for that cost.

## 3. The supply of a commodity money

A commodity money's value depends on how many units exist compared with the goods they chase. That is week 4's money per capita, with the item stock in place of gold.

The stock follows week 8's model exactly. New units arrive at rate `F` (drops plus duplication). Units leave at rate `d × S` (used in recipes, sold to trigger events, lost when accounts quit). The steady stock is `S* = F / d`.

What changes is how you read it. For a gear item, a higher `S*` means lower prices for that item. For a money item, a higher `S*` means **higher prices for everything else, in that unit**. If the stock of rings doubles while the goods traded stay the same, the price of a set of armour in rings roughly doubles. That is inflation in the commodity money.

Three things follow.

**Dupes raise `F` without anyone playing.** A duplication exploit is an extra faucet with no connection to effort. Week 4's model says prices in that unit will rise.

**Sinks keep the stock bounded.** The Horadric Cube recipes that consume a Stone of Jordan, and selling rings to trigger the Diablo clone event, are both sinks. Blizzard's own guide says the clone appears only on Battle.net realms and hints that the Stone of Jordan is involved. Community guides describe the trigger as a count of rings sold to vendors across the realm. Every ring sold that way leaves the economy. Without sinks, `d` is close to zero, and a money item piles up like the no-destruction breastplate of week 8.

**When a unit gets too cheap, players switch to a scarcer one.** Money needs to be worth enough that you do not carry hundreds of units for a single trade. When a money item becomes too common, traders move to a rarer item as their big denomination and keep the old one for small trades. In Diablo II: Resurrected, community trade listings on diablo2.io in September 2026 priced a Stone of Jordan at about one Vex rune or two Ist runes. The ring had become small change, and high runes had become the large notes. You will see the same pattern in any game where one money item inflates. A new, scarcer unit appears above it.

### Numbers you can check

A realm where rings drop at `F = 40` per day. Players use `d = 0.2%` of the stock per day in recipes and events.

- `S* = 40 / 0.002 = 20,000` rings.
- A duplication exploit adds 60 rings per day for a month before it is fixed. The stock ends about 1,750 higher than it would have been (a little under `60 × 30 = 1,800`, since the sink removes a few), about 9% of `S*`, and prices in rings rise by roughly that much.
- After the fix, the excess decays at `d` per day, back toward `S*`, taking about `0.69 / 0.002 ≈ 347` days to halve. A month of exploit costs the economy a year of elevated prices.

The last point is the one to remember. With a small `d`, commodity money has a long memory. Mistakes in its supply linger.

## 4. Designing for it, or against it

You have three choices when you design a game with player trade.

1. **Make gold work.** Give gold the three jobs. Keep it a good store of value (no large penalties on held gold), let it express high values (an auction house where top items sell for gold, week 10), and keep its supply under control (week 4). Most theme-park MMOs take this route. If gold works, players have no reason to pick an item.
2. **Design commodity money on purpose.** Choose the items, give them uses that destroy them, and plan their drop rates as a money supply. Path of Exile's route. You gain sinks for free and lose simplicity.
3. **Accept that it will emerge, and watch for it.** In a game with a weak or missing currency, some item will become money. Check your item list against the properties table before launch. The item that passes most rows is your future currency. Protect it from dupes and plan its sinks before players find it.

Whatever you choose, watch your telemetry (week 12) for the signs. If trade chat and trade listings quote prices in an item, that item is money, whatever your design document says.

## In-class activity (25 minutes)

In groups of three, take a game design with these tradable items and a gold currency with a 15% death penalty on carried gold:

- Iron ore (stacks to 100, used in crafting)
- A healing potion (stacks to 20, consumed on use)
- A rare gem with random quality from 1 to 100 (1 slot, used to upgrade gear, destroyed on use)
- A cosmetic hat (1 slot, no stats, fixed appearance, never destroyed)
- A teleport scroll (stacks to 50, consumed on use, sold by vendors for 100 gold)

1. Score each item against the six rows of the properties table (0, 1 or 2 per row). Which item is most likely to become money?
2. Why is gold likely to fail? Which of the three jobs?
3. Propose one rule change that makes gold work, and one that makes your top item a safer money (for example, fixing the gem's quality).
4. Compute the barter and money search costs for this market (`G = 5`) and say whether barter would be tolerable.

Expected output: the scored table, the predicted money, two rule changes, and the two search costs.

## Common misconceptions

- **"Players use an item as money because the gold is inflated."** Inflation is one reason. Diablo II's gold failed because it was a poor store of value and could not express high values. An economy with stable gold can still lose to an item if gold cannot buy what players want.
- **"Commodity money is barter."** Barter is trading goods for goods with no common unit. Commodity money is a single agreed unit, which removes the double coincidence of wants. The Stone of Jordan made Diablo II trade *less* like barter.
- **"More money items make players richer."** More units raise prices in that unit. A realm with twice the rings does not have twice the goods.
- **"Designed commodity money solves the problem."** It moves the problem. Path of Exile gains built-in sinks and pays with a multi-currency barter problem that needed its own market tools.

## Check yourself

1. A game has 30 kinds of tradable goods. How many barter meetings does a trader expect before completing one trade? How many with money? How many exchange rates would a barter market need?
2. Two candidates could become money in a game: a ring with fixed stats that never wears out, and an amulet with the same use but stats that roll randomly from a range. Which is the better money and why? Name the row of the properties table.
3. A money item has `F = 25` per day and `d = 0.5%` per day. What is its steady stock? The designers add a new recipe that consumes these items and raises `d` to 1%. What happens to the steady stock and to prices quoted in that item?
4. Explain, using the realm death penalty, why a Diablo II player with 1,000,000 gold at character level 90 might prefer to hold their wealth in rings. How much gold would one death cost them?

<details>
<summary>Answers</summary>

1. Barter: `(30 − 1)² = 841` meetings. Money: `2 × 29 = 58`. Barter exchange rates: `30 × 29 / 2 = 435`.
2. The fixed-stat ring. It passes the "uniform" row. Every ring is worth the same, so no one needs to inspect a unit before accepting it. Random rolls make each amulet a separate good, which brings back the barter problem.
3. `S* = 25 / 0.005 = 5,000`. With `d = 1%`, `S* = 2,500`. The stock halves over time, so prices quoted in that item fall toward half their old level. That is deflation in the commodity money, which makes it more attractive to hold.
4. The penalty is the character level in percent, capped at 20%, so at level 90 it is 20% of all gold carried and in the stash: 200,000 gold per death. Rings on the corpse or in the stash are not subject to that penalty, so they hold value better.

</details>

## Lab / assignment hook

This week feeds the models assignment (30%). Extend [Lab 08's item lifecycle sheet](../labs/lab08.md) with one money item. Track its stock under drops, a one-month duplication exploit and a sink recipe, and plot prices quoted in that item over one year. Week 10's lab on market design ([Lab 10](../labs/lab10.md)) then uses the barter search cost from section 2.

## Sources

- Blizzard Entertainment, *The Arreat Summit* (classic.battle.net), Diablo II: Lord of Destruction, archived official guide reflecting patches 1.10 to 1.14. Pages used: "Runes" (the "1 Shael or Amn for 1 SOJ" scam warning); "Trading" (example trade-game name "Silks4TwoJordan"); unique rings (the Stone of Jordan's fixed stats and required level 29); "Rings and Amulets" (never need repair); "Characters" (classic.battle.net/diablo2exp/basics/characters.shtml, re-read September 2026: death penalty equal to character level in percent, capped at 20%, taken from carried and stashed gold; Single Player exempts the stash and 500 gold per level); "Vendors" (basics/vendors.shtml, re-read September 2026: most a vendor pays for an item, 5,000 gold in Normal Act I rising by act to 30,000 in Nightmare and 35,000 in Hell); "The Horadric Cube" (recipes that consume a Stone of Jordan); the Diablo clone page (realm-only, hint at the Stone of Jordan).
- diablo2.io, "The Stone of Jordan" item page and trade listings (Diablo II: Resurrected, accessed September 2026). Community trade prices around one Vex or two Ist runes; community notes that selling rings to vendors advances the Diablo clone event. Community data, not an official source.
- Wikipedia, "Diablo II". Item duplication exploits were among the bugs addressed in patches.
- Radford, R. A. (1945). "The Economic Organisation of a P.O.W. Camp." *Economica*, 12(48), doi:10.2307/2550133. Cigarettes as currency; inflation and deflation with parcel supply.
- Wikipedia, "Commodity money". Summary of Radford's cigarette currency and the shift to mackerel pouches in US prisons after smoking bans.
- Grinding Gear Games, "Dev Diary: Rethinking Gold as a Currency" (pathofexile.com, 8 February 2011), as cited by Wikipedia, "Path of Exile". No gold for trade; currency items with their own uses. Gold added in patch 3.25, Settlers of Kalguur (26 July 2024), not tradable between players.
- Path of Exile Wiki, "Chaos Orb" (current). Rerolls a rare item's modifiers; 1×1, stack size 20; one of the three orbs most used as currency between players with the Divine Orb and Mirror of Kalandra.
- Lehdonvirta, V. & Castronova, E. (2014). *Virtual Economies: Design and Analysis*. MIT Press.

## Interactive spec: examples/w09-barter-vs-money.html

**The one insight:** the cost of barter grows with the square of the number of kinds of goods, while money makes it grow in a straight line, so a market with many goods will adopt some money, whether the designer provides one or not.

**Layout:** two linked views side by side on desktop, stacked on mobile. Left, "Prices you need to know". Right, "Meetings until you trade". A readout row with exact numbers under both.

**Controls:**
- `G`, kinds of goods: slider 3-40, default 10.
- Mode toggle: "Barter" / "Money" (default Barter).
- Traders simulated: 200, 1,000 (default) or 5,000.
- Button "Run market again" (new random seed). Seeded RNG so the default view is reproducible.

**Left view (network):** `G` dots evenly on a circle, labelled 1..G. Barter mode draws every pair as a line (`G(G−1)/2` lines). Money mode designates good 1 as money, moves it to the centre, and draws `G − 1` lines from it to the rest. Show the line count in large type.

**Right view (simulation):**
- Each simulated trader holds `h` uniform in 1..G and wants `w` uniform among goods ≠ `h`.
- Barter: each meeting draws a partner holding `h'` uniform among goods ≠ `h` and wanting `w'` uniform among goods ≠ `h'`. Success if `h' = w` and `w' = h`. Count meetings to first success.
- Money: phase 1 (sell), each meeting succeeds with probability `1/(G − 1)` (partner wants `h`); phase 2 (buy), each meeting succeeds with probability `1/(G − 1)` (partner holds `w`). Count total meetings across both phases.
- Plot a histogram of meetings per trader (bins chosen so the mean and the 95th percentile are on screen; put overflow in a final "more" bin). Draw a vertical line at the simulated mean and a dashed line at the theoretical mean.
- Readouts: theoretical mean (`(G−1)²` or `2(G−1)`), simulated mean, simulated median, share of traders needing more than twice the mean.

**Test values:**
- `G = 5`: barter theory 16, money theory 8; lines 10 vs 4.
- `G = 10`: barter 81, money 18; lines 45 vs 9.
- `G = 20`: barter 361, money 38; lines 190 vs 19.
- With 1,000 traders, the simulated mean should fall within about 7% of theory for barter (standard error of a geometric mean with `p` small is close to `mean / sqrt(n)`, about 3%). The builder should assert this in a console self-test at `G = 10`.

**Accessibility:** the mode toggle is a real button group reachable by keyboard; the histogram has a text summary ("Mean 81 meetings; 1 trader in 7 needed more than 162"); respects reduced motion by drawing the histogram without animation. No game art; the money good is drawn as a plain ring shape, not any game's icon.
