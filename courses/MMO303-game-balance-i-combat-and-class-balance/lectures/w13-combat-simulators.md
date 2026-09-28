# MMO303 · Week 13 — Combat Simulators

**Why this matters:** Once a class has procs, cooldowns and a priority list, no spreadsheet can tell you its damage, and no single test fight can either. A combat simulator plays the fight thousands of times and tells you the average, the spread and how sure you are. Without that last number, you will buff the wrong class.

**You will be able to:**
- Compute the expected value and standard deviation of per-fight DPS for a class with random critical hits, and check a simulator against them.
- Compute how many simulated fights you need to rank two classes whose averages differ by a given gap.
- Design the core loop of an event-driven combat simulator: state, clock, action policy, random numbers and output.
- Critique a balance claim that rests on a small number of fights or on an unvalidated simulator.

**Before class:** Schreiber & Romero, *Game Balance* (2021), the chapter on simulation and the chapter on probability; the SimulationCraft wiki pages "StatisticalBehaviour" and "ActionLists" (short, both linked in Sources).

**Prerequisites from earlier courses:** Monte Carlo simulation ([MA102 week 11](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w11-monte-carlo-simulation.md)) and sampling error ([MA102 week 13](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md)); simulation-driven balance ([GD203 week 12](../../GD203-combat-and-progression-design/lectures/w12-simulation-driven-balance.md)) and time-to-kill ([GD203 week 4](../../GD203-combat-and-progression-design/lectures/w04-time-to-kill-and-time-to-die.md)); effective HP from [MMO303 week 2](w02-armor-and-damage-mitigation.md); stat weights from [MMO303 week 12](w12-stat-weights-and-theorycrafting.md).

**Interactive:** [`examples/w13-monte-carlo-dps.html`](../examples/w13-monte-carlo-dps.html). Keep it open during section 2.

---

## 1. What a simulator answers that a spreadsheet cannot

Up to now in this course you have mostly worked with expected values. Expected damage per hit is base damage times one plus crit chance times the extra crit damage. Effective HP is health times the armor multiplier. These formulas are exact for the average, and a spreadsheet handles them well.

A spreadsheet starts to fail in three situations, and a real MMO class hits all three.

**State.** Many abilities depend on what happened earlier. A proc (a random chance for an effect to trigger) might have an internal cooldown, so it cannot trigger again for 10 seconds. A resource like rage or combo points builds up and gets spent. A buff lasts 8 seconds and changes which button you press next. The value of the next action depends on the history of the fight, and the history is random.

**Decisions.** A player does not press buttons in a fixed rotation. They follow a priority: "use the big cooldown if it is ready, else spend resources if you have 5, else use the builder." Which branch fires depends on state, so the order of actions differs from fight to fight.

**Spread.** Even when the average is easy, you may care about the distribution. How often does a healer run out of mana before the boss dies? How often does a burst class fail to kill a target inside a 3-second window? These are questions about the tails, and an average says nothing about tails.

A **combat simulator** is a program that plays out a fight step by step, with the game's real rules, and records what happened. A **Monte Carlo** simulator runs that fight many times with different random numbers and reports statistics across the runs. Each run is called an **iteration**.

The rest of this lecture is about using that tool honestly. The key idea is simple. Every number a Monte Carlo simulator gives you is an estimate, and every estimate has an error bar. If you do not know the error bar, you do not know what the simulator said.

## 2. Worked example: one fight lies

### The hook

SimulationCraft is the open-source simulator World of Warcraft players use to compare gear, talents and rotations. The web service Raidbots runs it in the cloud, so players can sim without installing anything. By default, SimulationCraft does not run a fixed number of fights. It keeps running iterations until its estimate of the statistical error drops to 0.2% of the result, with a ceiling of one million iterations. Its default fight also has a length of 300 seconds, varied by up to 20% across iterations so that the result is not tuned to one exact kill time.

That should surprise you. A boss fight in the game happens once. You can see your own damage meter at the end. Why would a tool need thousands of fake fights to tell you a number you can read off a meter?

Because the meter from one fight is mostly noise. Let's measure how much.

### The model

Take two classes that auto-attack a target dummy. Each attack is one hit. No procs, no cooldowns, so we can compute everything by hand and then check the simulator against it.

- `D` is the base damage of one hit.
- `p` is the crit chance, the probability that a hit is a critical hit.
- `m` is the crit multiplier. A crit deals `m × D`.
- `n` is the number of hits in the fight.
- `T` is the fight length in seconds.

