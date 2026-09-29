# MMO307 · Week 04 — Gear Treadmills and Item Level

**Why this matters:** On the day a new season starts, most of your players' gear stops mattering. How much of it stops, and how much a player's old best item is still worth, is decided by a few item-level numbers and one budget curve. You can compute all of it before you ship, and players will feel every digit.

**You will be able to:**
- Compute where an item from one season lands on the next season's ladder, and how many seasons it survives, from the ladder's width W and the creep per season c.
- Compare linear and exponential item budgets, and compute what an item-level gap is worth in power under each.
- Design a season ladder (width, track spacing, overlap, budget growth) that meets targets for carry-over, felt upgrade size and the widest gap that can share content.
- Critique a shipped treadmill by rewriting its published item-level tables in the ladder model.

**Before class:** Schreiber & Romero, *Game Balance* (2021), the chapter "Progression in PvE Games". Warcraft Wiki, "Midnight Season 1" and "Midnight Season 2", the "Item upgrade tracks" tables only (10 minutes).

**Prerequisites from earlier courses:** [GD203 week 9, item budgets and stat weights](../../GD203-combat-and-progression-design/lectures/w09-item-budgets-and-stat-weights.md) (an item level labels a stat budget `B(ilvl)`). [GD203 week 8, power curves](../../GD203-combat-and-progression-design/lectures/w08-power-curves-and-level-scaling.md) (linear against exponential growth, and power ratios). [GD203 week 14, horizontal vs vertical progression](../../GD203-combat-and-progression-design/lectures/w14-horizontal-vs-vertical-progression.md) (the sharing band `F`). This course's [week 1](w01-the-endgame-problem.md) (the chase inside one tier) and [week 2](w02-vertical-progression-and-power-creep.md) (the ratchet that sets creep per tier `c`, and power per item level `1 + g`).

**Interactive:** [`examples/w04-season-ladder.html`](../examples/w04-season-ladder.html). Keep it open during section 2.

---

## 1. The seam between tiers

Week 1 looked inside one tier. A player fills slots with drops, tokens or a weekly choice, and the chase ends when the set is complete. Week 2 looked across many tiers and showed that the ratchet rule forces the item-level top to creep by `c = o × s + u` levels per tier.

This week sits on the seam between two tiers. A **gear treadmill** is the loop that runs there. A new tier (a raid, a dungeon season, a patch) arrives with better gear. Its easiest items are about as good as the old tier's middle items. Players who finished the old chase start a new one, and most of their old gear stops mattering. Week 2 told you how fast the ladder moves. This week asks what that movement does to the items players already own, and what an item-level gap is actually worth.

Two terms need pinning down.

- **Item level (ilvl).** Every World of Warcraft item has one. It labels the item's stat budget, as GD203 week 9 showed. Warcraft Wiki notes that the game shows each character's average item level on the character sheet and uses item level to gate queues for dungeons and raids.
- **Ladder.** The range of item levels a season hands out, from its **entry** to its **top**. Modern WoW builds each season's ladder from **upgrade tracks**, overlapping bands that items climb by spending an upgrade currency. Week 2's rungs are the tracks' starting points.

## 2. Worked example: last season's best is this season's Veteran 4

### The hook

In Midnight Season 1 (17 March to 11 August 2026), the best gear a World of Warcraft player could own was Myth track rank 6, at item level 289. Season 2 opened on 18 August 2026. Its lowest track, Adventurer, starts at 266, and its Myth track starts at 318.

Look up 289 in the Season 2 table and you find Veteran 4. The best item of the old season sits on the second-lowest track of the new one, the track whose crests came from Raid Finder and Heroic dungeons in Season 1.

It was not a one-off. In The War Within, Season 2's Myth 6 was item level 678. Season 3 opened with Veteran 4 at exactly 678.

Two seams, the same landing spot. That is not a coincidence. It falls out of two numbers.

### The model

Describe each season's ladder by two numbers.

- `W`, the **width** of the ladder: top minus entry, in item levels.
- `c`, the **creep** per season: how far the entry and the top move up from one season to the next. This is week 2's `c`, now read off real tables instead of derived from rungs.

