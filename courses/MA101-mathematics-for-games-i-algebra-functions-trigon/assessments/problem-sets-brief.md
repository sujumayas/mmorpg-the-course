# MA101 problem sets brief

**Weight:** 40% of the course grade, split evenly across six problem sets (about 6.7% each).
**Work:** written parts individually, labs as each lab brief says (some are pairs).
**Related:** [exam bank](exam-bank.md), [curve-design project](curve-design-project-brief.md), [midterm and final](midterm-and-final-brief.md).

## What a problem set is

Each problem set covers two or three weeks and has two parts of equal weight.

- **Written part (50% of the set).** Six to eight problems, handed out in the first week the set covers. At least 60% of the marks come from running a lecture model on numbers you have not seen. Every set also has one explain question and one critique or design question. None of the problems are copied from the exam bank, so the bank stays useful for revision.
- **Lab part (50% of the set).** The labs assigned in the set's weeks. Each lab keeps its own due date and is graded with the rubric printed in its brief. The lab part of the set is the average of those lab grades.

The written part practises the models in small pieces. The labs practise building them in a spreadsheet or script. The exams test the first skill without a computer, which is why the written part asks for working by hand.

## Schedule

| Set | Weeks | Labs in the set | Written part released | Written part due |
|---|---|---|---|---|
| PS1 | 1 and 2 | [Lab 01](../labs/lab01.md), [Lab 02](../labs/lab02.md) | week 1 | start of week 3 |
| PS2 | 3 and 4 | [Lab 03](../labs/lab03.md), [Lab 04](../labs/lab04.md) | week 3 | start of week 5 |
| PS3 | 5 and 6 | [Lab 05](../labs/lab05.md), [Lab 06](../labs/lab06.md) | week 5 | start of week 7 |
| PS4 | 7 and 8 | [Lab 07](../labs/lab07.md), [Lab 08](../labs/lab08.md) | week 7 | start of week 9 |
| PS5 | 9, 10 and 11 | [Lab 09](../labs/lab09.md), [Lab 10](../labs/lab10.md), [Lab 11](../labs/lab11.md) | week 9 | start of week 12 |
| PS6 | 12, 13 and 14 | [Lab 12](../labs/lab12.md), [Lab 13](../labs/lab13.md), [Lab 14](../labs/lab14.md) | week 12 | start of week 15 |

PS3 is returned with worked solutions before the week 8 midterm. PS6 is returned before the final.

## Rules for the written part

- **Show the model, then the numbers.** Write the formula you are using with every symbol named, substitute, and give the result with units. An answer without working earns at most a quarter of the problem's marks.
- **Check one value.** Every multi-step problem ends with a check: the other endpoint of a fitted line, a neighbouring level in a rounding problem, a brute-force count for a logarithm answer. The lectures model this habit and the rubric rewards it.
- **Round at the end.** Keep full precision in intermediate steps. Report to three significant figures unless the model itself rounds (a `floor` in a stat formula, a whole number of purchases).
- **Tools.** A calculator, spreadsheet or Python is fine for arithmetic. The written reasoning must be yours.
- **Collaboration.** You may discuss problems with classmates. Write your answers alone and name the people you discussed with at the top of the submission.
- **Late work.** Each student has one 48-hour extension for the semester, used by telling the instructor before the deadline. Otherwise the written part loses 10% per day late and is not accepted after three days, because worked solutions go out then.
- **Game facts.** Any fact about a shipped game that a problem needs is given in the problem, taken from a lecture that cites it. You never need to look up a game's constants.

## Sample problems

Two or three samples per set, at the level of the real sets. Answers are included so you can calibrate.

### PS1 (weeks 1 and 2)

1. A species has base HP 80. Your copy has IV 31 and 252 HP EVs. Using the week 1 HP formula `HP = floor((2B + I + floor(E/4)) · L / 100) + L + 10`, compute its HP at level 50 and level 100.
2. A potion heals 50 at character level 1 and 410 at level 25. Write the healing line in point-slope form and compute the healing at level 40.

<details>
<summary>Answers</summary>

- Problem 1. `raw = 160 + 31 + 63 = 254`. Level 50: `127 + 50 + 10 = 187`. Level 100: `254 + 100 + 10 = 364`.
- Problem 2. Slope `(410 − 50) / 24 = 15`. `heal(L) = 50 + 15·(L − 1)`. `heal(40) = 50 + 15 × 39 = 635`.

</details>

### PS2 (weeks 3 and 4)

