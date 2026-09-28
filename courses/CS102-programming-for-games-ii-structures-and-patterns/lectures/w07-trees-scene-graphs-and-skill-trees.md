# CS102 · Week 07 — Trees: Scene Graphs and Skill Trees

**Why this matters:** Every scene you build in an engine is a tree, and so is almost every talent screen you have spent points in. When a sword floats a metre away from the hand holding it, or a refund leaves a player with a skill whose prerequisite is gone, the bug is a tree operation done wrong. This week you learn the handful of operations that trees support and write each one in a few lines of Python.

**You will be able to:**
- Compute the world position and angle of any node in a 2D scene graph from the local values on its path to the root.
- Write recursive pre-order and post-order walks, and choose the right one for drawing, transform updates, refunds and totals.
- Predict how many nodes a change touches (the subtree size) and explain why storing world positions directly breaks when a parent moves.
- Implement prerequisite checks, path costs and subtree refunds for a skill tree, and recognize when a "tree" in a game is really a graph.

**Before class:** Nystrom, *Game Programming Patterns* (2014), "Dirty Flag" chapter (the motivation and the first half of the pattern section, on local and world transforms). Godot Engine documentation (stable, 4.x), class reference for `Node2D`, the `position` and `global_position` properties. Reread your notes on tree order from CS101 week 7.

**Prerequisites from earlier courses:** [CS101 week 7, scenes, nodes and scripts](../../CS101-programming-for-games-i/lectures/w07-engine-intro-scenes-nodes-scripts.md) (the scene tree, pre-order "tree order", and why `_ready` runs children first). [CS101 week 4, functions and decomposition](../../CS101-programming-for-games-i/lectures/w04-functions-and-decomposition.md) (functions that call functions). [MA101 week 10, angles, radians, sin and cos](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w10-angles-radians-sin-cos.md) and [MA101 week 12, 2D vectors](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w12-2d-vectors.md) (rotating a point). From this course, [week 6 on stacks](w06-queues-and-stacks-undo-and-command-buffers.md), because recursion runs on the call stack.

**Interactive:** [Scene graph transforms](../examples/w07-scene-graph-transforms.html). Keep it open during section 2.

---

## 1. What a tree is, in code

A **tree** is a set of **nodes** joined by parent-child links, with two rules. Exactly one node, the **root**, has no parent. Every other node has exactly one parent. Follow parent links upward from any node and you always reach the root, and you never loop.

A few more words you will use all term:

- A node's **children** are the nodes whose parent it is. Nodes with no children are **leaves**.
- The **subtree** of a node is that node plus all its children, their children, and so on down. Every node is the root of its own subtree.
- The **depth** of a node is the number of links between it and the root. The root has depth 0.
- The **path to the root** is the chain of parents from a node up to the root.

In CS101 week 7 you met the Godot scene tree and learned that the engine visits it in "tree order": a node, then each of its children's subtrees in turn. That order has a name, **pre-order**, and you will write it yourself this week. You also saw that `_ready` runs the other way, children before parents. That is **post-order**. Both come from the same short recursive function.

Here is the smallest useful tree node in Python:

```python
class Node:
    def __init__(self, name):
        self.name = name
        self.parent = None
        self.children = []

    def add_child(self, child):
        child.parent = self
        self.children.append(child)
        return child
```

Two pointers per link: the child knows its parent, and the parent keeps a list of children. You could store only one direction. Keeping both costs a little memory and lets you walk up (for transforms and prerequisites) and down (for drawing and refunds) without searching.

### Recursion: a function that trusts itself

A **recursive** function calls itself on a smaller piece of the problem. Trees are made of smaller trees, so tree code is almost always recursive. Counting the nodes in a subtree is the classic first example:

```python
def subtree_size(node):
    return 1 + sum(subtree_size(c) for c in node.children)
```

Read it as a promise. "The size of my subtree is me, plus the sizes of my children's subtrees." A leaf has no children, so the `sum` is 0 and the answer is 1. That leaf case is the **base case**: the input small enough to answer without another call. Every recursive function needs one, or it calls itself until Python stops it.

