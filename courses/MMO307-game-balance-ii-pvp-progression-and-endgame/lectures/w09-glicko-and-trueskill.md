# MMO307 · Week 09 — Glicko and Uncertainty; TrueSkill for Teams

**Why this matters:** Elo gives a returning player and a daily player the same rating and moves both by the same K. Players notice. New accounts take dozens of games to place, veterans coming back from a break get stuck at old ratings, and in team games one new player on a veteran team swings the whole team's result. Systems that track how sure they are about each rating fix all three, and they are what modern ladders and matchmakers run on.

**You will be able to:**
- Compute a Glicko update by hand, including the rating deviation, and reproduce Glickman's published example.
- Explain the "effective K" of a Glicko update and compute it from a player's rating deviation.
- Compute a TrueSkill two-team update and explain why a newcomer's rating moves more than a veteran teammate's after the same result.
- Choose between Elo, Glicko and TrueSkill for a stated game, and set the parameter that controls how fast a rating can follow a changing player.

**Before class:** Glickman, "The Glicko System" (glicko.net, about 6 pages), all of it. Herbrich, Minka & Graepel (2006), "TrueSkill: A Bayesian Skill Rating System", sections 1 and 2. Microsoft Research's TrueSkill project page, the sections on how the system works and on teams.

**Prerequisites from earlier courses:** [MA102 week 8, dice sums and the normal curve](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w08-dice-sums-and-the-normal-curve.md) (the normal distribution, standard deviation and the cumulative curve Φ). [MA102 week 13, sampling and confidence](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md) (why a small sample gives a wide interval). [MA102 week 11, Monte Carlo simulation](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w11-monte-carlo-simulation.md). This course: [week 8, Elo and expected score](w08-elo-and-expected-score.md) (the update rule, K, and the speed-against-noise trade). [Week 10, matchmaking](w10-matchmaking-quality-vs-queue-time.md) uses this week's ratings to build matches.

**Interactive:** [`examples/w09-rating-uncertainty.html`](../examples/w09-rating-uncertainty.html). Keep it open during sections 2 and 3.

---

## 1. The same rating is not the same knowledge

Glickman opens his paper with a case you can feel. Two players rated 1,700 play, and the first wins. The first has just returned after years away. The second plays every weekend. Under the US Chess Federation's Elo, both move 16 points. But the returning player's 1,700 was barely believable. Beating an opponent whose 1,700 is well established is strong evidence that the returner is much better than 1,700, so their rating should move a lot. And the regular's rating should barely move, because they lost to someone whose strength nobody knows.

Elo cannot express this because a rating is a single number. The fix is to store two numbers per player.

- A **rating** `r`, the best current guess of strength.
- A **rating deviation** `RD`, how uncertain that guess is, in rating points. It is a standard deviation.

Read the pair as a range. Glickman suggests reporting `r ± 1.96·RD` as a 95% interval. A player at 1,850 with RD 50 is very likely between about 1,750 and 1,950. A new player at 1,500 with RD 350 could be almost anywhere from 814 to 2,186.

Two rules follow from what RD means. Playing games teaches you about a player, so **games always shrink RD**. Time away lets a player change unseen, so **inactivity always grows RD**. Everything else in this lecture is the arithmetic of those two rules.

## 2. Worked example: the question mark on your rating

### The hook

On Lichess, a new account starts at 1,500 and the site's FAQ describes it as 1,500 ± 1,000. For your first games the rating carries a question mark, and it moves by hundreds of points after a single result. The question mark disappears once the rating deviation falls to 110 or below, and it comes back if you stop playing for a long time. Chess.com's help pages describe the same behaviour. Ratings swing in your first games, and if you have not played in a while, your next game moves your rating more. Both sites are running Glickman's idea. The question mark is RD made visible.

### The model

Glickman's original system, now called Glicko-1, updates each player at the end of a **rating period**, a batch of games treated as simultaneous. With one game per period, it updates after every game. For a player with rating `r` and deviation `RD` who plays opponents `j` with ratings `r_j` and deviations `RD_j`, scoring `s_j`:

```
q = ln(10) / 400 = 0.0057565

g(RD) = 1 / sqrt(1 + 3·q²·RD² / π²)

E_j = 1 / (1 + 10^(−g(RD_j)·(r − r_j) / 400))

1/d² = q² · Σ g(RD_j)² · E_j · (1 − E_j)

r'  = r + q / (1/RD² + 1/d²) · Σ g(RD_j) · (s_j − E_j)
RD' = sqrt(1 / (1/RD² + 1/d²))
```

Read each piece in terms you already know.

- `E_j` is week 8's expected score, except the gap is shrunk by `g(RD_j)`. When the opponent's rating is uncertain, `g` is below 1 and the prediction is pulled toward 50%. You know less, so you predict less boldly.
- `1/RD²` is how much you knew before the period. `1/d²` is how much the period's games taught you. Information adds, so the new uncertainty is `1/RD'² = 1/RD² + 1/d²`. That is why games always shrink RD.
- The rating update is week 8's `K × surprise`, with the surprise weighted by `g`. The role of K is played by `q / (1/RD² + 1/d²) = q·RD'²`. A large RD means a large step.

Between periods, uncertainty grows:

```
RD at start of next period = min( sqrt(RD² + c²·t), 350 )
```

where `t` is the number of periods since the player last played and `c` is a constant the designer chooses. New players start at `r = 1,500` and `RD = 350`.

### Numbers you can check

Glickman's paper works one example. A player at 1,500 with RD 200 plays three games in a period. They win against 1,400 (RD 30), lose against 1,550 (RD 100), and lose against 1,700 (RD 300). The paper gets `r' = 1,464` and `RD' = 151.4`. The code below reproduces it, then asks a design question. How much does one even-match win move a player, as a function of their own RD?

```python
import math

Q = math.log(10) / 400

def g(rd):
    return 1 / math.sqrt(1 + 3 * Q**2 * rd**2 / math.pi**2)

def expected(r, rj, rdj):
    return 1 / (1 + 10 ** (-g(rdj) * (r - rj) / 400))

def glicko_update(r, rd, games):
    """games: list of (opponent rating, opponent RD, score) in one rating period."""
    inv_d2 = Q**2 * sum(g(rdj)**2 * expected(r, rj, rdj) * (1 - expected(r, rj, rdj))
                        for rj, rdj, _ in games)
    denom = 1 / rd**2 + inv_d2
    r_new = r + Q / denom * sum(g(rdj) * (s - expected(r, rj, rdj)) for rj, rdj, s in games)
    return r_new, math.sqrt(1 / denom)

r, rd = glicko_update(1500, 200, [(1400, 30, 1), (1550, 100, 0), (1700, 300, 0)])
print(f"Glickman's example: r' = {r:.0f}, RD' = {rd:.1f}")
print("own RD | win vs 1500 (RD 50) | effective K | RD after")
for own in (350, 250, 150, 100, 60, 30):
    r2, rd2 = glicko_update(1500, own, [(1500, 50, 1)])
    print(f"{own:6} | {r2 - 1500:+19.1f} | {2 * (r2 - 1500):11.1f} | {rd2:8.1f}")
```

```
Glickman's example: r' = 1464, RD' = 151.4
own RD | win vs 1500 (RD 50) | effective K | RD after
   350 |              +175.0 |       350.0 |    248.1
   250 |              +118.0 |       236.1 |    203.8
   150 |               +54.1 |       108.2 |    138.0
   100 |               +26.3 |        52.6 |     96.2
    60 |                +9.9 |        19.9 |     59.1
    30 |                +2.5 |         5.1 |     29.9
```

The **effective K** column is twice the gain from one even win, which is what week 8's K would have to be to produce the same step. A brand-new player moves as if K were 350. A settled player at RD 60 moves as if K were 20. At RD 30, K is effectively 5. One system does what FIDE needed three K values and a game counter to do, and it does it continuously.

Notice also how slowly RD falls. One game takes a new player from 350 only to 248. A single result is not much information, so it takes several games before the question mark goes away.

### The visual

Open [`examples/w09-rating-uncertainty.html`](../examples/w09-rating-uncertainty.html). The top view draws your belief about a player as a bell curve centred on `r` with width `RD`. Press "Win" or "Loss" against the opponent set by the sliders. The curve jumps and narrows. The ghost of the previous curve stays behind, so you see both the move and the shrink. The bottom view plots effective K against RD, with a marker at your current RD. Play ten games and watch the marker slide down the curve. Now press "Skip 10 periods" and watch the curve widen and the marker climb back up. The Lichess question mark appears in the top view whenever RD is above 110.

