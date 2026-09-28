# MA102 · Week 06 — Binomial Distribution: Crits Over a Fight

**Why this matters:** "I have 10% crit and went a whole fight without one" is one of the most common complaints in any game with crits. The binomial distribution tells you exactly how often that happens, and so how often your players will feel cheated by a system that is working as designed.

**You will be able to:**
- Decide whether a game process meets the four conditions for a binomial model.
- Compute binomial probabilities, including "exactly k", "at least k" and "none", for crits, procs and drops.
- Compute the mean and standard deviation of a crit count and use them to predict the spread of observed crit rates in fights of different lengths.
- Critique a crit or drop system by computing how many players land in the unlucky tail.

**Before class:** Schreiber, *Game Balance Concepts* (blog course, 2010), Level 4 "Probability and Randomness", the sections on independent trials; Schreiber & Romero, *Game Balance* (2021), the chapter on probability, the sections on combinations and repeated trials.

**Prerequisites from earlier courses:** MA101 week 4, exponents and exponential decay (see the [MA101 syllabus](../../MA101-mathematics-for-games-i-algebra-functions-trigon/syllabus.md)). From this course, [week 2, independence](w02-independent-events-and-the-gamblers-fallacy.md), [week 3, the complement rule](w03-complement-rule-chance-of-at-least-one-drop.md), [week 4, expected value](w04-expected-value-comparing-weapons.md) and [week 5, variance](w05-variance-and-swingy-designs.md).

**Interactive:** [Crits over a fight](../examples/w06-crit-binomial.html). Keep it open during section 2.

---

## 1. Counting successes in a fixed number of tries

Weeks 2 and 3 dealt with single events and "at least one" questions. Most game questions are about **how many**. How many crits in this fight? How many of 25 raiders get the drop? How many of my 10 pulls are rare? Each of these counts successes across a fixed number of tries, and they all share one distribution.

### The four conditions

A count `K` follows a **binomial distribution** when all four of these hold:

1. **Fixed number of trials.** You decide `n` in advance: 8 attacks, 25 raiders, 10 pulls.
2. **Two outcomes per trial.** Each trial is a success (crit, drop) or a failure. What counts as success is your choice, as long as it is yes-or-no.
3. **Same probability every trial.** Every trial succeeds with the same probability `p`.
4. **Independent trials.** One trial's result does not change another's probability. You met independence in week 2.

We write `K ~ Binomial(n, p)`, read "K is binomial with n trials and success probability p".

Hold on to the four conditions. At the end of the lecture you will see that some of the most interesting game systems are interesting precisely because they break one of them on purpose.

### Where the formula comes from

Take `n = 3` attacks with crit chance `p`. What is the probability of exactly one crit?

List the ways it can happen: crit on the first attack only (C, N, N), the second only (N, C, N), or the third only (N, N, C). By independence, each sequence has probability `p × (1 − p) × (1 − p) = p(1 − p)²`. There are 3 sequences, so

```
P(K = 1) = 3 p (1 − p)²
```

In general, a particular sequence with `k` crits and `n − k` non-crits has probability `p^k (1 − p)^(n − k)`, and the number of such sequences is the number of ways to choose which `k` of the `n` positions are crits. That number is the **binomial coefficient**:

```
C(n, k) = n! / (k! (n − k)!)
```

read "n choose k". `n!` (n factorial) means `n × (n − 1) × ... × 2 × 1`, and `0! = 1`. So C(3, 1) = 6 / (1 × 2) = 3, matching the list. C(8, 2) = 40,320 / (2 × 720) = 28.

Putting it together:

```
P(K = k) = C(n, k) × p^k × (1 − p)^(n − k)
```

Every symbol, once more: `n` trials, `k` successes you are asking about, `p` success chance per trial, `C(n, k)` the number of arrangements.

Two special cases you already know:

- `k = 0`: C(n, 0) = 1, so `P(K = 0) = (1 − p)^n`. That is "no successes in n tries", the complement of week 3's "at least one".
- `k = n`: `P(K = n) = p^n`. Every trial succeeds.

### Mean and spread

