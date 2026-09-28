# MMO303 · Week 04 — Stacking Mitigation: Multiplicative Layers

**Why this matters:** Every MMO tank ends up with several damage-reduction effects running at once. Armor, a stance, a cooldown, a raid buff, a shield. The rule you choose for combining them decides whether a tank can ever become immune, how much each new effect is worth, and whether your patch notes can promise "a 20% reduction" and mean it.

**You will be able to:**
- Compute total damage taken and the effective-HP multiplier for any stack of percentage reductions, under additive and multiplicative rules.
- Convert any reduction into "doublings" of survival and add layers in that form.
- Recognize the same stacking rule in Path of Exile's increased/more modifiers and Diablo IV's damage buckets.
- Decide where flat reductions and absorb shields go in the order of operations, and predict what changes when you move them.

**Before class:** Schreiber & Romero, *Game Balance* (2021), the chapters on combat formulas and on transitive systems; reread the MMO303 week 2 lecture sections 4 and 5.

**Prerequisites from earlier courses:** [MMO303 week 2, armor and damage mitigation](w02-armor-and-damage-mitigation.md) (the `A / (A + K)` model and effective HP). [MMO303 week 3, effective HP and effective DPS](w03-effective-hp-and-effective-dps.md). [GD203 week 3, mitigation curves and effective HP](../../GD203-combat-and-progression-design/lectures/w03-mitigation-curves-and-effective-hp.md). [MA101 week 4, exponentials](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w04-exponentials-and-the-xp-curve.md) and [MA101 week 5, logarithms](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w05-logarithms-how-many-levels-until.md).

**Interactive:** [`examples/w04-mitigation-layers.html`](../examples/w04-mitigation-layers.html). Keep it open during section 2.

---

## 1. Layers, and why the combining rule is a design decision

A **mitigation layer** is any effect that scales down incoming damage by a fraction. We write each layer as its reduction `r`, a number between 0 and 1. A 30% damage-reduction buff is `r = 0.3`. Armor under the week 2 formula is a layer too, with `r = A / (A + K)`.

A **flat layer** subtracts a fixed amount instead, like a block that removes 200 damage from a hit. An **absorb** (or shield) is a pool of hit points that soaks damage before your real health does. We treat those two in section 4. For now, only percentages.

The moment a character has two percentage layers, you need a rule for combining them. There are two obvious candidates.

- **Additive stacking.** Add the reductions, then apply the sum once. A 30% layer and a 20% layer give 50%.
- **Multiplicative stacking.** Apply each layer to whatever damage survived the previous one. A 30% layer leaves 70% of the damage, and a 20% layer leaves 80% of that, so 56% gets through. Total reduction is 44%.

Neither rule is the law of nature. Both have shipped in commercial games, often in the same game for different stat categories. The point of this week is that the choice has consequences you can compute in advance, and you should compute them before you ship.

Designers who pick by reflex tend to pick additive, because the tooltip math is friendly. Then a player finds five items that each say "10% less damage taken," adds a talent and a buff, and reaches 100%. The patch that fixes it has to invent a cap. Caps create their own problems, as you saw with linear-percent armor in week 2.

## 2. Worked example: 75% plus 75% is not 150%

### The hook

In classic World of Warcraft (the 2019 re-release of the 1.12-era game), armor reduces physical damage and is capped at 75% reduction. Warriors also have a cooldown called Shield Wall, which reduces all damage taken by 75% for 10 seconds.

So picture a warrior at the armor cap pressing Shield Wall. Add the numbers the way a new player would. 75% plus 75% is 150%. Does the warrior now heal from every hit?

Of course not. The warrior takes 6.25% of the incoming physical damage. That is a 93.75% reduction. It is a huge number, but it is not immunity, and the gap between "93.75%" and "100%" is where all the interesting design lives.

### The model

Damage passes through each layer in turn. Each layer lets through the fraction `(1 − r)`.

```
taken      = D × (1 − r1) × (1 − r2) × ... × (1 − rn)
reduction  = 1 − (1 − r1)(1 − r2)...(1 − rn)
EHP        = HP / [(1 − r1)(1 − r2)...(1 − rn)]
multiplier M = 1/(1 − r1) × 1/(1 − r2) × ... × 1/(1 − rn)
```

