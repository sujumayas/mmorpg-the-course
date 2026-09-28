# MA101 · Week 04 — Exponentials: growth and the XP curve

**Why this matters:** Every leveling system, upgrade price and idle-game counter you have played is built on one of two ideas. Either each step adds a fixed amount, or each step multiplies by a fixed amount. The second idea, exponential growth, is how RuneScape makes level 99 feel like a lifetime and how Cookie Clicker keeps a building worth buying after you own a hundred of them. If you can't read an exponential, you can't predict how long your players will grind.

**You will be able to:**
- Write an exponential function `y = a · b^x` from a description ("doubles every 7 levels") and name its growth factor, growth rate and doubling interval.
- Compute the total of an exponential per-level cost with the geometric series formula and explain why the total is also exponential.
- Explain, with numbers, why level 92 is half of level 99 in RuneScape and predict the "halfway level" of any exponential XP table.
- Critique an XP curve by comparing exponential and polynomial shapes, and pick one deliberately for a target feel.

**Before class:** OpenStax, *College Algebra 2e*, sections 6.1 (Exponential Functions) and 6.2 (Graphs of Exponential Functions). Skim the Old School RuneScape Wiki "Experience" page and look only at the table.

**Prerequisites from earlier courses:** [MA101 week 2, linear functions and rates](w02-linear-functions-and-rates.md) and [week 3, polynomials](w03-polynomials-and-quadratic-curves.md). You need the idea of a function as an input-output machine from [week 1](w01-functions-as-machines.md) and the slope of a line from week 2.

**Interactive:** [`examples/w04-xp-curve.html`](../examples/w04-xp-curve.html). Keep it open during section 2.

---

## 1. Adding versus multiplying

Start with two ways a number can grow as some input `x` goes up by one step.

**Linear growth adds.** Each step adds the same amount `m`. You met this in week 2 as `y = m·x + c`. If a sword gains 4 damage per upgrade, ten upgrades add 40 damage, and the hundredth upgrade adds the same 4 as the first.

**Exponential growth multiplies.** Each step multiplies by the same number `b`. The general form is:

```
y = a · b^x
```

- `a` is the starting value, the output when `x = 0`.
- `b` is the **growth factor**, the number you multiply by each step. It must be positive.
- `x` is the input, often a level or a count of purchases.

If `b > 1` the function grows. If `0 < b < 1` it shrinks, which we call **exponential decay**. If `b = 1` nothing changes.

Designers and players rarely say "growth factor". They say "15% more expensive each time". That percentage is the **growth rate** `r`, and the two are tied by one equation:

```
b = 1 + r
```

A 15% increase per building means `b = 1.15`. A 10% loss per second means `b = 0.9`.

### The doubling interval

The most useful fact about an exponential is how many steps it takes to double. Call that the **doubling interval** `d`. If the function doubles every `d` steps, you can write it as:

```
y = a · 2^(x/d)
```

This is the same function as `a · b^x` with `b = 2^(1/d)`. Check it: `(2^(1/d))^x = 2^(x/d)`. Writing it with base 2 makes the behavior readable at a glance. "Doubles every 7 levels" is `2^(x/7)`. "Doubles every 5 purchases" is `2^(x/5)`.

To go the other way, from a growth factor to a doubling interval, you need logarithms, which are next week's topic. For now, use this rule of thumb that you can verify on a calculator:

```
d ≈ 70 / (growth rate in percent)
```

At 15% per step, `d ≈ 70 / 15 ≈ 4.7` steps. The exact value is 4.96. The rule is rough above about 20%, but it lets you sanity-check a design in your head.

### The property that defines exponentials

A linear function has a constant **difference** between neighbors. An exponential has a constant **ratio** between neighbors:

```
f(x + 1) / f(x) = b         for every x
f(x + d) / f(x) = 2         for every x
```

This one property explains almost everything in this lecture. If a function doubles every `d` steps, then the value at any point is half the value `d` steps later. No matter where you stand, the next `d` steps cost as much as everything before them combined.

Test yourself before reading on. If a curve doubles every 7 levels, what fraction of the level-99 total have you earned at level 92?

## 2. Worked example: the RuneScape XP curve

### The hook

RuneScape players have a saying: level 92 is halfway to 99. It sounds like a joke. The skill levels go from 1 to 99, so 92 looks like 93% of the way there. But on the Old School RuneScape experience table, reaching level 92 in a skill takes 6,517,253 experience points (XP), and reaching level 99 takes 13,034,431. That is 50.0% of the total, correct to the first decimal place. The last seven levels take as long as the first ninety-one.

