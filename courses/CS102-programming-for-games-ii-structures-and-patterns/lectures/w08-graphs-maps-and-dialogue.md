# CS102 · Week 08 — Graphs: Maps and Dialogue

**Why this matters:** A dungeon map, a conversation, a quest chain and a passive skill web are all the same structure: things joined by links. Once you store them as a graph, one short search answers the questions designers and QA ask every day. How far is the vault? Can the player ever reach this line of dialogue? Is there a conversation branch with no way out? This week you write that search and use it as a bug finder.

**You will be able to:**
- Represent a map or a dialogue as an adjacency list in Python and compute its size in nodes and edges.
- Trace breadth-first search by hand, queue state included, and compute shortest move counts and paths.
- Build a linter that reports unreachable nodes, dead ends and broken links in a dialogue graph.
- Choose between an adjacency list and an adjacency matrix by access pattern, and state what a static reachability check cannot see.

**Before class:** Python documentation, `collections.deque` (the queue you will use). Play 15 minutes of Open Adventure, the open-source port of Colossal Cave Adventure, and draw the first ten locations you visit as boxes with arrows. inkle, *Writing with Ink* (github.com/inkle/ink, Documentation/WritingWithInk.md), sections 3 "Knots" and 4 "Diverts".

**Prerequisites from earlier courses:** [CS102 week 7, trees](w07-trees-scene-graphs-and-skill-trees.md) (nodes, parents, traversal orders, and the skill "trees" that turned out to be graphs). [CS102 week 5, hash maps](w05-arrays-linked-lists-and-hash-maps.md) (why a dict lookup is fast). [CS102 week 4, Big-O](w04-big-o-intuition-for-game-developers.md) (reading `O(V + E)`). Queues from [CS102 week 6](w06-queues-and-stacks-undo-and-command-buffers.md). [GS101 week 5, text adventures and MUD1](../../GS101-history-and-critical-study-of-games/lectures/w05-text-adventures-and-mud1.md) (the history of Colossal Cave Adventure). [CS101 week 5, lists](../../CS101-programming-for-games-i/lectures/w05-arrays-and-lists-inventories.md) (why `pop(0)` on a list is slow).

**Interactive:** [BFS reachability](../examples/w08-bfs-reachability.html). Keep it open during section 3.

---

## 1. From trees to graphs

Last week a tree had one rule that made everything easy: every node except the root has exactly one parent. Drop that rule and you have a **graph**.

- A graph is a set of **nodes** (also called vertices) and a set of **edges**, each joining two nodes. We write `V` for the number of nodes and `E` for the number of edges.
- In an **undirected** graph an edge works both ways. A corridor between Hall and Armory lets you walk either direction.
- In a **directed** graph each edge has a direction, `A → B`. A dialogue choice takes you from one line to the next, never back along the same edge. A trapdoor drops you into a room you cannot climb out of. Most game graphs are directed, and an undirected corridor is stored as two directed edges.
- A **path** is a sequence of nodes where each consecutive pair is joined by an edge. Its **length** is its number of edges.
- A **cycle** is a path that returns to its start. Trees have none. Maps and conversations are full of them ("Never mind" goes back to the greeting).
- Node `B` is **reachable** from `A` if some path leads from `A` to `B`.
- A **weighted** graph gives each edge a cost, such as travel time. This week every edge costs 1 move or 1 choice. CS203 adds weights.

Every tree is a graph. The skill structures you met at the end of week 7 sit between the two. Diablo II's cold skills are a **directed acyclic graph (DAG)**, where edges have a direction and there are no cycles, but a node can have several parents. Path of Exile's passive web has cycles, so it is a general graph.

## 2. Storing a graph

There are three common layouts. Take a small invented dungeon of 7 rooms:

```
Gate --- Hall --- Armory --- Crypt --- Shrine
           \                  /          |
            +----- Well -----+           v  (a drop, one-way)
Gate <----------------------------------- Vault  (a door that opens only from inside)
```

