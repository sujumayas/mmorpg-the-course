# GD102 · Week 14 — Tuning with Spreadsheets

**Why this matters:** Every system you have diagrammed this semester has numbers in it, and the diagram cannot tell you whether those numbers are right. A spreadsheet can. It runs your stocks and flows forward one row at a time, shows you where the system settles, and lets you ask "what value of this knob gives me that result?" in seconds instead of in a two-week playtest.

**You will be able to:**
- Build a one-row-per-step spreadsheet model of a stock-and-flow system, with inputs, tables and check columns kept apart.
- Compute the purchase gap between two buildings under a rising-price rule, and explain why rising prices act as a balancing loop that pushes players toward a mix.
- Use goal seek and a one-at-a-time sensitivity table to find which knob hits a design target and which knob the result depends on most.
- Critique a tuning choice by comparing two knobs that hit the same target but change the system differently.

**Before class:** Adams & Dormans, *Game Mechanics: Advanced Game Design* (2012), chapter 4 on internal economies (reread the parts on feedback and equilibrium) and chapter 8, "Simulating and Balancing Games"; Meadows, *Thinking in Systems* (2008), chapter 2 on "one-stock" systems with a balancing loop. Bring a laptop with Excel, LibreOffice Calc or Google Sheets, and your lab 13 specification.

**Prerequisites from earlier courses:** exponential prices and the `base × 1.15^n` rule from [MA101 week 4](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w04-exponentials-and-the-xp-curve.md) (this lecture uses the formula; it does not re-derive it); stocks and flows (week 2), balancing loops (week 4) and internal economies (week 7) from this course ([week 2](w02-stocks-and-flows.md), [week 4](w04-negative-feedback-loops-rubber-banding.md), [week 7](w07-internal-economies-sources-drains-converters.md)); the parameter table and derived numbers from [GD102 week 13](w13-systems-documentation.md).

**Interactive:** [Payback braid](../examples/w14-payback-braid.html). Keep it open during section 2.

---

## 1. A spreadsheet is a system model

In week 2 you drew stocks as boxes and flows as pipes. A spreadsheet holds the same model with a different layout. **Each stock is a column. Each row is one step of time. Each flow is a formula** that computes the next row from the current one.

The rule behind every such sheet is the stock equation you already know:

```
stock[next step] = stock[this step] + inflows − outflows
```

Here is the smallest useful example. A player's guild bank earns 100 gold a day from members (a faucet). It pays upkeep equal to 10% of whatever is in the bank each day (a drain that grows with the stock). In symbols, with `G` the gold in the bank, `I` the daily income and `s` the upkeep rate:

```
G[d+1] = G[d] + I − s × G[d]
```

Start the bank at 0 with `I = 100` and `s = 0.10`:

| Day | Gold at end of day |
|---|---|
| 0 | 0 |
| 1 | 100.0 |
| 2 | 190.0 |
| 3 | 271.0 |
| 4 | 343.9 |
| 5 | 409.5 |
| 7 | 521.7 |
| 10 | 651.3 |
| 14 | 771.2 |

Check day 2 by hand: `100 + 100 − 0.1 × 100 = 190`. The bank grows fast, then slower, and never passes 1,000. That ceiling is the **equilibrium**, the stock level where inflow equals outflow. Setting `I = s × G` gives `G* = I / s = 100 / 0.10 = 1,000`. Upkeep is a balancing loop (week 4): the more gold there is, the faster it drains. The spreadsheet shows you the loop's effect as a curve bending toward a line.

### The layout

Keep three kinds of cell apart. This layout is the same one GD203 will use for combat balance later in the degree ([GD203 week 11](../../GD203-combat-and-progression-design/lectures/w11-spreadsheet-balancing-workshop.md)), so learning it now pays twice.

- **Inputs.** Every tunable number lives in exactly one labelled cell on an Inputs tab, with its unit and a note. Use the parameter names from your week 13 specification (`guild_income`, `upkeep_rate`). Color input cells one way, for example pale yellow, so nobody overwrites a formula thinking it is a value.
- **Tables.** One row per step (day, purchase, level). Every cell in a column has the same formula, filled down. The gold column above is `=B2 + guild_income - upkeep_rate * B2` in every row. If one row needs to be different, that difference is a rule and belongs in the inputs, not in a hand-edited cell.
- **Checks.** Columns that compare a result with a target and flag it. "Day 14 gold between 700 and 900." "Equilibrium below 2,000." Use conditional formatting so a failing check turns red. A check column is a test, like the given/when/then cases from last week.

