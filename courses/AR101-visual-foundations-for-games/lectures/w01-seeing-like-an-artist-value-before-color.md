# AR101 · Week 01 — Seeing Like an Artist: Value Before Color

**Why this matters:** Players find the enemy, the ledge and the health potion by how light or dark they are long before they notice what color they are. If you pick colors first and check value never, you will ship a bright red potion that disappears on a gray floor, and no amount of saturation will save it.

**You will be able to:**
- Compute the value (CIE lightness, L*) of any sRGB color and the value gap between a figure and its background.
- Predict which scene elements merge when a picture is reduced to 4, 3 or 2 values.
- Plan a small game scene as a three-value thumbnail before choosing any hue.
- Critique a screenshot or mockup by naming the pairs of elements whose value gap is too small.

**Before class:** Solarski, *Drawing Basics and Video Game Art* (2012), the material on light, shade and value (find it through the table of contents; any printing of the 2012 edition works). Mitchell, Francke and Eng, "Illustrative Rendering in Team Fortress 2" (2007), section 1 and section 4.3, about four pages. W3C, WCAG 2.1, the definition of "relative luminance" (one paragraph).

**Prerequisites from earlier courses:** None. This is a first-semester course. Two later lectures build directly on this one. [UX201 week 11, accessibility guidelines](../../UX201-game-ux-and-player-psychology/lectures/w11-accessibility-guidelines.md) turns the same luminance formula into contrast ratios for text. [GD101 week 12, feedback, juice, clarity and readability](../../GD101-introduction-to-game-design/lectures/w12-feedback-juice-clarity-readability.md) uses the squint test you learn here as a quick hierarchy check.

**Interactive:** [`examples/w01-value-view.html`](../examples/w01-value-view.html). Keep it open during section 2.

---

## 1. Three properties of a color, and the one your eye trusts first

Every color you pick in a paint program has three independent properties.

- **Hue** is the named color family: red, orange, green, blue, violet.
- **Saturation** (also called chroma) is how intense the color is, from a gray with no color at all to the purest version of the hue.
- **Value** is how light or dark the color is, from black to white. Artists say "value", scientists say "lightness". This course uses the words interchangeably.

Value is the property that carries shape. Draw a sphere with only light and dark, no hue, and it reads as a sphere. Draw it with a perfect hue gradient at one constant value and it reads as a flat disc with a rainbow on it. The same is true of an enemy standing in a corridor. The eye finds the enemy's edge where light meets dark.

There is a physiological reason for this. The visual system resolves fine detail better in luminance (brightness) contrast than in color contrast. In a classic experiment, Kathy Mullen (1985) measured how much contrast people needed to see stripes that differed only in color (red against green, or blue against yellow) and compared it with stripes that differed only in brightness. For anything finer than very broad stripes (above about half a cycle per degree of visual angle), people were more sensitive to the brightness stripes, and the finest color-only stripes they could resolve were about 11 to 12 cycles per degree. In plain terms, color tells you *what* a large area is, and value tells you *where its edges are*. A sprite 32 pixels tall on a phone screen is all edges.

So artists work in this order:

1. Plan the values. Decide what is darkest, what is lightest, and what sits in the middle.
2. Check that everything the player must find is separated in value from what surrounds it.
3. Only then choose hues and saturations, keeping each one at the value you planned.

This lecture gives you a number for step 2, so "separated in value" stops being a feeling.

### Figure and ground

Two more terms. The **figure** is the thing the player must notice: the character, the pickup, the door. The **ground** is whatever sits directly behind it: floor, sky, wall. Readability is almost always a question about one figure against one ground. "Is the potion readable?" means "Is the potion readable *on this floor*?" The same potion can read well in one room and vanish in the next.

## 2. Worked example: the red potion that vanished

### The hook: a console that let you repaint every game

The original Game Boy (Nintendo, 1989) had a 160 × 144 pixel screen that could show four shades of green-gray and nothing else. Every game made for it was designed in exactly four values.