Season `k` runs from entry `E_k` to top `E_k + W`, and `E_(k+1) = E_k + c`.

**Where an old item lands.** An item at item level `i` from season `k`, seen from season `k + n`, sits at a fraction of the new ladder:

```
x_n = (i − E_k − n × c) / W
```

`x = 0` is the new entry and `x = 1` is the new top. Below zero, the item is worse than anything the new season hands out.

**How long an item survives.** It stays at or above the entry while `x_n ≥ 0`, so the number of later seasons it survives is

```
n_max = floor((i − E_k) / c)
```

For the old top, `i − E_k = W`. The best item of a season lands at `x_1 = 1 − c / W` and survives `floor(W / c)` seasons. Call `W / c` the **carry-over ratio**. It is the single number that decides how much of a season's effort carries into the next.

**What a gap is worth.** Week 2 assumed each item level multiplies power by `1 + g`. Under that assumption, two items `d` levels apart differ in power by `(1 + g)^d`. Three gaps matter at the seam.

```
patch-day gap     (1 + g)^(W − c)    old top against the new entry
season growth     (1 + g)^c          new top against the old top
in-season spread  (1 + g)^W          top against entry, same season
```

Section 3 tests the `1 + g` assumption against real budget formulas. For now, keep it.

Every symbol, once more: `E_k` entry of season `k`, `W` width, `c` creep per season, `i` an item's level, `x_n` its position `n` seasons later, `n_max` seasons survived, `g` power per item level.

### Numbers you can check

Midnight's two seasons, from the Warcraft Wiki tables, have `E_1 = 220` (Adventurer 1) and a top of 289 (Myth 6), so `W = 69`. Season 2 starts at 266, so `c = 46`. The carry-over ratio is `69 / 46 = 1.5`.

Take the top rank of each Season 1 track and find where it lands in Season 2.

| Season 1 item | ilvl i | Position in Season 2, x_1 = (i − 266) / 69 | Season 2 rank at that ilvl | Seasons survived, floor((i − 220) / 46) |
|---|---|---|---|---|
| Adventurer 6 | 237 | −0.42 | below the ladder | 0 |
| Veteran 6 | 250 | −0.23 | below the ladder | 0 |
| Champion 6 | 263 | −0.04 | below the ladder | 0 |
| Hero 6 | 276 | 0.14 | Adventurer 4 | 1 |
| Myth 6 | 289 | 0.33 | Veteran 4 | 1 |

Only the two highest tracks survive the seam, each for exactly one season. Two thirds of the old ladder's width, everything below 266, is under the new entry on patch day. And because `c / W = 2/3`, the old top always lands a third of the way up the new ladder. Veteran 4 is simply the rank that sits there.

Check the War Within pair the same way. Season 2 ran from 610 (Adventurer 1) to 678 (Myth 6), so `W = 68`. Season 3 started at 655, so `c = 45`. The old top lands at `(678 − 655) / 68 = 0.34`, which is Veteran 4 again. Two expansions, nearly the same `W` and `c`, so the same landing spot.

Now the gaps, with week 2's `g = 1%` per item level.

| Gap | Formula | Value |
|---|---|---|
| Patch day, old top vs new entry | `1.01^(69 − 46) = 1.01^23` | 1.26 |
| Season growth, new top vs old top | `1.01^46` | 1.58 |
| In-season spread, top vs entry | `1.01^69` | 1.99 |
| One upgrade rank (about 3.4 ilvl) | `1.01^3.4` | 1.034 |

Read the third row against GD203 week 14. There, `F = 2` was about the widest power gap one encounter can serve. A 69-level ladder at 1% per level is a spread of 1.99. At this `g`, a single season's ladder is exactly as wide as a shared encounter can stretch.

You can reproduce the landing table and the gaps with a few lines of Python.

```python
import math

E1, W, c, g = 220, 69, 46, 0.01
for name, i in [("Champion 6", 263), ("Hero 6", 276), ("Myth 6", 289)]:
    x = (i - (E1 + c)) / W
    n_max = math.floor((i - E1) / c)
    print(f"{name}: x_1 = {x:.2f}, survives {n_max} season(s)")
print(f"patch day {(1 + g) ** (W - c):.2f}, growth {(1 + g) ** c:.2f}, spread {(1 + g) ** W:.2f}")
```

