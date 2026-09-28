# CS101 review: open items

Review date 2026-09-28. Everything fixed during the review is already in the lecture, lab and assessment files. This file lists only what is still open, with a proposed fix for each.

## 1. Forward links that still point at syllabi

- **Files:** `lectures/w03-loops-and-the-game-loop.md` (CS202 week 12, deterministic lockstep), `lectures/w10-collision-basics-aabb-and-circles.md` (MA201 week 9, separating axis test), `lectures/w12-debugging-breakpoints-logging-rubber-ducking.md` (CS202 week 5, bit packing), `lectures/w14-polish-pass-sound-particles-screen-shake.md` (AU101).
- **Problem:** those lectures don't exist yet, so the links go to the course syllabus.
- **Fix:** once CS202 w05 and w12, MA201 w09 and the AU101 lectures exist, change each link to the lecture file. The week number is already in the link text.

## 2. CS101 relies on concurrent MA101 weeks that come later

- **Files:** w08 (vector length, MA101 w12), w10 (distance and squared distance, MA101 w12 and w14), w13 (squared distance, MA101 w14), w04 and w05 (clamps, MA101 w07).
- **Problem:** CS101 has no prerequisites, and MA101 runs in the same semester. These CS101 weeks use ideas that MA101 teaches later.
- **Done in this review:** each lecture now explains what it uses: Pythagoras and √2 in w08, the squared-distance argument in w10, and `min` as a cap in w05. The links now say "later this semester" instead of "you studied".
- **Open:** the program could reorder MA101 so that vectors and distance come before CS101 week 8. That is a curriculum decision, not a lecture fix.

## 3. Stub demos crash when a lab starter is run directly

- **Files:** `labs/lab05-starter/inventory.py`, `lab06-starter/itemdb.py`, `lab07-starter/scene_tree.py`, `lab08-starter/jump_input.py`, `lab09-starter/frame_rates.py`, `lab10-starter/collision.py`, `lab11-starter/ghosts.py`.
- **Problem:** running the file before any work raises `NotImplementedError` from the `__main__` demo. The test files handle this and report "not implemented yet". The plain script shows a traceback instead.
- **Fix (optional):** wrap each `__main__` demo in `try/except NotImplementedError` and print "Fill in Part B first, then run the tests." The lab sheets' first step already tells students to expect failures, so nothing is broken.

## 4. Machine-specific timings in w06

- **File:** `lectures/w06-dictionaries-item-databases.md`, timing table.
- **Problem:** the times are from an Apple M4 Pro with Python 3.13.5. A rerun in this review gave 265 µs for the 10,000-record list against 260 µs in the table. The shape matches and the numbers are close.
- **Fix:** none needed. The review added a `timeit` snippet so students can reproduce the table, and the Sources line now points to it.
