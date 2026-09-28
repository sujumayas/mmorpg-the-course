# GS101 · Week 08 — 3D and the genre explosion

**Why this matters:** Between 1992 and 2001, games moved from flat maps to polygon worlds, and a whole shelf of new genres appeared: the 3D platformer, the 3D action-adventure, survival horror, the open-world city game. It is tempting to say "the hardware got better, so games got better." This week gives you a sharper tool. You will compute what the hardware actually allowed per frame, see how designers hid the limits, and read famous design features (fog, cameras, lock-on targeting) as answers to problems that 3D created.

**You will be able to:**
- Compute a per-frame polygon budget from a throughput figure and a frame rate, and a maximum draw distance from that budget.
- Explain why doubling the frame rate cuts draw distance by about 29% rather than half, and when fixed costs make it worse.
- Identify fog, camera systems and lock-on targeting in late-1990s games as responses to specific 3D problems, citing the game and era.
- Write a "constraint reading" of a 3D game that separates what the hardware forced from what the designers chose.

**Before class:** Donovan, *Replay: The History of Video Games* (2010), the pages on the 32-bit and 64-bit console generation and on id Software's shooters. The course reader lists the pages. Watch any five minutes of recorded play of a mid-1990s 3D console game (for example Turok: Dinosaur Hunter or Silent Hill) and write down every place you notice the edge of the visible world.

**Prerequisites from earlier courses:** None; this is a first-semester course. The model uses only multiplication, division and a square root. If you want the maths behind it, [MA101 week 3, polynomials and quadratic curves](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w03-polynomials-and-quadratic-curves.md) explains why area grows with the square of distance, and [MA101 week 13, dot product, facing and vision cones](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w13-dot-product-facing-and-vision-cones.md) treats view cones properly. [GD101 week 13, genres as clusters of mechanics](../../GD101-introduction-to-game-design/lectures/w13-genres-as-clusters-of-mechanics.md) gives the definition of genre used in section 3. Last week's [lecture on the PC era](w07-the-pc-era-strategy-simulation-modding.md) covers Doom's modding; this week covers its rendering.

**Interactive:** [Draw distance budget](../examples/w08-draw-distance-budget.html). Keep it open during section 2.

---

## 1. From flat maps to polygon worlds

### 2.5D: the illusion of depth

id Software's Wolfenstein 3D (May 1992) and Doom (December 1993) looked three-dimensional, but their worlds were drawn from flat floor plans. Doom's levels have heights, stairs and lifts, yet no room can sit on top of another room, and enemies are flat pictures (sprites) that always face you. Players and historians call this **2.5D**: a 2D map rendered to look like 3D. It was fast enough to run on an ordinary home PC, which is why it came first.

### True 3D

A **polygon** is a flat shape, almost always a triangle, defined by its corners in 3D space. A **true 3D** engine builds everything (walls, floors, characters) from polygons and can draw them from any angle. id's Quake (June 1996) was the landmark on PC. Its engine used polygonal models instead of sprites and full 3D levels instead of a 2.5D map.

Consoles moved at the same time. Sony's PlayStation launched in Japan on 3 December 1994 with a dedicated chip for 3D geometry. Nintendo's Nintendo 64 followed in Japan on 23 June 1996, with an analog stick designed for moving in 3D, launching alongside Super Mario 64. On PC, 3dfx sent its Voodoo Graphics 3D chip to manufacturing in November 1995. When id released GLQuake in January 1997, a version of Quake that used 3D acceleration cards, the Voodoo was the only consumer card at the time that ran it well.

### Vocabulary for this week

- **Frame rate** (`f`): how many images the game draws per second, in frames per second (fps). 30 and 60 are the common targets.
- **Polygon throughput** (`R`): how many polygons the hardware can draw per second.
- **Polygon budget** (`P`): how many polygons you can afford in one frame.
- **Draw distance** (`d`): how far from the camera the game bothers to draw anything.
- **Pop-in**: objects suddenly appearing when they cross the draw distance.
- **Distance fog**: shading distant objects toward a flat colour so that, at the draw distance, they fade into haze instead of popping.

## 2. Worked example: why 1990s 3D worlds were foggy

### The hook

Play Turok: Dinosaur Hunter (Nintendo 64, March 1997) and you can see only a small circle of jungle around you. Dinosaurs charge out of thick white mist. Reviewers at the time noticed. GameSpot's reviewer liked how enemies emerged "fangs first" but also said the fog hid the console's limits. Two years later, Silent Hill (PlayStation, February 1999) wrapped its whole town in fog and darkness, and Edge magazine praised Konami for using the draw-distance problem to chilling effect.