It prints:

```
Champion 6: x_1 = -0.04, survives 0 season(s)
Hero 6: x_1 = 0.14, survives 1 season(s)
Myth 6: x_1 = 0.33, survives 1 season(s)
patch day 1.26, growth 1.58, spread 1.99
```

### A visual you can move

Open the interactive. The left panel draws three consecutive seasons as horizontal ladders on an item-level axis, stacked one above another, with the five tracks shaded inside each. A marker shows an item you pick (default Season 1 Myth 6), and a dotted line drops from it through the later seasons. In item levels the creep looks modest. Each ladder is offset by 46 levels, about 16% of 289, and the old top still sits comfortably inside the next ladder.

The right panel draws the same ladders on a power axis, `(1 + g)^(i − E_1)`, on a linear scale. Now each season's ladder is wider than the last and sits further right, because a constant item-level step is a constant power ratio. The dotted line shows how far your item falls behind. On patch day it is worth 1.26 new entries, and the new top is worth 1.58 of it.

Drag `c` up to 69, equal to `W`. The old top lands exactly on the new entry, and the carry-over ratio is 1. Drag it down to 23 and the old top lands two thirds of the way up and survives three seasons. Then switch the budget to "linear" and watch the right panel's ladders stop widening. Section 3 explains why.

### Cross-game recognition

**World of Warcraft (The War Within Season 2 to 3, 2025; Midnight Season 1 to 2, 2026).** Both seams used `c` near 45 and `W` near 68, a carry-over ratio of 1.5, and both put the old top at Veteran 4. Inside a season the tracks repeat the pattern at a smaller scale. In Midnight Season 1, five tracks each span 17 item levels (six ranks 3 or 4 levels apart) and start 13 apart, so neighbouring tracks share two ranks. A Veteran 6 item (250) is already Champion 2. Gear from easier content is not wasted the moment a player moves up a difficulty. That is the same `x` logic applied between tracks instead of seasons.

**Final Fantasy XIV (Dawntrail, patches 7.05 to 7.4, 2024 to 2025).** The game's tomestone gear moves in fixed steps. The wiki's tomestone history lists item level 720 to 730 gear from patch 7.05, 750 to 760 from patch 7.2 and 780 to 790 from patch 7.4. So each rotation has `c = 30` and each set spans about `W = 10`. The carry-over ratio is `10 / 30 ≈ 0.33`. An old tomestone set lands at `x = 1 − 3 = −2` on the next set's ladder, far below the entry, on the day it arrives. Tomestone gear never carries over. The same page records that when a new capped tomestone arrives, the old one loses its weekly cap, so the old rung becomes cheap to reach. Week 6 returns to that as a catch-up rule.

**Guild Wars 2 (level 80 endgame since 2012).** GD203 week 14 showed that the top stat tier, ascended, is 5% above exotic gear and has not moved since it arrived in 2012. In ladder terms `c = 0` after one early step. The carry-over ratio is infinite, every item keeps its value forever, and there is no treadmill. What the game gives up is the new-tier jolt that WoW's 1.58 per season buys.

Three games, three positions on the same dial. For any treadmill, read two consecutive tables, compute `W`, `c` and `W / c`, and you know how much of a player's effort survives the seam.

### Eyes-open design judgment

The carry-over ratio is a choice, and each end of the dial has a cost.

- **Low carry-over (`W / c ≤ 1`)** gives everyone a clean start. A player returning from a break is as well equipped as a veteran on patch day, which helps returning players and keeps the community together. The cost is that a season's effort buys nothing next season. Expect committed players to ease off late in each season, because nothing they earn will last.
- **High carry-over (`W / c ≥ 2`)** rewards finishing a season, because the top items stay useful for two or more seasons. The cost is a patch-day gap between veterans and everyone else, `(1 + g)^(W − c)`, at the start of every season.
- **A wide ladder** gives more to chase and more room for difficulty tracks. It also widens the in-season spread `(1 + g)^W`. Past `W = ln F / ln(1 + g)`, the top and bottom of your own season can no longer share an encounter.
- **The rank step sets how an upgrade feels.** At 1% per level, a 3.4-level rank is worth 3.4%. Players need the tooltip to notice that. A bigger step is felt, and it eats ladder width faster.

