# MA102 · Week 08 — Dice Sums and the Normal Curve (2d6 vs 1d12)

**Why this matters:** Two dice rules can share a range and nearly share an average, yet one feels reliable and the other feels like chaos. The difference is the shape of the distribution, and it decides how much a +1 bonus is worth, how often players see extreme results, and whether skill or luck wins your game.

**You will be able to:**
- Compute the exact distribution of a sum of dice by counting outcomes, and its mean and standard deviation from a formula.
- Compare two dice rules by their "at least t" success curves and compute the value of a +1 modifier at any target.
- Approximate the sum of many dice with a normal curve and check the approximation against exact values.
- Choose a dice expression for a design goal (reliable, swingy, rare extremes) and justify the choice with numbers.

**Before class:** Schreiber, *Game Balance Concepts*, Level 4 ("Probability and Randomness"), the sections on dice and bell curves. Schreiber & Romero, *Game Balance* (2021), the probability chapter, sections on dice and distributions.

**Prerequisites from earlier courses:** Sample spaces and counting outcomes, MA102 week 1. Expected value, MA102 week 4. Variance and standard deviation, MA102 week 5. The binomial distribution, MA102 week 6. (See the [MA102 syllabus](../syllabus.md) for these weeks.) Function graphs and reading curve shapes, MA101 weeks 1 to 4 ([MA101 syllabus](../../MA101-mathematics-for-games-i-algebra-functions-trigon/syllabus.md)).

**Interactive:** [Dice shapes: 2d6 vs 1d12](../examples/w08-dice-shapes.html) (spec at the end of this lecture). Keep it open during section 2.

---

## 1. Adding dice changes the shape

Roll one fair six-sided die. Each face, 1 to 6, comes up with chance 1/6. The distribution is **flat** (also called **uniform**): every result is equally likely.

Now roll two dice and add them. Tabletop players write this **2d6**: the number before the "d" is how many dice, the number after is how many sides. The sum runs from 2 to 12. It is tempting to guess each sum is equally likely, 1 in 11. It is not.

Use the sample-space method from week 1. Two dice have `6 × 6 = 36` equally likely ordered outcomes. Count how many give each sum.

- A sum of 2 needs (1,1). That is 1 way.
- A sum of 3 needs (1,2) or (2,1). That is 2 ways.
- A sum of 7 has (1,6), (2,5), (3,4), (4,3), (5,2), (6,1). That is 6 ways.
- A sum of 12 needs (6,6). That is 1 way.

The counts climb by one from 2 to 7 and fall by one from 7 to 12. The shape is a **triangle**. The middle is six times as likely as either end.

The reason is simple. Extreme sums need both dice to be extreme together. Middle sums can be built many ways, because a high roll on one die can be balanced by a low roll on the other. The more dice you add, the more ways there are to land in the middle, and the rarer the extremes become. That single observation is the whole lecture.

## 2. Worked example: 2d6 vs 1d12, same range, different game

### The hook

In Catan (first published in 1995), every turn the active player rolls two six-sided dice. Each land hex carries a number token from 2 to 12, and hexes whose number is rolled produce resources. There is no token for 7. Rolling a 7 moves the robber, which blocks a hex, and anyone holding 8 or more resource cards must discard half.

Look at a set of tokens and you will see dots under the numbers. The 6 and 8 tokens have five dots and are printed in red. The 2 and 12 have one dot. The dots are the count of ways to roll that number out of 36. The game prints its own probability distribution on the board. New players learn in one game that a settlement on a 6 or an 8 pays far more often than one on a 2 or a 12, and that the robber shows up more than any other single number.

Now imagine Catan with a twelve-sided die. The range is almost the same, 1 to 12 instead of 2 to 12. But every number would pay out equally, the red 6 and 8 would be no better than a 2, and placement, the main strategic decision of the opening, would stop mattering. Same range. A completely different game.

### The model

For the sum `S` of two six-sided dice:

```
P(2d6 = s) = (6 − |s − 7|) / 36      for s = 2, 3, ..., 12
P(1d12 = s) = 1 / 12                 for s = 1, 2, ..., 12
```

For any number `N` of fair dice with `F` faces each (written NdF), the mean and standard deviation are:

```
mean = N × (F + 1) / 2
variance = N × (F² − 1) / 12
SD = √variance
```

- `N` is the number of dice.
- `F` is the number of faces on each die.
- The variance of a single die is `(F² − 1)/12`. Dice are independent, so variances add (week 5), which is why the formula multiplies by `N`.

