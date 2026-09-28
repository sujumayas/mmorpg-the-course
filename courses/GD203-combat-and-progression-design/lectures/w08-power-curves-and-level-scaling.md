# GD203 · Week 08 — Power curves and level scaling

**Why this matters:** A level number is a promise about power. Whether "five levels above you" means "slightly tougher" or "run" depends on the shape of your power curve, and whether levels mean anything at all depends on how enemies scale with the player.

**You will be able to:**
- Compute a character's power as offense times defense and use the power ratio to predict who wins a fight and how fast.
- Compare linear and exponential power curves by the power ratio of a fixed level gap, at any point in the game.
- Model fixed, full, banded and downscaled level scaling as a function from player level to enemy level, and compute the resulting power ratio.
- Critique a level-scaling scheme by predicting what it does to old content, grinding and the feeling of progress.

**Before class:** Schreiber & Romero, *Game Balance* (2021), the chapters on progression curves and on characters; Schreiber, *Game Balance Concepts*, level 7 ("Advancement, Progression and Pacing").

**Prerequisites from earlier courses:** MA101 week 4, [exponential growth](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w04-exponentials-and-the-xp-curve.md), and week 7, [caps and floors with piecewise functions](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w07-piecewise-caps-and-floors.md). GD102 weeks 3 and 4, positive and negative feedback loops ([GD102 syllabus](../../GD102-systems-design-and-game-mechanics/syllabus.md)). GD203 week 4, [time-to-kill](w04-time-to-kill-and-time-to-die.md), and week 7, [XP curves](w07-xp-curves.md).

**Interactive:** [Level gap](../examples/w08-level-gap.html) (built from the spec at the end of this lecture). Keep it open during sections 2 and 4.

---

## 1. Power as one number

Week 4 gave you time-to-kill. Use it to boil a fight down to a single number.

Say the player deals `a_p` damage per second and has `h_p` health. The enemy deals `a_e` and has `h_e`. Ignore mitigation for now, or fold it in by using effective HP from week 3.

```
Time for the player to kill the enemy:   TTK_p = h_e / a_p
Time for the enemy to kill the player:   TTK_e = h_p / a_e
```

The player wins if `TTK_p < TTK_e`. Divide one by the other:

```
R = TTK_e / TTK_p = (a_p × h_p) / (a_e × h_e)
```

Define **power** as `P = a × h`, offense times defense. Then `R = P_p / P_e`, the **power ratio**. If `R = 2`, the player survives twice as long as the fight takes, so they end it with about half their health left. If `R = 1`, it is a coin flip. If `R = 0.5`, the player loses and deals only half the enemy's health before dying.

Two properties make this definition useful.

- Offense and defense count equally. Doubling damage or doubling health doubles power. That matches how TTK works, and it is why the "glass cannon" and the "tank" can have the same power.
- Power multiplies. If each stat grows by a factor `g` per level, power grows by `g²` per level.

A **power curve** is `P(L)`, power as a function of level. Everything this week is about the shape of that curve and about the enemy's curve next to it.

## 2. Worked example: is five levels a big gap?

### The hook

In Pokémon, a level 10 Pokémon beats a level 5 one of the same species almost every time. A level 55 facing a level 50 is a much closer fight. Players feel this without doing any math. Early levels feel huge and late levels feel small.

In many MMOs the opposite is true. A monster five levels above you is dangerous at level 10 and just as dangerous at level 50. Same gap, same feeling.

Both games are internally consistent. They differ in one design decision, the shape of the power curve.

### The model

Compare two simple curves. In both, attack and health grow at the same rate.

```
Linear:        a(L) = 10 × L          h(L) = 100 × L              P(L) = 1,000 × L²
Exponential:   a(L) = 10 × g^(L−1)    h(L) = 100 × g^(L−1)        P(L) = 1,000 × g^(2(L−1))
```

- `L` is the character level.
- `g` is the per-level growth of each stat in the exponential curve. We use `g = 1.1`, so each stat grows 10% per level and power grows `1.1² = 1.21`, or 21%, per level.

