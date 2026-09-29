# MMO307 · Week 02 — Vertical Progression and Power Creep

**Why this matters:** Every long-running MMO with gear tiers has the same chart. The top item level climbs expansion after expansion until someone has to squish it. Players blame designers for lacking discipline. The model in this lecture shows that most of the climb is forced by one reasonable rule, and it tells you which numbers set the speed.

**You will be able to:**
- Compute the power creep per tier and per expansion that a difficulty ladder and an upgrade rule force.
- Measure creep from a shipped game's item-level history, both as an additive step and as a growth ratio, and say which one the data fits.
- Convert creep in item levels into a power growth rate and a content shelf life.
- Critique a tier plan by predicting how each design knob (rungs, spacing, overlap, upgrade margin, tiers per expansion) changes creep.

**Before class:** Schreiber & Romero, *Game Balance* (2021), the chapter "Progression in PvE Games" (the sections on power curves and on long-term progression). Warcraft Wiki, "Stat squish" (15 minutes; read the History section and look at the item level table).

**Prerequisites from earlier courses:** [GD203 week 14, horizontal vs vertical progression](../../GD203-combat-and-progression-design/lectures/w14-horizontal-vs-vertical-progression.md) (the power gap `G = r^t` and shelf life `t* = ln F / ln r`, which we reuse without re-deriving). [GD203 week 8, power curves and level scaling](../../GD203-combat-and-progression-design/lectures/w08-power-curves-and-level-scaling.md) (why a squish leaves every ratio unchanged). [GD203 week 9, item budgets](../../GD203-combat-and-progression-design/lectures/w09-item-budgets-and-stat-weights.md). [Week 1 of this course](w01-the-endgame-problem.md) (the reset family of endgame goals).

**Interactive:** [`examples/w02-power-creep.html`](../examples/w02-power-creep.html). Keep it open during section 2.

---

## 1. Vertical progression after the cap

In week 1 you saw that every gear chase ends, and one family of answers is the **reset**. A new tier of content arrives with gear that beats the old gear, and the chase starts again. This is **vertical progression** at the endgame. Power goes up, tier after tier.

GD203 week 14 gave you the cost of this in one formula. If each tier multiplies power by `r`, two players `t` tiers apart have a power gap `r^t`, and content can serve them together only while that gap stays below a band `F`. The shelf life of a tier is `t* = ln F / ln r`. You will use that result today. What GD203 did not ask is where `r` comes from. It treated growth per tier as a number the designer picks. In practice designers feel they have very little choice, and the history of long-running games agrees with them.

**Power creep** is the name for this steady rise. More precisely, it is the growth over time in the power of the best rewards available, and so in the power that new content must be tuned against. Creep is not a bug. It is how vertical progression works. The design question is its rate.

### Item level, the label on the power

Most modern MMOs attach a single number to every item, the **item level** (ilvl). The Warcraft Wiki describes it as a rough indicator of an item's power, with two items of equal item level meant to be worth about the same. In GD203 week 9 terms, item level names the size of an item's stat budget.

Item level is a label, not power itself. How much power one item level buys depends on the game's budget formula, which week 4 examines. This lecture works in item levels first, because that is what games publish and what players see, and converts to power at the end.

## 2. Worked example: the power creep chart

### The hook

Here is the top of World of Warcraft's item-level range in each expansion, from the Warcraft Wiki's squish table. Each range runs from the first normal-difficulty raid of the expansion to the highest item level a player could reach in it.

| Expansion | Item level range (native scale) |
|---|---|
| World of Warcraft (Classic era) | 66-86 |
| The Burning Crusade | 120-159 |
| Wrath of the Lich King | 213-284 |
| Cataclysm | 359-416 |
| Mists of Pandaria | 496-580 |
| Warlords of Draenor | 670-735 |
| Legion | 835-1000 |

