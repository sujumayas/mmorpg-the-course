# GD203 · Week 02 — Damage Formulas: Subtractive vs Divisive vs Multiplicative

**Why this matters:** The damage formula is the sentence your combat system says every time anything hits anything. Pick subtractive and you have quietly decided that weak enemies will one day stop mattering. Pick divisive and you have decided they never will. Most designers make this choice by copying the last game they played, and discover its consequences months later.

**You will be able to:**
- Write the three families of damage formula (subtractive, divisive, ratio) and compute the damage each one lets through for any attack and defense.
- Rewrite a shipped game's damage formula into a common "fraction that gets through" form and name its tuning constant.
- Predict which formula makes swarms of weak enemies harmless, and derive the hit size at which subtractive and divisive defense give the same result.
- Design an order of operations for a damage pipeline and show how changing the order changes the damage.

**Before class:** Schreiber & Romero, *Game Balance* (2021), chapter 10 (combat), first half; Schreiber, *Game Balance Concepts*, Level 2 ("Numeric Relationships") if you have not read it for week 1.

**Prerequisites from earlier courses:** rational functions and asymptotes, the `A/(A+K)` shape ([MA101 week 6](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w06-rational-functions-and-asymptotes.md)); piecewise functions, caps and floors ([MA101 week 7](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w07-piecewise-caps-and-floors.md)); additive and multiplicative modifiers from [GD203 week 1](w01-stats-as-design-language.md).

**Interactive:** [examples/w02-damage-models.html](../examples/w02-damage-models.html) (built from the spec at the end of this lecture). Keep it open during section 2.

---

## 1. What a damage formula decides

Every hit in a combat game passes through a **damage pipeline**, a sequence of steps that turns "the attacker swings" into "the defender loses this much health." A typical pipeline looks like this:

```
raw damage (weapon, spell power)
  -> attacker modifiers (week 1: additive pools, multiplicative bonuses)
  -> defense (this week: armor, defense, resistance)
  -> floors and caps (minimum damage, maximum damage)
  -> health loss
```

This week is about the defense step. The defender has a number, which we will call `A` for armor even when a game calls it Defense, Toughness or Resistance. The formula decides how that number reduces the incoming damage `D`. There are only a handful of shapes in common use, and each one makes a different promise to players.

To compare them fairly, always rewrite a formula into one form:

```
damage taken = D × f
```

`f` is the **fraction that gets through**. It is between 0 and 1 for ordinary defense. The **mitigation** is `1 − f`, the fraction stopped. When you read a new game's formula, your first job is to find `f` and ask what it depends on. If `f` depends on `D`, then the size of the hit changes how good armor is. That single question separates the three families.

### Family 1: subtractive

```
damage taken = max(0, D − A)
f = max(0, 1 − A/D)
```

The defender's armor is subtracted from each hit. This is the oldest and most readable formula. A player can do it in their head. Notice that `f` depends on `A/D`, the ratio of armor to hit size. Armor is strong against small hits and weak against big ones. When `A ≥ D`, the hit does nothing at all.

### Family 2: divisive

```
damage taken = D × K / (A + K)
f = K / (A + K)
```

Here `K` is a constant you choose. When `A = K`, `f = 1/2`, so **K is the armor that halves damage**. The key property is that `f` does not contain `D`. A 5-damage poke and a 5,000-damage slam are reduced by the same fraction. `f` also never reaches zero, however large `A` becomes.

### Family 3: ratio (multiplicative)

```
damage taken ∝ Atk / Def
```

Here both sides have a stat, and damage is proportional to the attacker's stat divided by the defender's. Doubling the defender's stat halves the damage. Doubling both leaves it unchanged. This is multiplicative in a precise sense: defense multiplies damage by `1/Def`, and the attacker's stat multiplies it by `Atk`. Because only the ratio matters, both stats can grow as large as you like without the formula breaking.

