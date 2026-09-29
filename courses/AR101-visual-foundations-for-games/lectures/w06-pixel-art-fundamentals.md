# AR101 · Week 06 — Pixel Art Fundamentals

**Why this matters:** In pixel art every pixel is a decision you can see. A line one pixel off reads as a wobble, a sprite scaled by 2.5 has pixels of two different sizes, and a stray dot becomes noise the player's eye keeps landing on. This week gives you the grid-level rules that decide whether small art reads as clean or messy, and the arithmetic behind them, so you can fix problems by counting instead of by feel.

**You will be able to:**
- Compute the run pattern of any pixel line from its width and height, and predict whether it will look clean.
- Choose line angles for a pixel-art style (including the 2:1 "isometric" angle) and explain why true 30° lines are avoided.
- Compute the on-screen width of every art pixel at a given scale, and explain why non-integer scaling creates mixels.
- Critique a sprite for orphan pixels, jaggies, doubles, banding and pillow shading, and fix each.

**Before class:** Wikipedia, "Isometric video game graphics," the section on the difference between true isometric projection and the 2:1 pixel ratio (about 5 minutes). NESdev Wiki, "PPU palettes" and "PPU OAM," the first screen of each (about 10 minutes); you only need the sprite sizes and the palette limits. Bring the zone palette you are building in lab 05.

**Prerequisites from earlier courses:** From this course, [week 3, silhouette readability](w03-silhouette-readability.md) (a small sprite must read as a silhouette first) and [week 5, palettes](w05-palettes-and-color-harmony.md) (you will draw with a limited palette and its ramps). Value checks use the L* and ΔV of [week 1](w01-seeing-like-an-artist-value-before-color.md). Slope as rise over run is from [MA101 week 2](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w02-linear-functions-and-rates.md), and the `floor` function from [MA101 week 7](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w07-piecewise-caps-and-floors.md).

**Interactive:** [`examples/w06-clean-pixel-lines.html`](../examples/w06-clean-pixel-lines.html). Keep it open during section 2.

---

## 1. The grid is the medium

**Pixel art** is art drawn and displayed so that each pixel of the image is placed by hand and shown as a crisp square. It started as a hardware necessity and survives as a style. Either way, the grid sets the rules.

### Budgets you can count

On the NES, a hardware sprite is 8 × 8 or 8 × 16 pixels, and a sprite palette holds 4 entries, one of them transparent, so each sprite gets 3 visible colors. Only 8 sprites can share one scanline. Backgrounds choose a palette per 16 × 16 pixel area (2 × 2 tiles). The whole picture is 256 × 240 pixels. The original Game Boy screen is 160 × 144 pixels, with sprites of 8 × 8 or 8 × 16, 4 shades, and at most 10 sprites per line. Characters in games for those machines were built from several hardware sprites, but the limits still shaped every drawing.

You are not bound by that hardware, and you should still set budgets, because they force the decisions that make small art readable. A useful way to state a budget:

- **Canvas.** A 16 × 16 sprite has 256 pixels. A 32 × 32 sprite has 1,024, four times as many to draw, animate and keep consistent.
- **Colors.** A small sprite rarely needs more than one ramp of three or four steps per material plus an outline color. Your week 5 palette is the budget.
- **Features.** At 16 × 16, a face is an eye or two and maybe a mouth. An eye is one or two pixels. If a feature is smaller than two pixels, or differs from its neighbors by less than week 1's ΔV of 20, it will not read at game scale.

That last point is the rule week 7 relies on for tiles. Detail that is smaller than two pixels or lower than about 20 in ΔV disappears when the art is shown at its intended size. Draw at 1× in a second window while you work. If you only look at the zoomed canvas, you will add detail nobody can see.

### Silhouette first, then interior

Week 3 taught you to test a character by filling it black. In pixel art this is how you start. You block the silhouette with one color at the target size, check it reads, then subdivide the interior with your ramps. Adding shading cannot rescue a silhouette that fails at 1×.

## 2. Worked example: why pixel art loves 26.57°

### The hook