Then the chart breaks. Patch 8.0.1 (the Battle for Azeroth pre-patch, 2018) squished item levels so that Legion's 1000 became 265. Battle for Azeroth then ran from 340 to 485. Patch 9.0.1 (the Shadowlands pre-patch, 2020) squished again, so 485 became 140. Shadowlands, Dragonflight and The War Within then ran from 184 to 311, 376 to 528 and 623 to 730. Patch 12.0.0 (the Midnight pre-patch, January 2026) squished a third time, and 730 became 170.

Final Fantasy XIV tells a steadier story. Its official wiki lists the maximum item level at each level cap as 130, 270, 400, 530, 660 and 790, from A Realm Reborn to Dawntrail. After the first step, every expansion adds exactly 130.

Two games, two shapes, one direction. Neither studio set out to inflate numbers. Here is why both did.

### The model

A **tier** is one batch of endgame content with its own gear. Most modern raids are released on several difficulties at once, so a tier is really a ladder.

- `D` is the number of difficulty **rungs** in a tier (for example story, normal, heroic, mythic).
- `s` is the item-level **spacing** between neighbouring rungs.
- `L_t` is the item level of the lowest rung of tier `t`. The rungs of tier `t` sit at `L_t, L_t + s, ..., L_t + (D − 1)s`.
- `u` is the **upgrade margin**, the smallest item-level gain that a player will do content for. Below it a reward feels like a sidegrade.
- `o` is the **overlap rule**, the rung (counting from 0 at the bottom) whose players the next tier's lowest rung must upgrade. With `o = 0`, the new entry rung only has to beat the old entry rung. With `o = D − 1`, the new entry rung must beat the old top rung, so every player's gear is replaced.

The **ratchet rule** says the next tier's lowest rung must be at least `u` above rung `o` of the current tier:

```
L_(t+1) = L_t + o × s + u
```

So the creep per tier is

```
c = o × s + u
```

and an expansion with `T` tiers creeps by

```
C = T × c = T × (o × s + u)
```

Three things stand out. Creep is **additive** in item level, the same number of levels every tier. It does not depend on how high the numbers already are. And every term is a design choice that sounds harmless on its own. More difficulty rungs, a clear visible upgrade, and new gear that replaces old gear are all things players ask for.

**From item level to power.** Assume each item level multiplies a character's power by a fixed factor `1 + g`. (This is a modelling assumption, not a published figure; week 4 examines real budget curves.) Then creep of `c` item levels per tier is a power growth per tier of

```
r = (1 + g)^c
```

and GD203's shelf life becomes

```
t* = ln F / (c × ln(1 + g))
```

Linear growth in the label becomes exponential growth in power, and the overlap rule sets the shelf life.

### Numbers you can check

Take a four-rung ladder (`D = 4`) with spacing `s = 10` and upgrade margin `u = 5`. Three tiers per expansion (`T = 3`). For the power conversion use `g = 1%` per item level and GD203's band `F = 2`.

| Overlap rule `o` | Meaning | Creep per tier `c` | Per expansion `C` | Power per tier `r = 1.01^c` | Shelf life `t*` (tiers) |
|---|---|---|---|---|---|
| 0 | new entry beats old entry | 5 | 15 | 1.051 | 13.93 |
| 1 | new entry beats old second rung | 15 | 45 | 1.161 | 4.64 |
| 2 | new entry beats old third rung | 25 | 75 | 1.282 | 2.79 |
| 3 | new entry beats old top rung | 35 | 105 | 1.417 | 1.99 |

Moving from `o = 0` to `o = 3` multiplies creep by 7 and cuts shelf life from about 14 tiers to 2. The spacing and the margin barely matter by comparison. The overlap rule is the big knob, and it is the one designers rarely write down.

Now add a fifth rung to the same ladder and keep the "replace everyone's gear" rule, which becomes `o = 4`. Creep per tier rises from 35 to 45. If the expansion also gains a fourth tier, `C` rises from 105 to 180. That is the kind of jump the WoW chart shows, as you'll see in the cross-game section.

