# GD201 · Week 04 — Guiding the player: landmarks, light, weenies

**Why this matters:** A player who doesn't know where to go stops playing your level and starts playing "find the exit." Landmarks and light are how you steer people without arrows or text, and both obey simple optics. If you don't do the arithmetic, you will place a tower that looks enormous in the editor and turns out to be a speck on the player's screen.

**You will be able to:**
- Compute the share of the screen a landmark fills from its height, its distance and the camera's field of view, and convert between horizontal and vertical field of view.
- Derive the largest distance at which a landmark stays legible, and the height a landmark needs to be legible from a given viewpoint.
- Compute the luminance contrast ratio between a lit target and its background, and predict when a light will guide and when it will vanish.
- Design a landmark hierarchy for a zone using Lynch's five elements, and critique a shipped game's use of a "weenie."

**Before class:** Christopher Totten, *An Architectural Approach to Level Design* (2nd ed., CRC Press, 2019), chapter 4, the sections "Pathfinding with Architectural Weenies" and "Organizing the Sandbox: Kevin Lynch's Image of the City." Kevin Lynch, *The Image of the City* (MIT Press, 1960), the chapter on the city image and its elements. Play the first 20 minutes of any open-world game and, every time you change direction, write down what made you turn.

**Prerequisites from earlier courses:** [MA101 week 10, angles, sine and cosine](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w10-angles-radians-sin-cos.md) (the tangent of an angle as rise over run). [MA101 week 6, rational functions](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w06-rational-functions-and-asymptotes.md) (why a quantity like `h / d` falls off as a hyperbola). [UX201 week 1, perception and attention](../../UX201-game-ux-and-player-psychology/lectures/w01-perception-attention-memory.md) (what the eye picks out before the player thinks). From this course, [week 2, blockout and greyboxing](w02-blockout-and-greyboxing.md) and [week 3, flow and pacing](w03-flow-pacing-and-intensity-graphs.md). You will greybox this week's landmarks with week 2's tools.

**Interactive:** [`examples/w04-landmark-range.html`](../examples/w04-landmark-range.html). Keep it open during section 2.

---

## 1. Why players need something to walk toward

Walk out of an unfamiliar hotel and, before choosing a direction, you look for something big you recognize and for the brightest, most open route. Players do the same in a level. The skill of finding your way through a space is called **wayfinding**, and a level designer's job is to make it easy when the game is about something else, and hard only when being lost is the point.

The vocabulary we will use comes from urban planning. In 1960 Kevin Lynch published *The Image of the City*, a study of how residents of Boston, Jersey City and Los Angeles drew their cities from memory. He found that people build their mental maps from five kinds of element.

- **Paths** are the channels people move along: streets, trails, canals, corridors.
- **Edges** are boundaries that stop or redirect movement: walls, shorelines, cliffs, rivers.
- **Districts** are areas with a shared character that you feel yourself enter and leave: the market quarter, the swamp, the ruined district.
- **Nodes** are places where paths meet and people gather: squares, crossroads, a camp.
- **Landmarks** are reference points you see but usually don't enter: a tower, a mountain, a giant tree.

This lecture is about the last one, plus light, which is how you make any of the five stand out. Next week covers the small-scale cues (a painted ledge, a rope, a door that looks openable). Here we deal with the large-scale ones that you can see from across a zone.

### The weenie

Walt Disney's designers had a name for a landmark whose job is to pull people toward it. They called it a **weenie**, after the hot dog you wave in front of a dog to get it to follow you. Cinderella Castle at the Magic Kingdom in Florida is the textbook case. It stands at the end of Main Street, U.S.A., and it was conceived as the main weenie that draws guests from the entrance, up the street, to the central hub from which every other area of the park can be reached.

The weenie gives you a direction and a reason to keep walking from the moment you enter. Totten brings the term into level design in today's reading. A weenie is a landmark with a job, placed to pull players along the route you want and sized so they can see it from where they start.

That second condition is where designers go wrong. "Visible" is not a feeling. It is a number of pixels, and you can compute it.

## 2. Worked example: how tall must a landmark be?

### The hook

