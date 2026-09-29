# AR101 · Week 12 — Accessibility: Color-Blindness and Contrast

**Why this matters:** In any 20-player raid group, the odds are high that at least one player sees red and green very differently from you. If your boss's deadly zone is "the red one" and the safe zone is "the green one", that player is guessing. This week you learn to see your art through their eyes with a simulator, and to design warnings that work for everyone without a special mode.

**You will be able to:**
- Simulate protanopia, deuteranopia and tritanopia on any color with a published matrix, and read the result.
- Compute the value gap (ΔV) and the total color difference (ΔE) between two colors before and after simulation, and explain why ΔV survives while hue differences collapse.
- Redesign a raid telegraph so that its critical pairs pass ΔV ≥ 20 and the 3:1 contrast ratio for every type of color vision.
- Critique a game's color-blind options and choose between a palette swap, a filter and redundant shape coding.

**Before class:** Machado, Oliveira and Fernandes (2009), "A Physiologically-based Model for Simulation of Color Vision Deficiency", sections 1 and 3 (skim the physiology, read the results figures). The Game Accessibility Guidelines entry "Ensure no essential information is conveyed by a fixed colour alone" (one page). Reread section 3 of AR101 week 1 on the contrast ratio.

**Prerequisites from earlier courses:** None outside AR101. You need linear RGB, L* and the value gap ΔV with its threshold of 20 from [AR101 week 1](w01-seeing-like-an-artist-value-before-color.md), hue and value as separate properties from [AR101 week 4](w04-color-theory-hue-saturation-value.md), and the two-tone telegraph from [AR101 week 10](w10-readability-in-chaos-vfx-and-telegraphing.md). Later, [UX201 week 11, accessibility guidelines](../../UX201-game-ux-and-player-psychology/lectures/w11-accessibility-guidelines.md) covers text contrast, subtitles and the wider accessibility checklist, [MMO306 week 5, telegraphing and readability](../../MMO306-content-design-at-scale-quests-dungeons-and-raid/lectures/w05-telegraphing-and-readability.md) designs raid telegraphs as encounter mechanics, and [MMO306 week 14, accessibility in group content](../../MMO306-content-design-at-scale-quests-dungeons-and-raid/lectures/w14-accessibility-in-group-content.md) audits whole fights for cue coverage across a group. Next semester, [AU101 week 13](../../AU101-audio-for-games/lectures/w13-accessibility-subtitles-and-visual-sound-cues.md) covers the audio side: subtitles and visual sound cues. This week stays with the artist's part of the problem, the colors and values themselves.

**Interactive:** [examples/w12-colorblind-telegraph.html](../examples/w12-colorblind-telegraph.html). Keep it open during section 2.

---

## 1. How color vision varies

Most people have three kinds of **cone cells** in the retina. Each kind responds most to a different band of wavelengths, roughly long (L, reddish), medium (M, greenish) and short (S, bluish). Your brain compares the three signals. Color is that comparison.

**Color vision deficiency (CVD)** means one kind of cone is missing or shifted. There are three main families, named after the cone involved.

- **Protan** (L cones). Reds look darker and closer to greens and browns.
- **Deutan** (M cones). Reds and greens become hard to tell apart, without the darkening of reds.
- **Tritan** (S cones). Blues and greens, and yellows and pinks, become hard to tell apart. This family is rare.

Each family comes in two strengths. A person with **dichromacy** (protanopia, deuteranopia, tritanopia) has only two working cone types. A person with **anomalous trichromacy** (protanomaly, deuteranomaly, tritanomaly) has three, but one is shifted, so the effect is milder. The mild forms are more common than the strong ones.

How many players is that? The US National Eye Institute puts it at about 1 in 12 men, and the UK charity Colour Blind Awareness at about 1 in 12 men and 1 in 200 women. Red-green types (protan and deutan) are by far the most common. The chance that a group contains at least one affected player grows fast with group size. For a group of `n` men, it is `1 − (11/12)^n`.