- `D` is the raw incoming damage.
- `r_i` is layer `i`'s reduction, from 0 to just under 1.
- `HP` is the character's health. `EHP` (effective HP) is the raw damage the character can absorb before dying, as defined in week 2.
- `M` is the EHP multiplier. It says how many times longer the character survives compared with no mitigation at all.

The key line is the last one. **Each layer multiplies survival by its own factor `1/(1 − r)`, independent of every other layer.** A 20% layer always multiplies EHP by 1.25. A 50% layer always doubles it. A 75% layer always quadruples it. It does not matter what else is stacked.

For the warrior, `M = 4 × 4 = 16`. At the armor cap with Shield Wall up, the warrior lasts sixteen times as long as an unarmored target with the same health.

### Doublings: turning multiplication into addition

Multiplying is harder to do in your head than adding, so take logarithms. Define a layer's **doublings** as

```
doublings(r) = −log2(1 − r)
```

A doubling is one factor of two in survival time. Now the whole stack is

```
total doublings = doublings(r1) + doublings(r2) + ... + doublings(rn)
M = 2 ^ (total doublings)
```

Some values you should memorize, because they make stack math fast:

| Reduction `r` | Damage let through | EHP factor `1/(1 − r)` | Doublings |
|---|---|---|---|
| 10% | 90% | 1.111 | 0.152 |
| 20% | 80% | 1.25 | 0.322 |
| 30% | 70% | 1.429 | 0.515 |
| 50% | 50% | 2 | 1 |
| 75% | 25% | 4 | 2 |
| 87.5% | 12.5% | 8 | 3 |
| 90% | 10% | 10 | 3.32 |

The warrior's armor cap is 2 doublings. Shield Wall is 2 doublings. Total 4, and `2^4 = 16`. Armor from week 2 fits in too. In League of Legends 100 armor is 50% reduction against physical damage, which is exactly 1 doubling. 300 armor is 75%, 2 doublings.

This is the same insight as week 2, one level up. In week 2 you learned that the mitigation percentage misleads and EHP tells the truth. This week, reduction percentages *combine* in a misleading way, and doublings combine in the honest way. Multiplicative layers are additive in doublings.

### Numbers you can check

Stack identical 20% layers, one at a time, under both rules. Take a 10,000 HP tank.

| Layers | Multiplicative: let through | Multiplicative: reduction | Multiplicative: EHP | Additive: let through | Additive: EHP |
|---|---|---|---|---|---|
| 0 | 100% | 0% | 10,000 | 100% | 10,000 |
| 1 | 80% | 20% | 12,500 | 80% | 12,500 |
| 2 | 64% | 36% | 15,625 | 60% | 16,667 |
| 3 | 51.2% | 48.8% | 19,531 | 40% | 25,000 |
| 4 | 40.96% | 59.04% | 24,414 | 20% | 50,000 |
| 5 | 32.77% | 67.23% | 30,518 | 0% | infinite |

Verify two rows by hand. Row 3 multiplicative is `0.8 × 0.8 × 0.8 = 0.512`, and `10,000 / 0.512 = 19,531`. Row 4 additive is `1 − 4 × 0.2 = 0.2`, and `10,000 / 0.2 = 50,000`.

Read the columns in the way week 2 taught you. Under multiplicative stacking, every row multiplies EHP by 1.25. The fifth layer is worth exactly what the first was, in relative terms. Under additive stacking, each layer is worth more than the one before. The fourth layer doubles EHP, and the fifth makes the tank immortal. That is the runaway you must plan for.

### The visual

Open the interactive. The left panel is a bar showing the fraction of damage let through, with each layer drawn as a slice cut off the bar. The right panel shows the same stack as blocks on a doublings axis, where every layer is a block of width `−log2(1 − r)`.

Start with the "five 20% layers" preset. On the left, the slices shrink as you add layers: 20 points, then 16, then 12.8. It looks like each layer does less. On the right, the five blocks are identical. Each one adds 0.322 doublings. Same numbers, two views. Now flip the stacking rule to additive. The left bar hits zero at the fifth layer, and the right panel's last block runs off the edge of the axis to infinity.

