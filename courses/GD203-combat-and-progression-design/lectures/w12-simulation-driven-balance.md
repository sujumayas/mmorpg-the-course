# GD203 · Week 12 — Simulation-Driven Balance

**Why this matters:** Your spreadsheet says a fight takes 4 hits. The player's fight takes 3, or 4, or 5, and whether they live depends on which. Spreadsheets compute averages. Players experience distributions. A simulation is how a designer sees the distribution before the players do.
**You will be able to:**
- Write a Monte Carlo combat simulation that produces a hits-to-kill distribution and a win rate, and validate it against an exact calculation.
- Compute how many simulated fights you need for a given precision, and report a win rate with a confidence interval.
- Explain, with numbers, why initiative and breakpoints swing win rates far more than averages suggest, and why variance helps the underdog.
- Design a parameter sweep that maps where a matchup is balanced.

**Before class:** Schreiber & Romero, *Game Balance* (2021), the chapter on probability and the chapter on simulation; Schreiber, *Game Balance Concepts*, level 10 ("Final Boss", which includes the course's spreadsheet tutorial). Install Python 3, or be ready to use a spreadsheet with a random-number function.
**Prerequisites from earlier courses:** MA102 week 11, [Monte Carlo simulation](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w11-monte-carlo-simulation.md), and week 13, [sampling and confidence](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md); GD203 week 4, [time-to-kill and time-to-die](w04-time-to-kill-and-time-to-die.md), for breakpoints and the first-strike rule; GD203 week 6, [critical hits and variance](w06-critical-hits-and-variance.md); GD203 week 11, [spreadsheet balancing workshop](w11-spreadsheet-balancing-workshop.md); CS101 week 13, randomness ([lecture](../../CS101-programming-for-games-i/lectures/w13-randomness-spawning-and-procedural-variety.md)).
**Interactive:** [Duel simulator](../examples/w12-duel-simulator.html) (built from the spec at the end of this lecture). Keep it open during section 2.

---

## 1. What a spreadsheet cannot tell you

Last week's sheet answered every question of the form "what is the average?" It cannot answer these:

- **How often?** How often does this fight take 5 hits instead of 4? How often does the player die to this elite?
- **Who goes first?** Week 4 showed that with discrete hits, the first strike can decide a duel. With random damage, the first strike matters some of the time. How much of the time?
- **What if the enemy is smart?** An enemy that heals itself at 30% health, or a player who saves a cooldown for the right moment, changes the fight in ways that depend on the fight's state.
- **What does this proc do?** A "10% chance on hit to deal bonus damage" effect interacts with every other stat. Closed-form formulas for such interactions get long and wrong.

A **Monte Carlo simulation** answers all of them the same way. You write down the rules of one fight as a program, including the dice. You run the fight thousands of times with fresh random numbers. You count outcomes. MA102 week 11 introduced the method. This week applies it to combat.

The players of World of Warcraft reached the same conclusion. SimulationCraft, a community tool, simulates a character's damage over thousands of fight iterations. Its documentation explains that it exists because proc-based effects and class synergies made traditional closed-form calculators inaccurate. Players today routinely pick gear by running a simulation instead of reading tooltips.

## 2. Worked example: what the average hides

### The hook

Two shipped games show the gap between the average and the answer.

In Doom (1993), the shotgun fires 7 pellets of 5, 10 or 15 damage each, for an average of 70 at point blank. An Imp has 60 health. The average says one blast kills an Imp. Work out the distribution and you find that even with every pellet hitting, about one Imp in eight survives the first blast.

In competitive Pokémon, players rarely ask how much damage an attack does. They ask a damage calculator such as the Pokémon Showdown calculator, and it answers with a probability, in the form "X% chance to 2HKO" (to knock out in two hits). Each hit's damage takes one of 16 random rolls, so "does it knock out?" has a probability, not a yes or no, and the community's main tool reports that probability first.

Both games tell you the same thing. Whether a fight is won is a question about a distribution. Spreadsheets give you its middle. Simulations give you the whole thing.

### The model

One fight is a loop. Here it is in Python, for an attacker whose hits can crit:

```python
import random

def hits_to_kill(rng, enemy_hp=50, base=10, crit_chance=0.25, crit_mult=2):
    hp, hits = enemy_hp, 0
    while hp > 0:
        hits += 1
        hp -= base * crit_mult if rng.random() < crit_chance else base
    return hits

rng = random.Random(42)                       # fixed seed: same results every run
runs = [hits_to_kill(rng) for _ in range(10_000)]
for k in sorted(set(runs)):
    print(k, runs.count(k) / len(runs))
```

Every symbol: `enemy_hp` is the target's health, `base` is the hit's normal damage, `crit_chance` is the chance a hit crits, `crit_mult` is the crit multiplier, and `rng` is a seeded random-number generator. The output is the **hits-to-kill distribution**, the share of fights that took 1, 2, 3, ... hits.

A **duel** is two of these loops interleaved. Attackers alternate swings, the one who goes first swings first, and the first to reach zero health loses. Run it thousands of times and count wins.

### Numbers you can check

Take a sword that deals 10 damage, with a 25% chance to crit for double. The average hit is `0.75 × 10 + 0.25 × 20 = 12.5`. The enemy has 50 health. A spreadsheet says `50 / 12.5 = 4` hits.

Now work out the real distribution by hand. After `k` hits with `c` crits, total damage is `10k + 10c`.

- **3 hits** kills only with at least 2 crits (`30 + 20 = 50`). Probability `3 × 0.25² × 0.75 + 0.25³ = 0.1406 + 0.0156 = 0.156`.
- **4 hits or fewer** needs at least 1 crit in 4 (`40 + 10 = 50`). Probability `1 − 0.75⁴ = 0.684`. So exactly 4 hits is `0.684 − 0.156 = 0.527`.
- **5 hits** always kills (`50`). The rest, `0.316`.

| Hits to kill | Probability | What the spreadsheet says |
|---|---|---|
| 3 | 15.6% | — |
| 4 | 52.7% | 4 hits, every time |
| 5 | 31.6% | — |
| Mean | 4.16 hits | 4.00 hits |

The mean is off by only 4%. The more important number is the third row. In almost a third of fights the crit sword is no faster than a plain 10-damage sword that never crits. That is the breakpoint effect from week 4, now with dice.

Now the duel. The enemy deals fixed damage and kills our hero with exactly its 4th attack. The spreadsheet says the hero kills in 4 and the enemy kills in 4, and week 4's rule says whoever swings first wins. Simulate instead:

| Situation | Spreadsheet (average) | True win rate for the hero |
|---|---|---|
| Hero swings first | Hero wins, 100% | 68.4% (hero needs ≤ 4 hits) |
| Enemy swings first | Hero loses, 0% | 15.6% (hero needs ≤ 3 hits) |

The average-based prediction is wrong in both rows, and wrong by a lot. Initiative still matters enormously (68% against 16%), but neither side is certain.

The two shipped games, worked the same way:

| Case | Average says | Distribution says |
|---|---|---|
| Doom shotgun (7 pellets, each 5, 10 or 15, all hit) vs Imp (60 health) | 70 ≥ 60, always one blast | One blast kills 87.5% of the time. Needs the 7 pellet rolls of 1-3 to sum to at least 12. |
| Pokémon, level 50, power-80 move vs same-level target (lecture 11 assumptions: 31-37 damage per hit, 175 HP) | 175 / 33.75 = 5.19 hits | Knocks out in 5 hits 7.7% of the time, otherwise 6 |

You can check the Doom line by counting. There are `3⁷ = 2,187` equally likely pellet combinations, and 1,913 of them sum to 12 or more. (Doom draws its random numbers from a fixed table, so the pellet rolls are close to, not exactly, uniform.)

### See it move

Open the interactive. The left view shows the spreadsheet's answer, a single bar at the average hits-to-kill and a verdict ("Hero wins" or "Hero loses"). The right view shows the simulated distribution as a histogram that fills in as fights run, with the win rate and its 95% confidence interval underneath.

Start with the crit sword and hero-first. The left view says 4 hits and a certain win. The right view grows three bars and settles near 68%. Flip "who swings first" and the left verdict flips to a certain loss while the right settles near 16%. Then slide crit chance down to 0. The histogram collapses to a single bar at 5, the left and right views finally agree, and the hero loses in both orders. With no randomness, the simulation must reproduce the spreadsheet exactly. That is how you check your simulation is correct.

### Cross-game recognition

**Doom.** The shotgun's seven small random pellets make a sum whose spread is narrow compared with its mean. That is why the Imp dies to one blast most of the time. A single pellet of 35 to 105 damage with the same average would one-shot the Imp far less reliably (about 65% of the time, 46 of the 71 values from 35 to 105, if each were equally likely). Many small random pieces give a tighter distribution than one big one, a fact MA102 week 8 covered with 2d6 against 1d12.

**Pokémon.** The 16-value damage roll spans 85% to 100% of the maximum. That is a narrow spread, chosen so that most matchups have a certain outcome and only matchups near a breakpoint depend on the roll. The Showdown calculator's habit of reporting "guaranteed" or "X% chance" is the distribution view made into a user interface.

**World of Warcraft and SimulationCraft.** Rotations, procs and cooldowns make a damage dealer's output a random process over minutes, not seconds. The community answer is the same loop at larger scale, thousands of iterations of a whole boss fight, reporting a mean and an error estimate. The method you just wrote is the same method, stripped down to one sword.

Three games, one idea. Whenever the question is "how often?" or "who wins?", compute the distribution, and do not trust a verdict built on an average near a breakpoint.

### Eyes-open design judgment

**Simulate when outcomes are near a breakpoint or depend on order.** If the average hits-to-kill is 4.9, the distribution spreads across 4, 5 and 6, and the average is a poor guide. If the average is 4.5 with a tiny spread, the spreadsheet is fine. A quick rule is to simulate whenever the average is within one standard deviation of a whole number of hits, or whenever turn order matters.

**Validate before you trust.** Turn randomness off and check the simulation matches the spreadsheet. Then check one case against an exact calculation, like the 68.4% above. A simulation that has never been checked is a random-number generator with opinions.

**The simulation only knows what you told it.** It will report a precise win rate for a fight in which the enemy AI always uses its strongest attack and the player never dodges. That number is precise and may be wrong for real play. State your assumptions next to every result, and treat AI and player policy as inputs to vary, not as facts.

**Randomness is a dial you set.** More variance means more upsets, fewer certain outcomes, and fights that feel less determined by stats. Section 5 shows exactly who benefits.

## 3. Building a combat simulation

A useful combat sim has five parts. Keep them separate so you can change one without breaking the others.

1. **State.** Everything the fight needs to know. Each combatant's health, resources, cooldown timers, buffs, and the clock.
2. **Rules.** Functions that take a state and an action and return a new state. "Attack resolves: roll crit, subtract mitigation, subtract health." These should be the same formulas as your spreadsheet, ideally read from the same exported data (week 11 section 4).
3. **Policy.** How each side chooses actions. For a first sim, a fixed priority list ("use the big attack when it is ready, otherwise the basic attack"). CS203 covers richer AI ([syllabus](../../CS203-artificial-intelligence-for-games/syllabus.md)).
4. **Loop.** Turn-based fights alternate turns. Real-time fights use an **event queue**, a list of future actions sorted by the time they happen. Pop the earliest event, resolve it, schedule the next one for that actor at `now + attack interval`. This handles combatants with different attack speeds without a fixed tick.
5. **Recorder.** Log what you need to answer your question. Winner, fight length, hits taken, overkill damage on the killing blow. Do not log everything by default, or ten thousand fights will fill your disk.

### Seeds and reproducibility

Always create the random-number generator with a **seed**, a fixed starting value, and record it with your results. The same seed gives the same sequence of random numbers, so a colleague can rerun your exact 10,000 fights. When you find a strange fight, the seed lets you replay it and step through it.

### Common random numbers

When you compare two designs (sword A against sword B), run both against the same sequence of random events. Seed each fight's generator from the fight number, so fight #347 rolls the same crits for both swords. The difference between the designs then comes from the design, not from luck. This technique is called **common random numbers**. Because both designs face the same luck, the noise in their difference drops, and you need fewer fights to see a real gap.

## 4. How many fights is enough?

A simulated win rate is an estimate. Its precision depends on the number of fights `N`. For a win rate `p`, the **standard error** is:

```
SE = sqrt(p × (1 − p) / N)
```

A 95% confidence interval is about `p ± 1.96 × SE`. For the hero-first duel, with `p ≈ 0.684`:

| Fights N | 95% interval half-width | Report as |
|---|---|---|
| 100 | ± 9.1 points | 68% ± 9 |
| 1,000 | ± 2.9 points | 68.4% ± 2.9 |
| 10,000 | ± 0.91 points | 68.4% ± 0.9 |
| 100,000 | ± 0.29 points | 68.4% ± 0.3 |

Every tenfold increase in fights buys about a threefold increase in precision, because of the square root. In one run of 100 fights we got a win rate of 80%. That is 2.5 standard errors from the truth, and nothing about the number warned us. With 10,000 fights, the same code landed at 69.2%, inside its interval.

Two practical rules follow.

- **Report the interval, always.** "68%" invites a colleague to argue with "70%". "68% ± 3" tells them the argument is noise.
- **Pick N from the decision.** If you only need to know whether a matchup is between 40% and 60%, a few hundred fights will do. If you are comparing two swords that differ by 1%, you need tens of thousands, or common random numbers. MA102 week 13 covers why small samples mislead; the same arithmetic governs your simulator.

## 5. Variance helps the underdog

Here is a result that changes how you think about randomness in combat. Two fighters, both with 50 health.

- **A** hits for 10 every swing. A needs 5 swings to kill B.
- **B** averages 9 per swing. With steady damage, B needs 6 swings and always loses.

Now give B a swingy weapon that deals 0 or 18 with equal odds. Same average, 9. B now wins when it lands 3 heavy hits (54 damage) before A lands its fifth swing.

| B's weapon | A swings first | B swings first |
|---|---|---|
| Steady 9 | B wins 0% | B wins 0% |
| 0 or 18 (avg 9) | B wins 31.3% | B wins 50.0% |

Check the first number. With A swinging first, B gets 4 swings before A's fifth. B needs at least 3 heavies in 4, probability `(4 + 1) / 16 = 31.25%`. With B first, B gets 5 swings and needs at least 3 of 5, probability `(10 + 5 + 1) / 32 = 50%`.

Flip it. Give the favorite the variance instead. A deals 0 or 20 (average 10), B deals a steady 9. A's win rate drops from 100% to 65.6% when A swings first.

The rule is general. **Variance helps whoever would lose on average.** The favorite wants a steady, predictable fight where the better stats show through. The underdog wants a coin-flippy one. As a designer, the amount of randomness in combat is a dial that sets how often the weaker side wins:

- In PvE, where the player is usually the favorite, high variance makes routine fights occasionally dangerous. That can be exciting, or it can feel unfair when a trash mob crits the player to death.
- In PvP, variance lets weaker players win sometimes, which keeps them playing, and lets stronger players lose sometimes, which frustrates them. A ranked mode and a casual mode of the same game can reasonably want different settings of this dial.
- In boss design, variance in the boss's damage tests the healer's reserve. A steady boss can be healed exactly. A swingy boss forces a safety margin.

## 6. Sweeps: mapping where a matchup is balanced

One simulation answers one question. A **sweep** runs the simulation across a grid of parameter values and plots the result. For example, sweep the hero's crit chance from 0% to 50% and the enemy's health from 40 to 70, run 2,000 fights at each grid point, and color each cell by the hero's win rate.

The result is a heatmap. The cells near 50% form a curved band, the **balance frontier**. Every design on that band is an even fight. The heatmap shows you three things a single number cannot. Where the frontier lies. How steep the slope is on either side (a steep slope means small changes swing the matchup, so the design is fragile). And where the jumps are, which are the breakpoints showing up as cliffs.

Combine the sweep with week 11's sensitivity analysis. The spreadsheet tells you which inputs move the averages. The sweep tells you which inputs move the outcomes. They are often not the same inputs.

## In-class activity (25 minutes)

Pairs, one laptop, Python or a spreadsheet.

1. **Build (10 min).** Write the `hits_to_kill` function from section 2 and a duel function that alternates swings. Use a seed.
2. **Validate (5 min).** Run 10,000 hero-first duels with crit chance 0.25. Your result must fall within 68.4% ± 0.9. Then set crit chance to 0 and confirm the hero wins 0%.
3. **Explore (10 min).** Find the crit chance at which the hero-first duel is exactly even (50%). Then find it for enemy-first. Report both with their confidence intervals.

Expected output: the two crit chances, the N you used, and one sentence on why they are so far apart.

## Common misconceptions

- **"If the average damage is above the target's health, it dies in one hit."** Only if the minimum damage is above it. The Doom shotgun averages 70 against 60 health and still fails about one time in eight.
- **"More simulation runs make the answer more correct."** More runs make it more precise. If the rules or AI policy are wrong, 100,000 runs give a very precise wrong answer.
- **"A win rate of 52% from 200 fights means A is favored."** The 95% interval is about ± 7 points. You cannot tell A from an even fight.
- **"Randomness makes games fairer."** Randomness helps the weaker side. Whether that is fair depends on who is weaker and why.

## Check yourself

1. A sword deals 10 damage with a 50% chance to crit for double. The enemy has 40 health. Give the hits-to-kill distribution and the mean.
2. Your simulator reports a 45% win rate from 400 fights. Compute the 95% interval. Can you conclude the matchup is unfavorable?
3. Using the underdog table, B has the 0-or-18 weapon and swings first. A gets a buff that lets it kill in 4 swings instead of 5. What is B's win rate now?
4. You want to know if sword X beats sword Y by at least 1 percentage point of win rate. Without common random numbers, roughly how many fights per sword do you need for a 95% interval of ± 0.5 points on each win rate near 50%?

<details>
<summary>Answers</summary>

1. Damage after `k` hits with `c` crits is `10k + 10c`. **2 hits** needs 2 crits: `0.25`. **3 hits or fewer** needs at least 1 crit in 3: `1 − 0.5³ = 0.875`, so exactly 3 is `0.625`. **4 hits** always kills: `0.125`. Mean `= 2 × 0.25 + 3 × 0.625 + 4 × 0.125 = 2.875`.
2. `SE = sqrt(0.45 × 0.55 / 400) = 0.0249`. Interval `45% ± 4.9`, from 40.1% to 49.9%. The interval sits just below 50%, so the matchup is probably unfavorable, but only barely. Run more fights before acting on it.
3. B swings first, then alternates. A's fourth swing comes after B's fourth, so B gets 4 swings and needs at least 3 heavies: `5 / 16 = 31.25%`.
4. `1.96 × sqrt(0.25 / N) = 0.005` gives `N ≈ 38,400` fights per sword.

</details>

## Lab / assignment hook

**Lab 12: Duel simulator** ([labs/lab12.md](../labs/lab12.md)). You build a seeded Monte Carlo duel simulator, validate it against three exact results from this lecture, and run a two-parameter sweep to map a balance frontier. It is the first part of the course's simulation assessment (20%).

## Sources

- id Software, *Doom* source code (linuxdoom-1.10, released 1997), files `p_pspr.c` and `info.c`. The shotgun fires 7 pellets of `5 × (1d3)`; the Imp has 60 spawn health (Doom and Doom II, 1993-1994). Random numbers come from a fixed 256-entry table, so rolls are close to uniform.
- Smogon University, "The Complete Damage Formula for Black & White" (generation V). The 16-value random roll from 85% to 100%. Bulbapedia, "Damage", for the same roll in later generations.
- Pokémon Showdown damage calculator (calc.pokemonshowdown.com) and its Smogon forum development thread. Reports knockout chances per number of hits, such as "X% chance to 2HKO", computed from the combinations of damage rolls (current as of 2026).
- SimulationCraft project (simulationcraft.org) and Warcraft Wiki, "SimulationCraft". An event-driven World of Warcraft combat simulator; its documentation gives proc-based effects and class synergy as the reason closed-form calculators became inaccurate (retail World of Warcraft, ongoing).
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press.
- Schreiber, I. (2010). *Game Balance Concepts*, level 10, "Final Boss", 8 September 2010, which has the course's Excel tutorial section. https://gamebalanceconcepts.wordpress.com/2010/09/08/level-10-final-boss/

## Interactive spec: examples/w12-duel-simulator.html

**The one insight.** An average-based prediction gives one verdict. A simulation of the same fight gives a distribution and a win rate that can be far from that verdict, and the gap is largest near breakpoints and when turn order matters. With randomness turned off, the two views must agree.

**Layout.** Two linked views, stacked on mobile, side by side at 1024 px and wider.

- **Left: the spreadsheet view.** One bar at `ceil(enemy HP / mean hit)` hits-to-kill, the mean hit value, and a verdict line ("Hero wins" or "Hero loses") from the rule: hero wins if its average hits-to-kill `≤` enemy's hits-to-kill when the hero swings first, `<` when the enemy swings first.
- **Right: the simulation view.** Histogram of simulated hero hits-to-kill (bars labelled with percentages to 1 decimal), the exact distribution drawn as outline markers over the bars, and below it "Hero wins X% ± Y (95%, N fights)". Also a small running line chart of win rate against fights run, with the interval band, so students see it converge.

**Controls.**
- Hero: base damage (1-30, default 10), crit chance (0-100%, step 1, default 25%), crit multiplier (1.5, 2, 3; default 2).
- Enemy: health (10-150, default 50), enemy hits-to-kill-hero (1-10, default 4; the enemy deals fixed damage).
- Who swings first: hero / enemy (default hero).
- Fights: 100, 1,000, 10,000 (default 1,000); "Run" and "Run +1,000" buttons; seed field (default 42) with a "new seed" button.
- Preset tab "Underdog": A steady 10 vs B with selectable weapon (steady 9, or 0/18 at 50%), both 50 HP, first-swinger toggle.
- Preset tab "Doom shotgun": 7 pellets of 5 × (1d3), target health slider 20-200 (default 60), shows one-blast kill chance.

**Formulas.**
- Hero hit: `base × mult` with probability `crit`, else `base`.
- Exact hits-to-kill distribution by dynamic programming over accumulated damage, for the overlay.
- Duel, hero first: hero wins if hero hits-to-kill `≤ enemyHTK`. Enemy first: hero wins if `≤ enemyHTK − 1`.
- 95% interval: `1.96 × sqrt(p(1 − p) / N)`.
- Use a seedable PRNG (for example mulberry32) so a given seed reproduces results.

**Test values (exact overlay and simulated results within the interval).**
- Defaults: hits 3 / 4 / 5 at 15.6% / 52.7% / 31.6%; hero-first win 68.4%; enemy-first win 15.6%; left view shows 4 hits and "Hero wins".
- Crit chance 0: single bar at 5 hits, both views say "Hero loses", simulated win 0.0%.
- Crit chance 50%, enemy HP 40: 2 / 3 / 4 hits at 25% / 62.5% / 12.5%, mean 2.875.
- Underdog: B with 0/18, A first → B wins 31.25%; B first → 50.0%. Steady 9 → 0%.
- Doom shotgun (exact, by enumerating all 2,187 pellet combinations): health 60 → 87.47% (1,913 / 2,187); health 70 → 58.98% (1,290 / 2,187); health 80 → 24.69% (540 / 2,187); health 100 → 0.37% (8 / 2,187).

**First screen.** Defaults with 1,000 fights already run, so the left view says "Hero wins" and the right says about 68%. The "who swings first" toggle is the most prominent control.

**Accessibility and motion.** Histogram bars animate in over 300 ms, instant under `prefers-reduced-motion`. All controls keyboard-operable. Numbers are text, not only drawn on canvas.
