# MMO307 · Week 14 — Measuring Balance with Win Rates and Pick Rates

**Why this matters:** Win rate is the first number anyone checks after a patch. On many rated ladders the matchmaker quietly pushes it to 50% for every class, including the broken one. If you don't know where the signal went, you will call an overpowered class balanced and ship the next patch on top of it.

**You will be able to:**
- Compute the win rate a class shows from its advantage in rating points and the share `f` of its players' rated games played on it.
- Compute a class's over-representation in the top slice of a ladder from its rating shift, and choose a cutoff that trades magnification against sample size.
- Choose the right balance signal (win rate, early-window win rate, top-of-ladder representation, pick rate, presence) for a game's rating structure, and justify the choice.
- Critique a balance dashboard for signals it hides and for confounders it ignores.

**Before class:** Elo, *The Rating of Chessplayers, Past and Present* (1978), the opening chapter on the rating scale and expected scores (course reading). Riot Games, "/dev: Champion Balance Framework" (2019). Reread [MMO303 week 1, section 3](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w01-what-balanced-means.md) ("Viability in numbers: win rates and why they lie"). About 45 minutes in total.

**Prerequisites from earlier courses:** [MMO303 week 1](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w01-what-balanced-means.md) (mirror correction, pick bias, `N_eff`). [MA102 week 13](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md) (confidence intervals for a rate) and [MA102 week 14](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w14-intro-to-hypothesis-testing-ab.md) (comparing two rates). From this course, [week 8](w08-elo-and-expected-score.md) (Elo expected score, the slope `g` and the time constant of a rating), [week 10](w10-matchmaking-quality-vs-queue-time.md) (matchmaking), [week 11](w11-seasonal-structures-and-resets.md) (seasons and resets) and [week 13](w13-meta-game-and-patch-cycles.md) (settling after a patch).

**Interactive:** [`examples/w14-rating-absorbs-advantage.html`](../examples/w14-rating-absorbs-advantage.html). Open it for section 2.

---

## 1. Four numbers on every balance dashboard

Every competitive game's balance dashboard shows some version of these four numbers, cut by class, spec, hero or champion.

- **Win rate.** Wins divided by games played with the option. It answers the question "when players pick this, how often do they win?"
- **Pick rate.** The share of games (or of player slots) in which the option appears. It answers "how often do players choose this?" It measures belief and taste as much as power.
- **Ban rate.** In games with a ban phase, the share of games where the option is removed before picks. It measures fear.
- **Presence.** Pick rate plus ban rate. It measures how much of the game the option occupies, whether played or feared. Riot's framework, described in MMO303 week 1, uses presence as its signal for professional play.

MMO303 week 1 covered three traps in reading win rate. Mirror matches pull a popular class toward 50%. The players who choose a class shape its win rate. Small samples make rare classes noisy. Keep those corrections. For the error bars, MA102 week 13's interval for a rate gives a quick rule. With `n` games at a win rate near 50%, the 95% interval is about `±1.96 × √(0.25/n)`. At 10,000 games that is `±0.98` percentage points, and at 1,000 games `±3.1`.

This lecture adds a trap that sits upstream of all three. On a rated ladder, **the matchmaker and the rating system are part of the measurement**. The same class can show a 58% win rate on one ladder and 50% on another with identical strength, depending on who owns the rating.

## 2. Worked example: the strongest spec with a 50% win rate

### The hook

World of Warcraft's Rated Solo Shuffle, the solo-queue 3v3 arena mode, tracks a separate rating for each specialization of each character. Blizzard built it that way when the rated mode arrived in patch 10.0.0 (Dragonflight, 2022). League of Legends does the opposite. Its hidden matchmaking rating (MMR) belongs to the player, per queue, whatever champion they pick, and it moves only with wins and losses.

Now suppose each game has a spec (or champion) that is clearly too strong. Players on the League side can see it in the champion's win rate. Players on the WoW side who check the spec's win rate over a season find it sitting near 50%. So they don't use win rate. They look at which specs crowd the top of the ladder. Same kind of overtuning, different measurements. Why does one ladder hide the win rate and the other doesn't?

### The model

Use [week 8](w08-elo-and-expected-score.md)'s Elo expected score. A player whose effective strength is `x` rating points above their opponent's wins with probability

```
E(x) = 1 / (1 + 10^(−x/400))
```

This is the course's formula `1/(1 + 10^((R_B − R_A)/400))` with `x = R_A − R_B`. Week 8 called its slope at `x = 0` `g = ln 10 / 1600 ≈ 0.00144` per rating point. Near an even match, every 10 points of advantage add about 1.44 percentage points of win probability.

