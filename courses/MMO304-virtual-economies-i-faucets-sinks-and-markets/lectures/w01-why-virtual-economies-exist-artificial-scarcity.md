# MMO304 · Week 01 — Why Virtual Economies Exist: Artificial Scarcity

**Why this matters:** A server can copy a sword a million times at no cost, yet players will grind for hours or pay real money to own one. That price exists only because a designer decided the sword should be scarce. Every economy you build in this course starts with that decision, so you need to know how to make it on purpose and how to read what it will cost your players.

**You will be able to:**
- Compute the expected time cost and the long-run market price of a farmable item from its drop chance, attempt time and the farming wage.
- Explain why a market price follows the average cost while individual players feel the unlucky tail, and compute the median and 95th-percentile wait.
- Compare four levers of artificial scarcity (chance, effort, rate limits and fixed supply) and predict what each does to prices and to players.
- Critique a drop-rate proposal by converting it into hours and into gold before it ships.

**Before class:** Lehdonvirta & Castronova, *Virtual Economies: Design and Analysis* (MIT Press, 2014), chapters 1 and 2, "Introduction" and "Theories of Human Behavior". Castronova (2001), "Virtual Worlds: A First-Hand Account of Market and Society on the Cyberian Frontier", CESifo Working Paper 618, the introduction and the section on the Norrath economy (about 12 pages).

**Prerequisites from earlier courses:** [MA102 week 7, the geometric distribution](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w07-geometric-distribution-kills-until-the-drop.md) (mean wait `1/p`, median and dry tail). [MA102 week 4, expected value](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md). GD102 [week 2, stocks and flows](../../GD102-systems-design-and-game-mechanics/lectures/w02-stocks-and-flows.md) and [week 7, internal economies](../../GD102-systems-design-and-game-mechanics/lectures/w07-internal-economies-sources-drains-converters.md). [GD101 week 9, meaningful decisions](../../GD101-introduction-to-game-design/lectures/w09-choice-and-meaningful-decisions.md).

**Interactive:** [The scarcity dial](../examples/w01-scarcity-dial.html). Drag the drop chance and flip random drop to fixed cost to see the price hold while the tail disappears.

---

## 1. Copies cost nothing, so why do they have a price?

In March 1999 the economist Edward Castronova studied Norrath, the world of EverQuest. He found that its players traded in-game currency and items for real dollars on auction sites. From those prices he estimated that an hour of play produced about 3.42 US dollars of goods, and that a unit of the game's currency traded at about one cent (0.0107 dollars). His paper placed Norrath's output per person somewhere between Russia and Bulgaria.

That result puzzled people then and it should puzzle you now. Nothing in Norrath costs anything to make. The sword on the server is a row in a database. Sony could have given every player a thousand of them. Yet people paid money, and spent hours, to get one.

The explanation is the core idea of this course. **A good has a price only when it is scarce**, which means that if it were free, people would want more of it than exists. In the physical world scarcity comes from nature: there is only so much iron and so many hours of labour. In a virtual world there is no natural scarcity at all. Every limit is a rule someone wrote. Economists call this **artificial scarcity**, and it is the designer's job.

Some definitions you will use all semester:

- A **good** is anything a player can own and would rather have than not: an item, a currency, a mount, a title.
- **Scarcity** means the quantity people want at a price of zero is larger than the quantity available.
- **Opportunity cost** is the value of the best thing you gave up to get something. For a player, the opportunity cost of an hour spent farming one item is whatever else that hour could have earned.
- A **virtual economy** is the set of rules that decide how goods enter the world, move between players and leave it, together with the behaviour those rules produce.

### Why a designer wants scarcity at all

You could remove scarcity. Some single-player games do: a cheat menu gives every item. The result is that nothing is worth getting. Scarcity is what turns items into goals, and goals are what an MMO sells to players over months and years. It also does three other jobs:

- It creates **choices**. If gold is limited, spending it on a mount means not spending it on armour. In GD101 week 9 you met the idea that a choice needs a real trade-off to be interesting. Scarcity supplies the trade-off.
- It creates **trade**. Players only trade when one has something another lacks. A world with no scarcity has no market, no merchants and no reason to talk to the player selling ore outside the bank.
- It creates **meaning**. A rare mount says something about its owner only because most players do not have one. Week 2 builds a model of this.

So the question is never "should my game have scarcity?" It is "how much, of what, and delivered through which rule?" The rest of this lecture gives you a way to put a number on "how much".

## 2. Worked example: a drop rate is a price tag written in hours

### The hook

Castronova's 3.42 dollars an hour is the surprising fact. It says that EverQuest players, by playing, were producing goods other people would pay for, at a rate comparable to a low-wage job. That can only happen if the goods took time to get. The designers had made time the scarce input. Let's build the model that turns a drop rate into that time, and the time into a price.

### The model

Suppose an item drops from a monster with chance `p` per kill, and each kill takes `t` hours of play (including travel and waiting). From MA102 week 7, the number of kills until the first drop follows a geometric distribution with mean `1/p`. So the expected time to get one copy is:

```
T = t / p
```

Now let `w` be the **farming wage**: the gold per hour a typical player earns from the best alternative activity (quests, selling common materials, whatever pays best). If someone could earn `w` gold per hour elsewhere, spending `T` hours on this item costs them `w × T` gold of forgone income. In a market where many players can farm the item, the long-run price settles near that opportunity cost:

```
P ≈ w × T = w × t / p
```

- `p` is the drop chance per attempt.
- `t` is the time per attempt, in hours.
- `T` is the expected hours per copy.
- `w` is the farming wage in gold per hour.
- `P` is the long-run market price in gold.

Why does price settle there? If the item sold for more than `w × T`, farming it would pay better than anything else, more players would farm it, more copies would reach the market and the price would fall. If it sold for less, farmers would switch to better-paying work, fewer copies would arrive and the price would rise. The price is pulled toward the point where farming this item pays exactly the going wage. Economists call this a long-run equilibrium. It holds when the item is tradeable and enough players can farm it. We will see below what happens when those conditions fail.

### Numbers you can check

Take an invented game with a farming wage of `w = 600` gold per hour. Four items:

| Item | Time per attempt `t` | Drop chance `p` | Mean attempts `1/p` | Expected hours `T` | Price `P = w × T` |
|---|---|---|---|---|---|
| Common hide | 30 s | 50% | 2 | 0.017 (1 min) | 10 |
| Uncommon ring | 1 min | 5% | 20 | 0.33 (20 min) | 200 |
| Rare sword | 2 min | 0.5% | 200 | 6.67 | 4,000 |
| Rare sword, drop halved | 2 min | 0.25% | 400 | 13.3 | 8,000 |

Check the rare sword by hand. Two minutes is `1/30` of an hour. Divide by 0.005 and you get 6.67 hours. Multiply by 600 and you get 4,000 gold.

The last row is the first design lesson. Halving the drop chance doubles the price. The designer who writes "0.25%" in a spreadsheet is really writing "8,000 gold" on every sword. Doubling the kill time has exactly the same effect on price, because only the ratio `t / p` enters the formula.

### What the average hides

The price follows the mean, because the market pools many farmers and their luck averages out. A single player does not get the mean. MA102 week 7 gave you the tools to see how far off one player can be. For a drop chance `p`, the attempt count by which half of players have succeeded is `ln(0.5) / ln(1 − p)`, and the count by which 95% have succeeded is `ln(0.05) / ln(1 − p)`, both rounded up.

| Rare sword (`p` = 0.5%, 2 min per kill) | Kills | Hours |
|---|---|---|
| Median player | 139 | 4.6 |
| Mean (sets the price) | 200 | 6.7 |
| 95th-percentile player | 598 | 19.9 |