Each call waits on the **call stack** (week 6) until its children's calls return. So the stack grows as deep as the tree. Python's default recursion limit is about 1,000 frames, and a scene tree 1,000 levels deep does not happen in practice. A linked chain of 5,000 dialogue lines or a corridor of 5,000 tiles might, and in week 8 you will use a loop and an explicit queue instead.

## 2. Worked example: move the parent, the children follow

### The hook

Build a tank in Godot from four nodes: `Tank`, a child `Turret`, its child `Barrel`, and the barrel's child `Muzzle` where the shot spawns. Drive the tank and the turret, barrel and muzzle come along. Rotate the turret and the barrel swings round, and the muzzle flash appears at the new barrel tip. You never wrote a line of code on the barrel telling it to follow.

Players see the same thing in every game with a character holding something. The sword stays in the hand through every animation frame. The trick is that the engine does not store where the barrel is in the world at all. It stores where the barrel is *relative to the turret*, and it works out the world position when it needs it. Godot's documentation says this directly: a `Node2D`'s `position` is relative to its parent, and a separate `global_position` gives the world value.

### The model

Each node stores a **local transform**. In 2D, without scaling, that is a position `(x, y)` and an angle `a` measured in the parent's frame. Its **world transform** is found by combining its parent's world transform with its own local one:

```
world_angle(n) = world_angle(parent) + a
world_pos(n)   = world_pos(parent) + R(world_angle(parent)) · (x, y)

R(t) · (x, y) = (x cos t − y sin t,  x sin t + y cos t)
```

- `a` is the node's local angle, in degrees, counter-clockwise.
- `(x, y)` is the node's local offset from its parent.
- `R(t)` rotates a vector by angle `t`, the rotation you met in MA101 week 10.
- For the root, which has no parent, world equals local.

Read the second line aloud. "Start where my parent is. Turn my offset by the way my parent is facing. Step along it." The parent's angle rotates the child's offset, and the child's own angle only matters to *its* children. That asymmetry is the whole design, and the most common source of bugs when students write it for the first time.

In code, the model is one recursive method:

```python
import math

class Node:
    def __init__(self, name, x=0.0, y=0.0, angle=0.0):
        self.name, self.x, self.y, self.angle = name, x, y, angle
        self.parent, self.children = None, []

    def add_child(self, child):
        child.parent = self
        self.children.append(child)
        return child

    def world(self):
        if self.parent is None:
            return self.x, self.y, self.angle
        px, py, pa = self.parent.world()
        t = math.radians(pa)
        wx = px + self.x * math.cos(t) - self.y * math.sin(t)
        wy = py + self.x * math.sin(t) + self.y * math.cos(t)
        return wx, wy, pa + self.angle

tank   = Node("Tank", 100, 100, 0)
turret = tank.add_child(Node("Turret", 10, 0, 0))
barrel = turret.add_child(Node("Barrel", 30, 0, 0))
muzzle = barrel.add_child(Node("Muzzle", 20, 0, 0))

turret.angle = 30
print([round(v, 1) for v in muzzle.world()])   # [153.3, 125.0, 30]
```

The base case is the root. Every other call asks its parent first, so the recursion climbs to the root and the answers flow back down the path.

### Numbers you can check

Use the tank above. The tank sits at `(100, 100)`. The turret is 10 units forward of the tank's centre, the barrel's pivot is 30 units along the turret, and the muzzle is 20 units along the barrel. All local angles start at 0.

| Tank angle | Turret angle | Turret world | Barrel world | Muzzle world | Muzzle world angle |
|---|---|---|---|---|---|
| 0° | 0° | (110, 100) | (140, 100) | (160, 100) | 0° |
| 0° | 30° | (110, 100) | (136.0, 115.0) | (153.3, 125.0) | 30° |
| 0° | 90° | (110, 100) | (110, 130) | (110, 150) | 90° |
| 90° | 0° | (100, 110) | (100, 140) | (100, 160) | 90° |
| 90° | 30° | (100, 110) | (85.0, 136.0) | (75.0, 153.3) | 120° |

