# MA201 · Week 11 — Spatial Partitioning: Grids and Quadtrees

**Why this matters:** Week 9's overlap tests and week 10's impulses are cheap for one pair and ruinous for every pair. Before any of them run, the engine has to find the few pairs worth testing. You already know one way to do that, the uniform grid from CS102. This week you learn to choose its cell size with a formula instead of a guess, to see exactly when no cell size works, and to build the structure that adapts instead, the quadtree.

**You will be able to:**
- Compute the expected work of a grid query from the query radius, the cell size and the local density, and find the best cell size.
- Predict when one grid cannot serve a whole world, using the ratio of the best cell sizes in its busiest and emptiest regions.
- Build a point quadtree with a capacity and a depth limit, and count the work of a query in it.
- Choose between a grid, a hashed grid, a quadtree and a bounding-volume tree for a stated game scenario, and defend the choice with numbers.

**Before class:** Millington, *Game Physics Engine Development* (2nd ed., 2010), chapter 12, sections on the collision detection pipeline, broad-phase detection and spatial partitioning. Nystrom, *Game Programming Patterns* (2014), "Spatial Partition" (free at gameprogrammingpatterns.com). Optional: Ericson, *Real-Time Collision Detection* (2005), chapter 7 sections 7.1 (uniform grids) and 7.3 (quadtrees and octrees).

**Prerequisites from earlier courses:** [CS102 week 4, Big-O intuition](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w04-big-o-intuition-for-game-developers.md), section 2 (the all-pairs check, the uniform grid with cell size equal to the radius, and its collapse when units cluster). This lecture starts where that worked example ends and does not repeat it. [CS102 week 7, trees](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w07-trees-scene-graphs-and-skill-trees.md) (recursion over a tree). [MA101 week 14, distances and ranges](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w14-distances-ranges-and-squared-distance.md) (squared-distance tests, the narrow phase you run on every candidate). [MA201 week 9, collision detection](w09-collision-detection-spheres-aabb-sat.md) (AABB overlap).

**Interactive:** [`examples/w11-cell-size-tradeoff.html`](../examples/w11-cell-size-tradeoff.html). Keep it open during section 2.

---

## 1. Broad phase, narrow phase, and what a query costs

A collision or proximity system runs in two stages. The **broad phase** finds candidate pairs cheaply and may include pairs that turn out to be apart. The **narrow phase** runs the exact test (circle distance, AABB overlap, SAT from week 9) on each candidate. A broad phase must never miss a pair that really overlaps. It is allowed to report extra ones, and every extra one costs a narrow-phase test.

In CS102 week 4 you counted that trade for one grid with cells as wide as the interaction radius. The numbers came from assuming units spread evenly, and the lecture closed by showing the grid falling back toward `n²/2` checks when everyone crowded into one corner. That leaves two questions open, and they are this week's subject.

1. The cell size was fixed at the radius. Is that the best choice, and what is the best choice when the radius and the crowd density differ across the map?
2. If different parts of the map want different cell sizes, can one structure give each region its own?

To answer them we need a cost we can count for a single **query**, "which entities are within `r` of the point `(x, y)`?" A grid answers it in two steps. It visits every cell that overlaps the query square from `(x − r, y − r)` to `(x + r, y + r)`, and it tests every entity stored in those cells. Both steps cost time. We will count one unit of work per cell visited and one per entity tested, so

```
work = cells visited + entities tested
```

Weighting the two equally is a modelling choice. In Python a dictionary lookup and a distance test cost roughly the same. In C++ with a flat array of cells, visiting a cell is cheaper. Lab 11 measures the real ratio on your machine and shows how it moves the answer.

## 2. Worked example: the capital city and the wilderness

### The hook

Minecraft cuts its world into chunks of 16 × 16 blocks, stacked in sections 16 blocks tall. In Java Edition that world reaches 30 million blocks from the center in each direction. The same 16-block grid covers a packed village, a mob farm, an empty ocean and a desert nobody will ever visit. One cell size, everywhere, and the game runs.

