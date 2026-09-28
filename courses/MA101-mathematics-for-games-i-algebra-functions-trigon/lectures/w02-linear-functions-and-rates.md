# MA101 · Week 02 — Linear Functions and Rates (Damage per Level)

**Why this matters:** "+N per level" is the most common growth rule in games, and it is the one players complain about most ("the last 20 levels do nothing"). A straight line has two numbers in it. Once you can read, fit and compare those two numbers, you can decide what a level should feel like instead of discovering it in playtest.

**You will be able to:**
- Compute the slope and intercept of a linear game rule from its formula, a table, or two data points.
- Explain, with numbers, why a constant absolute gain is a shrinking relative gain.
- Convert rates between units (per second, per swing, per level, per stat point) and compose them.
- Find where two linear rules cross and use the crossover to make a design decision.

**Before class:** Ian Schreiber, *Game Balance Concepts* (2010 blog course), "Level 3: Transitive Mechanics and Cost Curves," the sections on cost curves. Dunn & Parberry, *3D Math Primer*, chapter 1, the section on 2D coordinate spaces (reread if graphs still feel slow).

**Prerequisites from earlier courses:** [MA101 week 1](w01-functions-as-machines.md) (functions, variables and parameters, composition, inverses). No earlier courses.

**Interactive:** [`examples/w02-flat-growth.html`](../examples/w02-flat-growth.html). Keep it open during section 2.

---

## 1. What makes a function linear

A function is **linear** when every step of the same size in the input changes the output by the same amount. Walk one step right on the graph and you always go up (or down) by the same distance. The graph is a straight line.

Every linear function can be written as

```
f(x) = b + m·x
```

- `m` is the **slope**, also called the **rate of change**. It is how much the output changes when the input goes up by 1.
- `b` is the **intercept**. It is the output when the input is 0, the point where the line crosses the vertical axis.

Maths textbooks usually write `mx + b`. Game designers usually think "start at b, then add m per step," so this course writes `b + m·x`. Same function.

### Slope has units

A slope is always "output units per input unit." That sounds pedantic until it saves you.

- Life gained per character level: **life / level**.
- Damage per second: **damage / second**.
- Attack power per point of Strength: **AP / Strength**.

If you multiply two rates, the units multiply too, and matching units cancel. `(AP / Strength) × (DPS / AP) = DPS / Strength`. When the units of your answer come out wrong, the arithmetic is wrong. Check units before you check numbers.

### Reading a slope from a table

You do not need the formula to find the slope. Take any two rows, divide the change in output by the change in input:

```
m = (y₂ − y₁) / (x₂ − x₁)
```

For the Minecraft fall-damage rule from [week 1](w01-functions-as-machines.md), the rows `d = 8, damage = 5` and `d = 13, damage = 10` give `m = (10 − 5) / (13 − 8) = 1` damage per block. Take two other rows past the third block and you get 1 again. That is the test for linearity from data: **every pair of rows gives the same slope.** If the slopes differ, the rule is not linear, and you have learned something.

## 2. Worked example: the line that feels like it slows down

### The hook

In Diablo II, a Barbarian starts at level 1 with 55 life and 25 Vitality. Every level-up gives 2 life directly and 5 stat points to spend. Each point spent on Vitality gives the Barbarian 4 more life. A player who puts all 5 points into Vitality every level gains exactly `2 + 5 × 4 = 22` life per level, from level 2 all the way to level 99.

The first of those level-ups raises life from 55 to 77, a 40% jump. The last one, from 98 to 99, raises it by 1%. Players describe this as "levels getting weaker." The rule never changed. So did leveling slow down or not?

### The model

With every stat point in Vitality and no items, the Barbarian's life is a linear function of level:

```
Life(L) = 55 + 22·(L − 1)
        = 33 + 22·L
```

- `L` is the character level, 1 to 99.
- 55 is the life at level 1.
- 22 is the slope, in life per level.
- The second line is the same function tidied into `b + m·L` form, with intercept 33. The intercept is "life at level 0," a level that does not exist. That is common. The intercept is a tool for writing the line, not always a value the game ever shows.

Two quantities describe "how much a level-up gave":

```
absolute gain  = Life(L) − Life(L − 1) = 22            (always)
relative gain  = 22 / Life(L − 1)                       (shrinks)
```