| Group | Chance of at least one player with CVD |
|---|---|
| 5 men (a dungeon party) | 35% |
| 10 men | 58% |
| 10 men and 10 women | 60% |
| 20 men | 82% |
| 40 men (a large classic-era raid) | 97% |

For raid design, a color-blind player is not an edge case. They are in most of your groups.

Notice what CVD does *not* change much: the value of a color. Value comes mostly from how much light reaches all the cones together, and it survives when one cone type is missing. The hue comparison is what breaks. You already know a tool that measures value and ignores hue, the grayscale test from week 1. This lecture makes that connection exact.

## 2. Worked example: the raid telegraph through four pairs of eyes

### The hook

League of Legends added a Colorblind Mode in patch V1.0.0.132, released on January 17, 2012. The patch notes said it improved health bars and various effects and animations for colorblind players. Overwatch added nine colorblind-friendly team colors in its October 9, 2018 patch, with separate choices for enemy and friendly UI. Splatoon, a game about two teams painting the floor in two ink colors, has a Color Lock option that fixes the team colors to a pair chosen to be easy to tell apart.

All three are fixes shipped after launch for a problem that was in the art from day one. Here is that problem in a raid, with numbers, and the fix that avoids needing a special mode.

### The model

To see a color as a dichromat does, multiply its linear RGB values by a 3 × 3 matrix. Machado, Oliveira and Fernandes (2009) derived these matrices from a model of how cone responses combine. Their severity 1.0 matrices simulate full dichromacy, the strongest case.

```
[R', G', B'] = M_type × [R, G, B]      (linear RGB, then clip each to 0..1)

M_protan = | 0.152286   1.052583  -0.204868 |
           | 0.114503   0.786281   0.099216 |
           |-0.003882  -0.048116   1.051998 |

M_deutan = | 0.367322   0.860646  -0.227968 |
           | 0.280085   0.672501   0.047413 |
           |-0.011820   0.042940   0.968881 |

M_tritan = | 1.255528  -0.076749  -0.178779 |
           |-0.078411   0.930809   0.147602 |
           | 0.004733   0.691367   0.303900 |
```

- `R, G, B` are the linear-light channels from week 1, found by undoing the sRGB curve.
- `M_type` is the matrix for one type of dichromacy.
- `R', G', B'` are the linear channels of the color the simulated viewer sees.

Then measure two differences between any pair of colors, before and after simulation.

```
ΔV = |L*₁ − L*₂|                               value gap (week 1)
ΔE = √( (L*₁ − L*₂)² + (a*₁ − a*₂)² + (b*₁ − b*₂)² )   total color difference
```

`L*`, `a*` and `b*` are the three coordinates of **CIELAB**, a color space built so that equal distances look roughly equally different. `L*` is the value you know. `a*` runs from green to red and `b*` from blue to yellow. `ΔE` (the 1976 CIELAB difference) counts value and hue together. A ΔE around 2 is about the smallest difference most people notice side by side. Differences in the tens are obvious.

The model makes one prediction you can test: **simulation shrinks ΔE a lot along the axis the viewer has lost, and moves ΔV only a little.** So a pair of colors separated mainly by hue collapses. A pair separated by value holds.

### Numbers you can check

A raid boss slams the floor. The designer paints the danger zone red, the safe zone green, on a mossy stone floor.

- Floor: sRGB (96, 112, 72).
- Danger zone: (200, 48, 40).
- Safe zone: (64, 168, 72).

Here is each color after simulation, in sRGB and with its L*.

| Viewer | Floor | Danger (red) | Safe (green) |
|---|---|---|---|
| Typical vision | (96, 112, 72), L* 45.0 | (200, 48, 40), L* 45.0 | (64, 168, 72), L* 61.3 |
| Protanopia | (116, 107, 69), L* 45.2 | (95, 85, 37), L* 36.2 | (171, 153, 63), L* 63.3 |
| Deuteranopia | (114, 106, 74), L* 44.8 | (133, 118, 33), L* 49.6 | (158, 144, 79), L* 59.8 |
| Tritanopia | (98, 108, 102), L* 44.8 | (220, 0, 48), L* 46.3 | (42, 164, 147), L* 60.8 |

