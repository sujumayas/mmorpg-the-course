# MMO307 · Week 08 — Elo and Expected Score

**Why this matters:** Every ranked ladder you ship will be judged by one question from players, "did I deserve that?" Elo is the simplest rating system that answers it with a rule players can check. Its one tuning constant, K, decides how fast new players find their level and how much their rating shakes once they get there, and you cannot have both.

**You will be able to:**
- Compute an Elo update by hand, and explain why beating a weak opponent is worth almost nothing.
- Prove that a correctly rated player's expected rating change is zero, and use that to spot a rating that is wrong.
- Derive the speed and noise of an Elo ladder from K, and choose K for a stated goal.
- Critique rule changes to Elo (unequal K, rating floors, gap caps, team averages) by the points they add to or remove from the pool.

**Before class:** Elo, *The Rating of Chessplayers, Past and Present* (1978), chapter 1 on the rating scale and chapter 8 on the development coefficient (K). FIDE Rating Regulations, section 8.3 (K factors and the 400-point rule). Glickman, "The Glicko System", pages 1 and 2 only, for the problem next week solves.

**Prerequisites from earlier courses:** [MA101 week 5, logarithms](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w05-logarithms-how-many-levels-until.md) derives the expected-score curve as log-odds, where each 400 points multiplies the odds by 10. [GD101 week 10, chance vs skill](../../GD101-introduction-to-game-design/lectures/w10-chance-vs-skill-and-randomness.md) reads the 400 as the size of the random swing. [MA102 week 4, expected value](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md) and [MA102 week 13, sampling](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md) give the tools for section 4. This course: [week 7](w07-pvp-vs-pve-split-tuning.md) balanced classes so that the player, not the class, should decide the match.

**Interactive:** [`examples/w08-elo-expected-score.html`](../examples/w08-elo-expected-score.html). Keep it open during sections 2 and 4.

---

## 1. What a rating is for

Two earlier lectures gave you the expected-score curve. For two players with ratings `R_A` and `R_B`,

```
E_A = 1 / (1 + 10^((R_B − R_A) / 400))
```

`E_A` is A's **expected score**, the average points per game A should take, where a win is 1, a draw ½ and a loss 0. In a game without draws it is A's win probability. MA101 week 5 showed that the rating gap is 400 times the base-10 logarithm of the odds. GD101 week 10 showed that 400 plays the role of the die in "skill plus a die". We will not re-derive either. This week asks the next question. Where do the ratings come from?

A rating is a number whose differences predict results. Nothing more. A rating of 1,800 means nothing alone. It means something only against another rating, through the curve above. Two consequences follow, and a designer should keep both in mind.

- **Only gaps matter.** Add 1,000 to every player's rating and every prediction stays the same. The starting value (1,500, 1,200, 0) is a presentation choice.
- **A rating is an estimate.** A player has some true strength you cannot see. The rating is your best current guess, built from results. Every rule in this lecture is a rule for moving that guess toward the truth.

## 2. Worked example: points at stake

### The hook

Under the US Chess Federation's version of Elo, as Glickman describes it, two players rated 1,700 play and the winner gains 16 points while the loser drops 16. Now let a 2,300 player beat a 1,500 player. The winner gains about a third of a point. If the 2,300 player loses instead, they drop almost 32. Players describe this as "the system punishes you for playing weaker opponents". It doesn't. It charges exactly what the result was worth, and seeing why is the whole of Elo.

### The model

After a game, each player's rating moves by K times the surprise:

```
R_A' = R_A + K × (S_A − E_A)
```

- `S_A` is A's actual score, 1, ½ or 0.
- `E_A` is A's expected score from the curve.
- `K` is the **development coefficient**, the most points one game can move a rating.

The term `S_A − E_A` is the **surprise**. Win a game you were expected to win 99% of the time and the surprise is 0.01. Lose it and the surprise is −0.99. If both players use the same K, B's change is exactly minus A's change, because `E_B = 1 − E_A` and `S_B = 1 − S_A`. Points move from one player to the other, and the total in the pool stays constant. That is called **zero-sum**.

### Numbers you can check

With `K = 32`, the favourite's win gain is `32 × (1 − E)` and loss is `32 × E`:

| Rating gap | Favourite's `E` | Win: favourite gains | Loss: favourite loses |
|---|---|---|---|
| 0 | 0.500 | 16.0 | 16.0 |
| 100 | 0.640 | 11.5 | 20.5 |
| 200 | 0.760 | 7.7 | 24.3 |
| 300 | 0.849 | 4.8 | 27.2 |
| 400 | 0.909 | 2.9 | 29.1 |
| 500 | 0.947 | 1.7 | 30.3 |
| 600 | 0.969 | 1.0 | 31.0 |
| 700 | 0.983 | 0.6 | 31.4 |
| 800 | 0.990 | 0.3 | 31.7 |

The two right columns always add to K. That is the zero-sum rule again, seen from one player. Code that prints this table:

```python
def expected(r_a, r_b):
    return 1 / (1 + 10 ** ((r_b - r_a) / 400))

def update(r_a, r_b, score_a, k=32):
    delta = k * (score_a - expected(r_a, r_b))
    return r_a + delta, r_b - delta

for gap in range(0, 801, 100):
    e = expected(1500 + gap, 1500)
    print(f"gap {gap:3}  E = {e:.3f}  win +{32 * (1 - e):4.1f}  loss -{32 * e:4.1f}")
```

```
gap   0  E = 0.500  win +16.0  loss -16.0
gap 100  E = 0.640  win +11.5  loss -20.5
gap 200  E = 0.760  win + 7.7  loss -24.3
gap 300  E = 0.849  win + 4.8  loss -27.2
gap 400  E = 0.909  win + 2.9  loss -29.1
gap 500  E = 0.947  win + 1.7  loss -30.3
gap 600  E = 0.969  win + 1.0  loss -31.0
gap 700  E = 0.983  win + 0.6  loss -31.4
gap 800  E = 0.990  win + 0.3  loss -31.7
```

### Why the trade is fair: the expected change is zero

Here is the property that makes the asymmetric table fair. Suppose the favourite's true chance of winning is `p`. Their average change per game is

```
average change = p × K(1 − E) + (1 − p) × K(0 − E) = K × (p − E)
```

If the rating is right, `p = E`, and the average change is exactly zero. At an 800-point gap, the favourite gains 0.3 points 99 times and loses 31.7 once, and `99 × 0.3 ≈ 1 × 31.7`. Playing weak opponents neither helps nor hurts a correctly rated player on average. It only adds noise.

Turn the property around and you get a diagnostic. **If a player's rating keeps rising, their true `p` is above their `E`, so their rating is too low.** The drift `K × (p − E)` is the system correcting itself, and its size tells you how wrong the rating is. A new player who wins 70% of even-rated games is about 147 points underrated, because `E = 0.7` at a 147-point gap.

### The visual

Open [`examples/w08-elo-expected-score.html`](../examples/w08-elo-expected-score.html). The left view is the expected-score curve with a slider for the rating gap from 0 to 800. The right view shows the same gap as two bars, what the favourite wins if they win and loses if they lose, with K adjustable. Drag the gap up. The curve flattens toward 1 while the bars swap sizes, the win bar shrinking to a sliver and the loss bar growing to nearly K. Now switch on "true skill" and set a true gap different from the rating gap. A third readout shows the average change per game, `K(p − E)`. It is zero only when the two gaps match. Watching it change sign as you cross the true gap is the insight.

### Cross-game recognition

**Chess, FIDE (regulations effective March 1, 2024).** FIDE uses three values of K. It is 40 for a new player until they complete events with at least 30 games, and for players under 18 rated below 2,300. It is 20 for everyone else below 2,400, and 10 once a player has reached 2,400. FIDE also limits the gap that enters the formula. From October 1, 2025, a difference of more than 400 points counts as 400 for players rated below 2,650. Rewritten in our form, FIDE is our model with K chosen by a player's history, and with `E` capped at 0.909.

**League of Legends (Seasons 1 and 2, to 2013).** Ranked play used an Elo rating that players could see, until the League system of tiers and League Points replaced it in Season 3 (2013). For five-player teams, per the League of Legends Wiki, each team got a team Elo built from its members' ratings, and every player on the winning team gained while every player on the losing team lost. Rewritten in our form, `R_A` and `R_B` are team ratings and every member takes the same `K(S − E)`. Riot's exact formulas were never published, so treat this as structure, not constants.

