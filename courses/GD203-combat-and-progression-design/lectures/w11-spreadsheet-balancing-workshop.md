# GD203 · Week 11 — Spreadsheet Balancing Workshop

**Why this matters:** Every number you have designed in this course lives in a spreadsheet somewhere, and most balance bugs are spreadsheet bugs. A sheet that is laid out well answers "what happens at level 27?" in one glance. A sheet that is laid out badly hides a one-shot at level 27 until players find it.
**You will be able to:**
- Lay out a balance spreadsheet with separate inputs, per-level tables and check columns, so that every number traces to one input.
- Compute time-to-kill across all levels and diagnose why it drifts, using the growth rates of health and damage.
- Recognize the ratio form (attack divided by defense, armor divided by a level constant) as the tool that keeps fights the same length at every level, and decide when you want drift instead.
- Run a sensitivity test and a goal seek to find which input a balance problem depends on.

**Before class:** Schreiber, *Game Balance Concepts*, level 10 ("Final Boss", which includes the course's spreadsheet tutorial); Schreiber & Romero, *Game Balance* (2021), the chapter on spreadsheets. Bring a laptop with Google Sheets, Excel or LibreOffice Calc, and your lab 10 sheet.
**Prerequisites from earlier courses:** GD102 week 14, tuning with spreadsheets ([syllabus](../../GD102-systems-design-and-game-mechanics/syllabus.md)); GD203 week 4, [time-to-kill and time-to-die](w04-time-to-kill-and-time-to-die.md); GD203 week 8, [power curves and level scaling](w08-power-curves-and-level-scaling.md); GD203 week 10, [enemy design by the numbers](w10-enemy-design-by-the-numbers.md); MMO303 week 2, [armor and damage mitigation](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w02-armor-and-damage-mitigation.md).
**Interactive:** [Level sweep](../examples/w11-level-sweep.html) (built from the spec at the end of this lecture). Keep it open during section 2.

---

## 1. What a balance sheet is for

A balance spreadsheet is a machine for answering questions. "What is the player's DPS at level 12?" is a lookup. "Does any fight between levels 1 and 60 last fewer than two hits?" is the question you actually built the sheet for. Lay the sheet out so that the second kind of question is answered by looking, not by hunting.

This workshop uses one layout for every sheet in the course. It has four kinds of tab.

**Inputs.** Every constant the design depends on, one per cell, each with a label, a unit and a note on where it came from. Growth rates, role targets, base stats, caps. Color input cells one way (this course uses pale yellow) so nobody mistakes them for results. If a number appears in a formula anywhere else in the workbook, that is a bug waiting to happen. Move it here and reference it.

**Tables.** One row per level (or per item, or per enemy). Columns are derived quantities, computed from inputs and from earlier columns in the same row. Every cell in a column uses the same formula, filled down. If one row needs a special case, that special case is a design decision and belongs in its own input, not in a hand-edited cell.

**Checks.** Columns that compare a derived value to a target band and turn red when it falls outside. "Hits to kill between 3 and 7." "No single enemy hit above 25% of player health." "Encounter cost under budget." A good sheet has more check columns than you think it needs. A check column is a test, and you would not ship code without tests.

**Scenarios.** Specific situations pulled from the tables. "A level 15 player fights room C." These use lookups (`XLOOKUP` or `INDEX`/`MATCH`) into the tables, so they update when any input changes.

### Naming and references

Name your important inputs (`Player_DPS_growth`, `Soldier_TTK`) using your tool's named-range feature. A formula that reads `=Player_HP * Soldier_share / Soldier_TTK` is checkable by a colleague. A formula that reads `=C4*$Inputs.$B$17/$Inputs.$B$12` is not.

Learn the difference between relative references (`B4`, which shift when you fill down) and absolute references (`$B$4`, which do not). Most broken balance sheets have one missing dollar sign. The symptom is a column that looks right for the first row and drifts after that.

### Plot ratios, not raw values

Raw stats grow with level, so a chart of raw health and raw damage shows two lines going up. That tells you nothing about how fights feel. Plot the quantities the player feels: hits-to-kill, time-to-kill, encounter cost as a share of health, hours per level. These should be flat, or change in a way you chose. A flat line on a chart of a ratio is the picture of a balanced progression. A line that bends is a question you need to answer.

## 2. Worked example: does the fight stay the same length at every level?

### The hook

In the main-series Pokémon games, a level 5 creature and a level 100 creature of the same species hit different targets for very different damage. At level 5 a typical attack does single digits. At level 100 it does dozens. Yet if both fight an opponent of their own level, the number of hits needed to win barely moves. Players rarely notice this, because it is exactly what they expect. The designers had to make it happen, and a spreadsheet shows how.

### The model

Fight length in hits is health divided by damage per hit:

```
hits(L) = HP(L) / damage(L)
```

If health and damage both grow with level, the fight stays the same length only when they grow **at the same rate**. Write each as a power of level, `HP ∝ L^a` and `damage ∝ L^b`. Then:

```
hits(L) ∝ L^(a − b)
```

`a = b` gives a flat line. `a > b` makes fights longer as the player levels. `a < b` makes them shorter, until eventually everything dies in one hit.

The Pokémon damage formula (generation V onward) keeps `a` and `b` equal with a ratio:

```
damage = ((2 × L / 5 + 2) × Power × A / D) / 50 + 2      then × random 0.85 to 1.00
```

- `L` is the attacker's level. The first bracket grows linearly with it.
- `Power` is the move's base power, fixed per move.
- `A / D` is the attacker's Attack divided by the defender's Defense. Both grow roughly linearly with level, so at equal levels the ratio stays near 1.

So damage grows like `L` (from the level bracket) times `A/D` (roughly constant), giving `b = 1`. Health comes from the stat formula, `HP = floor((2 × Base + IV + floor(EV / 4)) × L / 100) + L + 10`, which also grows like `L`, giving `a = 1`. Ratio in, flat fight length out.

### Numbers you can check

Build this table yourself. Assumptions: attacker and defender at the same level; base Attack, Defense and HP all 100; individual values (IVs) 31, effort values (EVs) 0, neutral nature; a move with power 80, no same-type bonus, neutral type matchup, no critical hit. Non-HP stats use `floor((2 × Base + IV + floor(EV/4)) × L / 100) + 5`. Integer division truncates at each step, and the random factor takes one of 16 values from 85% to 100%.

| Level | Attack = Defense | HP | Damage range | Mean damage | Share of HP per hit | Hits to KO (HP ÷ mean) |
|---|---|---|---|---|---|---|
| 5 | 16 | 26 | 6-8 | 6.88 | 26.4% | 3.78 |
| 10 | 28 | 43 | 9-11 | 9.69 | 22.5% | 4.44 |
| 20 | 51 | 76 | 15-18 | 16.19 | 21.3% | 4.69 |
| 30 | 74 | 109 | 20-24 | 21.75 | 20.0% | 5.01 |
| 50 | 120 | 175 | 31-37 | 33.75 | 19.3% | 5.19 |
| 75 | 178 | 258 | 45-53 | 48.56 | 18.8% | 5.31 |
| 100 | 236 | 341 | 58-69 | 63.38 | 18.6% | 5.38 |

Raw damage grows tenfold. Hits to KO moves from 3.8 to 5.4, and above level 20 it barely moves at all (4.7 to 5.4 across 80 levels). Where it does move, at low levels, the cause is the small constants. The `+ 2` at the end of the damage formula and the `+ 5` in the stat formula are a large share of the total when stats are in the teens and a rounding error when they are in the hundreds. Those constants make early fights a little shorter. That may well be deliberate, since the first minutes of a game are when fights should be quickest.

Now the counter-example. Here is a homebrew sheet a student might write, with weapon damage and a Strength stat that both grow linearly, multiplied together:

```
W(L) = 10 + 2L        weapon damage
S(L) = 10 + 2L        Strength
damage(L) = W × S / 12
enemy HP(L) = 50 + 10L
```

| Level | W | S | Damage per hit | Enemy HP | Hits to kill |
|---|---|---|---|---|---|
| 1 | 12 | 12 | 12.0 | 60 | 5.0 |
| 5 | 20 | 20 | 33.3 | 100 | 3.0 |
| 10 | 30 | 30 | 75.0 | 150 | 2.0 |
| 20 | 50 | 50 | 208.3 | 250 | 1.2 |
| 30 | 70 | 70 | 408.3 | 350 | 0.86 |

Each stat on its own grows linearly, which looks safe. Multiplied, they grow like `L²`, so `b = 2` against `a = 1`. By level 30 every enemy dies to one hit. Nothing in the raw-stat columns looks wrong. Only the hits-to-kill column shows it, which is why that column exists.

The fix is the Pokémon move. Divide by a defensive stat that grows at the same rate: `damage = W × S / Def` with `Def(L) = 10 + 2L`. The product and the divisor cancel to `W`, and hits to kill becomes `(50 + 10L) / (10 + 2L) = 5` at every level. Exactly flat.

### See it move

Open the interactive. The left view plots raw values (player damage per hit and enemy HP) against level, and both lines climb, which looks healthy. The right view plots hits-to-kill against the same levels, with a shaded target band from 3 to 7 hits. Start with the "multiplied stats" preset and watch the right-hand line fall through the band. Then switch the damage model to "ratio" and watch the same left-hand chart barely change while the right-hand line snaps flat. The growth-exponent readout under the right chart shows `a − b` updating as you drag.

### Cross-game recognition

**World of Warcraft, classic era.** Armor mitigation is `armor / (armor + 400 + 85 × attacker level)` for attackers of level 1 to 59. The constant in the denominator grows with the attacker's level, as MMO303 week 2 showed. If defenders' armor also grows roughly linearly with level, the ratio stays steady, and a level 20 warrior against level 20 enemies mitigates about the same share as a level 50 warrior against level 50 enemies. The same ratio trick, applied to mitigation.

**Diablo II.** The chance to hit includes the factor `attacker level / (attacker level + defender level)`. At equal levels it is always one half, whether both are level 10 or level 80. The formula compares levels by ratio, so a level gap of 5 matters a lot at level 10 and little at level 80. Ratio in, level-independent behavior out.

**Your own sheet.** The lab 10 stat blocks used `h = P × t` and `d = s × H / t`. Enemy health is defined as a multiple of player DPS and enemy damage as a multiple of player health. That is the same idea taken to its limit. Enemies do not have their own growth rates at all; they inherit the player's, so `a = b` by construction.

Three presentations, one principle. When a formula divides one side's stat by the other side's, and both grow at the same rate, level cancels out. When you read a new game's combat formulas, look for the division and ask what scales with what.

### Eyes-open design judgment

**Flat is a choice, not a law.** Many games want some drift. A game might let fights get slightly longer as the player gains more abilities, so that there is time to use them. A power-fantasy game might let fights get shorter as the player masters the systems. The goal of the sheet is that the drift you ship is the drift you picked. Put the target band on the chart and check that the line stays inside it.

**Ratios hide level gaps, and that can be good or bad.** With a pure ratio, a level 60 player against level 50 enemies has a 20% edge. A level 15 player against level 5 enemies has a 200% edge. The same 10-level gap means different things at different points in the game. If you want a fixed gap to always feel the same, compare levels by their difference instead, as a level-difference table does. If you want high-level gaps to shrink in importance, that is what ratios already do. Decide which one your game needs.

**Multiplying stats is the most common way to break a sheet.** Weapon damage times a Strength multiplier, times a talent multiplier, times a gear multiplier. Each factor grows gently. Their product grows like a high power of level. Whenever two things that grow get multiplied, count exponents, and make sure the other side of the fight gets a matching exponent (a defensive stat to divide by, or health that grows faster).

**Small constants dominate early.** `+2`, `+5`, `+10` terms are invisible at level 50 and decisive at level 3. Tune your low levels separately and look at them on the chart, not only at the averages.

## 3. Workshop techniques

The rest of the session is hands-on. These are the techniques you will use.

### Goal seek: solving for the input that hits a target

Most spreadsheet tools can solve "what input makes this output equal that value?" Excel and LibreOffice call it Goal Seek; in Google Sheets it is an add-on, or you can do it by hand with a helper column. Use it to answer questions like "what Soldier TTK makes room D cost exactly 70%?" Goal seek changes one input at a time, so it answers "which value?", not "which input?". For the second question, use sensitivity.

### Sensitivity: which input does this problem depend on?

Take the output you care about (say, the worst hits-to-kill across all levels). Change each input by +10% and by −10%, one at a time, and record how much the output moves. Sort the inputs by how far they moved the output. The top one or two are your real levers. The rest barely matter, and you should stop arguing about them.

In a spreadsheet, a one-variable data table (Excel's "What-If Analysis, Data Table") does this for one input across many values. You can also build it by hand. Make a column of trial values, copy the model into a hidden block, and reference the trial value instead of the input. This is more work to set up, but it is the only way to get a sensitivity table in every tool.

A sensitivity table tells you whether your design is **robust**, which no single scenario can. If a 10% change in any input moves hits-to-kill by less than half a hit, your balance survives the patches that will come. If one input moves it by two hits, every change to that input needs a full check.

### Conditional formatting as a test runner

Apply a color rule to each check column: green inside the band, amber within 10% of an edge, red outside. Then zoom out until the whole table fits on one screen. Red cells jump out. Train yourself to look at the check tab first after every change, the way a programmer looks at test results.

### Charts that tell the truth

- Plot what the player feels (hits, seconds, shares of health), not raw stats.
- Use a log scale on the y-axis for anything that grows exponentially. On a log scale, exponential growth is a straight line, and a change in growth rate shows as a change in slope.
- Draw the target band on the chart as a shaded region. A line without a target is decoration.
- Put the level on the x-axis for progression charts and time on the x-axis for fight charts. Do not mix them.

### Common spreadsheet bugs in balance work

- **The missing dollar sign.** A reference that should be absolute is relative, so the formula drifts one row per row. The symptom is a correct first row and slightly wrong rows below it.
- **The hardcoded patch.** Someone typed a number over a formula in one row to "fix" a level. The fix is invisible until an input changes and that row does not follow.
- **The off-by-one level.** Row 2 holds level 1, so `ROW()` is one more than the level. Store the level in its own column and reference that, never the row number.
- **Rounding in the wrong place.** Games round at specific steps (Pokémon truncates after almost every operation). Round where the game rounds, and nowhere else, or your sheet disagrees with the build by a point here and there.
- **Averages where the game uses dice.** A mean damage of 33.75 does not tell you how often a fight takes 5 hits instead of 6. That question needs next week's simulation.

## 4. From the sheet to the build

A balance sheet is only useful if the numbers in the game match it. Two habits keep them in sync.

**Export, don't retype.** Designers who copy numbers from a sheet into a game editor by hand introduce errors. Set up an export (a CSV the game reads at load, or a script that writes the data files) so the sheet is the one source of truth. DB201 covers data-driven content pipelines in more depth ([syllabus](../../DB201-data-persistence-and-telemetry/syllabus.md)).

**Test the build against the sheet.** Pick a handful of scenarios from your sheet (a level 15 player hits a level 15 soldier) and check the damage number the game shows against the sheet. A mismatch means one of them is wrong, and you want to find out before a player does.

## In-class activity (30 minutes)

This is a workshop session, so the activity is longer. Work in pairs on one laptop, using your lab 10 sheet or the homebrew model from section 2.

1. **Restructure (10 min).** Move every constant to an `Inputs` tab with a name. Check that there are no numbers typed into any formula except 0 and 1.
2. **Add the feel column (5 min).** Add hits-to-kill for the soldier role against the player's weapon at every level. Chart it with a 3-to-7 target band.
3. **Break it on purpose (5 min).** Add a Strength stat that grows linearly and multiplies the player's damage. Watch the chart. Compute `a − b` for your new model.
4. **Fix it two ways (10 min).** First, add a defensive stat to divide by. Second, undo that and instead make enemy health grow fast enough to match. Compare the two charts. Which fix changes the low-level fights more?

Expected output: a screenshot of each of the three charts (broken, fixed by ratio, fixed by health growth) and a three-sentence note on which fix you would ship and why.

## Common misconceptions

- **"If every stat grows linearly, the game stays balanced."** Products of linear stats grow faster than linear. Check what gets multiplied.
- **"The raw-stat chart looks smooth, so the progression is fine."** Smooth raw stats can hide a collapsing hits-to-kill. Chart the ratio the player feels.
- **"A sensitivity test is the same as trying a few scenarios."** A scenario tells you one outcome. A sensitivity test tells you which input the outcome depends on and how strongly.
- **"The spreadsheet is the design."** The sheet models averages and assumptions. Distributions, AI behavior and player skill are not in it. That is next week's job.

## Check yourself

1. In a game, player damage grows like `L^1.5` and enemy health grows like `L`. Hits to kill is 6 at level 4. Estimate hits to kill at level 16.
2. Using the Pokémon formulas and assumptions in section 2, compute the Attack stat and HP at level 40. (Base 100, IV 31, EV 0, neutral nature.)
3. A designer's sheet has `damage = Weapon × (1 + Str/100) × (1 + Crit bonus)`. Weapon grows linearly with level, Str grows linearly, and Crit bonus is fixed. What exponent `b` does damage have at high levels? What exponent should enemy health have if fights must stay the same length?
4. You run a sensitivity test. A 10% change in soldier TTK moves room D's cost by 7 percentage points, and a 10% change in player health growth moves it by 1 point. Which input should the next patch avoid touching, and why?

<details>
<summary>Answers</summary>

1. `hits ∝ L^(1 − 1.5) = L^(−0.5)`. Level 16 is 4 times level 4, so hits scale by `4^(−0.5) = 0.5`. About 3 hits.
2. Attack `= floor((200 + 31) × 40 / 100) + 5 = floor(92.4) + 5 = 97`. HP `= floor(92.4) + 40 + 10 = 142`.
3. For large Str, `(1 + Str/100)` grows linearly, so damage is linear times linear, `b = 2`. Enemy health needs `a = 2` (or a defensive stat that grows linearly to divide by).
4. Soldier TTK. The room's cost is very sensitive to it, so small changes swing the room across its budget. Any change to it needs the whole room table rechecked. Player health growth is safe to adjust.

</details>

## Lab / assignment hook

**Lab 11: The level-sweep balance sheet** ([labs/lab11.md](../labs/lab11.md)). You rebuild your lab 10 sheet into the four-tab layout, add hits-to-kill and encounter-cost checks across levels 1-30, run a sensitivity table on six inputs, and write a short robustness report. The sheet becomes the spine of the final combat system spec.

## Sources

- Bulbapedia, "Damage" and "Stat" (main-series games). Damage formula with the `(2 × Level / 5 + 2)` level term, `A/D`, `/50 + 2`, and the random factor of 85% to 100%; stat formulas for HP and other stats from generation III onward. Checked against Smogon University, "The Complete Damage Formula for Black & White" (generation V), which gives the truncated-division form and the 16-value random roll.
- Warcraft Wiki, "Armor". `armor / (armor + 400 + 85 × level)` for attacker levels 1-59, classic era.
- The Amazon Basin (Diablo II), "Technical Formulas". Chance to hit including the `alvl / (alvl + dlvl)` level factor.
- Schreiber, I. (2010). *Game Balance Concepts*, level 10, "Final Boss" (spreadsheet tutorial) (online course). https://gamebalanceconcepts.wordpress.com/
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press.

## Interactive spec: examples/w11-level-sweep.html

**The one insight.** Raw stats can all climb smoothly while the fight length collapses or balloons. Fight length stays flat only when health and damage grow at the same rate, and dividing by a stat from the other side of the fight is the simplest way to make that happen.

**Layout.** Two linked charts, stacked on mobile, side by side at 1024 px and wider. Levels 1-60 on the x-axis of both.

- **Left: raw values.** Player damage per hit and enemy HP against level, two lines, y-axis linear with a toggle for log scale.
- **Right: hits to kill.** `enemy HP / damage per hit` against level. Shaded target band from 3 to 7 hits (band limits editable). Points outside the band drawn in the warning color. Below the chart, a readout: "HP grows like L^a, damage like L^b, a − b = X", where the exponents are estimated from the slope of log(value) against log(L) between levels 30 and 60.
- **Table under both charts.** Levels 1, 5, 10, 20, 30, 60 with W, S, Def, damage, HP and hits to kill, to 2 decimals.

**Controls.**
- Damage model radio: "Weapon only" (`damage = W`), "Multiplied stats" (`damage = W × S / k`), "Ratio" (`damage = W × S / Def`), "Pokémon" (preset, see below).
- Sliders: weapon growth per level `gW` (0-5, default 2), Strength growth `gS` (0-5, default 2), defense growth `gD` (0-5, default 2), enemy HP growth `gH` (0-30, default 10). Base values W₀ = S₀ = Def₀ = 10, HP₀ = 50, `k = 12`.
- Formulas: `W = W₀ + gW × L`, `S = S₀ + gS × L`, `Def = Def₀ + gD × L`, `HP = HP₀ + gH × L`.

**Pokémon preset.** Uses the generation V formulas with truncation at each step: stat `= floor(231 × L / 100) + 5`, HP `= floor(231 × L / 100) + L + 10`, base damage `= floor(floor(floor((floor(2L/5) + 2) × 80 × A / D) / 50) + 2`, mean damage `= average over r = 85..100 of floor(base × r / 100)`. Sliders are disabled in this preset. Plot levels 5-100 instead of 1-60.

**Test values (must match exactly).**
- Multiplied stats, defaults: L1 damage 12.00, HP 60, hits 5.00; L10 damage 75.00, HP 150, hits 2.00; L30 damage 408.33, HP 350, hits 0.86.
- Ratio, defaults: hits 5.00 at every level.
- Pokémon preset: L5 hits 3.78; L50 hits 5.19; L100 hits 5.38; L50 damage range 31-37, mean 33.75.

**First screen.** "Multiplied stats" with defaults, so the left chart shows two healthy climbing lines and the right chart shows hits falling through the bottom of the band at level 6 (2.73 hits). A single button "Divide by defense" switches to "Ratio".

**Accessibility.** All sliders keyboard-operable with visible values. Chart lines distinguishable without color (solid and dashed). Respect `prefers-reduced-motion` for transitions.
