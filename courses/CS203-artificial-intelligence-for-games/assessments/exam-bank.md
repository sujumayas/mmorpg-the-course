# CS203 · Exam bank: quiz, practice and viva questions

CS203 has no written exam. The grade comes from the labs (50%, see [labs-brief.md](labs-brief.md)) and the final NPC ecosystem demo (50%, see [final-demo-brief.md](final-demo-brief.md)). This bank has three other jobs.

- **Practice.** Work a week's questions before its lab is due. If you can answer them with the lecture closed, the lab will go quickly.
- **Lab quizzes.** Each lab session from week 2 on opens with a 10-minute ungraded quiz of two or three questions from this bank. Usually one applies a lecture model to new numbers or traces code, and one asks you to explain or critique.
- **Viva.** The lab spot checks and the week 15 demo viva ask questions in this style, rewritten with the numbers from your own world and your own code.

Every question is tagged with the week or weeks it draws on and one type.

- **compute**: apply a lecture model (braking distance, `f = g + h`, switch points, break-even exposure, threat margin, frame budget) to values you have not seen before.
- **trace**: step an algorithm by hand and give its state after each step.
- **code**: say what a piece of Python prints, and why.
- **explain**: say why something behaves as it does, with a number or a trace as evidence.
- **design**: choose a technique or a value for a stated situation and justify it.
- **critique**: find what is wrong with a piece of code or a proposal and say how to fix it.

All numbers are invented unless a question names a game. Every game fact used here comes from the lecture of the tagged week, which cites its source and version. Every code snippet runs as shown with Python 3.13 (`.venv/bin/python`). A snippet whose first line says it uses a lecture's definitions runs when pasted below that lecture's code block. Every number in the answers was recomputed in Python from the lectures' own models. Write your own answer before you open the solution.

---

## Week 1: Game AI vs academic AI

1. *Week 1 · compute.* Pac-Man is at `(6, 9)` facing up. Blinky is at `(10, 5)`. Clyde's corner is `(0, 30)`.
   (a) Give Blinky's, Pinky's and Inky's chase targets, with the arcade's facing-up bug.
   (b) Is Clyde chasing or retreating when he stands at `(12, 3)`? At `(9, 4)`? Do not take a square root.
   (c) Turn Pac-Man to face down. Which targets change, and to what?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) Blinky `(6, 9)`, Pinky `(2, 5)`, Inky `(−2, 9)`. (b) Chasing at `(12, 3)`, retreating at `(9, 4)`. (c) Pinky becomes `(6, 13)` and Inky `(2, 17)`. Blinky and Clyde do not depend on facing.

(a) Blinky targets Pac-Man's tile. Facing up, "four ahead" is four up and four left because of the overflow bug, so Pinky targets `(6 − 4, 9 − 4) = (2, 5)`. Inky's offset tile is two up and two left, `(4, 7)`. Double the vector from Blinky to it: `2 × (4, 7) − (10, 5) = (−2, 9)`. A target outside the maze is fine. The turn rule only needs a point to measure distance to, as the scatter corners already show.

(b) At `(12, 3)`: `(6 − 12)² + (9 − 3)² = 36 + 36 = 72 ≥ 64`, so Clyde is at least 8 tiles away and chases `(6, 9)`. At `(9, 4)`: `9 + 25 = 34 < 64`, so he retreats to `(0, 30)`.

(c) Facing down, `f = (0, 1)` and there is no bug. Pinky: `(6, 9 + 4) = (6, 13)`. Inky's offset is `(6, 11)`, so his target is `2 × (6, 11) − (10, 5) = (2, 17)`.
</details>

2. *Week 1 · code.* This is the lecture's turn rule. What does each `print` show? What rule does the third call expose as missing?

```python
UP, LEFT, DOWN, RIGHT = (0, -1), (-1, 0), (0, 1), (1, 0)
ORDER = [UP, LEFT, DOWN, RIGHT]

def choose_direction(tile, heading, open_dirs, target):
    reverse = (-heading[0], -heading[1])
    best, best_d2 = None, None
    for d in ORDER:
        if d not in open_dirs or d == reverse:
            continue
        nx, ny = tile[0] + d[0], tile[1] + d[1]
        d2 = (nx - target[0]) ** 2 + (ny - target[1]) ** 2
        if best is None or d2 < best_d2:
            best, best_d2 = d, d2
    return best

print(choose_direction((8, 8), UP, {UP, LEFT, RIGHT}, (5, 5)))
print(choose_direction((8, 8), UP, {LEFT, DOWN, RIGHT}, (5, 5)))
print(choose_direction((8, 8), UP, {DOWN}, (5, 5)))
```

<details>
<summary>Answer and worked solution</summary>

**Answer.**

```
(0, -1)
(-1, 0)
None
```

First call. The ghost heads up, so down is the reverse and is skipped. Up leads to `(8, 7)`: `3² + 2² = 13`. Left leads to `(7, 8)`: `2² + 3² = 13`. Right leads to `(9, 8)`: `4² + 3² = 25`. Up and left tie at 13, and up comes first in the tie order, so up wins. The strict `<` in the code is what makes the tie order work. With `<=`, left would win.

Second call. Up is closed and down is the reverse. Left scores 13 and right 25, so left.

Third call. The only open exit is the reverse, so the loop skips everything and returns `None`. The lecture's function is the bare turn rule. The full ghost, as in Lab 01 and the interactive, reverses at a dead end. A caller that moved the ghost by `None` would crash, so the dead-end case has to be handled explicitly.
</details>

3. *Week 1 · compute.* Use the published schedules from the lecture (scatter first, then alternating).
   (a) How many seconds of scatter does the player get in the first 90 s of level 1? What share of the time is that?
   (b) The same for levels 2 to 4.
   (c) On level 5, what share of the first 30 s is scatter? Why is it higher than the level 5 share for the first 60 s in the lecture's table?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 24 s, 26.7%. (b) 19 s, 21.1%. (c) 10 s, 33.3%.

(a) Level 1 is scatter 7, chase 20, scatter 7, chase 20, scatter 5, chase 20, scatter 5. Scatter runs 0 to 7, 27 to 34, 54 to 59 and 79 to 84. All four fall inside 90 s: `7 + 7 + 5 + 5 = 24` s, and `24 / 90 = 26.7%`.

(b) Levels 2 to 4 have the same first five phases, but the third chase lasts 1,033 s. Scatter is 0 to 7, 27 to 34 and 54 to 59, so 19 s, and `19 / 90 = 21.1%`.

(c) Level 5 is scatter 5, chase 20, scatter 5, chase 20, scatter 5. The first 30 s hold scatter at 0 to 5 and 25 to 30, so 10 s, a third. The first 60 s add only one more 5 s scatter (50 to 55) against 20 more seconds of chase, so the share falls to 25%. The rest arrives early and in short pieces, and the longer the level runs, the less of it there is.
</details>

4. *Week 1 · compute.* An NPC thinks every frame at 60 Hz and reacts on the frame after it sees the player.
   (a) How long is that reaction, and how does it compare with the lecture's human reaction figures?
   (b) How many frames of deliberate delay bring it to about 0.2 s, and to about 0.4 s?
   (c) Another NPC thinks at 5 Hz with no deliberate delay. What range of reaction times does it show, and why might you still add a delay?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 16.7 ms, about 12 times faster than a simple human reaction. (b) 12 frames and 24 frames. (c) Between 0 and 200 ms, 100 ms on average.

(a) One frame is `1000 / 60 = 16.7` ms. Rabin gives about 0.2 s for a simple human reaction and 0.4 s when a mental comparison is needed. `200 / 16.7 = 12`, so the NPC reacts 12 times faster than a person can, which players feel as unfairness even if they cannot name it.

(b) `0.2 × 60 = 12` frames and `0.4 × 60 = 24` frames.

(c) At 5 Hz a think happens every 200 ms. A change that arrives just before a think is seen almost at once, and one that arrives just after waits almost 200 ms. The spread comes from timing, not from the design, so the NPC's reactions vary for no reason the player can see. A fixed delay on top (for example, act 0.2 s after the think that first saw the player) makes the reaction consistent, which is week 1's readable test.
</details>

## Week 2: Steering behaviors

5. *Week 2 · compute.* An ogre has `max_speed = 4` m/s and `max_accel = 3` m/s².
   (a) What is its braking distance `b`, and how far does seek overshoot a target?
   (b) Roughly how far does arrive overshoot with a slowing radius of 2 m?
   (c) What range of slowing radii gives a clean stop, and from what radius can it follow the ramp exactly?
   (d) Inside the ramp at `r = 2b`, what is the time constant of the exponential tail?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) `b = 2.67` m; seek overshoots by 2.67 m. (b) About 0.67 m. (c) From 2.67 m; exact ramp following from 5.33 m. (d) 1.33 s.

(a) `b = v² / (2a) = 16 / 6 = 2.67` m. Seek starts braking only after it passes the target, so it overshoots by `b`.

(b) `r < b`, so the overshoot is about `b − r = 0.67` m. A 60 Hz run of the lecture's 1D model with these values gives 0.67 m.

(c) No overshoot needs `r ≥ b = 2.67` m. Following the ramp from the moment it enters needs `max_speed² / r ≤ a`, so `r ≥ v² / a = 16 / 3 = 5.33` m, which is `2b`.

(d) Inside the ramp, speed is proportional to remaining distance, and the time constant is `r / max_speed = 5.33 / 4 = 1.33` s. The soldier's at `r = b` was 0.25 s. The ogre needs room to stop and a long, slow creep at the end, so a stopping distance matters even more for it.
</details>

6. *Week 2 · code.* A soldier runs east at full speed and its seek target is due north. What does this one frame of the vehicle model print? Roughly how long must a 90° turn take at this acceleration, at least?

```python
import math

DT = 1 / 60

def truncate(v, limit):
    n = math.hypot(*v)
    return v if n <= limit else (v[0] * limit / n, v[1] * limit / n)

def step(pos, vel, desired, max_speed, max_accel):
    dv = truncate((desired[0] - vel[0], desired[1] - vel[1]), max_accel * DT)
    vel = truncate((vel[0] + dv[0], vel[1] + dv[1]), max_speed)
    return (pos[0] + vel[0] * DT, pos[1] + vel[1] * DT), vel

pos, vel = (0.0, 0.0), (6.0, 0.0)          # running east at full speed
target = (0.0, 10.0)                       # the target is due north
dx, dy = target[0] - pos[0], target[1] - pos[1]
n = math.hypot(dx, dy)
desired = (dx / n * 6.0, dy / n * 6.0)     # seek
pos, vel = step(pos, vel, desired, max_speed=6.0, max_accel=12.0)
print(f"vel = ({vel[0]:.3f}, {vel[1]:.3f}), speed {math.hypot(*vel):.3f}")
print(f"pos = ({pos[0]:.4f}, {pos[1]:.4f})")
```

<details>
<summary>Answer and worked solution</summary>

**Answer.**

```
vel = (5.859, 0.141), speed 5.860
pos = (0.0976, 0.0024)
```

The desired velocity is `(0, 6)`. The steering request is `(0, 6) − (6, 0) = (−6, 6)`, of length `√72 = 8.49`. One frame allows `12 / 60 = 0.2` m/s of change, so the request is scaled to length 0.2: `(−0.141, 0.141)`. The new velocity is `(5.859, 0.141)`, speed 5.860, under `max_speed`, so the second truncate changes nothing. Position moves by `velocity / 60`.

