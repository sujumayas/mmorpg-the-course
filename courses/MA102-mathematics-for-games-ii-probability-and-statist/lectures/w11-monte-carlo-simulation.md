# MA102 · Week 11 — Monte Carlo simulation

**Why this matters:** Most real game systems are too tangled for a clean formula. Mulligans, pity counters, crits that interact with health thresholds. Monte Carlo simulation lets you answer "how often does this happen?" for any system you can write as code, and tells you how far to trust the answer.

**You will be able to:**
- Write a Monte Carlo estimator for a probability or an expected value, with a fixed seed.
- Compute the 95% margin of error of a simulated probability and choose the number of trials needed for a target precision.
- Validate a simulation against an exact result before trusting it on a harder question.
- Critique a simulation for model errors (wrong rules) as distinct from sampling error (too few trials).

**Before class:** Eckhardt, R. (1987), "Stan Ulam, John von Neumann, and the Monte Carlo Method", *Los Alamos Science* 15, pp. 131-137 (read the first three pages). Schreiber, *Game Balance Concepts* (2010), Level 5, the section on computing probabilities by simulation. Revisit your [lab 07](../labs/lab07.md) code.

**Prerequisites from earlier courses:** [MA102 week 10, PRD and pity](w10-pseudo-random-distribution-and-pity-timers.md), [week 7, geometric distribution](w07-geometric-distribution-kills-until-the-drop.md), [week 5, variance](w05-variance-and-swingy-designs.md) and [week 3, the complement rule](w03-complement-rule-chance-of-at-least-one-drop.md). Loops, functions and lists from [CS101](../../CS101-programming-for-games-i/syllabus.md) weeks 3 to 5.

**Interactive:** [Monte Carlo mulligan](../examples/w11-monte-carlo-mulligan.html), open it during section 4.

---

## 1. When the formula runs out

Last week you needed the Dota 2 constant `C` for a 25% effect. There was no algebraic way to get it. You had to guess, compute, and adjust. That was a small taste of a big problem. Many questions designers ask have exact answers in principle, but the algebra is long, easy to get wrong, and has to be redone every time the rules change.

Some examples you could face in your first month on a design team:

- A card game lets you throw back cards from your opening hand. How often do you hold a key card by turn 3 if you throw back everything else?
- A crit system uses PRD, the boss has 1,000 HP, and crits double damage. What is the distribution of the number of hits to kill?
- A loot table drops two items per boss from a weighted list, with duplicate protection. How many clears until a 20-player raid has everything?

**Monte Carlo simulation** answers all of these the same way. Write the rules as a program. Run the program many times with random inputs. Count how often the event happens, or average the quantity you care about. The law of large numbers (week 1) guarantees that the average of many independent runs settles near the true value. The method's name, and its first serious use, date from 1946. Stanislaw Ulam, recovering from an illness, wondered how likely a game of Canfield solitaire was to come out. The combinatorics defeated him. It struck him that dealing a hundred games and counting the wins would be far more practical. He and John von Neumann turned that idea into a method for neutron physics at Los Alamos, and Nicholas Metropolis named it after the casino.

The word "simulation" can sound like a lesser answer. It is not. For a system with any complexity, a validated simulation is usually more trustworthy than a hand derivation, because the program is a direct translation of the rules and the derivation is a chain of clever steps where one slip ruins everything.

## 2. The recipe

Every Monte Carlo estimate in this course follows the same six steps.

1. **Write the rules as a function.** One call plays one complete trial: one opening hand, one boss fight, one player's pulls until a 5-star.
2. **Return one number per trial.** For a probability, return 1 if the event happened and 0 if not. For an expected value, return the quantity (hits to kill, pulls used, gold earned).
3. **Repeat `n` times** with a seeded random number generator.
4. **Average** the returned numbers. That average is your estimate, written with a hat: `p̂` for a probability, `x̄` for a mean.
5. **Attach a margin of error** (section 3).
6. **Validate** on a case you can solve exactly before you trust the program on the case you can't.

In Python, the skeleton is short:

```python
import random, math

def trial(rng):
    # play one complete round of the rules; return 1 if the event happened, else 0
    ...

def estimate(n, seed=42):
    rng = random.Random(seed)            # a private, seeded generator
    hits = sum(trial(rng) for _ in range(n))
    p_hat = hits / n
    margin = 1.96 * math.sqrt(p_hat * (1 - p_hat) / n)
    return p_hat, margin
```