### A visual you can move

Open the interactive. The first tab, "The chart," plots the WoW table above against time, on the native scale. It is a sawtooth, climbing through seven expansions to 1000, dropping to 265, climbing again, dropping to 140, climbing to 730, dropping to 170. A toggle switches to a log axis, and a second toggle overlays Final Fantasy XIV's straight line.

On the native scale the WoW climb looks like it accelerates, and the squishes look like the fix. Now press "Increments." The chart becomes bars, one per expansion, showing how many item levels each expansion added on the scale in use at the time. After each squish the bars do not shrink. Battle for Azeroth added 220 levels after the first squish, and the three expansions after the second squish added 171, 217 and 202. The squish reset the label. It did not touch the ratchet.

The second tab, "The ratchet," draws the ladder model. Each tier is a column of `D` rungs. Drag `o` from 0 to `D − 1` and watch the columns pull apart. The readout shows `c`, `C`, `r` and `t*` live.

### Cross-game recognition

**World of Warcraft (Classic era to The War Within).** The increments from one expansion's top to the next were 73, 125, 132, 164, 155 and 265 item levels from Burning Crusade to Legion. The Warcraft Wiki's history of the squish, drawing on a 2011 developer blog, gives the reasoning in the ratchet's terms. Moving to a new tier was meant to bring a matching jump in power, and a new tier of loot was meant to always feel like an upgrade. That is the upgrade margin `u` with a high overlap `o`. The same history singles out Wrath of the Lich King, where hard modes and a fourth raid tier sent item levels far above what the team had planned. In the model, that is `D` and `T` both growing, which raises `C` directly.

**Final Fantasy XIV (A Realm Reborn to Dawntrail).** The official wiki describes a fixed schedule since Stormblood. At each level cap there are three tiers of item levels spanning 100 in total, 40 released with the x.0 and x.05 patches, 30 with x.2 and 30 with x.4. Each rise matches a new tomestone and a new 8-player raid tier. Leveling to the next cap adds about 30 more. So `T = 3` with steps of 40, 30 and 30, plus 30 between expansions, is 130 every time. That is the ratchet with every term fixed by policy. It creeps just as surely as WoW, but at a rate anyone can predict years ahead, which is what a content calendar needs.

**Guild Wars 2 (2012 onward).** Guild Wars 2 stopped the ratchet instead of tuning it. Its wiki lists ascended gear as 5% stronger than exotic and legendary gear as equal to ascended, and the level cap has stayed at 80. In model terms it ran the ratchet for one tier, then set `c = 0`. GD203 week 14 already worked through what that buys and what it costs, so here only note the corollary. A game with `c = 0` needs week 1's other families (rank and breadth) to carry the whole endgame.

**World of Warcraft rated PvP (current).** Even inside a creeping game, a mode can opt out. The Warcraft Wiki notes that item level in battlegrounds, arenas and rated battlegrounds is limited by a PvP item level cap. That is a local `c = 0` for a mode where a power gap is unfair rather than rewarding. Week 7 treats this kind of split tuning in depth.

Four cases, one model. For any vertical system, ask how many rungs and tiers it has, how far apart the rungs are, what a visible upgrade needs, and whose gear the next tier must beat.

### Eyes-open design judgment

The ratchet is not something to eliminate. It is something to set on purpose.

- **A high overlap `o` gives clean resets.** Everyone's gear is replaced at once, old content can be ignored, and the new tier is easy to explain. It costs you shelf life. At `o = D − 1` a tier is out of date in about two tiers.
- **A low overlap keeps old gear useful.** Top players from last tier can skip the new tier's lower rungs, which slows creep and keeps last tier's hardest content meaningful. It also means the new tier offers those players less, so they may run out of goals sooner (week 1).
- **More rungs widen the audience and speed creep.** Every rung you add either raises `(D − 1)s` or forces smaller spacing. If you add rungs, shrink `s` or lower `o` to hold `c`.
- **The upgrade margin is a perception, and perception can be served other ways.** A set bonus, a new effect or a cosmetic can make a reward feel new without adding item levels. That is week 3's subject.
- **A squish is maintenance, not a cure.** GD203 week 8 showed that dividing every number leaves every ratio unchanged. The increments chart shows that the ratchet keeps turning at the same rate after a squish. Week 5 covers when squishing is worth its cost.

