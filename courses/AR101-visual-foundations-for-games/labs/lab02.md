# AR101 · Lab 02: The shape cast

**Week:** 2, shape language ([lecture](../lectures/w02-shape-language-circles-squares-triangles.md)).
**Time:** 2 hours in lab, plus up to 4 hours at home.
**Weight:** one of the weekly studies (50% of the course grade in total).

## Objective

Design a small cast for an invented game in which every character and prop tells the player what it is and how to treat it through its shapes alone. Then test whether strangers read it the way you intended, and measure the shapes to explain the results.

This is a studio exercise. The only code is a finished helper that does the arithmetic.

## Brief

Your game is a cozy dungeon crawler for players aged 10 and up. You need six designs:

| Slot | Message the player must get in one second |
|---|---|
| Character A, the helper | Friendly, safe to approach |
| Character B, the guardian | Solid, hard to move, on your side |
| Character C, the threat | Dangerous, keep away |
| Prop D, the pickup | Safe to touch, good for you |
| Prop E, the obstacle | Blocks the way, harmless to touch |
| Prop F, the hazard | Hurts on contact, and shows which side is dangerous |

Rules:

- Each design has one primary shape family (circle, square or triangle) chosen for its message, following lecture section 3 (big, medium, small shapes).
- Characters A, B and C share the same face (the same simple eyes and mouth) and the same height. Only their shapes may differ.
- No color in the first pass. Black ink or flat gray only.
- Original designs only. No game characters, no traced art.

## Starter materials

All in [`lab02-starter/`](lab02-starter/).

- [`shape_measure.py`](lab02-starter/shape_measure.py), a finished helper. Give it a CSV of outline points and it prints circularity `C`, the sharpest corner θ and the lecture's reading for each shape. Run `python3 shape_measure.py shapes.csv` to see it on the example file.
- [`shapes.csv`](lab02-starter/shapes.csv), an example with a triangle, a square, a 3 : 1 bar, an octagon, a five-point star and a circle. The helper should print `C` 0.605, 0.785, 0.589, 0.948, 0.419 and 0.999 for them.
- The [interactive](../examples/w02-shape-reader.html), whose polygon mode accepts the same points.

## Steps

1. **Thumbnails.** For each of the six slots, draw at least four thumbnails (24 or more in total), about 4 cm tall. Vary the primary shape, the proportions and the direction of points.
2. **Select.** Pick one thumbnail per slot. Write one sentence per pick naming its primary, secondary and tertiary shapes.
3. **Clean drawings.** Redraw the six picks at about 10 cm tall, flat fill, on one sheet.
4. **Measure.** On grid paper or in a drawing program, trace the outer outline of each primary shape with 8 to 20 points. Put the points in a CSV (`name,x,y`) and run the helper. Record `C`, θ and the reading for all six.
5. **Blind-read test.** Show the six clean drawings, one at a time for about two seconds each, to at least five people who have not seen your brief. For each design, ask "Would you walk up to this, walk around it, or run from it?" and, for props, "Would you touch it?" Record every answer.
6. **Compare.** Score each design: how many of the five readers gave the answer you intended. Put the scores next to the measured readings.
7. **Revise.** Redesign the two lowest-scoring designs. Measure them again and run the blind-read test again with at least three new people.

## Deliverable

One PDF or image set containing the 24+ thumbnails, the six clean drawings (before and after revision for the two you revised), the measurement table, the blind-read results table, and a note of at most 400 words. The note must answer: where did the measured reading and the human reading disagree, and why? Include your CSV of outline points.

The deliverable is checkable. A grader should be able to rerun your CSV through the helper and get your table, and count your readers' answers.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Exploration | 24+ thumbnails with real variety in family, proportion and direction | 24 thumbnails, little variety | Fewer than 24 | 15% |
| Shape clarity | Each final design has one clear primary family matching its slot; face and height rules kept | One design mixes families without purpose | Several designs off-message or rules broken | 30% |
| Measurement | All six measured, CSV reruns to the same table, readings discussed | Measured, small errors | Missing or not reproducible | 15% |
| Blind-read test | Five or more readers per design, results tabled, revision retested | Test run, fewer readers or no retest | Not run | 25% |
| Reflection | Explains disagreements between model and readers with specific causes (context, convention, detail, direction) | Describes disagreements without explaining them | Missing | 15% |
