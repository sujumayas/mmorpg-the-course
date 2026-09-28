# GD203 · Week 03 — Mitigation Curves and Effective HP

**Why this matters:** Players judge defensive stats by the percentage on the tooltip, and that percentage bends in ways that make good stats look bad and dangerous stats look harmless. Effective HP is the one number that tells you how long a character lives. Once you can compute it, you can see through the percentage and price defense on purpose.

**You will be able to:**
- Derive effective HP (EHP) from any mitigation formula and show that it is linear in armor under the divisive formula.
- Compute EHP for several shipped games' defense formulas, including caps, and identify where each one has constant, increasing or zero returns.
- Compute EHP against mixed damage types and use it to decide which defensive stat to raise next.
- Find the split between health and armor that maximizes EHP for a fixed budget.

**Before class:** Schreiber & Romero, *Game Balance* (2021), chapter 10 (combat), second half; Schreiber, *Game Balance Concepts*, Level 3 ("Transitive Mechanics and Cost Curves").

**Prerequisites from earlier courses:** the divisive formula and "fraction that gets through" from [GD203 week 2](w02-damage-formulas.md); multiplicative stacking from [GD203 week 1](w01-stats-as-design-language.md); rational functions and asymptotes ([MA101 week 6](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w06-rational-functions-and-asymptotes.md)); expected value ([MA102 week 4](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md)).

**Interactive:** [`examples/w03-effective-hp.html`](../examples/w03-effective-hp.html) (built from the spec at the end of this lecture). Keep it open during section 2.

---

## 1. Mitigation curves

Last week you rewrote every damage formula as `damage taken = D × f`, where `f` is the fraction that gets through and `1 − f` is the mitigation. A **mitigation curve** is the graph of mitigation against the defensive stat. Plot it for any game and you will see one of four shapes.

- **Linear to a cap.** Each point gives a fixed percentage, until a maximum. "1 point = 1% reduction, max 75%." The curve is a straight ramp that stops dead.
- **Hyperbolic.** The divisive formula `A / (A + K)`. The curve rises steeply, then flattens toward 100% without ever reaching it.
- **Exponential decay of damage.** Each point multiplies damage taken by a fixed factor, such as 0.99. Mitigation is `1 − 0.99^A`. The curve also flattens toward 100%, but differently from the hyperbola.
- **Hit-dependent.** Subtractive armor. There is no single curve, one per hit size, as you saw in week 2.

The first three can be compared on one chart for a single hit, and on that chart they look like a matter of taste. The hyperbola "flattens," so it must have diminishing returns. The linear ramp is steady until the cap. This lecture shows that the mitigation chart is the wrong chart. It hides what each shape does to survival, and it gets the answer backward for two of the three.

### Effective HP

Players don't die when mitigation hits a number. They die when health hits zero. The right question is how much raw, pre-mitigation damage a character can absorb before dying. That quantity is **effective health** or **effective HP (EHP)**:

```
EHP = HP / f = HP / (1 − mitigation)
```

If a character has 1,000 HP and takes half of every hit, attackers must deal 2,000 raw damage to kill them. EHP is 2,000. If they take a quarter, EHP is 4,000.

EHP converts every defensive stat into one currency, hit points. That is what makes it useful. Health, armor, resistance, dodge and damage-reduction buffs can all be compared in EHP, and "which one should I raise?" becomes arithmetic. It also turns directly into time. If a character faces a steady 200 raw DPS, their **time to die** is `EHP / 200` seconds. [Week 4](w04-time-to-kill-and-time-to-die.md) builds on that.

## 2. Worked example: effective HP is linear in armor

### The hook

In League of Legends, a champion with 100 armor takes half damage from physical attacks. With 200 armor they take a third, with 300 a quarter. Look at the mitigation that 100 extra armor buys each time:

| Armor | Mitigation | Gain from the last 100 armor |
|---|---|---|
| 0 | 0% | — |
| 100 | 50.0% | +50.0 points |
| 200 | 66.7% | +16.7 points |
| 300 | 75.0% | +8.3 points |
| 400 | 80.0% | +5.0 points |