Choose `W / c` for the behavior you want on patch day, and check the spread against your widest shared encounter. Do not let the numbers come out of whatever the last season used.

## 3. What is an item level worth? Linear and exponential budgets

Week 2 converted item levels to power with a constant `1 + g` per level. That is an **exponential budget**: `B(i) = B_0 × (1 + g)^i`. Every gap of `d` levels is the same ratio wherever it sits on the scale. It is the assumption behind every table above.

It is not the only choice, and World of Warcraft has not always made it. Warcraft Wiki's "Stat budget" page records community-derived formulas for Burning Crusade items (2007 era) in which weapon damage and armor are straight lines in item level. For epic one-handed weapons above item level 138, the formula is

```
DPS = 0.6 × ilvl + 15.5
```

That is a **linear budget**: `B(i) = a × i + b`. Under a linear budget, the value of one more item level, as a fraction of what you already have, shrinks as item level grows:

```
g_eff(i) = a / (a × i + b)
```

| Item level | DPS = 0.6 × ilvl + 15.5 | Gain from +13 ilvl | Effective g per level |
|---|---|---|---|
| 146 | 103.1 | +7.6% | 0.58% |
| 159 | 110.9 | +7.0% | 0.54% |
| 200 | 135.5 | +5.8% | 0.44% |
| 300 | 195.5 | +4.0% | 0.31% |

The same 13-level step is a 7.6% upgrade at 146 and a 4.0% upgrade at 300. A linear budget makes creep **self-limiting** in power. Week 2's additive creep of `c` levels per tier gives shrinking power ratios, and the in-season spread `B(E + W) / B(E)` shrinks as the game goes on. The cost is that upgrades feel smaller every tier, so the designer must raise `c` just to keep the upgrade margin `u` felt. That is the ratchet running faster to stand still.

The exponential budget does the opposite. Every step feels the same forever, and power ratios stay put, but raw numbers grow without limit. Warcraft Wiki's history of the first stat squish says that when patch 6.0.2 (October 2014) squished the game, items from level 60 through Mists of Pandaria dungeon gear were moved from an exponential scale to a linear one. In other words, the game had been running an exponential budget, and the fix for its numbers included switching the oldest part of the curve to linear. Next week is about that fix.

| Budget | Formula | A fixed item-level gap is | Numbers over time | Upgrade feel over time |
|---|---|---|---|---|
| Exponential | `B_0 (1 + g)^i` | a fixed ratio | grow without limit | constant |
| Linear | `a i + b` | a shrinking ratio | grow slowly | fades |

Neither is correct. Choose deliberately, and write `g` or `a` and `b` in your design document next to week 2's `c`.

## 4. Designing a ladder backwards

Most teams start from targets. The model inverts cleanly, with the exponential budget.

**From a carry-over target.** If the old top should land a fraction `x` of the way up the new ladder, then `c = (1 − x) × W`. For `x = 1/3` and `W = 69`, `c = 46`. That is Midnight's pair exactly.

**From a sharing target.** If the top and entry of one season must still share content within a band `F`, then `W ≤ ln F / ln(1 + g)`. With `F = 2` and `g = 1%`, `W ≤ 69.7`.

**From a patch-day gap target.** If a veteran should start the new season no more than a factor `P` ahead of a newcomer, then `W − c ≤ ln P / ln(1 + g)`. With `P = 1.2`, `W − c ≤ 18.3`.

Week 2's section 5 adds the shelf-life target, `t* = ln F / (c × ln(1 + g))`. Put all four together and they conflict. Faster growth needs a bigger `c`. Carry-over needs `W` large relative to `c`. The sharing band caps `W`. And the patch-day target caps `W − c`. You cannot have fast growth, high carry-over, a narrow in-season spread and a small patch-day gap at once. Midnight's numbers pick growth of 1.58 per season and a carry-over of one third, and they sit right at the sharing edge. Its patch-day gap of 1.26 is the price.

