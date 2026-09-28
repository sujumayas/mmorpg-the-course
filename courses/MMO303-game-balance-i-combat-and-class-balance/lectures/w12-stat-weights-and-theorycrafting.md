# MMO303 · Week 12 — Stat Weights and Theorycrafting

**Why this matters:** Your players will turn your combat formulas into a single number per stat and gear by it. If you know how those numbers are made, you can predict which items players will want, spot a stat that makes every other stat pointless, and set conversion rates so that gearing decisions stay interesting.

**You will be able to:**
- Compute a stat weight as a normalized marginal gain, both by derivative and by finite difference.
- Derive the best split of a stat budget for a product-of-sums damage formula and show that weights are equal at that split.
- Explain why stat weights change with gear, talents and fight type, and estimate how much simulation noise a weight can carry.
- Critique a stat system for dominant stats, cliffs at caps and homogenized items.

**Before class:** Schreiber & Romero, *Game Balance* (2021), the chapters on transitive mechanics and cost curves (item budgets); Raidbots, "Beware of Stat Weights" (short support article); SimulationCraft wiki, "StatsScaling" (the first two sections).

**Prerequisites from earlier courses:** item budgets and stat weights from [GD203 week 9](../../GD203-combat-and-progression-design/lectures/w09-item-budgets-and-stat-weights.md); the armor-versus-health budget rule in [MMO303 week 2](w02-armor-and-damage-mitigation.md), section 5; expected value and Monte Carlo simulation from MA102 [week 4](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md) and [week 11](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w11-monte-carlo-simulation.md).

**Interactive:** [`examples/w12-stat-weights.html`](../examples/w12-stat-weights.html) (built from the spec at the end of this lecture). Keep it open during section 2.

---

## 1. Theorycrafting and the stat weight

**Theorycrafting** is the player practice of reverse-engineering a game's combat formulas and using them to find the best choices. It began in forum threads where players pooled combat logs and spreadsheets. The best known is Elitist Jerks, a World of Warcraft raiding guild whose public forums were the center of WoW theorycrafting from the mid-2000s until the site went offline around 2016. Its guild master, Ion Hazzikostas, later joined Blizzard and became one of World of Warcraft's directors. The pipeline from theorycrafter to game designer is common, because the skills are the same. Theorycrafters model a game from the outside; designers model it from the inside.

Today much of theorycrafting runs through simulators. SimulationCraft is an open-source combat simulator for World of Warcraft, and web services such as Raidbots run it for players who paste in their character. One of the things these tools produce is a set of **stat weights**, which SimulationCraft calls **scale factors**.

A stat weight answers one question: **if I gain one point of this stat, how much DPS do I gain?** Formally, it is the partial derivative of DPS with respect to that stat, at the character's current gear:

```
raw weight of stat x = ∂DPS / ∂x
```

Raw weights are hard to compare across characters, because a character with better gear gains more DPS from everything. So tools usually **normalize** by the primary stat (strength, agility or intellect in WoW, or "power" in our examples). The primary stat gets weight 1.00, and every other stat is expressed relative to it:

```
normalized weight of x = (∂DPS/∂x) / (∂DPS/∂P)
```

A normalized weight of 0.25 for haste means "one point of haste is worth a quarter of a point of power, right now, for this character." Players multiply each stat on an item by its weight and add, which gives the item a single score. That is the same arithmetic as the item budget you built in GD203, used in reverse. The designer prices stats to make items. The player weights stats to rank them.

## 2. Worked example: the stat weight that changes when you gear

### The hook

SimulationCraft measures a scale factor by running the character's fight, adding a fixed number of points of one stat, running it again, and dividing the DPS difference by the number of points added. Raidbots, the most used front end for it, publishes an article warning its own users against leaning on the result. Its point is that stat weights are a snapshot of one character at one moment. Change a ring and the weights change. Two players of the same class and specialization, with different gear, get different weights.