From 50 points to 5 points. Armor seems to fall off a cliff, and players often conclude that stacking it is a waste. Is the fourth hundred armor really worth a tenth of the first?

### The model

Start from the divisive formula, `f = K / (A + K)`, and substitute it into EHP:

```
EHP = HP / f
    = HP × (A + K) / K
    = HP × (1 + A/K)
```

- `HP` is the character's health.
- `A` is armor.
- `K` is the armor that halves damage (100 in League of Legends).

The last line is a straight line in `A`. Its slope is `HP / K`. **Every point of armor adds exactly HP/K effective health, whether it is your first point or your four-hundredth.** In League of Legends, with `K = 100`, one point of armor adds 1% of your health as EHP against physical damage.

### Numbers you can check

A champion with 1,000 HP faces physical hits of 250 damage each.

| Armor | Mitigation | EHP | EHP from the last step | Hits to die (250 each) |
|---|---|---|---|---|
| 0 | 0% | 1,000 | — | 4 |
| 50 | 33.3% | 1,500 | +500 | 6 |
| 100 | 50.0% | 2,000 | +500 | 8 |
| 200 | 66.7% | 3,000 | +1,000 | 12 |
| 300 | 75.0% | 4,000 | +1,000 | 16 |
| 400 | 80.0% | 5,000 | +1,000 | 20 |

Check one row. At 300 armor, `f = 100/400 = 0.25`. EHP = 1,000 / 0.25 = 4,000. Hits to die = 4,000 / 250 = 16. Every 50 armor adds 500 EHP and 2 hits, every 100 adds 1,000 EHP and 4 hits, from the first point to the last.

Why does the percentage mislead? Look at damage taken instead of damage stopped. Going from 75% to 80% mitigation is only +5 points, but damage taken falls from 25% to 20%. That is one fifth less damage than a moment ago. The closer mitigation gets to 100%, the more each percentage point is worth, and the divisive formula hands out percentage points more slowly at exactly the rate that cancels this. What is left over is a constant gain in survival.

Compare it with health. Adding 1,000 HP to a 1,000 HP character doubles their health, while adding 1,000 HP to a 5,000 HP character adds only 20%. Nobody calls that diminishing returns on health. Under the divisive formula, armor behaves the same way. The "diminishing returns" is an artifact of reading a percentage.

### Move it yourself

Open the interactive. It shows two linked charts with the same armor slider under both.

- The left chart plots mitigation against armor. It bends and flattens. A bracket shows "mitigation from the last 100 armor" shrinking as you drag right.
- The right chart plots EHP against armor. It is a straight line. The same bracket, now labeled "EHP from the last 100 armor," stays the same height wherever you drag.

Now change the model selector. "Linear 1% per point, cap 75%" draws a mitigation ramp on the left, and on the right an EHP curve that bends upward, then goes flat at the cap. "Exponential 0.99 per point" draws a mitigation curve that looks almost like the hyperbola on the left, and on the right an EHP curve that shoots up. Three models that look similar in the percent view look completely different in the EHP view. The EHP view is the one that tells the truth about survival.

### The same idea in other games

**Dota 2** (patch 7.27 onward) multiplies physical damage by `1 / (1 + 0.06A)` for positive armor. As shown in week 2, that is `K / (A + K)` with `K ≈ 16.7`. So:

```
EHP = HP × (1 + 0.06A)
```

A straight line again. Each point of armor adds 6% of the hero's health as effective health against physical damage. A 1,000 HP hero with 10 armor has 1,600 physical EHP, and with 20 armor, 2,200. The constant is different from League's because Dota's armor numbers are small, but the shape and the lesson are identical.

**Classic World of Warcraft** reduces physical damage by `A / (A + 400 + 85L)` for attacker levels 1-59, where `L` is the attacker's level, capped at 75%. So `K = 400 + 85L`, and `EHP = HP × (1 + A/K)` is linear up to the cap. Against a level-50 attacker, `K = 400 + 4,250 = 4,650`. The cap of 75% means `f = 0.25` and EHP = 4 × HP, which you reach at `A = 3K = 13,950`. Past that point the line goes flat, and armor adds nothing. Classic WoW has two extra lessons here. First, K grows with the attacker's level, so the same armor gives a smaller EHP slope against stronger enemies. Second, the cap changes the shape. Linear, then dead.

