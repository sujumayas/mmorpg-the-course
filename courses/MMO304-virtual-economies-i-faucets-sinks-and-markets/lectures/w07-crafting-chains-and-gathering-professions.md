# MMO304 · Week 07 — Crafting Chains and Gathering Professions

**Why this matters:** Crafting is where your economy turns raw materials into the things players want. Every recipe you write sets how much ore the world must produce, who earns gold from it, and whether a crafted item is worth more or less than what went into it. Get the chain wrong and gatherers starve, crafters work at a loss, or the market floods with gear nobody needs.

**You will be able to:**
- Compute the raw materials a finished item really consumes, given recipe quantities, success chances and refund effects.
- Compute the value added (or destroyed) at each stage of a crafting chain.
- Predict the market price of a crafted item when many players craft it for experience rather than profit.
- Design a gathering profession whose hourly income lands where you want it relative to other activities.

**Before class:** Lehdonvirta & Castronova, *Virtual Economies: Design and Analysis* (2014), the chapters on production and on markets. Skim the Old School RuneScape Wiki guide "Pay-to-play Smithing training" and note every method with a negative profit.

**Prerequisites from earlier courses:** GD102 [week 6, converters in Machinations](../../GD102-systems-design-and-game-mechanics/lectures/w06-machinations-diagrams-ii-converters-traders-gates.md) and [week 7, internal economies with sources, drains and converters](../../GD102-systems-design-and-game-mechanics/lectures/w07-internal-economies-sources-drains-converters.md). [MA102 week 4, expected value](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md) (averages over random outcomes). [GD203 week 9, item budgets](../../GD203-combat-and-progression-design/lectures/w09-item-budgets-and-stat-weights.md) (pricing an item in one currency). From this course, [week 3, faucets, sinks and transformations](w03-faucets-sinks-and-transformations.md) and [week 6, supply and demand in auction houses](w06-supply-demand-and-equilibrium-in-auction-houses.md).

**Interactive:** [Crafting chain cost and market price](../examples/w07-crafting-chain.html). Set the chain on the left, then push experience crafters past the kink on the right.

---

## 1. Crafting is a transformation

In week 3 you sorted every rule in an economy into four kinds. Three of them matter here. A **faucet** creates something from nothing (a monster drops gold). A **sink** destroys something (a vendor takes your gold for a mount). A **transformation** turns one thing into another. Crafting is the largest transformation in most MMOs. Ore goes in, a bar comes out. Bars go in, a breastplate comes out.

A transformation creates no currency and destroys none. What it does is change the *form* of value, and that has three consequences you control as a designer.

First, it sets **derived demand**. Nobody wants iron ore for its own sake. Players want ore because someone wants the breastplate. So the demand for every raw material is the demand for everything made from it, multiplied through the recipes. If you change one recipe at the top of a chain, the price of ore at the bottom moves.

Second, it decides **who gets paid**. Every stage is a job. Gatherers sell raw materials, refiners sell intermediate goods, crafters sell finished ones. The chain's shape decides how many jobs exist and how much each pays.

Third, it can act as a **hidden sink**. If a crafted item sells for less than its materials cost, value leaves the economy at the crafting bench. The ore is gone. What replaced it is worth less. You will see a real case of this in section 2, and a model for when it happens in section 3.

A few terms before we start:

- A **crafting chain** is the sequence of recipes from raw material to finished good. A *linear* chain has one input per stage. A *branching* chain combines several inputs.
- A **gathering profession** is a player activity that turns time into raw materials: mining, herb picking, skinning, fishing.
- A **bill of materials** is the full list of raw inputs one finished item consumes, after following every recipe down to the bottom.
- **Value added** at a stage is the price of what comes out minus the cost of what goes in.

## 2. Worked example: the recipe says five, the ore says ten

### The hook

In Old School RuneScape, an iron platebody is smithed from 5 iron bars. Each iron bar is smelted from 1 iron ore. So a platebody costs 5 ore, right?