Journey (thatgamecompany, 2012) opens with a small robed figure in a desert. Walk to the top of the first dune and a huge mountain with a glowing crack in its peak fills the horizon. The game never tells you to go there. It doesn't need to. The mountain is the destination of the whole game, and you can see it from the first minute.

Now picture your own first open zone. You place a 50-meter watchtower at its center as the weenie. In the editor it looks huge, because the editor camera is 200 meters away. Then the playtest reports come in. Players who spawned in the far corner, two kilometers away, say they never noticed a tower. Were they not paying attention, or was the tower too small? You can answer that before the playtest.

### The model

A game camera is a pinhole camera. Everything you see lies inside a pyramid that opens from the camera. The **vertical field of view** `V` is the angle between the top and bottom edges of that pyramid.

Stand at distance `d` from a landmark and look straight at it. At that distance, the top half of the view rises `d × tan(V/2)` above the center line. That is the tangent from MA101 week 10, rise over run. So the whole screen, from bottom edge to top edge, covers a slice of the world `2 d tan(V/2)` tall. A landmark of height `h` fills a fraction of that slice:

```
f = h / (2 × d × tan(V/2))
P = f × S
```

- `h` is the landmark's height in meters (or any unit, as long as `d` uses the same one).
- `d` is the distance from the camera to the landmark along the view direction.
- `V` is the vertical field of view.
- `f` is the **screen fraction**, the share of the screen height the landmark covers.
- `S` is the screen height in pixels, and `P` is the landmark's height on screen in pixels.

This formula is exact for a perspective camera, not an approximation, as long as `d` is measured along the view direction. The whole model is one ratio, `h / d`, times a constant set by the camera.

### Horizontal and vertical field of view

Convert before you compute. Unity's camera stores the vertical angle, while many options menus show a horizontal one. With Hor+ scaling, the most common approach, the vertical angle is fixed and the horizontal angle grows with the aspect ratio. For a screen of aspect ratio `a` (width divided by height):

```
V = 2 × atan( tan(H/2) / a )
```

At 16:9 (`a = 1.778`), a horizontal field of view of 90° gives `tan(45°) = 1`, so `tan(V/2) = 1 / 1.778 = 0.5625` and `V = 58.7°`. That makes `2 tan(V/2) = 1.125` exactly, which keeps this lecture's arithmetic clean. We will use a 90° horizontal view at 16:9 from here on unless we say otherwise.

| Horizontal FOV at 16:9 | Vertical FOV | `2 tan(V/2)` |
|---|---|---|
| 60° | 36.0° | 0.650 |
| 70° | 43.0° | 0.788 |
| 90° | 58.7° | 1.125 |
| 110° | 77.6° | 1.607 |

### Numbers you can check

With `2 tan(V/2) = 1.125` and a 1080-pixel-tall screen, the 50-meter tower gives `f = 50 / (1.125 d)` and `P = 1080 × f = 48,000 / d`.

| Distance `d` | Screen fraction `f` | Pixels at 1080p |
|---|---|---|
| 100 m | 44.4% | 480 |
| 250 m | 17.8% | 192 |
| 500 m | 8.9% | 96 |
| 1,000 m | 4.4% | 48 |
| 2,000 m | 2.2% | 24 |
| 4,000 m | 1.1% | 12 |

Double the distance and the on-screen height halves, the hyperbola `1/d` from MA101 week 6. At 2 km your tower is 24 pixels tall, easy to miss on a busy horizon. The playtesters were not careless.

The Python below prints the table.

```python
import math

def vertical_fov(h_fov_deg, aspect=16 / 9):
    return 2 * math.degrees(math.atan(math.tan(math.radians(h_fov_deg) / 2) / aspect))

def screen_fraction(height, distance, v_fov_deg):
    return height / (2 * distance * math.tan(math.radians(v_fov_deg) / 2))

V = vertical_fov(90)
print(f"V = {V:.1f} degrees")
for d in (100, 250, 500, 1000, 2000, 4000):
    f = screen_fraction(50, d, V)
    print(f"{d:>5} m  {f:6.1%}  {1080 * f:5.0f} px")
```

It prints `V = 58.7 degrees`, then the six rows with 480, 192, 96, 48, 24 and 12 pixels.