When the Game Boy Color arrived in 1998, it could run those old cartridges, and it let players choose a color palette for them. Holding one of several button combinations while the startup logo was on screen picked one of 12 palettes, one of which reproduced the original grayscale. The same game could be played in browns, in blues, or in reds and greens.

Players noticed something odd. Most palettes worked. The games stayed playable in colors their artists never saw. How can a picture survive having every color replaced?

Because the game never stored colors. It stored four *shade numbers*, and the palette only decided what color each number would be painted. As long as the four colors in a palette stayed in the same light-to-dark order and far enough apart in value, every figure still separated from its ground. The information lived in value the whole time. Hue was a costume.

Now the reverse problem, which you will meet on your first art job. A level artist paints a dungeon floor in a neutral stone gray. A prop artist paints the health potion bright, saturated red, the most eye-catching color in the palette. On the artist's monitor it looks great. In playtests, players walk straight past it. Why?

### The model: value as a number

To compare values you need a number that matches how light a color *looks*. The average of R, G and B does not work (you'll see why shortly). The standard answer is **CIE lightness, L\***, which runs from 0 (black) to 100 (white) and was designed so that equal steps look like roughly equal steps in lightness. It is computed in two stages.

**Stage 1, relative luminance Y.** Take the sRGB channel values R, G, B (each 0 to 255). For each channel, divide by 255 to get `c` between 0 and 1, then undo the display's gamma curve:

```
linear(c) = c / 12.92                       if c ≤ 0.04045
linear(c) = ((c + 0.055) / 1.055) ^ 2.4     otherwise

Y = 0.2126 × linear(R) + 0.7152 × linear(G) + 0.0722 × linear(B)
```

`Y` is the amount of light the pixel emits, from 0 to 1. The three weights say how bright each primary looks to a human: green counts almost ten times as much as blue. This is the same `Y` the web accessibility standard (WCAG) calls relative luminance.

**Stage 2, lightness L\*.** Light and perceived lightness are not proportional. Doubling the light does not look twice as bright. L* applies a cube-root curve:

```
L* = 116 × Y^(1/3) − 16         if Y > 216/24389  (about 0.0089)
L* = (24389/27) × Y              otherwise (very dark colors)
```

**The value gap** between a figure and its ground is

```
ΔV = | L*(figure) − L*(ground) |
```

In this course we use a working rule for gameplay-critical figures: **ΔV of at least 20** to read reliably, **40 or more** for something that must be spotted in a fraction of a second, and **under 10** means the two will merge. These thresholds are a course convention, calibrated so they roughly match the web's 3:1 contrast guideline for mid-tones (section 3 checks that). They are not a law of vision.

### Numbers you can check

Here is the dungeon, run through the model. You can compute any row with a calculator, or with this Python, which prints exactly the L* column.

```python
def srgb_to_linear(c):
    c = c / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def lightness(r, g, b):
    y = (0.2126 * srgb_to_linear(r) + 0.7152 * srgb_to_linear(g)
         + 0.0722 * srgb_to_linear(b))
    return 116 * y ** (1 / 3) - 16 if y > 216 / 24389 else 24389 / 27 * y


colors = {
    "stone floor": (128, 128, 128),
    "red potion": (255, 0, 0),
    "dark red potion": (200, 40, 40),
    "pale potion": (255, 160, 160),
    "gold potion": (230, 200, 60),
    "dark floor": (60, 60, 60),
}
for name, rgb in colors.items():
    print(f"{name:16} L* = {lightness(*rgb):5.1f}")
```

```
stone floor      L* =  53.6
red potion       L* =  53.2
dark red potion  L* =  44.2
pale potion      L* =  75.4
gold potion      L* =  81.0
dark floor       L* =  25.3
```

Now pair them up:

| Figure | Ground | L* figure | L* ground | ΔV | Verdict |
|---|---|---|---|---|---|
| Red potion (255, 0, 0) | Stone floor (128, 128, 128) | 53.2 | 53.6 | 0.4 | Merges |
| Dark red potion (200, 40, 40) | Stone floor | 44.2 | 53.6 | 9.4 | Merges |
| Pale potion (255, 160, 160) | Stone floor | 75.4 | 53.6 | 21.8 | Reads |
| Gold potion (230, 200, 60) | Stone floor | 81.0 | 53.6 | 27.4 | Reads |
| Red potion (255, 0, 0) | Dark floor (60, 60, 60) | 53.2 | 25.3 | 27.9 | Reads |

The first row is the playtest failure. Pure red and middle gray differ by less than half a point of lightness. In value they are the same color. A player who glances at the room sees an even gray field. Only someone who looks straight at the potion and attends to hue will find it.

Look at the two fixes that work. You can move the figure (make the potion paler, or change it to gold), or you can move the ground (darken the floor). The red potion on the dark floor reads fine without any change to the potion. Readability is a property of the *pair*.

Notice what does not work: making the red darker and richer (row 2). It feels like "more red" should stand out more. It moves the potion a few points in value and leaves it inside the merge zone.

### The trap of naive desaturation

Most paint programs can turn an image gray. Some of those commands average the three channels: `gray = (R + G + B) / 3`. Try it on the three primaries:

| Color | Channel average | L* of that gray | True L* of the color | Error |
|---|---|---|---|---|
| Pure red (255, 0, 0) | 85 | 36.1 | 53.2 | −17.1 |
| Pure green (0, 255, 0) | 85 | 36.1 | 87.7 | −51.6 |
| Pure blue (0, 0, 255) | 85 | 36.1 | 32.3 | +3.8 |

The average says pure green and pure blue are the same value. They are 55 points apart, more than half the whole scale. If you check your values with a naive gray filter, you will approve a blue enemy on a green field that in fact reads fine, and you will miss problems like the red potion. Use a grayscale mode built on luminance or lightness (many programs offer a "luminosity" blend mode or a Lab/L* channel), or use the interactive, which computes L* exactly.

### A visual you can move

Open the interactive. The left panel shows a small invented dungeon room in color: a stone floor, a potion, a coin, a player and an enemy. The right panel shows the same room with every color replaced by the gray of equal L*. With the defaults, the potion is plainly visible on the left and invisible on the right.

Select the potion and drag its color around. Watch the ΔV readout. Then press **Match value**, which moves any color you pick to the floor's exact lightness. Pick a green, a violet, a cyan. Each of them disappears on the right. Any hue can vanish. Now switch the **Bands** control to 4 (the Game Boy's four shades), then 3, then 2. Elements that share a band merge into one flat area. That is what your player sees in a quick glance, in dim light, on a cheap screen, or from across the room.