Many "isometric" pixel-art games are not isometric at all. True isometric projection draws the ground axes at 30° from horizontal. Pixel artists draw them at about 26.57° instead, using lines that step two pixels across for every one pixel up. The Wikipedia article on isometric game graphics names this the 2:1 pixel ratio and says early hardware could not draw clean 30° lines, because it lacked the colors and processing power for anti-aliasing. So the whole visual style of a genre bent its geometry by 3.4° to get cleaner lines.

What makes one angle clean and another messy? And why can't a 30° line be clean at any size?

### The model

On a pixel grid, a straight line is a staircase. Take a line that is `w` pixels wide and `h` pixels tall, with `w ≥ h ≥ 1` (a shallow line; for a steep one, swap the roles of rows and columns). It is drawn as `h` horizontal **runs**, one per row, and each run starts where the previous one ended, one row up. The length of run `k`, for `k = 0, 1, …, h − 1`, is

```
r_k = floor((k + 1) × w / h) − floor(k × w / h)

angle   = atan(h / w)
period  p = h / gcd(w, h)
```

- `floor` rounds down to a whole number.
- The runs always add up to `w`, and each run is either `floor(w/h)` or one more.
- `gcd(w, h)` is the greatest common divisor. The run pattern repeats every `p` runs.

The model gives three kinds of line.

- **Clean** (`p = 1`): every run has the same length. This happens exactly when `h` divides `w`: slopes 1:1, 2:1, 3:1, 4:1 and so on.
- **Steady** (`p = 2`): runs alternate between two lengths, such as 2, 3, 2, 3. The eye reads the alternation as a texture, and the line still looks straight.
- **Wobbly** (`p ≥ 3`): the longer runs arrive at irregular-looking intervals, and the eye sees a line that bends slightly each time the pattern changes.

A **jaggy** is anything this formula cannot produce. If two runs in a line differ by more than one pixel, or the long runs bunch together (3, 3, 1, 1 instead of 2, 2, 2, 2), the line has a kink. Hand-drawn lines get jaggies all the time; this is how you find them.

### Numbers you can check

| Size w × h | Angle | Runs | Period p | Reads as |
|---|---|---|---|---|
| 8 × 8 | 45.00° | 1, 1, 1, 1, 1, 1, 1, 1 | 1 | clean |
| 8 × 4 | 26.57° | 2, 2, 2, 2 | 1 | clean (the "isometric" line) |
| 12 × 4 | 18.43° | 3, 3, 3, 3 | 1 | clean |
| 10 × 4 | 21.80° | 2, 3, 2, 3 | 2 | steady |
| 9 × 4 | 23.96° | 2, 2, 2, 3 | 4 | wobbly |
| 7 × 4 | 29.74° | 1, 2, 2, 2 | 4 | wobbly |
| 12 × 5 | 22.62° | 2, 2, 3, 2, 3 | 5 | wobbly |

Check one row by hand. For 12 × 5, `w/h = 2.4`. The floors of `2.4k` for `k = 0 … 5` are 0, 2, 4, 7, 9, 12. The differences are 2, 2, 3, 2, 3. And `gcd(12, 5) = 1`, so `p = 5`: the pattern never repeats inside this line.

Now the hook's question. A 30° line needs `h / w = tan 30° = 0.577…`, which is `1/√3`. That is irrational, so no whole-number `w` and `h` can hit it exactly, and any close fraction has a large period. The 7 × 4 row (29.74°) is about as close as a short line gets, and it is wobbly, with a single short run at the start. The 2:1 line gives up 3.43° and gets the cleanest possible pattern. That is the trade the genre made.

### The same thing in code

```python
from math import atan2, degrees, floor, gcd

def runs(w, h):
    """Run lengths of a pixel line w columns wide and h rows tall (w >= h >= 1)."""
    return [(k + 1) * w // h - k * w // h for k in range(h)]

def period(w, h):
    """How many runs before the pattern repeats."""
    return h // gcd(w, h)

for w, h in [(8, 8), (8, 4), (12, 4), (10, 4), (9, 4), (7, 4), (12, 5)]:
    angle = degrees(atan2(h, w))
    print(f"{w:>2}x{h}  {angle:5.2f} deg  runs {runs(w, h)}  period {period(w, h)}")

def pixel_widths(scale, n):
    """Screen pixels covered by each of n art pixels at a given scale."""
    return [floor((i + 1) * scale) - floor(i * scale) for i in range(n)]

print(pixel_widths(2.5, 6), pixel_widths(3, 6), pixel_widths(1080 / 240, 6))
```