### Legibility range

Now turn the question around. Pick the smallest screen fraction at which your landmark still reads as a landmark, and call it `f_min`. Solve the model for `d`:

```
d_max = h / (2 × f_min × tan(V/2))
```

There is no universal value for `f_min`. It depends on the landmark's shape, its contrast with the sky, the clutter around it and the player's screen size. You set it by testing in your own game. For this lecture we will use `f_min = 2%` of screen height, about 22 pixels at 1080p. That is a starting guess for a high-contrast silhouette against open sky, and the in-class activity asks you to measure your own.

With `f_min = 0.02` and `2 tan(V/2) = 1.125`, the range is `d_max = h / 0.0225`, or about `44.4 × h`.

| Landmark | Height `h` | Legible up to `d_max` |
|---|---|---|
| Person-sized marker | 2 m | 89 m |
| Large tree | 10 m | 444 m |
| Ruined keep | 25 m | 1,111 m |
| Watchtower | 50 m | 2,222 m |
| Castle spire | 57.6 m | 2,560 m |
| Cliff face | 100 m | 4,444 m |
| Mountain | 300 m | 13,333 m |

Read the table the other way, too. To be legible from the far corner of a zone 2.5 km away, a landmark needs `h = 0.0225 × 2,500 = 56` meters. Your 50-meter tower was close, but under. If you can't make it taller, you have three other levers in the formula. You can move it closer to the spawn (smaller `d`). You can give it a light or a strong color so that a smaller `f_min` still reads (section 3). Or you can accept that players in the corner will orient by a different, nearer landmark (section 4).

### What resolution does and doesn't change

A player on a 4K screen (2,160 pixels tall) sees the 2 km tower at 48 pixels instead of 24. That doesn't double its range. A 27-inch monitor is the same physical size at 1080p and at 4K, so the tower covers the same share of the player's eye. What matters to a human is the screen fraction `f`, which is why this lecture sets the threshold as a fraction. Pixels matter only for thin, distant features one or two pixels wide, which flicker.

Field of view is different. It changes `f` directly. A player who widens the horizontal view from 60° to 90° divides every landmark's height on screen by `1.125 / 0.650 = 1.73`. The legibility range shrinks by the same factor. If your game lets players change field of view, test landmarks at the widest setting you allow.

### Reading a landmark's size off a screenshot

You often want to know how big a shipped game's landmarks are. You can't read them from the game's files, but you can measure them. Take a screenshot at a known distance (many games show distance to a map marker). Measure the landmark's height in pixels, `P`. Rearrange the model:

```
h = P × 2 d tan(V/2) / S
```

Suppose a 1080p screenshot with a 90° horizontal view shows a tower 60 pixels tall from 800 meters. Then `h = 60 × 800 × 1.125 / 1080 = 50` meters. A second screenshot from 400 meters should show 120 pixels. If it doesn't, check the distances, not the field of view. `P × d = h × S / (2 tan(V/2))` is the same for both shots whatever `V` you assumed, so a mismatch means a distance is off or the camera changed. Test the field of view with an object of known height, such as a door.

### The visual

Open [`examples/w04-landmark-range.html`](../examples/w04-landmark-range.html). The left view is a simple horizon from the player's position with a generic tower drawn at its true screen size. The right view plots the screen fraction against distance, with a horizontal line at `f_min`. The point where the curve crosses the line is `d_max`.

Drag the distance slider and watch the tower shrink while the marker slides down the hyperbola. Double the height. The curve doubles and `d_max` moves twice as far out. Switch 1080p to 4K. The pixel readout doubles, but the curve and `d_max` stay put. Widen the field of view and the curve sinks. Legibility is a ratio of height to distance, and the camera sets the exchange rate.

### Cross-game recognition

The same ratio sits under every weenie. What varies is how the designer raised `h / d` or lowered the threshold.

**Magic Kingdom, Cinderella Castle (opened 1971).** The castle stands 56 meters (183 feet) above the water, or 57.6 meters (189 feet) measured from the bottom of its moat. That is the "castle spire" row in the table. The designers also used **forced perspective**, making details smaller toward the top so the eye reads the building as taller than it is. In our model, forced perspective raises the *perceived* `h` without adding real height. Disneyland's Sleeping Beauty Castle, at 23 meters (77 feet), uses the same trick, with larger elements at the base and smaller ones at the turrets. By our model its legibility range is only 40% of Cinderella Castle's, which is fine in a smaller park with a shorter approach.