Two games, two genres, the same fog. Was it style, or was it arithmetic? Here is the arithmetic.

### One model, stated once

```
P       = R × e / f                 polygons you can draw in one frame
P_world = P − C                     polygons left for the scenery
A       = P_world / ρ               ground area you can afford to show
A       = (θ / 2) × d²              area of a view cone of angle θ out to distance d
d       = √( 2 × P_world / (ρ × θ) )  maximum draw distance
```

- `R` is the hardware's polygon throughput per second, as printed on the spec sheet.
- `e` is efficiency, the share of `R` a real game achieves once it spends time on game logic, sound and everything else. Spec-sheet numbers are peak figures. We do not know `e` for any particular game, so it is an assumption you set, and you must say so.
- `f` is the frame rate.
- `C` is the fixed cost per frame: characters, weapons, the interface. It does not shrink when you look at less scenery.
- `ρ` (rho) is scene density, polygons per square metre of ground.
- `θ` (theta) is the horizontal field of view in radians. 90° is `π/2 ≈ 1.571`.

The last step comes from the area of a circular sector, `(θ/2) × d²`. That square is the whole story, as you will see.

### A spec-sheet number, read carefully

Sony's published figures for the original PlayStation give 360,000 flat-shaded polygons per second and 180,000 texture-mapped polygons per second. Those are what the spec sheet shows. They are not what any given game computes. Real games draw textured, lit polygons, and they share the machine with everything else. So we will take `R = 180,000` and set `e = 0.5`, a round assumption, not a measured value. With the interactive you can change it.

### Numbers you can check

Fix `R = 180,000`, `e = 0.5`, `θ = 90°` and `ρ = 0.5` polygons per square metre (an invented, sparse scene). First with no fixed cost (`C = 0`):

| Frame rate `f` | Budget `P` | `P_world` | Area `A` (m²) | Draw distance `d` (m) |
|---|---|---|---|---|
| 20 | 4,500 | 4,500 | 9,000 | 107.0 |
| 30 | 3,000 | 3,000 | 6,000 | 87.4 |
| 60 | 1,500 | 1,500 | 3,000 | 61.8 |

Check the 30 fps row by hand. `P = 180,000 × 0.5 / 30 = 3,000`. `A = 3,000 / 0.5 = 6,000`. `d = √(2 × 3,000 / (0.5 × 1.571)) = √(7,639) ≈ 87.4`.

Now the surprise. Going from 30 to 60 fps halves the budget, but the draw distance drops from 87.4 m to 61.8 m, only about 29%. Area grows with the square of distance, so half the area costs you only a factor of `1/√2 ≈ 0.71` in distance.

Now add a realistic fixed cost, `C = 1,000` polygons for the player's weapon, a few enemies and the interface:

| Frame rate `f` | Budget `P` | `P_world` | Draw distance `d` (m) |
|---|---|---|---|
| 20 | 4,500 | 3,500 | 94.4 |
| 30 | 3,000 | 2,000 | 71.4 |
| 60 | 1,500 | 500 | 35.7 |

With fixed costs, 60 fps cuts the scenery budget by three quarters, not half, and draw distance falls by half. The square root softens the blow of a smaller budget. Fixed costs sharpen it again, because they come off the top before the scenery gets anything.

Two more checks you can do with the interactive: widening the field of view to 120° at 30 fps with `C = 0` shrinks `d` from 87.4 m to 75.7 m, and doubling scene density to `ρ = 1` shrinks it to 61.8 m. Every extra tree, and every degree of peripheral vision, is paid for in distance.

### A visual you can move

The interactive has two linked views. The left view is a top-down map: the player at the bottom, a view cone, and a shaded sector showing what you can afford to draw. The right view is a first-person strip where the scene fades to fog at exactly `d`. Under both views sits the budget bar, split into fixed cost and scenery. The frame rate is a row of buttons (20, 25, 30, 50 and 60 fps). Click 30, then 60. On the map the cone looks like it barely shrinks. On the budget bar, half the polygons disappear. Then raise the fixed-cost slider and watch the cone collapse far faster than the bar. Toggle "fog off" to see the pop-in the fog was hiding.

### Cross-game recognition

Now read three games as solutions to the same equation.