Now describe a class and the ladder around it.

- `s` is a player's skill, in rating points.
- `δ` (delta) is the **class advantage**. A player on this class plays as if their skill were `s + δ`. A +60 class makes everyone who plays it 60 points better.
- `f` is the **share of the rating's games played on the class**. On a ladder where the rating belongs to the spec, `f = 1`. On a ladder where one rating covers every champion a player uses, `f` is the share of that player's games on this one.
- `R` is the player's rating, and the matchmaker pairs players with equal `R`.

A rating settles where the player wins half their games against equal-rated opponents. Their opponents play at their ratings, on average. On the class the player plays at `s + δ`, and off it at `s`. So `R` settles where

```
f × E(s + δ − R) + (1 − f) × E(s − R) = 1/2
```

For the advantages balance deals with (tens of points, where `E` is nearly straight), the solution is

```
R ≈ s + f × δ
```

The rating absorbs the share of the advantage the player always brings. Put that back into `E` to get the win rate the class shows against equal-rated opponents:

```
class win rate = E(s + δ − R) = E((1 − f) × δ)
```

The part of `δ` the rating has swallowed, `f × δ`, has left the win rate. It went into the ratings, so the class's players now sit `f × δ` points higher on the ladder than equally skilled players of other classes.

To see that shift, look at the top of the ladder. Suppose skills are spread normally with standard deviation `σ`, the class is a small share of the ladder, and its players are as skilled as anyone else. The share of the class that lands in the ladder's top slice `q` (for example `q = 0.001` for the top 0.1%) is

```
top share = 1 − Φ(z_q − f × δ / σ),   where z_q = Φ⁻¹(1 − q)
```

Here `Φ` is the standard normal cumulative distribution from [MA102 week 8](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w08-dice-sums-and-the-normal-curve.md). Divide by `q` to get the **representation ratio**. At 1.0 the class is represented fairly at the top, and at 2.0 it appears twice as often as its share of the ladder.

### Numbers you can check

Take a class with `δ = +60` and a ladder with `σ = 200`. First, the win rate as the rating's share of games on the class grows:

| `f` | Rating shift `f × δ` | Class win rate `E((1 − f) × 60)` | Exact equilibrium win rate |
|---|---|---|---|
| 0 | 0 | 58.55% | 58.55% |
| 0.10 | 6 | 57.71% | 57.72% |
| 0.25 | 15 | 56.44% | 56.45% |
| 0.50 | 30 | 54.31% | 54.31% |
| 0.75 | 45 | 52.16% | 52.15% |
| 1 | 60 | 50.00% | 50.00% |

The last column solves the settling equation exactly, by bisection. The approximation is off by at most 0.01 points here, and it is exact at `f = 0`, `½` and `1`. Check the `f = 0.5` row by hand. `E(30) = 1 / (1 + 10^(−0.075)) = 1 / (1 + 0.841) = 0.543`.

Now the representation ratio at four cutoffs:

| Top slice `q` | `z_q` | `f = 0` | `f = 0.25` | `f = 0.5` | `f = 0.75` | `f = 1` |
|---|---|---|---|---|---|---|
| 50% | 0.000 | 1.00 | 1.06 | 1.12 | 1.18 | 1.24 |
| 10% | 1.282 | 1.00 | 1.14 | 1.29 | 1.45 | 1.63 |
| 1% | 2.326 | 1.00 | 1.22 | 1.48 | 1.78 | 2.14 |
| 0.1% | 3.090 | 1.00 | 1.28 | 1.64 | 2.08 | 2.63 |

Check one cell by hand. At `f = 1` and the top 10%, the shift is `60 / 200 = 0.3` standard deviations, so the class needs `z > 1.282 − 0.3 = 0.982`. That happens `1 − Φ(0.982) = 16.3%` of the time, against 10% for everyone else, a ratio of 1.63.

Read the two tables together. As `f` goes from 0 to 1, the win-rate column falls to 50% and the representation columns climb. The signal doesn't disappear. It moves from the win rate into the ratings. And the further up the ladder you look, the larger it gets. At the top 0.1%, a +60 class on a per-spec ladder is 2.6 times over-represented while its win rate is exactly 50%.

### How fast the rating absorbs the advantage

