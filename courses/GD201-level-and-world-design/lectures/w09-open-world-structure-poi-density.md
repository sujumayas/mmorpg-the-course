# GD201 · Week 09 — Open-world structure: POI density

**Why this matters:** "The map is huge but there's nothing to do" and "the map is cluttered with icons" are the two complaints every open world gets, sometimes about the same game. Both are about one number: how many seconds a player travels between interesting things. That number comes from two quantities you control, how densely you place content and how fast the player moves, and one of them enters squared.

**You will be able to:**
- Compute the travel gap between points of interest from density and speed, and the density needed to hit a target gap.
- Explain, with numbers, why doubling travel speed divides the content needed for the same rhythm by four, and use that to price mounts and fast travel against content.
- Compare grid, random and jittered POI layouts by their empty areas, and audit a zone for dead zones.
- Critique a shipped open world's structure by rewriting its travel speeds and placement rules into the same model.

**Before class:** Christopher Totten, *An Architectural Approach to Level Design* (2nd ed., CRC Press, 2019), chapter 7 "Rewards in Gamespaces" and chapter 10 "Possibility Spaces and Worldbuilding". Play 20 minutes of any open-world game on foot, and write down the time each time something makes you change direction.

**Prerequisites from earlier courses:** [MA101 week 2, linear functions and rates](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w02-linear-functions-and-rates.md) (time equals distance over speed; unit conversion). [MA101 week 14, distances and ranges](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w14-distances-ranges-and-squared-distance.md) (Euclidean distance and circles of radius `r`). From this course, [week 3, flow and pacing](w03-flow-pacing-and-intensity-graphs.md) (rhythm as alternating tension and rest), [week 4, landmarks](w04-guiding-the-player-landmarks-light-weenies.md) (the distance `d_max` at which a landmark stays legible) and [week 7, verticality](w07-verticality-and-navigation.md) (edge times and why height changes what you can see).

**Interactive:** [`examples/w09-poi-gap.html`](../examples/w09-poi-gap.html). Keep it open during section 2.

---

## 1. Open worlds are built from gaps

A linear level decides the order of its content. An **open world** lets the player choose the order, and often the route, across a large area. The designer gives up control of the sequence and keeps control of two things: where content sits and how fast players move between it.

Terms for this week:

- A **point of interest (POI)** is any place that gives the player something to do or notice: a camp of enemies, a shrine, a village, a vista, a chest, a quest giver. Designers disagree about what counts. Decide for your project and apply it the same way everywhere. This lecture counts a POI as something worth stopping for.
- **Density** `ρ` (the Greek letter rho) is POIs per square kilometre.
- **Spacing** `a` is the typical distance from a POI to its nearest neighbour, in metres.
- **Travel speed** `v` is how fast the player crosses open ground, in metres per second. It changes with sprinting, mounts, vehicles and gliders.
- The **travel gap** `t` is the time between leaving one POI and reaching the next.
- **Dwell time** is the time spent at a POI once you arrive.

Week 3 described pacing as alternating tension and release. In an open world, the travel gap is the release and the POI is the tension, and the player's own movement sets the tempo. Get the gap wrong in one direction and the world feels empty. Get it wrong in the other and players never get to enjoy the scenery, because another icon is always pulling at them.

## 2. Worked example: walking-speed math

### The hook

In World of Warcraft's early patches (1.x), the first mount was bought at level 40 and made you 60% faster. That sounds like a 60% change. But think about what it does to the world. In one minute of riding you can reach any point inside a circle of radius `1.6` times as large as before. The area of that circle grows with the square of the radius, `1.6² = 2.56`. So the mount didn't make the world 60% smaller. It made each minute of travel reach 2.56 times as much ground.

Every open world designer who adds a mount, a glider or a fast-travel point is changing that square. This section shows what it does to the gaps between POIs.

### The model

Put the POIs on a square grid with spacing `a`. Each grid cell is `a × a`, so each POI "owns" `a²` of ground and the density is:

```
ρ = 1 / a²           (a in km gives ρ in POIs per km²)
a = 1 / sqrt(ρ)
```

A player walking from one POI to the nearest one covers `a` metres at speed `v`, so the travel gap is:

```
t = a / v = 1 / (v × sqrt(ρ))
```

Turn it around to get the density you need for a target gap:

```
ρ_needed = 1 / (v × t)²
```

That last line holds the whole lesson. **Speed enters squared.** Double `v` with the same target gap and you need one quarter the POIs. Halve `v` and you need four times as many. Travel speed is a multiplier on your content budget, and it multiplies by its square.

