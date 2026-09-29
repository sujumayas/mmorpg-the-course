# CS203 · Week 04 — A* and heuristics

**Why this matters:** Dijkstra's algorithm finds the cheapest path, but it finds it by looking in every direction at once, including straight away from the goal. A* adds one number per cell, a guess of the distance left, and on a typical game map it looks at a third of the cells or fewer for the same answer. The guess is also where most pathfinding bugs come from. Pick it badly and your units walk past the road, or your server stalls when 200 enemies path around a lake.

**You will be able to:**
- Compute `f = g + h` for any cell on a grid and predict which cell A* expands next.
- Choose an admissible heuristic for 4-connected, 8-connected, hex and weighted-terrain maps, and prove a given heuristic is or is not admissible with one counterexample.
- Measure nodes expanded and path cost for Dijkstra, A* and weighted A* on the same map, and explain the difference from the shape of the search.
- Decide when to trade path quality for search speed, and state the bound you are accepting.

**Before class:** Millington, *AI for Games* (3rd ed., 2019), chapter 4 "Pathfinding", the sections on A* and on heuristics. Rabin, S. and Sturtevant, N., "Pathfinding Architecture Optimizations", *Game AI Pro* (2013), chapter 17, sections 17.1 to 17.3 (free online at gameaipro.com). Skim Amit Patel's "Introduction to the A* Algorithm" (Red Blob Games) and play with its diagrams for ten minutes.

**Prerequisites from earlier courses:** [CS102 week 8, graphs, maps and dialogue](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w08-graphs-maps-and-dialogue.md) (adjacency lists and breadth-first search). [CS203 week 3, graphs and Dijkstra](w03-graphs-and-dijkstra.md), which this lecture treats as the baseline (same `g(n)`, open list and closed set). [MA101 week 14, distances](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w14-distances-ranges-and-squared-distance.md) (Manhattan, Chebyshev and Euclidean distance; you will reuse them as heuristics). [CS102 week 4, Big-O intuition](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w04-big-o-intuition-for-game-developers.md). [GD201 week 7, verticality and navigation](../../GD201-level-and-world-design/lectures/w07-verticality-and-navigation.md) used Dijkstra to time routes through a level; this week makes that search fast.

**Interactive:** [`examples/w04-astar-vs-dijkstra.html`](../examples/w04-astar-vs-dijkstra.html). Keep it open during section 2.

---

## 1. What Dijkstra wastes

Last week you ran Dijkstra's algorithm. It keeps an open list (a priority queue of cells waiting to be looked at), always takes out the cell with the smallest cost so far, and relaxes its neighbors. We call that cost `g(n)`: the cheapest known cost from the start to cell `n`. Taking a cell out of the open list and relaxing its neighbors is called **expanding** it. The number of cells expanded is the honest measure of how much work a search did, because every expansion costs a heap operation and a look at every neighbor.

Dijkstra expands cells in order of `g`. On an open grid with 4-way movement, the cells with `g ≤ 5` form a diamond around the start, and the search grows that diamond one ring at a time until the goal falls inside it. The goal might be 11 cells east. Dijkstra doesn't know that. It spends as much effort 11 cells west, north and south as it does east. On a square map with the goal at distance `d`, that is roughly `2d²` cells for a path of `d` steps.

That was fine for GD201's five-node level graph. It is not fine when an RTS player drags a box around 60 units and right-clicks the far side of a 256 × 256 map.

## 2. Worked example: A* vs Dijkstra on the same map

### The hook

In October 2019, Factorio's developers published a Friday Facts post (FFF-317) about rewriting how the game's biters find paths. Factorio used A*. The trouble showed up when a player's artillery provoked a biter base on the far side of a lake. Hundreds of biters asked for paths at once, and each search was guided by straight-line distance to the target. Straight-line distance points across the water. So every search first flooded the near shore, cell by cell, before it discovered the way around. The fix was not a faster A*. It was a better guess of the remaining distance, taken from a coarse map of 32 × 32-tile chunks that already knew about the lake.

