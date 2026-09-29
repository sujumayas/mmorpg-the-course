# CS203 · Week 14 — Performance: AI LOD and time-slicing

**Why this matters:** Every technique in this course costs CPU time, and the AI gets a small slice of each frame. When 600 agents all decide to think on the same frame, the player sees a hitch. When you fix that by making them take turns, the player sees enemies that react late. This week you learn to trade one for the other on purpose, with numbers, and to spend the savings on the agents the player is actually watching.

**You will be able to:**
- Compute the worst-frame cost, average cost and worst reaction delay of an AI update policy from the agent count, the cost of a think, the frame length and the budget.
- Implement a budgeted round-robin scheduler with a priority tier, and a time-sliced A* that pauses when its per-frame step budget runs out.
- Derive the delay each tier of agents pays under a fixed budget, and pick a budget and tier split for a given scene.
- Critique an AI level-of-detail (LOD) plan by naming what each tier gives up and whether the player can see it.

**Before class:** Millington, *AI for Games* (3rd ed., 2019), chapter 9 "Execution management" (scheduling, anytime algorithms and level of detail). Sunshine-Hill, B., "Phenomenal AI Level-of-Detail Control with the LOD Trader", *Game AI Pro* (2013), chapter 14, sections 1 to 3 (free online at gameaipro.com). Skim the comments in the `path_finder` block of Factorio's `map-settings.lua` (linked in Sources).

**Prerequisites from earlier courses:** [CS101 week 9, delta time and frame-rate independence](../../CS101-programming-for-games-i/lectures/w09-delta-time-and-frame-rate-independence.md) (what a frame is and why 60 fps means 16.7 ms). [CS102 week 4, Big-O intuition](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w04-big-o-intuition-for-game-developers.md) (cost that grows with the number of agents). [CS102 week 6, queues and stacks](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w06-queues-and-stacks-undo-and-command-buffers.md) (the round-robin queue). [CS203 week 4, A* and heuristics](w04-a-star-and-heuristics.md) (the search you will time-slice). [CS203 week 10, perception systems](w10-perception-systems.md), whose update rate is the first thing LOD cuts. If you take CS202 this semester, its [week 13 on tick rate and bandwidth budgets](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w13-tick-rate-and-bandwidth-budgets.md) shows that a server tick is a CPU budget too.

**Interactive:** [`examples/w14-frame-budget.html`](../examples/w14-frame-budget.html). Keep it open during section 2.

---

## 1. The AI's slice of a frame

At 60 frames per second, a frame lasts `1000 / 60 = 16.7` ms. Everything happens inside it: input, physics, animation, audio, rendering, networking and AI. The AI does not get the whole frame. A common working rule on a team is to give it a fixed **budget**, a number of milliseconds per frame that the AI must not exceed. In this lecture the budget is 2 ms, about 12% of the frame. Your project's number will differ. The method will not.

Two measurements matter, and they are not the same.

- The **average cost** is the total AI time over a second divided by the number of frames. It tells you whether the AI fits at all.
- The **worst-frame cost** is the most expensive single frame. It tells you whether the player sees a **hitch**, a frame that takes visibly longer than its neighbors. A game that averages 2 ms of AI but spends 24 ms on one frame in six stutters ten times a second, and every player notices.

The tools in this lecture all move work between frames. None of them makes a think cheaper. That is the key to reading them. When you move work later, somebody waits. The question is always who waits, for how long, and whether the player can tell.

A few terms before the worked example.

- A **think** is one agent's decision update: read perception, run its state machine, behavior tree or utility scores, and pick an action. Movement along an existing path is cheaper and usually runs every frame. In this lecture, "think" means the expensive part.
- The **think cost** `c` is the CPU time of one think, measured with a profiler. We use `c = 40 µs` (0.04 ms).
- The **wait** of an agent is the number of frames between two of its thinks. It adds directly to the agent's reaction time. If the player steps into view just after a guard has thought, the guard cannot react until its next think.
- **Time-slicing** means spreading work across frames on purpose: some agents think this frame, the others next frame, or one long job does a little work each frame.
- **AI level of detail (LOD)** means giving different agents different amounts of AI work, usually by how much the player can see of them.

## 2. Worked example: 600 guards and a 2 ms budget

### The hook