**World of Warcraft arenas (before patch 5.4.0).** Arena teams had two numbers, a visible team rating and a hidden matchmaking rating (MMR). Per Warcraft Wiki, the rating change after a match depended on the difference between the two teams' MMRs. Beating a higher-MMR team paid more, and losing to a weaker team cost more. That is `K(S − E)` again, with `E` computed from a hidden number while the reward was paid into a visible one. Section 5 comes back to that split.

Three games and one rule. When you see any ladder that pays more for upsets, look for the surprise term `S − E` and ask what K is and what feeds `E`.

### Design judgment, eyes open

- **Elo is transparent.** A player can compute their own update. That matters for trust, and it is the main reason to prefer it over opaque systems for a visible ladder.
- **It is zero-sum only if K is shared.** Section 5 shows what unequal K does to the pool.
- **It assumes one number describes a player.** Rock-paper-scissors matchups (MMO303 week 9) break that, because A beats B and B beats C doesn't make A beat C. Elo will average over them silently.
- **It does not know how sure it is.** A returning player and a daily player at the same rating get the same K. That is next week's problem.

## 3. Reading `E` as a prediction you can test

A rating system makes a prediction before every game, so you can grade it. Group games by the predicted `E`, say every game where the favourite's `E` was between 0.70 and 0.80, and count how often the favourite actually won. If the system is **calibrated**, the favourites in that bucket win about 75% of the time. MA102 week 13 gives you the margin of error for that count. With 400 games in the bucket, a 95% interval is about ±4 percentage points.

Calibration catches two common problems.

- **A scale that is too narrow or too wide.** If favourites at `E = 0.9` win only 80% of the time, your 400 is too small for this game. There is more randomness per game than chess has. The fix is a larger scale constant, which is like GD101's bigger die.
- **Structural bias.** If favourites always overperform in one map, faction or class pairing, the rating is absorbing something that is not player skill. [Week 14](w14-measuring-balance-with-win-rates-and-pick-rates.md) of this course measures that with win rates.

Calibration is also the honest answer to a player who says "the system is rigged." Show them the bucket table.

## 4. Choosing K: speed against noise

K is a trade. Large K moves ratings fast, so new players reach their level in few games. It also moves them fast when nothing has changed, so an established player's rating bounces around their true level. You can compute both effects.

### The model

Consider one player whose true strength is `T` and whose rating is `R`. Matchmaking pairs them with accurately rated opponents at their current rating, so every game has `E = 0.5`, and the player's true win chance is `p = E(T − R)` from the curve.

Near `R = T`, the curve is almost a straight line with slope

```
g = ln(10) / 1600 ≈ 0.00144 per rating point
```

(the slope of `1 / (1 + 10^(−x/400))` at `x = 0`). So a player `x` points underrated wins about `0.5 + g·x` of their games, and their average gain per game is `K·g·x`. The gap closes by a fixed fraction `K·g` each game. That gives two numbers:

```
time constant   τ = 1 / (K·g)            games to close about 63% of a gap
steady noise    σ = sqrt(K / (8·g))      rating standard deviation once settled
```

The first follows from the gap shrinking by `K·g` per game. The second comes from balancing that pull against the random step `±K/2` each game. The step has variance `K²/4`, the pull removes a fraction `2·K·g` of the variance per game, and at balance `σ² = K/(8g)`. To close a gap from `G_0` to `G`, you need about `τ × ln(G_0 / G)` games. From 300 points down to 30 takes `τ × ln 10 ≈ 2.3 τ` games.

### Numbers you can check

A simulation of a player with true strength 1,800 who starts at 1,500, repeated 200 times for each K:

```python
import math, random

def expected(r_a, r_b):
    return 1 / (1 + 10 ** ((r_b - r_a) / 400))

def climb(k, true=1800, start=1500, games=400, seed=7):
    """One player, always matched against an accurately rated opponent at
    the player's current rating. Returns the rating after each game."""
    rng = random.Random(seed)
    r, history = start, []
    for _ in range(games):
        p_win = expected(true, r)          # truth decides the result
        s = 1 if rng.random() < p_win else 0
        r += k * (s - 0.5)                 # rating says the match is even
        history.append(r)
    return history

g = math.log(10) / 1600
for k in (10, 20, 32, 40):
    runs = [climb(k, seed=s) for s in range(200)]
    # games until the average run is within 30 points of the truth
    avg = [sum(run[i] for run in runs) / len(runs) for i in range(400)]
    reach = next(i + 1 for i, r in enumerate(avg) if r >= 1770)
    tail = [run[i] for run in runs for i in range(300, 400)]
    mean = sum(tail) / len(tail)
    sd = (sum((x - mean) ** 2 for x in tail) / len(tail)) ** 0.5
    print(f"K={k:2}  tau={1/(k*g):5.1f} games  reach={reach:3}  "
          f"predicted sd={math.sqrt(k / (8 * g)):4.1f}  simulated sd={sd:4.1f}")
```

```
K=10  tau= 69.5 games  reach=165  predicted sd=29.5  simulated sd=28.7
K=20  tau= 34.7 games  reach= 85  predicted sd=41.7  simulated sd=41.8
K=32  tau= 21.7 games  reach= 55  predicted sd=52.7  simulated sd=53.9
K=40  tau= 17.4 games  reach= 41  predicted sd=58.9  simulated sd=60.5
```

The `reach` column is close to `2.3 τ` (160, 80, 50 and 40 predicted), and the simulated noise matches the formula within a couple of points. Read the table as a menu.

| K | Games to reach ±30 of true | Settled rating wobble (1 sd) |
|---|---|---|
| 10 | about 165 | about 29 |
| 20 | about 85 | about 42 |
| 32 | about 55 | about 53 |
| 40 | about 41 | about 59 |

Quadrupling K from 10 to 40 cuts the climb by a factor of 4 but only doubles the wobble, because noise grows with the square root of K. A player at K = 32 who is exactly 1,800 in true strength will spend about a third of their time more than 53 points away from 1,800, purely from luck. Streaks of five straight losses at an even `E` happen in about 3% of five-game stretches, and at K = 32 each one costs 80 points.

In the interactive's second tab, "Choosing K", drag K and watch 20 simulated players climb from 1,500 to 1,800. The spread of the lines after they arrive is the noise, and the time for the pack to arrive is the speed.

### What the numbers say about design

- **One K cannot serve both a new player and an established one.** This is why FIDE uses 40 for the first 30 games and lower values later. A 30-game provisional period at K = 40 covers almost two time constants.
- **Set K from the wobble you can tolerate on the ladder display.** If a 50-point bounce after a bad evening will make players quit, K = 32 is too large for your visible rating.
- **Game length matters.** A chess player plays a few rated games a week. An arena player can play 30 in an evening. At K = 32, 30 games is more than one time constant, so a tilted evening can move a rating by 100 points or more.

## 5. Changes to Elo, and what each does to the pool

Every ladder you ship will modify basic Elo. Most modifications change the total number of points in the pool, and that total sets the meaning of every rating. Track it.

### Unequal K injects or removes points

Under FIDE's rules, a new player at K = 40 and an established player at K = 10 can meet. At equal ratings, if the new player wins, they gain `40 × 0.5 = 20` and the established player loses `10 × 0.5 = 5`. The pool gains 15 points. If the new player loses, the pool loses 15. Whether this inflates or deflates the pool depends on whether new players win or lose more than expected. New players who start underrated, like our 1,800 climber starting at 1,500, win more than expected and add points on balance.

### New players and leavers move the average

In a zero-sum pool, the average rating stays at the starting value only if nobody leaves. Players who improve, climb and then quit take their gains with them, and the players they beat keep their losses. If most leavers are above the starting value, the pool deflates, and a 1,600 rating means more this year than last. Designers fight this with small point injections, and some ladders reset each season, which [week 11](w11-seasonal-structures-and-resets.md) covers.

### Floors create points

Many games set a rating floor, a value below which a player cannot drop, to protect beginners. Every loss that would have gone below the floor still pays the winner in full. Points appear from nowhere, and the pool inflates from the bottom.

### Gap caps make weak opponents profitable

