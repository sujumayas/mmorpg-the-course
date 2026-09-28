# MA102 · Final exam brief

**Weight:** 25% of the course grade.
**When:** week 15, in the scheduled exam slot.
**Length:** 2 hours, plus 10 minutes of reading time before you may write.
**Work:** individual, invigilated.

## What the exam tests

The exam tests whether you can apply the course's models to numbers you have not seen, explain what the results mean, and use them to make or critique a design decision. It does not test recall of lecture text or of the game facts used as examples. Any real-game number you need is given in the question.

Every week from 1 to 14 appears at least once. The questions are drawn from the [exam bank](exam-bank.md) items tagged **final**, with new numbers and sometimes a new game context. If you can do the bank's final-tagged questions without looking at the answers, you are ready.

## Format

| Section | Questions | Marks | Suggested time | What it asks |
|---|---|---|---|---|
| A. Compute | 10 short questions, answer all | 40 (4 each) | 50 minutes | Apply one model to new numbers. One question per week for ten different weeks |
| B. Explain and critique | Answer 3 of 4 | 30 (10 each) | 36 minutes | Explain a result or find the error in a claim, using numbers. Covers the weeks section A skipped |
| C. Design | 1 multi-part problem, answer all parts | 30 | 34 minutes | Design a small system to meet stated targets and defend it. Always combines at least three weeks |

Total 100 marks, scaled to 25 course points.

### Sample paper built from the bank

This is the paper you would sit if the exam used the bank's numbers unchanged. Use it as a timed mock.

- **Section A:** questions 1 (week 1), 5 (week 2), 9 (week 3), 13 (week 4), 18 (week 5), 22 (week 6), 27 (week 7), 32 (week 8), 37 (week 9), 44 (week 10).
- **Section B:** choose 3 of questions 49 (weeks 10 and 11), 53 (week 12), 59 (week 13), 64 (week 14).
- **Section C:** question 65 (weeks 3, 7, 9 and 10).

## What you may bring

- A non-programmable scientific calculator with `ln`, powers and square roots.
- One A4 sheet of your own notes, handwritten, both sides.
- Pens. Rough paper is provided.

No phones, laptops or printed notes.

## What the paper provides

The exam includes this formula sheet and table. You do not need to memorize them. You need to know when each applies.

**Probability.** `P(A or B) = P(A) + P(B) − P(A and B)`. Independent: `P(A and B) = P(A) P(B)`. `P(A | B) = P(A and B)/P(B)`. At least one in n: `1 − (1 − p)^n`.

**Expected value and spread.** `E[X] = Σ x P(x)`. `Var(X) = E[X²] − μ²`. CV `= σ/μ`. Crit hit: `μ = b(1 + c(m − 1))`, `σ² = b²(m − 1)² c(1 − c)`. n independent copies: mean `nμ`, SD `√n σ`.

**Distributions.** Binomial: `C(n, k) p^k (1 − p)^(n − k)`, mean `np`, SD `√(np(1 − p))`. Geometric: `P(X > n) = (1 − p)^n`, mean `1/p`, SD `√(1 − p)/p`, percentile `ceil(ln(1 − q)/ln(1 − p))`. NdF: mean `N(F + 1)/2`, variance `N(F² − 1)/12`.

**Tables and pity.** `P(i) = w_i/W`. Weight for chance q: `w = Rq/(1 − q)`. Hard pity at H: `E = (1 − (1 − p)^H)/p`. General: `E[N] = Σ` of survival probabilities.

**Estimation.** `SE = √(p̂(1 − p̂)/n)`, 95% margin `1.96 SE`. Wilson centre `(p̂ + z²/2n)/(1 + z²/n)`, half-width `z√(p̂(1 − p̂)/n + z²/4n²)/(1 + z²/n)`. Rule of three: `3/n`. Sample size: `n = z² p(1 − p)/m²`.

**A/B tests.** Pooled `SE = √(p̂(1 − p̂)(1/n_A + 1/n_B))`, `z = (p̂_B − p̂_A)/SE`. Per-group n for 80% power: `7.85 (p_A(1 − p_A) + p_B(1 − p_B))/d²`, or Lehr's `16 p(1 − p)/d²`.

**Normal table, Φ(z) = P(Z ≤ z).**

| z | 0.84 | 1.00 | 1.20 | 1.28 | 1.30 | 1.35 | 1.50 | 1.645 | 1.96 | 2.00 | 2.30 | 2.33 | 2.576 | 3.00 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Φ(z) | 0.7995 | 0.8413 | 0.8849 | 0.8997 | 0.9032 | 0.9115 | 0.9332 | 0.9500 | 0.9750 | 0.9772 | 0.9893 | 0.9901 | 0.9950 | 0.9987 |

## Marking scheme

### Section A (4 marks each)

| Marks | What earns them |
|---|---|
| 2 | Correct model chosen and set up with the question's numbers (for example, writing `1 − 0.996^250` for an at-least-one question) |
| 1 | Arithmetic carried through to a number |
| 1 | Correct final answer, rounded sensibly, with its meaning stated (a probability, a kill count, a DPS) |

Follow-through applies. If part (a) is wrong and part (b) uses it correctly, part (b) keeps its method and arithmetic marks. A right answer with no working earns 2 of 4.

### Sections B and C (point bands)

| Band | Section B (of 10) | Section C (of 30) | What the answer shows |
|---|---|---|---|
| Excellent | 9 to 10 | 26 to 30 | The right model, correct numbers, a clear statement of what the numbers mean for the design, and the trade-off or error named precisely |
| Good | 7 to 8 | 20 to 25 | Correct reasoning with a small numerical slip, or a correct result whose design meaning is only partly drawn out |
| Adequate | 5 to 6 | 14 to 19 | The main idea is right but a step is missing, or the answer argues from intuition where a number was needed |
| Weak | 2 to 4 | 6 to 13 | A relevant model is named but misapplied, or the answer restates the question |
| Missing | 0 to 1 | 0 to 5 | No relevant work |

In Section C, each part's mark allocation is printed on the paper. Rounding that breaks a stated target (for example, rounding a weight down so the 95% target slips by one kill) loses the mark for that check, as in bank question 65.

## Common ways students lose marks

- Adding probabilities of events that can overlap, or of repeated attempts (`n × p` instead of `1 − (1 − p)^n`).
- Using the mean wait as a deadline.
- Applying the binomial to a count without a fixed number of trials.
- Quoting a rate from a small sample without an interval.
- Reading a p-value as the probability the hypothesis is true.
- Stopping at the number. Sections B and C ask what the number means for the design.

## Administration

- Students with approved accommodations receive extra time as agreed with the disability office. Tell the instructor by week 12.
- A missed exam with documented illness is replaced by a sit in the next exam period, drawn from the same bank.
- Results are published with the component grades at the end of week 15. You can view your marked paper by appointment in the two weeks after.