Factorio runs its simulation at 60 ticks per second, and its enemies, the biters, find their way to the player's factory with a pathfinder. The game's own configuration file limits that pathfinder. In the `path_finder` block of `map-settings.lua` (Factorio 2.x), the setting `max_steps_worked_per_tick` is 1,000, with the comment that this is how many nodes can be expanded at most per tick. A longer search simply continues on the next tick. The same block raises the limit by 2×, 3× or 4× when the number of waiting requests exceeds 0, 100 or 500.

So when a large attack wave asks for paths at once, the frame rate is protected. What the player gets instead is a little time before the last biter starts moving. The developers chose delay over hitches, and wrote the exchange rate into a config file.

Here is the same choice in a scene you control. A fortress holds 600 guards, each with a 40 µs think. The designers want every guard to think about 10 times a second, every 6th frame at 60 fps. Four ways to schedule them, one total amount of work. Which is best?

### The model

Name the quantities.

- `N` agents, each costing `c` µs per think.
- A frame of `F` µs (16,667 at 60 fps) and an AI budget of `B` µs per frame.
- A desired think period of `P` frames (here 6).

**All at once.** Every agent thinks on the same frame, once every `P` frames.

```
worst frame = N × c        average = N × c / P        wait = P frames
```

**Staggered.** Agent `a` thinks on frames where `(frame + a) mod P = 0`. Each frame serves about `N / P` agents.

```
worst frame ≈ average = N × c / P                     wait = P frames
```

**Budgeted round robin.** Keep the agents in a queue. Each frame, take agents from the front and let them think until the budget is spent, then put them at the back. The number served per frame is

```
k = floor(B / c)
```

and every agent waits for the whole queue to come round:

```
worst frame ≤ B                                       wait = ceil(N / k) frames
```

**Budgeted with a near tier (LOD).** Mark `m` agents as near the player. They think every frame. The rest share what is left:

```
k_far = floor((B − m × c) / c)
wait_near = 1 frame                                   wait_far = ceil((N − m) / k_far) frames
```

The first two policies have a fixed wait and a cost that grows with `N`. The budgeted policies have a fixed cost and a wait that grows with `N`. That exchange is the whole lesson. **A budget turns CPU cost into delay.**

### The code

This program runs all four policies for two seconds of frames and measures the worst frame, the average and the longest wait each agent sees. Times are integer microseconds, so there is no rounding to worry about until the print.

```python
FRAME_US = 16_667                  # one frame at 60 fps, in microseconds
BUDGET_US = 2_000                  # the AI's share of each frame
THINK_US = 40                      # one agent's think
N, NEAR = 600, 20                  # agents; the first NEAR of them are near the player
FRAMES = 120                       # two seconds

def all_at_once(frame, cursor):    # everyone on every 6th frame
    return (list(range(N)) if frame % 6 == 0 else []), cursor

def staggered(frame, cursor):      # agent a thinks when (frame + a) % 6 == 0
    return [a for a in range(N) if (frame + a) % 6 == 0], cursor

def budgeted(frame, cursor):       # round robin until the budget is spent
    k = BUDGET_US // THINK_US
    return [(cursor + i) % N for i in range(k)], (cursor + k) % N

def budgeted_lod(frame, cursor):   # near agents every frame, the rest share what is left
    k = (BUDGET_US - NEAR * THINK_US) // THINK_US
    far = N - NEAR
    picked = list(range(NEAR)) + [NEAR + (cursor + i) % far for i in range(k)]
    return picked, (cursor + k) % far

def run(policy):
    last, wait = [0] * N, [0] * N  # frame of last think; longest wait seen, per agent
    cursor, costs = 0, []
    for frame in range(1, FRAMES + 1):
        thinkers, cursor = policy(frame, cursor)
        for a in thinkers:
            wait[a] = max(wait[a], frame - last[a])
            last[a] = frame
        costs.append(len(thinkers) * THINK_US)
    return max(costs), sum(costs) / FRAMES, max(wait[:NEAR]), max(wait[NEAR:])

print(f"{'policy':15}{'worst ms':>9}{'avg ms':>8}{'near wait':>11}{'far wait':>10}")
for name, policy in [("all at once", all_at_once), ("staggered", staggered),
                     ("budgeted", budgeted), ("budgeted + LOD", budgeted_lod)]:
    worst, avg, near, far = run(policy)
    print(f"{name:15}{worst / 1000:>9.1f}{avg / 1000:>8.1f}"
          f"{near * FRAME_US / 1000:>9.1f}ms{far * FRAME_US / 1000:>8.1f}ms")
```

