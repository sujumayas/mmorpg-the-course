# GD203 · Week 10 — Enemy Design by the Numbers

**Why this matters:** An enemy is two numbers pointed at the player. How long it takes to die, and how much of the player's health it takes with it. Once you can write both numbers down, you can design a goblin, a pack of goblins and a boss on purpose instead of by guessing and playtesting until it feels right.
**You will be able to:**
- Convert an enemy's hit points and damage into player units (time-to-kill and fraction of player health lost).
- Compute the health cost of an encounter with several enemies, under focus fire and under area damage.
- Derive the kill order that minimizes damage taken, and design enemy rosters so that kill order is a real decision.
- Build an enemy stat block from a role template (fodder, soldier, elite, boss) at any player level.

**Before class:** Schreiber & Romero, *Game Balance* (2021), the chapters on combat and on characters and enemies; Schreiber, *Game Balance Concepts*, level 3 (transitive mechanics and cost curves).
**Prerequisites from earlier courses:** GD203 week 4, [time-to-kill and time-to-die](w04-time-to-kill-and-time-to-die.md); GD203 week 8, [power curves and level scaling](w08-power-curves-and-level-scaling.md); GD102 week 3, positive feedback loops ([lecture](../../GD102-systems-design-and-game-mechanics/lectures/w03-positive-feedback-loops-snowballing.md)). Looking ahead, MMO303 week 2, [armor and damage mitigation](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w02-armor-and-damage-mitigation.md) (year 3), treats effective HP in depth.
**Interactive:** [Encounter cost](../examples/w10-encounter-cost.html) (built from the spec at the end of this lecture). Keep it open during section 2.

---

## 1. Enemies are measured in player units

Open the source code of the original Doom (id Software released it in 1997) and you find every monster's health as a plain integer. A Zombieman has 20. An Imp has 60. The pink Demon has 150, the Cacodemon 400, the Baron of Hell 1,000 and the Cyberdemon 4,000.

Those numbers mean nothing on their own. Nobody feels "60". What players feel is how many trigger pulls a monster takes. Doom's shotgun fires 7 pellets, and each pellet deals 5, 10 or 15 damage, so a point-blank blast averages 70. Divide and you get the numbers the designers were really choosing:

| Monster | Health | Average shotgun blasts to kill |
|---|---|---|
| Zombieman | 20 | 0.29 |
| Imp | 60 | 0.86 |
| Demon | 150 | 2.1 |
| Cacodemon | 400 | 5.7 |
| Baron of Hell | 1,000 | 14.3 |
| Cyberdemon | 4,000 | 57.1 |

Read down the right column and you can see the design. Fodder dies to one blast. The Demon takes two or three. The Baron is a wall you have to commit to. The Cyberdemon is a boss that you cannot fight with the shotgun at all; you need a bigger weapon or a lot of patience.

This is the first rule of enemy design. **Write enemy stats in player units, then convert to raw numbers last.** Two conversions matter.

- **Time-to-kill (TTK)** is how long the player needs to kill the enemy: `TTK = h / P`, where `h` is the enemy's health and `P` is the player's damage per second (DPS) against it. You met TTK in [GD203 week 4](w04-time-to-kill-and-time-to-die.md), including the off-by-one that discrete hits add. This lecture uses the smooth version, `h / P`, because it keeps the encounter math readable. Here TTK is the enemy's defensive number.
- **Threat rate** is the fraction of the player's health the enemy removes per second: `r = d / H`, where `d` is the enemy's DPS against the player and `H` is the player's health. This is the enemy's offensive number.

If a Doom Imp's fireball hits for between 3 and 24 and your marine has 100 health, one fireball costs 3% to 24% of your life. That percentage, and the number of blasts in the table, are the two numbers a player's body learns. The raw 60 and 3-to-24 are only how the code stores them.

### Why player units scale

When the player levels up, `P` and `H` grow. If you designed enemies in raw numbers, every enemy at every level needs retuning by hand. If you designed them in player units ("a soldier dies in 5 seconds and costs 10% of your health"), you recompute the raw stats from the player's curve at each level and the fight stays the same length. GD203 week 8 built those player curves. This week we hang enemies off them.

## 2. Worked example: what a fight costs

### The hook

Groups in World of Warcraft mark enemies with icons before a pull. By long-standing convention the skull goes on the enemy the group kills first, and the X on the one killed second. Ask a group why the skull is on the small caster and not on the big brute, and they will say the caster "hurts more." That instinct is right, and it has an exact form.