It costs 10. When you smelt iron ore at a normal furnace, there is a 50% chance the ore is too impure and simply vanishes. No bar, no experience. Half your ore disappears on average, so each bar costs 2 ore, and 5 bars cost 10.

Then look at the market. On the day this lecture was written, the Old School RuneScape Wiki listed iron ore at 73 coins on the Grand Exchange and the iron platebody at 87 coins. Ten ore cost about 730 coins. The finished platebody sells for about 87. The crafting bench destroys roughly 88% of the value that goes into it. Players do it anyway, by the thousand.

Two things are going on. One is arithmetic. Success chances multiply through a chain, so the recipe card understates the real cost. The other is economics. Most platebodies are made to train the Smithing skill, not to sell. This section handles the arithmetic. Section 3 handles the economics.

### The model

For each stage `i` of a chain, define the **effective input ratio**:

```
e_i = q_i × (1 − r_i) / s_i
```

- `q_i` is the recipe quantity, meaning how many units of the input the recipe lists per attempt.
- `s_i` is the success chance of one attempt (1 if it always works).
- `r_i` is the expected share of inputs saved or refunded (0 if there is no such effect).

`e_i` is the expected number of input units consumed per unit of output. For a linear chain, the raw material per finished item is the product of the stage ratios:

```
R = e_1 × e_2 × … × e_n
```

For a branching chain, you compute `e` for each input separately and add the paths. The expected cost of one finished item, at raw price `p`, is `C = R × p` plus any fees along the way.

Why a product? Because each stage's output is the next stage's input. If stage 2 needs 5 bars and each bar needs 2 ore, the platebody needs `5 × 2 = 10` ore. This is expected value from MA102 week 4 applied one stage at a time. A single smelt either uses 1 ore and gives a bar or uses 1 ore and gives nothing. Over many attempts, the average is 2 ore per bar.

### Numbers you can check

The iron platebody chain in Old School RuneScape:

| Stage | Recipe `q` | Success `s` | Refund `r` | Effective ratio `e` |
|---|---|---|---|---|
| Smelt iron bar | 1 iron ore | 0.5 | 0 | 2 ore per bar |
| Smith platebody | 5 iron bars | 1 | 0 | 5 bars per platebody |
| Whole chain | | | | `R = 2 × 5 = 10` ore |

The same chain when the smelter wears a ring of forging, casts Superheat Item, or uses the Blast Furnace (each makes iron smelting always succeed):

| Stage | `q` | `s` | `e` |
|---|---|---|---|
| Smelt iron bar | 1 | 1 | 1 |
| Smith platebody | 5 | 1 | 5 |
| Whole chain | | | `R = 5` ore |

One change to one success chance halves the ore the world must mine for every platebody. That is the lever you hold when you set a success rate.

The steel platebody shows a branching chain. A steel bar takes 1 iron ore and 2 coal with no failure chance, and a steel platebody takes 5 steel bars:

| Input path | Per bar | Bars | Per platebody |
|---|---|---|---|
| Iron ore | 1 | 5 | 5 |
| Coal | 2 | 5 | 10 |

Each steel platebody pulls 5 iron ore and 10 coal out of the world. If you want to know how much mining your server needs to support a given demand for steel armour, you multiply demand by this bill of materials.

Now put a price on it. Using the snapshot prices above, the iron platebody's material cost is `10 × 73 = 730` coins. With guaranteed smelting it is `5 × 73 = 365`. The market price of about 87 sits far below both. Hold that thought.

### A visual the student can move

Open the interactive. The left panel shows a two-stage chain as a bar of raw material. You set `q`, `s` and `r` for each stage, and the bar grows or shrinks to show `R`. A faint outline shows the "recipe card" count, `q_1 × q_2`, so you can see the gap that success chances and refunds create. Drag stage 1's success chance from 1 down to 0.5 and watch the real bar double while the recipe outline stays still.

