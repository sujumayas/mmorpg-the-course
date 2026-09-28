# MMO401 · Week 03 — Agent-based modeling II

**Why this matters:** Last week's model was a toy with a known answer. This week you turn an agent-based model into evidence a producer will act on: tied to real numbers, tested, run many times, and reported with its uncertainty. Along the way you find that two policies with identical faucet and sink totals can build completely different worlds.

**You will be able to:**
- Distinguish verification, validation and calibration, and write one test for each.
- Predict, from the shape of a faucet or sink (flat or proportional), whether it compresses or spreads the wealth distribution, and check the prediction by hand on four players.
- Run a policy experiment with replications and common random numbers, and report the result as a mean with a 95% confidence interval.
- Design a sensitivity sweep and explain which result would change your recommendation.

**Before class:** Reread [MA102 week 13, sampling and confidence](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md), sections 1-2. Dragulescu & Yakovenko (2001), "Evidence for the exponential distribution of income in the USA" (arXiv cond-mat/0008305), the introduction and the Lorenz-curve figure. Course text, Lehdonvirta & Castronova (2014), continue the assigned chapters 9-12.

**Prerequisites from earlier courses:** [Week 2 of this course, agent-based modeling I](w02-agent-based-modeling-i.md) (the random-exchange model, Gini, burn-in). [Week 1](w01-the-in-house-economist-role.md) (faucets and sinks as a share of the money supply). [GD203 week 12, simulation-driven balance](../../GD203-combat-and-progression-design/lectures/w12-simulation-driven-balance.md) (seeds, common random numbers, sweeps). [MA102 week 13](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md) (standard error, 95% intervals). [MMO304 week 3](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w03-faucets-sinks-and-transformations.md) (faucets and sinks) and [MMO304 week 12](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w12-economic-telemetry-and-dashboards.md) (telemetry).

**Interactive:** [Policy shape: same money line, different economies](../examples/w03-policy-shape.html). Keep it open during section 2.

---

## 1. From toy to instrument

A model that runs is not yet a model you can trust. Three separate checks turn one into the other. People mix them up, so learn the words.

- **Verification** asks: *does the code do what the specification says?* It is about bugs. Example test: total gold after a run equals starting gold plus all faucet payments minus all sink payments, to the coin.
- **Validation** asks: *does the model behave like the thing it represents?* It is about the rules. Example test: with no faucets or sinks, the model's settled Gini is close to 0.5, as the random-exchange theory predicts. With real telemetry, does the model reproduce patterns the live game shows?
- **Calibration** asks: *are the parameters set from real data?* It is about numbers. Example: set the faucet rate to the live game's faucets divided by its money supply.

A verified, uncalibrated model is a correct program about an imaginary game. A calibrated, unverified model is a buggy program with real-looking numbers, which is worse, because people believe it.

### Calibrating from a ledger

Week 1 read EVE Online's October 2024 data. Faucets paid about 170.8 trillion ISK that month, about 7.7% of the money supply. Sinks removed about 95.9 trillion, about 4.3%. If you were building an EVE-like model with a tick of one month, those two percentages would be your first calibration targets. Your model's faucets and sinks, summed across agents, should hit them.

Notice what the ledger cannot give you: how the 7.7% is split between players. For that you need either per-player telemetry (which the studio has and does not publish) or an assumption. This lecture is about why that assumption matters more than the totals.

## 2. Worked example: same money supply, different world

### The hook

Look again at where EVE's October 2024 ISK came from and went. The biggest single player-activity faucet was NPC bounty prizes, 26.8% of all faucets. A bounty is paid per pirate killed, so it pays more to whoever kills faster, and pilots in better-equipped ships kill faster. The biggest sink was the transaction tax, 21.3% of all sinks, charged as a percentage of each sale. Another 10.6% of sinks came from skill purchases, which are sold at set prices that are the same for every buyer.

So some faucets pay in proportion to what you already have, and some sinks take a flat amount regardless of what you have. Suppose a designer balances the books: injection equals removal every tick, the money supply is flat, the dashboard is green. Does it matter which faucet and which sink did the balancing?

It matters enormously. In the model below, one balanced policy cuts the Gini from about 0.51 to 0.20. Another balanced policy leaves it untouched. A third policy, also balanced on day one, lets the money supply run away and ends with two thirds of players holding almost nothing. The money-supply chart for the first two is the same flat line.

### The model