Two habits in that code matter more than they look.

**Seed the generator.** A **seed** is the starting value of a pseudo-random number generator. The same seed gives the same sequence of "random" numbers every time. With a fixed seed, you and a colleague can run the same simulation and get the same answer to the last digit. That makes bugs reproducible and results reviewable. Change the seed to check that a result is not a fluke of one sequence.

**Use your own generator object.** `random.Random(seed)` gives the simulation its own stream. If other code also draws random numbers, your results do not change when that code changes.

## 3. How many trials is enough?

A simulated probability is itself random. Run 100 trials twice with different seeds and you get two different answers. How far off can you be?

Each trial returns 1 with probability `p` and 0 otherwise. From week 5, one such trial has variance `p(1 − p)`. The average of `n` independent trials has variance `p(1 − p) / n`. Its standard deviation is the **standard error**:

```
SE = sqrt( p̂ (1 − p̂) / n )
95% margin of error ≈ 1.96 × SE
```

The 1.96 comes from the normal curve (week 8). About 95% of the time, the true `p` lies within 1.96 standard errors of your estimate. Week 13 builds this into full confidence intervals. For now, use it as a ruler.

For an expected value, replace `p̂(1 − p̂)` with the sample variance of the returned numbers. The logic is the same.

Here is the ruler for a probability near 0.5, the worst case, and near 0.365, which you will meet in a moment:

| Trials n | ±margin, p ≈ 0.5 | ±margin, p ≈ 0.365 |
|---|---|---|
| 100 | ±9.8 points | ±9.4 points |
| 1,000 | ±3.1 points | ±3.0 points |
| 10,000 | ±0.98 points | ±0.94 points |
| 100,000 | ±0.31 points | ±0.30 points |
| 1,000,000 | ±0.10 points | ±0.09 points |

Every row has ten times the trials and only about a third of the margin. Precision grows like `sqrt(n)`. **To halve the error you need four times the trials.** To gain one more reliable decimal digit, you need a hundred times the trials.

Two practical rules follow.

- **Know your target first.** If the design decision only changes when a rate moves by 5 points, 1,000 trials is enough. Do not wait for a million.
- **Rare events are expensive.** For an event with `p = 0.0005` (the 1-in-2,000 PRD drought from week 10), 10,000 trials give about 5 hits and a margin of ±0.04 points, almost as big as the estimate. You need millions of trials, or a smarter method, for a tight answer.

## 4. Worked example: does throwing back your hand find your combo card?

### The hook

In *Hearthstone*, most decks are built around a few key cards, and a constructed deck may hold at most two copies of any non-Legendary card. Players talk constantly about "mulliganing for" a key card, that is, throwing back their opening hand to dig for it. How often does a hard mulligan find a two-copy card by turn 3 when going first? It is tempting to guess well above half. It is almost exactly half. Without a mulligan it is barely over a third. You will get both numbers two ways, by simulation and by exact calculation, and see why simulation is the one you would reach for first.

### The model

The rules, as documented on the Hearthstone Wiki (current rules, 2026):

- The deck has 30 cards. Our key card appears twice.
- The player going first gets 3 cards. The player going second gets 4 cards plus The Coin, a spell that does not affect this question.
- **Mulligan.** You choose any cards to replace. Replacements come from the top of the deck. Only after you have your replacements are the replaced cards shuffled back into the deck. So you cannot draw back a card you just threw away as its own replacement.
- You draw one card at the start of each of your turns, including turn 1 for the first player.

So by the start of your turn 3, going first, you have seen 3 opening cards and 3 turn draws, 6 cards in all. Going second, 4 + 3 = 7.

The strategy we test is the **hard mulligan**: if the opening hand has no copy of the key card, throw back every card.

The simulation needs exactly one function:

```python
def trial(rng, first=True, mulligan=True):
    deck = [1, 1] + [0] * 28           # 1 = key card
    rng.shuffle(deck)
    k = 3 if first else 4
    hand, rest = deck[:k], deck[k:]
    if mulligan and 1 not in hand:
        new, rest = rest[:k], rest[k:]  # replacements from the top
        rest = rest + hand              # tossed cards go back...
        rng.shuffle(rest)               # ...and the deck is shuffled
        hand = new
    hand += rest[:3]                    # draws for turns 1, 2, 3
    return 1 if 1 in hand else 0
```

Notice what the code does not need. There is no combinatorics in it. It is a line-by-line copy of the rules.

### Numbers you can check

**Step one: validate.** Without a mulligan, there is an exact answer from the complement rule of week 3. The chance that none of the 6 cards seen is a copy is `C(28,6) / C(30,6)`, where `C(n,k)` counts the ways to choose `k` cards from `n`. That ratio simplifies to `(24 × 23) / (30 × 29) = 552 / 870`. So

```
P(key card by turn 3, going first, no mulligan)  = 1 − 552/870 ≈ 0.3655
P(key card by turn 3, going second, no mulligan) = 1 − (23 × 22)/(30 × 29) = 1 − 506/870 ≈ 0.4184
```

Now run the simulation with seed 42 and a growing number of trials:

| Trials | Going first, no mulligan | ±margin | Covers 0.3655? |
|---|---|---|---|
| 100 | 0.450 | ±0.098 | yes |
| 1,000 | 0.359 | ±0.030 | yes |
| 10,000 | 0.364 | ±0.009 | yes |
| 1,000,000 | 0.3650 | ±0.0009 | yes |

At 100 trials the estimate is off by 8.5 points, which is inside its honest margin. By a million trials it matches to three decimals. The program passes validation. Now, and only now, trust it with the question you could not answer by hand.

**Step two: the real question.** Same seed, hard mulligan on:

| Trials | Going first, hard mulligan | Going second, hard mulligan |
|---|---|---|
| 1,000 | 0.495 ± 0.031 | 0.591 ± 0.031 |
| 10,000 | 0.500 ± 0.010 | 0.585 ± 0.010 |
| 1,000,000 | 0.5009 ± 0.0010 | 0.5871 ± 0.0010 |

A hard mulligan raises the first player's chance from 36.6% to about 50.1%, and the second player's from 41.8% to about 58.7% (the exact value, by the method below, is 58.66%). Half the time, going first, you throw away a whole hand and still do not have the card on turn 3.

**Step three: an exact cross-check.** This case happens to be solvable, and doing it shows why you would rather not. Going first:

- The opening 3 cards contain a copy with probability `1 − C(28,3)/C(30,3) = 1 − 3276/4060 ≈ 0.1931`.
- Otherwise (probability 0.8069), you draw 3 replacements from 27 cards holding both copies. The chance they miss both is `C(25,3)/C(27,3) = 2300/2925 ≈ 0.7863`.
- The 3 tossed cards return, so the deck is again 27 cards with both copies. The 3 turn draws miss with the same chance, 0.7863.

```
P = 0.1931 + 0.8069 × (1 − 0.7863 × 0.7863)
  = 0.1931 + 0.8069 × 0.3817
  ≈ 0.5011
```

The simulation's 0.5009 ± 0.0010 contains it. Two independent methods agree, which is the strongest evidence you can get that both are right. But notice how much depended on one rules detail, that tossed cards return only after replacements are drawn. Get that wrong in the algebra and every line after it is wrong. Get it wrong in the code and it is one line to fix. Change the strategy to "keep a copy of a second key card too" and the algebra grows a new branch for every case. The simulation changes one `if`.

### Move it yourself

Open `examples/w11-monte-carlo-mulligan.html`. The left view animates hands being dealt, a few per second, so you can see individual trials. The right view plots the running estimate `p̂` against the number of trials on a log axis, with the shaded 95% band `±1.96 SE` around it and a horizontal line at the exact answer. Press "Run 10,000" and watch the estimate wander widely at first, then settle while the band narrows like `1/sqrt(n)`. Toggle the mulligan and going first or second. One picture carries the insight. The estimate is noisy, the band says how noisy, and the band contains the truth about 95% of the time.

### Same idea elsewhere

Every item here rewrites into the same form: *one function plays one trial and returns a number, and the average of many trials estimates the answer.*

