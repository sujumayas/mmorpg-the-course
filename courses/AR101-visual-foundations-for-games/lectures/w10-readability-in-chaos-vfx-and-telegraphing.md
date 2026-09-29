# AR101 · Week 10 — Readability in Chaos: VFX and Telegraphing

**Why this matters:** In a big fight, twenty players fire glowing spells at the same boss, and the one shape that tells them where to stand gets lost in the glow. Players then die to an attack they could not see and blame the game. This week you learn why bright effects erase warnings, and how to draw a warning that survives any amount of glow.

**You will be able to:**
- Compute the value contrast of a telegraph drawn with additive blending and with alpha blending over a background of stacked effects.
- Explain "headroom" and predict how many overlapping effects it takes to erase a light telegraph.
- Design a two-tone telegraph (light fill plus dark rim) and compute its worst-case contrast.
- Critique a busy combat screenshot by sorting every effect into signal or noise and naming the fix for each problem.

**Before class:** Solarski, *Drawing Basics and Video Game Art* (2012), the material on value and on contrast as a way to direct attention (find it through the table of contents and skim for the value-grouping figures). Reread your notes on value from AR101 week 1 and on anticipation poses from AR101 week 8.

**Prerequisites from earlier courses:** None outside AR101. This week uses value as CIE L* from 0 to 100 and the working rule that two areas separate when their values differ by at least 20, both from [AR101 week 1, value before color](w01-seeing-like-an-artist-value-before-color.md), where the value gap is written ΔV. It also uses the shape language of [AR101 week 2](w02-shape-language-circles-squares-triangles.md) and the anticipation-action-recovery timing of [AR101 week 8](w08-sprite-animation-frames-and-timing.md). Later, [GD101 week 12, feedback and readability](../../GD101-introduction-to-game-design/lectures/w12-feedback-juice-clarity-readability.md) turns the hidden time you study here into a reaction-time budget.

**Interactive:** [`examples/w10-telegraph-headroom.html`](../examples/w10-telegraph-headroom.html). Keep it open during section 2.

---

## 1. Signal and noise on a combat screen

Everything that moves or glows in a fight belongs to one of two groups.

A **signal** is a visual the player must act on. The orange circle on the floor that says "a slam lands here in two seconds" is a signal. So is the swirl over an enemy that says "this caster is about to heal". If a player misses a signal, they lose health, time or the fight.

**Noise** is everything else. The sparks from your own sword, the fireball your teammate throws, the shimmer of a shield buff, the smoke from a torch. Noise is often the best art in the game. It gives hits weight and spells personality. It is still noise in the narrow sense that no decision depends on seeing it.

A **telegraph** is the family of signals that warn about an attack before it lands. It usually has three parts, which you met as animation phases in week 8.

- **Windup (anticipation).** The boss raises its club, a circle appears under the target, a bar starts to fill.
- **Active.** The attack hits. Damage is dealt inside the marked area.
- **Recovery.** The boss is open to counterattack. The marked area fades.

A telegraph is only useful while the player can see it. That sounds obvious, and it is exactly what big fights break. The rest of this lecture explains the mechanism and the fix.

### Why effects glow

Most spell effects are drawn with **additive blending**. The renderer takes the color of the effect's pixel and adds it to the color already on screen. Black adds nothing, so a black background around a flame sprite is invisible, and the flame looks like it emits light. Artists love additive blending because it makes fire, magic and energy look bright without any extra work.

The other common mode is **alpha blending** (also called "over" blending). Here the new pixel replaces a fraction of the old one. A smoke sprite with 60% opacity shows 60% smoke and 40% of whatever was behind it. Alpha blending can make a pixel darker. Additive blending cannot.

Graphics APIs make the addition explicit. The OpenGL reference for blending writes the result as the sum of the source and destination terms, capped at the largest value the framebuffer can store. That cap is the whole problem. A pixel can only get so bright. Once it is white, adding more light changes nothing.

## 2. Worked example: the headroom of a telegraph

### The hook

World of Warcraft has a graphics option called Spell Density. Its settings run from Essential through Some, Half and Most up to Everything, with a Dynamic default that scales effects with how busy the screen is. The setting's current console variable dates from patch 9.0.1 (Shadowlands, October 2020), a raid-only Spell Density variable is listed back to patch 6.0.2 (2014), and patch 11.2.0 (August 2025) reworked the feature to improve visual clarity. Guild Wars 2 goes further. Its Hide Ally Visual Effects option can hide every effect produced by other players' skills.