The number of crits in a fight, call it `k`, follows a binomial distribution with `n` trials and success chance `p` (the MA102 week 6 model). The total damage is `D × (n + (m − 1) × k)`. Every hit deals at least `D`, and each crit adds `(m − 1) × D` on top.

Divide by `T` to get the fight's DPS. Using the mean and variance of the binomial, `n p` and `n p (1 − p)`:

```
mean DPS      μ = n × D × (1 + p × (m − 1)) / T
SD of DPS     σ = D × (m − 1) × sqrt(n × p × (1 − p)) / T
```

Now the Monte Carlo part. If you run `N` independent fights and average their DPS, the average is itself random. Its standard deviation is called the **standard error**:

```
standard error of the mean   SE = σ / sqrt(N)
95% interval for the mean    μ̂ ± 1.96 × SE
```

Here `μ̂` (read "mu hat") is the average your simulator reports. The 1.96 comes from the normal curve; about 95% of the time, the true mean lies within 1.96 standard errors of the estimate.

To compare two classes, A and B, you care about the difference of their means. If their runs are independent, the spreads add in squares:

```
σ_diff = sqrt(σ_A² + σ_B²)
SE_diff = σ_diff / sqrt(N)
N needed so the 95% interval of the difference is narrower than a gap g:
N = (1.96 × σ_diff / g)²
```

That last line is the one to remember. **The number of iterations you need grows with the square of how precise you want to be.** Halve the gap you want to detect and you need four times the fights.

### Numbers you can check

Two classes, a 60-second fight, one hit every 1.5 seconds, so `n = 40` hits. Crits deal double damage, `m = 2`.

- The **Duelist** hits for `D = 100` with `p = 25%` crit.
- The **Marksman** hits for `D = 110` with `p = 10%` crit.

Expected damage per hit is `100 × 1.25 = 125` for the Duelist and `110 × 1.10 = 121` for the Marksman.

| Class | Mean DPS μ | SD of one fight σ | Share of fights this class wins |
|---|---|---|---|
| Duelist (100, 25%) | 40 × 125 / 60 = 83.33 | 100 × sqrt(7.5) / 60 = 4.56 | 67.3% |
| Marksman (110, 10%) | 40 × 121 / 60 = 80.67 | 110 × sqrt(3.6) / 60 = 3.48 | 32.7% |

The Duelist is ahead by `2.67` DPS, which is 3.2% of its mean. In this course we treat a 3% gap between two classes in the same role as a real balance problem. Yet in **one fight in three**, the Marksman posts the higher number. The win shares in the last column come from an exact calculation over all 41 × 41 combinations of crit counts; ties are about 0.03%. If a designer or a player looks at one fight, a third of the time they will conclude the wrong class is stronger.

Now run many fights. With `σ_diff = sqrt(4.56² + 3.48²) = 5.74`:

| Fights per class N | SE of Duelist mean | 95% half-width, Duelist | SE of the difference | Chance the averages rank the classes wrong |
|---|---|---|---|---|
| 1 | 4.56 | ±8.95 | 5.74 | 32% |
| 10 | 1.44 | ±2.83 | 1.81 | 7.1% |
| 100 | 0.46 | ±0.89 | 0.57 | about 0.0002% |
| 1,000 | 0.14 | ±0.28 | 0.18 | effectively 0 |

The last column uses the normal approximation, `Φ(−gap / SE_diff)`, where `Φ` is the standard normal cumulative distribution. At `N = 1` it gives 32%, close to the exact 32.7%, which is a sign the approximation is fine here.

Using the sample-size formula:

| Gap you want to detect | As % of Duelist DPS | Fights per class needed |
|---|---|---|
| 2.67 DPS | 3.2% | 18 |
| 0.83 DPS | 1% | 183 |
| 0.083 DPS | 0.1% | 18,220 |

Ten times the precision costs a hundred times the fights. And if you want the Duelist's own average pinned to within 0.2% of its value, about SimulationCraft's default target, you need `(1.96 × 4.56 / 0.167)² ≈ 2,880` fights. The SimulationCraft documentation does not spell out which confidence level its error target uses, so treat this as the same order of magnitude, not the same setting.

### The visual