FIDE's 400-point cap means `E` never exceeds 0.909 in the formula. Suppose a player's true edge over a much weaker opponent is 800 points, so their true win chance is 0.99. Their average change per game is `K × (0.99 − 0.909) = 0.081 K`, which at K = 10 is +0.8 points a game. Under the cap, beating much weaker players is slow but positive, and a determined player can farm it. The cap exists to protect lower-rated players from large losses, and it creates this side effect. Every rule patch deserves the same check. Compute `K(p − E)` for the case the rule touches.

### Team averages hide individuals

A team rating built from members' ratings, as in early League of Legends, gives every member the same change. A player carried by four stronger teammates climbs with them. Elo cannot separate the members because it only sees the team result. Week 9's TrueSkill splits team updates by each player's uncertainty. It still cannot see who played well within one match.

### Visible and hidden numbers

WoW's old arena split, a hidden MMR driving matchmaking and the size of changes, and a visible rating that climbed from 0, is common. The hidden number is the estimate. The visible number is a progression bar that converges to it. That lets new players see steady progress while the estimate itself stays honest. The cost is that players can no longer compute their own update, and some will conclude the system is hiding something. Decide which of those you want deliberately.

## In-class activity (25 minutes)

Groups of three. One laptop running the interactive, one sheet of paper.

1. Player A is 1,640, player B is 1,560. With K = 24, compute both updates for an A win and for a B win. Check the zero-sum rule.
2. Your arena game has matches of 4 minutes and players who play 20 matches an evening. The ladder shows ratings to the public. Choose K so that an established player's settled wobble is under 35 points, using `σ = sqrt(K/(8g))`. How many games does a new player at that K need to close a 300-point gap to 30?
3. Propose a two-stage K (provisional, then established) that gets new players within 30 points in 20 games or fewer while keeping established wobble under 35. Say what happens to the pool when a provisional player beats an established one.
4. Your producer asks for a rating floor at 1,000. Write one paragraph for the design doc estimating how many points it injects if 5% of games involve a player at the floor losing.

Expected output: the four answers, with numbers. For step 2, `K ≤ 35² × 8g = 14.1`, so K = 14, with τ ≈ 49.6 games and about 114 games to close 300 to 30.

## Common misconceptions

- **"Beating weak players is bad for my rating."** On average it is neutral if your rating is right, because `K(p − E) = 0`. It is only noisier.
- **"A higher starting rating makes the system harder."** Only gaps matter. The starting value is a label.
- **"Bigger K makes the system more accurate."** It makes it faster and noisier. Noise grows with `sqrt(K)`, so once players are placed, a smaller K is more accurate.
- **"Elo is zero-sum, so average rating is fixed."** Only with equal K, no floors, and nobody leaving. Real ladders drift.

## Check yourself

1. A 1,900 player beats a 2,100 player with K = 20. How many points does each gain or lose?
2. A player at 1,500 wins 62% of games against opponents rated 1,500. About how far off is their rating, and in which direction?
3. With K = 16, what are `τ` and the settled wobble? How many games does it take to close a 200-point gap to 20?
4. Under a 400-point cap with K = 20, a player whose true edge over an opponent is 600 points plays 50 games against them. What is their expected total rating change? Without the cap?

<details>
<summary>Answers</summary>

1. The 1,900 player's `E = 1/(1 + 10^(200/400)) = 0.240`. They gain `20 × 0.760 = 15.2`. The 2,100 player loses 15.2.
2. `E = 0.62` at a gap of `400 × log10(0.62/0.38) = 85` points. The rating is about 85 points too low, and it will drift upward.
3. `τ = 1/(16 × 0.00144) = 43.4` games, wobble `sqrt(16/(8 × 0.00144)) = 37.3` points. Closing 200 to 20 takes `43.4 × ln 10 ≈ 100` games.
4. True `p` at 600 is 0.969, capped `E` is 0.909, so each game averages `20 × 0.060 = +1.2` and 50 games give about +60. Without the cap `E = p`, so the expected change is 0.

</details>

## Lab / assignment hook

[Lab 08, build and tune an Elo ladder](../labs/lab08.md). You will implement Elo, simulate a 500-player ladder with hidden true skills, measure calibration and rating error, and choose a two-stage K against targets. This lab is one of five that make up the rating lab (30%).