A fourth, simpler shape appears everywhere as a building block: **flat percent reduction**, `f = 1 − r`, where `r` is a percentage the item or buff states directly ("reduces damage taken by 20%"). Week 3 looks at what happens when percent reduction is stacked on a single stat. This week treats it as a layer in the pipeline (section 4).

## 2. Worked example: subtractive armor makes weak attacks useless; divisive never does

### The hook

In most Fire Emblem games, damage is the attacker's attack minus the defender's defense, and there is no minimum. A heavily armored knight whose defense exceeds an enemy's attack takes 0 damage from that enemy, every time. Put the knight in a corridor and a whole squad of weak soldiers cannot scratch it. The formula also hands the player the counter. Magic is checked against a different stat, resistance, so a unit built for high defense can still fall to spells.

That is a design choice, and it is a big one. Now imagine the same formula in a game where your character's armor keeps growing for 40 hours. At some point every early enemy, then every mid-game enemy, becomes a wall-bouncer. Which formula keeps a swarm of weak enemies dangerous, and which one retires them?

### The model

Put the two formulas side by side in "fraction that gets through" form:

```
Subtractive:  f_sub = max(0, 1 − A/D)
Divisive:     f_div = K / (A + K)
```

- `D` is the raw damage of one hit.
- `A` is the defender's armor.
- `K` is the divisive constant, the armor that halves damage. We use `K = 100` throughout this example.

Under subtractive, `f` falls as `A` rises and hits zero when `A = D`. Small hits reach zero first. Under divisive, `f` is the same for every hit size and approaches zero without ever getting there.

There is one more result you can derive from these two lines. For a given armor and hit, subtractive lets more damage through than divisive exactly when

```
D − A > D × K / (A + K)
(D − A)(A + K) > D × K
D × A − A² − A × K > 0
D > A + K
```

So **subtractive is softer than divisive against hits bigger than A + K, and harsher against hits smaller than A + K.** The two formulas are not a "strong" and a "weak" version of one idea. They disagree about which enemies armor should protect you from.

### Numbers you can check

Three attackers hit a defender. A swarm creature hits for 20, a soldier for 100, a boss for 500. The table shows the fraction of each hit that gets through as the defender's armor grows, with `K = 100` for divisive.

| Armor A | Swarm (20) sub | Soldier (100) sub | Boss (500) sub | Any hit, divisive |
|---|---|---|---|---|
| 0 | 100% | 100% | 100% | 100% |
| 10 | 50% | 90% | 98% | 90.9% |
| 20 | 0% | 80% | 96% | 83.3% |
| 50 | 0% | 50% | 90% | 66.7% |
| 100 | 0% | 0% | 80% | 50.0% |
| 200 | 0% | 0% | 60% | 33.3% |

Check two cells by hand. Subtractive, A = 50 against the boss: 500 − 50 = 450, and 450/500 = 90%. Divisive, A = 50: 100/150 = 66.7%, for every column.

Read down the columns. Under subtractive, the swarm is harmless at 20 armor and the soldier at 100. The boss has lost only 20% of its damage by then. Under divisive, all three lose the same share at every armor value. At 200 armor, a swarm hit still does 20 × 1/3 ≈ 6.7 damage.

Now the swarm comparison that makes the point concrete. Ten swarm creatures each hit once for 20, a total of 200 raw damage. One ogre hits once for 200. Same raw total.

| Defender armor | 10 swarm hits, subtractive | 1 ogre hit, subtractive | Either, divisive (K = 100) |
|---|---|---|---|
| 0 | 200 | 200 | 200 |
| 10 | 100 | 190 | 181.8 |
| 20 | 0 | 180 | 166.7 |
| 50 | 0 | 150 | 133.3 |

Under subtractive, 20 armor turns ten attackers into none. Under divisive, it doesn't matter how the 200 raw damage is split up. Check the crossover result too. At A = 50, `A + K = 150`. The ogre's 200-damage hit is bigger than 150, so subtractive should let more through than divisive, and it does (150 against 133.3). The swarm's 20-damage hits are smaller than 150, so subtractive is harsher (0 against 133.3).

