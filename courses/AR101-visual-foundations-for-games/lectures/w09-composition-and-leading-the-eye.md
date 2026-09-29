# AR101 · Week 09 — Composition and Leading the Eye

**Why this matters:** Every screen of your game makes the player look somewhere first. If that first place is a pretty cloud instead of the exit, the enemy or the item they need, the scene has failed, however good each asset looks on its own. Composition is how you decide the order in which the eye visits things. This week you learn a model that predicts that order from a greyscale thumbnail, so you can check a scene before anyone plays it.

**You will be able to:**
- Compute a local contrast map for a value thumbnail and predict the first focal point.
- Compute the hierarchy ratio between the focal point and its strongest rival, and judge whether a scene has one clear focus.
- Fix a scene with competing focal points by changing values, and justify each change with numbers.
- Critique a game scene's composition using contrast, leading lines, framing and the camera.

**Before class:** Chris Solarski, *Drawing Basics and Video Game Art* (2012), the material on composition and on value (use the index). Bruce Block, *The Visual Story* (2nd ed., 2008), the chapter on the principle of contrast and affinity. Bring five screenshots from games you play, each one a moment where you knew where to go without being told.

**Prerequisites from earlier courses:** AR101 has no prerequisite courses. From this course, [week 1, value before color](w01-seeing-like-an-artist-value-before-color.md) supplies value as CIE L* from 0 to 100 and the value gap ΔV, and [week 3 on silhouettes](w03-silhouette-readability.md) supplies the black-fill test. Later in the program, [GD201 week 4, guiding the player](../../GD201-level-and-world-design/lectures/w04-guiding-the-player-landmarks-light-weenies.md) measures one landmark against its background with the WCAG contrast ratio, and [UX201 week 1, perception and attention](../../UX201-game-ux-and-player-psychology/lectures/w01-perception-attention-memory.md) explains why a single odd item pops out of a crowd. This week sits between them. It ranks every region of one frame against its neighbours.

**Interactive:** [`examples/w09-focal-map.html`](../examples/w09-focal-map.html). Keep it open during section 2.

---

## 1. Composition is an order, not a picture

**Composition** is the arrangement of shapes, values and colors in a frame so that the viewer looks at things in a chosen order. The first place the eye lands is the **focal point**. The places it visits next are the **secondary** and **tertiary** points. The whole ranking is the scene's **visual hierarchy**.

A game scene has a job that a painting doesn't. It has to tell a player, in about a second, where they can go and what can hurt them. So the question for a game composition is never "is it beautiful?" It is "does the eye land on the thing the player needs, and does it land there first?"

Artists check this with **thumbnails**. A thumbnail is a tiny version of the scene, often a few centimeters wide, in three to five flat values and no color. At that size detail vanishes and only the large value shapes remain. Many artists also use the **squint test**. Half-close your eyes at the screen until the detail blurs, and see what stays visible. Both tricks throw away what doesn't drive the eye, so the hierarchy shows through.

Why value and not color? In week 1 you saw that value (how light or dark something is) carries shape and depth even with color removed. For the eye's first jump, the strongest pull is a place where value changes sharply. Color, detail, faces and motion also pull. Motion in particular beats almost everything in a game, and week 10 deals with it. But in a still frame, value contrast is the part you can measure and the part that survives every screen, every color-blind player and every lighting change. Get the value hierarchy right first. Color can then strengthen it, and it shouldn't have to rescue it.

## 2. Worked example: where does the eye land first?

### The hook

Limbo (Playdead, 2010) has no color. Its world is presented in greyscale, with lighting and a film-grain filter, and reviewers compared it to film noir and silent film. Every hazard, ledge, rope and exit a player finds is found through value alone, and players still find them.

So a greyscale frame carries enough information to steer a player. That means you can model the steering with a greyscale thumbnail and some arithmetic. And the arithmetic makes one prediction that surprises most students. The eye doesn't go to the brightest thing on screen. It goes to the thing that differs most from what surrounds it.

### The model

Divide the thumbnail into a grid of cells and give each cell its value `V`, the CIE lightness L* from week 1, where 0 is black and 100 is white. For each cell, compare it with its neighbours:

```
C(cell)  = | V(cell) − mean of V over the cell's neighbours |
focal    = the cell with the largest C
rival    = the cell with the largest C that doesn't touch the focal cell
H        = C(focal) / C(rival)
```

