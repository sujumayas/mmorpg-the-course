# GD203 · Week 04 — Time-to-kill (TTK) and time-to-die

**Why this matters:** Players do not feel damage numbers. They feel how many swings it takes and how many seconds pass before something falls over. If you tune damage and health without looking at hits-to-kill, you will ship upgrades that change nothing and small buffs that change everything.

**You will be able to:**
- Compute hits-to-kill and time-to-kill (TTK) for any weapon and target, including the off-by-one from the first hit.
- Predict which damage changes cross a breakpoint and which do nothing, and state the margin to the next breakpoint as a percentage.
- Derive enemy health from a target fight length, and place it inside a breakpoint step so small balance changes do not flip it.
- Compare time-to-kill with time-to-die to decide who wins a duel and how many decisions each side gets.

**Before class:** Schreiber & Romero, *Game Balance* (2021), the chapter on combat and the chapter on the math of time and pacing; Schreiber, *Game Balance Concepts*, level 3 (transitive relationships and cost curves). Skim the Minecraft Wiki pages "Sword" and "Zombie" (Java Edition).

**Prerequisites from earlier courses:** Expected value and damage per second from [MA102 week 4](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md). Feedback loops and pacing from GD102 [week 3](../../GD102-systems-design-and-game-mechanics/lectures/w03-positive-feedback-loops-snowballing.md) and [week 4](../../GD102-systems-design-and-game-mechanics/lectures/w04-negative-feedback-loops-rubber-banding.md). Mitigation and effective HP from [GD203 week 3](w03-mitigation-curves-and-effective-hp.md). You will meet effective HP again, in depth, in [MMO303 week 3](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w03-effective-hp-and-effective-dps.md).

**Interactive:** [examples/w04-breakpoint-staircase.html](../examples/w04-breakpoint-staircase.html) (specified at the end of this lecture). Keep it open during section 2.

---

## 1. Two clocks in every fight

Every fight runs two clocks at once.

**Time-to-kill (TTK)** is how long it takes you to bring a target from full health to zero. **Time-to-die (TTD)** is the same clock seen from the other side, how long the target takes to kill you. A duel is a race between the two. If your TTK is shorter than your TTD, you win. If it is longer, you lose. Everything else in combat design, from armor to healing to crowd control, is a way of speeding up one clock or slowing down the other.

In week 3 you learned to express survival as effective HP. This week you turn effective HP into seconds. Seconds are what the player experiences, and seconds are what you should write in your design document. "A trash mob should die in about 4 seconds for a player of the right level" is a design goal a whole team can test. "Trash mobs have 340 HP" is not, until someone does this week's arithmetic.

The first instinct is to compute TTK like this:

```
TTK ≈ H / DPS
```

where `H` is the target's health and `DPS` is damage per second. That is the smooth estimate. It is a fine first guess and it is wrong in a specific, predictable way whenever the number of hits is small. The rest of this lecture is about that way.

## 2. Worked example: breakpoints, or why the better sword kills no faster

### The hook

In Minecraft (Java Edition, after the 1.9 combat update), a diamond sword lists 7 attack damage and a netherite sword lists 8. Both swing at the same speed, 1.6 attacks per second, which the wiki gives as a 0.625-second cooldown between full-strength swings. On paper the netherite sword does 14% more damage per second.

Take both to a plain adult zombie. A zombie has 20 health points on every difficulty. Both swords kill it in exactly three swings. The upgrade that cost you a smithing template and a netherite ingot does nothing at all against the most common hostile mob in the game.

Now go the other way. An iron sword lists 6 damage, only one point less than diamond. It needs four swings. One point of damage, a 14% difference, costs you a full extra swing and 50% more time.

So a 14% upgrade can be worth 0% or worth 33%, depending on where you stand. Players notice this. They say an upgrade "doesn't feel better," or that some item is "a must-have." They are feeling breakpoints.

### The model

A **breakpoint** is a damage value at which the number of hits needed to kill a target drops by one. The model has one line for hits and one for time:

```
hits = ceil(H / d)
TTK  = (hits − 1) × Δ
```

- `H` is the target's health after any flat changes (buffs, shields).
- `d` is the damage one hit actually deals, after mitigation.
- `Δ` (delta) is the time between hits, the attack interval.
- `ceil` rounds up to the next whole number. You cannot deal 2.86 hits.