A binomial count is the sum of `n` independent yes-or-no variables. Each one has mean `p` and, from week 5, variance `p(1 − p)`. Linearity of expectation (week 4) and additivity of variance for independent variables (week 5) give

```
E[K]   = n p
Var(K) = n p (1 − p)
SD(K)  = √(n p (1 − p))
```

No new theory. The binomial is what you get when you add up week 5's single crit `n` times.

## 2. Worked example: the champion's dry spell

### The hook

In Dungeons & Dragons 5th edition, an attack scores a critical hit when the d20 shows a natural 20, a 5% chance. The fighter's Champion subclass gets Improved Critical at 3rd level, which makes 19 or 20 a crit. That doubles the crit chance to 10%. At 5th level a fighter gets Extra Attack and swings twice per turn. So a 5th-level champion in a four-round fight makes 8 attacks with a 10% crit chance each.

Ask the table: how often does that champion finish the fight **without a single crit**? Most players guess "rarely, maybe one fight in ten". The answer is 43%. The subclass whose whole identity is critting goes crit-less in almost half of its four-round fights.

### The model

Each attack's d20 roll is independent, has two outcomes for our purposes (crit or not), and has the same crit chance. With a fixed 8 attacks, all four conditions hold:

```
K ~ Binomial(n = 8, p = 0.10)       champion
K ~ Binomial(n = 8, p = 0.05)       any other attacker
P(K = k) = C(8, k) × p^k × (1 − p)^(8 − k)
```

### Numbers you can check

| Crits k | C(8, k) | Champion, p = 0.10 | Others, p = 0.05 |
|---|---|---|---|
| 0 | 1 | 0.4305 | 0.6634 |
| 1 | 8 | 0.3826 | 0.2793 |
| 2 | 28 | 0.1488 | 0.0515 |
| 3 | 56 | 0.0331 | 0.0054 |
| 4 or more | | 0.0050 | 0.0004 |
| **Mean n p** | | **0.80** | **0.40** |
| **SD √(n p (1 − p))** | | **0.85** | **0.62** |

Check two cells by hand.

- Champion, zero crits: 0.9⁸. Square 0.9 three times: 0.81, 0.6561, 0.4305. So 43.0%.
- Champion, two crits: 28 × 0.1² × 0.9⁶ = 28 × 0.01 × 0.5314 = 0.1488.

Three observations.

**The most likely outcome is zero crits.** For the champion, 0 edges out 1 (43.0% versus 38.3%). For everyone else, zero crits is two thirds of fights. The average of 0.8 crits per fight is correct and misleading at the same time: no fight has 0.8 crits, and the single most common fight has none.

**Doubling the chance does not halve the dry spells.** The champion's no-crit rate is 43%, not 33% (half of 66%). Because `P(K = 0) = (1 − p)^n`, doubling `p` changes the base of a power, not a simple factor. To halve the no-crit rate you need a much bigger change in `p` or `n`.

**Multi-crit fights are rare and memorable.** The champion gets 2 or more crits in about 19% of fights. That is the fight players tell stories about, which is part of why the "crit fighter" identity survives a 43% dry-spell rate.

### A visual you can move

Open the interactive. It shows the same distribution twice.

The left panel counts crits: a bar chart of `P(K = k)` for `k = 0` to `n`. The right panel shows the **observed crit rate** `k / n` on a fixed axis from 0% to 100%, with a band marking the true rate `p`.

Set `p = 25%` and drag the number of attacks `n` from 6 up to 200. On the left, the bars spread out and move right: more attacks, more crits, more spread in the count. On the right, the opposite happens: the distribution **narrows** around 25%. Both views are correct. The count's SD grows like `√n`, while the rate's SD, `√(p(1 − p)/n)`, shrinks like `1/√n`. This is week 5's long-fight rule, seen through crits.

Here are the numbers the interactive prints for `p = 0.25`:

| Attacks n | Mean crits | SD of count | P(no crits) | P(observed rate between 15% and 35%) | P(observed rate ≥ 40%) |
|---|---|---|---|---|---|
| 6 | 1.5 | 1.06 | 17.8% | 65.3% | 16.9% |
| 20 | 5 | 1.94 | 0.32% | 80.7% | 10.2% |
| 50 | 12.5 | 3.06 | 0.00006% | 90.0% | 1.4% |
| 200 | 50 | 6.12 | about 0 | 99.9% | 0.0002% |