With `.venv/bin/python` it prints:

```
 8x8  45.00 deg  runs [1, 1, 1, 1, 1, 1, 1, 1]  period 1
 8x4  26.57 deg  runs [2, 2, 2, 2]  period 1
12x4  18.43 deg  runs [3, 3, 3, 3]  period 1
10x4  21.80 deg  runs [2, 3, 2, 3]  period 2
 9x4  23.96 deg  runs [2, 2, 2, 3]  period 4
 7x4  29.74 deg  runs [1, 2, 2, 2]  period 4
12x5  22.62 deg  runs [2, 2, 3, 2, 3]  period 5
[2, 3, 2, 3, 2, 3] [3, 3, 3, 3, 3, 3] [4, 5, 4, 5, 4, 5]
```

The last line belongs to section 3. Notice that `pixel_widths` is the run formula again, with `scale` in place of `w / h`.

### A visual you can move

Open [`examples/w06-clean-pixel-lines.html`](../examples/w06-clean-pixel-lines.html). The left panel draws a line on a zoomed pixel grid, with each run outlined and labelled with its length. Drag the angle slider smoothly from 0° to 45°. The line's angle changes smoothly, but its look does not: it snaps into perfect staircases at a handful of angles and turns wobbly everywhere between.

The right panel is the explanation. It plots every line up to 32 pixels wide as a dot, angle on the horizontal axis and period on the vertical. Clean lines sit on the floor at `p = 1`. Every `w : 1` slope up to 32 : 1 is there, but only the first few are far enough apart to be useful choices: 45°, 26.57°, 18.43°, 14.04°, 11.31°. The rest, 6 : 1 to 32 : 1, crowd together below 10°, where a line is nearly flat anyway. Steady lines sit one row up. Everything else sprays upward. A vertical marker shows the true isometric 30°, standing in empty space. A small preview at 1× scale in the corner shows the line at its real size, where a wobble reads as a bend.

### Cross-game recognition

**Isometric pixel art (1980s onward).** Rewritten in the model, "2:1 dimetric" means `w/h = 2`, `p = 1`: runs of two, forever. Every floor tile edge, wall base and roof line in that style uses the same run pattern, which is why the style looks crisp even at small sizes, and why a 30° edge drawn by mistake in such a game looks broken.

**Bresenham's line algorithm (IBM, 1962).** Jack Bresenham wrote his line-drawing algorithm to drive a pen plotter attached to an IBM 1401. It decides for each column whether to step up a row, using only whole-number arithmetic. Its output is the same kind of run pattern as our formula: runs of `floor(w/h)` and one more, spread as evenly as possible (Bresenham rounds to the nearest row instead of flooring, which only moves where the long runs fall). Every engine's "draw line" routine inherits this pattern. So the wobble of a 12 × 5 line is not your hand shaking. It is arithmetic.

**Scaling retro resolutions to modern screens.** The NES picture is 240 pixels tall. On a 1080-pixel-tall display that is a scale of exactly 4.5, and the rows come out 4, 5, 4, 5 screen pixels tall, the run pattern of a 9 × 2 line. A Game Boy's 144 rows on the same display is a scale of 7.5: rows of 7 and 8. Section 3 shows why this matters and how to avoid it.

One formula covers art lines, rasterizer lines and scaled pixels.

### Eyes-open design judgment

- **Pick your angles up front.** A style guide for pixel art should list the allowed slopes, usually 1:1, 2:1 and sometimes 3:1 and 1:2. Everything else is drawn as a curve, not a line.
- **Steady lines are fine.** A 2, 3, 2, 3 line reads as straight. Do not twist a design to avoid it. Save the effort for wobbly lines on long edges, where the eye follows them.
- **Curves are runs that change gradually.** A clean curve's runs change length smoothly, such as 4, 3, 2, 1, 1 for a quarter circle's edge. A curve with runs 3, 1, 2, 1 has a bump. Use the same counting to fix curves.
- **Anti-aliasing can hide a wobble but costs colors.** A mid-tone pixel at each step softens the staircase. On a 3-color sprite you cannot afford it; on a 16-color one you can, sparingly (section 4).

