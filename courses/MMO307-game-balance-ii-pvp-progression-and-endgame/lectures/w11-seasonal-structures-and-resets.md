# MMO307 · Week 11 — Seasonal Structures and Resets

**Why this matters:** A season gives a competitive game a start, a finish and a reason to play again. The reset that opens each season also throws away information your matchmaker needs, and for the first weeks your best and worst players land in each other's matches. How much you reset decides how long that chaos lasts.

**You will be able to:**
- Compute how many games a soft rating reset takes to wash out, for any compression factor and K-factor, and check the answer by simulation.
- Separate the two things a ladder does, measuring skill and rewarding effort, and design a reset that treats them differently.
- Estimate the share of a season players spend misplaced, and use it to choose a season length and a reset strength.
- Critique shipped season designs (Hearthstone, Diablo III, FIDE chess) in terms of what they reset and what they keep.

**Before class:** Elo (1978), *The Rating of Chessplayers*, the chapter on rating development over time. Glickman, "The Glicko System" (1995 note), the section on rating deviation growing between rating periods. Skim FIDE's Rating Regulations (effective 1 March 2024), section 8 on K-factors.

**Prerequisites from earlier courses:** [MMO307 week 8, Elo and expected score](w08-elo-and-expected-score.md), especially section 4 on the time constant `τ`, and [week 9, Glicko and TrueSkill](w09-glicko-and-trueskill.md), on rating deviation. [MMO307 week 10, matchmaking quality vs queue time](w10-matchmaking-quality-vs-queue-time.md), because a misplaced player is a fairness problem for every opponent. [MMO307 week 4, gear treadmills and item level](w04-gear-treadmills-and-item-level.md), which covers what a season does to gear. [MA102 week 11, Monte Carlo simulation](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w11-monte-carlo-simulation.md). [MA101 week 5, logarithms](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w05-logarithms-how-many-levels-until.md), for solving `x^n = y` for `n`.

**Interactive:** [`examples/w11-soft-reset.html`](../examples/w11-soft-reset.html). Keep it open during section 2.

---

## 1. What a season resets

A **season** is a fixed stretch of time, usually two to six months, that ends with a reset and a set of rewards. Players come back at the start because the ladder is open again. They play through the end because rewards depend on where they finish.

"Reset" hides at least four different decisions. Keep them apart, because a game can reset one and keep the others.

- **Visible rank.** The badge, division or number the player sees and shows off.
- **Hidden rating.** The number the matchmaker uses, often called MMR (matchmaking rating). It may be the same as visible rank or entirely separate.
- **Characters and economy.** Some games start seasonal players from level 1 with an empty stash and a fresh market.
- **Gear.** A new tier of items makes the old tier obsolete. Week 4 covered this under the treadmill, so this week leaves gear aside.

A reset has benefits. It creates a fresh race with a clear finish line. It lets new players compete for top places without facing veterans' years of accumulated advantage. It removes stale ratings of players who quit. And it gives a natural date for balance changes and new content.

A reset also has costs. Every reset of the hidden rating makes the matchmaker's information worse. A player who was correctly placed yesterday is misplaced today, and every match they play until they settle is less fair for someone. The question for this week is how to price that cost.

## 2. Worked example: how long does a soft reset take to wash out?

### The hook

Hearthstone's ranked mode, since its April 2020 overhaul, resets every player's visible rank to Bronze 10 at the start of each season, legends included. That sounds drastic. Yet the matchmaking rating is not reset. It carries over, and it decides a **Star Bonus**, a multiplier on stars earned per win. Every player starts with at least 2, and the best players start with up to 11. A legend can be back in Diamond in an evening.

So Hearthstone wipes the number players see and keeps the number the game uses. Why go to that trouble? Why not reset the hidden rating too, or keep the visible rank? The answer comes from asking what a rating reset costs in games played.

### The model

Most rating resets are **soft resets**. Each player's rating is pulled part of the way toward the population mean `μ`:

```
r_new = μ + α × (r_old − μ)
```

`α` is the **compression factor**, between 0 and 1. With `α = 0` everyone starts at the mean, which is a hard reset. With `α = 1` nothing changes. With `α = 0.5` a player 600 points above the mean restarts 300 above it.

