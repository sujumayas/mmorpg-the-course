# AR101 · Lab 09: Composing for the first look

**Week:** 9, composition and leading the eye ([lecture](../lectures/w09-composition-and-leading-the-eye.md)).
**Time:** 2 hours in studio, plus up to 3 hours at home.
**Weight:** one of the weekly studies (50% of the course grade across all studies).
**Type:** studio brief with a checking script. You paint the scenes. The script checks your values against the week 9 model, and real people check the model.

## Objective

Paint one invented game scene three times in greyscale, each time steering the first look to a different target, and show with numbers that each version has one clear focal point. Then test whether people actually look where the model says.

## Starter materials

In [`lab09-starter/`](lab09-starter/):

- [`focal_map.py`](lab09-starter/focal_map.py) loads a PNG, converts every pixel to value (CIE L*, 0-100, as in week 1), averages it into a grid (8 by 5 by default), prints the value grid and the local contrast grid, finds the focal cell, the rival and `H`, and prints PASS if the focal cell is inside your target box and `H ≥ 1.5`. Needs Pillow, which is in the course `.venv`.
- [`make_example.py`](lab09-starter/make_example.py) writes `example_doorway.png`, the lecture's scene A padded to 8 by 5. Run it, then run the checker on it to see a passing report.
- The [interactive](../examples/w09-focal-map.html). Its image tool uses the same conversion as the script, so you can check a thumbnail in the browser too.
- Any paint program. Krita, GIMP, Photoshop, Procreate or a pixel editor all work. Canvas 320 by 200 pixels, greyscale only.

Try the example from the repository root:

```
.venv/bin/python courses/AR101-visual-foundations-for-games/labs/lab09-starter/make_example.py
.venv/bin/python courses/AR101-visual-foundations-for-games/labs/lab09-starter/focal_map.py courses/AR101-visual-foundations-for-games/labs/lab09-starter/example_doorway.png --target 1,4,1,4
```

It reports focal cell (1,4), `H` about 10.2, and PASS.

## The brief

Invent one scene from a game of your choice: a cave mouth, a market square, a ruined bridge, a boss arena. No existing game locations or characters. The scene must contain at least these three possible targets:

- **the exit** (a door, gap, path or stair),
- **a threat** (an enemy or hazard, shown as a simple shape),
- **a pickup** (a small object the player should collect).

Paint three versions of the same layout. Keep the shapes and positions the same and change only values. In version 1 the exit is the focal point, in version 2 the threat, in version 3 the pickup. Use at most five flat values per version.

## Steps

1. **Layout.** Sketch the layout once in line. Mark on an 8 by 5 grid which cells each target covers. Those are your three target boxes.
2. **Version 1, exit.** Block in five values. Run `focal_map.py v1.png --target <exit box>`. Iterate until PASS. Save the report from every run.
3. **Versions 2 and 3.** Repeat for the threat and the pickup. The pickup is small, so expect to work hardest here. You may need to quiet its surroundings (as in scene D) more than you brighten it.
4. **Finer grid.** Rerun each final version with `--grid 16x10` and the target box scaled to match. Note any version that passes at 8 by 5 and fails at 16 by 10, and explain why in one sentence.
5. **People test.** Show each final version for one second, in random order, to at least two classmates who haven't seen your work. Ask them to point to where they looked first. Record the cell.
6. **Compare.** For each version, did people look where the model said? For every miss, name what pulled them instead (a line, a shape like a face, the centre of the screen, an edge).

## Deliverable

One folder containing:

- `v1.png`, `v2.png`, `v3.png` (320 by 200, greyscale), each passing the checker at 8 by 5 with its target box.
- `reports.txt` with every checker run, in order, so the grader can see your iterations.
- `people.csv` with columns `version,tester,first_look_row,first_look_col,predicted_row,predicted_col`.
- `note.md`, at most 250 words. Which version was hardest to make pass, and what value change finally did it? How often did people match the model? What does the model miss that your testers showed you?

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Checker results | All three pass at 8 by 5 with H ≥ 1.5; step 4 explained | Two pass, or all pass with no step 4 | One or none pass | 30% |
| Same layout | Only values change between versions; shapes and positions identical | Minor layout drift | Different layouts | 15% |
| Value craft | At most five values, clear masses, targets readable at 1× | Readable with some noise | Muddy masses | 20% |
| People test | Two or more testers per version, recorded exactly | One tester per version | Missing | 15% |
| Note | Names the decisive value change and a specific limit of the model, with evidence | General comments | Missing or vague | 20% |
