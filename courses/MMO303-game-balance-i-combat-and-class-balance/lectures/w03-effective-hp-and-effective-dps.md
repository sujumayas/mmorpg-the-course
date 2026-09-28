# MMO303 · Week 03 — Effective HP and Effective DPS

**Why this matters:** Character sheets list health, resistances and damage per second as if each number stood alone. In a real fight they multiply together, and the class that looks strongest on paper can lose every duel. Class balance starts when you stop comparing sheets and start comparing how long each class takes to kill each other class.

**You will be able to:**
- Compute effective HP against mixed damage types and find the resist split that maximizes it.
- Compute time to die for a target that is being healed, and explain why healing makes mitigation worth more.
- Compute effective DPS from a sheet value, hit chance, crit, uptime and the target's defenses.
- Build a time-to-kill matrix for three or more classes and identify a dominant class from it.

**Before class:** Re-read week 2, sections 2 and 4. Schreiber & Romero, *Game Balance* (2021), the chapter on combat and the one on characters and classes (skim the latter). Optional: League of Legends Wiki, "Magic resistance" (the effective health section).

**Prerequisites from earlier courses:** effective HP for a single armor stat, `EHP = HP × (1 + A/K)`, from [MMO303 week 2](w02-armor-and-damage-mitigation.md) and [GD203 week 3, mitigation curves and effective HP](../../GD203-combat-and-progression-design/lectures/w03-mitigation-curves-and-effective-hp.md); time-to-kill and DPS from [GD203 week 4](../../GD203-combat-and-progression-design/lectures/w04-time-to-kill-and-time-to-die.md) and [GD203 week 5](../../GD203-combat-and-progression-design/lectures/w05-dps-burst-and-sustain.md); expected value from [MA102 week 4](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md).

**Interactive:** [Resist split explorer](../examples/w03-resist-split.html) (built from the spec at the end of this lecture). Keep it open during section 2.

---

## 1. From one armor stat to a whole fight

Last week you learned the most useful rewrite in combat math. If armor follows `A / (A + K)`, then effective health is a straight line in armor:

```
EHP = HP × (1 + A/K)
```

That formula answers one question well: how much raw damage of one type can this character absorb before dying? Real MMO fights ask three more.

1. **What if damage comes in several types?** Most games split damage into physical, magical (often several elements) and a type that ignores defenses. A character has a different EHP against each.
2. **What if the character is being healed?** Then the right measure is time, not health. How long until they die, if ever?
3. **What does the attacker actually deal?** The sheet DPS is before misses, crits, downtime and the target's defenses.

This lecture answers each in turn and then combines them into one table that tells you whether a set of classes is balanced against each other. We will keep one general definition throughout.

**Effective HP** is health divided by the fraction of raw damage that gets through:

```
EHP = HP / m
```

where `m` is the **damage multiplier**, the share of incoming raw damage that actually reaches health. For one armor stat `m = K / (A + K)`, which gives back last week's formula. Everything new today is about computing `m` for messier situations.

## 2. Worked example: two resists, one budget

### The hook

In *League of Legends*, armor reduces physical damage and magic resistance (MR) reduces magic damage. Riot uses the same formula for both. Physical damage is multiplied by `100 / (100 + armor)` and magic damage by `100 / (100 + MR)`, for non-negative values. Every League guide tells you to build armor against physical-heavy teams and MR against magic-heavy ones.

Here is what the guides don't tell you. Suppose the enemy team deals 80% physical damage. The instinct says to put 80% of your resist budget into armor. The best split is actually about 83% armor. If the enemy is 90% physical or more, you should buy no MR at all. And if the enemy is an even 50/50, splitting evenly makes you survive a third longer than stacking one stat.

None of this is written on any tooltip. It falls out of one line of algebra.

### The model

A character has health `HP`. Incoming raw damage is a fraction `w_p` physical and `w_m` magic, with `w_p + w_m = 1`. The character has armor `A` and magic resistance `M`, both using the same constant `K`.

```
m = w_p × K / (A + K) + w_m × K / (M + K)
EHP = HP / m
```

- `w_p`, `w_m` are the damage shares, which you read from the enemy's damage mix.
- `K / (A + K)` is the fraction of physical damage that gets through.
- `K / (M + K)` is the fraction of magic damage that gets through.
- `m` is the average of those two fractions, weighted by how much of each type arrives.