Look at the typical-vision row first. The red and the floor have the same L*, 45.0. Nobody planned that; a saturated red and a mid-dark moss just happen to carry the same value. Typical viewers see the zone anyway, because its hue is so different. That is a warning sign you could have caught in week 1: in grayscale, this danger zone is invisible.

Now the differences.

| Viewer | Danger vs floor: ΔV | ΔE | Danger vs safe: ΔV | ΔE |
|---|---|---|---|---|
| Typical vision | 0.0 | 75.2 | 16.3 | 109.5 |
| Protanopia | 9.0 | 11.1 | 27.1 | 33.5 |
| Deuteranopia | 4.8 | 27.7 | 10.2 | 14.5 |
| Tritanopia | 1.5 | 86.4 | 14.5 | 117.4 |

Read the danger-versus-floor columns. For typical vision, ΔE is 75, a huge difference that is entirely hue (ΔV is 0). For a protanope, ΔE drops to 11. The red has turned into a dark olive (95, 85, 37) sitting on a similar olive floor. For a deuteranope, ΔE drops to 28, and the danger-versus-safe difference falls from 110 to 15. The two zones are now two shades of khaki. For a tritanope, very little changes, because the red-green axis is intact.

Meanwhile ΔV barely moved. It was small from the start and stayed small. The protan red got darker, which gave it a ΔV of 9, still under the week 1 threshold of 20. **What survives simulation is the value gap you designed, and this design had none.**

You can run the whole calculation:

```python
# Machado, Oliveira & Fernandes (2009), severity 1.0, applied to linear RGB
CVD = {
    "protan": [[0.152286, 1.052583, -0.204868],
               [0.114503, 0.786281, 0.099216],
               [-0.003882, -0.048116, 1.051998]],
    "deutan": [[0.367322, 0.860646, -0.227968],
               [0.280085, 0.672501, 0.047413],
               [-0.011820, 0.042940, 0.968881]],
    "tritan": [[1.255528, -0.076749, -0.178779],
               [-0.078411, 0.930809, 0.147602],
               [0.004733, 0.691367, 0.303900]],
}


def lin(c):                      # sRGB 0-255 -> linear light 0-1 (week 1)
    c = c / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def simulate(rgb, kind):         # linear RGB seen by a dichromat, clipped to 0-1
    v = [lin(c) for c in rgb]
    if kind == "normal":
        return v
    return [min(1.0, max(0.0, sum(m * x for m, x in zip(row, v)))) for row in CVD[kind]]


def lab(v):                      # linear RGB -> CIELAB (D65 white)
    r, g, b = v
    xyz = (0.4124 * r + 0.3576 * g + 0.1805 * b,
           0.2126 * r + 0.7152 * g + 0.0722 * b,
           0.0193 * r + 0.1192 * g + 0.9505 * b)
    f = [t ** (1 / 3) if t > 216 / 24389 else (24389 / 27 * t + 16) / 116
         for t in (xyz[0] / 0.95047, xyz[1], xyz[2] / 1.08883)]
    return 116 * f[1] - 16, 500 * (f[0] - f[1]), 200 * (f[1] - f[2])


def diff(a, b):                  # (value gap dV, total difference dE)
    dl = [p - q for p, q in zip(a, b)]
    return abs(dl[0]), sum(d * d for d in dl) ** 0.5


floor, red, green = (96, 112, 72), (200, 48, 40), (64, 168, 72)
print("mode     red/floor dV  dE    red/green dV  dE")
for kind in ("normal", "protan", "deutan", "tritan"):
    f, r, g = (lab(simulate(c, kind)) for c in (floor, red, green))
    (v1, e1), (v2, e2) = diff(r, f), diff(r, g)
    print(f"{kind:<8} {v1:12.1f} {e1:5.1f} {v2:13.1f} {e2:5.1f}")
```

It prints the second table: `normal 0.0 75.2 16.3 109.5`, then the protan, deutan and tritan rows.

### The fix: put the difference in value, then add shape