Doom poses the same question from the other side. A Baron has 16.7 times an Imp's health, and its fireball averages 36 damage against the Imp's 13.5 (the source code rolls 8 × 1d8 for the Baron and 3 × 1d8 for the Imp). So is one Baron worth 16.7 Imps? Or 2.7? Or something else? By the end of this section you can answer it in one line.

### The model

One player with DPS `P` fights enemies one after another (focus fire). Enemy `i` has health `h_i` and DPS `d_i`. Every enemy deals damage until the moment it dies. So the damage the player takes is:

```
cost = Σ d_i × T_i
```

where `T_i` is the time at which enemy `i` dies. Under focus fire, `T_i` is the total health of every enemy killed up to and including `i`, divided by `P`.

That single line gives three results you will use every time you design an encounter.

**One enemy alone.** `cost = d × h / P`. The cost grows with the *product* of health and damage. Double either one and you double the cost. Double both and you quadruple it.

**A pack of n identical enemies.** The first dies at `h/P`, the second at `2h/P`, and so on. The sum is:

```
cost_pack = (d × h / P) × (1 + 2 + ... + n) = c × n(n+1)/2
```

where `c = d × h / P` is the cost of one enemy alone.

**Area damage (AoE).** If the player's attack hits every enemy at once for a fraction `a` of single-target DPS, all `n` enemies die together at time `h / (a × P)`:

```
cost_aoe = n × c / a
```

**Kill order.** With different enemies, the order changes `T_i`. The order that minimizes total cost is to kill enemies in decreasing order of `d_i / h_i`, damage per second per point of health. Call it an enemy's **priority ratio**. Kill the highest ratio first. (The proof is a swap argument. If two neighbours in the order are the wrong way round, swapping them lowers the cost, so the optimal order has no wrong-way neighbours.)

### Numbers you can check

Our test player has `P = 20` DPS and `H = 200` health. A goblin has `h = 40` and `d = 4`. One goblin dies in 2 seconds and costs `4 × 40 / 20 = 8` health, which is 4% of the player.

Now fight packs. The "merged" column is one big enemy with the pack's total health and total DPS (so for n = 5, an ogre with 200 health and 20 DPS).

| Goblins (n) | Focus fire, one at a time | One merged enemy | AoE at full DPS (a = 1) | AoE at half DPS (a = 0.5) |
|---|---|---|---|---|
| 1 | 8 | 8 | 8 | 16 |
| 2 | 24 | 32 | 16 | 32 |
| 3 | 48 | 72 | 24 | 48 |
| 5 | 120 | 200 | 40 | 80 |
| 8 | 288 | 512 | 64 | 128 |

Three facts jump out.

1. **The merged enemy is the deadliest.** Five goblins cost 120, 60% of the player. An ogre with the same totals costs 200 and kills the player exactly. Splitting an enemy into a pack makes it weaker, because every goblin that dies stops dealing damage. The ratio is `(n+1) / (2n)`, which heads toward one half for large packs.
2. **Pack cost grows with the square of pack size.** Eight goblins cost 36 times one goblin, not 8 times. Adding the sixth goblin adds 6 × 8 = 48 health of cost, while the first added 8.
3. **AoE flattens the square into a line.** With full-strength AoE, 8 goblins cost 8 times one goblin. Half-strength AoE breaks even with focus fire at `n = 3` and wins above it. In general AoE at fraction `a` beats focus fire when `a > 2 / (n + 1)`.

Now kill order. Put three different enemies in front of the same player:

| Enemy | Health h | DPS d | Priority ratio d/h |
|---|---|---|---|
| Archer | 20 | 6 | 0.30 |
| Shaman | 40 | 8 | 0.20 |
| Brute | 120 | 12 | 0.10 |

All six orders, with the cost of each:

| Kill order | Death times (s) | Cost |
|---|---|---|
| Archer, Shaman, Brute | 1, 3, 9 | 6 + 24 + 108 = **138** |
| Shaman, Archer, Brute | 2, 3, 9 | 16 + 18 + 108 = 142 |
| Archer, Brute, Shaman | 1, 7, 9 | 6 + 84 + 72 = 162 |
| Shaman, Brute, Archer | 2, 8, 9 | 16 + 96 + 54 = 166 |
| Brute, Archer, Shaman | 6, 7, 9 | 72 + 42 + 72 = 186 |
| Brute, Shaman, Archer | 6, 8, 9 | 72 + 64 + 54 = **190** |

