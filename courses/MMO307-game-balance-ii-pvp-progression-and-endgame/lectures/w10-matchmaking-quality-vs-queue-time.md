# MMO307 · Week 10 — Matchmaking Quality vs Queue Time

**Why this matters:** Every ranked queue answers two complaints at once. "I waited five minutes" and "that match was a stomp" come from the same dial, and turning it one way makes the other complaint louder. This week you learn to put numbers on both sides and choose a point on the curve on purpose.

**You will be able to:**
- Compute the expected queue time and expected match fairness for a player at any rating, given a rating distribution, an arrival rate and a search window.
- Derive why wait times explode for the best players and estimate by how much from their distance to the mean.
- Compare fixed and expanding search windows, and predict what splitting a queue into more modes does to wait times.
- Design matchmaking targets (a wait percentile and a fairness ceiling) and defend where they sit on the trade-off curve.

**Before class:** Herbrich, Minka & Graepel (2006), "TrueSkill: A Bayesian Skill Rating System", the short section on matchmaking and match quality. Microsoft Research's TrueSkill project page, the paragraphs on matchmaking. Reread your notes on the Elo expected-score curve from MMO307 week 8.

**Prerequisites from earlier courses:** [MMO307 week 8, Elo and expected score](w08-elo-and-expected-score.md), and [week 9, Glicko and TrueSkill](w09-glicko-and-trueskill.md), on rating uncertainty. [MA102 week 8, dice sums and the normal curve](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w08-dice-sums-and-the-normal-curve.md) for `Φ` and z-scores. [MA102 week 7, the geometric distribution](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w07-geometric-distribution-kills-until-the-drop.md) for waiting times, the mean `1/p` and percentiles. [MMO303 week 5, the holy trinity](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w05-the-holy-trinity-tank-healer-dps.md), section 3, for role-supply queue math. [MA102 week 11, Monte Carlo simulation](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w11-monte-carlo-simulation.md) for the lab.

**Interactive:** [`examples/w10-queue-fairness-curve.html`](../examples/w10-queue-fairness-curve.html). Keep it open during section 2.

---

## 1. Two complaints, one dial

A matchmaker has one job. It takes the players who are waiting and decides who plays whom. Two things make a pairing good.

- **Match quality**, or fairness, is how evenly matched the two sides are. You met the measure in week 8. If the stronger player's Elo expected score is 0.50, the match is a coin flip. If it is 0.80, the favourite wins four games in five and the match is close to decided before it starts.
- **Queue time** is how long a player waits between pressing the button and loading in.

Both depend on the **search window**, written `w`. It is the largest rating gap the matchmaker accepts. A player rated 1,700 with a window of 50 will play anyone from 1,650 to 1,750. A narrow window gives fair matches and long waits. A wide window gives short waits and lopsided matches.

That much is obvious. What is not obvious is the shape of the trade-off, and how differently it treats different players. The same window that gives the median player a 25-second queue can give the top player a 35-minute queue. Designers who tune the matchmaker by looking at the average wait never see that player, and that player is often the one streaming your game.

This lecture builds a small model you can compute by hand, then uses it to make three design decisions: how wide the window should be, whether it should grow while a player waits, and what splitting the queue into more modes will cost.

## 2. Worked example: the queue-time vs fairness curve

### The hook

Microsoft Research's page for TrueSkill, the rating system behind Halo 3 and later Xbox titles, says it plainly. There is an inherent conflict between waiting time and match quality, because the longer the matchmaker waits, the better the opponent it can find. The page then adds the part players feel. For the very best players there are simply not enough opponents of their level online at any moment.

Top players know this from experience. The queue that pops in seconds at a middling rank takes minutes near the top of the ladder, and the matches it eventually finds are often against someone far below. So here is the puzzle. The matchmaker treats every player the same. Why does it treat the best players so much worse?

### The model

Four quantities describe the queue.

- The **rating distribution**. Ratings across the population are roughly normal with mean `μ` and standard deviation `σ`. We use `μ = 1500` and `σ = 200`.
- The **arrival rate** `λ` is how many players enter the queue per minute, across all ratings. We use `λ = 12`.
- The waiting player's **rating** `r`.
- The **window** `w`.