Then load the "classic warrior" preset. Two blocks of exactly 2 doublings each, `M = 16`, and a let-through bar at 6.25%.

### Cross-game recognition

The same idea shows up on the damage side of many games. There it is written as "bonuses," and the question is whether bonuses add inside a pool or multiply across pools. The math is identical, with `(1 + b)` in place of `(1 − r)`.

**Path of Exile.** The game's modifier text uses two families of words on purpose. Modifiers that say "increased" or "reduced" are added together into one pool. Modifiers that say "more" or "less" each multiply the result separately. The official wiki's worked case uses 100% increased damage from gear, 100% increased from passives, and a support gem with 100% more damage. The increased values sum to 200%, giving a factor of 3, and the more modifier doubles it, so a 1,000 base becomes 6,000. The two increased sources sit in one additive pool, and the more source is a separate multiplicative layer.

**Diablo IV.** Item and skill text marks additive bonuses with `[+]` and multiplicative ones with `[x]`. All the `[+]` damage bonuses sum into one pool, often called the additive bucket, and each `[x]` multiplier applies on its own. Community damage guides for the game's seasonal era advise stacking across several buckets rather than piling into one, which is the doublings argument in plain words.

**Classic WoW, the hook.** Armor and Shield Wall are two separate layers that multiply. The 75% armor cap limits armor alone to 2 doublings. The cap does not stop other layers from adding their own doublings on top.

Put all three in one form. A pool is a group of effects that add before being turned into a factor. Layers are factors that multiply. Every game in this list uses both. The designer decides which effects go into which pool.

### The dilution effect

Additive pools have one consequence that players notice and designers sometimes forget. Adding more to a big pool is worth less and less. Suppose a character already has +200% increased damage. Their factor is 3.0. One more +20% increased makes it 3.2, a real gain of `3.2 / 3.0 − 1 = 6.7%`. A +20% more modifier instead gives a full 20% gain, since it multiplies the 3.0 on its own.

Defense mirrors this but with the opposite sign. An additive defense pool gets *more* valuable per point as it grows, because you are closing in on 100%. That is why additive pools are safe on offense and dangerous on defense. On offense, dilution slows runaway growth for you. On defense, additive stacking creates it.

### Eyes-open design judgment

Multiplicative stacking is the default for defensive layers in most modern MMOs for good reasons, but it has costs you must accept deliberately.

- **Strength.** No stack of layers below 100% can reach 100%. You never need a global cap to prevent immunity, though you may still want one to prevent near-immunity.
- **Strength.** Each layer's value is independent of the others. A designer can price a "20% damage reduction" cooldown once, as 0.322 doublings, and know it will mean the same thing on every character.
- **Cost.** Tooltips lie in the other direction. A player who sees "20% reduction" three times expects 60% and gets 48.8%. Show the combined total on the character sheet, or players will file bug reports.
- **Cost.** Near-immunity is still reachable. Four 75% layers let through 0.39% of damage, which is `M = 256`. If your content has any way to stack cooldowns, you need a rule about it (shared cooldowns, a diminishing layer, or boss abilities that ignore some layers).
- **When additive makes sense.** On offense, additive pools give you dilution, which is a free brake on power growth. On defense, additive stacking works only if the pool is small and hard-capped, like a single "damage reduction from gear" stat that tops out at 20%.

The mature approach is the one Path of Exile and Diablo IV both use. Put most effects into a few additive pools, keep a small number of true multiplicative layers, and make the text tell players which is which.

## 3. Where caps go

A cap is a maximum on reduction. With layers, you must decide what the cap applies to. The choice changes the numbers a lot.

**Per-layer cap.** Each layer has its own limit. Classic WoW's 75% armor cap is one of these. It stops armor from exceeding 2 doublings. Other layers still stack on top.

**Total cap.** The combined reduction cannot exceed a value. If the total cap is 90%, then `M` can never exceed 10, or 3.32 doublings, no matter what the player stacks. Once a player hits it, every further layer is worthless. A total cap is simple to reason about, but it creates the same "stack to the cap and stop" behavior that linear armor did in week 2, only one level higher.