**Edge list.** A plain list of pairs: `[("Gate", "Hall"), ("Hall", "Gate"), ...]`. Easy to write in a file and easy to load. Slow to answer "where can I go from Hall?", because you must scan every edge, `O(E)`.

**Adjacency matrix.** A `V × V` grid where cell `[a][b]` is 1 if there is an edge `a → b`. Checking one edge is a single lookup, `O(1)`. Listing Hall's neighbours means scanning a whole row, `O(V)`. It always uses `V²` cells, even when most are 0.

**Adjacency list.** For each node, the list of nodes its edges lead to. In Python, a dict of lists:

```python
MAP = {
    "Gate":   ["Hall"],
    "Hall":   ["Gate", "Armory", "Well"],
    "Armory": ["Hall", "Crypt"],
    "Well":   ["Hall", "Crypt"],
    "Crypt":  ["Armory", "Well", "Shrine"],
    "Shrine": ["Crypt", "Vault"],      # the drop into the vault is one-way
    "Vault":  ["Gate"],                # a door that opens only from inside
}
```

Finding a node's list is a dict lookup, which week 5 showed is fast on average. Listing its neighbours costs only as many steps as it has neighbours. Memory is `V + E`. This dungeon has `V = 7` and `E = 14` directed edges.

Pick by access pattern, the way you picked in week 5. Game maps and dialogues are **sparse**: each node links to a handful of others, however large the graph grows. The real Colossal Cave data shows how sparse. Open Adventure's data file (section 3) has 185 locations and 580 distinct directed links. A matrix would need `185² = 34,225` cells to store 580 ones, a fill rate under 2%. The adjacency list stores the 580 entries and nothing else. Use a matrix only when the graph is small and dense, or when "is there an edge from `a` to `b`?" is the question you ask millions of times.

## 3. Worked example: one search, two jobs

### The hook

In Colossal Cave Adventure, stand in the well house at the start of the game and type the magic word `PLUGH`. One command later you are deep in the cave at a room marked "Y2". Walk there instead and it takes seven moves: out of the building, to the grate, down through it, along the cobble crawl to the pit, into the Hall of Mists, through a jumble of rock, and finally Y2. Players remember the magic words because they shortcut a map everyone had to draw by hand.

The source of that "seven" is not a guide or a player count. It comes from running a search over the game's own map data. Here is the same search pointed at a conversation. A writer adds a secret discount line for guild members, forgets to link to it from anywhere, and ships a line that no player can ever see. The same search, run on the dialogue, finds it in a millisecond.

### The model

**Breadth-first search (BFS)** explores a graph outward from a start node in layers: first every node 1 edge away, then every node 2 edges away, and so on. It keeps three things.

- A **queue** of nodes waiting to be explored, first in, first out. Use `collections.deque`, whose `popleft()` is `O(1)`. A plain list's `pop(0)` shifts every element (CS101 week 5).
- `dist[n]`, the number of edges from the start to `n`. A node is "seen" once it has a `dist`.
- `prev[n]`, the node we reached `n` from. Following `prev` backwards from any node spells out a shortest path.

```python
from collections import deque

def bfs(graph, start):
    dist, prev = {start: 0}, {start: None}
    queue = deque([start])
    while queue:
        u = queue.popleft()
        for w in graph[u]:
            if w in graph and w not in dist:   # skip broken links and seen nodes
                dist[w] = dist[u] + 1
                prev[w] = u
                queue.append(w)
    return dist, prev

def path_to(prev, target):
    if target not in prev:
        return []                              # unreachable
    path = []
    while target is not None:
        path.append(target)
        target = prev[target]
    return path[::-1]
```

Why is the first `dist` a node gets also the shortest? Because the queue holds nodes in order of distance. Every node at distance 1 is dequeued before any node at distance 2, so the first time BFS touches a node it is through the fewest possible edges. Each node enters the queue once and each edge is looked at once, so BFS costs `O(V + E)`. For Colossal Cave that is about 185 + 580 steps, far less than a millisecond.

Once you have `dist`, the linter is three one-liners:

