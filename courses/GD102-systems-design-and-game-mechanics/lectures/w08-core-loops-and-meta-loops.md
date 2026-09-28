# GD102 · Week 08 — Core loops and meta loops

**Why this matters:** Pitch meetings, design documents and postmortems all ask "what is the core loop?" Most answers are a circle of verbs with arrows between them, and that circle predicts nothing. This week you learn to write a loop as a system with a rate of return and a constraint, so you can say when the loop will stop growing and what the meta loop has to do about it.

**You will be able to:**
- Identify a game's core loop and meta loop, and name the resource that connects them.
- Compute the growth of a reinvesting core loop and find the cycle at which a constraint turns compounding into linear growth.
- Decide which of two options is better by first identifying the binding constraint, and show with numbers that the answer flips when the constraint changes.
- Critique a meta loop by asking which constraint of the core loop it moves, and whether it changes numbers or verbs.

**Before class:** Adams & Dormans, *Game Mechanics: Advanced Game Design* (2012), chapter 7 "Design Patterns", the engine patterns (static engine, dynamic engine, converter engine, engine building), with appendix B for the pattern summaries. Meadows, *Thinking in Systems* (2008), chapter 2, the section on a stock with one reinforcing loop and one balancing loop. Play 20 minutes of any roguelite or farming game and write down every action you repeat more than five times.

**Prerequisites from earlier courses:** From this course, [week 3, positive feedback](w03-positive-feedback-loops-snowballing.md), [week 4, negative feedback loops](w04-negative-feedback-loops-rubber-banding.md), [week 5, Machinations diagrams I](w05-machinations-diagrams-i.md) and [week 7, internal economies](w07-internal-economies-sources-drains-converters.md). Compounding growth `a · b^n` from MA101 [week 4, exponentials](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w04-exponentials-and-the-xp-curve.md), and caps written with `min` from MA101 [week 7, piecewise caps and floors](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w07-piecewise-caps-and-floors.md). MDA (loops are dynamics, not mechanics) from GD101 [week 4](../../GD101-introduction-to-game-design/lectures/w04-mda-mechanics-dynamics-aesthetics.md).

**Interactive:** [Farm loops: compounding until the watering limit binds](../examples/w08-farm-loops.html). Keep it open during section 2.

---

## 1. What a loop is, and what makes it "core"

A **loop** in game design is a cycle of player actions whose output feeds back into its own input. You kill monsters, they drop loot, the loot makes you stronger, being stronger lets you kill bigger monsters. The last step leads back to the first. In the language of week 1, a loop is a closed chain of relationships, and like every loop you have drawn so far it is either reinforcing or balancing.

The **core loop** is the loop the player repeats most often, whose output the rest of the game consumes. It is usually short, from a few seconds to a few minutes. If you took it out, you would have a different game.

A **meta loop** is a longer cycle that spends the output of the core loop to change the core loop itself or the options around it. It runs on a slower clock: hours, days or runs rather than seconds. Unlocking a new weapon type, upgrading a building, buying a permanent stat boost between roguelite runs: each is a turn of a meta loop.

Games usually stack several loops on different clocks. A useful way to find them is to ask, for each action, "how long until I do this again?"

| Clock | Typical length | What happens | Example of the question |
|---|---|---|---|
| Moment-to-moment | 1-10 seconds | Aim, dodge, click, water one tile | Did that input feel good? |
| Core loop | 1-30 minutes | A fight, a run, a farm day | Was that cycle worth it? |
| Meta loop | Hours to days | Upgrades, unlocks, levels | What will I spend it on? |
| Long arc | Weeks to months | Seasons, story, collection | Why am I still here? |

Two tests separate a real core loop from a list of features.

1. **It produces the currency the next clock spends.** If the meta loop buys upgrades with gold, the core loop is whatever makes gold. If the core loop and the meta loop use unrelated resources, the loops are not connected and one of them will feel pointless.
2. **Its output can be reinvested.** A core loop whose output feeds its own input is a reinforcing loop, the engine that week 3 warned you about. A core loop whose output only feeds the meta loop is a static engine in Adams and Dormans' terms: it pays a steady rate and does not grow by itself.

The worked example shows what happens when the two tests meet a limit.

## 2. Worked example: a farm that should have made fifteen thousand gold

### The hook

In Stardew Valley (current 1.6-era version), parsnip seeds cost 20 gold at Pierre's General Store. A parsnip takes 4 days to grow and sells for 35 gold. That is a 75% return every 4 days. A season lasts 28 days, which is seven parsnip harvests.

