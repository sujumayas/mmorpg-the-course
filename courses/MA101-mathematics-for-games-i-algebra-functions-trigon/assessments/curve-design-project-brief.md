# MA101 curve-design project brief

**Weight:** 20% of the course grade.
**Work:** individual.
**Due:** week 15, with a 5-minute showcase in the final session.
**Related:** [problem sets](problem-sets-brief.md), [midterm and final](midterm-and-final-brief.md).

## The task

Pick one quantity in a small game of your own invention. Decide how it should feel to a player, choose a curve that produces that feel, and prove with numbers that it does. Then compare it with one other curve family and explain why you did not ship that one.

This is the course in one piece of work. The lectures each took a shipped formula and showed its shape, its numbers, a visual and its trade-offs. Now you build one from the other direction, starting from the feel.

## Choose a brief

Pick one of these, or propose your own at milestone 1.

| Brief | Quantity | Lectures it draws on |
|---|---|---|
| A | XP curve for a 40-level crafting skill, with a stated halfway level and hours per level | [weeks 3](../lectures/w03-polynomials-and-quadratic-curves.md), [4](../lectures/w04-exponentials-and-the-xp-curve.md), [5](../lectures/w05-logarithms-how-many-levels-until.md) |
| B | A damage-reduction or dodge stat that never reaches 100%, with an EHP story | [weeks 6](../lectures/w06-rational-functions-and-asymptotes.md), [7](../lectures/w07-piecewise-caps-and-floors.md) |
| C | A health or stamina stat with soft caps where you want builds to stop | [week 7](../lectures/w07-piecewise-caps-and-floors.md) |
| D | A charged attack: hold time to damage, projectile speed and feedback, with a remap and an ease | [weeks 8](../lectures/w08-interpolation-lerp-inverse-lerp-remap.md), [9](../lectures/w09-easing-curves-for-animation-feel.md) |
| E | An orbiting-shield upgrade path across five upgrade levels, keeping coverage and hit rate in check | [week 10](../lectures/w10-angles-radians-sin-cos.md) |
| F | A guard detection meter that fills from angle and distance | [weeks 13](../lectures/w13-dot-product-facing-and-vision-cones.md), [14](../lectures/w14-distances-ranges-and-squared-distance.md) |
| G | A range or falloff rule on a grid, choosing a distance metric on purpose | [week 14](../lectures/w14-distances-ranges-and-squared-distance.md) |

Your own proposal is fine if it has a quantity a player feels, at least one parameter to tune and a clear alternative family to compare against.

Use a fictional game. If you mention a shipped game for comparison, cite the fact with its version or era, as the lectures do.

## Deliverables

- **Design document** of 1,500 to 2,500 words, PDF, with these sections in order.
  - *Target feel.* One sentence in the player's terms, then two to four measurable targets. Examples: "halfway level is 34", "level 40 takes no more than 3 hours", "the guard notices a player at the cone's edge after at least 2 seconds".
  - *The model.* Stated once, every symbol named, with its domain.
  - *Numbers you can check.* A table of at least six rows that a reader can verify by hand, including both ends of the domain.
  - *Two views.* Two linked graphs where one shows what the player sees and the other shows the quantity that matters (total against per-point gain, mitigation against EHP, position against speed, and so on). One sentence on what the pair reveals.
  - *The alternative.* One other curve family tuned to the same targets, with its own table, and the reason you rejected it.
  - *Edge cases.* What happens at the smallest and largest inputs, at any asymptote, breakpoint or clamp, and where rounding, frame rate or overflow could bite.
  - *Player presentation.* What the UI shows and why.
  - *Check yourself.* Two questions a classmate could answer with your model, with answers.
- **Working file.** A spreadsheet, script or single-file HTML page. It must compute from formulas, and it must let a reader change your main parameter and see both views update.
- **Test sheet.** At least eight input and expected-output pairs, including edge cases, that your working file passes.
- **Showcase.** A 5-minute talk in week 15, followed by 3 minutes of questions. Show the two views, move the parameter live, and state the one design decision you would defend hardest.

## Milestones

| Milestone | When | What you hand in | How it counts |
|---|---|---|---|
| M1 Proposal | start of week 10 | One page. Chosen brief, target-feel sentence, measurable targets, the curve family you expect to use and the alternative | Feedback within a week. Part of the "Process" row |
| M2 Draft | start of week 13 | The model, the numbers table and one of the two views. Peer review in the week 13 lab session: you review two classmates' drafts with a short checklist | Feedback from the instructor and two peers. Part of the "Process" row |
| M3 Final | week 15 | Document, working file, test sheet and showcase | Graded with the rubric below |

M1 lands after the midterm so you have seen all the curve families from weeks 1 to 9. The trigonometry and vector briefs (E, F, G) can be chosen at M1 even though weeks 10 to 14 are still ahead. The proposal only needs the target feel and the family.

## Rubric

Graded out of 100 points.

| Criterion | Points | Excellent | Good | Partial | Missing |
|---|---|---|---|---|---|
| Target feel and measurable targets | 10 | 9-10. Feel stated in player terms; targets are numbers the model can be tested against | 7-8. Targets present, one is vague | 4-6. Feel stated, targets not measurable | 0-3. Missing |
| Model correctness | 20 | 18-20. Model correct, symbols and domain stated, targets met exactly or within stated tolerance | 14-17. Correct model, one target missed or domain unstated | 8-13. Model has an error that changes a result | 0-7. Wrong family or broken model |
| Numbers and tests | 15 | 14-15. Table checkable by hand, test sheet has 8+ cases including edges, all pass | 11-13. Tests complete, one edge case missing | 6-10. Few tests or some fail | 0-5. Missing |
| Two views and working file | 15 | 14-15. Views are linked, reveal something the single view hides, and the file updates both from one parameter | 11-13. Both views present, link or insight weak | 6-10. One view, or file uses pasted values | 0-5. Missing |
| Alternative and trade-offs | 15 | 14-15. Alternative tuned to the same targets, compared with numbers, rejection argued from player experience | 11-13. Comparison with numbers, argument thin | 6-10. Alternative named, not tuned or not computed | 0-5. Missing |
| Edge cases | 10 | 9-10. Domain ends, asymptotes or breakpoints, and one implementation risk (rounding, frame rate, overflow) all handled | 7-8. Most handled | 4-6. Mentioned without numbers | 0-3. Missing |
| Communication and showcase | 10 | 9-10. Document and talk are clear, on time, and the live demo shows the key insight | 7-8. Clear, small gaps | 4-6. Hard to follow in places | 0-3. No showcase |
| Process (M1 and M2) | 5 | 5. Both milestones on time and complete, feedback visibly used | 3-4. One milestone late or thin | 1-2. One missing | 0. Both missing |

## Practical notes

- The document word count excludes tables, formulas and the check-yourself answers.
- The one-time 48-hour extension from the problem sets does not apply to M3. The showcase happens in the final session.
- If you work on brief F or G, lab 13 and lab 14, with their starter files in `labs/starter/`, already contain code you may reuse. Say which parts are reused.