**Turok: Dinosaur Hunter (Iguana Entertainment, Nintendo 64, 1997).** Dense jungle means a high `ρ`. A first-person view with enemies close to the player means a real fixed cost `C`. The equation says `d` must be small, and the game's answer was heavy distance fog. GameSpot's March 1997 review noted that the frame rate dropped when more than a few enemies were on screen, and that the fog was there to reduce the slowdown. That is the fixed cost `C` and the scenery budget fighting over the same `P`.

**Silent Hill (Konami, PlayStation, 1999).** The same PlayStation budget, a detailed town (high `ρ`), and a third-person camera. Konami used fog and darkness to hide pop-in and the hardware's limits, and turned the short `d` into the game's mood. The constraint did not change. What Konami decided to make of it did. You can hear the difference in the reviews: Edge treated it as a design achievement, not a workaround.

**Grand Theft Auto III (DMA Design, PlayStation 2, October 2001).** A whole city you can drive through at speed. Speed matters, because the faster you move, the sooner distant objects cross `d`. Reviewers of later ports still noted the short draw distance and sudden pop-up, and the Windows version of May 2002 supported a higher draw distance on stronger PCs. Same equation, one more generation of hardware, and `d` was still the pressure point.

A modern reader will recognize the same trade-off in any game that offers a "performance mode" (higher frame rate) and a "quality mode" (more detail, lower frame rate). The variables are the same ones in this model, even though modern engines use many more tricks to manage them.

### Eyes-open judgment

- **The model is a budget, not a renderer.** Real engines use culling (not drawing what is hidden behind walls), level of detail (fewer polygons for distant objects) and texture and fill-rate limits that this model ignores. It captures one pressure, the per-frame polygon budget, and that pressure was real. Do not claim it explains any single game's exact draw distance.
- **Spec sheets are not measurements.** Every value of `e` you pick is a guess. State it. When a source says a console "does 360,000 polygons per second," ask what kind of polygon and under what conditions.
- **Frame rate is a design decision.** Choosing 30 over 60 buys scenery. Choosing 60 buys responsiveness. Choosing a narrow field of view buys distance but can make players feel boxed in. None of these is correct in general. A historian should ask which one a team chose and what the game gained.
- **A limit can become a style.** Silent Hill shows that the same constraint can produce a workaround or an identity. When you close-read a game, do not stop at "the fog is a hardware limit." Ask what the designers did with it.

### Check yourself (worked example)

1. A console has `R = 360,000`, `e = 0.4`, and the game runs at 30 fps with `C = 800`. Scene density is `ρ = 0.5`, field of view 90°. Compute `P`, `P_world` and `d`.
2. A team wants to double its draw distance without changing hardware, density or field of view. By what factor must `P_world` grow? Is that possible by halving the frame rate alone?

<details>
<summary>Answers</summary>

1. `P = 360,000 × 0.4 / 30 = 4,800`. `P_world = 4,000`. `d = √(2 × 4,000 / (0.5 × 1.571)) = √(10,186) ≈ 100.9 m`.
2. `d` grows with the square root of `P_world`, so doubling `d` needs four times `P_world`. Halving the frame rate doubles `P` but, with a fixed cost `C`, more than doubles `P_world`. Setting `2P − C = 4(P − C)` shows it reaches four times only when `C = 2P/3`. For example, with `P = 3,000` and `C = 2,000`, `P_world` goes from 1,000 to 4,000 at half the frame rate, which doubles `d`. With `C = 0` it only doubles `P_world`, and `d` grows by 41%.

</details>

## 3. New problems, new genres

A **genre**, in the sense of GD101 week 13, is a cluster of mechanics that games share. The 3D shift did not only make old genres look different. It created new problems, and the clusters of solutions that worked became new genres.

### Problem 1: where is the camera?

In a 2D game, the camera is the screen. In 3D, it is a virtual object that someone has to place every frame. Super Mario 64 (Japan, June 1996) is the standard example. Its team began development with the characters and the camera system and spent months choosing a view. The game made the camera part of the fiction (a cloud-riding character films Mario) and let players rotate it or switch to first person. Reviewers praised the analog control and criticized the camera, which sometimes moved to unhelpful angles or got stuck behind walls. Both reactions are evidence. The first says the problem was solved well enough to play. The second says it was not solved.

The 3D platformer, as a genre, is a cluster built around that solution: analog movement in any direction, a camera that follows and can be adjusted, and levels designed as open spaces to explore rather than lines to run along.