The fight always lasts 9 seconds, because the player must chew through 180 health at 20 DPS whatever the order. What changes is who is alive during those 9 seconds. The best order costs 138 (69% of the player's health). The worst costs 190 (95%). The same enemies, the same player and the same fight length leave the player alive with 62 health or with 10. That gap is the reward for a decision, and the priority ratio tells you where it comes from.

### See it move

Open the interactive. The top view is a staircase. Each enemy is a horizontal band whose height is its DPS, and the band ends when the enemy dies. The shaded area under the staircase is the damage the player takes. The bottom view shows the same enemies as a list of health and DPS totals, which never change.

Drag the enemies into a different kill order. The totals in the bottom view stay put, the fight length stays at 9 seconds, and the shaded area grows or shrinks. Tall, short bands (high `d/h`) belong on the left, where they end early. Then open the "Pack vs merged vs AoE" tab, set the pack size to 5, and switch the mode from Focus fire to Merged. The staircase becomes one tall rectangle and the damage taken goes from 120 to 200. Switch to AoE and the five bands end together.

### Cross-game recognition

**Doom, the Baron and the Imps.** Use the cost formula `c = d × h / P` and hold `P` fixed. A Baron has 16.7 times the health and 2.7 times the average fireball damage of an Imp, so its cost is `16.7 × 2.7 ≈ 44` Imp-units. A room of `n` Imps shot one at a time costs `n(n+1)/2` Imp-units. Setting the two equal gives `n ≈ 9`. By this model one Baron takes as much health as nine Imps killed in sequence. The model assumes both monsters fire at the same rate and land the same share of shots, which Doom's code does not promise, so treat the "nine" as the method's answer rather than a measured fact about Doom play. The shape of the answer is the point. It is neither 16.7 nor 2.7, because cost multiplies health and damage.

**World of Warcraft kill markers.** The skull-then-X convention is a hand-written kill order. The math says the skull should go on the highest `d/h` enemy, which in most packs is a caster or healer with low health and high output. A healer is a special case worth noticing. It adds health to its allies, which raises their `h`, so killing it early also shortens every later `T_i`. Crowd control (the moon icon, by convention a sheep or a sap) removes an enemy's `d` for a while, which is like moving it to the end of the order for free.

**Lanchester's square law.** In 1916 the engineer F. W. Lanchester modelled battles between two forces that aim their fire. He showed that a force's strength goes with the *square* of its numbers times the effectiveness of each unit. Our pack formula is the one-sided version. The player's health drains at a rate set by how many enemies are still alive, and the total drain grows with `n²`. MMO303 week 11 treats the two-sided case ([Lanchester's laws and group combat](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w11-lanchesters-laws-and-group-combat.md)).

**Factory scheduling.** In 1956 W. E. Smith published the rule for ordering jobs on a single machine to minimize the weighted sum of their completion times. Sort the jobs by weight divided by processing time, largest first. Replace "job" with "enemy", "processing time" with `h/P` and "weight" with `d`, and you have the priority ratio exactly. Operations researchers call it Smith's rule or weighted shortest processing time. Your player is a machine that processes enemies, and the damage taken is the weighted waiting time.

Three settings, one sum. When you meet a new encounter, write down `d`, `h` and the player's `P`, and ask two questions. What does each enemy cost alone? And which enemy has the highest `d/h`?

### Eyes-open design judgment

**If every enemy has the same priority ratio, kill order does not matter.** Check the math. With equal `d/h`, every order gives the same cost. That is a design smell. A roster where the ratio varies (glass-cannon archers, sturdy brutes) turns target selection into a real choice with a measurable payoff, like the 138 versus 190 above. When you build a roster, make the ratios differ on purpose and make the high-ratio enemies readable at a glance, by silhouette, color or animation.

**Packs and big enemies are different tools.** A pack is cheaper than one merged enemy under focus fire, and much cheaper under AoE. A big single enemy concentrates cost. That concentration is fine if the player has tools to reduce `d` (dodging, blocking, interrupts) and dangerous if they don't. Doom's Cyberdemon costs almost nothing to a player who never gets hit, and everything to one who stands still.

