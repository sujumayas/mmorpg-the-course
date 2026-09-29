# AR101 · Week 05 — Palettes and Color Harmony

**Why this matters:** A game's palette is a promise. Once the grass, the stone and the enemies share a small set of related colors, a new asset either fits in or sticks out, and players read "sticks out" as "important." This week you learn to build palettes on purpose: ramps that shade without going muddy, and hue relationships you can name, measure and defend in a review.

**You will be able to:**
- Build a color ramp from three lerps (hue, saturation, value) and compute its colors and lightness (L*) step by step.
- Explain, with numbers, why a hue-shifted ramp reads with more depth than a ramp that only changes HSV V.
- Place hues for a palette with the standard harmony schemes, and compute the angles for any base hue.
- Design and critique a limited game palette, including a reserved hue for gameplay signals.

**Before class:** Solarski, *Drawing Basics and Video Game Art* (Watson-Guptill, 2012), the material on color, focusing on palettes and color relationships (find it through the table of contents). Mitchell, Francke and Eng, "Illustrative Rendering in Team Fortress 2" (NPAR 2007), section 3 (half a page) and the paragraph on team colors in section 4. Browse the Lospec palette list for ten minutes and pick one palette under 16 colors you like; bring its hex values.

**Prerequisites from earlier courses:** [AR101 week 4, hue, saturation and value](w04-color-theory-hue-saturation-value.md) (HSV, the ceiling rule, and why HSV V is not value). [MA101 week 8, lerp and remap](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w08-interpolation-lerp-inverse-lerp-remap.md): every ramp in this lecture is built from `lerp`. [MA101 week 10, angles](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w10-angles-radians-sin-cos.md) for wrap-around on the hue wheel. [AR101 week 1, value before color](w01-seeing-like-an-artist-value-before-color.md) for L* and the value gap ΔV.

**Interactive:** [`examples/w05-hue-shift-ramp.html`](../examples/w05-hue-shift-ramp.html). Keep it open during section 2.

---

## 1. What a palette is

A **palette** is the fixed list of colors an image, an asset set or a whole game is allowed to use. On old hardware the list was forced on artists. The NES could put 4 colors, one of them transparent, in each sprite palette, and it held 4 sprite palettes at a time, all drawn from a master set of 64. The original Game Boy had 4 shades. Modern hardware can show millions of colors, and many teams limit themselves anyway, because a short list makes everything look like it belongs together.

A palette is not a random handful of colors. Look at any good one and you will find the same structure:

- **Ramps.** A **ramp** is an ordered run of colors from dark to light that belong to one material or family: skin, grass, stone, metal. A ramp is how you shade. Each step is one "shade" on a sprite or one band of light on a surface.
- **Neutrals.** A few low-saturation colors for shadows, outlines, UI panels and distant background.
- **Accents.** One or two saturated colors that appear in small areas. Often one of them is **reserved**: it only ever appears on a gameplay signal, such as a hazard, a loot drop or an interactable.

So a 16-color palette is often something like four ramps of three or four steps, plus a couple of neutrals and an accent, with some colors shared between ramps. The rest of the lecture is about building the ramps (section 2) and choosing their hues (section 3).

## 2. Worked example: shadows go cool, not black

### The hook

When Valve described the look of Team Fortress 2 in 2007, they listed two rules they had taken from the commercial illustrators who inspired the game. First, shading follows a warm-to-cool hue shift, and shadows go to cool colors, not to black. Second, saturation increases at the **terminator**, the band where a surface turns from lit to shadowed.

Now try the obvious way to shade a green object in any paint program. Pick a mid green, then make darker and lighter versions by dragging only the HSV V slider. The result looks flat, like colored plastic, and the lightest step glows like a highlighter pen. Artists call this a **straight ramp** and call its dark end muddy. Something in Valve's two rules fixes it. The question is what, and by how much.

### The model

A ramp of `n` steps is three lerps. For step `i` from 0 (darkest) to `n − 1` (lightest), let `t = i / (n − 1)`. Then:

```
V_i = lerp(V_dark, V_light, t)
H_i = lerp_hue(H_shadow, H_light, t)
S_i = S_mid − (S_mid − S_end) × |2t − 1|

lerp(a, b, t)     = a + (b − a) × t
lerp_hue(a, b, t) = a + d × t,  where d = ((b − a + 180) mod 360) − 180
```

- `V_dark` and `V_light` are the HSV V of the darkest and lightest step.
- `H_shadow` and `H_light` are the hues at the two ends. `lerp_hue` travels the short way around the wheel, so a ramp from 350° to 30° passes through 0°, not through 180°. The result is taken mod 360.
- `S_mid` is the saturation at the middle step. `S_end` is the saturation at both ends. The `|2t − 1|` term is 1 at the ends and 0 in the middle, so saturation peaks in the midtones. That is Valve's second rule.

A **straight ramp** is the special case `H_shadow = H_light` and `S_mid = S_end`. A **hue-shifted ramp** moves `H_shadow` toward blue (240°) and `H_light` toward yellow (60°). That is Valve's first rule, "shadows go cool," plus its partner, "light goes warm." Blue and yellow are used as the targets because, in week 4's ceiling table, yellow sits closest under its ceiling and blue furthest: moving toward yellow raises L* a little for free, and moving toward blue lowers it.

Start with 15° to 40° of shift at each end and tune by eye. There is no correct number. The interactive lets you see what each choice does.

### Numbers you can check

Take a grass ramp with five steps, from `V_dark = 20%` to `V_light = 90%`. So `t` is 0, 0.25, 0.5, 0.75, 1 and V is 20, 37.5, 55, 72.5, 90.

The **straight** ramp keeps `H = 120°` and `S = 60%`. The **shifted** ramp uses `H_shadow = 160°` (40° toward blue) and `H_light = 80°` (40° toward yellow), with `S_mid = 70%` and `S_end = 45%`.

| Step | t | V | Straight H, S | Straight hex | Straight L* | Shifted H, S | Shifted hex | Shifted L* |
|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 20% | 120°, 60% | 143314 | 18.2 | 160°, 45% | 1C332B | 19.2 |
| 1 | 0.25 | 37.5% | 120°, 60% | 266026 | 35.8 | 140°, 57.5% | 29603B | 36.3 |
| 2 | 0.5 | 55% | 120°, 60% | 388C38 | 51.7 | 120°, 70% | 2A8C2A | 51.2 |
| 3 | 0.75 | 72.5% | 120°, 60% | 4AB94A | 67.0 | 100°, 57.5% | 72B94F | 68.6 |
| 4 | 1 | 90% | 120°, 60% | 5CE65C | 81.6 | 80°, 45% | C3E67E | 86.9 |

Check step 3 of the shifted ramp by hand with the HSV-to-RGB rule from week 4, section 2. `C = V × S = 0.725 × 0.575 = 0.417`. `H/60 = 1.667`, so `X = C × (1 − |1.667 mod 2 − 1|) = 0.417 × 0.333 = 0.139`. Hue is between 60° and 120°, so `(r, g, b) = (X, C, 0)`. Add `m = V − C = 0.308` and multiply by 255: `(0.447, 0.725, 0.308) × 255 = (114, 185, 79)`, which is `72B94F`. Week 1's formula gives L* 68.6.

Three things stand out.

1. **Same value staircase, plus hue.** Both ramps use exactly the same HSV V at every step, and their L* columns stay within 1.6 of each other except at the top, where the shifted highlight gains 5.3 (86.9 against 81.6) because it moved toward yellow. So the shift keeps the value structure you planned in week 1 and adds a second kind of separation on top. Week 4 warned that a hue change moves value; here the moves are small because the shift is spread across the ramp and the ends also lose saturation, which lifts them toward their ceiling.
2. **The highlight stops glowing.** The straight ramp's top step `5CE65C` keeps 60% saturation at 90% V, a large area of saturated light color, which week 4 warned against. The shifted top step `C3E67E` has lower S and a warm lean, so it reads as sunlight on grass.
3. **Neighbors differ in two ways.** In the straight ramp, each step differs from the next only in value. In the shifted ramp, each step also differs in hue. On a sprite that means the bands of shading separate more clearly at the same step count, which matters when you only have 3 or 4 steps.