Now ask the question from the hook. How much more powerful is a character `Δ` levels higher?

```
Linear:        P(L + Δ) / P(L) = ((L + Δ) / L)²
Exponential:   P(L + Δ) / P(L) = g^(2Δ)
```

The exponential ratio does not contain `L`. A five-level gap is worth `1.21⁵ = 2.59` times the power at level 1, level 20 or level 500. The linear ratio shrinks toward 1 as `L` grows.

### Numbers you can check

Power ratio of a character five levels above another (`Δ = 5`):

| Lower level `L` | Linear `((L+5)/L)²` | Exponential `1.21⁵` |
|---|---|---|
| 1 | 36.00 | 2.59 |
| 5 | 4.00 | 2.59 |
| 10 | 2.25 | 2.59 |
| 20 | 1.56 | 2.59 |
| 50 | 1.21 | 2.59 |

Verify one linear row with TTK directly. A level 20 player against a level 25 enemy: the player needs `h_e / a_p = 2,500 / 200 = 12.5` seconds and the enemy needs `h_p / a_e = 2,000 / 250 = 8` seconds. `R = 8 / 12.5 = 0.64`, which is `1 / 1.5625`. The table says the higher character has 1.56 times the power, so the check holds.

Another way to read the same curves is to ask how many levels it takes to double your power.

- Exponential: `log 2 / log 1.21 = 3.6` levels, always.
- Linear: solve `(L + d)² = 2L²`, giving `d = L × (√2 − 1) ≈ 0.41 L`. That is 2 levels at level 5, 4 at level 10, 8 at level 20 and 21 at level 50.

On a linear curve, a level becomes less meaningful as the game goes on. On an exponential curve, each level means the same thing forever.

Open the interactive. The left chart plots `P(L)` for both curves. With a linear y-axis the exponential curve looks like it explodes and the linear one looks tame, so you would guess the exponential game has the bigger late-game gaps. The right chart plots the ratio `P(L + Δ) / P(L)`. There the exponential line is flat and the linear line collapses toward 1. Drag `Δ` and `g` and watch which line moves.

### Cross-game recognition

**Pokémon (Generation III onward).** Stats come from a formula that is linear in level. For attack-type stats it is `floor((2 × Base + IV + floor(EV / 4)) × Level / 100) + 5`, then a nature multiplier. HP uses the same bracket plus `Level + 10`. Take a species with base 100, maximum IV 31, no EVs and a neutral nature.

| Level | Attack | HP | Power `Attack × HP` |
|---|---|---|---|
| 5 | 16 | 26 | 416 |
| 10 | 28 | 43 | 1,204 |
| 50 | 120 | 175 | 21,000 |
| 55 | 132 | 192 | 25,344 |

Level 10 over level 5 is `1,204 / 416 = 2.89` times the power. Level 55 over level 50 is `25,344 / 21,000 = 1.21`. The same five levels are worth less than half as much late in the game. The constants `+5` and `+Level + 10` make the early ratio smaller than the pure linear model's 4.0, but the shape is the same. This is our linear curve, and it is why a trainer with a five-level lead in the late game still needs good type matchups.

**Final Fantasy VIII (1999).** Enemy level is set from the party's average level, plus or minus a random modifier of one fifth of that average, capped at 100. The community guide at Jegged notes that enemy HP and strength grow faster per level than the party's do, so grinding levels can make fights harder. In our language, the enemy's power curve is steeper than the player's, and the scaling rule keeps `L_e` next to `L_p`. So `R` falls as you level unless you raise power by other means, which in FF8 is the junction system.

**World of Warcraft (2004 to 2014, before patch 6.0.2).** Blizzard said the game's numbers grew far larger than planned over its first decade, because power jumped by a large factor with every content tier. Warcraft Wiki records the symptom. The Throne of Thunder boss Ra-den had about 1.5 billion health, close to the 2,147,483,647 limit of a 32-bit signed integer. That is what a multiplicative power curve does when it runs for ten years. Patch 6.0.2 cut most numbers to about 4% of their old values and player health to about 8%. Blizzard cut health less on purpose, to weaken burst damage. So the squish kept the ratios between tiers, which is exactly the property of an exponential curve, and changed one ratio on purpose.