Think about what that means. A studio pays VFX artists for years to make spells look spectacular, then ships a menu option to delete most of them. Why would players ask for that, and why would the studio agree? Because in a raid those effects stack until the floor turns white, and a white floor is where warnings go to die. You can calculate when that happens.

### The model

Work in value, the L* scale from week 1: 0 is black and 100 is white. We treat each overlapping effect as adding a fixed number of value points. This is a simplification, and we check it against the real linear-light math later in this section.

```
background        B(N) = min(100, V_floor + N × e)
additive fill     C_fill = min(t, 100 − B)
dark rim (alpha)  C_rim  = α × B
readable if       C ≥ 20
```

- `V_floor` is the value of the bare ground where the telegraph sits.
- `N` is the number of player effects overlapping that spot.
- `e` is how many value points one effect adds on average.
- `B` is the background value after the effects, capped at 100 because a pixel cannot be brighter than white.
- `t` is the value an additive telegraph fill adds on top of the background.
- `100 − B` is the **headroom**: how far the background can still brighten before it hits white.
- `α` (alpha) is the opacity of a black rim drawn with alpha blending. Over a background of value `B`, it leaves `(1 − α) × B`, so its contrast is `α × B`.
- `C` is the value contrast between the telegraph and the background right next to it. The readability threshold of 20 is the same working gap you used in week 1.

Read the fill line slowly. An additive telegraph can add `t` points only if there is room for them. When the background is already near white, most of `t` is thrown away by the cap. **The contrast of a light signal is limited by its headroom.** The dark rim behaves the other way around. The brighter the background, the more a dark rim stands out.

### Numbers you can check

Take a mossy stone floor at `V_floor = 30`, player effects that add `e = 10` points each, an additive fill of `t = 40`, and a black rim at `α = 0.8`.

| Effects overlapping N | Background B | Headroom 100 − B | Fill contrast | Rim contrast | Best of the two |
|---|---|---|---|---|---|
| 0 | 30 | 70 | 40 | 24 | 40 |
| 1 | 40 | 60 | 40 | 32 | 40 |
| 2 | 50 | 50 | 40 | 40 | 40 |
| 3 | 60 | 40 | 40 | 48 | 48 |
| 4 | 70 | 30 | 30 | 56 | 56 |
| 5 | 80 | 20 | 20 | 64 | 64 |
| 6 | 90 | 10 | 10 (fails) | 72 | 72 |
| 7 | 100 | 0 | 0 (fails) | 80 | 80 |

Check one row by hand. At `N = 5` the background is `30 + 5 × 10 = 80`. The fill can add at most `100 − 80 = 20` points, so its contrast is 20, right on the threshold. The rim leaves `0.2 × 80 = 16`, so its contrast is `80 − 16 = 64`.

Two things stand out. First, the fill-only telegraph works perfectly on an empty floor and fails with six overlapping effects. Six is not a lot. In a 20-player raid, six spells landing near the boss at once is an ordinary second. Second, the rim-only telegraph is weakest on the empty floor (24, just above the threshold) and gets stronger as the fight gets busier. The two styles fail in opposite conditions.

Put both on the same telegraph and take whichever contrast is larger. The worst case of the pair is:

```
worst case = min( t , 100 × α / (1 + α) )
```

The second term is where the falling fill line crosses the rising rim line. With `α = 0.8` it is `80 / 1.8 = 44.4`, which is above `t = 40`, so the worst case is 40 at every background from black to white. A telegraph with a light fill and a dark rim never drops below 40 contrast in this model. That is the **two-tone rule**: a signal with one light part and one dark part always has a part that contrasts with the background, whatever the background does.

The same numbers run as a short script. It prints the table above, then repeats the fill test in linear light, which is how a modern renderer really adds effects.