The right panel is the market for the finished item. Leave it for section 3.

### Cross-game recognition

The effective-ratio formula appears in many disguises. The skill is seeing that each game's rule changes one of `q`, `s` or `r`.

**EVE Online (current).** Manufacturing uses blueprints. Researching a blueprint's Material Efficiency (ME) up to level 10 cuts the materials it needs by up to 10%. In our terms `r = 0.10` at ME 10. EVE adds two rules that break the smooth formula. Material counts are rounded up to a whole number *after* multiplying by the number of runs, and no material can drop below one unit per run. So an input listed at 3 units saves nothing on a single run (`3 × 0.9 = 2.7`, rounded up to 3) but saves 3 units across 10 runs (`30 × 0.9 = 27`). An input listed at 1 unit never gets cheaper at all. Industrialists batch their jobs for exactly this reason. The formula is the same, with a `ceil()` wrapped around it.

**World of Warcraft (Dragonflight onward, from patch 10.0.0 in October 2022).** Crafting professions gained a stat called Resourcefulness, which gives a chance for a craft to use fewer reagents. A chance of saving a share of the inputs is an expected refund: `r = (proc chance) × (share saved)`. If a crafter has a 20% proc chance that saves 30% of the reagents (invented numbers, for illustration), then `r = 0.2 × 0.3 = 0.06`, and the chain consumes 6% less raw material on average.

**Old School RuneScape again.** The ring of forging, Superheat Item and Blast Furnace do not change `q` or `r`. They set `s = 1`. Three different player-facing features, one parameter.

Three games, three mechanics, one line of arithmetic. When you read a new crafting system, list every rule and ask which of `q`, `s` or `r` it touches. If a rule touches none of them, it is changing something else, such as the time per craft or who may craft.

### Eyes-open design judgment

The effective ratio is the knob that ties your crafting to your gathering. Some decisions to make on purpose:

- **Failure chances are ore sinks.** A 50% failure chance at the bottom of a chain doubles the raw demand of everything above it. That can be a good way to keep gatherers busy. It is also invisible to players unless you show it. If your recipe window says "5 bars" and the real cost is 10 ore, show the expected ore cost somewhere, or players will feel cheated when they run out.
- **Upgrades that set `s = 1` are demand cuts.** Every time you add a way to make a stage reliable, you cut the world's demand for the raw input. Old School RuneScape can afford to, because iron is cheap and the upgrades cost something (a ring that wears out, a spell that uses runes, a minigame with a fee). Price your reliability upgrades so they are a trade-off, not a free halving.
- **Refunds reward specialists.** A refund stat like Resourcefulness makes a dedicated crafter's goods cheaper to produce than a casual crafter's. That creates a reason to buy from specialists instead of crafting yourself, which is good for a market. It also means specialists will undercut everyone else, so casual crafting stops paying.
- **Rounding rules reward batching.** EVE's round-up-per-job rule makes small jobs wasteful. That pushes industry toward large, planned operations. If you want casual crafting, avoid rounding that punishes small batches.

## 3. Crafting at a loss: the experience crafter

Back to the puzzle. Why does a platebody that costs 365 to 730 coins in ore sell for about 87?

Because most of the people making it are not trying to sell it. They are buying Smithing experience. The Old School RuneScape Wiki's Smithing training guide lists iron platebodies as a method for levels 33 to 39, using 620 iron bars at a total profit of about −108,900 coins. That guide's money figures assume you buy bars. Dividing, `620 / 5 = 124` platebodies, so each one loses about 878 coins. The guide lists other methods, including gold bars at the Blast Furnace, that cost players coins for every point of experience they earn. Players accept the loss because the level is what they want.

This happens in any game where crafting is also progression. Call the two kinds of crafter:

- **Profit crafters**, who craft only if the item sells for at least its cost `C`. They will make as many as the market wants at price `C`, and none below it.
- **Experience crafters**, who craft a fixed number `X` per day regardless of price, because the experience is the point. They sell whatever they make for whatever it fetches.