**Journey (thatgamecompany, 2012).** The mountain is the extreme case. It is so large that `h / d` stays above any threshold from the first dune to the last scene. The game uses one landmark for its entire length, and the glowing crack at the peak adds a light cue on top of the silhouette.

**The Legend of Zelda: Breath of the Wild (Nintendo, 2017).** When Link places the Sheikah Slate in the first terminal, 15 Sheikah Towers rise out of the ground across Hyrule at once. Each is a tall, narrow structure, and each one glows blue once activated. After the first tower is activated, the game's shrines begin to glow orange. Rewrite this in our terms. The towers are landmarks tall enough to be legible from far away, placed so that from almost anywhere at least one is inside `d_max`. The colored glow lowers the effective `f_min`, so shrines, which are small, still register from a distance. Notice that the 15 towers look alike. They don't help you tell one place from another. They mean one thing, "climb me to see the map," and their spacing is the design decision.

For any game's landmarks, ask what `h / d` is from the start, and how the designer lowered the threshold when `h / d` fell short.

### Eyes-open design judgment

Landmark arithmetic tells you whether a landmark can be seen. It doesn't tell you whether it should be. Decide these on purpose.

- **Size for the worst viewpoint, not the average.** Compute `d_max` against the farthest place a player can start or respawn, and against the widest field of view you allow. The editor camera is the least representative viewpoint in the project.
- **Tall landmarks are expensive.** A 300-meter mountain legible from 13 km must be rendered from 13 km. Draw distance and fog cap `d_max` regardless of height. Behind a fog wall at 1.5 km, a landmark 2 km away doesn't exist.
- **One weenie per decision.** A weenie answers "which way?" If the player can see three equally strong weenies, it answers nothing. Use one global landmark per zone and let smaller ones do local work.
- **A landmark must be unique to orient.** Breath of the Wild's towers look the same on purpose because they share one function. If you want players to know *where* they are, each landmark needs a distinct silhouette. A second copy of the castle on the other side of the map destroys the first one's value.
- **Occlusion beats arithmetic.** A 100-meter cliff behind a 20-meter ridge has an `f` of zero. Check sightlines from the start points in the greybox. Week 7 (verticality) and week 12 (sightlines) return to this.

### Check yourself on the landmark

1. A 30-meter lighthouse stands 1,200 meters from the player. The game uses a 90° horizontal view at 16:9. What fraction of the screen does it fill, and how many pixels is that at 1080p?
2. The same game's options menu lets players pick a 70° horizontal view. From how far away is the lighthouse legible at `f_min = 2%` with 70°, and with 90°?
3. A designer wants a weenie legible from a spawn point 3.6 km away, with a 90° horizontal view. How tall must it be at `f_min = 2%`? At `f_min = 1.5%`, if you add a strong light?

<details>
<summary>Answers</summary>

1. `f = 30 / (1.125 × 1,200) = 0.0222`, so 2.2% of the screen, `0.0222 × 1080 = 24` pixels.
2. At 70°, `2 tan(V/2) = 0.788`, so `d_max = 30 / (0.02 × 0.788) = 1,904` m. At 90°, `d_max = 30 / 0.0225 = 1,333` m. The narrower view makes the lighthouse legible about 570 meters farther out.
3. `h = 0.02 × 1.125 × 3,600 = 81` m. With `f_min = 0.015`, `h = 0.015 × 1.125 × 3,600 = 60.75` m, about 61 m. The light is worth 20 meters of tower.

</details>

## 3. Light: contrast is the signal

Designers say "players follow the light." Totten's chapters on symbols and on shade and shadow treat light and contrast as a guiding tool, and you will see it in almost any linear game. The lit doorway at the end of a dark corridor, the patch of sun in a forest clearing, the lamp above the right house. The heuristic works, but it works for a precise reason. The eye doesn't respond to brightness alone. It responds to the difference in brightness between a thing and what surrounds it. A bright light on a bright wall guides nobody.

