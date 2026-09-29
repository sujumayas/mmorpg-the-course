# CS203 · Week 03 — Graphs and Dijkstra

**Why this matters:** Every time a strategy game highlights where your unit can move, or an NPC takes the long road around a swamp, a shortest-path search has run over a weighted graph. Breadth-first search from CS102 counts steps, but players care about time, and time is not steps. Dijkstra's algorithm is the fix, and it is also the baseline every faster pathfinder in the next two weeks is measured against.

**You will be able to:**
- Model a level as a weighted graph (rooms and corridors, or a tile grid with terrain costs) and state what the weights mean in game units.
- Trace Dijkstra's algorithm by hand, open list included, and compute costs, paths and the order in which nodes are expanded.
- Compute a unit's movement range under a budget and explain where real turn-based rules (Civilization VI's) break the simple model.
- Critique a cost table and choose between BFS, Dijkstra and a multi-source Dijkstra map for a given NPC job.

**Before class:** Millington, *AI for Games* (3rd ed., 2019), chapter 4, the sections on the pathfinding graph and Dijkstra. Reread CS102 week 8, section 3 (breadth-first search). Brian Walker, "The Incredible Power of Dijkstra Maps", RogueBasin (free online, 15 minutes).

**Prerequisites from earlier courses:** [CS102 week 8, graphs, maps and dialogue](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w08-graphs-maps-and-dialogue.md) (adjacency lists, directed edges, BFS, `dist` and `prev`; this week reuses the same seven-room dungeon). [CS102 week 6, queues and stacks](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w06-queues-and-stacks-undo-and-command-buffers.md) (the FIFO queue that Dijkstra replaces with a priority queue). [CS102 week 4, Big-O](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w04-big-o-intuition-for-game-developers.md) (reading `O((V + E) log V)`). [GD201 week 7, verticality and navigation](../../GD201-level-and-world-design/lectures/w07-verticality-and-navigation.md) (you used Dijkstra there to time routes through a level; this week opens the box). [CS203 week 1](w01-game-ai-vs-academic-ai.md) (the five tests).

**Interactive:** [`examples/w03-dijkstra-terrain.html`](../examples/w03-dijkstra-terrain.html). Keep it open during section 2.

---

## 1. Weighted graphs

In CS102 week 8 every edge cost one move. That is right for a text adventure, where `GO NORTH` is one command whatever the room. It is wrong almost everywhere else. A corridor can be 4 seconds long or 15. A forest tile takes longer to cross than a road. A **weighted graph** gives each edge a number, its **weight** or **cost**, and the length of a path becomes the sum of its edge costs rather than the count of its edges.

The weights must mean something in game units, and you must say what. Typical choices:

- **Seconds of travel.** Distance divided by speed, with slowdowns for mud or stairs. Natural for real-time NPCs.
- **Movement points.** The currency of turn-based games. A unit gets a budget per turn, and each tile costs some of it.
- **Risk or preference.** Designer-chosen numbers that make an NPC avoid lit areas or prefer cover. These are not physical, and that is fine, as long as everyone on the team knows what a cost of 3 means.

In an adjacency list, weights sit next to each neighbour. Here is the seven-room dungeon from CS102 week 8, now with walking times in seconds, plus one new edge, a collapsed stair from the Hall straight down to the Crypt that you have to squeeze through.

```
Gate --4-- Hall --3-- Armory --9-- Crypt --2-- Shrine
            |  \                  / |            |
            2   +------15--------+  4            1 (one-way drop)
            |                       |            v
           Well --------------------+          Vault --5--> Gate (one-way door)
```

Two warnings before we search it.

- **Undirected corridors are stored twice.** Hall to Armory and Armory to Hall are two directed edges with the same weight. One-way drops and doors are stored once, exactly as in CS102.
- **Costs must be zero or positive.** Dijkstra's algorithm, below, is only correct when no edge has a negative cost. If a designer wants a "speed boost pad" to make a route attractive, give it a small positive cost, never a negative one.