Now give the character a fixed resist budget `R = A + M`. Which split maximizes EHP? Minimizing `m` with a Lagrange multiplier (or by setting the derivative with respect to `A` to zero) gives

```
(A + K) / (M + K) = √w_p / √w_m
```

In words, **armor-plus-K and MR-plus-K should be in the ratio of the square roots of the damage shares**, not the shares themselves. Writing `S = √w_p + √w_m`, the optimum is

```
A* + K = (2K + R) × √w_p / S
EHP*  = HP × (2K + R) / (K × S²)
```

If this gives a negative value for `M*`, the best you can do is put everything into armor, and vice versa. That happens when `w_m / w_p < (K / (K + R))²`.

### Numbers you can check

Take a 2,000 HP champion with `K = 100` and a budget of 200 total resist points. Assume, for now, that armor and MR cost the same per point.

**Enemy damage 50% physical, 50% magic.**

| Armor / MR | Physical gets through | Magic gets through | m | EHP |
|---|---|---|---|---|
| 200 / 0 | 0.333 | 1.000 | 0.667 | 3,000 |
| 150 / 50 | 0.400 | 0.667 | 0.533 | 3,750 |
| 100 / 100 | 0.500 | 0.500 | 0.500 | 4,000 |

The even split survives 33% longer than stacking one stat, from the same 200 points. Check the formula: `S = 2 × √0.5 = 1.414`, `S² = 2`, so `EHP* = 2,000 × 400 / (100 × 2) = 4,000`.

**Enemy damage 80% physical, 20% magic.**

| Armor / MR | Physical gets through | Magic gets through | m | EHP |
|---|---|---|---|---|
| 200 / 0 | 0.333 | 1.000 | 0.467 | 4,286 |
| 167 / 33 | 0.375 | 0.750 | 0.450 | 4,444 |
| 160 / 40 | 0.385 | 0.714 | 0.451 | 4,439 |
| 100 / 100 | 0.500 | 0.500 | 0.500 | 4,000 |

Here `√0.8 = 0.894`, `√0.2 = 0.447`, `S = 1.342` and `S² = 1.8`. The optimum is `A* + K = 400 × 0.894 / 1.342 = 266.7`, so `A* = 166.7` and `M* = 33.3`. That is 83% armor, not 80%. `EHP* = 2,000 × 400 / 180 = 4,444`.

Look at how flat the top of this table is. The proportional 160/40 split is only 5 EHP short of the optimum, and even pure armor is within 4%. A balanced 100/100 split, the "safe" choice, loses 10%. Two lessons follow. Near the optimum, small mistakes cost little. Far from it, on the wrong side, they cost a lot.

**When to buy no MR at all.** With `K = 100` and `R = 200`, the all-armor condition is `w_m / w_p < (100/300)² = 1/9`, which means magic under 10% of incoming damage. Below that line, every MR point is worth less than an armor point, all the way down.

### A visual you can move

Open the [resist split explorer](../examples/w03-resist-split.html). The left panel shows the percent view players see, two bars for "physical reduction" and "magic reduction." The right panel shows the survival view, EHP plotted against the armor share of your budget, with a dot for your current split and a marker at the optimum.

Set physical share to 50% and drag the split slider from all-armor to all-MR. The left panel always looks like a decent build, since one bar is always high. The right panel shows a hill with its peak in the middle and 25% lower EHP at both ends. Below the plot, a stacked bar shows damage taken by type. At the ends, one colour fills most of the bar. That colour is your weak link, the damage type that is doing most of the killing.

Now drag physical share to 90% and watch the peak slide to the left edge and stay there.

### Cross-game recognition

The core arithmetic here is a **weighted harmonic mean**. If your EHP multiplier against physical is `E_p = 1 + A/K` and against magic is `E_m = 1 + M/K`, your EHP multiplier against the mix is

```
E_mix = 1 / (w_p / E_p + w_m / E_m)
```

Harmonic means are dominated by their smallest term. That is why the weak link rules.

**Dota 2 (patch 7.27 onward, June 2020).** Physical damage is multiplied by `1 − 0.06A / (1 + 0.06|A|)`. For positive armor that simplifies to `1 / (1 + 0.06A)`, which is `K / (A + K)` with `K = 1/0.06 ≈ 16.7`. So a Dota hero's physical EHP is `HP × (1 + 0.06A)`, and each armor point is worth 6% of health. Magic resistance works differently. It is a plain percentage. Every hero starts at 25% base, intelligence adds 0.1% per point to that base, and further sources stack multiplicatively. Dota also has pure damage, which ignores both. Rewrite a hero with 1,500 HP, 10 armor and 25% magic resistance (ignoring the small intelligence bonus) facing a 50/50 mix: physical passes `1/1.6 = 0.625`, magic passes `0.75`, `m = 0.6875`, and `EHP = 2,182`. Same weighted mean, different formula inside each slot.

