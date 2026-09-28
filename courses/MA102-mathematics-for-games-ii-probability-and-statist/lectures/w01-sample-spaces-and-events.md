# MA102 · Week 01 — Probability basics: sample spaces and events

**Why this matters:** Every crit, dodge, drop and shuffle in a game is a probability that a designer picked, whether on purpose or by accident. This week gives you the one skill that makes the rest of the course work. You will learn to list what can happen, count the part you care about, and turn that count into a number you can defend in a design review.

**You will be able to:**
- Write the sample space of a game roll and identify an event as a subset of it.
- Compute the probability of an event by counting equally likely outcomes, and by summing weights when outcomes are not equally likely.
- Compute "and", "or" and "not" probabilities on a two-roll grid, using the addition rule without double counting.
- Critique a rule of thumb such as "advantage is worth +5" by computing where it holds and where it fails.

**Before class:** Ian Schreiber, *Game Balance Concepts* (blog course, 2010), Level 4, "Probability and Randomness", read up to the section on cards. Schreiber & Romero, *Game Balance* (2021), the chapter on probability and dice, first half.

**Prerequisites from earlier courses:** Fractions, percentages and reading a function's graph from MA101 [week 1, functions as machines](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w01-functions-as-machines.md) and [week 2, linear functions and rates](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w02-linear-functions-and-rates.md). You will reuse MA101's habit of drawing two views of the same quantity.

**Interactive:** [examples/w01-advantage-grid.html](../examples/w01-advantage-grid.html) (built from the spec at the end of this lecture). Keep it open during section 2.

---

## 1. Randomness you can count

Start with the smallest possible random thing in a game, one roll of a 20-sided die. Before you can say anything about chances, you need three words.

A **random experiment** is any process whose result you cannot predict in advance but whose possible results you can list. Rolling a die, opening a chest, and drawing a card are all random experiments.

An **outcome** is one possible result of the experiment. Rolling a 17 on a d20 is an outcome.

The **sample space**, written `S`, is the set of every possible outcome. For one d20 it is `S = {1, 2, 3, ..., 20}`, which has 20 outcomes.

An **event** is any group of outcomes you care about. It is a subset of the sample space. "Roll 15 or higher" is the event `E = {15, 16, 17, 18, 19, 20}`. "Roll a natural 20" is the event `{20}`. "Roll anything" is the whole of `S`. "Roll a 21" is the empty event, which contains no outcomes.

Here is the first formula of the course. When every outcome in the sample space is equally likely,

```
P(E) = |E| / |S|
```

- `P(E)` is the probability of event `E`, a number from 0 to 1.
- `|E|` is the number of outcomes in the event.
- `|S|` is the number of outcomes in the sample space.

So the chance of rolling 15 or higher on a fair d20 is `6 / 20 = 0.30`, or 30%. The chance of a natural 20 is `1 / 20 = 5%`.

Three facts follow straight from the formula, and you will use them every week:

- Every probability is between 0 (the event never happens) and 1 (the event always happens).
- `P(S) = 1`. Something in the sample space always happens.
- If you split the sample space into pieces that do not overlap, their probabilities add up to 1.

That last fact is the most useful debugging tool in probability. If you build a loot table and the chances of all its rows add to 1.07, you have a bug, not a generous boss.

### Two ways to read a probability

A probability of 30% has two readings, and good designers switch between them without thinking.

The **counting reading** says that 6 of the 20 equally likely faces are in the event. This is what you compute on paper.

The **frequency reading** says that if you rolled the die many thousands of times, close to 30% of the rolls would land in the event. This is what players experience, and it is what a simulation measures. The two readings agree because of a result called the law of large numbers, which week 11 (Monte Carlo simulation) makes precise. For now, trust that counting predicts long-run frequency, and notice the phrase "long-run". Over five rolls, anything can happen. Weeks 2 and 13 are about what that means for players.

### Choosing the sample space is a design decision

The formula `|E| / |S|` only works when every outcome is equally likely. That sounds like a technicality. It is actually where most beginner mistakes live.

Roll two six-sided dice and add them. You could write the sample space as the sums, `{2, 3, ..., 12}`, which has 11 outcomes. Then `P(sum = 7) = 1/11`? No. The sums are not equally likely. There is one way to roll a 2 (a 1 and a 1) and six ways to roll a 7. The correct equally likely sample space is the 36 ordered pairs `(first die, second die)`, and `P(sum = 7) = 6/36 = 1/6`.