Suppose you start spring with 300 gold, plant everything, sell everything, and plant again. On paper your gold multiplies by 1.75 every harvest:

```
300 × 1.75^7 = 300 × 50.27 ≈ 15,080 gold
```

No player's first spring looks like that. The farm grows fast at first and then, somewhere in the middle of the month, it stops accelerating. Nothing in the price list changed. What stopped it?

### The model

The core loop is plant, water, harvest, sell, buy seeds. Write it as one cycle per harvest.

```
n_k     = min( floor(G_k / c), W )
G_(k+1) = G_k + (p − c) × n_k
W       = floor( E / w )
```

- `G_k` is your gold at the start of cycle `k`.
- `c` is the seed cost (20 for parsnip) and `p` is the sale price (35).
- `n_k` is how many tiles you plant this cycle. You plant as many as you can afford, up to a limit.
- `W` is the **watering limit**: the most tiles you can water in one day.
- `E` is the energy bar. The Stardew Valley Wiki gives a maximum of 270.
- `w` is the energy cost of one watering can use. It is 2 at Farming level 0 and falls by 0.1 per Farming level, so `w = 2 − 0.1 × L`.

This is a model, and it simplifies on purpose. It ignores the energy you spend tilling soil, the walks to refill the can (which holds 40 uses at the start), the season's first and last days, crop quality and everything else you might do with your day. Every simplification makes the real farm grow slower than the model, so the model is an upper bound.

The `min` in the first line is the whole story. The core loop has two limits. **Gold** limits how many seeds you can buy. **Energy** limits how many tiles you can water. Whichever is smaller is the **binding constraint**, the one that actually decides `n_k`.

While gold binds, `n_k` grows with `G_k`, so gold grows by a fixed factor each cycle: `G_(k+1) ≈ G_k × p / c = 1.75 × G_k`. That is a reinforcing loop, and it compounds. Once energy binds, `n_k = W` every cycle, and gold grows by a fixed amount: `(p − c) × W` per cycle. That is linear. The loop has not broken. Its binding constraint has moved.

### Numbers you can check

At Farming level 0, `W = floor(270 / 2) = 135` tiles. Start with 300 gold and hold the level at 0 (the "fixed limit" column). Then let Farming XP raise the level (the "levels on" column). Each parsnip harvest gives 8 Farming XP, and the wiki's XP table puts level 1 at 100 XP, level 2 at 380, level 4 at 1,300, level 5 at 2,150 and level 6 at 3,300.

| Day | Unlimited: tiles / gold | Fixed limit 135: tiles / gold | Levels on: limit / tiles / gold |
|---|---|---|---|
| 4 | 15 / 525 | 15 / 525 | 135 / 15 / 525 |
| 8 | 26 / 915 | 26 / 915 | 142 / 26 / 915 |
| 12 | 45 / 1,590 | 45 / 1,590 | 142 / 45 / 1,590 |
| 16 | 79 / 2,775 | 79 / 2,775 | 150 / 79 / 2,775 |
| 20 | 138 / 4,845 | **135** / 4,800 | 168 / 138 / 4,845 |
| 24 | 242 / 8,475 | **135** / 6,825 | 180 / **180** / 7,545 |
| 28 | 423 / 14,820 | **135** / 8,850 | 192 / **192** / 10,425 |

Bold entries are cycles where energy binds. Check the first rows by hand: 300 gold buys 15 seeds, which return `15 × 35 = 525`. That buys 26 seeds (26 × 20 = 520, with 5 gold left over), which return `5 + 26 × 35 = 915`. The unlimited column ends at 14,820 rather than 15,080 only because you cannot buy a fraction of a seed.

For four cycles the three farms are identical. Then the fixed-limit farm hits 135 tiles on day 20 and from then on gains exactly `15 × 135 = 2,025` gold per cycle. By day 28 it has 8,850 gold, 60% of the unlimited farm. The farm with levels does better (10,425) because the Farming level raises the watering limit from 135 to 192 tiles over the month. That is a meta loop at work. Harvests produce XP, XP raises the level, the level lowers the energy cost of watering, and the lower cost lifts the constraint.

Open the interactive. The left chart plots gold on a logarithmic axis, where compounding growth is a straight line. The dashed "on paper" line is `300 × 1.75^k`. Your farm follows it exactly, then bends away on the cycle the watering limit binds. The right chart shows tiles planted against the watering limit, so you can see the two lines meet. Switch "Farming levels" on and watch the limit line climb in steps. Then drag the sprinkler slider.