### Check yourself (worked example)

1. Compute the runs, angle and period of a 15 × 6 line.
2. A hand-drawn line 10 pixels wide and 4 tall has runs 3, 1, 3, 3. Is it a jaggy? What should it be?

<details>
<summary>Answers</summary>

1. `w/h = 2.5`. Floors of `2.5k` for `k = 0 … 6`: 0, 2, 5, 7, 10, 12, 15. Runs 2, 3, 2, 3, 2, 3. Angle `atan(6/15) = 21.80°`. `gcd(15, 6) = 3`, so `p = 6/3 = 2`: a steady line, the same angle as 10 × 4.
2. Yes. The runs differ by 2 (3 against 1), which the model never produces. It should be 2, 3, 2, 3 (period 2). The single-pixel run reads as a kink.

</details>

## 3. Scale, and why pixels must stay square

Pixel art is drawn small and shown large. The engine multiplies each art pixel by a **scale factor** `s`. Art pixel `i` then covers screen columns from `floor(i × s)` up to `floor((i + 1) × s)`, so its width on screen is

```
width_i = floor((i + 1) × s) − floor(i × s)
```

This is the run formula with `s` in place of `w/h`, and it behaves the same way. At `s = 3` every art pixel is 3 screen pixels wide. At `s = 2.5` the widths alternate 2, 3, 2, 3. On a 16-pixel sprite that means half its pixels are 50% wider than the others. Lines that were clean at 1× turn wobbly on screen, and a one-pixel eye may land on a narrow column in one frame and a wide one the next as the sprite moves.

| Scale | Widths of the first six art pixels | Uniform? |
|---|---|---|
| 2 | 2, 2, 2, 2, 2, 2 | yes |
| 2.5 | 2, 3, 2, 3, 2, 3 | no |
| 3 | 3, 3, 3, 3, 3, 3 | yes |
| 4.5 (NES rows on 1080p) | 4, 5, 4, 5, 4, 5 | no |
| 7.5 (Game Boy rows on 1080p) | 7, 8, 7, 8, 7, 8 | no |

Two rules follow.

1. **Integer scale only.** Show pixel art at 1×, 2×, 3× and so on, and letterbox the leftover screen space. If a game must fill a screen whose size is not a multiple of the art, scale by the largest whole number that fits and add a border, or render to a larger internal canvas.
2. **Nearest-neighbor filtering.** Any smoothing filter blends neighboring pixels and blurs every edge. Pixel art needs "nearest" (also called point) filtering at every stage: export, import and display. Week 14 covers the import settings.

### Mixels

A **mixel** (mixed pixel) is an art pixel of a different size from the pixels around it. They appear in three ways:

- **Scaled assets.** One sprite is scaled by 1.5 "to read better" and now its pixels are 1.5 times the size of the tiles' pixels. Week 13 turns this into a style-bible rule.
- **Rotated sprites.** Rotating pixel art by anything but 90° resamples it, so pixels become diamonds and stair-steps of different sizes. Draw rotated frames by hand, or accept the look on purpose.
- **Mixed resolutions.** A 32 × 32 portrait placed next to 16 × 16 sprites at the same scale on screen. It can be a deliberate style, such as sharp UI text over chunky art. It should never be an accident.

The fix is always the same. Use one art pixel size per layer, set it in the style bible, and check it in the engine. Lab 06's checker tests for it by comparing your scaled export with an exact nearest-neighbor enlargement.

## 4. Pixel-level craft: five problems and their fixes

These are the errors a reviewer spots first on a small sprite. Each has a mechanical test.

**Orphan pixels.** A pixel whose color matches none of its eight neighbors. At 1× it reads as noise, a speck the eye keeps jumping to. Sometimes it is right (a one-pixel eye glint, a star). The test: list every orphan and justify each one, or merge it into a neighbor's color.