Hold on to that. Same algorithm, same map, same answer, and a very different amount of work, all decided by one function.

### The model

A* is Dijkstra with one change to the priority. Instead of ordering the open list by `g(n)`, it orders by

```
f(n) = g(n) + h(n)
```

- `g(n)` is the cheapest known cost from the start to `n`, exactly as in Dijkstra.
- `h(n)` is the **heuristic**: an estimate of the cheapest cost from `n` to the goal. It must be computable from `n` and the goal alone, without searching.
- `f(n)` is then an estimate of the cost of the best full path that goes through `n`.

Everything else is unchanged: pop the lowest `f`, skip it if already closed, relax its neighbors, stop when the goal is popped.

Two special cases tell you what `h` does. With `h = 0` everywhere, `f = g` and A* **is** Dijkstra. With `g` ignored and only `h` used, you get greedy best-first search, which charges at the goal and often finds a poor path. A* sits between them.

One rule makes the answer correct. If `h(n)` never overestimates the true remaining cost, A* returns a cheapest path. Such a heuristic is called **admissible**. A slightly stronger property, **consistency**, says that for every edge from `n` to `m` with cost `c`, `h(n) ≤ c + h(m)`: the estimate never drops by more than the step you just paid for. With a consistent heuristic, A* never needs to reopen a closed cell. All the heuristics in this lecture are consistent.

For a 4-connected grid where every step costs 1, the natural heuristic is Manhattan distance from MA101 week 14:

```
h(n) = |row(n) − row(goal)| + |col(n) − col(goal)|
```

It is admissible because no 4-way path can be shorter than the rows and columns it must cross.

### The code

This program runs both searches on the same 8 × 12 map with a wall in the way. It uses Python's `heapq` as the open list. The tuple pushed onto the heap is `(f, h, cell)`, so ties on `f` go to the cell with the smaller `h` (the one nearer the goal), then to the smaller `(row, col)`. The `w` argument is for section 4; leave it at 1 for now.

```python
import heapq

MAP = [
    "............",
    "............",
    "....#.......",
    "....#.......",
    "S...#......G",
    "....#.......",
    "....#.......",
    "............",
]

def find(ch):
    for r, row in enumerate(MAP):
        if ch in row:
            return (r, row.index(ch))

def neighbors(cell):
    r, c = cell
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(MAP) and 0 <= nc < len(MAP[0]) and MAP[nr][nc] != "#":
            yield (nr, nc)

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def zero(a, b):
    return 0

def search(start, goal, h, w=1):
    g = {start: 0}
    frontier = [(w * h(start, goal), h(start, goal), start)]
    closed = set()
    while frontier:
        f, _, cell = heapq.heappop(frontier)
        if cell in closed:
            continue
        closed.add(cell)
        if cell == goal:
            return g[goal], len(closed)
        for nxt in neighbors(cell):
            new_g = g[cell] + 1
            if new_g < g.get(nxt, float("inf")):
                g[nxt] = new_g
                hn = h(nxt, goal)
                heapq.heappush(frontier, (new_g + w * hn, hn, nxt))

S, G = find("S"), find("G")
for name, h, w in [("Dijkstra (h = 0)", zero, 1),
                   ("A* (Manhattan)", manhattan, 1),
                   ("Weighted A* (w = 2)", manhattan, 2)]:
    cost, expanded = search(S, G, h, w)
    print(f"{name:20} path cost {cost}, cells expanded {expanded}")
```

Output:

```
Dijkstra (h = 0)     path cost 17, cells expanded 91
A* (Manhattan)       path cost 17, cells expanded 32
Weighted A* (w = 2)  path cost 17, cells expanded 30
```

The map has 96 cells, 5 of them wall, so 91 are open. Dijkstra expanded every open cell on the map to find a 17-step path. A* found the same 17-step path after expanding 32, about a third.