Start from week 2's random exchange: `N = 1,000` players, 100 gold each, trades of 5 gold. Define a **tick** as 1,000 trades, one per player on average. At the end of each tick, apply one policy. Every policy is sized so that, at the starting money supply `M = 100,000`, it injects 2,000 gold and removes 2,000 gold per tick, which is 2% of the stock each way.

```
f = 2 gold    flat amount per player per tick
r = 0.02      proportional rate per tick
x             one player's gold before the policy step

Policy A, flat faucet + proportional sink:    x → x − r·x + f
Policy B, proportional faucet + proportional sink:
                                              x → x − r·x + (f·N) · x / M
Policy C, proportional faucet + flat sink:    x → max(0, x + r·x − f)
```

- In **A**, every player gets the same login-style payment and pays the same percentage tax on holdings.
- In **B**, a fixed faucet budget of 2,000 gold is paid out in proportion to holdings (richer players earn more, like bounties from better ships), and the sink is the same percentage tax as A.
- In **C**, income is proportional to holdings and the sink is a flat fee. A player who cannot pay the fee pays everything they have.

### Numbers you can check

Before simulating, do one tick by hand. Use four players with 100, 200, 300 and 400 gold (`M = 1,000`, Gini 0.25 from week 2), a flat amount `f = 25` and a rate `r = 10%`. Each policy injects and removes 100 gold, 10% of the stock, on the first tick.

| Player | Start | A: `0.9x + 25` | B: `0.9x + 100·x/1000` | C: `1.1x − 25` |
|---|---|---|---|---|
| 1 | 100 | 115 | 100 | 85 |
| 2 | 200 | 205 | 200 | 195 |
| 3 | 300 | 295 | 300 | 305 |
| 4 | 400 | 385 | 400 | 415 |
| Total | 1,000 | 1,000 | 1,000 | 1,000 |
| Gini | 0.250 | 0.225 | 0.250 | 0.275 |

All three totals are 1,000. An aggregate model sees three identical economies. The Gini moved down, stayed put and moved up.

You can see why with a little algebra. Every policy has a balance point at `x* = f / r = 250`, the average. Measure each player's gap from it, `x − 250`:

```
A:  new gap = (1 − r) × old gap     → gaps shrink by 10% per tick. Everyone drifts to 250.
B:  new gap = old gap               → nothing changes. Faucet and sink cancel for each player.
C:  new gap = (1 + r) × old gap     → gaps grow by 10% per tick. Players move away from 250.
```

Policy C's balance point is unstable, like a ball on a hilltop. Keep ticking C on the four players:

| Tick | Player 1 | Player 4 | Total | Gini |
|---|---|---|---|---|
| 0 | 100 | 400 | 1,000.00 | 0.250 |
| 1 | 85.00 | 415.00 | 1,000.00 | 0.275 |
| 3 | 50.35 | 449.65 | 1,000.00 | 0.333 |
| 5 | 8.42 | 491.58 | 1,000.00 | 0.403 |
| 6 | 0 | 515.73 | 1,015.73 | 0.424 |
| 8 | 0 | 571.54 | 1,071.54 | 0.450 |

Tick 6 is where the aggregate breaks too. Player 1 owes 25 but holds only 9.27 after income, so the flat sink under-collects. From then on less money leaves than enters, and the proportional faucet on the rich players compounds. The money supply, flat for five ticks, starts to climb. A dashboard that only tracks the total would have shown five green ticks and then a surprise.

### The simulation

Now the full model with trading, run for 1,000 ticks (one million trades). Values from seed 1, Python 3 `random`, using the lab 03 code. "Under 5" means the player cannot afford a single trade.

| Policy | Money supply at tick 1,000 | Gini | Top 10% share | Median | Under 5 gold |
|---|---|---|---|---|---|
| No policy (week 2) | 100,000 | 0.512 | 32.5% | 70.0 | 5.8% |
| A, flat faucet + proportional sink | 100,000 | 0.195 | 16.3% | 99.3 | 0.0% |
| B, proportional faucet + proportional sink | 100,000 | 0.512 | 32.5% | 70.0 | 5.8% |

B produces exactly the no-policy numbers, run for run, because with the same seed its faucet and sink cancel inside every wallet. It moves 2,000 gold a tick in and 2,000 out and changes nothing. Policy A turns the exponential into a hump around the average.

Policy C does not settle:

| Tick | Money supply | Gini | Median | Under 5 gold |
|---|---|---|---|---|
| 10 | 100,000 | 0.142 | 100.3 | 0.0% |
| 50 | 100,823 | 0.411 | 95.5 | 8.4% |
| 100 | 112,088 | 0.653 | 31.1 | 29.4% |
| 200 | 298,250 | 0.839 | 2.4 | 61.7% |
| 500 | about 88.6 million | 0.871 | 1.2 | 69.0% |

For the first 50 ticks the money supply is within 1% of target. By tick 200 it has tripled and the median player holds 2.4 gold.

One run is one story. Section 3 turns this into evidence. For now, the replicated values are: across seeds 1-20, policy A's Gini at tick 1,000 is 0.195 ± 0.002 and policy B's is 0.498 ± 0.004 (means with 95% confidence intervals). The intervals are nowhere near each other.

### Move it yourself

Open the interactive. The top view plots the money supply against ticks for the policies you switch on, one line each. The bottom view shows each policy's **Lorenz curve**: players sorted from poorest to richest along the x-axis, cumulative share of gold on the y-axis. A diagonal line means perfect equality, and the more the curve sags below it, the higher the Gini. Switch on A and B. In the top view their lines lie exactly on top of each other. In the bottom view A hugs the diagonal and B sags. Now add C and turn on the log scale: C's money line bends upward around tick 50, and its Lorenz curve collapses into the corner. The top chart is what a studio dashboard shows. The bottom chart is what players live in.

### Cross-game recognition

Classify each real faucet or sink by its shape. The shape predicts the direction of the distribution effect, whatever the game.

**EVE Online (October 2024 data).** Bounty prizes and other activity rewards pay more to players with better tools, so they behave like proportional faucets, the spreading kind. The transaction tax and broker fees take a percentage of trade value, so they are proportional sinks. Skill purchases at set prices are flat sinks, which weigh far more heavily on a new pilot than on a billionaire. EVE combines the spreading shapes (proportional faucet, flat sink) with a large proportional sink. Your model can tell you which effect wins for a given mix, and the ledger totals cannot.

**World of Warcraft (auction house, all versions).** The auction house takes 5% of the winning bid, a proportional sink on trade. Listing deposits are a percentage of the item's vendor price and are refunded if the item sells. So they fall hardest on players whose listings fail, a different shape again.

**Old School RuneScape (Grand Exchange, from December 2021).** Jagex added a tax on Grand Exchange sales on 9 December 2021 at 1%, and raised it to 2% on 29 May 2025. It is capped at 5 million coins per item, and items selling for under 50 coins pay nothing because the tax rounds down. The cap means the tax stops being proportional for items worth more than 250 million coins. Above that price it is a flat 5 million, a smaller share the more expensive the item. The floor exempts the cheapest trades. One rule contains three shapes, and a designer should know which trades fall in each. Week 7 builds the full transaction-tax model.

In all three games the same question sorts every rule: *does this faucet or sink scale with what the player already has?* Flat faucets and proportional sinks pull players toward the average. Proportional faucets and flat sinks push them apart.

### Eyes-open design judgment

- **Balance the shape, not only the total.** A faucet and sink plan that balances at the aggregate level can still widen the gap every tick. Put a distribution observer (Gini, median, share under an affordability line) on the same dashboard as the money supply.
- **Compression is not automatically good.** Policy A makes wealth nearly equal, which also means effort barely changes where you end up. A flat faucet large relative to what players earn from play is a welfare system, and it may kill the reason to farm. Many games want some spreading, just not a runaway.
- **Flat sinks need a floor, and the floor leaks.** When poor players cannot pay, the sink under-collects and the money supply drifts up, as in policy C. If a sink is flat, cap it relative to wealth or give it an exemption, and model the leak.
- **Proportional faucets compound.** Any income that scales with holdings grows like interest. Unless something scales against it (a proportional sink at least as large, or diminishing returns on the activity), the richest players grow fastest. Design the diminishing returns deliberately.
- **Neutral policies still cost something.** Policy B changes no one's relative position. It still makes players spend time earning and paying. That churn can be the point (it gives activity meaning) or a waste. Decide which.

## 3. Many runs: replications and common random numbers

One run of an agent-based model is a sample of size one. Different seeds give different results. To say "A gives a lower Gini than B" you need to know how much results vary between seeds.

A **replication** is one run with its own seed. Run `n` replications of each policy and treat the final Gini of each run as one observation. [MA102 week 13](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md) gives you the tool:

```
mean Gini            ḡ = average of the n final Ginis
standard error       SE = s / sqrt(n),   s = sample standard deviation of the n Ginis
95% interval         ḡ ± 1.96 × SE
```

For policy A with 20 replications, `s = 0.0046`, so `SE = 0.0046 / sqrt(20) = 0.0010` and the interval is `0.195 ± 0.002`. For B, `s = 0.0093`, `SE = 0.0021`, interval `0.498 ± 0.004`. The difference between them, 0.303, is more than 100 times the standard error of that difference (`sqrt(0.0010² + 0.0021²) ≈ 0.0023`). You would not need 20 runs to tell these apart. You would need them for a subtler question, like "does raising r from 2% to 2.5% lower the Gini?"

**Common random numbers** is the trick from [GD203 week 12](../../GD203-combat-and-progression-design/lectures/w12-simulation-driven-balance.md): give policy A and policy B the same seed list (1 to 20). Then run k of each policy sees the same sequence of trades, and the difference between them comes from the policy, not from luck. The lab 03 code does this. That is also why policy B's seed-1 run matched the no-policy run exactly: same seed, same trades, and a policy that changes nothing.

How many replications? Start with 10. If the confidence intervals of the policies you are comparing overlap, double it. Keep doubling until they separate or until the difference is too small to matter for a design decision. Deciding what "too small to matter" means is your job, not the statistics' job. A Gini difference of 0.005 will not change a single player's experience.

## 4. Sensitivity analysis: which assumption decides the answer?

Every parameter in your model is a guess to some degree. **Sensitivity analysis** asks how much the result moves when a guess moves. If a recommendation flips when a poorly known parameter changes a little, you must say so in the memo.

The simplest method is a **one-at-a-time sweep**: hold everything at its default and vary one parameter across a plausible range. Here is policy A's settled Gini as the rate `r` varies, with `f = r × 100` so the money supply stays at 100,000 (5 seeds each, tick 1,000):

| Rate r per tick | Flat payment f | Gini (mean of 5 seeds) |
|---|---|---|
| 0.5% | 0.5 | 0.331 |
| 1% | 1 | 0.263 |
| 2% | 2 | 0.195 |
| 5% | 5 | 0.122 |
| 10% | 10 | 0.083 |

Two things to read off this table. First, the direction is stable: every rate compresses the distribution relative to 0.51. So the qualitative recommendation "a flat faucet with a proportional sink compresses wealth" is safe. Second, the size is very sensitive at low rates. Going from 0.5% to 1% moves the Gini by about 0.07. If your calibration of `r` from the ledger is uncertain by a factor of two, your predicted Gini is uncertain by that much.

The flow share also depends on what a tick means. If one tick equals one day in your game and the live sink removes 4% of the money supply a month, then `r` is about 0.13% per tick, below the smallest row of the table. Calibrating the tick length is as important as calibrating the rate.

A more thorough method, a **grid sweep**, varies two parameters together, for example `r` and the trade size `d`, and draws the result as a heat map. Use grids when you suspect parameters interact. Use one-at-a-time sweeps first, because they are cheap and they tell you which parameters are worth a grid.

The most important sensitivity test is not numeric, though. It is **structural**: change a rule's shape and see if the answer survives. Section 2 was a structural test. Moving from A to B changed one rule's shape and the Gini went from 0.20 to 0.51, a bigger effect than any rate in the table. If you are unsure whether a live faucet is flat or proportional, finding out is worth more than refining its rate.

## 5. Reporting a model so someone else can check it

A model report in this course has four parts, a cut-down version of the ODD protocol from week 2.

1. **Overview.** Purpose in one sentence ("compare the wealth-distribution effects of three balanced faucet and sink designs"). Agents and their state. Schedule, including what a tick means.
2. **Rules.** Every rule, as an equation or pseudocode, with each parameter's value and where it came from: calibrated (with source), assumed (with reason) or swept (with range).
3. **Tests.** The verification tests you ran (conservation, the four-player hand case as a unit test) and the validation checks (the no-policy Gini near 0.5).
4. **Results.** Each result as a mean with a 95% interval, the number of replications, the seed list, burn-in length, and one sentence per sensitivity finding that would change the recommendation.