Output:

```
policy          worst ms  avg ms  near wait  far wait
all at once         24.0     4.0    100.0ms   100.0ms
staggered            4.0     4.0    100.0ms   100.0ms
budgeted             2.0     2.0    200.0ms   200.0ms
budgeted + LOD       2.0     2.0     16.7ms   333.3ms
```

### Numbers you can check

Every number in the output comes from the formulas. Work them by hand with `N = 600`, `c = 40`, `P = 6`, `B = 2,000`, `m = 20`.

| Policy | Worst frame | Average per frame | Near wait | Far wait |
|---|---|---|---|---|
| All at once | `600 × 40 = 24,000` µs | `24,000 / 6 = 4,000` µs | 6 frames = 100 ms | 6 frames = 100 ms |
| Staggered | `100 × 40 = 4,000` µs | 4,000 µs | 6 frames = 100 ms | 6 frames = 100 ms |
| Budgeted | `50 × 40 = 2,000` µs | 2,000 µs | `ceil(600 / 50) = 12` frames = 200 ms | 12 frames = 200 ms |
| Budgeted + LOD | 2,000 µs | 2,000 µs | 1 frame = 16.7 ms | `ceil(580 / 30) = 20` frames = 333 ms |

For the last row, the near tier uses `20 × 40 = 800` µs. That leaves 1,200 µs, room for `k_far = 30` far thinks per frame.

Read the table from top to bottom.

- **All at once** is the only policy that breaks the frame. A 24 ms AI spike cannot fit in a 16.7 ms frame even if nothing else ran. The average of 4 ms hides it completely.
- **Staggering** removes the spike for free. Same work, same wait, flat frames. There is almost never a reason not to stagger. But it still spends 4 ms, twice the budget, and it will grow with `N`.
- **The budget** caps the cost at 2 ms no matter how many guards the level designer places. The price is a 200 ms wait for everyone, including the guard the player is fighting.
- **The near tier** gives the 20 guards near the player a think every frame, 6 times better than the designers asked for. The 580 far guards wait a third of a second. Almost none of them are on screen.

Now grow the fortress. Under the plain budget, the wait is `ceil(N / 50)` frames.

| Guards `N` | Budgeted cost per frame | Wait | With 20 near guards: far wait |
|---|---|---|---|
| 300 | 2.0 ms | 6 frames = 100 ms | `ceil(280 / 30) = 10` frames = 167 ms |
| 600 | 2.0 ms | 12 frames = 200 ms | 20 frames = 333 ms |
| 1,200 | 2.0 ms | 24 frames = 400 ms | `ceil(1,180 / 30) = 40` frames = 667 ms |

The cost column never moves. The wait column doubles with `N`. At 300 guards the budget already meets the designers' 100 ms target, and you could shrink the budget. At 1,200, far guards wait two thirds of a second, which is fine for a guard dozing in a far tower and not fine for one the player can see across the courtyard.

### The visual

Open [`w14-frame-budget.html`](../examples/w14-frame-budget.html). The top view is a strip of 60 frame bars, one second of play, with a dashed line at the 2 ms budget and a solid line at 16.7 ms. The bottom view is a grid of 600 dots, one per guard, each coloured by how many frames since it last thought, with the 20 near guards drawn in a ring around the player.

Start on "all at once". The top view shows ten towers of 24 ms, each crossing the frame line. The dots all flash together and then all fade together. Switch to "staggered" and the towers flatten into a 4 ms band while the dots ripple. Switch to "budgeted" and the band drops to the budget line, and the ripple slows to half speed. Now drag the guard count to 1,200. The top view does not change at all. The bottom view slows to a crawl. Finally switch on the near tier, and the ring of dots around the player stays bright while the rest slows further. Two views, one exchange.

### Cross-game recognition

**Factorio (2.x, current data files).** The biter pathfinder is our budgeted scheduler for search steps. The budget is `max_steps_worked_per_tick = 1,000` node expansions per tick. It also has a priority tier. The comments in `map-settings.lua` say that up to 10 waiting requests are all accepted, that from 10 to 100 only requests with a short straight-line distance (under 100) are accepted, that short requests get half of each tick's steps (`short_request_ratio = 0.5`), and that a short request taking more than 1,000 steps is rescheduled as a long one. In our form, short requests are the near tier. They get a reserved share of `B` so that a single long search cannot starve them. The overload multipliers go one step further. When the queue passes 100 or 500 waiting requests, the game raises `B` itself, trading frame time back for less delay.