The whole change from `(6, 0)` to `(0, 6)` has length 8.49 m/s, and the body grants at most 12 m/s², so a 90° turn takes at least `8.49 / 12 = 0.71` s, about 42 frames. The soldier curves through the turn instead of pivoting. That curve is the point of steering by a velocity difference.
</details>

7. *Week 2 · compute.*
   (a) A pursuer at `(0, 0)` with `max_speed = 8` m/s uses `T = D / max_speed`. The quarry is at `(12, 16)` moving at `(−3, 0)` m/s. What point does the pursuer aim at this frame?
   (b) A soldier (`max_speed = 6` m/s) uses arrive with `r = 4` m. How long does it take to close the last stretch from 0.5 m left to 0.05 m left?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) `(4.5, 16)`. (b) About 1.54 s.

(a) `D = √(144 + 256) = 20`, so `T = 20 / 8 = 2.5` s. The predicted position is `(12, 16) + 2.5 × (−3, 0) = (4.5, 16)`. The pursuer aims well ahead of where the quarry is, cutting across its path.

(b) Inside the ramp the remaining distance decays exponentially with time constant `r / max_speed = 4 / 6 = 0.667` s. Going from 0.5 m to 0.05 m is a factor of 10, which takes `0.667 × ln 10 = 1.54` s. A 1.5 s creep over the last half meter reads as hesitation. A stopping distance of a few centimeters, or a smaller `r`, removes it.
</details>

8. *Week 2 · critique.* A bot blends two steering requests. Chase asks for `(5, 0)` with weight 0.7. Avoid asks for `(−6, 1)` with weight 0.3.
   (a) What is the blended request? What is it with equal weights of 0.5?
   (b) A teammate says "we tuned the weights to 0.7 and 0.3, so the stalemate is fixed." Is it? What would you do instead?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) `(1.7, 0.3)` and `(−0.5, 0.5)`. (b) No. The weights only move the place where the two requests cancel.

(a) `0.7 × (5, 0) + 0.3 × (−6, 1) = (3.5 − 1.8, 0.3) = (1.7, 0.3)`. With 0.5 each, `(2.5 − 3, 0.5) = (−0.5, 0.5)`: the bot backs off slightly and drifts sideways.

(b) Avoidance usually grows as the obstacle gets closer. With 0.7 and 0.3 the bot creeps toward the obstacle until the avoid request has grown enough to cancel the chase, and then it stops there, a little closer than before. The stalemate still happens. Fixes from the lecture: give avoidance priority and pick a side (steer around rather than away), or switch to context steering, where each behavior writes interest and danger per heading and one step picks the most interesting heading that is not dangerous. Fray reports that F1 2011 did the second and cut 4,000 lines of special cases.
</details>

## Week 3: Graphs and Dijkstra

9. *Week 3 · code.* This runs the lecture's Dijkstra on a small undirected graph. What does it print? Which pushes became stale, and what is the path to E?

```python
import heapq

def dijkstra(graph, start):
    g, prev = {start: 0}, {start: None}
    open_list = [(0, start)]
    closed = set()
    while open_list:
        cost, u = heapq.heappop(open_list)
        if u in closed:
            print(f"skip   {u} at {cost}")
            continue
        closed.add(u)
        print(f"expand {u} at {cost}")
        for w, step in graph[u]:
            new = cost + step
            if w not in g or new < g[w]:
                g[w], prev[w] = new, u
                heapq.heappush(open_list, (new, w))
    return g, prev

EDGES = [("A", "B", 2), ("A", "C", 5), ("B", "C", 1), ("B", "D", 7),
         ("C", "D", 2), ("C", "E", 6), ("D", "E", 1)]
graph = {n: [] for n in "ABCDE"}
for a, b, c in EDGES:              # undirected: store both directions
    graph[a].append((b, c))
    graph[b].append((a, c))
g, prev = dijkstra(graph, "A")
print(g)
```

<details>
<summary>Answer and worked solution</summary>

**Answer.**

```
expand A at 0
expand B at 2
expand C at 3
skip   C at 5
expand D at 5
expand E at 6
skip   D at 9
skip   E at 9
{'A': 0, 'B': 2, 'C': 3, 'D': 5, 'E': 6}
```

Expanding A pushes B at 2 and C at 5. Expanding B improves C to 3 and pushes D at 9. The C at 5 is now stale. Expanding C improves D to 5 and pushes E at 9. The D at 9 is stale. Expanding D improves E to 6. The E at 9 is stale. Three stale copies are skipped, and every one was a first discovery that looked final in BFS terms and was not.

The path to E follows `prev` back from E: E came from D, D from C, C from B, B from A. So A → B → C → D → E, cost `2 + 1 + 2 + 1 = 6`, four edges. The two-edge route A → C → E costs 11.
</details>

10. *Week 3 · code.* The Well floods, and its corridor to the Crypt now takes 12 s instead of 4. Everything else is the lecture's dungeon. Run the lecture's `dijkstra` and `path_to` with this table. What is printed, and why does a stale Crypt entry appear before the Shrine at the same cost?

```python
DUNGEON = {
    "Gate":   [("Hall", 4)],
    "Hall":   [("Gate", 4), ("Armory", 3), ("Well", 2), ("Crypt", 15)],
    "Armory": [("Hall", 3), ("Crypt", 9)],
    "Well":   [("Hall", 2), ("Crypt", 12)],
    "Crypt":  [("Hall", 15), ("Armory", 9), ("Well", 12), ("Shrine", 2)],
    "Shrine": [("Crypt", 2), ("Vault", 1)],
    "Vault":  [("Gate", 5)],
}
```

<details>
<summary>Answer and worked solution</summary>

**Answer.**

```
expand Gate   at  0
expand Hall   at  4
expand Well   at  6
expand Armory at  7
expand Crypt  at 16
skip   Crypt  at 18 (stale)
expand Shrine at 18
skip   Crypt  at 19 (stale)
expand Vault  at 19
{'Gate': 0, 'Hall': 4, 'Armory': 7, 'Well': 6, 'Crypt': 16, 'Shrine': 18, 'Vault': 19}
Gate -> Hall -> Armory -> Crypt
```

The Crypt is first pushed at 19 through the collapsed stair. The Well offers `6 + 12 = 18`, and the Armory offers `7 + 9 = 16`, the best. So the heap holds three Crypt copies, at 16, 18 and 19. The Shrine is pushed at `16 + 2 = 18`. Two entries tie at cost 18, `(18, "Crypt")` and `(18, "Shrine")`. Python compares tuples element by element, and `"Crypt" < "Shrine"`, so the stale Crypt comes out first and is skipped. Ties on cost are broken by the node name here, which is why a spec for an interactive must state the tie rule.
</details>

11. *Week 3 · compute.* Use the lecture's 6 × 5 terrain map and its printed `g` grid. How many tiles, start included, can the unit reach with budgets of 2, 5 and 6 MP?

<details>
<summary>Answer and worked solution</summary>

**Answer.** 6, 16 and 18 tiles.

The reachable set is every tile with `g ≤ budget`. The grid, rows top to bottom, is `2 3 4 5 6 7`, `1 3 5 7 7 8`, `0 2 5 8 9 9`, `1 3 # 7 7 8`, `2 3 4 5 6 7`.

- Budget 2: one tile in row 0, one in row 1, two in row 2, one in row 3, one in row 4. Total 6.
- Budget 5: four in row 0 (2 to 5), three in row 1 (1, 3, 5), three in row 2 (0, 2, 5), two in row 3 (1, 3), four in row 4. Total 16.
- Budget 6: five, three, three, two, five. Total 18.

These match Dijkstra with a budget, which never pushes a tile whose cost would exceed it. The range grows in cost contours: going from 5 to 6 MP adds only the two row-edge tiles at `g = 6`, because the middle of the map is expensive.
</details>

12. *Week 3 · compute.* A Civilization VI unit has 3 MP per turn. It follows the rules the lecture quotes: a unit needs the full cost of a tile before entering it, except that a unit with full MP can always move one tile.
   (a) How many turns does it take to walk a route whose tiles cost `1, 2, 2, 1` in that order? And a route costing `2, 2, 1, 1`?
   (b) Both routes cost 6 MP in the simple additive model. What does the difference mean for the search, and how does the lecture fix it?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 2 turns and 3 turns. (b) The cost of a step depends on the MP left, so the node must include it.

(a) Route `1, 2, 2, 1`. Turn 1: enter the 1 (2 left), enter the first 2 (0 left). Turn 2: enter the second 2 (1 left), enter the 1 (0 left). Done in 2 turns.

Route `2, 2, 1, 1`. Turn 1: enter the first 2 (1 left). The second 2 needs 2 MP and the unit has 1, so the turn ends with 1 MP wasted. Turn 2: enter the 2 (1 left), enter a 1 (0 left). Turn 3: enter the last 1. Three turns.

(b) The simple sum says both routes cost 6 and take `6 / 3 = 2` turns. The real rule wastes MP at turn boundaries, so the same tiles in a different order cost a whole extra turn. Dijkstra cannot see that if a node is only a tile. The fix is to change the graph, not the algorithm. Make each node a pair (tile, MP left this turn), let an edge that ends a turn reset MP, and order the heap by (turns, MP spent). Dijkstra then runs unchanged on the bigger graph.
</details>

## Week 4: A* and heuristics

13. *Week 4 · compute.* A* uses the lecture's heap key `(g + w × h, h, cell)`. The open list holds four cells.

| Cell | `g` | `h` |
|---|---|---|
| (3, 5) | 6 | 7 |
| (1, 4) | 4 | 9 |
| (6, 6) | 8 | 5 |
| (2, 8) | 10 | 4 |

   Which cell is expanded next with `w = 1`? With `w = 2`?

<details>
<summary>Answer and worked solution</summary>

**Answer.** `(6, 6)` with `w = 1`, `(2, 8)` with `w = 2`.

With `w = 1`, the `f` values are 13, 13, 13 and 14. Three cells tie at 13, and the second element of the key breaks the tie toward the smallest `h`: `(6, 6)` with `h = 5`.

With `w = 2`, `f = g + 2h` gives 20, 22, 18 and 18. `(6, 6)` and `(2, 8)` tie at 18, and the smaller `h` wins again, so `(2, 8)` with `h = 4`. Weighting `h` pulls the search toward cells that are closer to the goal even when they cost more to reach.
</details>

14. *Week 4 · compute.* An 8-way grid uses `D = 10` for a straight step and `D2 = 14` for a diagonal. A cell is at `(1, 1)` and the goal at `(8, 4)`, on an empty map.
   (a) Compute the octile, Manhattan and Chebyshev heuristics, and the true cost.
   (b) Which of the three are admissible here? By how much does each one miss?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) Octile 82, Manhattan 100, Chebyshev 70; true cost 82. (b) Octile and Chebyshev are admissible. Manhattan overestimates by 18. Chebyshev underestimates by 12.

(a) `dx = 7`, `dy = 3`. Octile is `10 × 7 + (14 − 10) × 3 = 82`. Manhattan is `10 × (7 + 3) = 100`. Chebyshev is `10 × 7 = 70`. On an empty map the cheapest route is 3 diagonals and 4 straight steps, `3 × 14 + 4 × 10 = 82`, so octile is exact.