### Problem 2: how do you fight something in 3D?

Swinging a sword at an enemy is easy in 2D, since you face left or right. In 3D, you have to aim in two dimensions while also moving and managing the camera. The Legend of Zelda: Ocarina of Time (November 1998) answered with **Z-targeting**: hold a button and the camera and your character lock on to one enemy, so movement becomes circling around the target. Nintendo presented the target marker as a fairy companion so it would feel less mechanical. Lock-on targeting became a default for 3D melee action games. When you play a modern action game and press a button to lock on, you are using the answer to a 1998 problem.

### Problem 3: how do you show the player where they are?

Flat maps are easy to read. A 3D world at a short draw distance is not. Solutions included landmarks visible above the fog, maps and compasses in the interface, and level structures (hub worlds, corridors) that limit how lost you can get. Survival horror took the opposite route. It made disorientation the point, using fixed or restricted cameras and fog to control what you see.

### The explosion as a table

| Problem 3D created | Signature answer | Example (era) | Genre cluster that formed |
|---|---|---|---|
| Camera placement | Following, adjustable camera; analog stick | Super Mario 64 (1996) | 3D platformer |
| Melee aiming | Lock-on targeting | Ocarina of Time (1998) | 3D action-adventure |
| Short draw distance | Fog as mood; restricted views | Silent Hill (1999) | Survival horror |
| Moving through a large world | Streaming city, vehicles, radio | Grand Theft Auto III (2001) | Open-world action |
| Polygon characters in close combat | Two fighters, small arena, high detail | Virtua Fighter (arcade, 1993) | 3D fighting |

The last row is worth a second look. Sega's Virtua Fighter reached arcades in 1993, before either 3D console, and its design fits the model from section 2 exactly. Two characters, a small arena and nothing in the distance. It puts almost the entire budget into the fixed cost `C` and almost nothing into scenery. A fighting game is the genre that fits early 3D hardware best, and it arrived early.

## 4. Reading history critically: technology is a pressure, not a cause

It is easy to write "3D technology created survival horror." That sentence is too strong. The PlayStation's budget pushed every PlayStation game toward short draw distances. Only some of them became survival horror. Technology sets the pressures. People choose the responses. Business and culture decide which responses spread.

A useful way to write about this is a **constraint reading**, in three steps.

1. **Name the constraint** with a number where you can. "PlayStation, about 3,000 textured polygons per frame at 30 fps under our assumptions."
2. **Find its trace** in the game. Fog at a fixed distance, a camera that avoids long views, levels built as rooms and corridors.
3. **Name the choice** the designers made about the trace. Hide it, dress it up or make it the point. Support your claim with evidence from the game or from what the developers or reviewers said at the time.

Step 3 is where the reading becomes criticism rather than a hardware report. Two teams facing the same limit made different games, and you want to say why.

## In-class activity (25 min)

In pairs, choose one 3D game released between 1996 and 2002 that one of you has played (or use a recorded playthrough).

1. Watch or play five minutes and log every trace of the draw distance: fog, darkness, pop-in, a camera that turns away from open spaces, walls that block long sightlines.
2. Using the interactive, pick values of `f`, `ρ`, `θ` and `C` that you think describe the game, and read off `d`. Write your assumptions in one line each.
3. Decide which of the three responses the game made to its constraint (hide, dress up, make it the point) and write two sentences of evidence.
4. Swap with another pair and challenge one of their assumptions.

Expected output: a trace log of at least five entries, one set of model values with `d`, and a two-sentence claim with evidence. These notes are the raw material for Lab 08.

## Common misconceptions

- **"60 fps halves the world."** Without fixed costs, it cuts draw distance by about 29%, because area grows with the square of distance. With large fixed costs it can be worse than half. Always ask what `C` is.
- **"The spec sheet tells you what the game draws."** Spec figures are peak throughput for a particular polygon type. Real games reach some fraction of them. That fraction is an assumption unless someone measured it.
- **"Fog was just a cheap trick."** It was a response to a real budget, and some teams made it central to the experience. Silent Hill's reviewers treated it as an achievement.
- **"Super Mario 64 solved the 3D camera."** It set a template that others followed, and reviewers at the time also criticized its camera. Camera design is still an active problem.

## Check yourself