- **Neighbours** are the up to eight cells touching the cell, including diagonals. Cells on the border have fewer.
- `C` is the cell's **local contrast**, how different it is from its surroundings, in value points. It is week 1's value gap ΔV, measured against the average of the neighbourhood instead of against one background. Week 1's rule of thumb carries over, so a cell with `C` under 10 merges into its surroundings and one of 20 or more reads.
- The **rival** is the strongest competitor elsewhere in the frame. Cells touching the focal cell are excluded because they usually belong to the same shape.
- `H` is the **hierarchy ratio**. It says how much the focal point beats its strongest competitor.

For this course, a scene with `H ≥ 1.5` has one clear focal point. A scene with `H` between 1.0 and 1.5 has two competing ones, and players' eyes will split between them. The 1.5 threshold is a teaching value that works on small thumbnails. It isn't a law of perception, and the lab asks you to test it on real people.

This is a simplified model of what vision scientists call **saliency**, how much a region stands out from its surroundings. Real saliency models compare features at many scales and include color, orientation and motion. Ours keeps one feature, value, at one scale, the thumbnail. That's enough to catch the most common composition mistakes, and simple enough to do by hand.

### Numbers you can check

Here is a 6 by 4 thumbnail of a dark forest with a lit doorway. Rows count from 0 at the top, columns from 0 at the left.

```
scene A: doorway                  local contrast C
20  20  25  20  20  20             0   1   5  14  13  22
20  20  20  20  85  20             3   2   1  10  64  15
30  25  20  20  30  20             3   2   6  15   4  21
35  35  35  35  35  35             5   6   8   7   7   7
```

Check the doorway at row 1, column 4. Its eight neighbours are seven cells of 20 and one of 30 (the step below it), a mean of `170 / 8 = 21.25`. So `C = |85 − 21.25| = 63.75`, which rounds to 64. The largest cell not touching the doorway is at row 3, column 2, with `C = 8`. `H = 64 / 8 = 8.0`. One unmistakable focal point.

Now make three changes, one at a time, starting from scene A each time.

| Scene | Change from A | Focal (C) | Rival (C) | H | Reading |
|---|---|---|---|---|---|
| A | none | door (64) | ground, row 3 col 2 (8) | 8.0 | one clear focus |
| B | bright sky patch, three cells of 80 top left | door (64) | sky, row 0 col 1 (35) | 1.83 | door wins, sky is a clear secondary |
| C | a torch of 85 at row 2, column 1 | door (64) | torch (58) | 1.10 | two competing focal points |
| D | the same torch at 50 | door (64) | torch (23) | 2.78 | door wins, torch is a supporting accent |

Scene C is the classic mistake. An environment artist adds a bright torch to "make the forest interesting", and the player's eye now splits between the torch and the door. Scene D keeps the torch but drops its value from 85 to 50. The torch still reads as a light, and `H` goes from 1.10 to 2.78.

Scene B shows a subtler point. The sky patch is 80, almost as bright as the door. But its three cells are next to each other, so each one's neighbours include bright sky, which lowers its contrast. A big bright area pulls less than a small bright spot of the same value. Size spreads contrast out.

Now the surprise. Take a different thumbnail: a sky of 80 filling rows 0 to 2, ground of 30 in row 3, a dark figure of 15 at row 1, column 2, and a white cloud of 100 at row 1, column 4. The cloud is the brightest cell in the frame. Its neighbours are all sky at 80, so `C = |100 − 80| = 20`. The figure's neighbours are also all sky, so `C = |15 − 80| = 65`. The figure wins by more than three to one. The eye goes to the dark silhouette against the light sky, not to the brightest thing on screen. This is the same reason week 3's black-fill silhouettes read so well. A dark shape on a light field has the most contrast in the frame.

The code below reproduces scenes A to D. Run it with `.venv/bin/python`.