**AoE classes change your pack math.** In a game with strong AoE, pack cost grows linearly, not with the square. Designers who tune packs for single-target classes find that AoE classes breeze through them, and designers who tune for AoE find single-target classes drowning. Decide which you are tuning for, then use the break-even `a > 2/(n+1)` to set AoE strength. If you want AoE to win only against 4 or more enemies, you need `a` between `2/5 = 0.4` and `2/4 = 0.5`.

**The model leaves things out.** It assumes constant DPS on both sides, no healing, no mitigation, no movement and perfect focus fire. Each omission is something you can add later (effective HP from MMO303 week 2 replaces `H`; healing adds a negative term), but the core insight survives. Cost is area under a staircase, and killing things early removes the tall steps.

## 3. From role to stat block

Now turn the model around. Instead of computing the cost of a given enemy, pick the cost you want and solve for the enemy.

### Role templates

Most action games and RPGs use a small set of enemy roles. The names vary. The numbers behind them follow a pattern like this one, written in player units:

| Role | Target TTK | Cost alone (share of player H) | Typical group size |
|---|---|---|---|
| Fodder | 1-2 s | 1-3% | 4-10 |
| Soldier | 4-6 s | 6-12% | 2-4 |
| Elite | 15-25 s | 25-40% | 1, with fodder |
| Boss | 90-180 s | well over 100% without dodging or healing | 1 |

These are this course's starting values, not an industry standard. Your game's pacing sets its own. The point is that each role is a pair of player-unit targets, and the raw stats follow.

### Solving for the stat block

Given the player's DPS `P` and health `H` at a level, a target TTK `t` and a target cost share `s`:

```
h = P × t                    (health that takes t seconds to chew through)
d = s × H / t                (since cost = d × t = s × H)
damage per hit = d × attack interval
```

Worked through for a soldier at a level where the player has `P = 20` and `H = 200`, with `t = 5 s`, `s = 10%` and one attack every 2 seconds:

- `h = 20 × 5 = 100` health.
- `d = 0.10 × 200 / 5 = 4` DPS.
- Damage per hit `= 4 × 2 = 8`, which is 4% of the player's health per hit, or 25 hits to kill the player.

Now suppose the player reaches a level where `P = 45` and `H = 380`. Same role, same targets: `h = 225`, `d = 7.6`, damage per hit 15.2. The fight feels the same because it *is* the same in player units. One refinement before you ship these numbers. With discrete hits, `h = P × t` often lands on the edge of a breakpoint step, so a tiny damage buff removes a whole hit. Week 4 section 4 gives the method for centering `h` inside its step; apply it as the last pass on every stat block. This is how you tie an enemy roster to the power curve from week 8. You store roles as player-unit targets and let the sheet compute raw stats per level. Next week's spreadsheet workshop builds exactly this table.

### Tabletop designers do this too

The 2014 *Dungeon Master's Guide* for Dungeons & Dragons fifth edition gives a monster-creation method built on the same two numbers. You look up a defensive rating from the monster's hit points (adjusted for armor class) and an offensive rating from its average damage per round (adjusted for attack bonus), and the final challenge rating is the average of the two. A monster with huge health and weak attacks lands in the middle, the same as one with modest health and strong attacks. That is the product rule `cost ∝ d × h` in tabletop clothing. Averaging two ratings on a scale that grows roughly geometrically behaves like multiplying the underlying quantities.

## 4. Beyond health and DPS

Two enemies can have identical `h` and `d` and feel nothing alike. Two extra numbers explain most of the difference.

**Hit size relative to player health.** An enemy with 4 DPS might hit for 4 every second or for 40 every ten seconds. The cost formula gives the same answer. The player does not experience it the same way. A hit worth 20% of the player's health is a spike, and spikes need warning. Big hits should come with a **telegraph**, a visible wind-up the player can read and react to. As a rule for your spec, if one hit exceeds about a quarter of the player's health, write down the telegraph time next to it. If one hit can exceed the player's full health, you have designed a one-shot, and it must be avoidable or it is a coin flip.

**Attack interval and the reaction window.** A telegraph shorter than the player's reaction time is not a telegraph. UX201 covers reaction-time measurements and how they change with cue type and cognitive load ([UX201 week 1](../../UX201-game-ux-and-player-psychology/lectures/w01-perception-attention-memory.md)). The slower the attack, the bigger the hit can be while keeping `d` fixed, and the more the enemy tests reading rather than endurance.