### Numbers you can check

The start is `S = (4, 0)` (row 4, column 0) and the goal is `G = (4, 11)`. The wall occupies column 4, rows 2 to 6. Here are A*'s first eight expansions. Check each `h` and `f` by hand.

| Order | Cell | g | h | f = g + h | Why this one |
|---|---|---|---|---|---|
| 1 | (4, 0) | 0 | 11 | 11 | the start |
| 2 | (4, 1) | 1 | 10 | 11 | f = 11, smallest h |
| 3 | (4, 2) | 2 | 9 | 11 | f = 11 |
| 4 | (4, 3) | 3 | 8 | 11 | f = 11; its east neighbor is wall |
| 5 | (3, 3) | 4 | 9 | 13 | no f = 11 cells left; f = 13, h = 9 |
| 6 | (5, 3) | 4 | 9 | 13 | tie with (3, 3), smaller row went first |
| 7 | (3, 2) | 3 | 10 | 13 | f = 13 |
| 8 | (5, 2) | 3 | 10 | 13 | f = 13 |

Rows 1 to 4 are A* doing what you hoped. Every step east keeps `f` at 11, because `g` goes up by 1 and `h` goes down by 1. The search runs straight at the goal. Then it hits the wall. No cell with `f = 11` is left, so it moves to the `f = 13` layer, and that layer includes cells back toward the start, like (3, 2) and (5, 2). This is A*'s version of the Factorio lake. When the heuristic points into an obstacle, A* fills the pocket in front of it one `f`-layer at a time until some layer reaches around the obstacle.

How much does the wall cost? The true path must climb from row 4 to row 1 to clear the wall's top end at row 2, then come back down: 3 rows up and 3 down on top of 11 columns across. That is `11 + 6 = 17`. A* must expand every cell with `f < 17` before it can be sure nothing cheaper exists, plus some with `f = 17`. Dijkstra must expand every cell with `g < 17`. On this map that is 90 cells, and with the goal itself it makes all 91.

A useful rule of thumb follows. **A*'s saving is largest when the heuristic is close to the true remaining cost.** On open ground Manhattan distance is exact, and A* expands only cells on a best path. Behind a wall it is off by the length of the detour, and A* pays for the difference.

### The visual

Open [`w04-astar-vs-dijkstra.html`](../examples/w04-astar-vs-dijkstra.html). The same map appears twice, Dijkstra on the left and A* on the right, with shared playback controls. Press play. Dijkstra's closed set grows as a diamond centered on the start. A*'s closed set grows as a thin line toward the goal, then bulges when it hits the wall. The counters under each grid read 91 and 32 at the end.

Now drag the goal around the wall to the same side as the start. Both counters drop, and A*'s drops more. Paint a longer wall and watch A*'s bulge grow while Dijkstra's diamond barely changes. Switch to the "lake" map, a U-shaped obstacle open away from the goal, and you are looking at the Factorio problem from the hook.

### Cross-game recognition

**Factorio (FFF-317, October 2019).** The biter pathfinder was already A*. What changed was `h`. The new version builds an abstract graph: each 32 × 32 chunk is reduced to a few nodes, one per connected patch of walkable tiles. A second search runs backwards from the goal over that abstract graph, and its distances become `h` for the detailed search. Distances on the abstract graph go around the lake, so `h` stops pointing into water. The post also describes keeping the abstract search's results between queries rather than restarting it, which the developers call Reverse Resumable A*. In our terms, they bought a heuristic much closer to the true cost, and paid for it with a second, cheap search.

