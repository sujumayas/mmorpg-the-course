# MA101 · Week 01 — Functions as machines: input stat, output effect

**Why this matters:** Every number on a character sheet was produced by a rule that took other numbers in and pushed one number out. If you can read those rules as functions, you can predict what a change will do before you ship it, and you can explain to a player why their upgrade felt small.

**You will be able to:**
- Compute the output of a multi-input game formula by hand, step by step, including rounding.
- Identify the variable, the parameters, the domain and the range of a game function.
- Compose two functions into a pipeline and compute the combined rate from input to final effect.
- Invert a simple function to answer a designer's "how much input do I need?" question.

**Before class:** Dunn & Parberry, *3D Math Primer for Graphics and Game Development* (2nd ed.), chapter 1, sections on 1D and 2D Cartesian coordinates (you need to be able to read a graph). Freya Holmér, "Math for Game Devs [2022, part 1]", the first 20 minutes (the "why math" and 1D number-line segments).

**Prerequisites from earlier courses:** None. This is the first mathematics course in the program. You need school algebra: order of operations, fractions, and solving `3x + 2 = 11` for `x`.

**Interactive:** [`examples/w01-stat-machine.html`](../examples/w01-stat-machine.html). Keep it open during section 2.

---

## 1. A function is a machine with one output

Picture a box. Numbers go in one side. One number comes out the other. The box always does the same thing to the same inputs. That box is a **function**.

You already use them. When you equip a sword with +12 attack and your damage goes from 40 to 52, a function took your stats in and produced a damage number. When you fall off a cliff in Minecraft and lose four hearts, a function took the height of the fall and produced the damage.

The formal definition has one rule that matters for designers:

> A function gives **exactly one output** for each allowed input.

That rule is why functions are useful in games. If the same inputs could give different outputs, you could not balance anything. (Randomness is not an exception. A random damage roll is a function of the stats *and* the random number the game drew. Give it the same draw and it gives the same result. [MA102](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w01-sample-spaces-and-events.md) treats the random part properly.)

### Notation

We write a function like this:

```
f(x) = 2x + 5
```

Read it as "f of x equals two x plus five." The letter `f` names the machine. The `x` in brackets is the input slot. The right-hand side is what the machine does. To use it, you put a number in the slot everywhere `x` appears:

```
f(10) = 2 × 10 + 5 = 25
```

Nothing forces you to call the machine `f` or the input `x`. In game code you will see `damage(attack)`, `xpToLevel(level)` or `fallDamage(blocks)`. Good names are better than short ones. In this course we use short names in derivations and long names in tables and code.

### Four terms you will use all semester

- **Variable.** The input you are studying right now. It changes as you move along a graph.
- **Parameter.** An input you are holding fixed for the moment. A character's class, a weapon's base damage or a monster's level are often parameters. Which inputs count as variables and which as parameters is your choice, not a fact about the formula.
- **Domain.** The set of inputs the function accepts. Level might run from 1 to 60. A fall distance cannot be negative. The domain is part of the design.
- **Range.** The set of outputs the function can actually produce. If your damage function can never output more than 9,999, then 9,999 is the top of its range, and your UI only needs four digits.

The distinction between variable and parameter is the idea that unlocks this whole lecture. A formula like `damage = attack × skillMultiplier − armor` has three inputs. When you ask "what does attack do?", attack is the variable and the other two are parameters. When you ask "what does armor do?", you swap roles. Same formula, different question, different graph.

## 2. Worked example: the Pokémon stat machine

### The hook

Pokémon's official competitive format, the Video Game Championships (VGC), sets every Pokémon above level 50 to level 50 for the duration of a battle. Serious players breed for a "perfect" individual value (IV) of 31 in the stats they care about, instead of a random 0 to 31.

Here is the surprise. With the same breeding effort, a perfect IV adds **15 points** to a stat at level 50 and **31 points** at level 100. Nothing about the Pokémon changed. The level did. So how can one input be worth twice as much just because a *different* input moved?

The answer is that inputs do not add their value directly to the output. They go through a machine first, and the machine's other settings decide how much each input is worth.

### The model

Since Generation III (Ruby and Sapphire, 2002), the main-series games compute every stat except HP with this machine:

```
Stat = floor( ( floor( (2·B + I + floor(E/4)) · L / 100 ) + 5 ) · N )
```