**Soft cap on the total.** You can compress the total instead of clipping it. For example, compute total doublings `d`, then use `d' = d` for `d ≤ 3` and `d' = 3 + 0.5 × (d − 3)` above that. Every layer still helps, just less past 8× survival. This is more work to explain, and the tooltip must show the compressed number.

Work through the per-layer case. A tank has 70% armor, a 40% stance and a 50% cooldown. Multiplicative, no total cap:

```
let through = 0.30 × 0.60 × 0.50 = 0.09     → 91% reduction, M = 11.1
doublings   = 1.737 + 0.737 + 1 = 3.474      → 2^3.474 = 11.1
```

With a total cap at 90%, the tank sits at `M = 10`. The cooldown, which should have doubled survival, only raised it from `1/(0.30 × 0.60) = 5.56` to 10, a factor of 1.8. A designer reading a patch note that says "cooldown reduces damage by 50%" would be wrong about what it does on this tank. That is a reason to avoid total caps or to document them loudly.

## 4. Flat layers, absorbs and the order of operations

Pure percentage layers commute. `0.8 × 0.5` equals `0.5 × 0.8`, so order does not matter. The moment a flat subtraction or an absorb enters the stack, order matters and your spec must state it.

### Flat reductions

Take a 1,000 damage hit, a flat block of 200, and a 50% layer.

```
subtract, then multiply: (1000 − 200) × 0.5 = 400
multiply, then subtract: 1000 × 0.5 − 200  = 300
```

The flat block is worth 100 damage in the first order and 200 in the second. Flat reductions applied late, after percentages, are worth their full face value. Flat reductions applied early get shrunk by every percentage layer after them. Against small hits, a late flat block can reduce damage to the minimum; against large hits, it barely matters. That is the same hit-size dependence you saw with subtractive armor in week 2.

### Absorbs

An absorb shield of size `S` soaks `S` damage *after* whatever layers sit in front of it. If the layers in front let through a fraction `f`, the shield is worth `S / f` raw damage.

A 2,000-point shield on a tank with 75% mitigation lets through `f = 0.25`, so the shield is worth 8,000 raw damage. The same shield on a caster with no mitigation is worth 2,000. Healers who cast shields on tanks are therefore getting four times the value per cast, which is one reason absorb-heavy healers are balanced around who they shield. If you put absorbs *before* mitigation in the order, the shield is worth exactly `S` on everyone, which is easier to balance and less interesting to play.

### A spec you can hand to a programmer

Write your damage pipeline as a numbered list, and publish it to the team. A reasonable default is:

1. Raw damage `D` from the attacker, after the attacker's own bonuses.
2. Attacker penetration applied to the defender's armor.
3. Armor layer `A / (A + K)`.
4. Other percentage layers, multiplied.
5. Flat reductions, with a minimum of 1 damage.
6. Absorb shields.
7. Health.

Each position is a choice. Moving flat reductions from step 5 to step 3, or absorbs from step 6 to step 2, is a balance change as large as any number tweak, and it deserves a patch note.

## 5. Budgeting a tank's cooldowns in doublings

Doublings make a tank's toolkit easy to reason about. Suppose a boss has an ability that hits for 60,000 raw damage every 30 seconds, and the tank has 25,000 HP. To survive without help, the tank needs `M ≥ 60,000 / 25,000 = 2.4`, which is `log2(2.4) = 1.26` doublings.

If passive armor provides 1 doubling (50%), the tank needs 0.26 more doublings for the big hit. A 20% cooldown provides 0.322. That is enough. A 15% cooldown provides 0.234, which is not, and the tank dies at `25,000 × 2 × 1/0.85 = 58,824` raw damage, just short.

Designers can build a whole encounter this way. Choose the doublings a tank must bring to each mechanic. Give the tank a set of cooldowns whose doublings and durations cover the mechanics with a little slack. Then check the case where the tank has used the wrong cooldown on the previous hit. That is where a healer's absorb, valued at `S / f`, becomes the save.

## In-class activity (25 minutes)

Work in pairs. You are designing the defensive kit for a new tank class in a game where armor gives at most 60% reduction.