Now try it with an MMO map. You have a capital city where players stand shoulder to shoulder at the auction house, and a wilderness where monsters are spread thin. Players in the city constantly ask "who is right next to me?" for clicks, collision and melee. Monsters in the wilderness ask "is any player within my aggro radius?", a much larger circle. You pick one grid cell size, and one of the two groups pays for it. Which one, how much, and what can you do about it?

### The model

Take a query of radius `r` in a region where entities have density `ρ` (entities per square metre), on a grid of cell size `s`. On average, the query square of side `2r` overlaps `(2r/s + 1)²` cells. Those cells cover an area of about `(2r + s)²`, so they hold about `ρ (2r + s)²` entities. Add the two:

```
W(s) = (2r/s + 1)² + ρ (2r + s)²
     = (2r + s)² × (1/s² + ρ)
```

- `W` is the expected work per query, in units of "cell visits plus entity tests".
- `r` is the query radius. `s` is the cell size. `ρ` is the local density.

The first term falls as cells grow (fewer cells to visit). The second rises (bigger cells hold more strangers). Setting the derivative of `W` to zero and simplifying gives a clean optimum:

```
s* = (2r / ρ)^(1/3)
```

The best cell size grows with the query radius and shrinks with density, both through a **cube root**. That cube root is the whole story of this example. It means the best cell size moves slowly, so a grid is forgiving, until the region you care about spans a large range of density and radius at once.

### Numbers you can check

The test world is 1,024 m square. The capital is a 64 m square in the middle with 2,000 players, so `ρ = 2,000 / 64² = 0.488` per m². The wilderness keeps clear of the city and holds 2,000 monsters spread over the rest, `ρ = 0.00198` per m². Players query `r = 4` m. Monsters query an aggro radius of `r = 30` m.

The best cell sizes from the formula:

- city: `s* = (8 / 0.488)^(1/3) = 16.4^(1/3) = 2.5` m
- wilderness: `s* = (60 / 0.00198)^(1/3) = 30,300^(1/3) = 31.2` m

They are 12 times apart. Here is the model beside a measurement on the actual scatter of 4,000 entities, for grids of several cell sizes. Each row is the average work for one query.

| Cell size `s` | City, model | City, measured | Wilderness, model | Wilderness, measured |
|---|---|---|---|---|
| 2.5 m | 71 | 67 | 633 | 632 |
| 4 m | 79 | 73 | 264 | 264 |
| 8 m | 129 | 113 | 81 | 81 |
| 16 m | 284 | 237 | 34 | 34 |
| 32 m | 783 | 633 | 25 | 24 |

Check one row by hand. For the city at `s = 16`, `(8 + 16)² × (1/256 + 0.488) = 576 × 0.492 = 283.4`. The measured city values run a little under the model because players near the city wall have empty ground on one side, which the uniform-density model ignores. The wilderness matches to within one unit.

Read across the table. A cell size that suits the city costs the wilderness 26 times its best. A cell size that suits the wilderness costs the city 9 times its best. The least bad compromise is around 8 m, where the city pays 1.7 times its best and the wilderness 3.4 times. Nothing about the code is wrong. The two regions want different grids.

### A structure that adapts: the quadtree

A **quadtree** is a tree in which each node covers a square region. A node starts as a **leaf** holding a list of entities. When a leaf holds more than a **capacity** `k` entities, it splits into four child squares of half its size and hands its entities down. To stop the tree growing forever when many entities share a point, splitting also stops at a **maximum depth**.

The effect is that leaves size themselves to the local density. Where entities are dense, leaves keep splitting until each holds about `k` entities, so a leaf's area is about `k / ρ`. In the city with `k = 8` that is a leaf about 4 m across, close to the city's `s*`. In the wilderness it is about 64 m. Nobody chose those sizes. The data did.