```python
V_FLOOR, E, T, ALPHA, GAP = 30, 10, 40, 0.8, 20

print(" N  bg  fill  rim  best")
for n in range(8):
    bg = min(100, V_FLOOR + n * E)
    fill = min(T, 100 - bg)          # additive fill: capped by headroom
    rim = ALPHA * bg                 # dark rim drawn over, value 0
    best = max(fill, rim)
    flag = "" if fill >= GAP else "  fill fails"
    print(f"{n:2d} {bg:4d} {fill:5d} {rim:4.0f} {best:5.0f}{flag}")


def to_y(L):   # CIE L* (0-100) -> relative luminance Y (0-1)
    return ((L + 16) / 116) ** 3 if L > 8 else L * 27 / 24389


def to_L(y):   # relative luminance -> CIE L*
    return 116 * y ** (1 / 3) - 16 if y > 216 / 24389 else y * 24389 / 27


floor = to_y(30)          # the same floor, now in linear light
effect = 0.06             # light one effect adds, in linear units
fill = 0.25               # light the additive telegraph adds
for n in (0, 2, 4, 8, 12, 16):
    bg = min(1.0, floor + n * effect)
    lit = min(1.0, bg + fill)
    print(f"N={n:2d}  bg L*={to_L(bg):5.1f}  fill contrast={to_L(lit) - to_L(bg):5.1f}")
```

The second half prints fill contrasts of 32.7, 21.9, 17.3, 12.7, 9.1 and 0.0 for 0, 2, 4, 8, 12 and 16 effects. In linear light the fill loses contrast even faster at first, because equal steps of added light look smaller and smaller as the background brightens. The value-point model is, if anything, generous to the additive fill. The conclusion stands either way: a light-only signal fades as the screen gets brighter, and it disappears when the screen hits white.

### A visual you can move

Open [`examples/w10-telegraph-headroom.html`](../examples/w10-telegraph-headroom.html). The left view is a top-down arena drawn in simple shapes: a stone floor, a boss marker and a telegraph circle, with player effects drawn as soft additive blobs. The right view plots contrast against the number of overlapping effects, one line for the fill, one for the rim and a bold line for the best of the two, with the threshold of 20 drawn across.

Start with "Fill only" and drag the effects slider from 0 to 8. Around 6 the circle on the left dissolves into the glow, and at the same moment the fill line on the right crosses the threshold. Now switch to "Fill + rim" and drag again. The circle stays readable the whole way, and the bold line never drops below 40. Then press "Grayscale". The circle is still readable, because the model is about value, not hue.

### Cross-game recognition

The model has three levers: lower the stacked brightness `N × e`, add a dark part to the signal, or keep signals out of the effect layer entirely. Shipped games pull all three.

**World of Warcraft, Spell Density (patch 9.0.1 onward, reworked in 11.2.0).** The setting lowers `N`, the number of other players' effects drawn. Its lowest setting is named Essential, which tells you the design intent. Effects that carry gameplay information stay, and decoration goes. In the model, this keeps `B` away from 100 so light signals keep their headroom.

**Guild Wars 2, Hide Ally Visual Effects and Effect LOD (current game).** The first option has four settings: Hide None (the default), Only Show Squad, Only Show Party and Hide All. NPC effects, and enemy player effects in PvP, are always shown. That split is the signal-noise split written into a menu. Allies mostly make noise for you, and enemies make signals. The separate Effect LOD option limits particle detail, which is a way of lowering `e` rather than `N`. The Guild Wars 2 Wiki also records a warning. As of June 2023, hiding ally effects could also hide some real mechanics, including the green circle players must share in the Samarog raid encounter. A filter can only protect signals if every signal is tagged as one.

**High-visibility clothing (outside games).** Safety vests built to ISO 20471 or ANSI/ISEA 107 combine two materials. The fluorescent yellow or orange fabric is for daylight. The retroreflective bands, which bounce headlight beams back to the driver, are for the dark. Neither works everywhere, so the garment carries both. That is the two-tone rule with the worst case covered by a second material.

**Your reaction budget (GD101 week 12).** The GD101 telegraph budget has a term `t_hidden` for time a warning is on screen but covered by effects. This lecture's model says when that hiding happens: whenever the telegraph's contrast drops under the threshold. Each second a telegraph spends below 20 contrast is a second of `t_hidden`.

Four places, one principle. A signal must keep contrast against every background it will meet, and a bright background has no room left for a bright signal.

### Eyes-open design judgment

- **Two-tone telegraphs cost almost nothing.** A thin dark rim or a dark inner band doubles the conditions in which a telegraph works. Consider it the default for any warning that can appear under player effects.
- **Filters need tags.** Density options and hide-effect options only work if every effect is marked as signal or noise in the data. Decide that at authoring time, per effect, and test it. The Guild Wars 2 case shows what happens when a mechanic is built from the same parts as decoration.
- **Turning noise down is the player's choice, not your fix.** A menu option helps players who find it. Your default settings should already keep the boss readable with a full group. Test at maximum density before you ship.
- **Dark rims have their own worst case.** A rim works against light backgrounds and weakens on dark ones. In a night zone or a dark cave, the light fill carries the signal. That is why you want both parts, not a switch from one to the other.
- **The numbers here are a model.** Real engines tone-map bright values instead of hard clipping, and real effects vary across the screen. Measure your own screenshots (the lab shows how). The shape of the result, a light signal fading on a bright screen, holds across all of these details.

