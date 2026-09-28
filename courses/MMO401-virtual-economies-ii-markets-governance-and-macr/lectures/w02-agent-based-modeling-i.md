# MMO401 · Week 02 — Agent-based modeling I

**Why this matters:** The faucet-and-sink spreadsheet from MMO304 tells you how much money exists. It cannot tell you who holds it, and players experience the economy through their own wallet, not the average one. An agent-based model simulates each player separately, so it can answer "who" questions. This week you build your first one and find that it disagrees with your intuition on the first run.

**You will be able to:**
- Name the parts of an agent-based model (agents, rules, environment, schedule, random seed, observers) and write the main loop in under 30 lines of code.
- Derive, by counting arrangements, why fair random trades between identical players produce a skewed wealth distribution.
- Compute the Gini coefficient, the share below the mean and the top-10% share from a list of balances, and compare them with the exponential prediction.
- Decide when an aggregate stock-flow model is enough and when you need agents.

**Before class:** Dragulescu, A. & Yakovenko, V. M. (2000), "Statistical mechanics of money," sections 1-3 (free on arXiv, cond-mat/0001432). Reread the seeds and trial-count sections of [MA102 week 11](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w11-monte-carlo-simulation.md). Course text, Lehdonvirta & Castronova (2014), continue the assigned chapters 9-12.

**Prerequisites from earlier courses:** [MA102 week 11, Monte Carlo simulation](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w11-monte-carlo-simulation.md) (seeded generators, repeated trials). [GD203 week 12, simulation-driven balance](../../GD203-combat-and-progression-design/lectures/w12-simulation-driven-balance.md) (what a spreadsheet cannot tell you). [MA102 week 12, descriptive statistics](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w12-descriptive-statistics-for-playtests.md) (mean versus median on skewed data). [MMO304 week 3](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w03-faucets-sinks-and-transformations.md) (faucets, sinks and the stock-flow model) and [MMO304 week 6](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w06-supply-demand-and-equilibrium-in-auction-houses.md) (auction-house equilibrium). [Week 1 of this course](w01-the-in-house-economist-role.md) (stocks, flows and why one summary number misleads).

**Interactive:** [Fair trades, unequal world](../examples/w02-random-exchange.html). Keep it open during section 3.

---

## 1. Where aggregate models run out

In MMO304 you modeled an economy as a few stocks (total gold, total ore) connected by flows (gold per hour from quests, gold per hour into repairs). That kind of model is called an **aggregate** or **stock-flow** model. It is fast, it fits in a spreadsheet, and for questions like "will the money supply grow?" it is the right tool.

It has one blind spot. Every player is folded into a single number. If total gold doubles, the model cannot say whether every player got twice as rich or whether a hundred players got a thousand times richer. Those are different games. The first one is mild inflation. The second one is a server where new players cannot afford anything the veterans sell.

An **agent-based model (ABM)** keeps every player separate. Each simulated player, called an **agent**, has its own state (gold, items, level) and follows rules (farm, trade, buy). You run the rules many times and watch what the population does. Patterns that no single rule mentions, like a wealth gap or a price bubble, show up on their own. That is called **emergence**.

### A game that surprised epidemiologists

The clearest case for agents came from outside economics. In September 2005 a new World of Warcraft raid, Zul'Gurub, contained a boss debuff called Corrupted Blood. It was meant to stay inside the raid. Players found that hunter pets could carry it out, and the plague reached the capital cities. It spread through player crowds and through non-player characters that carried it without dying. Blizzard tried quarantines and hotfixes, reset the servers, and patched pets to be immune on 8 October 2005.

Epidemiologists took notice. Ran Balicer wrote about it in *Epidemiology* in 2007. Eric Lofgren and Nina Fefferman argued in *The Lancet Infectious Diseases* the same year that game worlds capture something equation-based disease models leave out: how individual people actually react. Some players fled infected areas, some rushed in to help or to watch, some spread it on purpose. An aggregate model with one "infection rate" cannot contain a player who runs toward the plague. An agent can.

Economies are full of players who run toward the plague.

## 2. The parts of an agent-based model

Every ABM in this course has the same six parts. When you read or review a model, find each one.