1. A game runs at 30 fps with `P = 3,000`, `C = 1,000`, `ρ = 0.5` and a 90° field of view. The team cuts the fixed cost to 500 by simplifying enemies. What is the new draw distance? Compare it with the 71.4 m in section 2.
2. Explain in two sentences why a 3D fighting game suited 1993-era hardware better than a 3D open-world game. Use the symbols from the model.
3. A classmate writes "the PlayStation caused survival horror." Rewrite the claim so it survives the three-step constraint reading.
4. Name the 3D problem that Z-targeting answered, and one other game or genre you know that uses a descendant of that answer.
5. A modern game offers a 60 fps "performance mode" and a 30 fps "quality mode." Using the model, name two things the quality mode can spend its extra budget on, and state which one would change the draw distance.

<details>
<summary>Answers</summary>

1. `P_world = 2,500`, so `d = √(2 × 2,500 / (0.5 × 1.571)) = √(6,366) ≈ 79.8 m`, about 8 m more than 71.4 m. Cutting the fixed cost by half buys a noticeable but modest gain.
2. A fighting game shows two characters in a small arena, so almost the whole budget can go to `C` (detailed fighters) with small `P_world` and small `d`. An open world needs large `d` and often high `ρ`, which the budget could not pay for.
3. For example: "The PlayStation's per-frame budget forced short draw distances on its 3D games. Konami's Silent Hill team chose to make that limit the source of its atmosphere, and later survival horror games kept the choice." It names the constraint, the trace and the choice.
4. Aiming melee attacks at one enemy while moving in 3D. Most later 3D action games use a lock-on button, including many action RPGs.
5. It can spend it on scenery (`P_world`, which raises `d`) or on the fixed cost (`C`, more detailed characters, which does not). It can also raise `ρ` (denser scenes at the same `d`).

</details>

## Lab hook

[Lab 08, a constraint reading of a 3D game](../labs/lab08.md). You write a 900-word close reading of one game from 1996 to 2002 that names a technical constraint with numbers, documents its traces with timestamps or screenshots you describe in words, and argues what the designers chose to do with it. It is a practice run for the first graded close reading.

## Sources

- Wikipedia, "Wolfenstein 3D" and "Doom (1993 video game)", accessed September 2026. Release dates of 5 May 1992 and 10 December 1993.
- Wikipedia, "Quake (video game)", accessed September 2026. June 1996 release; polygonal models and full 3D levels instead of a 2.5D map; GLQuake beta on 22 January 1997 and the Voodoo as the only consumer card that ran it well.
- Wikipedia, "3dfx", accessed September 2026. Voodoo Graphics chip released to manufacturing on 6 November 1995.
- Wikipedia, "PlayStation (console)", accessed September 2026. Japanese launch on 3 December 1994.
- Wikipedia, "PlayStation technical specifications", accessed September 2026. 360,000 flat-shaded polygons per second (citing GamePro no. 72, September 1994) and 180,000 texture-mapped polygons per second. These are manufacturer peak figures, not measured in-game rates.
- Wikipedia, "Nintendo 64", accessed September 2026. Japanese launch on 23 June 1996.
- Wikipedia, "Super Mario 64", accessed September 2026. Development starting with the camera system, the Lakitu camera, analog control, and the mixed reviews of the camera in Next Generation and Electronic Gaming Monthly.
- Wikipedia, "Turok: Dinosaur Hunter", accessed September 2026. North American release on 4 March 1997; distance fog to reduce slowdown; Jeff Gerstmann's GameSpot review (4 March 1997) on slowdown with several enemies, fog used to reduce it, and enemies emerging from the mist.
- Konami of America press release, 23 February 1999 (konami.com/news/press/99/pr-990223.html, archived at web.archive.org/web/19990502204654/). North American release of Silent Hill, February 1999.
- Wikipedia, "Silent Hill (video game)", accessed September 2026. North American release in February 1999 (Japan in March); fog and darkness used to hide hardware limits and pop-in; Edge's Gameplay Innovation runner-up citation.
- Wikipedia, "Distance fog", accessed September 2026. Fogging as a response to limited processing power in mid-to-late 1990s games.
- Wikipedia, "The Legend of Zelda: Ocarina of Time", accessed September 2026. November 1998 release; Z-targeting and its fairy marker.
- Wikipedia, "Grand Theft Auto III", accessed September 2026. PlayStation 2 release on 23 October 2001; Windows release in May 2002 with higher draw distance; reviewers noting short draw distance and pop-up in later ports.
- Wikipedia, "Virtua Fighter (video game)", accessed September 2026. Arcade release in 1993.
- Donovan, T. (2010). *Replay: The History of Video Games*. Yellow Ant, East Sussex (xiv + 501 pp.).