Open `examples/w13-monte-carlo-dps.html`. The left panel shows two histograms of single-fight DPS, one per class, drawn on the same axis. They overlap heavily. The right panel shows the running average of each class as the number of fights grows, with a shaded 95% band around each line. Press "Run 1 fight" a few times and watch the ranking flip. Then drag the fights slider up. The histograms on the left keep the same width no matter how many fights you run, because one fight is always that noisy. The bands on the right shrink as `1 / sqrt(N)` and separate somewhere around 15 to 20 fights. The spread of fights never goes down. Only your uncertainty about the average does.

Then set both classes to the same expected damage per hit, for example the Marksman to `D = 113.6`, and watch the bands refuse to separate however far you push the slider. That is what "these classes are balanced, as far as the sim can tell" looks like.

### Cross-game recognition

**World of Warcraft, SimulationCraft.** The tool reads a character's gear and talents, plays a boss fight following an **action priority list** (a list of actions in priority order; each time the character can act, the simulator scans from the top and performs the first action whose conditions are met), and repeats until its error target is met. Its default fight style, called Patchwerk, is a single target with no movement and no adds, which is the same setup as our dummy. Other built-in styles add movement or waves of adds, which is how players test whether a class that wins on a dummy still wins in a messy fight. Raidbots' Top Gear feature runs this once per gear combination, so it compares many estimates at once. Every comparison is our `N = (1.96 × σ_diff / g)²` problem: two gear sets that differ by 0.1% need tens of thousands of iterations to rank reliably, and a tool that reports them without error bars is inviting players to chase noise.

**Path of Exile, Path of Building.** Path of Building, the community build planner, takes the other route. It computes DPS as average hit times attack rate times a crit factor, which is our `μ` formula with more terms. It does not play out fights. That is fast and exact for the average, and it needs no iterations at all. It is also blind to spread and to state. It cannot tell you how often you fail to kill a pack before it reaches you. In our terms, Path of Building computes `μ` exactly and never estimates `σ`. For linear, stateless damage this is the right call, and you should use the same shortcut when your model allows it.

**Magic: The Gathering, Frank Karsten's mana-base tables.** Karsten, a professional player and writer, built widely used tables of how many lands of each color a deck needs to cast its spells on time. The basic probability comes from the hypergeometric distribution, a closed form. But mulligan decisions, where a player redraws a bad opening hand, depend on what the hand looks like. That is state and decision, so Karsten used simulation code to play out opening hands and mulligans, and later authors adapted that code for new mulligan rules. Same structure as SimulationCraft: a closed form for the simple part, simulation where a policy enters, and many repetitions because a single game tells you almost nothing.

In all three, the question is the same. Can I write `μ` down? If yes, compute it. If a policy or state gets in the way, simulate, and then report `μ̂ ± 1.96 σ / sqrt(N)`, never `μ̂` alone.

### Eyes-open design judgment

- **Use a closed form when you can.** Our dummy fight did not need a simulator at all. If your class is linear and stateless, a formula is faster, exact and easier to reason about. Simulation is for the parts a formula cannot reach.
- **Always validate against a case you can compute.** Before you trust your simulator on a class with procs, set that class to the stateless case and check that `μ̂` lands inside `μ ± 1.96 SE` of the hand calculation. If it does not, the bug is in your simulator, not in the game.
- **Report the error bar with every number.** A balance spreadsheet that says "Duelist 83.4, Marksman 80.6" hides whether that gap is real. A table that says "83.4 ± 0.3, 80.6 ± 0.2 (N = 1,000)" does not.
- **Decide the gap that matters before you run.** If your studio will not act on a gap smaller than 1%, you need about 200 fights per class in this setup, not a million. Spending compute on precision nobody uses slows every iteration of your design loop.
- **Remember what the sim leaves out.** A simulated player never misclicks, never moves the wrong way, never forgets a cooldown. Classes that are hard to play will look stronger in simulation than in live logs. That gap is itself a balance fact, and section 4 returns to it.

## 3. Anatomy of a combat simulator

Every combat simulator, from SimulationCraft to the one you will write in the lab, has the same five parts.

### State

The **state** is everything the rules need to decide what happens next. For each actor, that includes health, resources, cooldown timers, active buffs and debuffs with their expiry times, and position if movement matters. For the fight, it includes the clock, the list of enemies, and any scripted phase changes. A good rule for deciding what goes in state: if two situations could lead to different outcomes, the state must be able to tell them apart.

### Clock

There are two ways to move time forward.

