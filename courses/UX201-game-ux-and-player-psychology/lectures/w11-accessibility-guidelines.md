# UX201 · Week 11 — Accessibility Guidelines

**Why this matters:** Some of your players can't see colour differences, can't hear dialogue, can't read small text from the couch, or can't hold a button for three seconds. Many more can't do one of those things for an evening, because of glare, a sleeping baby or a broken wrist. Accessibility guidelines turn "make it accessible" into checks you can run and numbers you can hit. This week you learn to run the checks, and to see why the hard cases in games differ from the hard cases on the web.

**You will be able to:**
- Compute relative luminance and the WCAG contrast ratio for any pair of colours, and check them against the 4.5:1, 3:1 and 7:1 thresholds used by the Xbox Accessibility Guidelines.
- Compute the backplate opacity that keeps subtitle text readable over the brightest background in a scene.
- Audit a game screen against selected Game Accessibility Guidelines and Xbox Accessibility Guidelines, and rank the fixes by who they help and what they cost.
- Explain why colour alone fails as a signal and redesign a colour-coded HUD so it survives colour-vision deficiency.

**Before class:** Game Accessibility Guidelines (gameaccessibilityguidelines.com), read the "Basic" guidelines in all six categories. Xbox Accessibility Guidelines 101 (text display), 102 (contrast) and 104 (subtitles and captions) on Microsoft Learn, about 30 minutes in total. W3C, WCAG 2.1, the definitions of "contrast ratio" and "relative luminance" (two short paragraphs).

**Prerequisites from earlier courses:** [UX201 week 1, perception, attention and memory](w01-perception-attention-memory.md), for pop-out features and why colour is a strong but fragile signal. [UX201 week 10, HUD and information design](w10-hud-and-information-design.md), for visual angle, which we use again for text size. [UX201 week 3, flow and difficulty](w03-flow-and-difficulty.md), for the difference between the challenge you intend and the challenge the interface adds. Looking ahead, [GD203 week 13, difficulty modes and scaling](../../GD203-combat-and-progression-design/lectures/w13-difficulty-modes-and-scaling.md) (next semester) covers assist options in depth. This week defines what you need. [MA101 week 4, exponentials](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w04-exponentials-and-the-xp-curve.md), because the luminance formula raises values to the power 2.4.

**Interactive:** [examples/w11-subtitle-contrast.html](../examples/w11-subtitle-contrast.html). Use it during section 2.

---

## 1. Who accessibility is for

**Accessibility** is the degree to which people with disabilities can play your game. A **disability** in this sense is a mismatch between a person and a design. A player with low vision is not disabled by a menu with large high-contrast text. The same player is disabled by 14-pixel grey text on a busy background.

Three kinds of mismatch are worth naming, because they tell you how many players a fix reaches.

- **Permanent.** A player who is Deaf, blind, colour-blind, or has limited use of their hands.
- **Temporary.** A player with a broken arm, an eye infection, or a migraine.
- **Situational.** A player on a small screen, far from the TV, in sunlight, in a noisy room, or with the sound off so they don't wake someone.

The numbers are larger than most teams expect. Microsoft's Xbox guidelines cite about 2.9 billion people worldwide with some degree of low vision. About 8% of men and 0.4% of women of Northern European ancestry have a congenital colour-vision deficiency. Most of those have a red-green type, and deuteranomaly alone affects about 5% of men. In a game with a million players and a typical male-heavy audience, that is tens of thousands of people who see your red and green markers differently from you.

The situational list matters for the business case. Every fix for a permanent disability also helps someone in a situation. The Xbox guidelines list, next to each guideline, the players it helps, and almost every list ends with players on small screens, far from the screen, on displays with glare, or playing with the sound off. Subtitles were built for Deaf players. They are also used by anyone in a loud room.

## 2. Worked example: the brightest background decides

### The hook

Many recent games give you a slider labelled something like "subtitle background opacity" running from 0% to 100%. Forza Horizon 4 has one, with a preview of the result. Minecraft has a similar slider for the chat text background. Microsoft's own guideline for subtitles asks for exactly this: a solid background the player can place behind subtitles, with opacity adjustable from 0 to 100%. It gives a reason in one line. White text over light desert sand is close to invisible.