Then set the opponent's RD high. The same win moves you less, because beating an unknown tells the system little.

### Cross-game recognition

**Lichess (Glicko-2, current).** Lichess uses Glicko-2, Glickman's later version. It keeps `r` and `RD` and adds a third number per player, a **volatility**, that is high when a player's results are erratic and makes their RD grow faster. The provisional mark is shown when the deviation is above 110. Rewritten in our form, Lichess is the model above with an RD threshold drawn on the screen.

**Chess.com (Glicko, current).** Chess.com's help pages say it uses the Glicko system, that ratings change a lot in a player's first games, and that RD grows while a player is inactive so the next game moves the rating more. That is `RD' = min(sqrt(RD² + c²t), 350)` described in plain words.

**Xbox Live (TrueSkill, Halo 3 onward).** Microsoft's system stores a mean `μ` and uncertainty `σ` per player, the same pair with different letters. New players start at `μ = 25`, `σ = 8.333`, and the displayed skill is the conservative estimate `μ − 3σ`, which starts at 0 and rises as σ shrinks. The project page lists Halo 3, Gears of War 4, Halo 5, Gears 5, Halo Infinite, Forza Motorsport 7 and Forza Motorsport among the titles that used it. Section 4 treats TrueSkill in detail because it adds teams.

Three services, one idea. When you see a rating that is "provisional", "placing", or starts at zero and climbs, look for the hidden uncertainty and ask how it shrinks with games and grows with time.

### Design judgment, eyes open

- **Show uncertainty or hide it, deliberately.** Lichess shows a question mark, which is honest and slightly scary. TrueSkill's `μ − 3σ` hides it inside a number that only rises for new players, which feels like progress and understates their skill for a while.
- **Glicko is not zero-sum.** Two players exchange different amounts, because each step depends on each player's own RD. The rating pool can drift. Glickman says so in the paper. If your economy pays rewards by rating, track the pool (week 8, section 5).
- **RD must never reach zero.** As games pile up, RD falls and effective K falls with it. Glickman recommends a floor, such as 30. Section 3 shows a floor alone is not enough.
- **Players can game uncertainty.** A player who stops playing lets RD grow, then returns with large steps. If rewards depend on peak rating, an inactive period can be a strategy. The cap at 350 limits it.

## 3. The new K is c

Week 8 showed that K trades speed against noise. Glicko has a new knob with the same job, the drift constant `c`, and it is easy to set badly.

### How c is chosen

Glickman's paper gives a rule of thumb. Decide how long it should take for a typical player's rating to become as uncertain as a new player's. If a typical RD is 50, periods are two months long, and five years without play should reset uncertainty fully, that is 30 periods, and solving `350 = sqrt(50² + c²·30)` gives `c = 63.2`. From RD 50, one idle period gives 80.6, five give 149.9, and thirty give 350.

### What goes wrong without it

Compare three rating rules for a player whose true strength is 1,800, who starts at 1,500 and plays one game per period against accurately rated opponents (RD 50) at their own rating. At game 150 the player improves to a true 2,000. The table averages 300 simulated careers per rule.

| Rule | Games to get within 30 of 1,800 | Wobble once settled (1 sd) | Games to get within 30 of 2,000 after the jump |
|---|---|---|---|
| Elo, K = 32 | 53 | 53 | 40 |
| Glicko, RD floor 30, `c = 0` | 17 | 25 | not within 150 games (1,856 after 50) |
| Glicko, RD floor 30, `c = 15` per game | 16 | 50 | 42 |

Glicko places new players three times faster than Elo in every version, because its early effective K is huge and then shrinks. That is its main gain. But without drift, RD falls to the floor, effective K settles near 5, and the rating is frozen. It is accurate for a player who never changes and useless for one who improves. With `c = 15` per game, RD settles near 72, effective K near 28, and the rating tracks the improvement as well as Elo does, with Elo-like wobble.

The lesson is week 8's trade again. Once a player is placed, `c` sets how fast a rating can follow real change and how much it shakes, exactly as K did. Glicko's advantage is placement speed and the honest display of uncertainty, not freedom from the trade. Lab 09 asks you to reproduce this table.

### Glicko-2's answer