Check row 2 by hand. The turret's world position does not change when *its own* angle changes, because its offset is turned by the tank's angle (0°). The barrel starts at the turret, `(110, 100)`, and steps 30 units at 30°. That step is `(30 cos 30°, 30 sin 30°) = (25.98, 15)`, landing at `(135.98, 115)`. The muzzle steps another 20 units at 30°, `(17.32, 10)`, to `(153.3, 125.0)`.

Row 5 is the one that makes the model click. The tank turned 90°, so every offset below it turned 90°. The turret added 30° more, so the barrel and muzzle point at 120°. You changed two numbers, and three world positions moved.

### A visual you can move

Open the interactive. The left panel is the tree: `Tank` with children `Turret`, `TrackL` and `TrackR`, and the chain `Turret → Barrel → Muzzle`. The right panel is the world, with the tank drawn as simple shapes. Drag the turret-angle slider. Three nodes in the tree light up, the turret's subtree, and three shapes move in the world. Drag the tank-angle slider and all six light up.

Now switch the storage mode to **"World positions stored directly."** In this mode each part keeps its world position as a plain number, the way you might first write it without a tree. Rotate the turret. The turret turns, and the barrel stays exactly where it was, hanging in the air at `(140, 100)`. To fix it you would have to find everything attached to the turret and move each piece yourself. Finding "everything attached" *is* walking the subtree. The tree was always there. The direct storage just hid it and made you do the walk by hand.

The counter under the world view shows "nodes recomputed: k of 6". It always equals the subtree size of the node you changed. That number is the cost of a change, and it is why engines spend effort on it (section 3).

### Cross-game recognition

- **Godot (4.x).** `Node2D.position` is local, `global_position` is world. The class reference tells you to use a `Node2D` as a parent to move, rotate and scale its children together. Drawing follows the tree too. Canvas items are drawn in tree order, and by default children are drawn on top of their parents. That is a pre-order walk deciding what covers what.
- **Unity (Unity 6).** The `Transform` component has `localPosition`, relative to the parent, and `position`, in world space. Its documentation describes parenting as applying position, rotation and scale hierarchically, and every object in a scene has a Transform. Different names, same model.
- **Skeletal animation.** A character's skeleton is a tree of bones, each with a local rotation. Rotate the upper arm and the forearm, hand and anything the hand holds all swing with it. The sword in the hand is a child of the hand bone.
- **Skill trees.** In section 4 you will refund a skill and have to unlearn everything that depended on it. That is the same "operation on a node applies to its subtree" rule, applied to points instead of positions.

One idea runs through all four. **A change to a node's local value affects exactly its subtree, and nothing outside it.**

### Eyes-open design judgment

Parenting is powerful and easy to overuse. Decide deliberately.

- **Parent when the child should inherit motion.** A turret on a tank, a hat on a head, a health bar that must never lag behind its enemy (CS101 week 7 showed parenting as one of three fixes for that lag).
- **Do not parent when the child should be free.** A fired bullet must not be a child of the barrel, or it will swing round when the turret turns. Spawn it at the muzzle's *world* position, then add it to the level, not the tank. Many first-year projects have homing bullets for exactly this reason.
- **Deep trees cost more.** The naive `world()` above walks to the root every time, so asking for every node's world transform costs the sum of all depths. A single pre-order pass that hands each child its parent's result costs one step per node (see section 3).
- **Reparenting changes meaning.** Moving a node to a new parent while keeping its local values makes it jump in the world. Engines offer "keep global transform" options for this, and you should know which one your tool uses.

### Check yourself (worked example)

1. The tank is at `(0, 0)` facing 180°. The turret is at local `(10, 0)` with angle 0°. Where is the turret in the world?
2. With the tank from the table at 0° and the turret at 90°, you change the barrel's local angle to 45°. Which world positions change: turret, barrel, muzzle?
3. A game stores world positions directly for a 12-part robot. The torso rotates. How many positions must the code update, and how does the code know which ones?

<details>
<summary>Answers</summary>