Why a slider? White text on a dark box looks fine in every screenshot of a dark scene. The box only matters when the scene behind it turns bright, and then it matters a great deal. Players who want no box at all are right about the dark scene. Players who need a solid box are right about the bright one. The question for the designer is concrete. What opacity does the box need so the text stays readable in the brightest scene your game has?

### The model

Readability of text depends mostly on **luminance contrast**, the difference in brightness between the text and what is behind it. The Web Content Accessibility Guidelines (WCAG 2.1) define it in two steps, and the Xbox Accessibility Guidelines use the same measure.

**Step 1, relative luminance.** For a colour with sRGB channels `R`, `G`, `B` from 0 to 255, divide each by 255 to get `c` from 0 to 1, then undo the display gamma:

```
lin(c) = c / 12.92                       if c ≤ 0.03928
lin(c) = ((c + 0.055) / 1.055) ^ 2.4     otherwise

L = 0.2126 × lin(R) + 0.7152 × lin(G) + 0.0722 × lin(B)
```

`L` runs from 0 (black) to 1 (white). The weights say that green contributes most to perceived brightness and blue least.

**Step 2, contrast ratio.** For the lighter luminance `L1` and the darker `L2`:

```
C = (L1 + 0.05) / (L2 + 0.05)
```

`C` runs from 1:1 (no contrast) to 21:1 (black on white). The `0.05` stands for stray light, so even pure black on screen is never perfectly dark.

**The thresholds.** The Xbox Accessibility Guidelines (XAG 102) ask for at least 4.5:1 for standard-size text and important visual elements, 3:1 for large text and large elements, and 7:1 for every UI element in a high-contrast mode. For games the key line in XAG 102 is this one. It says that when text sits over a non-solid background, you measure against **the lowest-contrast area of the background**. The average background doesn't count. The worst one does.

**Step 3, the backplate.** Put a black box with opacity `α` behind the text. We model the box as darkening the light behind it, in linear light:

```
L_behind = (1 − α) × L_background
```

White text has `L = 1`, so its contrast against the boxed background is:

```
C(α) = 1.05 / ((1 − α) × L_background + 0.05)
```

Solve `C(α) ≥ C_target` for the smallest opacity that works:

```
α ≥ 1 − (1.05 / C_target − 0.05) / L_background
```

For the 4.5:1 target, `1.05 / 4.5 − 0.05 = 0.1833`, so `α ≥ 1 − 0.1833 / L_background`.

### Numbers you can check

Six background colours from an invented open-world game, each a representative average for a patch of scene behind the subtitle line. White subtitle text.

| Background | Hex | `L` | `C` at α = 0 | α = 0.5 | α = 0.75 | α = 0.9 | α needed for 4.5:1 |
|---|---|---|---|---|---|---|---|
| Night sky | `#1B2233` | 0.016 | 15.9 | 18.1 | 19.4 | 20.3 | 0 |
| Forest | `#2E4A2B` | 0.057 | 9.9 | 13.4 | 16.4 | 18.9 | 0 |
| Stone | `#7A7A7A` | 0.195 | 4.3 | 7.1 | 10.6 | 15.1 | 0.06 |
| Clear sky | `#87CEEB` | 0.553 | 1.7 | 3.2 | 5.6 | 10.0 | 0.67 |
| Desert sand | `#E6C88C` | 0.600 | 1.6 | 3.0 | 5.3 | 9.5 | 0.70 |
| Snow | `#F2F4F7` | 0.903 | 1.1 | 2.1 | 3.8 | 7.5 | 0.80 |

Check the stone row by hand. `0x7A = 122`, so `c = 0.478`. `lin = ((0.478 + 0.055) / 1.055)^2.4 = 0.506^2.4 = 0.195`. All three channels are equal, so `L = 0.195`. With no box, `C = 1.05 / (0.195 + 0.05) = 4.29`. That is just below 4.5, which is why grey stone is the scene where testers first squint. A box at `α = 0.06` fixes it.

Now the snow row. With no box, white on snow is `1.05 / 0.953 = 1.10:1`, which is barely distinguishable from nothing. A 75% box gives 3.8:1, which passes for large text but fails for standard text. You need at least 80%.