**Civilization VI (with Gathering Storm).** Week 3 used this game's terrain costs: 1 movement point (MP) for flat open tiles, 2 for woods, hills or marsh. Roads go the other way. Per the Civilization Wiki, industrial-era roads cost 0.75 MP per tile, modern roads 0.5 MP, and Gathering Storm's railroads 0.25 MP. Now ask what heuristic keeps A* correct. Counting tiles to the goal (1 per tile) is admissible only if no tile costs less than 1. Once modern roads exist, a tile count can overestimate by a factor of 2, and with railroads by a factor of 4, so A* may ignore a road that really is faster. The admissible version multiplies the tile distance by the cheapest possible step: `h = 0.75 × tiles` in the industrial era, `0.5 × tiles` with modern roads, `0.25 × tiles` once railroads exist. The map is hexagonal, so "tiles" means hex distance, which in cube coordinates is `max(|dq|, |dr|, |ds|)` (Patel, "Hexagonal Grids"). Same A*, different distance function, and the scale factor is set by the cheapest terrain, which changes as the game goes on.

**The Moving AI benchmark maps.** When researchers compare pathfinding algorithms, they mostly use grid maps taken from shipped games: Dragon Age: Origins, Dragon Age 2, Baldur's Gate II, StarCraft and Warcraft III, maintained by Nathan Sturtevant's Moving AI Lab (Sturtevant 2012). BioWare gave permission for its maps to be shared for research. Nodes expanded, the number you just counted, is one of the standard measures on those maps. When you read a paper that says a method "expands 40% fewer nodes than A* with octile distance", it means the same thing as your 91 vs 32.

Three contexts, one model. Every one of them is `f = g + h`, and every design discussion is about `h`.

### Eyes-open design judgment

- **A* is only as good as `h`.** A cheap, admissible, badly informed `h` (straight-line distance through a lake) gives correct paths at Dijkstra-like cost. Before optimizing the heap, measure nodes expanded per query on your worst maps.
- **Better heuristics cost memory or setup time.** Factorio's abstract graph must be kept in step with player-built walls. Precomputed distance tables (the "differential heuristics" discussed in *Game AI Pro* chapter 17) cost memory per landmark. Decide what your game can afford per map, not per query.
- **The heuristic must match the movement rules exactly.** Allow diagonal moves and Manhattan distance becomes inadmissible (section 3). Add roads and "1 per tile" becomes inadmissible. Every rule change to movement is a rule change to `h`. Put that on the design checklist.
- **Players judge paths, not search counts.** An optimal path that zig-zags across a grid looks worse than a slightly longer straight one. Week 5 fixes that with navigation meshes and path smoothing.

## 3. Heuristics for the maps you will actually build

The table lists the standard admissible heuristic for each movement rule. `dx` and `dy` are the absolute column and row differences to the goal, `D` is the cost of a straight step and `D2` the cost of a diagonal step.

| Movement | Heuristic | Formula | Exact on an empty map? |
|---|---|---|---|
| 4-way grid | Manhattan | `D × (dx + dy)` | yes |
| 8-way grid, diagonal costs D | Chebyshev | `D × max(dx, dy)` | yes |
| 8-way grid, diagonal costs D2 | Octile | `D × max(dx, dy) + (D2 − D) × min(dx, dy)` | yes |
| Any angle (navmesh, open terrain) | Euclidean | `D × sqrt(dx² + dy²)` | yes |
| Hex grid | Hex distance | `D × max(|dq|, |dr|, |ds|)` in cube coordinates | yes |
| Any of the above with terrain costs | same formula | multiply by the cheapest terrain factor | no, only a lower bound |

The octile formula comes from counting moves. To cover `dx = 5, dy = 3` with 8-way steps, take 3 diagonal steps (they fix 3 rows and 3 columns at once) and 2 straight ones. With `D = 10, D2 = 14`, that costs `3 × 14 + 2 × 10 = 62`. The formula gives `10 × 5 + 4 × 3 = 62`.

### Proving a heuristic is wrong takes one cell