(b) Manhattan charges 20 for each diagonal that really costs 14, so it overestimates by `6 × min(dx, dy) = 18` and can make A* return a worse path. Chebyshev charges 10 for each diagonal, underestimating by `4 × 3 = 12`. It stays admissible but A* explores more, because the guess is further from the truth.
</details>

15. *Week 4 · code.* The lecture's section 2 program is run with a longer wall, so that only row 0 is open above it and the wall reaches the bottom row.

```python
MAP = [
    "............",
    "....#.......",
    "....#.......",
    "....#.......",
    "S...#......G",
    "....#.......",
    "....#.......",
    "....#.......",
]
```

   (a) Before running it, what path cost do you expect? Show the working.
   (b) The program prints expansions of 80 for Dijkstra, 41 for A* and 39 for weighted A*. Why does A* expand more here than the 32 on the lecture's map?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 19. (b) The heuristic is off by 8 instead of 6, so A* has to fill more `f`-layers in front of the wall.

The output is:

```
Dijkstra (h = 0)     path cost 19, cells expanded 80
A* (Manhattan)       path cost 19, cells expanded 41
Weighted A* (w = 2)  path cost 19, cells expanded 39
```

(a) The wall now blocks rows 1 to 7, so the only way past is row 0. From row 4 the path climbs 4 rows, crosses 11 columns and comes down 4 rows: `11 + 8 = 19`.

(b) Manhattan distance from the start is 11, and the true cost is 19. A* must expand every cell with `f < 19`, and the `f`-layers go 11, 13, 15, 17 before one reaches around the wall. On the lecture's map the detour was 6, so the layers stopped at 17 and the pocket in front of the wall was shorter. The bigger the gap between `h` and the true cost, the more A* behaves like Dijkstra. This is the Factorio lake from the hook in a small grid.
</details>

16. *Week 4 · compute.* On the lecture's road map (road tiles cost 1 to enter, ground costs 2, start `(3, 0)`, goal `(3, 10)`), `h = c × Manhattan`. Only `c ≤ 1` is admissible.
   (a) Running the lecture's `astar` with `c = 1.2` still returns the road (cost 16). With `c = 1.25` it returns 19. Derive where the switch happens by comparing two cells: the road's corner `(0, 0)` and the last ground tile before the goal, `(3, 9)`.
   (b) What does this say about "it worked in testing" as evidence for a heuristic?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) The road is found while `3 + 13c < 18 + c`, that is `c < 1.25`. (b) An inadmissible heuristic can pass on one map by luck of geometry and fail on the next.

(a) Along the road, `f` climbs while the route goes up the left column (each step adds 1 to `g` and `c` to `h`) and falls along the top row (each step adds 1 to `g` and removes `c` from `h`). Its highest value is at the corner `(0, 0)`: `g = 3`, Manhattan distance `3 + 10 = 13`, so `f = 3 + 13c`. Along the straight ground route, the last tile `(3, 9)` has `g = 18` and `h = c`, so `f = 18 + c`. Once `(3, 9)` is expanded, the goal is pushed at `f = 19` with `h = 0` and comes out next.

If `3 + 13c < 18 + c`, the corner comes off the heap first, the road cells behind it have smaller `f`, and the goal is reached by road at 16. That needs `12c < 15`, `c < 1.25`. At exactly 1.25 both are 19.25, the tie goes to the smaller `h`, which is `(3, 9)` at 1.25 against the corner's 16.25, and the unit walks straight across the ground. A sweep with the lecture's code confirms it: 1.245 gives 16, 1.25 gives 19.

(b) Every `c` between 1 and 1.25 is inadmissible, yet finds the road on this map. Stretch the detour or move the road one row further out and the threshold moves. Admissibility is a promise for every map. Passing one test map is not.
</details>

17. *Week 4 · compute.*
   (a) Weighted A* with `w = 1.25` runs on a map whose cheapest path costs 120. What is the worst cost it may return? What largest `w` guarantees paths at most 5% longer than optimal?
   (b) A late-game Civilization VI map has railroads at 0.25 MP per tile. A tile 12 hexes from the goal is on a railroad the whole way. What admissible heuristic value do you give it, and by what factor would "1 per hex" overestimate the true cost along that railroad?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 150, and `w ≤ 1.05`. (b) 3 MP; a factor of 4.

(a) With an admissible `h`, weighted A* returns at most `w` times the optimum: `1.25 × 120 = 150`. For at most 5% extra, `w ≤ 1.05`.

(b) The admissible heuristic multiplies hex distance by the cheapest step in the game, `12 × 0.25 = 3` MP. "1 per hex" says 12, while the railroad route costs 3, an overestimate by a factor of 4, and A* may ignore the railroad. The scale factor is set by the cheapest terrain, which changes as the game goes on.
</details>

## Week 5: Navigation meshes

18. *Week 5 · compute.* A navmesh triangle has vertices `(1, 1)`, `(7, 2)` and `(3, 6)`.
   (a) Show that the vertices are in counter-clockwise order.
   (b) Using the lecture's `cross(a, b, p)` for each edge, is `(4, 3)` inside? Is `(6, 5)`?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) The signed area test is positive (28). (b) `(4, 3)` is inside; `(6, 5)` is outside.

(a) `cross((1, 1), (7, 2), (3, 6)) = (6)(5) − (1)(2) = 28 > 0`, so the third vertex is to the left of the first edge and the order is counter-clockwise.

(b) With `cross(a, b, p) = (b.x − a.x)(p.y − a.y) − (b.y − a.y)(p.x − a.x)`:

| Edge | `p = (4, 3)` | `p = (6, 5)` |
|---|---|---|
| (1, 1) → (7, 2) | `6 × 2 − 1 × 3 = 9` | `6 × 4 − 1 × 5 = 19` |
| (7, 2) → (3, 6) | `−4 × 1 − 4 × (−3) = 8` | `−4 × 3 − 4 × (−1) = −8` |
| (3, 6) → (1, 1) | `−2 × (−3) − (−5) × 1 = 11` | `−2 × (−1) − (−5) × 3 = 17` |

All three are positive for `(4, 3)`, so it is inside. For `(6, 5)` the second edge gives −8: the point is to the right of that edge, outside the triangle.
</details>

19. *Week 5 · compute.* In the lecture's five-polygon level, the goal moves to `(11, 12)`. The start stays at `(1, 1)` and the portals are the same four.
   (a) What path does the lecture's `funnel` return, and how long is it?
   (b) How long is the midpoint path?
   (c) Check that the funnel path is legal at the door.

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) `[(1, 1), (10, 3), (11, 12)]`, 18.27 m. (b) 19.25 m. (c) It crosses `y = 8` at `x = 10.56` and `y = 9` at `x = 10.67`, both inside the door.

(a) The path still bends at the corridor's upper exit corner `(10, 3)`, because a straight line from `(1, 1)` toward the north room climbs out of the corridor long before `x = 10`. From `(10, 3)` the goal is up and slightly east, and the line fits through the door, so there is no second corner. Length `√85 + √82 = 9.22 + 9.06 = 18.27` m.

(b) Start, the four portal midpoints `(4, 2)`, `(10, 2)`, `(11, 8)`, `(11, 9)`, then the goal: `√10 + 6 + √37 + 1 + 3 = 3.16 + 6.00 + 6.08 + 1.00 + 3.00 = 19.25` m.

(c) The leg from `(10, 3)` to `(11, 12)` rises 9 m while moving 1 m east. At `y = 8` it is at `x = 10 + 5/9 = 10.56`, and at `y = 9` at `x = 10 + 6/9 = 10.67`. Both are between 10 and 12. Compare the lecture's goal `(13, 11)`, where the straight line would cross `y = 9` at 12.25, past the jamb, which is why that path needed the `(12, 9)` corner.
</details>

20. *Week 5 · compute.* A wall runs along `x = 5` between a start at `(0, 0)` and a goal at `(10, 0)`. Door A spans `y = 2` to `y = 10`. Door B spans `y = −4` to `y = −3`. A* over polygons uses midpoint costs.
   (a) Which door does A* choose? Give both midpoint costs.
   (b) Give the true funnel length through each door. How much longer is the chosen route?
   (c) Split door A's polygon so that `y = 2` to `y = 4` is its own portal. Which door does A* choose now?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) Door B, 12.21 against 15.62. (b) A 10.77 m, B 11.66 m; the chosen route is 8.3% longer. (c) Door A, at 11.66 against 12.21.

(a) Door A's midpoint is `(5, 6)`: `2 × √(25 + 36) = 15.62`. Door B's is `(5, −3.5)`: `2 × √(25 + 12.25) = 12.21`. B looks cheaper.

(b) The best path through A touches `(5, 2)`: `2 × √29 = 10.77`. Through B it touches `(5, −3)`: `2 × √34 = 11.66`. `11.66 / 10.77 = 1.083`. The character walks past a wide open door to use a narrow one.

(c) The new portal's midpoint is `(5, 3)`, cost `2 × √(25 + 9) = 11.66 < 12.21`, so A* picks door A and the funnel returns the 10.77 m path. Splitting wide portals is one of the lecture's fixes. It costs more nodes, not a new algorithm.
</details>

21. *Week 5 · compute.* The lecture's level is eroded by agent radius `r`, as Recast's `walkableRadius` does. The corridor spans `1 ≤ y ≤ 3` and the door `10 ≤ x ≤ 12`.
   (a) What is the largest radius that can still use the corridor and the door?
   (b) With `r = 0.9`, how wide is the walkable strip in the corridor?
   (c) A giant with `r = 1.2` uses the same mesh without erosion. What does the player see, and what is the standard fix?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 1.0 m. (b) 0.2 m. (c) The giant scrapes and clips through the walls, or gets stuck; the fix is a separate mesh eroded for its radius, which has no corridor at all.

(a) Erosion moves each wall-side edge inward by `r`. The corridor becomes `1 + r ≤ y ≤ 3 − r`, which exists only while `r ≤ 1`. The door is also 2 m wide, so the limit is 1.0 m.

(b) `3 − 0.9 − (1 + 0.9) = 0.2` m. The funnel path through it is nearly the center line.

(c) The mesh built for small agents says the corridor is walkable, so the giant's path goes through it with its body overlapping both walls. Erosion is the fix, and it costs one mesh per agent size. On a mesh eroded by 1.2 m, the corridor and door vanish, A* over polygons finds no corridor between room A and the north room, and the giant has no path. That is the correct answer, and the level designer must decide whether the giant should ever reach that room.
</details>

## Week 6: Finite state machines

22. *Week 6 · compute.* Two attackers alternate hits every 0.5 s, as in the lecture's model. This NPC turns faster than the lecture's: its switch cost is `T = 0.4` s.
   (a) For `L = 1, 2, 3, 4` s, give the switch period `P`, switches per minute and the fraction of time attacking.
   (b) What is the smallest whole-second `L` that keeps the NPC attacking at least 90% of the time, and what is its worst reaction delay?
   (c) Where does the lecture's rule of thumb `P ≈ 5T` put the knee for this NPC?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) See the table. (b) `L = 4` s, 91.1% attacking, worst reaction about 4.5 s. (c) At `P ≈ 2` s, so `L` of 2 s already gives 84%.