One honest caveat. Neither staircase is perfectly even. The straight ramp's steps are 17.6, 15.9, 15.3 and 14.6, the shifted ramp's 17.1, 14.9, 17.4 and 18.3. If you need an even staircase, adjust V per step until the L* steps match. Lab 05's `even_ramp` does that.

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

def lerp(a, b, t):
    return a + (b - a) * t

def lerp_hue(a, b, t):
    """Move from hue a toward hue b the short way around the wheel."""
    d = (b - a + 180) % 360 - 180
    return (a + d * t) % 360

def ramp(h_shadow, h_light, s_mid, s_end, v_dark, v_light, n):
    colors = []
    for i in range(n):
        t = i / (n - 1)
        h = lerp_hue(h_shadow, h_light, t)
        s = s_mid - (s_mid - s_end) * abs(2 * t - 1)
        v = lerp(v_dark, v_light, t)
        rgb = colorsys.hsv_to_rgb(h / 360, s / 100, v / 100)
        r, g, b = (int(c * 255 + 0.5) for c in rgb)
        colors.append((f"{r:02X}{g:02X}{b:02X}", lightness(r, g, b)))
    return colors

for label, args in [("straight", (120, 120, 60, 60, 20, 90, 5)),
                    ("shifted ", (160, 80, 70, 45, 20, 90, 5))]:
    print(label, "  ".join(f"{hx} {l:4.1f}" for hx, l in ramp(*args)))
