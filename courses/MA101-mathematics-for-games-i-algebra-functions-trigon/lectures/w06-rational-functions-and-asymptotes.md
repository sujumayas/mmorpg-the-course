# MA101 · Week 06 — Rational functions and asymptotes: A/(A+K)

**Why this matters:** Exponentials grow without end. Many game stats need the opposite: a curve that keeps rising but never crosses a line, so that stacking armor, cooldown reduction or dodge can never make a character immune. The standard tool is a rational function, and one of them, `A / (A + K)`, is the most copied formula in game design. This week you learn to read it, bend it, invert it and spot it when a game writes it in disguise.

**You will be able to:**
- Identify the vertical and horizontal asymptotes of a rational function and explain what each means for a game stat.
- Compute mitigation, damage taken and effective HP from `A / (A + K)`, and derive the effective-HP line.
- Invert the formula to find the armor needed for a target mitigation.
- Rewrite a published formula such as `(0.052 · A) / (0.9 + 0.048 · A)` into the standard form, and use its asymptote to find where it breaks.

**Before class:** OpenStax, *College Algebra 2e*, section 5.6 (Rational Functions), the parts on arrow notation, vertical asymptotes and horizontal asymptotes. Look up any champion in League of Legends and note its base armor.

**Prerequisites from earlier courses:** [MA101 week 4, exponentials](w04-exponentials-and-the-xp-curve.md) and [week 5, logarithms](w05-logarithms-how-many-levels-until.md) for the contrast between curves that grow without limit and curves that approach one. Linear functions from [MA101 week 2](w02-linear-functions-and-rates.md). This lecture is the math foundation for [MMO303 week 2, armor and damage mitigation](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w02-armor-and-damage-mitigation.md), which uses it for balance decisions two years from now.

**Interactive:** [`examples/w06-armor-curve.html`](../examples/w06-armor-curve.html). Keep it open during section 2.

---

## 1. Curves that approach a line

A **rational function** is one polynomial divided by another:

```
f(x) = P(x) / Q(x)
```

The name comes from "ratio", the same way rational numbers are ratios of whole numbers. The simplest one is:

```
f(x) = 1 / x
```

Try some values. At `x = 1` it is 1. At `x = 10` it is 0.1. At `x = 1,000` it is 0.001. It keeps shrinking toward 0 and never reaches it. Going the other way, at `x = 0.1` it is 10 and at `x = 0.001` it is 1,000. As `x` approaches 0 the output grows without limit, and at `x = 0` it is undefined because you cannot divide by zero.

Those two behaviors have names.

- A **horizontal asymptote** is a value the output approaches as the input grows very large. For `1/x` it is `y = 0`. We write `f(x) → 0 as x → ∞`, read "f of x approaches 0 as x goes to infinity".
- A **vertical asymptote** is an input where the denominator becomes zero and the output shoots off to plus or minus infinity. For `1/x` it is `x = 0`.

An asymptote is a line the graph gets closer and closer to. In game terms, a horizontal asymptote is a **soft cap**: a limit players can approach but never reach. A vertical asymptote is a **singularity**: a value where your formula divides by zero and your game crashes or prints "Infinity".

### Finding them by hand

For a rational function where the top and bottom are both straight lines, the kind you will use most:

```
f(x) = (a·x + b) / (c·x + d)
```

- **Vertical asymptote:** set the bottom to zero. `c·x + d = 0` gives `x = −d / c`.
- **Horizontal asymptote:** for very large `x`, the `b` and `d` barely matter, so `f(x)` behaves like `a·x / (c·x) = a / c`. The horizontal asymptote is `y = a / c`.

That is the entire toolkit for this week. Two lines of algebra tell you where the formula blows up and what it can never exceed.

## 2. Worked example: Armor / (Armor + K)

This is the course's anchor example. You will see it again in [GD203 week 3](../../GD203-combat-and-progression-design/lectures/w03-mitigation-curves-and-effective-hp.md) and [MMO303 week 2](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w02-armor-and-damage-mitigation.md), where the focus is on balance decisions. Here the focus is on the function itself.

### The hook