The absolute gain is the slope. It never changes. The relative gain divides the same 22 by a total that keeps growing, so it shrinks toward zero.

### Numbers you can check

| Level L | Life(L) | Absolute gain from L−1 | Relative gain from L−1 |
|---|---|---|---|
| 1 | 55 | — | — |
| 2 | 77 | +22 | +40.0% |
| 5 | 143 | +22 | +18.2% |
| 10 | 253 | +22 | +9.5% |
| 25 | 583 | +22 | +3.9% |
| 50 | 1,133 | +22 | +2.0% |
| 75 | 1,683 | +22 | +1.3% |
| 99 | 2,211 | +22 | +1.0% |

Check one row by hand. `Life(10) = 55 + 22 × 9 = 253`. `Life(9) = 231`. `22 / 231 = 0.095`, so 9.5%.

The third column is the line. The fourth column is the feeling.

### The visual

Open [`examples/w02-flat-growth.html`](../examples/w02-flat-growth.html). The left panel plots `Life(L)` against level: a straight line. The right panel plots the relative gain of each level-up: a curve that drops steeply at first and then flattens near zero.

Drag the level marker from 2 to 99. On the left, the marker climbs at a constant rate. On the right, it slides down a hill. Same numbers, two views, and they disagree about whether anything is slowing down. The line says "nothing changed." The curve says "each level matters less than the last." Both are true, because they answer different questions.

Now change the slope preset to "no Vitality" (2 life per level) and back to "all Vitality" (22). The left line tilts. The right curve barely changes shape: it still starts high and falls. Then drag the starting-life slider up to 200. Watch the right curve collapse. A big intercept makes even early levels feel small, because the first gains are divided by a large starting total.

### Why the relative view matters

Players compare what they have to what they had. A level that adds 22 life to 55 changes how many hits you survive by 40%. A level that adds 22 life to 2,189 changes it by 1%, well below what anyone notices in a fight. A useful rule of thumb from psychophysics, the study of how people perceive change, is that people notice ratios rather than differences. You do not need the exact law for design work. You need the habit: **whenever you add a constant, ask what fraction of the current total it is.**

This is the same argument as the armor lecture in MMO303, in reverse. There, the percentage view made armor look like it was falling off while survival grew in a straight line: [MMO303 week 2](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w02-armor-and-damage-mitigation.md). Here, the straight line is real and the "falling off" feeling is also real, because what players feel is the ratio.

### Cross-game recognition

A line hides inside many rules that are not written as `b + m·x`. Rewriting them into that form is the skill.

**Pokémon (Generation III onward).** From [week 1](w01-functions-as-machines.md), a non-HP stat with base 100, IV 31, no EVs and a neutral nature is `floor(231 × L / 100) + 5`. Drop the rounding and it is `5 + 2.31·L`: a line with slope 2.31 stat points per level and intercept 5. The base stat sets the slope, `(2B + IV + EV/4) / 100` per level. So a species with a higher base stat does not start much higher. It *climbs faster*. At level 5 a base-50 and a base-100 stat are 5 points apart. At level 100 they are 100 apart.

**World of Warcraft (classic era, patch 1.12 rules as used by WoW Classic in 2019).** Every 14 attack power adds 1 damage per second. That is a line with slope `1/14` DPS per AP. A warrior's 2 AP per Strength composes with it into a line with slope `2/14 = 1/7` DPS per Strength. Section 4 shows what happens when you change the rate's units from "per second" to "per swing."

**League of Legends (current live rules).** Champion stats grow with level, but *not* linearly. The increase at each level-up is `g × (0.65 + 0.035·n)`, where `g` is the champion's listed growth value and `n` is the new level. So the level 2 level-up gives 72% of `g` and the level 18 level-up gives 128% of `g`. The total at level 18 is exactly `17·g`, the same as a flat line would give. Riot kept the endpoint and moved gains from early levels to late ones. It is a deliberate answer to the problem in this worked example, and section 5 takes it apart.

Three games, three rules. Two are lines with a slope you can name. The third is a line's endpoints with a curve between them, chosen to fight the shrinking relative gain.

### Design judgment

A flat "+N per level" rule is a good default. Choose it deliberately.