```

With `.venv/bin/python` it prints:

```
straight 143314 18.2  266026 35.8  388C38 51.7  4AB94A 67.0  5CE65C 81.6
shifted  1C332B 19.2  29603B 36.3  2A8C2A 51.2  72B94F 68.6  C3E67E 86.9
```

`colorsys.hsv_to_rgb` takes hue as a fraction of a full turn, which is why the code divides by 360.

### A visual you can move

Open [`examples/w05-hue-shift-ramp.html`](../examples/w05-hue-shift-ramp.html). It draws a simple invented shape, a ball on a ledge, shaded in bands from each ramp, straight on the left and shifted on the right. Under each ball sits its ramp as swatches and as a grayscale strip. A hue wheel shows the shifted ramp as dots joined by an arc, so you can see the ramp bend from cyan-green through green to yellow-green.

Drag the shift slider from 0° to 60°. At 0° both ramps have one hue, and the only difference left is saturation: the right ramp peaks at 70% in the midtones and drops to 45% at the ends, while the left keeps 60% throughout. As you raise the shift, the right ball starts to look lit by warm light, while its grayscale strip barely changes. Hue is doing new work without undoing the value plan. Push past about 60° and the ramp stops reading as one material: the highlight turns yellow and the shadow turns teal. That upper limit is the design judgment the formula cannot make for you.

### Cross-game recognition

Rewrite each case as "which way does hue move as L* rises?"

**Team Fortress 2 (Valve, 2007).** The rendering paper implements its shading rule with a lookup texture that has, in the paper's description, a grayscale part, a cool part for the shadowed side and a small reddish band at the terminator. Rewritten as a ramp: `H_shadow` is cool, the middle has the highest saturation and a warm lean, and the lit side is near neutral. The paper also credits an older idea, Gooch shading from technical illustration (1998), which uses a cool-to-warm shift to show surface orientation.

**PICO-8's greens (Lexaloffle, fixed palette).** Sort PICO-8's green-family colors by L* and read off the hue: dark green `008751` has H = 156° and L* 49.4; green `00E436` has H = 134° and L* 79.5; yellow `FFEC27` has H = 55° and L* 92.3. As L* rises, hue moves from the cyan side of green toward yellow. The palette gives you a hue-shifted grass ramp for free, and it would not with a straight one.

**DawnBringer 16 (a widely used community palette on Lospec).** Its greens do the same: `346524` at H = 105° and L* 38.1, `6DAA2C` at H = 89° and L* 63.5, then `DAD45E` at H = 57° and L* 83.3. A different author, a different palette, the same direction of travel.

Three sources follow one rule. As a ramp gets lighter, its hue moves toward yellow; as it gets darker, toward blue. And saturation is highest in the middle, not at the ends.

### Eyes-open design judgment

- **Hue shifting is a style, not a law.** It suggests warm light and cool ambient shadow, which suits daylight outdoors. A cave lit by green crystals should shift its highlights toward green, not yellow. Decide what the light source is, then shift toward it.
- **Shared ends make a palette cohere.** If every ramp's darkest step leans toward the same cool hue, shadows across different materials look like they are in the same world. Many limited palettes reuse one or two dark colors as the bottom of several ramps. Plan this, and it saves slots.
- **Too much shift breaks the material.** Past a certain angle the ends of the ramp read as different materials. Check each ramp on an actual sprite, not only as swatches.
- **Watch the value steps.** Hue shifting changes L* (week 4). Always recheck the grayscale strip, because shading needs clear value steps first and pleasant hue second.

### Check yourself (worked example)

1. Compute `lerp_hue(350, 30, 0.5)` and `lerp_hue(200, 60, 0.5)`. Which way around the wheel does each go?
2. A four-step skin ramp uses `H_shadow = 350°`, `H_light = 40°`, `S_mid = 80%`, `S_end = 55%`, `V_dark = 25%`, `V_light = 95%`. What are H, S and V at step 2 (`t = 2/3`)?

<details>
<summary>Answers</summary>

1. For 350 to 30: `d = ((30 − 350 + 180) mod 360) − 180 = (−140 mod 360) − 180 = 220 − 180 = 40`, so the result is `350 + 20 = 370 mod 360 = 10°`, passing through red. For 200 to 60: `d = (40 mod 360) − 180 = −140`, so the result is `200 − 70 = 130°`, going down through green rather than up through magenta.
2. `d = 50`, so `H = 350 + 50 × 2/3 = 383.3 mod 360 = 23.3°`. `|2t − 1| = 1/3`, so `S = 80 − 25/3 = 71.7%`. `V = 25 + 70 × 2/3 = 71.7%`. The color is `B76734`, L* 51.9.

</details>

## 3. Harmony: choosing the hues

Ramps decide how one family shades. **Harmony schemes** decide which families sit together. They are named patterns of angles on the hue wheel. With a base hue `H`, the classic schemes are:

| Scheme | Hues | Example with H = 20° (orange-red) |
|---|---|---|
| Monochromatic | H only, varied in S and V | 20° |
| Analogous | H − 30°, H, H + 30° | 350°, 20°, 50° |
| Complementary | H, H + 180° | 20°, 200° |
| Split-complementary | H, H + 150°, H + 210° | 20°, 170°, 230° |
| Triadic | H, H + 120°, H + 240° | 20°, 140°, 260° |
| Tetradic (square) | H, H + 90°, H + 180°, H + 270° | 20°, 110°, 200°, 290° |

All angles are mod 360. These are the angles on the RGB/HSV wheel you use on screen. Traditional painting books draw the same schemes on the red-yellow-blue paint wheel, where the complement of red is green. On a screen it is cyan. If a reference and your color picker disagree, that is usually why.

What do the schemes do? Each one sets how much **hue contrast** the palette has.

- **Analogous** palettes have little hue contrast. They feel calm and unified. The risk is that nothing stands out, so readability must come from value and saturation.
- **Complementary** palettes have the most hue contrast between two families. They are the natural choice for two opposing sides. Team Fortress 2's red team base uses warm colors and its blue team base uses cool colors, according to Valve's paper, which puts the two teams on opposite halves of the wheel.
- **Split-complementary** and **triadic** give a main family and two supporting ones. They suit a world with several zones or factions that must feel distinct but related.

A harmony scheme picks base hues only. Each hue then becomes a ramp from section 2, and its shadow and light ends drift toward blue and yellow. So a real palette's hues spread out around each scheme angle. That is fine. The scheme is a starting skeleton.

### Hue budget for gameplay

A game palette has a job illustration does not. It must keep signals readable. Two rules help.

1. **Reserve a hue.** Choose one hue that appears only on the thing players must never miss. Mirror's Edge (DICE, 2008) uses bold red for the objects its Runner Vision highlights, on a world that is mostly white, and that red reads as "go here" because the rest of the frame gives it no competition. Once a hue is reserved, never use it for decoration, or it stops meaning anything.
2. **Keep the reserved hue away from the base scheme.** If your world is analogous around green (90° to 150°), a reserved hue near the complement (around 300°, magenta) stands out on hue. Then check its value against the backgrounds it will appear on, with week 1's ΔV check, because hue alone fails for some players (week 12).

### How many colors?

Fewer colors force decisions. With 16 colors and, say, four ramps, each ramp gets three or four steps. That is enough for a shadow, a base, a light and sometimes a highlight, which is all a small sprite can show anyway (week 6). Bigger palettes let you paint subtle gradients, and they make it harder for many artists to stay consistent. A common production compromise is a small **master palette** for characters and gameplay objects and a looser one for backgrounds, so the gameplay layer stays consistent however large the team grows.

## 4. Critiquing a palette

When you review someone's palette, ask in this order:

1. **Value.** Sort the colors by L* (lab 05's `palette.py` report does this). Are there clusters where several colors share a value? Are there gaps with no color at all? A good palette covers the value range with no big holes.
2. **Ramps.** Can you trace each ramp from dark to light? Does its L* rise at every step? Does hue move consistently, or zigzag?
3. **Saturation.** Where are the high-S colors? Are there few of them? Are they the ones meant for gameplay?
4. **Harmony.** Which scheme is it closest to? Does the hue contrast match the tone of the game?
5. **Signals.** Is there a reserved hue? Does it collide in value with any large-area color?

This order is deliberate. Value problems break gameplay. Harmony problems only make things look worse.

## In-class activity (25 minutes)

Pairs. You need the interactive (its paste box reads out H, S, V and L*) and the palette you brought.

1. **Dissect (8 min).** Paste your chosen palette into the interactive's paste box and read off H, S, V and L* for each color. Group the colors into ramps. For each ramp, note the hue of each step in L* order and whether it shifts toward yellow as it lightens.
2. **Name the scheme (4 min).** Plot the ramps' middle hues on a hue wheel (the interactive has a paste box). Which harmony scheme is nearest?
3. **Rebuild (10 min).** Pick the ramp that shifts least. Using the ramp model, rebuild it with a shift toward yellow and blue. Keep the same number of steps and the same end L* values within ±5.
4. **Share (3 min).** Show the old and new ramp on the same shaded ball in the interactive. The class votes on which reads as more solid.

Expected output: a table with the old and new ramp (hex, H, S, V, L* per step) and one sentence on the scheme.

## Common misconceptions

- **"Darker means lower V only."** Lowering only V gives a straight ramp that reads flat. Real shadows also change hue (toward the ambient light) and saturation.
- **"Shadows should be black or gray."** Black shadows kill color and depth. Valve's paper lists "shadows go to cool, not black" as a founding rule of Team Fortress 2's look.
- **"Harmony schemes make a palette good."** They only set hue contrast. A triadic palette with no value structure is unreadable; a monochrome one with strong value structure (the Game Boy) is perfectly playable.
- **"Hue shifting always goes toward yellow."** It goes toward the light's color. Yellow is the default because sunlight is warm and yellow is light for free, not because it is required.

## Check yourself

1. A base hue of 200° (sky blue). List the hues of its split-complementary scheme. Which one would you reserve for a hazard, and why?
2. A straight ramp at H = 240°, S = 60%, with V = 30%, 60%, 90% has L* of 14.4, 30.9 and 46.5. You rebuild it with `H_shadow = 250°`, `H_light = 200°`, same S and V. Will the top step's L* rise or fall? Explain with week 4's ceiling rule before computing.
3. You have 16 slots. Your game needs skin, hair, cloth, metal, foliage, stone, one reserved hazard hue and an outline color. Propose a slot plan (how many steps per ramp, which colors are shared) and justify one sharing decision.
4. Compute the hue, saturation and value of step 1 (`t = 1/3`) of a four-step ramp with `H_shadow = 250°`, `H_light = 190°`, `S_mid = 60%`, `S_end = 40%`, `V_dark = 15%`, `V_light = 85%`.

<details>
<summary>Answers</summary>

1. `200 + 150 = 350°` and `200 + 210 = 410 mod 360 = 50°`. Reserve 350° (a red) or 50° (a yellow-orange) depending on the world. In a sky-blue world, either stands out on hue. Pick the one whose L* differs most from the large sky and ground colors. A saturated red sits around L* 53, so it reads on a pale sky; a yellow sits near 90 and reads on dark ground.
2. It rises. Blue sits furthest under its ceiling; moving from 240° toward 200° brings in green, the channel with the largest weight (0.7152), so the same V sits much closer to the ceiling. The new top step is `5CB8E6` at L* 71.1, far above 46.5. The shadow step barely moves (14.4 to 15.1), because 250° is still deep blue.
3. One reasonable plan: skin 3, hair 2, cloth 3, metal 2, foliage 3, stone 2, hazard 1, outline 1 is 17, one too many. Share the darkest stone step with the outline, or use the darkest foliage step as hair shadow. Sharing dark ends is cheap because dark colors differ little in hue to the eye, and it makes the shadows of different materials match.
4. `t = 1/3`. `d = ((190 − 250 + 180) mod 360) − 180 = −60`, so `H = 250 − 20 = 230°`. `|2t − 1| = 1/3`, so `S = 60 − 20/3 = 53.3%`. `V = 15 + 70/3 = 38.3%`. The color is `2E3662`, L* 24.0.

</details>

## Lab / assignment hook

[Lab 05, a zone palette](../labs/lab05.md). You write `lerp_hue`, `ramp`, `harmony` and `even_ramp`, test them against this lecture's tables, and then design a palette of at most 16 colors for an invented MMO zone with at least three hue-shifted ramps and one reserved hue. Deliverable: passing tests, a `.hex` palette file that passes the provided checker, and a one-page rationale. Week 6's pixel sprite will use this palette.

## Sources

- Mitchell, J., Francke, M. & Eng, D. (2007). "Illustrative Rendering in Team Fortress 2." NPAR 2007, Valve. Section 3 lists the warm-to-cool hue shift with cool shadows and increased saturation at the terminator; section 5 describes the diffuse warping texture with grayscale, cool and reddish terminator regions; section 4 describes warm red-team and cool blue-team bases and cites Gooch et al. (1998).
- Gooch, A., Gooch, B., Shirley, P. & Cohen, E. (1998). "A Non-Photorealistic Lighting Model for Automatic Technical Illustration." SIGGRAPH '98. Cool-to-warm shading.
- Lexaloffle, PICO-8 User Manual (version 0.2.7), fixed 16-color palette; hex values from Lospec, "PICO-8" palette page (retrieved September 2026).
- Lospec, "DawnBringer 16" palette page (retrieved September 2026). Hex values of the 16 colors, by the artist DawnBringer.
- NESdev Wiki, "PPU palettes" (retrieved September 2026). Four sprite palettes of four entries (entry 0 transparent), four background palettes, 64-entry master palette.
- Pan Docs (gbdev.io), "Palettes." Original Game Boy (DMG) shows four shades.
- Wikipedia, "Mirror's Edge" (retrieved September 2026). DICE, 2008; Runner Vision turns path objects red on white-dominated environments.
- Python documentation, `colorsys` module (Python 3). `hsv_to_rgb` uses hue as a fraction of a turn.

## Interactive spec: examples/w05-hue-shift-ramp.html

**Purpose.** Show that a hue-shifted ramp with the same HSV V as a straight ramp gives more value range and reads as lit, and let the student find where the shift stops reading as one material.

**The one insight the visual must make obvious.** On first load (the lecture's grass example), two shaded balls sit side by side. The right one looks sunlit, with neighboring bands that differ in hue, yet the two grayscale strips beneath them are nearly identical (L* within 1.6 per step except the top, +5.3). The hue shift adds separation without disturbing the value staircase.

**Layout.** Mobile: stacked. Desktop (900px and up): three columns, left ball, right ball, hue wheel; controls below.

**Views.**
1. Two invented scenes, each a circle (radius 80 px in a 200 × 200 SVG or canvas) resting on a flat ledge. Shade the circle in `n` concentric bands, offset toward the upper left to mimic a light from the upper left: band `i` uses ramp step `i` (darkest at the lower right). The ledge uses step 1 on top and step 0 on its front face. No outlines, no game characters.
2. Under each ball: the ramp as `n` swatches with hex and L* below each, and a grayscale strip where each swatch is the neutral gray of equal L* (as in the week 1 spec).
3. A hue wheel (a ring of 360 hue segments at S = 100%, V = 100%) with the shifted ramp's hues as dots at radius proportional to S, joined by an arc in step order. The straight ramp shows as a single dot.
4. A small line chart: L* (y, 0-100) against step (x) for both ramps, two lines, labelled "straight" and "shifted", with the L* range of each printed (lecture preset: "range 63.4" and "range 67.7").

**Controls.** Base hue H (0-359, default 120). Shift Δ (0-90°, default 40): `H_shadow = H + Δ` toward 240° and `H_light = H − Δ` toward 60° along the shorter way (implement as `H_shadow = lerp_hue(H, 240, Δ / dist(H, 240))` clamped so it does not pass 240, and the same toward 60; if H equals 60 or 240 the corresponding end stays at H). `S_mid` (0-100, default 70), `S_end` (0-100, default 45), `V_dark` (0-100, default 20), `V_light` (0-100, default 90), steps `n` (3-8, default 5). The straight ramp always uses `H`, `S = (S_mid + S_end) / 2` except in "lecture preset" mode, where it uses S = 60 exactly. A "Lecture preset" button restores the section 2 numbers. A "Set end hues directly" checkbox replaces H and Δ with two sliders, `H_shadow` and `H_light` (0-359); in this mode the straight ramp uses the midpoint hue `lerp_hue(H_shadow, H_light, 0.5)`. Ramps whose ends are not symmetric around a base hue, such as the second extra test ramp below, can only be reached this way. At Δ = 0 the two ramps share one hue but still differ in saturation (the straight ramp is flat, the shifted one peaks at `S_mid`), so the balls are close but not identical. A "Paste palette" box accepts hex codes (one per line or comma-separated) and plots them on the hue wheel sorted by L*, with a readout of H, S, V and L* per color, for the in-class activity.

**Warnings.** When Δ > 60 (or, with end hues set directly, when the arc between them exceeds 120°), show a caption "Ends may read as different materials". When any L* step between neighbors is below 10 (week 1's merge zone), highlight that pair in the swatch row and show "Value step too small".

**Formulas.** Exactly as lecture section 2: `t = i/(n−1)`, `V = lerp(V_dark, V_light, t)`, `H = lerp_hue(H_shadow, H_light, t)` with `d = ((b − a + 180) mod 360) − 180`, `S = S_mid − (S_mid − S_end)|2t − 1|`. HSV to RGB as in week 4 section 2; channel rounding `floor(x × 255 + 0.5)`. L* exactly as in week 1 (sRGB linearization, `Y = 0.2126R + 0.7152G + 0.0722B` on linear values, cube-root curve).

**Test values (lecture preset: H_shadow 160, H_light 80, S_mid 70, S_end 45, V 20→90, n 5).**
- Straight: `143314` 18.2, `266026` 35.8, `388C38` 51.7, `4AB94A` 67.0, `5CE65C` 81.6; range 63.4.
- Shifted: `1C332B` 19.2, `29603B` 36.3, `2A8C2A` 51.2, `72B94F` 68.6, `C3E67E` 86.9; range 67.7.
- `lerp_hue(350, 30, 0.5) = 10`, `lerp_hue(200, 60, 0.5) = 130`.
- Ramp(350, 40, 80, 55, 25, 95, n = 4) → `401D23` 16.0, `7B2D23` 29.9, `B76734` 51.9, `F2C66D` 82.0.
- Ramp(250, 190, 60, 40, 15, 85, n = 4), set with "Set end hues directly" → `191726` 8.6, `2E3662` 24.0, `49739D` 47.1, `82CAD9` 77.3.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`. Native labelled range inputs with numeric outputs; all views update on input. Swatches have text labels (hex, L*) so the page works without color perception. `prefers-reduced-motion`: no transitions. `prefers-color-scheme`: chrome only; swatches and balls always show true colors on a neutral mid-gray card so light and dark mode do not change how the ramps look.