### Cross-game recognition

The same principle appears across very different games once you look for it.

**Game Boy and Game Boy Color (1989, 1998).** Four values, stored as shade numbers, with color assigned afterward. In our terms, every Game Boy game is a four-band value plan, and each Game Boy Color palette maps those four bands to four colors. A palette works when its four colors keep increasing in L* with a reasonable gap between neighbors. If a palette gave two neighboring shades colors with nearly equal L*, every figure drawn in one of them would merge with any ground drawn in the other, whatever the hues.

**Return of the Obra Dinn (Lucas Pope, 2018).** A modern 3D game rendered in two values, black and white, in the style of early Macintosh games. It has no grays at all. It fakes them with dithering, patterns of black and white dots whose density stands in for lightness. Our model explains how that works. Seen from far enough away, a 50% checkerboard of black and white emits half the light, so `Y = 0.5` and `L* = 116 × 0.5^(1/3) − 16 ≈ 76`, not 50. Dither density is a value control, and it is not linear in lightness either. The whole game is readable because its artist planned figure and ground in value, the only property left.

**Team Fortress 2 (Valve, 2007).** Valve's artists and engineers wrote that their character shading was designed to convey shape through variation in luminance and hue, so players could read the scene and pick out other players across many lighting conditions. They also pushed shadows toward cool colors rather than toward black. In our terms, a shadow that stays a color keeps some value separation from a truly dark background. And they kept the world's geometry and textures low in repetition and visual noise, which the paper ties directly to gameplay: detail in the world should not compete with the players. That is the value-first workflow at production scale.