1. `R(180°) · (10, 0) = (−10, 0)`, so the turret is at `(−10, 0)`.
2. Only the muzzle. The barrel's own angle rotates its children's offsets, not its own position. The barrel stays at `(110, 130)`. The muzzle moves from `(110, 150)` to `(110 + 20 cos 135°, 130 + 20 sin 135°) = (95.9, 144.1)`.
3. Every part in the torso's subtree. The code knows which ones only by having the parent-child links, that is, by having a tree. Without them it cannot answer the question at all.

</details>

## 3. Walking a tree: pre-order, post-order, level order

A **traversal** visits every node once. Three orders cover almost everything games need.

```python
def preorder(node):
    out = [node.name]              # visit me first
    for c in node.children:
        out += preorder(c)
    return out

def postorder(node):
    out = []
    for c in node.children:
        out += postorder(c)
    return out + [node.name]       # visit me last
```

The only difference is where the visit happens: before the children or after them. For the tank tree (`Tank` with children `Turret`, `TrackL`, `TrackR`, and `Turret → Barrel → Muzzle`):

| Order | Sequence | Use it when |
|---|---|---|
| Pre-order | Tank, Turret, Barrel, Muzzle, TrackL, TrackR | The parent's result is needed first: world transforms, drawing parents under children, Godot's `_process` and `_enter_tree` |
| Post-order | Muzzle, Barrel, Turret, TrackL, TrackR, Tank | The children's results are needed first: totals, bounding boxes, refunds, Godot's `_ready` |
| Level order | Tank, Turret, TrackL, TrackR, Barrel, Muzzle | You want everything at depth 1 before depth 2: "nearest first" searches, which week 8 builds on |

Level order uses a queue instead of recursion. You will write it next week under its general name, breadth-first search.

### One pass for all world transforms

The recursive `world()` climbs to the root every time it is called. Call it on every node of a 1,000-node tree whose average depth is 8, and you do about 8,000 steps. A pre-order pass does the same job in 1,000 steps, because each node receives its parent's world transform instead of recomputing it:

```python
def update_world(node, parent_world=(0.0, 0.0, 0.0)):
    px, py, pa = parent_world
    t = math.radians(pa)
    node.wx = px + node.x * math.cos(t) - node.y * math.sin(t)
    node.wy = py + node.x * math.sin(t) + node.y * math.cos(t)
    node.wa = pa + node.angle
    for c in node.children:
        update_world(c, (node.wx, node.wy, node.wa))
```

Engines go one step further. They mark a node **dirty** when its local transform changes, and only recompute world transforms in dirty subtrees, only when someone asks. That is Nystrom's Dirty Flag pattern, and his motivating example is exactly this one: a ship, a crow's nest on the ship, a pirate in the nest and a parrot on the pirate. If nothing in the turret's subtree moved this frame, nothing there gets recomputed.

### Aggregates are post-order

Anything that summarizes a subtree needs the children's answers first. The total weight of everything a character carries in nested bags, the bounding box of a character and its attachments, the number of enemies left in a spawner's subtree. Each is `combine(my value, children's answers)`, which is `subtree_size` with a different `combine`.

## 4. Skill trees: the same operations, different payload

A skill tree stores skills instead of transforms. The parent is the **prerequisite**, the skill you must learn first. The same four operations appear, under new names.

```python
class Skill:
    def __init__(self, name, cost):
        self.name, self.cost, self.learned = name, cost, False
        self.parent, self.children = None, []

    def add_child(self, child):
        child.parent = self
        self.children.append(child)
        return child

def can_learn(skill):                       # look at one parent
    return not skill.learned and (skill.parent is None or skill.parent.learned)

def path_cost(skill):                       # walk up to the root
    return skill.cost + (path_cost(skill.parent) if skill.parent else 0)

def refund(skill):                          # post-order over the subtree
    points = sum(refund(c) for c in skill.children)
    if skill.learned:
        skill.learned = False
        points += skill.cost
    return points
```

Take an invented frost tree. `Frost Bolt` (1 point) is the root. Its children are `Ice Lance` (1) and `Frost Nova` (1). `Ice Lance` leads to `Shatter` (2) and `Frost Nova` leads to `Deep Freeze` (3).

