# AR101 · Lab 03: The silhouette test as a program

**Week:** 3, silhouette readability ([lecture](../lectures/w03-silhouette-readability.md)).
**Time:** 2 hours in lab, plus up to 3 hours at home.
**Weight:** one of the weekly studies (50% of the course grade in total). Your final roster is reused in the style bible (week 13).

## Objective

Turn the silhouette test into a repeatable check. You will write the four functions behind the lecture's pair table, reproduce its numbers, then design a four-class roster of your own and revise it until every pair is distinct at full and half size. Finally you will check the numbers against real people.

## Starter materials

All in [`lab03-starter/`](lab03-starter/). Standard-library Python, no packages needed.

- [`silhouette_test.py`](lab03-starter/silhouette_test.py), a skeleton with four empty functions (`iou`, `normalize`, `downsample`, `worst_pairs`) and a finished loader, renderer and report that prints the pair matrix at scales 1 and 1/2.
- [`sprites/`](lab03-starter/sprites/), the lecture's original roster as text files (`knight.txt`, `mage.txt`, `cleric.txt`, `rogue.txt`), 12 × 20, with `#` for filled and `.` for empty.
- [`test_silhouette.py`](lab03-starter/test_silhouette.py) with the lecture's values: pixel counts 91, 98, 74 and 74; cleric and rogue IoU 70/78; knight and mage 70/119; the rogue shrinking to 20 pixels at half size with its dagger gone; alignment that ignores where a sprite sits in its file; and the worst-pair ordering.
- The [interactive](../examples/w03-silhouette-lineup.html) for spot checks.

Run the tests from inside the folder with `python3 test_silhouette.py`. On the starter, one test passes (pixel counts) and six do not. When all pass, run `python3 silhouette_test.py sprites --threshold 0.80`.

## Steps

1. **Implement.** Fill in the four functions until every test passes. Do not change the tests.
2. **Reproduce.** Run the report on `sprites/`. Confirm the lecture's two tables: cleric and rogue at 0.897 at full size and 1.000 at half size.
3. **Apply the lecture's fixes.** Copy `sprites/` to `sprites_fixed/`. Add the cleric's robe and replace the rogue's dagger with the long knife (coordinates in the lecture's interactive spec). Confirm every pair is at or below 0.75 at both sizes.
4. **The anchor trap.** Make a copy of `mage.txt` in which the staff reaches the bottom row (add one `#` at column 10, row 19). Run the report again. Explain in three sentences what happened to the mage's pairs and why, then propose a better anchoring rule and say what it would get wrong.
5. **Your roster.** Design four classes for an invented game (tank, healer, ranged damage, melee damage) on a 16 × 24 grid. Start from a shared body of your own design, then give each class its own parts. Save them as text files in `my_roster/`.
6. **Iterate.** Run the report. Revise until no pair is at or above 0.80 at either scale, and aim for 0.75 or below. Keep every version in a numbered subfolder (`v1/`, `v2/`, ...), and log what you changed and why.
7. **Human check.** Print or display your final roster as black silhouettes in a shuffled order. Show it for one second to at least five people who know which role is which (give them a colored reference sheet first). Record how many they label correctly, per class.
8. **Compare.** Does the pair with the highest IoU match the pair people confused most? Write a short explanation either way, using the lecture's "eyes-open" points (weighting of the top of the outline, anchoring, pose).

**Stretch (optional).** Add a function that computes IoU on the top third of each normalized mask only, and report it next to the full IoU. Does it predict your human results better?

## Deliverable

The folder with `silhouette_test.py` (all tests passing), `sprites_fixed/`, the anchor-trap answer, `my_roster/` with every version, the report output for the final version at both scales, the human test results, and a note of at most 500 words covering steps 4, 6 and 8.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Code correctness | All tests pass; lecture tables reproduced; fixes confirmed | Tests pass, fixes not confirmed | Tests fail | 25% |
| Anchor trap | Correct diagnosis of the shifted feet anchor, a better rule proposed with its own weakness named | Diagnosis correct, no alternative | Missing or wrong | 10% |
| Roster design | Four classes each owning a large, distinct part of the outline; all pairs ≤ 0.75 at both scales | All pairs below 0.80, some above 0.75 | A pair at 0.80 or more | 30% |
| Iteration log | Versions kept, each change justified by the numbers | Versions kept, thin reasons | No history | 10% |
| Human check and comparison | Five or more people, per-class scores, a reasoned comparison with IoU | Test run, comparison thin | Not run | 25% |