In League of Legends, a champion with 100 armor takes half damage from physical attacks. Buy another 100 armor and damage taken drops to one third. Another 100 and it is one quarter. The percentage of damage blocked goes 50%, 67%, 75%, and each 100 armor seems to buy less than the last. Players say armor has "diminishing returns". Yet experienced players keep buying armor against physical damage late in a match. Either they are wrong, or the percentage is not telling the whole story.

It is not. The percentage curve bends. The quantity that decides fights, how much raw damage you can absorb before dying, grows in a straight line.

### The model

League of Legends' wiki gives the damage multiplier for non-negative armor as `100 / (100 + armor)`. Generalize the 100 to a constant `K` and you have the family:

```
damage taken       = D · K / (A + K)
mitigation m(A)    = A / (A + K)
```

- `A` is the defender's armor, zero or more.
- `K` is a positive constant chosen by the designer.
- `D` is incoming damage before armor.
- `m(A)` is the share of damage blocked, between 0 and 1.

Apply section 1. Written as `(a·A + b) / (c·A + d)`, mitigation has `a = 1`, `b = 0`, `c = 1`, `d = K`.

- **Horizontal asymptote:** `a / c = 1`. Mitigation approaches 100% and never reaches it. That is the soft cap.
- **Vertical asymptote:** `A = −K`. At `A = −100` in League, the formula divides by zero. Hold on to that; it matters for negative armor.
- **The half point:** set `A / (A + K) = 1/2`. Then `2A = A + K`, so `A = K`. **K is the armor that blocks exactly half the damage.** It is the most useful way to read the constant.

### From percent to survival: effective HP

A character dies when health reaches zero. So ask: how much raw, pre-armor damage can they absorb? Call this **effective HP (EHP)**. If a character has `H` health and takes the fraction `K / (A + K)` of each hit, then:

```
EHP = H / (fraction taken)
    = H / ( K / (A + K) )
    = H · (A + K) / K
    = H · (1 + A / K)
```

Look at the last line. It is `H + (H / K) · A`, a linear function of `A` with slope `H / K`. From week 2: a linear function adds the same amount per step. **Every point of armor adds exactly `H / K` effective HP**, whether it is the first point or the five-hundredth.

Dividing by a rational function flipped it into a line. That flip is the whole reason this formula is popular: the designer gets a percentage that can never reach 100%, and players get survival that never stops improving at a steady rate.

### The inverse: how much armor for a target?

Designers often start from a target. "At level 30, a tank should block 60%." Solve `m = A / (A + K)` for `A`:

```
m · (A + K) = A
m·A + m·K   = A
m·K         = A − m·A = A · (1 − m)
A           = K · m / (1 − m)
```

The inverse is itself a rational function, with a vertical asymptote at `m = 1`. That is the soft cap seen from the other side: 100% mitigation needs infinite armor. For `K = 100` and `m = 0.6`, you need `100 · 0.6 / 0.4 = 150` armor. For 90% you need 900. For 99% you need 9,900.

### Numbers you can check

League of Legends with `K = 100` and a 1,000 HP champion.

| Armor A | Mitigation m(A) | Damage taken | EHP | EHP gained from previous row |
|---|---|---|---|---|
| 0 | 0% | 100% | 1,000 | — |
| 50 | 33.3% | 66.7% | 1,500 | +500 |
| 100 | 50.0% | 50.0% | 2,000 | +500 |
| 200 | 66.7% | 33.3% | 3,000 | +1,000 (for 100 armor) |
| 300 | 75.0% | 25.0% | 4,000 | +1,000 |
| 400 | 80.0% | 20.0% | 5,000 | +1,000 |

Check any row by hand. Per point of armor, the EHP gain is always `1,000 / 100 = 10`. The mitigation column bends toward 100%. The EHP column is a straight line.

### Seeing it move

Open [`examples/w06-armor-curve.html`](../examples/w06-armor-curve.html). The left panel shows `m(A)` rising and flattening under a dashed line at 100%, the horizontal asymptote. The right panel shows EHP for the same armor as a straight line. Drag the armor slider and the two markers move together: the left one slows down, the right one moves at a constant speed. Then change `K`. A bigger `K` stretches the left curve sideways and makes the right line shallower, since the slope is `H / K`. Turn on "show negative armor". With the League preset the curve follows League's separate negative-armor rule and levels off, so it never reaches the vertical asymptote. Switch to Custom K to see what the plain formula would do: it plunges toward the vertical asymptote at `A = −K`. That contrast is why League needs a second rule.