Three things stand out.

1. **The average scene lies.** Averaged over the six backgrounds, a 50% box gives a mean contrast above 7:1. Yet it fails in half of them. XAG 102's rule to measure the lowest-contrast area is there because games spend minutes at a time in their brightest scenes.
2. **The needed opacity is set by one row.** A game with no snow and no desert could ship a 70% default. Add one snowy region and the default must rise to 80%, or the text needs another fix. Your art direction sets your accessibility default.
3. **Coloured text makes it worse.** Gold subtitle text (`#FFD700`, `L ≈ 0.70`) has a contrast of only 1.2:1 against snow, sky or sand. Coloured text for speaker names looks good in dark scenes and disappears in bright ones.

Back to the hook. The slider exists because no single opacity suits everyone. A player who needs 7:1 in every scene needs about 90% over snow. A player who finds the box intrusive can accept the risk in the scenes they play. The guideline's answer is a default that passes in your worst scene, plus a slider.

### A visual you can move

Open `examples/w11-subtitle-contrast.html`. The top view is a strip of scene made of the six background patches, with a subtitle line running across all of them over a box. Drag the opacity slider and watch the text. It is readable everywhere at 90% and vanishes over the snow at 0%. The box is drawn in linear light, as the model computes it, so what you see matches the numbers. A toggle redraws it with sRGB blending, as many UI engines do. The box then looks darker while the numbers stay on the linear model. That gap is the blending-mode caveat below. The bottom view is a chart of contrast ratio for each patch, with horizontal lines at 3:1, 4.5:1 and 7:1. The mean contrast is drawn as a dashed line, and the minimum as a thick one.

The one thing to notice: at 50% opacity the dashed mean sits comfortably above 4.5:1 while the thick minimum sits at 2.1:1. The mean looks safe and the worst case fails. Try the other controls too. Switch the text to gold and watch the bright patches collapse. Switch the box to an outline and see the minimum jump. Then add a patch of your own with the colour picker.

### Cross-game recognition

**Forza Horizon 4 and Minecraft, the backplate as a player setting.** Both games expose the `α` in our formula directly as a slider. Forza shows a preview so the player can judge the result. This is the model with the designer's constant turned into a player choice.

**For Honor, the outline as a local backplate.** XAG 102 describes For Honor's team symbols, which carry a black outline and then a white one. The white outline keeps the symbol visible against dark walls, and the black outline keeps it visible against light ones. In our terms, the outline guarantees the text a thin background of known luminance, so the worst background behind it no longer matters at the edge. Immortals Fenyx Rising, also cited by Microsoft, gives in-game text a black outline for the same reason.

**Sea of Thieves, the worst-patch rule applied.** Microsoft's example uses the Sea of Thieves accessibility menu, which sits on a patterned turquoise background of lighter and darker patches. The guideline says to measure against the lighter turquoise. That is our table's rule, measure against the snow and not the average, applied to a menu.

**Eagle Island, the whole scene as the backplate.** XAG 102 describes Eagle Island's option to dim the backdrop, up to 100%, which turns a busy forest into solid black, with an option to outline characters and platforms in white. That is `α` applied to the entire background instead of a box behind the text. The formula is the same, and the element that needs contrast is now the player character.

Each of these games asks the same question. What is the darkest or lightest thing that can ever sit behind this element, and how do I guarantee contrast against it? The answers differ (a box, an outline, a dimmed world), but the arithmetic is one formula.

### Eyes-open design judgment