Three games, three technologies (a 1989 LCD, a 2018 dithering shader, a 2007 3D renderer), one idea: the readable picture is a value plan first.

### Eyes-open design judgment

- **Use the ΔV check on pairs, not on colors.** A color is never "readable" on its own. Keep a list of the figure and ground pairs that matter for gameplay (player on every floor type, pickups on every floor type, enemies on every background) and check each one.
- **Decide what gets the biggest gap.** You can't separate everything from everything. A three-value plan (section 3) forces you to decide that enemies and pickups get the extremes and decoration lives in the middle. If the decoration gets the strongest contrast, it will pull the eye away from play.
- **Hue still matters, deliberately.** Two figures at the same value but different hues can still be told apart when a player looks straight at them. Hue is a good second channel for *identity* (which team, which element) once value has handled *detection* (is something there). The mistake is using hue for detection.
- **Know the model's limits.** L* predicts the lightness of a flat patch on a neutral surround. It does not capture that very saturated colors look somewhat brighter than their L* suggests (the Helmholtz-Kohlrausch effect), that a patch looks lighter on a dark surround, or that motion and flashing draw the eye regardless of value. Treat ΔV as a necessary check, not the whole story, and confirm with a playtest.
- **Don't stop at one ground.** A pickup that reads on the dungeon floor may vanish on the snow level. Games with many biomes often solve this with an outline or a small halo in a fixed value. That guarantees a known ground right around the figure, a trick you'll see again in UX201 week 11.

## 3. Value structure: planning a scene in three values

Once you can measure value, you can plan with it. The oldest planning tool in illustration is the **three-value thumbnail**: a small sketch (a few centimeters across) using only three flat tones, dark, middle and light. No hue, no gradients, no detail.

The three-value thumbnail forces three decisions.

1. **Which elements share a value group?** Everything in the same group will visually merge. That is fine for a wall and the floor next to it. It is a failure for an enemy and the wall behind it.
2. **Where is the strongest contrast?** The eye goes first to the place where the lightest light meets the darkest dark. Put that where you want the player to look: the exit, the boss, the objective.
3. **What is the dominant value?** A scene that is mostly dark with small lights reads as night, danger or mystery. A scene mostly light with small darks reads as open, calm or exposed. The proportion of each group sets mood before any color does.

A useful split for a game screen:

| Group | L* range (approx.) | Typical content |
|---|---|---|
| Dark | 0 to 35 | Deep background, shadows, some enemy bodies |
| Middle | 35 to 70 | Walkable ground, walls, large props |
| Light | 70 to 100 | Pickups, interactables, the player's highlights, the goal |

This is one plan among many. A snow level might flip it, with a light ground and dark figures. What matters is that ground and figures sit in different groups.

### Depth through value

Outdoors, air scatters light. Distant objects move toward the sky's value and lose contrast. Painters call this **atmospheric perspective**. Games use it deliberately, often through fog. In value terms, the far layer of a scene has a small value range close to the sky's value, and the near layer has the full range. If your background mountains have as much value contrast as your foreground enemies, the eye can't tell them apart in depth, and the background competes with gameplay. Compress the background's value range and it steps back.

### How the week 1 bands connect to the web's contrast rule