Two mechanical habits prevent most spreadsheet bugs. First, refer to inputs by name (named ranges in all three programs) or with absolute references (`$B$2`), so filling a formula down does not shift the reference. Second, never type a number into a formula. `=B2 + 100 - 0.1*B2` works today and silently disagrees with the inputs tab after the next tuning pass.

## 2. Worked example: why every idle player owns a mix

### The hook

Cookie Clicker is a browser idle game where you bake cookies and spend them on buildings that bake more cookies for you. Its wiki lists the first buildings' base prices and base production in cookies per second (CpS):

| Building | Base price | Base CpS | Seconds to pay back |
|---|---|---|---|
| Cursor | 15 | 0.1 | 150 |
| Grandma | 100 | 1 | 100 |
| Farm | 1,100 | 8 | 137.5 |
| Mine | 12,000 | 47 | 255.3 |

"Seconds to pay back" is price divided by CpS. It is how long a building takes to bake back its own cost. On those numbers the Grandma is the best deal by a wide margin. So why not buy only Grandmas? Model a player who always takes the best deal on offer and they rotate anyway. A few Grandmas, a Farm, a Cursor, another Grandma, a Farm. No rule tells them to diversify. The system does.

The reason is one line in the rules. Every time you buy a building, the next one of the same kind costs 15% more. MA101 week 4 treated that rule as an exponential curve. This week we treat it as a feedback loop and tune it in a spreadsheet.

### The model

Name the symbols for building `i`:

- `b_i` is its base price, `c_i` its CpS, and `n_i` how many you already own.
- `g` is the price growth factor per purchase. Cookie Clicker uses `g = 1.15`.
- The price of the next one is `b_i × g^(n_i)`, as in MA101 week 4.

The **payback time** of the next purchase is its price divided by what it adds:

```
payback_i = b_i × g^(n_i) / c_i
```

Model the player with the simplest sensible rule. **Always buy the building with the shortest payback.** This is a greedy rule. It ignores upgrades, clicking and the wait to afford expensive buildings, so treat it as a model of the base economy, not of how an expert plays the full game.

Now the systems reading. Buying a Grandma raises the next Grandma's payback by 15%. The more Grandmas you own, the worse the next Grandma looks, so the player turns to something else. That is a balancing loop on each building's attractiveness, the same shape as the guild bank's upkeep. The stock (Grandmas owned) feeds back to reduce its own inflow (the reason to buy another).

Where does it settle? The greedy player keeps buying whatever is cheapest, which pulls every building's payback toward the same value. When two paybacks are equal:

```
b_i × g^(n_i) / c_i  =  b_j × g^(n_j) / c_j

n_i − n_j  =  log_g( (b_j / c_j) / (b_i / c_i) )
           =  ln(payback ratio) / ln(g)
```

That is the whole model. **The gap in ownership between two buildings is fixed by the ratio of their base paybacks and by `g`.** It does not grow over time. A building with 1.5 times the base payback of another sits a constant `ln 1.5 / ln 1.15 ≈ 2.9` purchases behind it, forever.

### Numbers you can check

The payback of each building's next purchase, for the first few purchases (`g = 1.15`, seconds):

| Owned already | Cursor | Grandma | Farm | Mine |
|---|---|---|---|---|
| 0 | 150.0 | 100.0 | 137.5 | 255.3 |
| 1 | 172.5 | 115.0 | 158.1 | 293.6 |
| 2 | 198.4 | 132.3 | 181.8 | 337.7 |
| 3 | 228.1 | 152.1 | 209.1 | 388.3 |
| 4 | 262.4 | 174.9 | 240.5 | 446.6 |
| 5 | 301.7 | 201.1 | 276.6 | 513.5 |
| 6 | 347.0 | 231.3 | 318.0 | 590.5 |
| 7 | 399.0 | 266.0 | 365.8 | 679.1 |