A **fixed-step** simulator advances the clock by a small amount, say 0.1 seconds, and checks everything each step. It is easy to write. It is also wasteful, because nothing happens in most steps, and inaccurate, because an event scheduled at 1.25 seconds must happen at 1.2 or 1.3.

An **event-driven** simulator keeps a priority queue of future events sorted by time: "Duelist can act at 1.5 s", "bleed ticks at 2.0 s", "buff expires at 8.0 s". It pops the earliest event, jumps the clock straight to its time, applies it, and pushes any new events it causes. Time costs nothing between events, and every event happens at its exact time. Nearly every serious combat simulator is event-driven.

```
queue = [ (0.0, "actor ready", duelist), (0.0, "actor ready", marksman) ]
while queue not empty and clock < fight_length:
    time, kind, who = pop_earliest(queue)
    clock = time
    if kind == "actor ready":
        action = choose_action(who, state)        # the policy
        apply(action, who, state, rng)             # damage, resources, buffs
        push(queue, clock + action.cast_time, "actor ready", who)
        for effect in action.scheduled_effects:    # dots, buff expiry
            push(queue, clock + effect.delay, effect.kind, who)
    else:
        apply_event(kind, who, state, rng)
record(state)
```

### Policy

The **policy** decides which action an actor takes when it is free to act. The simplest useful policy is a priority list, the same structure SimulationCraft uses. Each entry has an action and a condition. The simulator walks the list from the top and takes the first entry whose condition holds.

The policy is part of the class's balance. Two designers can simulate the same class with different priority lists and get different answers, and both are "right" for their list. When you publish a sim result, publish the policy with it. When a class underperforms in simulation, check the policy before you check the numbers. A priority list that wastes a resource at cap can make a healthy class look 5% weak.

### Random numbers

A Monte Carlo simulator draws random numbers for crits, procs and damage ranges. Two practices matter.

**Seed your generator.** A **seed** is the starting value of a pseudo-random number generator. The same seed gives the same sequence of numbers, so the same simulation gives the same result. That makes bugs reproducible and lets a reviewer rerun your exact experiment. Record the seed in every report.

**Use common random numbers when comparing.** If you compare Duelist version 1 with Duelist version 2 (a buff), running each with its own random stream adds both spreads into `σ_diff`. If you instead give both versions the same stream, so fight 17 has the same crit rolls in both, the noise that is shared cancels in the difference. For a small change, this can cut the number of fights needed by a large factor, because most of the noise is shared. The technique is called **common random numbers**, and it is the cheapest speed-up in simulation-based balance. It works best when the two versions consume random numbers in the same order, so design your code so each actor has its own generator.

### Output

At minimum, record per iteration the metric you care about: DPS, healing per second, time-to-kill, damage taken, whether the healer ran out of mana. Then report the mean, the standard deviation, the standard error and, when the tails matter, percentiles. A healer who goes out of mana in 5% of fights has a problem the mean will never show.

## 4. Validating a simulator

A simulator that gives confident wrong answers is worse than no simulator, because people act on it. Validation has three layers.

**Unit checks against closed forms.** Build cases you can compute by hand, as in section 2. A single hit with no crit. A crit chance of 100%. A damage-over-time effect with a known number of ticks. An armor value where you know `A / (A + K)` from week 2. Each check is a test you run every time the code changes.

**Statistical checks.** For random cases, you cannot check an exact number, only whether the simulator's average falls inside the expected band. Run the Duelist for 10,000 fights. The mean should land in `83.33 ± 1.96 × 4.56 / 100 = 83.33 ± 0.09`. The standard deviation across fights should be close to 4.56. If the mean is right and the spread is wrong, look for a bug in how random numbers are shared or reused.

**Comparison with live data.** Finally, compare simulated results with logs from real play. In World of Warcraft, players upload combat logs to third-party sites such as Warcraft Logs, which rank performance per class and per boss. You can set your sim's median against the logged median for the same class and fight. Expect a gap. Real players move, die, lose uptime and make mistakes. The size of that gap, per class, is itself useful. A class that simulates 3% above another but logs 3% below it in the median is probably harder to play. You may decide that is fine, since harder classes can earn a higher ceiling, but decide it deliberately.

Where live data and simulation disagree in a way skill cannot explain, suspect the rules implementation. Simulators encode what their authors believe the game does, and patch notes do not always describe every change.

## 5. Using a simulator for class balance

