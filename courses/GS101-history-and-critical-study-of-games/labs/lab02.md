# GS101 · Lab 02: Rebuild the loop

**Week:** 2 · **Time:** 2 hours in the lab plus up to 2 hours at home · **Weight:** feeds the timeline project (25%) as one "technical cause" entry

**Lecture:** [Week 02, early computer games](../lectures/w02-early-computer-games.md)

## Objective

Implement the velocity-then-position update loop from the lecture, reproduce its tennis and orbit tables, and use your model to explain one early design decision. By the end you will have run the same loop that drove Tennis for Two's ball and Spacewar!'s ships, and written a short historical note that links a technical choice to how a game played.

## Starter materials

No files are needed. Use any spreadsheet (LibreOffice Calc, Google Sheets or Excel). If you prefer code, any language is fine, but submit a table of outputs as well.

**Sheet 1, "Court".** Put the constants in cells B1 to B4:

| Cell | Label | Value |
|---|---|---|
| B1 | g | 9.8 |
| B2 | dt | 0.1 |
| B3 | vx0 | 4 |
| B4 | vy0 | 6 |

Set up columns from row 7 down, with headers in row 6:

| Column | Header | Row 7 (start) | Row 8 onward (semi-implicit) |
|---|---|---|---|
| A | step | 0 | `=A7+1` |
| B | t | 0 | `=A8*$B$2` |
| C | vy | `=$B$4` | `=C7-$B$1*$B$2` |
| D | x | 0 | `=D7+$B$3*$B$2` |
| E | y | 0 | `=E7+C8*$B$2` |
| F | exact y | 0 | `=$B$4*B8-0.5*$B$1*B8^2` |
| G | y explicit | 0 | `=G7+H7*$B$2` |
| H | vy explicit | `=$B$4` | `=H7-$B$1*$B$2` |

Note the difference between E and G. Column E uses the new velocity (C8). Column G uses the old one (H7). Fill down 20 rows.

**Sheet 2, "Star".** Constants: `G` in B1 (1), `dt` in B2 (0.1). Columns from row 7:

| Column | Header | Row 7 | Row 8 onward (semi-implicit) |
|---|---|---|---|
| A | step | 0 | `=A7+1` |
| B | x | 1 | `=B7+D8*$B$2` |
| C | y | 0 | `=C7+E8*$B$2` |
| D | vx | 0 | `=D7-$B$1*B7/(B7^2+C7^2)^1.5*$B$2` |
| E | vy | 1 | `=E7-$B$1*C7/(B7^2+C7^2)^1.5*$B$2` |
| F | distance | `=SQRT(B7^2+C7^2)` | fill down |

Fill down 63 rows for one lap. Then build an explicit copy in columns H to L, where position uses the previous row's velocity and velocity uses the previous row's position.

**Target values to check against** (from the lecture): court semi-implicit apex 1.542, explicit apex 2.142, exact 1.837. Star after 63 steps: semi-implicit distance 1.001, explicit 2.090.

## Steps

1. **Court (30 min).** Build sheet 1. Confirm your rows at `t = 0.1, 0.2, 0.3` match the lecture. Chart columns D against E, F and G on one scatter chart.
2. **Star (30 min).** Build sheet 2 and its explicit copy. Confirm the distances after 1, 2 and 3 steps and after one lap. Chart x against y for both methods.
3. **Step size (15 min).** Change `dt` to 0.05 and then 0.2 on both sheets (adjust the number of rows so the star still completes one lap). Record the apex and the one-lap distance for each method in a small table.
4. **Gravity settings (15 min).** Tennis for Two's 1959 version offered low (Moon-like) and high (Jupiter-like) gravity. Use `g = 1.63` and `g = 24.8` as stand-ins. Record apex height and flight time. The lecture's sources do not give the values the 1959 machine used, so say in your notes that these are illustrative.
5. **Choose an early design decision (10 min).** Pick one: Dan Edwards's gravity star in Spacewar!, Computer Space dropping the star (1971), the Moon and Jupiter settings in Tennis for Two, or Asteroids' ship slowly coming to rest. Write its `accel` rule.
6. **Historical note (at home).** Write the note described under Deliverable.

## Deliverable

- Your spreadsheet (or code plus output tables) with both sheets, both charts and the step-size table.
- A 400-word historical note in the timeline-project format: the game and year, the technical decision, its `accel` rule, what the decision did to play (use your sheets as evidence), and one sentence on what the sources do not tell us about why the decision was made. Cite at least two sources from the lecture.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Court model | Both methods correct; values match targets; chart clear | One method correct or small mismatch explained | Values do not match and no explanation | 20% |
| Star model | Both methods correct; spiral and stable orbit both visible | One method correct | Not built or wrong | 20% |
| Step-size analysis | Table complete; states how error changes with `dt` for each method | Table complete, no conclusion | Missing | 15% |
| Accel rule | Correct rule for the chosen decision with every symbol named | Rule mostly correct | Missing or wrong | 10% |
| Historical note | Links a technical decision to play with evidence from the sheets; separates what is known from what is guessed; two sources cited | Link made but evidence thin or one source | Description only, or invented motives presented as fact | 25% |
| Writing | 350-450 words, plain and precise | Length or clarity slightly off | Far off length or hard to follow | 10% |