Players feel this as a wall. A skill that took a week to raise from 60 to 70 takes months to raise from 92 to 99. Is it a quirk of one table, or does it follow from the shape of the curve? It follows from the shape, and once you see why, you can design the wall where you want it.

### The model

RuneScape publishes its XP table, and the wikis for both Old School RuneScape and RuneScape 3 (regular skills) give the formula that produces it. The total XP needed to reach level `L` is:

```
xp(L) = floor( (1/4) · Σ_{n=1}^{L−1} floor( n + 300 · 2^(n/7) ) )
```

- `L` is the target level, from 1 to 99.
- `n` runs over every level below `L`. Each term is the XP cost of going from level `n` to level `n + 1`.
- `floor` rounds down to a whole number.
- `Σ` means "add up all the terms from `n = 1` to `n = L − 1`".

It looks intimidating. Strip out the parts that barely matter and it becomes simple. The `n` inside each term is at most 98, while `300 · 2^(n/7)` reaches millions, so the `n` barely matters at high levels. The floors change the result by a few points at most. Drop both and each level's cost is roughly:

```
cost(n) ≈ 75 · 2^(n/7)        (because 300 / 4 = 75)
```

That is an exponential with starting value 75 and a doubling interval of 7 levels. **Each level costs about 10.4% more than the one before**, since `2^(1/7) ≈ 1.104`.

The total is the sum of those costs. Section 3 shows how to add up an exponential exactly. The result is:

```
xp(L) ≈ 720.5 · 2^(L/7) − 796
```

For high levels the constant 796 is tiny next to the first term, so:

```
xp(L) ≈ 720 · 2^(L/7)
```

**The total XP doubles every 7 levels.** That is the whole secret. Level 99 minus 7 is level 92, so level 92 holds half the XP of 99. Level 85 is another 7 levels down, so it holds a quarter.

### Numbers you can check

The first XP column comes from running the exact formula. The approximation column uses `720.53 · 2^(L/7) − 795.53 + L(L−1)/8`, where the last term puts back the small `n` part of each cost (the sum of `n/4`). Keep the constants to two decimals. With 720.5 and 796 the level-99 row comes out about 600 XP low. You can reproduce every row in a spreadsheet in five minutes, which is part of this week's lab.

| Level L | Exact xp(L) | Approximation | Share of level 99 | XP for the next level |
|---|---|---|---|---|
| 10 | 1,154 | 1,155 | 0.009% | 204 |
| 50 | 101,333 | 101,339 | 0.78% | 10,612 |
| 70 | 737,627 | 737,635 | 5.66% | 76,818 |
| 85 | 3,258,594 | 3,258,603 | 25.0% | 339,198 |
| 92 | 6,517,253 | 6,517,263 | 50.0% | 678,376 |
| 99 | 13,034,431 | 13,034,441 | 100% | — |

The last column is `xp(L+1) − xp(L)` from the exact table. Notice that it grows by the same factor as the total: the cost of the next level at 92 is about double the cost at 85.

Two things to verify by hand:

1. Divide any row by the row seven levels below it (70 by 63, 99 by 92). You get very close to 2 every time above level 20 or so.
2. Divide level 99 by level 50. You get about 128.6. Forty-nine levels is seven doubling intervals, and `2^7 = 128`. The little extra comes from the constant term.

The Old School RuneScape Wiki makes the same observation in words: past roughly level 20, the XP for level `L + 7` is about double the XP for level `L`.

### Seeing it move

Open [`examples/w04-xp-curve.html`](../examples/w04-xp-curve.html). The left panel plots total XP against level on an ordinary axis. It looks flat for 70 levels and then shoots upward. From that picture you would think something changes around level 80. The right panel plots the same numbers with a logarithmic vertical axis, where each gridline is ten times the one below. There the curve is a straight line from about level 20 onward. Nothing changes at level 80. The curve does the same thing at every level: it doubles every 7.

Drag the level marker. The readout tells you what share of the maximum you hold and which level is the halfway point. Then drag the doubling-interval slider from 7 to 4. The halfway level becomes 95, which is 99 − 4. Drag it to 10 and the rule predicts 99 − 10 = 89, but the readout says 90. Level 89 holds 49.98% of the total, a hair short of half, because the small constant terms in the formula nudge the totals. **The halfway level is the maximum level minus one doubling interval, give or take a level.** That sentence is the insight the interactive exists to show.

### Why the wall is the same everywhere