Follow the greedy rule by always taking the smallest number not yet taken. The first 20 purchases are:

| Purchase | Buys | Its payback (s) |
|---|---|---|
| 1-3 | Grandma, Grandma, Grandma | 100.0, 115.0, 132.3 |
| 4 | Farm | 137.5 |
| 5 | Cursor | 150.0 |
| 6-8 | Grandma, Farm, Cursor | 152.1, 158.1, 172.5 |
| 9-11 | Grandma, Farm, Cursor | 174.9, 181.8, 198.4 |
| 12-14 | Grandma, Farm, Cursor | 201.1, 209.1, 228.1 |
| 15-16 | Grandma, Farm | 231.3, 240.5 |
| 17 | **Mine** (first) | 255.3 |
| 18-20 | Cursor, Grandma, Farm | 262.4, 266.0, 276.6 |

From purchase 17 on, the player cycles Mine, Cursor, Grandma, Farm, and never breaks the cycle. After 40 purchases they own 13 Grandmas, 11 Farms, 10 Cursors and 6 Mines. Compare the gaps with the formula:

| Pair | Base payback ratio | Predicted gap `ln(ratio)/ln(1.15)` | Gap after 40 purchases |
|---|---|---|---|
| Grandma vs Farm | 1.375 | 2.28 | 13 − 11 = 2 |
| Grandma vs Cursor | 1.5 | 2.90 | 13 − 10 = 3 |
| Grandma vs Mine | 2.553 | 6.71 | 13 − 6 = 7 |

The counts are whole numbers, so the gaps round, but they sit right on the prediction. The payback column in the greedy table climbs steadily with no jumps. Every purchase is only slightly worse than the one before it, whichever building it is. That smoothness is what the balancing loop buys you.

### Tuning it: a target and two knobs

Now act as the designer. Suppose your target, written in your week 13 specification as a derived number, is **"the first Mine arrives when the player owns 10 Grandmas."** Right now it arrives at 7. You have two obvious knobs.

**Knob 1, the Mine's base price.** Under the greedy rule the first Mine is bought when its base payback is lower than the next Grandma's. For the Mine to wait until Grandma 10 is owned, its base payback must sit between the payback of Grandma 10 and Grandma 11:

```
100 × 1.15^9  = 351.8 s    (payback of the 10th Grandma)
100 × 1.15^10 = 404.6 s    (payback of the 11th Grandma)

Mine base payback between 351.8 and 404.6 s
With c = 47 CpS:  Mine base price between 16,534 and 19,014
```

A goal seek finds this in one step (section 3 shows how). Check it with the sheet. At a Mine price of 16,600 the first Mine is purchase 25, with 10 Grandmas owned. At 19,000 it is purchase 27, still with 10 Grandmas. At 19,100 the player has already bought an 11th. Pick a value in the middle, say 17,500, so a later change to Grandma does not tip it over.

**Knob 2, the growth factor `g`.** Lowering `g` to 1.10 also delivers the first Mine at 10 Grandmas (purchase 24), with no change to the Mine at all. Raising it to 1.20 brings the Mine in at 6 Grandmas (purchase 14).

Both knobs hit the target. They are not the same change. The Mine price only moves one gap. The growth factor moves every gap at once, because every gap is divided by `ln g`:

| Gap | `g = 1.10` | `g = 1.15` | `g = 1.20` |
|---|---|---|---|
| Grandma vs Cursor | 4.25 | 2.90 | 2.22 |
| Grandma vs Farm | 3.34 | 2.28 | 1.75 |
| Grandma vs Mine (price 12,000) | 9.83 | 6.71 | 5.14 |

A lower `g` spreads the player's collection out and makes early buildings stay attractive longer. It also makes every price rise more slowly, which changes pacing across the whole game. If the only thing wrong was the Mine, change the Mine. Reaching for the global knob because it is one cell, when the problem was local, is the most common tuning mistake.

### See it move

Open the interactive. The left view, "Prices," draws each building's next price against purchase number. The lines fan apart and it looks like the buildings are drifting away from each other. The right view, "Payback of the next purchase," shows the greedy sequence and tells the truth. All four paybacks braid together into one rising band. Drag `g` down to 1.05 and the braid loosens into long runs of one building; drag it up to 1.30 and the player rotates almost every purchase. Then drag the Mine's base price and watch the readout "Grandmas owned at first Mine" step from 7 to 10. The ownership bars under the chart keep constant gaps no matter how far you run the sequence.