**Path of Exile 2 (early access, 2024-2025).** Elemental resistances (fire, cold, lightning) are linear percentages with a default cap of 75% and a hard cap of 90%. At 75%, you take a quarter of that element's damage, so your EHP against it is 4× your health. Suppose a boss deals equal parts of all three elements. With all three at 75%, `m = 0.25` and EHP is 4× health. Drop one to 0% and `m = (0.25 + 0.25 + 1) / 3 = 0.5`. Your EHP halves, even though two of three resist bars are still full. This is why players treat capped resistances as mandatory. The game's content assumes them, and one gap is a hole in the whole defense.

**Outside games: average speed.** Drive 60 km at 30 km/h and 60 km back at 90 km/h. Your average speed is not 60. It is `2 / (1/30 + 1/90) = 45` km/h, because the slow leg takes most of the time. Mixed-damage EHP is the same calculation. The damage type you resist worst takes most of your health.

### Eyes-open design judgment

The square-root rule is a property of your formula, and you can use it deliberately.

- **Two defensive stats create a build decision.** One universal "defense" stat removes the choice entirely. Splitting defense into types gives players a reason to scout the enemy and adapt. The cost is more stats to explain and more ways to build badly.
- **The damage mix is a design lever.** If every boss in your raid deals 95% physical damage, magic resistance is a dead stat for tanks (the all-armor rule says so). Give encounters varied mixes, or accept that one stat is PvE-irrelevant.
- **Price differences move the optimum.** If MR costs less per point than armor, the rule becomes `(A + K) / (M + K) = √(w_p × c_M) / √(w_m × c_A)`, where `c` is cost per point. Pricing is how you nudge players toward a split without forcing it.
- **Flat optima are forgiving; cliffs are not.** A formula with a flat peak (like this one near the optimum) lets casual players build "roughly right" and do fine. Linear percent resists with a cap, as in Path of Exile 2, create a cliff at the cap, so the game has to teach players to reach it. Pick which experience you want.
- **Show survival, not percentages.** Players read the left panel. If your UI can show "EHP against this enemy," it teaches the right lesson for free.

### Check yourself (worked example)

Questions 1 and 4 in the Check yourself section at the end of this lecture use this model directly. Try them before moving on.

## 3. True damage and the ceiling on EHP

Many games include a damage type that ignores all defenses. *League of Legends* calls it true damage; *Dota 2* calls it pure damage. Add a share `t` of such damage to the model:

```
m = (1 − t) × [w_p × K / (A + K) + w_m × K / (M + K)] + t
```

Here `w_p` and `w_m` are now shares of the mitigable part. The resist split rule does not change, because `t` does not depend on `A` or `M`. What changes is the ceiling. However much resist you buy, `m` never falls below `t`, so

```
EHP ≤ HP / t
```

With 10% true damage, no build can exceed 10× health. With the 2,000 HP champion at 100/100 against a 50/50 mix plus 10% true damage, `m = 0.9 × 0.5 + 0.1 = 0.55` and `EHP = 3,636`, down from 4,000.

True damage is a balance tool, and a blunt one. It guarantees that defensive stacking has a limit, which protects fights from becoming endless. It also makes defensive investment feel worse, and it gives attackers a counter that no build can answer. Use it in small shares and label it clearly.

## 4. Time, not health: effective HP under healing

In an MMO, tanks are rarely alone. A healer restores health while the boss deals damage. The right question becomes **time to die** (TTD), the number of seconds until health reaches zero.

Let the boss deal `D` raw damage per second, the tank have armor `A` with constant `K`, and a healer restore `H` health per second.

```
damage taken per second = D × K / (A + K)
TTD = HP / (D × K / (A + K) − H)        if damage taken > H
TTD = infinite                          otherwise
```

Take a tank with 10,000 HP facing a boss that deals 400 raw physical DPS, with `K = 100` and a healer providing 150 HPS. These are illustrative numbers for a fictional game.