Only arrivals within the window are acceptable. The share of arrivals that fall inside `[r − w, r + w]` is the normal probability of that interval:

```
p(r, w) = Φ((r + w − μ) / σ) − Φ((r − w − μ) / σ)
```

`Φ` is the standard normal cumulative distribution from MA102 week 8. Acceptable opponents therefore arrive at a rate of `λ × p(r, w)` per minute.

When events arrive at a steady rate and independently of each other, the wait for the first one is the continuous cousin of the geometric wait from MA102 week 7. It has the same memoryless behavior, and its mean is one over the rate:

```
mean wait (seconds) W(r, w) = 60 / (λ × p(r, w))
```

For fairness we reuse the Elo curve from week 8. If the two ratings differ by a gap `d`, the favourite's expected score is:

```
E_fav(d) = 1 / (1 + 10^(−d / 400))
```

The model's fairness number is the average of `E_fav` over all the opponents the window accepts, each weighted by how common that rating is.

One simplifying assumption is worth naming. The model counts only players who arrive after our player, so it ignores opponents who are already waiting. That makes it pessimistic about waits, by a factor of about two for a quiet queue. The lab removes the assumption with a simulation. The shape of the trade-off does not change, and the shape is the lesson.

### The shortcut you can do in your head

When the window is small compared with `σ`, the normal density barely changes across it, so the share is about the window's width times the density at `r`:

```
p(r, w) ≈ 2w × f(r),   where f(r) = exp(−z² / 2) / (σ √(2π))  and  z = (r − μ) / σ
```

For the median player, `z = 0`, and with `σ = 200` we get `σ √(2π) ≈ 501.3`. So `p ≈ w / 250.7` and:

```
W × w ≈ 60 × 250.7 / 12 ≈ 1,253   (seconds × rating points, median player)
```

The wait multiplied by the window is a constant. **Halve the window and you double the wait.** The curve is a hyperbola.

The fairness side has a shortcut too. Near a gap of zero, the Elo curve is almost a straight line with slope `ln 10 / 1600 ≈ 0.00144` per rating point (week 8 calls it `g`). In a small window the average gap is about `w / 2`, so:

```
E_fav ≈ 0.5 + 0.00072 × w
```

This works well up to a window of about 150. Beyond that the Elo curve bends and the shortcut overstates the favourite's edge.

Now the player at the top. A player at `r = 2100` sits three standard deviations above the mean, so `z = 3`. The density there is smaller by a factor of `exp(−9/2) ≈ 0.011`. Every wait is about **90 times longer** than the median player's for the same window. At two standard deviations the factor is `exp(−2) ≈ 0.135`, so waits are about 7.4 times longer. The matchmaker is identical for everyone. The population is not.

### Numbers you can check

This script computes the exact model. It prints the table below.

```python
from math import erf, sqrt, exp

MU, SIGMA = 1500, 200      # rating population
LAM = 12                   # players entering the queue per minute

def Phi(z):
    return 0.5 * (1 + erf(z / sqrt(2)))

def share_in_window(r, w):
    """Fraction of arriving players rated within r - w .. r + w."""
    return Phi((r + w - MU) / SIGMA) - Phi((r - w - MU) / SIGMA)

def mean_wait_seconds(r, w):
    return 60 / (LAM * share_in_window(r, w))

def favourite_score(r, w, steps=2000):
    """Average expected score of the stronger player, over accepted opponents."""
    num = den = 0.0
    for i in range(steps):
        x = r - w + (i + 0.5) * 2 * w / steps
        dens = exp(-0.5 * ((x - MU) / SIGMA) ** 2)
        gap = abs(x - r)
        num += dens / (1 + 10 ** (-gap / 400))
        den += dens
    return num / den

for r in (1500, 1900, 2100):
    print(f"rating {r}")
    for w in (25, 50, 100, 200, 400):
        print(f"  w={w:>3}  share={share_in_window(r, w):.4f}  "
              f"wait={mean_wait_seconds(r, w):7.1f} s  "
              f"favourite={favourite_score(r, w):.3f}")
```