**BFS answers the wrong question here.** BFS from the Gate reaches the Crypt in two edges, Gate to Hall to Crypt, through the collapsed stair. That route takes `4 + 15 = 19` s. The route through the Well has three edges and takes `4 + 2 + 4 = 10` s. BFS picks the first because it counts edges. We want the second.

## 2. Worked example: why your unit walks around the hill

### The hook

In Civilization VI, hover your cursor over a tile a few moves away and the game draws the route your unit will take. Often it is not the straight line. It bends around hills and woods, and once your civilization has roads it may take a longer road rather than cut across open country. The game is not being clever. It is running a shortest-path search in which each tile has a movement cost.

Civilization VI's rules make the costs concrete. According to the Civilization Wiki's movement page for the game, a flat open tile costs 1 movement point (MP) to enter. Woods, rainforest, hills and marsh cost 2. Hills combined with woods or rainforest cost 3. Mountains are impassable. Roads change the numbers. An ancient road makes most terrain cost 1, industrial roads cost 0.75 per tile and modern roads 0.5. A path that is longer in tiles can be cheaper in MP, and the route preview picks the cheaper one.

This lecture uses Civilization VI's terrain costs in a simplified form. We charge the cost of each tile you enter and ignore rivers, roads and turn boundaries for now. Section 3 comes back to what the simplification leaves out.

### The model

**Dijkstra's algorithm** (Dijkstra, 1959) is BFS with one change. BFS takes nodes from a first-in, first-out queue, which delivers them in order of *number of edges*. Dijkstra takes them from a **priority queue** ordered by *total cost so far*, so it delivers them in order of cost. The vocabulary below is the one week 4 builds on.

- `g(n)` is the cheapest cost found so far from the start to node `n`. (CS102 called it `dist`.)
- The **open list** is the priority queue of nodes waiting to be looked at, each with the cost at which it was added. In Python, `heapq` keeps a list as a min-heap: `heappop` returns the smallest item.
- **Expanding** a node means taking it off the open list and looking at its outgoing edges. Once a node is expanded, its `g` is final. It goes into the **closed set**.
- **Relaxing** an edge from `u` to `w` with cost `c` means asking "is `g(u) + c` cheaper than the best I know for `w`?" If yes, record the new `g(w)`, set `prev[w] = u`, and push `w` onto the open list.

Why is a node's cost final when it comes off the open list? Every node still waiting has a cost at least as large as the one just taken, because the heap always returns the smallest. Any other route to this node would have to pass through one of those waiting nodes and then add edges of zero or positive cost, so it cannot be cheaper. That argument is exactly where "no negative edges" is needed.

Python's `heapq` has no "decrease key" operation, so when a node's cost improves we simply push it again. The old, more expensive copy stays in the heap. When it eventually comes out, the node is already closed and we skip it. This is called **lazy deletion**, and it is the standard way to write Dijkstra in Python.

```python
import heapq

DUNGEON = {                     # room: [(neighbour, seconds to walk), ...]
    "Gate":   [("Hall", 4)],
    "Hall":   [("Gate", 4), ("Armory", 3), ("Well", 2), ("Crypt", 15)],
    "Armory": [("Hall", 3), ("Crypt", 9)],
    "Well":   [("Hall", 2), ("Crypt", 4)],
    "Crypt":  [("Hall", 15), ("Armory", 9), ("Well", 4), ("Shrine", 2)],
    "Shrine": [("Crypt", 2), ("Vault", 1)],     # the drop into the vault is one-way
    "Vault":  [("Gate", 5)],                    # the door opens only from inside
}

def dijkstra(graph, start):
    g, prev = {start: 0}, {start: None}         # best known cost, and where it came from
    open_list = [(0, start)]                    # a min-heap of (cost so far, node)
    closed = set()
    while open_list:
        cost, u = heapq.heappop(open_list)
        if u in closed:
            print(f"skip   {u:6} at {cost:2} (stale)")
            continue
        closed.add(u)                           # expand u: its cost is now final
        print(f"expand {u:6} at {cost:2}")
        for w, step in graph[u]:                # relax each outgoing edge
            new = cost + step
            if w not in g or new < g[w]:
                g[w], prev[w] = new, u
                heapq.heappush(open_list, (new, w))
    return g, prev

def path_to(prev, target):
    path = []
    while target is not None:
        path.append(target)
        target = prev[target]
    return path[::-1]

g, prev = dijkstra(DUNGEON, "Gate")
print(g)
print(" -> ".join(path_to(prev, "Crypt")))
```