The one thing to take from the visual: **a curve that approaches a limit in one view can be a straight line in the view that matters.** Always ask which quantity your players actually spend.

### Why the percentage misleads

Go from 75% to 80% mitigation. It looks like 5 points. But damage taken goes from 25% to 20%, so each hit now does one fifth less than before, and you survive 25% longer. Near the asymptote, each percentage point of mitigation is worth more survival. The formula hands those points out more slowly. The two effects cancel exactly, and the constant EHP slope is what remains.

### Cross-game recognition

The formula almost never appears in its clean form. The skill is rewriting it.

**World of Warcraft (classic era).** For attackers of level 1 to 59, the Warcraft Wiki gives armor's damage reduction as `armor / (armor + 400 + 85 × attacker level)`, capped at 75%. That is our form with `K = 400 + 85L`, where `L` is the attacker's level. So `K` is a linear function of level, and it grows as enemies get stronger.

| Attacker level | K | Mitigation from 2,000 armor | Armor at the 75% cap (3K) |
|---|---|---|---|
| 10 | 1,250 | 61.5% | 3,750 |
| 30 | 2,950 | 40.4% | 8,850 |
| 50 | 4,650 | 30.1% | 13,950 |
| 59 | 5,415 | 27.0% | 16,245 |

The same 2,000 armor blocks less against stronger attackers. Tying `K` to level keeps old gear from trivializing new enemies. The hard cap at 75% is where `A = 3K`, which limits the EHP multiplier to 4.

**League of Legends (ability haste).** The same shape governs time. Since the 2021 preseason, League has used **ability haste** in place of cooldown reduction. The wiki gives the cooldown as `base cooldown × 100 / (100 + haste)`. Replace armor with haste and damage with time: 100 haste halves cooldowns, 200 cuts them to a third. And the "EHP" of haste is casts per minute, which is `(60 / base) · (1 + haste/100)`, a straight line. A 10-second spell is cast 6 times a minute with no haste, 9 times at 50 haste, 12 at 100 and 18 at 200. The switch from a percentage stat (cooldown reduction) to this form means every point of haste now adds the same casts per minute, which is the property the EHP line gave armor.

**Dota 2 (patches 7.20 to 7.26, November 2018 to June 2020).** Valve's 7.20 patch notes gave armor's physical damage reduction as `(0.052 × armor) / (0.9 + 0.048 × armor)`. It does not look like our formula. Apply section 1 anyway. Divide the top and bottom by 0.048:

```
m(A) = (1.0833 · A) / (18.75 + A) = (13/12) · A / (A + 18.75)
```

So it is `A / (A + K)` with `K = 18.75`, multiplied by `13/12`. The horizontal asymptote is `a / c = 0.052 / 0.048 ≈ 1.083`. **As printed, this formula approaches 108% reduction, not 100%.** Set it equal to 1 and solve: `0.052A = 0.9 + 0.048A`, so `A = 225`. Past 225 armor the formula says the target takes negative damage. The patch notes do not say how the game handles that range, and no hero came near 225 armor in normal play. Valve replaced the formula in patch 7.27 (June 2020) with `(0.06 × armor) / (1 + 0.06 × armor)`. Divide by 0.06 and that is `A / (A + 16.7)`: the standard form, with an asymptote of exactly 100%. The lesson is about you as a designer: before shipping a rational formula, compute its horizontal asymptote. If it is above 1, you need a clamp or a proof that the input never gets there.

Four formulas, one family. When you meet a new stat formula with a division in it, write it as `(a·x + b) / (c·x + d)`, then ask three questions. What is the horizontal asymptote? Where is the vertical asymptote? What is the half point?

### Design judgment with eyes open

`A / (A + K)` is not the correct armor formula. It is a set of trade-offs.