```python
unreachable  = [n for n in graph if n not in dist]
dead_ends    = [n for n in dist if not graph[n] and n not in endings]
broken_links = [(a, b) for a in graph for b in graph[a] if b not in graph]
```

That is the whole model. **Reachable means "BFS from the start gave it a distance." Everything BFS did not reach is content no player will see.**

### Numbers you can check

**Job 1, the map.** Run `bfs(MAP, "Gate")` on the dungeon from section 2. Here is every step, with the queue after each one:

| Step | Dequeue | Newly seen (dist) | Queue after |
|---|---|---|---|
| 1 | Gate | Hall (1) | Hall |
| 2 | Hall | Armory (2), Well (2) | Armory, Well |
| 3 | Armory | Crypt (3) | Well, Crypt |
| 4 | Well | none (Crypt already seen) | Crypt |
| 5 | Crypt | Shrine (4) | Shrine |
| 6 | Shrine | Vault (5) | Vault |
| 7 | Vault | none (Gate already seen) | empty |

Step 4 is the one to understand. Well also leads to Crypt, but Crypt already has distance 3 from the Armory route. Arriving through Well would also give 3, never less, so BFS ignores it. `path_to(prev, "Vault")` gives Gate, Hall, Armory, Crypt, Shrine, Vault: 5 moves.

Now run it from the Vault instead. The one-way door puts Gate at distance 1 and Shrine at 5. From Shrine to Gate takes 2 moves (drop into the vault, go through the door), but from Gate to Shrine takes 4. In a directed graph, distance is not symmetric. Players feel that as "the shortcut back to town".

**Job 2, the dialogue.** Here is a small invented blacksmith conversation, as an adjacency list. Each key is a line of dialogue, each list the lines its choices lead to. `leave` and `bye` are endings.

```python
DIALOGUE = {
    "greet":           ["ask_price", "ask_rumor", "leave"],
    "ask_price":       ["haggle", "buy", "greet"],
    "haggle":          ["buy", "leave"],
    "buy":             ["bye"],
    "ask_rumor":       ["rumor_detail"],
    "rumor_detail":    [],            # writer forgot the choices
    "secret_discount": ["buy"],       # writer forgot to link here
    "leave":           [],
    "bye":             [],
}
```

`bfs(DIALOGUE, "greet")` gives:

| Line | dist | prev | Lint result |
|---|---|---|---|
| greet | 0 | — | start |
| ask_price | 1 | greet | |
| ask_rumor | 1 | greet | |
| leave | 1 | greet | ending |
| haggle | 2 | ask_price | |
| buy | 2 | ask_price | |
| rumor_detail | 2 | ask_rumor | **dead end**: no choices, not an ending |
| bye | 3 | buy | ending |
| secret_discount | — | — | **unreachable** |

`V = 9`, `E = 11`. BFS reached 8 lines. The ninth, `secret_discount`, is written, voiced and localized, and nobody will ever hear it. `rumor_detail` is reachable, and a player who picks it is stuck with no way to leave the conversation. The shortest route to buying something is `greet → ask_price → buy → bye`, 3 choices.

The map and the dialogue used the same function without changing a character of it.

### A visual you can move

Open the interactive. It has two presets, "Dungeon" and "Blacksmith". The graph is drawn on the left, the BFS table on the right. Press **Step** to dequeue one node at a time. The current node is outlined, nodes still in the queue are shown in a strip along the bottom in queue order, and each node fills with a colour for its distance once seen. Press **Run** to finish.

Click any edge to delete it, or drag from one node to another to add an edge. The search reruns at once. In the dungeon, delete `Crypt → Shrine` and watch Shrine and Vault turn grey (unreachable). Add the magic edge `Gate → Shrine` and watch Vault's distance drop from 5 to 2, the PLUGH effect. In the blacksmith, add `ask_price → secret_discount` and the unreachable badge disappears. The insight to look for is that the lint results change *only* when an edge changes. The lines' text never matters to the search.

### Cross-game recognition