Why `hits − 1`? The first hit lands at time zero, the moment the fight starts. Three hits at 0.625-second spacing land at 0, 0.625 and 1.25 seconds, so the target dies at 1.25 seconds, not 1.875. Forgetting this off-by-one is the most common mistake in TTK spreadsheets. It matters most at exactly the hit counts players care about most, two to five.

Compare the two formulas side by side:

```
smooth estimate:   TTK ≈ H × Δ / d        (a curve)
actual:            TTK = (ceil(H/d) − 1) × Δ   (a staircase)
```

The smooth estimate slopes down steadily as damage rises. The actual TTK is flat, then drops a whole step, then stays flat again. Every damage value between two breakpoints gives the same TTK.

### Numbers you can check

Zombies also carry 2 points of natural armor. Minecraft's armor formula, at these hit sizes, removes 1.6% of each hit (the wiki gives the zombie's reduction as 1.6% to 8% depending on damage, and 1.6% is the value for every sword hit here). So each hit deals `listed damage × 0.984`. Here is the full sword line against a bare adult zombie, full-strength swings only, no enchantments, no jump-crits:

| Sword | Listed damage | Damage after zombie armor | Hits to kill | TTK (s) | Paper DPS | Smooth estimate (s) |
|---|---|---|---|---|---|---|
| Wooden | 4 | 3.936 | 6 | 3.125 | 6.4 | 3.18 |
| Stone | 5 | 4.920 | 5 | 2.500 | 8.0 | 2.54 |
| Iron | 6 | 5.904 | 4 | 1.875 | 9.6 | 2.12 |
| Diamond | 7 | 6.888 | 3 | 1.250 | 11.2 | 1.82 |
| Netherite | 8 | 7.872 | 3 | 1.250 | 12.8 | 1.59 |

Check two rows by hand. Diamond: `20 / 6.888 = 2.90`, round up to 3 hits, `(3 − 1) × 0.625 = 1.25` seconds. Netherite: `20 / 7.872 = 2.54`, also 3 hits, also 1.25 seconds.

Now look at the wooden and stone rows. Without the zombie's armor, a wooden sword would need `20 / 4 = 5` hits exactly, and a stone sword `20 / 5 = 4`. With the armor, five wooden hits deal `5 × 3.936 = 19.68`. The zombie survives with 0.32 health and needs a sixth swing. Two points of natural armor, which remove only 1.6% of each hit, cost the wooden and stone swords a full extra hit each. That adds 25% and 33% to their TTK, from a 1.6% mitigation. The model predicts this because 20 is a multiple of 4 and 5. When health is an exact multiple of damage, the target sits right on the edge of a step, and the smallest push tips it over.

This is the property to remember. **Near a breakpoint, tiny changes are huge. Between breakpoints, big changes are nothing.**

The smooth estimate column shows why DPS alone misleads you. It says netherite is 13% faster than diamond. It is 0% faster. It says iron is 17% slower than diamond. It is 50% slower.

### See it move

Open `w04-breakpoint-staircase.html`. The left panel plots TTK against damage per hit. You see the smooth curve `H × Δ / d` and, drawn over it, the staircase. The right panel shows the target's health bar being chopped into hits, with the leftover "overkill" from the last hit shaded.

Load the Minecraft preset and drag the damage slider from 6 to 8. The smooth curve slides down the whole way. The staircase drops once, at a listed damage of about 6.78 (6.67 after armor), and then sits flat. Watch the overkill shading on the right grow as you move from diamond to netherite. That growing sliver is the extra damage the netherite sword deals that does nothing. Now set mitigation to 0% and slide back to 5. Watch the stone sword's step land exactly on the edge.

### Cross-game recognition

The same staircase appears in every game that has discrete hits, written in different words.

**Team Fortress 2.** The rocket launcher's base damage is 90 per rocket. Class health values are 125 for the Scout, 150 for the Medic, 200 for the Soldier and 300 for the Heavy. Rewrite each matchup as `ceil(H / 90)`. A Scout or Medic needs 2 rockets, a Soldier 3, a Heavy 4. The Heavy's 300 health is 30 more than three base rockets deliver, so every Heavy fight at base damage takes one more rocket, which with the launcher's 0.8-second firing interval is 0.8 more seconds. Actual rocket damage changes with distance and a random spread, which is next week's and week 6's topic, but TF2 players still talk in rockets-to-kill because the staircase is what they feel.

