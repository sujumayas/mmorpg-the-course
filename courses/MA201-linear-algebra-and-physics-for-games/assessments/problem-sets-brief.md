# MA201 problem sets brief

**Weight:** 40% of the course grade, split evenly across five problem sets (8% each).
**Work:** the written part individually. Labs in pairs or alone, as each lab says.
**Related:** [exam bank](exam-bank.md), [physics sandbox](sandbox-brief.md), [final exam](final-exam-brief.md).

## What a problem set is

Each problem set covers two or three weeks and has two parts.

- **Written part (40% of the set).** Five to seven problems, handed out in the first week the set covers. At least 60% of the marks come from running a lecture model on numbers you have not seen. Every set also has one explain question and one design or critique question. None of the problems are copied from the exam bank, so the bank stays useful for revision.
- **Lab part (60% of the set).** The labs assigned in the set's weeks. Each lab keeps its own due date and is marked out of 100 with the rubric printed in the lab. The lab part of the set is the average of those lab marks.

The labs carry more weight because they are where you build the models in code, measure them and write a recommendation from your own numbers. The written part practises the same models in small pieces by hand, which is the skill the final exam tests without a computer.

Several labs also build parts of the [physics sandbox](sandbox-brief.md). Your lab 07 integrators, lab 08 `Body`, lab 09 contacts, lab 10 resolver, lab 12 raycasts, lab 13 aim functions and lab 14 precision budget all go into it. A lab you do badly still has to work by week 15.

## Schedule

| Set | Weeks | Labs in the set | Written part released | Written part due |
|---|---|---|---|---|
| PS1 | 1 to 3 | [Lab 01](../labs/lab01.md), [Lab 02](../labs/lab02.md), [Lab 03](../labs/lab03.md) | week 1 | start of week 4 |
| PS2 | 4 and 5 | [Lab 04](../labs/lab04.md), [Lab 05](../labs/lab05.md) | week 4 | start of week 6 |
| PS3 | 6 to 8 | [Lab 06](../labs/lab06.md), [Lab 07](../labs/lab07.md), [Lab 08](../labs/lab08.md) | week 6 | start of week 9 |
| PS4 | 9 to 11 | [Lab 09](../labs/lab09.md), [Lab 10](../labs/lab10.md), [Lab 11](../labs/lab11.md) | week 9 | start of week 12 |
| PS5 | 12 to 14 | [Lab 12](../labs/lab12.md), [Lab 13](../labs/lab13.md), [Lab 14](../labs/lab14.md) | week 12 | start of week 15 |

Each written part is returned with worked solutions one week after it is due. PS5 is returned before the final exam.

## Rules for the written part

- **Show the model, then the numbers.** Write the formula you are using with every symbol named, substitute, and give the result with units. An answer without working earns at most a quarter of the problem's marks.
- **Check one value.** Every multi-step problem ends with a check: two dot products after a cross product, a round trip after an inverse, momentum before and after an impulse, the corners of the tile you picked. The lectures model this habit and the rubric rewards it.
- **Round at the end.** Keep full precision in intermediate steps. Report three or four significant figures, or the decimals the lecture's tables use. Where the model itself rounds (a `floor` in a tile picker, a whole number of ticks, a float32 gap), give the rounded value.
- **State the convention.** Say which way is up, which handedness, row or column vectors, and which FOV convention before you compute. Half the week 1 to 5 bugs are a convention nobody wrote down.
- **Tools.** A calculator, spreadsheet or Python is fine for arithmetic. If you use Python, paste the few lines you ran. The reasoning must be yours.
- **Collaboration.** You may discuss problems with classmates. Write your answers alone and name the people you discussed with at the top of the submission.
- **Late work.** Each student has one 48-hour extension for the written parts, used by telling the instructor before the deadline. Otherwise the written part loses 10% per day late and is not accepted after three days, because worked solutions go out then. Late labs follow the rule in each lab.
- **Game and engine facts.** Any fact about a shipped game or engine that a problem needs is given in the problem, taken from a lecture that cites it. You never need to look up a constant.

## Sample problems

Two or three samples per set, at the level of the real sets, with answers so you can calibrate. All numbers were recomputed from the lectures' models.

### PS1 (weeks 1 to 3)

1. Compute `(2, 0, 1) × (−1, 3, 2)` and check it with two dot products. What is the area of the triangle with those two edges?
2. An isometric map uses tiles 128 pixels wide and 64 tall with the week 2 layout. Which tile contains the click (100, 150)?
3. A parent has scale (3, 1). Its child square is rotated 30°. What is the child's corner angle in world space, and its determinant?

<details>
<summary>Answers</summary>

- Problem 1. `(0·2 − 1·3, 1·(−1) − 2·2, 2·3 − 0·(−1)) = (−3, −5, 6)`. Checks: `−6 + 0 + 6 = 0` and `3 − 15 + 12 = 0`. Length `√70 = 8.367`, area 4.18.
- Problem 2. `i = 100/128 + 150/64 = 3.125`, `j = 150/64 − 100/128 = 1.5625`. Tile (3, 1).
- Problem 3. Edges `(2.598, 0.5)` and `(−1.5, 0.866)`. Corner angle 139.11°. Determinant 3.