You need a number for that difference. The one used in accessibility standards is the **contrast ratio** from WCAG 2.1, the W3C's web accessibility guidelines. It is built for text on screens, which makes it a reasonable proxy for "does this shape stand out from that background" on the same screens.

First compute each color's **relative luminance** `L`, its brightness on a scale from 0 (black) to 1 (white). Take each 8-bit channel, divide by 255, and linearize it. Values at or below 0.04045 are divided by 12.92, and larger values `c` become `((c + 0.055) / 1.055)^2.4`. Then weight the channels by how sensitive the eye is to each:

```
L = 0.2126 R + 0.7152 G + 0.0722 B
contrast ratio = (L_lighter + 0.05) / (L_darker + 0.05)
```

The ratio runs from 1 (no difference) to 21 (black on white). WCAG asks for at least 3:1 for user-interface components and large text, and 4.5:1 for body text.

Here are the numbers for a few colors a level artist might use. Compute them yourself in the lab.

| Target | Background | L target | L background | Contrast ratio |
|---|---|---|---|---|
| Lit doorway (235, 200, 140) | Stone wall (60, 58, 66) | 0.609 | 0.044 | 7.02 |
| Unlit doorway (90, 80, 70) | Stone wall (60, 58, 66) | 0.084 | 0.044 | 1.42 |
| Dark tower (40, 40, 48) | Day sky (170, 190, 215) | 0.022 | 0.503 | 7.70 |
| Glowing tower (120, 200, 255) | Day sky (170, 190, 215) | 0.525 | 0.503 | 1.04 |
| Dark tower (40, 40, 48) | Night sky (24, 28, 48) | 0.022 | 0.012 | 1.15 |
| Glowing tower (120, 200, 255) | Night sky (24, 28, 48) | 0.525 | 0.012 | 9.22 |

Look at the tower rows. By day, the dark silhouette stands out at 7.7:1 and the glow does nothing (1.04:1, almost invisible). At night the numbers swap. The dark tower disappears into the sky and the glow carries the whole signal. A landmark that must work around the clock needs both, a dark mass and a light. If your game has a day-night cycle, test landmarks at the worst hour, not the prettiest one.

The doorway rows show the classic lighting trick. The same doorway goes from 1.42:1 to 7:1 when you light it. A lit exit reads at a glance. An unlit one blends into the wall.

Contrast connects the two halves of this lecture. Higher contrast lowers the `f_min` a landmark needs, because a small shape that differs sharply from its background still pops out (UX201 week 1). That is why Breath of the Wild's blue and orange glows work on small objects. They lower the threshold instead of raising the height.

Three cautions keep this honest.

- **The formula measures luminance, not hue.** Two colors of equal luminance, such as a saturated red and a saturated green, have a ratio near 1 even though they look different to most players. For a colorblind player they may look the same. Guide with brightness first and color second.
- **Tone mapping changes the numbers.** Engines render light in high dynamic range and then compress it to the screen. Measure contrast from a screenshot of the final image, not from the material color in the editor.
- **Players adapt.** Many engines apply automatic exposure that brightens dark scenes over a second or two. Your lit doorway at the end of a dark tunnel may look less bright once the player's view has adjusted. Measure after the exposure settles.

## 4. A landmark plan for a zone

One landmark rarely covers a whole zone. Plan in layers, using Lynch's vocabulary.

1. **One global landmark** (the weenie). Visible from every start and respawn point in the zone, so `d_max` is at least the longest start-to-landmark distance. It sets the zone's main direction.
2. **A few district landmarks.** Each marks one district and is legible within it and from its neighbors. A player who can see two district landmarks and the global one can place themselves on the map without opening it.
3. **Local cues.** Lit doors, open gates, a trail of torches. These operate over tens of meters and belong to next week's topic, signposting.

Landmarks serve **orientation** ("where am I?") and **attraction** ("where should I go?"). A global landmark does both. A district landmark mostly orients. If every landmark pulls, none does. Also respect Lynch's other elements. A landmark seen across an impassable edge, like a chasm, is a promise. If no path leads toward it for ten minutes, it breeds frustration. That can be a deliberate tease, but choose it. Weeks 9 and 10 return to this with points of interest and gating.