The four-player table in section 2 is worth reusing as a unit test. Any correct implementation of policy A must turn (100, 200, 300, 400) into (115, 205, 295, 385) in one tick when the trade step is switched off. A test like that takes two minutes to write and catches the most common bug: applying the sink after the faucet instead of before, which in policy A gives a steady money supply of 98,000 instead of 100,000.

## In-class activity (25 minutes)

Groups of three, one laptop per group with the lab 03 starter code (or the interactive).

1. **Classify (5 min).** Your instructor gives you six real or invented rules (for example "repair costs 10% of item value," "daily login gives 50 gold," "housing upkeep 1,000 gold per week," "quest reward scales with character level"). Label each as flat or proportional, faucet or sink, and predict whether it compresses or spreads.
2. **Test (12 min).** Pick the two rules your group disagrees about most. Encode each as a policy in the model, balanced so the money supply is flat at the start. Run 10 replications each with seeds 1 to 10. Report Gini as mean ± 95% interval.
3. **Sensitivity (8 min).** Double the rate of one rule. Does the direction of your result change? Does its size?

Expected output: the six labels with predictions, a two-row results table with intervals, and one sentence on whether your prediction held.

## Common misconceptions

- **"If faucets equal sinks, the economy is stable."** Totals can match while the distribution drifts, and a flat sink can start leaking once poorer players cannot pay (policy C). Watch distribution and collection rate, not only the total.
- **"Validation means the model is true."** Validation means the model reproduces the patterns you checked. It can still be wrong about patterns you did not check. Say which ones you checked.
- **"More replications fix a biased model."** Replications shrink random noise. They do nothing about a wrong rule. Twenty runs of policy C with the wrong sink order give a precise wrong answer.
- **"A sensitivity sweep is optional polish."** If the recommendation flips inside the plausible range of a parameter, the sweep is the finding.

## Check yourself

1. Four players hold 50, 150, 250 and 350 gold. Apply policy A once with `f = 20` and `r = 10%` (sink first, then faucet). Give the new balances, the total, and each player's gap from `f/r`.
2. Under policy C with `r = 5%` and `f = 10`, what is the balance point? A player 40 gold below it: how far below will they be after 3 ticks (ignoring the floor)?
3. Twelve replications of a policy give a mean Gini of 0.310 with sample standard deviation 0.021. Give the 95% interval. A second policy gives 0.322 ± 0.011 from twelve replications. Can you say the policies differ?
4. A live game's daily login reward pays 100 gold to every active character and the only large sink is a 3% auction-house cut. Using the shapes from section 2, predict the effect on the wealth distribution. Name one piece of telemetry that would test your prediction.
5. Why does policy B change nothing in any wallet, even though it moves 2,000 gold in and out each tick?

<details>
<summary>Answers</summary>

1. `0.9x + 20`: 65, 155, 245, 335. Total 800, the same as before, because the money supply 800 is exactly `N × f / r = 4 × 20 / 0.1`. Balance point `f/r = 200`. Gaps were −150, −50, +50, +150 and are now −135, −45, +45, +135, each shrunk by 10%.
2. Balance point `f/r = 10 / 0.05 = 200`. Gaps grow by 1.05 per tick: `40 × 1.05³ ≈ 46.3` below, so about 153.7 gold.
3. `SE = 0.021 / sqrt(12) ≈ 0.0061`, interval `0.310 ± 0.012`, so 0.298 to 0.322. The second runs 0.311 to 0.333. The intervals overlap heavily. You cannot say they differ. Run more replications with common random numbers, and ask whether a 0.012 difference would matter to players.
4. A flat faucet plus a proportional sink on trade compresses, like policy A. The auction-house cut is proportional to what a player sells, which is close to, but not the same as, proportional to what they hold. Test it with the Gini or median wallet of active characters over time, split by account age, and check whether new characters' wallets converge toward the median.
5. Each player receives `(f·N)·x/M` and pays `r·x`. With `f·N = 2,000`, `M = 100,000` and `r = 0.02`, both equal `0.02·x`. They cancel inside every wallet, so only the random trades move anyone.

</details>

## Lab / assignment hook

[Lab 03, a policy experiment](../labs/lab03.md). Using the lab 03 starter code, you calibrate a faucet and sink pair from a provided ledger, compare three balanced policies with 20 replications each, run a one-at-a-time sensitivity sweep, and write a four-part model report. It is the second ABM lab and the basis for the final model and memo in week 15.

## Sources