The rule of thumb: **write the sample space as the raw physical results, before you add, compare, or throw anything away.** Then build the event you care about from those raw results. Week 8 comes back to dice sums in depth. This week you will use the same trick on a mechanic that sits in thousands of games, rolling two dice and keeping one.

## 2. Worked example: is advantage worth +5?

### The hook

In *Baldur's Gate 3* (Larian Studios, 2023), and in the tabletop *Dungeons & Dragons* fifth edition rules it adapts, many situations grant **advantage**. You roll two d20s and keep the higher one. Its opposite, **disadvantage**, keeps the lower one.

Players talk about advantage as roughly "+5", and the 2014 Player's Handbook backs them up in one place. For passive checks, where nobody rolls, the rule says to add 5 for advantage and subtract 5 for disadvantage.

So is advantage worth +5? If you were designing a buff for your own game and had to choose between "roll twice, keep the higher" and "+5 to the roll", would it matter which one you picked?

Your intuition probably says "about the same". The answer is that they are identical at one meaningful target number and different almost everywhere else.

### The model

Advantage is two separate d20 rolls, so the raw sample space is every ordered pair of results.

```
S = { (a, b) : a in 1..20, b in 1..20 }       |S| = 20 × 20 = 400
Result with advantage = max(a, b)
Success event E_T = { (a, b) : max(a, b) >= T }
```

- `a` and `b` are the two die results. Each of the 400 pairs is equally likely.
- `T` is the target number, the value you need to roll to succeed. D&D calls it the difficulty class, or DC.
- `max(a, b)` is the higher of the two results.

Counting `E_T` directly is fiddly. Count the outcomes that are **not** in it instead. You fail only if both dice are below `T`. Each die has `T − 1` values below `T`, so there are `(T − 1) × (T − 1)` failing pairs. The rest succeed:

```
|E_T|        = 400 − (T − 1)²
P(adv, T)    = 1 − ((T − 1) / 20)²
P(+5, T)     = (26 − T) / 20, clipped to the range 0..1
P(plain, T)  = (21 − T) / 20
```

The `+5` line comes from counting too. With a +5 bonus you need a die result of `T − 5` or more, and there are `20 − (T − 5) + 1 = 26 − T` such faces.

Counting the failures and subtracting from the total is called the **complement rule**. Week 3 is built entirely on it. You have just used it once because it turned a messy count into a clean square.

### Numbers you can check

Here is the table for a selection of targets. Verify at least two rows by hand before you open the interactive.

| Target T | Plain d20 | Advantage | +5 bonus | Disadvantage | Successful pairs (of 400) |
|---|---|---|---|---|---|
| 2 | 95.0% | 99.75% | 100% | 90.25% | 399 |
| 6 | 75.0% | 93.75% | 100% | 56.25% | 375 |
| 8 | 65.0% | 87.75% | 90.0% | 42.25% | 351 |
| 11 | 50.0% | 75.0% | 75.0% | 25.0% | 300 |
| 14 | 35.0% | 57.75% | 60.0% | 12.25% | 231 |
| 16 | 25.0% | 43.75% | 50.0% | 6.25% | 175 |
| 18 | 15.0% | 27.75% | 40.0% | 2.25% | 111 |
| 20 | 5.0% | 9.75% | 30.0% | 0.25% | 39 |

Check the T = 11 row. Failing pairs are those where both dice show 1 to 10, so `10 × 10 = 100`. Successes are `400 − 100 = 300`, and `300 / 400 = 75%`. With +5, you need a 6 or higher, which is 15 faces of 20, also 75%. At this one target the rule of thumb is exact.

Now check T = 20. Failing pairs have both dice at 1 to 19, so `19 × 19 = 361` fail and 39 succeed, giving 9.75%. With +5 you need a 15 or higher, six faces, 30%. The "+5" rule overstates advantage by a factor of three.

Disadvantage keeps the lower die, so you succeed only if **both** dice reach `T`. Each die has `21 − T` good faces, which gives `(21 − T)²` successful pairs out of 400. At T = 11 that is `10 × 10 / 400 = 25%`.