A simulator is a measuring instrument. Balance work needs an experiment design around it.

### The balance matrix

For a DPS role, build a table with classes as rows and **fight styles** as columns. A useful minimum set of columns:

- Single target, stationary (the Patchwerk case).
- Single target with forced movement every 20 seconds.
- Two targets (cleave).
- Five or more targets (area damage).
- Short fight (60 seconds, where cooldowns dominate) and long fight (300 seconds, where sustained rotation dominates).

Each cell holds `μ̂ ± 1.96 SE` for that class in that style. Now you can see not only who is strongest but where each class is strongest. Week 1's idea of **viability** becomes concrete. A class is viable if it is within your tolerance band in at least one style the content actually asks for. Week 9's **counters** become concrete too. You want each class to have a column it wins and a column it loses.

### Tolerance bands

Decide in advance how close is close enough. Suppose your team's target is that every DPS class sits within 3% of the role average on the main fight style. Whatever number you pick sets the precision you need. If your band is ±3%, you need error bars well under 1%, which from section 2 means a few hundred fights per cell. That is affordable. A band of ±0.5% is not, and it would not survive contact with real player skill anyway.

### Sensitivity analysis

Once the matrix is filled, change one input at a time: +5% crit, +10% haste, +10% fight length. See how much each class moves. This is how you compute **stat weights**, the damage gained per point of each stat, which you met in week 12. It also tells you which classes are fragile. A class whose DPS jumps 8% when the fight is 20% longer will swing from weak to dominant depending on how well a raid group plays, and that makes it hard to balance.

### A caution on precision

Simulation feels rigorous because it produces many decimal places. Remember the three kinds of error in any sim result:

1. **Sampling error**, which you control with `N`.
2. **Model error**, where the sim's rules differ from the game's. Validation catches some of it.
3. **Policy error**, where the sim plays the class differently from players. Comparison with logs catches some of it.

More iterations only shrink the first. A result of `83.41 ± 0.01` from a sim with a wrong priority list is precise and wrong.

## In-class activity (25 minutes)

In groups of three, you will play simulator by hand and then compare with the formula.

**Materials:** two ten-sided dice (or a phone dice app) per group, the table from section 2, the interactive.

1. **(8 min)** Each group member simulates one 10-hit fight for the Duelist and one for the Marksman. For each hit, roll the two d10s as a percentile roll from 00 to 99. A crit is 00-24 for the Duelist and 00-09 for the Marksman. Record total damage and DPS for a 15-second fight (10 hits at 1.5 s).
2. **(4 min)** Pool the group's three fights per class. Which class won each fight? Which class has the higher group average?
3. **(5 min)** Compute the hand formula for a 10-hit, 15-second fight. Expected DPS is `10 × 125 / 15 = 83.3` for the Duelist and `10 × 121 / 15 = 80.7` for the Marksman. The SD is `100 × sqrt(10 × 0.25 × 0.75) / 15 = 9.1` and `110 × sqrt(10 × 0.1 × 0.9) / 15 = 7.0`. Are your group's results inside two SDs of the means?
4. **(8 min)** Pool the whole class's results on the board. With perhaps 30 fights per class, compute each class's average and its 95% half-width. Does the class-wide data rank the classes correctly? Check your answer against the interactive set to 10 hits and 15 seconds.

**Expected output:** a board table showing that most individual groups could not rank the classes reliably and that the pooled class data could, with the half-width computed.

## Common misconceptions

- **"More iterations make the fights less random."** They do not. The spread of single-fight DPS is fixed by the class design (4.56 for the Duelist). More iterations shrink only the error of the average, as `σ / sqrt(N)`.
- **"The simulator says 83.41, so the class does 83.41."** The simulator says 83.41 plus or minus its standard error, for its policy, on its fight style. Drop any of those three and the number means less than it seems.
- **"If the sim ran a million iterations, the result is accurate."** It is precise. Accuracy also needs correct rules and a realistic policy, and iterations fix neither.
- **"Simulation is always better than a formula."** For linear, stateless damage, a formula is exact, instant and easier to explain. Path of Building's approach is correct for what it computes. Simulate only where a formula cannot reach.

## Check yourself