In a six-attack skirmish, a 25% crit player sees a crit rate of 40% or more one fight in six, and zero crits another one fight in six. In a 200-attack boss fight, the observed rate lands within 10 points of 25% essentially every time. Short fights are where players "feel" the RNG.

### Cross-game recognition

**Pokémon (Generation VII onward).** A move at the base crit stage crits with probability 1/24. Over a 10-move battle, the chance of at least one crit is 1 − (23/24)¹⁰ = 0.347. Stage +2 (for example a high-crit move plus a crit-boosting item) raises the chance to 1/2. With 4 attacks at stage +2, `K ~ Binomial(4, 0.5)`, and the probabilities of 0 through 4 crits are 1/16, 4/16, 6/16, 4/16, 1/16: the row of Pascal's triangle, divided by 16. Players building "crit teams" are betting on this distribution.

**MMO drop rates.** Week 3 showed that with a 1% drop chance, about 63% of players have the item after 100 kills and about 1 in 20 still lacks it after 300. That second number is a binomial zero: `P(K = 0) = 0.99³⁰⁰ = 0.049`. The binomial also answers the next question players ask: how many copies will I have? After 300 kills, the expected count is 3, and the chances of 0, 1, 2 and 3 copies are 4.9%, 14.9%, 22.4% and 22.5%. More than 40% of farmers will have fewer than the "expected" 3. Week 7 will flip the question around to "how many kills until the first drop".

**Raid loot.** Suppose each of 25 raiders independently has a 4% chance to receive a specific item from a boss. The number who receive it is `Binomial(25, 0.04)`, with mean exactly 1. Yet the probability that nobody gets it is 0.96²⁵ = 36.0%, and the probability that two or more do is 26.4%. "One per kill on average" hides a third of kills with no drop at all. Designers who want exactly one item per kill have to build that rule in directly rather than rely on the average.

**Dota 2 and League of Legends, where the model fails on purpose.** Both games break condition 4. Dota 2 uses a pseudo-random distribution for most chance-based effects: the proc chance starts below the listed value and rises after every attack that fails to proc, then resets. League of Legends applies a similar pseudo-random adjustment to critical strikes. In both, one attack's result changes the next attack's probability, so the count is not binomial, and the dry-spell probability `(1 − p)^n` is far too high for them. Week 10 builds these systems; this week gives you the baseline they are designed to beat.

### Eyes-open design judgment

The binomial is the "fair dice" baseline. Its streaks are real, and players experience them as unfairness. What you should decide deliberately:

- **Know your dry-spell rate before players find it.** For any chance-based feature, compute `(1 − p)^n` for a typical `n`. If it is above about 25% for an effect that defines a class or build, expect complaints. The champion's 43% four-round dry spell is a real, published design; its players live with it because D&D fights are social and a missed crit costs little. In a competitive game, the same number may be unacceptable.
- **Count, don't average.** "0.8 crits per fight" and "one drop per kill" are true and useless for predicting how players feel. Report the probability of zero and the probability of the top outcomes alongside the mean.
- **Change `n`, not only `p`.** More, smaller trials (faster attacks, more drop rolls with lower value each) shrink the relative spread. A weapon with twice the attack speed and half the damage per hit makes twice as many trials per fight, so `(1 − p)^n` falls much faster. This is often a cleaner fix than changing crit chance.
- **Break independence only on purpose.** Pseudo-random crits and pity timers reduce dry spells but have costs: they are harder to explain, players can sometimes exploit the counter, and they change how crit chance stacks. Choose them because the binomial's tails are unacceptable for this feature, not by default.
- **Watch for hidden violations.** If crit chance changes mid-fight (buffs, execute phases), condition 3 fails. If the fight ends when the enemy dies, `n` is not fixed, and condition 1 fails; the count then depends on how fast you kill, which is the setting of week 7. Your binomial numbers are an approximation in those cases, and you should say so in the design document.

### Check yourself (worked example)