Output:

```
expand Gate   at  0
expand Hall   at  4
expand Well   at  6
expand Armory at  7
expand Crypt  at 10
expand Shrine at 12
expand Vault  at 13
skip   Crypt  at 19 (stale)
{'Gate': 0, 'Hall': 4, 'Armory': 7, 'Well': 6, 'Crypt': 10, 'Shrine': 12, 'Vault': 13}
Gate -> Hall -> Well -> Crypt
```

### Numbers you can check: the dungeon by hand

Trace it yourself before reading the table. The open list is shown after each expansion, smallest first.

| Step | Expand | `g` | Edges relaxed (new cost; kept?) | Open list afterwards |
|---|---|---|---|---|
| 1 | Gate | 0 | Hall 4 (new) | Hall 4 |
| 2 | Hall | 4 | Gate 8 (no), Armory 7 (new), Well 6 (new), Crypt 19 (new) | Well 6, Armory 7, Crypt 19 |
| 3 | Well | 6 | Hall 8 (no), Crypt 10 (better than 19) | Armory 7, Crypt 10, Crypt 19 |
| 4 | Armory | 7 | Hall 10 (no), Crypt 16 (no, 10 is better) | Crypt 10, Crypt 19 |
| 5 | Crypt | 10 | Hall, Armory, Well (no), Shrine 12 (new) | Shrine 12, Crypt 19 |
| 6 | Shrine | 12 | Crypt 14 (no), Vault 13 (new) | Vault 13, Crypt 19 |
| 7 | Vault | 13 | Gate 18 (no) | Crypt 19 |
| 8 | (Crypt 19) | — | stale copy, skipped | empty |

Step 2 is the moment BFS would have stopped caring. The Crypt was reached through the collapsed stair at cost 19, and in BFS that first discovery would have been final. In Dijkstra it is only a candidate. One step later the Well offers 10, and the Crypt's `g` drops. The expensive copy stays in the heap until step 8, when it is thrown away.

### Numbers you can check: terrain on a grid

A tile map is a graph too. Each open tile is a node, and it has an edge to each of its four neighbours. The edge costs whatever the *destination* tile costs to enter. Here is a 6 × 5 map using Civilization VI's costs: `.` open (1), `f` woods (2), `h` hills (2), `H` wooded hills (3), `M` mountain (impassable). The unit starts at the left edge of the middle row and wants the right edge.