| Skill | Depth | `path_cost` | Subtree size |
|---|---|---|---|
| Frost Bolt | 0 | 1 | 5 |
| Ice Lance | 1 | 2 | 2 |
| Shatter | 2 | 4 | 1 |
| Frost Nova | 1 | 2 | 2 |
| Deep Freeze | 2 | 5 | 1 |

Suppose a player has learned Frost Bolt, Ice Lance, Shatter and Frost Nova, 5 points in all. Refunding Ice Lance returns 3 points (Ice Lance and Shatter) and leaves the rest. If `refund` only unlearned the node itself, the player would keep Shatter with no Ice Lance under it, an illegal state that a later save-load or balance patch will trip over. The subtree rule prevents that by construction.

### When the "tree" is not a tree

Game menus call many things trees that are not. Look at the rule that unlocks a node and you can tell which structure you actually have.

- **Diablo II (original and Lord of Destruction).** The Sorceress's cold skills form a chain from Ice Bolt (required level 1) to Ice Blast (6) to Glacial Spike (18). Blizzard (24) lists *two* required skills, Glacial Spike and Frost Nova (6). Frozen Orb (30) requires Blizzard. A node with two parents breaks the tree rule. The structure is a **directed acyclic graph**: links have a direction and never loop, but a node may have several parents. `can_learn` must check all parents, and `path_cost` must collect the *set* of ancestors so a shared ancestor is not counted twice. To learn Frozen Orb from nothing you need six skills: Frozen Orb, Blizzard, Glacial Spike, Ice Blast, Ice Bolt and Frost Nova.
- **World of Warcraft (classic talent trees, before Mists of Pandaria).** Each class had three talent trees. Deeper tiers opened only after you had spent enough points in that tree, and some talents also required a specific earlier talent. The tier rule looks at a total over the whole tree, a post-order sum, not at one parent.
- **Path of Exile (version 3.x).** The passive skill "tree" is one large network shared by every class, with each class starting at a different spot. You may allocate any node connected to a node you already have. Paths loop and rejoin. That is a general graph, and the question "how many points to reach that notable?" is a shortest-path question, which is next week's topic.

So before you write the data structure, write down the unlock rule. One prerequisite per node gives you a tree and the code above. Several prerequisites give you a DAG. Adjacency to anything owned gives you a graph.

## In-class activity (25 minutes)

Work in pairs with the lab 07 starter file open.

1. **Draw first (8 min).** Sketch the scene tree for a mounted knight: horse, rider, rider's arm, lance, shield, banner on the lance. Give each node a local offset and angle of your choice. Mark which subtree moves when the rider turns in the saddle.
2. **Predict (7 min).** Using your numbers, compute by hand the world position of the banner tip when the horse faces 0° and the rider turns 90°. Write it down before running anything.
3. **Run (10 min).** Build your knight with the `Node` class from section 2 and print `world()` for the banner. If your hand answer and the program disagree, find which rule in the model you applied differently. The most common one is rotating a node's offset by its *own* angle instead of its parent's.

Expected output: a tree diagram, one hand-computed position, one program output that matches it, and one sentence naming the mistake you caught (or confirming none).

## Common misconceptions

- **"A node's angle rotates its own position."** It rotates its children's offsets. A node's own position is set by its parent's world angle. Row 2 of the table shows the turret staying put while its own angle changes.
- **"Storing world positions is simpler and faster."** It is simpler until something moves. Then you must find and update every attached part yourself, which is the tree walk done by hand and easy to get wrong.
- **"Pre-order and post-order are interchangeable."** Transforms and drawing need the parent first. Totals and refunds need the children first. Use the wrong one and you read stale or missing values.
- **"If the menu calls it a skill tree, it is a tree."** Check the unlock rule. Diablo II's Blizzard has two prerequisites and Path of Exile's passive tree loops, so neither is a tree in the data-structure sense.

## Check yourself