1. A 5th-level champion fights a long, eight-round battle: 16 attacks. What is the probability of no crits? Of 3 or more?
2. How many attacks must a non-champion (5% crit) make before the probability of zero crits drops below the champion's 43% for 8 attacks?
3. A designer wants a "crit build" whose four-round (8-attack) dry spell rate is at most 10%. What crit chance is needed?

<details>
<summary>Answers</summary>

1. Zero crits: 0.9¹⁶ = 0.1853, about 18.5%. Three or more: 1 − P(0) − P(1) − P(2). P(1) = 16 × 0.1 × 0.9¹⁵ = 0.3294. P(2) = 120 × 0.01 × 0.9¹⁴ = 0.2745. So 1 − 0.1853 − 0.3294 − 0.2745 = 0.2108, about 21%.
2. Solve 0.95ⁿ < 0.4305. Taking logarithms (MA101 week 5), n > ln(0.4305) / ln(0.95) = 16.4, so 17 attacks. The non-champion needs about twice as many attacks to match, as you might expect from half the crit chance.
3. Solve (1 − p)⁸ ≤ 0.10. Then 1 − p ≤ 0.10^(1/8) = 0.750, so p ≥ 0.25. A 25% crit chance, far above what the Champion's 10% gives.

</details>

## 3. Reading the shape: most likely, mean and tails

Three summary numbers of a binomial answer different design questions, and confusing them causes most of the misreadings in patch discussions.

- **The mean `n p`** answers "over thousands of fights, how many crits per fight?" Use it for balance spreadsheets and DPS.
- **The mode**, the most likely single value, answers "what does a typical fight look like?" For a binomial, the mode is the whole number just below `(n + 1) p`, or either neighbor when `(n + 1) p` is itself a whole number. For the champion, (8 + 1) × 0.1 = 0.9, so the mode is 0.
- **The tails**, like `P(K = 0)` or `P(K ≥ 3)`, answer "how many players will have a story, good or bad?" Multiply a tail probability by your player count. With 100,000 fights a day at a 1% tail, that is 1,000 fights a day in which something happened that a player might post about.

When a player reports "I got zero crits in 20 attacks at 10%", check the tail: 0.9²⁰ = 12.2%. That is one fight in eight, so across a large player base it happens constantly. It is not a bug. When a player reports zero crits in 200 attacks at 10%, the probability is 0.9²⁰⁰, about 7 in 10 billion. That is a bug report worth reading.

### Approaching the bell curve

As `n` grows, the binomial's bars take on a symmetric bell shape centered on `n p`. For `n = 200` and `p = 0.25`, the mean is 50 and the SD is 6.12, and the probability of landing within two SDs (between 38 and 62 crits) is 95.9%. That "about 95% within two standard deviations" rule belongs to the normal curve, which week 8 introduces through sums of dice. For now, notice that the binomial is already heading there, and that the rule of thumb works well once `n p` and `n (1 − p)` are both above about 10.

## 4. Damage from a binomial count

Crit counts become damage counts through the model from week 5. If each hit deals `b`, crits deal `m × b`, and there are `K` crits in `n` hits,

```
total damage = b × (n + K(m − 1))
E[total]     = b × (n + n p (m − 1))
SD(total)    = b × (m − 1) × √(n p (1 − p))
```

The total damage is a straight-line function of `K`, so its distribution is the binomial's shape, stretched by `b(m − 1)` and shifted by `b n`. Every probability you computed for crit counts transfers directly.

Example: 12 attacks, `b = 100`, `m = 2`, `p = 0.25`. The expected total is 100 × (12 + 3) = 1,500, with SD 100 × √(12 × 0.25 × 0.75) = 150. If the enemy has 1,500 HP, you kill within 12 attacks only when `K ≥ 3`, which has probability 60.9%. The "expected damage equals the HP" fight fails 39% of the time. Week 5 showed the same effect hit by hit; the binomial gives it to you in one line.

## In-class activity (25 minutes)

Pairs, each with one d20 (or a dice app) and a tally sheet.