Keep the warm color if you like it. Change the value structure, using the two-tone telegraph from week 10.

- Danger fill: a light orange, (255, 176, 48).
- Danger rim: a near-black, (32, 16, 16), a few pixels wide around the zone.
- Safe zone: no fill at all. A dashed light ring with inward-pointing chevrons, so it differs from the danger zone in shape rather than in color.

| Viewer | Fill L* | Fill ΔV vs floor | Rim L* | Rim ΔV vs floor | Rim contrast ratio vs floor |
|---|---|---|---|---|---|
| Typical vision | 77.6 | 32.6 | 6.5 | 38.5 | 3.42 : 1 |
| Protanopia | 73.3 | 28.1 | 5.6 | 39.6 | 3.50 : 1 |
| Deuteranopia | 80.1 | 35.3 | 7.0 | 37.8 | 3.36 : 1 |
| Tritanopia | 74.3 | 29.5 | 6.4 | 38.3 | 3.39 : 1 |

Every ΔV clears 20 for every viewer. The rim also clears the WCAG 2.1 minimum of 3:1 for graphical objects that users need to understand the content (success criterion 1.4.11), which week 1 showed is roughly a ΔV of 30 to 36 near mid values. The fill alone sits between 2.57 and 3.19 against the floor, so it passes our game threshold but meets the web's only for deuteranopia. The rim is what makes the design pass both, which is one more reason the two-tone rule from week 10 earns its place.

The danger-versus-safe problem is solved differently. The two zones no longer rely on color at all. One is a filled, dark-rimmed area. The other is an empty dashed ring with arrows. A player who sees no color, or who is looking at the fight through a haze of effects, can still tell them apart. This is **redundant coding**: the same message sent through more than one channel (value, shape, pattern, motion or sound), so losing one channel does not lose the message.

### A visual you can move

Open [`examples/w12-colorblind-telegraph.html`](../examples/w12-colorblind-telegraph.html). It shows a top-down raid arena drawn in simple shapes: a boss marker, the danger zone and the safe zone on the stone floor. The left panel is typical vision. The right panel is the same arena through the simulator you choose. Under them, a table lists ΔV, ΔE and contrast ratio for the critical pairs, with a pass or fail mark for each.

Start with the "Red / green" preset and set the right panel to Deuteranopia. On the left the zones are obvious. On the right they are two brownish shapes on a brownish floor, and the table shows ΔE for danger-versus-safe falling from 109.5 to 14.5. Now press "Grayscale", which turns both panels to luminance gray. The typical-vision arena looks just as broken as the simulated one. Load "Value + shape". Every ΔV against the floor now passes in all four modes, and the rim passes 3:1 in all four as well. Two marks stay red on purpose. The fill alone reaches 3:1 only for deuteranopia (2.57 to 3.19 across the modes), and danger versus safe still has a ΔV under 20 (13.0 to 19.6). The table marks that last row "shape differs", because the two zones are now told apart by shape, not by value or color. Try the "Four-up" view to see all simulators at once.

### Cross-game recognition

**League of Legends (Colorblind Mode, since patch V1.0.0.132, January 2012).** The mode changes how your own health bar and a range of effects are drawn. The League of Legends Wiki shows a separate colorblind version of the player's own health bar. In this lecture's terms, the default design relied on a hue difference that collapses for red-green viewers, and the mode moves the difference to where it survives.

**Overwatch (patch of October 9, 2018).** Players choose enemy and friendly UI colors from nine colorblind-friendly options, covering nameplates, HUD, health bars and hero outlines. This is a **palette swap**: instead of transforming the whole screen, the game changes the few colors that carry gameplay meaning. It works because only a small set of colors must be told apart, and players can pick a pair that separates in their own vision.