**Colossal Cave Adventure, Open Adventure 1.22 (July 2026) data, from Crowther and Woods's Adventure 2.5.** Open Adventure keeps the whole map in a data file, `adventure.yaml`. Each location has a list of travel rules, and a rule with a `goto` action is a directed edge. Parse the file and run BFS from the starting location, and you get these numbers (ignoring conditions such as the locked grate, which section 4 comes back to):

| Measure | Value |
|---|---|
| Locations `V` | 185 |
| Distinct directed `goto` links `E` | 580 |
| Links with no link back (one-way) | 75 |
| Reachable from the start by `goto` rules only | 172 |
| Reachable once the troll bridge is added | 182 |
| Moves, well house to Y2, with `PLUGH` / walking | 1 / 7 |

The magic word counts as one command even though the data routes it through an intermediate ">>Foof!<<" location that forwards you automatically. The script is below. It reuses the `bfs` function above, and you can run it after downloading `adventure.yaml` from the Open Adventure repository.

```python
import yaml
from collections import deque

class Loader(yaml.SafeLoader):
    pass
Loader.add_constructor("tag:yaml.org,2002:omap",
                       lambda l, n: l.construct_sequence(n, deep=True))

data = yaml.load(open("adventure.yaml"), Loader=Loader)
graph = {}
for entry in data["locations"]:
    (name, loc), = entry.items()
    graph[name] = sorted({rule["action"][1] for rule in loc.get("travel") or []
                          if rule["action"][0] == "goto"})

dist, prev = bfs(graph, "LOC_START")
print(len(graph), sum(map(len, graph.values())), len(dist))   # 185 580 172
print(sorted(set(graph) - set(dist)))
```

The 13 "unreachable" locations are the interesting part. Ten of them lie across the troll bridge. Crossing is not a `goto` rule. It is a `special` action handled in the C code, so a linter that reads only `goto` rules calls the far side of the chasm unreachable. That is a **false positive**, a reported problem that is not real. Add the bridge as an edge and 182 are reachable. Of the last three, two are the ends of the endgame repository, where the C code places the player directly when the cave closes. The third is a ledge that no travel rule points to at all. The lesson is not about 1970s code. Your graph is only as true as the edges you extract, and every edge that lives in code instead of data is invisible to your tools.