Let players demand the item according to a straight demand curve (week 6):

```
Q_d = a − b × P
```

- `a` is how many players would take one if it were free.
- `b` is how many fewer they want per coin of price.

At price `C`, players want `a − b × C` items. Two cases follow.

**Case 1, few experience crafters (`X < a − b × C`).** Experience crafters cover part of demand. Profit crafters fill the gap at price `C`. The market price equals the cost. Crafting is a fair transformation.

**Case 2, many experience crafters (`X ≥ a − b × C`).** Experience crafters alone make more than the market wants at cost. Profit crafters quit. The price falls until buyers take all `X` items:

```
P = (a − X) / b
```

The price has come unstuck from the cost. Each item now destroys `C − P` of value.

Most games also have a **floor** `F`: a price below which some sink buys everything. In Old School RuneScape that floor comes from the High Level Alchemy spell, which turns an item into a fixed number of coins (336 for an iron platebody) at the cost of a nature rune. When `(a − X) / b` would fall below `F`, the price sticks at `F` and the alchemy sink absorbs the surplus. Notice what that floor is. It turns the item into coins from nothing, so it is a faucet. The crafting chain ends in a gold faucet.

### Numbers you can check

An invented market with cost `C = 730`, demand `Q_d = 1,200 − 1.5 × P` per day, and a floor `F = 60`:

| Experience crafters `X` per day | Market price | Profit crafters make | Value destroyed per item |
|---|---|---|---|
| 0 | 730 | 105 | 0 |
| 100 | 730 | 5 | 0 |
| 500 | 466.7 | 0 | 263.3 |
| 1,000 | 133.3 | 0 | 596.7 |
| 1,200 | 60 (floor) | 0 | 670 |

The switch happens at `X = 1,200 − 1.5 × 730 = 105`. Below it, the price equals the cost and the only question is who makes the items. Above it, every extra experience crafter pushes the price down by `1 / 1.5 ≈ 0.67` coins until the floor catches it.

Now open the right panel of the interactive. Its horizontal line is the cost `C` from the left panel. Drag the experience-crafter slider past the kink and watch the price leave the cost line. Then go back to the left panel and turn on guaranteed smelting. The cost line drops to 365. The market price barely moves, because it was never set by cost in the first place.

### Where the money goes

It is tempting to say that 596.7 coins "vanish" with every item at `X = 1,000`. They do not. The experience crafter paid a gatherer 730 coins for ore and received 133.3 from a buyer. The coins moved from crafters to gatherers and buyers. What vanished was ore, turned into a platebody worth less.

That has a consequence for gathering. **Experience crafters are the gatherers' best customers.** They buy raw materials at whatever it takes and do not care that the output is worth little. If you remove experience from a craft (or make it cheap to level some other way), you remove a large block of demand for the raw material, and gatherers' income falls. Plan any change to crafting experience as a change to gathering income too.

## 4. Gathering professions: what an hour is worth

Gathering turns playtime into raw materials. The price of those materials, over the long run, is set less by crafting than by what else players could do with the hour.

### The opportunity-cost price

Suppose a player can earn `W` gold per hour from the best other activity open to them (questing, dungeon runs, selling drops). Gathering yields `u` units per hour. A player gathers only if `u × p ≥ W`, where `p` is the raw material's price. If many players are able to gather, the price settles near the break-even point:

```
p ≈ W / u
```

With `W = 6,000` gold per hour and `u = 120` ore per hour, ore settles near 50 gold. Double the ore per hour (a faster mining tool, more nodes) and the long-run price halves. The gatherer earns the same per hour. The crafter's cost falls.

This is why gatherers often complain that "gathering doesn't pay." In a free market with easy entry, it pays about what everything else pays. It cannot pay more for long, because players would switch to it.

### Shared nodes and crowding