The square comes from the two dimensions of the map. On a road, which is one dimension, POIs per kilometre scale with `v`, not `v²`. That difference matters in section 4.

### Numbers you can check

World of Warcraft's standard running speed is 7 yards per second. At 0.9144 m per yard that is 6.40 m/s, close to the 6 m/s this course uses for teaching levels. Take a target travel gap of 30 seconds (an invented design target for this example, not a figure from Blizzard). Using the standard `+60%` and `+100%` mount speeds:

| Travel mode | `v` (m/s) | Spacing `a = v t` | Density needed | POIs in a 2 km × 2 km zone |
|---|---|---|---|---|
| On foot | 6.40 | 192 m | 27.1 per km² | 108 |
| Mount +60% | 10.24 | 307 m | 10.6 per km² | 42 |
| Mount +100% | 12.80 | 384 m | 6.8 per km² | 27 |

Check the first row by hand. `v = 7 × 0.9144 = 6.40`. Spacing `6.40 × 30 = 192` m `= 0.192` km. Density `1 / 0.192² = 1 / 0.0369 = 27.1`. Multiply by the zone's 4 km² to get 108.5.

Compare the first and last rows. The fast mount doubles speed, and the zone needs a quarter of the POIs, 27 instead of 108. Or read it the other way. Take the zone built for walkers (192 m spacing) and ride it:

| Travel mode on the walker's zone | Travel gap |
|---|---|
| On foot | 30.0 s |
| Mount +60% | 18.75 s |
| Mount +100% | 15.0 s |

The mounted player meets POIs twice as often. If each POI has a dwell time of 45 seconds, the walker spends `45 / (45 + 30) = 60%` of their time at content, and the fast rider `45 / (45 + 15) = 75%`. The rider also finishes the zone in `108 × (45 + 15) = 6,480` s, 1.8 hours, where the walker needs `108 × 75 = 8,100` s, 2.25 hours. Speed spends your content faster.

Here is the table in code. Keep it. The lab builds on it.

```python
from math import sqrt, pi

YARD = 0.9144                      # metres per yard

def spacing_for_gap(v, gap):
    """Grid spacing in metres so that POIs are `gap` seconds apart at speed v (m/s)."""
    return v * gap

def density_for_gap(v, gap):
    """POIs per square kilometre on a square grid with that spacing."""
    a_km = spacing_for_gap(v, gap) / 1000
    return 1 / a_km ** 2

walk = 7 * YARD                    # 7 yards per second, in m/s
for label, v in [("on foot", walk), ("+60% mount", walk * 1.6), ("+100% mount", walk * 2.0)]:
    a, rho = spacing_for_gap(v, 30), density_for_gap(v, 30)
    print(f"{label:12} v={v:5.2f} m/s  spacing {a:5.0f} m  density {rho:5.1f}/km2  "
          f"POIs in 4 km2: {4 * rho:5.1f}")
```

Output:

```
on foot      v= 6.40 m/s  spacing   192 m  density  27.1/km2  POIs in 4 km2: 108.5
+60% mount   v=10.24 m/s  spacing   307 m  density  10.6/km2  POIs in 4 km2:  42.4
+100% mount  v=12.80 m/s  spacing   384 m  density   6.8/km2  POIs in 4 km2:  27.1
```

Open the interactive. The left view is a top-down 2 km zone with POIs and a player who walks from each POI to the nearest unvisited one. The right view is a timeline strip: one bar per leg, its length the travel gap in seconds, with a line at your target. Set the mode to "+100% mount" and watch the timeline bars shrink to half while the map doesn't change at all. Then drag the density slider down until the bars return to 30 s. The number of POIs on the map drops to a quarter. The map looks empty. The timeline looks the same as the walker's.

### Cross-game recognition