### Move it yourself

Open the interactive. The main chart plots `f` (fraction that gets through, 0% to 100%) against armor from 0 to 300. Under subtractive, you see three lines, one per hit size, each falling in a straight line to zero at `A = D`. The swarm line hits the floor almost at once. Switch to divisive and the three lines collapse into one curve, because `f` does not depend on hit size.

The second panel shows the swarm and the ogre as two bars of damage actually taken, with the same raw total. Drag the armor slider. Under subtractive, the swarm bar vanishes at 20 while the ogre bar barely moves. Under divisive, the two bars stay exactly equal. Turn on "show crossover" to shade the region `D > A + K` where subtractive is the softer rule.

### The same idea in other games

**Fire Emblem** is our subtractive case. Its formula is `attack − defense` (or `attack − resistance` for magic), and in most games the minimum is 0. A few entries, Fire Emblem Gaiden and its remake Echoes: Shadows of Valentia among them, set a minimum of 1 instead. In our form that is `f = max(1/D, 1 − A/D)`, a floor that keeps weak attackers relevant, if only barely. The effect is that no unit in those games is ever completely safe.

**League of Legends** is the clean divisive case. The game's damage multiplier for non-negative armor is `100 / (100 + armor)`, which is our `f_div` with `K = 100`. A champion with 100 armor takes half damage from every physical hit, whether it comes from a minion or an enemy champion's ultimate.

**Dota 2** uses the same shape in a disguise. Since patch 7.27 (June 2020), physical damage is multiplied by `1 − 0.06 × A / (1 + 0.06 × |A|)`. For positive armor, simplify:

```
f = 1 − 0.06A / (1 + 0.06A) = 1 / (1 + 0.06A) = 16.67 / (A + 16.67)
```

That is `K / (A + K)` with `K = 1/0.06 ≈ 16.7`. Dota 2 armor values are small (single and low double digits), so the constant is small too. A hero with about 16.7 armor takes half physical damage. Before 7.27 the constants were different, which is why you must always cite the patch.

**Pokémon** uses the ratio family. From Generation V onward, the core of the damage formula is

```
damage = ((2 × Level / 5 + 2) × Power × Atk / Def) / 50 + 2
```

followed by a random factor and other multipliers. The `Atk / Def` term is the ratio. At level 50, a move with 80 power, and equal Attack and Defense of 100, the core comes to about 37. Double the Defense to 200 and it falls to about 20. Double both and it stays at 37. Look at it through the divisive lens: `K / (A + K)` with the total defense `A + K` written as one number is just `K / Def`. The ratio formula is a divisive formula where the attacker's own stat plays the role of K. It never reaches zero, and weak attackers stay relevant. (The `+ 2` at the end is a small built-in floor.)

Four games, three presentations, and one question sorts them all. Does `f` depend on the size of the hit? In Fire Emblem, yes, so armor retires weak enemies. In League of Legends, Dota 2 and Pokémon, no, so it never does.

### Design judgment

Neither formula is correct. Each one makes a promise, and you should choose the promise.

**Choose subtractive when you want thresholds.** In a tactics game like Fire Emblem, a heavily armored unit that ignores weak attackers is a puzzle. You must bring the right answer (magic) or go around. Subtractive formulas also read perfectly on a tooltip. The costs are real, though.

- Weak enemies become harmless once armor passes their damage, so whole tiers of content stop mattering. In a long progression, this happens again and again.
- To stay relevant, enemy damage must grow at least as fast as player armor. Every number in the game inflates.
- You need a floor (minimum 1, or a minimum percentage) if you want to rule out total immunity, and the floor then becomes the whole damage of every weak enemy.
- The value of armor depends on what the player is fighting. The same 20 armor is superb against swarms and nearly useless against a boss. That is only good if you want armor to have that identity.