On an 8-way grid with `D = 10, D2 = 14`, is Manhattan distance admissible? Try the cell diagonally next to the goal. Manhattan says `10 × (1 + 1) = 20`. The true cost is one diagonal step, 14. Overestimate by 6, so no. Farther along the diagonal, `k` steps away, the overestimate is `6k`. The lab has you measure exactly this on a 16 × 16 map.

To prove a heuristic *is* admissible you need an argument for every cell, like "no path can cross fewer rows than dy." To prove it is not, you need one cell. That asymmetry is worth using in code review: for any heuristic someone proposes, ask for the cheapest single move in the game and check `h` against it.

### Terrain costs push `h` down

Weighted terrain makes the true cost higher than distance, never lower, as long as every terrain factor is at least 1. So plain octile distance stays admissible on a map with mud at 3× cost. It just becomes less informed: A* explores more, because `h` underestimates the muddy parts. If some terrain is cheaper than the base (roads), scale `h` down to the cheapest factor, as in the Civilization VI example.

## 4. Breaking admissibility on purpose

Sometimes you want a fast path more than a perfect one. **Weighted A*** orders the open list by

```
f(n) = g(n) + w × h(n),   w ≥ 1
```

The bigger `w`, the more A* behaves like greedy best-first search. There is a guarantee, which is why the method is respectable. With an admissible `h`, weighted A* returns a path whose cost is at most `w` times the optimum. With `w = 2`, never worse than double. In the wall map above, `w = 2` found the same 17-step path and saved two expansions. On larger open maps the savings are much bigger.

The danger is an overestimate you did not choose. The next program is the Civilization VI modern-road problem in miniature. Road tiles (`=`) cost 1 to enter, open ground (`.`) costs 2, both in half movement points. The straight route across the ground is 10 tiles. The road route goes 3 tiles up, 10 across and 3 down.

```python
import heapq

# = is road (costs 1 to enter), . is open ground (costs 2 to enter).
# Units are half movement points, so road = 0.5 MP and ground = 1 MP.
MAP = [
    "===========",
    "=.........=",
    "=.........=",
    "S.........G",
    "...........",
]
S, G = (3, 0), (3, 10)

def cost(cell):
    return 1 if MAP[cell[0]][cell[1]] in "=SG" else 2

def neighbors(cell):
    r, c = cell
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(MAP) and 0 <= nc < len(MAP[0]):
            yield (nr, nc)

def astar(per_tile):
    h = lambda a: per_tile * (abs(a[0] - G[0]) + abs(a[1] - G[1]))
    g = {S: 0}
    frontier = [(h(S), h(S), S)]
    closed = set()
    while frontier:
        _, _, cell = heapq.heappop(frontier)
        if cell in closed:
            continue
        closed.add(cell)
        if cell == G:
            return g[G], len(closed)
        for nxt in neighbors(cell):
            new_g = g[cell] + cost(nxt)
            if new_g < g.get(nxt, float("inf")):
                g[nxt] = new_g
                heapq.heappush(frontier, (new_g + h(nxt), h(nxt), nxt))

for per_tile in (0, 1, 2):
    c, n = astar(per_tile)
    print(f"h = {per_tile} per tile: path cost {c}, cells expanded {n}")
```

Output:

```
h = 0 per tile: path cost 16, cells expanded 50
h = 1 per tile: path cost 16, cells expanded 33
h = 2 per tile: path cost 19, cells expanded 11
```

Check the costs by hand. The road route enters 16 road tiles (3 up, 10 across, 3 down, with G itself a road tile) at 1 each: 16. The straight route enters 9 ground tiles at 2 and then G at 1: 19. With `h = 1` per tile, `h` is admissible (no tile costs less than 1) and A* finds the road. With `h = 2` per tile, the "obvious" choice if you think of ground as the normal cost, `h` overestimates every road tile by a factor of 2. A* expands 11 cells, marches straight across the ground and returns 19. The player sees their unit ignore a road that was right there. Nothing crashed, no assertion fired, and the bug report will say "units are dumb about roads."