(a) `P` is the first of 0.5, 1.5, 2.5, ... that is at least `L`, so `P = ceil(L − 0.5) + 0.5`.

| `L` (s) | `P` (s) | Switches per minute `60 / P` | Attacking `1 − 0.4 / P` |
|---|---|---|---|
| 1 | 1.5 | 40.0 | 73.3% |
| 2 | 2.5 | 24.0 | 84.0% |
| 3 | 3.5 | 17.1 | 88.6% |
| 4 | 4.5 | 13.3 | 91.1% |

(b) 90% needs `0.4 / P ≤ 0.1`, so `P ≥ 4`. The first available period is 4.5, which needs `L > 3.5`, so `L = 4`. The NPC then ignores the other attacker for up to 4.5 s.

(c) `5T = 2` s. The step from `L = 1` to `L = 2` buys 10.7 points, the next second 4.6 points and the one after 2.5. Past the knee each extra second buys less attack time and costs a full second of reaction delay.
</details>

23. *Week 6 · code.* The lecture's commitment simulation is run with a 0.4 s turn. What does it print, and why does the first line differ from the model's 73.3% in the last digit?

```python
TICK = 0.1
TURN = 4          # 0.4 s to turn and re-path

def simulate(lock, hits, ticks):
    target, held, turning = None, 0, 0
    switches = attacking = 0
    for t in range(ticks):
        for attacker in hits.get(t, []):
            if target is None:
                target, held = attacker, 0
            elif attacker != target and held >= lock:
                target, held, turning = attacker, 0, TURN
                switches += 1
        if turning > 0:
            turning -= 1
        elif target is not None:
            attacking += 1
        held += 1
    return switches, attacking

TICKS = 10_000
hits = {}
for t in range(0, TICKS, 10):
    hits.setdefault(t, []).append("A")
for t in range(5, TICKS, 10):
    hits.setdefault(t, []).append("B")

for lock in (10, 40):
    s, a = simulate(lock, hits, TICKS)
    print(f"L = {lock * TICK:.0f} s: {s / (TICKS * TICK / 60):.1f} switches/min, "
          f"{100 * a / TICKS:.1f}% attacking")
```

<details>
<summary>Answer and worked solution</summary>

**Answer.**

```
L = 1 s: 40.0 switches/min, 73.4% attacking
L = 4 s: 13.3 switches/min, 91.1% attacking
```

Both match question 22's model. The first target is taken at tick 0 without a turn, so the simulation starts with 1.5 s of attacking that the steady-state formula charges a turn for. Over 10,000 ticks that start-up adds a few ticks, enough to move 73.33% to 73.4% after rounding. The lecture runs 1,000 simulated seconds for this reason: long enough that start-up effects fall below the printed precision in most rows.
</details>

24. *Week 6 · code.* A guard is chasing a player it can always see. Its distance to the player is sampled once per tick. What does this print? What does the difference mean for the player?

```python
DIST = [2.1, 1.9, 2.2, 1.8, 2.3, 1.95, 2.05, 3.1]   # one reading per tick; the player is always seen

def run(enter, leave):
    state, log = "CHASE", []
    for tick, d in enumerate(DIST):
        if state == "CHASE" and d <= enter:
            state = "ATTACK"
            log.append(tick)
        elif state == "ATTACK" and d > leave:
            state = "CHASE"
            log.append(tick)
    return log

print("single threshold:", run(2.0, 2.0))
print("band 2 to 3 m:  ", run(2.0, 3.0))
```

<details>
<summary>Answer and worked solution</summary>

**Answer.**

```
single threshold: [1, 2, 3, 4, 5, 6]
band 2 to 3 m:   [1, 7]
```

With one threshold, every reading that crosses 2 m flips the state: ATTACK at tick 1 (1.9), CHASE at 2 (2.2), ATTACK at 3 (1.8), CHASE at 4 (2.3), ATTACK at 5 (1.95), CHASE at 6 (2.05). Six transitions in eight ticks. The player sees a guard that raises its weapon, lowers it and starts running, over and over, while standing at arm's length.

With the band, the guard enters ATTACK at tick 1 and stays until the distance exceeds 3 m at tick 7. Two transitions, and the first one happens on the same tick as before, so responsiveness to the real approach is unchanged. That is hysteresis on distance, the same idea as MA101's aggro and leash radii. It filters the wobble in one continuous input. It would not help with a stream of separate hits from two attackers, which needs the time lock of questions 22 and 23.
</details>

25. *Week 6 · compute.*
   (a) A Doom mod adds a monster whose run states last 5 tics each. At minimum, how long is its infighting lock? What if the mod also sets `BASETHRESHOLD` to 60 for a monster with 2-tic run states?
   (b) A designer adds STUNNED to a six-state guard. STUNNED can be entered from every other state and always exits to CHASE. How many transitions can the seven-state machine have at most, and how many new guards must be written?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 14.3 s and 3.4 s. (b) At most 42; 7 new guards.

(a) Doom's lock counts `A_Chase` calls, one per run state. 100 calls at 5 tics each is 500 tics, and `500 / 35 = 14.3` s. With a threshold of 60 and 2-tic states, `60 × 2 / 35 = 3.4` s. The true lock is longer in both cases, because the counter only drops while the monster is chasing, not while it attacks or flinches.

(b) `N(N − 1) = 7 × 6 = 42`. STUNNED adds 6 incoming transitions and 1 outgoing, so 7 new guards. A hierarchical machine would write the 6 incoming ones once, as a single transition on a superstate that holds the other six states.
</details>

## Week 7: Behavior trees

26. *Week 7 · code.* This uses the lecture's `Condition`, `Action`, `Composite`, `Selector` and `Sequence` classes from section 2, with the reactive rule. What do the two lines print? What does the second line tell you about the tree?

```python
# Uses the week 7 lecture's classes from section 2.
def trace(low_ammo_ticks):
    tree = Selector(
        Sequence(Condition("low_ammo"), Action("Reload", 2)),
        Sequence(Condition("sees"), Action("Shoot")),
        Action("Wander", 3),
    )
    out = []
    for t in range(6):
        bb = {"low_ammo": t in low_ammo_ticks, "sees": t in {1, 2, 3, 4, 5}}
        status = tree.tick(bb)
        out.append(f"{bb['acted']}:{status[0]}")
    return out

print(trace({2, 3}))
print(trace({2}))
```

<details>
<summary>Answer and worked solution</summary>

**Answer.**

```
['Wander:r', 'Shoot:r', 'Reload:r', 'Reload:s', 'Shoot:r', 'Shoot:r']
['Wander:r', 'Shoot:r', 'Reload:r', 'Shoot:r', 'Shoot:r', 'Shoot:r']
```

The letter after the colon is the root's status: `r` for RUNNING, `s` for SUCCESS.

First line. Tick 0: nothing is true, so Wander runs. Tick 1: "sees" is true, the root picks the shoot branch and aborts Wander. Tick 2: "low ammo" is true and outranks shooting, so Reload starts (1 of 2). Tick 3: still low, Reload finishes, the reload sequence succeeds and so does the root. Ticks 4 and 5: back to shooting.

Second line. "Low ammo" is true on tick 2 only. On tick 3 the root starts from the top, the reload condition fails, the shoot branch wins and `finish` halts Reload, resetting its counter. The reload never completes. This is the lecture's "reactivity is also flicker" point. A reactive selector drops a started action the moment its guard condition flickers false. Give the reload sequence memory, or check a fact that stays true until the reload is done (such as the magazine count), and the guard finishes what it started.
</details>

27. *Week 7 · trace.* The lecture's guard tree runs on a new 8-tick timeline at 5 Hz: noise on ticks 1 to 3, sees on ticks 3 to 6, in range on ticks 5 and 6, never hurt. Give the action on each tick under the memory rule and under the hybrid rule. Name every visible bug in the memory row.

<details>
<summary>Answer and worked solution</summary>

**Answer.**

| Tick | noise | sees | in range | Memory | Hybrid |
|---|---|---|---|---|---|
| 0 | — | — | — | Patrol | Patrol |
| 1 | yes | — | — | Patrol | GoToNoise |
| 2 | yes | — | — | Patrol | LookAround |
| 3 | yes | yes | — | Patrol | Chase |
| 4 | — | yes | — | Chase | Chase |
| 5 | — | yes | yes | Chase | Shoot |
| 6 | — | yes | yes | Chase | Shoot |
| 7 | — | — | — | Chase | Patrol |

Hybrid first. The noise at tick 1 wins over patrol at once, GoToNoise takes 2 ticks and succeeds on tick 2, so LookAround starts in the same tick. On tick 3 the fight branch is re-checked and wins. It shoots when in range and patrols again on tick 7.

Memory has three bugs. It ignores the noise, because the root resumes the running patrol leg (ticks 0 to 3) and never looks at the search branch. It reacts to the player one tick late (0.2 s), on tick 4, when the patrol leg has finished and the root starts from the top. And it never shoots: the fight sequence resumes at the engage selector, which resumes at the running Chase and never re-checks "in range?". On tick 7 it keeps chasing a player it cannot see, because the memory sequence skips "sees?" too.

The visit totals are 35 for memory and 69 for hybrid. Memory is cheap because it looks at almost nothing, which is exactly why it misses everything.
</details>

28. *Week 7 · compute.* From the lecture's reactive trace, the guard tree costs 8 node visits per tick while patrolling, 9 while fighting and 4 while fleeing. Under the memory rule a guard that is already shooting costs 5.
   (a) 200 guards fight the player at once, ticking at 5 Hz. How many visits per second under the reactive rule and under the memory rule? What if the tree ticked at 60 Hz instead?
   (b) Under the memory rule, patrol legs take 4 ticks. The player appears just after a leg starts. How many ticks, and how many seconds at 5 Hz, can pass before the guard reacts?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 9,000 against 5,000 per second at 5 Hz; 108,000 against 60,000 at 60 Hz. (b) Up to 3 ticks after the first tick that sees the player, 0.6 s, plus up to 0.2 s before that tick comes round, so up to about 0.8 s.

(a) Reactive: `200 × 5 × 9 = 9,000`. Memory: `200 × 5 × 5 = 5,000`. At 60 Hz both grow by 12 times. Going from 5 Hz to 60 Hz costs more than going from memory to reactive, and it makes the guard react faster than any human, so the tick rate is the bigger lever.

(b) The leg runs for 4 ticks and succeeds on its fourth. If "sees" first becomes true on the leg's second tick, the root does not look at the fight branch until the tick after the leg ends, 3 ticks later. The lecture's check-yourself question 3 has this case: sees at tick 1, reaction at tick 4. Add the up-to-one-tick wait before the first tick that samples the change, and the delay ranges from nothing to about 0.8 s depending only on where in the leg the player appeared. Players read that spread as randomness.
</details>

29. *Week 7 · design.* A designer reorders the lecture's guard so that the fight branch comes first and the flee branch second: `Selector[fight, flee, search, Patrol]`. Hybrid rule.
   (a) On a tick where "sees", "in range" and "hurt" are all true, what does each ordering do?
   (b) Which ordering is right? Answer for two different experience goals.

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) The lecture's order flees; the reordered tree shoots. (b) It depends on the character. A survivor should flee first; a berserker should fight first.