### Check yourself (worked example)

1. A floor has value 45 and each effect adds 15. How many overlapping effects make an additive fill with `t = 35` fail the 20 threshold?
2. What rim opacity `α` makes the two-tone worst case at least 30 when `t = 50`?
3. On a dark cave floor at value 10 with no effects, which part of a two-tone telegraph carries the signal, and what is its contrast with `t = 40`, `α = 0.8`?

<details>
<summary>Answers</summary>

1. The fill fails when `100 − B < 20`, so when `B > 80`. `B = 45 + 15N`, so `N = 3` gives 90. With 2 effects `B = 75` and headroom 25 still passes. It fails at 3 effects.
2. Need `100α / (1 + α) ≥ 30`, so `100α ≥ 30 + 30α`, `70α ≥ 30`, `α ≥ 0.43`. Since `t = 50` is above 30, the rim term sets the worst case.
3. The fill: `min(40, 100 − 10) = 40`. The rim gives only `0.8 × 10 = 8`, which fails on its own.

</details>

## 3. A toolkit for readable effects

The headroom model explains the most common failure. The rest of readability comes from a handful of habits. Each one maps onto something you learned earlier in the course.

### Reserve a value band for danger

In week 1 you split a palette into value bands. Do the same for effects. Decide that player effects stay in the middle bands (for example L* 35 to 75) and that the top and bottom bands belong to warnings. A telegraph with a near-white core and a near-black rim then contrasts with any player effect by construction. The discipline is on the effects team, not the telegraph: every new spell must stay inside its band.

### Reserve a hue family and a shape for danger

Hue is weaker than value (week 4), but it still helps once value is right. Many games use a consistent warm color for enemy attacks and cool or neutral colors for friendly effects. Pick one family and never use it for decoration. Shape does the same job with more force. Week 2 taught that sharp, angular shapes read as dangerous. Hard-edged geometric telegraphs (circles, cones, lines with crisp borders) look different from the soft, round, wispy shapes of most spell effects, even when both are the same brightness.

### Draw order decides who covers whom

Renderers draw in passes. Unity's render queues, for example, draw opaque geometry first, then alpha-tested geometry, then transparent objects, then an overlay pass for things that must appear on top of everything. Ground telegraphs are often decals projected onto the floor, which puts them early, and effects are transparent, which puts them later. By default, then, every spell paints over every warning. You can change this: draw telegraphs in a later pass, or make effects fade where they overlap a telegraph. Both are cheap, and both need a decision from someone who knows the warning matters.

### Scale effects with crowd size

A spell that looks right in a solo test is too bright in a group of twenty. Some games, like the density options above, drop other players' effects automatically as the count rises. Others reduce the brightness `e` of effects that do not belong to the viewer. Your own spells can stay spectacular, because you know you cast them. Other players' spells matter less to you and can be dimmer.

### Keep motion for signals

The eye is drawn to change. A pulsing ring or a filling bar says "something is about to happen" before the player has read its shape. If every idle effect also pulses, motion stops meaning anything. Keep the fastest and most regular motion for signals, and let decoration drift slowly.

### Test like a player

- **The grayscale test.** Convert a screenshot to grayscale. If you cannot find the telegraph, the value design has failed, whatever the colors look like.
- **The full-group test.** Record the fight with the maximum number of players using the flashiest abilities. Pause on the busiest frame and find every telegraph.
- **The squint test.** Blur the screenshot or squint at it from across the room. Whatever you still see first is what a panicked player sees first.

## In-class activity (25 minutes)

Work in groups of three. Each group gets a printed grayscale screenshot of a busy fight from a game of your choice (take it yourself and cite the game and version; do not use marketing art).

1. Circle every effect on the page. Label each one S (signal) or N (noise). (8 min)
2. For each signal, estimate its value and the value of the background around it using a gray step card from week 1. Compute the contrast. Mark any signal below 20. (8 min)
3. For each failing signal, name one fix from section 3 (value band, two-tone, draw order, density, shape) and sketch it on the printout. (7 min)
4. Post the sheet on the wall. Each group reads another group's sheet and finds one signal they missed. (2 min)