One player in twenty farms for about 20 hours, three times the average. The market still values the sword at 4,000 gold. That unlucky player has "paid" about 12,000 gold of their time for a 4,000-gold sword. That is the second design lesson. **Luck does not change what the market pays. It changes who pays it.** The rational move for the unlucky player is to stop farming and buy the sword with gold earned elsewhere, and in a game with a working market many do exactly that.

### The visual

Open the interactive. The left panel shows one player's wait as a histogram of hours until the drop, with the median, mean and 95th percentile marked. The right panel shows the market price bar, `w × t / p`. Drag the drop-chance slider and both panels move together. Then flip the toggle from "random drop" to "fixed cost" (a token system that gives the sword after exactly 200 kills). The price bar does not move at all. The histogram collapses into a single spike. Same price, completely different experience.

### Cross-game recognition

The model needs one number most games never print, the wage `w`. Real games give it away in different ways.

**EverQuest (1999, as measured by Castronova).** Castronova reported the wage in dollars, 3.42 per hour, and the currency's exchange rate, 0.0107 dollars per unit. Divide one by the other and you get the wage in the game's own money, about 320 units per hour. In our notation `w ≈ 320`. Any item's price in that currency, divided by 320, tells you how many hours of an average player's labour it represents. That is `T = P / w`, our formula read backwards.

**World of Warcraft Token (introduced in patch 6.1.2, April 2015, Americas).** Blizzard sold a token for 20 dollars that could be redeemed for 30 days of game time or sold to other players on the auction house for gold. At launch it sold for 30,000 gold. The token turned an exchange rate into a posted price: 1,500 gold per dollar. It also turned game time into an item with a price in hours. A player whose farming wage is 1,500 gold per hour pays for a month of play with `T = 30,000 / 1,500 = 20` hours of farming. Here the developer controls supply by selling tokens for money, and the gold price floats. It is the same `P = w × T` relationship, run in reverse. The market price tells you what the typical player's hour is worth.

**RuneScape Christmas crackers (25 December 2001).** The original crackers were handed out on a single day and never re-released. Each contained a partyhat. Today no amount of farming produces a new cracker, so `T` is infinite for everyone. The model's pull toward `w × T` vanishes, because no farmer can respond to a high price by making more. Price is then set by demand alone, and partyhats now trade for billions of coins. This is the case where the model's condition fails, and it is instructive. When supply cannot respond, prices are free to climb without limit.

Three games, one idea. When you meet a new item, ask how many hours of labour the market thinks it represents, and whether any player can respond to its price by making more.

### Eyes-open design judgment

The formula tells you what a drop rate costs. It does not tell you what it should cost. Decide these things deliberately:

- **Pick the price first, then derive the rate.** If you want a sword to cost about a day's play for a regular player, write down that target in hours, then solve `p = t / T`. Designers who start from "1% feels rare" end up with prices nobody chose.
- **Decide how much luck you want in the cost.** Random drops give the same mean price as a fixed token cost but spread the burden unevenly. A little variance makes kills exciting. A lot makes one player in twenty feel robbed. MA102 week 10 covers pity timers, which cut the tail without moving the mean much.
- **Watch the wage, not only the rate.** Every item's price is `w × T`. If a new zone doubles the farming wage, every farmable item's gold price doubles over time even though you changed no drop rate. Week 4 calls this inflation.
- **Know when the model stops working.** Soulbound items have no market price. Fixed-supply items escape the pull toward cost. A thin market with few farmers can sit far from `w × T` for weeks.

## 3. Four levers of artificial scarcity

The drop rate is one way to make something scarce. There are four, and most games use all of them at once. Each changes a different term.

