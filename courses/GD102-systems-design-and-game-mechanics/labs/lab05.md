# GD102 · Lab 05: Three spending machines

**Assigned:** week 5. **Due:** start of week 6. **Weight:** part of the Machinations models component (30% of the course).
**Lecture:** [Week 5, Machinations diagrams I](../lectures/w05-machinations-diagrams-i.md). **Interactive:** [w05-capped-pool.html](../examples/w05-capped-pool.html), for checking the capped pool.

## Objective

Build three versions of the same spending resource in Machinations: a capped pool, a pool that resets each turn, and a pool that carries over without limit. Run each against two spending policies and measure waste and cards played. By the end you should be able to predict, before running anything, which machine punishes which habit.

## Starter materials

**Tool.** A free machinations.io account. If the tool is unavailable, the same models can be run in a spreadsheet with one row per step; say which you used.

**Common settings for all three machines.** Treat one Machinations step as one turn of a fictional card game.

| Name | Value | Meaning |
|---|---|---|
| income | 3 per step | automatic source into the Energy pool |
| start | 3 | Energy at step 0 |
| cheap card | cost 2 | |
| big card | cost 7 | |
| run length | 30 steps | |

**Machine A, capped pool.** Energy has capacity 8. Energy carries over between steps up to the cap.

**Machine B, turn reset.** Energy has no capacity, but an automatic drain empties the pool at the end of every step, after the player has acted. Build this as a drain with a pull rate large enough to take everything (for example 99), fired after the play.

**Machine C, carry-over.** Energy has no capacity and no end-of-step drain.

**Policies.** Each step, after income arrives:

- **Spend-cheap.** Play as many cheap cards as the pool allows.
- **Save-for-big.** If the pool holds 7 or more, play one big card. Otherwise play nothing.

Every play must pull all-or-nothing. Build each play as an interactive drain and click it, or use an automatic drain with an activator if you have read ahead to week 6.

## Steps

1. **Predict.** Before building anything, fill in a 3 × 2 table (machine × policy) with your prediction of waste over 30 steps and cards played. Hand it in unchanged.
2. **Build A.** Build Machine A. Test it with no plays for 3 steps and confirm with the conservation check `start + income = pool + spent + wasted` that 4 is wasted by step 3 (3 + 9 = 8 + 0 + 4).
3. **Run A.** Run both policies for 30 steps. Record cards played, energy spent, energy wasted and the final pool. Apply the conservation check to every run.
4. **Build and run B.** Count energy removed by the end-of-step drain as wasted. Record the same four numbers for both policies.
5. **Build and run C.** Record the same four numbers for both policies.
6. **Explain.** For each of the six runs, write one sentence that explains the waste number using the idea "waste happens when resources arrive at a full pool or are drained unspent".
7. **Change one rule.** Pick one machine and one change of one number or one node (a different cap, a smaller end-of-step drain that only removes half, or an income that grows by 1 per step up to 10). Predict the effect, then run it and compare.

## Deliverable

A one-page report with: your unchanged predictions, a results table of the six runs (four numbers each plus the conservation check), a screenshot or export of each machine, the six explanations from step 6, and the result of step 7. Include a short paragraph that names which machine you would choose for a fast, aggressive game and which for a slow, planning-heavy game, with the numbers that back the choice.

## Rubric

| Criterion | Points | Full marks | Partial | Minimal |
|---|---|---|---|---|
| Predictions submitted | 5 | Complete table handed in before results | Partial table | Missing |
| Correct machines | 25 | All three machines built with correct activation modes, capacity, drains and all-or-nothing pulls | One machine wrong | Two or more wrong |
| Results and conservation | 25 | Six runs recorded, every conservation check holds | One or two checks fail or missing | Results without checks |
| Explanations | 15 | Each explanation names the full pool or the drain as the cause, with a number | Some explanations vague | Missing |
| Rule change | 15 | Prediction, run and comparison all present | Run without prediction | Missing |
| Design recommendation | 15 | Machine choices justified with numbers from the table | Choices stated without numbers | Missing |