**RimWorld (1.x).** RimWorld runs at 60 ticks per second at normal speed, and gives modders three update cadences. The RimWorld Wiki lists a normal tick, a rare tick every 250 ticks (about 4.2 s) and a long tick every 2,000 ticks (about 33 s). This is time-slicing by *kind* of work rather than by distance. A system that must react within a second belongs on the normal tick. A slow process, such as something that changes over in-game hours, can run on the rare or long tick. In our form, each cadence is a fixed period `P`, and choosing the rare tick for a system divides its average cost by 250. The wait it adds, 4 s, is invisible for a plant and would be absurd for a gunfight.

**Unreal Engine (5.x).** Epic's engine ships two tools that match the model. The Animation Budget Allocator limits the time spent updating skeletal-mesh animation to a fixed budget, 1.0 ms by default (`a.Budget.BudgetMs`), and throttles the update rate of less significant meshes first so the closest ones keep full quality. That is budgeted plus LOD, with animation in place of thinks. The Significance Manager is a framework for scoring how much each object matters. Epic's documentation lists reducing how often less significant AI runs, and limiting how many high-detail AI characters exist at once, as typical uses. The engine supplies the scoring hook. You supply the tiers and the budget.

Three different games and engines, one model. Each one has a budget `B`, some notion of which agents or jobs are near, and a queue for the rest. When you read a new engine's performance settings, look for those three things.

### Eyes-open design judgment

- **Stagger always. Budget when `N` is not under your control.** Staggering costs nothing and removes spikes. A budget matters when level designers, players or spawners decide how many agents exist. It is the only policy whose worst frame you can promise.
- **Pick the budget from the wait you can accept, not the other way round.** Start from the designers' reaction target, say 100 ms for anything on screen. With `k = B / c` and `wait = N / k`, the budget you need is `B = N × c / wait`. If that is too big, you need tiers, cheaper thinks or fewer agents. It is never solved by hoping.
- **Delay is visible. Hitches are more visible.** Players tolerate an enemy that reacts 200 ms late far better than a stutter, and a stutter hurts every system on screen. But delay stacks. Week 10's perception update rate, this week's think wait and the animation start-up all add up to the reaction time the player sees. Budget the total, not each piece alone.
- **Tiers create edges.** A guard that crosses from far to near changes behavior quality in one frame. If the far tier uses a cheaper decision model, the switch can look like a sudden change of mind. Use hysteresis, with different distances for promotion and demotion, as in the aggro and leash radii of [week 6](w06-finite-state-machines.md), and promote early, before the agent is on screen. In year 3, [MMO302 week 3](../../MMO302-mmo-server-architecture/lectures/w03-area-of-interest-grids-radius-hysteresis.md) applies the same idea to area of interest.

## 3. Time-slicing one long job

The scheduler above splits many small jobs across frames. Some single jobs are too big for one frame. A* on a large map can expand thousands of nodes, and at, say, 1 µs per expansion, a 5,000-node search takes 5 ms on its own. The fix is the same exchange. Let the search do a fixed number of expansions per frame, then pause and resume next frame. An algorithm that can stop at any point and resume later is called **interruptible**. One that also has a usable partial answer when stopped (the best path so far, a rough plan) is called an **anytime** algorithm.

Python's generators make an interruptible search short. This is week 4's `search()`, unchanged except for two lines that count expansions and `yield` when the frame's quota is spent. It runs on week 4's 8 × 12 map with the wall.

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

def sliced_search(start, goal, h, steps_per_frame):
    """Week 4's search as a generator. It yields None after each frame's quota of
    expansions and finally yields (cost, expanded)."""
    g = {start: 0}
    frontier = [(h(start, goal), h(start, goal), start)]
    closed = set()
    used = 0
    while frontier:
        f, _, cell = heapq.heappop(frontier)
        if cell in closed:
            continue
        closed.add(cell)
        if cell == goal:
            yield g[goal], len(closed)
            return
        for nxt in neighbors(cell):
            new_g = g[cell] + 1
            if new_g < g.get(nxt, float("inf")):
                g[nxt] = new_g
                hn = h(nxt, goal)
                heapq.heappush(frontier, (new_g + hn, hn, nxt))
        used += 1
        if used == steps_per_frame:    # out of budget: pause until next frame
            used = 0
            yield None