Here is the part players get wrong. The ordinary plot suggests that the endgame is harder than the early game. In one sense it is: 99 takes more hours than 50. But measure difficulty as "how many times more XP do I need than I already have?" and every stretch of 7 levels is the same, a doubling. Going from 50 to 57 doubles your XP. Going from 92 to 99 doubles your XP. If your XP per hour also grew with level at the same rate, every 7 levels would take equal time.

It doesn't grow that fast. XP per hour usually rises as players unlock better training methods, but more slowly than doubling every 7 levels. So the time per level grows too, and the endgame feels like a wall. The designer chooses the wall's steepness by choosing the ratio between the XP curve's growth and the reward curve's growth. We come back to this in section 4.

### Cross-game recognition

**Cookie Clicker (building prices).** In Cookie Clicker, every building has a base cost, and each copy you own raises the price of the next by 15%. The Cookie Clicker Wiki gives the price as `base cost × 1.15^M`, where `M` is the number you already own. A Cursor starts at 15 cookies and a Grandma at 100. Rewrite it in doubling form: `1.15^M = 2^(M/4.96)`. So the price **doubles about every 5 purchases**, the same shape as RuneScape with `d ≈ 5` instead of 7. The wiki notes this too: price roughly doubles every 5 buildings and grows about a thousandfold every 50. Check the second claim: `1.15^50 ≈ 1,084`. Your 51st Grandma costs about 108,000 cookies.

Apply the halfway rule. If you own 50 Cursors, what share of everything you spent on Cursors went into the last 5? By the rule, about half. The sum of a geometric series (section 3) confirms it: the last five of fifty cost 50.3% of the total.

**Pokémon (Medium Fast experience group).** Pokémon's XP tables are a useful contrast because they are **not** exponential. In the Generation III and IV games, a Pokémon in the Medium Fast group needs exactly `L³` total XP to reach level `L`, so 1,000,000 XP at level 100. The Slow group uses `1.25 · L³` (1,250,000 at 100) and the Fast group `0.8 · L³` (800,000). These are polynomials, the week 3 topic.

Ask the halfway question of `L³`. Half of 1,000,000 is 500,000, and the cube root of 500,000 is about 79.4. Level 79 holds 493,039 XP, just short of half, so in Pokémon the halfway level is 80, not 92. More telling, check the ratio test. From level 50 to 57, XP grows by `(57/50)³ ≈ 1.48`. From level 92 to 99, it grows by `(99/92)³ ≈ 1.25`. For a polynomial, the ratio for a fixed number of levels **shrinks** as you climb. The late game gets relatively easier. For an exponential the ratio stays fixed. That is the clearest test you have for telling the two apart in a table of numbers: compute ratios of neighbors and see if they stay constant.

Three games, one question. When you meet a progression table, compute `f(x + k) / f(x)` for a few `x`. Constant ratio means exponential, and `k` for a ratio of 2 is the doubling interval. A ratio that falls toward 1 means polynomial.

### Design judgment with eyes open

Choosing exponential growth for an XP curve is a decision with real costs. Make it knowingly.

- **Strength: it never runs out of room.** An exponential keeps the next goal meaningful at every level. RuneScape's 99 is a status symbol partly because the curve makes it cost as much as everything before 92.
- **Strength: one knob.** The doubling interval sets the feel. Short intervals (4 or 5) create a sharp endgame wall. Long intervals (10 or more) make the curve gentle and push the halfway level down.
- **Cost: the numbers explode.** At `d = 7`, going from level 99 to level 120 multiplies XP by eight. RuneScape 3 has skills that go past 99, and a designer who extends an exponential table must accept huge numbers or change the formula. Integer overflow is a real risk if your curve runs long; a 32-bit signed integer tops out at about 2.1 billion.
- **Cost: early levels come almost free.** With `d = 7`, level 20 costs 0.03% of level 99. That is fine for a skill players will grind for months. It is wrong for a 20-hour single-player RPG, where a cubic or even linear curve spreads the effort more evenly.
- **Cost: players read the linear plot.** They see "the last 7 levels take forever" and feel punished. If you want that feeling, keep it. If not, show progress as a share of the next doubling, or shorten the table.

A polynomial XP curve, like Pokémon's, is the right call when you want every level to feel like a similar effort and you don't expect players to grind for years. An exponential is the right call when the top of the table should be rare. A designer who copies RuneScape's formula into a short game gets a wall nobody wanted.

The questions in "Check yourself" below make you use this model: questions 1, 2 and 3.