One more number to note. Averaged over all 400 pairs, the kept die shows 13.825, compared with 10.5 for one die. So advantage raises the **average** roll by only about 3.3, yet at T = 11 it adds 25 percentage points to the success chance, the same as a flat +5. Average roll and chance of success are different quantities, and the question "what is advantage worth?" has no answer until you say which one you mean.

### The visual

Open `examples/w01-advantage-grid.html`. The left panel is the sample space itself, a 20 by 20 grid of squares, one per pair `(a, b)`. Squares in the success event light up. Drag the target slider and watch the lit region. It is always an L-shape, the whole grid minus a dark square in the bottom-left corner whose side is `T − 1`.

The right panel plots success chance against target for plain, advantage, +5 and disadvantage. The advantage curve is a bent line, steep in the middle and flat at the ends. The +5 line is straight until it hits 100%. They touch at T = 11 and nowhere else, apart from T = 1, where every roll succeeds anyway.

The two views explain each other. The grid tells you **why** the curve bends. The failing corner is a square, so it grows with the square of `T − 1`. A square grows slowly when it is small and fast when it is large, which is why advantage adds little at easy targets, a lot in the middle, and little again at hard targets where the corner nearly fills the grid.

### Cross-game recognition

The move you just made, writing two random numbers as a grid and shading the event, recurs across many games.

**Fire Emblem (The Binding Blade through Awakening, and Three Houses).** These games show the player a hit chance, say 90%. The game then draws **two** random numbers from 0 to 99 and averages them. The attack hits if the average is below the displayed number. The sample space is a 100 by 100 grid of 10,000 pairs, and the event is `a + b < 2H` where `H` is the displayed hit chance. Count the pairs and you get the "true hit". A displayed 90 is really 98.1%. A displayed 70 is really 82.3%. A displayed 50 is 50.5%, nearly unchanged. The two-number average pulls low results lower and high results higher, which makes likely hits more reliable and long shots rarer. This is a clean case of the rule from the MMO303 exemplar: distinguish what the game **shows** from what it **computes**. Later titles in the series (Fates, Shadows of Valentia, Engage) moved to a hybrid rule, so always name the game.

**Disadvantage, in the same games.** Keeping the lower die is the same 400-square grid with a different event. The success region is now the top-right square of side `21 − T`. A single grid holds advantage, disadvantage and a plain roll. That is the payoff of listing the raw sample space first. Any rule you can state about the two dice becomes a region you can count.

**Advantage in Baldur's Gate 3 specifically.** The video game applies advantage to attack rolls, ability checks and saving throws, and several sources of advantage do not stack. You still roll only two dice. In sample-space terms, three sources of advantage give the same 400-square grid as one, which is a deliberate cap. A designer who allowed stacking would be adding a third axis, a cube of 8,000 outcomes, and the failure corner would shrink as a cube instead of a square.

Three games, one idea. When you meet a "roll twice" or "combine two numbers" mechanic, draw the grid and shade the event before you trust anyone's rule of thumb.

### Eyes-open design judgment

When should you give players advantage, and when a flat bonus?

- **Advantage is self-limiting.** It can never push a success chance to 100% or a failure chance to 0. Stacking modifiers on a flat bonus can. If your game has many sources of buffs, a roll-twice mechanic protects you from bonuses that make checks automatic.
- **Advantage matters most in the middle.** It barely helps on easy checks and helps little on near-impossible ones. If you want a buff that lets a weak character attempt a heroic long shot, a flat bonus does that job and advantage does not.
- **Advantage is easy to state and hard to estimate.** Players cannot compute 9.75% in their heads. If your UI shows a percentage, compute it from the grid. If it shows "+5 equivalent", you are misleading anyone attempting a hard check.
- **Two-number averaging changes feel.** Fire Emblem's rule makes displayed numbers feel trustworthy at the top, at the cost of honesty. Decide deliberately whether your displayed number is the computed number. If it is not, expect players to find out and tell each other.

The deliberate choice is this. Decide which quantity your buff should change, average result or chance of success at the targets that matter, and pick the mechanic that changes that quantity.

### Check yourself (worked example)

1. With advantage, what is the chance of rolling at least 16? Count the failing corner and show the division.
2. With disadvantage, how many of the 400 pairs succeed at T = 6? What is that as a percentage?
3. A designer offers "reroll once if you fail" instead of advantage. Draw the sample space. Is it the same event as advantage? (Hint: when do you roll the second die, and does it matter?)