**Pokémon (competitive play).** Competitive players describe every attack as an "OHKO," "2HKO," "3HKO" and so on, meaning it knocks out in one, two or three hits. Damage calculators used by the Smogon community report results as "guaranteed 2HKO" or "a percentage chance to 2HKO." Players then spend effort values (EVs, where 4 EVs add 1 stat point at level 100) to push an attack just past a breakpoint, or to push their own bulk just past the opponent's. That is `ceil(H / d)` turned into a build-planning language. A whole community has organized its theorycraft around the staircase.

**World of Warcraft (classic Naxxramas, patch 1.12 era).** The boss Patchwerk has about 3,850,000 health and a 7-minute enrage timer, after which the fight is lost. The designers set a maximum TTK of 420 seconds, which forces a minimum raid DPS of `3,850,000 / 420 ≈ 9,170`. The wiki quotes about 9,500 to leave a margin. Here the staircase disappears. When a target takes tens of thousands of hits, rounding up adds one hit out of tens of thousands, so the smooth estimate `H / DPS` is effectively exact.

That last case gives you a rule for when to worry. The error from ignoring the staircase is at most one hit, so the relative error is at most `1 / hits`. At 3 hits, the smooth estimate can be off by a third. At 300 hits, it is off by a third of a percent. **Breakpoints matter when hits-to-kill is small.** That means PvP, trash mobs, one-shot mechanics and early game. Long boss fights can use DPS directly.

### Design judgment

Breakpoints are not a bug. They are a property of discrete hits, and you get to choose what they do.

- **Pick the hit counts first.** Decide how many hits each important matchup should take ("a starter weapon kills a starter enemy in 3 hits") and then choose numbers. Tuning numbers first and discovering the hit counts later is how you get the netherite problem.
- **Avoid accidental multiples.** Health values like 20, 60 or 100 divide evenly by many common damage numbers, which puts targets on the edge of steps. Unless you want a sharp breakpoint, pick health in the middle of a step (section 4 shows how).
- **Use breakpoints on purpose.** A clear breakpoint is a goal players can chase ("get 10% more damage and you 2-shot Scouts"). That can be a good reason to buy an item or pick a talent. The trade-off is that items just below the breakpoint feel worthless and items just above feel mandatory.
- **Blur them when you want smoothness.** Random damage ranges, damage over time and large hit counts all soften the staircase. Each has its own cost, covered in weeks 5 and 6.
- **Show the player.** If breakpoints matter, give players a way to see them. Hits-to-kill readouts, damage numbers and health bars with tick marks all help. A tooltip showing DPS alone hides the one thing that decides the fight.

## 3. Time-to-die and the race

Turn the model around. Your TTD against an enemy uses your health, their damage after your mitigation, and their attack interval:

```
TTD = (ceil(H_you / d_enemy) − 1) × Δ_enemy
```

A duel ends when the first clock runs out. With discrete hits, there is a subtlety the smooth view hides entirely. If both sides need three hits and swing at the same interval, whoever swings first wins, every time. The first strike is worth a full interval. This is why stealth openers, ambushes and "attack of opportunity" rules carry so much weight in games with low hit counts. In a smooth-DPS world, striking first is worth a fraction of a second. In a staircase world, it can decide the fight.

A useful single number for an encounter is the **safety ratio**:

```
R = TTD / TTK
```

- `R` well above 1 means you win comfortably and can make mistakes. A player fighting a weak mob might have `R = 10`.
- `R` near 1 means the fight is a coin flip. That is fine for an arena duel and bad for a quest mob.
- `R` below 1 means you lose unless something changes one of the clocks, such as healing, a stun, or a potion.

Designers use `R` to set difficulty bands. A trash mob might target `R` between 4 and 8, so a player who plays badly still wins. An elite might target `R` around 2. A boss has `R` well below 1 for a single player, which is why bosses are designed for groups, where healers slow down the TTD clock and many damage dealers speed up the TTK clock.

The safety ratio also shows why healing and damage trade off. Doubling your health doubles `TTD` and `R`. Doubling your damage halves `TTK` and also doubles `R`. In the smooth view these are equal. In the staircase view they are not, because either change may or may not cross a breakpoint. Check both before you decide which one to give a class.

## 4. Designing from a target TTK

Most of the time you do not start with numbers. You start with a feel. "A level-appropriate trash mob should die in about 4 seconds." Here is the method that turns a feel into health values.

**Step 1. Fix the player's hit.** Say the player's weapon deals `d = 12` damage every `Δ = 0.8` seconds, for 15 paper DPS.

**Step 2. Convert the target TTK to hits.** With the first hit at time zero, `TTK = (hits − 1) × Δ`. For 4 seconds, `hits = 4 / 0.8 + 1 = 6`.