## 3. Adding up an exponential: the geometric series

We skipped a step. Each level costs about `75 · 2^(n/7)`, and we claimed the total also looks like `720 · 2^(L/7)`. Why would a sum of exponentials be an exponential with the same doubling interval?

A **geometric series** is a sum where each term is the previous one times a fixed ratio `b`:

```
S = a + a·b + a·b² + ... + a·b^(N−1)
```

There is a trick to add it. Multiply the whole sum by `b`:

```
b·S = a·b + a·b² + ... + a·b^(N−1) + a·b^N
```

Subtract the first line from the second. Almost everything cancels, leaving:

```
b·S − S = a·b^N − a
S = a · (b^N − 1) / (b − 1)
```

That is the **geometric series formula**. Notice the `b^N` in it. The total grows with the same factor `b` as the individual terms. The division by `(b − 1)` only scales it.

Apply it to RuneScape with `b = 2^(1/7) ≈ 1.10409` and a first term of `75 · b` (the cost at `n = 1`):

```
xp(L) ≈ 75·b · (b^(L−1) − 1) / (b − 1)
      = 75 · (b^L − b) / (b − 1)
      = 720.5 · 2^(L/7) − 796
```

The `720.5` is `75 / (b − 1) = 75 / 0.10409`. The `796` is `75 · b / (b − 1)`. Every number in the model now has a source.

### The "last chunk" rule

The geometric series formula also explains why the last `d` purchases of any exponential cost about half the total. For large `N`, the `−1` in `b^N − 1` is negligible, so the total is close to `a · b^N / (b − 1)`, which is proportional to `b^N`. The total `d` steps ago was proportional to `b^(N−d) = b^N / 2`. So half the total came in the last `d` steps.

More generally, when you spend on an exponential for a long time, **the last step alone is a fixed share of everything you have spent**. That share is `(b − 1) / b`. For Cookie Clicker at 15% growth it is `0.15 / 1.15 ≈ 13%`. For RuneScape it is `0.104 / 1.104 ≈ 9.4%`. Check the second one against the table: level 99 minus level 98 is 1,228,825 XP, which is 9.4% of 13,034,431.

### Buying in bulk

Cookie Clicker lets you buy 10 buildings at once. The price of ten is a geometric series with `N = 10` and `b = 1.15`:

```
price of 10 = p · (1.15^10 − 1) / 0.15 ≈ 20.3 · p
```

where `p` is the price of the next single building. The Cookie Clicker Wiki gives the same multiplier of about 20.3. So ten buildings cost as much as about twenty of the first one. Players who "buy ten because it's cheaper per click" are paying the exponential tax in one lump.

## 4. Designing an exponential curve on purpose

A formula copied from another game carries that game's assumptions. Here is how to build one from your own goals.

### From two points

Suppose you want level 1 to cost 100 XP and level 50 to cost 1,000,000 total. Assume `xp(L) = a · b^L` and use the two conditions:

```
a · b^1  = 100
a · b^50 = 1,000,000
```

Divide the second by the first to cancel `a`:

```
b^49 = 10,000
```

You now need `b` such that raising it to the 49th power gives 10,000. That is `b = 10,000^(1/49) ≈ 1.207`, a growth of about 20.7% per level. The doubling interval is about 3.7 levels, so the halfway level is about 46. If that endgame wall is too sharp, relax one of your two points. Next week you will solve equations like `b^49 = 10,000` with logarithms, which makes this faster.

### Matching XP to rewards

What players feel is **time**, not XP. Time per level is:

```
hours(L) = cost(L) / rate(L)
```

where `rate(L)` is XP per hour at level `L`. If both cost and rate are exponential, say `cost ∝ 2^(L/7)` and `rate ∝ 2^(L/14)`, then hours per level is proportional to `2^(L/7 − L/14) = 2^(L/14)`. The time per level doubles every 14 levels. Dividing two exponentials gives another exponential whose exponent is the difference. You design the felt curve by setting the gap between the two.

If `rate` grows exactly as fast as `cost`, every level takes the same time. Some games aim for that in the early game and then let rewards fall behind to create a long tail.

### Exponential decay, briefly

The same model with `0 < b < 1` shrinks things. A debuff that loses 20% of its strength each second has strength `S · 0.8^t`. Its **half-life** plays the role the doubling interval played: the time to fall to half. Using the rule of thumb, `70 / 20 ≈ 3.5` seconds (exact: 3.1). Decay never reaches zero in the math, so games clamp it: remove the debuff below some threshold. You will formalize clamps in [week 7, caps and floors](w07-piecewise-caps-and-floors.md).