For 2d6: mean `= 2 × 7/2 = 7`, variance `= 2 × 35/12 = 5.83`, SD `≈ 2.42`.
For 1d12: mean `= 13/2 = 6.5`, variance `= 143/12 = 11.92`, SD `≈ 3.45`.

The averages differ by only half a point. The spread of 1d12 is 43% larger. That spread is what players feel.

### Numbers you can check

The "exactly" columns come from the counting above. The "at least" columns add up every result from `t` to the top. You can verify any row by counting dice pairs on paper.

| Target t | 2d6 ways (of 36) | P(2d6 = t) | P(1d12 = t) | P(2d6 ≥ t) | P(1d12 ≥ t) |
|---|---|---|---|---|---|
| 1 | 0 | 0% | 8.3% | 100% | 100% |
| 2 | 1 | 2.8% | 8.3% | 100% | 91.7% |
| 3 | 2 | 5.6% | 8.3% | 97.2% | 83.3% |
| 4 | 3 | 8.3% | 8.3% | 91.7% | 75.0% |
| 5 | 4 | 11.1% | 8.3% | 83.3% | 66.7% |
| 6 | 5 | 13.9% | 8.3% | 72.2% | 58.3% |
| 7 | 6 | 16.7% | 8.3% | 58.3% | 50.0% |
| 8 | 5 | 13.9% | 8.3% | 41.7% | 41.7% |
| 9 | 4 | 11.1% | 8.3% | 27.8% | 33.3% |
| 10 | 3 | 8.3% | 8.3% | 16.7% | 25.0% |
| 11 | 2 | 5.6% | 8.3% | 8.3% | 16.7% |
| 12 | 1 | 2.8% | 8.3% | 2.8% | 8.3% |

Three things to read from the table.

- **Exactly 7.** 2d6 rolls a 7 twice as often as 1d12 does, 16.7% against 8.3%.
- **The tails.** A 12 on 2d6 is 1 in 36. On 1d12 it is 1 in 12, three times as common. Rolling 10 or more is 16.7% against 25%. If 10+ is your "critical hit", 1d12 hands out 50% more of them.
- **The same answer at 8.** Both rules give 41.7% for "8 or more". Designers who test only one target will conclude the rules are equivalent. They are not.

### What a +1 bonus is worth

Now the result that changes design decisions. Suppose a player needs to roll `t` or more to succeed, and a skill or item gives them +1. How much does +1 raise the success chance?

On 1d12, every +1 adds exactly `1/12 ≈ 8.3` percentage points, whatever the target. The success curve is a straight line.

On 2d6, +1 adds `P(2d6 = t − 1)`, the chance of the one result that turns from a failure into a success. That depends on where the target sits:

| Target t | P(2d6 ≥ t) | With +1 | Gain from +1 | Gain on 1d12 |
|---|---|---|---|---|
| 12 | 2.8% | 8.3% | +5.6 points | +8.3 points |
| 10 | 16.7% | 27.8% | +11.1 points | +8.3 points |
| 8 | 41.7% | 58.3% | +16.7 points | +8.3 points |
| 6 | 72.2% | 83.3% | +11.1 points | +8.3 points |
| 4 | 91.7% | 97.2% | +5.6 points | +8.3 points |

On 2d6, a +1 against a middle target (8) is worth three times as much as the same +1 against a very hard target (12) or a very easy one (4). The success curve is an **S-shape**, steep in the middle and flat at both ends. On 1d12 it is a straight line.

That is the whole difference in feel. On a bell-shaped roll, small bonuses decide contests between evenly matched sides, and huge gaps in skill make the result nearly certain. On a flat roll, a bonus is worth the same everywhere, and even a big underdog keeps a real chance.

### The visual: two linked views

Open the interactive. The top view draws the two distributions as bar charts on the same axis: a triangle for 2d6 and a flat row of bars for 1d12. In this view they look like two similar games with a slightly different "texture."

The bottom view draws the success curve, `P(roll ≥ t)`, for both rules against the target `t`. Now the difference is obvious. The 1d12 line falls straight. The 2d6 curve is an S. Drag the target slider and a readout shows each rule's success chance. Press the "+1 bonus" toggle and both curves shift one step left; the gap between the old and new curve at your target is printed in percentage points. Move the target from 12 to 7 and watch the 2d6 gap grow from 5.6 to 16.7 points while the 1d12 gap stays at 8.3.

