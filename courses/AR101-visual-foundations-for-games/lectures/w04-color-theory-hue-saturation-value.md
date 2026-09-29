# AR101 · Week 04 — Color Theory: Hue, Saturation, Value

**Why this matters:** Every color picker you will use hands you three sliders, and one of them is labelled "value." It is not the value you measured in week 1. Artists who trust that slider make palette swaps whose shading collapses, team colors where one side reads darker, and highlights that glow like neon. This week you learn what the three numbers control and how to change one of them without breaking the value structure you planned.

**You will be able to:**
- Convert a color between RGB and HSV by hand and in code, and name what each HSV number controls.
- Predict how changing hue, saturation or HSV value moves a color's lightness L*, using the ceiling rule.
- Compute a value-preserving palette swap: new hue, same L* for every step.
- Critique a scene by separating its hue, saturation and value decisions.

**Before class:** Solarski, *Drawing Basics and Video Game Art* (Watson-Guptill, 2012), the material on color (find it through the table of contents; any printing of the 2012 edition works). Mitchell, Francke and Eng, "Illustrative Rendering in Team Fortress 2" (NPAR 2007), section 4, the paragraphs on color (about one page, free on Valve's site).

**Prerequisites from earlier courses:** AR101 has no prerequisite course. This week builds directly on [AR101 week 1, value before color](w01-seeing-like-an-artist-value-before-color.md): its L* formula and its value-gap rule (ΔV of at least 20) are used unchanged here. Silhouettes from [AR101 week 3](w03-silhouette-readability.md) come back in section 4. Hue is an angle, so the wrap-around arithmetic from [MA101 week 10, angles](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w10-angles-radians-sin-cos.md) applies. The code uses functions as in [CS101 week 4](../../CS101-programming-for-games-i/lectures/w04-functions-and-decomposition.md).

**Interactive:** [`examples/w04-palette-swap-value.html`](../examples/w04-palette-swap-value.html). Keep it open during section 2.

---

## 1. Three numbers for one color

### The screen speaks RGB

Your monitor makes every color from three lights: red, green and blue. Each pixel stores three numbers, usually from 0 to 255, and the screen adds the lights together. `(255, 0, 0)` is full red. `(255, 255, 0)` is red plus green, which your eye reads as yellow. `(255, 255, 255)` is all three at full, which is white. This is **additive** color. Light adds up toward white.

Paint works the other way. Pigments absorb light, so mixing paints moves toward dark mud. The red-yellow-blue wheel from school art classes describes paint. In a game you work with light, so the primaries are red, green and blue, and the complement of red is cyan, not green. Keep that in mind when an old art book tells you red and green are opposites.

RGB is how the machine stores color. It is a poor handle for an artist. If you want "the same green, a bit darker," you have to change all three numbers in the right ratio. So painting programs give you a second set of coordinates.

### HSV: the artist's handle

**HSV** stands for hue, saturation and value. It is the same color redescribed with three numbers that match three questions an artist asks.

- **Hue (H)** answers "which color family?" It is an angle from 0° to 360° around a wheel. Red sits at 0°, yellow at 60°, green at 120°, cyan at 180°, blue at 240°, magenta at 300°, and 360° wraps back to red. Because hue is an angle, 350° and 10° are only 20° apart.
- **Saturation (S)** answers "how intense, how far from gray?" It runs from 0% (a gray) to 100% (as pure as the hue can be at this brightness).
- **HSV value (V)** answers "how strong is the strongest channel?" It runs from 0% (black) to 100% (at least one channel at full).

A close cousin, **HSL**, uses lightness L, the average of the strongest and weakest channel, instead of V. Most tools offer one or both. Everything below applies to HSL's L as well.

### The word "value" now means two things

In week 1 you defined **value** as perceived lightness and measured it with CIE L*, from 0 (black) to 100 (white). The color picker's V is something else. It is the maximum of the three channels, with no weighting for how the eye responds to each. From here on this course keeps them apart:

- **HSV V** means the picker's slider.
- **Value** or **L\*** means perceived lightness, week 1's number. **ΔV** is still week 1's gap between two L* values.

Pure yellow and pure blue both have HSV V = 100%. Their L* are 97.1 and 32.3. Week 1 showed that averaging channels misleads you. This week's point is narrower and more practical: the slider an artist actually drags is also not value, and it fails in a predictable way.

## 2. Worked example: the palette swap that changes more than hue

### The hook

A **palette swap** is one of the oldest tricks in games. You draw a character once, then recolor it to make a variant. The Super Mario series has green and red Koopa Troopas that share one drawing and behave differently, so the color carries a rule the player must learn. On the NES, swaps were nearly free. Each sprite pixel stores an index from 0 to 3 into one of four sprite palettes (index 0 is transparent), so pointing the same tiles at a different palette recolors the sprite without new art.

Try the modern version. Draw a green slime with a four-step ramp and a black outline. In your paint program, rotate the hue by 120° to make a blue slime, keeping S and V as they were. The blue slime looks darker overall, and its shadow side melts into the outline. Rotate by 240° instead and you get a red slime that is darker too, but less so. You changed only hue. Why did the value structure change, and how do you swap hue without breaking it?

### The model

Take a color with channels `R`, `G`, `B` from 0 to 255. Divide each by 255 to get `r`, `g`, `b` between 0 and 1. The conversion to HSV is:

```
hi = max(r, g, b)        lo = min(r, g, b)        C = hi − lo

V = hi                             (as a percent: 100 × hi)
S = C / hi                         (S = 0 when hi = 0)
H = 60 × (((g − b) / C) mod 6)     if hi is r
H = 60 × ((b − r) / C + 2)         if hi is g
H = 60 × ((r − g) / C + 4)         if hi is b
                                   (H = 0 by convention when C = 0)
```

- `hi` and `lo` are the strongest and weakest channel.
- `C` is **chroma**, the spread between them. A gray has `C = 0`.
- `H` says which channel leads and how far the second-strongest channel pulls toward its neighbor on the wheel.

The conversion back, for H in degrees and S, V between 0 and 1, is: `C = V × S`, `X = C × (1 − |(H/60) mod 2 − 1|)`, `m = V − C`; pick `(r, g, b)` by which 60° sector H falls in: `(C, X, 0)` for 0-60°, `(X, C, 0)` for 60-120°, `(0, C, X)` for 120-180°, `(0, X, C)` for 180-240°, `(X, 0, C)` for 240-300°, `(C, 0, X)` for 300-360°; then add `m` to each and multiply by 255.

Now connect HSV to week 1's L*. One rule does it.

**The ceiling rule.** For a fixed HSV V, the gray at that V (S = 0) is the lightest color possible. Raising S pulls the weaker channels down, which can only lower L*. How far below the ceiling a fully saturated color falls depends on its hue, because the eye weights green heavily, red less and blue least (the 0.7152, 0.2126 and 0.0722 of week 1's formula).

```
L*(H, S, V) ≤ L*(gray at V)          equality only when S = 0
L* rises with V for fixed H and S
L* falls with S for fixed H and V
```

So HSV V is a ceiling, and hue and saturation decide how far under it the color sits. That explains the slime. Rotating hue with S and V fixed keeps every step under the same ceiling but moves it to a hue that falls further below it (blue) or less far (yellow). Each step falls by a different amount, so the gaps between steps change too.

The rule also gives the fix. To swap hue and keep value:

1. Compute the original step's L*.
2. At the new hue and the same S, raise or lower V until L* matches. L* rises steadily with V, so a simple search (bisection) finds it.
3. If even V = 100% is too dark, the new hue cannot be that light at that saturation. Keep V = 100% and lower S until L* matches.

### Numbers you can check

First, the ceiling for fully saturated hues at HSV V = 100%. The ceiling (white) is L* = 100.

| Color | RGB | H | L* | Below the ceiling |
|---|---|---|---|---|
| Yellow | 255, 255, 0 | 60° | 97.1 | 2.9 |
| Cyan | 0, 255, 255 | 180° | 91.1 | 8.9 |
| Green | 0, 255, 0 | 120° | 87.7 | 12.3 |
| Magenta | 255, 0, 255 | 300° | 60.3 | 39.7 |
| Red | 255, 0, 0 | 0° | 53.2 | 46.8 |
| Blue | 0, 0, 255 | 240° | 32.3 | 67.7 |

Every row has the same HSV V. L* runs from 32.3 to 97.1. A fully saturated blue can never be lighter than 32.3, whatever you do to the V slider.

Now the slime. The ramp is four steps at `H = 120°`: `(S, V)` of `(70, 25)`, `(65, 50)`, `(60, 75)` and `(35, 95)`, with a black outline (L* 0). Rotate the hue and keep S and V:

| Step | Green slime (H 120°) | Blue swap (H 240°) | Red swap (H 0°) |
|---|---|---|---|
| Dark | 134013, L* 23.2 | 131340, L* 8.8 | 401313, L* 13.2 |
| Shadow | 2D802D, L* 47.2 | 2D2D80, L* 23.6 | 802D2D, L* 31.0 |
| Base | 4DBF4D, L* 69.0 | 4D4DBF, L* 39.0 | BF4D4D, L* 48.2 |
| Light | 9DF29D, L* 88.5 | 9D9DF2, L* 67.8 | F29D9D, L* 73.2 |

Read it with week 1's rule. The green slime's dark step sits 23.2 above the black outline, which reads. The blue swap's dark step sits 8.8 above it, under 10, so it merges: that is the shadow melting into the outline. Every step of the blue slime is 14 to 30 points darker than the matching green step, so on the same forest floor it becomes a different gameplay object, harder to spot.

Check one cell by hand. The blue swap's base step is `H = 240°, S = 60%, V = 75%`. `C = 0.75 × 0.6 = 0.45`. `(H/60) mod 2 = 0`, so `X = 0.45 × (1 − 1) = 0`. Sector 240-300° gives `(X, 0, C) = (0, 0, 0.45)`. Add `m = 0.30`: `(0.30, 0.30, 0.75)`, times 255 is `(77, 77, 191)`, which is `4D4DBF`. Week 1's formula gives L* 39.0.

Finally, the value-preserving swap, found with the three-step procedure:

| Step | Target L* | Blue: S, V | Blue hex | Red: S, V | Red hex |
|---|---|---|---|---|---|
| Dark | 23.2 | 70%, 53.5% | 292989 | 70%, 39.9% | 661F1F |
| Shadow | 47.2 | 65%, 99.2% | 5959FD | 65%, 76.7% | C44444 |
| Base | 69.0 | 37.8%, 100% | 9F9FFF | 48.4%, 100% | FF8484 |
| Light | 88.5 | 13.9%, 100% | DCDCFF | 16.7%, 100% | FFD5D5 |

Every step now has the green slime's value, within half a point, so the shading and the outline gap survive. Notice what it cost. The blue slime's base and light steps hit the ceiling at V = 100% and had to give up saturation, down to 37.8% and 13.9%. A light blue cannot be a saturated blue. The red slime has the same problem, less severely. This is not a flaw in the method. It is the ceiling rule telling you what the color space allows.

### The same thing in code

```python
import colorsys

def lightness(r, g, b):
    """CIE L* of an sRGB color, exactly as in week 1."""
    def lin(c):
        c = c / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    y = 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)
    return 116 * y ** (1 / 3) - 16 if y > 216 / 24389 else 24389 / 27 * y

def hsv_to_rgb(h, s, v):
    """Hue in degrees, S and V in percent -> 0-255 channels."""
    rgb = colorsys.hsv_to_rgb((h % 360) / 360, s / 100, v / 100)
    return tuple(int(c * 255 + 0.5) for c in rgb)

slime = [(120, 70, 25), (120, 65, 50), (120, 60, 75), (120, 35, 95)]
for shift in (0, 120, 240):
    row = []
    for h, s, v in slime:
        r, g, b = hsv_to_rgb(h + shift, s, v)
        row.append(f"{r:02X}{g:02X}{b:02X} {lightness(r, g, b):4.1f}")
    print(f"H+{shift:<3}", " | ".join(row))
```

Run with `.venv/bin/python`, it prints the naive swap table:

```
H+0   134013 23.2 | 2D802D 47.2 | 4DBF4D 69.0 | 9DF29D 88.5
H+120 131340  8.8 | 2D2D80 23.6 | 4D4DBF 39.0 | 9D9DF2 67.8
H+240 401313 13.2 | 802D2D 31.0 | BF4D4D 48.2 | F29D9D 73.2
```

Python's `colorsys` takes hue as a fraction of a full turn, which is why the code divides by 360. Lab 04 has you write the conversions yourself and add the matching search.

### A visual you can move

Open [`examples/w04-palette-swap-value.html`](../examples/w04-palette-swap-value.html). It shows an invented slime, a rounded blob with a black outline, drawn twice: the original on the left and the swap on the right. Under each is its ramp and a grayscale version built from L*.

Drag the hue-rotation slider. In naive mode the right slime changes color and its grayscale strip jumps around. It gets darker through blue and violet, nearly unchanged near yellow-green. Flip the switch to "keep value." Now the grayscale strips stay identical whatever hue you pick, and the S and V readouts show where the method had to trade saturation for lightness. A small chart plots L* against hue for each step at its original S and V, with the ceiling drawn as a dashed line, so you can see the dip at blue that causes all this.

### Cross-game recognition

Each of these changes one HSV number on purpose and relies on the others to hold the structure.

**NES hardware palettes (Nintendo, 1983 onward).** The NES stored four sprite palettes of four entries each, entry 0 transparent, drawn from a 64-color master list. Swapping a palette is a hue change, and artists of the era had to pick the replacement colors by hand from the master list so the swapped sprite kept its dark-mid-light order. The procedure above is that manual choice, written as a search.

**PICO-8's `pal()` (Lexaloffle, current manual 0.2.7).** PICO-8's `pal(c0, c1)` swaps color index c0 for c1 when drawing. Because the palette is fixed at 16 colors, you cannot solve for an exact V. You pick the palette entry whose L* is closest to the one you are replacing. For example, the nearest in value to PICO-8 red `FF004D` (L* 53.8) is indigo `83769C` (L* 52.0), 1.8 apart, with dark green `008751` (L* 49.4) next at 4.4. Swapping red for blue `29ADFF` (L* 67.7) would move that part of the sprite 13.9 lighter.

**Team Fortress 2 (Valve, 2007).** The game has two teams, red and blue, and nine classes. Valve's rendering paper says the class silhouettes were designed to be distinct even with no interior shading, so shape carries class and color is left free to carry team. The paper also describes the red and blue color schemes as corresponding to each other, guided by one reference swatch, with muted colors dominating. The ceiling table shows why that correspondence has to be designed: a pure red and a pure blue differ by 20.9 in L*, so a naive swap would make one team read darker on the same map.

**Mirror's Edge (DICE, 2008).** When the player character takes damage, the game desaturates the screen. That is a saturation-only change. By the ceiling rule, lowering S at fixed V moves every color toward the gray at its ceiling, so the frame gets slightly lighter and loses hue, but the value order of the scene survives. Players can still run while the screen tells them they are hurt.

One principle covers all four cases. Hue and saturation can carry meaning (team, variant, health), but only if value is held steady underneath.

### Eyes-open design judgment

- **Swap in value first.** When you make a variant, decide whether it should read the same (same enemy, different element) or differently (elite, boss). If the same, match L* per step. If different, change value on purpose, not by accident of hue.
- **Accept the ceiling.** Light, saturated blues and violets do not exist. If a variant must be blue and light, it will be pale. If it must be saturated blue, it will be dark. Choose which, or pick a different hue for that variant.
- **Do not trust the V or L slider for readability.** Keep a grayscale preview built on lightness (week 1) open while you place gameplay colors.
- **Matching L* is necessary, not sufficient.** Two colors of equal value can still differ in how much they draw the eye (saturation, section 3) and in how they look against neighbors (section 4). Check the swap in context.

### Check yourself (worked example)

1. Convert `(51, 102, 153)` to HSV. Use week 1's formula (or code) to get its L*.
2. An ice variant of an enemy rotates a skin tone at `H = 20°, S = 50%, V = 80%` to `H = 200°`. Using the ceiling table, will the swapped color be lighter or darker than the original if you keep S and V? Why?

<details>
<summary>Answers</summary>

1. `hi = 0.6`, `lo = 0.2`, `C = 0.4`. V = 60%, S = 0.4/0.6 = 66.7%. Blue leads, so `H = 60 × ((0.2 − 0.4)/0.4 + 4) = 60 × 3.5 = 210°`. L* = 42.0.
2. Lighter. At 20° the color is red-orange, which sits far under its ceiling (red is 46.8 below). At 200° it is a sky blue near cyan, which sits much closer (cyan is 8.9 below). Same ceiling, smaller drop, so the swap is lighter: `(204, 136, 102)` at L* 62.8 becomes `(102, 170, 204)` at L* 66.5. Here the change is small because S is only 50%. At higher S it would grow.

</details>

## 3. Saturation as a spotlight

Saturation draws the eye, but only relative to its surroundings. A saturated red in a room of saturated colors is one voice in a crowd. The same red in a gray room is a shout. Designers treat saturation as a budget.

A useful way to plan it is **area times saturation**. The more screen area a hue covers, the lower its saturation should be, unless that area is what you want the player to look at. Backgrounds, floors and skies cover most of the frame and usually sit low in S. Characters, pickups, interactables and hazards cover little area and get high S. Valve's Team Fortress 2 paper describes this pattern for its environments: muted colors dominate and small areas of saturation give visual interest. Mirror's Edge pushes it further, with mostly white rooftops and a bold red that its Runner Vision system puts on the objects along the player's path.

Saturation can also carry state, a job it rarely has in illustration. A desaturated screen reads as "something is wrong," "this is the past" or "this object is inactive." Greyed-out UI buttons use the same signal. For it to work, the normal state needs enough saturation to lose.

Three rules follow.

- **Reserve the highest saturation for gameplay objects.** If the grass is as saturated as the health potion, the potion stops standing out.
- **Keep large, light areas low in saturation.** A big field of saturated, light color is tiring to look at and flattens depth. By the ceiling rule it is also only possible for yellows, greens and cyans. Pull S down as HSV V goes up in large areas. Next week turns this into a ramp rule.
- **Desaturation is not darkening.** Lowering S moves a color toward the gray at its ceiling, which is lighter, not darker. Use desaturation for "inactive" or "far away." Use value for "in shadow."

## 4. Context changes the color

The same RGB numbers do not always look the same. Josef Albers built a course around this in *Interaction of Color* (1963). His exercises make one gray look like two different grays by placing it on two different grounds, and make two different colors look alike by choosing their surroundings. The effect is called **simultaneous contrast**: a color looks lighter on a dark ground, darker on a light ground, and shifts slightly toward the complement of what surrounds it. Week 1 listed this as one of the limits of the L* model. Here is what it means in production.

First, a UI color you tested on a blank white canvas may look different over your game scene. Test HUD and signal colors on screenshots of the busiest and brightest scenes in the game.

Second, two colors with a ΔV of 15 may look well separated where they touch, because contrast at the edge exaggerates the difference, and merge when they sit apart on a noisy background. Use L* to find candidates for trouble, then look at the pixels in place.

Third, you can use the effect. A rim of the opposite value around a silhouette (week 3) makes the edge pop without changing the character's own colors. Valve's paper says Team Fortress 2 emphasizes silhouettes with rim highlights rather than dark outlines, which is this idea built into the lighting.

## 5. Warm and cool

Artists also sort hues by **temperature**. Warm hues run roughly from red through orange to yellow (about 0° to 70°, plus the magenta-reds near 330° to 360°). Cool hues run from green-cyan through blue to violet (about 150° to 270°). Greens and purples sit on the boundary and can lean either way.

Temperature is a convention, not a measurement of the pixel, and a strong one. Warm hues tend to read as near, active and inviting. Cool hues tend to read as far, calm or cold. Landscape painters use this for depth: far mountains go cooler, lighter and less saturated.

Notice how temperature lines up with the ceiling table. The warm hue yellow sits close to its ceiling, and the cool hue blue sits far under it. So at the same HSV V, a cool color is usually darker than a warm one. Painters' habit of "cool shadows, warm light" works with the color space instead of against it. Valve's paper lists the same rule for Team Fortress 2: shading follows a warm-to-cool shift, and shadows go to cool colors, not to black. Next week turns that sentence into a formula for building ramps.

## In-class activity (25 minutes)

Pairs. You need a laptop with an image editor that has an HSV picker, and the week's interactive.

1. **Draw (5 min).** On a 32 × 32 canvas, draw an invented creature with a four-step ramp in any hue and a black outline. Record each step's HSV and L* (use the interactive's readout).
2. **Naive swap (5 min).** Make two variants by rotating hue 120° and 240°, keeping S and V. Record the new L* values and mark every step whose ΔV to its neighbor, or to the outline, falls under 10.
3. **Value-preserving swap (10 min).** Rebuild both variants so each step matches the original L* within 2. Use the interactive's "keep value" mode to find S and V, then enter them in your editor. Note which steps had to lose saturation.
4. **Compare (5 min).** Put all three creatures on the same mid-gray and the same dark background. Swap laptops with another pair. They say which variant their eye finds first and whether the three read as the same creature.

Expected output: one PNG with the three creatures on both backgrounds, and a table with hue, S, V and L* for every step of all three.

## Common misconceptions

- **"Same HSV V means same brightness."** V is the strongest channel. Pure yellow and pure blue share V = 100% and differ by 64.8 in L*.
- **"Desaturating a color darkens it."** Lowering S moves the color toward the gray at its ceiling, which is lighter. A saturated blue at V = 100% goes from L* 32.3 to 100 as S goes to 0.
- **"Red and green are complements."** On the paint wheel, yes. On a screen, red's complement is cyan (180° away) and green's is magenta.
- **"A hue shift is a safe recolor."** It changes value unless you correct it, and by different amounts on each step of a ramp, which breaks the shading.

## Check yourself

1. Explain, using the ceiling rule, why a light, saturated violet (H = 270°, S = 90%) is impossible, and say what you would change to get a light violet.
2. You swap a player's gold cape (`FFD700`, H = 50.6°, S = V = 100%, L* 86.9) to magenta (H = 300°) for a second player, keeping S and V. Using the ceiling table, will the magenta cape be lighter or darker, and by roughly how much?
3. A designer wants the red and blue team versions of a character's shirt to share L* 45. At S = 80%, can the red one reach it by adjusting V? Can the blue one? (Hint: the blue at S = 80%, V = 100% is `(51, 51, 255)`.)
4. Why does a screen-wide desaturation keep the value order of a scene but make it slightly lighter? Use the ceiling rule.

<details>
<summary>Answers</summary>

1. At H = 270° the strongest channel is blue, and red is the second channel; green is the weakest. With S = 90% the green channel sits at 10% of V, so most of the eye's most-weighted channel is missing, and L* stays far under the ceiling. Even at V = 100% the color is `(140, 25, 255)` with L* 43.5. To get a light violet, lower S (mix green back in) and accept a paler color, which is what the value-preserving procedure does.
2. Darker, by a lot. At full S and V, magenta is `FF00FF` with L* 60.3, from the table. The gold starts at 86.9, so the drop is 26.6. (Pure yellow to magenta would drop 36.8; the gold drops less because it already leans toward orange and sits further under its ceiling.) Either way, the second player's cape would read as a different value, well past week 1's 20-point threshold.
3. Red: at S = 80%, V = 100% the color is `(255, 51, 51)` with L* 56.0, above 45, so lowering V finds 45 (at about V = 79.8%). Blue: `(51, 51, 255)` has L* 38.4, below 45 even at V = 100%, so it cannot reach 45 at S = 80%. Keep V = 100% and lower S until L* reaches 45 (at about S = 68.8%).
4. Every color moves toward the gray at its own ceiling. Colors that were far under their ceiling (saturated blues and reds) rise the most, and colors near it barely move. No color passes a color that was lighter and had the same or higher V, so the order mostly holds, while the whole frame drifts lighter and loses hue.

</details>

## Lab / assignment hook

[Lab 04, the palette swapper](../labs/lab04.md). You write `rgb_to_hsv`, `hsv_to_rgb` and a `match_value` search, test them against this lecture's tables, and then produce value-preserving variants of an invented creature palette. Deliverable: passing tests, two variant palettes as `.hex` files, a lineup image, and a 300-word note on which steps had to give up saturation and why.

## Sources

- Wikipedia, "Glossary of video game terms," entry "Palette swap" (retrieved September 2026). Definition; green and red Koopa Troopas in the Super Mario series as palette swaps with different behaviors.
- NESdev Wiki, "PPU palettes" (retrieved September 2026). Four sprite palettes of four entries each, entry 0 transparent, 6-bit indices into 64 master colors.
- Lexaloffle, PICO-8 User Manual (version 0.2.7). Fixed 16-color palette; `pal(c0, c1, [p])` swaps colors in the draw palette. Hex values from Lospec, "PICO-8" palette page (retrieved September 2026).
- Mitchell, J., Francke, M. & Eng, D. (2007). "Illustrative Rendering in Team Fortress 2." NPAR 2007, Valve. Red and blue team color schemes chosen to correspond, muted colors dominating with small saturated areas, rim highlights instead of dark outlines, warm-to-cool shading with cool shadows.
- Wikipedia, "Mirror's Edge" (retrieved September 2026). DICE, November 2008 on consoles; Runner Vision turns path objects red; white-dominated environments; colors desaturate as the player takes damage.
- Albers, J. (1963). *Interaction of Color*. Yale University Press. Simultaneous contrast and the relativity of color.
- Smith, A. R. (1978). "Color Gamut Transform Pairs." SIGGRAPH '78. The original description of the HSV model.
- CIE lightness L* and WCAG relative luminance as defined in AR101 week 1 (CIE 15:2004; W3C WCAG 2.1).

## Interactive spec: examples/w04-palette-swap-value.html

**Purpose.** Show that rotating hue with S and V fixed changes a sprite's value structure, and that solving V (then S) per step preserves it at a visible cost in saturation.

**The one insight the visual must make obvious.** On first load, with a rotation of 120° in naive mode, the right-hand slime is visibly darker and its grayscale strip shows its darkest step merging with the black outline (highlighted), while the left slime's strip has four clear steps. One click on "keep value" makes the two grayscale strips identical.

**Layout.** Mobile: stacked. Desktop (900px and up): two slimes side by side on top, chart below, controls in a sidebar.

**Views.**
1. Two invented slimes (SVG): a rounded blob about 160 × 120 px with a 3 px black outline, filled in four bands (dark at the bottom right, light at the upper left, as a simple light from the upper left) plus two small black eye dots. Left uses the original ramp, right the swapped ramp. No game characters.
2. Under each slime: four swatches with hex, H, S, V and L* (one decimal), and a grayscale strip where each swatch shows the neutral gray of equal L* (convert L* back to Y, then to sRGB, as in the week 1 spec). Any neighbor pair, or the dark step against the outline (L* 0), with ΔV < 10 gets a red dashed border and the label "merges".
3. Chart: x = hue 0°-360° (ticks every 60°), y = L* 0-100. For each of the four steps, a line of L*(H, S_i, V_i) as H varies, in the step's original color (with a text label for each line). A dashed line per step at its ceiling `L*(gray at V_i)`. A vertical marker at the current swapped hue. In "keep value" mode, add dots at each step's target L* on the marker.

**Controls.** Hue rotation (0-359°, step 1, default 120). Mode toggle: "naive" / "keep value" (default naive). Base ramp editor: four rows of H, S, V numeric inputs (default `(120, 70, 25)`, `(120, 65, 50)`, `(120, 60, 75)`, `(120, 35, 95)`), and a "reset to lecture" button. Background toggle: mid-gray `(128,128,128)` / dark `(40,40,40)` / light `(220,220,220)` behind both slimes.

**Formulas.** HSV to RGB as in lecture section 2, rounding each channel with `floor(x × 255 + 0.5)`. L* exactly as week 1: sRGB linearization, `Y = 0.2126R + 0.7152G + 0.0722B` (linear), `L* = 116 Y^(1/3) − 16` if `Y > 216/24389` else `(24389/27) Y`. Keep-value search per step: target `T = L*(original)`; new hue `H' = (H + rotation) mod 360`; if `L*(H', S, 100) ≥ T`, bisect V in [0, 100] (40 iterations) for the smallest V with `L* ≥ T`; else set V = 100 and bisect S in [0, S] for the largest S with `L* ≥ T`.

**Test values.**
- Naive, rotation 120: `131340` 8.8, `2D2D80` 23.6, `4D4DBF` 39.0, `9D9DF2` 67.8 (dark step flagged "merges" against the outline).
- Naive, rotation 240: `401313` 13.2, `802D2D` 31.0, `BF4D4D` 48.2, `F29D9D` 73.2.
- Keep value, rotation 120: `292989` (S 70, V 53.5), `5959FD` (65, 99.2), `9F9FFF` (37.8, 100), `DCDCFF` (13.9, 100); L* within 0.3 of 23.2, 47.2, 69.0, 88.5.
- Keep value, rotation 240: `661F1F`, `C44444`, `FF8484`, `FFD5D5`.
- Ceiling table at S = 100, V = 100: yellow 97.1, cyan 91.1, green 87.7, magenta 60.3, red 53.2, blue 32.3.
- `(51, 102, 153)` → H 210, S 66.7, V 60, L* 42.0.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`. Native labelled inputs with live numeric outputs; every swatch carries text labels so the page works without color perception. The chart has an aria-label describing the lowest point (blue) and highest (yellow) for the current ramp. `prefers-reduced-motion`: no transitions. `prefers-color-scheme` applies to page chrome only; slimes, swatches and chart lines keep their true colors on a neutral card.