```python
import heapq
from collections import deque

COST = {".": 1, "f": 2, "h": 2, "H": 3, "M": None}   # None: impassable
MAP = [
    "......",
    ".ffh..",
    ".hHHf.",
    ".fMf..",
    "......",
]
START, GOAL = (0, 2), (5, 2)                        # (column, row)

def neighbours(cell):
    x, y = cell
    for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):   # N, E, S, W
        nx, ny = x + dx, y + dy
        if 0 <= ny < len(MAP) and 0 <= nx < len(MAP[0]) and COST[MAP[ny][nx]]:
            yield (nx, ny), COST[MAP[ny][nx]]           # pay to ENTER a tile

def dijkstra(start, budget=float("inf")):
    g, prev, closed, order = {start: 0}, {start: None}, set(), []
    open_list = [(0, start)]
    while open_list:
        cost, u = heapq.heappop(open_list)
        if u in closed:
            continue
        closed.add(u)
        order.append(u)
        for w, step in neighbours(u):
            new = cost + step
            if new <= budget and (w not in g or new < g[w]):
                g[w], prev[w] = new, u
                heapq.heappush(open_list, (new, w))
    return g, prev, order

def bfs(start):
    prev, queue = {start: None}, deque([start])
    while queue:
        u = queue.popleft()
        for w, _ in neighbours(u):
            if w not in prev:
                prev[w] = u
                queue.append(w)
    return prev

def walk(prev, goal):
    path = []
    while goal is not None:
        path.append(goal)
        goal = prev[goal]
    return path[::-1]

def cost_of(path):
    return sum(COST[MAP[y][x]] for x, y in path[1:])

p_bfs = walk(bfs(START), GOAL)
g, prev, order = dijkstra(START)
p_dij = walk(prev, GOAL)
print("BFS      ", len(p_bfs) - 1, "tiles, cost", cost_of(p_bfs))
print("Dijkstra ", len(p_dij) - 1, "tiles, cost", cost_of(p_dij))
print("goal expanded as number", order.index(GOAL) + 1, "of", len(order))
for y in range(len(MAP)):
    print(" ".join(f"{g.get((x, y), '#'):>2}" for x in range(len(MAP[0]))))
reach, _, _ = dijkstra(START, budget=4)
print("tiles within 4 MP, start included:", len(reach))
```

Output:

```
BFS       5 tiles, cost 11
Dijkstra  9 tiles, cost 9
goal expanded as number 29 of 29
 2  3  4  5  6  7
 1  3  5  7  7  8
 0  2  5  8  9  9
 1  3  #  7  7  8
 2  3  4  5  6  7
tiles within 4 MP, start included: 12
```

Read the grid of `g` values as a cost map. Check a few by hand.

- The tile above the start is open, `g = 1`. The corner above that, `g = 2`.
- The woods tile at column 1, row 1 costs 2 to enter. Its cheapest neighbour is the open tile to its left at 1, so `g = 1 + 2 = 3`.
- The goal is reached by the BFS route straight along the middle row at `2 + 3 + 3 + 2 + 1 = 11`, the fewest tiles. Dijkstra's route goes up to the top row, along it, and down, 9 tiles at 1 MP each, total 9. The bottom row gives another route that also costs 9. When two routes tie, the one you get depends on the order ties come off the heap, which is why a spec for an interactive or a test must state the tie-break.

| Question | BFS | Dijkstra |
|---|---|---|
| Tiles walked to the goal | 5 | 9 |
| MP spent | 11 | 9 |
| Turns needed with 3 MP per turn (ignoring turn-boundary rules) | 4 | 3 |

Now the number that sets up next week. The goal was the **29th of 29** tiles expanded. Dijkstra searched the whole map, including the far corners behind the start, before it could be sure of the goal. It spreads out in all directions in order of cost because it has no idea where the goal is. Week 4's A* adds that idea.

**Movement range is Dijkstra with a budget.** Stop relaxing any edge that would push the cost past the unit's MP, and the set of tiles that received a `g` is the set the unit can reach this turn. With 4 MP the unit reaches 12 tiles, counting the one it stands on. That blue-highlighted region every tactics game draws is this search.

### Move it yourself

Open [the interactive](../examples/w03-dijkstra-terrain.html). The left grid runs BFS and the right grid runs Dijkstra on the same map. Press Step and watch the order of expansion. BFS spreads as a diamond, one ring per step, and plows straight through the wooded hills. Dijkstra's frontier spreads by cost. It races along the open top and bottom rows and crawls into the expensive middle, so its "rings" bulge around the hills. Paint a tile to change its terrain and both searches rerun. Drag the MP budget slider to see the movement range grow in cost contours, not step contours.