Suppose the old rating was accurate. Call the player's true skill `s`. After the reset, the player's **rating error** is how far the shown rating sits from the truth:

```
e₀ = s − r_new = (1 − α) × (s − μ)
```

Now the player plays. Week 8, section 4, already did the hard part. When the matchmaker pairs a player with accurately rated opponents at their shown rating, the gap between rating and truth closes by a fixed share `K·g` each game, where `g = ln 10 / 1600 ≈ 0.00144` is the slope of the Elo curve at a gap of zero. Week 8 turned that into a **time constant**:

```
τ = 1 / (K·g)          (about 21.7 games at K = 32)
games to close a gap from e₀ to ε  ≈  τ × ln(e₀ / ε)
```

This week adds one step. The reset sets `e₀`, so the reset decides how many time constants every player spends climbing back. With `K = 32`, one half-life is `τ × ln 2 ≈ 15` games. With `K = 64` it is 7.5.

We use a tolerance `ε = 25` rating points. A 25-point error shifts the Elo expected score by about 0.036, well inside the fairness a matchmaker can deliver anyway (week 10). One caution from week 8. The formula tracks the *average* error, the bias. Even a settled player at `K = 32` wobbles around their true rating with a standard deviation of about 53 points. A reset adds a bias on top of that wobble, and the bias is what we measure here.

### Numbers you can check

Take a player whose true rating is 2100, three standard deviations above a mean of 1500. This script evaluates the model for four compression factors.

```python
from math import log

g = log(10) / 1600            # slope of the Elo curve at a gap of zero (week 8)

def games_to_settle(error, k, eps=25):
    """Week 8's rule: about tau x ln(error / eps) games, with tau = 1 / (K g)."""
    tau = 1 / (k * g)
    return tau * log(error / eps)

for alpha in (0.0, 0.5, 0.8, 0.9):
    error = (1 - alpha) * (2100 - 1500)
    print(f"alpha {alpha}: error {error:3.0f}  "
          f"K=32 {games_to_settle(error, 32):4.1f}  K=64 {games_to_settle(error, 64):4.1f}")
```

```
alpha 0.0: error 600  K=32 69.0  K=64 34.5
alpha 0.5: error 300  K=32 54.0  K=64 27.0
alpha 0.8: error 120  K=32 34.1  K=64 17.0
alpha 0.9: error  60  K=32 19.0  K=64  9.5
```

The straight-line model is a shortcut. At large errors the Elo curve bends, so the real pull toward the truth is weaker than the straight line says. Check the model with a Monte Carlo simulation (MA102 week 11). Three thousand simulated players each start with the given error and play accurately rated opponents at their shown rating.

```python
import random

def expected(a, b):
    return 1 / (1 + 10 ** ((b - a) / 400))

def games_to_settle_sim(error, k, tolerance=25, players=3000, max_games=200):
    """Average over many players of true rating 2100 who start `error` too low.
    Each game is against an accurately rated opponent at the player's shown rating."""
    totals = [0.0] * (max_games + 1)
    for seed in range(players):
        rng = random.Random(seed)
        true, shown = 2100, 2100 - error
        for game in range(1, max_games + 1):
            win = rng.random() < expected(true, shown)
            shown += k * (win - 0.5)          # the opponent is rated `shown`, so E = 0.5
            totals[game] += true - shown
    return next(g for g in range(1, max_games + 1) if totals[g] / players < tolerance)

for error in (600, 300, 120, 60):
    print(f"error {error:3d}: K=32 {games_to_settle_sim(error, 32)}  "
          f"K=64 {games_to_settle_sim(error, 64)}")
```

```
error 600: K=32 78  K=64 40
error 300: K=32 56  K=64 29
error 120: K=32 35  K=64 18
error  60: K=32 19  K=64 10
```

Put the two side by side.

| Reset | `α` | Starting error | Games to within 25, K = 32 (model / sim) | K = 64 (model / sim) |
|---|---|---|---|---|
| Hard | 0.0 | 600 | 69.0 / 78 | 34.5 / 40 |
| Half | 0.5 | 300 | 54.0 / 56 | 27.0 / 29 |
| Light | 0.8 | 120 | 34.1 / 35 | 17.0 / 18 |
| Very light | 0.9 | 60 | 19.0 / 19 | 9.5 / 10 |