**Step 3. Find the step.** Six hits means `5 × 12 < H ≤ 6 × 12`, so `60 < H ≤ 72`. Any health in that range gives exactly 4.0 seconds.

Notice what the naive formula would have given you. `H = DPS × TTK = 15 × 4 = 60`. At 60 health, the mob dies in 5 hits and 3.2 seconds, 20% faster than you wanted. It also sits exactly on the edge of the step, so any damage buff of any size will not change it, and any damage nerf of any size will add a hit.

**Step 4. Center it.** Pick health in the middle of the step, say `H = 66`. Now compute the margin. The mob stays at 6 hits as long as `66 / d` rounds up to 6, which means `66 / 6 ≤ d < 66 / 5`, so `11 ≤ d < 13.2`. Player damage can drop 8.3% or rise 9.9% before the hit count changes. That margin is your tuning room. A patch that adds 5% player damage will not silently make every trash mob die one hit faster.

**Step 5. Check the other weapons.** If the game has several weapons, repeat for each. You will often find there is no single health value that sits centered for all of them. Then you choose which weapon's feel matters most at this point in the game, and accept that the others land nearer an edge. That is a design decision. Write it down.

The general rule for margin is this. For a target at `n` hits with health `H`, damage can range from `H / n` up to just under `H / (n − 1)`. Your job is to know where the typical player's damage sits in that range.

## 5. How long should a fight be?

TTK also sets how many decisions a fight contains.

Divide TTK by the time between meaningful player choices and you get a rough decision count. World of Warcraft uses a base global cooldown (GCD) of 1.5 seconds for most abilities in current retail, which haste can shorten to a floor of 0.75 seconds. A 3-second fight gives a player about two ability choices. The 420-second Patchwerk fight gives about 280.

Both are valid designs, for different purposes.

- **Short TTK (under about 3 decisions)** makes fights about positioning, target choice and who acts first. The fight is decided before it starts, by the choices that set it up. Many shooters live here. The risk is that the victim gets no decisions at all, and dying without a chance to respond feels unfair.
- **Medium TTK (5-20 decisions)** leaves room for reactions. The target can notice danger, use a defensive ability, or retreat. Most RPG trash and PvP brackets aim here.
- **Long TTK (dozens to hundreds of decisions)** turns a fight into a test of sustained execution and resource management. Mistakes are recoverable, but the fight can become repetitive unless it changes phase.

When you set a TTK target, also compute its partner, the TTD. If a player's TTD against an enemy is shorter than the time to recognize and respond to the threat, no defensive ability you design will ever get used. It will look good on the tooltip and be dead in practice.

## In-class activity (25 minutes)

Pairs. Each pair gets this starting kit.

| Weapon | Damage per hit | Interval (s) |
|---|---|---|
| Dagger | 9 | 0.5 |
| Sword | 16 | 0.8 |
| Hammer | 40 | 2.0 |

Paper DPS is 18, 20 and 20.

1. Set health for three enemies (rat, bandit, ogre) with target TTK for the sword of 0.8, 4.0 and 12.0 seconds. Use the method in section 4 and center each health value in its step. Record the damage margin for the sword.
2. Compute hits-to-kill and TTK for the dagger and hammer against each enemy. Mark any matchup where a weapon's TTK differs from the sword's by more than 25%.
3. A designer proposes a patch that gives the hammer +10% damage. For each enemy, say whether the hammer's TTK changes. Explain in one sentence why the answer differs by enemy.
4. Swap sheets with another pair. Find one enemy whose health sits within 5% of a breakpoint for any weapon.

Expected output: a filled 3 × 3 hits-to-kill table, three health values with margins, and a two-line recommendation on the hammer patch.

## Common misconceptions

- **"+10% damage means 10% faster kills."** Only when hits-to-kill is large. At low hit counts, +10% damage changes TTK by either 0% or a full step. Always recompute `ceil(H / d)`.
- **"TTK is hits × interval."** The first hit lands at time zero, so TTK is `(hits − 1) × interval`. For a 2-hit kill the naive formula doubles the real TTK.
- **"DPS decides who wins."** DPS predicts TTK only when many hits are needed. In short fights, hits-to-kill and who strikes first decide the winner.
- **"Breakpoints are a balance mistake to remove."** They are unavoidable with discrete hits. You choose whether they are sharp and deliberate or blurred, and you should place them on purpose.

## Check yourself