Write `D`, `s`, `u`, `o` and `T` into your design document, compute `C` and `t*`, and check them against your content calendar before the first tier ships.

### Check yourself (worked example)

1. A game has `D = 3`, `s = 12`, `u = 6` and `o = 2`, with two tiers per expansion. What is the creep per expansion in item levels?
2. With `g = 1%` and `F = 2`, what is the shelf life of a tier in that game? What happens to it if the designers switch to `o = 1`?

<details>
<summary>Answers</summary>

1. `c = 2 × 12 + 6 = 30`, so `C = 2 × 30 = 60` item levels per expansion.
2. `r = 1.01^30 = 1.348`, so `t* = ln 2 / ln 1.348 = 0.693 / 0.2986 = 2.32` tiers. With `o = 1`, `c = 18`, `r = 1.01^18 = 1.196` and `t* = 0.693 / 0.1791 = 3.87` tiers.

</details>

## 3. Measuring creep from data

Given an item-level history, you can ask which model fits it. Two candidates matter.

- **Additive creep.** Each period adds about the same number of item levels. This is the ratchet with fixed terms.
- **Multiplicative creep.** Each period multiplies item level by about the same ratio. This is what you would see if designers set each tier as "10% better than the last" on the label itself.

Compute both from the WoW and Final Fantasy XIV numbers.

```python
wow = [("TBC", 159), ("Wrath", 284), ("Cata", 416), ("MoP", 580),
       ("WoD", 735), ("Legion", 1000)]
prev = 86  # Classic-era top
for name, top in wow:
    print(f"{name:7s} +{top - prev:3d}  x{top / prev:.3f}")
    prev = top

ffxiv = [130, 270, 400, 530, 660, 790]
print([b - a for a, b in zip(ffxiv, ffxiv[1:])])
print([round(b / a, 3) for a, b in zip(ffxiv, ffxiv[1:])])
```

```
TBC     + 73  x1.849
Wrath   +125  x1.786
Cata    +132  x1.465
MoP     +164  x1.394
WoD     +155  x1.267
Legion  +265  x1.361
[140, 130, 130, 130, 130]
[2.077, 1.481, 1.325, 1.245, 1.197]
```

Final Fantasy XIV is additive, exactly. Its ratio falls every expansion, from 2.08 to 1.20, because the same 130 levels are a smaller share of a bigger number.

WoW is in between but closer to additive. Its ratios fall from 1.85 to about 1.36, so it is not multiplicative on the label. Its increments rise, from 73 to 265, so it is not a fixed ratchet either. It is a ratchet whose terms grew. That fits the wiki's account of hard modes and extra tiers.

Now the squished eras. Using each squish's mapping of the previous top as the starting point, the increments are 220 for Battle for Azeroth (265 to 485), then 171, 217 and 202 for Shadowlands, Dragonflight and The War Within. On a fresh, smaller scale the same size of step came back. On the new scale those steps are much larger ratios. Shadowlands' 140 to 311 is a ratio of 2.22, the largest in the table. That is the practical reason games squish again. Additive creep on a squished scale grows the ratios, and the numbers stop being readable within a few expansions.

A caution before you read too much into one table. Item level is a label. Whether additive creep in item level is additive or multiplicative in *power* depends on the budget formula. That is why the model separates `c` (in levels) from `g` (power per level). If you know `g` for your own game, and as the designer you do, you can turn any item-level plan into a power plan and a shelf life.

## 4. Creep beyond gear