**World of Warcraft (flying, Warlords of Draenor onward).** Flying mounts in WoW move far faster than ground travel and ignore the ground paths entirely. From Warlords of Draenor (2014) on, Blizzard held flying back in new zones until players earned a "Pathfinder" achievement later in the expansion. The achievement arrived in patch 6.2.0, and flying opened for its holders in patch 6.2.2. The stated reason was a compromise: players should experience the content on the ground rather than fly over it. In our terms, the zones were laid out for ground `v` and ground paths. A speed several times higher squares its way through the content budget, and it also removes the path structure (week 7's graph) that decided the order players met things.

**Minecraft (Java Edition, 1.21 era).** Minecraft places villages with two numbers. The world is cut into a grid of cells `spacing` chunks wide (34 for villages), and one village generation attempt is made per cell, at least `separation` chunks (8) from its neighbours. A chunk is 16 blocks, so the attempts sit on average `34 × 16 = 544` blocks apart. At the wiki's walking speed of 4.317 blocks per second, that is `544 / 4.317 = 126` seconds between village attempts. Sprinting at 5.612 blocks per second, 97 seconds. The density of attempts is `1 / 0.544² = 3.4` per km². Not every attempt produces a village, since the biome must allow one, so real gaps are longer. Minecraft's world generator is our model written as configuration: a grid spacing, a speed, and a gap that falls out of them.

**The Legend of Zelda: Breath of the Wild (2017).** Breath of the Wild changes how many POIs a player can *see*, not how many there are. Its 15 Sheikah Towers are climbable, and activating one gives the detailed map of the area around it. Height widens the view (week 7), and the paraglider turns height into horizontal travel at the same time. Section 4 turns "how many can I see" into a formula. Breath of the Wild is the case where the designers spent effort on visibility as well as density.

Three games, one relationship. The travel gap is spacing over speed, spacing comes from density, and the content you need scales with speed squared.

### Design judgment, eyes open

- **Pick a design speed per region and say it out loud.** A starting area walked on foot needs about 2.5 times the density of one crossed on a +60% mount (`1.6² = 2.56`). If both areas get the same density, one is packed and the other empty. The table in this section is a planning tool. Fill it in before you place anything.
- **A mount is a content decision.** Each speed boost cuts the time a zone lasts and the density it needs. Either build new zones at the lower density, or keep speed boosts out of dense areas (towns, dungeons, slow-travel zones). WoW's delayed flying is the second choice made at the scale of a whole expansion.
- **Fast travel skips gaps entirely.** A player who teleports to a waypoint spends zero seconds in the gap. That's right for backtracking (week 10). It's wrong for the first visit, which is why many games unlock fast travel only to places you have already reached on foot.
- **Don't fill every gap.** A 30-second gap is not dead time. It is where players read landmarks (week 4), plan, and enjoy the view. Worlds that squeeze gaps to near zero stop feeling like places and start feeling like checklists.
- **Density is not quality.** The model counts POIs as equal. A 30-second gap between two boring camps feels longer than a 60-second gap to a memorable one. Use the model to set the budget, then spend playtest time on which POIs work.

## 3. Grid, random or jittered

The square grid is a model, not a layout. Real worlds place POIs by hand or by rules, and the arrangement matters as much as the count.

**Pure random placement.** Scatter POIs uniformly at random at density `ρ`. The chance that a given spot has no POI within distance `r` is:

```
P(no POI within r) = exp(−ρ × π × r²)
```

For the walker's zone (`ρ = 27.1` per km²), the worst spot in the square grid is at the center of a cell, `a / sqrt(2) = 136` m from the nearest POI. With random placement at the same density, `exp(−27.1 × π × 0.136²) = exp(−1.575) = 0.21`. So 21% of the map is farther from any POI than the worst spot on the grid. Random placement has the same average and much worse holes. Some areas get clusters that feel crowded, and others get dead zones that feel empty.

**Grids feel artificial.** Players notice a camp every 192 m in a straight line. Nature doesn't do that.

**Jittered placement** is the usual compromise. Start from a grid, move each POI a random distance within its cell, and keep a minimum separation between neighbours. That's exactly Minecraft's spacing and separation rule. It keeps the grid's bound on empty space and hides its regularity. Poisson-disk sampling, a common algorithm in procedural generation, gets a similar result by rejecting points closer than a minimum distance.

**Hand placement** follows the terrain: POIs at river crossings, on hills, at the ends of sightlines. Audit it with the same tools. Compute the nearest-neighbour distance of every POI and the largest empty circle in the zone. The lab gives you a script for both.

## 4. Density you walk, density you see

The travel gap measures what happens after the player chooses a destination. Choosing needs a POI in view. If the player can make out a POI at distance `r` (week 4's `d_max`), the expected number in view in open terrain is:

```
N_visible = ρ × π × r²
```

With `r = 300` m:

| Density | `N_visible` |
|---|---|
| 27.1 per km² (tuned for walking) | 7.7 |
| 10.6 per km² (tuned for +60% mount) | 3.0 |
| 6.8 per km² (tuned for +100% mount) | 1.9 |

The walker's zone shows almost eight candidates at once, which can feel like a checklist. The fast rider's zone shows about two, which is enough to always have a next target. Here the square works in the designer's favour. Visibility grows with `r²`, so a small increase in how far players can see makes a sparse zone feel purposeful. Raise `r` from 300 m to 450 m in the rider's zone and `N_visible` goes from 1.9 to 4.3.

That's the reasoning behind towers, hills and overlooks as open-world furniture. They raise `r` for a moment, so the player sees many POIs at once and plans a route, then comes down to ground level where only one or two are visible and the gap does its work. Week 7's overlook before the drop is the same idea at the scale of one level.

Roads are the 1D case. Along a road, POIs per kilometre set the gap directly (`t = spacing / v`), and speed enters once, not squared. Roads concentrate players and let you pace content along one line, which is why open worlds often lay a road network over a sparser 2D field. Week 10 looks at how those paths join up.

## In-class activity (25 minutes)

Pairs, with the interactive and a printed 2 km × 2 km grid.

1. (5 min) Choose a design speed for your zone (on foot, or one mount speed) and a target travel gap between 20 and 60 s. Compute the spacing and the number of POIs.
2. (10 min) Place the POIs by hand on the grid, following terrain you sketch in (a river, a ridge, a road). Avoid a visible grid.
3. (5 min) Find the largest empty circle on your map by eye and measure its radius. Convert it to seconds at your speed. Is it more than twice your target gap?
4. (5 min) Now give the player a mount 60% faster. Decide what you'll change: remove POIs, add a slow-travel area, or accept shorter gaps. Write one sentence of justification.

Expected output: a hand-placed map, the four numbers (speed, gap, spacing, count), the largest empty circle in seconds, and your mount decision.

## Common misconceptions

- **"Twice as fast means half the content."** In an open field, it means a quarter. Content scales with speed squared in 2D, and only linearly along a road.
- **"Random placement is natural, so it's fair."** Random placement has the same average spacing as a grid but many more large holes. About one fifth of the map is emptier than the grid's worst spot at the density in section 3.
- **"More icons on the map means more to do."** The icons you can see scale with `ρ r²`. A dense zone with long view distances shows more than a player can use, and the extra ones read as chores.
- **"The travel gap is dead time."** It's the rest in the rhythm. A world with no gaps has no pacing.

## Check yourself

1. A game's base run speed is 5 m/s and the design target is a 40-second gap. What spacing and density does that imply? How many POIs in a 3 km × 3 km zone?
2. The same game adds a sprint that is 30% faster. By what factor should density fall to keep the 40-second gap while sprinting? Check it against Minecraft's walk and sprint speeds.
3. A zone has 12 POIs per km² placed at random. What fraction of the zone is more than 200 m from the nearest POI? What would that fraction be on a square grid of the same density?
4. A designer wants players to see at least 3 POIs at any time in a zone tuned for a +100% mount (6.8 per km²). How far must the legible distance `r` be?

<details>
<summary>Answers</summary>

1. Spacing `5 × 40 = 200` m. Density `1 / 0.2² = 25` per km². Area 9 km², so 225 POIs.
2. Density scales as `1 / v²`, so by `1 / 1.3² = 1 / 1.69`, a drop of about 41%. Minecraft: `5.612 / 4.317 = 1.30`, and `1.30² = 1.69`.
3. Random: `exp(−12 × π × 0.2²) = exp(−1.508) = 0.22`, so about 22%. Grid: spacing `1 / sqrt(12) = 0.289` km, the worst spot is `0.289 / sqrt(2) = 0.204` km from a POI. Only tiny corners of each cell are over 200 m away, so the fraction is close to zero (under 1%).
4. `6.8 × π × r² = 3` gives `r² = 3 / 21.36 = 0.140` km², `r = 0.375` km, about 375 m.

</details>

## Lab / assignment hook

[Lab 09, POI density audit](../labs/lab09.md). You implement the gap and density functions, a nearest-neighbour tour, a dead-zone finder and a visibility count, then audit a 2 km zone with 60 POIs that hides one large dead zone and one crowded cluster. You fix it for a walking design speed and again for a mounted one. It counts toward the analysis component, and your fixed layout is a starting point for the final zone.

## Sources

- Warcraft Wiki, "Speed" (accessed September 2026). Standard running speed 7 yards per second; a standard ground mount gives a 60% speed increase and an epic ground mount 100%.
- Warcraft Wiki, "Riding" (accessed September 2026). Before patch 1.12.1 riding was a single-rank ability bought at level 40; Apprentice (+60%) and Journeyman (+100%) ground riding; from Warlords of Draenor, flying tied to achievements later in each expansion as a compromise so players experience content on the ground; the Draenor Pathfinder achievement added in patch 6.2.0, with flying enabled for holders in patch 6.2.2.
- Minecraft Wiki, "Walking" and "Sprinting" (Java Edition). Walking 4.317 m/s (blocks per second), sprinting about 5.612 m/s, 30% faster.
- Minecraft Wiki, "Structure set" (Java Edition, 1.21 era). Villages use separation 8 and spacing 34 chunks; spacing is the average distance between neighbouring generation attempts and separation the minimum. Minecraft Wiki, "Chunk": a chunk is 16 × 16 blocks.
- Zelda Wiki, "Sheikah Tower" (*Breath of the Wild*, 2017). Fifteen towers; activating one gives a detailed map of the surrounding area.
- Totten, C. (2019). *An Architectural Approach to Level Design* (2nd ed.). A K Peters/CRC Press. Chapters 7 and 10 (doi:10.1201/9781351116305-7 and -10; titles checked on Crossref, September 2026).

## Interactive spec: examples/w09-poi-gap.html

**The one insight.** Doubling travel speed halves every travel gap. To get the old rhythm back you need only a quarter of the POIs, so a zone that looks nearly empty on the map can feel exactly as busy as a packed one.

**Layout.** Two linked views, stacked on narrow screens.

- **Left: top-down 2 km × 2 km zone.** POIs as small generic markers. The player's tour is drawn as connected line segments from the start (the POI nearest the center) to each nearest unvisited POI in turn, up to 30 legs. Legs longer than twice the target gap (at the current speed) are drawn in the warning colour and dashed. An optional overlay shows the dead zones: cells of a 50 m raster farther than `r_dead` from any POI, shaded.
- **Right: timeline strip.** One bar per leg in tour order, bar length = leg distance / `v` seconds, on an axis 0 to 120 s. A vertical line marks the target gap. Readouts: "Mean gap 30.0 s", "Longest gap", "POIs 100 on the grid (108 by formula)", "Density 27.1 per km²", "Visible within r: 7.7 (expected)".

**Controls.**
- Travel mode: segmented control On foot (6.40 m/s), Mount +60% (10.24), Mount +100% (12.80), Custom (slider 2 to 20 m/s, step 0.1).
- Density slider, 2 to 40 POIs per km², step 0.1, default 27.1. The POI count is `round(4 × ρ)`.
- Layout: Grid, Jittered (each POI uniformly within the central `(1 − 2s/a)` part of its cell where `s = 0.15a`), Random. Default Grid. Seeded generator (seed 9) so the first screen is fixed; a "Reshuffle" button changes the seed.
- Target gap slider, 10 to 90 s, step 5, default 30.
- "Match target" button: sets density to `1 / (v × target / 1000)²`.
- Legible distance `r` slider, 100 to 800 m, step 25, default 300 (used for `N_visible = ρ π (r/1000)²`).
- Toggle dead-zone overlay with `r_dead` = grid worst case `a / sqrt(2)` for the current density.

**Formulas.** `a = 1000 / sqrt(ρ)` m. Grid layout: POIs at cell centers of an `a` grid clipped to the zone (the count may differ from `round(4ρ)` by edge effects; show the actual count). Travel gap for a leg of length `d`: `d / v`. `ρ_needed = 1 / (v t / 1000)²`. Dead-zone fraction for random layout, shown as a readout: `exp(−ρ π (r_dead/1000)²)`.

**Test values.**
- On foot, ρ = 27.1, grid, target 30: spacing 192 m, grid legs 30.0 s each, `N_visible` at 300 m = 7.66.
- Switch to Mount +100% without changing density: grid legs 15.0 s. Mount +60%: 18.8 s (the lecture's 18.75 s uses the exact 192.0 m spacing; the slider's rounded ρ = 27.1 gives 192.1 m).
- Grid at ρ = 27.1 draws 100 POIs (a 10 × 10 grid of 192.1 m cells fits in 2 km), not the formula's 108; the page shows both counts.
- Mount +100%, press "Match target": ρ = 6.78, spacing 384 m, legs 30.0 s, `N_visible` = 1.92.
- Mount +60%, "Match target": ρ = 10.6, spacing 307 m.
- Random layout at ρ = 27.1: dead-zone readout 0.21 (21%).
- ρ = 6.8, `r` = 450 m: `N_visible` = 4.33.

**Accessibility.** All controls keyboard operable. Long legs are dashed as well as coloured. The timeline has a text table fallback listing each leg's seconds. Respect `prefers-reduced-motion` (no animated walker; draw the tour at once) and `prefers-color-scheme`.