Then change the dice. Set the left rule to 3d6 and the right rule to 1d20. The S-curve gets steeper and the flat line gets longer. Set the left rule to 8d6 and switch on the normal overlay: a smooth bell drawn on top of the bars, nearly touching every one.

### Cross-game recognition

The same idea, "sums bunch in the middle, so bonuses matter most there", runs through many games. Rewrite each rule as a success curve and you will see it.

**GURPS (Steve Jackson Games).** Every success roll in GURPS is 3d6, and you succeed if the total is *equal to or less than* your skill. A roll of 3 or 4 always succeeds, whatever your skill. Rewrite it as a success curve: `P(3d6 ≤ skill)`. At skill 10, that is 50.0%. At skill 11, 62.5%. The single point from 10 to 11 is worth 12.5 percentage points. From skill 16 (98.1%) to 17 (99.5%) it is worth 1.4 points. The designers chose a bell so that an average character is a coin flip, a trained one is reliable, and an expert almost never fails.

**Dungeons & Dragons 5th edition, d20 checks.** Attacks and checks use one d20 plus modifiers against a target number. That is a flat distribution: each +1 is worth exactly 5 percentage points wherever the target sits. This is the 1d12 side of our comparison, stretched to 20 faces. It keeps underdogs alive. A character needing an 18 still succeeds 15% of the time.

**D&D 5th edition, advantage.** When you have advantage, you roll a second d20 and use the higher result. That is not a sum, but it bends the flat line the same way. The chance of success becomes `1 − (1 − p)²`. Needing 11 or more, a flat 50% becomes 75%. Needing 20, 5% becomes 9.75%. Advantage is worth the most near the middle, like a sum. Designers in the d20 family use it to get bell-like behaviour for one roll without changing the dice.

**D&D 5th edition, Fireball.** The spell deals 8d6 fire damage on a failed save. Using our formulas: mean `8 × 3.5 = 28`, SD `√(8 × 35/12) ≈ 4.83`. The range is 8 to 48, but the chance of rolling exactly 48 is `1/6^8`, about 1 in 1.7 million. In practice Fireball deals 24 to 32 about 64% of the time. A wide printed range, a narrow real one.

**Catan, again.** Settlement placement is a bet on the triangle. A "6-8-5" corner collects on 14 of 36 rolls, 38.9% of turns. A "2-12-3" corner collects on 4 of 36, 11.1%. Experienced players count dots because the dots *are* the distribution.

Five contexts, one idea. When you meet a random rule, draw its success curve before you judge it. The question to ask is: *where is the curve steep, and where do my players' targets sit?*

### Design judgment, eyes open

Neither shape is correct. Each is a choice.

- **Choose a bell (several dice summed) when you want competence to show.** Bonuses decide close contests. Big skill gaps become near-certainties. Extreme results are rare, so when they happen they feel special. The cost is that underdogs rarely win, and players at the flat ends of the S feel their upgrades do nothing.
- **Choose flat (one die) when you want every point to feel the same and upsets to stay possible.** Tooltips are easy: "+1 = +5%". The cost is swinginess. An expert fails often, a novice succeeds often, and players may feel the dice matter more than their choices.
- **The value of a bonus depends on the target, so tune targets and bonuses together.** On a bell, if most targets sit near the middle, small bonuses are powerful and stacking them is dangerous. If targets sit at the ends, bonuses feel worthless. Design your difficulty numbers with the steep part of the curve in mind.
- **Displays can mislead.** "Damage 8 to 48" on a tooltip suggests a wide spread. Players will almost never see the ends. Consider showing the typical range, or the mean, instead of the extremes.
- **The number of dice is a spread knob independent of the average.** You can hold the mean fixed and change the feel. 1d20 and 3d6 both average 10.5. 3d6 has an SD of 2.96, 1d20 an SD of 5.77.

## 3. Why sums always drift toward a bell

### The central limit theorem, informally

You saw the shape change from flat (1 die) to triangle (2 dice). With 3 dice the triangle's sides curve and the top rounds off. By 8 dice the shape is a smooth, symmetric hump. This is not a coincidence of six-sided dice. It is one of the most important results in probability.

The **central limit theorem** says, roughly: add up many independent random quantities, and the total's distribution gets closer and closer to a particular bell-shaped curve, the **normal distribution**. It does not matter much what shape each piece has. A d4, a d20, a coin flip, a random damage roll: sum enough of them and you get the same bell. That is why the normal curve shows up in so many places, from test scores to total damage over a long fight.