- **Blending mode changes the number.** Our model darkens the background in linear light, which is how light physically mixes. Many UI systems blend in gamma-encoded sRGB instead, which makes a semi-transparent black box darker than our model predicts. A 50% sRGB-space black over pure white gives about 4.0:1, against our model's 1.9:1. Our figures are therefore conservative. Measure the real result on a screen capture with a contrast tool, as XAG 102 recommends.
- **Contrast ratio is not everything.** Size, weight, font, line length and time on screen all affect readability. A 4.5:1 subtitle that is 14 pixels tall on a TV is still unreadable (section 4).
- **A solid box costs something.** It hides part of the scene and some players find it intrusive. That is why the guideline asks for a slider and a sensible default, not a mandatory 100% box.
- **Outlines are cheaper but thinner.** An outline guarantees contrast only at the letter edges. For small or thin fonts, the outline can be most of the letter, which helps. For large, heavy text over busy detail, a box may still read better. Test both.
- **High-contrast modes have a different target.** XAG 102 asks for 7:1 in a high-contrast mode. It also notes that some players with reading difficulties find very high contrast harder, which is one more reason to make contrast adjustable rather than fixed.
- **You choose the worst case.** If your game has a white-out blizzard, it sets the default. You can change the art (a darker sky behind the subtitle area), the UI (more opacity) or both. Decide deliberately, and write the decision down.

### Check yourself (worked example)

1. A desert level's brightest sand is `#F0DCA0` with `L = 0.71`. What box opacity keeps white subtitles at 4.5:1? At 7:1?
2. Dark grey text `#333333` (`L = 0.033`) sits on a light parchment menu of `L = 0.80`. Compute the contrast. Does it pass for standard text? For a high-contrast mode?
3. A designer proposes white subtitles with no box but a 2-pixel black outline. A reviewer measures the contrast of the white fill against the snow as 1.1:1 and fails it. Is that the right measurement? What would you measure instead, and what would you still worry about?

<details>
<summary>Answers</summary>

1. 4.5:1: `α ≥ 1 − 0.1833 / 0.71 = 0.742`, so about 75%. 7:1: `1.05/7 − 0.05 = 0.10`, so `α ≥ 1 − 0.10 / 0.71 = 0.859`, about 86%.
2. `C = (0.80 + 0.05) / (0.033 + 0.05) = 0.85 / 0.083 = 10.2:1`. It passes 4.5:1 and 7:1.
3. The white fill is not adjacent to the snow. The outline sits between them, so the relevant contrasts are white against the black outline (21:1) and the outline against the snow (`(0.903 + 0.05) / (0 + 0.05) = 19.1:1`). Both pass. Still worry about the outline's width relative to the font at small sizes, and about busy textures where the outline merges with dark detail.

</details>

## 3. The guidelines you will actually use

Three sets of guidelines matter for game work. They overlap, and they are written for different purposes.

**Game Accessibility Guidelines** (gameaccessibilityguidelines.com) is a free, practitioner-written set organised by the kind of ability involved: motor, cognitive, vision, hearing, speech and general. Inside each category, guidelines are graded basic, intermediate and advanced. Basic guidelines are meant to be cheap and to help many people. Guideline titles give the flavour, for example "Allow controls to be remapped / reconfigured", "Use an easily readable default font size", "Ensure no essential information is conveyed by a fixed colour alone" and "Provide a visual indication of who is currently speaking". Start every audit with the basic list.

**Xbox Accessibility Guidelines (XAGs)** are Microsoft's numbered guidelines for games on its platforms, published on Microsoft Learn. Each one states a goal, gives scoping questions, shows examples from shipped games and ends with concrete implementation rules and a list of the players it helps. XAG 101 covers text display, 102 contrast, 103 additional channels for visual and audio cues, and 104 subtitles and captions. The XAGs are the most numeric of the three, which makes them the easiest to test against.

**WCAG** (Web Content Accessibility Guidelines, version 2.1 from the W3C) is written for websites. Game teams borrow its contrast formula and thresholds and apply its principles to menus. WCAG does not cover real-time play, so don't expect it to tell you anything about aiming or reaction time.

How to use them together:

1. **Scope.** For each guideline, ask whether your game has the feature it covers. XAG scoping questions are good for this. A game with no voice chat can skip speech-to-text.
2. **Audit.** Check each in-scope guideline against the build. Record pass, fail or partial, with a screenshot and a measured value where one exists.
3. **Rank.** Rank failures by the number of players affected (permanent, temporary and situational), by the severity (can't play at all, can play with difficulty, minor annoyance), and by cost.
4. **Test with players.** XAG 103 notes that simulation filters, such as colour-blindness filters, are useful internally but do not replace testing with real players who have the disability. Recruit them for your usability sessions ([week 8](w08-usability-testing-methods.md)).

## 4. Text size is an angle

XAG 101 sets minimum default text sizes, measured as the pixel height from the top of the tallest letter to the bottom of the lowest descender:

- Console: 26 px at 1080p (52 px at 4K).
- PC and VR: 18 px at 1080p (36 px at 4K).
- Mobile and game streaming: 18 px at 100 DPI, scaling linearly with pixel density (72 px at 400 DPI).

It also asks that players can scale text up to 200% of those minimums.

Why is the console number larger? Last week's visual angle answers it. A 1080p pixel on a 55-inch TV is 0.063 cm tall. 26 px is therefore 1.65 cm, and at 250 cm that subtends `atan(1.65 / 250) = 0.38°`, about 23 arcminutes. On a 24-inch monitor at 60 cm, a pixel is 0.028 cm, so 18 px is 0.50 cm and subtends `atan(0.50 / 60) = 0.48°`, about 29 arcminutes.

So the console minimum is larger in pixels and still smaller at the eye. On a 42-inch TV at the same couch distance, 26 px shrinks to about 17 arcminutes. This is why the guideline sets a minimum and asks for scaling. The designer doesn't know the player's TV or couch, and the player does.

A practical rule follows. Check your text size in degrees for the smallest screen and farthest seat you expect, then let the player scale up. XAG 101 also covers spacing (line spacing at least 1.5, lines of at most 80 characters in body text), mixed case for sentences, and at least one sans-serif option.

## 5. Colour alone is not a signal

Week 1 showed that colour is one of the strongest pop-out features. It is also the least reliable, because a large minority of players don't see the same colours.

A red-green colour-vision deficiency collapses hue differences along the red-green axis. What survives is mostly luminance. So a quick test for whether a pair of colours will stay distinct is their luminance contrast.

| Pair | Contrast ratio | Survives red-green deficiency? |
|---|---|---|
| Pure red `#FF0000` and pure green `#00FF00` | 2.9:1 | Partly, through brightness |
| Material red `#E53935` and green `#43A047` | 1.3:1 | Poorly. Nearly equal brightness |
| Orange `#FFB300` and blue `#1E88E5` | 2.0:1 | Better. The hues differ on the axis that survives, and brightness differs |

The middle row is the common trap. Many UI palettes pick a red and a green of similar brightness because they look balanced. For a player with deuteranopia, the two can look almost the same.

XAG 103 and the Game Accessibility Guidelines give the same fix in three layers.

1. **Never use colour alone for essential information.** Add a second channel: shape, icon, pattern, text or position. Microsoft's example is Grounded's crafting menu, which marks missing ingredients with red numbers and also a warning symbol and a text count.
2. **Let players choose the colours when colour carries meaning.** Call of Duty: Black Ops Cold War lets players pick the colours of the triangles for self, allies, enemies and party members on the map. Battlefield 2042 offers deuteranopia, protanopia and tritanopia presets, plus a custom colour picker with a preview in shadowy, mid-tone and bright scenes.
3. **Offer presets for the common types.** Forza Horizon 4 offers deuteranopia, protanopia, tritanopia and high-contrast presets.

Notice Battlefield's preview in three lighting conditions. It is the worked example's lesson again: a colour choice has to be checked against the worst background, not one screenshot.

## 6. Subtitles, captions and the rest of the checklist

**Subtitles** are text for speech. **Captions** are text for all important audio, including sound effects and music cues, often with a direction arrow. XAG 104 gives concrete defaults.

- Subtitles on by default, or the player can set them before any speech plays. Gears 5 enables them by default on first launch, then shows the accessibility menu after the opening video.
- Name the speaker when the speaker changes. Colour can mark the speaker only alongside the name.
- At most about 40 characters per line and two lines on screen (three in exceptional cases), with line breaks placed by hand at sensible points.
- Mixed case, at least one sans-serif font, text at least the XAG 101 minimum and scalable to 200%.
- A background box the player can turn on, with a colour choice and opacity from 0 to 100%.
- Captions for important sounds that are not already visible, with a direction marker for sounds off screen. Minecraft Java Edition shows sound captions with arrows for left and right.

The rest of a basic audit covers motor and cognitive access. Among the motor items are remappable controls, toggles instead of holds, no required rapid button mashing, and adjustable timing for quick-time events. Among the cognitive items are reminders of the current objective, tutorials the player can replay, and a clear option to lower difficulty or skip a failing section.

Accessibility and difficulty are close neighbours. Week 3 separated the challenge you intend from the challenge the interface adds. An accessibility option removes a barrier that was never meant to be the challenge, such as reading small text, seeing a colour or holding a button. An assist option changes the intended challenge, such as slowing time or reducing damage. Both are legitimate. Mixing them up leads teams to refuse a subtitle box "because it makes the game easier", which it doesn't, or to call a difficulty slider accessibility and stop there.

The Last of Us Part II (June 2020) is the game students most often cite here. Naughty Dog set out to extend the accessibility options it had introduced in Uncharted 4 so that every player could finish the story, and critics praised the result. Treat it as evidence of what a large team can ship, and use the guidelines to decide what your team can ship.

## In-class activity (25 minutes)

Pairs. You need a laptop with an image editor or colour picker, and three screenshots from one shipped game: a menu, a dialogue scene with subtitles, and a bright gameplay scene with HUD.

1. **Contrast (10 min).** In each screenshot, pick the text colour and the lightest (or darkest) background pixel directly behind it. Compute `L` for both and the contrast ratio. Mark pass or fail against 4.5:1.
2. **Worst case (5 min).** For the subtitle screenshot, find the brightest background in the game you can remember or find in a video. Compute the box opacity needed for 4.5:1 on that background.
3. **Checklist (10 min).** Check five basic Game Accessibility Guidelines of your choice against what you can see or find in the game's settings (remapping, subtitle options, colour options, text size, speaker names). Rank the failures by players affected.

Expected output: three measured contrast ratios, one required opacity, and a ranked list of five guideline results.

## Common misconceptions

- **"Accessibility is for a small group."** Permanent disabilities alone cover millions of players, and situational ones cover almost everyone at some point. Subtitles, remapping and text scaling are used far beyond the players they were designed for.
- **"If the screenshot looks fine, the contrast is fine."** Contrast in games depends on the scene behind the text. XAG 102 tells you to measure against the lowest-contrast area. One snowy level can fail a HUD that passes everywhere else.
- **"A colour-blind mode fixes colour problems."** A filter or palette swap helps, but information carried by colour alone still fails for some players. Add a second channel first, then offer colour options.
- **"Accessibility options make the game easier."** Most don't. A subtitle box, larger text or a remapped button removes a barrier, not a challenge. Assist options do change the challenge, and they are a separate, deliberate decision.

## Check yourself

1. Compute the contrast ratio of pure yellow text `#FFFF00` on pure white. Would you use it for a warning in a snowy level?
2. A HUD shows allies in green `#43A047` and enemies in red `#E53935`. Give two changes that make the distinction survive red-green colour-vision deficiency, and say which guideline each satisfies.
3. A mobile game shows 16 px text on a phone whose short side is 7.0 cm wide with 1080 px across it, held at 30 cm. Compute the text's visual angle in arcminutes and compare it with the console and PC figures in section 4.
4. Your team's subtitles have a fixed 60% box. A tester fails them over a white-out blizzard (`L = 0.95`). Give two different fixes and the opacity or other value each needs.

<details>
<summary>Answers</summary>

1. Yellow: `lin(1) = 1` for red and green, `lin(0) = 0` for blue, so `L = 0.2126 + 0.7152 = 0.928`. `C = 1.05 / 0.978 = 1.07:1`. No. It is effectively invisible on snow.
2. Add a shape difference (for example, allies as circles and enemies as diamonds) to satisfy "no essential information by colour alone" (GAG, XAG 103). Offer player-chosen colours or presets, as XAG 102 and 103 recommend. A third option is to use a luminance difference, such as light allies and dark enemies, with an outline.
3. One pixel is `7.0 / 1080 = 0.0065 cm`, so 16 px is 0.104 cm. `atan(0.104 / 30) = 0.198°`, about 11.9 arcminutes. That is about half the console figure at the couch. XAG 101 also sets a mobile minimum that scales with pixel density, 18 px at 100 DPI rising linearly (72 px at 400 DPI). This phone has about 392 DPI (1,080 px across 2.76 inches), so the minimum is about 70 px, and 16 px is far below it.
4. Raise the default opacity: `α ≥ 1 − 0.1833 / 0.95 = 0.807`, so at least 81%. Or keep 60% and add a black outline to the letters, which guarantees contrast at the edges. A third fix is to change the art so the area behind the subtitle line never reaches `L = 0.95` (for example, a darker vignette at the bottom of the screen in the blizzard).

</details>

## Lab hook

[Lab 11, accessibility audit of a shipped game](../labs/lab11.md). You audit one shipped game against twelve basic guidelines, measure contrast on the worst-case screens with the starter script, compute the needed subtitle box opacity, and write a ranked fix list. Deliverable: the audit table, the measurement sheet and a two-page memo.

## Sources

- Microsoft Learn, Xbox Accessibility Guideline 101, "Text display" (page dated May 2022, accessed September 2026). About 2.9 billion people with low vision; minimum text sizes 26 px at 1080p for console, 18 px at 1080p for PC and VR, mobile 18 px at 100 DPI scaling linearly with DPI; scaling to 200%; line width, spacing and case rules; Immortals Fenyx Rising's black text outline.
- Microsoft Learn, Xbox Accessibility Guideline 102, "Contrast" (page dated June 2023, accessed September 2026). 4.5:1 for standard text and elements, 3:1 for large text and inactive elements, 7:1 in high-contrast mode; measure against the lowest-contrast area of a non-solid background; examples from Sea of Thieves, For Honor (black and white outlines), Eagle Island (backdrop dimming and outlines), Minecraft (text background opacity), Fallout: New Vegas (HUD colour), Battlefield 2042 (colour-blind presets and custom colours with preview).
- Microsoft Learn, Xbox Accessibility Guideline 103, "Additional channels for visual and audio cues" (page dated May 2022, accessed September 2026). Colour should never be used alone; simulation filters do not replace testing with players; examples from Grounded, Call of Duty: Black Ops Cold War (player-chosen map colours) and Forza Horizon 4 (colour-blind and high-contrast presets).
- Microsoft Learn, Xbox Accessibility Guideline 104, "Subtitles and captions" (page dated May 2022, accessed September 2026). Speaker identification, 40-character lines, two lines, background colour and 0-100% opacity, white text over light desert sand as the failure case; examples from Gears 5 (subtitles on at first launch), Forza Horizon 4 (opacity slider with preview), Minecraft Java Edition (directional captions).
- W3C, *Web Content Accessibility Guidelines (WCAG) 2.1* (2018). Contrast ratio `(L1 + 0.05)/(L2 + 0.05)`; success criteria 1.4.3 (4.5:1, 3:1 for large text), 1.4.6 (7:1) and 1.4.11 (3:1 for non-text UI). W3C WAI wiki, "Relative luminance," for the linearisation constants and coefficients.
- Game Accessibility Guidelines (gameaccessibilityguidelines.com, full list, accessed September 2026). Categories motor, cognitive, vision, hearing, speech and general; basic, intermediate and advanced levels; guideline titles quoted in section 3.
- Wikipedia, "Color blindness" (accessed September 2026). About 8% of men and 0.4% of women of Northern European ancestry have congenital colour deficiency; male prevalence of protanopia 1.3%, deuteranopia 1.2%, deuteranomaly 5.0%.
- Wikipedia, "The Last of Us Part II" (accessed September 2026). Released 19 June 2020 on PlayStation 4; Naughty Dog expanded the accessibility options introduced in Uncharted 4.
- The six background colours, the gold text colour and the red/green/blue/orange palette pairs are teaching choices, not colours taken from any shipped game. The linear-light backplate model is a teaching simplification (see the design judgment on blending modes).

## Interactive spec: examples/w11-subtitle-contrast.html

**Purpose.** Show that subtitle readability over a game scene is set by the brightest background, not the average, and that the needed backplate opacity follows directly from the contrast formula.

**The one insight the visual must make obvious.** At 50% opacity the mean contrast line sits above 4.5:1 while the minimum sits at about 2.1:1 and the subtitle visibly disappears over the snow patch.

**Layout.** Two stacked views at all widths. Controls below. Numbers table at the bottom.

- **Top, "Scene strip".** Six equal-width rectangles in the colours below, side by side (wrapping to 3 × 2 at 390px). A single subtitle line of generic text ("Speaker: Keep moving, the storm is coming.") runs across the strip, each word over whichever patch lies beneath it, on a black box whose opacity is the slider value. By default, draw the box in linear light: fill each patch's box segment with the colour whose linear channels are `(1 − α)` times the patch's, so the picture matches the numbers. A "Box blending" toggle switches the drawing to sRGB blending (CSS `rgba(0,0,0,α)`), which looks darker. Contrast numbers always use the linear-light model. A caption explains the difference.
- **Bottom, "Contrast per patch".** Vertical bars, one per patch, height = contrast ratio on a log-scaled y axis from 1 to 21. Horizontal reference lines at 3, 4.5 and 7, labelled. A dashed horizontal line for the mean contrast and a thick line for the minimum. Bars below 4.5 get a hatch pattern as well as a warning colour.

**Patches (default).** Night sky `#1B2233`, Forest `#2E4A2B`, Stone `#7A7A7A`, Clear sky `#87CEEB`, Desert sand `#E6C88C`, Snow `#F2F4F7`. A seventh "custom" patch is added when the student uses the colour picker.

**Controls.**

- Box opacity `α`: slider 0-100%, step 1, default 50%.
- Text colour: segmented White `#FFFFFF`, Gold `#FFD700`, Custom (colour picker).
- Treatment: segmented Box, Outline (2 px black), Box + outline. In outline mode, contrast for each patch is computed as `min(C(text, black), C(black, patch))`, i.e. the text is judged against the outline and the outline against the background.
- Target: segmented 3:1, 4.5:1 (default), 7:1. Updates the "α needed" column and highlights the binding patch.
- Add custom patch: colour picker.
- Reset.

**Formulas.**

- `lin(c) = c/12.92` if `c ≤ 0.03928`, else `((c + 0.055)/1.055)^2.4`, with `c = channel/255`.
- `L = 0.2126 lin(R) + 0.7152 lin(G) + 0.0722 lin(B)`.
- Behind luminance with box: `L_b = (1 − α) × L_patch`.
- `C = (max(L_text, L_b) + 0.05) / (min(L_text, L_b) + 0.05)`.
- Needed opacity for white text and target `C*`: `α* = max(0, 1 − (1.05/C* − 0.05)/L_patch)`. For non-white text, solve numerically or with `α* = max(0, 1 − ((L_text + 0.05)/C* − 0.05)/L_patch)` when text is lighter than the boxed background.

**Numbers table.** For each patch: hex, `L` (3 decimals), contrast at current settings (2 decimals), pass/fail at the target, `α` needed.

**Test values** (white text, box only).

| Patch | L | C at 0% | 50% | 75% | 90% | α* for 4.5 |
|---|---|---|---|---|---|---|
| Night sky | 0.0162 | 15.87 | 18.08 | 19.43 | 20.34 | 0 |
| Forest | 0.0565 | 9.86 | 13.42 | 16.37 | 18.87 | 0 |
| Stone | 0.1946 | 4.29 | 7.13 | 10.64 | 15.12 | 0.058 |
| Clear sky | 0.5529 | 1.74 | 3.22 | 5.58 | 9.97 | 0.668 |
| Desert sand | 0.6002 | 1.61 | 3.00 | 5.25 | 9.54 | 0.695 |
| Snow | 0.9029 | 1.10 | 2.09 | 3.81 | 7.48 | 0.797 |

- Gold `#FFD700`: `L ≈ 0.698`; contrast on snow at 0% = 1.27, on sand 1.15, on night sky 11.31.
- `#767676` on white: 4.54.
- At 50%, mean of the six contrasts = 7.82, minimum = 2.09.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`, light and dark. Failing bars use hatch plus colour. All controls keyboard operable with visible focus and visible values. Respect `prefers-reduced-motion`. No game art or screenshots; patches are flat colours with text labels.