Glicko-2 makes the drift personal. Each player has a volatility that grows when their results surprise the system over several periods. A player on a sudden winning streak gets a larger drift, so their rating catches up faster, while a steady player's rating stays calm. Glickman's Glicko-2 example recommends starting volatility at 0.06 and choosing its own system constant, also called τ, between 0.3 and 1.2 by testing predictive accuracy. That is one more parameter to tune, and it only helps if your players really do change suddenly.

## 4. TrueSkill: uncertainty for teams

Elo and Glicko rate individuals in one-on-one games. Most MMO PvP is teams. TrueSkill, published by Herbrich, Minka and Graepel in 2006 and used on Xbox Live, extends the uncertainty idea to teams and to games with more than two sides.

### The model

Each player has a skill that the system does not know. Its belief about that skill is a normal distribution with mean `μ` and standard deviation `σ`, exactly Glicko's `r` and `RD` on a different scale. In each game, a player performs at their skill plus random noise with standard deviation `β`, the game's per-match luck. A **team's performance is the sum of its players' performances**. The team with the higher performance wins.

With that, the chance that team A beats team B is

```
c² = n·β² + Σ σ_i²                  (n players in the match, sum over all of them)
P(A beats B) = Φ( (Σ μ_A − Σ μ_B) / c )
```

where `Φ` is the cumulative normal curve from MA102 week 8. Compare it with Elo. Both are S-curves in the skill gap. Elo uses a logistic curve with a fixed scale of 400. TrueSkill uses the normal curve with a scale `c` that grows with both the game's luck and the players' uncertainty. When you are unsure of the players, predictions pull toward 50%, the same thing Glicko's `g(RD)` did.

After a win by team A, with `t = (Σ μ_A − Σ μ_B) / c`:

```
v = φ(t) / Φ(t)                     (φ is the normal density)
w = v · (v + t)

winner i:  μ_i' = μ_i + (σ_i² / c) · v
loser  j:  μ_j' = μ_j − (σ_j² / c) · v
everyone:  σ_i'² = σ_i² · (1 − (σ_i² / c²) · w)
```

Read the update the same way you read Glicko's. `v` is the surprise. It is large when the underdog wins (`t` very negative) and small when the favourite wins. Each player's share of it is proportional to their own `σ²`. **The more uncertain a player is, the more of the team's result they absorb.** Before each game, TrueSkill also adds a small drift `τ` to every σ, its version of Glicko's `c`. Draws are handled with a draw margin `ε`, which shifts `t` by `ε / c`.

The defaults are `μ = 25`, `σ = 25/3 ≈ 8.333`, `β = σ/2 ≈ 4.167` and `τ = σ/100 ≈ 0.083`. The open-source `trueskill` Python library uses these, with a default draw probability of 10%.

### Numbers you can check

```python
import math
from statistics import NormalDist

N = NormalDist()
BETA, TAU = 25 / 6, 25 / 300          # performance noise, per-game drift

def rate(winners, losers, draw_probability=0.0):
    """Two teams, each a list of (mu, sigma). Returns both teams updated."""
    n = len(winners) + len(losers)
    eps = N.inv_cdf((draw_probability + 1) / 2) * math.sqrt(n) * BETA
    winners = [(m, math.hypot(s, TAU)) for m, s in winners]
    losers = [(m, math.hypot(s, TAU)) for m, s in losers]
    c2 = n * BETA**2 + sum(s * s for _, s in winners + losers)
    c = math.sqrt(c2)
    t = (sum(m for m, _ in winners) - sum(m for m, _ in losers)) / c - eps / c
    v = N.pdf(t) / N.cdf(t)             # how much to move the means
    w = v * (v + t)                     # how much to shrink the variances
    up = [(m + s * s / c * v, s * math.sqrt(1 - s * s / c2 * w)) for m, s in winners]
    down = [(m - s * s / c * v, s * math.sqrt(1 - s * s / c2 * w)) for m, s in losers]
    return up, down

new = (25.0, 25 / 3)
(a,), (b,) = rate([new], [new], draw_probability=0.10)
print(f"1v1, two new players: winner {a[0]:.3f} ± {a[1]:.3f}, loser {b[0]:.3f} ± {b[1]:.3f}")
vet, rival = (30.0, 2.0), (28.0, 2.0)
for label, (w_team, l_team) in [("newcomer's team wins", ([vet, vet, new], [rival] * 3)),
                                ("newcomer's team loses", ([rival] * 3, [vet, vet, new]))]:
    up, down = rate(w_team, l_team)
    team = up if new in w_team else down
    print(f"{label}: veteran {team[0][0] - 30:+.2f}, newcomer {team[2][0] - 25:+.2f}, "
          f"newcomer sigma {team[2][1]:.2f}")
print(f"new player's displayed skill mu - 3 sigma = {25 - 3 * 25 / 3:.1f}")
```