| Part | What it is | Example in a game economy |
|---|---|---|
| Agents | The actors, each with its own state | 1,000 players, each with a gold balance |
| Rules | What an agent does given its state and what it sees | "If I have at least 5 gold, I may pay 5 gold to a random player" |
| Environment | Everything that is not an agent | The market, the price list, the map |
| Schedule | The order in which agents act and state updates | One random pair per step; a "tick" is 1,000 steps |
| Random seed | The starting value of the random number generator | `seed = 1`, recorded with every result |
| Observers | The numbers you compute to watch the run | Total gold, Gini coefficient, share of broke players |

A good habit is to write these six things down before any code. Ecologists who build agent-based models agreed on a standard way to do that, the ODD protocol (Overview, Design concepts, Details), published by Grimm and colleagues in 2006. You do not need the full protocol here. Week 3 uses a short version of it for your lab reports.

The main loop is always the same shape:

```
set up agents with starting state
for each step:
    choose which agent(s) act          (schedule)
    each chosen agent applies its rule (rules, may use the RNG)
    update the environment
    every so often, record observers
```

Two things about the schedule catch beginners. First, **synchronous** updates (everyone decides, then everyone acts at once) and **asynchronous** updates (one agent acts, the world changes, the next agent sees the change) can give different results. Games are asynchronous: the second player to reach the auction house sees the first player's purchase. Second, the order matters. If you always let agent 0 act first, agent 0 gets an advantage your game does not have. Pick actors at random.

## 3. Worked example: fair trades, unequal world

### The hook

In World of Warcraft, the trade window and the auction house move gold between players, and neither creates any. The auction house even destroys some: it keeps a 5% cut of each sale. Every player-to-player trade is, from the server's point of view, gold leaving one balance and arriving in another.

So imagine a fresh server where every character has exactly 100 gold, no quests pay out and nothing is destroyed. Players only trade with each other at fair prices, and nobody is smarter than anybody else. Does everyone stay near 100 gold?

Most people answer yes. The fair trades should cancel out. They do not. After enough trading, about 63% of players hold less than the average, the median player holds about 70 gold, and the richest tenth hold about a third of all the gold. Nothing in the rules favours anyone.

### The model

This is the random-exchange model that physicists Adrian Dragulescu and Victor Yakovenko published in 2000. Stated for a game:

```
N players, each starts with m0 gold.            (here N = 1,000, m0 = 100)
Each step:
    pick a random player i (the payer) and a different random player j
    if gold[i] ≥ d:  gold[i] −= d;  gold[j] += d      (here d = 5)
```

- `N` is the number of agents.
- `m0` is the starting balance, so the total gold is `M = N × m0` and never changes.
- `d` is the size of one trade.
- The rule "if gold[i] ≥ d" means nobody goes into debt. A player with less than `d` simply cannot pay this step.

Each step stands for a trade in which player i paid player j for something worth `d`. We ignore the item, because we only track gold. Every player is equally likely to be the payer or the payee. That is what "fair" means here.

Dragulescu and Yakovenko showed that, in any closed economy where money is conserved and exchanges are random like this, the balances settle into an **exponential distribution**:

```
share of players with about m gold  ∝  exp(−m / T),     where T = M / N = average balance
```

Physicists will recognise this as the Boltzmann-Gibbs distribution of energy in a gas, with the average balance playing the role of temperature. You met `exp` in [MA101 week 4](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w04-exponentials-and-the-xp-curve.md). Here it runs downhill: many players with little, a few with a lot.

### Why it happens: count the arrangements

You can see the reason with three players and three coins. List every way to split 3 coins among players A, B and C.

| Pattern | Arrangements | Count |
|---|---|---|
| (1, 1, 1) | A1 B1 C1 | 1 |
| (3, 0, 0) | A3, B3 or C3 | 3 |
| (2, 1, 0) | A2B1, A2C1, B2A1, B2C1, C2A1, C2B1 | 6 |
| Total | | 10 |

Random fair trades wander among these arrangements. Each move from one arrangement to another is exactly as likely as the move back, so in the long run every arrangement is equally likely. The equal split is 1 arrangement out of 10. Unequal splits are simply more numerous.

Now look at one player, say A. In how many of the 10 arrangements does A hold each amount?

| A holds | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| Arrangements | 4 | 3 | 2 | 1 |
| Probability | 40% | 30% | 20% | 10% |

The average is 1 coin, but A is most likely to hold 0, and holds less than the average 40% of the time and exactly the average only 30% of the time. The counts fall steadily as the amount rises. With 1,000 players and 20,000 trade-sized units of gold instead of 3, that falling staircase becomes the smooth exponential curve.

The point is not that trade is unfair. The point is that equality is one arrangement and inequality is millions of them. Chance alone pushes you toward the numerous ones.

