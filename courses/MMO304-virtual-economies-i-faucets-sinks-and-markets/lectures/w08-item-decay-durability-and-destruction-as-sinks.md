# MMO304 · Week 08 — Item Decay, Durability and Destruction as Sinks

**Why this matters:** Every item your game creates stays in the world until a rule takes it out. If nothing does, every player eventually owns everything, crafters have no customers and drops stop mattering. Durability, decay and destruction are the rules that take items out. Choosing among them decides whether your economy runs on repair bills, on replacement, or on nothing at all.

**You will be able to:**
- Compute the steady-state number of an item in the world from its creation rate and its destruction rate, and how fast the world gets there.
- Distinguish a durability system that sinks gold from one that sinks items, and predict the effect of each on crafters.
- Compute the gold a repair system removes per hour of play.
- Choose a destruction rate that holds an item's ownership near a target share of players.

**Before class:** Lehdonvirta & Castronova, *Virtual Economies: Design and Analysis* (2014), chapter 11, "Macroeconomic Design". Look at the "Mining, Production and Destruction History" chart in any recent CCP *Monthly Economic Report* for EVE Online.

**Prerequisites from earlier courses:** [MA102 week 7, the geometric distribution](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w07-geometric-distribution-kills-until-the-drop.md) (the mean wait `1/p`). [MA101 week 4, exponentials](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w04-exponentials-and-the-xp-curve.md) (repeated multiplication by `1 − d`). [GD102 week 2, stocks and flows](../../GD102-systems-design-and-game-mechanics/lectures/w02-stocks-and-flows.md). From this course, [week 3, faucets, sinks and transformations](w03-faucets-sinks-and-transformations.md) (flow sinks versus stock sinks), [week 2, value](w02-functional-hedonic-and-social-value.md) (obsolescence wipes functional value) and [week 7, crafting chains](w07-crafting-chains-and-gathering-professions.md).

**Interactive:** [Item stock and destruction rate](../examples/w08-item-stock-decay.html). Drag `d` from 0 to 2% and watch the stock level off and the price hold.

---

## 1. Four ways an item leaves

Week 3 was mostly about money. This week we apply the same stock-and-flow thinking to items. An item enters the world through a faucet (a drop, a quest reward, a vendor) or a transformation (crafting). The **item stock** is how many copies exist. The stock only shrinks when some rule removes copies. There are four such rules, and they behave very differently.

1. **Consumption.** The item is used up by design. A potion, an arrow, a scroll. Consumption is the cleanest item sink because the player chose to spend the item and got something for it.
2. **Destruction.** The item is lost, usually through failure. Your ship explodes, your gear drops on death and the killer takes only part of it, an upgrade attempt breaks the item. The copy is gone.
3. **Durability with repair.** The item wears down with use and you pay to restore it. The item never leaves. What leaves is gold, paid to a non-player repairer. This is a **gold sink wearing an item's clothes**.
4. **Obsolescence.** The item stays in the world, and a new tier of content makes it useless. Its copies still exist but nobody wants them. The value leaves, not the item. Week 2 called this the sink for functional value.

Three terms before the model:

- **Durability** is a number on an item that falls with use or with death. At zero the item stops working until it is repaired, or it is destroyed, depending on the game.
- **Decay** is durability loss driven by time or use rather than by a specific event.
- **Destruction rate** `d` is the share of the item stock removed per day, averaged over all copies.

## 2. Worked example: why nothing in EVE lasts and everything in WoW does

### The hook

In World of Warcraft you can die a thousand times in the same sword and still own the sword. Each death costs 10% of the maximum durability of every item you wear. Taking resurrection from a spirit healer costs another 25%, on items in your bags too. At zero durability a weapon becomes unusable and armour gives no stats. But the item is never destroyed. You pay a repair bill and it is whole again.

In EVE Online, the first time you lose a fight in a ship, the ship is gone. CCP's *Monthly Economic Report* for August 2026 notes that the month's largest battle, in the Pochven region, destroyed about 9,000 ships. The report plots destruction on the same chart as mining and production, because in EVE destruction is half of the economy.

Both games call their system "durability" or "loss". One removes gold and keeps items forever. The other removes items. They produce completely different markets, and one small model shows why.

### The model

Let `S` be the number of copies of one item type in the world. Each day:

```
S(next day) = S + F − d × S
```

- `F` is the number of new copies created per day (drops plus crafting).
- `d` is the destruction rate, the share of existing copies destroyed per day.
- `N` is the number of players who want one copy each.

If `d = 0`, the stock grows by `F` every day, forever: `S(t) = F × t`.