## In-class activity (25 minutes)

Work in pairs. You are designing the crafting skill for a small online game. The skill goes to level 40. Playtests say players gain about 2,000 XP per hour at level 1 and about 20,000 XP per hour at level 40.

1. Pick a doubling interval `d` for total XP and write `xp(L) = a · 2^(L/d)`. Set `a` so that level 2 costs about 100 XP.
2. Compute `xp(40)` and the halfway level. Say in one sentence whether the wall is where you want it.
3. Assume XP per hour grows exponentially from 2,000 at level 1 to 20,000 at level 40. Find its doubling interval using the two-point method (hint: `10^(1/39)`, then compare with `2^(1/d)` by trying values of `d`).
4. Estimate hours per level at levels 10, 25 and 40. Is the ratio between the last and the first what you intended?
5. Swap sheets with another pair. Find one player type (casual, completionist, returning player) your partner's curve serves badly.

**Expected output:** one half-page sheet with the formula, a four-row table and two sentences of design rationale. Keep it for the lab.

## Common misconceptions

- **"The last levels are harder because the curve bends upward."** In a pure exponential, every stretch of `d` levels doubles your XP. The curve does the same thing everywhere. The bend you see on an ordinary axis is an artifact of the axis. Plot on a log axis and it is a straight line.
- **"15% growth per level means 150% after 10 levels."** Growth compounds. Ten steps of 15% give `1.15^10 ≈ 4.05`, a 305% increase, not 150%. Adding percentages is the linear mistake.
- **"Any fast-rising table is exponential."** Pokémon's `L³` rises fast too. Check the ratio `f(x+k)/f(x)`. If it drifts toward 1, the table is polynomial.
- **"Buying ten at once is a discount."** In Cookie Clicker ten cost the same as buying them one after another, about 20.3 times the next single price. Bulk buttons change clicks, not cost.

## Check yourself

1. A game's total XP to reach level `L` is `500 · 2^(L/6)`. The level cap is 60. What is the halfway level? At what level do you hold one eighth of the level-60 total?
2. In RuneScape, you are at level 85 in a skill and gain about 150,000 XP per hour with your current method. Using only the doubling rule and the exact level-85 value (3,258,594 XP), estimate how many hours it takes to reach 92 and then to reach 99 at that same rate.
3. You own 30 Cookie Clicker Grandmas (base cost 100). What does the 31st cost? Roughly what share of all you spent on Grandmas went into the last one?
4. A designer proposes an XP table where level `L` needs `1,000 · L²` total. Is it exponential or polynomial? Where is its halfway level if the cap is 50?
5. An upgrade gives +8% damage each time and stacks without limit. How many upgrades double your damage, roughly? Exactly how much damage do 10 upgrades give?

<details>
<summary>Answers</summary>

1. The halfway level is one doubling interval below the cap, `60 − 6 = 54`. One eighth is three doublings down, `60 − 18 = 42`.
2. Level 92 is double level 85, so you need about another 3,258,594 XP, which is about 21.7 hours. Level 99 is double 92, so the next leg needs about 6,517,000 XP, about 43.4 hours. The second leg takes twice as long at a fixed rate. (Exact values: 3,258,659 and 6,517,178 XP, so the estimates are within a few seconds.)
3. `100 · 1.15^30 ≈ 6,621` cookies. The last one is about `0.15 / 1.15 ≈ 13%` of the total so far. (Exact: the total for 31 Grandmas is `100 · (1.15^31 − 1)/0.15 ≈ 50,096`, and 6,621 / 50,096 ≈ 13.2%.)
4. Polynomial (quadratic). Half of `1,000 · 50²` is 1,250,000, so `L² = 1,250` and `L ≈ 35.4`. The halfway level is about 35.
5. Rule of thumb: `70 / 8 ≈ 8.75` upgrades, so about 9 (the exact answer is 9.0). And 10 upgrades give `1.08^10 ≈ 2.16`, 116% more damage.

</details>

## Lab hook

**Lab 04: Build and tune an XP curve.** You rebuild the RuneScape table in a spreadsheet from its formula, confirm the halfway rule, then design your own exponential and polynomial curves for a 40-level crafting skill and compare the time-per-level each produces. See [`labs/lab04.md`](../labs/lab04.md). Next week's lecture, [Logarithms](w05-logarithms-how-many-levels-until.md), inverts the curves you build here.

## Sources