1. Design a jump that rises 5 tiles in 0.45 s. Give `g` and `v₀`.
2. An upgrade's price doubles every 6 purchases, `30 · 2^(M/6)`. What is the growth rate per purchase? What does the 25th upgrade cost?

<details>
<summary>Answers</summary>

- Problem 1. `g = 2 × 5 / 0.45² = 49.4` tiles/s². `v₀ = 2 × 5 / 0.45 = 22.2` tiles/s.
- Problem 2. `2^(1/6) − 1 = 12.2%` per purchase. The 25th has `M = 24`, so `30 × 2^4 = 480`.

</details>

### PS3 (weeks 5 and 6)

1. A building has base cost 80 and each copy costs 12% more. How many can a player buy from zero with 500,000?
2. A game uses `A / (A + 150)`. How much armor gives 40% mitigation, and what is the EHP multiplier there?

<details>
<summary>Answers</summary>

- Problem 1. `floor( ln(1 + 0.12 × 500,000 / 80) / ln 1.12 ) = floor( ln 751 / 0.1133 ) = floor(58.4) = 58`.
- Problem 2. `A = 150 × 0.4 / 0.6 = 100`. EHP multiplier `1 + 100/150 = 1.67`.

</details>

### PS4 (weeks 7 and 8)

1. A shield stat is `clamp(2·str − 20, 0, 150)`. Find both breakpoints and the per-point gain on each piece.
2. A heartbeat sound fades in as health falls, `volume = clampedRemap(hpFraction, 0.4, 0.1, 0, 1)`. What is the volume at 25% health, and at 60%?

<details>
<summary>Answers</summary>

- Problem 1. The floor ends where `2·str − 20 = 0`, at `str = 10`. The cap starts where `2·str − 20 = 150`, at `str = 85`. Gains are 0, 2 and 0 per point.
- Problem 2. `inverseLerp(0.4, 0.1, 0.25) = 0.5`, so volume 0.5. At 60% the fraction is −0.67, clamped to 0, so silent.

</details>

### PS5 (weeks 9, 10 and 11)

1. A dash covers 150 px in 0.25 s with `CubeOut`. How far has the character moved after 0.05 s?
2. Seven orbs circle at radius 90 px. What is the chord gap between neighbours?
3. A unit faces −170° and its target is at 100°. What is the shortest signed turn?

<details>
<summary>Answers</summary>

- Problem 1. `t = 0.2`, `CubeOut(0.2) = 1 − 0.8³ = 0.488`, so 73.2 px.
- Problem 2. `2 × 90 × sin(π/7) = 78.1` px.
- Problem 3. Raw `100 − (−170) = 270`. Wrapped `270 − 360 = −90`. Turn 90° in the negative direction.

</details>

### PS6 (weeks 12, 13 and 14)

1. Give the velocity for direction `(5, −12)` at a speed of 26 units/s.
2. A guard faces `(1, 0)` with half-angle 25°. The player's offset is `(12, 5)`, inside range. Is the player seen?
3. A pickup has radius 2.5. The player's offset from it is `(1.5, 2.1)`. Is it collected? Use squared distance only.

<details>
<summary>Answers</summary>

- Problem 1. Length 13, direction `(5/13, −12/13)`, velocity `(10, −24)`.
- Problem 2. `d̂ = (12/13, 5/13)`, `f̂ · d̂ = 0.923`. `cos 25° = 0.906`. Seen.
- Problem 3. `S = 2.25 + 4.41 = 6.66`. `r² = 6.25`. `6.66 > 6.25`, so not collected.

</details>

## Rubric for the written part

The written part of every set is graded out of 4 per criterion, weighted as below. The lab part uses each lab's own rubric.

| Criterion | Weight | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|---|
| Model choice and set-up | 30% | Correct model for every problem, every symbol named, parameters and variables identified | Correct models, one set-up unclear | One or two problems use the wrong model | Models missing or mostly wrong |
| Computation and checks | 30% | All results correct; every multi-step problem ends with a check that agrees | One arithmetic slip, checks present | Several slips or checks missing | Mostly wrong or no working |
| Units, rounding and domain | 10% | Units on every answer, rounding only where the model rounds, domain edges stated where they matter | One unit or rounding lapse | Units often missing, rounding too early | Ignored |
| Explanation and design judgment | 20% | Explain and critique answers argue from computed numbers and name a concrete consequence or fix | Argument sound, numbers thin | Opinion with little evidence | Missing |
| Presentation | 10% | A reader can follow every problem without asking; tables where tables help | Readable with small gaps | Hard to follow in places | Illegible or disorganised |

A score of 4 in every row is 100%. The set grade is `0.5 × written + 0.5 × average of the set's labs`.