### Cross-game recognition

A rising cost on repeated purchases, plus a player who buys the best value next, gives the same result everywhere, a steady mix with fixed gaps set by the ratio of values and the log of the growth factor.

**Old School RuneScape skills (current game).** The XP to gain a level grows by about `2^(1/7) ≈ 1.104` per level; MA101 week 4 and GD203 week 7 derive this from the published XP formula. Suppose a player wants to raise their total level as fast as possible, and one skill trains twice as fast (in XP per hour) as another. Treat "time to the next level" as the payback. It equals the XP cost divided by the XP rate, so the greedy player keeps the fast skill ahead by `ln 2 / ln(2^(1/7)) = 7` levels. Same formula, `g = 1.104`, payback ratio 2. The rising cost per level is the balancing loop that stops a total-level player from maxing one skill first.

**Armor versus health (MMO303 week 2).** In the divisive armor model, effective health is `HP × (1 + A/K)` ([MMO303 week 2](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w02-armor-and-damage-mitigation.md)). Each armor point adds `HP/K` effective health and each health point adds `1 + A/K`. Buying one raises the value of the other, so a player who always buys the stat with the better return per gold alternates, and lands on the split `HP × c_H = (A + K) × c_A`. Here the balancing is between two stocks instead of within one, but the reading is the same. A best-value-next player plus a changing marginal value produces a mix, and the designer sets where that mix lands through the prices.

**The guild bank from section 1.** The upkeep rate is a balancing loop that fixes an equilibrium `I/s`. The rising price is a balancing loop that fixes a gap `ln(ratio)/ln g`. In both, a spreadsheet shows you the settled state, and in both the tuning question is "which input moves the settled state where I want it."

### Eyes-open design judgment

- **Rising prices are a diversity tool.** They guarantee that no single option stays best, without any rule saying "you must diversify." That is why they are everywhere in idle and strategy games. If you want players to specialize, rising prices work against you; use flat prices and different synergies instead.
- **The gap depends on a log.** Because `ln g` is small for `g` near 1, small changes in `g` near 1 cause large changes in the mix. Going from 1.15 to 1.10 raised the Grandma-to-Mine gap from 6.7 to 9.8. Treat `g` as a sensitive knob and test it with a sensitivity table, not by feel.
- **The greedy model is a floor, not a player.** Real Cookie Clicker has upgrades that multiply specific buildings, and players who plan ahead. Those push the mix around. The model tells you the structure the base numbers create; playtests tell you how people bend it. Tune the base first, then layer the exceptions.
- **Local problem, local knob.** When one building is off, change that building's price or output. Changing `g` retunes the entire game's pacing to fix one row.
- **Alternatives.** Linear price growth (`b + k × n`) weakens the loop over time, so the mix slowly collapses toward the best base payback. A hard cap per building ("max 10 Grandmas") forces diversity with a cliff instead of a curve, and players stack to the cap and stop, the same cap behavior MMO303 week 2 describes for armor.

## 3. Tuning moves

Four spreadsheet techniques cover most tuning work at this level. All of them assume the layout from section 1: one cell per input, formulas everywhere else.

### Goal seek: solve for the input

Goal seek changes one input cell until a formula cell reaches a target. In Excel it is under Data, What-If Analysis, Goal Seek. In LibreOffice Calc it is under Tools, Goal Seek. In Google Sheets you can install an add-on, or do it by hand. Try a value too low and a value too high, then halve the interval until the result is close enough. Halving ten times gets you within a thousandth of the starting interval.

Use it on the guild bank. Target: 800 gold at the end of day 14. With `s = 0.10` fixed, goal seek on `guild_income` gives `I ≈ 103.7`. You can confirm with the closed form for this system, `G[d] = (I/s) × (1 − (1 − s)^d)`: `(103.7 / 0.1) × (1 − 0.9^14) ≈ 800`. In the idle example, goal seek on the Mine's base price with target "Grandmas owned at first Mine = 10" does not work directly, because the result jumps in whole steps. There, compute the boundaries by hand as in section 2, or step the input and watch where the count changes.