```python
def contrast_map(grid):
    rows, cols = len(grid), len(grid[0])
    out = []
    for r in range(rows):
        row = []
        for c in range(cols):
            near = [grid[rr][cc]
                    for rr in range(r - 1, r + 2) for cc in range(c - 1, c + 2)
                    if (rr, cc) != (r, c) and 0 <= rr < rows and 0 <= cc < cols]
            row.append(round(abs(grid[r][c] - sum(near) / len(near))))
        out.append(row)
    return out


def focal(grid):
    con = contrast_map(grid)
    ranked = sorted(((con[r][c], (r, c)) for r in range(len(con)) for c in range(len(con[0]))),
                    reverse=True)
    top, where = ranked[0]
    rival, rival_at = next((v, p) for v, p in ranked[1:]
                           if max(abs(p[0] - where[0]), abs(p[1] - where[1])) > 1)
    return where, top, rival_at, rival, round(top / rival, 2)


doorway = [[20, 20, 25, 20, 20, 20],
           [20, 20, 20, 20, 85, 20],
           [30, 25, 20, 20, 30, 20],
           [35, 35, 35, 35, 35, 35]]


def edit(grid, changes):
    g = [row[:] for row in grid]
    for (r, c), v in changes.items():
        g[r][c] = v
    return g


scenes = {
    "A doorway": doorway,
    "B + bright sky": edit(doorway, {(0, 0): 80, (0, 1): 80, (1, 0): 80}),
    "C + torch 85": edit(doorway, {(2, 1): 85}),
    "D torch at 50": edit(doorway, {(2, 1): 50}),
}
for name, g in scenes.items():
    print(f"{name:15}", focal(g))
```

It prints each scene's focal cell, its contrast, the rival cell, its contrast and `H`:

```
A doorway       ((1, 4), 64, (3, 2), 8, 8.0)
B + bright sky  ((1, 4), 64, (0, 1), 35, 1.83)
C + torch 85    ((1, 4), 64, (2, 1), 58, 1.1)
D torch at 50   ((1, 4), 64, (2, 1), 23, 2.78)
```

### The visual

Open [`examples/w09-focal-map.html`](../examples/w09-focal-map.html). The left view is an 8 by 5 value thumbnail you can paint. The right view is its local contrast map as a heat map, with the focal cell marked 1, the rival marked 2, and `H` printed above with a "clear" or "competing" label.

Load the doorway preset, then the torch preset. Drag the torch's value from 85 down to 50 and watch `H` climb past 1.5 as the label flips. Then load the silhouette preset and paint the cloud pure white. The left view gets brighter, but the heat map barely changes, and the marker stays on the dark figure. Brightness and attention are different things, and here you can see the gap.

### Cross-game recognition

**Mirror's Edge (DICE, 2008).** The game's Runner Vision turns objects the player can use (pipes, ramps, a zip line) bold red as the player approaches them. The city around them is mostly white, with strong primary colors and little green. The senior producer said the style grew out of the gameplay, so that players could focus on the red guidance. In our model, the art team pushed the background toward one flat, light value so that the neighbour mean around every red object is high and uniform. A saturated red is much darker than white in value, so each red object has a large `C`. And because the rest of the city is kept quiet, the rivals stay small and `H` stays high. The world is composed as a low-contrast field with a few high-contrast targets.

**Inside (Playdead, 2016).** Limbo's successor is mostly monochromatic, and it uses color sparingly to pick out the player's character and certain parts of the environment. That is scene D as a whole art direction. Everything that isn't a focal target is held to a narrow range of dull values, so that the few accents win clearly. Where Limbo steers with value alone, Inside keeps value doing most of the work and adds color only to raise a chosen cell's contrast further.