1. Give the tank one passive stance and two cooldowns. Choose each reduction and duration.
2. Convert every layer to doublings. Compute `M` for the worst case (passive only) and the best case (all layers).
3. The encounter team says the boss's heaviest hit is 4.5 times the tank's health. Show which combination of layers survives it, using doublings only.
4. Swap kits with another pair. Rewrite their kit under additive stacking. Find the first combination that reaches or exceeds 100%, or show that none does.

Expected output: a half-page table per pair with reductions, doublings, `M`, and a one-sentence verdict on whether the kit needs a shared cooldown rule.

## Common misconceptions

- **"Two 50% reductions make 100%."** Under multiplicative stacking, two 50% layers let through 25%. That is 2 doublings, or 4× survival.
- **"Later layers are weaker because the percentage gain shrinks."** Each layer multiplies survival by the same factor regardless of position. The shrinking percentage points are the same illusion as week 2's armor table.
- **"Additive stacking is simpler, so it's safer."** It is simpler to display. It is less safe on defense, because each new layer is worth more than the last and the sum can reach 100%.
- **"Order of operations doesn't matter."** It does not matter among pure percentage layers. It matters as soon as flat reductions or absorbs join the pipeline.

## Check yourself

1. A character has three layers: 40%, 25% and 10%, stacked multiplicatively. What fraction of damage gets through? What is the EHP multiplier? How many doublings is that?
2. The same three layers are changed to add inside one pool. What is the new multiplier? Which rule makes the 10% layer worth more, and by how much in EHP terms, for a 20,000 HP character?
3. A healer's 3,000-point absorb goes on a tank who lets through 20% of damage, and the absorb sits after mitigation. What raw damage does the shield absorb? What if absorbs are moved before mitigation?
4. A designer says "we'll let tanks stack as many cooldowns as they like, because multiplicative stacking can never reach 100%." Explain the problem using doublings.

<details>
<summary>Answers</summary>

1. `0.6 × 0.75 × 0.9 = 0.405`, so 40.5% gets through (59.5% reduction). `M = 1/0.405 = 2.469`. Doublings `= log2(2.469) = 1.304`, which also equals `0.737 + 0.415 + 0.152`.
2. Additive total is 75%, so `M = 4`. Under additive stacking, removing the 10% layer drops the pool to 65% and `M` to 2.857, so the layer adds `20,000 × (4 − 2.857) = 22,857` EHP. Under multiplicative stacking, removing it leaves `M = 1/(0.6 × 0.75) = 2.222`, so it adds `20,000 × (2.469 − 2.222) = 4,938` EHP. The additive rule makes the same 10% worth more than four times as much.
3. After mitigation it absorbs `3,000 / 0.2 = 15,000` raw damage. Before mitigation it absorbs exactly 3,000 raw damage.
4. Each extra cooldown still adds its doublings. Four 75% layers give 8 doublings, `M = 256`, so a 25,000 HP tank would need 6.4 million raw damage to die. The tank is effectively immune even though the math says "not 100%." You need a stacking rule for cooldowns, a total soft cap, or mechanics that bypass some layers.

</details>

## Lab hook

**Lab 04, mitigation stack audit** ([`labs/lab04.md`](../labs/lab04.md)). You build a damage pipeline sheet that takes a list of layers, flat reductions and absorbs in a stated order, reports let-through, doublings and EHP, and audits a provided tank kit for runaway combinations.

## Sources

- Warcraft Wiki, "Armor" and "Damage reduction". Classic era (patch 1.12 rules, re-released as WoW Classic in 2019): armor reduction for attacker levels 1 to 59 and the 75% armor cap. https://warcraft.wiki.gg/wiki/Armor
- Wowhead Classic database, "Shield Wall" (spell 871). Classic WoW: reduces damage taken from melee, ranged and spells by 75% for 10 seconds. https://www.wowhead.com/classic/spell=871/shield-wall
- Path of Exile Wiki, "Stat" and "Modifier". Path of Exile 1 (current live rules): increased/reduced modifiers add, more/less modifiers multiply; the 100% + 100% increased with 100% more example. https://pathofexile.fandom.com/wiki/Stat
- League of Legends Wiki, "Armor". Current live formula `100 / (100 + armor)`, used for the 1-doubling-per-100-armor conversion. https://leagueoflegends.fandom.com/wiki/Armor
- Maxroll, "In-Depth Damage Guide in Diablo 4", and Mobalytics, "Diablo 4 Damage Buckets Explained (updated Season 2)". Diablo IV 2023 to 2024 seasonal era: `[+]` bonuses sum into one additive bucket, `[x]` bonuses multiply separately. https://maxroll.gg/d4/resources/in-depth-damage-guide
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press.