| Armor | Damage taken per second | TTD, no healer | TTD, 150 HPS healer |
|---|---|---|---|
| 0 | 400.0 | 25.0 s | 40.0 s |
| 50 | 266.7 | 37.5 s | 85.7 s |
| 100 | 200.0 | 50.0 s | 200.0 s |
| 150 | 160.0 | 62.5 s | 1,000.0 s |
| 167 or more | 150.0 or less | 66.7 s or more | never dies |

Without a healer, TTD rises in a straight line with armor, as last week promised. With a healer, the same armor points become worth far more as damage taken approaches healing done. The step from 100 to 150 armor raises TTD from 200 to 1,000 seconds.

There is a neat way to see this. Healing arrives after mitigation. So 150 HPS on a target with 100 armor cancels `150 × (1 + 100/100) = 300` raw DPS. Healing and mitigation multiply each other. This synergy is the mathematical core of the tank-healer pair in [week 5](w05-the-holy-trinity-tank-healer-dps.md), and the reason healer mana, not healer throughput, usually decides long fights ([week 7](w07-healing-throughput-and-mana-economy.md)).

For balance, the lesson is to test tank mitigation with healing in the model. A 10% armor change can look minor on an unhealed TTD chart and still push a tank across the "never dies" line.

## 5. Effective DPS: what actually lands

Now the attacker's side. **Sheet DPS** is the number a character panel or tooltip shows, usually average damage per hit divided by attack interval. **Effective DPS** (eDPS) is what reaches the target's health. It is a chain of multipliers:

```
eDPS = sheet DPS × P(hit) × (1 + c × (M − 1)) × uptime × m_target
```

- `P(hit)` is the chance an attack connects. Week 2 showed Diablo II's chance-to-hit formula, which is one version.
- `c` is crit chance and `M` is the crit damage multiplier. The factor `1 + c(M − 1)` is the expected damage per hit relative to a normal hit (an expected value, from MA102).
- `uptime` is the fraction of the fight the character can attack. Melee characters lose uptime when the boss moves or when they must dodge. Casters lose it while moving if they cannot cast on the move.
- `m_target` is the target's damage multiplier against this attacker's damage type, from section 2.

### Worked numbers: the ranking flips

Two fictional classes, each shown here with the numbers on their character sheets.

| | Blademaster | Pyromancer |
|---|---|---|
| Sheet DPS | 100 | 90 |
| Hit chance | 95% | 100% |
| Crit chance / multiplier | 20% / 2.0× | 10% / 1.5× |
| Uptime | 90% (melee) | 100% (ranged) |
| Damage type | physical | magic |
| eDPS before defenses | 100 × 0.95 × 1.20 × 0.90 = **102.6** | 90 × 1.00 × 1.05 × 1.00 = **94.5** |

Against two different targets (`K = 100` for both armor and MR):

| Target | Armor / MR | Blademaster eDPS | Pyromancer eDPS |
|---|---|---|---|
| Armored golem | 100 / 25 | 102.6 × 0.500 = 51.3 | 94.5 × 0.800 = 75.6 |
| Cloth caster | 20 / 50 | 102.6 × 0.833 = 85.5 | 94.5 × 0.667 = 63.0 |

The Blademaster has the higher sheet DPS and the higher pre-defense eDPS. Against the golem it deals 32% less than the Pyromancer. Neither class is "the stronger damage dealer." Each is stronger against something, and the encounter design decides which.

### One global number can move every class

Crit multipliers are a good reminder to state the version of every formula. In *League of Legends*, critical strikes dealt 200% damage from launch, were reduced to 175% in patch 10.23 (late 2020), and were returned to 200% in patch 26.01, the first patch of 2026. For a champion at 60% crit chance, the crit factor moves from `1 + 0.6 × 0.75 = 1.45` to `1 + 0.6 × 1.0 = 1.6`, a 10.3% eDPS increase from one system constant, with no change to any champion. A designer who compares eDPS across patches without noting that change will blame or credit the wrong champion.

### The terms interact

The multipliers are independent only on paper. Hit chance matters more for a high-crit build, because a miss throws away a potential crit. Uptime penalties hit melee classes hardest in fights with movement, so the same class can be balanced in a stationary boss and weak in a mobile one. When you balance, compute eDPS per encounter type, not once.

## 6. Putting both sides together: the time-to-kill matrix

Class balance in PvP is about pairs. For attacker `i` and target `j`,

```
TTK(i → j) = EHP_j against i's damage type / eDPS_i
```