The difference from weighted A* is that you know you chose `w` and you know the bound. An accidental overestimate has no bound you control.

## 5. What the search costs

Each expansion does one heap pop (`O(log n)` for `n` entries in the open list) and one relaxation per neighbor, each of which may push onto the heap. The closed set and the `g` table grow with the number of cells touched. In the terms of CS102 week 4, A* is `O(E log V)` in the worst case, exactly like Dijkstra. Its advantage is not a better worst case. It is that on real maps with a good `h` it touches a small fraction of `V`.

Two practical details decide real performance:

- **Tie-breaking.** On open grids many cells share the same `f`. Breaking ties toward smaller `h` (as the code above does) makes A* follow one path to the goal instead of exploring a whole band of equally good ones. On an empty grid it is the difference between expanding a thin line and a filled rectangle.
- **Duplicates in the heap.** The code pushes a cell again when it finds a cheaper `g` and skips stale copies on pop (the `if cell in closed: continue` line). That is simpler than a decrease-key operation, and Python's `heapq` has none anyway. The cost is a heap that can hold a few copies of some cells.

*Game AI Pro* chapter 17 lists these and several more optimizations with measured speedups. Read it before you optimize anything, and measure nodes expanded first.

## In-class activity (25 minutes)

Work in pairs with graph paper and the interactive.

1. Draw a 10 × 10 grid. Place S and G nine columns apart on the same row. Draw a wall of your choice between them, at most 8 cells long.
2. By hand, run A* with Manhattan distance for the first ten expansions. Record `g`, `h` and `f` for each, as in the table in section 2. Use the tie-breaking rule from the lecture.
3. Predict the final number of cells A* and Dijkstra will expand. Write both numbers down before you check.
4. Build the same map in the interactive's custom mode and compare. If your prediction was off by more than 30%, find the first expansion where your trace and the interactive disagree.
5. Now change the wall so that A* expands at least three times as many cells as it did in step 4, while keeping the path cost the same or lower. Describe the shape you used in one sentence.

Expected output: a trace table, two predictions with their errors, and a wall shape that makes A* expensive with a sentence explaining why (it should mention where `h` points).

## Common misconceptions

- **"A* is faster than Dijkstra."** Only with an informative `h`. With `h = 0` it is Dijkstra, and with a heuristic that points into a large obstacle it can expand almost as much. The speedup is a property of the map plus the heuristic.
- **"A bigger heuristic is always better because it expands fewer nodes."** Up to the true cost, yes. Past it, you lose the guarantee of the cheapest path, as the road map showed (cost 19 instead of 16).
- **"Euclidean distance is always safe."** It is admissible for any movement where straight lines are the shortest route and every cost is at least the distance. On a map with roads or teleporters that are cheaper than walking, it can overestimate. Scale it by the cheapest cost per unit of distance, or add teleporter endpoints to the heuristic.
- **"A* finds the shortest path."** It finds the cheapest path under the costs you gave it. If your costs do not match the movement rules (diagonals costing 1, roads missing), the path is optimal for the wrong problem.

## Check yourself

1. On the 4-way map in section 2, compute `g`, `h` and `f` for the corner cell (0, 0). Does A* ever expand it? Does Dijkstra?
2. An 8-way grid uses `D = 10, D2 = 14`. Compute the octile heuristic from (2, 3) to (9, 5). Then give a cell and goal where Chebyshev distance `10 × max(dx, dy)` underestimates the true empty-map cost by more than 20.
3. In Civilization VI with Gathering Storm, a late-game map has open ground (1 MP), modern roads (0.5 MP) and a few railroads (0.25 MP). A designer proposes `h = hex distance × 0.5`, "because most of our fast routes are roads". Is it admissible? What would you change?
4. Weighted A* with `w = 1.5` on a map whose cheapest path costs 40. What is the worst path cost it can return? If playtesters never notice paths up to 10% longer than optimal, what is the largest `w` that guarantees they never notice?
5. In the road map of section 4, what is the largest per-tile factor that keeps `h` admissible? Is `h = 1.5` per tile guaranteed to find the road?