- **Strength: easy to budget.** You know the value at every level with one multiplication. Content designers can set enemy numbers with the same formula and stay in step.
- **Strength: easy to explain.** Players can predict "+22 life next level." Predictable rewards are good for planning builds.
- **Cost: late levels feel empty.** The relative gain falls like `1/L`. If levels 80 to 99 are meant to feel rewarding, the reward cannot be a flat stat bump. Give them something else (a skill, an item slot, a title) or change the growth rule.
- **Cost: the intercept is a hidden dial.** A large starting value flattens the early curve. A small one makes early levels feel huge and then drops them fast. Decide what level 2 should feel like and set `b` to match.
- **Alternatives.** Back-loaded growth (League) keeps the level-cap total and moves value later. Percentage growth, "+5% per level," keeps the relative gain constant but makes absolute numbers explode. That is exponential growth, the subject of [week 4](w04-exponentials-and-the-xp-curve.md). Pick the one whose problems you would rather manage.

### Check yourself (worked example)

1. With every point in Vitality, what is a Barbarian's life at level 30, and what relative gain does the level-up from 30 to 31 give?
2. From which level-up onward does each level add less than 2% life? Show the inequality.
3. Rewrite the Pokémon stat line for base 80, IV 31, 252 EVs and neutral nature in `b + m·L` form (ignore rounding).

(Answers at the end of the lecture.)

## 3. Building a line from two points

Designers often know two values and need the line through them. "Level 1 enemies should have 120 HP. Level 60 enemies should have 3,660 HP. What about level 37?"

Step 1, slope from the two points:

```
m = (3,660 − 120) / (60 − 1) = 3,540 / 59 = 60 HP per level
```

Step 2, write the line starting from a known point. The **point-slope form** says "start at a point you know, add the slope times how far you moved":

```
HP(L) = 120 + 60·(L − 1)
```

Step 3, use it. `HP(37) = 120 + 60 × 36 = 2,280`.

Step 4, check the other endpoint. `HP(60) = 120 + 60 × 59 = 3,660`. Always check the point you did not start from. It catches most slips.

Point-slope form is worth preferring in game work, because the starting point (level 1, the first zone, the cheapest item) is usually a number the designer actually chose. `120 + 60·(L − 1)` tells a reader where the line starts. `60 + 60·L` hides it.

### When two points give nonsense

Try a different request. "Level 10 enemies have 200 HP, level 40 enemies have 1,100 HP." The slope is `900 / 30 = 30`. The line is `HP(L) = 200 + 30·(L − 10)`. At level 1 it gives `200 − 270 = −70` HP.

The line is correct. Your domain is wrong. A line through two points extends forever in both directions, and it will pass through impossible values somewhere. When you fit a line, check its value at both ends of the real domain. If it breaks, you have three honest options: restrict the rule to the levels where it makes sense, pick a different starting point, or accept that the growth is not linear and move to a curve.

## 4. Rates, units and the per-swing trap

Many game numbers are rates, and games often show a rate in one unit while computing it in another.

In classic-era World of Warcraft a melee weapon has a **speed**, the number of seconds between swings, and a damage range. Attack power adds `AP / 14` to the weapon's damage per second. The game applies that bonus *per swing*, so each swing gets the per-second bonus multiplied by the seconds per swing:

```
damage per swing = (weapon DPS + AP / 14) × speed
```

Check the units: `(damage / second) × (seconds / swing) = damage / swing`. They work.

Now give a warrior 1,400 attack power, which is `1,400 / 14 = 100` bonus DPS, and compare two weapons.

| Weapon speed (s/swing) | Bonus per second | Bonus per swing | Swings per second |
|---|---|---|---|
| 1.5 | +100 | +150 | 0.667 |
| 2.6 | +100 | +260 | 0.385 |
| 3.8 | +100 | +380 | 0.263 |