Expected output: an annotated printout with every effect labeled, contrast numbers for every signal, and at least one sketched fix.

## Common misconceptions

- **"Brighter warnings are more visible."** Only while there is headroom. On a white-out a brighter additive warning adds nothing. A darker part is what survives.
- **"Red means danger, so a red telegraph is enough."** Hue does nothing if value is equal. A red circle at the same value as the floor disappears in grayscale, and for many color-blind players (week 12). Get the value right first.
- **"Players can turn effects down, so clutter is their problem."** Options help, but your defaults set the experience for most players. They also only work if your data separates signals from decoration.
- **"More particles make a telegraph clearer."** Particles in a telegraph are more noise if they use the same blending and colors as spells. A clean, hard-edged shape with a two-tone edge usually reads better than a busy one.

## Check yourself

1. A boss arena floor is L* 20. Player effects add 12 points each. You want an additive fill telegraph to stay readable (contrast at least 20) with up to 5 overlapping effects. What is the largest `t` that helps, and does any `t` save it at 6 effects?
2. A designer proposes making telegraphs fully opaque (alpha 1) pure white disks drawn in the overlay pass. Compute their contrast against backgrounds of 30 and 100. What is lost?
3. Explain in two sentences why a density option that removes 50% of other players' effects helps a light telegraph more on a bright floor than on a dark one.
4. Your effects team proposes a new ultimate ability with an average `e = 30`. Using the section 2 numbers (`V_floor = 30`, `t = 40`, `α = 0.8`), how many of these overlapping effects does it take to break a fill-only telegraph? Does the two-tone version still hold?

<details>
<summary>Answers</summary>

1. At 5 effects `B = 20 + 60 = 80`, headroom 20. The fill contrast is `min(t, 20)`, so any `t ≥ 20` reaches exactly 20 and a larger `t` adds nothing. At 6 effects `B = 92` and headroom is 8, so no value of `t` reaches 20.
2. An opaque white disk has value 100 whatever is behind it. Against 30 the contrast is 70. Against 100 it is 0. It also hides the floor and anything standing in the marked area, and it has the same white-out failure as the fill. The fix is a dark rim, not a brighter disk.
3. On a bright floor the background is already near the cap, so removing effects frees headroom that the light telegraph can use. On a dark floor the background is far from the cap either way, so the telegraph already had room and gains little.
4. `B = 30 + 30N`. The fill fails when `B > 80`, so at `N = 2` (`B = 90`). The two-tone worst case is `min(40, 44.4) = 40` whatever the background, so the two-tone telegraph still holds. The new ability hurts every fill-only signal in the game, which is a reason to put it inside the effects value band.

</details>

## Lab hook

[Lab 10, the chaos plate test](../labs/lab10.md). You generate identical "chaos plates" (a floor with 0, 2, 4 and 8 stacked additive effects), paint a telegraph for an invented boss attack on each plate, and measure its contrast with the provided probe script. The deliverable is a four-plate sheet in color and grayscale, the probe numbers, and a one-page rationale. It counts toward the weekly studies grade.

## Sources

- Solarski, C. (2012). *Drawing Basics and Video Game Art*. Watson-Guptill. Course reading on value and contrast.
- Khronos Group, OpenGL 4 Reference Pages, `glBlendFunc`. The blended result is the sum of source and destination terms, capped at the framebuffer's maximum per channel. https://registry.khronos.org/OpenGL-Refpages/gl4/html/glBlendFunc.xhtml
- Warcraft Wiki, "CVar graphicsSpellDensity". Settings Essential, Some, Half, Most, Dynamic (default) and Everything; added in patch 9.0.1 (2020-10-13). Also "Console variables", which lists `RAIDspellClutter` (Spell Density) from patch 6.0.2. https://warcraft.wiki.gg/wiki/CVar_graphicsSpellDensity
- Warcraft Wiki, "Patch 11.2.0" (released August 5, 2025). Patch notes state the Spell Density feature was revamped in this patch to increase visual clarity. Also "Hotfixes/2025 Archive" on reduced visual density at the Reduced and Essential settings.
- Guild Wars 2 Wiki, "Options" (current game, page revision of August 2026). Hide Ally Visual Effects settings (Hide None, Only Show Squad, Only Show Party, Hide All), NPC and enemy player effects always shown, the Effect LOD option, and the June 2023 note that hiding ally effects could hide mechanics such as the green circle in the Samarog encounter. https://wiki.guildwars2.com/wiki/Options
- Unity Manual, "SubShader tags" (render queue section). Background, Geometry, AlphaTest, Transparent and Overlay queues in draw order. https://docs.unity3d.com/Manual/SL-SubShaderTags.html
- Wikipedia, "High-visibility clothing". Fluorescent material for daylight, retroreflective material for low light; ISO 20471 and ANSI/ISEA 107.
- CIE L* formula and the value gap of 20: AR101 week 1.