```
1v1, two new players: winner 29.396 ± 7.171, loser 20.604 ± 7.171
newcomer's team wins: veteran +0.22, newcomer +3.76, newcomer sigma 7.35
newcomer's team loses: veteran -0.24, newcomer -4.21, newcomer sigma 7.29
new player's displayed skill mu - 3 sigma = 0.0
```

The first line matches the documented output of the `trueskill` library for two new players with its default 10% draw probability, which is a useful check that the formulas above are complete.

The team lines are the point. Two veterans (`μ = 30`, `σ = 2`) and one newcomer play three established rivals (`μ = 28`, `σ = 2`). The team sums are 85 against 84, almost even. When they win, each veteran gains 0.22 and the newcomer gains 3.76, about 17 times as much, which is the ratio of their variances, `8.334² / 2.002²`. The system has learned almost nothing about the veterans and a fair amount about the newcomer. Elo with one team rating, as in early League of Legends (week 8), would have moved all three by the same amount.

### What TrueSkill still cannot see

- **Who played well.** TrueSkill sees only which team won. Microsoft's project page is explicit that individual performance within a match is not used. A newcomer carried by veterans still gains 3.76.
- **Whether team strength really is a sum.** If one great player can win a match alone, or if a team is only as good as its weakest player, the sum is wrong. Many MMO team modes have roles ([MMO303 week 5](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w05-the-holy-trinity-tank-healer-dps.md)), where a bad healer ruins a team no matter how good its damage dealers are.
- **Parties.** Friends who queue together often play better than the sum of their skills, because they coordinate. The model has no term for that, so a party's members are overrated as a group and underrated when they later queue alone. Test for it on your own data by comparing party and solo win rates at equal predicted chances.

## 5. Choosing a system

| | Elo | Glicko-1 | Glicko-2 | TrueSkill |
|---|---|---|---|---|
| Numbers per player | rating | rating, RD | rating, RD, volatility | μ, σ |
| Teams | by averaging (crude) | no | no | yes, by sum |
| New-player placement | slow (fixed K) | fast (RD) | fast | fast (σ) |
| Follows a changing player | via K | via c | via c and volatility | via τ |
| Zero-sum | yes, with equal K | no | no | no |
| Players can check their own update | yes | with effort | hardly | hardly |
| Parameters to tune | K | c, RD floor, period length | τ, start volatility, period | β, τ, draw margin |

A decision rule of thumb for an MMO:

- **One-on-one ladder with public ratings, and players who value checking the math** (duels, a chess-like mode). Elo with a provisional K, or Glicko-1 with a visible question mark.
- **One-on-one with many new or returning players.** Glicko. Set `c` from a stated goal, and put a floor on RD.
- **Team modes with solo queue.** TrueSkill or a relative of it. Hide `μ` and `σ` for matchmaking and show players a progression number. [Week 10](w10-matchmaking-quality-vs-queue-time.md) uses exactly these numbers to build fair matches, and [week 11](w11-seasonal-structures-and-resets.md) decides what to do with them when a season ends.
- **Any system.** Measure calibration (week 8, section 3) on your own data before trusting defaults that were tuned for chess or Halo.

## In-class activity (25 minutes)

Pairs, one laptop with the interactive.

1. A player returns after 12 idle periods with `r = 1,700` and `RD = 60`, and the game uses `c = 40`. Compute their RD at the start of the next period.
2. They win one game against a 1,700 player with RD 50. Using the interactive or the code, compute the gain. What would a K = 32 Elo system have given?
3. In a 3v3 TrueSkill match, your team is two veterans (`μ = 32`, `σ = 1.5`) and one returning player whose σ has grown to 5. Before running the code, predict which player's μ moves most after a loss, and by roughly how many times as much as a veteran's. Then check with the code.
4. Your game shows `μ − 3σ` on the profile. A returning player complains that their displayed skill dropped while they were away without playing a single game. Explain why in two sentences, and propose a display that avoids the complaint.