**Splatoon and Splatoon 2 (Color Lock).** The team ink colors normally change from match to match. Color Lock fixes them. According to Inkipedia, the first game locks online battles to blue against orange, and Splatoon 2 locks matchmaking battles to yellow against dark purple. Run a similar pair through the model, for example yellow (250, 220, 40) against dark purple (70, 30, 110). Its ΔV is 66 for typical vision and stays between 63 and 67 in all three simulations. It runs along the blue-yellow axis that red-green viewers keep, and it is a light-against-dark pair, so it survives on both counts. A red (220, 40, 40) against a green (40, 180, 60), by comparison, has a ΔV of 16 and falls to a ΔE of 12 for deuteranopia.

**The Game Accessibility Guidelines.** Their basic-level guideline says not to convey essential information by a fixed color alone. It recommends presets for the common types plus custom color choice, and warns that full-screen filters can feel punitive to the players they are meant to help. That is the same ranking this lecture reaches: first design value and shape so no mode is needed, then offer palette swaps for the few gameplay colors, and use full-screen filters last if at all.

Four examples, one principle. Color can name things, but it cannot be the only thing that separates them. Value and shape carry the message for every viewer.

### Eyes-open design judgment

- **Design for everyone first, then add modes.** A telegraph that passes ΔV ≥ 20 for all four simulations needs no special mode. A mode is a fix for a design you already shipped, and players have to find it.
- **Palette swaps beat full-screen filters.** A filter that shifts every color on screen can make the rest of the art look wrong and still fail to separate the colors that matter. Swap only the gameplay-critical colors, and let players choose them.
- **Hue is still useful.** Warm danger and cool safety help typical viewers and many anomalous trichromats. Keep hue as a second channel, never the only one.
- **Simulators are models.** The severity 1.0 matrices show the strongest case. Most affected players have milder anomalous trichromacy and will see more than the simulation shows. If your design passes at full severity, it passes for them too. Test with real players when you can.
- **Contrast has a cost in mood.** A black rim and a near-white fill are loud. In a quiet, painterly zone, you may accept a thinner rim or a pattern instead. Decide it with the numbers in front of you, not by removing the rim because it "looks harsh".

### Check yourself (worked example)

1. A designer changes only the floor, to a darker stone of L* 25 in every simulation. What are the red danger zone's ΔV values now for typical vision and for protanopia? Does the fix work?
2. Why does simulation barely change the tritanope's view of the red-and-green design, and why is that no comfort?
3. A telegraph passes ΔV ≥ 20 against the floor in all four modes, but its danger and safe zones are both filled circles in different hues. What is still wrong, and what is the cheapest fix?

<details>
<summary>Answers</summary>

1. Typical vision: `|45.0 − 25| = 20.0`, right at the threshold. Protanopia: `|36.2 − 25| = 11.2`, which fails, because the protan red darkens toward the new floor. Darkening the floor moves the problem rather than solving it. A light fill or a dark rim fixes it for everyone.
2. Tritanopia affects the blue-yellow comparison. The red-green axis is intact, so the design looks almost the same. But tritanopia is the rarest type. The red-green types, for which the design fails, are the common ones.
3. Danger and safe are separated only by hue, so they may merge for some viewers even though both stand out from the floor. Change one zone's shape or pattern (an empty ring, arrows, stripes) or give the two zones a value gap of at least 20 between them.

</details>

## 3. Contrast beyond color-blindness

Color-blindness is one reason a player may miss a color difference. There are others, and the same fix covers them.

- **Low vision and older eyes.** Contrast sensitivity falls with age and with many eye conditions. A ΔV that works for a 20-year-old tester may not work for a 60-year-old player.
- **Screens and rooms.** A cheap monitor, a phone in sunlight, a TV with its brightness turned down or a projector in a lit classroom all compress contrast. Value gaps shrink. Hue differences shrink even more.
- **Busy scenes.** Week 10 showed that effects stacked on top of a telegraph eat its contrast. A color-blind player in a busy fight loses both channels at once.

This is why accessibility standards use **contrast ratio**, which you met in week 1: `(Y_light + 0.05) / (Y_dark + 0.05)`, where `Y` is relative luminance. WCAG 2.1 asks for at least 3:1 for graphical objects that users need in order to understand the content, such as icons, chart lines and, in our case, a boss's danger zone. Text has stricter requirements, which UX201 week 11 covers.