### The meta loop's real job: move the constraint

Farming levels lift the limit slowly. Even at Farming level 10, `w = 1` and `W = 270`, only double the level-0 limit. The bigger meta move in Stardew is the sprinkler. The wiki lists three: the basic sprinkler (recipe at Farming level 2) waters the 4 adjacent tiles, the quality sprinkler (level 6) waters 8, and the iridium sprinkler (level 9) waters 24, every morning, for no energy. Their ingredients are metal bars, which come from a different core loop: mining.

In the interactive, add 10 quality sprinklers. They water 80 tiles, which raises the limit from 135 to 215 at level 0. With levels on, the farm ends spring at 12,555 gold instead of 10,425. Sprinklers do something Farming levels do not. They remove a verb. A player with enough sprinklers stops watering and spends the morning on something else: mining for more bars, fishing, talking to villagers. The meta loop did not make the core loop faster. It changed what the core loop is.

This is the general pattern:

> A core loop grows until a constraint binds. A meta loop is worth building when it moves that constraint. The best meta loops change which verbs the core loop contains, not only its numbers.

### Which crop is better? It depends on the constraint

Here is the question that makes the constraint idea useful. Cauliflower seeds cost 80 gold, take 12 days, and sell for 175. Is cauliflower better than parsnip?

Compute two different rates.

| Crop | Growth factor per day (gold binds) | Profit per tile per day (tiles bind) |
|---|---|---|
| Parsnip | `1.75^(1/4) = 1.150`, about +15.0% a day | `(35 − 20) / 4 = 3.75` gold |
| Cauliflower | `(175/80)^(1/12) = 1.067`, about +6.7% a day | `(175 − 80) / 12 = 7.92` gold |

If gold is your binding constraint, parsnip wins: your money compounds more than twice as fast. If watering is your binding constraint, cauliflower wins: each tile you can water earns more than twice as much. Start the month with 20,000 gold and a 135-tile limit, and both crops fill all 135 tiles from day 1. Parsnips earn `135 × 15 = 2,025` per 4-day cycle, 7 cycles, 14,175 gold profit. Cauliflowers earn `135 × 95 = 12,825` per 12-day cycle, 2 cycles in 24 days, 25,650 gold profit.

The same two crops, the same prices, and the "better" crop flips. Asking "which is better?" without asking "what is binding?" is the most common analysis mistake in systems design. You will meet the same idea in MMO303 [week 12, stat weights and theorycrafting](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w12-stat-weights-and-theorycrafting.md), where the value of a stat changes when a different stat becomes the limit.

### Cross-game recognition

Every roguelite is a core loop (a run) feeding a meta loop (permanent upgrades). Rewrite each one as: core loop, output currency, constraint, meta sink, what the meta sink moves.

**Rogue Legacy (2013).** Core loop: one heir's attempt at the castle. Output: gold. When the heir dies, you pick one of three randomly generated heirs and spend gold on the manor, which raises stats such as health and mana and unlocks classes. Constraint: the heir's survival. Meta sink: manor upgrades. The distinctive rule is that any gold you have not spent must be paid to Charon to enter the castle again, though upgrades can reduce the amount. That turns the whole output of each run into a meta-loop input. There is no saving across runs. The designers removed the option to hoard, which forces every core loop to end in a meta decision.

**Vampire Survivors (1.0, October 2022).** Core loop: a stage session with a soft time limit of 15, 20 or 30 minutes depending on the stage, after which a powerful enemy called the Reaper appears. Output: gold coins. Meta sink: characters and persistent power-ups bought between sessions. Constraint: how long you survive within the session. Each power-up raises your survival, which raises the gold you collect next session. That is the reinforcing loop from the Stardew example, run across sessions instead of seasons.

**Hades (full release September 2020).** Core loop: an escape attempt through the Underworld. When Zagreus is defeated, the river Styx carries him back to the House of Hades, which works as the game's hub between attempts. Some currencies are lost on death and some carry over to buy permanent upgrades that affect future attempts. Constraint: survival depth. Meta sink: permanent upgrades at the House. Hades splits its currencies into ones that die with the run and ones that survive it, which lets the designers decide exactly how much of each run's output reaches the meta loop.

Three games, one structure. In each, a failed core loop still pays into the meta loop, which is why a lost run does not feel like lost time. And in each, the meta sink raises the constraint that ended the run.

