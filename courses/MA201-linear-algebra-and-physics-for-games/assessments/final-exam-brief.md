# MA201 final exam brief

**Weight:** 30% of the course grade.
**When:** week 15, in the exam period. The physics sandbox showcase is in the week 15 class session, so the two never fall on the same day.
**Question source:** the [exam bank](exam-bank.md), with numbers changed.
**Related:** [problem sets](problem-sets-brief.md), [physics sandbox](sandbox-brief.md).

## Why a written exam in a course full of code

The problem sets and the sandbox show that you can build the models with a computer, tests and time. The exam checks that you can use them without one: read a matrix by its columns, see that a dot product is negative before slerping, find the root of the intercept quadratic, and know that a float32 gap at 200 km is 1.6 cm. Those are the moments in a code review or a bug triage when nobody has a script ready. The questions are mostly computation, and the working earns most of the marks.

## Format

| | Final exam |
|---|---|
| Length | 150 minutes |
| Scope | weeks 1 to 14 |
| Part A | 8 short compute questions, 4 marks each (32) |
| Part B | 4 multi-part questions, 12 marks each (48). At least one is a code question and at least one is cross-week |
| Part C | 1 explain, design or critique question (20) |
| Total | 100 marks |
| Allowed | a non-programmable scientific calculator; two A4 sheets of your own notes, both sides, handwritten |
| Not allowed | phones, laptops, graphing or programmable calculators, printed notes |

Every fact about a shipped game or engine that a question needs is printed in the question, as it is in the bank: Unreal's `WalkableFloorZ` of 0.71, Box2D's max combine rule, Minecraft's per-tick drag and gravity, and so on. You never need to remember an engine's constants. You do need to remember the models: the cross product, the column reading of a matrix, the composition rule `B_world = Bp Bc`, the perspective divide and `θ_h = 2·atan(a·tan(θ_v/2))`, the half angle and the sign check, the three integrators and `ω·dt < 2`, `g·d/(1 − d)` and `c = −ln(d)/Δt`, the SAT radius, the impulse formula, `s* = (2r/ρ)^(1/3)`, the slab and sphere tests, the intercept quadratic, and `gap32(x)`.

## How questions are drawn from the bank

The bank is public from week 1, and studying it is the intended way to prepare.

- **Coverage.** Every week from 1 to 14 is tested at least once, counting cross-week questions for each week they list. Weeks 1 to 5 (transforms) carry 30 to 40% of the marks, weeks 6 to 10 (motion and collision) 35 to 45%, and weeks 11 to 14 (queries and precision) 20 to 30%.
- **New numbers.** Every compute and code question is used with new numbers or a changed snippet. The model, the steps and the structure stay the same. The instructor recomputes each new answer in Python with the lecture's model and keeps the script with the exam key.
- **Code questions.** Part B's code question shows a snippet of at most 25 lines in the style of the bank's code questions. You predict its output, find its bug, or write a short function by hand. Syntax slips that do not change the logic lose no marks.
- **Open questions.** Explain, design and critique questions may be used as written or with a new scenario that needs the same model.
- **Type mix.** At least 70% of the marks come from compute and code questions. Part C is always an explain, design or critique question.
- **Two versions.** The exam is set in two versions with different numbers. The second is used for make-up sittings.

## Marking compute and code questions

- **Method and answer.** A compute question's marks are split 40% for setting up the right model with the right values and convention, 40% for carrying it out, and 20% for the final answer with units and a check.
- **Follow-through.** An error is penalised once. Later steps that correctly use a wrong earlier value keep their method marks.
- **Tolerance.** Answers within one unit in the third significant figure are accepted. Where the model itself rounds (a `floor` in a tile picker, whole ticks, whole bounces, a float32 gap), the rounded value is required.
- **No answer is an answer.** "No intercept", "no inverse", "no normal" and "unstable" are full answers when the working shows why (a negative discriminant, a zero determinant, a zero-length cross product, `ω·dt > 2`).
- **Code.** A predicted output earns full marks only when it matches exactly, including the order of lines. Partial marks go to a correct trace of the logic with an arithmetic slip.

## Rubric for open questions

Part C and the explain, design or critique parts of Part B are marked with this rubric. The points below are for the 20-mark Part C. For a smaller part in Part B, the marker scales each row in proportion.

| Criterion | Points | Full | Partial | Minimal | None |
|---|---|---|---|---|---|
| Model | 5 | 5. Names the right model from the lectures and states it with every symbol | 3. Right model, stated with a small error | 1. Related model, or right model misapplied | 0 |
| Numbers as evidence | 7 | 7. At least two relevant numbers computed correctly and used in the argument | 4. One correct number, or two with a slip | 2. Numbers present but not relevant or mostly wrong | 0 |
| Reasoning | 4 | 4. Connects the numbers to what the player sees, feels or does, or to what breaks in the engine | 3. Connection made but loose | 1. Restates numbers without interpretation | 0 |
| Recommendation and trade-off | 4 | 4. A concrete change or choice, with its cost stated | 2. Concrete change, cost missing | 1. Vague direction ("make it more stable") | 0 |
| **Total** | **20** | | | | |

A design or critique answer that reaches a different conclusion from the bank's model answer earns full marks when it meets every row. The bank answers show one good argument, not the only one.

## Mark allocation

| Part | Questions | Marks each | Marks |
|---|---|---|---|
| A | 8 short compute | 4 | 32 |
| B | 4 multi-part (at least one code, at least one cross-week) | 12 | 48 |
| C | 1 explain, design or critique | 20 | 20 |
| **Total** | | | **100** |

## A sample paper

The final is built like this example, which uses bank questions as written. On the real paper the numbers change.

- **Part A.** Questions 1 (cross product), 5 (tile picking), 14 (FOV conversion), 18 (quaternion read-back), 32 (terminal velocity), 49 (cell size), 55 (slab test), 66 (float32 gaps).
- **Part B.** Question 19 (slerp the long way, week 5), question 30 (integrator code, week 7), question 43 with 44 (impulses and friction, week 10), and question 75 (SAT normal into the resolver, weeks 9 and 10).
- **Part C.** Question 71 (critique of a rounded lockstep checksum, week 14).

That paper covers weeks 1, 2, 4, 5, 7, 8, 9, 10, 11, 12 and 14 directly. A real paper must also cover weeks 3, 6 and 13, so one Part A slot would move to question 9, 23 or 58.

## Missed exams and adjustments

- A student who misses the exam for a documented reason sits the second version within two weeks.
- Adjustments such as extra time follow the university's disability and accessibility office. Tell the instructor at least two weeks before the exam.
- Graded scripts and a worked key are returned within two weeks. The key shows the full working for the numbers actually used.