**Canfield solitaire, 1946.** Ulam's original question. `trial()` deals and plays one game of Canfield and returns 1 for a win. The rules are simple to code and nearly impossible to analyze in closed form. That is the ideal Monte Carlo problem, and it is where the method began.

**Magic: The Gathering.** Since the London mulligan (adopted in 2019, with Core Set 2020), a player who mulligans draws a fresh seven cards and then puts one card on the bottom of the library for each mulligan taken. Questions like "how often does a 60-card deck with 24 lands have between two and four lands in an opening hand, if I mulligan hands with zero, one, six or seven lands?" are routinely answered by exactly the simulation above. Change 30 to 60, 3 to 7, and the keep rule.

**Genshin Impact expected pulls.** In week 10 you summed survival probabilities to get 62.30 expected pulls under the community soft-pity model. As a simulation, `trial()` pulls until a 5-star and returns the pull count. With 100,000 simulated players and seed 1, the average is 62.36 with a standard error of about 0.08. The exact 62.30 sits inside the margin. The simulated consolidated rate is `1 / 62.36 ≈ 1.604%`.

Different games, one method. You can now estimate any rate for any rule set you can write down.

### Design judgment

Simulation is the designer's default tool for probability, but it has failure modes that exact math does not. Decide these deliberately.

- **Model error beats sampling error.** A million trials of the wrong rules give a very precise wrong answer. The margin of error only measures randomness, never mistakes. That is why validation on a known case comes first, and why you should have a second person read `trial()` against the rules document.
- **Validate at the edges too.** Test a case where the answer is 0 or 1 (a deck of 30 copies of the key card) and one where you know the exact value. Bugs hide at boundaries.
- **Match precision to the decision.** A designer choosing between a 45% and a 55% design needs 1,000 trials. A live-ops analyst promising a published drop rate to within 0.1 points needs a million. Spending more is waste, spending less is guessing.
- **Keep the exact formula when you have it.** A closed form tells you why, and how the answer moves with each parameter. Simulation tells you what, for these parameters. Use the simulation to check the formula and the formula to explain the simulation.
- **Rare events need care.** If the event you care about happens once in a million trials, plain Monte Carlo is the wrong tool. Compute it exactly, or ask a data scientist about variance-reduction techniques.

### Check this example

1. Going second with no mulligan, you have seen 7 cards by turn 3. Confirm the exact 0.4184 from the formula, then state how many trials you need for a ±1 point margin.
2. A teammate's simulation says a hard mulligan going first gives 0.587 ± 0.001. The exact answer is 0.5011. Name the most likely rules bug.

<details>
<summary>Answers</summary>

1. `C(28,7)/C(30,7) = (23 × 22)/(30 × 29) = 506/870 ≈ 0.5816`, so the chance is `0.4184`. For ±0.01, solve `1.96 × sqrt(0.418 × 0.582 / n) = 0.01`, giving `n ≈ 9,350` trials.
2. 0.587 is the going-second value. The simulation almost certainly deals 4 opening cards (and 4 replacements) to the player going first. The margin of error is tiny, so this is a model error, not bad luck. It is exactly the kind of mistake validation against the no-mulligan exact value (0.3655) would have caught first.

</details>

## 5. Simulating whole distributions

A simulation can return more than a yes or no. Return the full outcome and keep every value, and you get the entire distribution. You can read off its mean, median, spread and tail, the descriptive statistics you meet next week.

Here is a case where that pays off, and where the result surprises. A boss has 1,000 HP. Each hit deals 100 damage, and a crit deals 200. The crit rate is 25%. How many hits to kill?

With independent crits at 25%, simulating 200,000 fights (seed 7) gives:

| Hits to kill | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|
| Independent 25% | 3.7% | 20.6% | 39.0% | 29.4% | 7.4% |
| PRD, C = 0.0847, counter fresh at fight start | 0.2% | 7.7% | 51.3% | 40.4% | 0.4% |

(Rare 5-hit kills under independent crits, about 0.1%, are left out of the table.)

The PRD fights are far more predictable. 92% end in 8 or 9 hits, compared with 68% for independent rolls. That is the week 10 story. But look at the means. Independent: 8.16 hits. PRD: 8.33 hits. PRD kills *slower* on average, even though both are "25% crit".

