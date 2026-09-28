# GD203 · Week 13 — Difficulty Modes and Scaling

**Why this matters:** Every difficulty menu you have ever used is a small set of multipliers on the time-to-kill and time-to-die numbers you built earlier in this course. If you know which multiplier moves which number, you can make a hard mode that feels tense instead of tedious, and a level-scaling system that keeps the world dangerous without erasing the player's growth.

**You will be able to:**
- Compute a fight's safety ratio (time-to-die divided by time-to-kill) and its health cost under any set of difficulty multipliers.
- Rewrite a shipped game's difficulty settings as player-damage, enemy-damage and enemy-health multipliers, and predict how each setting changes fight length.
- Derive how much of the player's growth survives a level-scaling rule, using a single scaling exponent.
- Design a difficulty ladder that separates "more dangerous" from "longer" and justify each lever you pull.

**Before class:** Schreiber & Romero, *Game Balance* (2021), the chapter "Progression in PvE Games" (the sections on difficulty curves and pacing). Schreiber, *Game Balance Concepts*, Level 7, "Advancement, Progression and Pacing" (2010, free online).

**Prerequisites from earlier courses:** GD203 [week 4, time-to-kill and time-to-die](w04-time-to-kill-and-time-to-die.md) (the safety ratio), [week 8, power curves and level scaling](w08-power-curves-and-level-scaling.md) (power ratio and scaling schemes) and [week 10, enemy design by the numbers](w10-enemy-design-by-the-numbers.md) (health cost of an encounter). UX201 week 3 (flow and difficulty), in the [UX201 syllabus](../../UX201-game-ux-and-player-psychology/syllabus.md). The effective-HP idea from [MMO303 week 2](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w02-armor-and-damage-mitigation.md) is used once in section 3.

**Interactive:** [Difficulty ladder](../examples/w13-difficulty-ladder.html). Keep it open during section 2.

---

## 1. What a difficulty setting changes

Pick up any single-player RPG and open its options menu. You will find a word ladder, something like Easy, Normal, Hard, Very Hard. The words promise a feeling. Underneath, the game changes numbers, and in most action RPGs the numbers it changes are few. Enemy health, enemy damage, player damage, sometimes the count of enemies, sometimes the resources you find.

In [week 4](w04-time-to-kill-and-time-to-die.md) you met two times that describe any one-on-one fight.

- **Time-to-kill (TTK)** is how long you need to bring the enemy to zero health.
- **Time-to-die (TTD)** is how long the enemy needs to bring you to zero health.

Neither number alone tells you whether a fight is hard. A 60-second TTK is a long fight, and it is only dangerous if your TTD is shorter than that. Week 4 combined them into one number, the **safety ratio**, time-to-die divided by time-to-kill.

```
R = TTD / TTK
```

A safety ratio of 3 means the enemy would need three times as long to kill you as you need to kill it. You win comfortably. A safety ratio of 1 is a coin flip if both sides just trade blows. A safety ratio below 1 means you lose a straight fight and must change one of the clocks by blocking, healing, kiting or using a potion.

Safety ratio has a second reading that players feel directly. If you win the fight, how much of your health bar did it cost? You spent TTK seconds taking damage at a rate that would empty your bar in TTD seconds, so:

```
health cost per fight = TTK / TTD = 1 / R
```

This is the same health cost you used to price encounters in [week 10](w10-enemy-design-by-the-numbers.md).

At safety ratio 3, each fight costs a third of your health. At safety ratio 12, it costs about 8%. At safety ratio 0.25, it would cost four full health bars, so you cannot win it by trading hits.

This is the quantity that difficulty modes move. The rest of the lecture shows how, and why the same menu entry can move it by far more than its label suggests.

### Two things a player feels

Keep two numbers apart for the rest of the session.

1. **Danger** is the safety ratio, or equivalently the health cost per fight. It decides how many mistakes you can afford.
2. **Duration** is the fight length, which for a fight you win is the TTK. It decides how long you spend doing the same thing.