<details>
<summary>Answers</summary>

1. Failing pairs have both dice at 1 to 15, so `15 × 15 = 225` fail and `175` succeed. `175 / 400 = 43.75%`.
2. Each die needs 6 or higher, which is 15 faces, so `15 × 15 = 225` pairs succeed. `225 / 400 = 56.25%`.
3. Yes. You fail only if both the first roll and the reroll are below T, the same corner of `(T − 1)²` pairs. Whether you roll the second die up front or only after a failure changes the pacing at the table, not the probability.

</details>

## 3. Combining events: and, or, not

Once events are regions of a sample space, combining them is just combining regions. Use the 400-square advantage grid as your picture throughout this section.

Let `A` be "the first die is 11 or higher" and `B` be "the second die is 11 or higher". Each covers half the grid, 200 squares, so `P(A) = P(B) = 0.5`.

**Not.** The **complement** of `A`, written `not A`, is every outcome outside `A`. It covers the other 200 squares. In general,

```
P(not A) = 1 − P(A)
```

**And.** The **intersection** `A and B` contains outcomes in both events. Here that is the top-right quarter, where both dice are 11 or higher, so 100 squares and `P(A and B) = 0.25`. Notice that this is exactly disadvantage at T = 11.

**Or.** The **union** `A or B` contains outcomes in at least one event. Here it is 300 squares, 75%. That is advantage at T = 11, as it should be. Advantage succeeds if either die succeeds.

Now the most common error in the whole topic. Why is `P(A or B)` 75% and not `0.5 + 0.5 = 100%`? Because adding the two regions counts the top-right quarter twice. The fix is the **addition rule**:

```
P(A or B) = P(A) + P(B) − P(A and B)
          = 0.5  + 0.5  − 0.25 = 0.75
```

Two events are **mutually exclusive** if they cannot both happen, so their intersection is empty. For mutually exclusive events, and only then, you can simply add: `P(A or B) = P(A) + P(B)`. "Roll a 1" and "roll a 20" on one die are mutually exclusive, so the chance of either is `1/20 + 1/20 = 10%`.

A game example where this bites. A weapon has "10% chance to stun" and "10% chance to burn" on each hit, rolled separately. A tooltip that says "20% chance to apply a status effect" is wrong. If the two rolls are independent (week 2 defines this properly), the chance of both is `0.1 × 0.1 = 1%`, and the chance of at least one is `0.1 + 0.1 − 0.01 = 19%`. One percentage point sounds small. On a skill with ten such effects the gap is large, and it is the kind of error that shows up in patch notes.

## 4. When outcomes are not equally likely

Many game systems do not roll dice with equal faces. A loot table lists items with **weights**, and the chance of each item is its share of the total weight.

| Item | Weight | Probability |
|---|---|---|
| Gold pile | 60 | 60 / 100 = 60% |
| Health potion | 25 | 25 / 100 = 25% |
| Rare ring | 10 | 10 / 100 = 10% |
| Epic sword | 4 | 4 / 100 = 4% |
| Legendary gem | 1 | 1 / 100 = 1% |
| Total | 100 | 100% |

The sample space is still the five items, but they are not equally likely, so `|E| / |S|` does not apply. Counting rows would give each item 20%. The general rule replaces counting with summing:

```
P(E) = sum of the probabilities of the outcomes in E
```

For "any item better than a potion" you add the ring, sword and gem, `10% + 4% + 1% = 15%`.

There is a useful way to see why weights work. Imagine 100 tickets in a hat, 60 labelled "gold", 25 "potion", and so on. Now every ticket is equally likely, and you are back to counting. A weighted table is just an equally likely sample space in which some outcomes have been given the same label. Week 9 builds full loot tables on this idea, including tables that roll on other tables.

Two practical warnings for implementation:

- **Weights do not need to sum to 100.** A table with weights 3, 1 and 1 gives 60%, 20% and 20%. Programmers often assume a sum of 100, then add an item and quietly change every other chance. Always divide by the actual total.
- **Adding a row changes every other row's chance.** Put a new item with weight 25 in the table above and the legendary gem drops from 1% to `1 / 125 = 0.8%`. Designers who tune "the gem's drop rate" in isolation get surprised by this.

## 5. What a probability does and does not promise