A few habits make contrast easy to keep.

- **Check pairs, not colors.** No color is accessible by itself. Write down the pairs that must be told apart (telegraph and floor, enemy and background, health bar and its empty track) and test each pair.
- **Test on every floor.** A telegraph that passes on grass may fail on sand. List the floors where the attack can happen and test on all of them, or give the telegraph a rim so it carries its own background.
- **Use value steps you can name.** If your palette (week 5) has value bands, give gameplay-critical colors their own band and keep decoration out of it.
- **Offer, but don't depend on, options.** Brightness sliders, colorblind palettes and effect-density settings help players adjust. Your defaults should already pass.

## 4. A color-blind check you can run every week

Build this into your routine from now on. It takes five minutes per screen.

1. **Grayscale first.** Convert the screenshot to luminance grayscale (week 1). If any critical element vanishes, fix value before anything else.
2. **Simulate the three types.** Run the image through protan, deutan and tritan simulation. The lab gives you a script. Many image editors also have a proofing mode for color blindness.
3. **Measure the critical pairs.** For each pair, record ΔV and contrast ratio in all four modes. Mark anything under ΔV 20 or 3:1.
4. **Check the shape channel.** For any two elements that mean different things, ask whether they would still be different if the screen were grayscale and blurred. If not, add shape, pattern or motion.
5. **Write it down.** Record the results in your style bible (week 13) so the next artist knows which pairs are critical and what the numbers must be.

## In-class activity (25 minutes)

Groups of three. Each group gets a printed page of six invented game UI and world elements in color: a health bar, a mana bar, a friendly and an enemy nameplate, a loot beam and a ground telegraph, each on its typical background. The instructor also hands out the same page run through deuteranopia simulation, face down.

1. Before turning the second page over, predict which pairs will merge for a deuteranope. Write your predictions. (5 min)
2. Turn it over. Score your predictions. (3 min)
3. For each element, measure the L* of it and its background with the class color picker and compute ΔV. Compare ΔV with which pairs merged. (10 min)
4. Redesign the worst element on paper so it passes ΔV ≥ 20 and uses one extra channel (shape, pattern or motion). (7 min)

Expected output: a prediction sheet with a score, a ΔV table for all six elements, and one redesigned element with its new ΔV.

## Common misconceptions

- **"Color-blind people see in black and white."** Almost all see color, just along fewer axes. Seeing no color at all is rare. That is why red-green is the problem and blue-yellow usually is not.
- **"A colorblind mode solves it."** A mode fixes one set of colors for players who find it. A design that passes in all simulations needs no mode.
- **"If it looks different to me, it is different."** Typical viewers see hue differences that vanish for many players. Only ΔV and shape are safe to rely on, so measure them.
- **"Red means danger for everyone."** For a protanope, saturated red becomes a dark, dull olive. It may carry less alarm than a light yellow.

## Check yourself

1. Compute the chance that a 25-man raid of men contains at least one player with CVD, using 1 in 12.
2. The linear RGB of a red is (0.58, 0.03, 0.02). Multiply it by `M_deutan` and give the three resulting linear values, rounded to three decimals. Which channel changed most?
3. An enemy nameplate is (220, 60, 60) and a friendly one is (60, 200, 90), both on a dark HUD. Using the lecture's results for a similar red and green, predict whether a deuteranope can tell them apart by color, and propose a fix that does not change either color.
4. You must make a telegraph pass the 3:1 contrast ratio against a floor of relative luminance Y = 0.145. What luminance must a darker rim have at most? What luminance must a lighter fill have at least? Can any pure red (maximum Y = 0.2126) be the lighter part?

<details>
<summary>Answers</summary>