1. A tree has a root with 3 children, and each child has 4 children. How many nodes are there, how deep is the deepest node, and how many nodes does rotating one depth-1 node touch?
2. Write, in one line of Python, a recursive function `depth(node)` that returns the number of links from `node` to the root.
3. The skill tree from section 4 has everything learned. A designer wants refunds to return only 50% of points, rounded down per skill. How many points does refunding Frost Nova return?
4. In the tank table, the tank faces 90° and the turret 90°. Compute the muzzle's world position and angle.
5. A crafting menu says "Steel Ingot requires Iron Ore and Coal." Is a recipe list with rules like this a tree, a DAG or a general graph? What changes in `path_cost`?

<details>
<summary>Answers</summary>

1. `1 + 3 + 12 = 16` nodes. The deepest nodes have depth 2. A depth-1 node's subtree is itself plus 4 children, so 5 nodes.
2. `def depth(node): return 0 if node.parent is None else 1 + depth(node.parent)`
3. Frost Nova (1 point) rounds down to 0 and Deep Freeze (3 points) rounds down to 1, so 1 point. Rounding per skill loses more than rounding the total (which would give 2). That is a design choice you must write in the spec.
4. The turret is at `(100, 110)` with world angle 180°. The barrel steps 30 units at 180° to `(70, 110)`. The muzzle steps 20 more to `(50, 110)`, world angle 180°.
5. A DAG. Steel Ingot has two parents, and recipes do not loop. `path_cost` must gather the set of all ancestors (and, for crafting, count quantities along each path), not follow one parent pointer.

</details>

## Lab / assignment hook

[Lab 07, scene graph and skill tree](../labs/lab07.md). Implement world transforms, both traversals, subtree size, `can_learn`, `path_cost` and `refund` in the starter file, then extend the skill tree to allow several prerequisites. Deliverable: the completed Python file passing all tests, plus a 200-word note on the DAG extension.

## Sources

- Godot Engine documentation, class reference `Node2D` (stable, Godot 4.7, accessed September 2026). `position` is relative to the parent; `global_position` is the world value; use `Node2D` as a parent to move, scale and rotate children.
- Godot Engine documentation, class reference `CanvasItem` (stable, 4.7). Canvas items are drawn in tree order; by default children are on top of their parents.
- Godot Engine documentation, class reference `Node` (stable, 4.7). `_enter_tree` parent before child; `_ready` in reverse order, children first.
- Unity Scripting API, `Transform` (Unity 6.6, accessed September 2026). Parenting applies position, rotation and scale hierarchically; `localPosition` is relative to the parent, `position` is world space; every object in a scene has a Transform.
- Nystrom, R. (2014). *Game Programming Patterns*, "Dirty Flag" chapter (gameprogrammingpatterns.com). Scene graphs, local and world transforms, and the ship, crow's nest, pirate and parrot example, paraphrased.
- The Amazon Basin wiki, Diablo II skill pages "Ice Bolt", "Ice Blast", "Glacial Spike", "Frost Nova", "Blizzard" and "Frozen Orb" (Diablo II and Lord of Destruction, accessed September 2026). Required levels 1, 6, 18, 6, 24 and 30; Blizzard requires Frost Nova and Glacial Spike; Frozen Orb requires Blizzard. The same values appear in the game's own `skills.txt` (`reqlevel`, `reqskill1`, `reqskill2`), as published for Diablo II: Resurrected by blizzhackers/d2data, `json/skills.json` (May 2026).
- Warcraft Wiki, "Talent" (history section on classic talent trees, accessed September 2026). Three trees per class; deeper tiers opened by points spent in that tree; some talents required earlier talents; the system was simplified from Wrath of the Lich King on and replaced in Mists of Pandaria.
- Path of Exile Wiki, "Passive skill" (Path of Exile 1, version 3.x, accessed September 2026). One network shared by all classes with different starting points; a point can be allocated to a node connected to an allocated node.
- The tank, knight and frost-tree numbers are invented for teaching.

## Interactive spec: examples/w07-scene-graph-transforms.html

**The one insight:** changing one node's local value moves exactly its subtree, and storing world positions directly breaks the moment a parent moves. The visible proof is the barrel left hanging in the air in "direct" mode, next to a counter that always equals the subtree size.

**Layout.** Two linked views, side by side at 1280 px, stacked at 390 px (world view on top).

