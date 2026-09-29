# GD203 · Week 09 — Item budgets and stat weights

**Why this matters:** An RPG with a few hundred items has a few hundred chances to ship one that is quietly better than everything else. An item budget is the tool that lets you price every stat in one currency and catch that item on your own sheet before players catch it in a week.

**You will be able to:**
- Compute an item's budget cost from a stat price list and flag items that are over or under budget.
- Compute an item's value to a specific build from stat weights, and explain why on-budget items can still differ in value.
- Derive a stat price list from the stat weights of a reference set of builds.
- Critique a budget system for the cases a linear price list misses (extremes, synergies, caps and procs).

**Before class:** Schreiber, *Game Balance Concepts*, level 3 ("Transitive Mechanics and Cost Curves"); Schreiber & Romero, *Game Balance* (2021), the chapter on transitive mechanics and cost curves.

**Prerequisites from earlier courses:** GD203 week 1, [stats as design language](w01-stats-as-design-language.md), for stat exchange rates. Looking ahead, MMO303 week 2, [armor and damage mitigation](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w02-armor-and-damage-mitigation.md) (year 3), section 5, splits a defensive budget between armor and health. MA102 week 4, [expected value](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md), for pricing procs. GD203 week 8, [power curves and level scaling](w08-power-curves-and-level-scaling.md), for how budgets grow with item level.

**Interactive:** [examples/w09-item-budget.html](../examples/w09-item-budget.html) (built from the spec at the end of this lecture). Keep it open during section 2.

---

## 1. One currency for every stat

Week 1 showed that each stat has an exchange rate into outcomes. One point of strength is worth some amount of damage per second. One point of stamina is worth some amount of health. An **item budget** turns those exchange rates into a pricing system.

It has three parts.

- **The currency.** An abstract unit, usually called a point. Pick one stat as the reference and set its price to 1. In this lecture strength is the reference.
- **The price list.** For each stat `s`, a price `p_s` in points per unit of stat. If crit rating costs 0.8, then 50 crit rating costs 40 points.
- **The budget.** How many points an item may spend. It depends on the item's level (item level, or ilvl) and its slot. Write it `B(ilvl, slot)`.

An item's **cost** is the sum of its stats times their prices:

```
cost(item) = Σ p_s × amount_s
```

An item is **on budget** if its cost equals `B`, **overbudget** if it costs more and **underbudget** if it costs less. A small tolerance, a few percent, is normal. Anything beyond that is a decision you should be able to defend in writing.

The budget does something a stat sheet alone cannot do. It lets you compare items with no stats in common. A chestpiece with strength and stamina and one with strength and haste can both be checked against the same number.

## 2. Worked example: the item that looks average and is not

### The hook

Hearthstone players judge a minion with no card text by a rule they call the vanilla test. A minion passes if its attack and health are at least its mana cost. Three classic neutral minions, all in the game since its 2014 launch and now in the Legacy set, sit right on one line. River Crocolisk costs 2 mana and is a 2/3. Chillwind Yeti costs 4 and is a 4/5. Boulderfist Ogre costs 6 and is a 6/7. Its flavor text jokes about having good stats for the cost. Each gives exactly `cost` attack and `cost + 1` health.

That pattern is a price list. Mana is the currency, and each mana buys one attack and one health, with one free health on top. Players reverse-engineered it from the cards, which means the designers were pricing stats consistently. The question for you is what happens when you forget to price one item, and whether you would notice.

### The model

Use the three parts from section 1. For this example, a level 50 chestpiece has budget `B = 100` points. The price list is:

| Stat | Price `p_s` (points per unit) | Why |
|---|---|---|
| Strength (Str) | 1.0 | Reference stat, raises damage for every build |
| Stamina (Sta) | 0.5 | Health only, valued mostly by tanks |
| Critical strike rating (Crit) | 0.8 | Damage for some builds more than others |
| Haste rating (Haste) | 0.8 | Damage for some builds more than others |

Every symbol again, in one place. `p_s` is the price of stat `s`. `amount_s` is how much of stat `s` the item has. `B` is the budget. Cost is `Σ p_s × amount_s`.

### Numbers you can check

Five chestpieces a designer submitted for the level 50 loot table:

| Item | Stats | Raw stat total | Budget cost | Verdict |
|---|---|---|---|---|
| Plate of the Ox | 50 Str, 100 Sta | 150 | 50 + 50 = 100 | On budget |
| Hauberk of Fury | 60 Str, 50 Crit | 110 | 60 + 40 = 100 | On budget |
| Swift Tunic | 40 Str, 75 Haste | 115 | 40 + 60 = 100 | On budget |
| Balanced Mail | 40 Str, 40 Sta, 25 Crit, 25 Haste | 130 | 40 + 20 + 20 + 20 = 100 | On budget |
| Precision Chestguard | 55 Str, 45 Crit, 30 Haste | 130 | 55 + 36 + 24 = 115 | 15% over |