A useful table for your zone document lists, for every start point, which landmarks are legible from it. Compute each distance from the map coordinates, compare it with each landmark's `d_max`, and mark the cell. Any start point with no legible landmark is a place where players will open the map or wander. The lab has you build exactly this table.

## 5. Landmarks in a shared world

This program's specialization is persistent online worlds, and landmarks do extra work there.

**Landmarks become language.** In a single-player game, a landmark talks to one player. In an online world, players use landmarks to talk to each other. "Meet at the big tree." "The camp is south of the broken bridge." A landmark that players can name gives a group a shared coordinate system with no user interface at all. When you design a landmark for a shared zone, ask whether players can describe it in two words. A "big tree" is nameable. A "slightly different ruin" is not.

**Landmarks must stay put.** In a persistent world, player building, events and later expansions can each block a sightline that used to work. List the protected sightlines in the zone's design document, the way a city protects the view of a cathedral.

**Crowds compete with the landmark.** Moving characters, effects and name plates are all distractors, so thresholds you tested alone may fail with 40 players on screen. Test with placeholder crowd clutter. Week 11 covers shared spaces.

## In-class activity (25 minutes)

Work in pairs with the interactive and a greybox of your own or the course's sample zone.

1. **Measure `f_min` (10 minutes).** One partner sets up the interactive with a tower of fixed height and hides the distance readout. The other partner looks at the horizon view for two seconds and says whether they see the tower. Move the distance until the answer flips. Repeat three times with clutter on and three times with clutter off. Record the screen fraction at which the tower stops being noticed. Compare your two `f_min` values with the lecture's 2%.
2. **Size a weenie (10 minutes).** Your zone is 3 km by 3 km, with three start points in three corners and the weenie at the center of the fourth side. Using your measured `f_min` (with clutter) and a 90° horizontal view, compute the minimum height of the weenie. Then compute the height again for players who set the view to 110°.
3. **Swap and critique (5 minutes).** Swap numbers with another pair. Find one start point in their plan where the weenie is legible but likely hidden behind terrain or at the wrong time of day.

Expected output: two measured `f_min` values, a weenie height at 90° and at 110°, and one weakness your partners found.

## Common misconceptions

- **"If it looks big in the editor, it's big enough."** The editor camera is close and usually narrow. The player is far away with a wide view. Compute the screen fraction from the worst start point.
- **"Higher resolution makes distant landmarks more visible."** It adds pixels, not size. On the same monitor, the landmark covers the same share of the player's view at 1080p and at 4K. Only field of view and distance change the screen fraction.
- **"Make it glow and players will see it."** Glow is a contrast tool, and contrast depends on the background. A glow against a bright sky can have a ratio near 1. Check the ratio at every time of day.
- **"More landmarks mean better navigation."** Past one weenie per zone, landmarks compete. The player needs one strong answer to "which way?" and a few distinct answers to "where am I?"

## Check yourself

1. A game uses a vertical field of view of 50°. A 40-meter tower stands 900 meters away. What screen fraction does it fill? What is its legibility range at `f_min = 2%`?
2. A designer doubles the height of a landmark and, to save rendering cost, also pushes the fog wall from 3 km to 2 km. The landmark sits 2.5 km from the spawn. Before the change, it was 50 m tall with a 90° horizontal view at 16:9 and `f_min = 2%`. Is it legible from the spawn before the change? After?
3. A level artist lights a doorway with warm light and the doorway's color becomes (200, 150, 90) against a wall of (120, 110, 100). The relative luminances are 0.348 and 0.161. What is the contrast ratio? Does it meet the 3:1 bar for interface components?
4. Explain, in terms of `h`, `d` and `f_min`, why Breath of the Wild can make shrines small but still findable from a distance.

<details>
<summary>Answers</summary>