The model is within two games for small errors and optimistic by about 12% for a hard reset. It gets the shape right, and the shape carries three lessons.

1. **Halving the reset does not halve the recovery.** Going from a hard reset to `α = 0.5` halves the starting error but saves only about 15 games in the model and 22 in the simulation at `K = 32`. Recovery time depends on the *logarithm* of the error. Each halving of the error saves one half-life, about 15 games, no matter where you start.
2. **K is the lever that scales everything.** Doubling `K` roughly halves every recovery. That is why many systems use a higher K for new or recently reset players, the provisional period week 8 discussed.
3. **Even a light reset costs games.** A 10% compression still takes the top player about 19 games to recover. If they play 40 games a season, half their season is spent climbing back to where they started.

### The cost to everyone else

A misplaced player is also a fairness problem for their opponents. Using week 10's measure, a player whose rating is 100 points too low beats their "equal" opponents with expected score 0.64, not 0.50. With week 8's rule, the number of games a player spends more than 100 points off is:

```
n(100) ≈ τ × ln(e₀ / 100)
```

At `K = 32` this is 39 games after a hard reset, 24 games after `α = 0.5`, and 4 games after `α = 0.8`. Every one of those games is a lopsided match for someone who did nothing wrong. Multiply by the share of your population far from the mean and you have the size of the "early-season stomp" complaint before it happens.

### A visual you can move

Open the interactive. The left panel shows two rating distributions. The wide one is true skill. The narrow one is shown rating after a reset with compression `α`. Drag `α` toward 0 and the shown distribution collapses onto the mean. The right panel plots the average error against games played for players at 1700, 1900 and 2100, with simulated points on top of the model's curves. The dashed line is the 25-point tolerance `ε`.

Drag `α` from 0.5 to 0 and watch the 2100 curve start twice as high but cross the tolerance only about 15 games later in the model. Now drag `K` from 32 to 64. Every curve squeezes to half its length. The picture makes the logarithm visible. The reset sets the starting height, and `K` sets how fast every curve falls.

### Cross-game recognition

**Hearthstone (ranked, patch 17.0 of March 2020 onward).** Visible rank resets hard, to Bronze 10 for everyone. Hidden MMR is not reset at all, so in our model `α = 1` for the matchmaker and the rating error is zero. The matchmaker keeps working perfectly on day one. The visible rank is handled like a reward track, and the Star Bonus is a K-factor on that track. A player with a bonus of 11 climbs 11 times faster than the base rate. Section 3 shows why the bonus is necessary for this design to work at all.

**Diablo III seasons (patch 2.1.0, August 2014 onward).** Diablo III resets characters and the economy. Seasonal characters start at level 1 with a separate stash, gold, artisans and Paragon experience. When the season ends, their progress rolls into the non-seasonal pool, and they become normal characters. In our terms the "rating" being reset is accumulated power, not skill. The reset is hard (`α = 0` for power) and it is voluntary. Nobody is forced into a season. The game sidesteps the misplacement problem by keeping the old world open for players who do not want the race.

**FIDE chess ratings (rating regulations effective March 2024).** The system Elo designed for chess has no seasons at all. FIDE publishes a new list on the first day of every month by applying each period's rated games to the previous list. In our terms `α = 1` forever, so the matchmaker's information is never thrown away. What chess does have is a high K for newcomers (40 for the first 30 games) and a low K for established top players (10 once they have reached 2400). Chess spends its K budget where error is likely, not on a calendar.

Three designs, one question. What is compressed, by how much, and what K governs the recovery? Hearthstone resets the reward and keeps the measurement. Diablo III resets power in a separate, optional world. Chess resets nothing and uses K to handle new players. None of them compresses the matchmaking rating in a way that makes early-season matches unfair. That tells you something.

### Eyes-open design judgment

- **Reset the reward, not the measurement, when you can.** If the purpose of the reset is a fresh race, reset a visible track and keep the hidden rating. You get the race without paying the misplacement cost.
- **If you must compress the hidden rating, raise K or uncertainty with it.** A soft reset with the old K wastes dozens of games per player. A reset that also raises each player's rating deviation (the Glicko approach of week 9) makes early games move ratings fast and settles players quickly.
- **Price the reset in games, then in weeks.** Divide recovery games by games per week for a typical player at each band. A reset that costs a casual player half their season is a design choice. Make it on purpose.
- **Hard resets suit power, not skill.** Resetting accumulated power (Diablo III) gives newcomers a fair race. Resetting a skill estimate to zero only produces mismatches, because skill did not reset.