If `d > 0`, the stock grows until destruction catches up with creation. That happens when `d × S = F`, so the **steady-state stock** is:

```
S* = F / d
```

Starting from zero, the stock approaches `S*` along the curve from MA101 week 4:

```
S(t) = S* × (1 − (1 − d)^t)
```

It gets halfway to `S*` after about `0.69 / d` days (exactly `ln 0.5 / ln(1 − d)`).

Two more facts come free. If each copy has chance `d` of being destroyed each day, its lifetime follows the geometric distribution from MA102 week 7, so the **mean lifetime** of a copy is `1 / d` days. And the **coverage**, the share of players who could own one, is `S* / N`.

That last number is the designer's lever. If you want an item to be owned by a share `c` of the players who want it, set:

```
d = F / (c × N)
```

### What coverage does to price

To see why coverage matters, give the item a simple market. Suppose the `N` players value the item at amounts spread evenly from 0 up to `P_max`, and the keenest buyers get theirs first. When `S` copies are owned, the buyers still waiting value it at most `P_max × (1 − S / N)`, so that is roughly the price of the next copy:

```
P ≈ P_max × (1 − S / N)
```

The price falls as coverage rises, and hits zero when everyone who wants one has one. In practice the price stops at a **floor**, often what a vendor pays, because below that sellers dump to the vendor instead.

### Numbers you can check

A server with `N = 10,000` players who each want one copy of a mid-level breastplate. Drops and crafting create `F = 100` copies per day. `P_max = 1,000` gold, and a vendor buys any copy for 50 (the floor).

| Destruction rate `d` | Mean lifetime | Steady stock `S*` | Coverage `S*/N` | Days to reach half of `S*` | Long-run price |
|---|---|---|---|---|---|
| 0 | forever | no limit (`100 × t`) | 100% on day 100, then more | — | floor (50) from day 95 |
| 0.5% per day | 200 days | 20,000 | 200% | 138 | floor (50) from day 129 |
| 1% per day | 100 days | 10,000 | 100% | 69 | floor (50) from day 299 |
| 2% per day | 50 days | 5,000 | 50% | 34 | 500 |
| 5% per day | 20 days | 2,000 | 20% | 13.5 | 800 |

With no destruction, the price reaches the vendor floor on day 95, when 95% of the players who want the breastplate own one, and everyone owns one by day 100. After that, every new copy is surplus and sells at the vendor floor. Crafters who make breastplates have no customers except new players.

With 2% daily destruction, the stock levels off at 5,000. Half the players who want one own one at any moment, the rest are shopping, and the price holds at about 500. Every day 100 copies are destroyed, so every day 100 new copies find buyers. **Destruction is what makes demand for crafted goods recurring.**

Check the design rule. To hold coverage at 50% with `F = 100` and `N = 10,000`, `d = 100 / (0.5 × 10,000) = 0.02`. That matches the table.

### A visual the student can move

Open the interactive. The top view plots `S(t)` over one year, with a dashed line at `N` (everyone owns one) and a ghost line for `d = 0`. The bottom view plots the price over the same year. Set `d = 0` and watch the stock ramp straight through the `N` line while the price slides to the floor and stays there. Now drag `d` up to 2%. The stock curve bends and flattens at 5,000, and the price levels off at 500 instead of collapsing. Drag `F` up and down. With `d = 0`, a bigger `F` only brings the collapse forward. With `d > 0`, it moves the level where the curve settles.

The two views are the point. The stock view looks like "more items, good". The price view shows what more items do to the people who make them.

### Cross-game recognition

Every durability rule can be written as a choice between moving gold (repair) and moving items (`d`).

**World of Warcraft (current, patch 12.0.7).** Death costs 10% durability on equipped items, plus 25% more from a spirit healer. Zero durability disables the item but never destroys it. In our model, `d = 0` for gear. Durability exists to charge gold, as week 3 described. WoW keeps its gear market alive by other means, chiefly obsolescence (new tiers each patch) and soulbound gear, which binds to the player who picks it up or equips it and can no longer be traded or sold on the auction house. It runs its item economy on consumables, where consumption supplies the `d`.

**EVE Online (current).** When a ship is destroyed, the hull is gone. Insurance pays out a share of CCP's estimate of the hull's value, not its market price, and covers nothing that was fitted to the ship or carried in it. So destruction here is an item sink with a small ISK faucet attached. EVE's daily `d` for combat ships is high, the players who build ships always have buyers, and the whole manufacturing economy of week 7 rests on it.