1. `2 tan(25°) = 0.9326`. `f = 40 / (0.9326 × 900) = 0.0477`, about 4.8% of the screen. `d_max = 40 / (0.02 × 0.9326) = 2,145` m.
2. Before, `d_max = 50 / 0.0225 = 2,222` m, less than 2.5 km, so it is not legible from the spawn. After, the 100 m landmark has `d_max = 4,444` m by size, but the fog wall at 2 km hides everything beyond 2 km. It is still invisible from the spawn. The fog change cancelled the height change.
3. `(0.348 + 0.05) / (0.161 + 0.05) = 0.398 / 0.211 = 1.89`. That's under 3:1. The warm light changed the hue more than the brightness. Brighten the doorway or darken the wall.
4. `d_max = h / (2 f_min tan(V/2))`. Shrines have a small `h`, which on its own would give a short range. The orange glow gives them high contrast against most backgrounds, which lowers `f_min`. A smaller threshold makes up for the smaller height.

</details>

## Lab / assignment hook

[Lab 04, landmark legibility audit](../labs/lab04.md). You write a small Python tool that reads a zone's landmarks and start points, computes screen fractions and contrast ratios, and prints a legibility matrix. Then you use it to fix the sample zone so that every start point sees the weenie and at least one district landmark. The greybox you fix feeds the blockouts assessment (40%).

## Sources

- Lynch, K. (1960). *The Image of the City*. MIT Press. Paths, edges, districts, nodes and landmarks, from studies of Boston, Jersey City and Los Angeles. Summary checked against Wikipedia, "The Image of the City."
- Totten, C. W. (2019). *An Architectural Approach to Level Design* (2nd ed.). CRC Press. Chapter 4 ("Pathfinding with Architectural Weenies," "Organizing the Sandbox: Kevin Lynch's Image of the City"), chapter 5 (contrast, symbols as guides), chapter 6 (shade and shadow). Table of contents checked on the publisher's page, Routledge.
- Wikipedia, "Cinderella Castle." Height 183 ft (56 m) above water, 189 ft (58 m) including the moat; the castle conceived as the primary "weenie" drawing guests through Main Street, U.S.A.; forced perspective. Magic Kingdom, opened 1971.
- Wikipedia, "Sleeping Beauty Castle." Height 77 ft (23 m); forced perspective with larger elements at the foundation and smaller ones at the turrets.
- Wikipedia, "Journey (2012 video game)." The mountain with a glowing crevice seen from the first dune as the game's destination. thatgamecompany, 2012.
- Zelda Wiki, "Sheikah Tower" (Breath of the Wild, 2017). Fifteen towers rise across Hyrule when the Sheikah Slate is placed in the first terminal; activated towers glow blue; shrines begin to glow orange after the Great Plateau Tower is activated; towers give map data.
- Wikipedia, "Field of view in video games." Horizontal and vertical field-of-view conversion with aspect ratio; Hor+ as the most common scaling method.
- Unity Scripting Reference, "Camera.fieldOfView" (current documentation). The camera's field of view is the vertical angle in degrees.
- W3C (2018, updated). *Web Content Accessibility Guidelines (WCAG) 2.1*. Definitions of relative luminance (sRGB linearization threshold 0.04045, coefficients 0.2126, 0.7152, 0.0722) and contrast ratio `(L1 + 0.05) / (L2 + 0.05)`; success criteria 1.4.3 (4.5:1 and 3:1) and 1.4.11 (3:1 non-text).

## Interactive spec: examples/w04-landmark-range.html

**The one insight.** A landmark's size on screen is `h / d` times a camera constant, so it falls off as a hyperbola. Doubling height doubles the legible range. Changing resolution changes pixel counts but not legibility. Widening the field of view shrinks everything.

**Layout.** Two linked views side by side on desktop (horizon left, chart right), stacked on mobile with the horizon on top. A readout panel sits under both.

**View A, "What the player sees".** A 16:9 viewport drawn in canvas or SVG. A flat horizon line at mid-height, a ground band below and a sky band above using palette tokens. A generic tower silhouette (a tall rectangle with a small pointed top, no real-world or game building) centered horizontally, its base on the horizon, drawn at height `f × viewport height`. If `f × viewport height < 1` px, draw a 1 px mark and label "below 1 px." When clutter is on, draw 30 low generic hill and tree shapes along the horizon with seeded random positions (seed 4) and heights between 0.5% and 3% of the viewport. When fog is on and `d > fog distance`, the tower is not drawn and a label says "beyond fog."