### Numbers you can check

For an exponential distribution with mean `T`, four summary numbers follow from the formula alone. You can check each with a calculator.

| Statistic | Formula | Value with T = 100 |
|---|---|---|
| Share of players below the mean | `1 − e^(−1)` | 63.2% |
| Median balance | `T × ln 2` | 69.3 gold |
| Share of all gold held by the richest 10% | `0.1 × (1 + ln 10)` | 33.0% |
| Gini coefficient | exactly `0.5` | 0.50 |

The **Gini coefficient** measures inequality on a scale from 0 (everyone equal) to 1 (one player has everything). For a list of `n` balances with mean `μ`, it is the average absolute difference between two randomly chosen players, divided by twice the mean:

```
G = Σ_i Σ_j |x_i − x_j|  /  (2 × n² × μ)
```

Check it on four players with 100, 200, 300 and 400 gold. The six pairwise differences are 100, 200, 300, 100, 200 and 100, which sum to 1,000. Each pair appears twice in the double sum, so the numerator is 2,000. The denominator is `2 × 16 × 250 = 8,000`. So `G = 0.25`.

Now the simulation. These values come from the Python code in section 4 with `seed = 1`, `N = 1,000`, `m0 = 100` and `d = 5`, so you can reproduce them exactly.

| Trades so far (per player) | Gini | Below mean | Median | Top 10% share | Broke (0 gold) | Total gold |
|---|---|---|---|---|---|---|
| 0 | 0.000 | 0% | 100 | 10.0% | 0% | 100,000 |
| 10,000 (10) | 0.126 | 44.5% | 100 | 13.9% | 0% | 100,000 |
| 100,000 (100) | 0.347 | 51.8% | 95 | 21.4% | 3.1% | 100,000 |
| 500,000 (500) | 0.469 | 59.6% | 75 | 30.3% | 2.5% | 100,000 |
| 1,000,000 (1,000) | 0.512 | 62.0% | 70 | 32.5% | 5.8% | 100,000 |
| 2,000,000 (2,000) | 0.519 | 62.2% | 65 | 34.2% | 6.7% | 100,000 |

The total never moves. The distribution walks from a spike at 100 to the exponential shape, and after about 1,000 trades per player it matches the theory. The Gini lands a little above 0.5 because gold here comes in chunks of 5, not continuously. With 20 chunks per player on average, the exact discrete prediction is a Gini of 0.512 and 4.8% of players broke, which is what the table shows within noise. Twenty runs with seeds 1 to 20 give a mean Gini of 0.510 with a standard deviation of 0.008 after 2,000 trades per player.

### Move it yourself

Open the interactive. The left view is a "skyline": 500 thin bars, one per player, sorted from poorest to richest, with a flat line at the average. The right view is a histogram of balances with the exponential curve `exp(−m/T)/T` drawn over it. Press Run. The skyline starts flat, then tilts into a ramp. The histogram starts as one tall bar at 100 and spreads until it sits on the curve. The counter for total gold never changes. Change the starting gold or the trade size and the curve rescales but keeps its shape. That is the lesson in one picture: the average holds still while the experience of the average player gets worse.

### Cross-context recognition

**Real incomes (United States, 1947-1994 data).** In a 2001 follow-up, Dragulescu and Yakovenko fitted US tax and census data and found that individual income follows an exponential distribution. For single earners the Gini came out close to 0.5, the value our model predicts. For two-earner families it was about 0.375, because adding two exponential incomes gives a less skewed total.

**Sugarscape (Epstein and Axtell, 1996).** In *Growing Artificial Societies*, agents with different vision and metabolism wander a grid collecting "sugar." Even this very simple world produces a strongly skewed wealth distribution. Sugarscape adds differences between agents. Our model shows that you do not even need those. Chance is enough to start the skew, and differences in skill make it steeper.

**Zero-intelligence traders (Gode and Sunder, 1993).** Section 5 describes the experiment in detail. Random traders in a double auction reach almost the same market efficiency as human traders. It is the same idea turned the other way: the rules of interaction, not the intelligence of the agents, set the outcome you see at the population level.

In all three, a population-level pattern comes from the structure of interactions, not from anyone's intention. When you see a pattern in your game's telemetry, your first question should be: *would it appear even if every player behaved randomly?* If yes, it is a baseline, not a discovery.

### Eyes-open design judgment