A probability describes the long run. It says nothing firm about the next roll or the next ten. With a 75% chance to hit, missing three times in a row has a probability of `0.25 × 0.25 × 0.25 ≈ 1.6%`, assuming the rolls do not affect each other. That is rare for one player in one fight. Across a million players making thousands of attacks a day, it happens constantly, and each of those players has a story about the game cheating them.

This is the bridge to next week. Week 2 defines independence, explains why players feel "due" for a drop, and shows how some games change their randomness to match that feeling. Keep the distinction from this week in mind. The probability is the fraction of the sample space. The experience is what one player sees in a short run, and it can look very different.

## In-class activity (25 minutes)

Work in pairs. Each pair needs two d20s (or a dice app), grid paper, and a laptop with a spreadsheet.

1. **Predict (3 min).** Without computing, each partner writes down a guess for the chance of success with advantage at T = 18. Record both guesses.
2. **Draw (7 min).** On grid paper, draw the 20 by 20 sample space. Shade the failing corner for T = 18. Count the squares and compute the probability. Compare with your guesses.
3. **Roll (8 min).** Roll advantage at T = 18 forty times and tally successes. Pool your tally with two neighbouring pairs, 120 rolls in total. How close is the pooled frequency to your computed answer? How close was your own 40-roll tally?
4. **Design (7 min).** Your game needs a buff for a rogue's "ambush" that should raise the chance of a hard hit (T = 18) to at least 40%. Choose between advantage, +5, and "roll three d20s keep the highest". Compute each option's chance at T = 18 and at T = 8. For three dice, the failing region is a cube, so the chance is `1 − ((T − 1)/20)³`.

**Expected output:** one sheet per pair with the grid, the computed probability, the pooled frequency, and a two-sentence recommendation for the ambush buff with both targets' numbers.

## Common misconceptions

- **"Advantage is +5."** Only at T = 11. It is worth less than +5 at every other target, and much less at hard targets, where a flat bonus is up to three times as strong.
- **"Two outcomes, so 50/50."** A chest either has the legendary gem or it does not, but those two outcomes are not equally likely. The formula `|E| / |S|` needs equally likely outcomes. List the raw results first.
- **"Or means add."** Adding works only for mutually exclusive events. Otherwise subtract the overlap, or you count it twice.
- **"The displayed number is the computed number."** Fire Emblem's displayed 90 is a computed 98.1. Always check how a game turns its shown value into a roll.

## Check yourself

1. A 2d6 roll succeeds on a sum of 10 or more. Write how many of the 36 ordered pairs succeed and give the probability.
2. A table has weights 50 (common), 30 (uncommon), 15 (rare), 5 (epic). A designer adds a legendary with weight 5. What is the new chance of a rare?
3. With advantage on a d20, what is the smallest target T at which the chance of success is below 50%?
4. A spell has a 30% chance to freeze and a 20% chance to knock back, rolled independently. What is the chance it does at least one of them? What is the chance it does neither?

<details>
<summary>Answers</summary>

1. Sum 10 has 3 pairs, 11 has 2, 12 has 1, so 6 pairs. `6 / 36 = 1/6 ≈ 16.7%`.
2. The new total is 105. `15 / 105 ≈ 14.3%`, down from 15%.
3. Need `1 − ((T − 1)/20)² < 0.5`, so `(T − 1)² > 200`, so `T − 1 ≥ 15`. At T = 15 the chance is `1 − 196/400 = 51%`. At T = 16 it is 43.75%. The answer is T = 16.
4. Both happen with chance `0.3 × 0.2 = 0.06`. At least one is `0.3 + 0.2 − 0.06 = 0.44`, so 44%. Neither is `1 − 0.44 = 0.56`, which also equals `0.7 × 0.8`.

</details>

## Lab hook

**Lab 01, Sample spaces in a spreadsheet** ([`labs/lab01.md`](../labs/lab01.md)). You will build the 20 by 20 advantage grid and Fire Emblem's 100 by 100 two-number grid as spreadsheet tables, count events with formulas, and check the results against a 10,000-roll simulation. The lab ends with a short memo recommending one "roll twice" rule for a hypothetical game.

## Sources