A query walks down from the root and visits only nodes whose square overlaps the query square. Its work is nodes visited plus entities tested in the leaves reached, the same units as the grid. Here is all of it, grids and tree, on the same scene.

```python
import random

WORLD = 1024.0
R_TOWN, R_WILD = 4.0, 30.0             # player query in town, mob aggro in the wild

rng = random.Random(7)
town = [(rng.uniform(480, 544), rng.uniform(480, 544)) for _ in range(2000)]
wild = []
while len(wild) < 2000:                # wilderness keeps clear of the town
    x, y = rng.uniform(0, WORLD), rng.uniform(0, WORLD)
    if not (416 < x < 608 and 416 < y < 608):
        wild.append((x, y))
points = town + wild


class Grid:
    def __init__(self, pts, s):
        self.s, self.cells = s, {}
        for i, (x, y) in enumerate(pts):
            self.cells.setdefault((int(x // s), int(y // s)), []).append(i)

    def work(self, x, y, r):           # cells visited + entities tested
        s = self.s
        xs = range(int((x - r) // s), int((x + r) // s) + 1)
        ys = range(int((y - r) // s), int((y + r) // s) + 1)
        return len(xs) * len(ys) + sum(len(self.cells.get((i, j), ())) for i in xs for j in ys)


class QuadTree:
    CAPACITY, MAX_DEPTH = 8, 10

    def __init__(self, x, y, size, depth=0):
        self.x, self.y, self.size, self.depth = x, y, size, depth
        self.items, self.kids = [], None

    def child(self, px, py):
        h = self.size / 2
        return self.kids[(py >= self.y + h) * 2 + (px >= self.x + h)]

    def insert(self, px, py):
        if self.kids:
            return self.child(px, py).insert(px, py)
        self.items.append((px, py))
        if len(self.items) > self.CAPACITY and self.depth < self.MAX_DEPTH:
            h = self.size / 2
            self.kids = [QuadTree(self.x + dx * h, self.y + dy * h, h, self.depth + 1)
                         for dy in (0, 1) for dx in (0, 1)]
            for p in self.items:
                self.child(*p).insert(*p)
            self.items = []

    def work(self, x, y, r):           # nodes visited + entities tested
        if (x + r < self.x or x - r >= self.x + self.size or
                y + r < self.y or y - r >= self.y + self.size):
            return 0
        if not self.kids:
            return 1 + len(self.items)
        return 1 + sum(k.work(x, y, r) for k in self.kids)


def per_query(index, group, r):        # average work, not counting yourself
    return sum(index.work(x, y, r) - 1 for x, y in group) / len(group)


tree = QuadTree(0.0, 0.0, WORLD)
for p in points:
    tree.insert(*p)
indexes = [(f"grid s={s}", Grid(points, s)) for s in (2.5, 4, 8, 16, 32)]
for name, index in indexes + [("quadtree", tree)]:
    t, w = per_query(index, town, R_TOWN), per_query(index, wild, R_WILD)
    print(f"{name:9s} town {t:4.0f}  wild {w:4.0f}  frame {2000 * (t + w):9,.0f}")
```

It prints:

```
grid s=2.5 town   67  wild  632  frame 1,398,653
grid s=4  town   73  wild  264  frame   674,433
grid s=8  town  113  wild   81  frame   389,034
grid s=16 town  237  wild   34  frame   541,631
grid s=32 town  633  wild   24  frame 1,313,540
quadtree  town   85  wild   34  frame   237,186
```

The "frame" column is the total work when all 4,000 entities query once. The ideal, if each region had its own perfect grid, is `2,000 × (67 + 24) = 182,000`. The best single grid (8 m) does 2.1 times that. The quadtree does 1.3 times that, without being told where the city is. Its city queries cost a little more than the city's best grid, 85 against 67, because every query walks about eight levels down from the root before it reaches a leaf. That descent is the price of adapting.

### A visual you can move