**Jaggies.** Kinks in lines and curves. The test is section 2's model: along a straight edge, runs must be `floor(w/h)` or one more, spread evenly; along a curve, run lengths should change one step at a time.

**Doubles.** Where a one-pixel line turns a corner or steps diagonally, an extra pixel in the corner makes a small L-shaped clump that looks thicker than the rest of the line. The test: along a line meant to be one pixel thick, no pixel should touch two others of the line both sideways and vertically. Some editors offer a "pixel-perfect" stroke mode that removes these as you draw.

**Banding.** Ramp steps placed in parallel stripes that follow the outline, so the shading looks like contour lines instead of light. It happens when every band is the same width and shape as the edge next to it. Fix it by varying band widths and following the form's lighting, not its outline.

**Pillow shading.** Light in the middle, dark all around the edge, whatever the light direction. It makes every shape look inflated. It is the most common beginner shading. Fix it by choosing a light direction (the top left is a common default) and shading consistently away from it, with the darkest band on the side facing away from the light.

### Outlines

An outline separates the sprite from any background, which week 1 would describe as buying a guaranteed ΔV at the edge. Three common choices:

- **Black outline.** Maximum separation, heavy look, costs one palette slot. Good for busy backgrounds.
- **Colored outline.** Each region outlined with the darkest step of its own ramp. Lighter feel, still separates, costs nothing extra if the ramp already has a dark step.
- **Selective outline** ("sel-out"). The outline gets lighter where light hits the edge. The softest look, the hardest to keep readable on light backgrounds.

Check the outline against your actual backgrounds with week 1's ΔV. An outline that merges with the ground (ΔV under 10) is not doing its job.

### Anti-aliasing and dithering

**Anti-aliasing** (by hand) places an intermediate color at the steps of a line or curve so the staircase looks smoother. Use it inside a sprite, on long diagonals and curves. Avoid it on the outer edge of a sprite that will be shown over many backgrounds, because the in-between color was chosen for one background and will halo on others.

**Dithering** mixes two colors in a checkerboard or pattern so that, at a distance, they read as a third. Week 1 showed that a 50% checker of black and white reads much lighter than middle gray because lightness follows a cube root of light. Dithering suits large flat areas and retro styles. On small sprites it usually reads as noise.

## In-class activity (25 minutes)

Pairs. Any pixel editor, a 64 × 64 canvas, the interactive, and your week 5 palette.

1. **Line drills (8 min).** Draw lines of 1:1, 2:1, 3:1, 5:2 and 12:5 as long as the canvas allows, each in one color with no anti-aliasing. Next to each, write its run list. Your partner checks each list against the formula.
2. **The 30° challenge (4 min).** Draw your best 30° line 28 pixels wide. Compute its runs (`w = 28`, `h = 16`) and period. Compare it with a 2:1 line of the same width. Which would you use for a building?
3. **A 16 × 16 item (10 min).** Draw a potion, key or shield with your week 5 palette: silhouette first, then one ramp, then an outline. Use at most 6 colors.
4. **Swap and review (3 min).** Swap with another pair. List every orphan pixel, jaggy, double and any pillow shading you find, with coordinates.

Expected output: the line sheet with run lists, the item at 1× and 4× (nearest neighbor), and your partner's review list.

## Common misconceptions

- **"A steeper or shallower line is just a different angle."** In pixel art the angle decides the run pattern. Only a few angles give equal runs; everything between looks wobbly.
- **"2.5× is fine, it's close to 3×."** Non-integer scale gives pixels of two widths. It is a correctness problem, not a quality slider.
- **"More colors make better pixel art."** Small sprites need fewer, well-chosen colors. Each extra color is another way to create orphans and noise.
- **"Shade around the edge to make it look round."** That is pillow shading. Roundness comes from shading relative to a light direction.

## Check yourself