The recognition question works for any game. Compute power at two levels a fixed gap apart, once early and once late, and see whether the ratio is flat or shrinking.

### Eyes-open design judgment

- **Linear power** makes early levels dramatic and late levels gentle. Mixed-level play gets easier as the game goes on, which is good for a game where friends at different levels play together (Pokémon link battles, tabletop groups). The cost is that late levels feel weak, so you must add other rewards (new moves, new items, new areas) or players stop caring about the number.
- **Exponential power** keeps every level equally meaningful and keeps level gaps equally dangerous. That is the right tool when levels gate content, as in MMO zones. The costs are large. Numbers grow fast. At `g = 1.1` per stat, power at level 60 is `1.21⁵⁹ ≈ 77,000` times power at level 1. Old content becomes trivial, and two friends five levels apart cannot play together without a scaling system.
- A designer should decide deliberately what a gap of `Δ` levels should mean at the start and end of the game, and choose the curve that delivers it. You can also mix them, for example exponential up to a soft cap and linear after it.

## 3. Power per hour: linking week 7 and week 8

Week 7 gave you time per level, `t(n)`. This week gives you power gained per level, `P(L + 1) / P(L)`. Combine them and you get the player's felt rate of progress, power growth per hour of play.

With an exponential power curve, each level multiplies power by 1.21. If week 7's plan makes each level take 8% longer than the last, the power gained per hour falls by about 8% per level. That is fine and common. Progress slows while each level keeps its meaning.

With a linear power curve and the same time plan, progress per hour falls twice over. Each level takes longer and is worth less. In the week 7 plan the last level-up, 29 to 30, takes 3.3 hours and adds only `(30/29)² − 1 ≈ 7.0%` power. Players will call that a grind, and they will be right.

The practical rule is to plot both curves on one sheet. Lab 08 asks you to do exactly that.

## 4. Level scaling: choosing the enemy's curve

So far the enemy's level was given. In a real game you decide it. **Level scaling** is any rule that sets enemy level (or player effective level) from the player's level. Write it as a function `L_e = f(L_p)`, then the power ratio for the exponential curve is

```
R = g^(2 × (L_p − L_e))
```

and each scaling scheme is a different `f`. Four schemes cover most shipped games. The table uses `g² = 1.21`, a zone designed around level 10, and player levels from 5 to 30.

| Player level | Fixed, `L_e = 10` | Full, `L_e = L_p` | Band, `L_e = clamp(L_p, 8, 15)` | Downscale player to 13 |
|---|---|---|---|---|
| 5 | 0.39 | 1.00 | 0.56 | 0.39 |
| 10 | 1.00 | 1.00 | 1.00 | 1.00 |
| 15 | 2.59 | 1.00 | 1.00 | 1.77 |
| 20 | 6.73 | 1.00 | 2.59 | 1.77 |
| 30 | 45.26 | 1.00 | 17.45 | 1.77 |

Check the band column at level 20. `clamp(20, 8, 15) = 15`, so the gap is 5 levels and `R = 1.21⁵ = 2.59`.

**Fixed levels.** Each zone has fixed enemy levels. This is the classic MMO approach. Coming back to an old zone at level 30 gives `R = 45`, so enemies die in one hit and give nothing. The upside is a clear sense of progress. The downside is that most of the world becomes irrelevant, and friends of different levels cannot share it.

**Full scaling.** Enemies match you. The Elder Scrolls IV: Oblivion (2006) raised the level of many NPCs and creatures and changed which creatures appear as you level, according to UESP. `R` stays at 1 in the level model, so any change in real power has to come from something the level does not capture: gear, skill choices, player skill. If the player's level-ups add less power than the enemy's do, `R` falls as you level. That is the Final Fantasy VIII case above. Full scaling keeps the whole world relevant and removes the feeling of outgrowing anything.