### Cross-game recognition

**Civilization VI (2016, with Gathering Storm rules).** Terrain costs make the edges, roads change them per era (1, 0.75, 0.5 MP per tile), and units with promotions such as Ranger ignore woods penalties. That last rule means the cost function belongs to the *unit*, not only the map. Two units standing on the same tile can have different shortest paths to the same goal.

**Unity's navigation system (AI Navigation package 2.0).** Unity's documentation describes navigation **areas** with a cost per area type. An area with cost 3.0 is treated as three times longer to cross, so a path will detour around shallow water set to a high cost. Each agent also has an area mask, and the documentation's own example lets humans walk through doors while zombies cannot. Unity runs A*, next week's algorithm, over this weighted graph. The weights are the same idea as Civilization's terrain costs, applied to a 3D level.

**Brogue (Brian Walker, first released 2009), Dijkstra maps.** Walker's RogueBasin article describes running the search *backwards*, from the goals outward over the whole level, and storing the resulting cost at every cell. He sets every goal cell to zero and repeatedly lowers each floor cell to one more than its cheapest neighbour until nothing changes. The result is exactly the `g` grid you printed above, with the goal as the start. Any monster can then walk to the goal by stepping "downhill" to its cheapest neighbour, with no per-monster search at all. Walker lists several tricks built on it. Put every unexplored tile in the goal set and you get auto-explore. For fleeing monsters, take the map around the player, multiply every value by a negative number around −1.2 and rescan. Monsters rolling downhill on that map run for the exits instead of cowering in corners, and the size of the multiplier controls how close the player must get before a cornered monster tries to dash past.

One search, three presentations. A route preview asks for the cheapest path from one start. A navigation mesh asks the same question with per-area weights and per-agent masks. A Dijkstra map runs the search once from the goals and lets any number of agents read the answer.

### Eyes-open design judgment

- **Costs are a design document.** Every number in `COST` changes where NPCs go and how players plan. Decide what a cost of 1 means (one second, one MP) and write it down. If woods cost 2 but feel like 1.2 in play, the preview route will look silly to players.
- **Know when BFS is enough.** If all edges really do cost the same (a grid where every tile is identical, or a dialogue graph), BFS gives the same answer and is simpler and faster. Dijkstra earns its place only when costs differ.
- **One search from the goal can serve many NPCs.** If many agents want the same destination (all zombies want the player), a single Dijkstra map from the destination, as in Brogue, is cheaper than one search per agent. If every agent wants a different destination, it is not.
- **Dijkstra explores everything cheaper than the goal.** On a 29-tile map that is harmless. On a 1,000 × 1,000 MMO zone with a goal 200 m away, it means searching a disk of 200 m in every direction, including behind you. That cost is next week's problem.
- **The fastest path is not always the path a player expects.** An NPC who takes a long detour because it is 0.3 s faster can look lost. Sometimes a small bias toward straight routes, or a road preference, looks smarter than the true optimum. This is week 1's lesson again.

## 3. Where turn-based rules break the simple model

Our grid charged the cost of each tile entered and added them up. Civilization VI's real rules are not purely additive, and the differences are instructive.

- **MP are checked before entering.** The Civilization Wiki's movement page notes that in Civilization VI a unit needs the full cost available before it moves onto a tile. In Civilization V a unit could enter a hill with only a fraction of an MP left.
- **A unit with full MP can always move one tile.** A Warrior with 2 MP can enter a tile that would cost 6 (woods and hills across a river), because it has not moved yet. But the same page gives an example of a Courser, the game's early cavalry, with 4.75 MP left that cannot enter that tile, because it has already moved.