Most MMOs place resource nodes in the open world, where they respawn at a fixed rate. If a zone produces `N_r` ore per hour across all its nodes, and `n` gatherers share it, each gets at most `N_r / n` ore per hour. When the zone is crowded, `u` falls, and by the formula above the price must rise before gathering pays again. Crowding on a new expansion's first day is why fresh raw materials sell for many times their later price.

Bots break this. A bot's "best other activity" is nothing, so its `W` is close to zero. Bots will gather at any positive price, and they crowd human gatherers out of nodes. The result is low raw prices, cheap crafting and humans who stop gathering. MMO309 returns to this ([syllabus](../../MMO309-security-anti-cheat-and-anti-bot/syllabus.md)).

### Profession structure: who can do what

World of Warcraft lets a character learn at most two primary professions at a time. Its gathering professions (Herbalism, Mining, Skinning) pair naturally with crafting professions (Alchemy, Blacksmithing, Leatherworking), and the game's own documentation notes that pairing a gatherer with its matching crafter reduces reliance on the auction house.

That limit is an economic design choice:

- **With a limit**, no character can do everything, so players must trade. The limit creates the market.
- **Without a limit**, as in Old School RuneScape where every character can train every skill, trade still happens, but it is driven by time rather than permission. A high-level player could mine their own ore and chooses to buy it because their hour is worth more elsewhere. That is the opportunity-cost rule again.

Both work. The limit gives you stronger interdependence early and at the cost of alt characters, since players who want every profession simply roll more characters. The open design gives you fewer alts, and the market rests on opportunity cost, which you tune through `u` and `W`.

## 5. Designing a chain

When you design a crafting chain, work top-down and then bottom-up.

1. **Top-down: set the finished item's role.** Is it progression gear, a consumable, a cosmetic? Consumables are the healthiest crafted goods because they are destroyed on use, so demand never saturates. Gear saturates unless something destroys it, which is next week's topic.
2. **Compute the bill of materials.** For each finished item, compute `R` for every raw input. Multiply by expected daily demand. That is the gathering your world must supply.
3. **Bottom-up: check the gatherers.** At your expected price `p ≈ W / u`, is the gathering hour competitive with your other activities? If you want gathering to be a real job, it must pay about as well as a dungeon run.
4. **Decide what experience does.** If crafting grants progression, expect Case 2 from section 3 for low-level items. Decide whether you are fine with those items flooding the market at the floor. Old School RuneScape accepts it. A game that wants low-level crafted gear to sell at a profit must limit experience crafting, for example with experience that only comes from items actually sold or used.
5. **Add intermediate goods on purpose.** Every stage is a job and a market. Too few stages and crafting feels thin. Too many and the chain is tedious. Each intermediate good should have more than one use, or it is just a delay.

## In-class activity (25 minutes)

In groups of three, design a two-stage chain for healing potions in a small MMO.

1. Choose recipe quantities, a success chance for each stage, and one refund mechanic. Compute `R` for each raw input.
2. Expected demand is 2,000 potions per day across the server. How many herbs per day must players gather?
3. Gathering yields 90 herbs per hour, and the best alternative activity pays 4,500 gold per hour. Estimate the long-run herb price and the potion's material cost.
4. Crafting potions grants Alchemy experience. Players who are leveling will make about 3,000 potions per day regardless of price. Using `Q_d = 5,000 − 10 × P`, is the market in Case 1 or Case 2? What is the potion price?

Expected output: the chain with numbers, the daily herb requirement, the potion price, and one sentence on whether you would change the experience rule.

## Common misconceptions

- **"The recipe tells you the cost."** Only when every stage always succeeds and nothing is refunded. Success chances divide and refunds multiply through every stage below. Compute `R`.
- **"If crafted items sell below material cost, the market is broken."** Not necessarily. When crafting is progression, experience crafters are buying levels, and the low price is a side effect. Decide whether you want that; don't assume it's a bug.
- **"Crafting at a loss destroys gold."** It destroys items. The gold moves from crafters to gatherers. That transfer is what keeps gathering worth doing.
- **"Making gathering faster helps gatherers."** In the long run it lowers the raw price and helps crafters and buyers. Gatherers' hourly income returns to what other activities pay.