| Window `w` | Median player (1500): wait | Fairness | 2σ above (1900): wait | Fairness | 3σ above (2100): wait | Fairness |
|---|---|---|---|---|---|---|
| 25 | 50.3 s | 0.518 | 367.6 s | 0.518 | 4,420 s | 0.518 |
| 50 | 25.3 s | 0.536 | 179.6 s | 0.536 | 2,081 s | 0.537 |
| 100 | 13.1 s | 0.570 | 82.5 s | 0.575 | 836.5 s | 0.580 |
| 200 | 7.3 s | 0.626 | 31.8 s | 0.656 | 220.1 s | 0.678 |
| 400 | 5.2 s | 0.683 | 10.0 s | 0.789 | 31.5 s | 0.835 |

Check two cells against the shortcuts. At the median with `w = 50`, the shortcut says `1253 / 50 ≈ 25.1` seconds, and the exact value is 25.3. At 2100 with `w = 50`, the shortcut says `25.1 / 0.011 ≈ 2,260` seconds, and the exact value is 2,081. The shortcut is close because the window is narrow. It drifts as the window widens and the density changes across it.

Three things jump out of the table.

1. **The median player's curve is gentle.** Going from a window of 50 to 100 saves 12 seconds and moves fairness from 0.536 to 0.570. Most designers would take either point.
2. **The top player's curve is brutal.** With the median player's window of 50, the 2100 player waits 35 minutes. To bring their wait down to half a minute you need a window of 400, and then the average favourite wins 83.5% of the time.
3. **The fairness column changes shape at the top.** For the median player, a wide window reaches down and up equally. For the 2100 player, almost every opponent inside a 400 window is *below* them, because there is hardly anyone above. The average gap is much larger than `w / 2`. Wide windows at the top produce the "why am I playing a Gold player?" complaints, and they are not a bug.

### A visual you can move

Open the interactive. The left panel shows the rating distribution with your player marked and the window shaded. The shaded area is `p(r, w)`. The right panel plots the trade-off curve, with mean wait on the horizontal axis (log scale) and the favourite's expected score on the vertical axis. Each point on the curve is one window size.

Drag the window slider for the median player and watch the point slide along a gentle curve near the bottom left. Now drag the rating slider to 2100 without touching the window. The shaded sliver on the left becomes almost invisible, and the point on the right jumps an order of magnitude to the right. Same rule, same window, different world. Then drag the arrival rate down to 3 per minute, an off-peak hour, and watch every curve slide right by a factor of four.

### Cross-game recognition

Every real matchmaker is more complex than this model. Each one still turns the same two knobs, `λ` (how many players are in the pool) and `p` (what share of them are acceptable).

**TrueSkill on Xbox Live (Halo 3 onward).** Microsoft's system defines match quality as the rescaled chance that the two sides would draw. A draw is most likely when the two skill estimates are equal and both are certain. In our terms that quality score replaces `E_fav` as the fairness axis. It rises toward its maximum as the gap goes to zero, just as `E_fav` falls toward 0.5. The project page also notes that uncertainty matters. Two players with the same skill estimate make a worse match if either estimate is uncertain (week 9's rating deviation `RD`, not our population `σ`). The trade-off Microsoft describes, and its note that top players lack opponents, is the right half of our table.

**Dota 2 (current client).** Valve's matchmaking settings let players tick which game modes and regions they accept. The Dota 2 Wiki notes that selecting more options can cut the wait sharply because the matchmaker searches a larger pool, and that Ranked Roles, where you queue for one position, usually takes longer. Both are statements about `p`. Every restriction a player adds multiplies their acceptable share by something less than one, and their wait grows by the reciprocal. Valve pays players to widen their own `p`. Queuing with all roles selected earns 4 Role Queue games, stored up to 60, which buy faster queues later. It is a trade of the player's flexibility now for the player's wait later.