Open [`examples/w11-cell-size-tradeoff.html`](../examples/w11-cell-size-tradeoff.html). The left view is the map from above, with the city's dense dots in the middle, the wilderness dots scattered around it, and one grid drawn over everything. Click any entity to see its query square and the cells it visits, shaded, with the tested entities highlighted. The right view plots `W(s)` for the city and for the wilderness on log axes, with a dot at the current cell size on each curve and a vertical line at each `s*`.

Drag the cell-size slider. Watch the two dots slide along their curves in opposite directions. When one reaches its valley, the other climbs a wall. That is the insight the page exists to show. Then toggle "quadtree". The grid lines on the map are replaced by the tree's leaves, small squares in the city and large ones outside, and the two dots on the right jump to nearly the bottom of both valleys at once.

### Cross-game recognition

**Minecraft (Java Edition, current versions).** The chunk is a uniform grid with `s = 16`, and it is stored as a **hashed grid**. A world 60 million blocks wide holds `(60,000,000 / 16)² ≈ 1.4 × 10¹³` chunk positions, so no array could hold them. The game keeps only the chunks near players loaded. In this lecture's terms that is a hashed grid, the dictionary-of-cells trick from the code above, where only occupied cells cost memory. Minecraft can use one cell size because its chunk has one main job, loading and saving terrain, where density does not vary much. Our MMO grid had two jobs with a 12× gap between their best sizes.

**Box2D (v2.4.1).** Box2D's broad phase is not a grid. It is a **dynamic AABB tree**, a binary tree whose leaves are the bounding boxes of shapes and whose inner nodes are boxes around their children. Like the quadtree it adapts to where things are, but it splits by objects rather than by space, so it never creates empty regions. It also stores each box enlarged by 0.1 m (`b2_aabbExtension`), so a shape can move a little without the tree being updated. Section 4 comes back to that idea.

**NVIDIA PhysX (5.4.1).** PhysX offers a choice of broad phases, and its documentation reads like this lecture's trade-offs. Sweep-and-prune is a good general choice when many objects are asleep and degrades when everything moves. Multi box pruning divides the world into regions the user must define, a coarse grid, and does not suffer from that. Automatic box pruning manages the regions itself, and the documentation recommends it as the default.

Three engines, three answers to the same problem. A fixed grid when density is predictable, a tree that adapts when it is not, and a menu when the engine can't know which game it is in.

### Eyes-open design judgment

- **Start with a grid, size it for the densest place that matters.** The table is lopsided. Cells too large for the city cost up to 9 times, and cells too small for the wilderness cost up to 26 times, but the city has more queries per second in most games. If one region dominates, `s*` for that region is often the answer, and a grid is simpler to build, debug and update than any tree.
- **Reach for a tree when the density spread is large or unknown.** The quantity to compute is the ratio of `s*` values across your world. Under about 2, any sensible grid is within a few tens of percent of ideal. At 12, as here, a single grid loses a factor of 2 or more.
- **Two grids can beat one tree.** If exactly two query types differ, as players and monsters do here, keep two grids with two cell sizes. Each costs memory and an update on every move, but each query then runs at its own optimum.
- **Density is a design decision.** The city's density came from the level designer putting the auction house in one building. Spreading services across the city lowers `ρ` and every query's cost. A physics programmer and a level designer should look at this table together.

## 3. Things that have size

The worked example used points. Real shapes have extent. A 3 m ogre may overlap four cells or straddle a quadtree boundary. Three standard answers, each with a cost.

**Insert into every cell it overlaps.** Queries stay simple, but a large object appears in many cells, a pair can be found twice (deduplicate with a set or a pair ID), and moving costs more because more cell lists change. For a grid this is the usual choice when objects are smaller than a cell.

**Store in the smallest node that contains it.** In a quadtree, an object that straddles a split line stays in the parent node instead of going down. It is simple and never duplicates, but objects that happen to sit on the big central split lines end up near the root, and every query tests them. A pebble lying on the world's middle line is tested by every query in the world.