A table of every `TTK(i → j)` is a **time-to-kill matrix**. In a duel between `i` and `j`, whoever has the shorter time to kill the other wins (ignoring burst, control and range, which later weeks add). The matrix is the simplest tool that captures both EHP and eDPS at once.

Three fictional classes, all with `K = 100`.

| Class | HP | Armor | MR | Pre-defense eDPS | Damage type |
|---|---|---|---|---|---|
| Blademaster | 1,200 | 60 | 20 | 102.6 | physical |
| Pyromancer | 800 | 20 | 50 | 94.5 | magic |
| Warden | 1,600 | 80 | 60 | 60.0 | physical |

Their EHPs are `HP × (1 + R/K)`, using armor against physical attackers and MR against magic ones.

| Target | EHP vs physical | EHP vs magic |
|---|---|---|
| Blademaster | 1,920 | 1,440 |
| Pyromancer | 960 | 1,200 |
| Warden | 2,880 | 2,560 |

Time to kill, in seconds (row attacks column):

| Attacker → target | Blademaster | Pyromancer | Warden |
|---|---|---|---|
| Blademaster | 18.7 | 9.4 | 28.1 |
| Pyromancer | 15.2 | 12.7 | 27.1 |
| Warden | 32.0 | 16.0 | 48.0 |

Read the duels off pairs of cells.

- Blademaster vs Pyromancer: 9.4 s against 15.2 s. Blademaster wins.
- Blademaster vs Warden: 28.1 s against 32.0 s. Blademaster wins, narrowly.
- Pyromancer vs Warden: 27.1 s against 16.0 s. Warden wins.

The Blademaster beats both other classes. In week 1's language, the roster is unfair in duels and will lose diversity, because players copy what wins. The matrix also tells you the margin. The Blademaster-Warden duel is a 14% gap (32.0 / 28.1), so a small change fixes it. The Blademaster-Pyromancer duel is a 63% gap, which needs a structural change.

A matrix with no dominant row is the starting point for intransitive design, the rock-paper-scissors structure of [week 9](w09-intransitivity-and-counters.md). The in-class activity asks you to create one.

### Judgment: what the matrix leaves out

The TTK matrix assumes both sides deal steady damage from the first second. Real fights have burst ([GD203 week 5](../../GD203-combat-and-progression-design/lectures/w05-dps-burst-and-sustain.md)), crowd control ([week 8](w08-crowd-control-and-diminishing-returns.md)), range and mobility, and healing. It also treats PvP duels as the unit, while many MMOs balance around group fights ([week 11](w11-lanchesters-laws-and-group-combat.md)). Use the matrix to find obvious dominance quickly and cheaply. Then confirm with a simulator ([week 13](w13-combat-simulators.md)) before you ship a change.

## In-class activity (25 minutes)

Pairs, with the three-class table from section 6 in a spreadsheet.

1. Rebuild the EHP table and the TTK matrix in the sheet with formulas, not typed values. Confirm your cells match the lecture to one decimal.
2. Change at most two numbers in the class table so that no class beats both others, and every class beats exactly one. Record which duel each class wins.
3. For your new roster, compute each class's pre-defense eDPS against the armored golem from section 5. Does your PvP fix change who is best at PvE?
4. Swap sheets with another pair. Find one number in their fix that a player would notice as a large change, and argue whether it is acceptable.

Expected output: the sheet, the two changes and a one-line cycle statement. One valid answer is to raise the Pyromancer's armor from 20 to 70 and lower the Blademaster's MR from 20 to 0. Then the Pyromancer's physical EHP is 1,360, the Blademaster kills it in 13.3 s and it kills the Blademaster in 12.7 s. The cycle becomes Pyromancer beats Blademaster, Blademaster beats Warden, Warden beats Pyromancer (22.7 s against 27.1 s).

## Common misconceptions

- **"Match your resists to the damage mix: 80% physical means 80% armor."** The optimum follows square roots, not shares. At 80/20 the best armor share is 83%, and below 10% magic you should buy no MR at all (for `K = 100`, budget 200).
- **"A high resist in one type makes me tanky."** EHP against a mix is a harmonic mean, dominated by your weakest resist. One uncapped element in Path of Exile 2 halves survival against an even three-element mix.
- **"Healing just adds to health, so it's separate from armor."** Healing arrives after mitigation, so each point of healing cancels `(1 + A/K)` points of raw damage. The two multiply.
- **"Higher sheet DPS means a stronger damage dealer."** eDPS depends on hit chance, crits, uptime and the target's defenses. The Blademaster's 100 sheet DPS loses to the Pyromancer's 90 against an armored target.