## Interactive spec: examples/w04-mitigation-layers.html

**The one insight.** Percentage layers look weaker the more you stack them, but on a doublings axis every layer is a block of fixed width, so multiplicative stacking gives constant returns in survival. Additive stacking gives runaway returns and hits immunity.

**Layout.** Two linked panels side by side on desktop, stacked on mobile.

- **Left panel, "Damage let through".** A horizontal bar from 0% to 100%. Starting from a full bar, each layer in order removes a slice equal to `r_i × (current remaining)` in multiplicative mode, or `r_i` of the original in additive mode. Draw each slice in a distinct palette color with its label (e.g. "Layer 2: −16.0 pts"). The remaining let-through fraction is shown as a large number.
- **Right panel, "Survival in doublings".** A horizontal axis from 0 to 8 doublings, tick labels showing both doublings and `M` (1×, 2×, 4×, 8×, 16×, 32×, 64×, 128×, 256×). Each layer is a block of width `−log2(1 − r_i)` placed end to end, same color as its slice on the left. In additive mode, draw one combined block of width `−log2(1 − Σr)`, and if `Σr ≥ 1`, draw it running off the right edge with an "immune" label.

**Controls.**
- Up to 6 layers. Each has a slider for `r` from 0% to 95% in 1% steps, a numeric input, and a remove button. An "Add layer" button.
- Stacking rule: radio group with "Multiplicative", "Additive", "Two pools". In "Two pools" mode each layer has a toggle A/B; layers inside a pool add, and the two pool results multiply: `let through = (1 − ΣA) × (1 − ΣB)`, each pool clamped at 0.
- HP input (default 10,000) for the EHP readout.
- Presets: "Five 20% layers", "Classic warrior (75% armor cap + Shield Wall 75%)", "Check yourself Q1 (40/25/10)".
- Optional toggle "Show absorb" with an absorb size `S` (default 2,000) placed after the layers; readout shows its raw value `S / f`.

**Readouts (always visible, copyable).** Let-through fraction `f`, total reduction `1 − f`, `M = 1/f`, doublings `log2(M)`, EHP `= HP × M`, and a small table listing each layer's `r`, factor `1/(1 − r)` and doublings.

**Formulas.**
- Multiplicative: `f = Π(1 − r_i)`.
- Additive: `f = max(0, 1 − Σ r_i)`. If `f = 0`, show `M` and EHP as "infinite (immune)".
- Two pools: `f = max(0, 1 − ΣA) × max(0, 1 − ΣB)`.
- Doublings per layer: `−log2(1 − r_i)`.

**Test values (the build must reproduce these).**
- Five 20% layers, multiplicative: `f = 0.32768`, reduction 67.23%, `M = 3.052`, doublings 1.610, EHP 30,518 at 10,000 HP.
- Five 20% layers, additive: `f = 0`, immune. Four layers additive: `f = 0.2`, `M = 5`, EHP 50,000.
- Classic warrior 75% and 75%, multiplicative: `f = 0.0625`, `M = 16`, doublings 4.000.
- 40/25/10 multiplicative: `f = 0.405`, `M = 2.469`, doublings 1.304. Additive: `f = 0.25`, `M = 4`.
- Two pools, A = {20%, 20%}, B = {30%}: `f = 0.6 × 0.7 = 0.42`, `M = 2.381`.
- Absorb 2,000 after 75% total mitigation: raw value 8,000.

**First screen.** Loads with "Five 20% layers" in multiplicative mode, so the shrinking slices on the left and the identical blocks on the right are visible without touching anything.
