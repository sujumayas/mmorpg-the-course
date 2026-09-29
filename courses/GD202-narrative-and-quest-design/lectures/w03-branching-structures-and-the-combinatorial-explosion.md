# GD202 · Week 03 — Branching Structures and the Combinatorial Explosion

**Why this matters:** Every writer who starts a branching story has the same plan. A choice here leads to three outcomes, each with its own choices. By the fifth layer the plan needs more words than a novel, and each player reads less than 2% of them. This week you learn to count that cost before you write it, and to use the structures shipped games use to keep choices without paying for every branch.

**You will be able to:**
- Compute the nodes, endings, distinct paths and share of content seen for a pure branching tree with `b` options and depth `d`.
- Derive how folding branches back together every `k` choices changes those numbers, and explain why paths stay at `b^d` while content shrinks.
- Classify a shipped game's structure with Ashwell's pattern names (time cave, gauntlet, branch and bottleneck, sorting hat and others) and predict its cost profile.
- Design a branching plan for a quest that fits a word budget and still offers the player a stated number of distinct paths.

**Before class:** Sam Kabo Ashwell, "Standard Patterns in Choice-Based Games" (blog post, 26 January 2015, free online, about 20 minutes). inkle, *Writing with Ink* (github.com/inkle/ink, `Documentation/WritingWithInk.md`), the Part One sections on choices, weave and gathers. Bateman (ed.), *Game Writing*, 2nd ed. (2021), the chapter on nonlinear structure (the course reader lists the pages).