<details>
<summary>Answers</summary>

1. `g = 4` (four steps up from (4, 0)). `h = |0 − 4| + |0 − 11| = 15`. `f = 19`. The cheapest path costs 17, and with a consistent heuristic A* never expands a cell whose `f` exceeds the optimal cost, so A* never touches (0, 0). Dijkstra orders by `g` alone, and `g = 4 < 17`, so Dijkstra expands it early.
2. `dx = 2, dy = 7`, so `10 × 7 + 4 × 2 = 78`. Chebyshev charges 10 for each diagonal step instead of 14, so it underestimates by `4 × min(dx, dy)`. Any pair with `min(dx, dy) ≥ 6`, for example (0, 0) to (6, 6): Chebyshev 60, true 84, off by 24.
3. No. Railroad hexes cost 0.25, less than 0.5, so along a railroad `h` can overestimate by a factor of 2, and A* may skip the railroad. Use `h = hex distance × 0.25`, or keep 0.25 as the floor and build a better-informed heuristic from a precomputed railroad network (the Factorio idea).
4. At most `1.5 × 40 = 60`. To guarantee at most 10% longer you need `w ≤ 1.1`.
5. The cheapest tile costs 1, so the largest admissible factor is 1. With 1.5 the heuristic overestimates road tiles by 50%, so there is no guarantee. On this map it misses the road: change the loop to `(0, 1, 1.5, 2)` and the 1.5 row reports path cost 19 after 17 expansions.

</details>

## Lab / assignment hook

[Lab 04, A* on a tactical grid](../labs/lab04.md). You implement octile distance and A* on an 8-way grid with mud and walls, check them against a reference Dijkstra, measure nodes expanded on four maps, and write a tool that finds the worst overestimate of any heuristic. The checks in `check_lab04.py` fail on the starter and pass when you are done.

## Sources

- Hart, P. E., Nilsson, N. J. and Raphael, B. (1968). "A Formal Basis for the Heuristic Determination of Minimum Cost Paths." *IEEE Transactions on Systems Science and Cybernetics* 4(2), 100-107. The original A* paper, with the admissibility result.
- Dijkstra, E. W. (1959). "A note on two problems in connexion with graphs." *Numerische Mathematik* 1, 269-271.
- Factorio, "Friday Facts #317: New pathfinding algorithm", by Oxyd, 18 October 2019. https://www.factorio.com/blog/post/fff-317. A* with a straight-line heuristic, the lake problem during artillery aggro, 32 × 32 chunk abstraction, reverse resumable A* as the heuristic source.
- Civilization Wiki (Fandom), "Road (Civ6)" and "Railroad (Civ6)". Civilization VI: industrial roads 0.75 MP per tile, modern roads 0.5 MP; railroads (Gathering Storm expansion, 2019) 0.25 MP. Base terrain costs as cited in CS203 week 3.
- Patel, A., "Introduction to the A* Algorithm" and "Hexagonal Grids", Red Blob Games (redblobgames.com). Heuristic families, tie-breaking, cube-coordinate hex distance.
- Sturtevant, N. (2012). "Benchmarks for Grid-Based Pathfinding." *IEEE Transactions on Computational Intelligence and AI in Games* 4(2), 144-148. Moving AI Lab benchmark page (movingai.com/benchmarks/grids.html) lists maps from Dragon Age: Origins, Dragon Age 2, Warcraft III, Baldur's Gate II and StarCraft, and credits BioWare for permission.
- Rabin, S. and Sturtevant, N. R. (2013). "Pathfinding Architecture Optimizations." In S. Rabin (ed.), *Game AI Pro*, chapter 17. CRC Press. Free at gameaipro.com.
- Millington, I. (2019). *AI for Games*, 3rd ed., chapter 4. CRC Press.