1. You want a roof edge at about 20°. Which line sizes up to 16 pixels wide give a clean or steady line closest to 20°? Show the runs.
2. A game renders at 384 × 216 and the player's monitor is 1920 × 1080. What is the scale? Is it safe for pixel art? What if the monitor is 2560 × 1440?
3. A sprite has an outline color at L* 18 and is placed on a dark cave floor at L* 12. What does week 1's rule say, and what would you change?
4. Compute the runs of a 20 × 8 line. Is it the same angle as any line in the section 2 table? Does it look the same?

<details>
<summary>Answers</summary>

1. `tan 20° ≈ 0.364`, so `w/h ≈ 2.75`. Clean options near it: 2:1 (26.57°) and 3:1 (18.43°), the closer. Steady options (`p = 2`): `w/h = 2.5`, such as 10 × 4 with runs 2, 3, 2, 3 at 21.80°. For a roof, 3:1 (runs 3, 3, 3, 3) is the cleanest near 20°, and 10 × 4 is the closest steady line. A 11 × 4 line (runs 2, 3, 3, 3, period 4, 19.98°) hits 20° almost exactly but wobbles.
2. `1920 / 384 = 5` and `1080 / 216 = 5`: an integer, so every art pixel is 5 × 5. Safe. On 2560 × 1440 the scale is `6.67`, not an integer. Use 6× (2304 × 1296) with a border, or render internally at a size that divides the screen.
3. ΔV = 6, under 10, so the outline merges with the floor and the silhouette is lost. Use a lighter outline on dark levels, or switch to a colored or selective outline whose edge pixels are lighter, or lighten the floor.
4. `w/h = 2.5`, runs 2, 3, 2, 3, 2, 3, 2, 3, period `8 / gcd(20, 8) = 2`. Same angle as 10 × 4 (21.80°) and the same steady pattern, just longer. Length does not change whether a line is clean; the ratio does.

</details>

## Lab / assignment hook

[Lab 06, a readable sprite](../labs/lab06.md). A studio brief: draw a 16 × 16, 24 × 24 or 32 × 32 sprite of an invented creature or item from your lab 05 zone, using only that palette, with at least one clean straight edge and a consistent light direction. Deliverable: the sprite at 1× and at an integer scale that passes the provided checker (palette, color count, orphans, exact scaling), plus an annotated review sheet.

## Sources

- NESdev Wiki, "PPU palettes" (retrieved September 2026). Four sprite palettes of four entries each, entry 0 transparent; background palettes; 64-color master palette.
- NESdev Wiki, "PPU OAM" (retrieved September 2026). 8 × 8 and 8 × 16 sprites; 64 sprites in OAM; 8 sprites per scanline.
- NESdev Wiki, "PPU attribute tables" (retrieved September 2026). One background palette choice per 16 × 16 pixel area (2 × 2 tiles).
- NESdev Wiki, "PPU rendering" (retrieved September 2026). A picture region of 256 × 240 pixels.
- Pan Docs (gbdev.io), "Specifications" and "Palettes" (retrieved September 2026). Original Game Boy: 160 × 144 screen, 8 × 8 or 8 × 16 sprites, 40 per screen and 10 per line, four shades.
- Wikipedia, "Isometric video game graphics" (retrieved September 2026). The 2:1 pixel pattern ratio, lines at about 26.565° (arctan ½), dimetric rather than true isometric projection, and the reason given (early hardware lacked the colors and processing power for anti-aliased 30° lines).
- Wikipedia, "Bresenham's line algorithm" (retrieved September 2026). Developed by Jack Elton Bresenham at IBM, in production use by 1962, for a Calcomp plotter attached to an IBM 1401.
- Bresenham, J. E. (1965). "Algorithm for computer control of a digital plotter." *IBM Systems Journal* 4(1), 25-30.

## Interactive spec: examples/w06-clean-pixel-lines.html

**Purpose.** Show that a smooth change of angle produces a pixel line whose look changes in jumps, clean at only a few angles, and that the same floor formula explains non-integer scaling.

**The one insight the visual must make obvious.** On first load, at 30°, the left panel shows a visibly uneven staircase with its runs labelled (for the default width 28: 28 × 16 with runs 1, 2, 2, 2, 1, 2, 2, 2, ...), and the right panel shows 30° standing in an empty gap while 26.57° sits on the `p = 1` floor. One tap on the "2:1" preset makes the left line perfectly regular.