## Check yourself

1. A recipe needs 4 leather per armour piece and always succeeds. Each leather is tanned from 3 hides with a 75% success chance. How many hides does one armour piece consume on average? What if a crafting stat refunds 10% of the leather on average?
2. In EVE Online, a blueprint needs 7 units of a mineral per run. At Material Efficiency 10, how many units does a single run need? How many do 10 runs need?
3. In the invented market of section 3 (`C = 730`, `Q_d = 1,200 − 1.5 × P`), the designer halves the cost to 365 by adding guaranteed smelting. With `X = 1,000`, what is the new price? With `X = 50`?
4. Ore takes 120 per hour to gather and the best alternative pays 6,000 per hour. A patch doubles node density, so gatherers now get 200 per hour. Estimate the long-run ore price before and after. What happens to the iron platebody's material cost from section 2?

<details>
<summary>Answers</summary>

1. Leather stage: `e = 3 / 0.75 = 4` hides per leather. Armour stage: `e = 4` leather. `R = 4 × 4 = 16` hides. With a 10% refund on the armour stage, `e_2 = 4 × 0.9 = 3.6`, so `R = 4 × 3.6 = 14.4` hides.
2. One run: `7 × 0.9 = 6.3`, rounded up to 7. No saving. Ten runs: `70 × 0.9 = 63` units, a saving of 7.
3. Demand at the new cost is `1,200 − 1.5 × 365 = 652.5`. With `X = 1,000`, `X > 652.5`, so Case 2 and `P = (1,200 − 1,000) / 1.5 = 133.3`. The price does not move. With `X = 50`, Case 1, so `P = 365` and profit crafters make about 602 items.
4. Before: `6,000 / 120 = 50`. After: `6,000 / 200 = 30`. The iron platebody's material cost at 10 ore drops from 500 to 300 (or from 250 to 150 with guaranteed smelting). If the market is in Case 2, its price does not change.

</details>

## Lab / assignment hook

[Lab 07, crafting chain workbook](../labs/lab07.md). You build a spreadsheet that computes the bill of materials for a three-stage branching chain, then find the experience-crafting volume at which the finished item's price leaves its cost. The workbook feeds the models assignment (30%).

## Sources

- Old School RuneScape Wiki, "Iron bar" (current game). Smelting iron ore has a 50% chance to fail without a ring of forging; Superheat Item and the Blast Furnace also guarantee success.
- Old School RuneScape Wiki, "Steel bar" (current game). A steel bar takes 1 iron ore and 2 coal; a steel platebody takes 5 steel bars.
- Old School RuneScape Wiki, "Iron platebody" and "Iron ore" (current game). An iron platebody takes 5 iron bars; high alchemy value 336 coins. Grand Exchange guide prices of 87 (platebody) and 73 (ore) coins as displayed when accessed in September 2026. These prices move daily; treat them as a snapshot.
- Old School RuneScape Wiki, "Pay-to-play Smithing training" (current game, accessed September 2026). Iron platebodies for levels 33-39 using 620 iron bars at a listed profit of about −108,900 coins; Blast Furnace gold bars listed at a negative coins-per-experience rate.
- EVE University Wiki, "Research" (current game). Material Efficiency research to level 10 reduces materials by up to 10%; rounding up happens after multiplying by runs; no material falls below one unit per run.
- Warcraft Wiki, "Resourcefulness (attribute)". Introduced with Dragonflight, patch 10.0.0 (October 2022); gives a chance to craft with reduced reagent cost. The proc numbers in this lecture are invented.
- Warcraft Wiki, "Profession" (current game). Two primary professions per character; gathering and production lists; pairing a gatherer with its matching crafter reduces auction house reliance.
- Lehdonvirta, V. & Castronova, E. (2014). *Virtual Economies: Design and Analysis*. MIT Press.