## Interactive spec: examples/w04-astar-vs-dijkstra.html

**Purpose.** The signature example of CS203. Show Dijkstra and A* running on the same map at the same time, so the student sees the diamond versus the beam, and the counters make the saving a number.

**The one insight.** A*'s work depends on how well `h` matches the true remaining cost. On the default map, the student should see within five seconds of pressing play that A* heads straight for the goal while Dijkstra spreads in all directions, and that A* bulges exactly where the wall blocks the line of sight to the goal.

**Layout.** Two grids side by side on desktop (Dijkstra left, A* right), stacked on mobile (A* first). Under each grid: "expanded N", "open list N", "path cost N". One shared control bar above both. First screen shows the default map with both searches already run to completion (final closed sets and paths visible), so the insight is on screen before any interaction. A "replay" button restarts the animation.

**Grid and rules.** 4-connected, every step costs 1, unless the "roads" map is selected. Cells: open, wall, road (road maps only), S, G. Search code must match the lecture exactly: heap key `(f, h, row, col)` compared lexicographically, where `f = g + w × h`; duplicates allowed in the open list; stale entries skipped on pop; expansion count = size of closed set when the goal is popped (goal included). Dijkstra is the same function with `h = 0`.

**Maps (selector).**
1. "Wall" (default): the 8 × 12 map from the lecture. S = (4, 0), G = (4, 11), wall at column 4, rows 2-6. Expected: Dijkstra cost 17, expanded 91. A* Manhattan cost 17, expanded 32. Weighted A* w = 2 cost 17, expanded 30.
2. "Lake": 9 × 14, rows
   `..............`, `..............`, `......####....`, `.........#....`, `..S......#..G.`, `.........#....`, `......####....`, `..............`, `..............`.
   Expected: Dijkstra cost 16, expanded 113. A* Manhattan cost 16, expanded 44.
3. "Roads": the 5 × 11 map from section 4, rows `===========`, `=.........=`, `=.........=`, `S.........G`, `...........`, S = (3, 0), G = (3, 10); entering road, S or G costs 1, ground costs 2. Heuristic = per-tile factor × Manhattan. Expected: factor 0: cost 16, expanded 50. Factor 1: cost 16, expanded 33. Factor 2: cost 19, expanded 11.
4. "Custom": 12 × 16 empty grid; click or tap (and Enter on a focused cell) toggles wall; drag S and G. Arrow keys move a focus cursor over cells.

**Controls.**
- Heuristic: Manhattan / Euclidean / zero (A* side only). On the Roads map, a slider "cost per tile in h" from 0 to 2 in steps of 0.5 replaces the heuristic choice.
- Weight `w` slider, 1.0 to 3.0, step 0.1 (A* side only). Label shows the bound: "path cost ≤ w × optimal".
- Play / pause, step (one expansion on each side), speed (1, 5, 20 expansions per second, plus "instant"), replay.
- Each control change reruns both searches instantly and shows the final state; the animation only runs on play or replay.

**Drawing.** Closed cells shaded with intensity by expansion order (early light, late dark). Open-list cells outlined. Final path drawn as a thick line through cell centers. Hovering or focusing a cell shows `g`, `h`, `f` for that cell on the A* side and `g` on the Dijkstra side. Use steel for Dijkstra, ochre for A*, red for the path, per the palette.

**Readouts that must match the lecture.** The eight-row trace table of section 2 must be reproducible with the step button on the Wall map: after 8 steps, A*'s closed cells are exactly (4,0), (4,1), (4,2), (4,3), (3,3), (5,3), (3,2), (5,2). Show a small "last expanded: (r, c) g h f" line under the A* grid.

**Accessibility.** All controls keyboard reachable; counters in an `aria-live="polite"` region updated at most once per second during animation; respects `prefers-reduced-motion` by defaulting speed to "instant".