The consequence is that the cost of reaching a tile depends on **how many MP are left when you arrive there**, not only on the tiles you have crossed. Two routes that both cost 5 in our simple sum can take a different number of turns. The fix is to change the graph, not the algorithm. Make each node a pair (tile, MP left this turn) and let an edge that ends a turn reset MP. Dijkstra then runs unchanged on the bigger graph, with cost measured as (turns, MP spent). This is a general trick worth remembering. When the cost of a step depends on history, put the relevant history into the node.

**Complexity.** With a binary heap, each push and pop costs `O(log n)`. Every node is expanded once and every edge relaxed once, and lazy deletion can push each edge's target once, so Dijkstra costs `O((V + E) log V)`. For the 29-tile grid that is a few hundred operations. For an MMO zone of a million cells, searched once per NPC per repath, it is the reason weeks 4, 5 and 14 exist.

## In-class activity (25 minutes)

Pairs. Each pair gets a printed 7 × 7 tile map with open ground, woods, hills and one river line, a start, a goal and a unit with 5 MP.

1. **Costs (5 min).** Using the lecture's costs, add a river rule of your own: crossing the river costs 2 extra MP. Write the rule as an edge cost, and say which edges it applies to.
2. **Trace (12 min).** Run Dijkstra from the start by hand until the goal is expanded. Keep the open list in a column, crossing out entries as you expand them and marking stale entries when you skip them. Write `g` in every tile you reach.
3. **Range (5 min).** Shade the tiles reachable with 5 MP.
4. **Compare (3 min).** Count the tiles you expanded before the goal. Circle any expanded tile that is clearly on the wrong side of the start. Next week you will make A* skip them.

Expected output: the rule, a completed map with `g` values, the shaded range, and an expansion count with the wasted tiles circled.

## Common misconceptions

- **"Dijkstra finds the path with the fewest steps."** It finds the path with the lowest total cost. With equal costs that is also the fewest steps, which is why BFS is a special case.
- **"The first time Dijkstra reaches a node, that's its cost."** Only BFS works that way. In Dijkstra, reaching a node gives a candidate. The cost is final only when the node is expanded. The Crypt was reached at 19 and finalized at 10.
- **"A negative cost is a neat way to make a route attractive."** It breaks the proof that expanded costs are final, and Dijkstra can then return wrong answers. Use small positive costs, or lower the costs of the attractive route's tiles instead.
- **"Movement range needs a different algorithm."** It is the same search with a budget. Stop relaxing edges that exceed the budget, and the reached set is the range.

## Check yourself

1. Run Dijkstra from A on this undirected graph: A–B 1, A–C 4, B–C 2, B–D 5, C–D 1. Give `g` for every node, the path to D, and any stale entries you skip.
2. In the dungeon, the collapsed stair between Hall and Crypt is cleared and now takes 5 s instead of 15. What are the new `g` values for Crypt, Shrine and Vault, and the new path to the Crypt?
3. On the 6 × 5 terrain map, how many tiles (start included) can the unit reach with a 3 MP budget?
4. Run the section 2 code on this directed graph: A→B 2, A→C 3, C→B −2, B→D 1. What does it report for D, what is the true cheapest cost, and which step goes wrong?
5. On a grid where open tiles cost 1, a designer sets woods to 1.1 "so NPCs prefer open ground, but only slightly". Will an NPC ever walk an extra tile to avoid one woods tile? Another designer sets woods to 5. How many extra tiles will an NPC walk to avoid one woods tile now, and what might a player think?

<details>
<summary>Answers</summary>