| Target | Constraint | Example (g = 1%) |
|---|---|---|
| Old top lands at `x` | `c = (1 − x) W` | `x = 1/3, W = 69` gives `c = 46` |
| Sharing band `F` | `W ≤ ln F / ln(1 + g)` | `F = 2` gives `W ≤ 69.7` |
| Patch-day gap `P` | `W − c ≤ ln P / ln(1 + g)` | `P = 1.2` gives `W − c ≤ 18.3` |
| Shelf life (week 2) | `c ≤ ln F / (t* ln(1 + g))` | `t* = 3, F = 2` gives `c ≤ 23.2` |

## 5. Tracks, difficulty and what the average hides

A season's ladder is split into bands that different content feeds. In Midnight Season 1, the Warcraft Wiki lists Adventurer from 220 to 237, Veteran 233 to 250, Champion 246 to 263, Hero 259 to 276 and Myth 272 to 289. Items climb ranks by spending crests, 20 per upgrade, with one crest type per track. The crest sources line up with difficulty. Veteran crests came from Raid Finder and Heroic dungeons, Champion from Normal raids and low Mythic+ keys, Hero from Heroic raids and mid keys, and Myth from Mythic raids and high keys.

This makes the in-season spread a spread by difficulty. A Myth-track player and an Adventurer-track player in the same season can be `1.01^69 ≈ 2` apart in power. Your group finder, open-world tuning and PvP brackets have to absorb that gap, and it is set by how many tracks you stack, not by how hard any single boss is.

Players and group finders read the **average** item level, so it drives behavior even where it misleads.

- **A gate on the average is a gate on a sum.** A player can pass it with one very high slot and one very low one. Fine for a dungeon queue, less fine for a tuned raid where the weapon slot carries a large share of the budget.
- **Averages mix seasons.** On patch day a veteran's average blends 289-level old items, each worth 1.26 new entries, with fresh drops. The average is a fair summary only when every slot uses the same budget curve, which is what GD203 week 9's budget rule is for.
- **The average moves in item levels, not power.** Going from 266 to 276 and from 324 to 334 are both +10 on the character sheet and, under an exponential budget, the same 10.5% ratio. In raw stats the second step is `1.01^58 ≈ 1.78` times larger. Players compare ratios by feel and raw numbers by tooltip, and the tooltip is the one that grows without limit.

## In-class activity (25 minutes)

In groups of three, design the next two seasons of a fictional MMO's ladder. Use `g = 0.8%` per item level.

1. Your producer wants the old season's best gear to land halfway up the new ladder (`x = 0.5`) and each season's top to grow by about 40% (`(1 + g)^c = 1.4`). Compute `c`, then `W`.
2. Check the sharing constraint with `F = 2` and the patch-day gap with `P = 1.2`. Which targets fail? Relax one and justify it in two sentences.
3. Split your final ladder into tracks with a two-rank overlap and six ranks each. List each track's range.
4. Swap ladders with another group. For their design compute `x_1`, `n_max` for their top item and their patch-day gap. Name one kind of player their design treats badly.

Expected output: `c`, `W`, a track table and a one-paragraph critique of the other group's ladder.

## Common misconceptions

- **"The creep is only 46 levels out of 289, so old gear loses 16%."** Item levels are labels on a budget curve. The loss is `(1 + g)^46` in budget, and three of the five old tracks fall below the new entry on patch day.
- **"Equal item-level gaps are equal upgrades."** Under an exponential budget they are equal ratios but growing amounts. Under a linear budget they are equal amounts but shrinking ratios. Neither makes them equal in both senses.
- **"A wide ladder gives more to chase, so wider is better."** Width is also the in-season spread. Past `ln F / ln(1 + g)` your own season can no longer share an encounter.
- **"Carry-over and fresh starts can both be maximized."** The old top lands at `x = 1 − c / W`. Raising carry-over means less creep or a wider ladder, and each has a cost.

## Check yourself