A patch changes `δ` overnight, but ratings take games to move. Week 8 showed that each game closes a fixed fraction `K·g` of the gap between a rating and true strength, a time constant of `1/(K·g)` games. A patch that adds `δ` to a class opens a gap of `f × δ` for everyone who plays it. With `K = 24`, `K·g = 3.45%` per game, a time constant of about 29 games per player.

That is [week 13](w13-meta-game-and-patch-cycles.md)'s exponential settling again, measured in games instead of days. It opens an **early window**. For the first ten or so games each player plays after a patch, the class shows most of its new advantage in its win rate. After 60 to 90 games the rating has absorbed most of it. The lab 14 simulator shows exactly this. For a +60 class on a per-spec ladder (2,000 players, `K = 24`), the class won about 57% of its games in the first ten rounds after the patch, averaged over five seeds. That dropped to about 51% by round 60 and stayed near 50.5% for the rest of the run. The simulated top-10% ratio (about 1.3 to 1.6, depending on the seed) lands below the closed form's 1.63. The main reason is the closed form's small-share assumption. In the simulation the class is 20% of the ladder, so its own shifted players raise the top-10% cutoff. Redo the calculation with that mixture and the ratio drops to 1.47. Week 8's settled rating noise, `√(K/(8g)) ≈ 46` points at `K = 24`, takes it to 1.45. The lab asks you to reproduce both steps.

### A visual you can move

Open [`examples/w14-rating-absorbs-advantage.html`](../examples/w14-rating-absorbs-advantage.html). The left view plots the class win rate against `f`. The right view shows two rating distributions, everyone and the class, with a line at the top-slice cutoff and the shaded tail beyond it. Drag `f` from 0 to 1. On the left the win rate slides down to 50%, and the class looks less and less of a problem. On the right the class's curve slides right, and its shaded tail beyond the cutoff grows. Then move the cutoff from the top 50% to the top 0.1%. The ratio in the number panel climbs from 1.24 to 2.63 at `f = 1`. The class hasn't changed. You are only looking further along the tail.

### Cross-game recognition

**World of Warcraft, Rated Solo Shuffle (patch 10.0.0 onward).** Rating is per specialization, so `f = 1` for every spec. A spec's season-long win rate tells you almost nothing about its strength, because the matchmaker has done its job. The signal lives in the rating distribution. Blizzard's own rewards sit exactly where the table says the magnification is largest. In Dragonflight, the seasonal Legend title went to the top 0.1% of the Solo Shuffle ladder among players with at least 50 games. The older arena brackets keep a separate personal rating per character for 2v2, 3v3 and rated battlegrounds. That puts them close to `f = 1` for any player who stays on one spec.

**League of Legends (current ranked queues).** MMR is per player per queue and moves with wins and losses, not with champion choice. Most players spread their games across several champions, so for any one champion `f` is small and the champion's win rate carries most of `δ`. That is why Riot's framework (MMO303 week 1) can put thresholds directly on win rate, per audience. There is one exception inside the same game. A "one-trick" who plays a single champion has `f` near 1, so their MMR absorbs that champion's advantage. Champions with many one-tricks read closer to 50% than their strength warrants, whether they are strong or weak.

**Overwatch 2, Role Queue (current competitive).** Each player has an independent rating for each role (tank, damage, support). A hero is one of several options in its role, so for a given hero `f` is the share of that player's role games spent on it. Hero win rates therefore show `(1 − f)` of the hero's advantage. That is the middle rows of the first table. A support hero with many dedicated mains reads closer to 50% than a hero people pick casually. Overwatch 2 also added a per-hero skill rating from Season 18 that is not used for matchmaking, so it records hero skill without feeding back into who you play against.

Three games, one equation. When you meet a new ladder, your first question is who owns the rating, and what `f` that implies for the thing you are measuring.

### Eyes-open design judgment

- **The 50% is the matchmaker working, not the class being balanced.** On a ladder where the rating owns the class, never read a season win rate as a balance verdict. Use the early window after a patch, or representation near the top.
- **Representation is confounded by who picks.** Top players may prefer a spec for reasons of skill ceiling, not raw power, and that also raises its top share. The model assumed the class's players are as skilled as anyone else. Read representation as a change, before and after a patch, rather than as a level. A spec that goes from 1.3× to 2.1× in the top 1% after a buff has been buffed by roughly the difference.
- **Magnification costs sample size.** The top 0.1% of a 50,000-player ladder is 50 players. A class with a 10% share expects 5 of them, and the natural spread of that count (about ±2.2, the square root of 5) is as large as the effect you are looking for. The top 1% holds 500 players and 50 expected, with a spread of about ±7, which is readable. Choose the deepest cutoff that still gives dozens of expected players.
- **Choose the rating structure knowing what it hides.** Per-spec ratings are fair to players who play several specs, because a weak off-spec does not drag down their main. But they move balance problems out of the win rate and into the ladder, and players feel them as "my spec can't reach the top." Per-player ratings keep the signal in the win rate, but a player who switches to a strong champion climbs past people of equal skill. Decide which failure you prefer.
- **Players experience the shift, not the win rate.** On an `f = 1` ladder a player on the overtuned spec does not win more games. They hold a higher rating and a better title. That makes the title distribution itself a balance outcome players care about.