Look at the raw stat total column first, because that is what a reviewer skimming tooltips sees. The Precision Chestguard has the same raw total as Balanced Mail and 20 less than Plate of the Ox. Nothing about it looks unusual. Priced in points, it is 15% over budget. It spends its points on expensive stats and none on cheap stamina, so its raw total hides its cost.

That is the whole signature lesson. **Raw stat totals are the wrong currency.** Stamina is cheap and inflates the total. Strength is expensive and deflates it. Only the price list puts them in the same units.

Now open the interactive. The left chart shows each item's raw stat total as a bar. The right chart shows each item's budget cost as a bar against a line at `B = 100`. On the left, Precision is in the middle of the pack. On the right, it is the one bar that crosses the line. Edit any item's stats and both charts update. Try to make Precision on budget while keeping its raw total at 130. You will find you have to move points into stamina.

### Cross-game recognition

**Hearthstone (Legacy set, originally the Basic set, 2014).** Rewrite the vanilla line as a budget. Price attack at 0.5 mana and health at 0.5 mana, and give every minion half a mana of free health. Then `cost = (Attack + Health − 1) / 2`. River Crocolisk: `(2 + 3 − 1) / 2 = 2`. Chillwind Yeti: `(4 + 5 − 1) / 2 = 4`. Boulderfist Ogre: `(6 + 7 − 1) / 2 = 6`. All three are exactly on budget. Now try Magma Rager, 3 mana, 5/1. The formula gives `(5 + 1 − 1) / 2 = 2.5`, slightly under budget, so the linear price list says it is a fair or even weak card, and that is right for the wrong reason. The Hearthstone wiki says it is widely considered one of the worst cards in the game. A 1-health minion dies to almost anything, so its 5 attack rarely gets used. A linear price list cannot see that the value of attack depends on having enough health to survive. Hold on to that failure for section 5.

**World of Warcraft (item level system, current retail game).** Every item has an item level, and Warcraft Wiki describes each item as spending its item level's budget on primary stats, secondary stats and effects in different ways. The wiki also notes that a formula linking stats to item level was first worked out by the player community and later confirmed at BlizzCon. We do not need Blizzard's exact prices. The structure is the same as our model. Item level sets `B`, and each item spends it on a mix of stats.