**Effective health against the player's damage type.** Armor and resistances change `h` into effective health, exactly as in MMO303 week 2. An enemy with 100 health and 100 armor under `K = 100` has 200 effective health against physical damage. Put effective health, not raw health, into `h = P × t`, or your TTK targets will drift the moment you add armor.

### Modifiers as multipliers

Many games create variety by stacking modifiers on a base enemy: an "elite" or "champion" version with more health, a "berserk" affix with more damage. In player units a modifier is a multiplier on `h`, on `d`, or on both, and it multiplies the cost. An affix that gives ×1.5 health and ×1.5 damage multiplies the cost by 2.25. If your design documents list modifiers as "+50% HP" and "+50% damage" in separate columns, add a third column for the cost multiplier. It prevents the classic mistake of stacking two "moderate" affixes into a monster that costs five times the base.

## In-class activity (25 minutes)

Work in pairs. You design one room for a dungeon at a level where the player has `P = 30` DPS and `H = 300` health. The room's budget is 60% of player health under the player's intended play (focus fire, no healing).

1. Build three enemy types using the role table. Give each a TTK, a cost share, and then compute `h`, `d` and damage per hit at a 2-second attack interval.
2. Make sure the three priority ratios differ by at least a factor of 2 between the highest and lowest.
3. Choose a group (for example 1 elite and 4 fodder) and compute the cost under the best and worst kill order. The best order should land inside the 60% budget. The worst should not.
4. Now add a player class with AoE at `a = 0.4`. Recompute the room cost for that class. Is it inside budget? If it is far under, what one number would you change?

Expected output: a one-page table with each enemy's `h`, `d`, hit size and priority ratio; the best-order and worst-order costs; and a two-sentence note on the AoE class. Swap with another pair and check one of their cost sums by hand.

## Common misconceptions

- **"An enemy with twice the stats is twice as dangerous."** Cost goes with health times damage. Twice the health and twice the damage is four times the cost.
- **"Five goblins are as dangerous as one ogre with five goblins' worth of stats."** Under focus fire the pack costs `(n+1)/(2n)` of the merged enemy, 60% for n = 5, because dead goblins stop hitting.
- **"Kill the enemy with the lowest health first."** Low health helps, but the rule is highest `d/h`. A low-health enemy that deals almost no damage belongs at the end.
- **"Kill order changes how long the fight takes."** With focus fire, the fight length is total health over `P` in every order. Kill order changes how much damage you take during it.

## Check yourself

1. A player with `P = 25` fights a single enemy with 150 health and 6 DPS. What does the enemy cost? What does a pack of four of them cost under focus fire?
2. For a pack of 6 identical enemies, what AoE fraction `a` breaks even with focus fire?
3. Two enemies. A has 60 health and 9 DPS. B has 30 health and 3 DPS. Which should die first, and how much damage does the right order save against a player with `P = 30`?
4. You want a soldier with a 6-second TTK and a cost of 12% against a player with `P = 40` and `H = 500`. It attacks every 1.5 seconds. Give its health, DPS and damage per hit.

<details>
<summary>Answers</summary>

1. Alone, `c = 6 × 150 / 25 = 36`. A pack of four costs `36 × 4 × 5 / 2 = 360`.
2. `a = 2 / (6 + 1) = 2/7 ≈ 0.29`.
3. Priority ratios are A `9/60 = 0.15` and B `3/30 = 0.10`, so A dies first. A first: A dies at 2 s (cost 18), B at 3 s (cost 9), total 27. B first: B dies at 1 s (cost 3), A at 3 s (cost 27), total 30. The right order saves 3 health.
4. `h = 40 × 6 = 240`. `d = 0.12 × 500 / 6 = 10` DPS. Damage per hit `= 10 × 1.5 = 15`.

</details>

## Lab / assignment hook

**Lab 10: Enemy roster from player units** ([labs/lab10.md](../labs/lab10.md)). You build a sheet that turns role templates into stat blocks across levels 1-30, compute encounter costs for five rooms, and flag every room whose cost falls outside its budget. It feeds next week's balancing workshop, which reuses the same sheet.

## Sources