## 3. Pick rate: belief, taste and power

Pick rate measures what players choose. Power is only one input to that choice, and it arrives with a lag.

- **Lag.** After a buff, pick rate rises on week 13's settling timescale, days for a well-connected player base. A buff nobody notices changes win rate with no pick change. A buff that is noticed but tiny changes picks with no win change.
- **Taste.** Fantasy, look, new cosmetics, ease of play and social pressure all move picks. A popular class may be popular for none of the reasons you tuned.
- **Normalization.** Compare a pick share with the fair share `1/n`, or use MMO303 week 1's `N_eff` for the whole roster. In a game with bans, an option banned in 40% of games can be picked in at most 60%, so divide by availability. The available pick rate is `pick rate / (1 − ban rate)`.

Putting pick rate against win rate gives four quadrants. Each one suggests a first question to ask, not a verdict.

| | High win rate | Low win rate |
|---|---|---|
| **High pick rate** | Strong and known. Check presence and representation; this is the usual nerf candidate. | Popular for other reasons, or a beginner magnet (MMO303 week 1). Check win rate by games played on the class before buffing. |
| **Low pick rate** | Specialist class, or strength not yet discovered. Check sample size and who plays it; expect picks to rise within a few `τ`. | Weak, or unloved. Check whether the few players are new to it; a buff may be needed, or a rework. |

Now add this week's model to the table. On an `f = 1` ladder every class sits in the middle column for win rate, and the table collapses to a single row per class. The quadrants only work where the rating does not own the class. On a per-spec ladder, replace the win-rate axis with top-slice representation.

## 4. A measurement recipe

Run these steps for any balance question on a rated ladder, in this order.

1. **Name the audience.** Pick the bracket you are tuning for, as Riot does with its four audiences. Top-of-ladder representation and bracket filters interact, so state both.
2. **Find `f`.** For the class you are measuring, what share of its players' rated games is on it? Rating per spec means 1. Rating per player means roughly the class's share of each player's games, which you can compute from match history. Report the median, and look for one-trick clusters.
3. **Choose the signal from `f`.** Small `f` means use win rate (mirror-corrected, MMO303 week 1). Large `f` means use the early-window win rate after a patch and the change in top-slice representation. Intermediate `f` means use both, and divide the win-rate excess by `(1 − f)` to estimate `δ`.
4. **Put error bars on it.** Win rate, `±0.98` points at 10,000 games. For representation, the expected count in the top slice, and its square root as a rough spread. Compare two patches with MA102 week 14's two-proportion test.
5. **Respect the clock.** Pick data is readable after about `2τ` (week 13). Rating-absorbed signals change over tens of games per player, so measure the early window within each player's first ten or so games after the patch.
6. **Compare against a target set before the patch.** Write the threshold down first, in the form MMO303 week 14 recommends for patch notes. A threshold chosen after seeing the data will always find something.

## In-class activity (25 minutes)

Pairs. An invented per-spec ladder (`f = 1`, `σ = 200`, `K = 24`) reports these numbers for four specs a month after a patch:

| Spec | Season win rate | Top 10% ratio | Top 1% ratio | Win rate, players' first 10 games after the patch |
|---|---|---|---|---|
| Arbiter | 50.6% | 1.9 | 2.6 | 58.9% |
| Bastion | 49.8% | 1.0 | 1.0 | 50.3% |
| Cinder | 49.5% | 0.7 | 0.6 | 45.1% |
| Drifter | 50.2% | 1.2 | 1.3 | 52.4% |

1. Rank the specs by strength, using only the season win rate. Then rank them again using the other three columns (5 minutes).
2. Estimate each spec's `δ` two ways. From the top 10% ratio `r`, use `δ = σ × (z_0.10 − Φ⁻¹(1 − 0.10 r))`. From the early-window win rate `W`, use `δ = 400 × log₁₀(W / (1 − W))` (10 minutes).
3. The two estimates disagree in a consistent direction. Explain why, using section 2's absorption rate (5 minutes).
4. Write one dashboard rule for this ladder that would have caught Arbiter within a week (5 minutes).