Expected output: the numbers for steps 1 to 3 and the explanation. For step 1, `sqrt(60² + 40² × 12) = sqrt(22,800) = 151.0`. For step 3, the variance ratio `(5² + τ²)/(1.5² + τ²)` is about 11, so the returning player's μ moves about 11 times as much as a veteran's.

## Common misconceptions

- **"RD is how inconsistent a player is."** RD is how uncertain the system is about the player's strength. A perfectly consistent player who never plays has a large RD. Glicko-2's volatility is the number closer to "inconsistent".
- **"Glicko removes the need to tune K."** It replaces K with `c` (and a floor), and `c` has the same speed-against-noise trade once players are placed.
- **"TrueSkill rewards the best player on the winning team."** It rewards the most uncertain player. Individual performance is not an input.
- **"`μ − 3σ` is the player's skill."** It is a deliberately low estimate. It rises as σ shrinks, even when μ does not change, so it reads as progress.

## Check yourself

1. Using the effective-K table from section 2, a player with RD 150 wins an even game against a 1,500 player with RD 50. How much do they gain, and what is their new RD? How many more such games would roughly halve their RD?
2. With Glickman's rule of thumb, you want RD to go from a typical 40 back to 350 in 24 periods. Find `c`.
3. Two new TrueSkill players (`μ = 25`, `σ = 8.333`) play with no draws allowed. Is the winner's new μ above or below 29.396? Explain without computing.
4. A TrueSkill team is three players with `σ = 3, 3, 6`. After a win with `v / c = 0.05`, how much does each player's μ rise?

<details>
<summary>Answers</summary>

1. Gain 54.1, new RD 138.0. Each even game against this opponent adds about the same amount to `1/RD²`, namely `q²·g(50)²·0.25 ≈ 8.1 × 10⁻⁶`. Halving RD from 150 to 75 needs `1/RD²` to rise from 4.4 × 10⁻⁵ to 1.8 × 10⁻⁴, a rise of 1.33 × 10⁻⁴, so about 16 or 17 games in total.
2. `350² = 40² + 24·c²`, so `c² = (122,500 − 1,600)/24 = 5,037.5` and `c = 71.0`.
3. Below. It is 29.205. With a draw margin, a win means the winner outperformed the loser by more than the margin, which is stronger evidence than outperforming them at all. Stronger evidence moves μ further, so the 10% draw setting gives the larger 29.396.
4. The rise is `σ² × v / c`: `9 × 0.05 = 0.45` for each of the first two players and `36 × 0.05 = 1.8` for the third.

</details>

## Lab / assignment hook

[Lab 09, Glicko and TrueSkill side by side](../labs/lab09.md). You will implement Glicko-1 and a two-team TrueSkill update, reproduce Glickman's example and the library's 1v1 values, rebuild the section 3 comparison table, and test a TrueSkill ladder on a simulated 3v3 mode with parties. This lab is one of five that make up the rating lab (30%).

## Sources

- Glickman, M. E. "The Glicko System" (glicko.net/glicko/glicko.pdf). The returning-player motivation; rating and RD; `r ± 1.96·RD` interval; formulas for `q`, `g`, `E`, `d²`, `r'`, `RD'`; unrated players at 1,500 and RD 350; `RD = min(sqrt(RD² + c²t), 350)`; the worked example giving 1,464 and 151.4; `c = 63.2` for 30 periods from RD 50; the recommended RD floor of about 30; the note that Glicko changes are not balanced.
- Glickman, M. E. (2022). "Example of the Glicko-2 system" (glicko.net/glicko/glicko2.pdf). Volatility per player, starting volatility 0.06, system constant τ between 0.3 and 1.2.
- Glickman, M. E. (1999). "Parameter estimation in large dynamic paired comparison experiments." *Applied Statistics* 48, 377-394.
- Lichess, "Frequently Asked Questions", rating section (accessed September 2026). Glicko-2; new players at 1,500 ± 1,000; provisional "?" when the deviation is above 110.
- Chess.com Help Center, "How do ratings work on Chess.com?" (accessed September 2026). Glicko; ratings change a lot in early games; RD increases with inactivity.
- Herbrich, R., Minka, T. & Graepel, T. (2006). "TrueSkill: A Bayesian Skill Rating System." *Advances in Neural Information Processing Systems 19*.
- Microsoft Research, "TrueSkill Ranking System" project page (accessed September 2026). Defaults `μ = 25`, `σ = 8.333`; conservative skill `μ − k·σ` with k usually 3; team skill as the sum of player skills; gains and losses proportional to each player's uncertainty; individual performance not used; titles including Halo 3, Forza Motorsport 7, Gears of War 4, Halo 5, Gears 5, Halo Infinite and Forza Motorsport.
- Lee, H. "TrueSkill" Python library documentation (trueskill.org, accessed September 2026). Defaults `β = 4.1667`, `τ = 0.0833`, draw probability 0.10; `rate_1vs1` on two new ratings gives 29.396 ± 7.171 and 20.604 ± 7.171; `expose` as `μ − 3σ` for leaderboards.