## Interactive spec: examples/w07-crafting-chain.html

**The one insight:** the recipe card understates what a crafted item consumes, because success chances and refunds multiply through the chain; and once experience crafters make more than the market wants at cost, the market price detaches from cost entirely, so lowering cost does nothing to price.

**Layout:** two linked panels side by side on desktop, stacked on mobile. Left: "What it really costs". Right: "What it sells for". Exact numbers printed under each panel.

**Left panel, chain cost.**
- Controls for stage 1 (raw to intermediate) and stage 2 (intermediate to finished): recipe quantity `q` (integer slider 1-10), success chance `s` (slider 0.10-1.00, step 0.05), refund `r` (slider 0-0.50, step 0.01). Raw price `p` (slider 1-200, default 73). Checkbox "Round up per craft (EVE rule)" that applies `ceil` to `q × (1 − r)` at each stage before dividing by `s`, with a minimum of 1.
- Formulas: `e_i = q_i × (1 − r_i) / s_i` (or `max(1, ceil(q_i × (1 − r_i))) / s_i` with rounding on). `R = e_1 × e_2`. Cost `C = R × p`.
- Visual: a horizontal bar of length `R` made of raw-material units, with a dashed outline of length `q_1 × q_2` labelled "recipe card". Print `e_1`, `e_2`, `R` and `C`.
- Preset buttons: "OSRS iron platebody" (`q1=1, s1=0.5, r1=0, q2=5, s2=1, r2=0, p=73`), "with ring of forging" (same with `s1=1`), "EVE-style refund" (`q1=3, s1=1, r1=0.10, q2=5, s2=1, r2=0`, rounding on).

**Right panel, market.**
- Controls: demand intercept `a` (slider 200-3,000, default 1,200), slope `b` (slider 0.5-5, step 0.1, default 1.5), experience-crafter output `X` (slider 0-2,000, default 0), floor `F` (slider 0-300, default 60).
- Formulas: `threshold = a − b × C`. If `X < threshold`, `P = C`, profit crafters make `threshold − X`. Else `P = max(F, (a − X) / b)`. Value destroyed per item `= max(0, C − P)`.
- Visual: price on the y axis, quantity on the x axis. Draw the demand line, the horizontal cost line at `C` (linked from the left panel), a vertical line at `X`, and the floor as a dotted horizontal line. Mark the equilibrium point. Shade the gap between `C` and `P` in the warning colour when `P < C`. A second small line chart below plots `P` against `X` from 0 to 2,000 for the current `C`, showing the flat segment, the kink at the threshold, the falling segment and the floor.
- Print `threshold`, `P`, profit-crafter output, value destroyed per item and `X × (C − P)` per day.

**Test values (the builder must reproduce these):**
- OSRS preset: `e1 = 2`, `e2 = 5`, `R = 10`, `C = 730`. With ring of forging: `R = 5`, `C = 365`.
- EVE-style preset with rounding on: `e1 = ceil(2.7) = 3`, `e2 = 5`, `R = 15`. Rounding off: `e1 = 2.7`, `R = 13.5`.
- Market with `C = 730`, `a = 1,200`, `b = 1.5`, `F = 60`: threshold 105. `X = 100` gives `P = 730`, profit crafters 5. `X = 500` gives `P = 466.7`. `X = 1,000` gives `P = 133.3`. `X = 1,200` gives `P = 60` (floor).
- Same market with `C = 365` and `X = 1,000`: `P = 133.3` (unchanged).

**Accessibility:** all sliders have visible labels and keyboard steps; the kink point and the "price has left cost" state are announced in a live text line ("Price equals cost" or "Price is X below cost"). No game art; draw ore and bars as plain shapes.