- **Strength: every point is worth the same survival.** Armor never becomes worthless and never explodes. You can hand it out freely across a long progression.
- **Strength: one readable knob.** `K` is the armor that halves damage. Tie it to level, as classic WoW does, and you control power creep with one line.
- **Cost: the tooltip lies.** A tooltip showing "Damage reduction: 75%" makes players think armor is falling off. Consider showing EHP or "survives N more hits".
- **Cost: negative inputs hit the vertical asymptote.** If armor-shred effects can push `A` below 0, the formula heads toward `A = −K` and blows up. League handles negative armor with a separate formula, `2 − 100 / (100 − armor)`, which rises toward a damage multiplier of 2 as armor goes very negative. You must decide what negative armor means before a player finds it for you.
- **Cost: the curve cannot give armor a special role.** With a constant `K`, armor is equally good against every attack. If you want armor to be strong against swarms and weak against bosses, you need `K` to depend on hit size, a choice [MMO303 week 2](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w02-armor-and-damage-mitigation.md) explores.

Questions 1 to 4 in "Check yourself" use this model.

## 3. Working with the general form

Most rational stat formulas you meet in games have the shape `(a·x + b) / (c·x + d)`. You now have a checklist for any of them.

1. **Asymptotes.** Vertical at `x = −d / c`, horizontal at `y = a / c`.
2. **Value at zero.** `f(0) = b / d`. For a mitigation formula this should be 0. If `b` is not 0, the stat does something even when the player has none of it.
3. **Half point or target point.** Solve `f(x) = t` by multiplying out: `a·x + b = t·(c·x + d)`, so `x = (t·d − b) / (a − t·c)`. The vertical asymptote of this inverse is at `t = a / c`, the horizontal asymptote of the original. The two asymptotes swap roles, the same way input and output swap for any inverse.
4. **Rewrite.** If `b = 0`, divide top and bottom by `c` to reach `(a/c) · x / (x + d/c)`. The standard form appears with `K = d / c` and a scale factor `a / c`.

Try it on the Dota formula with target `t = 0.5`: `x = (0.5 · 0.9 − 0) / (0.052 − 0.5 · 0.048) = 0.45 / 0.028 = 16.1` armor for half damage. Note that this is not `K = 18.75`. The scale factor `13/12` moves the half point.

### Shifting and scaling

Two small edits change a rational curve in ways you can predict.

- **Scaling the output**, `s · A / (A + K)`, moves the horizontal asymptote to `s`. Use `s < 1` to build a soft cap below 100%. For example `0.8 · A / (A + K)` approaches 80% and never reaches it.
- **Adding a floor**, `f0 + (1 − f0) · A / (A + K)`, starts the curve at `f0` instead of 0 and still approaches 1. This is how you give a class a base dodge chance that armor-like stats build on.

### Rational versus exponential soft caps

You can also build a soft cap from last week's tools: `1 − 0.5^(A/K)` also starts at 0, blocks half at `A = K` and approaches 1. It is a different curve, though. Its EHP multiplier is `2^(A/K)`, exponential in armor, so it explodes: at `A = 5K` a character survives 32 times as long rather than 6 times. Rational soft caps give linear EHP. Exponential soft caps give exponential EHP. Pick the one whose survival curve you want, and check it in the "compare" tab of the interactive.

| A / K | Rational A/(A+K) | EHP multiplier | Exponential 1 − 0.5^(A/K) | EHP multiplier |
|---|---|---|---|---|
| 0 | 0% | 1 | 0% | 1 |
| 1 | 50% | 2 | 50% | 2 |
| 2 | 66.7% | 3 | 75% | 4 |
| 3 | 75% | 4 | 87.5% | 8 |
| 5 | 83.3% | 6 | 96.9% | 32 |

At one `K` they agree. By five they disagree by a factor of five in survival.

## In-class activity (25 minutes)

Pairs. You are designing a "resilience" stat for a small co-op game with enemy levels 1 to 20. Resilience reduces all damage.