- **Left, "Tree":** a node-link diagram of six nodes. `Tank` at the top; children `Turret`, `TrackL`, `TrackR`; `Turret → Barrel → Muzzle` below. Each node box shows its name and local values `(x, y, a°)`. When a control changes a node, highlight that node and its whole subtree for 600 ms (skip the fade under `prefers-reduced-motion`, just show the highlight state until the next change).
- **Right, "World":** a 400 × 300 world-unit canvas with a light grid every 20 units, origin top-left, y pointing down on screen but labelled so that positive angles turn counter-clockwise in the maths (flip y when drawing). Draw the tank body as a 40 × 24 rectangle centred at the tank's world position and rotated by its world angle, tracks as two 44 × 6 rectangles at local `(0, ±12)`, the turret as a circle of radius 8, the barrel as a line from the barrel's world position to the muzzle's world position, and the muzzle as a small dot. Label the muzzle dot with its world coordinates to one decimal.
- **Readouts (copyable text, below the world view):** a table with one row per node: name, local `(x, y, a)`, world `(x, y, a)` to one decimal. Under it, "nodes recomputed: k of 6".

**Controls (all keyboard accessible, labelled):**

1. Tank x: slider 40 to 360, step 1, default 100.
2. Tank y: slider 40 to 260, step 1, default 100.
3. Tank angle: slider −180 to 180, step 1, default 0.
4. Turret angle: slider −180 to 180, step 1, default 0.
5. Barrel angle: slider −90 to 90, step 1, default 0.
6. Barrel length (the muzzle's local x): slider 5 to 40, step 1, default 20.
7. Storage mode toggle: "Local transforms (tree)" (default) or "World positions stored directly".
8. Reset button.

**Formulas.** For each node in pre-order: `world_angle = parent_world_angle + a`; `world_x = parent_x + x cos(parent_world_angle) − y sin(parent_world_angle)`; `world_y = parent_y + x sin(parent_world_angle) + y cos(parent_world_angle)`; angles in degrees converted to radians. Root world = local. Local values: Tank `(tank x, tank y, tank angle)`, Turret `(10, 0, turret angle)`, Barrel `(30, 0, barrel angle)`, Muzzle `(barrel length, 0, 0)`, TrackL `(0, 12, 0)`, TrackR `(0, −12, 0)`.

**"Nodes recomputed" rule.** Tank x, y or angle: 6. Turret angle: 3. Barrel angle or length: 2 (Barrel's angle moves only Muzzle's world position, but count the subtree of the changed node, which is Barrel and Muzzle). Show the name of the changed node beside the count.

**Direct mode.** On entering direct mode, freeze every node's current world transform as stored values. From then on each slider changes only the stored world values of the node it names (Tank sliders move only the tank body, turret angle rotates only the turret circle's stored angle, barrel controls change only the barrel line). Children do not follow. Show a warning chip, "Barrel and Muzzle did not move: nothing told them to", whenever a stored child is more than 1 unit from where the tree would put it. Switching back to tree mode recomputes from local values and clears the chip. "Nodes recomputed" reads "1 of 6 (you must move the others yourself)" in this mode.

**Test values (must match exactly to one decimal).** Defaults: Turret `(110.0, 100.0, 0)`, Barrel `(140.0, 100.0, 0)`, Muzzle `(160.0, 100.0, 0)`. Turret angle 30: Barrel `(136.0, 115.0, 30)`, Muzzle `(153.3, 125.0, 30)`. Turret angle 90: Barrel `(110.0, 130.0, 90)`, Muzzle `(110.0, 150.0, 90)`. Tank angle 90, turret 0: Turret `(100.0, 110.0, 90)`, Muzzle `(100.0, 160.0, 90)`. Tank angle 90, turret 30: Barrel `(85.0, 136.0, 120)`, Muzzle `(75.0, 153.3, 120)`. Turret 90, barrel 45: Muzzle `(95.9, 144.1, 135)`.

**First screen.** Load with turret angle 30 so the barrel is visibly rotated and the table already shows the non-trivial row. A one-line caption above the views: "Turn the turret. Count what moves. Then switch to direct storage and try again."