**Banded scaling.** Enemies scale with you inside a range and stop at the ends. UESP describes Skyrim's (2011) dungeons as having level ranges, with the example of a dungeon ranged 15 to 25 spawning level 15 creatures for a level 10 player. In our function this is `clamp(L_p, min, max)`. Inside the band `R = 1`, so content stays challenging for a while. Above the band you out-level it and `R` climbs. Below it the content is hard, which tells the player to come back later.

**Downscaling the player.** Instead of raising the enemy, lower the player. The Guild Wars 2 wiki documents dynamic level adjustment in PvE. A character's effective level drops to the area's maximum level plus one, so a level 50 character in a level 1 to 10 area fights as level 11. Skills and gear are kept, so a high-level character is still stronger than a true level 11. In the table this is `R = 1.21^(min(L_p, 13) − 10)`, a plateau at 1.77 before counting the gear bonus. Old content stays playable with friends, and you still feel some advantage.

**Rescaling everything (the squish).** When an exponential curve runs for years, the numbers get too big to read. World of Warcraft patch 9.0.1 (October 2020, the Shadowlands pre-patch) compressed level 120 characters to level 50 and set the new cap at 60, along with an item level squish. In our model a squish divides every `P` by the same factor, so every ratio `R` is unchanged. It fixes readability and leaves balance alone. MMO307 week 5 covers stat squishes in depth ([MMO307 syllabus](../../MMO307-game-balance-ii-pvp-progression-and-endgame/syllabus.md)).

In the interactive's "Scaling" tab you pick a scheme and drag the player level. The chart shows `R` against player level for all four schemes at once, with the chosen one highlighted.

## 5. Choosing a scheme deliberately

Each scheme answers the same question differently: what should the player feel when they get stronger?

- Fixed levels say "you outgrew this." Good for a clear journey through a world. Bad for social play across levels and for making old content matter.
- Full scaling says "the world grows with you." Good for open worlds where the player can go anywhere in any order. Bad because levels stop meaning power, and the leveling system can punish the player for playing (the FF8 trap). If you use it, make sure the player's per-level gain is at least as large as the enemy's, and give the player power sources the enemy does not copy.
- Banded scaling says "each place has a range." It is a compromise that keeps both an order to the world and some freedom. The designer has to set two numbers per zone, and bad bands make zones feel either pointless or walled.
- Downscaling says "you can go back, and you are still a veteran." It needs careful math because gear and skills stay, and the retained advantage is exactly what you must tune.

A single test catches most problems. Plot `R` against player level for every zone. If a line sits near 1 for the entire game, the player never feels growth. If a line shoots past 10, that content is dead once the player passes it.

## In-class activity (25 minutes)

Work in groups of three. You are designing an open-world RPG, levels 1 to 40, with six regions. Players may visit regions in any order after level 10.

1. Choose a power curve (linear, exponential, or a mix) and state what a five-level gap should mean at level 10 and at level 40. Give the power ratio for each.
2. Choose a scaling scheme for the regions. For banded scaling, write the bands.
3. Use the interactive's Scaling tab or a spreadsheet to plot `R` against player level for two regions, one early and one late.
4. Mark on your plot one level where a player will say "this is too easy" and one where they will say "this is unfair." Propose one change to fix each.

Expected output is one plot per group, the numbers from step 1, and two proposed changes with the ratio before and after.

## Common misconceptions

- **"Exponential curves make late-game gaps bigger."** In absolute numbers, yes. In ratio, which is what decides fights, a fixed gap is exactly as large at every level.
- **"Linear stats mean linear power."** If attack and health both grow linearly, power grows as `L²`. And the ratio of a fixed gap still shrinks.
- **"Full level scaling means the game stays balanced."** It keeps `R` near 1 only if player and enemy gain power at the same rate per level. If enemies gain faster, leveling makes the game harder.
- **"A stat squish rebalances the game."** Dividing every power by the same factor changes no ratio. It changes readability. Any balance change in a squish comes from things changed at the same time.