(a) A selector takes its first child that does not fail. With flee first, "hurt?" succeeds and RunToSafety runs. With fight first, "sees?" and "in range?" succeed and Shoot runs. The flee branch only runs when the guard is hurt and cannot see the player.

(b) Neither is a bug in the code. They are two personalities. For guards who should feel human and beatable, flee first: the player sees a wounded enemy break and run, which rewards damage. For a berserker whose threat is that it never backs off, fight first, and make the ordering readable with a bark or a visual rage state. The lecture's rule applies: most tree bugs are ordering bugs, found by asking "what should win when both are true?" for each pair of neighbouring branches. Write the answer in the design document, not only in the tree.
</details>

## Week 8: Utility AI

30. *Week 8 · compute.* The lecture's brute scores `Attack(e) = 0.6 + 0.3 × (1 − e)` and `Drink(h) = (1 − h)^k`.
   (a) With `k = 1.5`, at what health does it start drinking against a fresh enemy? Against an enemy at 30% health?
   (b) With `k = 2`, the same two switch points. Then with `k = 2` against an enemy at 0%.

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 28.9% and 13.1%. (b) 22.5% and 10.0%; 5.1% against a dying enemy.

The switch point is `h* = 1 − A^(1/k)`.

(a) Fresh enemy, `A = 0.6`: `1 − 0.6^(1/1.5) = 1 − 0.711 = 28.9%`. Enemy at 30%, `A = 0.6 + 0.3 × 0.7 = 0.81`: `1 − 0.81^(1/1.5) = 1 − 0.869 = 13.1%`.

(b) `k = 2`: `1 − √0.6 = 22.5%` (the lecture's value), and `1 − √0.81 = 1 − 0.9 = 10.0%`. Enemy at 0%, `A = 0.9`: `1 − √0.9 = 5.1%`. Every step toward a dying enemy makes the brute gamble harder. If a designer does not want drinking below 10%, a curve change will not guarantee it. A higher rank for "drink below 10%" will.
</details>

31. *Week 8 · compute.* A healer companion scores Heal tank as `(1 − t)^k × m^0.5`, where `t` is the tank's health and `m` the healer's mana, both from 0 to 1. Damage boss scores a flat 0.5, and ties go to Damage boss.
   (a) With full mana, the designer wants healing to start at 35% tank health. What `k` does that need?
   (b) With that `k`, where does healing start at 64% mana? At 25% mana?
   (c) What does (b) say about using a product to combine a resource consideration with an urgency one?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) `k = 1.61`. (b) At 25.3% tank health; at 25% mana, never. (c) The product can silently switch an action off in a whole region of states.

(a) `(1 − 0.35)^k = 0.5`, so `k = ln 0.5 / ln 0.65 = −0.693 / −0.431 = 1.61`.

(b) At 64% mana, `m^0.5 = 0.8`. Healing needs `(1 − t)^1.61 × 0.8 > 0.5`, so `(1 − t)^1.61 > 0.625`, `1 − t > 0.625^(1/1.61) = 0.747`, `t < 25.3%`. At 25% mana, `m^0.5 = 0.5`, so Heal tank is at most `1 × 0.5 = 0.5`, reached only at 0% tank health, and a tie goes to damage. The healer never heals.

(c) At a quarter of its mana the healer still has plenty for one heal, yet it watches the tank die. The product meant "scarce mana lowers the urge to heal", and at this curve it means "never heal". Draw the decision map for every mana level before shipping, and put "always heal below 15%" in a higher rank (dual utility) so no curve can overrule it.
</details>

32. *Week 8 · compute.* Action X has two considerations scoring 0.9 and 0.6. Action Y has three, each scoring 0.8. Which action wins under the product? Under the geometric mean? Which rule treats Y fairly, and what does that rule give up?

<details>
<summary>Answer and worked solution</summary>

**Answer.** The product picks X (0.540 against 0.512). The geometric mean picks Y (0.800 against 0.735).

Product: `0.9 × 0.6 = 0.540` and `0.8³ = 0.512`. Geometric mean: `√0.540 = 0.735` and `0.512^(1/3) = 0.800`.

Every one of Y's considerations is at 0.8, and X has one at 0.6, yet the product prefers X only because Y is described by one more factor. The geometric mean removes that bias and keeps the zero veto. What it gives up is the force of one low consideration. X's 0.6 hurts X less under the mean than under the product, so a mean can let through an action that one consideration was trying to discourage. Pick one rule for the whole game and tell your designers which.
</details>

33. *Week 8 · code.* The lecture's commitment replay runs on a new health trace. What does it print? For each bonus, say whether a potion ever finishes (3 drink thinks in a row), and explain the last line with the start and stop thresholds.

```python
HP = [35, 26, 22, 24, 21, 17, 20, 23, 27, 25, 19, 28]   # percent, one per think

def replay(bonus):
    current, row = "A", ""
    for hp in HP:
        scores = {"A": 0.6, "D": (1 - hp / 100) ** 2}
        scores[current] *= 1 + bonus
        current = max(scores, key=scores.get)
        row += current
    switches = sum(a != b for a, b in zip("A" + row, row))
    return row, switches

for bonus in (0.0, 0.1, 0.15):
    print(bonus, *replay(bonus))
```

<details>
<summary>Answer and worked solution</summary>

**Answer.**

```
0.0 AADADDDAAADA 6
0.1 AAAAADDDAAAA 2
0.15 AAAAAAAAAAAA 0
```

No bonus. Drink wins whenever health is below 22.5%, so every think at 22, 21, 17, 20 and 19 is D. There are 6 switches, and thinks 5, 6 and 7 (21, 17, 20) are three drinks in a row, so a potion finishes on think 7.

`b = 0.1`. The brute starts drinking below 18.8% and stops above 26.1%. It first drinks at 17 (think 6), stays on the potion at 20 and 23 because both are under 26.1, and finishes it on think 8. Two switches.

`b = 0.15`. Start drinking needs `(1 − h)² > 0.6 × 1.15 = 0.69`, so `h < 1 − √0.69 = 16.9%`. Stop needs `h > 1 − √(0.6 / 1.15) = 27.8%`. The lowest health in the trace is 17%, just above the start threshold, so the brute never drinks. The bonus bought perfect stability by delaying the decision past anything the fight produced. Size `b` from the noise in the input, here swings of about 5 points, not from how calm the NPC should look.
</details>

34. *Week 8 · compute.* An NPC's actions score 0.50, 0.30, 0.15 and 0.05, and it thinks once per second.
   (a) Under weighted random selection, how many times do you expect the 0.05 action in a 90-second fight?
   (b) Under "roll only among actions within 20% of the best", how many? What about "within 50% of the best", and what is the chance of the second action then?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 4.5 times. (b) 0 times; within 50%, the second action has a 37.5% chance.

(a) The chance is `0.05 / (0.50 + 0.30 + 0.15 + 0.05) = 5%`, and `0.05 × 90 = 4.5`. Some of those will be at the worst possible moment, Graham's "utterly stupid" choice.

(b) Within 20% means at least `0.8 × 0.50 = 0.40`. Only the best action qualifies, so the NPC is deterministic in this situation. Within 50% means at least 0.25, which admits 0.50 and 0.30. The second action's chance is `0.30 / 0.80 = 37.5%`. The filter width sets how often the NPC surprises the player, and every surprise must still be defensible.
</details>

## Week 9: GOAP

35. *Week 9 · compute.* A designer raises AttackFromCover from 2 to 5 in the lecture's soldier table and leaves everything else alone. Give the new plan and cost for the worlds "loaded, ammo, cover" and "empty, ammo, cover". What happened to the soldier's personality?

<details>
<summary>Answer and worked solution</summary>

**Answer.** Loaded, ammo, cover: AttackInOpen, cost 6. Empty, ammo, cover: Charge then Melee, cost 7. The cautious soldier became reckless in exactly the worlds where it has cover.

Loaded with cover. Cover then attack now costs `2 + 5 = 7`. AttackInOpen costs 6. Charge and Melee cost 7. The open attack wins.

Empty with ammo and cover. GoToCover, Reload, AttackFromCover costs `2 + 2 + 5 = 9`. Reload then AttackInOpen costs 8. Charge and Melee cost 7. The knife charge wins.

No soldier uses cover in any world any more, and nobody wrote a rule saying so. One cost changed and the planner rerouted in worlds the designer was not looking at. A regression table of all eight worlds, as in Lab 09, catches this before a playtester does.
</details>

36. *Week 9 · trace.* Run the lecture's planner on the world "empty gun, ammo, no cover". List the states it expands in order with their `g` and `f`, and explain why the last expanded state is not part of the plan.

<details>
<summary>Answer and worked solution</summary>

**Answer.** Four expansions: the start (`g = 0`, `f = 1`), after Reload (`g = 2`, `f = 3`), after Charge (`g = 4`, `f = 5`), and after Reload then Charge (`g = 6`, `f = 7`). The plan is Charge then Melee, cost 7.

From the start, only Reload (`f = 2 + 1 = 3`) and Charge (`f = 4 + 1 = 5`) lead to new states. FetchAmmo leads back to the start, which is closed. Expanding "after Reload" pushes AttackInOpen at `f = 8` and Charge at `f = 2 + 4 + 1 = 7`. Expanding "after Charge" pushes Reload at `f = 7` and Melee at `f = 7 + 0 = 7`.

Three entries now share `f = 7`. The push counter breaks ties, so the earliest pushed comes out first: Reload then Charge, pushed during the second expansion. It is expanded (fourth), although it cannot reach the goal cheaper than 7. Next comes Charge then Reload, which is the same set of true facts and is skipped as closed. Then Charge then Melee pops, the goal holds, and the planner returns cost 7 with 4 expansions. A tie on `f` costs extra work but never a worse plan, because the heuristic is admissible.
</details>

37. *Week 9 · compute.* Use the lecture's door actions (OpenDoor 1, KickDoor 3, WalkThroughDoor 1, DiveThroughWindow 5).
   (a) Only OpenDoor fails. List the plans, their costs and the actions the soldier attempts.
   (b) Now DiveThroughWindow costs 3, and again only OpenDoor fails. What changes, and what would a player notice?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) Plan 1: OpenDoor, WalkThroughDoor (2). Plan 2: KickDoor, WalkThroughDoor (4). Attempts: OpenDoor, KickDoor, WalkThroughDoor. (b) The second plan becomes DiveThroughWindow (3), so the soldier never tries to kick.

(a) After OpenDoor fails, the soldier learns `door_jammed`, which blocks OpenDoor. The cheapest remaining plans are kick and walk at 4 or dive at 5. Kicking succeeds, and the soldier walks through.

(b) With the window at 3, the second plan compares kick and walk (4) with dive (3), and dives. The soldier gives up on a door it could have kicked open. A player holding the door sees the enemy go straight for the window after one push. That may be the intended "clever" behavior or may read as a soldier who never fights for a door, depending on what the level is for. One cost decided it.
</details>

38. *Week 9 · critique.* In the lecture's table, FetchAmmo (cost 5) is never used in any of the eight worlds.
   (a) In the world "empty gun, no ammo, cover", what does the FetchAmmo route cost as a function of its cost `F`? Is there any whole-number `F ≥ 1` for which the soldier fetches ammo?
   (b) Name two data changes that bring the action back into play, and one risk of each.
   (c) The designer then adds two facts, `has_grenade` and `grenade_primed`. At most how many world states are there?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) `F + 6`; no whole number works. (b) For example, raise Charge to at least 9, or give Melee a precondition. (c) 256.