- `B` is the **base stat**. Every species has one per stat, fixed by the designers. A Pikachu's base Speed is not a Snorlax's base Speed.
- `I` is the **individual value** (IV), 0 to 31, set when the Pokémon is created.
- `E` is the **effort value** (EV), gained through training, at most 252 in one stat. Only a quarter of it counts, rounded down.
- `L` is the **level**, 1 to 100.
- `N` is the **nature multiplier**: 1.1 if the Pokémon's nature boosts this stat, 0.9 if it lowers it, 1.0 otherwise.
- `floor(x)` means "round down to a whole number." `floor(115.5) = 115`.

HP uses a slightly different machine, with no nature and a bigger constant that grows with level:

```
HP = floor( (2·B + I + floor(E/4)) · L / 100 ) + L + 10
```

Read the stat machine as a pipeline of four small steps:

1. **Combine.** Add up the species, the individual and the training: `raw = 2B + I + floor(E/4)`.
2. **Scale by level.** Multiply by `L/100` and round down.
3. **Add a floor.** Add 5 so no stat is ever tiny.
4. **Apply nature.** Multiply by `N` and round down.

Step 2 is the answer to the hook. The IV lives inside `raw`, and `raw` is multiplied by `L/100`. At level 100 that multiplier is 1, so every IV point is worth one stat point. At level 50 it is 0.5, so every IV point is worth half a stat point. The IV's value depends on the level parameter.

### Numbers you can check

Take a stat with base `B = 100`, a perfect IV of 31, no EVs and a neutral nature. Then `raw = 2 × 100 + 31 + 0 = 231`, and level is our variable.

| Level L | raw · L / 100 | floor | + 5 | Stat |
|---|---|---|---|---|
| 1 | 2.31 | 2 | 7 | 7 |
| 10 | 23.1 | 23 | 28 | 28 |
| 25 | 57.75 | 57 | 62 | 62 |
| 50 | 115.5 | 115 | 120 | 120 |
| 75 | 173.25 | 173 | 178 | 178 |
| 100 | 231 | 231 | 236 | 236 |

Now hold the level at 50 and change one input at a time. Each row differs from the first row in exactly one input.

| Change from B=100, IV 31, EV 0, neutral, L=50 | raw | Stat at L=50 | Change |
|---|---|---|---|
| (starting point) | 231 | 120 | — |
| IV 31 → 0 | 200 | 105 | −15 |
| EV 0 → 252 | 294 | 152 | +32 |
| Nature neutral → boosting | 231 | floor(120 × 1.1) = 132 | +12 |
| Base 100 → 50 | 131 | 70 | −50 |

Check the last row yourself: `131 × 50 / 100 = 65.5`, floor gives 65, plus 5 is 70.

Now do the same four changes at level 100. You will find the IV is worth 31, the EVs 63, the nature 23 and the base-stat drop 100. **Every input except the "+5" doubled in value when the level doubled.** That is what it means for level to be a multiplier on the other inputs.

One HP check, so you have tried both machines. A species with base HP 250, IV 31 and 252 HP EVs at level 100 has `raw = 500 + 31 + 63 = 594`, so `HP = 594 + 100 + 10 = 704`. At level 50 it has `297 + 50 + 10 = 357`.

### The visual

Open [`examples/w01-stat-machine.html`](../examples/w01-stat-machine.html). The left panel draws the four-step pipeline with the value at each stage written on it. The right panel graphs the stat against level for your current settings, with a faint second line showing the same Pokémon with IV 0.

Drag the level slider. Watch the gap between the two lines. At level 1 they are almost on top of each other. At level 100 they are 31 apart. The gap between the lines *is* the value of the IV, and you can see it grow. Then drag the base-stat slider and watch the whole line tilt. Base stat sets how steep the line is. Level decides where along the line you stand.

### Cross-game recognition

The idea to take away is "an input's worth depends on the other inputs it passes through." You will meet it in every game with a character sheet. Here it is in two more.

**World of Warcraft (classic era, 2019 re-release of the 2004-2006 rules).** A warrior's Strength does not add damage directly. It goes through two machines in a row. First, each point of Strength gives the warrior 2 attack power (AP). Second, every 14 AP adds 1 to the weapon's damage per second (DPS). Written as functions:

```
AP(Str)  = 2 · Str          (Strength's contribution only)
DPS(AP)  = weaponDPS + AP / 14
```

Chain them and one point of Strength is worth `2/14 = 1/7` DPS. Same structure as Pokémon: the value of the input you control depends on a conversion rate set by another part of the system. A class that gets 1 AP per Strength gets half that value from the same stat point.