### Check this example

1. With `K = 24`, what share of the error does one game remove? What are `τ` and the half-life in games?
2. A player 400 points above the mean suffers a reset with `α = 0.75`. How many games at `K = 32` until the model says they are within 25 points?

<details>
<summary>Answers</summary>

1. `K·g = 24 × 0.00144 ≈ 0.0345`, so about 3.5% per game. `τ = 1 / 0.0345 ≈ 29.0` games, and the half-life is `29.0 × ln 2 ≈ 20.1` games.
2. `e₀ = 0.25 × 400 = 100`. `n ≈ 21.7 × ln(100 / 25) = 21.7 × 1.386 ≈ 30.1` games.

</details>

## 3. Two tracks: the ladder you see and the rating you don't

Hearthstone's split is worth modelling on its own, because it contains a trap.

Once the matchmaker pairs you by hidden rating, your expected win rate is 50%. Suppose the visible ladder gives one star per win and takes one per loss. Then your expected progress per game is zero. You would drift up and down on a random walk and take thousands of games to climb. A visible reset without a matching fix makes the ladder unclimbable for exactly the players whose rating is accurate.

The fix is a bonus. Let a win give `b` stars and a loss cost 1. At a 50% win rate:

```
expected stars per game = 0.5 × b − 0.5 × 1 = (b − 1) / 2
```

Take an invented ladder of 150 stars from bottom to top.

| Stars per win `b` | Stars per game at 50% | Games to climb 150 stars |
|---|---|---|
| 1 | 0 | random walk, thousands |
| 2 | 0.5 | 300 |
| 4 | 1.5 | 100 |
| 11 | 5 | 30 |

The bonus is a K-factor for the visible track. Giving each player a bonus tied to their hidden rating makes the visible rank converge to where the hidden rating already is, at a speed the designer chooses. The reset creates a race, and the bonus decides how long the race lasts. That is why Hearthstone ties the Star Bonus to last season's rating. It also lowers the bonus by 1 each time the player reaches a rank floor (every 5 ranks), so the bonus fades as the visible rank approaches the hidden one, which is the same job a falling K does. A strong player who plays 30 games is back near the top, and a newer player can still climb past their old rank.

The trap has a second version. If visible rank is also used for rewards and the bonus runs out before a player reaches their true level, the season ends with players stuck below where they belong. The design has to guarantee that a typical player at each rating finishes their climb within a typical number of games.

## 4. Choosing a season length and reset strength

Put the numbers together into one planning metric, the **misplaced share of the season**:

```
misplaced share = games to settle / games played per season
```

Suppose the typical player plays 200 ranked games per season and your system uses `K = 32`.

| Reset | Games to settle (top player, simulated) | Misplaced share at 200 games | At 60 games |
|---|---|---|---|
| Hard, `α = 0` | 78 | 39% | more than the whole season |
| `α = 0.5` | 56 | 28% | 93% |
| `α = 0.8` | 35 | 18% | 58% |
| Visible only, hidden kept | 0 | 0% | 0% |

The last column is the uncomfortable one. A casual player who plays 60 games a season never settles under any meaningful hidden-rating reset. For them, every season is a season of mismatches.

Other pressures push the other way.

- **Stale ratings.** Players who stop playing keep their rating, so the top of the ladder fills with inactive names. A season end clears the visible ladder without touching the measurement. Many games add **decay** instead, a slow loss of visible rank for inactive players.
- **Rating drift.** In Elo, points only move between players. If players leave with more points than they started with, the total shrinks and the whole scale drifts down over time. If new players arrive above their true skill, it drifts up. A soft reset re-centres the scale each season. It is a blunt tool for this job, and it is often the stated reason for compressing hidden ratings.
- **Balance patches.** A big patch changes what "skill" means in a class-based game. A player whose class was weakened has a rating that is now too high. A light soft reset at the patch helps the matchmaker adapt. Raising rating deviation (week 9) does the same thing more precisely.