### Eyes-open design judgment

- **Strength of a reinforcing core loop:** the early game feels fast and generous. Doubling your farm every few days is exciting, and the player learns the loop by watching it pay off.
- **Cost:** compounding without a constraint breaks any economy within a few cycles. The unlimited farm reaches 14,820 gold in one month and would reach millions by the next. Someone has to design the constraint, and you should choose it, not discover it.
- **Choose the constraint deliberately.** Energy in Stardew, survival in a roguelite, run length in Vampire Survivors. A good constraint is one the player can see and plan around, and one a meta loop can move.
- **Meta loops that only change numbers** (5% more damage) are easy to add and quickly feel like a tax on time. Meta loops that change verbs (sprinklers, a new weapon type, a new class) are expensive to build and keep the core loop fresh.
- **Watch for the meta loop overtaking the core loop.** If permanent upgrades grow faster than content difficulty, the core loop stops asking anything of the player. Week 9 measures this exactly: how much power substitutes for how much skill.
- **Decide deliberately** how much of each core loop's output reaches the meta loop. Rogue Legacy forces all of it. Hades passes some and burns some. Stardew lets you save. Each choice changes whether players feel pushed to spend or free to plan.

## 3. The link between loops: exchange rate and cadence

Two numbers describe how a core loop connects to a meta loop.

The **exchange rate** is how much core-loop output one meta step costs, measured in core loops. If an upgrade costs 1,000 gold and a run pays 250, the exchange rate is 4 runs per upgrade.

The **cadence** is the exchange rate times the length of one core loop. Four runs of 20 minutes is one upgrade every 80 minutes. Cadence is what players feel. "I get something every session" and "I get something every few days" are cadence statements.

Cadence changes over time for two reasons. Meta costs usually rise with each purchase, which slows it. Meta upgrades usually raise core-loop output, which speeds it up. If a meta upgrade's cost rises by a factor `g` per purchase and core-loop income rises by a factor `h` per purchase, the exchange rate multiplies by `g / h` each time.

```
runs per upgrade (k-th) = (cost_0 / income_0) × (g / h)^k
```

- If `g = h`, cadence stays constant forever.
- If `g > h`, cadence slows exponentially, and eventually the meta loop feels finished.
- If `g < h`, cadence speeds up. The meta loop becomes a runaway reinforcing loop and upgrades pour in faster than players can use them.

Most designers want `g` a little above `h`, so that each upgrade takes slightly longer than the last and the meta loop winds down gradually, ending somewhere near the point where the content runs out. Week 14's spreadsheet lecture tunes exactly this ratio with idle-game prices: see [week 14, tuning with spreadsheets](w14-tuning-with-spreadsheets.md).

### Drawing loops in Machinations

In the diagram language from [week 5](w05-machinations-diagrams-i.md), a reinvesting core loop is a pool of gold feeding a converter (buy seeds) that feeds a delayed source (the crop grows) that pays back into the pool. The watering limit is a cap on the converter's rate. A meta loop is a second pool (XP, bars) whose state modifies the cap through a label on a state connection, which is [week 6](w06-machinations-diagrams-ii-converters-traders-gates.md) material. If your diagram has no cap on a reinforcing loop, the diagram is telling you your game has no constraint yet.

## 4. Loops in persistent games

In a single-player game the long arc ends. In an MMO it must not. That changes what meta loops are for.

A single-player meta loop can wind down, because the game is meant to be finished. An MMO needs meta loops that keep turning for years, and it needs them to turn at a similar rate for players who log in for one hour a week and players who log in for six hours a day. MMOs usually handle this with **time gates**: meta rewards limited per day or per week, so that the hardcore player's extra hours go into the core loop's other outputs rather than into faster meta progress. A time gate is a constraint on the meta loop's inflow, placed by the designer instead of emerging from the core loop.

Time gates solve the cadence problem across very different players, and they create their own trouble: players feel obliged to log in on the gate's schedule. That tension between healthy habits and obligation is an ethics question as much as a systems one, and MMO403 returns to it (see the [MMO403 syllabus](../../MMO403-business-monetization-and-ethics-of-live-games/syllabus.md)). For now, note that a time gate is a design tool with a cost, and that you should be able to say which constraint it replaces.

## In-class activity (25 minutes)

Work in groups of three. Pick one game that at least two of you have played for more than ten hours.