## Check yourself

1. A 3,000 HP character (`K = 100`) has a resist budget of 150 and faces damage that is 60% physical and 40% magic. What split of armor and MR maximizes EHP, and what is that EHP? What EHP would all-armor give?
2. A tank with 8,000 HP faces 500 raw physical DPS (`K = 100`) and has a healer providing 200 HPS. How much armor makes the tank unkillable? What is TTD at 100 armor, with and without the healer?
3. In *League of Legends*, how much does a champion's eDPS change between patch 10.23 and patch 26.01 rules at 60% crit chance, if nothing else changes? At 20% crit chance?
4. In a game with Path of Exile 2-style resistances, a boss deals equal fire, cold and lightning damage. Your character has 75%, 75% and 30%. What is your EHP as a multiple of health? How much longer do you survive if you raise the 30% to 75%?
5. In the section 6 matrix, by how much must the Warden's eDPS rise for it to beat the Blademaster? Does the change affect any other duel's winner?

<details>
<summary>Answers</summary>

1. `√0.6 = 0.775`, `√0.4 = 0.632`, `S = 1.407`, `S² = 1.98`. `A* + K = 350 × 0.775 / 1.407 = 192.7`, so armor 92.7 and MR 57.3. `EHP* = 3,000 × 350 / (100 × 1.98) = 5,303`. All-armor gives `m = 0.6 × 100/250 + 0.4 = 0.64` and `EHP = 4,688`, about 12% less.
2. Unkillable when `500 × 100 / (100 + A) ≤ 200`, so `A ≥ 150`. At 100 armor, damage taken is 250 per second. Without the healer TTD is `8,000 / 250 = 32` s. With the healer it is `8,000 / (250 − 200) = 160` s.
3. At 60% crit, the factor goes from 1.45 (175% crits) to 1.60 (200% crits), a 10.3% increase. At 20% crit it goes from 1.15 to 1.20, a 4.3% increase. High-crit champions gained more than twice as much from the same global change.
4. `m = (0.25 + 0.25 + 0.70) / 3 = 0.40`, so EHP is 2.5× health. Capping the third gives `m = 0.25`, EHP 4× health, which is 60% longer survival.
5. The Warden must kill the Blademaster in less than 28.1 s, so its eDPS must exceed `1,920 / 28.07 = 68.4`, up 14% from 60. The Warden then also beats the Pyromancer by more (it already won), so no other duel changes winner. But now the Warden beats both others, and it becomes the dominant class. Fixing one duel can move the problem instead of solving it.

</details>

## Lab hook

**Lab 03: The EHP / eDPS calculator and a four-class TTK matrix** ([labs/lab03.md](../labs/lab03.md)). You build a spreadsheet that computes mixed-damage EHP, healed TTD, eDPS and the full TTK matrix for four classes, then tune the roster until no class dominates. The calculator is the first piece of the simulator you build in week 13 and a required input to the final balance pass.

## Sources

- League of Legends Wiki, "Magic resistance" and "Armor." Damage multiplier `100 / (100 + MR)` for non-negative MR and the matching armor formula; effective health as `(1 + MR/100) × HP` against magic damage. Current live rules, 2026.
- League of Legends Wiki, "Critical strike." Base critical damage 200% from launch, 175% from patch V10.23, 200% again from patch V26.01.
- League of Legends Wiki, "True damage." True damage is not reduced by armor or magic resistance.
- Liquipedia Dota 2 Wiki, "Armor" and "Armor/Changelogs." Damage multiplier `1 − 0.06A / (1 + 0.06|A|)` introduced in patch 7.27 (June 2020), replacing the 7.20 formula.
- Liquipedia Dota 2 Wiki, "Magic Resistance" and its game-constant data module (Module:Attribute bonuses/data, read September 2026). 25% base hero magic resistance, +0.1% base magic resistance per point of intelligence, multiplicative stacking of further sources; armor factor 0.06. Current rules, 2026.
- Maxroll, "Defence Guide," Path of Exile 2 (written for early access, December 2024). Elemental resistances as a linear percentage, 75% default cap, 90% hard cap.
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press.

## Interactive spec: examples/w03-resist-split.html