**Choose divisive (or ratio) when you want scale-free defense.** Armor reduces every hit by the same share, so you can hand it out across 40 hours of progression without retiring content, and weak enemies in large numbers stay a threat. The costs:

- The tooltip is harder to read. Players see "50% reduction" and have to trust you.
- You lose the threshold fantasy. A divisive knight is never a wall.
- If you want armor to be better against some attacks than others, you must add a rule for it (Path of Exile 2 makes K depend on hit size, which you can read about in [MMO303 week 2](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w02-armor-and-damage-mitigation.md)).

The deciding question is concrete. **What should a weak enemy be able to do to a strong character?** If the answer is "nothing, and that's the reward for progressing," subtractive does it for free. If the answer is "a little, and many of them should still be a problem," you want divisive or ratio. Answer it before you write the formula, and write the answer in your design document so the next designer doesn't "simplify" it away.

### Check the model

1. With subtractive armor, a defender has 40 armor. Hits of 30, 80 and 400 arrive. What fraction of each gets through?
2. With divisive armor and `K = 100`, what armor makes a defender take one quarter of every hit?
3. With `K = 100` and `A = 60`, at what hit size do subtractive and divisive give the same damage? Check your answer by computing both.

Answers are in the Check yourself section at the end.

## 3. Floors, chip damage and hybrids

Pure subtractive formulas need a decision about the bottom. The common options:

- **Zero floor.** `max(0, D − A)`. True immunity is possible. Fire Emblem's default.
- **Flat floor.** `max(1, D − A)`. Every hit does something. Fire Emblem Gaiden's choice. The weakness is that "1 damage" means different things at different health scales. It is a real threat at 20 HP and invisible at 20,000.
- **Percentage floor.** `max(p × D, D − A)`. Every hit does at least a fixed share of its raw damage, say 10%. This keeps swarms relevant at any scale and turns subtractive into a hybrid, subtractive for hits near the armor value, flat-percent for small ones.

Check the percentage floor against the swarm table. With `p = 10%` and `A = 20`, each 20-damage swarm hit does `max(2, 0) = 2`, so ten hits do 20 instead of 0. The swarm is weak but not dead. The floor you pick decides how weak.

Designers call the damage that gets through a heavy defense **chip damage**. The floor is your chip-damage policy. If you want players to fear being surrounded even late in the game, you need chip damage. If you want late-game players to walk through early zones untouched, you don't.

## 4. Layers and order of operations

Real pipelines stack several defense steps: armor, then a shield buff, then a class passive. Two rules cover almost everything.

**Percent layers multiply.** A 30% reduction from a buff and a 20% reduction from a passive combine as

```
f = (1 − 0.30) × (1 − 0.20) = 0.70 × 0.80 = 0.56
```

That is 44% total reduction, not 50%. This is the multiplicative chain from week 1, applied to defense. It naturally prevents stacking to 100%, since no product of numbers above zero reaches zero.

**Order matters when you mix flat and percent.** Take a 100-damage hit, a flat reduction of 20 and a percent reduction of 50%.

```
flat first:     (100 − 20) × 0.5 = 40
percent first:  100 × 0.5 − 20   = 30
```

The same two defensive effects give 40 or 30 depending on order. Neither order is right, but your specification must choose one and your tooltips must agree with it. As a rule of thumb, applying flat reductions last makes them stronger against small hits (the swarm again). Applying them first makes them matter less. When players theorycraft your game, the order of operations is the first thing they will reverse-engineer, so publish it.

Attacker-side effects slot into the same pipeline. **Penetration** reduces the defender's armor before the formula reads it. Under subtractive, 10 penetration is worth exactly 10 damage per hit, until armor reaches zero. Under divisive, its value depends on how much armor the target has, which is a question for week 3.

## In-class activity (25 minutes)

Work in groups of three. You are designing the defense formula for a small action RPG. The player fights three enemy types for the whole game: rats (many, weak), guards (medium) and a boss at the end of each zone. Player armor grows from 0 at level 1 to 200 at level 20.