## Sources

- Elo, A. (1978). *The Rating of Chessplayers, Past and Present*. Arco. The rating scale and the development coefficient.
- FIDE Handbook, "FIDE Rating Regulations effective from 1 March 2024", section 8.3 (accessed September 2026). K = 40 until 30 games and for juniors under 2,300 until the end of the year of their 18th birthday; K = 20 below 2,400; K = 10 once 2,400 is reached; the rule that a difference over 400 counts as 400 for players rated below 2,650, effective October 1, 2025. https://handbook.fide.com/chapter/B022024
- Glickman, M. E. "The Glicko System" (glicko.net). The US Chess Federation example of two 1,700 players exchanging 16 points.
- League of Legends Wiki, "Elo rating system" (accessed September 2026). Elo used for ranked play until the League system in Season Three (2013); team Elo built from individual ratings; exact formulas unpublished.
- Warcraft Wiki, "Arena team" (accessed September 2026). Team rating and hidden matchmaking rating before patch 5.4.0; rating changes depend on the MMR difference.
- Wikipedia, "Elo rating system" (accessed September 2026), for the logistic form with base 10 and scale 400.

## Interactive spec: examples/w08-elo-expected-score.html

This is the course's signature worked example: "Elo expected score, 1/(1+10^(diff/400)), slider from 0 to 800 rating gap."

**The one insight:** the points a favourite risks grow as the points they can win shrink, and the two balance exactly when the rating is right. The average change `K(p − E)` is zero at the true gap and nowhere else.

**Tab 1, "Points at stake" (default):**

- Left view: the curve `E(d) = 1/(1 + 10^(−d/400))` for `d` from 0 to 800 on x, `E` from 0.5 to 1.0 on y. A draggable point on the curve at the current gap, with dashed guides to both axes.
- Right view: two vertical bars side by side, "If favourite wins: +K(1 − E)" and "If favourite loses: −K·E", on a shared axis from 0 to K. Numbers printed on each bar to 1 decimal.
- Controls: gap slider 0 to 800, step 10 (the signature control; also drags the curve point). K selector buttons 10, 16, 20, 24, 32, 40 (default 32).
- Toggle "Compare with true skill". When on, a second slider "true gap" 0 to 800 appears, a second marker shows `p = E(true gap)` on the curve, and a readout prints "Average change per game: K(p − E) = ±x.xx". Colour the readout positive when > 0 (rating too low), negative when < 0, neutral at |value| < 0.05.
- Numbers table under the views: rows for gaps 0, 100, ..., 800 with `E` (3 decimals), win gain, loss (1 decimal) for the current K. Highlight the row nearest the slider.

**Tab 2, "Choosing K":**

- Line chart of 20 simulated players, games 0 to 200 on x, rating 1,400 to 1,950 on y. Each starts at 1,500 with true strength 1,800. Each game: `p = E(1800 − R)`, win if a seeded uniform random number < p, then `R += K(S − 0.5)`. Dashed line at 1,800 and a shaded band 1,800 ± σ where `σ = sqrt(K/(8g))`, `g = ln 10/1600`.
- Controls: K slider 4 to 64, step 2 (default 32). "New seeds" button. Use a small seeded generator (for example mulberry32) so the same seed gives the same lines.
- Readouts: `τ = 1/(K·g)` (1 decimal), predicted games from 300 to 30 points `τ·ln 10` (whole number), predicted σ (1 decimal), and the measured standard deviation of all 20 lines over games 150 to 200.

**Test values:** gap 0 → E 0.500, +16.0/−16.0 at K 32. Gap 200 → 0.760, +7.7/−24.3. Gap 400 → 0.909, +2.9/−29.1. Gap 800 → 0.990, +0.3/−31.7. True gap 200 with rating gap 100 at K 32 → average change +3.83. K = 10 → τ 69.5, σ 29.5; K = 32 → τ 21.7, σ 52.7; K = 40 → τ 17.4, σ 58.9.

**First screen:** tab 1, gap 200, K 32, with the two bars clearly unequal (7.7 against 24.3). Caption: "The favourite wins a little or loses a lot. On average, exactly nothing."