**The one insight.** The percent view of resistances always looks reasonable, but survival (EHP) against a mixed damage source has a clear peak, and that peak follows the square roots of the damage shares. Stacking one resist leaves a weak link that the stacked damage bar makes visible.

**Layout.** Two linked views plus a readout strip. Side by side above 900px, stacked below (percent view first, then survival view).

- Left, "What the tooltip says": two horizontal bars, "Physical reduction" = `A/(A+K)` and "Magic reduction" = `M/(M+K)`, each labelled with a percentage to one decimal. Under them, a third bar, "True damage share," greyed, showing `t`.
- Right, "What keeps you alive": a line plot of EHP (y-axis, from 0 to the maximum over the curve, rounded up) against armor share of budget `s = A/R` (x-axis, 0% to 100%). A filled dot at the current split, a hollow diamond at the optimum split, and a dashed horizontal line at the ceiling `HP / t` when `t > 0` and the ceiling fits on the axis. Under the plot, one stacked horizontal bar "Damage that reaches you, by type," with three segments whose widths are `(1 − t) w_p K/(A+K)`, `(1 − t) w_m K/(M+K)` and `t`, normalized to the bar's total `m`. Label the largest segment "weak link."
- Readout strip: `A`, `M`, `m` (3 decimals), `EHP` (integer, thousands separator), `optimal A / M` (1 decimal), `EHP at optimum`, and `% of optimum` for the current split.

**Controls.** All keyboard reachable, arrow keys step the sliders.
- Health `HP`: 500 to 5,000, step 100, default 2,000.
- Resist budget `R`: 0 to 400, step 10, default 200.
- Constant `K`: 10 to 500, step 5, default 100. Include a preset toggle "League-style (K = 100)" and "Dota-style physical (K = 16.67)", the second of which sets K to 1/0.06 = 16.667 (bypassing the slider step) and relabels the magic bar as a note that Dota's magic resistance is a percentage and is not modelled here.
- Physical share of mitigable damage `w_p`: 0% to 100%, step 1, default 50. `w_m = 1 − w_p`.
- True damage share `t`: 0% to 30%, step 1, default 0.
- Split slider, armor share `s`: 0% to 100%, step 1, default 100. `A = s × R`, `M = R − A`.
- Button "Jump to optimum."

**Formulas.**
- `m = (1 − t) × [w_p × K/(A + K) + w_m × K/(M + K)] + t`
- `EHP = HP / m`
- `S = √w_p + √w_m`
- Unconstrained optimum `A* = (2K + R) × √w_p / S − K`, then clamp `A*` to `[0, R]`, `M* = R − A*`.
- `EHP*` = EHP computed at the clamped optimum (do not use the closed form when clamped).
- Curve: evaluate EHP at `s = 0, 0.005, ..., 1` (201 points).

**Test values (HP = 2,000, K = 100, R = 200).**

| w_p | t | A / M | m | EHP | Optimum A / M | EHP at optimum |
|---|---|---|---|---|---|---|
| 50% | 0 | 200 / 0 | 0.6667 | 3,000 | 100.0 / 100.0 | 4,000 |
| 50% | 0 | 150 / 50 | 0.5333 | 3,750 | 100.0 / 100.0 | 4,000 |
| 80% | 0 | 200 / 0 | 0.4667 | 4,286 | 166.7 / 33.3 | 4,444 |
| 80% | 0 | 160 / 40 | 0.4505 | 4,439 | 166.7 / 33.3 | 4,444 |
| 80% | 0 | 100 / 100 | 0.5000 | 4,000 | 166.7 / 33.3 | 4,444 |
| 90% | 0 | 200 / 0 | 0.4000 | 5,000 | 200.0 / 0.0 (clamped exactly at boundary) | 5,000 |
| 95% | 0 | 200 / 0 | 0.3667 | 5,455 | 200.0 / 0.0 (clamped) | 5,455 |
| 50% | 10% | 100 / 100 | 0.5500 | 3,636 | 100.0 / 100.0 | 3,636 |

Extra check with the Dota-style preset (`K = 16.667`, HP 1,500, `R = 10`, `w_p = 100%`, all armor): `m = 16.667 / 26.667 = 0.625`, EHP = 2,400.

**Visual rules.** Use `templates/interactive-tokens.css` inline. Two colours for physical and magic that stay distinguishable for colour-blind viewers (differ in lightness, not only hue), grey for true damage. No game art or logos. All numbers selectable. No animation when `prefers-reduced-motion` is set.