**World of Warcraft Dungeon Finder (patch 3.3.0, December 2009).** Before this patch, groups formed from one realm's players. The Dungeon Finder formed groups from every realm in a battlegroup. That multiplies `λ` by the number of realms. Since `W ∝ 1 / λ`, a battlegroup of ten realms cuts every wait by about ten, for every rating and every window, with no loss of fairness at all. The cost was social, not mathematical. You were now grouped with strangers you would never see again. The same Dungeon Finder later added Call to Arms to fix role scarcity, which is a different queue problem that MMO303 week 5 covers.

Three systems, one form. Each lever either enlarges the pool `λ`, enlarges the acceptable share `p`, or changes the fairness measure. When you read a new matchmaking change, ask which of the three it touches.

### Eyes-open design judgment

- **Average wait hides the problem.** A population-wide mean wait is dominated by the median player, who is fine. Report waits per rating band, and look at the top 1% separately.
- **A single fixed window is the wrong tool.** Any fixed window is either unfair in the middle or unbearable at the top. Section 3 shows the usual fix.
- **Pool size is the cheapest fairness.** Every doubling of `λ` halves waits at every rating and costs no fairness. Merging regions, modes, platforms or servers is often the best balance change a matchmaker can get. It costs latency, language and social ties, and those are real costs you must weigh.
- **Decide the fairness you want per mode.** A casual mode can accept a favourite at 0.65 if queues are instant. A ranked mode where rating is at stake should aim lower. Write the target down before tuning.
- **Fairness has a floor you cannot beat.** Ratings are estimates. If the rating system's error is 100 points, a window of 10 gains nothing over a window of 50. Tighten the window only as far as your ratings are accurate.

### Check this example

1. With `σ = 200` and `λ = 12`, estimate the median player's mean wait and fairness for `w = 80`, using the shortcuts.
2. A player at 1900 (two standard deviations up) uses `w = 50`. Estimate their wait from the median player's 25.1 seconds and the density factor. Compare with the table.

<details>
<summary>Answers</summary>

1. `W ≈ 1253 / 80 ≈ 15.7` seconds. `E_fav ≈ 0.5 + 0.00072 × 80 ≈ 0.558`.
2. The density factor at `z = 2` is `exp(−2) ≈ 0.135`, so `W ≈ 25.1 / 0.135 ≈ 186` seconds. The table says 179.6. The shortcut is a little high because the density rises toward the mean inside the window, which adds opponents on the lower side.

</details>

## 3. Expanding windows: a different window for every second

The standard fix for the top-player problem is to let the window grow while a player waits. The player starts with a strict window, so anyone who can be matched fairly is matched fairly. If nobody arrives, the window widens until someone does. Call the starting window `w₀`, the widening speed `v` in rating points per second, and the cap `w_max`:

```
w(t) = min(w₀ + v × t, w_max)
```

The chance of matching in any short moment now changes over time, so the wait is no longer a simple `1 / rate`. You can still compute it by stepping through time. Keep track of the probability that the player is still waiting, and at each small step multiply by the chance a suitable arrival shows up in that step. Record the window at the moment of the match, because the fairness depends on it.

With `w₀ = 25`, `v = 5` points per second and `w_max = 400`, same population and arrival rate:

| Player | Mean wait | Fairness at match | Fixed window with similar wait | Its fairness |
|---|---|---|---|---|
| 1500 (median) | 16.1 s | 0.571 | `w = 100`, 13.1 s | 0.570 |
| 1900 (2σ up) | 40.7 s | 0.673 | `w = 200`, 31.8 s | 0.656 |
| 2100 (3σ up) | 81.6 s | 0.799 | `w = 400`, 31.5 s | 0.835 |

Read this table carefully, because it does not flatter the expanding window.

For the median player, expansion buys nothing. A fixed window of 100 gives about the same wait and fairness. For the 2100 player, expansion has turned a 35-minute queue (at `w = 50`) into an 82-second one. It did that by accepting, on average, an opponent the player beats 80% of the time.

That is the honest result. **Expanding windows do not beat the trade-off curve. They choose a different point on it for each player, automatically.** The median player lands near the fair end because a match shows up before the window grows much. The top player lands near the fast end because nothing shows up until the window is wide. The widening speed `v` is the knob that decides how long you make the top player wait before you give up on fairness.