- **A Gini of 0.5 is the baseline, not a scandal.** If your economy's wallet Gini is 0.5, that is roughly what pure chance produces. Compare your measured number to a random-exchange baseline with the same money supply before calling it an exploit or a cartel.
- **Inequality you did not design still shapes play.** 63% of players below average means most players feel poorer than your balance spreadsheet says. If prices are set by the richest buyers, those players are priced out. You may decide to accept that, or to add faucets that pay everyone equally. Week 3 tests exactly that choice.
- **Trade size matters for speed, not for the end state.** Bigger trades reach the exponential faster. Rare expensive items (large `d` relative to wealth) churn the distribution quickly, which is one reason a big-ticket market feels volatile.
- **Use agents when the question has "who" in it.** "How much gold will exist in six months?" is an aggregate question. "How many new players will be able to afford a mount in six months?" is an agent question.
- **Do not trust an ABM you have not broken on purpose.** This model has a known answer. Your own models will not. Build in a check like "total gold never changes" and run it every time.

## 4. Building it: code and pitfalls

Here is the whole model in Python. It is the code that produced the table above.

```python
import random

def gini(xs):
    xs = sorted(xs); n = len(xs); s = sum(xs)
    cum = sum((i + 1) * x for i, x in enumerate(xs))
    return (2 * cum) / (n * s) - (n + 1) / n

def run(N=1000, m0=100, d=5, trades=1_000_000, seed=1):
    rng = random.Random(seed)          # private, seeded generator (MA102 week 11)
    gold = [m0] * N
    for t in range(trades):
        i = rng.randrange(N)           # payer
        j = rng.randrange(N - 1)       # payee, drawn so that j != i
        if j >= i:
            j += 1
        if gold[i] >= d:
            gold[i] -= d
            gold[j] += d
    assert sum(gold) == N * m0         # conservation check
    return gold

g = run()
print(round(gini(g), 3))               # 0.512
```

The `gini` function uses a sorted-list formula that gives the same answer as the double sum above, in `n log n` time instead of `n²`.

Five pitfalls, each of which has cost someone a week:

1. **Letting a player trade with themselves.** Drawing `j` from all `N` players sometimes gives `j == i`. Those steps do nothing but still count as trades, which slows the run and skews your "trades per player" axis. The `j += 1` trick above draws uniformly from the other `N − 1` players.
2. **Measuring before the model settles.** The first rows of the table are not the model's answer. They are the model on its way to its answer. The period you throw away is called **burn-in**. Plot an observer against time and wait until it stops drifting.
3. **Using floats for money that should be whole.** Floating-point gold can drift by tiny amounts, and then your conservation check fails for a reason that is not a bug in your rules. Use integers when the game uses integers.
4. **Using the global random generator.** If another part of your code also draws from `random`, your results change when that code changes. Give the model its own `random.Random(seed)`.
5. **Reporting one run.** One seed is one story. Week 3 turns runs into evidence with replications and confidence intervals.

## 5. Agents with intent: zero-intelligence traders

The random-exchange agents do not even know prices. Real markets have buyers who value an item and sellers who paid to make it. In 1993 Dhananjay Gode and Shyam Sunder asked how much of a market's performance comes from the traders' intelligence and how much comes from the market's rules. They built traders with **zero intelligence**: each one bids or asks a random price.

They tested two kinds. **Unconstrained** traders (ZI-U) could bid any price, even above what the item was worth to them. **Constrained** traders (ZI-C) bid randomly but never above their own value (buyers) or below their own cost (sellers). Put ZI-C traders into a double auction, the same institution as EVE's order book or a stock exchange, and the market's **allocative efficiency** comes out close to that of human traders. Allocative efficiency is the share of the maximum possible gains from trade that the market actually delivers. Gode and Sunder's title calls the market "a partial substitute for individual rationality."

A small case you can do by hand shows what efficiency measures. Three buyers value a potion at 30, 25 and 20 gold. Three sellers can make one at a cost of 10, 15 and 25 gold.

| Pair | Buyer value | Seller cost | Gain if they trade |
|---|---|---|---|
| Highest value with lowest cost | 30 | 10 | 20 |
| Second with second | 25 | 15 | 10 |
| Third with third | 20 | 25 | −5 (should not trade) |

The most surplus this market can make is 30 gold, from two trades. Any price between 20 and 25 clears it: two buyers are willing, two sellers are willing, and the third pair is not. A ZI-C market might pair the 30-buyer with the 15-seller and the 25-buyer with the 10-seller. The surplus is still `(30 − 15) + (25 − 10) = 30`. Efficiency is lost only when the wrong people trade, for example if the 20-buyer beats the 25-buyer to a cheap seller. The constraint "never trade at a loss" rules out the worst mistakes, and the auction's matching rules do the rest.