1. A weapon deals 14 damage every 0.5 seconds against a 100-health target with no mitigation. How many hits, and what is the TTK? What is the smallest whole-number damage per hit that removes one hit?
2. A raid boss has 2,000,000 health and a 5-minute enrage. What minimum raid DPS does that imply? Why can you ignore breakpoints here?
3. In the Minecraft model, what listed damage would a weapon need to kill a bare adult zombie in two hits, given the 1.6% armor reduction? Would the netherite axe (listed damage 10) do it?
4. You want an enemy to die in exactly 3 hits from a 25-damage weapon, and to stay at 3 hits even if player damage varies by ±10%. What health range works?

<details>
<summary>Answers</summary>

1. `100 / 14 = 7.14`, so 8 hits. TTK `= (8 − 1) × 0.5 = 3.5` seconds. For 7 hits you need `d ≥ 100 / 7 = 14.29`, so 15 damage. That is a 7% damage increase buying a 14% TTK cut (3.5 to 3.0 seconds).
2. `2,000,000 / 300 ≈ 6,667` DPS. The fight takes thousands of hits, so rounding up adds at most one hit, a relative error well under 1%.
3. Two hits need `2 × d × 0.984 ≥ 20`, so `d ≥ 10.16`. The netherite axe's 10 becomes 9.84 after armor. Two hits deal 19.68, and the zombie survives with 0.32 health. It needs three hits.
4. Damage ranges from 22.5 to 27.5. Three hits must kill at the low end, `H ≤ 3 × 22.5 = 67.5`. Two hits must fail at the high end, `H > 2 × 27.5 = 55`. So health from 56 to 67 works. The center, about 61, is safest.

</details>

## Lab / assignment hook

**[Lab 04: The breakpoint table](../labs/lab04.md).** Build a hits-to-kill matrix for a weapon set and an enemy roster, flag every matchup within 5% of a breakpoint, then retune enemy health so each sits centered in its step. You will reuse the sheet in weeks 5, 6 and 10.

## Sources

- Minecraft Wiki, "Sword" (Java Edition, 1.9 combat update onward, checked for the 1.21 era): listed attack damage 4 / 5 / 6 / 7 / 8 for wooden / stone / iron / diamond / netherite swords; attack speed 1.6, given as a 0.625-second cooldown; critical hits deal 1.5× base. https://minecraft.wiki/w/Sword
- Minecraft Wiki, "Zombie" (Java Edition): 20 health on every difficulty; 2 points of natural armor giving 1.6% to 8% reduction from most sources. https://minecraft.wiki/w/Zombie
- Minecraft Wiki, "Armor" (Java Edition): damage-reduction formula `damage × (1 − min(20, max(armor / 5, armor − 4 × damage / (min(toughness, 20) + 8))) / 25)`, with a breaking point of `armor × (toughness + 8) / 5` damage. With armor 2 and toughness 0, any hit above 3.2 damage is reduced by exactly 1.6%. https://minecraft.wiki/w/Armor
- Official TF2 Wiki, "Rocket Launcher": base damage 90, attack interval 0.8 s, clip of 4. https://wiki.teamfortress.com/wiki/Rocket_Launcher
- Official TF2 Wiki, "Health": class base health (Scout 125, Medic 150, Soldier 200, Heavy 300). https://wiki.teamfortress.com/wiki/Health
- Smogon Forums, "Pokémon Damage Calculator Tutorial": OHKO / 2HKO terminology, KO-chance reporting, and 4 EVs per stat point. https://www.smogon.com/forums/threads/pok%C3%A9mon-damage-calculator-tutorial.3700836/
- Warcraft Wiki, "Patchwerk (Classic)" (40-player Naxxramas, patch 1.12): about 3,850,000 health, 7-minute enrage, about 9,500 raid DPS needed. https://warcraft.wiki.gg/wiki/Patchwerk_(Classic)
- Warcraft Wiki, "Cooldown" and "Haste" (retail era): base global cooldown 1.5 s, reducible by haste to 0.75 s. https://warcraft.wiki.gg/wiki/Cooldown
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press.
- Schreiber, I. (2010). *Game Balance Concepts*, level 3. https://gamebalanceconcepts.wordpress.com/

## Interactive spec: examples/w04-breakpoint-staircase.html

**The one insight the visual must make obvious:** damage changes TTK in steps, not smoothly. Between breakpoints, extra damage only grows the wasted overkill. Near a breakpoint, a tiny change moves TTK by a whole interval.