1. **Clock table (8 min).** Fill in the four-row clock table from section 1 for your game. For each row, name the action and the resource it produces.
2. **Constraint (7 min).** For the core loop, write its version of `n = min(A, B)`. What are the two (or more) limits? Which one binds in the first hour, and which one binds after ten hours? Sketch gold (or the main currency) against time and mark the bend.
3. **Meta move (5 min).** Name the meta upgrade that moves the late-game constraint. Does it change numbers or verbs?
4. **Redesign (5 min).** Propose one change that moves the bend earlier or later by about 50%, and say which parameter of your `min` it touches.

Expected output: a completed clock table, a one-line `min` formula with both limits named, a sketch with the bend marked, and a one-sentence redesign. Groups present in 60 seconds each.

## Common misconceptions

- **"The core loop is the genre."** "Shoot things" is a genre. A core loop names the output and what it feeds. "Clear a room, collect currency, spend it on a boon, clear a harder room" is a loop.
- **"If the core loop compounds, the game gets more exciting forever."** Compounding always meets a constraint, designed or not. If you did not design one, the constraint will be something like inventory space or the player's patience, and it will feel like a bug.
- **"There is one best option."** Which crop, weapon or build is best depends on which constraint binds. When the constraint moves, the best option can flip, as parsnip and cauliflower do.
- **"Meta loops add engagement, so more meta loops is better."** Each meta loop needs a currency from some core loop and a constraint it moves. A meta loop that moves nothing is a sink the player resents.

## Check yourself

1. A crop costs 40 gold, sells for 100 and takes 6 days. Compute its growth factor per day when gold binds and its profit per tile per day when tiles bind. Against parsnip, which crop wins in each case?
2. In the model, you are at Farming level 5 and have 3,000 gold at the start of a cycle. How many parsnip tiles do you plant? How much gold do you have after the harvest?
3. A roguelite pays 200 gold per run. The first upgrade costs 600 gold and each later upgrade costs 1.3 times the previous one. Each upgrade raises gold per run by 10%. How many runs does the 1st upgrade take? The 6th? Is the meta loop speeding up or slowing down?
4. A designer says: "Players stop playing our farming game after day 20 because progress feels slow. Let's raise crop prices 20%." Using the model, explain why this may not help, and propose a change that targets the constraint instead.

<details>
<summary>Answers</summary>

1. Gold binds: `(100/40)^(1/6) = 2.5^(1/6) ≈ 1.165`, about 16.5% a day, slightly better than parsnip's 15.0%. Tiles bind: `(100 − 40)/6 = 10` gold per tile per day, better than parsnip's 3.75. The new crop wins in both cases.
2. At level 5, `w = 1.5` and `W = floor(270/1.5) = 180`. Gold allows `floor(3,000/20) = 150`. The smaller limit is gold, so you plant 150 tiles. After harvest: `3,000 + 15 × 150 = 5,250` gold.
3. First upgrade: 600/200 = 3 runs. Costs grow by `g = 1.3` and income by `h = 1.1` per upgrade, so the 6th upgrade (k = 5) takes `3 × (1.3/1.1)^5 = 3 × 2.30 ≈ 6.9` runs, so 7 runs. The meta loop is slowing down, because `g > h`.
4. After day 20 the watering limit binds, so gold grows by `(p − c) × W` per cycle. A 20% price rise raises the per-cycle gain from 15 to 22 gold per tile, a 47% gain, which helps, but it also speeds up the early compounding and moves the bend earlier. A change that targets the constraint (earlier access to sprinklers, or a lower watering cost) raises `W` and keeps the gold-per-tile economy intact.

</details>

## Lab hook

**Lab 08, loop anatomy and the bend** ([labs/lab08.md](../labs/lab08.md)). You rebuild the parsnip model in a spreadsheet, confirm the table above, add a second crop and sprinklers, and then write a loop anatomy of a game of your choice with its binding constraint. The loop anatomy is reused in the final system design document.

## Sources