(a) FetchAmmo, Reload, GoToCover, AttackFromCover costs `F + 2 + 2 + 2 = F + 6`, against Charge and Melee at 7. At `F = 1` both cost 7. Running the lecture's planner confirms that the tie goes to Charge then Melee, because its states were pushed earlier. Without cover, the fetch route costs `F + 2 + 6 = F + 8`, which never wins. FetchAmmo is a dead action, and a planner will let you ship it.

(b) Raise Charge to 9 or more. In "empty, no ammo, cover" the fetch route (11) then beats the knife (`9 + 3 = 12`), and the planner returns GoToCover, FetchAmmo, Reload, AttackFromCover. At Charge 8 both cost 11 and the tie still goes to the knife. The risk is every other world that used Charge. "Empty, ammo, no cover" now reloads and fires in the open (8) instead of charging, and "empty, no ammo, no cover" still charges but at cost 12. Rerun the regression table. Or give Melee a precondition such as `enemy_unarmored`. Against armored enemies the knife disappears, and both no-ammo worlds fetch ammo (costs 11 and 13). The risk is a world with no plan at all when the fetch route is also blocked, for example a level with no ammo crate.

(c) The lecture's soldier has 6 facts, so `2^6 = 64` states at most. Two more facts give `2^8 = 256`. Keep facts coarse and push expensive questions into procedural preconditions, as Orkin did.
</details>

## Week 10: Perception systems

39. *Week 10 · compute.* Use the lecture's parameters (`T_near = 1` s, `T_far = 4` s, `R = 20` m, `F = 6` s). A player stands 8 m from a guard in 80% light.
   (a) What is the fill time?
   (b) What is the break-even exposure `f*`?
   (c) If the player hides for 2 s at a time, how long can each peek last without the meter ever climbing?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 2.75 s. (b) 31.4%. (c) 0.92 s.

(a) `T = (1 + 3 × 8 / 20) / 0.8 = 2.2 / 0.8 = 2.75` s.

(b) `f* = T / (T + F) = 2.75 / 8.75 = 31.4%`.

(c) The meter holds steady when each peek adds no more than each hide removes: `e / T = h / F`, so `e = h × T / F = 2 × 2.75 / 6 = 0.92` s. Check the share: `0.92 / 2.92 = 31.4%`, exactly `f*`.
</details>

40. *Week 10 · code.* This uses the lecture's `detect_time` and `first_detection` from section 2. What does it print? Explain the second number by hand.

```python
# Uses the week 10 lecture's definitions from section 2.
print(detect_time(15))
print(first_detection([(1.0, True), (1.5, False)], 15))
print(first_detection([(1.0, True), (1.5, False)], 15, forget=8.0))
```

<details>
<summary>Answer and worked solution</summary>

**Answer.**

```
3.25
31.0
16.0
```

At 15 m, `T = 1 + 3 × 15 / 20 = 3.25` s. The pattern exposes the player 1 s in every 2.5 s, a 40% share, above `f* = 3.25 / 9.25 = 35.1%`, so the meter climbs.

Each peek adds `1 / 3.25 = 0.3077`. Each 1.5 s hide removes `1.5 / 6 = 0.25`. The meter never reaches 0 between peeks, so it gains `0.0577` per cycle. After `k` peeks and `k − 1` hides it stands at `k / 3.25 − (k − 1) × 0.25`. At `k = 13` that is `4 − 3 = 1` exactly, at the end of the 13th peek, `12 × 2.5 + 1 = 31.0` s. The lecture's code counts `meter ≥ 1 − 1e−9` as full, so floating-point rounding cannot push the detection one tick later.

With `F = 8`, each hide removes only 0.1875 and the meter climbs 0.1202 per cycle. Detection comes during the 7th peek, at 16.0 s. A longer memory nearly halved the time this peeking player survives, with no change to the guard's eyes.
</details>

41. *Week 10 · compute.* At a certain spot the fill time is `T = 3` s. The designer wants a player who is exposed 2 s out of every 5 s to be safe forever, and one exposed 2 s out of every 4 s to be caught eventually. What range of forget times `F` does this, and what happens at the edges?

<details>
<summary>Answer and worked solution</summary>

**Answer.** `3 < F ≤ 4.5` s.

Safe forever needs `f ≤ T / (T + F)`. With `f = 2/5`: `0.4 ≤ 3 / (3 + F)`, so `3 + F ≤ 7.5`, `F ≤ 4.5`. Caught eventually needs `f > T / (T + F)`. With `f = 1/2`: `0.5 > 3 / (3 + F)`, so `3 + F > 6`, `F > 3`.

Check `F = 4`. The 2-in-5 player gains `2/3 = 0.667` per peek and loses `3/4 = 0.75` per hide: safe. The 2-in-4 player gains 0.667 and loses 0.5: the meter climbs 0.167 per cycle. At `F = 4.5` the careful player sits exactly on break-even, and at `F = 3` the careless one does. Pick a value inside the range, not on its edge, so that small timing noise in a real player's rhythm does not decide the outcome.
</details>

42. *Week 10 · compute.*
   (a) A footstep with a 12 m radius happens at `(0, 0)`. A guard stands at `(10, 0)` behind a wall whose only gap is at `(5, 6)`. Is it heard with straight-line distance? With path distance? The guard is off-screen and far, so Blacklist's rule halves the radius. Is it heard then?
   (b) A level has 24 active agents that can all see each other. How many raycasts does a full agent-to-agent visibility check need?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) Straight line: heard (10 m). Path: not heard (15.62 m). Halved radius: not heard either way. (b) 276.

(a) Straight line: `10 < 12`, heard. Path: `2 × √(25 + 36) = 15.62 > 12`, not heard. With the off-screen rule, the radius drops to 6, and even the 10 m straight line is too far. The path test stops the through-wall cheat. The off-screen rule is a deliberate cheat in the player's favor for detections the player could not have seen coming.

(b) Each pair needs one ray: `24 × 23 / 2 = 276`. Welsh's example gives 120 for 16 agents. The count grows with the square of the agent count, which is why Crytek filtered targets first and ran raycasts asynchronously, hiding the frame or two of delay inside a fill time of a second or more.
</details>

## Week 11: Group tactics and formations

43. *Week 11 · compute.* Use the lecture's fight: soldiers deal 10 damage per second while attacking, and the player kills one every 5 s.
   (a) Give the total damage from a pack of 9 with no grid, with a cap of 3 attackers (`C_g = 12`) and with a cap of 5 (`C_g = 20`).
   (b) The player has 1,500 health. Which of the three settings kill them?
   (c) With a cap of 3, what is the smallest pack that deals more than 1,500?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 2,250, 1,200 and 1,750. (b) No grid and the cap of 5. (c) 12 soldiers, 1,650 damage.

(a) Total damage is `50 × Σ min(n, c)` for `n` from 9 down to 1. No grid: `50 × 9 × 10 / 2 = 2,250`. Cap 3: the attackers go 3 seven times, then 2, then 1, which is 24, and `24 × 50 = 1,200`. Cap 5: 5 five times, then 4, 3, 2, 1, which is 35, so 1,750.

(b) 2,250 and 1,750 exceed 1,500. The cap of 3 leaves the player with 300.

(c) For `N ≥ 3` the capped total is `50 × [6 + 3(N − 3)] = 300 + 150(N − 3)`. It first exceeds 1,500 when `N − 3 > 8`, so `N = 12`, giving 1,650. At `N = 11` it is exactly 1,500. Each extra soldier past the cap adds a flat 150, so the fight gets longer, not more intense.
</details>

44. *Week 11 · code.* This uses the lecture's `StageManager` class. What does it print? What does the second troll do while it holds a slot but no attack?

```python
# Uses the week 11 lecture's StageManager class from section 2.
TROLL = [("charge", 6), ("club", 4)]
SOLDIER = [("lunge", 5), ("swing", 3)]
stage = StageManager(grid_capacity=20, attack_capacity=12)
pack = [("troll 1", 8, TROLL), ("soldier 1", 4, SOLDIER),
        ("troll 2", 8, TROLL), ("soldier 2", 4, SOLDIER)]
admitted = [(n, a) for n, w, a in pack if stage.request_slot(n, w)]
print("on grid:", [n for n, _ in admitted], "| grid left", stage.grid_free)
for name, attacks in admitted:
    print(name, "->", stage.choose_attack(name, attacks), "| attack left", stage.attack_free)
```

<details>
<summary>Answer and worked solution</summary>

**Answer.**

```
on grid: ['troll 1', 'soldier 1', 'troll 2'] | grid left 0
troll 1 -> charge | attack left 6
soldier 1 -> lunge | attack left 1
troll 2 -> None | attack left 1
```

Grid: troll 1 takes 8 of 20 (12 left), soldier 1 takes 4 (8 left), troll 2 takes 8 (0 left), and soldier 2 is refused. Attacks: troll 1 charges (6 of 12, 6 left), soldier 1 lunges (5, 1 left), and troll 2 cannot afford charge (6) or club (4), so it gets `None`.

Troll 2 holds a slot on the approach circle without attacking. It should visibly do something there, such as circling, roaring or feinting, until an attack ends and releases capacity. A troll that stands still next to the player for a whole round is the week 1 artificial stupidity. Dawe's rotation fixes the fairness side: after an attack, the attacker gives its slot back, so the waiting soldier gets a turn.
</details>

45. *Week 11 · compute.* A formation's anchor is at `(5, 5)` facing west (`θ = 180°`). Its slots have offsets `(−2, 0)`, `(2, 0)` and `(0, 2)`, written as (right, forward). Where are the three slots in the world?

<details>
<summary>Answer and worked solution</summary>

**Answer.** `(5, 3)`, `(5, 7)` and `(3, 5)`.

With `θ = 180°`, forward is `f = (cos 180°, sin 180°) = (−1, 0)`, and right is `r = (sin 180°, −cos 180°) = (0, 1)`. Facing west, your right hand points north (+y). Then `slot = anchor + right × r + forward × f`.

- `(−2, 0)`: `(5, 5) + (−2)(0, 1) = (5, 3)`.
- `(2, 0)`: `(5, 5) + 2(0, 1) = (5, 7)`.
- `(0, 2)`: `(5, 5) + 2(−1, 0) = (3, 5)`.

The first two form a line across the direction of travel and the third is the point man two meters ahead, to the west.
</details>

46. *Week 11 · compute.* Three units at `(4, 4)`, `(3, 4)` and `(1, 2)` must fill slots at `(0, 6)`, `(3, 6)` and `(6, 6)`.
   (a) Units pick in the order listed, each taking its nearest free slot. What is the assignment, its total distance, and does any pair of paths cross?
   (b) What is the assignment with the smallest total distance?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) `(4, 4) → (3, 6)`, `(3, 4) → (0, 6)`, `(1, 2) → (6, 6)`: 12.24 m, one crossing. (b) `(4, 4) → (6, 6)`, `(3, 4) → (3, 6)`, `(1, 2) → (0, 6)`: 8.95 m, no crossing.