This is a design statement, whether or not you write it down. With `v = 5`, you have decided that a top player's time is worth more than their match quality after about a minute. You might decide the opposite for a tournament qualifier, where a wrong result costs more than a wait.

Two refinements appear in most shipped matchmakers.

- **Both players' windows must agree.** The lab's simulation pairs two waiting players only if their gap fits inside *both* windows. Otherwise a player who has just joined, with a strict window, gets dragged into a match set by someone else's wide one.
- **Waiting players count.** The simple model only looks at new arrivals. In a real pool, players who are already waiting are candidates too, so waits are shorter than the model says. That is why the model is a planning tool. You simulate to get the number you ship.

## 4. What splitting the queue costs

Every new queue divides `λ`. Suppose a game has one ranked queue with `λ = 12` per minute. Designers add solo and party queues, then a second ranked mode, and the players split roughly evenly into three pools with `λ = 4` each. Since `W ∝ 1 / λ`, every wait in the table triples at the same window.

To keep the median player's wait at 25 seconds, `W × w ≈ 1253` becomes `W × w ≈ 3760`, so the window must grow to about 150. Fairness drops from 0.536 to about `0.5 + 0.00072 × 150 ≈ 0.61`. The new mode has cost every match in the game some fairness, including matches in the modes that already existed.

The same arithmetic applies to every restriction.

- **Region and server.** A game with four regions has four pools. Merging two halves both their waits but adds latency. A 30-point rating gap may matter less than 80 milliseconds of ping.
- **Party size.** Matching a five-player party only against other five-player parties splits the pool. Letting parties face solo players restores `λ` but adds a coordination advantage that the rating system does not see.
- **Roles and recipes.** A team game needs a fixed mix of roles. The scarcest role sets how many matches can form, as MMO303 week 5 showed, and every player in a surplus role waits for it. That wait sits on top of the rating window. Role-restricted queues multiply the two problems.
- **Time of day.** `λ` swings through the day. The same window that works at 8 pm gives off-peak players four times the wait at 4 am. Some games widen windows at quiet hours. Others accept long queues and say so.

The lesson for content planning is blunt. Before you add a mode, estimate its `λ` and put it through the trade-off curve. A mode that looks popular in a survey can still fail if its players are split across five regions and three party sizes.

## 5. Choosing a point on the curve

A trade-off becomes a decision when you write targets. Two targets are enough for most queues.

**A wait target, as a percentile.** Players remember their worst queue, not their average one. The time to the first arrival of a steady random stream has a long right tail. Its 90th-percentile wait is `ln 10 ≈ 2.30` times its mean, the continuous version of the percentile rule from MA102 week 7. A mean of 25.3 seconds therefore means one queue in ten runs past 58 seconds. If your target is "90% of queues under a minute", the mean must stay under 26 seconds.

**A fairness ceiling.** Choose the highest average favourite expected score you accept. For a ranked mode, 0.60 is a common working number in this course. It means the favourite wins three games in five.

Then check both targets per rating band, not for the population. You will usually find the median band meets both easily and the top band cannot meet both at once. That is the moment for an explicit, written rule. Common choices:

- Accept longer waits at the top and tell players ("Estimated wait: 4 minutes"). Honesty lowers the complaint rate even when it cannot lower the wait.
- Accept worse fairness at the top and reduce what is at stake. For example, a lopsided match can move rating less when the favourite wins.
- Grow the pool at the top by merging regions or ranked modes only for the highest bands.

Every one of these is defensible. What is not defensible is discovering the top-band problem from a streamer's complaint after launch.

## In-class activity (25 minutes)

In groups of three, you run matchmaking for a small competitive MMO arena. The population has `μ = 1500` and `σ = 200`. At peak, 12 players per minute enter the queue. Off-peak it is 3.

1. Using the interactive, find the smallest fixed window that keeps the median player's mean wait under 20 seconds at peak. Record the fairness.
2. Find the wait and fairness for a 2100 player with the same window at peak and off-peak.
3. Propose one rule for the top band (expanding window, merged region, stakes reduction or honest waits). Put numbers on its cost using the model.
4. Trade proposals with another group. Name the player who is worst off under their rule and estimate how long that player waits.