**ink (inkle's narrative scripting language).** An ink story is made of **knots**, named sections of content, joined by **diverts**, written `->`. That is a directed graph with knots as nodes. The ink compiler warns when it finds a "loose end", content where the flow runs out without a divert, a choice or `-> END`. That warning is our `dead_ends` check, built into the tool.

**Twine.** Twine's reference calls a story a set of **passages**, notes that some people call them nodes, and says every story has exactly one start passage. Passages are nodes, links are directed edges, and the start passage is where BFS begins.

**Path of Exile (version 3.x).** You may allocate any passive node connected to one you already own. The set of nodes you could take next is exactly the **frontier** of a BFS started from everything you own at once. "How many points to reach that keystone?" is `dist` from that multi-node start.

Four contexts, one structure, one function.

### Eyes-open design judgment

- **Use BFS when every edge costs the same.** Moves between rooms, choices in a conversation, points on a passive tree. When edges have different costs (a long corridor, a slow swamp), BFS gives the fewest edges, not the least time. Use Dijkstra's algorithm or A\*, which CS203 weeks 3 and 4 cover.
- **Static reachability is optimistic.** The search above ignores conditions. The grate needs keys. A dialogue option may need a quest flag or 5 charisma. A line can be reachable in the graph and unreachable in every real play-through. Checking conditions means searching over (node, game state) pairs, and the number of states grows with every flag you add. GD202 week 4 covers dialogue state flags. Most teams run the cheap static check on every commit and accept that it misses some cases.
- **Static reachability can also be pessimistic.** Edges hidden in code, like the troll bridge, make the linter report false alarms. Teams then learn to ignore the linter, and the next real unreachable line ships. Keep traversal rules in data wherever you can, or teach the linter about the special cases.
- **Dead ends and unreachable nodes are not always bugs.** Cut content is often left in the files on purpose. A dialogue can end on a line by design if the engine closes the window. Give the linter an allow-list, and require a comment for every entry.
- **Choose the representation for the question.** An adjacency list for "where can I go from here?", which is what games ask. An adjacency matrix only for small, dense graphs where "is `a` next to `b`?" dominates.

### Check yourself (worked example)

1. In the dungeon, you delete `Hall → Armory` (one direction only). What is the new `dist` for Armory from Gate, and through which room?
2. A writer adds the choice `rumor_detail → greet` to the blacksmith dialogue. Which lint result changes?
3. A graph has 2,000 nodes and each node has on average 4 outgoing edges. Estimate the memory of an adjacency matrix and of an adjacency list, counted in stored entries.

<details>
<summary>Answers</summary>

1. Armory is now reached from Crypt: Gate (0), Hall (1), Well (2), Crypt (3), Armory (4). BFS finds the new shortest route with no change to the code.
2. `rumor_detail` is no longer a dead end. Nothing else changes: `secret_discount` is still unreachable.
3. Matrix: `2,000² = 4,000,000` cells. List: `2,000 + 8,000 = 10,000` entries. The list is 400 times smaller.

</details>

## 4. Depth-first search and cycles

BFS uses a queue. Swap it for a stack (`pop()` from the end instead of `popleft()`) and you get **depth-first search (DFS)**. DFS follows one path as deep as it can before backing up, the same order as week 7's pre-order walk. It reaches exactly the same set of nodes, so it works for reachability. It does not give shortest paths, because it may reach a node through a long route first.

DFS is the right tool for one job BFS does badly: **finding cycles**. A cycle in a conversation is normal. "Never mind" returns to the greeting. A cycle in a skill DAG or a quest-prerequisite graph is a bug. If quest A requires quest B and B requires A, neither can ever start. The standard check colours each node white (unvisited), grey (on the current path) or black (finished). Meeting a grey node means you have walked in a circle.

```python
def find_cycle(graph):
    WHITE, GREY, BLACK = 0, 1, 2
    colour = {n: WHITE for n in graph}

    def visit(n, path):
        colour[n] = GREY
        for w in graph[n]:
            if colour.get(w) == GREY:
                return path + [n, w]           # back to a node on this path
            if colour.get(w) == WHITE:
                found = visit(w, path + [n])
                if found:
                    return found
        colour[n] = BLACK
        return None

    for n in graph:
        if colour[n] == WHITE:
            found = visit(n, [])
            if found:
                return found
    return None

print(find_cycle({"A": ["B"], "B": ["C"], "C": ["A"]}))   # ['A', 'B', 'C', 'A']
```

Run `find_cycle` on the Diablo II cold skills from week 7 (Ice Bolt → Ice Blast → Glacial Spike → Blizzard → Frozen Orb, and Frost Nova → Blizzard) and it returns `None`. Add an accidental edge `Frozen Orb → Ice Bolt` and it reports the loop. A data-driven game (week 13) should run this check whenever designers edit prerequisite tables.

One warning. This `visit` is recursive, so a chain of thousands of nodes can hit Python's recursion limit of about 1,000. For big graphs, write DFS with an explicit stack, as you did for undo in week 6.

## In-class activity (25 minutes)

Groups of three. Each group gets a printed branching conversation of about 15 lines from a fictional quest giver, with choices marked as arrows. One member secretly adds two bugs before handing it to the next group: one unreachable line and one dead end.

1. **Adjacency list (8 min).** Write the conversation as a Python dict of lists.
2. **Trace by hand (10 min).** Run BFS from the first line on paper. Keep the queue in a column and cross nodes out as you dequeue them. Record `dist` for every line.
3. **Lint (5 min).** List the unreachable lines and the dead ends. Check your answer against the bug-planter's.
4. **Judge (2 min).** Name one line your static check would call reachable that a real player might never see, and say what condition would hide it.

Expected output: the dict, a completed BFS table, the two bugs found, and one sentence on a condition the check misses.

## Common misconceptions

- **"BFS and DFS find the same paths."** They reach the same *set* of nodes. Only BFS guarantees the path with the fewest edges.
- **"If the graph says it's reachable, players can reach it."** Static search ignores keys, flags and stats. It gives an upper bound on what players can see, and code-only edges like Colossal Cave's troll bridge can make it wrong in the other direction too.
- **"A dict of lists is just a messier matrix."** It stores only the edges that exist. For sparse game graphs it is tens to hundreds of times smaller, and listing a node's neighbours costs its number of neighbours instead of `V`.
- **"Distances are the same both ways."** Only in undirected graphs. One-way drops, doors and dialogue choices make `dist(A, B)` and `dist(B, A)` differ, as Gate and Shrine did.

## Check yourself

1. Write the adjacency list for a 4-room map where A connects both ways to B and C, B has a one-way drop to D, and D connects both ways to C. Give `V` and `E`.
2. Run BFS from D on your answer to question 1. Give `dist` for every room.
3. Why does BFS need `if w not in dist` before appending to the queue? What would happen in the dungeon without it?
4. A quest graph has 400 quests. Each lists on average 1.5 prerequisites. How many steps, roughly, does one BFS take, and how many would 400 separate "can I reach this quest?" searches take if you ran one per quest?
5. A linter reports `ending_good` as unreachable. Give two different causes, one in the data and one in how the graph was built.

<details>
<summary>Answers</summary>

1. `{"A": ["B", "C"], "B": ["A", "D"], "C": ["A", "D"], "D": ["C"]}`. `V = 4`, `E = 7`.
2. D (0), C (1), A (2), B (3).
3. Without it, nodes are queued again every time a new edge reaches them. On a graph with cycles (Hall ↔ Armory) the queue never empties and the program runs forever. With it, each node is queued once, which is what makes BFS `O(V + E)`.
4. One BFS is about `400 + 600 = 1,000` steps. One BFS from the start already answers "reachable?" for every quest, so 400 separate searches (about 400,000 steps) are wasted work.
5. In the data: no choice links to it, or a link to it has a typo in the target name (a broken link and an unreachable node at once). In the build: the edge exists only in code (a scripted jump, like the troll bridge) and the linter never saw it.

</details>

## Lab / assignment hook

[Lab 08, dialogue linter](../labs/lab08.md). Write `build_graph`, `bfs`, `path_to` and the three lint checks for a 12-line dialogue file with a planted typo, then point the linter at a dialogue you wrote yourself. Stretch: find reachable lines from which no ending can be reached. Deliverable: the completed Python file passing all tests, the lint report for your own dialogue, and a short note on one false positive or false negative.

## Sources

- Raymond, E. S. et al., Open Adventure, `adventure.yaml`, `main.c` and `NEWS.adoc` (gitlab.com/esr/open-adventure, release 1.22, July 2026; a forward port of Crowther and Woods's Adventure 2.5). The travel-rule format (goto, speak, special; conditions such as carry and with); the `PLUGH` rule from the building; the troll bridge as `special` action 3; the repository ends placed by code at closing time. All counts in the section 3 table were computed by the script in the lecture from this file (September 2026).
- Wikipedia, "Colossal Cave Adventure" (accessed September 2026), via GS101 week 5. Background on Crowther and Woods, the 1977 expansion and the about-140-location original.
- inkle, *Writing with Ink* (github.com/inkle/ink, Documentation/WritingWithInk.md, accessed September 2026). Knots, diverts with `->`, `-> END`, and the compiler's loose-end warning, paraphrased.
- Twine Reference, "Basic Concepts: Stories and Passages" (twinery.org/reference, Twine 2, accessed September 2026). Stories are made of passages, sometimes called nodes; every story has one start passage.
- Path of Exile Wiki, "Passive skill" (Path of Exile 1, version 3.x, accessed September 2026). Allocation to nodes connected to an allocated node; one network shared by all classes.
- The Amazon Basin wiki, Diablo II skill pages (Diablo II and Lord of Destruction), as cited in week 7. Cold-skill prerequisites.
- Python documentation, `collections.deque` (Python 3). `O(1)` appends and pops at either end.
- The dungeon, blacksmith and quest-graph examples are invented for teaching.

## Interactive spec: examples/w08-bfs-reachability.html

**The one insight:** one unchanged BFS function finds shortest routes on a map and unreachable or dead-end lines in a dialogue, and its answers change only when an edge changes. Seeing the grey "unreachable" nodes appear the instant you delete one edge is the moment the idea lands.

**Layout.** Two linked views, side by side at 1280 px, stacked at 390 px (graph on top).

- **Left, "Graph":** nodes as labelled rounded boxes at fixed preset positions, directed edges as arrows. An edge that exists in both directions is drawn as one line with two arrowheads. Before a search, nodes are neutral. After, each seen node is filled by distance using a sequential ramp from the shared palette (distance 0 darkest), unreachable nodes are grey with a dashed border and an "unreachable" badge, and dead ends (reachable, no outgoing edges, not an ending) get a warning-colour badge "dead end". Endings in the dialogue preset have a double border.
- **Right, "BFS table":** columns Node, dist, prev, Lint. Rows appear in the order nodes are first seen, then unreachable nodes at the bottom. Above the table, the current queue as a horizontal strip of chips, front on the left. Below, a readout: `V`, `E`, reachable count, and "shortest path to <selected node>: a → b → c (n edges)".

**Presets.**

1. **Dungeon** (start Gate). Nodes and edges exactly as `MAP` in section 2: Gate→Hall; Hall→Gate, Armory, Well; Armory→Hall, Crypt; Well→Hall, Crypt; Crypt→Armory, Well, Shrine; Shrine→Crypt, Vault; Vault→Gate. No endings.
2. **Blacksmith** (start greet). Nodes and edges exactly as `DIALOGUE` in section 3. Endings: leave, bye.

**Controls (keyboard accessible, labelled):**

1. Preset selector (Dungeon / Blacksmith).
2. Start node selector (defaults to the preset's start).
3. Step button (dequeues one node, updates the queue strip, table and colours), Run button (finishes), Reset button (clears the search, keeps edits).
4. Edit edges. Click or press Enter on an edge to delete it. To add, select a source node, then a target node (by click or by keyboard via two dropdowns "From" and "To" plus an Add button). Any edit reruns the search to completion immediately.
5. "Restore preset" button.
6. Target selector for the shortest-path readout; the path's edges are drawn thicker.

**Algorithm.** Standard BFS with a FIFO queue, iterating each node's outgoing edges in the order listed in the preset (new edges appended at the end). A target not in the node set is ignored (the dialogue preset has none by default). Distances are edge counts.

**Test values (must match).**

- Dungeon from Gate: Gate 0, Hall 1, Armory 2, Well 2, Crypt 3, Shrine 4, Vault 5. Step-by-step queue after each dequeue: [Hall], [Armory, Well], [Well, Crypt], [Crypt], [Shrine], [Vault], []. Path to Vault: Gate → Hall → Armory → Crypt → Shrine → Vault.
- Dungeon from Vault: Vault 0, Gate 1, Hall 2, Armory 3, Well 3, Crypt 4, Shrine 5.
- Dungeon, delete Crypt→Shrine: Shrine and Vault unreachable. Restore, add Gate→Shrine: Shrine 1, Vault 2.
- Blacksmith from greet: greet 0, ask_price 1, ask_rumor 1, leave 1, haggle 2, buy 2, rumor_detail 2, bye 3; secret_discount unreachable; rumor_detail dead end; `V = 9`, `E = 11`; reachable 8.
- Blacksmith, add ask_price→secret_discount: secret_discount 2, no unreachable nodes. Add rumor_detail→greet: no dead ends.

**First screen.** Dungeon preset with the search already run to completion, Vault selected as target so the 5-edge path is highlighted. Caption above the views: "Delete one edge. Watch what becomes unreachable."