**Dungeons & Dragons 5th edition (Player's Handbook, 2014, point buy).** Players build ability scores from 27 points. A score of 8 costs 0, each step up to 13 costs 1 more point (13 costs 5 in total), then 14 costs 7 and 15 costs 9. This is an item budget applied to a character, with one change. The price per step rises from 1 to 2 at the top. The designers made concentration expensive on purpose, so that three 15s use the whole budget and leave the other three scores at 8. That is a nonlinear price list, and it fixes the exact problem Magma Rager exposes.

Three games, one idea. Each has a currency, a price per stat and a budget per slot, card or character. When you meet a new game's items, try to find its line. Plot items of one level or cost against their stats and see which ones sit above it.

### Eyes-open design judgment

- **Why budget at all.** The budget turns "this feels strong" into a number you can argue about. It is the fastest way to review hundreds of items, and it catches Precision Chestguards before launch.
- **What the budget does not do.** It says nothing about whether an item is good for a particular build. All four on-budget chests cost 100. They will not be equally popular. Section 3 explains why, and why that is usually what you want.
- **Where the price list comes from.** Prices are a policy. Section 4 shows how to derive them from stat weights. Once set, they must be revisited whenever the combat formulas change, or the budget will price yesterday's game.
- **When to go over budget on purpose.** Items with drawbacks, a narrow use or a hard-to-reach source are often given extra budget. Write the reason next to the item. An undocumented overbudget item becomes the item every player of every build wants.

## 3. Stat weights: value to a build

Price is what an item costs the designer. **Value** is what it is worth to a particular player. The link between them is the **stat weight**.

A stat weight is the gain in a chosen outcome per unit of stat, for one build in one gear set:

```
w_s = ΔV / Δs
```

Here `V` is the outcome you care about, usually damage per second for damage dealers, effective HP for tanks, healing per second for healers. `Δs` is a small increase in stat `s`, and `ΔV` is the resulting change in `V`. The value of an item to a build is then

```
value(item, build) = Σ w_s × amount_s
```

This is the same sum as the budget cost, with weights in place of prices. That is why the two are easy to confuse and why keeping them apart is the skill.

SimulationCraft, the combat simulator used by World of Warcraft theorycrafters, computes weights this way. Its documentation calls them scale factors. It runs a baseline fight, adds a fixed amount of one stat, runs the fight again and divides the change in DPS by the change in stat. Raidbots, a service built on it, warns players that these weights move as gear changes because stats interact.

Take three builds for our level 50 chestpieces. Weights are in "DPS-equivalent units per point," normalized so strength is 1.0 for the damage builds.

| Stat | Build X (crit) | Build Y (haste) | Build T (tank, EHP units) |
|---|---|---|---|
| Str | 1.0 | 1.0 | 0.5 |
| Sta | 0 | 0 | 1.0 |
| Crit | 1.1 | 0.5 | 0.3 |
| Haste | 0.5 | 1.1 | 0.3 |

Value of each chestpiece:

| Item | Budget cost | Value to X | Value to Y | Value to T |
|---|---|---|---|---|
| Plate of the Ox | 100 | 50.0 | 50.0 | **125.0** |
| Hauberk of Fury | 100 | 115.0 | 85.0 | 45.0 |
| Swift Tunic | 100 | 77.5 | **122.5** | 42.5 |
| Balanced Mail | 100 | 80.0 | 80.0 | 75.0 |
| Precision Chestguard | 115 | **119.5** | 110.5 | 50.0 |

Check one cell. Swift Tunic for build Y is `40 × 1.0 + 75 × 1.1 = 40 + 82.5 = 122.5`.

Read the table as a designer. Each on-budget specialist item is best for exactly one build. Ox is the tank's chest, Swift is the haste build's chest, and Fury would be the crit build's chest. That is healthy itemization. Different players chase different items. But Precision Chestguard is first for build X and a close second for build Y. It pushes Fury out of the game entirely, and it is the item every damage dealer will farm. That is how a 15% budget error shows up in a live game: one item on everyone's wish list.

Balanced Mail is last or near last for every build. Hybrid items are a known trap. On budget, they spread points across stats that no single build values fully. If you want hybrids to be chosen, you need hybrid builds, or you must give them a budget bonus and write down why.

The interactive's second tab shows this table as a grouped bar chart with a build selector.

## 4. Deriving prices from weights

Where did the price list come from? From the weights. A price should be what a stat is worth to the players who want it, averaged across the builds you expect to see.

```
p_s = Σ_builds share_b × w_s,b   (normalized so the reference stat's price is 1)
```

For the two damage builds, with equal shares:

- Crit: `0.5 × 1.1 + 0.5 × 0.5 = 0.8`.
- Haste: `0.5 × 0.5 + 0.5 × 1.1 = 0.8`.
- Strength: `1.0`.

Those are the prices in section 2. Stamina is not in either damage build's weights, so its price is a policy decision. We priced it at 0.5 because tanks value it and we wanted the tank chest to cost the same as the others.

Three consequences follow.

1. **Prices depend on the population.** If 80% of players pick build Y, the average weight of haste rises to `0.2 × 0.5 + 0.8 × 1.1 = 0.98`, and haste items become underpriced relative to how much the playerbase values them. Watch popularity as well as math.
2. **Prices depend on the combat formulas.** Change how crit works and every crit weight changes, so every item with crit is now mispriced. Budget review belongs in the checklist for any formula change.
3. **Weights are local.** A weight is a slope at one gear set. If crit rating has a cap, its weight drops to 0 past the cap. If crit and crit damage multiply, each one's weight rises as you stack the other. MMO303 week 2 showed the same effect for armor and health, where each makes the other more valuable. A price list built from weights at one gear level will misprice items at another.

## 5. Where linear budgets break

The model in this lecture is linear. Cost is a sum and value is a sum. Real items break that in four common ways. Each has a standard fix.

**Extremes.** Magma Rager showed that an item concentrating everything in one stat can be much worse than its cost, because some stats need others to function. The reverse is also common. Concentrated stats can be much better than their cost when a build needs only one stat. The fix is a nonlinear price. D&D's point buy raises the price per step near the top. Some budget systems instead raise each stat's cost to a power greater than 1 before summing, which makes concentrated items cost more than spread ones.

**Synergy.** When two stats multiply in the damage formula, an item with both is worth more than the sum of its parts. Price the pair as well as each stat, or keep synergistic stats on different slots.

**Caps.** A stat with a cap has a weight that falls to zero at the cap. Items with that stat are fairly priced for new characters and worthless for capped ones. You can price them for the typical player at that item level, or remove the cap and use a divisive formula like the armor curve from MMO303 week 2.

**Procs and effects.** "10% chance on hit to deal 200 damage" has no stat. Price it by expected value, from MA102 week 4. At 2 hits per second it adds `0.10 × 200 × 2 = 40` DPS. Convert that into points using the damage stat's weight. If 1 strength gives 0.5 DPS for the reference build, the proc is worth 80 strength, or 80 points. Then note the variance. A proc that is fair on average can still be swingy enough to change how the item feels.

**Budget growth with item level.** The budget itself follows a curve. If `B(ilvl)` grows by the same factor per item level as the power curve from week 8, items stay in step with characters. If it grows faster, gear outruns levels and players feel stronger than the content. If it grows slower, levels outrun gear and loot feels pointless.

## In-class activity (25 minutes)

Pairs, one laptop each, using the interactive or a spreadsheet.

1. You receive six level 60 items from another pair's design, budget 120, with the price list from section 2. Compute each item's cost and flag any more than 5% off budget.
2. For every flagged item, propose the smallest edit that brings it on budget without changing its identity (which build it is for).
3. Using the three builds in section 3, find which item is best for each build. Is there an item nobody wants? Is there an item everybody wants?
4. Write two sentences for the design review: one item you would fix, and one overbudget item you would ship on purpose with its reason.

Expected output is a completed table (item, cost, verdict, value to X, Y and T) and the two sentences.

## Common misconceptions

- **"Two items with the same stat total are equally strong."** Totals mix cheap and expensive stats. Only priced totals compare.
- **"An on-budget item is balanced."** It costs the right amount. Whether it is worth the right amount depends on the build, and specialist items should be worth more to their build than to others.
- **"Stat weights are fixed numbers for a class."** They are slopes at one gear set. They move when gear, caps or other stats change.
- **"Prices should equal one build's weights."** Then every other build's items are mispriced. Prices average weights over the builds you expect.

## Check yourself

1. Using the section 2 price list, a level 50 chest has 30 Str, 60 Sta and 50 Haste. What is its cost? Is it on budget? Which build in section 3 values it most?
2. A designer adds a new stat, Mastery, with weights 1.3 for build X, 0.9 for build Y and 0.2 for build T. Players are 40% X, 40% Y and 20% T. What price should Mastery have, using all three builds and normalizing so strength costs 1? (Use strength weights 1.0, 1.0 and 0.5.)
3. A ring has a 5% chance on hit to heal 300. A healer build hits 1.5 times per second, and 1 point of Spirit gives 0.25 healing per second. How many Spirit points is the proc worth?
4. Using Hearthstone's `(Attack + Health − 1) / 2`, what should a 3/4 minion with no text cost? What does the formula say about a 7/1, and would you trust it?

<details>
<summary>Answers</summary>

1. `30 × 1.0 + 60 × 0.5 + 50 × 0.8 = 30 + 30 + 40 = 100`, on budget. Values: X `30 + 25 = 55`, Y `30 + 55 = 85`, T `15 + 60 + 15 = 90`. Build T values it most, narrowly over Y.
2. Average Mastery weight `0.4 × 1.3 + 0.4 × 0.9 + 0.2 × 0.2 = 0.92`. Average strength weight `0.4 + 0.4 + 0.1 = 0.9`. Normalized price `0.92 / 0.9 ≈ 1.02` points per Mastery.
3. Expected healing `0.05 × 300 × 1.5 = 22.5` per second. At 0.25 per Spirit, that is `22.5 / 0.25 = 90` Spirit points.
4. `(3 + 4 − 1) / 2 = 3` mana. A 7/1 gives `(7 + 1 − 1) / 2 = 3.5` mana. Do not trust it. Like Magma Rager, a 1-health body dies before its attack matters, so a linear price overstates its worth.

</details>

## Lab / assignment hook

**Lab 09, item budget audit** ([labs/lab09.md](../labs/lab09.md)). You audit a 12-item loot table, find the items that cheap stats and unpriced procs hide, compute stat weights from a small DPS model for two gear sets and re-derive the price list.

## Sources

- Hearthstone Wiki (wiki.gg), card pages "River Crocolisk", "Chillwind Yeti", "Boulderfist Ogre" and "Magma Rager" (Legacy set, originally the Basic set, 2014; moved to Legacy in March 2021). Mana cost, attack and health; Magma Rager's reputation as one of the weakest cards. https://hearthstone.wiki.gg/wiki/Chillwind_Yeti
- HearthPwn and Hearthstone forum discussions of the "vanilla test" (community term, 2014 onward). https://www.hearthpwn.com/forums/hearthstone-general/general-discussion/218420-what-stats-would-a-vanilla-minion-have-to-have-to
- Warcraft Wiki, "Item level" (World of Warcraft, retail, accessed September 2026). Items spend an item-level budget on stats and effects; community-derived formula later confirmed at BlizzCon. https://warcraft.wiki.gg/wiki/Item_level
- SimulationCraft wiki, "StatsScaling". Scale factors as change in DPS divided by stat delta. https://github.com/simulationcraft/simc/wiki/StatsScaling
- Raidbots Support, "Beware of Stat Weights". Weights change with gear because stats interact. https://support.raidbots.com/article/66-beware-of-stat-weights
- Dungeons & Dragons 5th edition *Player's Handbook* (2014), chapter 1, variant "Customizing Ability Scores", 27-point buy with costs 0 to 9 for scores 8 to 15, as summarised by Roll for Two, "Point Buy in D&D 5e". https://www.rollfortwo.com/articles/point-buy-5e/
- Schreiber, I. (2010). *Game Balance Concepts*, level 3, "Transitive Mechanics and Cost Curves" (online course). https://gamebalanceconcepts.wordpress.com/
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press. Chapter "Transitivity and Cost Curves".

## Interactive spec: examples/w09-item-budget.html

**The one insight.** Raw stat totals hide which item is overbudget. Priced in points, the Precision Chestguard is the only item over the line, even though its raw total is average. The two views must sit side by side so the student sees the ranking change.

**Tab 1, "Price the items".**
- Left chart, "Raw stat total (what the tooltip suggests)". Horizontal bars, one per item, sorted by raw total.
- Right chart, "Budget cost in points". Horizontal bars in the same item order as the left chart (do not re-sort, so the jump is visible), with a vertical line at B and a shaded tolerance band of ±5%. Bars beyond the band are coloured as warnings and labelled "+15% over".
- Editable table under the charts. Rows = items, columns = Str, Sta, Crit, Haste, raw total, cost, % of budget. Number inputs for each stat. A second small table with editable prices (defaults 1.0, 0.5, 0.8, 0.8) and budget B (default 100).
- Button "Add item" (up to 8 items) and "Reset to lecture values".
- Test values with defaults: Ox raw 150, cost 100. Fury raw 110, cost 100. Swift raw 115, cost 100. Balanced raw 130, cost 100. Precision raw 130, cost 115 (115%).

**Tab 2, "Value to a build".**
- Grouped bar chart, x = items, bars = value to builds X, Y and T. A dashed reference line at the item's budget cost for comparison.
- Build weight table, editable (defaults below). Highlight the top item for each build.
- Weights: X (Str 1.0, Sta 0, Crit 1.1, Haste 0.5), Y (Str 1.0, Sta 0, Crit 0.5, Haste 1.1), T (Str 0.5, Sta 1.0, Crit 0.3, Haste 0.3).
- Readout "Derived prices from build shares": share sliders for X, Y and T (default 50/50/0) and the resulting price per stat, normalized so Str = 1. With default shares, prices are Crit 0.8, Haste 0.8, Str 1.0, and Sta shows 0 with a note "set by policy".
- Test values: values X/Y/T for Ox 50/50/125, Fury 115/85/45, Swift 77.5/122.5/42.5, Balanced 80/80/75, Precision 119.5/110.5/50. With shares X 80%, Y 20%, T 0 the derived price of Haste is 0.62 and Crit 0.98. With shares X 20%, Y 80%, Haste is 0.98.

**Tab 3, "Vanilla line" (small).**
- Scatter plot of four minions (attack + health on x, mana cost on y) with the line `cost = (A + H − 1) / 2`. Points: River Crocolisk (2, 2/3), Chillwind Yeti (4, 4/5), Boulderfist Ogre (6, 6/7), Magma Rager (3, 5/1). Draw generic circles with text labels only, no card art or logos.
- Note beside Magma Rager: "Priced 2.5 by the line. Played as much worse. The line cannot see that 1 health makes attack useless."

**Formulas.** `raw = Σ amount_s`. `cost = Σ p_s × amount_s`. `value_b = Σ w_s,b × amount_s`. Derived price `p_s = (Σ_b share_b × w_s,b) / (Σ_b share_b × w_Str,b)`.

**Accessibility.** All inputs labelled and keyboard reachable. Values printed on or beside every bar. Warning state uses an icon or text label as well as colour. Charts reflow to stacked single column under 600px.