## Interactive spec: examples/w10-telegraph-headroom.html

**The one insight:** a light signal can only be as bright as the headroom left above the background, so stacked glowing effects erase it. A dark rim does the opposite, and a telegraph with both never drops below `min(t, 100α/(1+α))`.

**Layout.** Two panels. Mobile: stacked, arena first. Desktop (≥ 960px): arena left (about 55% width), chart right.

1. **Arena (canvas or SVG).** A square top-down floor filled with the gray value `V_floor` (render every value `V` as the sRGB gray whose L* equals `V`; convert with `Y = ((V+16)/116)^3` for `V > 8`, else `V × 27/24389`, then sRGB-encode). A generic boss marker (a dark hexagon, no art) at top center. A telegraph circle of radius 22% of the panel, centered below the boss. `N` soft round effect blobs (radial gradient, value added `e` at the center, fading to 0 at the edge, radius 18% of the panel) placed so all `N` overlap the telegraph's rim area; in the overlap region the background equals the model's `B(N)`. Composite in value points: `pixel = min(100, V_floor + sum of blob contributions)`. Telegraph fill: add `t` to the background inside the circle, capped at 100. Rim: a ring 3% of panel width, darkened to `(1 − α) × background`. Optional "Grayscale" toggle desaturates the whole panel (it is already mostly gray; the effect blobs get a warm tint `hsl(35, 70%, …)` in color mode with the same value).
2. **Chart (SVG).** x = overlapping effects N from 0 to 10, y = contrast from 0 to 100. Three lines: fill `min(t, 100 − B)` (ochre, dashed), rim `α × B` (steel, dashed), best of the two (ink, solid, thicker). Horizontal threshold line at 20 (blood color, labeled "readable"). A vertical marker at the current N. Shade the region where the currently selected style is below 20.

**Readout (always visible, copyable text).** `B`, headroom `100 − B`, fill contrast, rim contrast, contrast of the selected style, verdict "readable" or "lost", and the worst case `min(t, 100α/(1+α))` for the two-tone style.

**Controls.**
- Effects overlapping N: 0 to 10, step 1, default 6.
- Floor value `V_floor`: 0 to 90, step 5, default 30.
- Value per effect `e`: 0 to 30, step 1, default 10.
- Fill strength `t`: 0 to 60, step 5, default 40.
- Rim opacity `α`: 0 to 1, step 0.05, default 0.8.
- Style: radio "Fill only", "Rim only", "Fill + rim" (default "Fill only" so the first screen shows the failure).
- Toggle "Grayscale". Button "Reset".
All controls keyboard operable with visible focus; sliders update both views immediately.

**Test values (builder must reproduce, `V_floor = 30`, `e = 10`, `t = 40`, `α = 0.8`).**

| N | B | Fill | Rim | Best |
|---|---|---|---|---|
| 0 | 30 | 40 | 24 | 40 |
| 2 | 50 | 40 | 40 | 40 |
| 4 | 70 | 30 | 56 | 56 |
| 5 | 80 | 20 | 64 | 64 |
| 6 | 90 | 10 | 72 | 72 |
| 7 | 100 | 0 | 80 | 80 |

Two-tone worst case readout: 40.0 (the rim-fill crossing is 44.4). With `α = 0.5` the worst case reads 33.3. With `V_floor = 45`, `e = 15`, `t = 35`, fill-only verdict flips to "lost" at N = 3.

**First screen.** N = 6, "Fill only": the circle is barely visible in the glow, the fill line sits at 10 under the threshold, and a caption reads "Six spells. The warning is still there. You can't see it." Switching to "Fill + rim" restores the circle without moving any slider.

**Accessibility and style.** Shared palette from `templates/interactive-tokens.css`, both color schemes (the arena itself stays in gray values in both). Lines are distinguished by dash pattern and direct labels as well as color. With reduced motion, blobs are static (no flicker). No game art, logos or characters.