**Old School RuneScape, Barrows equipment (current).** Barrows armour and weapons degrade over 15 hours of combat. At zero the item cannot be equipped until repaired. A fully degraded set costs 330,000 coins to repair at a non-player repairer. A player-owned armour stand charges `NPC price × (1 − Smithing level / 200)`, so at Smithing 99 the same repair costs 166,650. The item is never destroyed, so as in WoW, `d = 0` and this is a gold sink. It scales with combat time, the flow sink of week 3.

**Diablo II (original game and Lord of Destruction).** Weapons and armour lose durability and need repair. Blizzard's own guide notes that rings and amulets never need repair at all. Remember that detail. It matters in week 9, when a ring becomes the game's money.

Four games, one question. When durability hits zero, does the item leave the world, or does gold? Write down the answer and you know which market the rule is feeding.

### Eyes-open design judgment

- **Repair-only durability feeds nobody but the sink.** It removes gold, which may be what you need, but it does nothing for crafters. If you want a crafting economy for gear, you need `d > 0` somewhere, or obsolescence on a schedule.
- **Destruction feels like loss.** Players hate losing things they own, more than they enjoy gaining the same amount. EVE makes destruction acceptable by making it the core of the game, by selling insurance, and by letting players see that ships are affordable and replaceable. A theme-park MMO that destroys gear on death will lose casual players fast. Soften destruction with insurance, partial drops, or making the destroyed thing cheap relative to income.
- **Pick `d` from the coverage you want, not from feel.** The formula `d = F / (c × N)` lets you start from a design goal ("about half of mid-level players should be shopping for this at any time") and derive the rate.
- **`N` changes over time.** Coverage is `S* / N`. If your population falls, the same `d` gives higher coverage and lower prices. If a new expansion brings players back, coverage drops and prices spike. Revisit `d` with the population.
- **Know what zero durability means in your game.** "Broken but repairable" and "destroyed" are different economies. Players will ask. Your item tooltip should say.

## 3. Repair as a gold sink: pricing the bill

When durability ends in repair, the sink is gold, and you can compute its size.

For wear driven by time or use (Barrows-style):

```
gold sink per hour = full repair cost / lifespan in hours
```

For wear driven by death (WoW-style):

```
gold sink per hour = deaths per hour × durability lost per death × full repair cost
```

The first formula with the Barrows numbers: `330,000 / 15 = 22,000` coins per hour of combat at the non-player repairer, or `166,650 / 15 = 11,110` per hour with Smithing 99. Old School RuneScape made repair cheaper for players who trained a skill. That turns a flat sink into one that is lighter for invested players, and it makes Smithing worth more to the player who trained it.

The second formula needs invented numbers, since WoW repair prices depend on item level and change with every expansion. Say a full set of gear costs 50 gold to repair from zero, and a player dies 3 times an hour in a hard dungeon, with no spirit healer:

```
3 × 0.10 × 50 = 15 gold per hour
```

A raid group learning a boss might wipe 10 times an hour: `10 × 0.10 × 50 = 50` gold per hour each. The sink hits failing players hardest. That may be what you want (it discourages throwing bodies at content) or it may feel cruel, in which case you cap it or waive it on certain failures.

### Where repair fits in the money model

Repair is a **flow sink**. It scales with play time, not with the money stock. Week 3 showed that flow sinks set the pace at which players get richer but cannot on their own put a ceiling on money per player. Week 4 added that flat sinks fall hardest on poor players. Durability repair has both properties. It is a good pacing tool and a bad inflation cure. Use it to tune how fast income grows, and use stock sinks (taxes, luxury goods) to hold the level.

## 4. Obsolescence: the sink that leaves the items behind

A new raid tier makes last tier's gear obsolete. Nothing is destroyed, yet the old gear's price falls to the floor, because its functional value is gone. In the model above, a new tier raises the bar for "wanting one": `N` for the old item drops toward the number of new or catching-up players. Coverage `S / N` shoots up, and by the price formula the price collapses.

Obsolescence is powerful because it resets every player's demand at once. It is also blunt. It wipes the value of everything players earned in the old tier, which many experience as their work being erased. Games that rely on it usually soften the blow with ways to turn old items into something useful. Examples are salvaging them into materials (a transformation back into week 7's chain), trading them in for currency toward the new tier, or cosmetic systems that keep an item's look after its stats are gone.

Compare obsolescence with `d > 0`:

| Property | Destruction (`d > 0`) | Obsolescence (new tier) |
|---|---|---|
| What leaves | the item copy | the item's value |
| Timing | continuous, a little every day | in steps, at each release |
| Crafter demand | steady | spikes after each release |
| Player feeling | loss of a thing | loss of progress |
| Design cost | tune one rate | ship new content on schedule |

Many games use both. Consumables and some gear decay continuously, and tiers reset the top of the market periodically.

## 5. Designing a decay package

Put the pieces together when you design an item category:

1. **Decide the item's role.** Consumable, gear, cosmetic, trade good? Consumables need no extra sink. Cosmetics usually should not decay, since their social value (week 2) depends on persistence.
2. **Pick a coverage target.** What share of the players who want it should own one at a time? Lower coverage means steadier crafter demand and higher prices.
3. **Estimate `F` and `N`.** Use your drop tables and crafting volumes from week 7.
4. **Derive `d`.** `d = F / (c × N)`. Then translate `d` into a player-facing rule. A 2% daily rate might be "each death has a 10% chance to destroy one equipped item", tuned with telemetry to deaths per day.
5. **Choose repair or replacement.** If `d` must be low for player-comfort reasons, add a repair sink to handle gold separately. Keep the two jobs apart in your spec so you can tune them separately.

## In-class activity (25 minutes)

In pairs, design the durability rule for a mid-level shield in a small MMO with 4,000 players who want one. Players create 60 shields per day.