Expected output: a four-line spec (window rule, top-band rule, wait target, fairness ceiling) plus the other group's "worst-off player" estimate.

## Common misconceptions

- **"A good matchmaker gives everyone fair matches and short queues."** Only if the pool is huge. For a fixed pool, wait multiplied by window is roughly constant, so fairness costs time. The shape of the curve is set by the population, not by code quality.
- **"The top player's long queue means the matchmaker is broken."** It means the density of opponents at that rating is tiny. At three standard deviations it is about 1% of the median's. The same code gives the same window to everyone and very different waits.
- **"Expanding windows solve the trade-off."** They pick a different point on it for each player. The median player barely notices. The top player trades fairness for time at the rate you set with `v`.
- **"Adding a mode only affects players who choose it."** It removes those players from the other pools. Every wait elsewhere grows by the share of `λ` that left.

## Check yourself

1. A queue has `σ = 250` instead of 200, and `λ = 12`. Using the shortcut, what is the median player's `W × w` constant? What window gives a 25-second mean wait?
2. A game merges two regions of equal size into one queue. The median player's window stays at 50. What happens to their wait and their fairness? What happens to the wait of a player at 2100?
3. A designer reports "mean queue time 14 seconds, target met". Name two numbers you would ask for before agreeing.
4. With a mean wait of 40 seconds, what share of queues last longer than 92 seconds?

<details>
<summary>Answers</summary>

1. `σ √(2π) ≈ 626.7`, so `p ≈ 2w / 626.7 = w / 313.3`, and `W × w ≈ 60 × 313.3 / 12 ≈ 1,567`. A 25-second wait needs `w ≈ 1567 / 25 ≈ 63`. A wider population spreads players thinner, so the same wait costs a wider window.
2. `λ` doubles, so the median wait halves, from 25.3 to about 12.7 seconds, and fairness is unchanged at 0.536. The 2100 player's wait also halves, from 2,081 to about 1,040 seconds. That is still 17 minutes, so merging helps but does not fix the top band on its own.
3. The wait by rating band (especially the top 1%), and a tail percentile such as the 90th, not the mean. A fairness number per band would be the third, since a short average wait can come from a wide window.
4. The 90th percentile is `2.30 × 40 = 92` seconds, so 10% of queues last longer. More generally, the share longer than `t` is `exp(−t / mean) = exp(−2.3) ≈ 0.10`.

</details>

## Lab hook

[Lab 10, queue-time vs fairness](../labs/lab10.md). You implement this lecture's model, then a second-by-second simulation where waiting players match each other with expanding windows. You compare the two, measure waits by rating band, and tune the window growth to meet a wait target and a fairness ceiling at peak and off-peak. The lab's matchmaker feeds the season simulation in [lab 11](../labs/lab11.md).

## Sources

- Microsoft Research, "TrueSkill Ranking System" project page (accessed September 2026). Match quality as rescaled draw probability, the effect of uncertainty on match quality, the stated conflict between waiting time and match quality, and the note that top players lack opponents of their level. Lists Halo 3 among the titles that used TrueSkill.
- Herbrich, R., Minka, T. & Graepel, T. (2006). "TrueSkill: A Bayesian Skill Rating System." *Advances in Neural Information Processing Systems 19*. The matchmaking section defines match quality from draw probability.
- Dota 2 Wiki, "Matchmaking" (current client, accessed September 2026). Selecting more modes and settings widens the search pool and shortens waits; Ranked Roles usually take longer; Role Queue games earned at 4 per all-roles search, up to 60 stored.
- Warcraft Wiki, "Dungeon Finder" (patch 3.3.0, 8 December 2009). Cross-realm grouping from all servers in the battlegroup, five-player groups of tank, healer and damage roles.
- Elo, A. (1978). *The Rating of Chessplayers, Past and Present*. Arco. The expected-score curve reused as the fairness measure.
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press. Background on PvP balance and matchmaking.

## Interactive spec: examples/w10-queue-fairness-curve.html