1. `1 − (11/12)^25 ≈ 1 − 0.114 = 0.886`, about 89%.
2. Row 1: `0.367322 × 0.58 + 0.860646 × 0.03 − 0.227968 × 0.02 = 0.213 + 0.026 − 0.005 = 0.234`. Row 2: `0.280085 × 0.58 + 0.672501 × 0.03 + 0.047413 × 0.02 = 0.162 + 0.020 + 0.001 = 0.184`. Row 3: `−0.011820 × 0.58 + 0.042940 × 0.03 + 0.968881 × 0.02 = −0.007 + 0.001 + 0.019 = 0.014`. Red fell from 0.58 to 0.234 and green rose from 0.03 to 0.184: the red-green difference nearly vanished.
3. The lecture's red (220, 40, 40) and green (40, 180, 60) fall to ΔE 12 for deuteranopia, so these two will be hard to separate by color. Keep the colors and add shape: a different nameplate frame (spiked for enemies, rounded for friends, as in week 2), or an icon.
4. Darker: `(0.145 + 0.05) / (Y + 0.05) ≥ 3` gives `Y ≤ 0.015`. Lighter: `(Y + 0.05) / 0.195 ≥ 3` gives `Y ≥ 0.535`. Pure red tops out at 0.2126, so it cannot be the lighter part on this floor. It can only pass by being very dark, or by adding a rim.

</details>

## Lab hook

[Lab 12, the color-blind audit](../labs/lab12.md). You finish a Python tool that simulates the three dichromacies and audits a palette's critical pairs, then use it to redesign a raid encounter's telegraph set so every pair passes in all four modes. The deliverable is the four-up render of your final design, the audit report before and after, and a short rationale.

## Sources

- Machado, G. M., Oliveira, M. M. & Fernandes, L. A. F. (2009). "A Physiologically-based Model for Simulation of Color Vision Deficiency." *IEEE Transactions on Visualization and Computer Graphics*, 15(6), 1291-1298. Severity 1.0 matrices from the authors' supplementary page. https://www.inf.ufrgs.br/~oliveira/pubs_files/CVD_Simulation/CVD_Simulation.html
- National Eye Institute, "Color Blindness" (accessed 2026). About 1 in 12 men; red-green is the most common type. https://www.nei.nih.gov/learn-about-eye-health/eye-conditions-and-diseases/color-blindness
- Colour Blind Awareness, "Colour Blindness" (accessed 2026). About 1 in 12 men and 1 in 200 women. https://www.colourblindawareness.org/colour-blindness/
- W3C (2018). *Web Content Accessibility Guidelines (WCAG) 2.1*, Understanding Success Criterion 1.4.11 Non-text Contrast. 3:1 minimum for UI components and graphical objects; contrast ratio definition. https://www.w3.org/WAI/WCAG21/Understanding/non-text-contrast.html
- League of Legends Wiki, "V1.0.0.132" (patch released January 17, 2012). Addition of Colorblind Mode for health bars and various effects, with the reproduced patch-note text and a link to an archived copy of Riot's original forum post (retrieved 29 September 2026). Also "Health bar", self health bar colorblind variant.
- Overwatch Wiki, "October 9, 2018 Patch". Color blind option updates: nine colorblind-friendly colors, enemy and friendly UI colored separately, under Options > Video > Color Blind Options (patch notes reproduced on the wiki, retrieved 29 September 2026).
- Inkipedia, "Options" (Splatoon, 2015; Splatoon 2, 2017). Color Lock pairs: blue versus orange for online battles in Splatoon; yellow versus dark purple for matchmaking battles in Splatoon 2. https://splatoonwiki.org/wiki/Options
- Game Accessibility Guidelines, "Ensure no essential information is conveyed by a fixed colour alone" (basic level). https://gameaccessibilityguidelines.com/ensure-no-essential-information-is-conveyed-by-a-colour-alone/
- CIELAB and ΔE (CIE 1976); sRGB linearization and relative luminance as in AR101 week 1.

## Interactive spec: examples/w12-colorblind-telegraph.html

**The one insight:** simulation of color-blindness collapses hue differences and leaves value differences almost intact. A red-on-green telegraph that looks obvious to typical vision turns to khaki on khaki for a deuteranope, and a value-plus-shape design stays readable for all four viewers.