**Film and painting (Block's contrast and affinity).** Bruce Block's working rule for film is that contrast in a visual component raises intensity and **affinity** (similarity) lowers it. A cinematographer who wants you to look at one actor lights them differently from the rest of the frame and keeps the rest similar. That is `C` for the target and a small `C` for everything else, written in words for a film crew.

Three games and a film rule, one idea. The eye goes to the largest local difference. A designer controls the order of looking by deciding where differences are allowed to be large.

### Eyes-open design judgment

- **Quiet backgrounds are a choice with a cost.** Mirror's Edge's white city makes the red paths obvious, and some players find it sterile. A detailed, high-contrast environment is beautiful and harder to read. Decide which scenes need to be read in one second (combat, traversal under pressure) and which can reward slow looking (hubs, vistas).
- **Pick one focal point per frame and rank the rest.** The model penalizes two strong focal points because players split their attention. A scene can have many interesting things. It should have exactly one first thing.
- **Don't solve everything with brightness.** Scene B shows that big bright areas pull less than you'd think, and the silhouette case shows dark shapes can win. Reach for the value difference, in whichever direction the neighbourhood allows.
- **The model is value-only and still.** It ignores motion, faces, text and color. A moving enemy, a face or a word on screen will beat a static high-contrast cell. Use the model to clean up the environment so that those signals don't have to fight it.
- **Test at the right size.** A cell in a 6 by 4 thumbnail is a sixth of the screen. At that scale you're composing large masses. Check small targets, like a key on the floor, with a finer grid or the squint test at full size.

### Check yourself on the model

1. A cell of value 70 has neighbours 30, 30, 30, 40, 40, 40, 50 and 60. What is its local contrast?
2. A scene's focal cell has `C = 42` and the strongest non-touching rival has `C = 30`. What is `H`? What would you change, and by how much, to reach 1.5?
3. A bright cell of 90 sits in a field of 90s. Far away in the same field sits a dark rock of 10, whose neighbours are also all 90. Which has the higher local contrast?

<details>
<summary>Answers</summary>

1. Mean of neighbours `= 320 / 8 = 40`. `C = |70 − 40| = 30`.
2. `H = 42 / 30 = 1.4`, competing. To reach 1.5 you need the rival at most `42 / 1.5 = 28`, so bring the rival's value closer to its surroundings by at least 2 points of contrast, or raise the focal contrast to at least 45.
3. The bright cell has `C = |90 − 90| = 0`, since it matches its surroundings. The rock has `C = |10 − 90| = 80`. The brightest cell in the frame gets no attention at all.

</details>

## 3. Leading lines, framing and placement

Contrast decides where the eye lands first. Other tools decide where it goes next and how it gets there.

**Leading lines.** The eye tends to travel along strong edges and lines: a road, a wall's top edge, a row of lamps, a cliff's rim. If those lines point at the focal point, the eye slides to it. If they point off the edge of the screen, they carry the eye out of the frame. In a thumbnail, extend every strong line with a ruler. Count how many pass through or near the focal cell. A composition where most lines converge on the target reinforces the contrast model. One where lines lead elsewhere needs a higher `H` to compensate.

**Converging lines and perspective.** In a corridor seen in perspective, the floor, ceiling and wall edges all meet at the vanishing point. Put the exit at that point and every line in the scene leads to it. This is why so many linear games use long corridors with a lit door at the end. The contrast model and the lines agree.

**Framing.** A dark archway, overhanging branches or a gap between two buildings surround a region with a band of contrasting value. The frame raises the contrast at its edge and also cuts the region off from rivals outside. Scene A's doorway is framed by dark forest on every side, which is part of why its `H` is so high.

**Placement.** The rule of thirds divides the frame into a 3 by 3 grid and suggests placing the focal point near one of the four intersections instead of dead centre. It's a starting habit from photography and painting. It gives a sense of direction and space, and it isn't a law. In games the camera often locks the player character to the centre, so the character is already there. Environmental focal points then sit off-centre, ahead of the character in the direction of travel, which gives the player room to look into.

**Negative space.** Empty areas of low contrast are not wasted. They are what makes the focal point's neighbour mean low and uniform. A composition with no quiet areas has no clear hierarchy, because everything is a rival.

## 4. Composition when the camera moves

A painting is composed once. A game frame is composed sixty times a second by a camera the player controls. That changes what "composition" means for a game artist.

**The player character is a permanent focal point.** In most third-person and side-view games, the character stays near the centre and moves. It must always win against the environment behind it, which means the character's value range should differ from the background's. A character with dark values in a dark level vanishes. Week 3's silhouette test is the character half of this rule, and this week's contrast map is the environment half.

**Compose the likely views, not every view.** You can't control every camera angle, but you can predict the important ones. Those are the view on entering a room, the view from a ledge, and the view at the end of a corridor. Take screenshots from those positions, reduce them to thumbnails, and run the contrast model. The lab does exactly this.

**The HUD takes space.** Health bars, minimaps and hotbars usually sit in the corners and along the bottom. They are high-contrast by design, so they are permanent rivals. Keep your environment focal points out of the HUD's regions, and keep the HUD's values from overpowering the play area. Week 11 on UI hierarchy returns to this.

**Hierarchy has to survive chaos.** In combat, effects and enemies flood the screen with contrast. An environment that already uses its full value range leaves no room for the effects to read. Keep environment values in a narrower band during combat spaces, so that enemies and telegraphs can own the extremes. Week 10 builds on this.

## In-class activity (25 minutes)

Work in groups of three with the five screenshots each of you brought.

1. For each screenshot, one person reduces it to a 6 by 4 grid of values by eye, writing a number from 0 to 100 in each cell. (Use the interactive's "image" tool if you prefer. It averages each cell for you.)
2. Another person, without seeing the grid, marks on the full screenshot where they looked first.
3. Compute `C` for the three most likely cells by hand and find the focal cell and `H`.
4. Compare the prediction with where your classmate looked. Record hit or miss.
5. For every miss, name the thing the model ignores that won (motion blur, a face, text, color, a leading line).

Expected output: a table of 15 screenshots with predicted focal cell, `H`, observed first look, hit or miss, and a reason for each miss. The class pools its tables at the end to see how often a value-only model predicts the first look.

## Common misconceptions

- **"The eye goes to the brightest thing."** It goes to the largest local difference. A dark shape on a light field often wins, as in the silhouette example.
- **"More detail makes a focal point stronger."** Detail at thumbnail size averages out to a mid value. It can make a region interesting on second look, but it rarely wins the first.
- **"Composition is for concept art, not gameplay."** In a game, composition decides whether players find the exit, see the enemy and ignore the scenery. It is a readability tool.
- **"Follow the rule of thirds."** It's a starting habit. In games the character often sits at the centre, and a scene's hierarchy comes from contrast and lines far more than from grid placement.

## Check yourself

1. Compute `C` for the cell of value 20 at row 0, column 0 in scene A. It has only three neighbours.
2. In scene C, an artist proposes making the door brighter to win back the hierarchy. The door is already 85. What is the most the door's contrast can reach if its value goes to 100, and what is `H` then? Is that enough?
3. You have a greyscale thumbnail where the exit sits at `C = 30` and a decorative statue at `C = 45`, far from it. List two changes to the statue and one to the exit's surroundings that would each push `H` for the exit above 1.5, with the numbers each change needs.
4. Why do the three bright sky cells in scene B each score lower than the lone torch in scene C, even though both are bright?

<details>
<summary>Answers</summary>

1. Neighbours are (0,1) = 20, (1,0) = 20 and (1,1) = 20. Mean 20, so `C = 0`.
2. The door's neighbour mean is 21.25, so at 100, `C = 100 − 21.25 = 78.75`. `H = 78.75 / 58 = 1.36`, still below 1.5. Brightening the door alone doesn't fix it. You have to lower the rival, as scene D does.
3. The exit needs `C_exit ≥ 1.5 × C_statue`. With the exit at 30, the statue must fall to `C ≤ 20`, a cut of 25. Change one: move the statue's value 25 points toward its neighbour mean. Change two: leave the statue alone and repaint its neighbours so their mean moves 25 points toward the statue's value. Change three, on the exit side: with the statue still at 45, the exit needs `C ≥ 67.5`, so move the mean of the exit's neighbours at least 37.5 points away from the exit's value.
4. Each sky cell has other bright sky cells among its neighbours, which raises the neighbour mean and shrinks the difference. The torch is a single bright cell surrounded by dark forest. Contrast depends on the neighbourhood, not on brightness.

</details>

## Lab / assignment hook

[Lab 09, composing for the first look](../labs/lab09.md). You paint three greyscale thumbnails of one game scene with the focal point in three different places, run the provided focal-map script on each, and test the predictions on two classmates. Deliverable: three PNGs that meet the target, the script's reports, and a 250-word note comparing the model with where people actually looked.

## Sources

- Wikipedia, "Limbo (video game)" (Playdead, 2010; article read September 2026). Greyscale, monochromatic presentation with lighting and film-grain effects; reviewers' comparisons to film noir and silent film. https://en.wikipedia.org/wiki/Limbo_(video_game)
- Wikipedia, "Mirror's Edge" (DICE, 2008; article read September 2026), citing IGN and MTV interviews. Runner Vision turns usable objects red; outdoor environments mostly white with strong primary colors and little green; senior producer Owen O'Brien on the style growing from gameplay. https://en.wikipedia.org/wiki/Mirror%27s_Edge
- Wikipedia, "Inside (video game)" (Playdead, 2016; article read September 2026). Mostly monochromatic, with color used sparingly to highlight the player and parts of the environment. https://en.wikipedia.org/wiki/Inside_(video_game)
- Block, B. (2008). *The Visual Story* (2nd ed.). Focal Press. The principle of contrast and affinity, which has its own chapter ("Contrast & Affinity" in the publisher's table of contents for the current edition, Routledge, read September 2026).
- Solarski, C. (2012). *Drawing Basics and Video Game Art*. Watson-Guptill. Course reading on composition and value.
- The local contrast model, the hierarchy ratio, its 1.5 threshold and all thumbnail values are this course's teaching model, a simplified single-feature version of saliency.

## Interactive spec: examples/w09-focal-map.html

**Purpose.** Show that the eye's first target is the cell most different from its neighbours, not the brightest cell, and let students fix competing focal points by changing values.

**Layout.** Two linked views, side by side on desktop, stacked on mobile.

- **Left: thumbnail.** An 8 by 5 grid of grey cells (value V rendered as the sRGB grey whose CIE L* is nearest V, using week 1's formulas), each labelled with its value in small text (toggle). Paint with a value brush: pick a value with a slider or with number keys 0-9 (0 = 0, 9 = 90, Shift+9 = 100), then click, tap or drag over cells. Keyboard: arrow keys move a focus ring, Enter paints. Presets only use part of the grid where noted; unused cells take the preset's background value.
- **Right: contrast map.** The same grid, each cell colored by `C` on a single-hue sequential scale from the shared palette (0 = lightest, 80+ = darkest) with `C` printed in each cell. The focal cell gets a ring and the label "1". The rival gets a dashed ring and "2". Cells touching the focal cell are faintly hatched to show they are excluded from the rival search.
- **Status bar above both views:** "Focal (r, c) C = 64 · Rival (r, c) C = 8 · H = 8.00 · clear focus" or "… · competing". Use the label "clear focus" when `H ≥ 1.5`, "competing" otherwise.

**Presets.** Put the lecture's 6 by 4 scenes in the top-left 6 by 4 cells. Fill column 6 and 7 and row 4 as described.

- "Doorway": scene A. Columns 6-7 rows 0-2 = 20, row 3 all 35, row 4 all 35.
- "Doorway + sky": scene B, same padding.
- "Torch": scene C, same padding. "Torch dimmed" = scene D.
- "Silhouette": rows 0-2 = 80, rows 3-4 = 30, figure 15 at (1, 2), cloud 100 at (1, 4), all other columns sky or ground by row.
- "Blank 50": every cell 50 (H undefined; show "no focal point" when the maximum C is 0).

**Formulas.** `C = |V − mean(neighbours)|`, up to 8 neighbours, fewer at borders, rounded to the nearest integer for display but compared unrounded. Focal = max C (ties broken by lowest row, then lowest column). Rival = max C among cells whose Chebyshev distance from the focal cell is greater than 1. `H = C_focal / C_rival`, shown to 2 decimals; if `C_rival = 0`, show "H = ∞".

**Test values (8 by 5 padded grids, unrounded).** Doorway: focal (1, 4) C = 63.75, rival (2, 2) C = 6.25, H = 10.20. Doorway + sky: rival (0, 1) C = 35.00, H = 1.82. Torch: rival (2, 1) C = 58.12, H = 1.10, "competing". Torch dimmed: rival (2, 1) C = 23.12, H = 2.76. Silhouette: focal (1, 2) C = 65.00, rival is the cloud (1, 4) C = 20.00, H = 3.25. The exact torch values are 58.125 and 23.125; displays round to two decimals half to even, as Python's `round` does, so they show as 58.12 and 23.12. Padding changes the doorway's rival from the lecture's 6 by 4 value (8.0) because the padded cells add quiet neighbours; show the padded numbers.

**"Image" tool.** A file input that loads a local image, converts every pixel to CIE L* with week 1's formulas (linearize sRGB, relative luminance Y, then L*), to match `focal_map.py` in lab 09, averages it into the 8 by 5 grid, and replaces the thumbnail. Nothing is uploaded.

**Insight to make obvious.** In the Silhouette preset, painting the cloud from 100 down to 80 and back changes the left view visibly while the focal marker never leaves the dark figure.

**Accessibility and style.** Tokens from `templates/interactive-tokens.css`, inline. The heat map uses one hue plus printed numbers, so it works without color vision. All painting reachable by keyboard. No animation beyond instant updates.