### Sensitivity: which input does the result depend on?

Change one input at a time by a fixed amount, hold everything else, and record the result. This is **one-at-a-time sensitivity**. Lay it out as a small table, one row per input:

| Input changed (all else at default) | Day-14 gold, low | Default | Day-14 gold, high |
|---|---|---|---|
| `guild_income` 90 / 110 | 694.1 | 771.2 | 848.4 |
| `upkeep_rate` 0.05 / 0.15 | 1,024.7 | 771.2 | 598.2 |

Income moves the result by ±10%, exactly in proportion. Upkeep moves it by +33% and −22%, and unevenly. So day-14 gold depends more on upkeep, and upkeep is the knob to test carefully. Sorted by the size of the swing and drawn as horizontal bars, this table becomes a **tornado chart**, the standard way to show a team which inputs matter.

Excel builds these tables automatically with Data Table (under What-If Analysis), and LibreOffice with Multiple Operations. In any program you can build one by hand, with a column of input values and a column that repeats the result formula with that value substituted.

### Scenarios: named sets of inputs

A **scenario** is a named set of inputs: "casual player," "guild of 50," "patch 1.2 proposal." Keep them as columns on the Inputs tab and add one cell that picks which column is live (with `INDEX` or `CHOOSE`). Now switching the whole model between cases is one cell, and the check columns tell you which scenario breaks a target.

### Check columns as tests

Write the design targets from your week 13 specification as check columns before you start tuning, not after. "Grandmas at first Mine = 10." "Equilibrium gold between 800 and 1,200." "No payback jump between consecutive purchases above 20%." Then tune until everything is green. Writing the check first stops you from quietly moving the target to match the numbers you happen to have.

## 4. When the spreadsheet is not enough

Spreadsheets are the right first tool for systems with a few stocks, deterministic flows and a simple player rule. They struggle in three situations, and you should recognize them.

- **Randomness.** If a flow is random (a 5% drop, a critical hit), one row per step gives you one lucky or unlucky run. Either compute expected values in the sheet, or run the model many times. That is Monte Carlo simulation, covered in [MA102 week 11](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w11-monte-carlo-simulation.md). A spreadsheet can do a few hundred runs with a random column and a data table; beyond that, write a script.
- **Many interacting agents.** A market where thousands of players buy and sell, or a guild whose members each follow their own rule, is hard to express as columns. Week 12's emergent-behavior models are the tool there.
- **Rules that branch a lot.** A greedy rule with four buildings is one `MATCH(MIN(...))` per row. A rule with ten conditions becomes a formula nobody can read. When a cell formula needs more than two nested `IF`s, move that logic to code and keep the sheet for inputs and results.

The sheet is also where most tuning bugs start. The usual suspects are a typed-in number that should have referenced an input, a relative reference that shifted when filled down, a percent entered as 15 instead of 0.15, and an off-by-one where row 1 means "after the first purchase" in one column and "before it" in another. Your check columns catch the first three if you wrote them. Only careful labelling catches the last.

### From the sheet to the document to the game

Close the loop with week 13. The spreadsheet's Inputs tab and the specification's parameter table carry the same names and the same values. The specification's derived-numbers table is a copy of the sheet's check column targets. When a tuning pass changes a value, you update the sheet, re-export the data file the game reads, and add a line to the specification's change log with the reason and the sensitivity result that justified it. Three artifacts, one set of numbers.

## In-class activity (25 min)

Work in pairs with one laptop. Materials: the Cookie Clicker base numbers from section 2, the interactive.

1. **Build the payback sheet (10 min).** Inputs tab with base price, CpS and `g` for the four buildings. A table with one row per purchase: columns for "owned" of each building, the four next-purchase paybacks, and "buys" (`=INDEX(names, MATCH(MIN(paybacks), paybacks, 0))`). Fill down 40 rows. Check: purchase 17 is the first Mine.
2. **Hit a target (8 min).** Your target: the first Farm should arrive after the fifth Grandma, not the third. Find a Farm base price that does it. Then find a Farm CpS that does it with the price unchanged. Record both.
3. **Compare the knobs (5 min).** For each of your two changes, record the ownership counts after 40 purchases. Which change moved the Farm-versus-Cursor gap, and by how much?
4. **Defend a choice (2 min).** Write two sentences: which knob you would ship, and what other part of the game each one affects.