| Lever | What it limits | Example rule | What it does to price |
|---|---|---|---|
| Chance | Copies per attempt (`p`) | 0.5% drop | Raises `T`, adds variance |
| Effort | Time per copy (`t`) | 500 ore to craft | Raises `T`, no variance |
| Rate limit | Copies per calendar day | One raid lockout a week, a daily quest | Caps supply per week, independent of hours spent |
| Fixed supply | Total copies ever | Event item, retired mount | Breaks the pull toward cost |

A fifth rule, **binding**, is often grouped with these. A soulbound item (one that cannot be traded once picked up) is not scarcer. It is removed from the market. It still costs its owner `T` hours, but it has no price, and no one can buy their way past the grind. Binding is how a designer says "this reward must be earned in play".

### Rate limits change the unit of scarcity

Rate limits deserve a closer look because they break the simple formula in a useful way. Suppose a raid can be run once per week, takes 3 hours, and a given item drops with chance 20% per run. The hours cost is `T = 3 / 0.2 = 15` hours. But a player cannot spend those 15 hours in one weekend. They need on average `1 / 0.2 = 5` weeks.

So a rate-limited item is scarce in calendar time, not only in hours. The whole server can produce at most (number of raiders × 0.2) copies a week, however hard they play. That caps supply, which caps how fast prices can fall. It also caps how fast the most dedicated players can outpace everyone else, which is why MMOs lean on weekly lockouts. The cost is that players feel held back, and the game's calendar becomes a schedule they must keep.

### Fixed supply and speculation

The partyhat case shows the power and the danger of fixed supply. Fixed-supply goods are the purest form of status (week 2). They also attract **speculation**: players buy them expecting the price to rise, not to use them. If a bug duplicates them, the damage is permanent. RuneScape's partyhats were affected by a duplication glitch in 2003 that the RuneScape Wiki still describes as distorting how many of each colour exist. When you create a fixed-supply item, you are committing to guard its supply forever.

## 4. Where the wage comes from, and why it attracts the outside world

The farming wage `w` looks like a player number, but it is set by you. Every quest reward, every vendor price and every monster's gold drop contributes to it. Week 3 treats these as **faucets**, the rules that create money. For now notice one consequence.

Castronova's 3.42 dollars an hour was a wage in real money. Once an hour of play has a real-money value, someone will play for the money rather than for fun. If `w` converted to dollars is higher than the local wage in some part of the world, players there can earn a living by farming gold and selling it. That is the origin of gold farming and real-money trade, the topic of week 11. The scarcity you design for fun sets a price that the outside world can see and act on. A designer who makes items too slow to farm is also raising the reward for anyone willing to sell shortcuts.

This is the tension that runs through the whole course. Scarcity creates goals, trade and meaning. The same scarcity creates prices, and prices invite behaviour you did not design: speculation, hoarding, farming for profit, cheating to duplicate. You cannot remove the second set without removing the first. You can only choose the scarcity carefully and watch what it does.

## In-class activity (25 minutes)

Work in pairs. Your studio is shipping a small MMO. Playtests show a regular player earns `w = 400` gold per hour from quests and common materials.

1. The design lead wants these target prices. For each item, choose the lever (chance, effort, rate limit or fixed supply) and compute the rule's numbers.
   - A healing potion material worth 5 gold. Each gathering node takes 20 seconds.
   - A mid-level ring worth 1,200 gold. The monster takes 90 seconds to find and kill.
   - A raid weapon that should take a regular player about 6 weeks, from a 2-hour weekly run.
   - A cosmetic cloak that should mark the first month's players forever.
2. For the ring, compute the median and 95th-percentile farming time. Decide whether the tail is acceptable. If not, propose a change that keeps the price.
3. For the raid weapon, decide whether it should be tradeable. Write two sentences on what changes if it is.

Expected output: a table with lever, rule numbers and implied price for each item, the two tail numbers for the ring, and the two-sentence tradeability decision.

## Common misconceptions