**Layout.** Two linked panels, side by side on desktop, stacked on mobile (left panel first).

**Left panel: "TTK vs damage per hit."**
- x axis: damage per hit before mitigation, `d_listed`, from `max(1, floor(0.25 × d_default))` to `3 × d_default` of the active preset (for the Minecraft preset, `max(1, floor(1.75)) = 1` to 21).
- y axis: TTK in seconds, from 0 to the TTK at the left edge.
- Series 1 (ochre, thin dashed): smooth estimate `TTK_smooth = H × Δ / d_eff`, where `d_eff = d_listed × (1 − m)`.
- Series 2 (blood red, thick, stepped): `TTK = (ceil(H / d_eff) − 1) × Δ`. Draw vertical risers at every breakpoint `d_listed = H / (k × (1 − m))` for integers k.
- A vertical cursor at the current `d_listed`, with a dot on each series.
- Label each flat step with its hit count ("3 hits").
- Guard `ceil` against floating error: use `Math.ceil(H / d_eff − 1e-9)`.

**Right panel: "The health bar, chopped into hits."**
- A horizontal bar of length H. Mark each hit as a segment of width `d_eff`, alternating two tints of blood red, numbered 1..hits. The final segment is clipped at H. Draw the part of the last hit beyond H as a hatched ochre "overkill" block outside the bar.
- Under the bar, a timeline from 0 to TTK with a tick at each hit time `0, Δ, 2Δ, ...`.

**Controls (all keyboard accessible, each with a numeric input next to the slider).**
- Damage per hit (listed): slider, step 0.01.
- Target health H: 1 to 5,000,000 (log slider), default from preset.
- Mitigation m: 0% to 50%, step 0.1%.
- Attack interval Δ: 0.1 to 3.0 s, step 0.005.
- Preset buttons:
  - "Minecraft zombie" (H 20, m 1.6%, Δ 0.625, d 7), with quick-pick chips for wooden 4, stone 5, iron 6, diamond 7, netherite 8.
  - "TF2 rocket" (d 90, m 0, Δ 0.8), with target chips Scout 125, Medic 150, Soldier 200, Heavy 300.
  - "Raid boss" (H 3,850,000, d 3,000, Δ 1.5, m 0). This shows the staircase shrinking into the smooth curve.

**Readouts (exact numbers, copyable):** effective damage per hit (3 decimals), hits to kill, TTK (3 decimals), smooth estimate (3 decimals), gap between them as %, overkill (HP), "damage needed for one fewer hit" `H / ((hits − 1)(1 − m))` and the % increase from current, and "damage at which you need one more hit" `H / (hits × (1 − m))` and the % decrease from current. When hits = 1, show "already one-hit" for the first.

**Test values (must match exactly):**
| Preset / input | Hits | TTK (s) | Smooth (s) | Overkill |
|---|---|---|---|---|
| Minecraft, d 4 | 6 | 3.125 | 3.176 | 3.616 |
| Minecraft, d 5 | 5 | 2.500 | 2.541 | 4.600 |
| Minecraft, d 6 | 4 | 1.875 | 2.117 | 3.616 |
| Minecraft, d 7 | 3 | 1.250 | 1.815 | 0.664 |
| Minecraft, d 8 | 3 | 1.250 | 1.588 | 3.616 |
| Minecraft, d 10 | 3 | 1.250 | 1.270 | 9.520 |
| Minecraft, d 5, m 0 | 4 | 1.875 | 2.500 | 0.000 |
| TF2, Heavy 300 | 4 | 2.400 | 2.667 | 60 |
| TF2, Scout 125 | 2 | 0.800 | 1.111 | 55 |
| H 100, d 14, m 0, Δ 0.5 | 8 | 3.500 | 3.571 | 12 |

The Minecraft, d 5, m 0 row is the ceil-guard test: `20 / 5` is exactly 4, and a missing guard can round floating error up to 5 hits. The Minecraft d 10 row uses Δ 0.625 (sword speed). It checks the two-hit near miss from Check yourself question 3, not the axe's real swing speed.

**First screen:** Minecraft preset at d 7 with the netherite chip (d 8) visibly highlighted as "same TTK." No instructions above the fold beyond a one-line caption: "Diamond and netherite: 14% more damage, same three swings."

**Style:** program palette from `templates/interactive-tokens.css`. Damage in blood red, overkill and smooth estimate in ochre, mitigation readout in steel. No game art or logos. Respect `prefers-reduced-motion` (no animated transitions of the bar when set).