- id Software, *Doom* source code (linuxdoom-1.10, released 1997), files `info.c`, `p_pspr.c` and `p_map.c`. Monster spawn health (Zombieman 20, Imp 60, Demon 150, Cacodemon 400, Baron of Hell 1,000, Cyberdemon 4,000); the shotgun fires 7 pellets of `5 × (1d3)`; missile damage is `(1d8) × base`, with base 3 for the Imp fireball and 8 for the Baron's. Values apply to Doom and Doom II (1993-1994). Doom's random numbers come from a fixed table, so "1d3" and "1d8" are close to, not exactly, uniform.
- Warcraft Wiki, "Target marker". The skull-first, X-second convention and the use of other icons for crowd-control targets (convention since classic World of Warcraft, still current).
- Lanchester, F. W. (1916). *Aircraft in Warfare: The Dawn of the Fourth Arm*. Constable. The square law for aimed fire.
- Smith, W. E. (1956). "Various optimizers for single-stage production." *Naval Research Logistics Quarterly*, 3(1-2), 59-66. The ratio rule for minimizing weighted completion time.
- Wizards of the Coast (2014). *Dungeon Master's Guide* (D&D 5th edition), chapter 9, "Creating a Monster". Defensive and offensive challenge ratings averaged into a final rating.
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press.
- Schreiber, I. (2010). *Game Balance Concepts*, level 3.

## Interactive spec: examples/w10-encounter-cost.html

**The one insight.** The damage an encounter costs is the area under a staircase of enemy DPS over time. Fight length and stat totals can stay fixed while the area changes a lot, because killing high `d/h` enemies first removes the tall steps early.

**Layout.** Two linked views, stacked on mobile, side by side at 1024 px and wider.

- **Top view: DPS staircase.** x-axis is time in seconds (0 to fight length, auto-scaled). y-axis is incoming DPS. Each alive enemy is a band stacked on the others, colored per enemy, height `d_i`, ending at that enemy's death time `T_i`. The area is filled. Label the total area as "Damage taken: N (X% of player health)". Draw a horizontal dashed line at the value that would make the area equal to player health, and turn the damage label to the warning color when area ≥ H.
- **Bottom view: totals.** A small table with each enemy's h, d, `d/h` (2 decimals), death time and personal cost `d_i × T_i`, plus a totals row (sum h, sum d, fight length, total cost). Sum h, sum d and fight length must visibly not change when the order changes.

**Tabs.**

1. **Kill order.** Three enemies, defaults Archer (h 20, d 6), Shaman (h 40, d 8), Brute (h 120, d 12). Player `P = 20`, `H = 200`. Reorder by drag or by up/down buttons on each row (buttons are required for keyboard use). A "best order" button sorts by `d/h` descending, a "worst order" button sorts ascending. Show a mini table of all 6 permutations with their costs, highlighting the current one.
2. **Pack vs merged vs AoE.** Goblin h 40, d 4, player `P = 20`, `H = 200`. Controls: pack size n (1-10), mode radio (focus fire / merged / AoE), AoE fraction `a` slider (0.1-1.0, step 0.05). Merged mode draws one enemy with `n × h`, `n × d`. AoE mode draws n bands all ending at `h / (a × P)`. Show the break-even text "AoE beats focus fire when a > 2/(n+1) = X".
3. **Custom.** Up to 5 enemies with editable h and d (number inputs), player P and H inputs.

**Formulas.**
- Focus fire: `T_i = (Σ_{j ≤ i in order} h_j) / P`; cost `= Σ d_i × T_i`.
- AoE: all enemies take `a × P` each, `T_i = h_i / (a × P)` (each dies independently in its own time); cost `= Σ d_i × T_i`.
- Merged: one enemy with `Σh` and `Σd`.

**Test values (must match exactly).**
- Kill-order tab: Archer, Shaman, Brute → death times 1, 3, 9; cost 138. Brute, Shaman, Archer → 6, 8, 9; cost 190. All six permutation costs: 138, 142, 162, 166, 186, 190.
- Pack tab, focus fire: n = 1 → 8; n = 3 → 48; n = 5 → 120; n = 8 → 288.
- Pack tab, merged: n = 5 → 200 (label turns warning color, equals H).
- Pack tab, AoE: n = 5, a = 1 → 40; n = 5, a = 0.5 → 80; n = 3, a = 0.5 → 48 (equals focus fire, show "break-even").

**First screen.** The kill-order tab in the worst order (cost 190, 95% of health) with the "best order" button prominent. One press shows the area shrink to 138.

**Accessibility and motion.** Animate band widths over 300 ms, disabled under `prefers-reduced-motion`. All controls reachable by keyboard. Numbers in the totals table are selectable text.