- **"Rare means expensive."** Rarity raises price only if people want the item. A 0.01% drop that nobody uses sells for its vendor price. The formula gives a cost ceiling that farmers respond to, and demand decides whether anyone pays it.
- **"The vendor price is what the item is worth."** The vendor price is only a floor, the gold the game pays for it. Player prices come from the cost of getting the item and from demand, and they can sit far above that floor.
- **"If I was unlucky, the drop rate must be lower than stated."** With `p` = 0.5%, one player in twenty needs about 600 kills. A crowd of unlucky players is exactly what an honest 0.5% produces.
- **"Artificial scarcity is a trick to exploit players."** It can be abused, but without it there are no goals, no trade and no status. The design question is how much and through which lever, not whether.

## Check yourself

1. A crafting reagent takes 45 seconds to gather and drops with chance 15%. The farming wage is 900 gold per hour. What is its expected long-run price? What happens to the price if a patch doubles gathering speed?
2. An item trades at 12,000 gold. Farmers earn about 1,500 gold per hour elsewhere, and a kill takes 3 minutes. What drop chance is the market implying?
3. A boss drop has `p` = 1% and each attempt takes 6 minutes. Compute the mean, median and 95th-percentile hours to get it.
4. In the WoW Token example, suppose the gold price of a token rises from 30,000 to 60,000 while the dollar price stays at 20. What does the model say happened to the farming wage measured in gold? Name one change in the game that could cause it.
5. A designer proposes making a popular crafted mount require one "event crystal" that is only available for two weeks a year. Which lever is that? Predict what happens to the mount's price in the other fifty weeks.

<details>
<summary>Answers</summary>

1. `t = 45 / 3600 = 0.0125` hours. `T = 0.0125 / 0.15 = 0.0833` hours (5 minutes). `P = 900 × 0.0833 = 75` gold. Doubling gathering speed halves `t`, so `T` and the long-run price both halve, to about 37.5 gold.
2. `T = P / w = 12,000 / 1,500 = 8` hours. `t = 3 / 60 = 0.05` hours. `p = t / T = 0.05 / 8 = 0.00625`, about 0.63%.
3. Mean attempts 100, so 10 hours. Median attempts `ln(0.5) / ln(0.99) = 68.97`, rounded up to 69, so 6.9 hours. 95th percentile `ln(0.05) / ln(0.99) = 298.07`, rounded up to 299, so 29.9 hours.
4. If a month of game time is worth roughly the same number of hours to a typical player, a doubled gold price means the gold earned per hour has roughly doubled, from about 1,500 to 3,000 gold per hour. A new expansion zone with larger gold rewards, or a general rise in money supply per player (inflation, week 4), would do it.
5. It is a rate limit bordering on fixed supply. Crystals can only enter the world during the event window, so the supply of mounts stops growing for fifty weeks while demand continues. Expect the mount's price to rise through the year, and expect speculators to buy crystals during the event to sell later.

</details>

## Lab / assignment hook

[Lab 01, pricing scarcity in hours](../labs/lab01.md). You will build a sheet that converts a loot table into hours and gold, simulate 1,000 farmers to see the tail, and redesign three drop rates to hit target prices. It feeds the Models assignment (30%).

## Sources