**Materials:** the interactive, a spreadsheet or paper.

1. (5 min) Write, in one sentence, what a level-20 player should experience when surrounded by ten level-1 rats. This is your design promise.
2. (10 min) Choose a formula and constants that deliver the promise. Use the interactive to test rat hits of 10, guard hits of 60 and boss hits of 400 at armor 0, 100 and 200. Fill in a 3 × 3 table of fraction-through values.
3. (5 min) Decide a floor policy (none, flat, percentage) and a position for your one percent-reduction buff in the pipeline. Compute one hit end to end.
4. (5 min) Trade tables with another group. Find a combination of armor and enemy type where their promise breaks.

**Expected output:** a one-sentence promise, a formula with constants, a 3 × 3 table, a written pipeline order, and one found break in another group's design.

## Common misconceptions

- **"Subtractive is simpler, so it's easier to balance."** It is easier to read and harder to balance, because the value of each armor point depends on the size of the hit it faces.
- **"Divisive armor has diminishing returns, so it's weaker."** Every armor point matters under divisive, and at no armor value does a weak enemy stop doing damage. Whether its returns diminish depends on what you measure, which is week 3's topic.
- **"30% and 20% reduction make 50%."** Percent layers multiply. They make 44%.
- **"Order of operations is a programmer's detail."** It changes damage. In the example, the same two effects gave 40 or 30. It belongs in the design spec.

## Check yourself

1. With subtractive armor, a defender has 40 armor. Hits of 30, 80 and 400 arrive. What fraction of each gets through?
2. With divisive armor and `K = 100`, what armor makes a defender take one quarter of every hit?
3. With `K = 100` and `A = 60`, at what hit size do subtractive and divisive give the same damage? Check your answer by computing both.
4. Rewrite `damage taken = D / (1 + A/250)` in the form `D × K / (A + K)`. What is K?
5. A designer adds a 10% floor to subtractive armor: `max(0.1 × D, D − A)`. At what armor does a 50-damage hit start doing floor damage? How much damage do eight such hits do against 80 armor?

<details>
<summary>Answers</summary>

1. 30: `max(0, 30 − 40) = 0`, so 0%. 80: 40/80 = 50%. 400: 360/400 = 90%.
2. `100 / (A + 100) = 1/4`, so `A + 100 = 400` and `A = 300`.
3. They are equal when `D = A + K = 160`. Subtractive: 160 − 60 = 100. Divisive: 160 × 100/160 = 100. Equal.
4. `D / (1 + A/250) = D × 250 / (250 + A)`, so `K = 250`.
5. The floor takes over when `D − A < 0.1 × D`, that is `50 − A < 5`, so at `A > 45`. At 80 armor each hit does `max(5, −30) = 5`, and eight hits do 40.

</details>

## Lab / assignment hook

**Lab 02: Three damage formulas in one sheet** ([labs/lab02.md](../labs/lab02.md)). You build a spreadsheet that computes damage taken for a table of attacks and armor values under subtractive, divisive and ratio formulas, plot fraction-through curves, and write a short recommendation for the in-class RPG. Week 3's lab extends the same sheet to effective HP.

## Sources

- Fire Emblem Wiki, "Damage": damage is attack minus defense or resistance; minimum 0 in most games; minimum 1 in Gaiden, Genealogy of the Holy War, Thracia 776 and Echoes: Shadows of Valentia.
- League of Legends Wiki, "Armor": damage multiplier `100 / (100 + armor)` for non-negative armor. Current as of 2025-2026 seasons.
- Dota 2 Wiki (Fandom), "Armor" and "Armor/Changelogs"; Valve, Dota 2 patch notes 7.27 (June 2020, dota2.com/patches/7.27): "Armor formula is now (Armor × 0.06 / (1 + Armor × 0.06))", giving the multiplier `1 − 0.06A / (1 + 0.06|A|)`.
- Bulbapedia, "Damage": core damage formula for Generation V onward, `((2 × Level / 5 + 2) × Power × A / D) / 50 + 2`, before random and other modifiers. Smogon University, "The Complete Damage Formula for Black & White" (smogon.com/bw/articles/bw_complete_damage_formula), gives the same base formula and the random factor of 85% to 100%. The worked numbers in this lecture ignore flooring and the random factor.
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press. Chapter 10.
- Schreiber, I. (2010). *Game Balance Concepts*, Level 2. gamebalanceconcepts.wordpress.com.