**Minecraft (Java Edition).** Fall damage is a function of the number of blocks you fell. The first 3 blocks are free. Each block after that costs 1 health point (half a heart). A player at full health has 20 health points, so a 23-block fall is exactly fatal without armor or enchantments:

```
fallDamage(d) = max(0, d − 3)
fallDamage(23) = 20
```

Here the "other input" is hidden in the rule itself. The constant 3 decides how much every block is worth: nothing for the first three, one point each after. Change the 3 to a 5 and a 10-block fall goes from 7 damage to 5, a 29% cut, while a 23-block fall goes from 20 to 18, a 10% cut. One parameter, different effects at different inputs.

Three games, three formulas, one habit: before you judge a number, find the machine it goes through and ask which other inputs set its worth.

### Design judgment

What should you take from the Pokémon machine as a designer?

- **Multiplying by level keeps old investments proportional.** Because IVs, EVs and base stats are all scaled by `L/100`, a Pokémon that is 20% better than another at level 20 is still about 20% better at level 80. That is a choice. A game that added IVs *after* the level step (`... + 5 + I`) would make IVs matter a lot early and very little late.
- **The "+5" and "+L+10" terms protect the low end.** Without them a level 1 Pokémon with a low base stat could have a stat of 0 or 1, and damage formulas that divide by Defense would break. When you write a formula, test it at the smallest inputs in its domain.
- **Rounding costs information.** The `floor` steps throw away fractions. At level 50 an odd `raw` loses half a point. This is invisible most of the time and then decides a speed tie in a tournament. Round once, at the end, unless you have a reason.
- **Setting a level for competition is choosing a parameter for everyone.** The VGC level-50 rule turns level from a variable into a parameter that every player shares. Once that is fixed, the competitive question becomes only about base stats, IVs, EVs and nature. Fixing a parameter is a strong design tool for making comparisons fair.
- **Players cannot see the machine.** The summary screen shows the output, not the steps. If you want players to reason about their investments, you need to show them the parts that matter, or accept that only players who read wikis will.

### Check yourself (worked example)

1. A Pokémon has base Speed 80, IV 31, 252 Speed EVs and a boosting nature. Compute its Speed at level 50 and at level 100.
2. At level 50, how much Speed does a boosting nature add compared with a neutral nature for the Pokémon in question 1? Why is it not simply 10% of the neutral value in every case?
3. A classic-era warrior can gain either 10 Strength or 25 AP from two items. Which adds more DPS, and by how much?

(Answers at the end of the lecture.)

## 3. Four ways to show the same function

A function is the rule, not any one picture of it. You will switch between four views constantly, so practise all of them.

**Formula.** `fallDamage(d) = max(0, d − 3)`. Short and exact. Hard to read at a glance for most people.

**Table.** Pick inputs, list outputs.

| Blocks fallen d | 0 | 2 | 3 | 4 | 8 | 13 | 23 |
|---|---|---|---|---|---|---|---|
| Damage | 0 | 0 | 0 | 1 | 5 | 10 | 20 |

Tables are what a player builds from experiments and what a designer builds in a spreadsheet. They show specific values well and trends poorly.

**Graph.** Put the input on the horizontal axis and the output on the vertical axis, and draw a point for every input. For fall damage you get a flat line along zero up to `d = 3`, then a line rising one unit for every unit to the right. The shape, a flat run and then a ramp, is visible in a way the formula hides. Graphs show trends well and exact values poorly.

**Code.** The version the game actually runs.

```
function fallDamage(blocks) {
  return Math.max(0, blocks - 3);
}
```

Code adds something the other three views leave out: the **type** of the input. Minecraft measures fall distance as a decimal number, not a whole count of blocks, so real code also has to decide how to round. Every time you move from a formula to code, write down where the rounding happens.

A rule of thumb for designers: build the table first (it catches arithmetic mistakes), draw the graph second (it catches shape mistakes), write the formula third, and treat code as a translation of the formula, checked against the table.

## 4. Domain and range are design decisions

When a mathematician writes a function they state its domain. When a designer writes one they often forget, and the bug reports tell them later.

Ask three questions of every game function.

**What inputs are legal?** Pokémon levels run 1 to 100. IVs run 0 to 31. EVs run 0 to 252 per stat. Each of those limits is written into the game's data. A value outside the domain is a bug or a cheat. Your formula does not need to behave well there, but your code does need to reject it.