S, G = (4, 0), (4, 11)
for name, h in [("Dijkstra", zero), ("A*", manhattan)]:
    for budget in (8, 32):
        frames = 0
        for result in sliced_search(S, G, h, budget):
            frames += 1
            if result is not None:
                cost, expanded = result
        print(f"{name:8} budget {budget:>2}/frame: cost {cost}, expanded {expanded}, "
              f"answer on frame {frames}")
```

Output:

```
Dijkstra budget  8/frame: cost 17, expanded 91, answer on frame 12
Dijkstra budget 32/frame: cost 17, expanded 91, answer on frame 3
A*       budget  8/frame: cost 17, expanded 32, answer on frame 4
A*       budget 32/frame: cost 17, expanded 32, answer on frame 1
```

The path and cost are identical to week 4. Only the frame on which the answer arrives changes, and it follows `ceil(expanded / steps_per_frame)`: `ceil(91 / 8) = 12` and `ceil(32 / 8) = 4`. Notice what week 4's work buys you here. A* expands a third of Dijkstra's nodes, so under the same per-frame budget its answer arrives three times sooner. A better heuristic is not only less CPU. Under a budget it is less delay.

Three practical points come with time-sliced searches.

- **The world can change while you search.** A door can close between frame 1 and frame 12. Either check the path when it arrives, or have the search re-read costs as it goes.
- **Give the agent something to do while it waits.** A guard that freezes for 12 frames looks broken. Start walking toward the goal in a straight line, turn the head, or play a "thinking" animation. The player should see a decision being made, not a lag.
- **Cap the total, not only the slice.** A search that will never finish (the goal is unreachable) will happily consume its slice forever. Factorio's settings include a termination rule for exactly this: the search stops once its steps exceed a multiple of the start-to-goal estimate, with a minimum of 2,000 steps.

## 4. What else level of detail can cut

Think frequency is the first thing LOD reduces, but not the only one. For each tier, decide what to degrade, and check that the player cannot see it.

| What | Near (on screen, close) | Mid (visible, far) | Far (off screen) |
|---|---|---|---|
| Think frequency | every frame to every 3rd | every 6th to 12th | every second or less |
| Perception | full line-of-sight rays (week 10) | one ray, or distance only | none; wake on events |
| Pathfinding | full A* on the navmesh (week 5) | coarse A* on an abstract graph | teleport along a precomputed route, or none |
| Steering | full avoidance (week 2) | separation only | none |
| Animation | full rate | reduced rate | none |

Two rules keep this honest.

- **Never degrade what the player is looking at.** Visible stupidity is the failure week 1 called artificial stupidity. A guard at 100 m that turns a beat late is invisible. A guard at 5 m that walks through a table is not.
- **Off-screen agents must stay consistent when they come back.** If a far merchant simply stops, the market is empty when the player arrives. A cheap far tier can advance agents along a schedule ("at 9:00 go to the stall") without simulating the walk, then place them correctly when they are promoted. The player judges only what they find.

MMO servers face the same problem with many players watching different places at once. [MMO404 week 12, AI at scale](../../MMO404-advanced-networked-simulation/lectures/w12-ai-at-scale.md) builds distance tiers across a whole zone and shows that the cost follows where players stand. This week's budget and queue are the single-machine version of the same idea.

## In-class activity (25 minutes)

In pairs. You are the AI programmer on a stealth game. The level has 400 guards, of whom at most 25 can be on screen at once. A think costs 60 µs. The designers want on-screen guards to react within 50 ms and off-screen guards within 500 ms. The frame is 16.7 ms.

1. (5 min) Compute the cost per frame if every guard thinks every 3rd frame, staggered. What share of the frame is that?
2. (8 min) Design a budgeted two-tier scheduler that meets both reaction targets. What is the smallest budget `B` that works? Show the calculation for both tiers.
3. (7 min) The level designer adds 200 guards. Which target breaks first, and what is the new smallest `B`? Suggest one change that is not "raise the budget".
4. (5 min) Swap with another pair. Find one situation in their design where a guard is visibly late or visibly stupid.

Expected output: your two budgets with calculations, the one non-budget change, and the weakness your partners found.

## Common misconceptions

- **"Time-slicing makes the AI faster."** It makes no think cheaper. It moves work to other frames and adds delay. The total CPU per second is unchanged or, with the budget, capped.
- **"If the average fits, the frame fits."** The average hides spikes. All-at-once scheduling averages 4 ms and spends 24 ms on one frame in six. Always measure the worst frame.
- **"LOD means distance."** Distance is one proxy for how much the player can see. Line of sight, being in combat, being targeted, or being part of a quest can matter more. A far sniper aiming at the player is near in every sense that counts.
- **"A budget protects me from too many agents."** It protects the frame. The agents pay instead, and past some `N` their wait becomes visible. A budget without a maximum acceptable wait is half a design.

## Check yourself

1. A game has 900 agents with a 25 µs think and a 1.5 ms budget. How many agents think per frame, and how long, in milliseconds at 60 fps, does the worst-off agent wait?
2. The same game adds a near tier of 30 agents that think every frame. What is the far wait now?
3. A designer asks for every one of 900 agents to react within 100 ms, 25 µs per think, 60 fps. What budget does that need? Is it cheaper to meet the target with a near tier of 30, if only near agents need 100 ms and far agents may take 1 s?
4. A time-sliced A* with a budget of 200 expansions per frame needs 1,450 expansions for a path. On which frame does the answer arrive? The heuristic is improved so the same path needs 600 expansions. How many frames sooner does the agent start moving?
5. RimWorld's rare tick runs every 250 ticks at 60 ticks per second. A mod checks every pawn for hunger on the rare tick instead of every tick. By what factor does the average cost fall, and what is the longest delay before a pawn notices it is hungry?

<details>
<summary>Answers</summary>

1. `k = floor(1,500 / 25) = 60` per frame. Wait `ceil(900 / 60) = 15` frames `= 250` ms.
2. Near tier costs `30 × 25 = 750` µs, leaving 750 µs for `30` far thinks per frame. Far wait `ceil(870 / 30) = 29` frames, about 483 ms.
3. 100 ms is 6 frames, so `k = ceil(900 / 6) = 150` thinks per frame, `B = 150 × 25 = 3,750` µs. With tiers: near costs 750 µs; far agents need `ceil(870 / 60) = 15` thinks per frame (1 s is 60 frames), 375 µs. Total `B = 1,125` µs, less than a third.
4. `ceil(1,450 / 200) = 8` frames. With 600 expansions, `ceil(600 / 200) = 3` frames, so 5 frames (83 ms) sooner.
5. The average cost falls by a factor of 250. The longest delay is 250 ticks, about 4.2 s.

</details>

## Lab / assignment hook

[Lab 14, a frame-budget scheduler](../labs/lab14.md). You build a budgeted round-robin scheduler with a near tier and variable think costs, a time-sliced A* on the lab 4 style grid, and measure worst-frame cost and worst wait for a fortress of guards. The checks in `test_scheduler.py` fail on the starter and pass when you are done. The scheduler is the one you will run your final NPC ecosystem demo on.

## Sources

- Wube Software, Factorio, `base/prototypes/map-settings.lua` in the `factorio-data` repository on GitHub (base mod version 2.1.20, accessed September 2026). https://github.com/wube/factorio-data. `path_finder` settings and their comments: `max_steps_worked_per_tick = 1000`, `short_request_ratio = 0.5`, `max_clients_to_accept_any_new_request = 10`, `max_clients_to_accept_short_new_request = 100`, `direct_distance_to_consider_short_request = 100`, `short_request_max_steps = 1000`, `min_steps_to_check_path_find_termination = 2000`, `overload_levels = {0, 100, 500}` with `overload_multipliers = {2, 3, 4}`.
- Factorio Wiki, "Time" (current). 60 ticks per real second at game speed 1.
- RimWorld Wiki, "Time" (RimWorld 1.x, accessed September 2026). 60 ticks per second at normal speed; rare tick every 250 ticks, long tick every 2,000 ticks.
- Epic Games, "Animation Budget Allocator in Unreal Engine" (Unreal Engine 5.8 documentation). Fixed time budget for skeletal-mesh animation, default `a.Budget.BudgetMs = 1.0`, throttling of less significant meshes.
- Epic Games, "Significance Manager in Unreal Engine" (Unreal Engine 5.8 documentation). Project-defined significance functions; typical uses include reducing AI update frequency for less significant objects.
- Sunshine-Hill, B. (2013). "Phenomenal AI Level-of-Detail Control with the LOD Trader." In S. Rabin (ed.), *Game AI Pro*, chapter 14. CRC Press. Free at gameaipro.com.
- Millington, I. (2019). *AI for Games*, 3rd ed., chapter 9 "Execution management". CRC Press.

## Interactive spec: examples/w14-frame-budget.html

**Purpose.** Show that a budget converts AI cost into delay. The same guards, scheduled four ways, with one view for the frame and one for the guards.

**The one insight.** Under a budget, the frame-cost view stays flat no matter how many guards there are, while the guards' wait grows in proportion. The student should see, within ten seconds of dragging the guard count, that the top view does not move and the bottom view slows down.

**Layout.** Top: a bar chart of the last 60 frames (one second), bar height = AI time that frame in ms, with a dashed line at the budget and a solid line at 16.7 ms labelled "frame". Axis 0 to 30 ms, bars that exceed 30 are clipped with a marker. Bottom: a grid of `N` dots (up to 1,200) representing guards. The first `m` guards are drawn in a ring around a player marker in the center; the rest fill a square around it. Each dot's brightness shows frames since its last think (bright = just thought, fading linearly to dim at 40 frames). Right of the views on desktop, below them under 700 px: a numbers panel. Controls above.

**Model (must match the lecture exactly).**
- Integer microseconds. `F = 16,667`, defaults `N = 600`, `c = 40`, `B = 2,000`, `P = 6`, `m = 20`.
- Policies, applied per frame `f = 1, 2, 3, ...`:
  - All at once: all agents think when `f mod P = 0`.
  - Staggered: agent `a` (0-based) thinks when `(f + a) mod P = 0`.
  - Budgeted: `k = floor(B / c)`, agents `(cursor + i) mod N` for `i < k`, then `cursor += k`.
  - Budgeted + LOD: agents `0..m−1` every frame; `k_far = floor((B − m c) / c)`; far agents `m + (cursor + i) mod (N − m)`, `cursor += k_far`. If `m × c > B`, show a warning "near tier exceeds budget" and serve only the first `floor(B / c)` near agents.
- Frame cost = thinks × `c`. Wait = frames since the agent's previous think.
- Numbers panel: worst frame (ms, one decimal), average (ms, one decimal) over the last 120 frames, formula-based near wait and far wait in frames and ms, and the formulas with the current numbers substituted, for example "wait = ceil(580 / 30) = 20 frames = 333.3 ms".

**Controls.**
- Policy: four radio buttons, default "budgeted".
- Guards `N`: slider 60 to 1,200, step 20.
- Think cost `c`: slider 10 to 100 µs, step 5.
- Budget `B`: slider 500 to 6,000 µs, step 100.
- Near tier `m`: slider 0 to 60, step 1 (active only for budgeted + LOD).
- Play / pause, and step (one frame). Speed: real time (60 frames per second) or slow (6 per second).
- All controls reset the cursor and the frame history, then run 120 frames at once (a warm-up) so the worst-frame and average readouts, which are measured over the last 120 frames, show the test values below before the student presses Play.

**Test values (defaults unless stated).**
- All at once: worst 24.0 ms, average 4.0 ms, wait 6 frames = 100.0 ms for all.
- Staggered: worst 4.0, average 4.0, wait 100.0 ms.
- Budgeted: worst 2.0, average 2.0, wait 12 frames = 200.0 ms.
- Budgeted + LOD: worst 2.0, average 2.0, near 1 frame = 16.7 ms, far 20 frames = 333.3 ms.
- Budgeted, `N = 300`: wait 6 frames = 100.0 ms. `N = 1,200`: wait 24 frames = 400.0 ms. LOD with `N = 1,200`: far wait 40 frames = 666.7 ms.
- Check-yourself 1: `N = 900`, `c = 25`, `B = 1,500`, budgeted: 60 per frame, wait 15 frames = 250.0 ms. With `m = 30`: far 30 per frame, wait 29 frames = 483.3 ms.

**First screen.** Budgeted policy running at real time, with the caption "2 ms of AI every frame. Now drag the guard count."

**Accessibility.** All controls keyboard operable with visible focus. The numbers panel updates an `aria-live="polite"` region at most once per second. With `prefers-reduced-motion`, start paused and advance only on the step button or at the slow speed. Palette from `templates/interactive-tokens.css`, light and dark. Near-tier dots differ from far dots by shape (ring vs square) as well as position.