(a) Unit `(4, 4)` is `√5 = 2.24` from `(3, 6)`, closer than `(6, 6)` at `√8 = 2.83`, so it takes `(3, 6)`. Unit `(3, 4)` is left with `(0, 6)` at `√13 = 3.61` and `(6, 6)` at 3.61. The tie goes to the first slot in the list, `(0, 6)`. Unit `(1, 2)` gets `(6, 6)`: `√41 = 6.40`. Total 12.24 m. The last unit's path runs from the lower left to the upper right and crosses the second unit's path.

(b) Trying all six orders, the best is `√8 + 2 + √17 = 2.83 + 2.00 + 4.12 = 8.95` m. As the lecture proves, the shortest total can never contain a crossing, because swapping two crossing paths always shortens the total. Greedy spent 37% more walking and made two units cut across each other.
</details>

47. *Week 11 · design.* A designer wants the Kung-Fu Circle, exactly one attacker at a time, for a pack of six sword-wielding cultists fighting the player in a narrow chapel.
   (a) Using the lecture's fight model (10 damage per second per attacker, one kill every 5 s), what total damage does the player take from the pack? How does that compare with no cap?
   (b) Give one risk of a cap of one that the numbers do not show, and one change that keeps the cap but reduces that risk.

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 300 against 1,050. (b) The five waiting cultists can look staged; keep them busy with visible actions or rotate attackers quickly.

(a) With one attacker at a time, every 5 s period deals `1 × 10 × 5 = 50`, and there are six periods: 300. With no cap, `50 × 6 × 7 / 2 = 1,050`, three and a half times more.

(b) A cap of one is readable and dramatic, but five enemies politely waiting their turn read as a stage show, the lecture's warning. Players notice the rule and stop believing the enemies. Keep the cap and make the waiting state active: cultists circle toward free slots (Reckoning's approach), throw daggers that do not use the melee token, or shout barks that telegraph the next attacker. Each keeps the one-at-a-time damage profile while the scene stays alive.
</details>

## Week 12: MMO mob AI

48. *Week 12 · compute.* Using the lecture's rule of thumb from Warcraft Wiki, what is the aggro radius for a level 60 player approaching mobs of level 40, 52, 58, 64 and 90?

<details>
<summary>Answer and worked solution</summary>

**Answer.** 5, 12, 18, 24 and 45 yards.

The rule is `max(5, min(45, 20 + (mob − player)))`. Level 40: `20 − 20 = 0`, raised to the 5-yard floor. Level 52: `20 − 8 = 12`. Level 58: `18`. Level 64: `24`. Level 90: `20 + 30 = 50`, capped at 45.

The shape carries the design. A high-level player walks past weak mobs almost untouched, since 5 yards is melee range, and a low-level player is warned away from a dangerous zone from 45 yards.
</details>

49. *Week 12 · compute.* A tank deals `d = 300` damage per second with multiplier `m = 1.5`. The boss hits the tank for `B = 1,500` per second, and the healer heals exactly that from second 2.
   (a) What is the healer margin `S`, and the smallest safe multiplier `m*`?
   (b) In the lecture's `healer_pull` model, in which second does the boss turn to the healer?
   (c) Two mobs are in combat instead of one. Recompute `S`.

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) `S = 0.78`, `m* = 1.92`. (b) Second 5. (c) `S = 1.56`, and the boss never turns.

(a) `S = 2.6 × m × d × N / B = 2.6 × 1.5 × 300 / 1,500 = 0.78`. `m* = B / (2.6 × d × N) = 1,500 / 780 = 1.92`.

(b) The tank gains `1.5 × 300 = 450` per second from second 1. The healer gains `0.5 × 1,500 = 750` per second from second 2. At second `t` the healer has `750(t − 1)` and the tank `450t`. The ranged healer takes the boss when `750(t − 1) > 1.3 × 450t = 585t`, so `165t > 750`, `t > 4.55`. First whole second: 5. Check: at `t = 5` the healer has 3,000 and `1.3 × 2,250 = 2,925`. Running `healer_pull(1.5, boss_dps=1500, tank_dps=300)` returns 5.

(c) Healing threat is split between the mobs, so the healer's rate on each halves and `S` doubles to 1.56. `healer_pull(..., mobs=2)` returns `None`. The catch from the lecture applies: the healer's threat also lands on the second mob, so the tank must hold it too.
</details>

50. *Week 12 · code.* This uses the lecture's `ThreatTable` class. The tank and rogue are in melee, the healer at range. What do the four `print` calls show? Explain the last one.

```python
# Uses the week 12 lecture's ThreatTable class from section 2.
t = ThreatTable()
melee = {"tank", "rogue"}
for who, amount in [("tank", 500), ("rogue", 300), ("healer", 200)]:
    t.add(who, amount)
print(t.choose(melee))
t.add("rogue", 260)            # rogue 560, tank 500
print(t.choose(melee))
t.add("healer", 460)           # healer 660
print(t.choose(melee))
t.add("tank", 120)             # tank 620
print(t.choose(melee), t.threat)
```

<details>
<summary>Answer and worked solution</summary>

**Answer.**

```
tank
rogue
rogue
tank {'tank': 620, 'rogue': 560, 'healer': 660}
```

First call: no target yet, so the highest threat, the tank at 500, becomes the target with no threshold.

Second: the rogue at 560 is in melee and needs more than 110% of 500. `5,600 > 5,500`, so the rogue takes the boss.

Third: the healer at 660 is at range and needs more than 130% of the rogue's 560, which is 728. It is not enough. The tank at 500 is below the rogue. The rogue keeps the boss.

Fourth: the tank reaches 620, and `6,200 > 11 × 560 = 6,160`, so the tank takes it back. The healer has the most threat on the table, 660, and is not the target. The rule compares each challenger with the current target, not with the top of the table, and the healer's ranged threshold is measured against whoever holds aggro now. Threat order and target order are different things, which is one reason addons that show the 110% and 130% lines exist.
</details>

51. *Week 12 · compute.* In question 49's fight (`m = 1.5`, one mob), the tank taunts at second 5, the moment the boss turns to the healer. The taunt sets the tank's threat equal to the healer's and forces the target for 3 s. When does the healer take the boss again? What does this say about taunts when `S < 1`?

<details>
<summary>Answer and worked solution</summary>

**Answer.** Six seconds after the taunt, at second 11.

At second 5 the healer has 3,000, so the taunt sets the tank to 3,000. After `s` more seconds the healer has `3,000 + 750s` and the tank `3,000 + 450s`. The healer retakes the boss when `3,000 + 750s > 1.3 × (3,000 + 450s) = 3,900 + 585s`, so `165s > 900`, `s > 5.45`. At `s = 6`, `7,500 > 7,410`. At `s = 5`, `6,750 < 6,825`. The 3 s forced target ends first, so it does not matter.

A taunt resets who is on top. It does not change the slopes. With `S < 1` the healer's line is steeper than 1.3 times the tank's, so the healer wins every race, and the tank would need to taunt every 6 s. The fix is on the slope: raise `m` or `d`, lower `B`, or add mobs that split the healing threat.
</details>

52. *Week 12 · critique.* A designer proposes: "Open-world mobs leash at 60 m from wherever they were last hit, and evade by walking home at normal speed while still attacking anyone in reach." Find two problems with numbers or concrete exploits, and propose a fix for each.

<details>
<summary>Answer and worked solution</summary>

**Answer.** Resetting the leash on each hit allows kiting across the map. Attacking while walking home allows training and griefing.

Problem 1. Measuring from the last hit is the classic-era rule the lecture lists. A player who hits the mob every 50 m can drag it indefinitely, across zones and into other players. Fix: measure the leash from the spawn point, or from where combat started, and never reset it on damage. Running always escapes, and kiting is capped at the leash distance.

Problem 2. An evading mob that still attacks can be led through a crowd. Every player it passes is hit and pulled into combat, which is training, the exploit leashing exists to block. It also lets a player fight a mob that is walking away without fighting back fully. Fix: during EVADE the mob ignores everyone, is immune to damage, regenerates, and runs home faster than it walks. The immunity is visible and consistent, so players read it as a rule, not a cheat.
</details>

## Week 13: Boss AI and scripted encounters

53. *Week 13 · compute.* A group deals 2,500 DPS against the lecture's Warden (`H = 600,000`, enrage 360 s).
   (a) When does the Warden die?
   (b) How many times does each ability fire under HP gates?
   (c) Under the lecture's time gates?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 240 s. (b) Summon adds 2, Meteor 1, Firestorm 3. (c) Summon adds 3, Meteor 2, Firestorm 1.

(a) `600,000 / 2,500 = 240` s, well inside the enrage.

(b) HP-gated phases last `H_i / D`. P1 lasts `240,000 / 2,500 = 96` s: Summon at 20 and 65, but not 110. P2 lasts `180,000 / 2,500 = 72` s: Meteor at 40, but not 80. P3 lasts 72 s: Firestorm at 15, 40 and 65.

(c) Time gates fix P1 at 0 to 120 s and P2 at 120 to 210 s, and P3 starts at 210 s. Summon fires at 20, 65 and 110. Meteor at 160 and 200. Firestorm at 225 only, since the next would be at 250, after the kill at 240.

Running the lecture's `hp_gated(2_500)` and `time_gated(2_500)` returns `[2, 1, 3]` and `[3, 2, 1]`. The HP-gated fight shows every phase briefly. The time-gated fight shows the opening in full and clips the ending.
</details>

54. *Week 13 · compute.* In the HP-gated Warden, each cast after the first also has a skip threshold, the DPS at or above which it is lost.
   (a) Give the thresholds for Summon adds' second and third casts and Meteor's second cast.
   (b) At the design DPS of 2,000, how many Meteors does a group see? At 2,300?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 3,692, 2,182 and 2,250 DPS. (b) Two at 2,000; one at 2,300.

(a) A cast at phase time `t` is lost once `t ≥ H_i / D`, that is `D ≥ H_i / t`. Summon's second cast at 65 s: `240,000 / 65 = 3,692`. Its third at 110 s: `240,000 / 110 = 2,182`. Meteor's second at 80 s: `180,000 / 80 = 2,250`.

(b) At 2,000 DPS, P2 lasts 90 s, so Meteor fires at 40 and 80. At 2,300 DPS, P2 lasts `180,000 / 2,300 = 78.3` s and the second Meteor is gone. From 2,250 DPS, only 12.5% above design, a group sees half the signature mechanic. The first Meteor survives until 4,500.
</details>

55. *Week 13 · compute.* The Warden runs with the lecture's guard: P2 cannot end before `40 + 5 = 45` s of phase time, so Meteor always fires once. A group deals 5,000 DPS.
   (a) How long is each phase, and when does the Warden die? Compare with no guard.
   (b) How much of the group's damage is wasted while the boss is held, as a share of its health?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 48 s, 45 s and 36 s; the kill comes at 129 s instead of 120 s. (b) 45,000 damage, 7.5% of the Warden's health.

(a) P1 lasts `240,000 / 5,000 = 48` s. P2's HP would be gone after 36 s, but the guard holds it until 45 s, and Meteor fires at 40 s. P3 lasts 36 s. Total `48 + 45 + 36 = 129` s. Without the guard the kill comes at `600,000 / 5,000 = 120` s and Meteor never fires, since 5,000 is above its 4,500 threshold.