1. Expand A (0), B (1), C (3, via B, better than 4), skip stale C at 4, expand D (4, via C, better than 6), skip stale D at 6. `g`: A 0, B 1, C 3, D 4. Path A → B → C → D.
2. Crypt `min(4 + 5, 4 + 2 + 4) = 9` via Hall directly. Shrine 11, Vault 12. Path Gate → Hall → Crypt.
3. 10 tiles, the ones with `g ≤ 3` in the printed grid (two in each row).
4. It expands A (0), then B at 2 and relaxes B→D, giving D 3. Then it expands C at 3 and finds B at `3 − 2 = 1`. It records `g(B) = 1` and pushes B, but B is already closed, so the new copy is skipped as stale and B's edges are never relaxed again. D stays at 3. The true cheapest cost is A→C→B→D, `3 − 2 + 1 = 2`. The step that goes wrong is closing B at 2. With a negative edge still unexplored, the cost of an expanded node is not final.
5. At 1.1, never. Crossing the woods tile costs 0.1 more than an open tile, and an extra tile costs at least 1, so a longer route always loses. The change only decides between routes of equal length, so it works as a tie-break. At 5, crossing the woods costs 4 more than an open tile, so the NPC will walk up to 3 extra open tiles to avoid it, and at exactly 4 extra tiles the two routes tie. If woods do not slow the player much, players will see NPCs skirting a single tree for no visible reason and read it as artificial stupidity. The cost table should match how the terrain feels in play.

</details>

## Lab / assignment hook

[Lab 03, terrain costs and movement range](../labs/lab03.md). Implement Dijkstra with a budget and a Brogue-style Dijkstra map on a tile grid loaded from a text file, so the provided tests pass. Then tune a cost table so an NPC's route matches a designer's intent on three maps. Deliverable: the passing code, the three route screenshots or text dumps, and a 300-word cost-table rationale.

## Sources