Why? The PRD rate is 25% only in the long run. On the first attack of a fresh counter the chance is 8.5%, then 17%, then 25.4%. A fight of about 8 hits spends most of its time in the low part of the ramp, so fewer crits land than 25% of 8. If your game resets the counter at the start of each fight, the realized crit rate in short fights is below the tooltip. If the counter persists between fights, as it does per unit in Dota 2, the effect mostly disappears. That single assumption changes the answer. You would not find this by reasoning about "25% crit". You find it in ten lines of simulation, and then you go and read the spec to see which assumption is true.

## In-class activity (25 minutes)

Work in pairs with a laptop and Python (a notebook is fine).

1. **Validate (10 min).** Write `trial()` for one turn of *Yahtzee*-style dice: roll five six-sided dice, keep the most common face, reroll the rest, twice more. Return 1 if all five match. The known answer for this "keep the most common value" strategy is about 4.60%. Run 10,000 and 200,000 trials with a fixed seed and report `p̂ ± margin`. Does the margin cover 4.60%?
2. **Break it on purpose (5 min).** Introduce one plausible bug (forget to keep the dice between rolls, or reroll all five). Record how far the answer moves. Would your margin of error have warned you? (It would not. That is the point.)
3. **Extend (10 min).** Change the rule to "keep the most common face, but if there is a tie, keep the higher face". Estimate the new rate and state whether the difference from step 1 is larger than the combined margins.

Expected output: a four-row table (validated rate, bugged rate, extended rate, exact reference) with margins, and one sentence on what the margin can and cannot protect you from.

## Common misconceptions

- **"More trials fix everything."** More trials shrink sampling error. They do nothing about wrong rules. A precise wrong answer is still wrong.
- **"10 times the trials gives 10 times the precision."** Precision grows like `sqrt(n)`. Ten times the trials cuts the margin by about a factor of 3.2.
- **"A simulation isn't real math."** It is a statistical estimate with a known error, grounded in the law of large numbers. Physicists have used it since 1946 for problems no one can solve by hand.
- **"If two runs disagree, the program is broken."** Two runs with different seeds should disagree, by about the margin of error. Worry if they disagree by much more than that, or if runs with the same seed disagree at all.

## Check yourself

1. You need a crit-rate estimate within ±0.5 percentage points (95%) for a rate near 30%. How many trials?
2. A simulation of 2,500 raid clears estimates a drop rate of 4.0%. Give the 95% margin. Is it consistent with a claimed rate of 5%?
3. A colleague runs a mulligan simulation with 1,000 trials and gets 0.47, then 0.53 with a different seed. Is something wrong? Explain with numbers.
4. Your simulated mean pulls for a gacha rule is 58.1 with a sample standard deviation of 22 across 40,000 simulated players. What is the standard error of the mean? Is an exact answer of 58.4 consistent with it?

<details>
<summary>Answers</summary>

1. `1.96 × sqrt(0.3 × 0.7 / n) = 0.005` gives `n = 0.21 × (1.96/0.005)^2 ≈ 32,300` trials.
2. `SE = sqrt(0.04 × 0.96 / 2500) ≈ 0.0039`, so the margin is about ±0.8 points. The interval is roughly 3.2% to 4.8%. A 5% rate lies just outside, so the data sit uneasily with the claim. Week 14 turns this into a formal test.
3. Probably not. At n = 1,000 and p near 0.5, the margin is about ±3.1 points, so two runs can easily differ by 6 points. Run more trials before suspecting a bug.
4. `SE = 22 / sqrt(40000) = 0.11`. The margin is about ±0.22, so the interval is about 57.9 to 58.3. An exact 58.4 falls just outside, which is worth a second look at the rules or the formula.

</details>

## Lab hook

**[Lab 11: Monte Carlo lab (graded, 20% of the course)](../labs/lab11.md).** You build a validated simulation of a loot system with pity, report every estimate with a margin, and answer three design questions that have no closed form. It reuses your lab 07 and lab 10 code.

## Sources