Expected output: the sheet, the two values from step 2, the count table from step 3 and the two sentences.

## Common misconceptions

- **"The spreadsheet is the answer."** It is a model with a stated player rule. Its answer is only as good as that rule. Write the rule next to the table ("greedy by payback, no upgrades") so nobody mistakes the sheet for a forecast of real play.
- **"Rising prices mean buildings drift apart."** Prices drift apart; ownership gaps stay constant. The greedy player's paybacks braid together. Look at the quantity the player decides on, not the quantity on the price tag.
- **"Change the global knob, it is only one cell."** One cell can hold the whole game's pacing. Use the sensitivity table to see how many results a knob moves before you touch it.
- **"If income goes up 10%, everything goes up 10%."** Only for results linear in income. In the guild bank, upkeep changes the day-14 result unevenly (+33% and −22% for a ±50% change). Always check the other inputs too.

## Check yourself

1. The guild bank has income 150 gold a day and upkeep 5% a day. What is its equilibrium? Starting from 0, what is the gold after day 2?
2. In a game with `g = 1.12`, building A has base payback 80 s and building B has base payback 160 s. A greedy player owns 20 of A. About how many B do they own?
3. With Cookie Clicker's base numbers and `g = 1.15`, you want the first Mine to arrive when the player owns exactly 8 Grandmas. What range of Mine base prices does that require (keep 47 CpS)?
4. A colleague fixes "Mines arrive too early" by changing `g` from 1.15 to 1.10. Name two other effects of that change, with numbers from this lecture.

<details>
<summary>Answers</summary>

1. Equilibrium `G* = I / s = 150 / 0.05 = 3,000`. Day 1: `0 + 150 − 0 = 150`. Day 2: `150 + 150 − 0.05 × 150 = 292.5`.
2. Gap `= ln(160/80) / ln(1.12) = 0.693 / 0.113 ≈ 6.1`. They own about `20 − 6 = 14` of B.
3. The Mine's base payback must sit between the paybacks of the 8th and 9th Grandma: `100 × 1.15^7 = 266.0 s` and `100 × 1.15^8 = 305.9 s`. Times 47 CpS: a base price between about 12,502 and 14,377. (Check in the sheet; the boundaries themselves are ties.)
4. Any two of these: the Grandma-versus-Cursor gap grows from 2.90 to 4.25 and the Grandma-versus-Farm gap from 2.28 to 3.34, so the whole collection spreads out; every building's price rises more slowly, so the price of the 20th of anything drops from `1.15^19 ≈ 14.2` times its base to `1.10^19 ≈ 6.1` times, which speeds up the whole game's pacing; runs of the same building get longer before the player switches.

</details>

## Lab hook

**Lab 14, tune an idle economy** ([labs/lab14.md](../labs/lab14.md)). You build the payback sheet from the in-class activity with generic buildings, add a fifth building of your own design, hit three stated targets using goal seek and sensitivity tables, and write a tuning memo that names the knob you changed for each target and why. The sheet and memo become the tuning appendix of your final SDD.

## Sources

- The Cookie Clicker Wiki (wiki.gg), "Building" (current web version, accessed September 2026). Each purchase multiplies a building's price by 1.15; base prices and base CpS for Cursor (15, 0.1), Grandma (100, 1), Farm (1,100, 8) and Mine (12,000, 47). Cookie Clicker also has upgrades that change CpS, which this lecture's model leaves out on purpose.
- Old School RuneScape Wiki, "Experience" (current game, accessed September 2026), as cited in MA101 week 4 and GD203 week 7. The XP formula whose per-level cost doubles about every 7 levels, giving a growth factor of about `2^(1/7)`.
- Adams, E. & Dormans, J. (2012). *Game Mechanics: Advanced Game Design*. New Riders. Chapter 4, internal economies, feedback and equilibrium; chapter 8, simulating and balancing games.
- Meadows, D. H. (2008). *Thinking in Systems: A Primer*. Chelsea Green. Chapter 2, one-stock systems with a balancing loop.
- Microsoft Support, Excel "What-If Analysis" (Goal Seek and Data Table) and LibreOffice Help, Calc "Goal Seek" and "Multiple Operations" (current versions, accessed September 2026). Menu locations for the tools in section 3.
- The guild bank, the greedy purchase sequence, the gap tables and the tuning boundaries are computed from the models in this lecture and reproduced in the interactive and lab 14.

