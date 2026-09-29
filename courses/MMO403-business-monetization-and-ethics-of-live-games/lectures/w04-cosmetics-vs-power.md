# MMO403 · Week 04 — Cosmetics vs Power

**Why this matters:** "Is it pay-to-win?" is the first question players ask about any store, and the answer decides whether they trust your game. Teams often answer it by looking at win rates, and in a game with matchmaking that is exactly where a paid advantage hides. This week you learn to measure what a purchased edge is worth, where it shows up, and how to write a store policy you can defend with numbers.

**You will be able to:**
- Classify any store item as cosmetic, convenience, time-saver or power, and name who loses when someone buys it.
- Compute the win chance and the rating-point value of a purchased stat edge from a model of fight noise.
- Predict how a paid edge redistributes a ranked ladder after matchmaking, and explain why win rates do not reveal it.
- Critique a store policy for a PvP and a PvE game, and propose a line between what you sell and what players must earn.

**Before class:** Fields & Cotton, *Social Game Design: Monetization Methods and Mechanics* (Morgan Kaufmann, 2011), the chapters on virtual goods and on the types of items games sell. Reread your notes on expected score from MMO307 week 8.

**Prerequisites from earlier courses:** [MMO307 week 8, Elo and expected score](../../MMO307-game-balance-ii-pvp-progression-and-endgame/lectures/w08-elo-and-expected-score.md) (the curve `E = 1 / (1 + 10^(−D/400))` and why a correctly rated player's expected change is zero). [GD101 week 10, chance vs skill](../../GD101-introduction-to-game-design/lectures/w10-chance-vs-skill-and-randomness.md) (the "skill plus a die" model and how the size of the die sets the value of an edge). [MA102 week 8, dice sums and the normal curve](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w08-dice-sums-and-the-normal-curve.md) (the normal CDF `Φ`). [MMO305 week 7, status and conspicuous display](../../MMO305-social-systems-and-online-behaviour/lectures/w07-status-prestige-and-conspicuous-display.md) (why cosmetics carry value at all). [MMO303 week 3, effective HP and effective DPS](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w03-effective-hp-and-effective-dps.md) (time to kill as HP over DPS).

**Interactive:** [Paid edge ladder](../examples/w04-paid-edge-ladder.html), built from the spec at the end of this lecture. Keep it open during section 2.

---

## 1. Four things a store can sell

Every item in a live game's store falls somewhere on one line. At one end, the item changes only how you look. At the other end, it changes whether you win. In between sit two kinds of item that most arguments are really about.

| Kind | What it changes | Example of the kind | Who loses when you buy it? |
|---|---|---|---|
| Cosmetic | Appearance, sound, animation | A weapon skin, an emote | Nobody in the match. Possibly players who wanted to stand out with the same look. |
| Convenience | Friction outside play | Extra storage, extra character slots, a better trade interface | Nobody directly. Non-buyers carry more friction. |
| Time-saver | How fast you reach something everyone can reach | An XP boost, a character level boost, an early unlock | Players you compete with during the window when you are ahead. |
| Power | What you can do once you are there | A stat bonus, an exclusive weapon, a stronger character | Your opponents, every match. |

The last column is the useful one. Call it the **who-loses test**. For each item, ask which other player is worse off because you paid. If the answer is "nobody", the item is fair in the narrow sense that matters for competition. If the answer is "the player I just beat", you are selling power, whatever the item is called.

Two refinements make the test sharper.

**PvE and PvP differ.** In a raid, a stronger teammate helps you. Selling power there does not take wins from anyone in the fight. It still has costs, which section 4 covers: groups start to expect the paid power, and a bought item that can be traded becomes part of the economy. In PvP, one player's gain is another's loss, match by match. The same +10% damage item is a mild convenience in a solo dungeon and a direct transfer of wins in an arena.

**Time-savers become power when time matters.** An XP boost in a game with no competition just skips content. The same boost at the start of a season race, where the first guild to the level cap gets the first raid kill, sells a head start in a contest. Overwatch 2 is a clean case, covered below. Selling early access to a hero is a time-saver on paper and a power item for every match in which the hero is strong and the non-buyer does not have it.

Most designers accept this line in principle. The trouble starts with the next question. How big does an edge have to be before it matters? Players say "any edge is pay-to-win". Producers say "it's only 5%". Both are guessing. The worked example replaces the guess with a number.

## 2. Worked example: the +10% that hides in the win rate

### The hook

In November 2017, the day before *Star Wars Battlefront II* launched, Electronic Arts switched off all microtransactions in the game. Players in the pre-release period had found that the loot crates sold for real money contained Star Cards, which raise a class's stats such as damage output or health regeneration. EA said it would bring purchases back after changes. On 16 March 2018 the developer DICE announced a new system. Crates would hold only credits and cosmetics, and Star Cards would be earned through play. The first part shipped on 21 March and the rest in April.

Here is the puzzle. Suppose EA had kept the crates, and suppose its analysts had checked the win rate of heavy buyers a few months after launch. In a game with skill-based matchmaking, they would likely have found that buyers won about half their matches, the same as everyone else. Would that prove the crates were fair? It would not, and seeing why is this week's model.

### The model

We need three steps. The first turns a stat edge into a win chance. The second turns the win chance into rating points. The third shows where those points go on a ladder.

**Step 1: stat edge to win chance.** Picture a duel between two players of equal skill. Each fight, each player's time to kill the other (TTK, which in MMO303 week 3 was HP divided by DPS) varies with aim, positioning and luck. Model that variation as a random factor on the log of the time, the same for both players:

```
ln T_buyer = ln T0 − ln(1 + b) + e1
ln T_other = ln T0 + e2
e1, e2 independent, normal, mean 0, standard deviation σ
```

- `b` is the purchased edge, as a fraction. A +10% damage item gives `b = 0.10`, so the buyer kills `1.1` times as fast.
- `σ` is the **fight noise**, the spread of one player's kill time from fight to fight, on a log scale. `σ = 0.25` means a player's kill time is usually within about 25% of their average.
- `T0` is the kill time with no edge. It cancels out.

The buyer wins if they kill first, which happens when `ln T_buyer < ln T_other`. The difference of two independent normals is normal with standard deviation `σ√2`, so

```
p = P(buyer wins) = Φ( ln(1 + b) / (σ √2) )
```

where `Φ` is the standard normal CDF from MA102 week 8. This is the same "skill plus a die" structure you met in GD101 week 10. The edge `ln(1 + b)` plays the role of the skill gap, and `σ√2` plays the role of the die.

**Step 2: win chance to rating points.** MMO307 week 8 gave the Elo expected score, `E = 1 / (1 + 10^(−D/400))`. Solve it for `D` and you get the rating gap that produces a win chance `p` between two players:

```
Δ = 400 × log10( p / (1 − p) )
```

`Δ` is the purchased edge **measured in rating points**. It lets you say "this item is worth 75 Elo" and compare it with anything else that moves a rating.

**Step 3: where the points go.** Now put the edge into a ranked ladder with matchmaking. MMO307 week 8 showed that a player whose rating is correct has an expected rating change of zero. A buyer who is `Δ` stronger than their skill rating wins more than half their games at first, so their rating climbs. It stops climbing when they meet opponents who are `Δ` better than their skill, and there they win half their games again. After the ladder settles, **a buyer's rating is their skill plus `Δ`, and their win rate is 50%**.

That is the whole trick. Matchmaking converts a paid edge into rank. A dashboard that tracks buyers' win rates will show nothing, because matchmaking has already paired them with stronger opponents. The advantage appears in who holds the top ranks.

To measure that, let skill ratings across the population be normal with a spread `s` (we use `s = 200` points, a plausible spread for a ladder of this kind), and let a fraction `f` of players buy the edge. Payers are then distributed as `N(Δ, s)` and non-payers as `N(0, s)`. The share of the top 10% held by payers is found by locating the rating cut-off `t` above which 10% of all players sit, then asking what fraction of those are payers.

### Numbers you can check

Take `σ = 0.25` and a +10% edge. Then `ln(1.1) = 0.0953` and `σ√2 = 0.354`, so `z = 0.0953 / 0.354 = 0.270`. From a normal table, `Φ(0.270) = 0.606`. The buyer wins 60.6% of duels against an equal. Convert: `0.606 / 0.394 = 1.54`, `log10(1.54) = 0.187`, so `Δ = 400 × 0.187 = 75` points.

The code below produces the full table. It runs as shown with `.venv/bin/python`.

```python
from math import erf, log, log10, sqrt

def phi(x):
    return 0.5 * (1 + erf(x / sqrt(2)))

def win_prob(b, sigma):
    """Chance a buyer with a +b damage edge beats an equal-skill non-buyer."""
    return phi(log(1 + b) / (sigma * sqrt(2)))

def rating_gap(p):
    """Elo points that give the same expected score p."""
    return 400 * log10(p / (1 - p))

def payer_share_on_top(delta, f, sd=200, top=0.10):
    """Share of the top `top` of the ladder held by payers after matchmaking."""
    lo, hi = -3000.0, 3000.0
    for _ in range(100):                      # bisection for the cut-off rating
        t = (lo + hi) / 2
        above = (1 - f) * (1 - phi(t / sd)) + f * (1 - phi((t - delta) / sd))
        lo, hi = (t, hi) if above > top else (lo, t)
    return f * (1 - phi((t - delta) / sd)) / top

for b in (0.02, 0.05, 0.10, 0.20):
    p = win_prob(b, sigma=0.25)
    d = rating_gap(p)
    print(f"+{b:.0%}  win {p:.1%}  Elo {d:5.1f}  "
          f"top 10% {payer_share_on_top(d, 0.2):.1%}  "
          f"top 1% {payer_share_on_top(d, 0.2, top=0.01):.1%}")
```

Output:

```
+2%  win 52.2%  Elo  15.5  top 10% 22.2%  top 1% 23.5%
+5%  win 55.5%  Elo  38.3  top 10% 25.8%  top 1% 29.2%
+10%  win 60.6%  Elo  75.0  top 10% 31.9%  top 1% 39.8%
+20%  win 69.7%  Elo 144.7  top 10% 44.8%  top 1% 61.8%
```

In table form, with 20% of players buying (`f = 0.2`), fight noise `σ = 0.25` and a ladder spread of 200 points:

| Edge `b` | Duel win vs equal | Rating value `Δ` | Payers in top 10% | Payers in top 1% | Buyers' win rate after matchmaking |
|---|---|---|---|---|---|
| 0% | 50.0% | 0 | 20.0% | 20.0% | 50% |
| +2% | 52.2% | 15.5 | 22.2% | 23.5% | 50% |
| +5% | 55.5% | 38.3 | 25.8% | 29.2% | 50% |
| +10% | 60.6% | 75.0 | 31.9% | 39.8% | 50% |
| +20% | 69.7% | 144.7 | 44.8% | 61.8% | 50% |

Read the last two columns together. The win-rate column never moves. The top-1% column doubles from 20% to about 40% at +10%, and passes 60% at +20%. The further up the ladder you look, the more the paid edge shows, because the top of a normal distribution is where a small shift changes the most.

Now vary the noise. Keep `b = 0.05` and change `σ`:

| Fight noise `σ` | Duel win vs equal | Rating value `Δ` |
|---|---|---|
| 0.10 (precise, skill-heavy) | 63.5% | 96 |
| 0.25 | 55.5% | 38 |
| 0.50 (swingy, luck-heavy) | 52.8% | 19 |

The same +5% is worth five times as many rating points in a precise game as in a swingy one. "It's only 5%" is not a claim you can check until you know the noise.

Finally, a casual mode with no matchmaking. If buyers are matched at random, a buyer with a 60.6% duel edge faces other buyers 20% of the time and non-buyers 80% of the time. Their win rate is `0.2 × 0.5 + 0.8 × 0.606 = 58.5%`. A non-buyer's is `0.8 × 0.5 + 0.2 × 0.394 = 47.9%`. In unranked play the edge shows in win rates. In ranked play it moves into rank. Either way somebody pays for it.

### Move it yourself

Open `examples/w04-paid-edge-ladder.html`. The left view is the dashboard a producer would see, the win rate of buyers and non-buyers, which sits flat at 50% when matchmaking is on. The right view is the ladder, two overlapping bell curves for buyers and non-buyers, with the top 10% shaded and the payer share printed. Drag the edge slider from 0% to 20% and watch the left view stay flat while the right view fills with buyers at the top. Then drag the noise slider down to 0.10 and watch the same edge push buyers much further up. Turn matchmaking off and the effect jumps from the right view to the left.

### Cross-game recognition

Each of these cases puts a different value of `b` into the same model.

**Star Wars Battlefront II (2017 launch, March 2018 overhaul).** Star Cards raised class stats and came from paid crates at launch, so `b > 0` and purchasable. The overhaul kept the Star Cards and their stat effects but tied them to playing a class, so `b > 0` and earned only. In our model the edge still exists after the change. The difference is who can buy it. Money no longer buys `Δ`, and time spent on a class buys it for everyone at the same rate.

**Overwatch 2 (October 2022 to April 2024).** At launch, new heroes were rewards on the battle pass. Free players unlocked each new hero at a tier deep in the free track, while premium pass buyers got the hero at once. This sells a time-saver, and it becomes power in any match where the new hero is strong. `b` is the value of having the hero, and it applies only during the window before free players reach the unlock tier. Players called it pay-to-win. Blizzard reversed the rule with Season 10 in April 2024, making new heroes free for everyone, and unlocked the earlier pass heroes too.

**Dota 2 (2013 onward).** Every hero is available to every player for free, and Valve sells only items that do not alter gameplay, such as hero cosmetics and audio packs. That is `b = 0` by policy. The design pays for it by selling appearance at very high volume, which only works because the player base is large enough that people see and value each other's looks (section 3).

**Path of Exile (2013 onward).** Grinding Gear Games sells mainly cosmetics, plus account features such as extra stash storage and extra character slots beyond the free maximum. That is convenience. Nothing in a match changes, so the who-loses test says "nobody in the fight". Critics point out that a free player's storage is tight enough that extra tabs feel close to required. The model cannot settle that argument, because it is about friction, not wins. It does tell you the argument is about a different line on the table in section 1.

### Design judgment

The model gives you numbers. The decision is still yours, and it involves more than the numbers.

- **Decide what dashboard would catch a paid edge, before you sell one.** Win rates by payer status will look clean in any mode with matchmaking. Track the payer share of the top 10% and top 1% of every ladder, by season. If it rises above the payer share of the whole population, the store is buying rank.
- **Price the edge in rating points, not percent.** "+5%" means 19 points in one game and 96 in another. Write your store policy in `Δ`, for example "no purchasable item may be worth more than 10 rating points in any ranked mode", and compute `Δ` with the fight noise you measure from telemetry.
- **The top of the ladder is where trust is decided.** Streamers, tournament players and guild leaders live in the top 1%. The table shows that is exactly where a small edge has the largest effect. A game can survive grumbling in the middle of the ladder. It struggles to survive a top 100 that looks bought.
- **A reversal costs more than restraint.** Battlefront II and Overwatch 2 both changed course after launch. Each reversal gave away revenue that had been forecast, and each came after the damage to trust. If your model says an item is power, decide before launch whether you will sell it.
- **Selling power is not automatically wrong.** Many successful games, especially in PvE and in markets where players expect it, sell time and power openly. What makes it defensible is honesty about what is sold and where it applies, and keeping ranked play clean. What makes it indefensible is selling power while saying you do not.

### Check this example

1. With `σ = 0.25`, what duel win chance does a +20% edge give? Show the `z` value.
2. A store item gives 38 rating points. With `f = 0.2` and `s = 200`, what share of the top 10% will be payers after matchmaking? What will their win rate be?

<details>
<summary>Answers</summary>

1. `ln(1.2) = 0.182`, `z = 0.182 / 0.354 = 0.516`, `Φ(0.516) = 0.697`, so 69.7%.
2. From the table, about 25.8%. Their win rate settles at 50%, the same as everyone's, because the edge has become rank.

</details>

## 3. Cosmetics are not free of consequences

A cosmetic-only store passes the who-loses test for matches. It does not settle every question.

**Cosmetics sell status, and status needs an audience.** MMO305 week 7 showed that a display item is valuable because other players see it and read something from it. That has two business consequences. First, cosmetic revenue grows with the number of people who see each item, so cosmetic-only models favor games with large, visible, social player bases and struggle in small or solo games. Second, anything that makes items less rare makes each one less valuable as a signal. A studio that sells many copies of a "rare" look is spending the status of everyone who already owns it. MMO305's worked example on badge dilution is the same effect seen from the player's side.

**Some cosmetics change what other players can see.** A dark, low-contrast outfit on a dark map is harder to spot. A skin that changes a weapon's firing effects can make its range or timing harder to read. A slimmer character model can look like a smaller target even when the hitbox is the same. Competitive shooters handle this by reviewing skins for visibility and by keeping hitboxes identical across skins. In our model, a cosmetic that hides you adds a small `b` in exactly the modes where noise is lowest. Review every cosmetic for the gameplay information it hides or adds.

**Cosmetic-only does not mean ethics solved.** How a cosmetic is sold matters as much as what it is. A cosmetic sold for a fixed price with the item shown up front raises few concerns. The same cosmetic sold through a random box, a countdown timer or a premium currency with an awkward exchange rate raises all the questions weeks 3, 6 and 8 deal with. "We only sell cosmetics" answers the fairness question. It does not answer the manipulation question.

## 4. Power outside the arena: PvE and the economy

Many MMOs sell things that never touch a duel: XP boosts, level boosts, crafting speed, extra daily attempts. The duel model does not apply, but the who-loses test still does. Three effects are common.

**Expectations move.** If a purchasable boost makes a raid noticeably easier, raid leaders start to expect it. A player who does not buy it is then a weaker applicant for a group. This is a PvE version of the ladder effect. Nobody's win rate against the boss changes much, but the social cost of not paying rises. Watch for group-finder rules, guild requirements and forum guides that treat a paid item as standard.

**Tradeable power becomes currency.** If a bought item or boost can be traded, its effect enters the player economy. Players who never pay can buy it from those who do, and the store price becomes a ceiling on its market price. That is sometimes a deliberate design, and week 11 studies the most important version, subscription tokens. It also means a store change moves prices in your economy, which MMO308 week 12 taught you to monitor.

**Content length becomes a sales lever.** If the store sells a way to skip the grind, every designer who tunes the grind is, in effect, tuning demand for that product. That conflict of interest is real even when the team is well-meaning. A common safeguard is to set progression targets before the store team prices the skip, and to review them with the store numbers hidden.

A practical store policy for an MMO usually draws two lines. One line says what is sold in PvP modes (typically cosmetics only). The other says what is sold elsewhere, and how the team will measure whether it has become expected. Write both down and publish the first.

## In-class activity (25 minutes)

Work in groups of three. Each group gets one of these proposed store items for a fantasy MMO with a ranked arena and a raid game.

- A. A mount that is 10% faster than the fastest earnable mount.
- B. A "rested XP" potion that doubles XP gain for 7 days.
- C. A cosmetic armor set with a dark, matte finish.
- D. Early access to a new class, 14 days before it unlocks for free.

1. Place the item on the four-kind line and run the who-loses test separately for the arena and the raid game.
2. For the arena, estimate `b` for the item in the worst case (for D, assume the new class has a 5% edge over the average class in its first two weeks). With `σ = 0.25`, compute the duel win chance and `Δ`.
3. Decide whether to sell it, change it, or drop it. Write one sentence of policy that would cover similar items in future.
4. Name the dashboard metric you would watch for three months after launch.

Expected output: a filled row per item (kind, who loses, `b`, `Δ`, decision) and one policy sentence per group, read out to the class.

## Common misconceptions

- **"Buyers' win rate is 50%, so the store is fair."** In a matchmade mode, a buyer's win rate always drifts back to 50%. The edge shows up as rank. Look at the payer share of the top of the ladder.
- **"5% is too small to matter."** Its value depends on fight noise. With `σ = 0.10`, +5% is worth 96 rating points, enough to move a median player from the 50th to about the 68th percentile.
- **"Cosmetic-only means no ethical questions."** It answers the fairness question for matches. How cosmetics are sold, and whether some carry gameplay information, are separate questions.
- **"Power in PvE hurts nobody."** It changes what groups expect, and tradeable power changes the economy. The harm is social and economic, not a lost duel.

## Check yourself

1. A game has fight noise `σ = 0.40`. A store item gives +8% damage. Compute the duel win chance against an equal player and the rating value `Δ`.
2. Your analytics team reports that in ranked play buyers of a stat item win 50.4% of matches and non-buyers 49.9%. The producer concludes the item has no effect. What would you measure instead, and what result would change your mind?
3. In an unranked mode with random opponents, 30% of players own an item that gives a 60% duel win chance against non-owners. What are the owners' and non-owners' overall win rates?
4. A designer argues that selling early access to a new character is "just a time-saver". Using the who-loses test and the model, state when that is true and when it is not.

<details>
<summary>Answers</summary>

1. `ln(1.08) = 0.0770`, `σ√2 = 0.566`, `z = 0.136`, `Φ(0.136) = 0.554`, so 55.4%. `Δ = 400 × log10(0.554 / 0.446) = 400 × 0.094 ≈ 38` points.
2. Win rates will be near 50% under matchmaking whatever the item does. Measure the share of buyers in the top 10% and top 1% of the ladder, compared with their share of the population. If buyers are 20% of players and 30% or more of the top 10%, the item is buying rank.
3. Owners face owners 30% of the time and non-owners 70%: `0.3 × 0.5 + 0.7 × 0.6 = 57%`. Non-owners: `0.7 × 0.5 + 0.3 × 0.4 = 47%`.
4. It is a time-saver if the character has no advantage over the rest of the roster during the early-access window, or if the window only affects unranked or PvE play. It is power if the character is stronger than average in ranked play during the window, because opponents without access lose matches to it. In the model, `b` is the character's edge and it applies for the length of the window.

</details>

## Lab / assignment hook

[Lab 04, measure a paid edge](../labs/lab04.md). You implement the win-chance, rating-gap and ladder-share functions, then run a full Elo ladder simulation in which 20% of players buy an edge. You confirm that buyers' win rates return to 50% while their share of the top of the ladder rises, and you write a one-page store policy in rating points. The analysis feeds the ethics analysis assignment (20%).

## Sources

- Wikipedia, "Star Wars Battlefront II (2017 video game)", section on the microtransactions controversy (accessed September 2026). Star Cards as the main stat progression; microtransactions disabled the day before the 17 November 2017 release; DICE's 16 March 2018 overhaul announcement making crates credits and cosmetics only, with part one released 21 March and part two in April 2018.
- Wikipedia, "Overwatch 2" and "Battle pass" (accessed September 2026). New heroes on the battle pass from the October 2022 launch; the change with Season 10 in April 2024 making new and earlier pass heroes free for all players.
- Wikipedia, "Dota 2" (accessed September 2026). Free-to-play since the 2013 release; revenue from the Dota Store and Dota Plus selling items that do not alter gameplay.
- Wikipedia, "Path of Exile" (accessed September 2026). Free-to-play since January 2013; mainly cosmetic purchases, with account features such as public trade storage and extra character slots beyond the default maximum sold separately.
- Elo, A. (1978). *The Rating of Chessplayers, Past and Present*. Arco. The expected-score curve used in step 2, as taught in MMO307 week 8.
- Fields, T. & Cotton, B. (2011). *Social Game Design: Monetization Methods and Mechanics*. Morgan Kaufmann. Chapters on virtual goods.
- The fight-noise model, the 20% payer share and the ladder spread of 200 points are teaching assumptions, not measurements from any game. Replace them with your own telemetry.

## Interactive spec: examples/w04-paid-edge-ladder.html

**The one insight.** Under matchmaking a paid edge is invisible in win rates and fully visible in who holds the top of the ladder. Without matchmaking it shows in win rates instead. Either way it goes somewhere.

**Layout.** Two linked views side by side at 1280px, stacked at 390px. Left: "What the dashboard shows", two vertical bars (buyers, non-buyers) of win rate from 30% to 70%, with a dashed 50% line and values printed on top. Right: "What the ladder shows", two overlapping normal density curves on a rating axis from −800 to +800: non-buyers `N(0, s)` scaled by `1 − f`, buyers `N(Δ, s)` scaled by `f`. Shade the region above the top-10% cut-off `t`, split by color and hatch pattern into buyer and non-buyer area. Print the payer share of the top 10% and top 1% above the curve. Below both, a one-line chain readout: `b → p → Δ`.

**Controls (all update instantly).**
- Edge `b`, 0% to 30% in 1-point steps, default 10%.
- Fight noise `σ`, 0.05 to 0.60 in 0.01 steps, default 0.25.
- Payer share `f`, 1% to 60% in 1-point steps, default 20%.
- Ladder spread `s`, 100 to 400 in steps of 10, default 200.
- Matchmaking toggle, on by default.
- Reset button.

**Formulas.**
- `p = Φ( ln(1 + b) / (σ √2) )`, with `Φ` computed from an `erf` approximation accurate to 1e-7 (Abramowitz and Stegun 7.1.26 or better).
- `Δ = 400 × log10(p / (1 − p))`.
- Cut-off `t` solves `(1 − f)(1 − Φ(t/s)) + f(1 − Φ((t − Δ)/s)) = q` by bisection on `[−3000, 3000]`, 100 iterations, for `q = 0.10` and `q = 0.01`.
- Payer share of top `q` = `f(1 − Φ((t − Δ)/s)) / q`.
- Matchmaking on: both win-rate bars show 50.0%, and the ladder shows buyers shifted by `Δ`. Matchmaking off: buyer win rate `f × 0.5 + (1 − f) × p`, non-buyer win rate `(1 − f) × 0.5 + f × (1 − p)`, and the ladder view greys out with the note "no rating ladder in this mode".

**Readouts.** `p` (one decimal percent), `Δ` (one decimal), payer share of top 10% and top 1% (one decimal percent), buyer and non-buyer win rates. When matchmaking is on and payer share of top 1% exceeds `2f`, print "Buyers hold twice their share of the top 1%".

**Test values.**
- Defaults: `p = 60.6%`, `Δ = 75.0`, top 10% share 31.9%, top 1% share 39.8%, both win rates 50.0%.
- `b = 5%`: `p = 55.5%`, `Δ = 38.3`, top 10% 25.8%, top 1% 29.2%.
- `b = 20%`: `p = 69.7%`, `Δ = 144.7`, top 10% 44.8%, top 1% 61.8%.
- `b = 5%`, `σ = 0.10`: `p = 63.5%`, `Δ = 96.2`. `σ = 0.50`: `p = 52.8%`, `Δ = 19.1`.
- Defaults with matchmaking off: buyer win rate 58.5%, non-buyer 47.9%.
- `b = 0`: `Δ = 0`, both shares equal `f`.

**Accessibility and style.** Native range inputs with visible labels and numeric outputs; the toggle is a real checkbox. Buyers and non-buyers differ by hatch pattern as well as color. Colors from `templates/interactive-tokens.css`. No game art, logos or characters.