1. Each partner plays a champion fighter: roll 8 d20s per "fight", counting 19 and 20 as crits. Play 10 fights each and record the crit count per fight (10 minutes).
2. Pool the class's fights on the board in a tally by crit count (0, 1, 2, 3, 4+).
3. Convert the tally to proportions and compare with the table in section 2. Which row is furthest off? Given the class's total number of fights, is that difference surprising? (Hint: the class's proportion of zero-crit fights is itself a binomial count over the number of fights.)
4. Redesign: propose a rule that keeps the champion's average at 0.8 crits per 8 attacks but brings the zero-crit rate under 25%. Describe it in one sentence and state which binomial condition it breaks.

Expected output: a class tally close to 43/38/15/3/0.5 percent, one sentence per pair on the largest deviation, and one rule per pair. Common good answers include "guaranteed crit on the 8th attack if none yet" (breaks independence) and "roll 16 half-damage attacks" (changes `n`, keeps the binomial).

## Common misconceptions

- **"10% crit over 10 attacks guarantees one crit."** The expected count is 1, but P(zero) = 0.9¹⁰ = 34.9%. Averages are not guarantees.
- **"Doubling the chance halves the chance of none."** `P(K = 0) = (1 − p)^n`. From 5% to 10% over 8 attacks, it drops from 66% to 43%, not to 33%.
- **"Any count of successes is binomial."** Only with a fixed `n`, the same `p` and independence. Crits under a pseudo-random system and kills-until-drop are not binomial.
- **"A 25% crit player who crits 40% of the time in a fight is lucky in a meaningful way."** In a 6-attack fight that happens 17% of the time. Over short fights, observed rates wander far from the sheet value, and that is expected behavior.

## Check yourself

1. A raid of 20 players each has an independent 5% chance to get a mount from a boss. What is the probability that nobody gets it? That exactly one person does? What is the expected number?
2. A proc has a 20% chance on each of 15 hits. Compute the mean and SD of the proc count and the probability of 6 or more procs.
3. A player with 30% crit chance reports 0 crits in 25 attacks. Is that a plausible streak or a likely bug? Use the binomial.

<details>
<summary>Answers</summary>

1. P(nobody) = 0.95²⁰ = 0.358. P(exactly one) = 20 × 0.05 × 0.95¹⁹ = 20 × 0.05 × 0.3774 = 0.377. Expected number = 20 × 0.05 = 1.
2. Mean = 15 × 0.2 = 3. SD = √(15 × 0.2 × 0.8) = √2.4 = 1.55. P(K ≥ 6) = 1 − P(K ≤ 5) = 1 − (0.0352 + 0.1319 + 0.2309 + 0.2501 + 0.1876 + 0.1032) = 1 − 0.9389 = 0.061.
3. P(0) = 0.7²⁵ = 0.00013, about 1 in 7,500 streaks of 25 attacks. With a large player base this will happen to someone daily, so it is not proof of a bug by itself. But it is rare enough that repeated reports from the same setup are worth a telemetry check.

</details>

## Lab hook

**Lab 06: Crit simulator versus the binomial** ([`labs/lab06.md`](../labs/lab06.md)). You write a short simulation (spreadsheet or Python) of 10,000 fights, compare the histogram of crit counts with the binomial formula, and measure how the observed crit rate's spread shrinks with fight length. The simulation code is the seed for the Monte Carlo lab in week 11.

## Sources

- Wizards of the Coast, *System Reference Document 5.1* (D&D 5th edition, 2016): natural 20 is a critical hit; Fighter class Extra Attack at 5th level; Champion archetype Improved Critical (critical hit on 19 or 20) at 3rd level. The 2024 revision (SRD 5.2) keeps Improved Critical on 19 or 20.
- Serebii.net, "Critical Hits" (Pokémon, Generation VII onward): base crit chance 1/24, stage +2 crit chance 1/2. https://www.serebii.net/games/criticalhits.shtml
- Dota 2 Wiki, "Random Distribution" (accessed September 2026): most chance-based abilities use a pseudo-random distribution whose chance increases after each failed trial. https://dota2.fandom.com/wiki/Random_Distribution
- League of Legends Wiki, "Critical strike" (accessed September 2026): critical strikes use a pseudo-random algorithm rather than independent rolls. https://wiki.leagueoflegends.com/en-us/Critical_strike
- Schreiber, I. (2010). *Game Balance Concepts*, Level 4, "Probability and Randomness". https://gamebalanceconcepts.wordpress.com/
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press.