## Interactive spec: examples/w14-payback-braid.html

**The one insight the visual must make obvious:** rising prices look like buildings drifting apart, but for a best-value-next player they are a balancing loop. Every building's payback braids into one rising band, and ownership gaps stay constant at `ln(payback ratio) / ln g`.

**Layout.** Two linked charts side by side at 900 px and wider, stacked below that, with an ownership bar strip underneath.

- **Left chart, "Prices".** x axis: purchase number 1 to N (default N = 60). y axis: next price of each building on a linear scale (toggle "log scale", default off). One line per building, four colors from the shared palette. With linear scale the lines fan apart dramatically; that is the intended first impression.
- **Right chart, "Payback of the next purchase".** x axis: purchase number 1 to N. y axis: payback in seconds. Plot the greedy sequence: at purchase k, a dot colored by the building bought, at its payback. Also draw, as thin lines, each building's current next-purchase payback at every step. The four thin lines stay within one narrow band after the first ~17 purchases. Shade the band between the minimum and maximum of the four lines.
- **Ownership strip.** Four horizontal bars showing counts owned after purchase N, with the gap to Grandma printed on each bar ("Farm: 11, 2 behind Grandma"), and next to it the predicted gap `ln(ratio)/ln g` to two decimals.

**Controls** (keyboard accessible, numeric values visible):

- Growth factor `g`: slider 1.05 to 1.30, step 0.01, default 1.15.
- Mine base price: slider 8,000 to 30,000, step 100, default 12,000.
- Farm base price: slider 500 to 3,000, step 50, default 1,100.
- Purchases N: slider 20 to 120, default 60.
- Button "Reset to Cookie Clicker base numbers".
- Target readout: "Grandmas owned at first Mine: 7" (updates live), and "First Mine at purchase: 17".

**Model (exact).** Buildings: Cursor (15, 0.1), Grandma (100, 1), Farm (1,100, 8), Mine (12,000, 47), as (base price, CpS). Owned counts start at 0. At each purchase k = 1 … N, compute `payback_i = base_i × g^(owned_i) / cps_i`, buy the building with the smallest payback (ties go to the earlier building in the list Cursor, Grandma, Farm, Mine), record it, increment its count. Prices are not rounded.

**Test values** (`g = 1.15`, default prices unless stated):

- First 5 purchases: Grandma 100.0, Grandma 115.0, Grandma 132.3, Farm 137.5, Cursor 150.0.
- First Mine at purchase 17 with 7 Grandmas, 5 Farms, 4 Cursors owned.
- After 40 purchases: Cursor 10, Grandma 13, Farm 11, Mine 6.
- Predicted gaps: Grandma vs Cursor 2.90, vs Farm 2.28, vs Mine 6.71.
- Mine price 16,600: first Mine at purchase 25 with 10 Grandmas. Mine price 19,000: purchase 27, 10 Grandmas. Mine price 19,100: purchase 28, 11 Grandmas.
- `g = 1.10`: first Mine at purchase 24 with 10 Grandmas. `g = 1.20`: purchase 14 with 6 Grandmas.
- Predicted gaps at `g = 1.10`: 4.25, 3.34, 9.83. At `g = 1.20`: 2.22, 1.75, 5.14.

**Text summary** under the charts, one sentence, for example: "With g = 1.15 the player keeps about 3 more Grandmas than Cursors, 2 more than Farms and 7 more than Mines, and every purchase pays back within a few seconds of the last."

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`, light and dark themes, `prefers-reduced-motion` disables transitions. Buildings are drawn as plain colored shapes with text names; no Cookie Clicker art, fonts or logos. Colors are never the only cue: dots also carry a one-letter label (C, G, F, M) on hover and focus, and the ownership bars are labelled with text.