Expected output: two rankings, a table of eight `δ` estimates, a two-sentence explanation and one rule. (Arbiter's top 10% estimate is about +81 and its early-window estimate about +62. The early window already includes some absorption, so it reads low.)

## Common misconceptions

- **"A 50% win rate means the class is balanced."** On a ladder where the rating owns the class, every class converges to 50%. The strength has moved into the ratings. [MMO303 week 9](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w09-intransitivity-and-counters.md) showed a second route to the same 50%, where a counter loop settles the population mix instead of the ratings. Check both before you trust the number.
- **"Top-of-ladder representation is the purest signal."** It is the most magnified signal and the most confounded. It mixes power with who picks the class, and at deep cutoffs it rests on a handful of players.
- **"High pick rate means strong."** Pick rate is belief plus taste, with a lag. Read it against win rate or representation, and against the time since the patch.
- **"Skill-adjusted win rate fixes the matchmaker problem."** Comparing wins with the Elo-expected wins per match only measures what the rating has not absorbed, which is `(1 − f) × δ` again. Any rating that sees the class's games absorbs the class.

## Check yourself

1. In a game with a per-player rating, you play 20% of your ranked games on a champion with `δ = +40`. What win rate do you show on it against equal-rated opponents, and how far above your skill does your rating sit?
2. On a per-spec ladder with `σ = 200`, a spec shows a 50.4% win rate over the season and 1.9 times its fair share of the top 1%. Estimate `δ`.
3. Your ladder has 50,000 players, and the spec you are worried about has a 10% share. Why would a designer rather read the top 1% than the top 0.1%, even though the 0.1% magnifies the signal more?
4. After a patch, a spec wins 56% of its players' first ten games. Estimate `δ` from that number, and say whether the true value is likely higher or lower.

<details>
<summary>Answers</summary>

1. The win rate is `E(0.8 × 40) = E(32) = 1 / (1 + 10^(−0.08)) = 54.6%`. The rating sits `0.2 × 40 = 8` points above skill.
2. The top share is `0.019`, so `Φ⁻¹(0.981) = 2.075`. With `z_0.01 = 2.326`, `δ = 200 × (2.326 − 2.075) ≈ 50` points. The 50.4% win rate is consistent with `f = 1` and tells you nothing on its own.
3. The top 0.1% holds 50 players, and the spec expects 5 of them, with a spread of about ±2.2. The top 1% holds 500, and the spec expects 50, with a spread of about ±7, or about ±14% of the count. The 0.1% cut shows a bigger ratio, but you cannot distinguish 1.0× from 1.5× with 5 players.
4. `δ = 400 × log₁₀(0.56/0.44) = 400 × 0.105 ≈ 42` points. The true value is likely higher, because ratings start absorbing the advantage from the first game (3.45% of the gap per game at `K = 24`), so the first ten games already show a partly absorbed signal.

</details>

## Lab hook

[Lab 14, does the ladder hide an overpowered class?](../labs/lab14.md) You implement Elo expected score and updates, and the two closed forms from section 2. Then you run a ladder simulator to see the win rate absorbed, compare simulated representation with the closed form, and design a dashboard rule. This lab is part of the rating lab assessment and feeds the rating simulation in the final season design.

## Sources

- Warcraft Wiki, "Solo Shuffle" (warcraft.wiki.gg, accessed September 2026). Rated Solo Shuffle introduced in patch 10.0.0 with a rating tracked for each of a character's specializations; mode added unrated in 9.2.0.
- Warcraft Wiki, "Arena season" (accessed September 2026). Dragonflight seasonal Legend title for the top 0.1% of the Solo Shuffle ladder with at least 50 games.
- Warcraft Wiki, "Arena" (accessed September 2026). Separate personal rating per character for 2v2, 3v3 and rated battlegrounds.
- League of Legends Wiki, "Matchmaking" (wiki.leagueoflegends.com, current ranked queues, accessed September 2026). Hidden MMR per player and queue, estimated from whom the player wins and loses against.
- Riot Games (May 30, 2019). "/dev: Champion Balance Framework." leagueoflegends.com. Audiences, win-rate and presence thresholds (details in MMO303 week 1).
- Overwatch Wiki, "Competitive Play" (overwatch.fandom.com, accessed September 2026). Role Queue gives an independent rating for each of the three roles; per-hero SR from Season 18, not used for matchmaking.
- Elo, A. E. (1978). *The Rating of Chessplayers, Past and Present*. Arco. The logistic expected-score form used in week 8.
- Model, tables and simulation results are this course's own; the simulator is `labs/lab14-starter/ladder.py`.

## Interactive spec: examples/w14-rating-absorbs-advantage.html

**The one insight:** as more of a rating's games are played on a strong class, its win rate falls to 50% and its players move up the ladder instead. The signal does not vanish. It moves from the left view to the right, and a deeper cutoff magnifies it.

**Layout.** Two linked views side by side at 1280px, stacked at 390px (win-rate view first). Controls above, number panel below. The first screen uses the defaults, so the left marker sits at 50% while the right view clearly shows the shifted tail.

**Left view: class win rate against `f`.**
- x axis: `f` from 0 to 1. y axis: win rate from 40% to 70%, with a reference line at 50%.
- Curve: `W(f) = E((1 − f) δ)` with `E(x) = 1 / (1 + 10^(−x/400))`.
- Filled marker at the current `f`, labeled with `W` to two decimals.
- Optional toggle "exact": overlays the exact equilibrium win rate from bisection on `f E(δ − x) + (1 − f) E(−x) = 0.5` (solve for `x`, then `W = E(δ − x)`), to show the approximation is almost indistinguishable.

**Right view: rating distributions.**
- x axis: rating from `1500 − 4σ` to `1500 + 4σ + 150`. Two normal curves with SD `σ`: "everyone else" centered at 1500, "this class" centered at `1500 + f δ`. Both normalized to the same area (show shape, not population).
- Vertical line at the cutoff `1500 + z_q σ`, with `z_q = Φ⁻¹(1 − q)`. Shade the area beyond the cutoff under both curves in different patterns.
- A label near the cutoff: "top q: this class ×ratio".

**Controls.**
- `δ` (class advantage): slider −100 to +150 rating points, step 5, default +60.
- `f` (share of the rating's games on this class): slider 0 to 1, step 0.05, default 1.
- Cutoff `q`: segmented control, top 50% / 10% / 1% / 0.1%, default 1%.
- `σ` (skill spread): slider 100 to 300, step 10, default 200.
- Preset buttons: "Per-spec ladder (f = 1)", "Per-player, many champions (f = 0.1)", "Half and half (f = 0.5)".
- All sliders keyboard operable; segmented control uses arrow keys.

**Formulas.**
- `W = 1 / (1 + 10^(−(1 − f) δ / 400))`.
- `shift = f δ`.
- `top share = 1 − Φ(z_q − shift / σ)`, `ratio = top share / q`. Implement `Φ` with a standard erf approximation (Abramowitz and Stegun 7.1.26 is accurate enough) and `Φ⁻¹` with a rational approximation (for example Acklam's), or hard-code `z_q` for the four cutoffs: 0, 1.2816, 2.3263, 3.0902.
- Early-window estimate (show in the panel as an aside): `E(δ)` is the win rate before any absorption.

**Number panel.** `δ`, `f`, `σ`, cutoff; win rate `W` (two decimals); rating shift `f δ`; top share for the class and for everyone (three decimals, as percent); representation ratio (two decimals); "win rate before absorption" `E(δ)`.

**Test values** (`σ = 200`).
- `δ = 60`, `f = 0`: `W = 58.55%`, ratio 1.00 at any cutoff.
- `δ = 60`, `f = 0.5`: `W = 54.31%`, shift 30, top 10% ratio 1.29, top 1% ratio 1.48.
- `δ = 60`, `f = 1`: `W = 50.00%`, shift 60; ratios 1.24 (50%), 1.63 (10%), 2.14 (1%), 2.63 (0.1%); top 0.1% share 0.263%.
- `δ = 80`, `f = 1`: top 1% ratio 2.70, top 10% ratio 1.89, `E(δ) = 61.3%`.
- `δ = −40`, `f = 1`: top 1% ratio 0.58, top 10% ratio 0.69.
- Exact toggle at `δ = 60`, `f = 0.75`: exact `W = 52.15%` against approximate 52.16%.

**Accessibility and style.** Shared palette from `templates/interactive-tokens.css`, copied inline. The two distributions differ by line style and fill pattern as well as color. Respect `prefers-reduced-motion` and `prefers-color-scheme`. No game names, logos, class icons or art in the graphic; labels say "this class" and "everyone else".
