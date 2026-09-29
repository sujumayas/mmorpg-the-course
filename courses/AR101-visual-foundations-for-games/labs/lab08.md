# AR101 · Lab 08: One set of drawings, two weights

**Week:** 8, sprite animation: frames and timing ([lecture](../lectures/w08-sprite-animation-frames-and-timing.md)).
**Time:** 2 hours in studio, plus up to 4 hours at home.
**Weight:** one of the weekly studies (50% of the course grade across all studies).
**Type:** studio brief. The art is the main work. A small script checks your timing sheets so the numbers can be graded the same way for everyone.

## Objective

Animate one attack for an invented character, using six to eight drawings. Then deliver it twice, once timed as a light attack and once as a heavy attack, without changing a single drawing. You show that weight comes from timing, and you learn to write timing down so a programmer can use it.

## Starter materials

In [`lab08-starter/`](lab08-starter/):

- [`check_timing.py`](lab08-starter/check_timing.py) reads two timing sheets (light and heavy), prints the start tick of every drawing and the phase sums, and checks the six rules listed below. Standard-library Python.
- [`example_light.csv`](lab08-starter/example_light.csv) and [`example_heavy.csv`](lab08-starter/example_heavy.csv) are the lecture's light and heavy swing timings. They pass the checker. [`example_even.csv`](lab08-starter/example_even.csv) is the even timing and fails when used as both sheets. Run it to see the failure messages.
- The [interactive](../examples/w08-timing-chart.html) for trying holds before you export.
- Any pixel editor with per-frame durations. Aseprite, LibreSprite and Piskel all work. Canvas size 48 by 48 pixels, at most 8 colors, reusing the palette rules from week 5 and the pixel rules from week 6.

Try the checker first from the repository root:

```
.venv/bin/python courses/AR101-visual-foundations-for-games/labs/lab08-starter/check_timing.py courses/AR101-visual-foundations-for-games/labs/lab08-starter/example_light.csv courses/AR101-visual-foundations-for-games/labs/lab08-starter/example_heavy.csv
```

It prints both schedules and `ALL RULES PASS`.

## The brief

Your character is an invented creature or person with one attack: a swing, bite, stomp, slam or cast. No existing game characters, and no traced art.

The checker enforces these rules on your two sheets:

1. Both sheets list the same drawings in the same order.
2. Every hold is a whole number from 1 to 60 ticks, and the phases run windup, active, recovery, each present at least once.
3. The light version totals 15 to 30 ticks (250 to 500 ms).
4. The heavy windup is at least twice the light windup.
5. The heavy recovery is longer than the light recovery.
6. The heavy active phase is no more than 2 ticks longer than the light one.

Rule 6 is the lesson. You may not make the heavy attack heavy by holding the hit longer.

## Steps

1. **Thumbnails.** Sketch the six to eight poses as silhouettes at full size (48 by 48). Black-fill each one and check it reads on its own, as in week 3. Mark which are windup, active and recovery.
2. **Key poses.** Draw the peak of the windup and the strike first. These two carry the idea. Then draw the rest.
3. **Light timing.** Write `light.csv` with the header `drawing,hold_ticks,phase`. Enter the holds in your editor. At 60 ticks per second, a hold of `h` ticks is `h × 1000 / 60` ms. Prefer multiples of 3 ticks, which give whole milliseconds (50, 100, 150 ms).
4. **Heavy timing.** Copy the sheet to `heavy.csv` and change only the holds. Put the new time in the windup peak and the settle.
5. **Check.** Run `check_timing.py light.csv heavy.csv` until it prints `ALL RULES PASS`.
6. **Blind test.** Show both GIFs to two classmates in random order. Ask which is heavy and which hold told them. Write down their answers exactly.
7. **Export.** Export each version as a GIF at 4× scale and as a horizontal sprite sheet PNG (one row, drawings in play order).

## Deliverable

One folder containing:

- `light.gif`, `heavy.gif` (4× scale) and `sheet.png` (the drawings once, in order).
- `light.csv` and `heavy.csv`, which pass the checker. Paste the checker's output into your note.
- `note.md`, at most 200 words. Where did the heavy version's extra ticks go, drawing by drawing? What did your blind testers say? If one of them got it wrong, which hold would you change?

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Timing sheets | Both pass the checker; holds planned in multiples of 3 or rounding explained | Pass the checker, no reasoning on ms | Fail the checker | 20% |
| Readable poses | Every drawing reads as a silhouette at 1×; windup peak and strike are the clearest | One drawing muddy | Several drawings don't read | 25% |
| Weight contrast | Blind testers identify the heavy version and name the hold | Identified, but testers can't say why | Testers can't tell | 25% |
| Pixel craft | Clean lines, consistent palette and light direction across drawings | Minor noise or palette drift | Inconsistent drawings | 15% |
| Note | Accounts for every added tick and proposes a concrete change | Partial account | Missing or vague | 15% |