- CCP Games, raw data for the EVE Online Monthly Economic Report, October 2024 (`sinks_and_faucets_history.csv`, `money_supply.csv`). Faucet and sink shares (bounty prizes 26.8% of faucets, transaction tax 21.3%, skill purchases 10.6% of sinks) and the 7.7% and 4.3% of money supply were computed by the author from these files.
- Warcraft Wiki, "Auction House." 5% cut of the winning bid; deposits as a percentage of vendor sell price, refunded on sale.
- Old School RuneScape Wiki, "Grand Exchange." Tax introduced 9 December 2021 at 1%, raised to 2% on 29 May 2025, capped at 5 million coins per item, rounds down so items under 50 coins pay nothing, with listed exemptions.
- Dragulescu, A. & Yakovenko, V. M. (2000). "Statistical mechanics of money." *European Physical Journal B* 17, 723.
- Dragulescu, A. & Yakovenko, V. M. (2001). "Evidence for the exponential distribution of income in the USA." *European Physical Journal B* 20, 585.
- Grimm, V. et al. (2006). "A standard protocol for describing individual-based and agent-based models." *Ecological Modelling* 198, 115-126.
- Simulation values in sections 2-4 computed by the author with the lab 03 code (Python 3 `random`, seed 1 for single runs, seeds 1-20 for replications, seeds 1-5 for the sweep).

## Interactive spec: examples/w03-policy-shape.html

**Insight the visual must make obvious:** policies A and B draw the same money-supply line, but different Lorenz curves. The aggregate chart cannot tell them apart and the distribution chart can.

**Layout.** Two linked panels stacked vertically (both widths), plus a results table.

1. **Top, "What the dashboard shows."** Money supply against tick (0 to the current tick), one line per enabled policy, colours from the token palette (A, B, C and "no policy" each get a fixed colour and a text label at the line's end). Linear y-axis by default with a toggle for log scale. A dashed target line at `N × m0`.
2. **Bottom, "What players live in."** Lorenz curves for each enabled policy at the current tick: x = cumulative share of players (poorest first), y = cumulative share of gold, with the diagonal equality line. Legend shows each policy's Gini to three decimals.
3. **Results table** under the charts, one row per enabled policy: money supply, Gini, top-10% share, median, share under `d` gold. Same column order and formatting as the lecture's simulation table.

**Controls.**
- Checkboxes for No policy, A, B, C (default: A and B on, so the first screen shows two identical money lines and two different Lorenz curves).
- Rate `r` slider 0.5%-10% (default 2%). Flat amount is derived, `f = r × m0`, and displayed.
- Run / Pause, speed (ticks per frame 1-50), "+100 ticks" button, Reset.
- Seed field (default 1), mulberry32. All enabled policies share the same seed so they see identical trade sequences (common random numbers). Implement by running each policy in its own agent array with its own PRNG initialised from the same seed.
- N fixed at 1,000, m0 = 100, d = 5, one tick = N trades.
- "Hand check" button that switches to the 4-player case (balances 100, 200, 300, 400; `f = 25`, `r = 10%`, trading off) and steps one tick per click, showing the balances in the table.

**Rules.**
- Trade step as week 2: `i` uniform, `j` uniform over the others, move `d` if `gold[i] ≥ d`. Gold is a float here because the policies produce fractions.
- After each tick: A `x ← x − r x + f`. B `x ← x − r x + (f N) x / M` with `M` the pre-policy total. C `x ← max(0, x + r x − f)`. No policy: unchanged.

**Test values.**
- Hand check, one tick: A (115, 205, 295, 385), Gini 0.225; B unchanged, Gini 0.250; C (85, 195, 305, 415), Gini 0.275. C after 6 ticks: player 1 = 0, total 1,015.73.
- Full model, tick 1,000, r = 2%: A money supply 100,000 and Gini in 0.18-0.21; B money supply 100,000 and Gini in 0.47-0.53; the A and B money lines must coincide to within rounding at every tick.
- C, r = 2%: money supply within 2% of 100,000 at tick 30 and above 150,000 by tick 200 (reference seed-1 Python values 112,088 at tick 100 and 298,250 at tick 200; the page's PRNG will differ).
- With B and No policy both enabled and the same seed, their Lorenz curves must be identical.

**Accessibility.** Keyboard operable controls with labels, visible focus, `prefers-reduced-motion` switches Run to stepwise "+10 ticks" updates, both colour schemes supported via `templates/interactive-tokens.css`. No game art.