The normal curve is fixed by two numbers, its mean `μ` (mu) and standard deviation `σ` (sigma). For a sum of dice, use the formulas from section 2. For 8d6, `μ = 28` and `σ ≈ 4.83`.

### The 68-95 rule

For a normal distribution:

- About 68% of results fall within 1 SD of the mean.
- About 95% fall within 2 SD.
- About 99.7% fall within 3 SD.

Check it against exact 8d6 values. Within 1 SD means 23.17 to 32.83, so the whole numbers 24 to 32. The exact probability, counted by computer over all `6^8 = 1,679,616` outcomes, is 64.2%. Within 2 SD means 19 to 37: exact 95.3%. The rule of thumb is close. The 1 SD case is off by a few points because dice give whole numbers and the band has to be cut at an integer.

### Using the normal approximation

Counting exact outcomes gets expensive fast. 8d6 has 1.7 million, 20d6 has 3.7 × 10^15. The normal curve gives quick estimates.

To estimate `P(8d6 ≥ 35)`:

1. Find how many SDs 35 is above the mean. Dice give whole numbers, so use 34.5 as the boundary (this is called a **continuity correction**). `z = (34.5 − 28) / 4.83 ≈ 1.35`.
2. Look up the chance a normal value exceeds `z = 1.35`. It is about 8.9%.
3. The exact answer is 9.07%. The estimate is off by less than 0.2 points.

Without the correction, using `z = (35 − 28)/4.83 = 1.45`, you get 7.4%, noticeably worse. When you approximate whole-number results with a smooth curve, always shift the boundary by half a step.

**When not to trust the approximation.** With only 2 or 3 dice, the shape is still visibly a triangle or a rounded triangle, and normal estimates in the tails can be poor. Far out in the tails, for example the chance of 48 on 8d6, the normal curve gives the wrong order of magnitude. For small dice pools, count exactly or simulate. For large pools, the bell is a good tool.

### The bell in video games

Video games rarely show dice, but they sum random things constantly. Total damage over a fight of 40 hits, each with a random damage range and a crit chance, is a sum of 40 random pieces, so it is close to normal. The number of crits in 100 swings is binomial (week 6), and a binomial with many trials is also nearly normal. The time to clear a dungeon with 12 random pulls is a sum. Whenever you add many independent random parts, expect a bell, with mean equal to the sum of the means and variance equal to the sum of the variances. You can predict a whole fight's spread without simulating it.

This has a design consequence. A single hit can be very swingy, yet a whole fight is not, because the swings cancel. If playtesters say "combat feels random" in short fights but "fine" in long ones, the central limit theorem is why. Short fights sum few parts.

## 4. Dice as a design vocabulary

Three separate knobs describe any dice rule.

1. **Range**, from the minimum to the maximum. `N` to `N × F` for NdF.
2. **Mean**, `N × (F + 1)/2`, plus any flat bonus.
3. **Spread**, the SD `√(N × (F² − 1)/12)`. Fewer, larger dice give more spread. More, smaller dice give less.

You can change one without the others. Here are four damage expressions that all average 10.5:

| Rule | Range | Mean | SD | P(result ≥ 16) |
|---|---|---|---|---|
| 1d20 | 1 to 20 | 10.5 | 5.77 | 25.0% |
| 3d6 | 3 to 18 | 10.5 | 2.96 | 4.6% |
| 1d6 + 7 | 8 to 13 | 10.5 | 1.71 | 0% |
| 2d10 − 0.5 | not whole numbers, avoid | 10.5 | 4.06 | — |

The last row is there as a warning. If you need a specific mean, adjust with a flat bonus and pick dice for the spread. Do not fight the arithmetic with fractions.

Compare 1d20 and 3d6. The same average, but a big hit of 16 or more is more than five times as common on 1d20. If big hits trigger stagger or a kill, that one choice decides how often the fight's pacing breaks. And look at 1d6 + 7: it can never reach 16. A large flat bonus with a small die gives a steady, predictable hit, which is what many games want for the basic attack.

The P(3d6 ≥ 16) value comes from `(6 + 3 + 1)/216 = 10/216`, the ways to roll 16, 17 or 18. Count them yourself with the method from section 1 if you want the practice.

## In-class activity (25 minutes)

Pairs. Paper, two six-sided dice per pair, one twelve-sided die per pair (or a dice app), and the interactive.