**The one insight.** The same matchmaking window gives very different waits to different players, because the density of opponents falls off like `exp(−z²/2)`. The trade-off curve for the median player is gentle. For a player three standard deviations up it sits about 90 times further right, and wide windows there produce lopsided matches because almost every opponent is below.

**Layout.** Two linked panels, side by side from 900px, stacked on mobile. A readout table below them.

**Left panel, "Who can you play?".** The normal density of ratings, `μ` and `σ` from the controls, x-axis from `μ − 4σ` to `μ + 4σ`. A vertical marker at the player's rating `r`. The interval `[r − w, r + w]` shaded under the curve. Label the shaded area with `p(r, w)` to four decimals.

**Right panel, "Wait vs fairness".** x-axis mean wait in seconds, log scale from 1 to 10,000. y-axis favourite's expected score, 0.5 to 0.9. Draw the trade-off curve for the current `r` by sweeping `w` from 10 to 600 in steps of 5. Draw the curve for the median player (`r = μ`) in a muted color as a reference. Mark the current `w` as a filled point on the current curve. Draw two dashed guide lines for the targets (defaults: 60-second 90th-percentile wait, shown as a vertical line at mean `60 / 2.3026 ≈ 26.1` s; fairness ceiling 0.60, horizontal).

**Controls.**
- Player rating `r`: 900 to 2300, step 10, default 2100.
- Window `w`: 10 to 600, step 5, default 50.
- Arrival rate `λ`: 1 to 60 per minute, step 1, default 12. Buttons "Peak (12)" and "Off-peak (3)".
- Population `σ`: 100 to 400, step 10, default 200. `μ` fixed at 1500.
- Toggle "Expanding window": when on, show inputs `w₀` (default 25), `v` (default 5 points/s), `w_max` (default 400), and plot the expanding-window result as a distinct marker (diamond) on the right panel.

**Formulas.**
- `Φ(z) = 0.5 × (1 + erf(z / √2))`; implement `erf` with an approximation accurate to about 1e-7 (Abramowitz and Stegun 7.1.26 is enough).
- `p(r, w) = Φ((r + w − μ)/σ) − Φ((r − w − μ)/σ)`.
- Mean wait `W = 60 / (λ × p)` seconds.
- Fairness: average of `1 / (1 + 10^(−|x − r|/400))` over `x` in `[r − w, r + w]`, weighted by `exp(−0.5((x − μ)/σ)²)`, midpoint rule with 2,000 steps.
- Expanding window: step `dt = 0.01` s up to 3,600 s. `alive` starts at 1. Each step: `w = min(w₀ + v t, w_max)`, `hazard = λ/60 × p(r, w)`, `m = alive × hazard × dt`, `wait += alive × dt`, `fav += m × fairness(r, w)` (fairness with 200 steps is fine here), `alive −= m`. Report `wait` and `fav / (1 − alive)`.

**Readout table.** For the current settings: `z`, `p`, mean wait, 90th-percentile wait (`2.3026 × W`), fairness, and the density ratio `exp(−z²/2)`. When expanding is on, add its mean wait and fairness.

**Test values (must match the lecture).** With `σ = 200`, `λ = 12`, fixed windows:
- `r = 1500, w = 50`: `p = 0.1974`, wait 25.3 s, fairness 0.536.
- `r = 1900, w = 100`: wait 82.5 s, fairness 0.575.
- `r = 2100, w = 50`: wait 2,081 s; `w = 400`: wait 31.5 s, fairness 0.835.
- Expanding (`w₀ = 25, v = 5, w_max = 400`): `r = 1500` gives 16.1 s and 0.571; `r = 2100` gives 81.6 s and 0.799.

**First screen.** `r = 2100`, `w = 50`, peak arrival rate. The current point sits far right of the muted median curve, with the readout showing a 2,081-second wait, so the insight is visible before any interaction.

**Accessibility.** All controls keyboard operable with visible labels and live numeric values. An `aria-live` region summarises the current point in one sentence ("Rating 2100, window 50: mean wait 34.7 minutes, favourite wins 53.7%"). No animation when `prefers-reduced-motion` is set.