- Wizards of the Coast, *System Reference Document 5.1* (2016), "Using Ability Scores", Passive Checks: "If the character has advantage on the check, add 5." Same rule in the *Dungeons & Dragons Basic Rules* (2014), "Using Ability Scores", sections on advantage and disadvantage and on passive checks (+5 for advantage, −5 for disadvantage). D&D Beyond, dndbeyond.com/sources/dnd/basic-rules-2014/using-ability-scores. Paraphrased.
- bg3.wiki, "Advantage" (Baldur's Gate 3, release version 2023 and later patches). Roll two d20 and use the higher; applies to attack rolls, ability checks and saving throws; multiple sources do not stack; average kept roll 13.825.
- Fire Emblem Wiki, "True hit". Two-random-number averaging used from The Binding Blade through Awakening and in Three Houses; true hit table (displayed 50 → 50.50%, 70 → 82.30%, 80 → 92.20%, 90 → 98.10%); Fates, Shadows of Valentia and Engage use a hybrid system. Values recomputed for this lecture by counting the 10,000 pairs.
- Schreiber, I. (2010). *Game Balance Concepts*, Level 4, "Probability and Randomness". gamebalanceconcepts.wordpress.com.
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press. Chapter on probability and dice.
- All other numbers in this lecture are computed from the stated models and can be reproduced by counting.

## Interactive spec: examples/w01-advantage-grid.html

**The one insight.** Advantage equals +5 at exactly one real target (T = 11). The two also tie at T = 1, where every roll succeeds. Everywhere else advantage is weaker, because its failure region is a square that grows with `(T − 1)²`, while +5 shifts a straight line.

**Layout.** Two linked panels side by side on desktop, stacked on mobile (grid first).

**Panel A, the sample space.** A 20 × 20 grid of square cells. X-axis is die `a` (1 to 20, left to right). Y-axis is die `b` (1 to 20, bottom to top). Each cell is coloured by whether it is in the current event.
- Mode "Advantage": success if `max(a, b) >= T`. The failing region is the bottom-left `(T − 1) × (T − 1)` square.
- Mode "Disadvantage": success if `min(a, b) >= T`. The success region is the top-right `(21 − T) × (21 − T)` square.
- Mode "Plain": success if `a >= T` (column band; b is ignored). Show a small note "the second die does not matter".
- Under the grid, print the count: "Successful pairs: N of 400 = X%". Hovering or focusing a cell shows `(a, b) → kept value`.

**Panel B, success chance vs target.** X-axis T from 1 to 20 (integers). Y-axis success chance 0% to 100%. Four series drawn as step-points joined by lines:
- plain `(21 − T)/20`
- advantage `1 − ((T − 1)/20)²`
- +5 `clamp((26 − T)/20, 0, 1)`
- disadvantage `((21 − T)/20)²`
A vertical cursor at the current T with the four values printed next to it. Mark T = 11 with a small label "advantage = +5 only here". Shade the gap between the +5 line and the advantage curve.

**Controls.**
- Slider T, 1 to 20, default 18 (so the first screen shows the large gap: 27.75% vs 40%). Keyboard arrows step by 1.
- Mode toggle: Advantage / Disadvantage / Plain (radio group, default Advantage).
- Button "Roll 100": animates (or, under reduced motion, instantly marks) 100 random pairs as dots on the grid and shows the observed success fraction next to the computed one.
- Optional stretch: "Fire Emblem mode" switch that replaces the grid with a 100 × 100 grid (0 to 99 per axis, drawn as a canvas), slider H from 0 to 100, event `a + b < 2H`, and a readout of the true hit. Test values: H = 50 → 50.50%, H = 70 → 82.30%, H = 80 → 92.20%, H = 90 → 98.10%.

**Test values (must match exactly).**

| T | Plain | Advantage | +5 | Disadvantage | Pairs |
|---|---|---|---|---|---|
| 2 | 95.00% | 99.75% | 100% | 90.25% | 399 |
| 11 | 50.00% | 75.00% | 75.00% | 25.00% | 300 |
| 16 | 25.00% | 43.75% | 50.00% | 6.25% | 175 |
| 18 | 15.00% | 27.75% | 40.00% | 2.25% | 111 |
| 20 | 5.00% | 9.75% | 30.00% | 0.25% | 39 |

Also show "Average kept die with advantage: 13.825 (plain: 10.5)" as a static fact line.

**Accessibility.** All controls keyboard reachable; the grid colours must differ in lightness, not only hue; respect `prefers-reduced-motion` for the roll animation.