## Interactive spec: examples/w02-damage-models.html

**Purpose.** Signature worked example for GD203: subtractive armor makes weak attacks useless; divisive `A/(A+K)` never does.

**The one insight.** Under subtractive, the lines for different hit sizes fan out and the smallest hits drop to zero first. Under divisive, all hit sizes collapse onto one curve that never reaches zero. The swarm-versus-ogre bars make the consequence physical: same raw damage, and under subtractive the swarm vanishes.

**Layout.** Two linked views, side by side on desktop, stacked on mobile.

- **View 1, "Fraction that gets through."** Line chart. x axis armor `A` from 0 to 300. y axis `f` from 0% to 100%. Series:
  - Subtractive mode: three lines, `f = max(0, 1 − A/D)` for D = swarm hit, soldier hit, boss hit (defaults 20, 100, 500), each labeled with its D. Straight lines hitting zero at `A = D`.
  - Divisive mode: one curve `f = K/(A + K)`, labeled "every hit size." Draw faint copies of the subtractive lines for reference.
  - "Both" mode (default on first load): all four series.
  - A vertical marker at the current armor, with dots on each series and their values printed beside them (one decimal).
- **View 2, "Same raw damage, different outcome."** Two horizontal bar groups at the current armor. Group "Swarm": `N` hits of size `d` (defaults N = 10, d = 20). Group "Ogre": one hit of size `N × d`. Each group shows a subtractive bar and a divisive bar of damage actually taken, with the number printed (one decimal). Axis fixed at 0 to `N × d`.

**Controls.**
- Slider armor `A`: 0-300, step 1, default 20.
- Slider `K`: 10-400, step 5, default 100.
- Mode select: Subtractive, Divisive, Both.
- Number inputs for the three hit sizes (1-1000) and for swarm `N` (1-20) and `d` (1-200).
- Floor select for subtractive: None (default), Flat 1, 10% of D. Applies to all subtractive series and bars: `max(0, D − A)`, `max(1, D − A)`, `max(0.1D, D − A)`.
- Checkbox "Show crossover": shades the band on View 1 where, for the currently highlighted hit size, subtractive lets more through than divisive (`D > A + K`), and prints "Subtractive is softer for hits above A + K = ___".

**Exact test values (K = 100, floor none; must match the lecture tables).**
- A = 10: subtractive 50.0% / 90.0% / 98.0%; divisive 90.9%.
- A = 20: 0.0% / 80.0% / 96.0%; divisive 83.3%.
- A = 50: 0.0% / 50.0% / 90.0%; divisive 66.7%.
- A = 100: 0.0% / 0.0% / 80.0%; divisive 50.0%.
- A = 200: 0.0% / 0.0% / 60.0%; divisive 33.3%.
- View 2, N = 10, d = 20: A = 10 → swarm sub 100.0, ogre sub 190.0, divisive both 181.8. A = 20 → 0.0, 180.0, 166.7. A = 50 → 0.0, 150.0, 133.3.
- Floor 10% at A = 20: each swarm hit 2.0, swarm total 20.0.

**Accessibility and style.** Palette from `templates/interactive-tokens.css`. Hit sizes use three distinct tokens plus line style (solid, dashed, dotted) so they read in grayscale. All values printed as text. Keyboard access for every control; reduced motion disables bar transitions. No game names or art in the visual; the lecture carries the game references.