Players find this confusing. If haste is "worth 0.24" for your class, how can it be worth something else for your friend? The answer is that a stat weight is not a property of a stat. It is a slope on a curve, and you are standing at a different place on that curve from your friend. This example shows what that curve looks like and where the top is.

### The model

A fictional MMO class deals damage with three stats:

- `P`, **power**: each point adds 1 to base damage per second.
- `c`, **crit chance**: the probability that a hit is a critical hit, which deals `m` times normal damage. We start with `m = 2`.
- `h`, **haste**: the fraction by which attack speed is increased. 10% haste means 10% more hits per second.

Crit and haste are bought with **rating**, a raw number on gear that the game converts to a percentage. In this game, 40 rating equals 1 percentage point, so `R = 4,000` rating equals 100%. Every character has 5% base crit and 0% base haste. Expected DPS is:

```
DPS = P × (1 + (m − 1)·c) × (1 + h)
c = 0.05 + crit rating / 4000
h = haste rating / 4000
```

The middle factor is the expected damage multiplier from crits (from MA102's expected value: a hit is worth `1 × (1 − c) + m × c = 1 + (m − 1)·c`). The last factor is the extra hits from haste.

Take derivatives. Power multiplies everything else. Each point of crit rating adds `(m − 1)/4000` to the crit factor, and each point of haste rating adds `1/4000` to the haste factor:

```
∂DPS/∂P           = (1 + (m − 1)c) × (1 + h)
∂DPS/∂crit rating = P × (m − 1)/4000 × (1 + h)
∂DPS/∂haste rating = P × 1/4000 × (1 + (m − 1)c)
```

Divide by `∂DPS/∂P` to normalize. The `(1 + h)` and crit factors cancel in a useful way:

```
weight(crit)  = P × (m − 1) / (4000 × (1 + (m − 1)c))
weight(haste) = P            / (4000 × (1 + h))
```

Read the result. **The weight of crit goes down as you get more crit, and the weight of haste goes down as you get more haste.** Each stat is diluted by its own factor. That is the source of the snapshot effect. Your weights depend on how much of each stat you already have.

### Numbers you can check

A character has 1,000 power and 1,200 secondary rating to split between crit and haste. With `m = 2`:

| Crit rating | Haste rating | Crit | Haste | DPS | Weight of crit | Weight of haste |
|---|---|---|---|---|---|---|
| 0 | 1,200 | 5.0% | 30.0% | 1,365.0 | 0.238 | 0.192 |
| 200 | 1,000 | 10.0% | 25.0% | 1,375.0 | 0.227 | 0.200 |
| 500 | 700 | 17.5% | 17.5% | **1,380.6** | **0.213** | **0.213** |
| 800 | 400 | 25.0% | 10.0% | 1,375.0 | 0.200 | 0.227 |
| 1,000 | 200 | 30.0% | 5.0% | 1,365.0 | 0.192 | 0.238 |
| 1,200 | 0 | 35.0% | 0.0% | 1,350.0 | 0.185 | 0.250 |

Check the middle row by hand. `1000 × (1 + 0.175) × (1 + 0.175) = 1000 × 1.380625 = 1,380.6`. Weight of crit `= 1000 / (4000 × 1.175) = 0.2128`, and haste is the same.

Three things stand out.

1. **At the best split, the two weights are equal.** Everywhere else, the stat with the higher weight is the one to buy more of, and buying it moves you toward the best split. This is not a coincidence of these numbers. When you trade one stat for another at a fixed price, you gain from the trade until the last point of each is worth the same. Equal weights are the test for "I am at the top."
2. **The best split is where the two factors are equal.** `1 + c = 1 + h` at 17.5% each. The haste side gets 200 more rating because crit starts with a 5% head start. In general, for a product of terms `(base_i + rating_i / R_i)` with equal rating prices, the best split makes every term equal.
3. **The top is flat.** Going all-haste costs 1.1% DPS. Going all-crit costs 2.2%. Stat weights matter most for pricing items and ranking choices far from the top, much less for fine-tuning near it.

### A visual you can move

Open the [stat weights interactive](../examples/w12-stat-weights.html). The left panel plots DPS against the crit/haste split as you slide 1,200 rating from all haste to all crit. It is a gentle hill. The right panel shows the two stat weights as bars at the current split. Drag the split slider. As you move left of the peak, the crit bar grows taller than the haste bar; move right of it and haste wins. At the top of the hill, the bars are exactly level.

Now flip the "Crit damage talent" switch, which sets `m = 2.5`. The hill tilts, the peak slides almost all the way to crit, and the bars at your old split are no longer level. Same gear, same class, different talent, different weights. That is the whole Raidbots warning in one click.

### Cross-game recognition

The rule "at the best allocation, the marginal values are equal, and for products of sums that means equal bucket sizes" shows up in any game whose damage or defense formula multiplies several additive groups together.

**Path of Exile, "increased" versus "more."** Path of Exile sorts damage modifiers into two kinds. All "increased" modifiers add together into one sum, and each "more" modifier multiplies separately:

```
damage = base × (1 + sum of increased) × (1 + more₁) × (1 + more₂) × ...
```

That is our DPS formula with more terms. Its consequence is the same dilution we saw for crit. With 100% increased damage already, another 50% increased takes you from 2.0× to 2.5×, a 25% gain. A 50% more modifier is a 50% gain regardless. Path of Exile players value "more" modifiers highly for exactly this reason, and a build with a huge increased total and no more modifiers is poorly balanced in the same way as our all-crit character.

**Diablo IV's damage buckets.** At its 2023 launch, Diablo IV's advanced tooltips marked damage bonuses as additive `[+]` or multiplicative `[x]`. Additive bonuses of the same kind pool into one bucket; buckets multiply with each other. Community guides from that era advise spreading investment across buckets instead of stacking one. Rewritten into our form, each bucket is a factor `(1 + bucket total)`, and the advice is our equal-factor rule. (The rules have moved since launch. Maxroll's guide for Season 13, in 2026, keeps the `[+]` and `[x]` markers but lets some `[x]` bonuses sum with each other before they multiply. Check the current version before you quote specifics.)

**Armor versus health in week 2.** In week 2 you found that effective health is `EHP = HP × (1 + A/K)`, and that the best defensive split satisfies `HP × c_H = (A + K) × c_A`. That is the equal-weights rule applied to survival. With equal prices it says `HP = A + K` in the right units: the two factors of the product should be the same size. Armor and health are two buckets in a product, exactly like crit and haste.

Four contexts, one idea. When a formula multiplies sums, stacking one sum dilutes it, the best allocation balances the factors, and the stat weights are equal at that balance.

### Eyes-open design judgment

You control the formula, the conversion rates, and the budget. Choose them knowing what players will do with the resulting weights.

- **Multiplicative formulas reward balance, and that can be good or bad.** They make every stat worth having and stop any one stat from running away. They also push every build toward the same balanced split, which can make items feel interchangeable. If you want specializations to prefer different stats, give them different formulas or different multipliers. Different flavor text will not do it.
- **Talents and set bonuses should move the peak deliberately.** The crit-damage talent in this example turns a balanced class into a crit stacker. That can be a strong, readable identity ("this build wants crit"). It can also make half the loot table worthless to that build. Decide which you want before you ship the talent.
- **A flat top gives players freedom; a sharp top gives them a spreadsheet.** When the optimum is flat, as here, players can gear by feel and lose 1 or 2%. If your formula has a sharp peak (hard caps, big breakpoints), the difference between guessing and simming becomes large, and your community will treat simulators as mandatory.
- **Hiding formulas does not stop theorycrafting.** Players will measure the formula from combat logs within days of launch. Plan for your formulas to be known, and design them so that knowing them still leaves choices.

## 3. Measuring weights by simulation

Real combat is not a closed-form formula. Crits are random, abilities have cooldowns, procs trigger on hits, and haste interacts with global cooldowns. So tools measure weights by **finite difference**: run the simulation, add a small amount `Δ` of one stat, run it again, and divide:

```
weight(x) ≈ (DPS(x + Δ) − DPS(x)) / Δ
```

Apply this to our model at 1,000 crit rating and 200 haste rating (DPS 1,365.0), with `Δ = 100`.

| Change | New DPS | Gain | Gain per point | Normalized |
|---|---|---|---|---|
| +100 power | 1,501.5 | 136.5 | 1.365 | 1.00 |
| +100 crit rating | 1,391.25 | 26.25 | 0.2625 | 0.19 |
| +100 haste rating | 1,397.5 | 32.5 | 0.325 | 0.24 |

The normalized values match the derivative table (0.192 and 0.238). In this model the formula is linear in each stat alone, so the finite difference is exact. In a real sim it is not.

### Noise

A real simulation's average DPS carries random error from the finite number of simulated fights. Suppose a simulator reports DPS with a standard error of 0.5% of 1,365, about ±6.8 DPS. The difference of two such runs has an error of `sqrt(2) × 6.8 ≈ 9.7` DPS. Our crit gain is 26.25 DPS. So a single measurement of the crit weight would be `0.26 ± 0.10` per point. That is too noisy to tell crit from haste, whose true values differ by only 0.06.

You have two fixes, and both come from MA102's week on Monte Carlo simulation.

- **Raise `Δ`.** The signal grows with `Δ` while the noise does not. Double `Δ` and you double the gain against the same error. SimulationCraft's default delta is tied to the rating needed for a few percent of haste for this reason. The cost is that a large `Δ` measures the average slope over a range, not the slope at your gear, so it blurs curves with caps or breakpoints.
- **Run more iterations.** Standard error falls with the square root of the number of simulated fights. Halving the noise costs four times the computing time.

Designers running internal balance sims face the same choice. Use large enough deltas and enough iterations that the weights you compare differ by more than the noise.

## 4. Caps, breakpoints and cliffs

The model in section 2 is smooth. Many real stat systems are not.

- A **cap** is a value past which a stat does nothing. If crit chance is capped at 50%, the crit weight falls to exactly zero at 50% and stays there. In week 2 you saw the same cliff with a linear-percent armor cap. Players stack to the cap and stop, so every item with the capped stat becomes dead weight for them.
- A **breakpoint** is a value where a stat's effect jumps. If a damage-over-time effect ticks every 3 seconds divided by haste, and the effect lasts 12 seconds, it ticks 4 times at 0% haste and gets a 5th tick only once the tick interval drops to 2.4 seconds, which needs 25% haste. Between 0% and 25% haste, extra haste adds nothing to that effect; at 25% it adds a whole tick. A stat weight measured with a small `Δ` near a breakpoint is either zero or huge, depending on which side you stand.
- A **soft cap** or **diminishing return** reduces a stat's effect gradually past some value. It avoids a cliff, and it adds another reason for the weight to fall as you stack the stat.

Each of these makes the stat weight a poor summary, and each makes direct simulation of whole items (what Raidbots recommends) more valuable. As a designer, prefer smooth curves unless the cliff is the point, and never add a cap whose only purpose is to hide a formula that explodes. Fix the formula instead, as week 2 did with armor.

## 5. How designers use stat weights

Players use weights to rank items. Designers use them for four jobs.

1. **Pricing items.** In GD203 you built item budgets: a slot at a given item level gets a budget, and each stat has a price. The prices should track the stat weights of the specs that will use the item. If crit is priced at 0.25 power per point but every spec values it at 0.19, crit items will be priced as better than they are and players will feel cheated by them.
2. **Detecting a dominant stat.** Compute the weights for every spec at typical gear. If one secondary stat is the top weight for nearly every spec, loot has homogenized: every player wants the same items, and loot distribution in groups becomes a fight. You usually want each secondary stat to be the best stat for at least a few specs.
3. **Checking that choices exist.** If the best split is at a corner (all of one stat), players have no gearing decision. If the peak is interior and flat, they have freedom. If it is interior and sharp, they have a puzzle that only a simulator solves. Pick one on purpose.
4. **Predicting the effect of a change.** Changing a conversion rate or a crit multiplier moves every weight. Before you ship, recompute the weights for each spec and compare the item rankings before and after. A rating change that looks small can flip which items players want from an entire raid tier.

## 6. The talent that moves the peak

Here is the table from section 2 with the crit-damage talent, `m = 2.5`, so each crit adds 1.5 times normal damage instead of 1.

| Crit rating | Haste rating | DPS (`m = 2`) | DPS (`m = 2.5`) | Crit weight (`m = 2.5`) | Haste weight |
|---|---|---|---|---|---|
| 0 | 1,200 | 1,365.0 | 1,397.5 | 0.349 | 0.192 |
| 500 | 700 | **1,380.6** | 1,483.4 | 0.297 | 0.213 |
| 800 | 400 | 1,375.0 | 1,512.5 | 0.273 | 0.227 |
| 1,000 | 200 | 1,365.0 | 1,522.5 | 0.259 | 0.238 |
| 1,167 | 33 | 1,352.8 | **1,525.1** | 0.248 | 0.248 |

The equal-factor rule predicts the new peak. The crit factor is `1 + 1.5c`, which you can write as `1.5 × (0.667 + c)`. Setting `0.667 + c = 1 + h` with a 1,200-rating budget gives about 1,167 crit rating and 33 haste rating, which matches the table. A player who kept their old balanced gear after taking the talent would lose 2.7% DPS against the new peak, and their old weights (0.21 and 0.21) would steer them wrong.

This is also a balance lever. If haste gear is piling up unused because every spec loves crit, adjust the multipliers, conversion rates or talents until some specs' peaks sit on the haste side.

## In-class activity (25 minutes)

Groups of three. Materials: the interactive and a spreadsheet.

1. Set the secondary budget to 1,600 rating and `m = 2`. Find the best split by the equal-factor rule, then confirm it on the interactive. (5 min)
2. A designer proposes changing the haste conversion so that 50 rating gives 1% (instead of 40). Recompute the best split and the DPS at the peak. Which items gain value and which lose? (10 min)
3. You are designing a second spec for the same class. Choose one change (a multiplier, a base value or a conversion rate) that puts this spec's peak on the haste side, so the two specs want different items. Show the new weights at the new peak. (10 min)

Expected output: three numbers per step (crit rating, haste rating, DPS at the peak) and one paragraph explaining the change in step 3.

## Common misconceptions

- **"Haste is worth 0.24 for my class."** A weight is a slope at your current gear, talents and fight. It changes as soon as any of those change.
- **"If crit has the highest weight, I should stack only crit."** The weight falls as you add crit. Buy the highest-weight stat until the weights are equal, then stop.
- **"Stat weights tell you the best item."** They are a linear estimate. For items with procs, set bonuses, or stats near a cap or breakpoint, only simulating the item itself gives a reliable answer.
- **"A weight measured by simulation is exact."** It carries simulation noise, which can be larger than the gap between two stats. Check the error before you trust a ranking.

## Check yourself

1. With 1,000 power, `m = 2`, 5% base crit, 0% base haste and 40 rating per 1%, compute the normalized crit and haste weights at 600 crit rating and 600 haste rating. Which stat should the player buy next?
2. A character has 2,000 rating to split and the same rules as question 1. What is the best split, and what is the DPS there?
3. Path of Exile character A has 200% increased damage and no more modifiers. Character B has 50% increased damage and one 40% more modifier. Each can add either 30% increased or 20% more. Which should each pick, and by how much does their damage rise?
4. A sim reports a crit gain of 31 DPS and a haste gain of 27 DPS for `Δ = 100`, with each run's standard error 8 DPS. Can you conclude that crit is worth more? What would you change to find out?

<details>
<summary>Answers</summary>

1. Crit is 20%, haste 15%. Weight of crit `= 1000 / (4000 × 1.20) = 0.208`. Weight of haste `= 1000 / (4000 × 1.15) = 0.217`. Haste is slightly higher, so buy haste. The best split for 1,200 rating is 500/700, and 600/600 is just past it on the crit side.
2. Equal factors: `1.05 + crit/4000 = 1 + haste/4000` with `crit + haste = 2000`. So `haste − crit = 200`, giving 900 crit rating and 1,100 haste rating. Both factors are 1.275, and DPS `= 1000 × 1.275² = 1,625.6`.
3. A: 30% increased takes 3.0× to 3.3×, a 10% gain; 20% more is a 20% gain. A picks more. B: 30% increased takes 1.5× to 1.8×, a 20% gain; 20% more is also a 20% gain. B is indifferent. The more stacked the increased pool, the stronger the case for more.
4. No. The difference of two runs has error `sqrt(2) × 8 ≈ 11.3` DPS, so each gain is about ±11. A 4-DPS difference between them is well inside the noise. Use a larger `Δ` (say 400) or run enough iterations to cut the standard error by at least a factor of 3 (9 times the iterations), then compare again.

</details>

## Lab hook

**Lab 12: Measuring stat weights with a noisy simulator.** You build a small randomized combat sim for the class in this lecture, measure stat weights by finite difference, estimate their error, and find the delta and iteration count needed to rank crit against haste reliably. See [`labs/lab12.md`](../labs/lab12.md). The simulator carries forward into week 13.

## Sources

- SimulationCraft wiki, "StatsScaling" (GitHub, checked 2026). Scale factors computed as the DPS difference divided by the stat delta; optional normalization so the primary stat equals 1.0; default delta tied to the rating for a few percent of haste (116 rating in the Shadowlands era). https://github.com/simulationcraft/simc/wiki/StatsScaling
- Raidbots Support, "Beware of Stat Weights" (checked 2026). Stat weights as a coarse approximation of one moment; direct item sims preferred. https://support.raidbots.com/article/66-beware-of-stat-weights
- Warcraft Wiki, "ElitistJerks," and Vice, "An Oral History of Azeroth's Most Influential Guild." Forum history, the site going offline around 2016, and Ion Hazzikostas's later role at Blizzard. https://warcraft.wiki.gg/wiki/ElitistJerks
- Path of Exile Wiki (Fandom), "Stat," and Maxroll, "Damage Scaling" (Path of Exile 2 guide, checked 2026). Increased modifiers are additive with each other; more modifiers multiply separately. https://pathofexile.fandom.com/wiki/Stat
- Mobalytics, "Diablo 4 Damage Buckets Explained" and Maxroll, "In-Depth Damage Guide" (Diablo IV, 2023 launch through Season 3). Additive `[+]` and multiplicative `[x]` tooltip markers; buckets multiply; advice to spread across buckets. Maxroll's guide as updated for Season 13 (June 2026) adds summed multipliers, where some `[x]` bonuses add together first. https://maxroll.gg/d4/resources/in-depth-damage-guide
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press. Transitive mechanics, cost curves and item pricing.
- The crit/haste class, its conversion rates and all tables in this lecture are fictional teaching values, not data from a shipped game.

## Interactive spec: examples/w12-stat-weights.html

**The one insight:** at the best split of a stat budget, the stat weights are equal. Anywhere else, the higher weight points toward the peak, so weights are slopes on a curve and change when you move along it or when a talent reshapes it.

**Layout.** Two linked panels side by side at ≥ 900px, stacked below that. A readout strip under both.

1. **DPS hill (left).** x-axis: crit rating from 0 to the budget (haste rating is budget minus crit). y-axis: DPS. Plot the curve at 1-rating resolution. Mark the current split with a draggable dot and the peak with a small triangle and label "peak". Draw the tangent line at the current split (slope = `∂DPS/∂crit − ∂DPS/∂haste` per rating) so the student sees it flatten at the top. When the talent toggle changes `m`, keep a faint ghost of the previous curve for 2 seconds (skip the fade under reduced motion).
2. **Weights (right).** Two vertical bars: normalized crit weight and normalized haste weight at the current split, with values to three decimals above each bar. A third, thinner bar for power fixed at 1.000 for reference. When the two bars are within 0.002 of each other, draw a "balanced" label between them.

**Readout strip (copyable text).** Crit rating, haste rating, crit %, haste %, DPS (one decimal), crit weight, haste weight, peak split and peak DPS, and "% below peak" for the current split.

**Controls.**
- Slider "Crit rating" from 0 to budget, step 1 (also moves by dragging the dot). Default 1,000.
- Number input "Secondary budget", 400 to 3,000, step 100, default 1,200.
- Number input "Power", 500 to 3,000, step 50, default 1,000.
- Select "Rating per 1% crit" and "Rating per 1% haste", each 20 to 80, step 5, default 40.
- Toggle "Crit damage talent": off sets `m = 2`, on sets `m = 2.5`.
- Toggle "Crit cap at 30%" (off by default): clamps `c` at 0.30; the crit weight shows 0.000 above the cap and the hill has a visible kink.
- Button "Jump to peak". All controls keyboard operable with visible focus.

**Formulas.**
- `c = min(cap, 0.05 + crit / (100 × Rc))` where `Rc` is rating per 1% crit and `cap` is 1.0 unless the cap toggle is on (0.30).
- `h = haste / (100 × Rh)`.
- `DPS = P × (1 + (m − 1) × c) × (1 + h)`.
- `∂DPS/∂P = (1 + (m − 1)c)(1 + h)`.
- `∂DPS/∂crit = P × (m − 1) / (100 Rc) × (1 + h)` if below cap, else 0.
- `∂DPS/∂haste = P / (100 Rh) × (1 + (m − 1)c)`.
- Normalized weights: divide each by `∂DPS/∂P`.
- Peak: evaluate every integer crit rating from 0 to the budget and take the maximum DPS (ties to the lower crit value).

**Test values (builder must reproduce, defaults unless stated).**
| Crit rating | m | DPS | Crit weight | Haste weight |
|---|---|---|---|---|
| 0 | 2 | 1,365.0 | 0.238 | 0.192 |
| 500 | 2 | 1,380.6 (peak) | 0.213 | 0.213 |
| 1,000 | 2 | 1,365.0 | 0.192 | 0.238 |
| 1,200 | 2 | 1,350.0 | 0.185 | 0.250 |
| 500 | 2.5 | 1,483.4 | 0.297 | 0.213 |
| 1,167 | 2.5 | 1,525.1 (peak) | 0.248 | 0.248 |

- Budget 2,000, `m = 2`: peak at 900 crit rating, DPS 1,625.6.
- Crit cap on, `m = 2`, budget 1,200: crit reaches 30% at 1,000 rating, and the crit weight reads 0.000 from 1,000 upward.

**First screen.** Load at crit rating 1,000 with `m = 2`, so the haste bar (0.238) is visibly taller than the crit bar (0.192) and the dot sits right of the peak. Caption: "Haste is worth more here. Move toward the peak and watch the bars meet."

**Accessibility and style.** Shared palette from `templates/interactive-tokens.css`, light and dark modes, bars labeled with text as well as color, no game art or logos.