- Eckhardt, R. (1987). "Stan Ulam, John von Neumann, and the Monte Carlo Method." *Los Alamos Science*, Special Issue 15, pp. 131-137. Ulam's Canfield solitaire question in 1946, the collaboration with von Neumann, and Metropolis naming the method.
- Hearthstone Wiki (hearthstone.wiki.gg), "Mulligan" (current rules, accessed September 2026). Opening hand sizes of 3 and 4 plus The Coin, replacements drawn before tossed cards are shuffled back.
- Blizzard Entertainment, *Hearthstone* deck-building rules: 30-card constructed decks, at most two copies of a non-Legendary card (in-game collection manager, current).
- Wizards of the Coast (2019), "The London Mulligan", magic.wizards.com, 3 June 2019. The draw-seven, bottom-one-per-mulligan rule adopted with Core Set 2020.
- Cornell University Math Explorers' Club, "Yahtzee Solutions" (2006-2007). The roughly 4.6% chance of five of a kind in one turn under the keep-the-most-common strategy.
- Genshin Impact figures and the community soft-pity model: see the Sources section of [week 10](w10-pseudo-random-distribution-and-pity-timers.md).
- Liquipedia Dota 2 Wiki, "Random Distribution" (accessed September 2026). PRD constant for 25% and per-unit counters.

## Interactive spec: examples/w11-monte-carlo-mulligan.html

**Insight the visual must make obvious:** a simulated probability wanders at small n and settles as n grows, the 95% band narrows like 1/sqrt(n), and the band contains the exact answer. Precision is bought with the square of the effort.

**Layout.** Two linked views, stacked on mobile, side by side from 900px.

1. **Hand viewer (left or top).** Shows the latest trial as a row of card rectangles: opening hand, mulligan replacements (if any, with the tossed cards greyed and labelled "shuffled back"), then three turn draws. Key-card copies are highlighted in the accent color; all other cards are plain. Below it, a running tally of hits and trials. No card art; generic rectangles with "K" for the key card.
2. **Convergence plot (right or bottom).** X axis: number of trials, log scale from 10 to 10^6. Y axis: estimated probability, 0.2 to 0.8. A line of the running estimate `p̂`, a shaded band `p̂ ± 1.96 × sqrt(p̂(1−p̂)/n)`, and a horizontal dashed line at the exact value for the current settings, labelled.

**Controls** (all keyboard accessible):
- Toggle "Going first / Going second".
- Toggle "Hard mulligan on / off".
- Buttons: "Deal 1", "Run 100", "Run 10,000", "Run 1,000,000" (the last runs in chunks via requestAnimationFrame so the page stays responsive; the hand viewer only shows the final trial). "Reset".
- Seed field (integer, default 42) using a seeded PRNG (mulberry32). Same seed and settings must reproduce the same curve.
- Checkbox "Show 20 independent runs" that overlays 20 faint running-estimate lines with seeds 1-20, making the 1/sqrt(n) funnel shape visible.

**Model.** Deck of 30 with 2 key cards. Opening hand 3 (first) or 4 (second). If mulligan is on and the hand has no key card, replace all opening cards: take replacements from the top of the remaining deck, then append the tossed cards to the remaining deck and shuffle it. Then draw 3 more cards. Success if any key card is in hand.

**Exact reference values** (shown as the dashed line):
- First, no mulligan: `1 − 552/870 = 0.36552`.
- Second, no mulligan: `1 − 506/870 = 0.41839`.
- First, hard mulligan: `0.19310 + 0.80690 × (1 − (2300/2925)^2) = 0.50109`.
- Second, hard mulligan: compute the same way with 4-card hands: `P0 = 1 − C(28,4)/C(30,4)`, replacement miss `C(24,4)/C(26,4)`, turn-draw miss from a 26-card deck `C(24,3)/C(26,3)`; `P = P0 + (1 − P0)(1 − miss_repl × miss_draw)`. The result is 0.58661; the simulated value at 10^6 trials with seed 42 was 0.5871 ± 0.0010.

**Readout table:** n, hits, `p̂`, SE, 95% margin, exact value, and "exact inside band?" (yes/no).

**Test values:** with seed 42, going first, no mulligan, the estimate at n = 10^6 must lie within ±0.0015 of 0.3655; hard mulligan within ±0.0015 of 0.5011. The margin at n = 100 and p̂ = 0.5 must read ±0.098.

**First screen:** going first, hard mulligan on, 20-run overlay visible, already run to n = 10,000, so the funnel and the exact line are visible before any interaction.