1. A season's ladder runs from 400 to 460 and the next season starts at 440. Where does the old top land on the new ladder, and how many seasons does it survive?
2. With `g = 1.2%`, what is the season growth for `c = 30`? What is the in-season spread for `W = 60`?
3. You want the old top to land exactly at the new entry, with `W = 50`. What creep does that need, and what is the carry-over ratio?
4. Under the Burning Crusade epic weapon formula, what is the DPS at item level 250, and what percentage does a +13 step from there add? Compare it with the exponential budget at `g = 0.5%`.
5. A game uses `g = 1%`, `W = 69` and wants a patch-day gap of at most 1.15. What is the smallest `c` it can use, and where does the old top then land?

<details>
<summary>Answers</summary>

1. `W = 60`, `c = 40`. The old top (460) sits at `(460 − 440) / 60 = 0.33` of the new ladder. It survives `floor(60 / 40) = 1` season.
2. Growth `1.012^30 ≈ 1.43`. Spread `1.012^60 ≈ 2.04`, just over an `F = 2` band.
3. Landing at the entry means `x = 0`, so `c = W = 50`. The carry-over ratio is 1.
4. `0.6 × 250 + 15.5 = 165.5`. At 263 it is `173.3`, a gain of `7.8 / 165.5 ≈ 4.7%`. At `g = 0.5%`, a 13-level step is `1.005^13 ≈ 6.7%` everywhere on the scale.
5. `W − c ≤ ln 1.15 / ln 1.01 = 0.1398 / 0.00995 ≈ 14.0`, so `c ≥ 55`. The old top then lands at `x = 1 − 55 / 69 ≈ 0.20`.

</details>

## Lab / assignment hook

[Lab 04, the season ladder](../labs/lab04.md). You load the Midnight and War Within track tables, write functions for landing position, survival and gaps under both budget shapes, test them against this lecture's numbers, then design a three-season ladder that meets targets you choose. The results feed the progression analysis assignment (30%).

## Sources

- Warcraft Wiki, "Item level" (World of Warcraft, retail, accessed September 2026). Item level as a budget indicator; average item level on the character sheet; item level used to gate queues. https://warcraft.wiki.gg/wiki/Item_level
- Warcraft Wiki, "Midnight Season 1" (accessed September 2026). Dates 17 March to 11 August 2026; tracks Adventurer 220 to 237, Veteran 233 to 250, Champion 246 to 263, Hero 259 to 276, Myth 272 to 289, six ranks each; 20 crests per upgrade; crest sources by difficulty. https://warcraft.wiki.gg/wiki/Midnight_Season_1
- Warcraft Wiki, "Midnight Season 2" (accessed September 2026). Start date 18 August 2026; tracks from Adventurer 1 (266) to Myth 6 (334); item level 289 is Veteran 4. https://warcraft.wiki.gg/wiki/Midnight_Season_2
- Warcraft Wiki, "The War Within Season 2" and "Valorstones" (Season 3 track table, accessed September 2026). Season 2 tracks from Adventurer 1 (610) to Myth 6 (678); Season 3 from Adventurer 1 (655) to Myth 6 (723), with 678 at Veteran 4. https://warcraft.wiki.gg/wiki/Valorstones
- Warcraft Wiki, "Stat budget" (flagged by the wiki as outdated; Burning Crusade era). Community-derived weapon DPS formulas, epic one-handed `0.6 × ilvl + 15.5` above item level 138. https://warcraft.wiki.gg/wiki/Stat_budget
- Warcraft Wiki, "Stat squish", section "The original squish" (patch 6.0.2, 14 October 2014). Items from level 60 through Mists of Pandaria dungeon gear moved from an exponential to a linear scale. https://warcraft.wiki.gg/wiki/Stat_squish
- Final Fantasy XIV Online Wiki (consolegameswiki), "Allagan Tomestone" (Dawntrail, accessed September 2026). Tomestone gear at item level 720 to 730 (patch 7.05), 750 to 760 (7.2) and 780 to 790 (7.4); previous tomestone uncapped when a new one arrives. https://ffxiv.consolegameswiki.com/wiki/Allagan_Tomestone
- Guild Wars 2 ascended equipment at 5% above exotic, introduced November 2012: as cited in GD203 week 14 (Guild Wars 2 Wiki, "Ascended equipment").
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press.