- Castronova, E. (2001). "Virtual Worlds: A First-Hand Account of Market and Society on the Cyberian Frontier." CESifo Working Paper No. 618. Norrath (EverQuest) in March 1999: hourly wage about 3.42 US dollars, currency at 0.0107 dollars, GNP per capita between Russia and Bulgaria. Abstract checked on RePEc/IDEAS.
- Lehdonvirta, V. & Castronova, E. (2014). *Virtual Economies: Design and Analysis*. MIT Press. Chapter titles and order checked against the MIT Press chapter DOIs on Crossref (10.7551/mitpress/9525.003.0002 to .0015, September 2026): 1 Introduction, 2 Theories of Human Behavior, 3 Goods, 4 Supply and Demand, 5 Regulating Markets, 6 Market Power and Pricing, 7 Methods of Exchange, 8 Externalities and Secondary Market Trade, 9 Institutions and Nonmarket Allocation, 10 Money, 11 Macroeconomic Design, 12 Macroeconomic Management, 13 Policymaking, 14 Why the Real World Needs Virtual Economy Design.
- Warcraft Wiki, "WoW Token". Introduced in patch 6.1.2 on 7 April 2015 in the Americas at 20 US dollars, initial gold price 30,000, redeemable for 30 days of game time.
- RuneScape Wiki, "Christmas cracker". Released 25 December 2001 in the first RuneScape Christmas event, available that day only, never re-released, contained partyhats; notes the 2003 duplication glitch and partyhat prices in the billions of coins.
- Schreiber, I. (2010). *Game Balance Concepts*, Level 4, "Probability and Randomness", for the geometric-distribution results reused from MA102 week 7.

## Interactive spec: examples/w01-scarcity-dial.html

**The one insight:** the market price is set by the mean hours per copy, `w × t / p`, while each player lives somewhere in a wide distribution around that mean. Changing luck into a fixed cost leaves the price unchanged and removes the tail.

**Layout.** Two linked panels side by side on desktop, stacked on mobile (left panel first).

- Left panel, "One player's wait": a histogram of hours until the drop for the geometric distribution, drawn from the exact probability mass `P(K = k) = (1 − p)^(k − 1) × p`, with kills converted to hours by `× t`. Bin into 40 bins from 0 to the 99th-percentile hours. Vertical markers labelled Median, Mean and 95th percentile, with their hour values printed.
- Right panel, "What the market pays": a single horizontal bar for price `P = w × t / p`, with the number printed. Beneath it, a second, thinner bar labelled "What the 95th-percentile player paid in time" = `w × t × k95`, so the gap between the two bars is visible.

**Controls.**

- Drop chance `p`: log-scale slider from 0.05% to 50%, default 0.5%. Show the value as a percentage.
- Time per attempt `t`: slider 10 s to 10 min, default 2 min.
- Farming wage `w`: slider 50 to 5,000 gold per hour, default 600.
- Toggle "Random drop" / "Fixed cost". In fixed-cost mode the item arrives after exactly `ceil(1/p)` attempts. The histogram becomes a single bar at `ceil(1/p) × t` hours, and the median, mean and 95th-percentile markers coincide.
- Preset buttons: "Common hide", "Uncommon ring", "Rare sword", "Rare sword, drop halved" (the four rows of the lecture's table).

**Readout table** (always visible, copyable): mean attempts `1/p`, expected hours `T = t/p`, price `P`, median attempts `ceil(ln 0.5 / ln(1 − p))`, 95th-percentile attempts `ceil(ln 0.05 / ln(1 − p))`, and each attempt count converted to hours.

**Test values** (must match exactly, rounded as shown):

- Rare sword (`p` = 0.005, `t` = 2 min, `w` = 600): mean 200 attempts, `T` = 6.67 h, `P` = 4,000; median 139 attempts (4.63 h); 95th percentile 598 attempts (19.93 h); 95th-percentile time cost in gold `600 × 19.93 ≈ 11,960`.
- Rare sword, drop halved (`p` = 0.0025): mean 400, `T` = 13.33 h, `P` = 8,000; median 277; 95th percentile 1,197.
- Uncommon ring (`p` = 0.05, `t` = 1 min): `T` = 0.33 h, `P` = 200; median 14; 95th percentile 59.
- Common hide (`p` = 0.5, `t` = 30 s): `T` = 0.0167 h, `P` = 10; median 1; 95th percentile 5.
- Fixed-cost mode, rare sword: all three markers at 200 attempts (6.67 h), price still 4,000.

**Accessibility.** All controls keyboard operable with visible focus. Markers distinguished by label and line style, not colour alone. Respect `prefers-reduced-motion` by disabling bar transitions.