1. Choose a coverage target and derive `d`. What is a shield's mean lifetime?
2. Turn `d` into a player-facing rule tied to deaths. Assume the average player dies 3 times per day. What per-death destruction chance gives your `d`? (Hint: ignore players who don't carry the shield, and treat each death as independent.)
3. Add a repair cost for the gold side. Pick a full repair price and compute the gold sink per player per day.
4. Swap with another pair and name the players who will hate their rule most.

Expected output: `d`, lifetime, the per-death chance, the repair sink, and the complaint your partners predicted.

## Common misconceptions

- **"Durability is an item sink."** Only if zero durability destroys the item. In WoW, Barrows and Diablo II, zero means repair, and the sink is gold.
- **"Destruction makes items scarce and players poorer."** Destruction makes item stock level off. Players who craft or farm those items gain customers. Whether the average player is poorer depends on the price level you choose.
- **"A higher creation rate means more players own the item forever."** With `d > 0`, higher `F` raises the steady stock in proportion, but the stock still levels off. With `d = 0`, higher `F` only makes saturation happen sooner.
- **"Repair costs fix inflation."** Repair is a flow sink. It slows money growth but cannot put a ceiling on it (week 3).

## Check yourself

1. A rare mount is created at 5 per day and destroyed at 0.1% per day. What is its steady-state stock? What is a copy's mean lifetime? About how many days until the stock is halfway to steady state?
2. Using the price rule `P ≈ P_max × (1 − S / N)` with `P_max = 2,000` and `N = 8,000`, what is the long-run price of an item with `F = 40` per day and `d = 1%`?
3. A player at Smithing 60 repairs a fully degraded Barrows set on an armour stand. What does it cost, and what is the sink per hour of combat?
4. A designer wants a crafted helmet owned by 40% of the 25,000 players who want one. Players create 250 per day. What `d` should the designer choose? If the average player dies 4 times per day, what per-death chance of destroying the helmet gives about that `d`?

<details>
<summary>Answers</summary>

1. `S* = 5 / 0.001 = 5,000`. Mean lifetime `1 / 0.001 = 1,000` days. Halfway after about `0.69 / 0.001 ≈ 693` days, nearly two years.
2. `S* = 40 / 0.01 = 4,000`, so `S / N = 0.5` and `P ≈ 2,000 × 0.5 = 1,000`.
3. `330,000 × (1 − 60/200) = 330,000 × 0.7 = 231,000` coins. Per hour: `231,000 / 15 = 15,400`.
4. `d = 250 / (0.4 × 25,000) = 0.025`, or 2.5% per day. With 4 deaths per day and per-death chance `x`, the daily survival is `(1 − x)^4 = 0.975`, so `x = 1 − 0.975^(1/4) ≈ 0.0063`, about 0.63% per death. The quick estimate `0.025 / 4 = 0.00625` is almost the same, because `x` is small.

</details>

## Lab / assignment hook

[Lab 08, item lifecycle simulation](../labs/lab08.md). You simulate the stock and price of three item types for one year in a spreadsheet, then design a decay package that holds each at a target coverage, and compute the gold its repair rules remove. It feeds the models assignment (30%).

## Sources

- Warcraft Wiki, "Durability" (current game, patch 12.0.7 era, accessed September 2026). 10% durability loss on death for equipped items, an extra 25% on equipped and bagged items when resurrecting at a spirit healer; items at zero durability give no stats and broken weapons cannot be used, but items are not destroyed.
- CCP Games, *Monthly Economic Report, August 2026* (eveonline.com, published 9 September 2026). The largest battle of August, in Pochven, destroyed about 9,000 ships; the report charts mining, production and destruction history together.
- EVE University Wiki, "Insurance" (current game). Insurance pays a share of CCP's estimated hull value, below market value, and covers only the hull, not fitted modules, rigs or cargo.
- Old School RuneScape Wiki, "Barrows equipment" (current game, accessed September 2026). 15 hours of combat lifespan; unequippable at zero until repaired; a fully degraded set costs 330,000 coins at non-player repairers; armour stand cost `NPC price × (1 − Smithing level / 200)`, 166,650 at level 99.
- Warcraft Wiki, "Soulbound" (current game). Bind on pickup and bind on equip; soulbound items cannot be traded, mailed or sold on the auction house.
- Blizzard Entertainment, *The Arreat Summit*, "Rings and Amulets" (Diablo II: Lord of Destruction). Rings and amulets are not subject to wear and never need repair.
- Lehdonvirta, V. & Castronova, E. (2014). *Virtual Economies: Design and Analysis*. MIT Press.

## Interactive spec: examples/w08-item-stock-decay.html

**The one insight:** without destruction, an item's stock grows past the number of players who want it and its price collapses to the floor forever; any positive destruction rate makes the stock level off at `F / d`, which holds the price up and keeps crafters' demand recurring.

**Layout:** two stacked charts sharing one time axis (days 0-365), stock on top, price below. Controls in a panel beside them on desktop, above them on mobile. Exact numbers in a readout row.

**Controls:**
- `F`, copies created per day: slider 0-500, step 10, default 100.
- `d`, destruction rate per day: slider 0-10%, step 0.1%, default 0.
- `N`, players who want one: slider 1,000-50,000, step 1,000, default 10,000.
- `P_max`: slider 100-5,000, step 100, default 1,000.
- Floor: slider 0-500, step 10, default 50.
- Toggle "Show d = 0 ghost" (default on).
- Preset buttons: "No destruction (WoW-style gear)" sets `d = 0`; "EVE-style" sets `d = 2%`; "Target 50% coverage" computes `d = F / (0.5 × N)` from current `F` and `N`.

**Formulas (discrete days, `S(0) = 0`):**
- `S(t + 1) = S(t) + F − d × S(t)`. Equivalent closed form for `d > 0`: `S(t) = (F/d) × (1 − (1 − d)^t)`; for `d = 0`: `S(t) = F × t`.
- `P(t) = max(floor, P_max × (1 − S(t) / N))`.
- Readouts: `S* = F / d` (or "no limit"), mean lifetime `1/d`, coverage `S*/N`, days to half `ln 0.5 / ln(1 − d)`, stock and price on day 365, and the first day `S ≥ N` if any.

**Visuals:**
- Top chart: `S(t)` solid line; dashed horizontal line at `N` labelled "everyone who wants one has one"; dotted horizontal line at `S*` when finite; ghost line for `d = 0` in a muted colour.
- Bottom chart: `P(t)` solid line; dashed line at the floor; ghost price line for `d = 0`. Shade the region where price sits on the floor.

**Test values (defaults `F = 100`, `N = 10,000`, `P_max = 1,000`, floor 50):**
- `d = 0`: `S(100) = 10,000`; price reaches the floor on day 95 (`1,000 × (1 − 9,500/10,000) = 50`) and stays there; `S(365) = 36,500`.
- `d = 1%`: `S* = 10,000`, lifetime 100 days, half at 69.0 days, `S(100) ≈ 6,340`, `S(365) ≈ 9,745`, `P(365) ≈ 50` (floor, since `1,000 × 0.0255 = 25.5 < 50`); price first reaches the floor on day 299.
- `d = 0.5%`: price first reaches the floor on day 129.
- `d = 2%`: `S* = 5,000`, lifetime 50, half at 34.3 days, `S(365) ≈ 4,997`, `P(365) ≈ 500`.
- `d = 5%`: `S* = 2,000`, half at 13.5 days, `P(365) ≈ 800`.
- "Target 50% coverage" preset with defaults sets `d = 2.0%`.

**Accessibility:** sliders labelled with current values and keyboard steps; a live text line states "Stock levels off at S* (coverage X%)" or "No limit: stock passes N on day T". No game art.