1. Pick a formula. It must be rational, start at 0% for 0 resilience, and never exceed 70% reduction. Write it in the form `s · R / (R + K)` and state `s`.
2. Decide how `K` depends on enemy level. Write `K(L)` as a linear function, then compute `K` at levels 1, 10 and 20.
3. Using the inverse, compute the resilience a level-20 tank needs for 50% reduction against a level-20 enemy.
4. Compute the EHP multiplier at that point. Is it still a straight line in resilience? (Hint: with `s < 1` it is not exactly. Work out `1 / (1 − s·R/(R+K))` and see.)
5. Swap with another pair and find one input that breaks their formula: a vertical asymptote reachable in play, a negative value or a level where the stat is useless.

**Expected output:** the formula, a three-row `K` table, the answer to step 3 and one sentence on what you learned in step 4.

## Common misconceptions

- **"Armor has diminishing returns."** In mitigation percentage, yes. In effective HP, no. Every point adds `H / K`. Always ask which quantity someone means.
- **"An asymptote is a maximum you eventually reach."** The curve approaches it and never gets there. A reachable limit is a hard cap, which is a piecewise function (next week).
- **"All formulas with a division in them cap at 100%."** The cap is `a / c`. The Dota 7.20 formula's was about 108%. Compute it.
- **"The formula works for any input."** Rational functions have a vertical asymptote. For `A / (A + K)` it sits at `A = −K`. Any effect that can reduce the input below zero must be checked against it.

## Check yourself

1. A game uses `K = 250`. How much armor gives 60% mitigation? How many times longer does that character survive than with no armor?
2. A 2,000 HP champion in League has 150 armor and buys 30 more. How much EHP against physical damage does that add? Would the same 30 armor add more or less on a 3,000 HP champion?
3. Rewrite `damage taken = D × 600 / (600 + armor)` as a mitigation formula. What is `K`? What armor blocks 75%?
4. In classic WoW, how much armor does a character need to block 50% of a level-40 attacker's damage? How far is that from the 75% cap for the same attacker?
5. Find the vertical and horizontal asymptotes of `f(x) = (3x + 6) / (2x + 10)`. What is `f(0)`? Would it be a sensible mitigation formula?

<details>
<summary>Answers</summary>

1. `A = K · m / (1 − m) = 250 · 0.6 / 0.4 = 375`. EHP multiplier `1 + 375 / 250 = 2.5`, so 2.5 times as long.
2. Each armor point adds `H / K = 2,000 / 100 = 20` EHP, so 30 armor adds 600. On a 3,000 HP champion it adds 900. Armor is worth more on high-health characters, and health is worth more on high-armor ones.
3. Mitigation `= armor / (armor + 600)`, so `K = 600`. For 75%, `A = 600 · 0.75 / 0.25 = 1,800`.
4. `K = 400 + 85 · 40 = 3,800`. Half damage at `A = K = 3,800`. The 75% cap is at `3K = 11,400`, three times as much armor.
5. Vertical asymptote at `x = −10 / 2 = −5`. Horizontal at `3 / 2 = 1.5`. `f(0) = 6 / 10 = 0.6`. As a mitigation formula it is broken twice: it gives 60% reduction at zero stat and approaches 150%, which crosses 100% at `3x + 6 = 2x + 10`, that is `x = 4`.

</details>

## Lab hook

**Lab 06: Asymptote audit.** You build a spreadsheet that plots mitigation and EHP for four formulas (League armor, classic WoW at three attacker levels, the Dota 7.20 formula and one of your own), find each one's asymptotes and half point by algebra, and confirm them numerically. See [`labs/lab06.md`](../labs/lab06.md). Next week, [piecewise functions, caps and floors](w07-piecewise-caps-and-floors.md), covers the tool for hard caps and floors like WoW's 75% limit.

## Sources