The ratchet rule applies to any reward that must beat what players already have to be wanted.

- **New abilities and talents.** A new talent that is weaker than the one it competes with is never picked. A designer who wants it picked makes it at least as good, and the average power of the chosen set rises. MMO303 week 1 called this viability. Here it is viability over time.
- **New classes and specializations.** A new class launched weaker than the existing ones is ignored. Launched stronger, it pulls the whole roster's target up when the others are buffed to match.
- **PvP rewards.** When PvP gear is also PvE gear, PvP players must keep up with the ratchet. When a mode caps item level, as WoW's rated PvP does, that mode leaves the ratchet.

In each case the fix is the same trio of knobs. Lower the margin by which new things must win (make new options different instead of stronger), lower the overlap (let old options stay competitive), or cap the mode. Each knob costs something players value, the "shiny upgrade" moment in particular. Your job is to decide how much of that moment the game can afford.

## 5. Planning creep for a five-year game

Here is how the ratchet turns into a plan.

Suppose you plan five expansions over ten years, each with three tiers. You want any tier's content to stay usable for players two tiers behind (`t* ≥ 3`, a little slack) at `F = 2`, and your budget formula gives `g = 1%` per item level.

From `t* = ln F / (c × ln 1.01) ≥ 3`, the creep per tier must satisfy `c ≤ ln 2 / (3 × ln 1.01) = 0.693 / 0.02985 = 23.2` item levels.

With a four-rung ladder at `s = 10` and `u = 5`, that allows `o × 10 + 5 ≤ 23.2`, so `o ≤ 1.8`. The new entry rung may beat the old second rung but not the third. Over the whole plan, creep is `15 tiers × 15 levels = 225` item levels at `o = 1`, a power multiplier of `1.01^225 = 9.4`. That is a number you can show your engineers, who will tell you whether the damage and health values it implies still fit on screen and in their data types, and so whether you need a squish somewhere in the plan (week 5).

The same arithmetic run the other way tells you what a designer's reflex costs. "Every tier should replace all gear" means `o = 3`, `c = 35` and `t* = 2.0`, and over 15 tiers a power multiplier of `1.01^525 = 186`. That game will squish at least once.

## In-class activity (25 minutes)

Pairs. You are the systems designer on a new MMO's first expansion plan, three tiers per expansion, four expansions planned.