In UX201 you will measure text contrast with the WCAG contrast ratio `(Y_light + 0.05) / (Y_dark + 0.05)` and its 3:1 minimum for large elements. Start from the middle gray floor (Y = 0.2159, L* = 53.6). The color that is exactly 3:1 lighter has Y ≈ 0.748, which is L* ≈ 89.3, a gap of about 36. The color exactly 3:1 darker has Y ≈ 0.039, which is L* ≈ 23.2, a gap of about 30. So around the middle of the scale, 3:1 corresponds to a ΔV of 30 to 36. Our working threshold of 20 is looser, because a game figure usually has other help (size, motion, shape) that a line of small text does not. For UI text, use the stricter UX201 standard.

## 4. Tools for seeing value

You will use four tools all semester.

- **The squint test.** Squint at your screen or step back until detail blurs. Fine detail and most hue information fade first, and the value pattern stays. If the thing you want players to notice is not what remains, fix the values.
- **A grayscale view.** Put a luminosity-based grayscale layer over your whole painting and toggle it often. Avoid channel averaging for the reasons in section 2.
- **A band view.** Posterize the grayscale into 3 or 4 levels. This is the Game Boy test. It shows merges that a smooth grayscale can hide.
- **A ΔV list.** For shipping work, write down the gameplay-critical pairs and their measured gaps, just like the table above. Lab 01 automates it.

## In-class activity (25 minutes)

Work in pairs. Materials: paper, a gray marker or pencil that can make one flat middle tone, a black marker, and the interactive.

1. **(8 min)** Each person draws three thumbnails, about 6 × 4 cm, of the same small game scene: a corridor with the player, one enemy, one pickup and an exit door. Use only white paper, one middle tone and black. Each thumbnail must put the strongest contrast somewhere different.
2. **(5 min)** Swap sketches. Your partner has five seconds per thumbnail to point to "the first thing I saw". Record it.
3. **(7 min)** Pick the best thumbnail. In the interactive, set the five scene colors so that their values match your thumbnail's three groups. Then choose hues that you like while keeping each element in its group. Record the five RGB values and their L*.
4. **(5 min)** Switch the band view to 3. Does your color version collapse back to your thumbnail? If an element jumped to a different band, adjust it.

Expected output: three thumbnails with the partner's "first seen" notes, and a five-row table of RGB, L* and group for the chosen design.

## Common misconceptions

- **"Saturated colors stand out, so a bright red pickup is always visible."** Saturation catches attention when you look straight at it. Detection at a glance depends on value. Pure red has L* 53, the same as middle gray.
- **"Turn it gray with a desaturate filter to check values."** Channel averaging puts pure green and pure blue at the same gray, although their L* differ by 55. Use a luminance-based grayscale.
- **"A color is readable or it isn't."** Readability belongs to a figure and ground pair. The red potion fails on stone and passes on the dark floor with no change to the potion.
- **"Value only matters for black-and-white games."** Every picture has a value structure. Color games just hide their value mistakes from the artist who painted them, until a player walks past the potion.

## Check yourself

1. A floor has RGB (200, 200, 200), L* 80.6. You want a pickup with ΔV at least 20. What range of L* can the pickup have? Would pure green (0, 255, 0) work?
2. Compute L* for pure blue (0, 0, 255) using the formulas in section 2. Show the value of `Y` along the way.
3. A Game Boy Color-style palette maps the four shades to colors with L* of 20, 45, 48 and 90. Which shades will be hard to tell apart, and what kind of scene element should an artist avoid drawing in one of them on top of the other?
4. A 25% dither (one white dot in every four, the rest black) is used as a "dark gray". What L* does it approximate from a distance?

<details>
<summary>Answers</summary>