## Check yourself

1. In a game where stats grow 8% per level each, how much more powerful is a character 10 levels higher? How many levels double power?
2. A game uses `a(L) = 20 + 5L` and `h(L) = 200 + 50L`. What is the power ratio of level 8 over level 4, and of level 44 over level 40?
3. A zone is band-scaled to levels 20 to 30 with power growing 21% per level. What is `R` for players at levels 15, 25 and 35?
4. A downscaling system sets the player to zone max plus 1 but keeps gear worth 30% extra power. A level 60 player enters a level 1 to 20 zone and fights a level 18 enemy. Using 21% per level, what is `R`?

<details>
<summary>Answers</summary>

1. Power grows `1.08² = 1.1664` per level. Ten levels: `1.1664^10 ≈ 4.66` times. Doubling: `log 2 / log 1.1664 ≈ 4.5` levels.
2. Both stats are proportional to `(4 + L)`, so power is proportional to `(4 + L)²`. Level 8 over 4: `(12/8)² = 2.25`. Level 44 over 40: `(48/44)² ≈ 1.19`.
3. Level 15: enemies clamp to 20, `R = 1.21^(−5) ≈ 0.39`. Level 25: inside the band, `R = 1`. Level 35: enemies clamp to 30, `R = 1.21^5 ≈ 2.59`.
4. Effective level is 21, three above the enemy, so `R = 1.21³ × 1.3 ≈ 1.77 × 1.3 ≈ 2.30`.

</details>

## Lab / assignment hook

**Lab 08, power curves and scaling bands** ([labs/lab08.md](../labs/lab08.md)). You extend your week 7 pacing sheet with player and enemy power curves, plot `R` for every zone of a small game under two scaling schemes, and recommend one.

## Sources

- Bulbapedia, "Stat" (Generation III onward), and Pokémon Wiki, "Statistics". Stat formulas `floor((2 × Base + IV + floor(EV/4)) × Level / 100) + 5` times nature, and HP `floor((2 × Base + IV + floor(EV/4)) × Level / 100) + Level + 10`. https://bulbapedia.bulbagarden.net/wiki/Stat and https://pokemon.fandom.com/wiki/Statistics
- Jegged.com, "Final Fantasy VIII Tips and Tricks: Character/Enemy Leveling" (original 1999 release and remaster). Enemy level from party average plus or minus one fifth, cap at 100, and the note that grinding can make battles harder. https://jegged.com/Games/Final-Fantasy-VIII/Tips-and-Tricks/Character-Enemy-Leveling.html
- UESP, "Oblivion:Leveling" (The Elder Scrolls IV: Oblivion, 2006). Opponent levels and creature types rise with player level, and loot quality is level-dependent. https://en.uesp.net/wiki/Oblivion:Leveling
- UESP, "Skyrim:Leveling" (The Elder Scrolls V: Skyrim, 2011). Dungeon level ranges and the 15 to 25 example. https://en.uesp.net/wiki/Skyrim:Leveling
- Guild Wars 2 Wiki, "Dynamic level adjustment" (current game). Effective level of area maximum plus one, retained skills and gear, WvW upscaling to 80. https://wiki.guildwars2.com/wiki/Dynamic_level_adjustment
- Warcraft Wiki, "Stat squish", and Blizzard Watch, "We finally know exactly what level your character will be in Shadowlands" (September 2020). Patch 9.0.1 level squish from 120 to 50, new cap 60. https://warcraft.wiki.gg/wiki/Stat_squish
- Warcraft Wiki, "Stat squish", section on patch 6.0.2 (Warlords of Draenor pre-patch, 2014). Developer reasoning about number growth, Ra-den's health near the 32-bit limit, reduction to about 4% (player health about 8%).
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press.
- Schreiber, I. (2010). *Game Balance Concepts*, level 7, "Advancement, Progression and Pacing" (online course). https://gamebalanceconcepts.wordpress.com/