</details>

### PS2 (weeks 4 and 5)

1. A game uses vertical FOV 80°. What horizontal angle does a 32:9 monitor show?
2. An engine prints the quaternion `(0.7071, 0, 0, −0.7071)`. Name the rotation and say where it sends `(0, 1, 0)`.
3. With near 0.1 m and far 500 m, at what depth does `z_ndc` reach 0?

<details>
<summary>Answers</summary>

- Problem 1. `2·atan(32/9 · tan 40°) = 142.94°`.
- Problem 2. `θ = 2·acos(0.7071) = 90°` about `(0, 0, −1)`, the same as −90° about z. It sends (0, 1, 0) to (1, 0, 0).
- Problem 3. `2Fn / (F + n) = 100 / 500.1 = 0.19996`, about 0.2 m, twice the near distance.

</details>

### PS3 (weeks 6 to 8)

1. A cloth runs semi-implicit Euler at 144 Hz. What is the largest stable `k / m`?
2. Convert a drag factor of 0.96 per tick at 20 Hz to a coefficient in 1/s and a per-step factor at 144 Hz.
3. A player jumps at 450 px/s under 1,000 px/s² from an elevator rising at 120 px/s, with `DO_NOTHING`. What is the apex above the elevator floor and the air time until landing on it?

<details>
<summary>Answers</summary>

- Problem 1. `ω < 2 × 144 = 288` rad/s, so `k / m < 82,944`.
- Problem 2. `c = −ln(0.96) / 0.05 = 0.816` per second. `0.96^(20/144) = 0.99435`.
- Problem 3. Relative launch `450 − 120 = 330` px/s. Apex `330² / 2000 = 54.5` px. Air time `2 × 330 / 1000 = 0.66` s.

</details>

### PS4 (weeks 9 to 11)

1. A 2 kg ball hits a wall head on at 5 m/s with `e = 0.4`. Give the impulse and the rebound velocity.
2. Entities query `r = 2` m at a density of 1 per m². Give `s*` and `W(s*)`.

<details>
<summary>Answers</summary>

- Problem 1. The wall has inverse mass 0, so `j = 1.4 × 5 / 0.5 = 14` N·s. Rebound `5 − 14/2 = −2` m/s, which is `0.4 × 5` the other way.
- Problem 2. `s* = (4 / 1)^(1/3) = 1.587` m. `W = (4 + 1.587)² × (1/1.587² + 1) = 43.6`.

</details>

### PS5 (weeks 12 to 14)

1. A ray starts at (0, 10, 0) with direction (0.6, −0.8, 0). Where does it hit the ground plane y = 0?
2. A walker at 3 m/s on a 20 Hz tick is 100 km from the origin in float32. What speed does it actually move at?
3. A target 25 m away runs straight across at 5 m/s. A bolt flies at 15 m/s. Give the flight time and lead angle.

<details>
<summary>Answers</summary>

- Problem 1. `t = (0 − 10) / (−0.8) = 12.5`. Hit at (7.5, 0, 0).
- Problem 2. Step 0.15 m, gap `2⁻⁷ = 0.0078` m, ratio 19.2, rounds to 19 gaps, 0.1484 m per tick, 2.97 m/s (1% slow).
- Problem 3. `t = 25 / √(225 − 25) = 1.768` s. `sin(lead) = 5 / 15`, lead 19.47°.

</details>

## Rubric for the written part

Each criterion is scored from 0 to 4 and earns `points × score ÷ 4`. The lab part of the set uses each lab's own rubric.

| Criterion | Points | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|---|
| Model choice and set-up | 25 | Right model for every problem, every symbol named, convention stated (up axis, handedness, FOV convention, normal direction) | Right models, one set-up or convention unclear | One or two problems use the wrong model or convention | Models missing or mostly wrong |
| Computation | 25 | All results correct to the stated precision | One arithmetic slip | Several slips | Mostly wrong or no working |
| Checks | 15 | Every multi-step problem ends with a check that agrees (dot products, round trip, momentum, corners) | Checks on most problems | Checks on one or two problems | No checks |
| Units, rounding and edge cases | 10 | Units on every answer, rounding only where the model rounds, edge cases named where they matter (zero-length normal, no intercept, `c·h > 1`) | One lapse | Units often missing, rounding too early | Ignored |
| Explanation and design judgment | 15 | Explain, design and critique answers argue from computed numbers and name a concrete consequence or fix | Argument sound, numbers thin | Opinion with little evidence | Missing |
| Presentation | 10 | A reader can follow every problem without asking; tables where tables help; code pasted where used | Readable with small gaps | Hard to follow in places | Illegible or disorganised |
| **Total** | **100** | | | | |

The set mark is `0.4 × written + 0.6 × average of the set's labs`. The problem-set component of the course grade is the mean of the five set marks, times 0.40.

## Academic integrity

You may use the lecture code, the lab starters and any documentation. You may ask a classmate or an AI assistant to explain an error message or a concept, and you must say so in one line at the top of the submission. You may not submit working or code you cannot explain. In each lab session from week 2 on, the instructor asks a few students two short questions about their last written part, in the style of the exam bank with the student's own numbers. A student who cannot explain their own working has that problem re-marked after a ten-minute conversation.