**What happens at the edges?** At `d = 3` the fall-damage function switches from "free" to "costs damage." At level 1 the stat machine produces single-digit stats. Edges are where players find exploits and where formulas divide by zero. Test them first.

**What outputs are possible, and does the rest of the game handle them?** The maximum Pokémon stat is bounded because every input is bounded. You can compute that ceiling, and the UI designer needs it to size the number box. If your damage formula has no upper bound, a stack of multipliers will one day produce a number your health bar cannot display.

The `max(0, ...)` in the fall-damage rule is a **clamp**, a small function that forces an output into an allowed range. You will see clamps everywhere, and week 7 is devoted to them. For now, notice that a clamp changes the shape of the graph. Without it, falls under 3 blocks would *heal* you.

## 5. Composition: machines in a pipeline

Game systems rarely use one function. The output of one machine is the input of the next. That chaining is called **composition**.

If `g` turns Strength into attack power and `h` turns attack power into DPS, then

```
h(g(Str))
```

means "put Strength into g, then put the result into h." Read it from the inside out. Some books write it `(h ∘ g)(Str)`. Same thing.

Using the classic WoW warrior numbers, with a 50 DPS weapon and ignoring AP from other sources:

| Strength | g: AP = 2·Str | h: DPS = 50 + AP/14 | Change per 10 Str |
|---|---|---|---|
| 0 | 0 | 50.00 | — |
| 70 | 140 | 60.00 | +1.43 per 10 |
| 140 | 280 | 70.00 | +1.43 per 10 |
| 210 | 420 | 80.00 | +1.43 per 10 |

Every 70 Strength adds exactly 10 DPS. The composed function is `DPS = 50 + Str/7`. You found the combined rate by multiplying the two rates: 2 AP per Strength times 1/14 DPS per AP.

**Order matters.** Suppose a buff adds 10% to attack power and a second buff adds a flat 100 attack power. "Add 100, then multiply by 1.1" gives `1.1 × (AP + 100)`. "Multiply by 1.1, then add 100" gives `1.1 × AP + 100`. At 1,000 AP those are 1,210 and 1,200. Ten AP is a small gap, but the spec must say which one the game does, because players will measure it. The exemplar lecture in MMO303 makes the same point about armor penetration: [MMO303 week 2, section 4](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w02-armor-and-damage-mitigation.md).

A practical habit: when a damage number looks wrong, write the pipeline out as a composition, one box per step, and compute each intermediate. The bug is almost always in the order of two boxes or in a rounding step between them.

## 6. Inverse functions: running the machine backwards

Designers ask backwards questions all the time. "How high can a player fall and survive?" "What level does this Pokémon need to reach 150 Attack?" "How much Strength does a warrior need for 100 DPS?"

Each of these asks for the input that produces a given output. The function that answers it is the **inverse**, written `f⁻¹`. For a simple rule you find it by solving for the input.

Fall damage, for falls longer than 3 blocks:

```
damage = d − 3
d = damage + 3
```

A player with 20 health points dies at `d = 20 + 3 = 23` blocks. To survive, they must fall at most 22. You used the inverse without the name.

Warrior Strength for a DPS target, with a 50 DPS weapon:

```
DPS = 50 + Str / 7
Str = 7 · (DPS − 50)
```

For 100 DPS the warrior needs `7 × 50 = 350` Strength, which is 700 attack power.

Two warnings.

First, an inverse only exists where each output comes from a single input. `fallDamage` gives 0 for every fall from 0 to 3 blocks, so "which fall gave 0 damage?" has no single answer. On the flat part the function has no inverse. On the ramp it does.

Second, the rounding in the Pokémon machine means several levels can produce the same stat, and some stat values are skipped. For "what level reaches 150 Attack?" you solve the formula without the floors to get close, then check neighbouring whole levels in a table. That "solve roughly, then check in a table" method works for almost every game formula you will meet.

## In-class activity (25 minutes)

Work in pairs. You need a spreadsheet and the interactive.

1. **Build the machine.** In a spreadsheet, create input cells for B, IV, EV, L and N. Build the four pipeline steps in four separate cells, then the final stat. Check your sheet against the first table in section 2 at levels 1, 50 and 100.
2. **Measure each input's worth.** At level 50, record how much the stat changes when you add 1 to B, 1 to IV, and 4 to EV. Repeat at level 100. Write one sentence explaining the pattern.
3. **Redesign.** Propose a change to the formula so that IVs are worth the same number of points at every level. Write the new formula and compute the stat at levels 50 and 100 for B = 100, IV 31. Is your version better for a casual player? For a tournament?
4. **Swap and break.** Swap sheets with another pair. Find one input (inside the legal domain) where their redesigned formula gives a result they did not intend.