## Interactive spec: examples/w08-draw-distance-budget.html

**Insight the visual must make obvious:** halving the polygon budget (for example, going from 30 to 60 fps) shrinks the visible world by only about 29% because area grows with the square of distance, but a fixed per-frame cost for characters and interface eats the scenery budget first and can cut draw distance by half or more.

**Layout:** two linked views side by side at 1280px, stacked at 390px (map on top). A horizontal budget bar and a numbers readout sit under both.

**Left view, "Top-down budget map":** the player as a small generic marker at the bottom centre, a view cone of angle `θ` opening upward, and a filled sector of radius `d` in the accent colour. Draw a faint reference arc at the default `d` (87.4 m) so changes are visible against it. Scatter generic tree glyphs (simple circles) at a density proportional to `ρ` across the whole map; those inside the sector are solid, those outside are ghosted. Include a distance scale bar in metres.

**Right view, "First-person strip":** a simple horizon view. Draw rows of generic tree shapes at increasing distance, scaled by perspective (`size ∝ 1/distance`). Apply linear fog from `0.7 × d` (no fog) to `d` (full fog colour). Objects beyond `d` are not drawn. With the "fog off" toggle, fog is disabled and objects beyond `d` still vanish, so the hard edge (pop-in line) is visible.

**Budget bar:** a single horizontal bar of length proportional to `P`, split into `C` (fixed cost, secondary colour) and `P_world` (accent colour), with both values printed. If `C ≥ P`, show `P_world = 0`, `d = 0` and a warning "No budget left for scenery."

**Controls (all keyboard operable, with visible numeric values):**
- Throughput `R`: preset buttons "360,000 (flat-shaded spec)", "180,000 (textured spec)" (default), plus a numeric input 10,000 to 2,000,000.
- Efficiency `e`: slider 0.1 to 1.0, step 0.05, default 0.5. Label it "assumption".
- Frame rate `f`: segmented control 20 / 25 / 30 / 50 / 60, default 30.
- Fixed cost `C`: slider 0 to 3,000, step 100, default 0.
- Density `ρ`: slider 0.1 to 2.0, step 0.05, default 0.5 polygons per m².
- Field of view `θ`: slider 45° to 120°, step 5°, default 90°.
- "Fog off" toggle (default off).
- Presets: "Section 2, no fixed cost" (defaults), "Section 2, C = 1,000", "Fighting game" (`C = 2,500`, `ρ = 0.5`, `f = 30`), "Wide view" (`θ = 120°`).
- Reset button.

**Formulas:** `P = R × e / f`; `P_world = max(0, P − C)`; `A = P_world / ρ`; `θ_rad = θ × π / 180`; `d = √(2 × P_world / (ρ × θ_rad))`. Also show the ratio `d / d_ref` where `d_ref` is `d` at the same settings but `f = 30`.

**Readout:** `P`, `C`, `P_world`, `A` (m², integer), `d` (m, one decimal), `d / d_ref` (two decimals).

**Test values (R = 180,000, e = 0.5, ρ = 0.5, θ = 90° unless stated):**
- `C = 0`: `f = 20` gives `P = 4,500`, `d = 107.0`; `f = 30` gives `P = 3,000`, `A = 6,000`, `d = 87.4`; `f = 60` gives `P = 1,500`, `d = 61.8`, `d / d_ref = 0.71`.
- `C = 1,000`: `f = 20` gives `d = 94.4`; `f = 30` gives `d = 71.4`; `f = 60` gives `P_world = 500`, `d = 35.7`, `d / d_ref = 0.50`.
- `C = 0`, `f = 30`, `θ = 120°`: `d = 75.7`. `θ = 60°`: `d = 107.0`.
- `C = 0`, `f = 30`, `ρ = 1.0`: `d = 61.8`. `ρ = 0.25`: `d = 123.6`.
- `R = 360,000`, `e = 0.4`, `f = 30`, `C = 800`: `P = 4,800`, `P_world = 4,000`, `d = 100.9`.

**Motion and theme:** animate sector radius changes over 200 ms unless `prefers-reduced-motion` is set. Fog colour follows the page background token so it reads correctly in light and dark mode. No game art, logos or screenshots; all shapes are generic.