## Interactive spec: examples/w08-level-gap.html

**The one insight.** On an exponential power curve a fixed level gap is worth the same at every level. On a linear curve the same gap shrinks toward nothing. The absolute-power chart suggests the opposite, so the two views must sit side by side.

**Tab 1, "Level gap".**
- Left chart, "Power `P(L)`". Two lines, linear and exponential, x = level 1 … Lmax (default 60), y = power. Toggle linear or log y-axis, default linear so the exponential line looks explosive.
- Right chart, "Power ratio of a character Δ levels higher, `P(L + Δ) / P(L)`". Same two series. y-axis log scale from 1 to 100, with a horizontal guide at 2 labelled "twice as strong".
- A shared vertical cursor. Hover or keyboard-step on either chart moves a cursor at level L on both charts, with a readout: L, P_lin(L), P_exp(L), ratio_lin, ratio_exp, and "levels to double power" for each curve at L.
- Controls: `Δ` slider 1 … 20, default 5. `g` (per-stat growth) slider 1.02 … 1.20, step 0.01, default 1.10. `Lmax` slider 20 … 100, default 60. Checkbox "Pokémon mode" that replaces the linear series with the Pokémon Gen III+ formulas (base 100, IV 31, EV 0, neutral nature), power = attack × HP.

**Formulas.**
- Linear: `a = 10L`, `h = 100L`, `P = a × h`.
- Exponential: `a = 10 × g^(L−1)`, `h = 100 × g^(L−1)`, `P = a × h`.
- Pokémon: `atk = floor(231 × L / 100) + 5`, `hp = floor(231 × L / 100) + L + 10`, `P = atk × hp`.
- Levels to double: linear `L × (√2 − 1)`, exponential `ln 2 / (2 ln g)`.

**Test values.**
- Δ = 5, g = 1.10: exponential ratio 2.594 at every L. Linear ratio 36.00 at L = 1, 4.00 at L = 5, 2.25 at L = 10, 1.5625 at L = 20, 1.21 at L = 50.
- Levels to double at g = 1.10: exponential 3.64. Linear 2.07 at L = 5, 4.14 at L = 10, 20.71 at L = 50.
- Pokémon mode: P(5) = 416, P(10) = 1,204, P(50) = 21,000, P(55) = 25,344. Ratios with Δ = 5: 2.894 at L = 5, 1.207 at L = 50.
- g = 1.10, P_exp(60) / P_exp(1) = 1.21^59 ≈ 7.7 × 10^4.

**Tab 2, "Scaling".**
- One chart, x = player level 1 … 40, y = power ratio R on a log axis (0.1 to 100) with a band shaded between 0.67 and 1.5 labelled "fair fight".
- Four series, one per scheme: Fixed (`L_e = Z`), Full (`L_e = L_p`), Band (`L_e = clamp(L_p, Bmin, Bmax)`), Downscale (`L_eff = min(L_p, Zmax + 1)`, enemy fixed at Z, R multiplied by a gear bonus factor).
- `R = g^(2 × (L_player_effective − L_e))` with the same `g` as tab 1.
- Controls: zone level Z (default 10), band min and max (default 8 and 15), zone max for downscaling (default 12), retained gear bonus (default 1.0, range 1.0 … 2.0), scheme highlight radio buttons, player level slider with readout of R for all four schemes.
- Test values with g = 1.10, Z = 10, band 8 to 15, zone max 12, gear 1.0: at player level 5, R = 0.386, 1, 0.564, 0.386. At 15: 2.594, 1, 1, 1.772. At 20: 6.727, 1, 2.594, 1.772. At 30: 45.26, 1, 17.45, 1.772.

**Accessibility.** Keyboard control of the cursor (arrow keys when a chart has focus), all readouts as text, colour plus line style (solid, dashed, dotted, dash-dot) to tell series apart, no animation under reduced motion.
