# MA102 · Week 10 — Pseudo-random distribution and pity timers

**Why this matters:** A fair die can still hand one player ten misses in a row, and that player will call your game broken. This week you learn the tools shipped games use to keep the average rate the same while controlling the streaks, and how to calculate what each tool costs.

**You will be able to:**
- Compute the gap distribution, mean gap and worst case for a pseudo-random (PRD) effect, given its constant C.
- Derive the expected number of pulls under a hard or soft pity rule and check it against a published "consolidated" rate.
- Compare independent rolls, PRD, pity counters and shuffle bags on long-run rate, spread and worst case.
- Design a pity rule for a drop of a given rate and defend its parameters.

**Before class:** Schreiber, *Game Balance Concepts* (2010 blog course), Level 5, "Probability and Randomness Gone Horribly Wrong", the sections on player perception and pseudo-randomness. Schreiber & Romero, *Game Balance* (2021), the probability chapters, sections on dependent events.

**Prerequisites from earlier courses:** [MA102 week 7, geometric distribution](w07-geometric-distribution-kills-until-the-drop.md), [week 5, variance](w05-variance-and-swingy-designs.md), [week 4, expected value](w04-expected-value-comparing-weapons.md) and [week 2, the gambler's fallacy](w02-independent-events-and-the-gamblers-fallacy.md). [Week 9, weighted loot tables](w09-weighted-tables-and-loot-table-design.md) is where pity attaches. Powers and running totals from [MA101 week 4](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w04-exponentials-and-the-xp-curve.md).

**Interactive:** [examples/w10-prd-streaks.html](../examples/w10-prd-streaks.html) for section 2 and [examples/w10-gacha-pity.html](../examples/w10-gacha-pity.html) for section 4.

---

## 1. Independent rolls make streaks, and players remember streaks

In week 7 you modeled "attacks until the effect fires" with the geometric distribution. If an effect fires with probability `p` on every attack, independently of every other attack, then the number of attacks `N` until it fires has

```
P(N = n) = (1 − p)^(n − 1) × p
E[N]     = 1 / p
SD[N]    = sqrt(1 − p) / p
```

Take `p = 0.25`, a 25% stun on hit. The mean gap is 4 attacks. The standard deviation is `sqrt(0.75) / 0.25 ≈ 3.46` attacks, almost as large as the mean. That is the geometric distribution's signature. It is memoryless, so a long drought tells you nothing about the next roll, and droughts are common.

Two numbers make this concrete.

- The chance of 10 attacks in a row with no stun is `0.75^10 ≈ 5.6%`, about 1 in 18 droughts of that length.
- The chance that the stun fires on two attacks in a row is `0.25`. One in four stuns is immediately followed by another.

Now scale up. A match has hundreds of attacks per hero. A popular game runs millions of matches a week. "One in 18" is not a rare event. It happens to thousands of players every hour, and every one of them experiences it as the game being unfair. The back-to-back stuns feel just as bad from the other side.

A designer can respond in two ways. You can accept the variance and let it be part of the game's texture, which works when the stakes of a single roll are low. Or you can keep the long-run rate and change the shape of the gap distribution. This lecture is about the second option. The three tools you will meet are:

- **Pseudo-random distribution (PRD).** The chance rises with every failure and resets on success.
- **Pity counter.** Rolls stay independent until a counter forces a success (hard pity) or ramps the chance up (soft pity).
- **Shuffle bag.** Draw outcomes without replacement from a bag that holds exactly the right proportion of successes.

All three make trials **dependent**. That word matters. The gambler's fallacy from week 2 says "I'm due" is wrong for independent rolls. Under these systems, "I'm due" is correct. That is the whole point of them.

## 2. Worked example: Dota 2's pseudo-random bash

### The hook

In Dota 2, many chance-on-hit effects are listed with a fixed percentage. A 25% bash is the standard wiki example. Yet on the first attack after a bash, the real chance is only about 8.5%. After one miss it is about 17%, then about 25.4%, and it keeps climbing. Over a long fight the bash still lands on 25% of attacks. Players who track their attacks notice that bashes almost never come back to back and never vanish for long. Nothing on the tooltip tells you this.

### The model

Valve's system, inherited from the Warcraft III engine, is called pseudo-random distribution. Let `N` count attacks since the last proc (a proc is the effect firing). The chance on the `N`th attack is

```
P(proc on attack N | no proc since reset) = min(1, C × N)
```

- `C` is a constant chosen per nominal chance. It is both the first-attack chance and the step added after each failure.
- When the effect fires, `N` resets to 1.
- Once `C × N ≥ 1`, the proc is guaranteed. So the longest possible gap is `ceil(1 / C)` attacks.

Why is `C` smaller than the nominal 25%? Because the chance keeps rising, the process fires sooner on average than a flat `C` would. The designer needs the mean gap to equal `1 / p = 4` attacks, so the long-run proc rate is exactly `p`. The probability that the first proc lands on attack `n` is

```
P(N = n) = [ (1 − C)(1 − 2C)…(1 − (n − 1)C) ] × min(1, nC)
```

and we need `Σ n × P(N = n) = 1 / p`. There is no neat algebraic solution for `C`. You find it numerically, by trying a value, computing the mean gap, and nudging `C` up or down (bisection). Next week's Monte Carlo lecture shows a second way to check it. The published table gives, for 25%, `C ≈ 0.084744`.

### Numbers you can check

With `C = 0.0847`, compute the per-attack chance, the chance the proc first lands on that attack, and the running total. Row 3, for example: the chance of reaching attack 3 is `(1 − 0.0847)(1 − 0.1695) ≈ 0.7601`, and `0.7601 × 0.2542 ≈ 0.1932`.

| Attack since last proc | Chance on this attack | P(first proc here) | Cumulative |
|---|---|---|---|
| 1 | 8.47% | 8.47% | 8.47% |
| 2 | 16.95% | 15.51% | 23.99% |
| 3 | 25.42% | 19.32% | 43.31% |
| 4 | 33.90% | 19.22% | 62.53% |
| 5 | 42.37% | 15.88% | 78.41% |
| 6 | 50.85% | 10.98% | 89.39% |
| 7 | 59.32% | 6.30% | 95.68% |
| 8 | 67.80% | 2.93% | 98.61% |
| 9 | 76.27% | 1.06% | 99.67% |
| 10 | 84.74% | 0.28% | 99.95% |
| 11 | 93.22% | 0.05% | 99.997% |
| 12 | 100% | ≈0.003% | 100% |

Now put the two systems side by side. Both have a long-run rate of exactly 25%.

| Measure | Independent 25% | PRD, C = 0.0847 |
|---|---|---|
| Mean gap (attacks) | 4.00 | 4.00 |
| SD of gap | 3.46 | 1.90 |
| Chance of back-to-back procs | 25% | 8.5% |
| P(gap ≥ 8 attacks) | 13.3% | 4.3% |
| P(10 misses, then gap ≥ 11) | 5.6% | 0.05% |
| Longest possible gap | unbounded | 12 |

Read the last three rows carefully. A 10-attack drought goes from 1 in 18 to about 1 in 2,000. Back-to-back procs drop by a factor of three. The mean does not move at all. The spread of the gap is cut almost in half.

The same pattern holds at every nominal rate. Here are a few values from the Dota 2 table, with the standard deviations you can compute from the formula above:

| Nominal p | C | Longest gap | SD of gap (PRD) | SD of gap (independent) |
|---|---|---|---|---|
| 10% | 0.01475 | 68 | 5.06 | 9.49 |
| 20% | 0.05570 | 18 | 2.43 | 4.47 |
| 25% | 0.08474 | 12 | 1.90 | 3.46 |
| 40% | 0.20155 | 5 | 1.08 | 1.94 |
| 50% | 0.30210 | 4 | 0.81 | 1.41 |

For 10%, the guarantee sits at `ceil(1 / 0.01475) = 68` attacks, but the chance of getting that far is so small it rounds to zero. In practice, about 1 gap in 160 reaches 25 attacks and about 1 in 2,000 reaches 30.

### Move it yourself

Open [examples/w10-prd-streaks.html](../examples/w10-prd-streaks.html). The top view is a strip of 100 attacks rolled under both systems from the same button press. Independent rolls cluster and leave holes. PRD rolls look like a picket fence with jitter. The bottom view is the gap histogram for both. Drag the nominal-chance slider. The two histograms always have the same mean, marked with a shared line, but the independent one keeps a long tail and the PRD one stays compact and cuts off at `ceil(1/C)`. Same average, different feel. That is the insight to take away.

### Same idea elsewhere

Rewrite each of these into one form, "the chance on this trial depends on what happened since the last success".

**Warcraft III.** The Dota 2 mechanic comes from the Warcraft III engine, where the original Dota was a custom map. Same model, older engine. The Liquipedia page still lists legacy values from the original Warcraft III map alongside the Dota 2 table.

**Tetris (Guideline games).** Modern Tetris games that follow the Tetris Guideline use the "Random Generator", known to players as the 7-bag. Each bag holds exactly one of each of the seven pieces, shuffled. When the bag empties, a new one is shuffled. The chance of an I piece on the next draw depends on how many pieces have been drawn from the current bag and whether the I has already come out. It rises to 1 when it is the last piece left. The longest possible wait between two I pieces is 12 pieces (I first in one bag, last in the next). Under independent draws with `p = 1/7`, a 12-piece drought has probability `(6/7)^12 ≈ 16%`, and longer ones are always possible.

**Fire Emblem (Game Boy Advance era).** This one is a contrast. Starting with *The Binding Blade* (2002), the series rolled two random numbers from 0 to 99 and compared their average to the displayed hit rate. The trials are still independent. What changes is the per-trial rate. A displayed 75 hits about 87.8% of the time, a displayed 90 about 98.1%, and a displayed 25 only about 12.8%. It reduces the pain of missing a "sure" shot, which is the same player complaint PRD answers, but it does so by making the tooltip less honest instead of making trials depend on history. Compare the MMO303 discussion of what a tooltip shows versus what the game computes, in [MMO303 week 2](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w02-armor-and-damage-mitigation.md).

Three games and three mechanisms share one goal. Each keeps the average and reshapes the extremes.

### Design judgment

PRD is a strong default for frequent, visible, per-hit effects. Before you use it, decide these points deliberately.

- **It needs state.** Every unit and every effect carries its own counter. That is cheap on one machine but must be replicated and kept authoritative on a server. In an MMO with thousands of entities, it is a real cost.
- **It can in principle be farmed.** If a player can make failed attempts cheaply (hitting creeps before turning to a hero), they can "charge up" a proc. Liquipedia notes that this works in theory and is "nearly impossible" in practice, and that failures against targets where the effect cannot apply do not advance the counter. Your spec must say which attempts count.
- **It changes what 25% means.** The tooltip number is a long-run rate, not a per-attack chance. For most players this is fine. For theorycrafters, publish the rule.
- **It does little for rare events.** PRD shines when `p` is between about 10% and 50%. For a 1% drop, the ramp is so slow that the gap distribution still has a long tail. Rare events need a counter with a hard cap, which is section 3.

### Check this example

1. A 20% effect uses `C = 0.0557`. What is its guaranteed-by attack, and what is the chance of the effect on the first attack after a proc?
2. For the same 20% effect with independent rolls, what is the chance of a gap of 18 or more attacks?

<details>
<summary>Answers</summary>

1. `ceil(1 / 0.0557) = ceil(17.95) = 18` attacks. The first-attack chance is `C = 5.57%`.
2. The first 17 attacks must all miss: `0.8^17 ≈ 2.3%`. Under PRD that probability is effectively zero.

</details>

## 3. Pity counters: hard and soft

PRD ramps from the first trial. A **pity counter** leaves the base rate alone for most of the run and only intervenes near the end. It counts consecutive failures, which players call "pity".

- **Hard pity** at `H`: rolls are independent at rate `p` until trial `H`, which is a guaranteed success. The counter then resets.
- **Soft pity** starting at `S`: from trial `S` onward, the chance rises by a step `d` per trial until it reaches 1, usually at the hard pity.

Hard pity alone has a clean expected value. The chance of still waiting after `k` trials is `(1 − p)^k`, and the expected wait is the sum of those survival chances:

```
E[N] = Σ_{k=0}^{H−1} (1 − p)^k = (1 − (1 − p)^H) / p
```

Example with made-up numbers. Suppose a card pack has a 5% chance of a top-rarity card and a hard pity at 40 packs. Then

```
E[N] = (1 − 0.95^40) / 0.05 = (1 − 0.1285) / 0.05 ≈ 17.4 packs
P(reach the pity pack) = 0.95^39 ≈ 13.5%
```

Pity trims the mean from 20 to 17.4 packs. More important, it caps the worst case. About one player in seven reaches the pity pack, so the rule is not a rare safety net. It shapes a large share of the population's experience.

With soft pity there is no neat closed form. You compute the per-trial chances in a table and sum, exactly as you did for PRD. That is the next worked example.

## 4. Worked example: gacha pity and the published 1.6%

### The hook

*Genshin Impact* (HoYoverse, 2020) publishes its odds in-game. On its main banners, a 5-star item has a base probability of 0.6% per pull, a "consolidated probability (including guarantee)" of 1.6%, and a guarantee of at least one 5-star within 90 pulls. One in 62.5 pulls sounds generous. But ask players when their 5-star arrived, and most will say "somewhere after 74". Both are true. By the end of this example you will see why, and you will see how the published numbers let you check a pity model the developer never documented.

### The model

The developer publishes the base rate, the consolidated rate and the hard pity. It does not publish how the chance rises before 90. Community datasets built from millions of player-submitted pull histories (for example the Paimon.moe tracker) show a sharp jump after pull 73. The widely used community model is:

```
p_n = 0.006                      for n = 1 … 73
p_n = 0.006 + 0.06 × (n − 73)    for n = 74 … 89
p_90 = 1
```

- `n` is the pull number since the last 5-star.
- `p_n` is the chance that pull `n` gives a 5-star, given none so far.
- The soft pity starts at 74 and adds about 6 percentage points per pull.

This is a community estimate, not an official formula. Treat it as a hypothesis. The expected-value tools from week 4 let you test it.

The expected number of pulls is again the sum of survival chances:

```
E[N] = Σ_{k=0}^{89} P(no 5-star in the first k pulls)
     = Σ_{k=0}^{89} Π_{n=1}^{k} (1 − p_n)
```

and the long-run rate is `1 / E[N]`.

### Numbers you can check

The chance of surviving the first 73 pulls is `0.994^73 ≈ 0.6445`. So 35.6% of players get their 5-star at the base rate, and 64.4% enter soft pity. From there the table ramps fast.

| Pull n | Chance on this pull | P(5-star lands here) | Cumulative |
|---|---|---|---|
| 1 | 0.6% | 0.60% | 0.6% |
| 50 | 0.6% | 0.45% | 26.0% |
| 73 | 0.6% | 0.39% | 35.6% |
| 74 | 6.6% | 4.25% | 39.8% |
| 75 | 12.6% | 7.58% | 47.4% |
| 76 | 18.6% | 9.79% | 57.2% |
| 77 | 24.6% | 10.53% | 67.7% |
| 78 | 30.6% | 9.88% | 77.6% |
| 80 | 42.6% | 6.05% | 91.8% |
| 85 | 72.6% | 0.18% | 99.93% |
| 90 | 100% | ≈0% | 100% |

Now the headline numbers, computed by summing the survival column. The no-pity mean is `1 / p = 166.7`. The interactive's "No pity" preset uses a hard cap at pull 1000 as a stand-in for "never", which cuts off the 0.25% of players who would wait past 1000 pulls and shows 166.26 instead.

| Rule | Expected pulls | Long-run rate | Median pull | P(reach pull 90) |
|---|---|---|---|---|
| No pity, 0.6% forever | 166.7 | 0.60% | 116 | — |
| Hard pity at 90 only | 69.7 | 1.43% | 90 | 58.5% |
| Soft pity at 74 (+6%/pull) + hard 90 | 62.3 | 1.605% | 76 | ≈0% |

Look at the second row. With hard pity alone, the long-run rate would be 1.43%, not the published 1.6%. The 0.6% base rate plus a 90-pull guarantee cannot produce 1.6% by themselves. Something must raise the chance before pull 90. The community soft-pity model lands on 1.605%, which rounds to the published figure. The official numbers and the player data agree. That is how you test an undocumented rule. Compute the expected value it implies and compare it with the one number the developer did publish.

Look also at the mean and the median. The mean is 62.3 pulls, the median 76. The distribution has a long flat stretch of early lucky pulls, then a spike. The consolidated rate is honest about the average and silent about the typical player. Week 12 returns to this gap between mean and median.

### Move it yourself

Open [examples/w10-gacha-pity.html](../examples/w10-gacha-pity.html). The left view plots `p_n`, the per-pull chance, as a line that sits on the floor and then climbs a ramp. The right view plots the distribution of the pull on which the 5-star lands, with the mean and median marked. Sliders set the base rate, the soft-pity start, the step and the hard pity. The readout shows expected pulls and consolidated rate next to the published 1.6% target. Move the soft-pity start from 74 down to 60 and watch the spike slide left while the mean drops to about 53 pulls (53.1 with the +6 step). Turn soft pity off and watch 58.5% of the population pile up on pull 90.

### Same idea elsewhere

**Hearthstone card packs.** Blizzard has confirmed that a Legendary card is guaranteed within 40 packs of the previous one in the same set, and that an Epic is guaranteed within 10 packs. Since *Knights of the Frozen Throne* (2017), the first 10 packs of a new set also guarantee a Legendary. These are hard-pity counters, one per rarity and per set. Written in our form, `p_n = p` for `n < 40` and `p_40 = 1`.

**Dota 2 PRD, seen again.** PRD is soft pity that starts at trial 1. The rule `p_n = C × n` is our soft-pity formula with `S = 1`, base rate 0 and step `C`. The gacha model and the Dota model are two settings of the same three knobs: where the ramp starts, how steep it is, and where it hits 1.

**Tetris 7-bag.** A bag of seven is a pity counter for every piece at once, with the guarantee at the end of each bag.

### Design judgment

Pity changes spending and planning, so choose each parameter with that in mind.

- **The hard cap is a promise about the worst case.** It turns "you might never get it" into a known maximum cost. In a game that sells pulls, that maximum is the most important number on the page, and players will plan around it.
- **Soft pity moves the typical experience.** In the model above, almost everyone who reaches pull 74 gets the 5-star by pull 82. The experience is "save up about 75 pulls", not "1.6% per pull". If you want players to feel the base rate, keep the soft pity late and gentle.
- **Pity creates a sunk-cost cliff.** A player at pull 70 knows the ramp is close and is pushed to keep pulling. That is a design lever with ethical weight when real money is involved. MMO403 covers the business and ethics side in depth (see the [MMO403 syllabus](../../MMO403-business-monetization-and-ethics-of-live-games/syllabus.md)).
- **Publish what you compute.** The consolidated rate hides the shape. A clear statement of the counter rule treats players as adults and saves your community from reverse-engineering it.

### Check this example

1. Under hard pity only at 90 with a 0.6% base rate, what fraction of players reach pull 90? Show the calculation.
2. A designer wants the consolidated rate to reach about 1.86%. The interactive shows that soft pity starting at 60 with a 4-point step gives about 53.9 expected pulls. Is that on target?

<details>
<summary>Answers</summary>

1. They must miss 89 pulls: `0.994^89 ≈ 0.585`, so 58.5%.
2. `1 / 53.9 ≈ 1.855%`. Yes, that is about 1.86%.

</details>

## 5. Choosing a variance-control tool

Every tool in this lecture keeps the long-run rate and trades something for a tighter gap distribution. Put them in one table before you pick.

| Tool | Long-run rate | Worst case | State to store | Player can see it? | Typical use |
|---|---|---|---|---|---|
| Independent roll | exact | unbounded | none | — | low-stakes, frequent events |
| PRD (`C × N`) | exact if C is solved | `ceil(1/C)` | counter per effect | rarely | crits, bashes, evasion |
| Hard pity | raised slightly | `H` trials | counter per player | often shown | rare drops, card packs |
| Soft pity | raised more | `H` trials | counter per player | inferred | premium pulls |
| Shuffle bag | exact | bag size limits it | the bag contents | often learned | piece or card sequences |

Two questions decide most cases.

1. **How often does the event happen, and how much does one outcome matter?** A crit every few seconds wants PRD. A 1% raid drop wants a counter with a cap.
2. **Should players be able to plan around it?** Visible pity invites planning and saving. Hidden PRD invites trust but not strategy. Neither is wrong. Choose on purpose.

A note on pity for loot in an MMO. A counter per player per item is a lot of state if your loot tables have thousands of entries. Many games apply pity at the level of a rarity tier or a boss, not each item. That choice decides whether "bad luck protection" feels personal or generic. Week 9's weighted tables are where you would attach it.

## In-class activity (25 minutes)

Work in pairs. Your game has a raid boss whose mount drops at 1% per kill, one kill per week per player.

1. Compute the expected number of weeks and the chance a player still lacks the mount after 150 weeks under independent rolls. (Use the complement rule from week 3.)
2. Propose a hard pity `H` so that no player waits longer than two years of weekly kills. Compute the new expected wait with `E = (1 − 0.99^H) / 0.01`.
3. Propose a soft pity instead, with a start `S` and step `d`. Use the gacha interactive with the base rate set to 1% and report the expected weeks and the median.
4. Write two sentences on which version you would ship and why.

Expected output: a small table of the three rules with mean, median and worst case, plus your two sentences. Swap with another pair and find one way their players might feel cheated.

## Common misconceptions

- **"PRD makes a 25% effect proc more often."** It does not. `C` is solved so the long-run rate is exactly 25%. It changes spread, not mean.
- **"The consolidated 1.6% means I'll get a 5-star around pull 62."** 62.3 is the mean. The median is 76, and 64% of players go past pull 73.
- **"'I'm due' is always the gambler's fallacy."** Only for independent trials. Under PRD, pity or a shuffle bag, a drought really does raise the next chance. Knowing which system you are in is the whole question.
- **"Hard pity at 90 means the rate is 1 in 90."** The guarantee caps the worst case. The expected wait depends on the base rate and any soft pity, and it is well below 90.

## Check yourself

1. A 30% PRD effect uses `C = 0.1189`. What is the longest possible gap? What is the chance the effect fires on each of the first three attacks after a proc (given none yet)?
2. A drop has a 2% rate and a hard pity at 60. Compute the expected number of attempts and the chance of reaching the pity attempt.
3. Using only the published *Genshin Impact* numbers (0.6% base, 90-pull guarantee, 1.6% consolidated), explain why you know the chance must rise before pull 90.
4. A designer says "PRD and a shuffle bag are the same thing." Name one situation where they behave differently.

<details>
<summary>Answers</summary>

1. `ceil(1 / 0.1189) = ceil(8.41) = 9` attacks. Chances are 11.9%, 23.8% and 35.7%.
2. `E = (1 − 0.98^60) / 0.02 = (1 − 0.2976) / 0.02 ≈ 35.1` attempts. Reaching attempt 60 needs 59 misses: `0.98^59 ≈ 30.4%`.
3. With 0.6% flat and a guarantee at 90, the expected pulls are `(1 − 0.994^90) / 0.006 ≈ 69.7`, a rate of 1.43%. The published 1.6% needs about 62.5 expected pulls, so some pulls before 90 must have a higher chance.
4. A bag guarantees exact proportions within each bag, so it also limits how many successes can cluster (at most two in a row for a 1-in-7 piece, at a bag boundary). PRD resets after each success and allows back-to-back procs at chance C. Also, a bag with several success types (seven pieces) tracks all of them at once, while PRD tracks one effect.

</details>

## Lab hook

**[Lab 10: Design a bad-luck protection rule](../labs/lab10.md).** You implement independent, PRD and pity rules in a notebook, solve `C` by bisection, and pick a rule for a loot drop with a written justification. The simulation code you write here is reused in lab 11.

## Sources

- Liquipedia Dota 2 Wiki, "Random Distribution" (Dota 2, re-read September 2026). https://liquipedia.net/dota2/Random_Distribution. The `P(N) = C × N` rule, the table of C values from 5% to 95%, the 25% bash worked example, the note that failed attempts on invalid targets do not advance the counter, and the legacy table from the original Warcraft III DotA map.
- Diplograph, "The Dota 2 Pseudo-Random Distribution Creates Semi-Consistent Effects" (notes on Dota 2 PRD). Origin in the Warcraft III engine.
- HoYoverse, *Genshin Impact* in-game wish "Details" page (versions 1.x to 7.x). Base 0.600%, consolidated 1.600%, 5-star guaranteed at least once per 90 pulls. The official event wish notices on genshin.hoyoverse.com (for example the Version 7.1 notice, September 2026) do not print the rates and send players to this in-game page. The figures were cross-checked against KeqingMains and community wikis, since the in-game page cannot be fetched from outside the game.
- Paimon.moe community wish tracker and the Genshin Impact Fandom community analyses of pull histories (2021 onward). Source of the community soft-pity model starting at pull 74 with about 6 percentage points per pull. This is a community estimate, labelled as such in the text. KeqingMains Theorycrafting Library, "Gacha" (accessed September 2026), gives the same 0.6% base, 90-pull guarantee and soft pity from pull 74.
- Hearthstone Wiki (hearthstone.wiki.gg), "Card pack" (accessed September 2026), citing Blizzard's March 2023 statement on pack rules. Epic within 10 packs, Legendary within 40 packs, first-10-packs Legendary guarantee introduced with *Knights of the Frozen Throne* (10 August 2017).
- TetrisWiki, "Random Generator" (Tetris Guideline games). The 7-bag rule and the 12-piece maximum gap between I pieces.
- Fire Emblem Wiki, "True hit". Two-random-number averaging from *The Binding Blade* (2002), with conversions 75 → 87.75%, 90 → 98.10%, 25 → 12.75%.
- Schreiber, I. (2010). *Game Balance Concepts*, Level 5. Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press.

## Interactive spec: examples/w10-prd-streaks.html

**Insight the visual must make obvious:** independent rolls and PRD at the same nominal chance have the same mean gap, but PRD removes long droughts and back-to-back clusters.

**Layout.** Two linked views stacked on mobile, side by side from 900px.

1. **Attack strip (top).** Two rows of 100 cells each, labelled "Independent" and "PRD". A cell is filled (accent color) when the effect procs on that attack. Both rows are rolled together when the user presses "Roll 100 attacks". Under each row show: procs in 100 attacks, longest gap, number of back-to-back procs.
2. **Gap histogram (bottom).** X axis: gap length in attacks, 1 to `max(30, ceil(3/p))`. Y axis: probability. Two series drawn as grouped bars or two outlined step lines: exact geometric `P(N=n) = (1−p)^(n−1) p` and exact PRD `P(N=n) = Π_{i<n}(1 − min(1,iC)) × min(1,nC)`. A single vertical line at the shared mean `1/p`, labelled. A dashed vertical line at `ceil(1/C)` labelled "PRD guarantee".

**Controls.**
- Nominal chance slider: 5% to 60%, step 5%. On change, compute `C` by bisection on `[0, p]` so that `Σ n P(N=n) = 1/p` (60 iterations, stop when the tail probability < 1e-12). Do not hard-code the table except as test values.
- "Roll 100 attacks" button (keyboard focusable), and a seed display so the same roll can be reproduced. Use a small seeded PRNG (mulberry32).
- Toggle "Show tail only (gap ≥ 8)" that zooms the histogram's y axis to make the tail comparison readable.

**Readout table** (exact numbers, copyable): C, mean gap (both), SD of gap (both), P(back-to-back) (p vs C), P(gap ≥ 8), P(gap ≥ 11), longest possible gap.

**Test values** (the builder must assert these on load in a console check):
- p = 0.25 → C = 0.084744 (±1e-6), SD independent 3.464, SD PRD 1.897, P(gap ≥ 8) 0.1335 vs 0.0432, P(gap ≥ 11) 0.0563 vs 0.0005, longest gap 12.
- p = 0.10 → C = 0.014746, longest gap 68, SD PRD 5.06.
- p = 0.50 → C = 0.302103, longest gap 4, SD PRD 0.81.

**First screen:** p = 25%, one pre-rolled strip with a fixed seed that shows at least one independent gap ≥ 10 (pick the seed by search at build time), and the histogram already drawn.

## Interactive spec: examples/w10-gacha-pity.html

**Insight the visual must make obvious:** the consolidated rate describes the mean, but soft pity piles most players into a narrow band just after the ramp starts, so the median sits far above the mean.

**Layout.** Two linked views.

1. **Per-pull chance (left or top).** X axis: pull number 1 to H. Y axis: `p_n` from 0 to 1. A line that is flat at the base rate, then ramps. Shade the soft-pity region.
2. **Landing distribution (right or bottom).** X axis: pull number 1 to H. Bars: `P(first success at n) = p_n × Π_{i<n}(1 − p_i)`. Vertical markers for mean (solid) and median (dashed), both labelled with values. A faint cumulative line on a secondary axis.

**Controls.**
- Base rate: 0.1% to 5%, step 0.1% (default 0.6%).
- Soft-pity start S: 1 to H, step 1 (default 74). A checkbox "Soft pity on" (default on).
- Step d: 0.5 to 20 percentage points, step 0.5 (default 6).
- Hard pity H: 10 to 200 (default 90). Always force `p_H = 1`.
- Preset buttons: "Genshin community model (0.6%, 74, +6, 90)", "Hard pity only", "No pity (H = 1000)", "Hearthstone-style (5%, hard 40, hypothetical rate)".

**Model.** `p_n = base` for `n < S`; `p_n = min(1, base + d × (n − S + 1))` for `S ≤ n < H`; `p_H = 1`.

**Readout** next to the charts: expected pulls `E = Σ_{k=0}^{H−1} Π_{n=1}^{k}(1 − p_n)`, consolidated rate `1/E` (with a reference marker at 1.6%), median pull, SD of pulls, P(reach S), P(reach H).

**Test values:**
- Genshin model → E = 62.30, rate 1.605%, median 76, SD 24.3, P(reach 74) = 0.6445.
- Hard pity only (0.6%, H = 90) → E = 69.70, rate 1.435%, median 90, P(reach 90) = 0.5853.
- Soft start 60, step 4, H 90, base 0.6% → E = 53.89, rate 1.855%, median 63.
- Base 5%, hard 40, no soft → E = 17.43, P(reach 40) = 0.1353.

**First screen:** the Genshin preset, with the mean and median markers visibly far apart.