## Interactive spec: examples/w09-rating-uncertainty.html

**The one insight:** the size of a rating change comes from uncertainty. A wide belief moves a lot and narrows; a narrow belief barely moves. Time away widens it again.

**Tab 1, "Glicko belief" (default):**

- Top view: a normal curve for the player's belief, centre `r`, standard deviation `RD`, x axis 700 to 2,300. Shade `r ± 1.96·RD`. After each result, keep the previous curve as a faint ghost. When `RD > 110`, show a large "?" next to the rating readout (label it "provisional, as on Lichess").
- Bottom view: effective K against own RD, for RD 30 to 350 on x. Effective K is `2 × (r' − r)` for a single win against the current opponent at equal rating. Draw it as a curve computed from the Glicko formulas with the opponent's current RD. A marker shows the player's current RD.
- Controls: opponent rating slider 1,000 to 2,000 (default: equal to player's current rating, with a "match me" checkbox on by default); opponent RD slider 30 to 350 (default 50); buttons "Win", "Draw", "Loss" (each runs one single-game rating period); "Skip 10 periods" (applies `RD = min(sqrt(RD² + 10c²), 350)`); c slider 0 to 100 (default 15) with a "c = 63.2" shortcut; RD floor 30 (checkbox, on); "Add one period of drift before each game" (checkbox, off), which applies `RD = min(sqrt(RD² + c²), 350)` before every result; player presets "Reset to new player" (1,500, RD 350), "Settled" (1,500, RD 100), "Veteran" (1,500, RD 50) and "Glickman's example".
- Readouts: `r`, `RD`, the 95% interval, the last change, effective K.
- History strip: small sparkline of `r` over the last 40 games.

**Tab 2, "TrueSkill teams":**

- Two teams of three. Each player card shows `μ` and `σ` with sliders (`μ` 10 to 40, `σ` 0.5 to 8.5). Defaults: team A = (30, 2), (30, 2), (25, 8.333); team B = (28, 2) × 3.
- Show `P(A wins) = Φ((ΣμA − ΣμB)/c)` with `c² = 6β² + Σσ²`, β = 25/6.
- Buttons "A wins", "B wins". Apply the section 4 update with τ = 25/300 added to every σ first, no draw margin. Animate each player's μ bar moving by its change and print the change next to it.
- A bar chart "Share of the team's update" showing `σ_i²/Σσ²` within each team, so the newcomer's dominance is visible.

**Test values:** Glickman example button (preset) gives `r' = 1,464`, `RD' = 151.4`. New player vs 1,500 RD 50, win: +175.0, RD 248.1. RD 100, same win: +26.3, RD 96.2. RD 50 plus 30 idle periods at c = 63.2: RD 349.8 (capped at 350). Tab 2 defaults: A wins → veterans +0.22, newcomer +3.76, newcomer σ 7.35; B wins → veterans −0.24, newcomer −4.21, newcomer σ 7.29. Two new 1v1 players with a 10% draw probability option (checkbox in tab 2's advanced panel): 29.396 ± 7.171 and 20.604 ± 7.171.

**First screen:** tab 1 with a new player (1,500, RD 350), "?" visible, and the effective-K curve with the marker at the top left. Caption: "Your first game moves you like K = 350. Your hundredth, like K = 20."