## Interactive spec: examples/w04-season-ladder.html

**Insight the visual must make obvious:** a constant item-level creep looks like a small, steady offset on the item-level axis, but under an exponential budget each season's ladder is wider and further right on the power axis, and the old top always lands at the same fraction `1 − c/W` of the new ladder (a third of the way up at Midnight's numbers).

**Layout.** Two linked panels, side by side on desktop, stacked on mobile (item-level panel first).

- **Left panel, "Item level".** Three horizontal bars stacked vertically, one per season `k = 1, 2, 3`. Bar `k` spans `[E_1 + (k − 1)c, E_1 + (k − 1)c + W]` on a shared item-level axis. Inside each bar, shade five tracks at the Midnight offsets scaled to `W`: track `j` (j = 0..4) starts at `E_k + j × W × 13/69` and is `W × 17/69` wide, so the default reproduces 220-237, 233-250, 246-263, 259-276, 272-289. Label the tracks A, V, C, H, M. A marker at the chosen item `i` on season 1's bar, with a dotted vertical line down through seasons 2 and 3. Beside seasons 2 and 3, print `x_n = (i − E_1 − n c) / W` to two decimals, or "below ladder" when negative.
- **Right panel, "Power relative to season 1 entry".** The same three bars on a horizontal axis of `B(i)/B(E_1)`, linear scale, with a toggle for log scale. Budget shape toggle: "exponential" uses `(1 + g)^(i − E_1)`; "linear" uses `(a i + b)/(a E_1 + b)` with `a = 0.6`, `b = 15.5`. Same marker and dotted line. Under the panel print patch-day gap `B(E_1 + W)/B(E_1 + c)`, season growth `B(E_1 + W + c)/B(E_1 + W)` and in-season spread `B(E_1 + W)/B(E_1)`, each to two decimals.

**Controls (keyboard accessible, values shown).**
- Creep `c`: slider 0 to 100, step 1, default 46.
- Width `W`: slider 10 to 120, step 1, default 69.
- `g`: slider 0.000 to 0.030, step 0.001, default 0.010 (disabled when the budget is linear).
- Budget shape: exponential (default) or linear.
- Item: a select of the five season 1 track tops at the scaled positions (defaults 237, 250, 263, 276, 289) plus "custom" with a number input. Default Myth 6.
- `E_1`: number input, default 220.
- Presets: "Midnight S1 to S2" (`E_1 = 220, W = 69, c = 46`), "War Within S2 to S3" (`E_1 = 610, W = 68, c = 45`), "FFXIV tomestone sets" (`E_1 = 720, W = 10, c = 30`), "No treadmill" (`c = 0`).

**Readouts** (copyable): `n_max = floor((i − E_1)/c)` ("never leaves" when `c = 0`), carry-over ratio `W/c`, and the largest sharable width `ln F / ln(1 + g)` with an `F` input (default 2).

**Exact test values.**
- Midnight preset, exponential, `g = 0.010`, Myth 6 (289): `x_1 = 0.33`, `x_2` below ladder (−0.33), `n_max = 1`; patch-day gap 1.26, growth 1.58, spread 1.99; `W/c = 1.50`; sharable width 69.7.
- Hero 6 (276): `x_1 = 0.14`, `n_max = 1`. Champion 6 (263): `x_1 = −0.04`, below ladder, `n_max = 0`.
- War Within preset, item 678: `x_1 = 0.34`, `n_max = 1`.
- `c = 69, W = 69`: Myth 6 `x_1 = 0.00`, `n_max = 1`, patch-day gap 1.00.
- `c = 23, W = 69`: Myth 6 `x_1 = 0.67`, `n_max = 3`.
- Linear budget, Midnight preset: spread `(0.6 × 289 + 15.5)/(0.6 × 220 + 15.5) = 188.9/147.5 = 1.28`; growth `(0.6 × 335 + 15.5)/(188.9) = 216.5/188.9 = 1.15`.

**First screen:** the Midnight preset with Myth 6 selected, so the student sees "Season 2: x = 0.33" on the left and the widening ladders on the right. Caption under both panels: "Every season adds the same 46 item levels. In power, every season multiplies by 1.58."