The season length itself is a pacing decision. Short seasons (one month in Hearthstone's case) make each race short and frequent. Long seasons give the ladder time to settle and make the finishing position mean more. The rule of thumb from the table: choose `α` and `K` so that the misplaced share for your median player is under about a quarter of their season. Where it cannot be, move the reset to a visible track.

## In-class activity (25 minutes)

Pairs. You are designing season rules for an arena PvP mode with `μ = 1500` and a population standard deviation of 200. Players are matched by hidden rating with `K = 32`. Casual players play 50 games per season, committed players 250.

1. Pick a compression factor `α` for the hidden rating (including `α = 1`). Use the interactive to find how many games a player at 1900 needs to settle.
2. Compute the misplaced share for a casual and a committed player at 1900.
3. Design the visible track. Choose the bonus rule (stars per win as a function of hidden rating) so that a casual player at 1900 reaches their deserved visible rank within their 50 games. Use the table in section 3.
4. Swap with another pair. Find the player who is worst served by their rules. Name them in one sentence with numbers.

Expected output: a five-line season spec (hidden reset, K rule, visible reset, bonus rule, season length) and the other pair's worst-served player.

## Common misconceptions

- **"A soft reset of half the distance takes half as long to settle."** Recovery depends on the logarithm of the error. Halving the starting error saves one half-life, about 15 games at `K = 32`, not half the games.
- **"Resetting everyone to the same rating is the fairest start."** It is fair in rules and unfair in matches. Skill did not reset, so the matchmaker spends dozens of games per player producing lopsided games.
- **"If ranks reset, the matchmaker must reset too."** Visible rank and matchmaking rating can be separate numbers. Resetting only the visible one gives the race without the mismatches, provided the climb has a bonus.
- **"Higher K is always better after a reset."** It settles players faster but makes their ratings noisier afterward, because every game moves them further. Raise K for recently reset or new players and lower it again once they settle.

## Check yourself

1. Your system uses `K = 20` and a soft reset with `α = 0.6`. A player's true rating is 1,300 with a mean of 1,500. What is their starting error, in which direction, and how many games does the linear model predict before they are within 25 points?
2. A designer proposes resetting visible rank to the bottom each month while matching by hidden rating, with 1 star per win and 1 per loss. Predict what an accurately rated player experiences over 100 games.
3. A game resets hidden ratings with `α = 0.5` and `K = 32`. Its median committed player plays 120 games per season. Using the simulated values, what is the misplaced share for a player at 2100? Propose one change that halves it, and check your change with the model.

<details>
<summary>Answers</summary>

1. `r_new = 1500 + 0.6 × (1300 − 1500) = 1380`, so the player is shown 80 points too high (`e₀ = −80`). The model is symmetric, so use `|e₀| = 80`. `τ = 1 / (20 × 0.00144) ≈ 34.7` games, and `n ≈ 34.7 × ln(80 / 25) ≈ 34.7 × 1.163 ≈ 40.4` games.
2. At a 50% win rate the expected stars per game is `(1 − 1)/2 = 0`. Their visible rank does a random walk. After 100 games its standard deviation is about `√100 = 10` stars, so a typical player ends within about 10 stars of the bottom. The ladder is unclimbable for accurate players.
3. 56 / 120 ≈ 47%. Doubling K to 64 gives 29 simulated games, 24%. Or keep K and lighten the reset to `α = 0.9`: 19 games, 16%. Or keep the hidden rating and reset only the visible rank: 0%.

</details>

## Lab hook

[Lab 11, season simulation](../labs/lab11.md). You simulate a full population through a season end with a soft reset, using an Elo matchmaker. You measure average rating error and the share of lopsided matches game by game, compare hard, soft and visible-only resets, and propose a reset rule with numbers. It reuses the matching idea from [lab 10](../labs/lab10.md) and feeds the final season design project.

## Sources

- Hearthstone Wiki, "Ranked" (current rules, from patch 17.0.0.44222 of 26 March 2020, live 1 April 2020). All players reset to Bronze 10 at the end of each season; MMR carries over and sets the Star Bonus; every player starts a season with at least 2 Star Bonus, up to 11 for high Legend; the bonus drops by 1 at each rank floor; seasons last one month. https://hearthstone.wiki.gg/wiki/Ranked
- Diablo Wiki, "Season" (Diablo III, patch 2.1.0, August 2014 onward). Seasonal characters start fresh with separate stash, gold, artisans and Paragon experience; at season end their progress rolls into the non-seasonal roster.
- FIDE, *Rating Regulations* (effective 1 March 2024), sections 7.1 and 8.3. Monthly lists built from the previous list; K = 40 for a player's first 30 games (and for juniors under 2300), K = 20 below 2400, K = 10 once 2400 is reached. https://handbook.fide.com/chapter/B022024
- Elo, A. (1978). *The Rating of Chessplayers, Past and Present*. Arco. The update rule and expected-score curve.
- Glickman, M. (1995). "The Glicko System." Boston University. Rating deviation that grows during inactivity, the principled alternative to compressing ratings.

## Interactive spec: examples/w11-soft-reset.html

**The one insight.** A soft reset sets how far each player starts from the truth, and K sets how fast every player falls back. Because recovery takes about `τ × ln(e₀ / ε)` games, halving the reset saves only one half-life, while doubling K halves every recovery.

**Layout.** Two linked panels, side by side from 900px, stacked on mobile. Readout table below.

**Left panel, "Shown vs true".** Two normal curves on one axis from 700 to 2300. True skill `N(1500, 200)` in a muted color. Shown rating after reset `N(1500, α × 200)` in the accent color. Vertical markers at 1700, 1900 and 2100 on the true curve, each with an arrow to its reset position `1500 + α × (s − 1500)`.

**Right panel, "Error vs games played".** x-axis games 0 to 120. y-axis average error in rating points, 0 to 620. For each of the three players (1700, 1900, 2100), draw the model curve `e₀ × exp(−n / τ)` as a line and the simulated average error as dots every 5 games. Dashed horizontal line at the tolerance `ε`. Mark where each simulated series first drops below `ε`.

**Controls.**
- Compression `α`: 0 to 1, step 0.05, default 0.5.
- K: 8 to 64, step 4, default 32.
- Provisional games: 0 to 30, step 5, default 0. During the first N games after the reset, K is doubled.
- Tolerance `ε`: 10 to 100, step 5, default 25.
- Games per season: 20 to 400, step 10, default 200 (used in the readout only).
- Button "Re-run simulation" with a seed field (default 10; seed 10 gives the 56 games and 28% below, seed 1 gives 58 games and 29%).

**Formulas.**
- `g = ln(10) / 1600`, `τ = 1 / (K·g)`.
- Model curve: `e_n = e₀ × exp(−n / τ)`, with `e₀ = (1 − α)(s − 1500)`. With provisional games N, use `τ/2` for `n ≤ N` and `τ` after.
- Model games to settle: `τ × ln(e₀ / ε)` (piecewise with provisional games).
- Simulation: 2,000 players per curve (fewer is fine on low-end devices, but at least 500). Each player starts at `shown = s − e₀`. Each game: win with probability `1 / (1 + 10^((shown − s)/400))`; `shown += K × (win − 0.5)`. Average `s − shown` across players after each game. Use a seeded PRNG (mulberry32) so results are reproducible.

**Readout table.** One row per player: `e₀`, model games to settle, simulated games to settle, games spent more than 100 points off (model), misplaced share of the season.

**Test values (must match the lecture, `s = 2100`).** Model, `K = 32`: `α = 0` gives 69.0, `α = 0.5` gives 54.0, `α = 0.8` gives 34.1, `α = 0.9` gives 19.0. `K = 64`: 34.5, 27.0, 17.0, 9.5. Simulated values should land within ±3 games of 78, 56, 35, 19 (K = 32) and 40, 29, 18, 10 (K = 64); exact values depend on the PRNG. `τ` at `K = 32` reads 21.7 games and the half-life 15.1 games.

**First screen.** `α = 0.5`, `K = 32`, all three curves drawn, the 2100 readout showing 54.0 model and about 56 simulated games, misplaced share 28%.

**Accessibility.** All controls keyboard operable with labels and live values. An `aria-live` sentence summarises the 2100 player ("Starts 300 points low, settles in about 56 games, 28% of a 200-game season"). No animation under `prefers-reduced-motion`.