**Layout.** Mobile: stacked (typical arena, simulated arena, table). Desktop (≥ 960px): two arenas side by side on top, table below. A "Four-up" toggle replaces the pair with a 2 × 2 grid (typical, protan, deutan, tritan).

**Arena (canvas).** Square top-down floor filled with the floor color. A boss marker (dark hexagon) at top center. Danger zone: circle of radius 28% of the panel, centered lower left, with optional rim (width 3% of panel). Safe zone: circle of radius 18%, lower right, rendered either as a filled circle (preset "Red / green") or as an unfilled dashed ring with four inward chevrons ("Value + shape"). A faint grid pattern on the floor (±2 L* at most) for texture. No game art.

**Simulation.** For each pixel color (compute per drawn color, not per pixel, since all shapes are flat colors): sRGB to linear (week 1 formula), multiply by the Machado severity 1.0 matrix for the selected type, clip to 0-1, encode back to sRGB. A "Severity" slider (0 to 1, step 0.1) blends linearly between the identity and the severity 1.0 matrix, labeled "approximation: the paper publishes separate matrices per severity". Toggle "Grayscale" applies to both panels (luminance gray from Y), and to all four in Four-up.

**Table (copyable text).** Rows: danger fill vs floor, danger rim vs floor (if rim on), danger vs safe, safe vs floor. Columns for each of the four viewers: ΔV, ΔE (CIE 1976), contrast ratio. Mark pass (ΔV ≥ 20) with a check and fail with a cross; show contrast ratio ≥ 3 with a second mark. Also show each simulated color's sRGB and L* in a collapsible detail.

**Controls.**
- Presets: "Red / green" (default), "Value + shape", "Team pair" (yellow (250, 220, 40) danger, dark purple (70, 30, 110) safe, filled).
- Right panel viewer: Protanopia, Deuteranopia (default), Tritanopia.
- Color pickers: floor, danger fill, danger rim (with on/off), safe zone. Safe style: filled or dashed ring with chevrons.
- Severity slider, Grayscale toggle, Four-up toggle, Reset.
All controls keyboard operable with visible focus.

**Test values (builder must reproduce to ±0.1).**
- Floor (96, 112, 72), red (200, 48, 40), green (64, 168, 72). Simulated sRGB: protan floor (116, 107, 69), red (95, 85, 37), green (171, 153, 63); deutan floor (114, 106, 74), red (133, 118, 33), green (158, 144, 79); tritan floor (98, 108, 102), red (220, 0, 48), green (42, 164, 147).
- Red vs floor ΔV / ΔE: typical 0.0 / 75.2, protan 9.0 / 11.1, deutan 4.8 / 27.7, tritan 1.5 / 86.4.
- Red vs green ΔV / ΔE: typical 16.3 / 109.5, protan 27.1 / 33.5, deutan 10.2 / 14.5, tritan 14.5 / 117.4.
- "Value + shape": fill (255, 176, 48) L* 77.6 / 73.3 / 80.1 / 74.3 (typical, protan, deutan, tritan); rim (32, 16, 16) ΔV vs floor 38.5 / 39.6 / 37.8 / 38.3; rim contrast ratio vs floor 3.42 / 3.50 / 3.36 / 3.39; fill contrast ratio vs floor 2.94 / 2.57 / 3.19 / 2.69.
- "Value + shape", danger fill vs safe ring: ΔV 15.5 / 19.6 / 13.0 / 18.7, marked fail on ΔV with the note "shape differs"; safe ring vs floor ΔV 48.1 / 47.7 / 48.3 / 48.2.
- "Team pair": yellow vs purple ΔV 66.4 / 63.6 / 67.3 / 63.4.

**First screen.** "Red / green" preset, Deuteranopia on the right: the left arena shows a vivid red zone and green zone, the right shows two khaki shapes on a khaki floor, table full of crosses. Caption: "Same arena. One in twelve men sees the right side."

**Accessibility and style.** Shared palette tokens for the page chrome, both color schemes (arenas keep their own colors). Pass and fail are marked with symbols and text as well as color. With reduced motion, no animated transitions. No game art, logos or characters.