Per second, attack power is worth exactly the same on every weapon. Per swing, the slow weapon gets two and a half times as much. Anything in the game that happens *once per swing* (a single big hit, a proc, a special attack that adds to one swing's damage) sees the per-swing number. Anything that runs over time sees the per-second number.

That is the per-swing trap. It is the same slope, `1/14`, seen through two different units. When a player says "attack power is better on slow weapons," ask "better per what?" The answer changes the design question.

### Composing rates

Rates chain the way functions chain in [week 1](w01-functions-as-machines.md). If each link is linear, the chain is linear, and its slope is the product of the slopes:

```
Strength → AP:        2 AP / Str
AP → DPS:             1/14 DPS / AP
DPS → per swing:      3.8 (damage/swing) / DPS     on a 3.8-speed weapon

Strength → per swing: 2 × 1/14 × 3.8 ≈ 0.543 damage per swing per Strength
```

So 100 Strength adds about 54 damage to each swing of a 3.8-speed weapon. That multiplication of slopes is the most useful single trick in this lecture. It lets you value any stat in any unit without running the game.

## 5. Two lines: crossings and ratios

### Where lines cross

Two linear rules meet at exactly one point unless they have the same slope. That meeting point often *is* the design decision.

Suppose you have two rings. Ring A gives a flat +30 damage. Ring B gives `10 + 2·L` damage at character level `L`. Which is better? Set them equal:

```
30 = 10 + 2·L   →   L = 10
```

Below level 10 Ring A wins. Above level 10 Ring B wins. At level 10 they tie. You have found the level at which a sensible player swaps rings, and you can move it by changing any of the three numbers. If you want Ring A to stay relevant until level 25, you need `30 = 10 + m·25`, so `m = 0.8`, or you raise A to `10 + 2 × 25 = 60`.

Designers use crossovers to make sure no item is strictly better than another everywhere. Two lines with different slopes always trade places somewhere. Your job is to put that place inside the part of the game players will reach.

### Where ratios settle

Many feelings depend on the ratio of two lines, not on either line alone. How many hits does a Barbarian survive? That is `life / damage per hit`. Take the all-Vitality Barbarian and an enemy whose hit is `D(L) = 5 + 4·(L − 1)` at the same level.

| Level | Life | Enemy hit | Hits to die |
|---|---|---|---|
| 1 | 55 | 5 | 11.0 |
| 10 | 253 | 41 | 6.2 |
| 50 | 1,133 | 201 | 5.6 |
| 99 | 2,211 | 397 | 5.6 |

The ratio starts at 11 and settles near `22 / 4 = 5.5`, the ratio of the slopes. That is a general fact. As the input grows, the ratio of two lines approaches the ratio of their slopes, because the intercepts become small next to the growing slope terms.

The design lesson is sharp. **Intercepts control the early game. Slopes control the late game.** If early fights feel too easy, change the intercepts. If endgame fights feel off, the intercepts cannot save you. Change the slopes.

## 6. When a line is not enough: League's back-loaded growth

League of Legends gives the cleanest example of a designer bending a line on purpose. The live rule (per the League of Legends Wiki, current in 2026) is that a champion's stat at level `n` is

```
stat(n) = base + g·(n − 1)·(0.7025 + 0.0175·(n − 1))
```

and the increase at each level-up is `g·(0.65 + 0.035·n)`. Take a growth value of `g = 4` and compare with the flat line `base + 4·(n − 1)`.

| Level n | League total growth | Flat-line total growth | League level-up gain |
|---|---|---|---|
| 2 | 2.88 | 4 | 2.88 |
| 6 | 15.80 | 20 | 3.44 |
| 10 | 30.96 | 36 | 4.00 |
| 14 | 48.36 | 52 | 4.56 |
| 18 | 68.00 | 68 | 5.12 |

Check level 10: `9 × (0.7025 + 0.0175 × 9) = 9 × 0.86 = 7.74`, times 4 is 30.96.

The endpoints match. The middle sags below the line. The last column is the interesting one. The per-level gain is itself a line in `n`, rising by `4 × 0.035 = 0.14` each level. A function whose *rate of change* is linear is a **quadratic**, which is next week's subject. So League fixed the "late levels feel empty" problem by making the growth rule one degree higher than a line.

You can now say what that buys and costs. It keeps the level-18 totals every champion was balanced around. It gives late levels a larger absolute gain, which partly offsets the shrinking relative gain. It costs readability. The tooltip value `g` is no longer what you get from any single level except around level 10.

## In-class activity (25 minutes)

In groups of three, design the "life per level" rule for a new class in a game with levels 1 to 50.

1. Choose the feeling. Write one sentence for what level 2 should feel like and one for level 50.
2. Choose `b` and `m` for a linear rule that matches your level-2 sentence. Compute the relative gain at levels 2, 10, 25 and 50.
3. An enemy archetype hits for `8 + 3·(L − 1)`. Compute hits-to-die at levels 1, 25 and 50. What does it settle toward?
4. Find the level where your class's life line crosses another group's. Decide whether that crossover is a problem.
5. Present your line in one sentence and one number to the class: "Our class gains X per level; at level 50 a level-up is worth Y%."

Expected output: a filled-in table for steps 2 and 3, and the crossover level from step 4.

## Common misconceptions

- **"Leveling slows down, so the formula has diminishing returns."** The absolute gain is constant. Only the relative gain shrinks. Say which one you mean.
- **"The intercept is the starting value."** Only if the input starts at 0. With levels starting at 1, the starting value is `b + m`, and point-slope form `start + m·(L − 1)` is clearer.
- **"AP is worth more on slow weapons."** Per swing, yes. Per second, no. Always ask "per what?"
- **"A line through two good points is good everywhere."** Check the ends of your real domain. The level 10 and 40 line gave negative HP at level 1.

## Check yourself

1. A Barbarian puts 3 of the 5 points into Vitality at every level-up and 2 elsewhere. Write the life rule in point-slope form, and compute life at level 60.
2. A designer wants enemy damage of 12 at level 1 and 250 at level 35. Find the line, then compute damage at level 20.
3. A classic-era warrior uses a 2.6-speed weapon and gains 70 Strength. How much damage does each swing gain? How much DPS?
4. In League, a champion has health growth `g = 90`. How much health has it gained from growth by level 9? How much does the level-up from 8 to 9 give?
5. Ring A gives +45 damage. Ring B gives `5 + 1.6·L`. At what level should a player switch, and which ring is better at level 30?

<details>
<summary>Answers</summary>

Worked-example questions:

1. `Life(30) = 55 + 22 × 29 = 693`. The level-up to 31 gives `22 / 693 ≈ 3.2%`.
2. Need `22 / Life(L) < 0.02`, so `Life(L) > 1,100`. `33 + 22·L > 1,100` gives `L > 48.5`, so from level 49. The level-up from 49 to 50 adds `22 / 1,111 ≈ 1.98%`. Check: from 48 to 49 it is `22 / 1,089 ≈ 2.02%`.
3. `raw = 160 + 31 + 63 = 254`, so the line is `5 + 2.54·L`: intercept 5, slope 2.54 per level.

End-of-lecture questions:

1. Slope `2 + 3 × 4 = 14` life per level. `Life(L) = 55 + 14·(L − 1)`. `Life(60) = 55 + 14 × 59 = 881`.
2. `m = (250 − 12) / 34 = 7`. `D(L) = 12 + 7·(L − 1)`. `D(20) = 12 + 7 × 19 = 145`.
3. 70 Strength is 140 AP, which is `140 / 14 = 10` DPS. Per swing: `10 × 2.6 = 26` damage.
4. Total at level 9: `90 × 8 × (0.7025 + 0.0175 × 8) = 90 × 8 × 0.8425 = 606.6`. A flat line would give 720. The level-up to 9: `90 × (0.65 + 0.035 × 9) = 90 × 0.965 = 86.85`.
5. `45 = 5 + 1.6·L` gives `L = 25`. At level 30 Ring B gives `5 + 48 = 53`, so B is better by 8.

</details>

## Lab hook

**Lab 02: Fit, compare and cross.** You fit lines to a growth table from two points, detect which of four data sets are really linear using slopes between rows, and design two items whose crossover lands at a level you choose. See [`labs/lab02.md`](../labs/lab02.md).

## Sources

- Diablo II Barbarian life (Diablo II: Lord of Destruction era, values as listed on the official site): The Arreat Summit (Blizzard's official Diablo II site), "Classes: Barbarian." Starting life 55, starting Vitality 25, +2 life per level, +4 life per Vitality point.
- Diablo II stat points per level: The Arreat Summit, "F.A.Q.: Skills, Corpses, and Hirelings." 5 attribute points and 1 skill point per level.
- Classic-era World of Warcraft attack power: Vanilla WoW Archive, "Attack power" (patch 1.12 rules, WoW Classic 2019). 14 AP per 1 DPS, damage per swing `(weapon DPS + AP/14) × weapon speed`, 2 AP per Strength for warriors.
- League of Legends champion growth: League of Legends Wiki, "Champion statistic" (live rules, 2026). Per-level increase `g × (0.65 + 0.035 × n)`, 17 times the growth value by level 18. The closed form with 0.7025 and 0.0175 appears on the same page for attack speed and gives the same totals.
- Pokémon stat formula: The Cave of Dragonflies, "Stat Mechanics" (Generation III onward). See week 1.
- Schreiber, I. (2010). *Game Balance Concepts*, "Level 3: Transitive Mechanics and Cost Curves." gamebalanceconcepts.wordpress.com.
- Dunn, F. & Parberry, I. (2011). *3D Math Primer for Graphics and Game Development*, 2nd ed. CRC Press. Chapter 1.

## Interactive spec: examples/w02-flat-growth.html

**The one insight the visual must make obvious:** a constant absolute gain (a straight line) is a shrinking relative gain (a falling curve). The student drags one level marker and sees it climb steadily on the left while it slides downhill on the right.

**Layout.** Two linked panels, side by side on desktop, stacked on phones (line on top).

**Left panel: "Life by level."** x-axis level 1 to `Lmax`, y-axis life, auto-scaled to `Life(Lmax)` rounded up to the next 500. Plot `Life(L) = S + m·(L − 1)` as a solid ochre line with a dot at every integer level. The current level has a larger dot and a small step marker drawn from `(L−1, Life(L−1))` to `(L, Life(L))` labelled `+m`.

**Right panel: "What each level-up adds."** Same x-axis (levels 2 to `Lmax`). y-axis relative gain in percent, 0% to max(40%, value at L=2) rounded up to the next 10%. Plot `100 × m / Life(L − 1)` as a falling curve (moss colour) with dots at integer levels. The current level has a larger dot and a label, for example "+22 = +9.5%". Draw a dashed horizontal guide at 2% labelled "hard to notice (rule of thumb)".

**Controls** (keyboard operable, numeric readouts):
- Level marker L: slider 2 to `Lmax`, default 10.
- Starting life S: slider 0 to 300, step 5, default 55.
- Life per level m: slider 0 to 50, step 1, default 22. Two preset buttons: "All Vitality (22)" and "No Vitality (2)".
- Level cap `Lmax`: select 50 or 99, default 99.
- Toggle "Back-loaded (League-style) growth, same total at cap". When on, overlay on the left a dashed steel curve that uses League's shape but is rescaled so it ends on the line at the cap:
  ```
  shape(L) = (L − 1)·(0.7025 + 0.0175·(L − 1))
  k        = m·(Lmax − 1) / shape(Lmax)
  B(L)     = S + k·shape(L)
  ```
  On the right, overlay its relative gain `100 × (B(L) − B(L−1)) / B(L−1)` as a dashed steel curve. Label it "same endpoint, gains moved later". (For `Lmax = 18`, `shape(18) = 17` and `k = m`, which is League's actual rule.)

**Readout table below the panels** with rows L = 2, 5, 10, 25, 50, 75, 99 (omit rows above `Lmax`) and columns "Life", "Gain", "Relative gain". Values to one decimal for percentages, whole numbers for life.

**Test values** (defaults S = 55, m = 22, Lmax = 99, toggle off):
| L | Life | Relative gain from L−1 |
|---|---|---|
| 2 | 77 | 40.0% |
| 5 | 143 | 18.2% |
| 10 | 253 | 9.5% |
| 25 | 583 | 3.9% |
| 50 | 1,133 | 2.0% |
| 75 | 1,683 | 1.3% |
| 99 | 2,211 | 1.0% |

Other checks: S = 55, m = 2 gives Life(99) = 251. S = 200, m = 22 gives relative gain at L = 2 of 11.0%. League-style check with S = 0, m = 4, Lmax = 18 (allow `Lmax = 18` via a hidden test parameter `?cap=18` in the URL): B(10) = 30.96, B(18) = 68.00.

No game logos, character art or class icons. Label the presets in plain words; name Diablo II only in a caption ("defaults match a Diablo II Barbarian who puts every point in Vitality").