1. **Roll it.** One partner rolls 2d6, the other 1d12, 36 times each. Tally results. Put your tallies on the class board. Compare the class total to the "exactly" columns of the table in section 2. How many rolls did the class need before the triangle was visible?
2. **Design a check system.** You are building a skill-check rule for a narrative RPG where characters have skill ratings 0 to 5. The goal: a skill-0 character should succeed at a "normal" task about 40% of the time, a skill-5 character about 95% of the time, and the jump from skill 2 to skill 3 should feel bigger than the jump from 4 to 5.
   - Choose a dice rule (for example 2d6 + skill ≥ target, or 1d12 + skill ≥ target) and a target.
   - Compute the success chance for skills 0 to 5. Use the table or the interactive.
3. **Defend it.** Explain in two sentences why your rule meets the goal, and name the one player experience your rule sacrifices.

**Expected output:** a short table (skill 0 to 5 against success chance), your rule, and your two-sentence defence. One team with 2d6 and one with 1d12 present, and the class compares.

## Common misconceptions

- **"Same range means same odds."** 2d6 and 1d12 share a range almost exactly, but 2d6 rolls a 7 twice as often and a 12 three times less often. Range tells you the limits, not the shape.
- **"A +1 is a +1."** On a flat roll it is worth the same everywhere. On a bell it is worth most near the middle and very little at the ends. The value of a bonus depends on the target.
- **"More dice means bigger numbers."** Not if you hold the mean fixed. More dice means *less* relative spread and rarer extremes. 3d6 and 1d20 have the same average.
- **"The normal curve is exact for dice."** It is an approximation that improves with more dice. With 2 dice the shape is a triangle. In the far tails the approximation can be wrong by a lot. Use a continuity correction and check exact values when it matters.

## Check yourself

1. A board game uses 2d6 and a player wins a bonus on a roll of 11 or 12. What is the chance per roll? If the game switched to 1d12, what would it be? By what factor did the chance change?
2. You are designing a check that uses 3d6 roll-under (succeed on total ≤ skill). A player at skill 12 gets a +2 item. What is their success chance before and after? A player at skill 16 gets the same item. How much does it help them?
3. Compute the mean and SD of 4d8. Using the normal approximation with a continuity correction, estimate the chance that 4d8 is at least 25.
4. A designer wants a weapon with average damage 14 that "never feels random." Propose two dice expressions with mean 14 and different SDs. Which one meets the goal better, and what is its SD?

<details>
<summary>Answers</summary>

1. On 2d6, 11 has 2 ways and 12 has 1 way, so `3/36 = 8.3%`. On 1d12 it is `2/12 = 16.7%`. The chance doubled.
2. From the 3d6 cumulative values, `P(3d6 ≤ 12) = 74.1%` and `P(3d6 ≤ 14) = 90.7%`, a gain of 16.6 points. At skill 16, `P(≤ 16) = 98.1%` and `P(≤ 18) = 100%` (before any special failure rules), a gain of 1.9 points. The same item is worth about nine times more to the middle player.
3. Mean `= 4 × 9/2 = 18`. Variance `= 4 × (64 − 1)/12 = 21`, so SD `≈ 4.58`. With the continuity correction, `z = (24.5 − 18)/4.58 ≈ 1.42`, so the estimate is about 7.8%. (The exact value, by enumeration, is 8.1%, so the estimate is close but a little low.)
4. Many answers work. Examples: `2d6 + 7` has mean 14 and SD `√(2 × 35/12) ≈ 2.42`. `1d4 + 11.5` does not work (fractional). `2d4 + 9` has mean 14 and SD `√(2 × 15/12) ≈ 1.58`. `4d6 − 0` has mean 14 and SD `≈ 3.42`. For "never feels random", the smallest SD wins, so `2d4 + 9` (SD 1.58, range 11 to 17) beats `4d6` (SD 3.42, range 4 to 24). The trade-off is that the hit never surprises anyone.

</details>

## Lab hook

**Lab 08, Dice by design** ([labs/lab08.md](../labs/lab08.md)). Build a notebook or spreadsheet that computes the exact distribution and success curve for any NdF + bonus by convolution, then use it to design the check rule for a small RPG and defend it in a one-page memo.

## Sources