A good hard mode usually raises danger. A bad hard mode often raises duration by accident. Players have a word for the second one, "damage sponge," and it is rarely a compliment.

## 2. Worked example: the Skyrim ladder

### The hook

The Elder Scrolls V: Skyrim has six difficulty levels. On the hardest, Legendary, the player takes three times normal damage. It sounds like Legendary is three times harder than Adept, the default. Players who try it report something different. Fights feel far more than three times as dangerous, and they also take much longer. Both observations come out of the same two multipliers.

### The model

Name the multipliers a difficulty setting can apply.

- `p` is the player damage multiplier (how much of your normal damage lands on enemies).
- `e` is the enemy damage multiplier (how much of the enemy's normal damage lands on you).
- `h` is the enemy health multiplier.

Start from a base fight on the default setting with time-to-kill `TTK₀` and time-to-die `TTD₀`, so base safety ratio `R₀ = TTD₀ / TTK₀`. Your damage per second goes up by `p` and the enemy's health by `h`, so TTK scales by `h / p`. The enemy's damage per second goes up by `e`, so TTD scales by `1 / e`. Put them together:

```
TTK = TTK₀ × h / p
TTD = TTD₀ / e
R   = R₀ × p / (h × e)
fight length = TTK₀ × h / p
```

Read the safety ratio line slowly. Danger depends on the *product* of the enemy-side multipliers divided by your own multiplier. Fight length depends only on `h / p`. The enemy damage multiplier `e` changes danger without touching duration. The player damage multiplier `p` changes both.

This is a model, and it leaves things out on purpose. It ignores healing, blocking, dodging, and every tactic a real player uses. That is fine. We want to know what the multipliers do before the player responds to them.

### Numbers you can check

The Unofficial Elder Scrolls Pages list Skyrim's multipliers as follows (Legendary was added in patch 1.9). Skyrim changes damage on both sides and leaves enemy health alone, so `h = 1`. Take a base fight on Adept against a bandit that you kill in 10 seconds and that would kill you in 30 seconds, so `R₀ = 3`.

| Setting | p (your damage) | e (damage to you) | TTK (s) | TTD (s) | Safety ratio R | Health cost per fight | Ratio vs Adept |
|---|---|---|---|---|---|---|---|
| Novice | 2 | 0.5 | 5.0 | 60 | 12 | 8.3% | ×4 |
| Apprentice | 1.5 | 0.75 | 6.7 | 40 | 6 | 16.7% | ×2 |
| Adept | 1 | 1 | 10.0 | 30 | 3 | 33.3% | ×1 |
| Expert | 0.75 | 1.5 | 13.3 | 20 | 1.5 | 66.7% | ×½ |
| Master | 0.5 | 2 | 20.0 | 15 | 0.75 | 133% | ×¼ |
| Legendary | 0.25 | 3 | 40.0 | 10 | 0.25 | 400% | ×1/12 |

Check one row by hand. On Master, `R = 3 × 0.5 / (1 × 2) = 0.75`. The fight length is `10 / 0.5 = 20` seconds. The health cost is `1 / 0.75 = 133%`, so a Master bandit kills you about three quarters of the way through a straight trade.

Three things jump out.

**The ladder is geometric.** From Novice to Master, each step halves the safety ratio exactly. The designers (or at least the numbers) built a ladder of equal ratios, which is the right shape for a quantity players feel as "how many mistakes can I make." A ladder of equal differences would feel lopsided, with huge jumps at the easy end and tiny ones at the hard end.

**Legendary breaks the pattern.** The step from Master to Legendary divides safety ratio by 3, not 2. Legendary is 12 times as dangerous as Adept and 48 times as dangerous as Novice. The menu word "Legendary" and the tooltip idea "take 3× damage" both undersell it, because the player damage cut compounds with the enemy damage boost.

**Hard modes are also long modes.** Because `p` falls as difficulty rises, every step up makes fights longer. Legendary fights take 40 seconds where Adept fights take 10. Half of Legendary's difficulty comes from a knob that makes fights four times longer. That is the damage-sponge complaint, explained by one column.

### A visual you can move

Open the interactive. The left panel shows what the menu shows you, a bar for each multiplier on a plain linear scale. Legendary's damage-taken bar is three times as tall as Adept's, and it looks like a moderate change.

The right panel plots each setting as a point. The horizontal axis is fight length. The vertical axis is health cost per fight, on a log scale. Dotted lines mark constant safety ratio. The six Skyrim points climb up and to the right. Drag the `p` slider and watch a point move diagonally, because player damage changes danger and duration together. Drag the `e` slider and the point moves straight up, because enemy damage changes only danger. Now try to reproduce Legendary's danger with `p = 1`. You need `e = 12`, and the fight stays at 10 seconds. Same safety ratio, a quarter of the duration. Whether that is better is the design question in section 5.

### Cross-game recognition

The skill here is rewriting any game's difficulty settings into `(p, e, h)` and reading off the two consequences. Here are three more games.

**Doom (1993).** On the easiest skill, "I'm Too Young to Die," the player takes half damage and ammo pickups are doubled. In our terms, `e = 0.5`, `p = 1`, `h = 1`. Safety ratio doubles and fight length does not change at all. Doubled ammo is a resource lever that sits outside our formula; it does not change TTK, it changes how many fights you can afford before you run dry. id Software lowered danger without making anything take longer.

**World of Warcraft, Mythic+ (Legion, patch 7.2.5, 2017).** Patch 7.2.5 set each keystone level to raise enemy health and damage by 10%, up from 8%. Here `h = e = s` for a step factor `s`, and `p = 1` until the group gears up. So each level divides safety ratio by `s²` and multiplies fight length by `s`. One level at 10% divides safety ratio by `1.1² = 1.21`. From +2 to +10 is eight steps, so `s = 1.1⁸ ≈ 2.14`. Safety ratio falls by `2.14² ≈ 4.59`, and every pull lasts more than twice as long. Blizzard has changed the per-level rate several times since, which is why you always name the patch or season when you quote these.

**The Elder Scrolls IV: Oblivion (2006).** Oblivion uses a slider instead of named steps. According to the Construction Set documentation for the game setting that controls it, the slider raises the damage you deal and divides the damage you take by the same factor, and the hard end inverts this. That is `p = 1/e` everywhere on the slider. Plug it in and safety ratio scales by `1/e²` while fight length scales by `e`. Oblivion's slider is the Skyrim ladder made continuous, and it has the same compounding. A slider position that doubles damage taken quarters the safety ratio.

Four games, one form. Once you have `p`, `e` and `h`, danger is `p / (h × e)` and duration is `h / p`. Everything else on the menu (ammo, enemy count, aggression) is a lever outside this pair, and you should name it separately.

### Eyes-open design judgment

What should you decide deliberately?

- **Which knob carries the difficulty.** If you want harder fights without longer fights, push `e` and leave `p` and `h` alone. If you want longer fights (more time to read an enemy, more room for combos), raise `h` and accept that danger rises too unless you offset it with `e < 1`.
- **Whether steps are equal ratios.** Players judge difficulty by how often they fail, which tracks safety ratio multiplicatively. Aim for equal ratios between steps. If one step is much larger than the others, as Legendary is, label it that way, so players do not feel tricked.
- **What the player does when safety ratio drops below 1.** At safety ratio 0.25 the straight trade is gone, and the fight becomes a test of blocking, healing, dodging and consumables. That can be great. It can also turn a build-expression game into a potion-management game. Decide which you are making.
- **Whether you tell the player the truth.** The Skyrim numbers in this lecture come from community documentation, not from the game's menu. A tooltip that said "enemies are about 12× as dangerous" would be honest and useful. Most games choose adjectives instead.

### Check yourself (on the example)

1. A mode uses `p = 0.8`, `e = 1.25`, `h = 1` on the base fight above. Compute safety ratio, health cost per fight, and fight length.
2. You want a mode with half of Adept's safety ratio and no change in fight length. Give `(p, e, h)`.

<details>
<summary>Answers</summary>

1. `R = 3 × 0.8 / 1.25 = 1.92`. Health cost `1 / 1.92 ≈ 52%`. Fight length `10 / 0.8 = 12.5` s.
2. Fight length depends on `h / p`, so keep `h = p = 1`. Then `R = 3 / e = 1.5` gives `e = 2`.

</details>

## 3. The other levers

Damage and health multipliers are the easiest levers to build and the easiest to explain. They are not the only ones, and some games avoid them on purpose.

**Enemy count.** A second enemy of the same kind doubles incoming damage per second while both are alive. If you focus them one at a time, total TTK doubles and you take one enemy's damage rate for the whole fight plus the second's for the first half. That is `1 + 2 = 3` times the damage of one fight in twice the time (the focus-fire cost from week 10), so the safety ratio falls by a factor of 3. If you spread your damage across both, say with area damage at half strength (`a = 0.5` in week 10's terms), both stay alive the whole time, the fight takes twice as long, and the safety ratio falls by 4, the same drop as Skyrim's step from Adept to Master. Full-strength area damage kills both in the time of one fight, so the safety ratio only halves. In general `N` enemies focused one at a time cost `N(N + 1) / 2` single fights. Enemy count behaves like raising `h` and `e` together, which is the Mythic+ shape.

**Aggression and uptime.** How often enemies attack changes their effective damage per second without changing any number on a tooltip. An enemy that attacks every 3 seconds instead of every 4 has `e = 4/3` in disguise. Resident Evil 4 (2005) is widely described by players as quietly adjusting enemy aggression and damage based on how well you are doing. Capcom has not published the rules, so treat the details as community findings.

**Execution windows.** Some games keep every number the same and shrink the time you have to react, for example a shorter parry window or a faster wind-up. Our safety ratio model cannot see this lever, because it assumes the player trades hits evenly. The lever changes how often the player's ideal play succeeds, which in turn changes the *effective* `e` a given player experiences. That is useful. A shorter parry window hurts a careless player more than a precise one, so it separates skill levels in a way a flat `e` never can.

**Resources.** Ammo, potions, mana regeneration. Doom's doubled ammo is the classic case. Resource levers do not change a single fight's safety ratio. They change how many fights you can take in a row before you must retreat, which is a different kind of danger, attrition. If your game has attrition, write down a second quantity, the number of average fights a full set of resources buys. Health cost per fight, from section 1, is exactly the number you need.

**Layering levers with mitigation.** If your game has an armor stat, remember from MMO303 week 2 that effective HP scales as `HP × (1 + A/K)`. A difficulty setting that multiplies enemy damage by `e` is equivalent, for danger, to dividing the player's effective HP by `e`. You can express a hard mode either way, but only one of them shows up on the character sheet. Pick the one that keeps the character sheet meaningful.

### Adaptive difficulty

Everything so far is static. The player picks a setting and it stays. **Dynamic difficulty adjustment** (DDA) changes the multipliers during play based on how the player is doing.

The best-documented example comes from Valve. Michael Booth's 2009 talk on the AI systems of Left 4 Dead describes a "Director" that estimates each survivor's stress from damage taken and nearby threats, then cycles between building up pressure, holding a peak, and backing off for a relaxation period of roughly half a minute. It does not tune a safety ratio to a fixed target. It tunes the *rhythm* of danger so that quiet stretches follow intense ones.

Adaptive systems raise two design questions you should answer on paper before you build one.

1. **Does the player know?** A hidden adjustment that lowers `e` when you struggle can feel like help. Discovered later, it can feel like the game was lying about your skill.
2. **Is it exploitable?** If playing badly makes the game easier, a skilled player can play badly on purpose before a hard section. Any DDA that reads "recent performance" needs a slow response, or bounds, or both.

## 4. Level scaling: difficulty that follows you

Difficulty modes move the safety ratio once, by the player's choice. **Level scaling** moves it continuously as the player grows. [Week 8](w08-power-curves-and-level-scaling.md) modelled four schemes (fixed, full, banded, downscaled) as functions from player level to enemy level. This section adds one knob that puts scaling and difficulty modes in the same formula.

Recall from week 8 that power is offense times defense, `P = a × h`, and that the safety ratio of a fight equals the power ratio, `R = P_player / P_enemy`. Let the player's power grow by a factor `P` over the game. Let enemy power grow by `P^α`, where `α` is a **scaling exponent** between 0 and 1. Then:

```
R = R₀ × P^(1 − α)
```

- `α = 0` is week 8's fixed scheme. Enemies stay where you left them. Three times the power gives three times the safety ratio, and old zones become trivial.
- `α = 1` is full scaling. Enemies grow exactly as fast as you and the safety ratio never moves. At level 50 a common bandit still costs a third of your health bar.
- Anything in between is partial scaling. With `α = 0.5`, three times the power gives `√3 ≈ 1.73` times the safety ratio. You feel growth, and the world stays relevant.

| Player power growth P | R growth, α = 0 | α = 0.5 | α = 0.8 | α = 1 |
|---|---|---|---|---|
| 1 | 1 | 1 | 1 | 1 |
| 2 | 2 | 1.41 | 1.15 | 1 |
| 3 | 3 | 1.73 | 1.25 | 1 |
| 5 | 5 | 2.24 | 1.38 | 1 |

Check the `α = 0.8`, `P = 3` cell yourself. `3^0.2 ≈ 1.25`.

Now combine this with section 2. A difficulty mode multiplies `R` by a constant, `p / (h × e)`. Scaling multiplies it by `P^(1 − α)`. Together:

```
R = R₀ × p / (h × e) × P^(1 − α)
```

The two knobs do different jobs. The difficulty mode sets the *height* of the curve, meaning how dangerous a fight is at any moment. The scaling exponent sets its *slope*, meaning how much of the player's growth they get to feel. You can pair a hard mode with gentle scaling, or an easy mode with steep scaling, and the player will feel the difference. Many games tie both to one menu entry. You do not have to.

### Gear is part of power

The Elder Scrolls IV: Oblivion (2006) sits close to `α = 1`. The Unofficial Elder Scrolls Pages note that the quality of weapons and armor found on enemies rises with your level, alongside their stats. Players' best-known complaint is the roadside bandit wearing armor worth more than a castle. The model explains why the game did it. `P` includes the player's gear. If enemies scaled their stats and not their gear, every gear upgrade would still raise the player's power against them, and the effective `α` would fall below 1. To hold the ratio constant, the game had to scale enemy gear too, and in doing so it broke the fiction. If you want full scaling, decide in advance which parts of player power the enemy copies, and accept what the copies look like in the world.

Guild Wars 2's downscaling, from week 8, is the mirror image. It pushes the player's level-based stats down and leaves gear, skills and traits alone, so the part of `P` that survives is the part that comes from options and equipment. Next week treats that split directly.

### What scaling costs

Full scaling makes the world reusable. Every zone stays a valid place to play, which matters when you have spent a year building it. The cost is that the player's growth becomes invisible in the one number they feel, the safety ratio. Players notice. The fix is rarely to turn scaling off. Choose an `α` below 1, or scale only some enemies, or scale stats while letting the player's new abilities (not new numbers) carry the feeling of growth.

## 5. Designing a difficulty ladder

Put the pieces together into a procedure you can follow.

1. **Measure the base fight.** From your week 4 and week 12 work, get TTK₀ and TTD₀ for a representative fight on the default setting. Compute `R₀`.
2. **Pick a target safety ratio for each rung.** Use equal ratios. A factor of 2 per rung, as Skyrim uses up to Master, is a sensible default. Write the targets down as health cost per fight, because designers and testers find percentages easier to argue about than ratios.
3. **Decide the duration budget.** Set an upper bound for fight length on the hardest rung. If your default fight is 10 seconds and you refuse to go above 15, then `h / p ≤ 1.5` on every rung.
4. **Solve for the multipliers.** With safety ratio and duration fixed, `h / p` is known and `p / (h × e)` is known, so `e` follows. Choose `p` and `h` to keep the character sheet meaningful (for example, never let `p` drop below 0.75 so gear still feels good).
5. **Add non-numeric levers last.** Execution windows, enemy count, AI behaviour, resources. Each one moves effective safety ratio, so re-measure with a playtest or a simulation from week 12.
6. **Offer assists separately from difficulty.** Celeste (2018) is the reference case. Its Assist Mode lets players slow the game speed, add air dashes, grant infinite stamina, or turn on invincibility, each as a separate toggle. Those are accessibility tools, not rungs on a ladder, and presenting them apart from "difficulty" avoids telling a player who needs them that they are playing "Easy."

## In-class activity (25 minutes)

Work in pairs. You are tuning a small action RPG. The default fight against a standard enemy has `TTK₀ = 8` s and `TTD₀ = 24` s.

1. Compute `R₀` and the health cost per fight on the default setting.
2. Design four rungs (Story, Normal, Hard, Nightmare). Normal is the default. Each rung should halve the safety ratio of the one below it, and Story should have double Normal's safety ratio. No rung may have fights longer than 12 s.
3. Solve for `(p, e, h)` on each rung. Record them in a table with TTK, TTD, safety ratio, health cost and fight length.
4. Now build the same four safety ratios using only enemy count and `e`. How many enemies per encounter do you need on Nightmare, and what happens to fight length?
5. Swap sheets with another pair. Find the rung where their design will feel most like a damage sponge, and say why in one sentence.

Expected output: two tables and a one-paragraph recommendation. Most pairs discover that the fight-length cap forces them to put nearly all the difficulty into `e`.

## Common misconceptions

- **"Taking 3× damage makes the game 3× harder."** Only if nothing else changes. Skyrim's Legendary also cuts your damage to a quarter, so safety ratio falls by 12, not 3. Always multiply the player-side and enemy-side changes together.
- **"More enemy health is a fair way to make fights harder."** It makes them harder and longer at the same time. If you do not want the extra length, raise enemy damage instead.
- **"Level scaling means the player never gets stronger."** Only at `α = 1`. With partial scaling the player's safety ratio still grows as `P^(1 − α)`. The design choice is the exponent, not on or off.
- **"An easy mode and an assist mode are the same thing."** An easy mode shifts every multiplier at once. An assist mode lets the player remove one specific barrier (reaction speed, stamina) and keep the rest.

## Check yourself

1. A game's Hard mode sets `p = 0.7`, `e = 1.4`, `h = 1.2`. Compared with Normal, by what factor does the safety ratio change, and by what factor does fight length change?
2. Using the patch 7.2.5 Mythic+ scaling of 10% per level, how much does safety ratio fall and fight length rise going from a +2 to a +7 keystone, assuming the group's gear does not change?
3. Your player's power grows by a factor of 8 over the campaign. You want the safety ratio at the end to be exactly twice the safety ratio at the start. What scaling exponent `α` should enemies use?
4. A designer proposes making Hard mode by "doubling enemy count." Using the safety ratio model, how does this compare with Skyrim's step from Adept to Master in danger and in fight length?

<details>
<summary>Answers</summary>

1. Safety ratio factor `p / (h × e) = 0.7 / (1.2 × 1.4) = 0.7 / 1.68 ≈ 0.417`, so about 2.4 times as dangerous. Fight length factor `h / p = 1.2 / 0.7 ≈ 1.71`.
2. Five steps at 10%. Fight length multiplies by `1.1⁵ ≈ 1.61`. Safety ratio divides by `1.1¹⁰ ≈ 2.59`, so it falls to under 40% of its +2 value.
3. `8^(1 − α) = 2`, so `(1 − α) × log 8 = log 2`, which gives `1 − α = 1/3` and `α ≈ 0.67`.
4. With focus fire, two enemies cost `1 + 2 = 3` single fights of damage, so the safety ratio falls by 3, a little less than Adept to Master's 4. With half-strength area damage that hits both, it falls by exactly 4. Fight length doubles in both cases (Skyrim's Master fight takes 20 s instead of 10 s because `p = 0.5`). So the numbers nearly match, and the difference is in what the player does. Two enemies invite positioning and kill-order choices, and one tougher enemy does not.

</details>

## Lab / assignment hook

**Lab 13, difficulty ladder** ([`labs/lab13.md`](../labs/lab13.md)). You will extend your week 4 TTK sheet into a difficulty sheet: four rungs with target safety ratios and a fight-length cap, solved for `(p, e, h)`, plus a level-scaling tab that plots safety ratio across 30 levels for three values of `α`. Deliverable: the sheet and a 400-word design memo.

## Sources

- The Unofficial Elder Scrolls Pages (UESP), "Skyrim:Difficulty". Damage multipliers for the six difficulty settings; Legendary added in patch 1.9 (Skyrim, 2011, with later patches).
- The Elder Scrolls Construction Set Wiki, "FDifficultyDamageMultiplier". Oblivion's difficulty slider scales damage dealt up and damage received down by one factor, inverted at the hard end (Oblivion, 2006). Sources disagree on the size of the extreme factor, so this lecture does not use it.
- UESP, "Oblivion:Leveling". Opponent strength and enemy and loot equipment quality rise with player level (Oblivion, 2006).
- LevelSkip, "The Well-Appointed Bandit: The Case for Level Scaling in The Elder Scrolls". Player reception of Oblivion's gear-scaled bandits.
- Doom Wiki (Fandom), "Skill level", and the Steam guide "DOOM Engine - Difficulty Levels". On "I'm Too Young to Die" the player takes half damage and ammo pickups are doubled (Doom, 1993, and Doom II).
- Warcraft Wiki, "Mythic+" (accessed September 2026). Patch 7.2.5 (Legion, 2017) notes: enemy health and damage increase by 10% per keystone level, was 8%. The rate has changed in later patches.
- Guild Wars 2 Wiki, "Dynamic level adjustment". Downscaling to zone maximum plus one; skills, traits and gear retained (current live game).
- Resident Evil Wiki, "Game Rank (RE4)". Player-documented adaptive difficulty; not officially confirmed by Capcom (Resident Evil 4, 2005).
- Booth, M. (2009). "The AI Systems of Left 4 Dead." Talk at AIIDE 2009, Valve. The Director's stress estimate and build-up, peak and relax cycle.
- Game Developer, "Check out Celeste's remarkably granular Assist options", and Celeste Wiki, "Assist Mode". Game speed, stamina, air dash and invincibility options (Celeste, 2018).
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press. Chapter "Progression in PvE Games".
- Schreiber, I. (2010). *Game Balance Concepts*, Level 7, "Advancement, Progression and Pacing".

## Interactive spec: examples/w13-difficulty-ladder.html

**The one insight.** A difficulty setting has two effects that the menu hides: danger (safety ratio) and duration (fight length). Player damage moves both. Enemy damage moves only danger. The multipliers compound, so Legendary is 12× as dangerous as Adept, not 3×.

**Layout.** Two linked panels side by side at 1280px, stacked at 390px. Preset row above both panels, sliders below.

**Left panel, "What the menu says."** Grouped bar chart, linear y-axis 0 to 4. For the current setting, three bars: `p` (player damage, ochre), `e` (damage to you, blood), `h` (enemy health, steel). A faint ghost of the Adept bars (all 1) sits behind. Caption under the chart: "Damage to you ×{e}".

**Right panel, "What you feel."** Scatter plot. x-axis: fight length in seconds, linear, 0 to 60. y-axis: health cost per fight, log scale from 2% to 1000%, gridlines at 5%, 10%, 25%, 50%, 100%, 200%, 500%. A horizontal band at 100% labelled "straight trade lost above this line". Dotted iso-safety ratio lines are horizontal in this plot (health cost = 1/M), so label them on the right edge with their safety ratio (M = 12, 6, 3, 1.5, 0.75, 0.25). The six Skyrim presets are always drawn as small labelled grey dots. The current setting is a large dot in ink with a trail showing its last position.

**Readout (exact numbers, copyable).** A table under the right panel with columns Setting, p, e, h, TTK, TTD, Safety ratio, Health cost, Ratio vs Adept, Length vs Adept. Values to 2 decimals (percentages to 1 decimal).

**Controls.**
- Preset buttons: Novice, Apprentice, Adept, Expert, Master, Legendary. Each sets `(p, e, h)`.
- Sliders: `p` 0.1 to 3 (step 0.05), `e` 0.25 to 12 (step 0.05, logarithmic slider mapping), `h` 0.25 to 4 (step 0.05, log mapping).
- Number inputs: `TTK₀` (default 10 s, range 1 to 60) and `TTD₀` (default 30 s, range 1 to 300).
- Toggle "Lock fight length": when on, moving `p` also moves `h` so that `h / p` stays constant.
- All controls keyboard operable; sliders have visible labels and live values.

**Formulas.**
```
TTK = TTK0 * h / p
TTD = TTD0 / e
R   = TTD / TTK            // = (TTD0/TTK0) * p / (h*e)
cost = 1 / R               // shown as a percentage
ratioVsAdept = p / (h*e)
lengthVsAdept = h / p
```

**Presets (Skyrim, UESP).** Novice (2, 0.5, 1), Apprentice (1.5, 0.75, 1), Adept (1, 1, 1), Expert (0.75, 1.5, 1), Master (0.5, 2, 1), Legendary (0.25, 3, 1).

**Test values (defaults TTK₀ = 10, TTD₀ = 30).**
- Adept: TTK 10.00, TTD 30.00, R 3.00, cost 33.3%, ratio vs Adept 1.00, length vs Adept 1.00.
- Master: TTK 20.00, TTD 15.00, R 0.75, cost 133.3%.
- Legendary: TTK 40.00, TTD 10.00, R 0.25, cost 400.0%, ratio vs Adept 0.08 (display "1/12").
- Novice: TTK 5.00, TTD 60.00, R 12.00, cost 8.3%.
- Custom `p = 1, e = 12, h = 1`: TTK 10.00, TTD 2.50, R 0.25, cost 400.0% (same danger as Legendary, a quarter of the length).
- Custom `p = 0.8, e = 1.25, h = 1`: R 1.92, cost 52.1%, TTK 12.50.

**Moment of insight.** On load, the page shows Adept and Legendary together: the left panel's ghost vs current bars look like a modest change, and the right panel shows Legendary's dot four times further right and twelve times higher. A one-line caption states "Legendary: 12× the danger, 4× the length." A button "Same danger, no sponge" jumps to `p = 1, e = 12, h = 1` and animates the dot straight left (skip the animation under `prefers-reduced-motion`).

**Second tab, "Level scaling."** Line chart of safety ratio growth vs player power `P` from 1 to 5 for a slider-controlled `α` (0 to 1, step 0.05) plus fixed reference curves for `α = 0`, `0.5`, `1`. Formula `growth = P^(1 - α)`. Test values: `P = 3`, `α = 0.8` gives 1.25; `P = 5`, `α = 0.5` gives 2.24; `P = 2`, `α = 0` gives 2.00; `P = 8`, `α = 0.667` gives 2.00.