Expected output: one spreadsheet per pair and a half-page note answering steps 2 to 4.

## Common misconceptions

- **"A +1 to a stat always adds the same amount to the result."** Only if the input goes straight to the output. When it passes through a multiplier, its worth depends on the multiplier's other input, as with IVs and level. Find the machine before you value the input.
- **"The number on the summary screen is the stat the game uses."** It is the output of one machine. Battle damage feeds that number into another machine, with its own multipliers. Distinguish what the screen shows from what the damage formula computes.
- **"Composition order does not matter because multiplication is commutative."** Multiplication alone commutes. A pipeline with any addition or clamp in it does not. `1.1 × (x + 100)` is not `1.1 × x + 100`.
- **"Every function has an inverse."** Only where each output comes from one input. Flat regions, clamps and rounding all break the inverse.

## Check yourself

1. Compute the Attack stat of a Pokémon with base Attack 130, IV 20, 100 Attack EVs and a lowering nature at level 50.
2. In the classic-era WoW warrior pipeline, how much Strength is equivalent to one extra point of weapon DPS?
3. A designer changes Minecraft-style fall damage to `max(0, 2·(d − 4))` with 20 health points. What is the highest survivable fall in whole blocks? What are the domain and range if falls are capped at 100 blocks?
4. For the stat pipeline with B = 100, IV 31, EV 0, neutral nature, find the lowest level at which the stat reaches at least 150. Show the rough solve and the table check.

<details>
<summary>Answers</summary>

Worked-example questions:

1. `raw = 160 + 31 + 63 = 254`. Level 50: `254 × 0.5 = 127`, plus 5 is 132, times 1.1 is 145.2, floor 145. Level 100: `254 + 5 = 259`, times 1.1 is 284.9, floor 284.
2. Neutral at level 50 gives 132, boosting gives 145, a gain of 13. The nature multiplies the value after the `+5` and then rounds down, so the gain is 10% of the pre-nature value rounded down, which is not always exactly 10% of the final number. At other levels the 10% applies to a bigger or smaller number, so the gain in points changes too.
3. 10 Strength is 20 AP, worth `20/14 ≈ 1.43` DPS. 25 AP is worth `25/14 ≈ 1.79` DPS. The AP item wins by about 0.36 DPS.

End-of-lecture questions:

1. `raw = 260 + 20 + 25 = 305`. `305 × 50 / 100 = 152.5`, floor 152, plus 5 is 157, times 0.9 is 141.3, floor 141.
2. One DPS needs 14 AP, which is 7 Strength.
3. Survive while `2(d − 4) ≤ 19` (at 20 damage you die). So `d − 4 ≤ 9.5`, and the highest whole-block survivable fall is 13 blocks (18 damage). A 14-block fall does 20 and kills. Domain: 0 to 100 blocks. Range: 0 to `2 × 96 = 192` damage (in whole blocks, the even numbers from 0 to 192).
4. Rough solve without floors: `231 × L / 100 + 5 = 150` gives `L = 145 × 100 / 231 ≈ 62.8`. Table check: L = 62 gives `floor(143.22) + 5 = 148`. L = 63 gives `floor(145.53) + 5 = 150`. Answer: level 63.

</details>

## Lab hook

**Lab 01: Build a stat machine.** You rebuild the Pokémon stat pipeline and the classic WoW Strength pipeline in a spreadsheet, graph each against its main variable, and write the inverse for one designer question per system. See [`labs/lab01.md`](../labs/lab01.md).

## Sources