- League of Legends Wiki, "Armor" (patch V26.10, accessed September 2026). Post-mitigation damage `= damage / (1 + armor/100)` for non-negative armor, and `damage × (2 − 100/(100 − armor))` for negative armor.
- League of Legends Wiki, "Ability haste" (accessed September 2026). Cooldown `= base × 100 / (100 + haste)`; ability haste replaced cooldown reduction in the 2021 preseason; 100 haste halves cooldowns.
- Warcraft Wiki, "Armor" and "Damage reduction" (classic era, accessed September 2026). Reduction `= armor / (armor + 400 + 85 × attacker level)` for attacker levels 1 to 59; 75% maximum.
- Valve, "Dota 2 Gameplay Update 7.20" (official patch notes, November 2018). Armor damage reduction `(0.052 × armor) / (0.9 + 0.048 × armor)`.
- Liquipedia Dota 2 Wiki, "Armor/Changelogs" and "Version 7.27" (retrieved September 2026). The 7.20 formula stayed until patch 7.27 (28 June 2020), which changed it to `(0.06 × armor) / (1 + 0.06 × |armor|)`. The wiki writes both formulas with `|armor|` in the denominator, so negative armor stays bounded.
- OpenStax, *College Algebra 2e* (2021), section 5.6, for asymptote definitions and notation.
- Every other number in this lecture is computed from the formulas above.

## Interactive spec: examples/w06-armor-curve.html

**The one insight:** the mitigation curve `A / (A + K)` bends toward a 100% asymptote, while effective HP for the same armor is a straight line. Two linked views of one formula.

**Layout.** Two plots side by side on desktop, stacked on mobile, sharing a horizontal axis "Armor A".

- **Left, "What the tooltip shows":** `m(A)` from 0 to 100% (vertical axis to 110% when the Dota preset is active). A dashed horizontal line at the asymptote `a / c`, labeled "asymptote: 100%" (or the preset's value). A dotted vertical guide at the half point with the label "K = …".
- **Right, "What keeps you alive":** `EHP(A) = H / (1 − m(A))`. A straight line for the standard form. Add small tick marks on the armor axis every `K` units, each labeled "+H", so students see equal steps.
- A vertical marker at the selected armor on both plots.

**Controls (labeled, keyboard accessible):**

1. Armor slider `A`, 0 to 600 in steps of 1, default 100. When "show negative armor" is on, the range is `−0.95·K` to 600 (never reaching `−K`).
2. Preset selector: "League of Legends (K = 100)" (default), "Classic WoW" (reveals an attacker-level slider 1 to 59, default 30, with `K = 400 + 85·L` and a 75% hard cap drawn as a solid line), "Dota 2 patch 7.20" (uses `m = 0.052A / (0.9 + 0.048A)`, armor range 0 to 300), "Custom K" (reveals a K slider 10 to 1,000).
3. Health `H`, number input 100 to 10,000, default 1,000.
4. Toggle "show negative armor". For League, use the published negative branch: damage multiplier `2 − 100 / (100 − A)`, so `m = 1 − (2 − 100/(100 − A))`. For Custom K, draw the plain formula and let it plunge toward the vertical asymptote at `A = −K`, with the asymptote drawn and labeled.
5. Tab "Compare" that overlays `1 − 0.5^(A/K)` on both plots in a second color, with its EHP `H · 2^(A/K)` on the right (clip the axis at 10·H and mark where it leaves the chart).

**Readouts (copyable):** `m(A)` to one decimal, damage taken per 100 incoming, `EHP` rounded, EHP gained per armor point (`H / K`, or the numerical slope for Dota and WoW-capped cases), and the armor needed for a target mitigation typed into a small input (`A = K·m / (1 − m)`; for Dota use `A = 0.9m / (0.052 − 0.048m)`).

**Test values.**

- League, `H = 1,000`: `A = 100` gives 50.0% and EHP 2,000; `A = 300` gives 75.0% and EHP 4,000; target 60% needs 150 armor.
- Classic WoW, attacker level 50, `A = 2,000`: 30.1%. The 75% cap is reached at `A = 13,950`, after which the EHP line goes flat.
- Dota 7.20: `A = 10` gives 37.7%; `A = 20` gives 55.9%; `A = 225` gives 100.0%; `A = 300` gives 102.0%, displayed with a warning badge "formula exceeds 100%".
- Compare tab, `K = 100`, `A = 500`: rational 83.3% with EHP multiplier 6; exponential 96.9% with multiplier 32.

**First screen:** League preset, `A = 100`, both markers visible, readout "100 armor: 50.0% blocked, EHP 2,000 (+10 per point, always)".