**Diablo II** handles elemental damage with resistances that work as linear percent: 40% fire resistance means you take 60% of fire damage. The default maximum is 75%, and some items raise the maximum to at most 95%. Now apply the EHP lens:

| Fire resistance | Fraction taken | EHP multiplier | Gain from the last step |
|---|---|---|---|
| 0% | 100% | 1.00× | — |
| 25% | 75% | 1.33× | +33% |
| 50% | 50% | 2.00× | +50% |
| 74% | 26% | 3.85× | — |
| 75% (default cap) | 25% | 4.00× | +4.0% from 74% |
| 80% (raised cap) | 20% | 5.00× | +25% from 75% |

Linear percent has **increasing** returns in survival. The last 25 points of resistance (50% to 75%) double your EHP, while the first 25 add a third. This is why resistances near the cap matter so much in Diablo II, and why items that raise the maximum are valuable. Going from a 75% to an 80% cap is a quarter more survival against that element. The expansion Lord of Destruction also subtracts 100 from all resistances in Hell difficulty. A character with no resistance gear there sits at −100%, takes double damage, and has an EHP multiplier of 0.5. They need 175 points of resistance from gear just to reach the cap.

Three games and three presentations. In League, Dota 2 and classic WoW, EHP is a straight line in armor, so every point is worth the same (until WoW's cap). In Diablo II, EHP bends upward, so every point is worth more than the last until the cap stops it. The percentage view hides both facts.

### Design judgment

Which mitigation curve you choose decides how players value defense, whether you intend it or not.

**The divisive formula gives constant returns in EHP.** That is its great strength. You can hand out armor throughout a long progression and it never becomes worthless and never explodes. There is no point at which a player "should stop" stacking it, so it doesn't force every build to one number. The cost is legibility. The tooltip percentage will convince players that armor is falling off. If that misreading matters to you, show EHP or "survives N more hits" instead of, or alongside, the percentage.

**Linear percent gives increasing returns, so it needs a cap.** Without a cap, 100% means immunity. With a cap, the cap becomes a target every serious player aims for, and every point beyond it is dead. That can be a good thing. In Diablo II, the −100 Hell penalty means a character needs 175 points of resistance from gear to reach the cap, which turns the cap into a gear check for the hardest difficulty. It is a bad thing when you wanted players to make trade-offs, because a capped stat with increasing returns has only one right answer, "max it."

**Caps turn any curve into a cliff.** Classic WoW's 75% armor cap sits at three times K, and K grows with attacker level, so the armor needed to reach it keeps rising as enemies get stronger. Below the cap, armor is linear in EHP. At the cap, it stops. For a designer, a cap placed within reach is a decision about where a build stops. A cap placed out of reach is a safety rail. Know which one you placed.

**Exponential-per-point mitigation is almost never what you want.** It looks like the hyperbola on a percent chart, and it has increasing returns with no natural limit. At 300 points, `0.99^300 ≈ 0.049`, an EHP multiplier near 20×. If you find this shape in a design document, it is probably an accident of someone multiplying "1% reduction per point" instead of adding it.

So decide what return you want players to get from the next point of defense (constant, rising or falling), then pick the formula that produces it in EHP, not in the percentage.

### Check the model

1. A game uses `K = 250`. How much armor gives 60% mitigation? What is the EHP multiplier?
2. A Dota 2 hero has 1,200 HP and 8 armor. What is their physical EHP? How much does one more point of armor add?
3. In Diablo II, a character goes from 60% to 75% cold resistance. By what factor does their EHP against cold damage change?

Answers are in the Check yourself section at the end.

## 3. EHP against mixed damage

Real enemies deal more than one kind of damage. Suppose a fight is 60% physical and 40% magical by raw damage, and your character has separate armor and magic resistance, both divisive with `K = 100`. The fraction of all raw damage that gets through is the weighted average:

```
f_total = 0.6 × f_phys + 0.4 × f_mag
EHP = HP / f_total
```

Take 1,000 HP, 100 armor (`f_phys = 0.5`) and 0 magic resistance (`f_mag = 1`).

```
f_total = 0.6 × 0.5 + 0.4 × 1.0 = 0.70      EHP = 1,429
```

You have 100 points to spend on one resistance. Option A, 100 more armor, gives `f_phys = 1/3`:

```
f_total = 0.6 × 0.333 + 0.4 × 1.0 = 0.60     EHP = 1,667
```

Option B, 100 magic resistance, gives `f_mag = 0.5`:

```
f_total = 0.6 × 0.5 + 0.4 × 0.5 = 0.50       EHP = 2,000
```

Option B wins by a wide margin, even though only 40% of incoming damage is magical. The reason is that the unprotected damage type dominates `f_total`. This gives you a rule to teach players and to build into encounters. **Raise the defense you have least of, weighted by how much of that damage you face.** As a designer, you control the weights. An encounter that is 90% magical damage punishes a character built only for armor, and that is a legitimate way to ask players to adapt.

### Dodge and block as mitigation

Some defenses don't reduce each hit; they remove some hits entirely. A 20% chance to dodge means that, on average, 80% of hits land. In expectation (the long-run average from [MA102 week 4](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md)), that is `f = 0.8`, and it stacks multiplicatively with armor like any other layer:

```
f = (1 − dodge) × K / (A + K)
```

With 20% dodge and 100 armor at `K = 100`, `f = 0.8 × 0.5 = 0.4`, an EHP multiplier of 2.5. The difference from armor is **variance**. Armor makes every hit smaller. Dodge makes some hits vanish and leaves others at full size. Over a long fight they give the same EHP. Over three hits, a dodge character can take all three at full damage and die much earlier than the average says. [Week 6](w06-critical-hits-and-variance.md) on critical hits and variance returns to this.

## 4. Spending a defensive budget: health or armor?

Because `EHP = HP × (1 + A/K)`, armor and health multiply each other. Each armor point adds `HP/K` EHP, so armor is worth more to a character with lots of health. Each health point adds `1 + A/K` EHP, so health is worth more to a character with lots of armor. That means the best defense is a mix, and you can compute the best mix.

Suppose one budget point buys either `a` armor or `h` health. The EHP-maximizing split is where the last point spent on each gives the same EHP:

```
(HP / K) × a = (1 + A/K) × h
which simplifies to    HP / h = (A + K) / a
```

Try it. A character starts with 500 HP and 0 armor, `K = 100`, and has 100 budget points. One point buys 50 HP or 5 armor. Let `x` points go into health.

```
HP = 500 + 50x        A = 5 × (100 − x) = 500 − 5x
EHP = (500 + 50x) × (1 + (500 − 5x)/100) = (500 + 50x)(6 − 0.05x)
```

| Points into health (x) | HP | Armor | EHP |
|---|---|---|---|
| 0 | 500 | 500 | 3,000 |
| 25 | 1,750 | 375 | 8,313 |
| 55 | 3,250 | 225 | 10,563 |
| 75 | 4,250 | 125 | 9,563 |
| 100 | 5,500 | 0 | 5,500 |

The peak is at `x = 55`. Check it with the rule. `HP / h = 3,250 / 50 = 65`, and `(A + K) / a = 325 / 5 = 65`. Equal, so no single point would do more good moved to the other side. The extremes are poor. All armor gives 3,000 EHP, all health 5,500, and the balanced split more than 10,500.

For a designer, this has a direct use. Players will find the balanced split, so **your prices for health and armor decide what a "correct" tank build looks like.** If you want tanks to carry mostly health, make armor expensive. If you want armor-heavy tanks, make health expensive. Set the prices on purpose, and use this calculation to check where they lead. [Week 9](w09-item-budgets-and-stat-weights.md) (item budgets and stat weights) generalizes this pricing to every stat.

## In-class activity (25 minutes)

Work in pairs. You are tuning defense for a level 1-30 RPG with one tank class.

**Materials:** the interactive, a spreadsheet.

1. (5 min) Choose a mitigation model (divisive, linear with cap, or divisive with a cap) and write one sentence on what return the next point of defense should give at level 30 (constant, rising, falling).
2. (8 min) For a level-30 tank with 3,000 HP, find the defense value that gives 60% mitigation under your model. Compute the EHP multiplier and the EHP, and check them in the interactive.
3. (7 min) Your level-30 boss deals 70% physical and 30% fire damage. The tank has 60% physical mitigation and 0% fire. Compute weighted EHP. Then compute it again after adding 30% fire resistance, and after adding enough armor to reach 70% physical. Which is better?
4. (5 min) Write one sentence to put on the tooltip that tells players the truth about armor under your model.

**Expected output:** the chosen model with a one-sentence rationale, three EHP numbers with working, a comparison, and a tooltip sentence.

## Common misconceptions

- **"Armor has diminishing returns."** In the mitigation percentage, yes. In EHP, which measures survival, the divisive formula gives constant returns. Always ask which quantity someone means.
- **"Linear percent is the safe, simple choice."** It has increasing returns in survival and explodes at 100%. It is safe only with a cap, and the cap then becomes the only target.
- **"If 60% of damage is physical, armor is the better buy."** Not if you have much more armor than resistance. The weakest defense dominates the weighted `f`, so raise the one you have least of, weighted by exposure.
- **"Dodge and armor are interchangeable because they give the same EHP."** They give the same average. Dodge adds variance, and short fights are decided by variance.

## Check yourself

1. A game uses `K = 250`. How much armor gives 60% mitigation? What is the EHP multiplier?
2. A Dota 2 hero has 1,200 HP and 8 armor. What is their physical EHP? How much does one more point of armor add?
3. In Diablo II, a character goes from 60% to 75% cold resistance. By what factor does their EHP against cold damage change?
4. A character has 2,000 HP and 150 armor at `K = 100`. They can add 30 armor or 300 HP. Which adds more EHP, and by how much?
5. A designer proposes "each point of Toughness gives 1% damage reduction, no cap, and Toughness drops on every item." Predict what happens to the game and give one concrete fix.

<details>
<summary>Answers</summary>

1. `A / (A + 250) = 0.6`, so `A = 0.6A + 150`, `0.4A = 150`, `A = 375`. EHP multiplier `1 + 375/250 = 2.5×`.
2. `EHP = 1,200 × (1 + 0.06 × 8) = 1,200 × 1.48 = 1,776`. One more point adds `0.06 × 1,200 = 72` EHP.
3. At 60% the fraction taken is 0.4, multiplier 2.5×. At 75% it is 0.25, multiplier 4×. EHP rises by a factor of 4 / 2.5 = 1.6.
4. Current EHP = 2,000 × 2.5 = 5,000. 30 armor adds `2,000/100 × 30 = 600`, giving 5,600. 300 HP adds `300 × 2.5 = 750`, giving 5,750. Health wins by 150 EHP.
5. EHP = HP / (1 − T/100) grows without limit as Toughness approaches 100, and at 100 the character is immune. Players stack Toughness above everything, and late-game characters become unkillable. Fixes: switch to a divisive formula `T / (T + K)`, or add a cap (for example 75%) and accept that players will stack to the cap and stop.

</details>

## Lab / assignment hook

**Lab 03: Effective HP and the defensive budget** ([labs/lab03.md](../labs/lab03.md)). You extend the Lab 02 sheet with EHP columns for four mitigation models, add a mixed-damage calculator, and find the optimal health-armor split for three price settings. Deliverable: the sheet and a 400-word memo recommending a mitigation model for your in-class RPG.

## Sources

- League of Legends Wiki, "Armor": damage multiplier `100 / (100 + armor)` for non-negative armor. Current as of 2025-2026 seasons.
- Dota 2 Wiki (Fandom), "Armor" and "Armor/Changelogs"; Valve, Dota 2 patch 7.27 notes (June 2020, dota2.com/patches/7.27): multiplier `1 − 0.06A / (1 + 0.06|A|)`.
- Warcraft Wiki, "Damage reduction", and Wowpedia, "Armor": `armor / (armor + 400 + 85 × attacker level)` for attacker levels 1-59, 75% cap. Classic era (patch 1.x) and the 2019 Classic re-release.
- Blizzard, Diablo II: Lord of Destruction "Resistances" page (classic.battle.net/diablo2exp/basics/resistances.shtml), and Diablo Wiki (Fandom), "Resistances (Diablo II)": default maximum resistance 75%, raisable to 95% by some items; Lord of Destruction resistance penalties 0 / −40 / −100 in Normal / Nightmare / Hell.
- candlesan, "The Simple Math Hiding in Your Favorite Games" (YouTube Short): the framing of armor as a formula designers should choose deliberately.
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press. Chapter 10.
- Schreiber, I. (2010). *Game Balance Concepts*, Level 3. gamebalanceconcepts.wordpress.com.

## Interactive spec: examples/w03-effective-hp.html

**Purpose.** Signature worked example for GD203: effective HP is linear in armor. Every point is worth the same, and the "diminishing returns" is an illusion of the percent view.

**The one insight.** Two linked charts share one armor axis. The left (mitigation %) bends and its "gain from the last 100" bracket shrinks. The right (EHP) is a straight line and its bracket stays the same height. Switching models shows that curves which look alike in percent look completely different in EHP.

**Layout.** Two charts side by side on desktop, stacked on mobile (percent above, EHP below), sharing one x axis range and one armor marker.

- **Left chart, "Mitigation (what the tooltip shows)."** x axis armor `A` 0-400. y axis mitigation 0-100%. The current model's curve, a marker at the current `A`, and a bracket showing mitigation gained between `A − 100` and `A` (hidden when `A < 100`), labeled "+X.X points from the last 100".
- **Right chart, "Effective HP (how long you live)."** Same x axis. y axis EHP from 0 to an automatic maximum (clamp display at 20 × HP and show "off chart" above it). Curve `EHP = HP / f(A)`, marker, and a bracket "+X EHP from the last 100".
- **Readout row** under the charts: Armor, Mitigation (1 decimal %), EHP (integer), Hits to die = `ceil(EHP / hit)` with hit size shown, EHP per armor point at the current `A` (the derivative, 1 decimal).

**Controls.**
- Slider armor `A`: 0-400, step 1, default 300.
- Slider `HP`: 200-5,000, step 100, default 1,000.
- Slider `K` (divisive constant): 10-500, step 5, default 100. Hidden when the selected model does not use K.
- Number input hit size: default 250.
- Model select:
  - Divisive (default): `f = K / (A + K)`.
  - Linear 1% per point, cap 75%: `f = max(0.25, 1 − A/100)`.
  - Exponential 0.99 per point: `f = 0.99^A`.
  - Divisive with 75% cap: `f = max(0.25, K / (A + K))`.
- Toggle "Compare all models": draws all four curves faintly on both charts with a legend.

**Exact test values (HP = 1,000, K = 100, hit = 250; must match the lecture tables).**
- Divisive: A = 0 → 0.0%, 1,000 EHP, 4 hits. A = 50 → 33.3%, 1,500, 6. A = 100 → 50.0%, 2,000, 8. A = 200 → 66.7%, 3,000, 12. A = 300 → 75.0%, 4,000, 16. A = 400 → 80.0%, 5,000, 20. EHP per armor point is 10.0 everywhere. The right-chart bracket reads "+1,000 EHP from the last 100" at every A ≥ 100; the left bracket reads +50.0, +16.7, +8.3, +5.0 at A = 100, 200, 300, 400.
- Linear with cap: A = 50 → 50.0%, 2,000 EHP. A = 74 → 74.0%, 3,846. A = 75 → 75.0%, 4,000. A = 200 → 75.0%, 4,000 (bracket "+0 EHP").
- Exponential: A = 100 → 63.4%, 2,732 EHP. A = 300 → 95.1%, 20,391 EHP (off chart at default scale; readout still exact).
- Divisive with cap: A = 300 → 75.0%, 4,000; A = 400 → 75.0%, 4,000.

**Accessibility and style.** Palette from `templates/interactive-tokens.css`; each model has a token color plus a distinct line style. All values printed as text. Every control keyboard reachable with visible focus. Reduced motion disables curve morphing. No game names or art inside the visual.