- Stardew Valley Wiki (current 1.6-era game, accessed September 2026): "Parsnip" (4 days, sells for 35g, 8 Farming XP), "Parsnip Seeds" (20g at Pierre's), "Cauliflower" (12 days, 175g), "Cauliflower Seeds" (80g at Pierre's), "Farming" (XP table, levels 1-10; harvest XP formula), "Skills" (tool energy 2 at level 0, minus 0.1 per level), "Watering Can" (40 uses; maximum energy 270), "Sprinkler" (4, 8 and 24 tiles; recipes at Farming levels 2, 6 and 9), "Seasons" (28 days per season), "Day Cycle" (0.7 real seconds per game minute).
- Wikipedia, "Rogue Legacy" (2013 release, accessed September 2026): a choice of three generated heirs, manor upgrades to stats and classes, unspent gold paid to Charon to enter the castle, reducible by upgrades.
- Wikipedia, "Vampire Survivors" (accessed September 2026): session limits of 15, 20 or 30 minutes, the Reaper, gold for persistent power-ups, 1.0 release 20 October 2022.
- Wikipedia, "Hades (video game)" (accessed September 2026): full release 17 September 2020; return to the House of Hades on defeat; currencies lost on death versus currencies for permanent upgrades.
- Adams, E. & Dormans, J. (2012). *Game Mechanics: Advanced Game Design*. New Riders. Chapter 7 and appendix B (engine patterns).
- Meadows, D. H. (2008). *Thinking in Systems: A Primer*. Chelsea Green. Chapter 2.

## Interactive spec: examples/w08-farm-loops.html

**The one insight.** Gold compounds along the "on paper" exponential until the watering limit binds, then bends to a straight line. The bend is visible on a log axis as the moment the farm's line peels away from the dashed line. Meta upgrades (levels, sprinklers) move the bend; they do not change the early slope.

**Layout.** Two linked charts side by side on desktop, stacked on mobile. Controls below. Cycle table under the controls.

**Left chart, "Gold".** x = day (0 to 28), y = gold on a log axis (toggle to linear). Series: the farm's gold at the end of each cycle (solid, markers at each harvest), and the "on paper" line `G_0 × (p/c)^k` (dashed). A vertical marker at the first cycle where energy binds, labelled "Watering limit reached (day X)".

**Right chart, "Tiles vs limit".** x = day, y = tiles. Bars for `n_k`, a step line for the limit `W_k`. Bars that equal the limit are filled in the accent color; others are outlined.

**Controls.**
- Crop: Parsnip (c = 20, p = 35, 4 days, 8 XP) or Cauliflower (c = 80, p = 175, 12 days, 23 XP).
- Starting gold `G_0`: slider 100 to 20,000 (log-scaled), default 300.
- Energy limit on/off (default on). Off means `W` is infinite.
- Farming levels on/off (default off, so the first view shows the fixed limit of 135).
- Quality sprinklers: slider 0 to 40, default 0. Each adds 8 tiles to `W`.
- Season length: fixed 28 days; cycles that would end after day 28 are not run.

**Formulas.**
- `W_k = floor(270 / (2 − 0.1 × L_k)) + 8 × S` (use `L_k = 0` when levels are off).
- `n_k = min(floor(G_k / c), W_k)`.
- `G_(k+1) = G_k + (p − c) × n_k`.
- `XP_(k+1) = XP_k + xp × n_k`, where xp is 8 (parsnip) or 23 (cauliflower). `L` is the highest level whose threshold XP has been reached, thresholds `[0, 100, 380, 770, 1300, 2150, 3300, 4800, 6900, 10000, 15000]`. The level updates after the harvest and applies from the next cycle.

**Readouts (copyable table).** One row per cycle: day, level, limit `W`, tiles `n`, gold at end, XP. Summary line: gold at day 28, day the limit first binds, and the ratio of final gold to the "on paper" value.

**Test values (must match).**
- Parsnip, 300 g, limit on, levels off: gold 525, 915, 1,590, 2,775, 4,800, 6,825, 8,850 on days 4 to 28; limit binds on day 20.
- Parsnip, 300 g, limit on, levels on: limits 135, 142, 142, 150, 168, 180, 192; tiles 15, 26, 45, 79, 138, 180, 192; final gold 10,425; final XP 5,400 (level 7).
- Parsnip, 300 g, limit off: final gold 14,820. "On paper" at day 28: 15,080 (rounded).
- Parsnip, 300 g, levels on, 10 sprinklers: final gold 12,555.
- Parsnip, 20,000 g, levels off: final gold 34,175. Cauliflower, 20,000 g, levels off: gold 32,825 at day 12 and 45,650 at day 24.
- Cauliflower, 300 g, levels on: tiles 3 then 7, gold 585 then 1,250.

**Accessibility.** All controls keyboard operable with visible labels and values. `aria-live` summary: "Watering limit reached on day 20. Final gold 8,850, 59% of the on-paper value." No animation under `prefers-reduced-motion`. Series distinguished by line style and markers as well as color.