**View B, "Screen fraction vs distance".** x-axis distance from 0 to 5,000 m, ticks every 500 m. y-axis screen fraction from 0% to 20% (clip the curve above 20% with a small arrow label "off chart"). Plot `f(d) = h / (2 d tan(V/2))` for `d` from 50 m. Draw a horizontal dashed line at `f_min`, labeled "legibility threshold." Mark `d_max` with a vertical line and label "legible to X m." Draw the player's current distance as a dot on the curve. Shade the region `d > d_max` lightly. If fog is on, draw a vertical wall at the fog distance, label "fog," and shade everything beyond it. Also draw a faint "ghost" curve for the preset's original height so doubling height is visible as a second curve.

**Controls.**
- Landmark height `h`: 2 to 300 m, step 1, default 50.
- Distance `d`: 50 to 5,000 m, step 10, default 2,000.
- Horizontal field of view `H`: 50° to 120°, step 1, default 90.
- Aspect ratio: 16:9 (default), 21:9, 4:3.
- Resolution (screen height `S`): 720, 1080 (default), 1440, 2160.
- Threshold `f_min`: 0.5% to 5%, step 0.1%, default 2.0%.
- Toggles: clutter (default off), fog (default off), fog distance 500 to 5,000 m, step 100, default 3,000.
- Buttons: "Double height" (sets `h = 2h`, keeps ghost curve), presets "Watchtower (50 m)", "Castle spire (57.6 m)", "Small castle (23 m)", "Mountain (300 m)".

**Readouts (monospace, copyable).** `V` in degrees to 1 decimal, `2 tan(V/2)` to 3 decimals, `f` as a percent to 1 decimal, pixel height `P = f × S` to the nearest pixel, `d_max` in meters to the nearest meter, "legible" or "not legible" in words (and "hidden by fog" when applicable).

**Exact formulas.**
- `V = 2 atan(tan(H/2) / a)`, with `a` = 16/9, 21/9 or 4/3.
- `f = h / (2 d tan(V/2))`, `P = f × S`.
- `d_max = h / (2 f_min tan(V/2))`, then capped at the fog distance if fog is on.
- Legible if `f ≥ f_min` and (fog off or `d ≤ fog distance`).

**Test values (16:9, the build must reproduce these).**
- `H = 90°`: `V = 58.7°`, `2 tan(V/2) = 1.125`.
- `h = 50`, `S = 1080`, `H = 90°`: `d = 100` gives 44.4% and 480 px; 250 gives 17.8% and 192 px; 500 gives 8.9% and 96 px; 1,000 gives 4.4% and 48 px; 2,000 gives 2.2% and 24 px; 4,000 gives 1.1% and 12 px.
- `f_min = 2%`, `H = 90°`: `h = 50` gives `d_max = 2,222` m; `h = 57.6` gives 2,560 m; `h = 23` gives 1,022 m; `h = 100` gives 4,444 m.
- `H = 60°`: `V = 36.0°`, `2 tan(V/2) = 0.650`; `h = 50` gives `d_max = 3,849` m.
- `H = 70°`: `2 tan(V/2) = 0.788`; `h = 30` gives `d_max = 1,904` m (check yourself question 2).
- `S = 2160`, `h = 50`, `d = 2,000`, `H = 90°`: 2.2%, 48 px, `d_max` unchanged at 2,222 m.
- Fog at 2,000 m, `h = 100`: `d_max` shown as 2,000 m (fog), size-only range 4,444 m listed beside it.

**First screen.** `h = 50`, `d = 2,000`, `H = 90°`, 1080p, `f_min = 2%`, clutter on. The tower is a thin 24 px sliver among clutter, and the chart dot sits just above the threshold line. Caption: "24 pixels. Legible on paper, easy to miss on a busy horizon. Try doubling the height."

**Accessibility and motion.** All controls are native labeled inputs, reachable by keyboard. The legible/not legible state is shown in words, not only color. No animation except an optional 300 ms ease when "Double height" is pressed; skip it under `prefers-reduced-motion`. Palette from `templates/interactive-tokens.css`, light and dark.