- Wikipedia, "Catan". First published 1995 by Kosmos. Two six-sided dice decide which hexes produce; a roll of 7 moves the robber and players with 8 or more resource cards discard half.
- Catan GmbH, official rulebook downloads (catan.com, "Game Rules"), and secondary summaries at catangenerator.org ("Catan Rules") and playsettlr.com ("Catan Dice Probability"): number tokens carry dots showing relative frequency, and 6 and 8 are printed in red (base game, current edition).
- GURPS Wiki, "Success Roll", summarising *GURPS Basic Set* (4th edition, 2004), p. B343. Success rolls are 3d6 against a target, succeeding on a total equal to or below it; a roll of 3 or 4 is always a success.
- Wizards of the Coast, *Dungeons & Dragons System Reference Document 5.1*, "Advantage and Disadvantage" (roll a second d20 and use the higher or lower) and the spell "Fireball" (8d6 fire damage on a failed Dexterity save). D&D 5th edition, 2014 rules.
- Schreiber, I. (2010). *Game Balance Concepts*, Level 4, "Probability and Randomness" (online course).
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press. Probability chapter.
- Exact dice probabilities in this lecture were computed by full enumeration in Python and can be reproduced in Lab 08.

## Interactive spec: examples/w08-dice-shapes.html

**Purpose.** Show that 2d6 and 1d12 look similar as bar charts but have completely different success curves, so a +1 bonus is worth three times more in the middle of 2d6 than at its edges while on 1d12 it is constant. The insight that must be obvious on first load: *the straight line vs the S-curve in the bottom chart, with the +1 gap printed at the default target of 8.*

**Layout.** Two stacked, horizontally aligned charts sharing an x-axis (result value). Top: distributions. Bottom: success curves. On desktop, a controls column on the right; on mobile, controls below the charts.

**Rule model.** Two rules, A and B, each defined as `N d F + bonus` with `N` from 1 to 12, `F` in {4, 6, 8, 10, 12, 20}, bonus from −10 to +10. Default A = 2d6 + 0, B = 1d12 + 0. Compute each exact distribution by convolution: start from `[1]` and convolve `N` times with a length-F array of ones, then divide by `F^N`. Shift by `N + bonus` for the x-values.

**Top chart.** Grouped or overlaid bars of `P(A = x)` and `P(B = x)` over the union of both ranges, in the two palette series colours, with a legend. Optional "normal overlay" checkbox draws a smooth curve for each rule with `μ = N(F + 1)/2 + bonus`, `σ = √(N(F² − 1)/12)`, scaled to bar height (density times 1).

**Bottom chart.** Step lines of `P(A ≥ t)` and `P(B ≥ t)` against target `t`. Mode toggle "roll ≥ target" (default) or "roll ≤ target" (roll-under, for GURPS-style). A vertical target line at `t`.

**Controls.**
- Target slider over the union range, default 8.
- "+1 bonus" toggle: when on, draw a dashed copy of each success curve for the rule with bonus + 1, and print at the target the gain in percentage points for A and for B.
- Rule editors for A and B (N stepper, F select, bonus stepper), plus presets: "2d6 vs 1d12", "3d6 vs 1d20", "8d6 (Fireball)", "d20 with advantage vs d20" (advantage is a special rule: `P(max of two d20 ≥ t) = 1 − ((t − 1)/20)²` for t in 1 to 20; include it as a rule type "adv d20").

**Numbers panel.** For each rule: range, mean, SD, `P(= t)`, `P(≥ t)`, and the +1 gain at t. When the normal overlay is on, also the normal estimate of `P(≥ t)` with continuity correction, `1 − Φ((t − 0.5 − μ)/σ)`, beside the exact value.

**Test values.**
- 2d6: mean 7, SD 2.415. `P(≥ 8) = 41.67%`, `P(≥ 10) = 16.67%`, `P(= 7) = 16.67%`. +1 gain at t = 8: 16.67 points; at t = 12: 5.56 points.
- 1d12: mean 6.5, SD 3.452. `P(≥ 8) = 41.67%`. +1 gain anywhere in 2 to 12: 8.33 points.
- 3d6: `P(≤ 10) = 50.0%`, `P(≤ 11) = 62.5%`, `P(≥ 16) = 4.63%`.
- 8d6: mean 28, SD 4.830. `P(≥ 35)` exact 9.07%, normal with correction 8.92%.
- Advantage d20: `P(≥ 11) = 75%`, `P(≥ 20) = 9.75%`.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`. The two series must differ by both colour and pattern (solid vs hatched bars, solid vs dashed lines) so the chart reads in greyscale. All controls keyboard operable. No dice artwork from any product; plain shapes only.