## Interactive spec: examples/w06-crit-binomial.html

**Purpose.** Show the binomial distribution of crit counts and, in a linked view, the distribution of the observed crit rate, so students see the count spread out while the rate narrows as fights get longer.

**The one insight the visual must make obvious.** In short fights the observed crit rate wanders far from the listed chance (and zero crits is common); in long fights it locks onto the listed chance. Same `p`, different `n`, very different experience.

**Layout.** Two linked panels side by side at desktop, stacked at 390px, plus a stats strip.

- Left panel, "Crits this fight": bar chart of `P(K = k)` for `k = 0 … n`. For `n > 60`, draw bars only for `k` with `P ≥ 0.0005` and label the axis range. Highlight the `k = 0` bar in a warning tone. Mark the mean `n p` with a vertical line.
- Right panel, "Observed crit rate": the same probabilities plotted at `x = k / n` on a fixed 0% to 100% axis (use thin bars or a stem plot). A shaded band from 15% to 35% by default, or `p ± 10` points when `p` changes. A vertical line at `p`.
- Stats strip, exact values to four decimals: mean, SD of count, SD of rate `√(p(1 − p)/n)`, mode, `P(K = 0)`, `P(K ≥ t)` for a threshold `t`, `P(rate in band)`.
- Optional toggle "Simulate": runs 1,000 simulated fights with a seeded RNG (for example mulberry32 with seed 1) and overlays the empirical histogram as outlined bars on the left panel.

**Controls** (keyboard accessible, values visible):

- Attacks per fight `n`: 1 to 200, step 1, default 8.
- Crit chance `p`: 0% to 100%, step 0.5%, default 10%.
- Threshold `t` for the "at least" readout: 0 to `n`, default 2.
- Preset buttons: "Champion, 4 rounds" (n = 8, p = 0.10), "Non-champion" (n = 8, p = 0.05), "Skirmish" (n = 6, p = 0.25), "Boss fight" (n = 200, p = 0.25), "1% drop, 300 kills" (n = 300 with the slider max temporarily raised to 300, p = 0.01).
- Reset button.

**Formulas.**

- `P(K = k) = C(n, k) p^k (1 − p)^(n − k)`. Compute in log space (`lgamma` via a Lanczos approximation, or iterative multiplication `P(k+1) = P(k) × (n − k)/(k + 1) × p/(1 − p)`) to stay stable at `n = 300`. Handle `p = 0` and `p = 1` as special cases.
- Mean `n p`, SD `√(n p (1 − p))`, rate SD `√(p (1 − p) / n)`.
- Mode: `floor((n + 1) p)`, and if `(n + 1) p` is a whole number between 1 and n, show both it and one less.

**Test values.**

| n | p | P(K=0) | P(K=1) | P(K=2) | P(K≥2) | Mean | SD | P(rate 15%-35%) |
|---|---|---|---|---|---|---|---|---|
| 8 | 0.10 | 0.4305 | 0.3826 | 0.1488 | 0.1869 | 0.80 | 0.8485 | — |
| 8 | 0.05 | 0.6634 | 0.2793 | 0.0515 | 0.0572 | 0.40 | 0.6164 | — |
| 6 | 0.25 | 0.1780 | 0.3560 | 0.2966 | 0.4661 | 1.50 | 1.0607 | 0.6526 |
| 20 | 0.25 | 0.0032 | 0.0211 | 0.0669 | 0.9757 | 5.00 | 1.9365 | 0.8069 |
| 200 | 0.25 | ≈0 | ≈0 | ≈0 | ≈1 | 50.00 | 6.1237 | 0.9992 |
| 300 | 0.01 | 0.0490 | 0.1486 | 0.2244 | 0.8024 | 3.00 | 1.7234 | — |

The band column uses the default 15% to 35% band, inclusive, and applies only when `p = 0.25`.

**Accessibility and style.** Shared palette from `templates/interactive-tokens.css`, light and dark themes, `prefers-reduced-motion` disables bar animations, all controls reachable by keyboard, no game art or class icons.