- Old School RuneScape Wiki, "Experience" (accessed September 2026). The experience table (level 92 at 6,517,253 XP, level 99 at 13,034,431 XP, level 85 at 3,258,594 XP), the total-XP formula, the 200,000,000 XP cap per skill, and the observation that the XP for `L + 7` is about double the XP for `L` past roughly level 20.
- RuneScape Wiki, "Experience" (RuneScape 3, accessed September 2026). The same formula for regular skills; elite skills such as Invention use a different curve.
- The Cookie Clicker Wiki (wiki.gg), "Buildings" (current web version, accessed September 2026). Price formula `base cost × 1.15^M`, base prices (Cursor 15, Grandma 100, Farm 1,100), the bulk-buy multiplier of about 20.3, and the rough "doubling every 5 buildings" description.
- Serebii.net, "Experience Points" (Generation III and IV mechanics). Experience group formulas: Fast `0.8·L³`, Medium Fast `L³`, Slow `1.25·L³`, with 800,000, 1,000,000 and 1,250,000 XP at level 100.
- OpenStax, *College Algebra 2e* (2021), sections 6.1 and 6.2, for the definitions of exponential growth and decay.
- Every other number in this lecture is computed from the formulas above and can be reproduced in the lab spreadsheet.

## Interactive spec: examples/w04-xp-curve.html

**The one insight:** an XP curve that looks like a sudden wall on an ordinary axis is a straight line on a log axis, and its halfway level is always the maximum level minus one doubling interval.

**Layout.** Two linked plots side by side on desktop (stacked on mobile, linear on top). Both share the horizontal axis "Level" from 1 to `Lmax`.

- **Left plot, "What players see":** total XP `xp(L)` on an ordinary vertical axis from 0 to `xp(Lmax)`. Shade the area under the curve from the halfway level to `Lmax` in the accent color.
- **Right plot, "What the curve does":** the same `xp(L)` on a log10 vertical axis with gridlines at each power of ten. Draw a thin dashed straight line for the pure approximation `720.5 · 2^(L/d)` (scaled with the controls below) so students see the exact curve joins it after about level 20.
- Both plots show a vertical marker at the selected level and a horizontal marker at half of `xp(Lmax)`.

**Controls (all keyboard accessible, labeled):**

1. Level slider, integer 1 to `Lmax`, default 92.
2. Doubling interval `d` slider, 3 to 14 in steps of 0.5, default 7.
3. Max level `Lmax`, number stepper 20 to 120, default 99.
4. Curve toggle with three options: "RuneScape formula" (default), "Pure exponential" and "Polynomial L³ (Pokémon Medium Fast shape)". The polynomial option ignores `d` and is scaled so that `xp(Lmax)` matches the RuneScape value at the current `Lmax`, which makes the halfway levels comparable.

**Formulas.**

- RuneScape formula, generalized: `xp(L) = floor( (1/4) · Σ_{n=1}^{L−1} floor( n + 300 · 2^(n/d) ) )`. With `d = 7` this is the published table.
- Pure exponential: with `b = 2^(1/d)`, `xp(L) = max(0, 75 · (b^L − b) / (b − 1))`. At `d = 7` this is `720.5 · 2^(L/7) − 796`.
- Polynomial: `xp(L) = xp_RS(Lmax) · (L / Lmax)^3`.
- Halfway level: the smallest integer `L` with `xp(L) ≥ xp(Lmax) / 2`.

**Readouts (next to the plots, copyable text):** `xp(L)` with thousands separators, `xp(L+1) − xp(L)`, share of max as a percentage with one decimal, the halfway level, and the ratio `xp(L) / xp(L − d)` rounded to three decimals (shown as "n/a" when `L − d < 1`).

**Test values (RuneScape formula, d = 7, Lmax = 99):**

| Level | xp(L) | Share of 99 |
|---|---|---|
| 2 | 83 | 0.0% |
| 50 | 101,333 | 0.8% |
| 85 | 3,258,594 | 25.0% |
| 92 | 6,517,253 | 50.0% |
| 98 | 11,805,606 | 90.6% |
| 99 | 13,034,431 | 100.0% |

Halfway level must read 92 at `d = 7`. With the polynomial option at `Lmax = 99`, the halfway level must read 79 (since `0.5^(1/3) · 99 ≈ 78.6`, the first integer at or above half is 79).

**First screen:** level 92 selected, the shaded region visible on the left plot, the log plot showing the straight line, and the readout "Level 92 holds 50.0% of the XP for 99".
