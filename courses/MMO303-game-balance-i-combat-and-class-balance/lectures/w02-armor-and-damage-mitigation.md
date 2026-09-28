# MMO303 · Week 02 — Armor and Damage Mitigation

**Why this matters:** Armor is the stat players misread most often, and the formula you pick for it quietly decides whether tanks work, whether swarms of weak enemies matter, and whether your endgame breaks when numbers grow. Designers who don't understand it tend to "fix" it into something worse.

**You will be able to:**
- Derive the effective-HP form of the divisive armor formula and explain why it is linear.
- Recognize the same formula when it's written differently (League of Legends, Diablo II, World of Warcraft, Path of Exile 2).
- Compare divisive, subtractive and linear-percent armor models and predict the problems each creates.
- Decide how to spend a defensive budget between armor and health.

**Before class:** Schreiber & Romero, *Game Balance* (2021), the chapter on combat formulas; GD203 week 3 (mitigation curves).

**Interactive:** [`examples/w02-armor-curve.html`](../examples/w02-armor-curve.html) — keep it open during section 2.

---

## 1. The puzzle players notice

In League of Legends, a champion with 100 armor takes half damage from physical attacks. Buy another 100 armor and they now take one third. Another 100 and they take one quarter.

Look at the mitigation percentages and it seems armor is getting worse with every purchase:

| Armor | Damage taken | Damage mitigated | Gain from last 100 armor |
|---|---|---|---|
| 0 | 100% | 0% | — |
| 100 | 50% | 50% | +50 points |
| 200 | 33.3% | 66.7% | +16.7 points |
| 300 | 25% | 75% | +8.3 points |
| 400 | 20% | 80% | +5 points |

Players call this "diminishing returns," and many designers believe them. The rest of this lecture shows why that reading is wrong for the question that actually matters (how long you survive), and when it is right.

## 2. Worked example: one formula, hiding everywhere

### The model

The family of formulas we care about has one shape:

```
mitigation = A / (A + K)
damage taken = D × K / (A + K)
```

- `A` is the defender's armor.
- `K` is a constant the designer chooses (it may depend on level or hit size — more on that shortly).
- `D` is the incoming damage before armor.

Notice what `K` means: when `A = K`, mitigation is exactly 50%. **K is the amount of armor that halves damage.**

### From percent to survival: effective HP

Players don't live or die by percentages. They die when health hits zero. So ask a better question: *how much raw damage can I absorb before dying?* That's **effective health (EHP)**:

```
EHP = HP / (1 − mitigation)
    = HP / (K / (A + K))
    = HP × (A + K) / K
    = HP × (1 + A/K)
```

That last line is the whole lesson. **Effective HP is a straight line in armor.** Every point of armor adds exactly `HP / K` effective health, whether it's your first point or your five-hundredth.

In League, `K = 100`, so each point of armor gives you **1% of your base health** as extra effective health against physical damage. 100 armor doubles your survival time; 200 triples it; 300 quadruples it.

Redo the table with a 1,000 HP champion:

| Armor | Mitigation | EHP | EHP gained from last 100 armor |
|---|---|---|---|
| 0 | 0% | 1,000 | — |
| 100 | 50% | 2,000 | +1,000 |
| 200 | 66.7% | 3,000 | +1,000 |
| 300 | 75% | 4,000 | +1,000 |
| 400 | 80% | 5,000 | +1,000 |

The percentage column bends. The EHP column is dead straight. Open the interactive now: drag the armor slider and watch the curve on the left flatten while the line on the right climbs at a constant rate. Same numbers, two views.

### Why the percent view lies

Going from 75% to 80% mitigation looks like a tiny +5 points. But look at damage *taken*: it drops from 25% to 20%, so you now take one fifth less damage than you did a moment ago. The closer you get to 100% mitigation, the more each percentage point is worth — which is exactly why the formula needs to hand them out more slowly. The two effects cancel perfectly, and what's left is a constant gain in survival.

A useful comparison: adding 1,000 HP to a 1,000 HP character doubles their health; adding it to a 5,000 HP character is only +20%. Nobody calls health "diminishing returns." Armor under this formula behaves exactly like health.

### Cross-game recognition

The formula rarely appears in its clean form. Learning to rewrite it is the skill.