**Layout.** Mobile: stacked (line grid, chart, scale strip). Desktop (900px and up): line grid left, chart right, scale strip full width below.

**Views.**
1. **Line grid.** A `W × H` pixel grid (W = line width, up to 32; each cell 10-16 CSS px depending on space) drawn as squares, no anti-aliasing. The line's pixels are filled; each run gets an alternating light tint and a small number above it with its length. A thin ideal line from corner to corner is overlaid for comparison. Readout: `w × h`, angle to two decimals, run list, period `p`, and the verdict "clean" (p = 1), "steady" (p = 2), "wobbly" (p ≥ 3). A 1× preview (actual size, `image-rendering: pixelated`) of the same line sits in the corner.
2. **Period chart.** SVG scatter: x = angle 0°-45°, y = period p (1 to 16, top clipped with a "16+" band). One dot per pair (w, h) with 1 ≤ h ≤ w ≤ 32 and gcd(w, h) = 1 (reduced ratios only, so each angle appears once). Dots at p = 1 (all 32 slopes from 1 : 1 to 32 : 1) are emphasized, and the five widest-spaced are labelled 45°, 26.57°, 18.43°, 14.04°, 11.31°. A vertical dashed marker at 30° labelled "true isometric". A vertical marker for the current line's angle. Clicking or pressing Enter on a dot loads that ratio into the line grid.
3. **Scale strip.** A 16-pixel invented pattern (alternating two colors, one pixel each) drawn at scale `s`: each art pixel `i` is `floor((i+1)s) − floor(i s)` screen pixels wide. Under it the list of widths and "uniform" or "mixed widths". Presets: 2, 2.5, 3, 4.5 (NES rows on 1080p), 7.5 (Game Boy rows on 1080p).

**Controls.** Angle slider 0°-45° (step 0.01°, default 30). Width slider `w` 4-32 (default 28). The height is `h = round(w × tan(angle))`, clamped to 1…w; the actual angle `atan(h/w)` is shown next to the requested angle. Presets: "1:1", "2:1", "3:1", "5:2", "12:5", "30°". Scale slider 1-8 (step 0.1, default 2.5) with the presets above. All sliders keyboard operable; arrow keys step by the slider step, Page Up/Down by 1° or 1.

**Formulas.** `runs(w, h)[k] = floor((k+1)w/h) − floor(kw/h)` for `k = 0 … h−1`, with integer arithmetic. `p = h / gcd(w, h)`. Line pixels: for run k, columns from `floor(kw/h)` to `floor((k+1)w/h) − 1` in row k (row 0 at the bottom). For `h = 0` (angle near 0) draw a single horizontal run of w.

**Test values.**
- `runs(8, 4) = [2, 2, 2, 2]`, p 1, 26.57°. `runs(10, 4) = [2, 3, 2, 3]`, p 2, 21.80°. `runs(9, 4) = [2, 2, 2, 3]`, p 4. `runs(7, 4) = [1, 2, 2, 2]`, p 4, 29.74°. `runs(12, 5) = [2, 2, 3, 2, 3]`, p 5, 22.62°. `runs(15, 6) = [2, 3, 2, 3, 2, 3]`, p 2. `runs(20, 8)`: period 2.
- Default (w 28, angle 30°): `h = round(28 × 0.5774) = 16`, actual angle 29.74°, `runs(28, 16) = [1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2]`, `p = 16 / gcd(28, 16) = 4`, verdict "wobbly".
- Scale widths: s = 2.5 → 2, 3, 2, 3, …; s = 3 → all 3; s = 4.5 → 4, 5, 4, 5, …; s = 7.5 → 7, 8, 7, 8, ….

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`. Run lengths are always printed as numbers, so nothing depends on color. The chart dots are focusable buttons with aria-labels ("ratio 2 to 1, 26.57 degrees, period 1, clean"). `prefers-reduced-motion`: no transitions. `prefers-color-scheme`: grid and chart use the token colors for both themes. No game art: only grids, lines and an abstract two-color strip.