**Loose cells.** Store each object by its center only, and make each cell or node "loose", meaning its region for querying is enlarged by the largest object radius (a loose quadtree typically doubles each node's size, as Ulrich described in *Game Programming Gems*, 2000). An object then belongs to exactly one place, and the query grows by the maximum radius. Box2D's fattened boxes are the same idea applied to motion instead of size.

## 4. Things that move

Every structure above must be updated as entities move. Three strategies.

- **Rebuild every frame.** Throw the structure away and insert everything again. For a hashed grid that is `n` dictionary inserts, which is often the fastest option, and it has no bookkeeping bugs. For a quadtree each insert walks the tree, so rebuilding costs `n × depth`.
- **Update on cell change.** Compute each entity's new cell after it moves. Only if it changed, remove it from the old list and add it to the new one. Most frames most entities stay in their cell. For a quadtree a move can also trigger a merge (four siblings now hold few enough to become one leaf) or a split, so updates are more code.
- **Update only past a margin.** Store an enlarged box and update the structure only when the object leaves it, as Box2D does. Entities that jitter at a cell border no longer hop back and forth every frame.

The move rate matters as much as the query rate. A server with 2,000 monsters wandering slowly and 2,000 players querying constantly wants cheap queries. A bullet-hell game with 5,000 bullets that each move far every frame and query once wants cheap inserts, and a rebuilt hashed grid is hard to beat.

## 5. Choosing a structure

| Situation | Start with | Why |
|---|---|---|
| Similar-size objects, density varies less than about 8× (cell ratio under 2) | Uniform grid, `s = s*` for the busiest region | Simplest, cheapest updates, near ideal |
| Unbounded or huge world, sparse occupancy | Hashed grid | Only occupied cells cost memory |
| Density varies a lot, or crowds move unpredictably (world bosses, sieges) | Quadtree (octree in 3D), or a dynamic AABB tree | Leaf size follows the crowd |
| Many query types with very different radii | One grid per query type, or a tree | Each radius has its own `s*` |
| Objects range from pebbles to castles | AABB tree, or loose grid/quadtree | Size is handled without duplicates |
| Mostly static world geometry | Tree built once, offline | Build cost does not matter |

Whatever you choose, keep the narrow phase exact and count work before and after. The structure only changes how many candidates reach the narrow phase, never which pairs are really touching.

Next week's raycasts use the same structures. A ray against a grid walks the cells it crosses, one at a time, and a ray against a tree skips every node its line misses. The grid walk is next week's worked example.

## In-class activity (25 minutes)

In groups of three, you are handed a zone plan for a new MMO region, a 2 km × 2 km map with three areas: a trade hub (1,500 players in a 100 m square), a quest valley (600 monsters and 300 players in a 500 m square), and open wilds (400 monsters over the rest). Players query 5 m, monsters 25 m.

1. Compute `ρ` and `s*` for each area and each query type that happens there. (8 min)
2. Decide between one grid, two grids and a quadtree. Use `W(s)` to estimate the work per query for your choice in each area, and the total per frame. (10 min)
3. The live team announces a world boss in the open wilds that draws 1,000 players into a 60 m circle. Recompute for your choice. Does it survive, and if not, what would you change? (7 min)

Expected output: a table of `ρ`, `s*` and `W` per area, your choice in one sentence, and the world-boss number.

## Common misconceptions

- **"Smaller cells are always more precise, so they're always better."** Precision is not the goal. Smaller cells mean more cells to visit, and for a large query radius that term dominates. The best size is `(2r/ρ)^(1/3)`, not "as small as possible".
- **"Cell size should equal the query radius."** That is a good first guess and often within a factor of 2. In our wilderness `s* ≈ r`, but in the city `s*` is well under `r` because the density is so high.
- **"A quadtree is always faster than a grid."** Here it lost to the best city grid, 85 against 67, because of the descent from the root, and it costs more to update. It wins when one grid cannot fit the whole world.
- **"Partitioning fixes crowds."** It removes pairs that are far apart. In a true crowd, where everyone is within range of everyone, the answer itself has `n²/2` pairs, as CS102 week 4 showed. No structure can report them without touching them.

## Check yourself

1. A shooter's players query `r = 10` m at a density of 0.02 per m². What cell size minimizes `W`, and what is `W` there?
2. A designer doubles the city's population to 4,000 in the same 64 m square. By what factor does the city's `s*` change? Compute the new `W` at `s = 2.5` and at the new `s*`.
3. A world has two regions whose `s*` values are 6 m and 7.5 m. Should you build a quadtree? Justify with one number.
4. In a quadtree with capacity 8, about how wide is a leaf in a region with 0.05 entities per m²?

<details>
<summary>Answers</summary>

1. `s* = (20 / 0.02)^(1/3) = 1,000^(1/3) = 10` m. `W = (20 + 10)² × (1/100 + 0.02) = 900 × 0.03 = 27`.
2. `ρ` doubles to 0.977, so `s*` shrinks by `2^(1/3) = 1.26`, from 2.54 m to 2.01 m. At `s = 2.5`: `(10.5)² × (0.16 + 0.977) = 110.25 × 1.137 = 125.3`. At `s = 2.01`: `(10.01)² × (0.2475 + 0.977) = 100.2 × 1.2245 = 122.7`. The old cell size is within about 2% of the new best, which is the cube root's forgiveness at work.
3. The ratio is 1.25. Using `s = 7` for both, each region pays `W(7)` against its own best, a few percent at most (try it for any `r` and `ρ` pair that gives those `s*`). One grid is fine, and the tree's descent cost would likely make things worse.
4. Leaf area `≈ k / ρ = 8 / 0.05 = 160` m², so about `√160 ≈ 12.6` m across. The tree only makes power-of-two sizes, so in practice leaves are the nearest split level, 16 m or 8 m for a 1,024 m root.

</details>

## Lab / assignment hook

[Lab 11, grids, quadtrees and a world boss](../labs/lab11.md). You extend this lecture's grid and quadtree to return exact neighbors, handle moving entities, and measure time as well as work. Then you pick a structure for a zone whose crowd moves to a world boss halfway through a recorded session, and defend it with numbers.

## Sources

- Minecraft Wiki, "Chunk" (Java Edition, accessed September 2026). Chunks are 16 × 16 blocks divided into 16-block-tall sections; Java Edition worlds extend 30 million blocks in each cardinal direction; only chunks near players are loaded.
- Catto, E. Box2D v2.4.1 (GitHub `erincatto/box2d`, tag `v2.4.1`). `README.md` (dynamic tree broad phase); `b2_dynamic_tree.h` (binary tree of enlarged AABBs, used for volume queries and ray casts); `b2_common.h` (`b2_aabbExtension` 0.1 m).
- NVIDIA. PhysX 5.4.1 SDK documentation, "Rigid Body Collision", broad-phase algorithms (SAP, MBP, ABP, PABP, GPU) and their stated strengths.
- Nystrom, R. (2014). *Game Programming Patterns*, "Spatial Partition". Genever Benning.
- Ericson, C. (2005). *Real-Time Collision Detection*. Morgan Kaufmann. Chapter 7.
- Ulrich, T. (2000). "Loose Octrees." In M. DeLoura (ed.), *Game Programming Gems*. Charles River Media.
- Millington, I. (2010). *Game Physics Engine Development*, 2nd ed. Morgan Kaufmann. Chapter 12.

## Interactive spec: examples/w11-cell-size-tradeoff.html

**The one insight:** the best grid cell size depends on density and query radius, `s* = (2r/ρ)^(1/3)`. A busy city and a sparse wilderness have best sizes 12× apart, so dragging one cell size always pushes one region up its cost wall. A quadtree sits near both minima at once.

**Layout.** Two linked views, side by side at 1280 px, stacked at 390 px (map on top).

- **Left, "Map":** the 1,024 m square world drawn to fit, with a zoom toggle "whole world / city close-up" (close-up shows x and y from 448 to 576). 2,000 city dots uniform in [480, 544]², 2,000 wilderness dots uniform over the world excluding (416, 608)². Generate with mulberry32, seed 11, city first, then wilderness by rejection. Grid lines drawn at the current cell size (in close-up only when `s ≥ 2`; in whole-world view only when `s ≥ 8`, else a note "grid too fine to draw"). Clicking or pressing Enter on a focused dot selects it: draw its query square (half-width 4 m for city dots, 30 m for wilderness dots), shade visited cells, and highlight tested entities. A readout shows "cells visited", "entities tested", "work".
- **Right, "Cost":** log-log plot of `W(s)` against `s` from 1 m to 128 m, two curves: city (`r = 4`, `ρ = 0.488`) and wilderness (`r = 30`, `ρ = 0.00198`). A dot on each curve at the current `s`. Vertical dashed lines at `s* = 2.5` and `31.2`, labelled. Below the plot, a four-row table: city model, city measured (average over all 2,000 city dots), wilderness model, wilderness measured, and a "frame total" = 2,000 × (city measured + wilderness measured), plus "ideal 182,000" and the ratio.

**Controls (labelled, keyboard accessible):**

1. Cell size `s` slider, logarithmic from 1 to 128 m, with snap points at 2.5, 4, 8, 16, 32. Default 8.
2. Index toggle: "Grid" (default) / "Quadtree (capacity 8, max depth 10)". In quadtree mode, draw leaf squares instead of grid lines, and the two plot dots move to the measured quadtree values at a fixed x position labelled "quadtree" (they are not a function of `s`).
3. Query radius sliders: city `r` 1 to 10 m (default 4), wilderness `r` 5 to 60 m (default 30). Changing them updates the curves, `s*` and the measurements.
4. Zoom toggle.

**Formulas.** `W(s) = (2r + s)² × (1/s² + ρ)`, `s* = (2r/ρ)^(1/3)`. Grid measured work for a query at `(x, y)`: cells `= (⌊(x+r)/s⌋ − ⌊(x−r)/s⌋ + 1) × (same in y)`, plus the count of all entities in those cells, minus 1 (the querier). Quadtree: root covers [0, 1024)², leaf splits when it holds more than 8 points and depth < 10, child index `(py ≥ mid_y) × 2 + (px ≥ mid_x)`; query work = nodes whose square overlaps the query square (overlap test `x + r < node.x` or `x − r ≥ node.x + size` rejects, same in y) plus points in overlapped leaves, minus 1.

**Test values (model, must match exactly).** City: `W(2.5) = 71.5`, `W(4) = 79.3`, `W(8) = 129.0`, `W(16) = 283.5`, `W(32) = 782.8`; `s* = 2.54`. Wilderness: `W(2.5) = 632.7`, `W(4) = 264.1`, `W(8) = 81.4`, `W(16) = 34.0`, `W(32) = 25.0`; `s* = 31.2`. Check yourself 1: `r = 10`, `ρ = 0.02` gives `s* = 10`, `W = 27`. Measured values will differ slightly from the lecture's Python table (different random generator) but must land within 10% of: city 67, 73, 113, 237, 633; wilderness 632, 264, 81, 34, 24; quadtree city 85, wilderness 34.

**First screen.** Whole-world view, grid at 8 m, a city dot and a wilderness dot pre-selected with their query squares, both cost dots visible partway up their curves. Caption: "One cell size, two regions. Drag it and watch one of them climb a wall."

**Accessibility.** All controls reachable by Tab with visible focus; dots can be cycled with arrow keys when the map has focus. A live region reads the four-row table when it changes. Respects `prefers-reduced-motion` (no animated transitions) and `prefers-color-scheme` via `templates/interactive-tokens.css`. Plain dots and lines only.