**League of Legends.** Riot publishes the formula as a damage multiplier: `damage taken = damage × 100 / (100 + armor)` for non-negative armor. Subtract from 1 and you get `armor / (armor + 100)` — our formula with `K = 100`. League also handles negative armor with a separate branch, `2 − 100 / (100 − armor)`, so shredding a target below zero increases damage without the formula exploding.

**Diablo II.** Diablo II doesn't reduce damage at all — it changes whether you get hit. The chance to hit is `2 × AR / (AR + DR) × alvl / (alvl + dlvl)`, clamped between 5% and 95%, where AR is attack rating, DR is defense, and the last factor compares attacker and defender levels. When the levels are equal, that level factor is ½ and the chance to hit becomes `AR / (AR + DR)`. The chance to *miss* is then `DR / (DR + AR)` — our formula, with **the attacker's accuracy playing the role of K**. Any single swing either hits or misses, but over many swings the expected damage taken follows the same curve. Same principle, delivered as probability.

**World of Warcraft (classic era).** For attackers of level 1–59, armor reduces physical damage by `armor / (armor + 400 + 85 × attacker level)`, capped at 75%. Here `K = 400 + 85 × level`, so a level-50 attacker has `K = 4,650`. Making K grow with level is how the game stops armor from old gear trivializing new enemies: the same armor is worth less against a stronger attacker. The 75% cap limits the EHP multiplier to 4× (reached at `A = 3K`).

**Path of Exile 2.** Armour reduces a hit by `armour / (armour + 10 × damage)`, capped at 90%. Here **K depends on the size of the hit**. Armor is superb against many small hits and weak against one huge slam: with 1,000 armour, a 100-damage hit is halved, but a 1,000-damage hit is reduced by only about 9%. The first Path of Exile uses the same shape with a different multiplier, which has changed across patches — a reminder to always cite a formula's version.

Four games, four presentations, one idea. When you meet a new game's armor formula, your first move should be to try rewriting it as `A / (A + K)` and ask: *what is K here, and what does it depend on?*

## 3. The alternatives, and the problems they bring

Many designers find the divisive formula unnecessarily complex and reach for something "simpler." Each simpler model has a cost. Use the model-comparison tab in the interactive to see them side by side.

### Subtractive armor: `taken = max(minimum, D − A)`

Easy to read on a tooltip. But it makes armor's value depend entirely on hit size. Against a swarm of 20-damage hits, 15 armor removes 75% of the damage. Against a 500-damage boss attack, the same 15 armor removes 3%. Consequences:

- Weak enemies become harmless once armor passes their damage, so a whole category of content stops mattering.
- Enemies must hit harder as the game goes on just to register, which inflates every number in the game.
- You need a minimum-damage floor or players become literally immune.

Path of Exile's hit-size-dependent K is a softer version of this same trade-off — chosen deliberately, to make armour a defense against many small hits rather than a universal one.

### Linear percent: "each point of armor = 1% reduction"

Readable, and gains look constant on the tooltip. But survival time is `1 / (1 − mitigation)`, so as mitigation approaches 100%, EHP explodes: 90% means 10× survival, 99% means 100×. The designer must add a hard cap, and then every point past the cap is worthless, so players stack to the cap and stop. You've replaced a smooth curve with a cliff.

### The divisive formula, with eyes open

The divisive formula is not "correct"; it's a set of trade-offs you should choose knowingly:

- **Strength:** every point is worth the same in survival, so it never becomes worthless and never explodes. You can hand out armor freely across a long progression.
- **Strength:** K is a single tuning knob. Tie it to level (WoW) to control power creep, or to hit size (Path of Exile 2) to give armor a specific identity.
- **Cost:** the tooltip percentage misleads players into thinking armor is falling off. Consider showing EHP or "survives N more hits" instead.
- **Cost:** it treats all incoming damage alike unless K varies. If you want armor to have a counter-role (strong vs swarms, weak vs bosses), you need an extra design decision.

## 4. Stacking and ordering

### Mitigation layers multiply

Armor rarely acts alone. A tank with 50% armor mitigation who also gets a 20% damage-reduction buff does **not** reach 70% reduction. Damage passes through each layer in turn:

```
taken = D × (1 − 0.5) × (1 − 0.2) = 0.4 × D    → 60% total reduction
EHP multiplier = 2 × 1.25 = 2.5
```