1. A Brawler hits 40 times in a 60-second fight for `D = 90` with a 40% crit chance and a 2× crit multiplier. Compute its expected DPS and the SD of single-fight DPS. Is it stronger or weaker than the Duelist on average, and by how many DPS?
2. Two healer builds differ by an expected 0.5% of their mean healing per second, which is 80. The SD of the difference for a single fight is 6. How many fights per build do you need so that the 95% interval of the difference is narrower than the gap?
3. A designer simulates 20 fights for each of the Duelist and the Marksman and finds the Marksman ahead by 1.0 DPS. Using `σ_diff = 5.74`, how many standard errors is that? Should the designer nerf the Marksman?
4. Your simulator runs the Duelist for 10,000 fights and reports a mean DPS of 83.61 with an SD of 4.55. Is that consistent with the hand formula? What would you look for first?

<details>
<summary>Answers</summary>

1. Expected damage per hit is `90 × 1.4 = 126`, so `μ = 40 × 126 / 60 = 84.0`. SD is `90 × sqrt(40 × 0.4 × 0.6) / 60 = 90 × 3.10 / 60 = 4.65`. The Brawler is 0.67 DPS stronger than the Duelist on average, a gap you would need about `(1.96 × sqrt(4.65² + 4.56²) / 0.67)² ≈ 367` fights per class to confirm.
2. The gap is `0.005 × 80 = 0.4`. `N = (1.96 × 6 / 0.4)² = 29.4² ≈ 865` fights per build. With common random numbers the SD of the difference would drop and so would N.
3. `SE_diff = 5.74 / sqrt(20) = 1.28`, so a 1.0 DPS lead is 0.78 standard errors from zero. That is not evidence the Marksman is stronger, so no nerf. There is a second point. We know the true gap is 2.67 in the Duelist's favor, and a Marksman lead of 1.0 or more is `(1.0 + 2.67) / 1.28 = 2.9` standard errors away from it, which happens only about 0.2% of the time. Either the designer drew a rare sample or the simulator has a bug. Run more fights and validate the sim before touching either class.
4. The expected band is `83.33 ± 1.96 × 4.56 / 100 = 83.33 ± 0.09`. The reported 83.61 is 6 standard errors high, far outside the band, while the SD matches. Suspect a bug that adds damage without changing the spread, such as an extra hit per fight (41 hits instead of 40 gives `41 × 125 / 60 = 85.4`, too high) or a rounding rule. Check the hit count and the fight-end condition first.

</details>

## Lab hook

**Lab 13: Build a combat simulator.** You will write an event-driven simulator for two classes, validate it against the hand formulas from this lecture, then add one stateful mechanic (a proc with an internal cooldown) and produce a balance matrix with error bars. This lab is the first milestone of the simulator assessment. See [labs/lab13.md](../labs/lab13.md). Week 14 uses your results to write patch notes.

## Sources