For a game designer the lesson is uncomfortable and useful. Much of what your market does is set by its rules (who sees which orders, how offers match, what fees apply), not by how clever your players are. That is why week 5 spends a whole session on order books, and why week 7's transaction-tax model is an agent-based simulation.

## In-class activity (25 minutes)

Run the random-exchange model with people. Groups of six. Each person starts with 5 tokens (coins or paper clips). You need one six-sided die per group.

1. Number yourselves 1 to 6. Each round, roll twice: the first roll picks the payer, the second picks the payee. Reroll the second if it matches the first. If the payer has at least one token, they give one to the payee. (15 min, aim for 40 rounds; one person keeps a tally sheet)
2. At rounds 0, 10, 20, 30 and 40, write down everyone's holdings, sorted. Compute the share of people below the mean (the mean is always 5).
3. Pool results from all groups on the board. Compare the share with 0 tokens against the prediction from counting arrangements. With 6 people and 30 tokens there are `C(35, 5) = 324,632` arrangements, and one player holds 0 in `C(34, 4) = 46,376` of them, about 14.3%. (10 min)

Expected output: each group's sorted holdings at round 40, the class-wide share of broke players, and a one-sentence answer to "did anyone cheat?"

## Common misconceptions

- **"If every trade is fair, the distribution stays equal."** Fair trades make every arrangement equally likely, and unequal arrangements vastly outnumber equal ones. Fairness of the process does not mean equality of the result.
- **"Inequality means some players are better at the game."** It can, but the random-exchange baseline already has a Gini of about 0.5 with identical players. Skill adds to that baseline. Measure against it.
- **"An ABM is just a Monte Carlo simulation."** A Monte Carlo simulation repeats independent trials of the same thing (MA102 week 11). In an ABM the agents interact, so each step depends on everything before it. You still use Monte Carlo ideas (seeds, replications) to study an ABM's output.
- **"More agents make the model more realistic."** More agents reduce noise. Realism comes from the rules. A million agents following a wrong rule give you a precise wrong answer.

## Check yourself

1. In the random-exchange model with an average of 250 gold per player, what are the predicted median balance and the share of players below 250?
2. With three players and four coins, how many arrangements are there? In how many does player A hold 0 coins? What probability does that give?
3. Four players hold 50, 50, 150 and 150 gold. Compute the Gini coefficient.
4. A colleague runs the section 4 code for 50,000 trades with 1,000 players and reports "Gini 0.26, so trading is mild on our server." What is wrong with the conclusion?
5. Your game's live wallet Gini is 0.78. Is that evidence of something beyond chance? What would you compute to decide?

<details>
<summary>Answers</summary>

1. Median `250 × ln 2 ≈ 173` gold. Share below 250 is `1 − e^(−1) ≈ 63.2%`.
2. The number of ways to put 4 identical coins into 3 players is `C(6, 2) = 15`. If A holds 0, the 4 coins go to B and C in 5 ways (0-4 through 4-0). So `5/15 ≈ 33%`.
3. Mean 100. Pairwise differences: 0 (the two 50s), 0 (the two 150s) and four pairs of 100, sum 400. Numerator `2 × 400 = 800`, denominator `2 × 16 × 100 = 3,200`. `G = 0.25`.
4. 50,000 trades is 50 per player, still in burn-in. The table shows Gini still climbing at that point. The settled value is about 0.51. Measure after the observer stops drifting.
5. Yes, it is well above the random-exchange baseline of about 0.5. To be sure, run the random-exchange model with your server's actual player count and money supply, several seeds, and compare. Then add one real-game difference at a time (income from play, sinks, skill) to see which one moves the Gini toward 0.78. Week 3 shows how.

</details>

## Lab / assignment hook

[Lab 02, your first agent-based economy](../labs/lab02.md). Implement the random-exchange model from the starter code, verify it against the exponential predictions, then add one rule of your own (a trade-size distribution, a savings rule, or a minimum balance) and report how it changes the Gini. This is the first of the ABM labs that make up 40% of the course grade.

## Sources