Multiplicative layering is itself a design choice: it naturally prevents stacking to 100%, and it makes each layer's EHP multipliers compose cleanly.

### Penetration: order matters

Armor-reduction effects on the attacker's side ("ignore 30% of armor", "−20 armor") are applied to A *before* the formula. Whether flat or percentage reductions apply first changes results, so your spec must define the order explicitly and your tooltip must reflect it. Assign this as a spreadsheet exercise: compute the same scenario under both orders and compare.

## 5. Spending a defensive budget: armor or health?

Because `EHP = HP × (1 + A/K)`, each armor point adds `HP/K` EHP and each HP point adds `1 + A/K` EHP. If armor costs `c_A` per point and health costs `c_H` per point (in gold, stat budget, or item slots), the EHP-maximizing split satisfies:

```
HP × c_H = (A + K) × c_A
```

In words: the more health you have, the more valuable armor becomes, and vice versa. The best defense is balanced between them. This is why theorycrafters say "don't stack only one defensive stat," and why you as the designer should price the two so that sensible builds land in a range you like.

## In-class activity (25 minutes)

In pairs, design the armor system for a small MMO with levels 1–30.

1. Choose a K rule (constant, level-based, or hit-size-based). Justify it in two sentences.
2. Using the interactive's custom-K mode, find the armor a level-30 tank needs to reach 60% mitigation against a level-30 boss.
3. Decide whether you want a cap. If yes, what EHP multiplier does it imply?
4. Swap with another pair. Find one situation their system handles badly.

## Common misconceptions

- **"Armor has diminishing returns."** In mitigation percentage, yes. In survival time, no — every point adds the same EHP. Always ask which quantity someone means.
- **"Two 50% reductions make 100%."** Layers multiply: two 50% layers give 75%.
- **"Subtractive armor is simpler, so it's easier to balance."** It's easier to read and harder to balance, because its value depends on hit size.
- **"The tooltip percentage is what I get."** In games where K depends on attacker level (WoW) or hit size (Path of Exile), the tooltip shows the value against one reference attacker only.

## Check yourself

1. A game uses `K = 250`. How much armor gives 60% mitigation? How many times longer does that character survive than with 0 armor?
2. In League, a 2,000 HP champion with 150 armor buys 30 more armor. How much EHP does that add against physical damage? Would the same 30 armor add more or less EHP on a 3,000 HP champion?
3. Rewrite `damage taken = D × 600 / (600 + armor)` in mitigation form. What is K?
4. A designer proposes "each point of armor reduces damage by 1%, capped at 80%." Describe what players will do and why.

<details>
<summary>Answers</summary>

1. `A/(A+250) = 0.6` → `A = 375`. EHP multiplier `1 + 375/250 = 2.5×`.
2. Each armor point adds `HP/K = 2000/100 = 20` EHP, so 30 armor adds 600 EHP. On a 3,000 HP champion it adds 900 — armor is worth more on high-health characters.
3. Mitigation `= armor / (armor + 600)`, so `K = 600`.
4. They'll stack exactly 80 armor and stop, because every point past the cap is worthless and every point below it is increasingly valuable (70% → 80% cuts damage taken by a third). Builds converge, and items with armor above the cap become dead stats.

</details>

## Lab hook

**Lab 02 — Mitigation spreadsheet.** Build a sheet that computes mitigation, damage taken and EHP for the four games in section 2, then add your own formula from the in-class activity and plot all five on one chart. Deliverable: the sheet and a 300-word recommendation memo.

## Sources

- candlesan, "The Simple Math Hiding in Your Favorite Games" (YouTube Short) — the source of this lecture's framing; its description notes the Diablo II and League of Legends forms and argues designers should choose armor rules deliberately.
- League of Legends Wiki, "Armor" — damage multiplier `100/(100+armor)` and the negative-armor branch.
- The Amazon Basin (Diablo II), "Technical Formulas" — chance-to-hit formula and 5%/95% clamps.
- Warcraft Wiki, "Armor" and "Damage reduction" — `armor / (armor + 400 + 85 × level)` for attacker levels 1–59; 75% cap.
- Path of Exile 2 Wiki, "Armour" — `armour / (armour + 10 × damage)`, 90% cap, rules of thumb.
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press.