- Dijkstra, E. W. (1959). "A note on two problems in connexion with graphs." *Numerische Mathematik* 1, 269-271. The shortest-path algorithm.
- Civilization Wiki (Fandom), "Movement (Civ6)" and "Road (Civ6)", read September 2026 via the wiki's API. Civilization VI (2016) with Gathering Storm rules: flat tiles 1 MP; woods, rainforest, hills and marsh 2; hills with woods or rainforest 3; mountains impassable; MP checked before entering a tile (a change from Civilization V); a unit with full MP can always move one tile, with the Warrior and Courser examples; road costs by era (ancient 1 for most terrain, industrial 0.75, modern 0.5); Ranger promotion ignoring woods and rainforest penalties.
- Unity Technologies, AI Navigation package 2.0 manual, "Navigation Areas and Costs" (read September 2026). Area cost as a multiplier on traversal, the water example, the per-agent area mask and the humans-through-doors example, Unity's use of A*.
- Walker, B. "The Incredible Power of Dijkstra Maps." RogueBasin (read September 2026 via the wiki's API). Construction by repeated relaxation from goal cells; rolling downhill; safety maps by multiplying by about −1.2 and rescanning; auto-explore. RogueBasin's Brogue page lists Walker as the developer and November 27, 2009 as the release of version 1.0.
- Millington, I. (2019). *AI for Games*, 3rd ed. CRC Press. Chapter 4, the pathfinding graph and Dijkstra.
- The dungeon (extended from CS102 week 8), the 6 × 5 terrain map and the 7 × 7 activity map are invented for teaching.

## Interactive spec: examples/w03-dijkstra-terrain.html

**The one insight:** BFS expands in rings of steps and walks straight through expensive terrain; Dijkstra expands in rings of *cost*, bulges around the expensive tiles, and finds the cheaper, longer route. The student should see the two frontiers diverge on the same map, and notice that Dijkstra reached the goal last of all 29 tiles.

**Layout.** Two grids side by side at 1280 px ("BFS: fewest tiles" left, "Dijkstra: lowest cost" right), stacked at 390 px (BFS on top). Shared controls above, a readout strip under each grid, and a small legend of terrain costs.

- Each tile is a square with a terrain fill from the shared palette plus a one-letter label (`.`, `f`, `h`, `H`, `M`) so color is not the only cue. Start and goal get outlined badges "S" and "G".
- As a search runs, expanded tiles show their number in expansion order in a corner and their `g` (Dijkstra) or step count (BFS) in the center. Tiles currently on the open list get a dashed outline. The final path is drawn as a thick line through tile centers.
- Under each grid: "tiles walked", "cost (MP)", "tiles expanded before the goal", and for Dijkstra "stale entries skipped".
- A third toggleable overlay on the Dijkstra grid, "Movement range": tiles with `g ≤ budget` tinted, with the contour between reachable and unreachable drawn as a line.

**Controls (keyboard accessible, labelled):**

1. Step (both searches advance one expansion), Run to end, Reset, speed select for auto-play (1, 4, 16 expansions per second).
2. Terrain brush: a select with Open (1), Woods (2), Hills (2), Wooded hills (3), Mountain (impassable). Click or press Enter on a tile to paint it. Painting reruns both searches to completion immediately. Keyboard: arrow keys move a tile cursor in the focused grid, Enter paints.
3. "Move start" and "Move goal" buttons, then choose a tile.
4. MP budget slider, 0 to 15, step 1, default 4, with the reachable tile count printed ("12 tiles within 4 MP, start included").
5. Preset select: "Lecture map" (default) and "Open field" (all open, same size; there BFS and Dijkstra give paths of the same cost).
6. Restore preset.

**Algorithms (must match the lecture code).**

- Grid coordinates `(column, row)`, 6 columns by 5 rows for the lecture map. Neighbour order N, E, S, W. Entering a tile costs its terrain cost; mountains are not neighbours.
- BFS: FIFO queue, `prev` recorded on first discovery.
- Dijkstra: binary min-heap of `(cost, column, row)` so ties break by lower cost, then lower column, then lower row (this matches Python's comparison of `(cost, (x, y))` tuples). Lazy deletion: skip a popped tile already closed and count it as a stale entry. Update `g` and `prev` only on strictly lower cost. The search runs to exhaustion (no early exit), so "tiles expanded before the goal" is the goal's position in expansion order.
- Movement range: Dijkstra with the same rules, never pushing a tile whose new cost exceeds the budget.

**Lecture map.** Rows top to bottom: `......`, `.ffh..`, `.hHHf.`, `.fMf..`, `......`. Start `(0, 2)`, goal `(5, 2)`. Costs `.` 1, `f` 2, `h` 2, `H` 3, `M` impassable.

**Test values (must match).**

- BFS path: 5 tiles, cost 11, straight along row 2.
- Dijkstra path: 9 tiles, cost 9: `(0,2) (0,1) (0,0) (1,0) (2,0) (3,0) (4,0) (4,1) (5,1) (5,2)`.
- Dijkstra `g` grid, rows top to bottom: `2 3 4 5 6 7`; `1 3 5 7 7 8`; `0 2 5 8 9 9`; `1 3 # 7 7 8`; `2 3 4 5 6 7`.
- Goal expanded as number 29 of 29.
- Budget 4: 12 tiles. Budget 3: 10 tiles. Budget 0: 1 tile.
- Paint `(2, 2)` from `H` to `.`: both searches rerun at once. BFS: 5 tiles, cost 9. Dijkstra: 5 tiles, cost 9, straight along row 2 (a tie with the top and bottom routes, resolved by the heap order above).
- Open field preset: BFS and Dijkstra both report 5 tiles, cost 5.

**First screen.** Lecture map with both searches already run to the end, both paths drawn, readouts showing "5 tiles, 11 MP" and "9 tiles, 9 MP". Caption: "Same map. BFS counts tiles, Dijkstra counts cost. Press Reset, then Step."

**Accessibility.** All controls reachable by Tab with visible focus; the grids are focusable with an arrow-key cursor. A live region announces each step ("Dijkstra expands 1,0 at cost 3"). Respects `prefers-reduced-motion` (auto-play off, Step only) and `prefers-color-scheme`. Palette from `templates/interactive-tokens.css`. Terrain is drawn with flat fills and letters, no game art.