(b) The boss is held at 30% for `45 − 36 = 9` s, and the group's damage in that time does nothing: `9 × 5,000 = 45,000`, which is `45,000 / 600,000 = 7.5%` of total health. That is the price of the guarantee. Strong groups see the mechanic, and they also see their damage bounce off a boss that will not drop, which can feel like the game is cheating. Show it: an invulnerability shield or a line of dialogue makes the hold readable.
</details>

56. *Week 13 · compute.*
   (a) A raid boss has 1,200,000 health and an enrage at 8 minutes. What DPS must the group sustain?
   (b) A phase covers 300,000 health. Its signature ability's first cast lands at `30 ± 5` s (jitter). Over what DPS range can the first cast be skipped?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 2,500 DPS. (b) From 8,571 to 12,000 DPS.

(a) `D_min = H / E = 1,200,000 / 480 = 2,500`.

(b) With jitter the first cast lands between 25 and 35 s. The phase lasts `300,000 / D`. The cast is lost if it lands at or after that. It can be lost as soon as the phase is shorter than 35 s, at `300,000 / 35 = 8,571` DPS, and it is always lost when the phase is 25 s or shorter, at `300,000 / 25 = 12,000` DPS. Between the two, whether the group sees it depends on the roll, which makes the skip threshold a probability rather than a cliff.
</details>

57. *Week 13 · compute.* The lecture's Ragnaros rule: after 3 minutes of combat he submerges and summons 8 adds, and returns after 90 s or when all 8 adds are dead, whichever comes first.
   (a) A raid kills one add every 12 s. How long is he submerged, which rule fires, and how many adds are dead when he returns?
   (b) A raid strong enough to kill him in 170 s. What does it see of the submerge phase?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 90 s; the timer fires; 7 adds are dead. (b) Nothing.

(a) Eight adds at one every 12 s would all be dead at 96 s. The 90 s timer fires first. By 90 s the raid has killed adds at 12, 24, ..., 84 s, which is 7, and the eighth is still alive when he returns.

(b) The submerge is time-gated at 180 s. A kill at 170 s comes first, so the raid never sees the phase, exactly like the time-gated Warden's later phases. The event gate only shortens a phase that has already started.
</details>

## Week 14: Performance, AI LOD and time-slicing

58. *Week 14 · compute.* A town has 800 NPCs with a 50 µs think and a 2.5 ms AI budget per frame at 60 fps.
   (a) Under the budgeted round robin, how many NPCs think per frame, and how long does each wait between thinks?
   (b) The 25 NPCs nearest the player become a near tier that thinks every frame. What is the far wait now?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 50 per frame; 16 frames, 266.7 ms. (b) 31 frames, 516.7 ms.

(a) `k = floor(2,500 / 50) = 50`. Wait `ceil(800 / 50) = 16` frames, and `16 × 16.667 = 266.7` ms.

(b) The near tier costs `25 × 50 = 1,250` µs, leaving 1,250 µs for `k_far = 25` far thinks per frame. The far wait is `ceil(775 / 25) = 31` frames, 516.7 ms. The 25 near NPCs react within one frame, and the other 775 wait more than half a second. That is fine for a baker across town and not fine for a guard the player can see across the square.
</details>

59. *Week 14 · compute.* A game has 1,000 agents with a 30 µs think at 60 fps.
   (a) The designer wants every agent to react within 150 ms. What budget does that need, and what share of a 16.7 ms frame is it?
   (b) Only the 40 agents near the player need 150 ms; the rest may take 1 s. What budget does a two-tier scheduler need?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 3,360 µs, about 20% of the frame. (b) 1,680 µs.

(a) 150 ms is 9 frames. Every agent must think once per 9 frames, so `k = ceil(1,000 / 9) = 112` thinks per frame and `B = 112 × 30 = 3,360` µs. That is `3.36 / 16.7 = 20%` of the frame, far above a typical AI share.

(b) The near tier thinks every frame, which is faster than 150 ms requires but is the lecture's near-tier rule: `40 × 30 = 1,200` µs. The 960 far agents need one think per 60 frames: `ceil(960 / 60) = 16` per frame, 480 µs. Total `1,680` µs, half of (a), and the near agents get a 16.7 ms reaction instead of 150 ms. The lecture's advice, "pick the budget from the wait you can accept", works per tier.
</details>

60. *Week 14 · code.* This uses the lecture's `sliced_search`, `zero` and `manhattan` from section 3, on week 4's wall map. What does it print? Why does A* at 31 steps per frame need 2 frames, not 1?

```python
# Uses the week 14 lecture's definitions from section 3.
S, G = (4, 0), (4, 11)
for name, h in [("Dijkstra", zero), ("A*", manhattan)]:
    for budget in (10, 16, 31):
        frames = sum(1 for _ in sliced_search(S, G, h, budget))
        print(f"{name:8} {budget:>2} per frame: answer on frame {frames}")
```

<details>
<summary>Answer and worked solution</summary>

**Answer.**

```
Dijkstra 10 per frame: answer on frame 10
Dijkstra 16 per frame: answer on frame 6
Dijkstra 31 per frame: answer on frame 3
A*       10 per frame: answer on frame 4
A*       16 per frame: answer on frame 2
A*       31 per frame: answer on frame 2
```

Every generator step is one frame, and the answer arrives on frame `ceil(expanded / steps_per_frame)`. Dijkstra closes 91 cells: `ceil(91 / 10) = 10`, `ceil(91 / 16) = 6`, `ceil(91 / 31) = 3`. A* closes 32: `ceil(32 / 10) = 4`, `ceil(32 / 16) = 2`, `ceil(32 / 31) = 2`.

At 31 per frame, A* does 31 expansions on frame 1 and pauses. The goal is the 32nd cell closed, so it comes off the heap on frame 2. One more step per frame (32) would answer on frame 1, as the lecture's run shows. Under the same budget, A* answers three times sooner than Dijkstra at 10 steps per frame. A better heuristic is less delay, not only less CPU.
</details>

61. *Week 14 · compute.*
   (a) 450 agents with a 60 µs think each want to think every 5th frame. Give the worst frame and average cost for "all at once" and for "staggered".
   (b) RimWorld's long tick runs every 2,000 ticks at 60 ticks per second. How long can a pawn wait for a check that runs on the long tick?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) All at once: 27.0 ms worst, 5.4 ms average. Staggered: 5.4 ms both. (b) About 33.3 s.

(a) All at once: `450 × 60 = 27,000` µs on one frame in five, longer than the whole 16.7 ms frame, so the game hitches 12 times a second. The average `27,000 / 5 = 5,400` µs hides that completely. Staggered: `450 / 5 = 90` agents per frame, `90 × 60 = 5,400` µs every frame. Same work, same wait, no spike.

(b) `2,000 / 60 = 33.3` s. That is invisible for a slow process, such as a plant growing, and absurd for anything a player expects a pawn to notice within a few seconds.
</details>

## Week 15: The NPC ecosystem (synthesis)

62. *Weeks 10 and 14 · compute.* In a student's ecosystem, a guard's reaction to seeing the player passes through three stages: perception runs at 10 Hz, thinks run under a plain budget with a 200 ms wait, and the attack animation has a 250 ms wind-up before the first hit.
   (a) What is the worst-case delay from the player stepping into view (with the meter already full) to the first hit?
   (b) The guard is moved into a near tier that thinks every frame at 60 fps. What is the new worst case?
   (c) Compare both with the week 1 reaction figures. Which stage would you cut first, and which would you keep?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 550 ms. (b) About 367 ms. (c) Both are slower than a human reacting to a simple event; cut the think wait first and keep the wind-up.

(a) Up to 100 ms before the next perception update, up to 200 ms before the next think, then 250 ms of wind-up: `100 + 200 + 250 = 550` ms.

(b) The think wait drops to one frame, 16.7 ms: `100 + 16.7 + 250 = 366.7` ms.

(c) Rabin's figures are about 200 ms for a simple reaction and 400 ms when a comparison is needed. The near-tier guard lands inside that range, and the far-tier one is slower than a thinking human. The wind-up is the telegraph that makes the attack readable and beatable, so it stays. The think wait is invisible cost that only makes the guard look slow, so the near tier is the right fix. The lecture's warning holds: delays stack, so budget the total, not each stage alone.
</details>

63. *Weeks 6 to 9 · design.* Your ecosystem has three NPC types: villagers who follow a daily schedule and react to danger, a wolf pack that hunts livestock at night, and a watch captain who must decide between chasing a thief, protecting a merchant and calling for reinforcements. Choose a decision method for each, using the week 9 comparison table, and give one number you will tune for each.

<details>
<summary>Answer and worked solution</summary>

**Answer.** One defensible answer: villagers use a state machine, the wolves a behavior tree with a group token, and the captain utility scoring. Other choices earn full marks if each is tied to the table.

Villagers have few modes (work, eat, sleep, flee) and must be readable at a glance, which is where a state machine is strongest. Tune the flee transition with a commitment time from week 6, for example `L` chosen so that a villager who flees keeps fleeing for at least 3 s after the last scare. That stops the dithering a single threshold causes when a wolf circles at the edge of the flee radius.

Wolves run ordered steps with fixed priorities (flee when hurt, attack when the pack has a token, stalk, roam), so a behavior tree with the hybrid tick rule fits. Tune the attack token capacity with the week 11 damage model, so that a pack of six takes a sheep in about the time a player needs to notice and respond.

The captain's priorities slide with the situation, so utility scoring fits. Tune the switch point between "chase thief" and "protect merchant" as a function of the merchant's danger, and add a commitment bonus sized from the noise in the danger input, as in week 8.

A planner would suit none of these as well. None needs to invent an order of steps at run time, and a planner's plans need reviewing that a three-week project cannot afford.
</details>

64. *Weeks 2, 4, 10 and 14 · critique.* A milestone 1 proposal reads: "Our wolves path on an 8-way grid with octile distance. Roads cost half as much as grass. Our guards detect the player instantly inside a 30° cone. All 300 NPCs think every frame, at about 40 µs each. Wolves seek their prey and stop when they reach it." Find four problems. Give a number for each where you can, and a fix.

<details>
<summary>Answer and worked solution</summary>

**Answer.** An inadmissible heuristic on roads, a detection rule with no window, a 12 ms AI frame, and seek used for stopping.

The heuristic. Octile distance assumes every step costs at least the base cost. Road steps cost half, so along a road the heuristic overestimates by a factor of 2, and A* can walk wolves past a road that is faster (the week 4 road map returned 19 instead of 16). Fix: scale octile by 0.5, the cheapest terrain factor, or precompute a road-aware heuristic.
Instant detection. With no meter, the break-even exposure is 0, so any glimpse is a detection. Peeking never works, the player gets no warning, and the guard fails the readable and beatable tests. Fix: a fill-and-drain meter with a suspicious state, for example `T_near = 1` s and a forget time chosen from `f*` at the distances the level uses.
The budget. `300 × 40 = 12,000` µs is 12 ms, 72% of a 16.7 ms frame, before rendering or physics. Fix: stagger at least, and better a budget with a near tier. With 2 ms and a 20-NPC near tier, `k_far = 30` and the far wait is `ceil(280 / 30) = 10` frames, 167 ms.
Seek to stop. Seek overshoots by `b = v² / (2a)` and orbits a stationary target. A wolf with 8 m/s and 16 m/s² overshoots its prey by 2 m and circles it. Fix: arrive with a slowing radius of at least `b = 2` m, and a stopping distance.
</details>
