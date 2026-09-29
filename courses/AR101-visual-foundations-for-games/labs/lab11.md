# AR101 · Lab 11: The hierarchy audit

**Week:** 11 ([lecture](../lectures/w11-ui-visual-hierarchy.md))
**Time:** 2 hours in the studio, plus up to 3 hours to finish.
**Work mode:** individual.
**Counts toward:** weekly studies (50% of the course grade, shared across the weekly labs).

## Objective

Measure the hierarchy of a shipped UI panel, then redesign it so the eye's order matches the order of importance. You finish a small tool that turns the lecture's weight model into a report, and you check its verdict against your own eyes with a blur.

## Starter materials

- [`lab11-starter/hierarchy.py`](lab11-starter/hierarchy.py): a Python 3 skeleton (standard library only) with `lightness` provided and four functions to write: `weight`, `element_weight`, `inversions` and `weak_steps`. It also has a CSV loader and a report.
- [`lab11-starter/test_hierarchy.py`](lab11-starter/test_hierarchy.py): tests built from the lecture's numbers. They all fail on the starter.
- [`lab11-starter/loot_labels.csv`](lab11-starter/loot_labels.csv): the lecture's "hue only" loot labels, as a format example. Columns: `name`, `level` (1 = least important), `size` (relative to body text), `text` (hex), `plate` (hex, blank for none), `plate_area` (in body-text lines).
- [`lab11-starter/blur_preview.py`](lab11-starter/blur_preview.py): the squint test as a script (needs Pillow, which the course `.venv` has). It writes a blurred copy of any PNG, optionally in grayscale.
- Any layout or paint tool for the mockups (Figma, Krita, GIMP, Aseprite or similar).
- The [squint hierarchy interactive](../examples/w11-squint-hierarchy.html) for quick what-if checks.

Run the tests first from inside `lab11-starter/`, with the course Python:

```
python test_hierarchy.py
```

Every test prints `TODO` until you write the functions.

## Steps

### Part A: finish the tool (35 min)

1. Implement the four functions following their docstrings and the lecture's section 2 model. Run the tests until all six pass.
2. Run `python hierarchy.py loot_labels.csv --ground 525252`. You should get weights of about 29.9, 65.1, 13.1 and 12.8, "inversions: 5 of 6" and two weak steps. These match the lecture's hue-only table (the ground here is L* 34.9 rather than exactly 35).

### Part B: audit a shipped panel (35 min)

3. Pick one UI panel from a game you can play: an item tooltip, a quest tracker, a vendor window, a party frame or a loot window. Take a screenshot at your normal resolution. Record the game, platform and version or date.
4. Write the panel's importance list (5 to 10 elements) and give each a level from 1 (least) to 4 (most).
5. Fill a CSV for the panel. Use a color picker for text and plate colors. Estimate `size` against the panel's body text and `plate_area` in body-text lines. Pick the ground color from the area right around the panel.
6. Run the tool. Then run `python blur_preview.py your_screenshot.png --gray` and write down the order in which blobs catch your eye. Compare the two orders.

### Part C: redesign (50 min)

7. Mock up a redesign of the same panel with the same content. Keep any color code the game uses for categories, and change weight channels (size, value, plates, grouping, position) to fix the inversions and weak steps.
8. Fill a CSV for your redesign and run the tool until it reports zero inversions and no weak steps, or explain in your note why one weak step is acceptable.
9. Run the blur on your mockup and compare it with the original's blur.
10. Test the redesign on two grounds: the panel's real background and a much lighter or darker one (for example a snowfield or a cave). Report both.

## Deliverable

- A single PDF, at most 4 pages, containing:
  - the original screenshot and its blurred version, with the importance list and the tool's report;
  - your mockup and its blurred version, with the tool's report on both grounds;
  - a design note of 250 to 350 words: what the original's hierarchy ranked wrongly, which channels you changed and why, and one disagreement between the model and your eye, with your explanation.
- Your finished `hierarchy.py` and both CSV files.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Tool correctness | All six tests pass; Part A report matches the lecture | Tests pass but report misread, or one function wrong with a correct fix described | Tests fail | 20 |
| Audit of the shipped panel | Importance list is defensible, CSV values traceable to the screenshot, model and blur orders compared | Audit done but values guessed or comparison missing | Missing | 20 |
| Redesign result | Zero inversions and no weak steps on the real ground, and a stated plan for the second ground | One inversion or weak step left without justification | Redesign does not improve the report | 25 |
| Craft | Mockup is clean, keeps the game's category code, reads correctly in the blur | Readable but rough, or loses the category code | Unreadable | 20 |
| Design note | Specific, uses the lecture's terms, includes a real model-versus-eye disagreement | Generic, or no disagreement discussed | Missing | 15 |
| **Total** | | | | **100** |