- SimulationCraft wiki, "StatisticalBehaviour" (GitHub, current as of 2025-2026). Default settings of 0.2% target error and a maximum of 1,000,000 iterations; the page does not state the confidence level of the error target. https://github.com/simulationcraft/simc/wiki/StatisticalBehaviour
- SimulationCraft wiki, "Options". Default `max_time` of 300 seconds and `vary_combat_length` of 0.2. https://github.com/simulationcraft/simc/wiki/Options
- SimulationCraft wiki, "ActionLists". Actions lists are scanned from the top, first available action is performed; described as priority lists. https://github.com/simulationcraft/simc/wiki/ActionLists
- SimulationCraft fight styles (Patchwerk as no movement and no adds; HecticAddCleave; DungeonSlice), as described in the SimulationCraft wiki and in Maxroll, "SimulationCraft and Raidbots Guide" (patch 11.0.2, The War Within). https://maxroll.gg/wow/resources/simulationcraft-and-raidbots-guide
- Warcraft Logs (https://www.warcraftlogs.com/), combat-log ranking site for World of Warcraft, current.
- Raidbots, Top Gear and Droptimizer pages and support article "Droptimizer: How Does It Work?" (The War Within era). Raidbots runs SimulationCraft in the cloud. https://www.raidbots.com/ and https://support.raidbots.com/article/59-droptimizer-how-does-it-work
- Path of Building Community, "PathOfBuilding" repository (offline build planner for Path of Exile, current releases). Computes average DPS from average hit, rate and crit factor. https://github.com/PathOfBuildingCommunity/PathOfBuilding
- Karsten, F., "How Many Colored Mana Sources Do You Need to Consistently Cast Your Spells? A Guilds of Ravnica Update," ChannelFireball (2018), as referenced by dchiu30, "Karsten-Mana-Calculator" (GitHub). The statement that Karsten's tables come from simulation code that handles mulligans is from teryror, "An updated and expanded guide on building mana bases in Magic: the Gathering" (GitHub gist), which adapts Karsten's simulation code for the London mulligan. https://gist.github.com/teryror/881d60e08480a56043895d3bbb83c374
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press.
- The Duelist and Marksman classes, their numbers, and all derived tables are invented for this lecture. The exact single-fight win shares were computed by enumerating all binomial outcomes.

## Interactive spec: examples/w13-monte-carlo-dps.html

**Insight the visual must make obvious:** the spread of single-fight DPS never shrinks, but the uncertainty of the average shrinks as `1 / sqrt(N)`, so a gap invisible in one fight becomes certain after a few dozen.

**Layout:** two linked panels side by side on desktop, stacked on mobile (histograms first).

- **Left panel, "One fight at a time":** overlaid histograms of single-fight DPS for class A (Duelist, damage red token) and class B (Marksman, steel token), using all fights run so far. Bin width 1 DPS. Draw a thin vertical line at each class's theoretical mean `μ`, and a faint normal curve with mean `μ` and SD `σ` scaled to the histogram. Label: "Fights where B beat A: X of N (Y%)".
- **Right panel, "The average over N fights":** x-axis is N on a log scale from 1 to 5,000. For each class, plot the running mean `μ̂(N)` as a line, and a shaded band `μ̂(N) ± 1.96 × s(N) / sqrt(N)`, where `s(N)` is the sample SD so far (use theoretical σ for N < 5). Mark with a dot and text the first N at which the two bands stop overlapping and stay separate for the rest of the run: "Bands separate at N = ...".

**Controls (all keyboard accessible):**
- For each class: base damage `D` (slider 50-200, step 0.1), crit chance `p` (0-100%, step 1), crit multiplier `m` (1.0-3.0, step 0.1).
- Shared: hits per fight `n` (5-100, default 40), fight length `T` in seconds (5-300, default 60).
- Buttons: "Run 1 fight", "Run 10", "Run 100", "Run to 5,000", "Reset". "Run to 5,000" animates in batches unless `prefers-reduced-motion` is set, in which case it jumps to the end.
- Seed field (integer, default 13) and a "Common random numbers" toggle (default off). When on, both classes use the same uniform draw for hit i of fight j; show the SE of the difference both ways in the readout so the reduction is visible.
- Preset buttons: "Lecture default" (A: 100, 25%, 2.0; B: 110, 10%, 2.0; n 40; T 60), "Equal means" (lecture default with B `D = 125 / 1.1 = 113.64`, so both classes expect 125 per hit), "In-class dice" (lecture default with n 10, T 15).

**Readout (exact numbers next to the visual):** for each class, theoretical `μ` and `σ`, simulated `μ̂`, sample SD, SE, and 95% half-width; the theoretical gap `μ_A − μ_B`; `σ_diff`; the formula `N = (1.96 σ_diff / gap)²` evaluated; the normal-approximation probability of wrong ranking at current N, `Φ(−gap / (σ_diff / sqrt(N)))`.

**Formulas:**
- One fight: for i in 1..n, draw `u ~ U(0,1)`; crit if `u < p`; hit damage `D × (crit ? m : 1)`. Fight DPS = sum / T.
- `μ = n D (1 + p(m − 1)) / T`; `σ = D (m − 1) sqrt(n p (1 − p)) / T`.
- Use a seeded PRNG (mulberry32 or similar), so the same seed reproduces the same run.

**Test values (lecture default):**
- Duelist `μ = 83.333`, `σ = 4.564`; Marksman `μ = 80.667`, `σ = 3.479`; gap 2.667; `σ_diff = 5.739`.
- Required N for the gap: 17.8 (display 18). For a 1% gap (0.833): 183.
- Wrong-ranking probability: N = 1 → 32.1%; N = 10 → 7.1%; N = 100 → below 0.001%.
- Exact single-fight P(B > A) = 32.66% (normal approx 32.1%); with 5,000 simulated fights the displayed share should land within about ±1.3 points of 32.7%.
- "In-class dice" preset: Duelist `μ = 83.33`, `σ = 9.13`; Marksman `μ = 80.67`, `σ = 6.96`.
- "Equal means" preset: both `μ = 83.33`; bands should never separate for long.