- Wikipedia, "Corrupted Blood incident" (accessed 2026). Zul'Gurub debuff, 13 September to 8 October 2005, pet immunity patch, and the epidemiology papers that followed.
- Balicer, R. D. (2007). "Modeling infectious diseases dissemination through online role-playing games." *Epidemiology* 18(2).
- Lofgren, E. T. & Fefferman, N. H. (2007). "The untapped potential of virtual game worlds to shed light on real world epidemics." *The Lancet Infectious Diseases* 7(9).
- Warcraft Wiki, "Auction House." 5% cut of the winning bid; deposit rules; faction auction houses merged in patch 6.0.2 (2014).
- Dragulescu, A. & Yakovenko, V. M. (2000). "Statistical mechanics of money." *European Physical Journal B* 17, 723. The random-exchange model and the exponential (Boltzmann-Gibbs) result.
- Dragulescu, A. & Yakovenko, V. M. (2001). "Evidence for the exponential distribution of income in the USA." *European Physical Journal B* 20, 585. Gini about 0.5 for single earners.
- Epstein, J. M. & Axtell, R. (1996). *Growing Artificial Societies: Social Science from the Bottom Up*. Brookings Institution Press.
- Gode, D. K. & Sunder, S. (1993). "Allocative Efficiency of Markets with Zero-Intelligence Traders: Market as a Partial Substitute for Individual Rationality." *Journal of Political Economy* 101(1), 119-137.
- Grimm, V. et al. (2006). "A standard protocol for describing individual-based and agent-based models." *Ecological Modelling* 198, 115-126.
- Simulation values in section 3 computed by the author with the section 4 code (Python 3 `random`, seed 1 and seeds 1-20).

## Interactive spec: examples/w02-random-exchange.html

**Insight the visual must make obvious:** total gold never changes, yet the distribution moves from everyone-equal to an exponential shape where most players are below average.

**Layout.** Two linked panels plus a stats strip. Side by side at 1280px, stacked at 390px.

1. **Left, "Every player, sorted."** A skyline of `N` vertical bars (default N = 500), sorted ascending by gold, height = gold. A horizontal line at the mean `T = m0` labelled "average." Bars below the line use the muted token colour, bars above use the accent colour, so the share below average is visible as the width of the muted region.
2. **Right, "How many players hold how much."** Histogram of balances, bin width = `d`, x from 0 to `6 × T`. Overlay the continuous exponential prediction `N × d × exp(−m/T) / T` as a line, labelled "exponential prediction." Toggle to a log y-axis (on log scale the prediction is a straight line).
3. **Stats strip** (live, monospaced): trades per player, total gold (must stay constant, show it prominently), Gini, share below mean, median, top-10% share, share broke. Next to each of the last four, the exponential prediction in a lighter style: 63.2%, `T ln 2`, 33.0%, 0.50 (and the discrete-chunk correction for broke, `1/(T/d + 1)`).

**Controls.**
- Run / Pause button (space bar toggles). Speed slider: 10 to 5,000 trades per animation frame.
- Buttons "+100 trades per player" and "+1,000 trades per player" that advance instantly without animation.
- N: 100, 500 (default), 1,000.
- Starting gold `m0`: 20-500 (default 100). Trade size `d`: 1-50 (default 5). Changing either resets.
- Seed field (integer, default 1), mulberry32 PRNG. Same seed and settings must reproduce the same run. Reset button.

**Rule per trade.** Draw `i` uniformly from 0..N−1, draw `j` uniformly from 0..N−2 and add 1 if `j ≥ i`. If `gold[i] ≥ d`, move `d` from i to j. Gold stays integer.

**Gini.** Sorted formula `G = 2 Σ (k+1) x_(k) / (n Σx) − (n+1)/n` with 0-based `k`.

**Test values.**
- At 0 trades: Gini 0.000, top-10% share 10.0%, below mean 0%.
- N = 1,000, m0 = 100, d = 5, after 2,000 trades per player: Gini in 0.49-0.53, below mean 60-64%, median 60-75, top-10% share 31-36%. (The Python reference with seed 1 gives 0.519, 62.2%, 65, 34.2%; the page's PRNG stream will differ.)
- Total gold equals `N × m0` at every frame. If it ever differs, show a red "conservation broken" badge (this is a self-test and should never appear).
- d = 1, m0 = 100: after 1,000 trades per player the Gini is still well below 0.5 (about 0.25), demonstrating slower relaxation with small trades.

**Reduced motion.** With `prefers-reduced-motion`, Run advances in steps of 100 trades per player per click instead of animating. No game art; bars and lines only, palette from `templates/interactive-tokens.css`.