- Pokémon stat formulas (Generation III onward, all main-series games since Ruby and Sapphire): The Cave of Dragonflies, "Stat Mechanics," and Bulbapedia, "Stat." Both give the non-HP formula with the nature multiplier applied after the `+5`, and the HP formula with `+ L + 10`. IV range 0 to 31, EV maximum 252 per stat from Generation VI onward (255 earlier).
- VGC level rule: Victory Road, "Pokémon Scarlet & Violet: Rules & Regulations for VGC," summarising the Play! Pokémon VGC rules, which set Pokémon above level 50 to level 50 during battle (Scarlet and Violet era, 2022 onward).
- Classic-era World of Warcraft attack power: Vanilla WoW Archive, "Attack power" (patch 1.12 rules used by WoW Classic, 2019). Every 14 AP adds 1 DPS. Warriors gain 2 AP per point of Strength.
- Minecraft fall damage: Minecraft Wiki, "Damage," section "Fall damage" (Java Edition, current in 2026). One health point per block fallen beyond the third. With 20 health points and no armor, 23 blocks is fatal.
- Dunn, F. & Parberry, I. (2011). *3D Math Primer for Graphics and Game Development*, 2nd ed. CRC Press. Chapter 1.
- Holmér, F. (2022). "Math for Game Devs [2022, part 1]: Numbers, Vectors & Dot Product." YouTube lecture recorded for FutureGames students.

## Interactive spec: examples/w01-stat-machine.html

**The one insight the visual must make obvious:** an input's worth depends on the other inputs it passes through. The gap between "IV 31" and "IV 0" lines is small at low level and large at high level, and the student sees it grow as they drag.

**Layout.** Two linked panels. On phones they stack (pipeline on top, graph below). On desktop they sit side by side.

**Left panel: the pipeline.** Four boxes in a row (column on phones), joined by arrows, each labelled and showing its current value with the arithmetic:
1. "Combine": `2·B + IV + floor(EV/4) = raw`, e.g. `2·100 + 31 + 0 = 231`.
2. "Scale by level": `floor(raw · L / 100)`, e.g. `floor(231 · 50 / 100) = floor(115.5) = 115`.
3. "Add 5": e.g. `115 + 5 = 120`.
4. "Nature": `floor(value · N)`, e.g. `floor(120 · 1.0) = 120`.
Below the boxes, a big output number: "Stat = 120". Beside it, "IV worth at this level: +15" computed as stat(IV=current) minus stat(IV=0) with all other inputs unchanged.

**Right panel: the graph.** x-axis level 1 to 100. y-axis stat, auto-scaled to the maximum of the current line at level 100 (round up to the next multiple of 50). Plot:
- Solid line (ochre, "value"): stat for current B, IV, EV, N at every integer level 1 to 100.
- Faint dashed line (ink-soft): the same with IV = 0.
- A dot on the solid line at the current level, with a vertical bracket between the two lines at that level labelled with the gap.

**Controls** (all keyboard operable, with visible numeric readouts):
- Base stat B: slider 5 to 255, step 1, default 100.
- IV: slider 0 to 31, step 1, default 31.
- EV: slider 0 to 252, step 4, default 0.
- Level L: slider 1 to 100, step 1, default 50.
- Nature: three-way segmented control "lowering 0.9 / neutral 1.0 / boosting 1.1", default neutral.
- A "Compare at L=50 vs L=100" button that animates the level slider between 50 and 100 (skip animation under `prefers-reduced-motion`).

**Formulas (exact).**
```
raw   = 2*B + IV + Math.floor(EV/4)
s1    = Math.floor(raw * L / 100)
s2    = s1 + 5
stat  = Math.floor(s2 * N)
```
Use `Math.floor(s2 * N + 1e-9)` to avoid floating-point cases like `120 * 1.1 = 131.99999`. Cross-check: floor(120 × 1.1) must print 132.

**Test values** (must match exactly):
| B | IV | EV | N | L | Stat |
|---|---|---|---|---|---|
| 100 | 31 | 0 | 1.0 | 1 | 7 |
| 100 | 31 | 0 | 1.0 | 25 | 62 |
| 100 | 31 | 0 | 1.0 | 50 | 120 |
| 100 | 31 | 0 | 1.0 | 100 | 236 |
| 100 | 0 | 0 | 1.0 | 50 | 105 |
| 100 | 31 | 252 | 1.0 | 50 | 152 |
| 100 | 31 | 0 | 1.1 | 50 | 132 |
| 50 | 31 | 0 | 1.0 | 50 | 70 |
| 80 | 31 | 252 | 1.1 | 50 | 145 |
| 130 | 20 | 100 | 0.9 | 50 | 141 |

IV gap readout test: B=100, EV 0, neutral. L=50 shows +15, L=100 shows +31.

**Below the panels:** a small live table with rows L = 1, 25, 50, 75, 100 and columns "stat", "stat with IV 0", "IV worth", so students can copy numbers into the lecture's table. No Pokémon names, sprites or logos anywhere. Label the tool "Stat pipeline (Generation III+ formula)".