1. **(5 min)** Pick `D`, `s` and `u` for your raid ladder. Justify each in one sentence (who is each rung for, and what makes an upgrade visible).
2. **(7 min)** Use the interactive's ratchet tab to find the largest `o` that keeps `t* ≥ 3` tiers at `g = 1%` and `F = 2`. Record `c` and `C`.
3. **(8 min)** Your producer wants a fifth rung for a new "legend" difficulty. Show what it does to `c` if you keep `o` as a rung index, and propose a change to `s` or `o` that holds `c` where it was.
4. **(5 min)** Swap plans with another pair. Find the tier in their plan whose players get the smallest upgrade from the next tier, and say whether those players will still have a reason to play (use week 1's families).

Expected output: a one-row table of your `D, s, u, o, T, c, C, t*`, your five-rung fix, and the other pair's weakest point.

## Common misconceptions

- **"Power creep means the designers lost control."** A fixed ratchet creeps at a fixed rate by design. Final Fantasy XIV's 130 levels per expansion is creep under complete control. The question is whether the rate was chosen.
- **"The squish fixed power creep."** It rescaled the label. On WoW's data the increments per expansion after each squish were about as large as before it. Ratios between players (GD203 week 8) do not change at all.
- **"Item level growth is exponential, so power growth is exponential."** Item level growth in both games is closer to additive. Power growth may still be exponential, but that comes from the budget formula (`g`), not from the item-level chart.
- **"More difficulty rungs are free content."** Each rung either widens the ladder, which raises `c` under a high overlap rule, or narrows the spacing, which makes each rung's reward feel smaller.

## Check yourself

1. A tier plan has `D = 4`, `s = 13`, `u = 7` and `o = 2`, with four tiers per expansion. Compute `c` and `C`. How many item levels does the game add over three expansions?
2. The WoW data shows the top item level going from 580 to 735 across one expansion. Treat that as a single additive step. What ratio does it correspond to, and what ratio would the same step of 155 be if it started from 140?
3. At the BlizzCon 2013 presentation of the first squish, a character at item level 530 was shown with 20,640 intellect before the squish and 1,100 after. By what factor did intellect shrink? If two characters had 20,640 and 18,000 intellect before, what is the ratio between them after, assuming the same factor applies to both?
4. Your game has `g = 0.8%` per item level and you want `t* ≥ 4` at `F = 1.5`. What is the largest creep per tier you can allow?

<details>
<summary>Answers</summary>

1. `c = 2 × 13 + 7 = 33`, `C = 4 × 33 = 132`. Over three expansions, 396 item levels.
2. `735 / 580 = 1.267`. From 140, `295 / 140 = 2.107`. The same step is a much larger ratio on a small scale.
3. `20,640 / 1,100 = 18.8`. The ratio is unchanged at `20,640 / 18,000 = 1.147` (after, `1,100 / 959 = 1.147`). A squish rescales every number by the same factor, so every ratio survives.
4. `c ≤ ln 1.5 / (4 × ln 1.008) = 0.4055 / (4 × 0.007968) = 12.7` item levels per tier.

</details>

## Lab / assignment hook

[Lab 02, power creep audit](../labs/lab02.md). You will load the item-level histories from this lecture, fit additive and multiplicative models, implement the ratchet, and write a creep budget for a four-expansion plan. It feeds the progression analysis assignment (30%).

## Sources

- Warcraft Wiki, "Stat squish" (current, updated for Midnight). Squishes in patches 6.0.2, 8.0.1, 9.0.1 and 12.0.0; item level squish table with native ranges from the first normal-difficulty raid to the highest achievable item level for each expansion, and their values after each squish; History section summarising the reasons for item-level inflation, including Wrath of the Lich King's hard modes and fourth raid tier; BlizzCon 2013 slide values at item level 530. https://warcraft.wiki.gg/wiki/Stat_squish
- Street, G. "Dev Watercooler: The Great Item Squish (or Not) of Pandaria." World of Warcraft official site, November 2011. Cited by the wiki's History section. https://worldofwarcraft.blizzard.com/en-us/news/3885585/dev-watercooler-the-great-item-squish-or-not-of-pandaria
- Warcraft Wiki, "Patch 12.0.0" (Midnight pre-expansion, released 20 January 2026). Lists the stat squish among the patch's changes. https://warcraft.wiki.gg/wiki/Patch_12.0.0
- Warcraft Wiki, "Item level" (current). Item level as a rough indicator of an item's power and budget; PvP item level cap in battlegrounds, arenas and rated battlegrounds. https://warcraft.wiki.gg/wiki/Item_level
- Final Fantasy XIV Online Wiki, "Item Level" (Dawntrail era, 2026). Maximum item level per level cap (130, 270, 400, 530, 660, 790); three tiers spanning 100 item levels at each cap since Stormblood, released at x.0/x.05, x.2 and x.4; about 30 levels between caps. https://ffxiv.consolegameswiki.com/wiki/Item_Level
- Guild Wars 2 Wiki, "Ascended equipment" (current). Ascended stats 5% above exotic and equal to legendary. https://wiki.guildwars2.com/wiki/Ascended_equipment
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press. Chapter "Progression in PvE Games".

## Interactive spec: examples/w02-power-creep.html

**The one insight.** The item-level chart looks like runaway growth that squishes fix. The increments view shows the ratchet turning at the same rate before and after every squish, and the ratchet tab shows that the overlap rule, not the size of the numbers, sets the rate.

**Layout.** Two tabs, "The chart" and "The ratchet." Each tab has the chart on top, controls below, readout under the controls. Works at 390px (single column) and 1280px.

**Tab 1, "The chart."**
- Data, hard-coded. WoW native tops by expansion index: Classic 86, TBC 159, Wrath 284, Cata 416, MoP 580, WoD 735, Legion 1000, then squish to 265 (patch 8.0.1), BfA 485, squish to 140 (patch 9.0.1), SL 311, DF 528, TWW 730, squish to 170 (patch 12.0.0). Also show each expansion's bottom as a lighter bar segment (ranges from the lecture table for Classic to Legion, and from the paragraph under it for BfA 340-485, SL 184-311, DF 376-528, TWW 623-730).
- Final Fantasy XIV tops by expansion: 130, 270, 400, 530, 660, 790 (ARR to Dawntrail).
- x-axis: expansion order (11 WoW expansions; FFXIV's 6 aligned to their own index, with a note that the time axes differ). y-axis: item level.
- Squishes drawn as vertical drops with a small label "8.0.1: 1000 → 265" etc.
- Toggles: "Log axis" (y log scale), "Show FFXIV", "Increments" (replaces lines with bars of per-expansion increments on the scale in use: 73, 125, 132, 164, 155, 265, 220, 171, 217, 202 for WoW; 140, 130, 130, 130, 130 for FFXIV; bars after a squish are outlined differently).
- Caption under the increments view: "After each squish the steps are as big as before. The label reset; the ratchet didn't."
- Readout table: expansion, top, increment, ratio to previous top (3 decimals). Values as in lecture section 3.

**Tab 2, "The ratchet."**
- Chart: x-axis tiers 0 to `T × E` (E expansions, default 4). Each tier is a column of `D` dots (rungs) at `L_t + j × s`, `j = 0..D−1`, with `L_0 = 100`. Connect each tier's rung `o` to the next tier's rung 0 with an arrow labelled `+u`.
- A second small chart below: power multiplier `r^t = (1+g)^(c t)` on a log axis, with a shaded band `G ≤ F` and a marker at `t*`.
- Controls: `D` stepper 2 to 6 (default 4); `s` slider 1 to 30 (default 10); `u` slider 0 to 20 (default 5); `o` stepper 0 to `D − 1` (default 1; clamp when `D` changes); `T` stepper 1 to 5 (default 3); `E` stepper 1 to 6 (default 4); `g` slider 0.2% to 2.0% step 0.1% (default 1.0%); `F` slider 1.2 to 4 step 0.1 (default 2).
- Readout: `c = o s + u`, `C = T c`, total over plan `E C`, `r = (1+g)^c` (3 decimals), `t* = ln F / (c ln(1+g))` (2 decimals; "unlimited" if `c = 0`), plan power multiplier `(1+g)^(E T c)` (1 decimal).
- Keyboard operable controls with labels and live values; respects `prefers-reduced-motion`.

**Formulas.**
```
c      = o * s + u
C      = T * c
r      = (1 + g)^c
tStar  = ln(F) / (c * ln(1 + g))
plan   = (1 + g)^(E * T * c)
```

**Test values.**
- `D=4, s=10, u=5, g=1%, F=2, T=3`: `o=0` gives `c=5, C=15, r=1.051, t*=13.93`; `o=1` gives `c=15, C=45, r=1.161, t*=4.64`; `o=2` gives `c=25, C=75, r=1.282, t*=2.79`; `o=3` gives `c=35, C=105, r=1.417, t*=1.99`.
- `D=3, s=12, u=6, o=2, T=2`: `c=30, C=60`, `t*=2.32`.
- `o=1, T=3, E=5, s=10, u=5, g=1%`: plan multiplier `1.01^225 = 9.4`. `o=3`: `1.01^525 = 185.7`.
- `g=0.8%, F=1.5`: `t* ≥ 4` needs `c ≤ 12.7`.
