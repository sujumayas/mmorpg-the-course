# CS203 · Week 05 — Navigation meshes

**Why this matters:** A grid chops a level into hundreds of squares that mean nothing to a designer, and A* over those squares returns staircase paths that look robotic. Most 3D games since the mid-2000s describe walkable space as a handful of convex polygons instead, search those, and then pull the path tight around corners. If you use Unity, Unreal or Godot, you are already using this method, and the bugs you will meet (NPCs scraping walls, taking the long door, walking into a gap they can't fit) come from its details.

**You will be able to:**
- Explain why navigation mesh polygons must be convex, and test whether a point lies inside a convex polygon with 2D cross products.
- Build the polygon graph of a small level, list its portals with correct left and right endpoints, and compute the midpoint path through them.
- Trace the funnel (string-pulling) algorithm by hand and compute the length of the resulting path.
- Critique a navmesh path for agent radius, door choice and polygon layout, and predict when A* over polygons picks the wrong route.

**Before class:** Sturtevant, N. R., "Choosing a Search Space Representation", *Game AI Pro* (2013), chapter 18 (6 pages, free at gameaipro.com). Mononen, M., "Simple Stupid Funnel Algorithm", *Digesting Duck* blog, 8 March 2010. Millington, *AI for Games* (3rd ed., 2019), chapter 4, the section on world representations.

**Prerequisites from earlier courses:** [CS203 week 4, A* and heuristics](w04-a-star-and-heuristics.md) (A* is the search we run over polygons). [MA101 week 13, dot product and facing](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w13-dot-product-facing-and-vision-cones.md), section on left and right, where you met the 2D cross product as the "perp dot". [MA101 week 12, 2D vectors](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w12-2d-vectors.md). [CS102 week 8, graphs](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w08-graphs-maps-and-dialogue.md) (adjacency lists).

**Interactive:** [`examples/w05-navmesh-funnel.html`](../examples/w05-navmesh-funnel.html). Keep it open during section 2.

---

## 1. Three ways to describe where a character can walk

Pathfinding needs a graph. The level is not a graph, so you choose how to turn walkable space into one. That choice is the **search space representation**, and Sturtevant's chapter lists three common ones.

- **Grid.** Cover the floor with equal squares (or hexes) and make each walkable cell a node. Easy to build and edit, and it is what last week's lab used. The costs: the node count grows with area, not with complexity, so an empty 100 m hall at 0.5 m cells is 40,000 nodes. Paths move in 8 directions at most, so a diagonal line across a room comes out as a staircase.
- **Waypoint graph.** A designer (or a tool) places points by hand and links the ones with a clear line between them. Few nodes and quick to search. But the graph says nothing about the space *between* waypoints. A character that is pushed off its line has no idea whether the floor next to it is walkable.
- **Navigation mesh (navmesh).** Cover the walkable floor with convex polygons that share edges. Each polygon is a node, each shared edge is a link. The polygons describe the whole walkable area, not a few sample points.

In a 2008 essay, "Fixing Pathfinding Once and For All", the AI developer Paul Tozour argued that waypoint graphs cause zig-zagging paths, scale poorly to large open areas, and need a separate graph for every size of character. He listed Halo 2, Halo 3, F.E.A.R., Counter-Strike: Source, the Metroid Prime series and the Jak series as games that used navmeshes. The engines you will use in later courses build one for you, as section 4 shows.

### Why convex

A polygon is **convex** if the straight segment between any two points inside it stays inside it. A rectangle is convex. An L-shape is not: a line between the ends of the L cuts across the corner.

That one property is the whole reason navmeshes work. If a character stands anywhere in a convex polygon, it can walk in a straight line to any other point of the same polygon with no further search. So the search only has to decide *which polygons* to cross. Inside each one, straight lines are free.

To test whether a point `p` lies inside a convex polygon whose vertices are listed counter-clockwise, walk the edges. For each edge from `a` to `b`, compute the 2D cross product

```
cross(a, b, p) = (b.x − a.x) × (p.y − a.y) − (b.y − a.y) × (p.x − a.x)
```

It is positive when `p` is to the left of the direction `a → b`, negative when to the right and zero when on the line. You met the same quantity in MA101 week 13 as the left-or-right test for a guard. For a counter-clockwise polygon the inside is on the left of every edge, so `p` is inside (or on the boundary) when every cross product is `≥ 0`. One negative value means outside.

## 2. Worked example: the path that hugs the corner

### The hook

Watch an NPC in an older game walk through a series of doors. Many of them walk to the center of each doorway and turn there, even when the next doorway is off to one side. Tozour's essay calls out this kind of rigid, zig-zag route as the signature of waypoint graphs. Players read it as "robot walking". A person would cut the corner, passing close to the door frame on the inside of the turn.

The navmesh makes the better path possible, because it records that the whole doorway is walkable, not just its center. An algorithm still has to find that path. This section builds it.

### The level

The level is five convex polygons (all rectangles here, to keep the numbers easy), with coordinates in meters:

| Polygon | Corners (x, y) | Area (m²) |
|---|---|---|
| Room A | (0, 0) to (4, 4) | 16 |
| Corridor | (4, 1) to (10, 3) | 12 |
| Room B | (10, 0) to (14, 8) | 32 |
| Door | (10, 8) to (12, 9) | 2 |
| North room | (8, 9) to (14, 13) | 24 |

Neighboring polygons touch along a shared segment called a **portal**. There are four portals: `x = 4` for `1 ≤ y ≤ 3` (Room A to corridor), `x = 10` for `1 ≤ y ≤ 3` (corridor to Room B), `y = 8` for `10 ≤ x ≤ 12` (Room B to door) and `y = 9` for `10 ≤ x ≤ 12` (door to north room).

A character stands at `start = (1, 1)` in Room A and wants to reach `goal = (13, 11)` in the north room.

### The model

Pathfinding on a navmesh has two stages.

**Stage 1: the corridor.** Find which polygons to cross. Build a graph with one node per polygon and one edge per portal, and run A* from the start's polygon to the goal's polygon, exactly as in week 4. The result is a list of polygons, called the **corridor**. Here it is Room A → corridor → Room B → door → north room, and it gives us the four portals in order.

**Stage 2: the straight path.** Find the shortest line through those portals. Each portal is a segment with two endpoints. Name them from the walker's point of view: facing the direction of travel, `left` is the endpoint on your left and `right` the one on your right. For the first portal the walker faces east, so `left = (4, 3)` and `right = (4, 1)`.

The naive answer walks through the midpoint of every portal. The better answer is the **funnel algorithm**, also called string pulling, in the form Mikko Mononen published in 2010 as the "simple stupid funnel algorithm":

1. Put the **apex** at the start. The funnel is two rays from the apex, one through a left point and one through a right point. At the start both rays point at the apex itself.
2. For each portal in order, try to narrow the funnel:
   - If the portal's right point is inside the funnel (not to the right of the current right ray), move the right ray to it. But if it lies past the left ray, the funnel has collapsed: the current left point is a corner the path must turn around. Add it to the path, make it the new apex, and restart the scan from the portal after the one that point came from.
   - Do the same for the portal's left point, with left and right swapped.
3. Treat the goal as a final portal whose left and right points are both the goal. When you reach it, add the goal.

"Inside the funnel" and "past the other ray" are both 2D cross product signs, the same test as the convex-polygon check. That is the whole algorithm: no queue, no search, one pass with occasional restarts.

### The code

```python
import math

def cross(o, a, b):
    """2D cross product of (a - o) and (b - o). Positive: b is left of o->a."""
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def funnel(start, goal, portals):
    """Simple stupid funnel algorithm. portals = [(left, right), ...]."""
    portals = portals + [(goal, goal)]
    path = [start]
    apex = left = right = start
    apex_i = left_i = right_i = -1
    i = 0
    while i < len(portals):
        new_l, new_r = portals[i]
        # tighten the right edge if the new right point is inside the funnel
        if cross(apex, right, new_r) >= 0:
            if apex == right or cross(apex, left, new_r) < 0:
                right, right_i = new_r, i
            else:  # right crossed over left: left corner is a waypoint
                path.append(left)
                apex = right = left
                apex_i = right_i = left_i
                i = apex_i + 1
                continue
        # tighten the left edge if the new left point is inside the funnel
        if cross(apex, left, new_l) <= 0:
            if apex == left or cross(apex, right, new_l) > 0:
                left, left_i = new_l, i
            else:  # left crossed over right: right corner is a waypoint
                path.append(right)
                apex = left = right
                apex_i = left_i = right_i
                i = apex_i + 1
                continue
        i += 1
    if path[-1] != goal:
        path.append(goal)
    return path

def length(points):
    return sum(math.dist(a, b) for a, b in zip(points, points[1:]))

start, goal = (1, 1), (13, 11)
# the four doorways crossed on the way, as (left, right) seen by the walker
portals = [((4, 3), (4, 1)),     # room A -> corridor
           ((10, 3), (10, 1)),   # corridor -> room B
           ((10, 8), (12, 8)),   # room B -> door
           ((10, 9), (12, 9))]   # door -> north room

mid = [start] + [((l[0] + r[0]) / 2, (l[1] + r[1]) / 2) for l, r in portals] + [goal]
pulled = funnel(start, goal, portals)
print("midpoint path:", mid)
print(f"  length {length(mid):.2f} m, {len(mid) - 2} turns")
print("funnel path:  ", pulled)
print(f"  length {length(pulled):.2f} m, {len(pulled) - 2} turns")
```

Output:

```
midpoint path: [(1, 1), (4.0, 2.0), (10.0, 2.0), (11.0, 8.0), (11.0, 9.0), (13, 11)]
  length 19.07 m, 4 turns
funnel path:   [(1, 1), (10, 3), (12, 9), (13, 11)]
  length 17.78 m, 2 turns
```

### Numbers you can check

Segment by segment:

| Path | Segment | Length (m) |
|---|---|---|
| Midpoints | (1, 1) → (4, 2) | √10 = 3.16 |
| | (4, 2) → (10, 2) | 6.00 |
| | (10, 2) → (11, 8) | √37 = 6.08 |
| | (11, 8) → (11, 9) | 1.00 |
| | (11, 9) → (13, 11) | √8 = 2.83 |
| | **Total** | **19.07** |
| Funnel | (1, 1) → (10, 3) | √85 = 9.22 |
| | (10, 3) → (12, 9) | √40 = 6.32 |
| | (12, 9) → (13, 11) | √5 = 2.24 |
| | **Total** | **17.78** |

The midpoint path is 7% longer and turns four times. The funnel path turns twice, at two real corners.

Check that the funnel path is legal. The first leg, from (1, 1) to (10, 3), rises 2 m over 9 m. At `x = 4` it is at `y = 1 + 2 × 3/9 = 1.67`, inside the first portal's range 1 to 3. At `x = 10` it is exactly at `y = 3`, the top corner of the corridor's exit. That is why (10, 3) is a waypoint: the path grazes the corridor's upper wall where it ends. The second leg, from (10, 3) to (12, 9), crosses `y = 8` at `x = 10 + 2 × 5/6 = 11.67` and `y = 9` at `x = 12`, both inside the door. Could the path skip (12, 9) and go straight from (10, 3) to the goal? That line crosses `y = 9` at `x = 10 + 3 × 6/8 = 12.25`, which is past the door's east jamb at 12. So no. The path must bend around the jamb at (12, 9).

For scale, cover the same 86 m² with 0.5 m grid cells and you get 344 nodes. One run of 8-way A* with octile distance on that grid (the lab 4 code, from the cell centered at (1.25, 1.25) to the cell centered at (13.25, 11.25), the same displacement as our start and goal) expanded 142 cells and returned a staircase path of 19.36 m with 5 changes of direction. The navmesh search has 5 nodes and 4 edges. Its corridor is found almost instantly, and the funnel turns it into a shorter path than the grid could represent at all.

### The visual

Open [`w05-navmesh-funnel.html`](../examples/w05-navmesh-funnel.html). The default view shows this level, both paths, and their lengths. Drag the start and goal points. The midpoint path always kinks at every portal. The funnel path only bends at corners, and each bend sits exactly on a portal endpoint. Press "step" to watch the funnel: the apex, the left ray and the right ray are drawn, and each step shows one portal narrowing the funnel or collapsing it onto a corner. Then widen the door with the slider. When the door spans `10 ≤ x ≤ 13`, the direct line from (10, 3) to the goal fits (it crosses `y = 9` at 12.25), the (12, 9) corner disappears, and the path drops to 2 segments.

### Cross-game recognition

**Recast and Detour (Unity, Unreal Engine, Godot, O3DE).** Recast, originally by Mikko Mononen and now maintained as the open-source recastnavigation project, builds navmeshes from level geometry. Its README says it powers AI navigation in Unity, Unreal, Godot and O3DE. Its runtime half, Detour, splits pathfinding into exactly our two stages. `findPath` runs A* over polygons and returns a polygon corridor. `findStraightPath` takes that corridor and, as its source comments put it, performs "string pulling". Detour's A* places each polygon's search node at the midpoint of the portal it was entered through and uses straight-line distance to the goal, scaled by 0.999, as `h`. That is week 4's model with the midpoints of this week as the nodes.

**Halo 2, F.E.A.R., Counter-Strike: Source and others (mid-2000s).** Tozour's 2008 list shows that navmeshes were already standard in shipped 3D action games before engines packaged them. The design pressure was the same as in our level: rooms, doors and corridors where people expect characters to cut corners.

**Grid games, one level up.** Factorio's biter pathfinding from last week groups each 32 × 32 chunk into a few connected patches and searches those first. That is the corridor idea on a grid. First find which regions to cross with a small search, then do the detailed work only inside them. Navmeshes, abstract grid graphs and Detour's tiled meshes all make the same trade. Search a small graph of regions, then fix up the path locally.

### Eyes-open design judgment

- **Corners are touched exactly.** The funnel path passes through (10, 3), a wall corner. A character with a 0.4 m radius following it would scrape the wall. Recast solves this before the mesh exists: its `walkableRadius` setting erodes the walkable area away from walls by the agent's radius, so every polygon vertex already sits one radius from a wall. The cost is one mesh per agent size. A giant and a goblin need different meshes, or the giant gets stuck in doors the goblin fits through.
- **A* over polygons is approximate.** The corridor is chosen using distances between portal midpoints, then smoothed. The smoothed path is shortest *within that corridor*, not necessarily in the level. Section 3 shows a case where this picks the wrong door.
- **Polygon layout changes behavior.** The same floor can be cut into polygons many ways. Long thin triangles give distorted midpoint distances. Recast limits polygon size and vertex count (`maxVertsPerPoly`, `maxEdgeLen`) for this reason. When a character takes a strange route, draw the navmesh before blaming the AI.
- **Not everything is floor.** Jumps, ladders and doors that open need extra links that are not shared edges (Detour calls them off-mesh connections). Moving obstacles need either local avoidance (week 2's steering) or rebuilding parts of the mesh at runtime, which is why Recast supports tiles.

## 3. When the corridor is wrong

A* over polygons needs a cost for each edge in the polygon graph. The common choice, Detour's included, measures distances between portal midpoints. That hides the width of each portal. A wide door's midpoint can be far from the line you would actually walk.

Take a wall along `x = 5` between a start at (0, 0) and a goal at (10, 0), with two gaps. Door A is wide, from `y = 1` to `y = 9`. Door B is narrow, from `y = −3` to `y = −2`.

| Door | Midpoint | Midpoint path cost | Best path through the door | True cost |
|---|---|---|---|---|
| A (wide) | (5, 5) | 2 × √50 = 14.14 | via (5, 1) | 2 × √26 = 10.20 |
| B (narrow) | (5, −2.5) | 2 × √31.25 = 11.18 | via (5, −2) | 2 × √29 = 10.77 |

Measured by midpoints, door B looks 3 m cheaper, so A* picks it. After string pulling, the path through door B is 10.77 m, while the path through door A would have been 10.20 m. The character takes a route about 6% longer and, worse, walks past an open door to use a narrow one. Players notice that.

Fixes, each with a cost:

- Measure edge costs to the nearest point of each portal instead of its midpoint. More accurate, a little more work per edge, and still not exact because the nearest point depends on where you came from.
- Split wide portals by cutting large polygons into smaller ones. More nodes, same algorithm.
- Run the funnel on the two or three best corridors and keep the shortest. Correct for small cases, more expensive in general.
- Accept it. A few percent is often invisible. Being deliberate about that choice is what matters, and knowing where it shows up (wide doorways next to narrow ones) tells your level designers what to avoid.

## 4. Where navmeshes come from

You will rarely draw a navmesh by hand. Recast's pipeline, as its README describes it, has four steps:

1. **Voxelize.** Rasterize the level's triangles into a 3D grid of small boxes (voxels).
2. **Filter.** Remove voxels an agent cannot stand on: slopes steeper than `walkableSlopeAngle`, ceilings lower than `walkableHeight`, ledges taller than `walkableClimb`, and everything within `walkableRadius` of a wall.
3. **Regions.** Group the remaining walkable voxels into connected regions.
4. **Polygons.** Trace the outline of each region, simplify it, and cut it into convex polygons.

Every parameter in step 2 is a design decision about your characters. `walkableClimb` decides whether a character steps onto a crate or has to jump. `walkableSlopeAngle` decides whether a hillside is a path or a wall. If a designer complains that an NPC won't climb stairs the player can climb, compare these numbers with the player controller's before touching AI code.

Godot, Unity and Unreal wrap this pipeline in a "bake" button and draw the result as a colored overlay. Turn that overlay on whenever you debug navigation.

## In-class activity (25 minutes)

Work in groups of three with graph paper, a ruler and the interactive.

1. Draw an L-shaped room: an 8 × 2 m horizontal bar from (0, 0) to (8, 2), with a 2 × 6 m vertical bar from (6, 2) to (8, 8) on its right end.
2. Split it into convex polygons in two different ways: one with the fewest polygons you can, and one with at least four.
3. For each split, list the portals with left and right endpoints for a walker going from (1, 1) to (7, 7).
4. Compute the midpoint path length for each split, and the funnel path length (it should be the same for both splits, so check that it is).
5. Report which split gave the worse midpoint path, and by how much. Then explain in two sentences what this means for A*'s choice of corridor in a level with two routes.

Expected output: two drawings with portals labeled, two midpoint lengths, one funnel length (the bend should be at the inner corner (6, 2)), and the two-sentence explanation.

## Common misconceptions

- **"The navmesh is the path."** The navmesh is the map. The path comes from A* over the polygons plus the funnel inside the corridor.
- **"Any polygon will do."** Only convex polygons let a character walk straight between any two points inside them. With a concave polygon, a straight line inside one node can leave the walkable area.
- **"The funnel algorithm finds the shortest path in the level."** It finds the shortest path through the corridor it is given. If A* chose the wrong corridor (section 3), the funnel faithfully smooths the wrong route.
- **"String pulling makes characters avoid walls."** It does the opposite. It pulls the path tight against every corner. Clearance comes from eroding the mesh by the agent radius before the search.

## Check yourself

1. Is the point (3, 2) inside the triangle with counter-clockwise vertices (0, 0), (4, 0), (0, 4)? Show the three cross products.
2. In the worked example, move the goal to (9, 12). Which portal endpoints become corners of the funnel path, and what is its length? (Hint: the path now bends around the door's west jamb.)
3. Suppose the characters in the worked example have radius 0.5 m and the mesh is eroded by that radius. The corridor becomes `1.5 ≤ y ≤ 2.5` and the door `10.5 ≤ x ≤ 11.5`. Does the funnel path still bend at the corridor's exit? Give the new corner.
4. In the two-door example of section 3, how wide would door B have to be (extending downward from `y = −2`) for midpoint costs to prefer door A?

<details>
<summary>Answers</summary>

1. Edge (0,0)→(4,0): `4 × 2 − 0 × 3 = 8`. Edge (4,0)→(0,4): `(−4) × (2 − 0) − 4 × (3 − 4) = −8 + 4 = −4`. Edge (0,4)→(0,0): `0 × (2 − 4) − (−4) × (3 − 0) = 12`. One is negative, so the point is outside. Check: `x + y = 5 > 4`, beyond the hypotenuse.
2. Run `funnel((1, 1), (9, 12), portals)`. It returns `[(1, 1), (10, 3), (10, 9), (9, 12)]`. From (10, 3) the goal is up and to the left, so the path hugs the west side of the door and turns at its top-left corner (10, 9). Length `√85 + 6 + √10 = 9.22 + 6.00 + 3.16 = 18.38` m.
3. Yes. The portals become `((4, 2.5), (4, 1.5))`, `((10, 2.5), (10, 1.5))`, `((10.5, 8), (11.5, 8))` and `((10.5, 9), (11.5, 9))`. The funnel returns `[(1, 1), (4, 1.5), (10, 2.5), (11.5, 9), (13, 11)]`, 18.29 m. The corridor exit corner moves to (10, 2.5) and the door jamb to (11.5, 9). There is also a new bend at (4, 1.5): the start at `y = 1` is now below the eroded corridor floor, so the path must step up into it. Every corner moved away from the walls by the radius, which is the point of erosion, and the path got 0.5 m longer.
4. Door B's midpoint cost is `2 × √(25 + m²)` where `m` is the distance of its midpoint below the x-axis. Door A costs 14.14 by midpoints, so `25 + m² > 50`, `m > 5`. The midpoint must be below `y = −5`, so door B must run from `y = −2` to below `y = −8`: at least 6 m wide. Wider doors look *worse* to midpoint costs, which is the bug.

</details>

## Lab / assignment hook

[Lab 05, a navmesh by hand](../labs/lab05.md). You implement point location in convex polygons, find portals between polygons, orient them left and right, and write the funnel algorithm, then check that every path you produce stays on the mesh. The checks in `check_lab05.py` fail on the starter and pass when you are done.

## Sources

- Tozour, P. (2008). "Fixing Pathfinding Once and For All." *Game/AI* blog (ai-blog.net), 26 July 2008. Waypoint graph limitations; list of shipped games using navmeshes (Halo 2, Halo 3, F.E.A.R., Counter-Strike: Source, Metroid Prime series, Jak series).
- Mononen, M. (2010). "Simple Stupid Funnel Algorithm." *Digesting Duck* blog, 8 March 2010. The apex, left and right funnel with restarts.
- recastnavigation project, README and source (GitHub, main branch, accessed September 2026). Four-step Recast pipeline; "powers AI navigation features in Unity, Unreal, Godot, O3DE". `Recast.h`: `walkableSlopeAngle`, `walkableHeight`, `walkableClimb`, `walkableRadius`, `maxEdgeLen`, `maxVertsPerPoly`. `DetourNavMeshQuery.cpp`: `findPath` places nodes at edge midpoints and uses `H_SCALE = 0.999` on straight-line distance; `findStraightPath` performs string pulling. https://github.com/recastnavigation/recastnavigation
- Factorio, "Friday Facts #317: New pathfinding algorithm" (18 October 2019). Chunk-level abstraction ahead of detailed search.
- Sturtevant, N. R. (2013). "Choosing a Search Space Representation." In S. Rabin (ed.), *Game AI Pro*, chapter 18. CRC Press. Free at gameaipro.com.
- Millington, I. (2019). *AI for Games*, 3rd ed., chapter 4. CRC Press.

## Interactive spec: examples/w05-navmesh-funnel.html

**Purpose.** Let the student see the difference between walking through portal midpoints and pulling the string, and watch the funnel algorithm decide where the corners are.

**The one insight.** The funnel path only ever bends at portal endpoints (real corners), and it is always shorter than the midpoint path. The first screen must show both paths on the default level with their lengths, 19.07 m and 17.78 m, so the insight is visible before any interaction.

**Scene.** Top-down view of the five rectangles from section 2, in meters, y up: Room A (0,0)-(4,4), Corridor (4,1)-(10,3), Room B (10,0)-(14,8), Door (10,8)-(12,9), North room (8,9)-(14,13). Fill walkable polygons in a light tint with thin outlines; draw portals as dashed segments with their endpoints marked L and R for the current direction of travel. Everything outside the polygons is wall (hatched).

**Controls.**
- Drag start (default (1, 1)) and goal (default (13, 11)); both clamp to the nearest point inside the mesh. Keyboard: Tab to a handle, arrow keys move it by 0.25 m, Shift+arrow by 1 m.
- Door width slider: moves the door's east edge (and the matching part of the portals) from x = 10.5 to x = 14, default 12. The north room and Room B do not change.
- Agent radius slider, 0 to 0.8 m, step 0.1, default 0. When above 0, shrink every polygon by the radius (for these axis-aligned rectangles, move each side that borders a wall inward by r; portal endpoints move inward by r too) and draw the original outline faintly.
- Toggle: show midpoint path, show funnel path (both on by default).
- Funnel stepper: "step" and "reset" buttons. Each step processes one portal side (right, then left) and draws the apex (dot), left ray and right ray, and highlights the portal being tested. When the funnel collapses, flash the new corner and draw it into the path.
- Preset buttons for the check-yourself cases: "Goal (9, 12)" and "Two doors" (the section 3 layout: start (0,0), goal (10,0), wall at x = 5 with gaps y ∈ [1, 9] and y ∈ [−3, −2]; show both corridors, their midpoint costs 14.14 and 11.18, and their funnel lengths 10.20 and 10.77, and highlight the one A* picks by midpoint cost).

**Readouts.** Next to the map: a table listing each path's points and total length to two decimals, and the number of turns. Corridor as a list of polygon names. For the two-doors preset, the midpoint cost and funnel length of each door.

**Formulas and test values.** Use the lecture's `cross` and `funnel` exactly (port to JS). Midpoint path = start, portal midpoints in order, goal. Test values the builder must reproduce:
- default: midpoint 19.07 m with points (1,1), (4,2), (10,2), (11,8), (11,9), (13,11); funnel 17.78 m with points (1,1), (10,3), (12,9), (13,11).
- goal (9, 12): funnel (1,1), (10,3), (10,9), (9,12), length 18.38.
- start (2, 2), goal (13, 1) (corridor A → corridor → B only): funnel is a straight line, length 11.05.
- door east edge at 13: funnel (1,1), (10,3), (13,11), length 17.76.
- agent radius 0.5, default start and goal: portals ((4,2.5),(4,1.5)), ((10,2.5),(10,1.5)), ((10.5,8),(11.5,8)), ((10.5,9),(11.5,9)); funnel (1,1), (4,1.5), (10,2.5), (11.5,9), (13,11), length 18.29.

**Accessibility.** All controls keyboard reachable; path lengths in an `aria-live="polite"` region; step animations respect `prefers-reduced-motion` (no flash, just redraw).