**Prerequisites from earlier courses:** [GD202 week 2, the player as co-author](w02-the-player-as-co-author.md) (acknowledgement versus branching for a single choice; this week handles many choices at once). [CS102 week 7, trees](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w07-trees-scene-graphs-and-skill-trees.md) and [CS102 week 8, graphs, maps and dialogue](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w08-graphs-maps-and-dialogue.md) (nodes, edges, reachability, dialogue as a graph). [MA101 week 4, exponentials](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w04-exponentials-and-the-xp-curve.md) (why `b^d` outruns any budget). [GD101 week 9, choice and meaningful decisions](../../GD101-introduction-to-game-design/lectures/w09-choice-and-meaningful-decisions.md) (game trees, from the player's side).

**Interactive:** [`examples/w03-branch-explosion.html`](../examples/w03-branch-explosion.html), the course's signature example. Keep it open during section 2.

---

## 1. Stories as graphs

Last week you honored one choice. This week there are many, and you need a way to draw them.

A branching story is a **graph**. Each **node** is a unit of content: a scene, a passage, a block of dialogue. Each **edge** is a way to move from one node to the next, usually a player choice. You met graphs in CS102 week 8. Here we care less about searching them and more about counting them, because every node is something a writer must write, a voice actor must record and a tester must reach.

Four counts describe any branching structure:

- **Nodes**: how many units of content exist. This is the cost.
- **Endings**: nodes with no way forward.
- **Paths**: distinct routes from the start to an ending. This is what the player experiences as "different playthroughs."
- **Nodes seen**: how many nodes one playthrough visits. This is what a single player gets.

The ratio of the last to the first is the **share seen**, the fraction of your writing one player reads. You met this idea in week 2 for a single choice. This week it becomes the number that decides whether a structure is affordable.

Two shapes matter most.

A **tree** never rejoins. Every node has exactly one way in. Each path ends at its own ending, so paths equal endings.

A **folded** structure (formally, a directed acyclic graph) lets branches rejoin at a shared node. Many paths can pass through the same node. Designers call the shared node a **bottleneck**, a **gather** (ink's word), or a **fold-back** point.

## 2. Worked example: the branch explosion calculator

### The hook

The Cave of Time (Edward Packard, Bantam Books, 1979) was the first book in Bantam's Choose Your Own Adventure series. The format is simple. After a few pages, you face two or three options, each sending you to a different page, until you reach one of many endings. Early titles in the series had as many as 44 endings. Later ones had as few as 7.

That drop is the whole lesson of this week in one fact. Why would a series famous for endings cut them by more than 80%? And why do so few modern games branch the way that first book did?

For a modern contrast, take The Witcher 2: Assassins of Kings (CD Projekt Red, 2011). At the end of its first chapter, the player chooses to side with one of two leaders, and that choice sets the path of the entire second chapter. Every player who finishes the game has skipped one of two versions of a whole chapter that the studio wrote, voiced and tested. That is one binary choice. Imagine five of them in a row.

### The model

Start with a **pure tree**. Every choice offers `b` options, and every path passes through `d` choices before it ends.

```
nodes    N_tree = 1 + b + b² + ... + b^d = (b^(d+1) − 1) / (b − 1)
endings  E      = b^d
paths    P      = b^d
seen     V      = d + 1
share seen      = V / N_tree
```

- `b` is the branching factor, the number of options at each choice.
- `d` is the depth, the number of choices on one path.
- `N_tree` counts every node, level by level: 1 start node, `b` after the first choice, `b²` after the second, and so on.
- `V` counts the nodes one player visits: the start plus one node per choice.

Now add **fold-back**. After every `k` choices, all the branches rejoin at one bottleneck node, and a new tree starts from there. Each segment of `k` choices adds `b + b² + ... + b^k` nodes, plus one bottleneck. The final segment ends in its leaves (the endings) instead of a bottleneck.

```
grow(k) = b + b² + ... + b^k
with d = m·k (m segments of k choices):
nodes    N_fold = 1 + (m − 1)·(grow(k) + 1) + grow(k)
endings  E      = b^k
paths    P      = b^d          (unchanged!)
seen     V      = d + (m − 1) + 1 = d + d/k
```

When `k = d` there is one segment, no bottleneck, and the formula gives back the pure tree. When `k = 1` every choice rejoins immediately. That is the **branch and bottleneck** shape, with `N = 1 + d·(b + 1) − 1 = d·(b + 1)` nodes. (If `k` does not divide `d`, the last segment is shorter. The code below handles that.)

The line to stare at is **paths**. Folding does not reduce the number of distinct routes through the story. With `b = 3` and `d = 5`, the player still makes five three-way choices, and there are still `3^5 = 243` different sequences of choices. What folding removes is the content that only one of those 243 sequences would ever see.

### Numbers you can check

Pure trees with three options per choice:

| Depth `d` | Nodes | Endings | Nodes seen | Share seen |
|---|---|---|---|---|
| 1 | 4 | 3 | 2 | 50.0% |
| 2 | 13 | 9 | 3 | 23.1% |
| 3 | 40 | 27 | 4 | 10.0% |
| 5 | 364 | 243 | 6 | 1.6% |
| 10 | 88,573 | 59,049 | 11 | 0.01% |

Check `d = 2` by hand: 1 start node, 3 after the first choice, 9 after the second, total 13. One player sees the start, one of the 3, and one of the 9: 3 nodes. `3/13 = 23.1%`.

At `d = 5`, with 300 words per node (a short scene), the tree needs `364 × 300 = 109,200` words. That is longer than many novels. One player reads `6 × 300 = 1,800` words of it.

Now hold `b = 3` and `d = 5` fixed and fold back every `k` choices:

| Fold every `k` | Nodes | Endings | Paths | Nodes seen | Share seen |
|---|---|---|---|---|---|
| 5 (pure tree) | 364 | 243 | 243 | 6 | 1.6% |
| 4 | 125 | 3 | 243 | 7 | 5.6% |
| 3 | 53 | 9 | 243 | 7 | 13.2% |
| 2 | 30 | 3 | 243 | 8 | 26.7% |
| 1 (branch and bottleneck) | 20 | 3 | 243 | 10 | 50.0% |

Check `k = 1` by hand. Start node: 1. Each of the first four choices adds 3 option nodes and 1 bottleneck, so `4 × 4 = 16`. The fifth choice adds 3 option nodes that are the endings. Total `1 + 16 + 3 = 20`. One player sees the start, then an option and a bottleneck four times, then one ending: `1 + 8 + 1 = 10`.

The paths column never moves. The nodes column falls from 364 to 20, an 18-fold cut. At 300 words per node the branch-and-bottleneck version is 6,000 words, which is one writer's week, not one writer's year.

This code reproduces both tables. It runs as shown with `.venv/bin/python`.

```python
def structure(b, d, k):
    """Nodes, endings, paths and nodes seen per playthrough.
    b options per choice, d choices per path, fold back every k choices."""
    segs, left = [], d
    while left > 0:
        segs.append(min(k, left))
        left -= segs[-1]
    grow = lambda s: sum(b ** i for i in range(1, s + 1))   # nodes in one segment
    nodes = 1 + sum(grow(s) + 1 for s in segs[:-1]) + grow(segs[-1])
    seen = 1 + sum(s + 1 for s in segs[:-1]) + segs[-1]
    return nodes, b ** segs[-1], b ** d, seen

print("pure tree, b = 3")
for d in [1, 2, 3, 5, 10]:
    nodes, ends, paths, seen = structure(3, d, d)
    print(f"d={d:2}  nodes={nodes:6,}  endings={ends:6,}  seen={seen:2}  share={seen/nodes:.2%}")

print("b = 3, d = 5, fold every k choices")
for k in [5, 4, 3, 2, 1]:
    nodes, ends, paths, seen = structure(3, 5, k)
    print(f"k={k}  nodes={nodes:3}  endings={ends:3}  paths={paths}  seen={seen:2}  share={seen/nodes:.1%}")
```

Output:

```
pure tree, b = 3
d= 1  nodes=     4  endings=     3  seen= 2  share=50.00%
d= 2  nodes=    13  endings=     9  seen= 3  share=23.08%
d= 3  nodes=    40  endings=    27  seen= 4  share=10.00%
d= 5  nodes=   364  endings=   243  seen= 6  share=1.65%
d=10  nodes=88,573  endings=59,049  seen=11  share=0.01%
b = 3, d = 5, fold every k choices
k=5  nodes=364  endings=243  paths=243  seen= 6  share=1.6%
k=4  nodes=125  endings=  3  paths=243  seen= 7  share=5.6%
k=3  nodes= 53  endings=  9  paths=243  seen= 7  share=13.2%
k=2  nodes= 30  endings=  3  paths=243  seen= 8  share=26.7%
k=1  nodes= 20  endings=  3  paths=243  seen=10  share=50.0%
```

### A visual you can move

Open [the branch explosion calculator](../examples/w03-branch-explosion.html). The left view draws the structure itself, node by node, for your chosen `b`, `d` and `k`. The right view plots two lines against depth on a logarithmic axis: nodes you must write, and paths the player can take.

Start with the pure tree (`k = d`) and drag the depth slider from 1 to 6. The drawing turns into a fan too dense to read, and on the right the two lines climb together. Now drag `k` down to 1. The drawing collapses into a braid of small diamonds. On the right, the paths line does not move at all, and the nodes line drops flat and becomes a straight, slowly rising line. The gap between the two lines is what folding buys you: choices the player makes, without content only one player will see.

Then press "Highlight one playthrough." One path lights up. In the pure tree it is a thin thread through a huge fan. In the folded version it touches half the nodes on screen.

### Cross-game recognition

The same trade shows up in every medium that branches. Rewrite each case as `b`, `d` and `k` and it becomes the same calculation.

**Choose Your Own Adventure books (Bantam, 1979 onward).** Two or three options per choice and many endings: a pure tree, or close to one, which Ashwell's catalog names the **time cave** after The Cave of Time. A paper book has a fixed number of pages, so a high ending count forces each path to be short. That is the tree formula working as a budget. With a fixed number of nodes `N`, more endings means smaller `d`. The later titles in the series, with fewer endings, could afford longer paths.

**The Witcher 2: Assassins of Kings (CD Projekt Red, 2011).** One binary choice at the end of chapter 1 sets which version of chapter 2 the player sees, and later content brings the paths back together. In the model this is `b = 2` with nodes the size of a whole chapter and a fold after one choice. The share seen for chapter 2 is 50%, the same as a single branch and bottleneck step, but each node is many hours long. The studio paid for a whole chapter most players never see, and in return got a choice that players talk about for years. Ashwell would call this shape a **sorting hat**: early choices decide which long, mostly linear branch you get.

**Telltale's The Walking Dead (2012).** Each episode includes several points where the player chooses between two options, and the story keeps rejoining shared events. You saw in week 2 that Shawn is always bitten whatever the player tries. That is branch and bottleneck (`b = 2`, `k = 1`) at the level of the plot, with week 2's acknowledgement lines carrying the memory of each choice past the bottleneck.

**ink (inkle's scripting language).** ink builds the bottleneck into its syntax. In ink's "weave" style, options split the flow and a **gather**, a line starting with `-`, brings every option back to one point. The documentation's own summary is that options separate the paths of the story and gathers bring them back together. A writer using ink gets `k = 1` by default and has to do extra work to avoid folding. That is a tool encoding a design lesson.

Four media, one formula. Paper, a big-budget RPG, an episodic adventure and a scripting language all push toward folding, because `b^d` beats every budget.

### Eyes-open design judgment

Folding is not free, and a pure tree is not always wrong.

- **Folding costs memory, or it costs meaning.** After a bottleneck, the story forgets which branch the player took unless you store it. Without state, 243 paths collapse into 3 experiences and players feel their choices were cosmetic. With state, you pay week 2's acknowledgement costs at every later read. Week 4 builds the system that makes this manageable.
- **Paths are not experiences.** The model counts `3^5 = 243` paths in the branch-and-bottleneck structure, but two paths that differ only in the tone of one line are not different playthroughs to a player. Count only choices that players would describe differently when retelling.
- **Pure trees are right for short, replayable content.** A three-minute branching conversation that players replay to see other outcomes can afford a tree with `d = 2` or `d = 3`. At `d = 3` and `b = 3`, you write 40 nodes and each playthrough sees 10% of them, which is fine if replaying is the point.
- **Branch late, fold early.** A single unmerged branch after node `s` of an `N`-node chain costs `(b − 1)·(N − s)` extra nodes. An early branch doubles everything after it. Put expensive divergence near endings, where there is little left to duplicate, and fold early splits back fast.
- **Big branches need big signals.** If you do spend a Witcher-2-sized branch, tell players they are at a fork. An unsignaled branch that big means half your players never learn the other chapter exists, and the choice cannot feel meaningful if the player cannot see it was one.
- **Testing follows paths, not nodes.** Folding shrinks content, but a tester who wants to cover every path of `b = 3, d = 5` still faces 243 routes, plus every combination of stored flags. Week 14 on narrative testing deals with this.

### Check the model

1. A pure tree with `b = 2` and `d = 4`. Compute nodes, endings and share seen.
2. A branch-and-bottleneck structure (`k = 1`) with `b = 4` and `d = 6`. Compute nodes, paths and nodes seen.

<details>
<summary>Answers</summary>

1. Nodes `1 + 2 + 4 + 8 + 16 = 31`. Endings `2^4 = 16`. Seen `5`. Share `5/31 = 16.1%`.
2. Five full segments of `4 + 1 = 5` nodes, plus the start, plus 4 final endings: `1 + 25 + 4 = 30`. Paths `4^6 = 4,096`. Seen `1 + 5 × 2 + 1 = 12`.

</details>

## 3. A catalog of structures

The fold parameter `k` is one dial. Shipped games combine several, and the field has names for the common combinations. Sam Kabo Ashwell's 2015 catalog is the standard reference. Here are its main patterns, each paraphrased and placed in this lecture's terms.

| Pattern (Ashwell 2015) | Shape in brief | In our terms | Cost profile |
|---|---|---|---|
| Time cave | Heavy branching, many endings, little or no rejoining | Pure tree, `k = d` | Nodes grow as `b^d`; short paths |
| Gauntlet | A mostly linear central thread; side branches end fast in failure or rejoin quickly | Chain with short dead-end branches | Cheap; choices feel risky but rarely change the story |
| Branch and bottleneck | Branches that regularly rejoin at shared events, with state tracking what differed | `k = 1` or small `k`, plus flags | Linear in `d`; needs state to feel different |
| Quest | Clusters of content organized by place, many routes, few endings | Folded graph shaped like a map | Moderate; suits a consistent world |
| Open map | Stable locations the player can move between freely | Graph with cycles (not a tree) | Cheap per node; weak narrative drive |
| Sorting hat | Early choices decide which long linear branch the player gets | One early branch with huge nodes | High, but predictable |
| Floating modules | Encounters that appear when state conditions are met, with no central trunk | No fixed graph; rules pick content | Scales with content count, not paths |
| Loop and grow | A repeating cycle where state unlocks new options each time around | A cycle plus flags | Reuses nodes; needs careful state design |

Three observations about this table.

First, only the time cave has exponential cost. Every other pattern is a strategy for escaping it. That is the most useful fact in the catalog.

Second, the right-hand patterns (floating modules, loop and grow) stop being graphs you can draw and become rules that pick content from state. That is the direction dialogue systems take in week 4, and it is how online RPGs handle the millions of combinations of quests players have done.

Third, Outer Wilds, from week 1, is loop and grow in its purest form. The world resets every 22 minutes, and what grows is the player's knowledge. The "state" lives partly in the ship's log and partly in the player's head.

## 4. Budgeting a branching quest

Here is the procedure to use before writing a branching quest. It turns the model into a plan.

1. **Fix the budget.** Words, voice lines or scenes. Say 6,000 words.
2. **Fix the node size.** How long is one unit of content? Say 300 words. So you can afford 20 nodes.
3. **Fix what players will describe as different.** How many choices would a player mention when retelling? Say 4 choices with 3 options each (`b = 3`, `d = 4`).
4. **Compute the pure tree.** `1 + 3 + 9 + 27 + 81 = 121` nodes. Six times over budget.
5. **Fold until it fits.** With `k = 1`: `4 × 4 = 16` nodes (three bottlenecks plus the start give `1 + 3 × 4 + 3 = 16`). Fits, with 4 nodes left for acknowledgements.
6. **Spend the slack on memory.** Use the 4 spare nodes (1,200 words) for week 2's acknowledgement lines and one heavy payoff. Each choice gets read at least once after its bottleneck.
7. **Place any real branch late.** If one choice must diverge fully, make it the last one, where the extra cost is only the ending nodes.

Run step 5 with `k = 2` instead and you get `1 + (12 + 1) + 12 = 26` nodes, 30% over budget. A plan like this lets you tell a producer exactly what a design change costs before anyone writes a line.

### A note on online games

Everything above assumes one player owns the story. In an online RPG, several players share the same world, and a branch that changes the world (a town burned, a leader killed) cannot be true for one player and false for the one standing next to them. MMOs therefore branch less, fold faster and move most branch state into things only the choosing player sees. Week 13 covers the techniques. For now, add one question to your budget procedure. If this branch changes the world, whose world does it change?

## In-class activity (25 minutes)

Work in groups of three. Materials: the calculator, paper, a word budget card from the instructor (either 4,500, 6,000 or 9,000 words).

1. **(5 min)** Choose a quest premise in one sentence. Decide how many choices a player would mention when retelling it (`d`) and how many options each has (`b`).
2. **(5 min)** Compute the pure tree at 300 words per node. How many times over your budget is it?
3. **(8 min)** In the calculator, find the largest `k` that fits your budget. Then draw the structure on paper, labelling each bottleneck with the event every path shares there.
4. **(5 min)** For each bottleneck, write one flag it must remember and one line that reads it afterwards.
5. **(2 min)** Name the pattern from Ashwell's catalog that your structure most resembles.

Expected output: `b`, `d`, the pure-tree cost, the chosen `k` with its node count, a drawn structure with labelled bottlenecks, and a flag list.

## Common misconceptions

- **"Folding back means fewer choices."** Folding leaves the number of paths at `b^d`. It removes content that only one path would see, not the choices themselves.
- **"More endings means more replay value."** Endings are cheap to count and expensive to write. Players value endings they can tell apart and that respond to what they did. Three endings that each reflect choices across the game often beat 243 that differ by a line.
- **"The explosion is a problem for big games only."** At `b = 3`, depth 5 already needs 364 nodes. A student project with a single five-choice conversation hits the wall.
- **"A branch and bottleneck game has fake choices."** Only if nothing survives the bottleneck. With flags and acknowledgement lines, choices carry past each fold. Without them, players will call the choices fake, and they will be right.

## Check yourself

1. A writer plans a pure tree with `b = 2` and `d = 8`. How many nodes, and what share of them does one player see?
2. A pure tree with `b = 3`, `d = 5` has 364 nodes. If you add one more level of depth, how many nodes do you add? How does that compare to adding one more choice to a `k = 1` structure with the same `b`?
3. A designer has a 40-node budget and wants every player to make 6 binary choices (`b = 2`, `d = 6`). Which values of `k` fit? Show the node counts.
4. In Ashwell's catalog, which pattern matches "the player picks one of three companions at the start, and the rest of the game is a linear story shaped by that companion"? Explain in the model's terms.

<details>
<summary>Answers</summary>

1. Nodes `2^9 − 1 = 511`. Seen `9`. Share `9/511 = 1.8%`.
2. The new level adds `3^6 = 729` nodes, bringing the tree to 1,093. In a `k = 1` structure, one more choice adds `b + 1 = 4` nodes (3 options plus the bottleneck that replaces the old endings' role). Exponential versus linear.
3. Use `N = 1 + (m − 1)(grow(k) + 1) + grow(k)` with `b = 2`. `k = 1`: `grow = 2`, `m = 6`, `N = 1 + 5 × 3 + 2 = 18`. `k = 2`: `grow = 6`, `m = 3`, `N = 1 + 2 × 7 + 6 = 21`. `k = 3`: `grow = 14`, `m = 2`, `N = 1 + 15 + 14 = 30`. `k = 4` (segments 4 and 2): `1 + (30 + 1) + 6 = 38`. `k = 5` (segments 5 and 1): `1 + (62 + 1) + 2 = 66`. `k = 6`: `127`. So `k` from 1 to 4 fits the 40-node budget.
4. Sorting hat. One early choice with `b = 3` sends the player into one of three long linear branches. The share seen is about a third of the post-choice content, the same as a single fold step with `b = 3`, but each branch node is huge.

</details>

## Lab / assignment hook

[Lab 03, branch explosion analyzer](../labs/lab03.md). You will write the closed-form counts from this lecture, then a graph analyzer that counts reachable nodes, endings, distinct paths and the average path length of any dialogue graph, fast enough for billions of paths. You will run it on a sample graph and on your own quest plan. It feeds the final quest chain (60%), which must fit a stated word budget.

## Sources

- Wikipedia, "Choose Your Own Adventure" (accessed September 2026). The Cave of Time by Edward Packard, Bantam Books, 1979, the first book in the series; readers face two or three options after a few pages; endings range from as many as 44 in early titles to as few as 7 in later ones.
- Ashwell, S. K. (2015, 26 January). "Standard Patterns in Choice-Based Games." *These Heterogenous Tasks* (blog). Pattern names and descriptions (time cave, gauntlet, branch and bottleneck, quest, open map, sorting hat, floating modules, loop and grow), paraphrased; the time cave is named after The Cave of Time.
- Wikipedia, "The Witcher 2: Assassins of Kings" (accessed September 2026). CD Projekt Red, 2011; multiple paths and endings; at the end of chapter 1 the player chooses between assisting Iorveth or Roche, which sets the path of chapter 2.
- Wikipedia, "The Walking Dead (video game)" (accessed September 2026). Telltale Games, 2012; each episode includes several points where the player chooses between two options; Shawn Greene is always bitten.
- inkle, *Writing with Ink*, `Documentation/WritingWithInk.md` in github.com/inkle/ink (master branch, read September 2026). Weave, gathers marked with `-`, and the summary that options separate the story's paths and gathers bring them back together.
- Wikipedia, "Outer Wilds" (accessed September 2026). 22-minute loop; only the ship's log persists.
- Bateman, C. (ed.) (2021). *Game Writing: Narrative Skills for Videogames*, 2nd ed. Bloomsbury.

## Interactive spec: examples/w03-branch-explosion.html

**The one insight.** Folding branches back together leaves the number of distinct paths at `b^d` while the content you must write drops from exponential to linear. Two lines that start together on a log plot split apart as soon as `k` falls below `d`.

**Layout.** Two linked views, stacked on mobile (below 700px), side by side above. A readout strip under both.

- **View A, "The structure."** Draws the graph for the current `b`, `d`, `k` as a left-to-right layered diagram. Start node on the left; option nodes as small circles; bottleneck nodes as larger squares; endings as flagged circles. Draw every node when the node count is at most 400. Above 400 nodes, draw the first two levels of each segment exactly and replace deeper levels with a shaded wedge labelled with its node count ("+ 729 nodes"), so the layout never freezes. Button "Highlight one playthrough" picks a random path (seeded) and draws it in the accent color with its nodes filled; all other nodes dim.
- **View B, "Cost versus choice."** X-axis depth `d` from 1 to 10. Y-axis logarithmic, 1 to 10^6. Two series computed for the current `b` and `k`: "Nodes to write" and "Paths a player can take". A third dashed series "Nodes to write (pure tree)" for comparison. Vertical cursor at the current `d` with exact values for all three series. Shade the gap between the paths line and the nodes line.
- **Readout strip.** Nodes, endings, paths, nodes seen, share seen (percent, 2 decimals when under 2%, 1 decimal otherwise), and words to write at the current words-per-node, plus "one player reads" words.

**Controls.**
- Options per choice `b`: 2 to 5 (default 3).
- Depth `d`: 1 to 10 (default 5).
- Fold every `k` choices: 1 to `d` (default `d`, the pure tree, so the first screen shows the explosion; the slider's end is labelled "no fold").
- Words per node: a slider from 50 to 2,000, step 50 (default 300), plus a number field that accepts 50 to 50,000 so the Sorting hat preset's 20,000 fits.
- Preset buttons: "Time cave (b=3, d=5, k=5)", "Branch and bottleneck (b=3, d=5, k=1)", "Sorting hat (b=2, d=1, words per node 20,000)", "Budget quest (b=3, d=4, k=1)".
- All controls keyboard operable; every change redraws both views immediately (no animation if `prefers-reduced-motion`).

**Formulas.**
- Segments: split `d` into chunks of `k`, the last chunk `d − k·(ceil(d/k) − 1)`.
- `grow(s) = b + b² + ... + b^s`.
- Nodes `= 1 + Σ over all but the last segment of (grow(s) + 1) + grow(last)`.
- Endings `= b^last`. Paths `= b^d`. Seen `= 1 + Σ over all but the last segment of (s + 1) + last`.
- Share seen `= seen / nodes`. Words `= nodes × words per node`; one player reads `seen × words per node`.

**Test values (must match).**

| b | d | k | Nodes | Endings | Paths | Seen | Share |
|---|---|---|---|---|---|---|---|
| 3 | 5 | 5 | 364 | 243 | 243 | 6 | 1.65% |
| 3 | 5 | 4 | 125 | 3 | 243 | 7 | 5.6% |
| 3 | 5 | 3 | 53 | 9 | 243 | 7 | 13.2% |
| 3 | 5 | 2 | 30 | 3 | 243 | 8 | 26.7% |
| 3 | 5 | 1 | 20 | 3 | 243 | 10 | 50.0% |
| 3 | 10 | 10 | 88,573 | 59,049 | 59,049 | 11 | 0.01% |
| 2 | 4 | 4 | 31 | 16 | 16 | 5 | 16.1% |
| 4 | 6 | 1 | 30 | 4 | 4,096 | 12 | 40.0% |
| 2 | 6 | 4 | 38 | 4 | 64 | 8 | 21.1% |
| 3 | 4 | 1 | 16 | 3 | 81 | 8 | 50.0% |

At the default words per node (300), `b=3, d=5, k=5` must show 109,200 words to write and 1,800 read by one player.

**Accessibility and style.** Series differ by dash pattern and label as well as color. The structure drawing has a text summary for screen readers ("364 nodes, 243 endings; one playthrough visits 6"). Use `templates/interactive-tokens.css`. No game art; nodes are plain shapes.