1. The pickup needs L* ≤ 60.6 (darker than the floor by 20; it can't be 20 lighter because the scale ends at 100). Pure green has L* 87.7, a gap of only 7.1, so it merges with the floor. A dark green or a saturated blue would work.
2. linear(0) = 0 and linear(255) = 1, so `Y = 0.0722 × 1 = 0.0722`. That is above 0.0089, so `L* = 116 × 0.0722^(1/3) − 16 = 116 × 0.4164 − 16 ≈ 32.3`.
3. The second and third shades (L* 45 and 48, a gap of 3) will merge. Any figure drawn in one of those shades over a ground in the other (a character over a floor, a pickup over a wall) will vanish. The artist should keep figures and their grounds in shades that are at least 20 apart, for example the second shade on the fourth.
4. One white dot in four emits a quarter of the light, `Y = 0.25`, so `L* = 116 × 0.25^(1/3) − 16 ≈ 57.1`. It looks like a middle gray, much lighter than the "25%" suggests, because lightness follows a cube root of light.

</details>

## Lab / assignment hook

[Lab 01, the value checker](../labs/lab01.md). You will implement the L* computation and a pair checker in Python, run it on a supplied dungeon palette, then paint three value studies of your own and prove with the checker that every gameplay-critical pair has ΔV of at least 20. This is the first of the weekly studies (50% of the course grade).

## Sources

- Pan Docs (gbdev.io), "Specifications" (original Game Boy, DMG, 1989). Screen resolution 160 × 144, four shades.
- Pan Docs (gbdev.io), "Power Up Sequence" (Game Boy Color boot ROM). Monochrome-only games get a compatibility palette that the user can override with button combinations during the logo animation.
- Wikipedia, "Game Boy Color" (1998 hardware). Boot ROM holds palettes for more than 90 titles; users can choose from 12 palettes, one of which reproduces the original grayscale, by pressing a button combination at startup.
- Wikipedia, "Return of the Obra Dinn" (Lucas Pope, 3909 LLC, October 2018). 1-bit monochrome style inspired by early Macintosh games; rendering changed to reduce motion sickness caused by dithering.
- Mitchell, J., Francke, M. and Eng, D. (2007). "Illustrative Rendering in Team Fortress 2." *Proceedings of NPAR 2007*, ACM. Sections 1, 3 and 4.3: shading that conveys shape through variation in luminance and hue so players can read the scene and identify players; shadows shift toward cool colors rather than black; low visual noise in world textures. Official TF2 Wiki, "Art style", summarizes the same points.
- Mullen, K. T. (1985). "The contrast sensitivity of human colour vision to red-green and blue-yellow chromatic gratings." *Journal of Physiology* 359, 381-400. Above about 0.5 cycles per degree, sensitivity is greater for luminance gratings than chromatic ones; chromatic acuity limit about 11-12 cycles per degree.
- W3C (2018). *Web Content Accessibility Guidelines (WCAG) 2.1*, definitions of "relative luminance" and "contrast ratio". sRGB linearization and the 0.2126, 0.7152, 0.0722 weights; the 3:1 threshold for non-text elements (success criterion 1.4.11).
- CIE 1976 L\*a\*b\* lightness definition (CIE 15:2004, *Colorimetry*, 3rd ed.). `L* = 116 f(Y) − 16` with the linear segment below `Y = 216/24389`.
- Fairchild, M. D. (2013). *Color Appearance Models*, 3rd ed., Wiley. Background on the Helmholtz-Kohlrausch effect and simultaneous contrast, the limits of a flat-patch lightness model.
- Solarski, C. (2012). *Drawing Basics and Video Game Art*. Watson-Guptill. Course reading on value and light.

## Interactive spec: examples/w01-value-view.html

**The one insight.** Two colors that look completely different can be the same value, and then they merge. The first screen must show a clearly visible red potion on the left and an invisible one on the right, with ΔV 0.4 printed next to it.

**Layout.** Two linked panels side by side on desktop (stacked on phones, color above value), with a readout table below and controls beside or below.

- **Left panel, "Color".** A top-down invented dungeon room drawn with simple shapes on a 10 × 7 tile grid. Floor: every tile filled with the floor color, with thin tile seams 4 L* darker. Potion: a circle with a small rectangle neck, about 0.6 tile wide. Coin: a small circle. Player: a circle head over a rounded body. Enemy: a rounded rectangle with two small triangle horns. No game characters or logos.
- **Right panel, "Value only".** The identical drawing, with every color replaced by the neutral gray of equal L*. Conversion: compute L*, then `Y = ((L* + 16) / 116)^3` if L* > 8 else `L* / 903.3`, then encode to sRGB (`12.92 Y` if Y ≤ 0.0031308, else `1.055 Y^(1/2.4) − 0.055`), times 255, rounded, used for R = G = B.

**Controls (all keyboard reachable, native inputs, values printed).**
- Element selector (radio or segmented control): floor, potion, coin, player, enemy.
- Color editing for the selected element: three sliders R, G, B (0-255) plus a native color input, kept in sync.
- **Match value** button: moves the selected element's color to the floor's L* while keeping its hue direction. Method: if the element is lighter than the floor, blend its sRGB toward black `(1 − t) × rgb`; if darker, blend toward white `rgb + t × (255 − rgb)`. Binary search `t` in [0, 1] until |ΔL*| < 0.1 (at most 30 iterations). Disabled when floor is selected.
- **Bands:** off, 4, 3, 2. When on, the value panel snaps each element's L* to its band's center (for n bands, band `k = min(floor(L*/100 × n), n − 1)`, center `(k + 0.5) × 100 / n`). Elements with the same band are outlined with a dashed line in the value panel and flagged "merged" in the table.
- **Gray method:** "L* (correct)" or "channel average (wrong)". The average mode sets gray to `round((R+G+B)/3)` and shows a warning line: "Average gray: pure green and pure blue both become 85."
- **Threshold** slider for the pass line, 5 to 50, default 20.
- **Presets:** "Red potion on stone" (default), "Pale potion", "Dark floor", "Game Boy four shades" (floor, potion, coin and enemy set to the four invented greens listed below, player unchanged), "Naive gray trap" (enemy pure blue, floor pure green).

**Readout table.** One row per element: name, RGB, L* (one decimal), band (when on), ΔV against floor (one decimal), and a pass or fail mark against the threshold, with the fail rows in the damage color and a text label (not color alone).

**Default state.** Floor (128, 128, 128). Potion (255, 0, 0). Coin (230, 200, 60). Player (60, 90, 200). Enemy (90, 110, 60). Bands off, L* method, threshold 20.

**Test values (must match to one decimal).**

| Color | L* |
|---|---|
| (128, 128, 128) | 53.6 |
| (255, 0, 0) | 53.2 |
| (200, 40, 40) | 44.2 |
| (255, 160, 160) | 75.4 |
| (230, 200, 60) | 81.0 |
| (60, 60, 60) | 25.3 |
| (60, 90, 200) | 41.9 |
| (90, 110, 60) | 43.7 |
| (0, 255, 0) | 87.7 |
| (0, 0, 255) | 32.3 |

Default ΔV against floor: potion 0.4 (fail), coin 27.4 (pass), player 11.7 (fail), enemy 9.9 (fail). Inverse check: L* 50 gives gray 119; L* 62.5 gives 151; L* 87.5 gives 219; L* 12.5 gives 33. For the "Game Boy four shades" preset use these invented greens: enemy (15, 56, 15) L* 19.9, potion (48, 98, 48) L* 37.1, floor (139, 172, 15) L* 65.8, coin (155, 188, 15) L* 71.5. With 4 bands the floor and coin both land in band 2 and are flagged merged (ΔV 5.8, from the unrounded 71.53 − 65.77). That is the point of the preset. Two greens that look distinct side by side still merge at a glance.

**Accessibility and motion.** Pass or fail is shown by text and icon shape as well as color. No animation is required; any transition respects `prefers-reduced-motion`. Palette tokens from `templates/interactive-tokens.css`, light and dark themes. The scene colors themselves are data and do not change with the theme.
