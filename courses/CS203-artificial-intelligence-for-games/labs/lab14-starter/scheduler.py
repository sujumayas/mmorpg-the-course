"""CS203 Lab 14 starter: spending a frame budget on AI.

Times are integer microseconds. A frame at 60 fps is 16,667 us.

An Agent has an id, the cost of one think in microseconds, and a flag saying
whether it is near the player. A *policy* is any function that takes the frame
number (1, 2, 3, ...) and returns the list of agent ids that think on that frame.
simulate() runs a policy and measures the worst frame, the average frame and
the longest wait (frames between two thinks) of every agent.

Run:   python scheduler.py          prints the lecture's comparison for the fortress
Check: python test_scheduler.py     exits 0 only when your work is complete

You write the parts marked TODO. Leave simulate(), astar() and the maps alone:
the tests use them as the reference.
"""
import heapq
import math
from collections import namedtuple

FRAME_US = 16_667
Agent = namedtuple("Agent", "id cost near")


def fortress(n=600, near=20, cost=40):
    """The lecture's fortress: n guards, the first `near` of them near the player."""
    return [Agent(i, cost, i < near) for i in range(n)]


def simulate(policy, agents, frames=240):
    """Run `policy` for `frames` frames. Return a dict with
        worst: most expensive frame (us)      average: mean frame cost (us, float)
        costs: list of frame costs             wait: {agent id: longest wait in frames}
    An agent's first wait is counted from frame 0."""
    cost = {a.id: a.cost for a in agents}
    last = {a.id: 0 for a in agents}
    wait = {a.id: 0 for a in agents}
    costs = []
    for f in range(1, frames + 1):
        ids = policy(f)
        for i in ids:
            wait[i] = max(wait[i], f - last[i])
            last[i] = f
        costs.append(sum(cost[i] for i in ids))
    for i in wait:  # agents that never thought waited the whole run
        if last[i] == 0:
            wait[i] = frames + 1
    return {"worst": max(costs), "average": sum(costs) / frames, "costs": costs, "wait": wait}


def all_at_once(agents, period):
    """Reference policy: every agent thinks when frame % period == 0."""
    ids = [a.id for a in agents]
    return lambda f: ids if f % period == 0 else []


# ---------------------------------------------------------------- TODO 1
def staggered(agents, period):
    """Return a policy in which agent a thinks when (frame + a.id) % period == 0."""
    raise NotImplementedError("staggered")


# ---------------------------------------------------------------- TODO 2
class BudgetScheduler:
    """Budgeted round robin with a near tier.

    Each call serves, in this order:
      1. every near agent, in the order given, while its cost fits in what is left
         of the budget (serve at least the first near agent even if it does not fit);
      2. far agents in round-robin order, starting where the previous frame stopped,
         while the next far agent's cost fits in what is left. Stop at the first one
         that does not fit (no skipping ahead), EXCEPT that if no far agent has been
         served yet this frame, serve that one anyway so the queue always advances.
    The cursor into the far list persists between frames.
    """

    def __init__(self, agents, budget_us):
        self.budget = budget_us
        self.near = [a for a in agents if a.near]
        self.far = [a for a in agents if not a.near]
        self.cursor = 0

    def __call__(self, frame):
        raise NotImplementedError("BudgetScheduler.__call__")


# ---------------------------------------------------------------- TODO 3
def predicted_wait(n_near, n_far, cost, budget):
    """Lecture formulas for equal-cost agents, in frames: return (near_wait, far_wait).
    k_far = floor((budget - n_near * cost) / cost), at least 1 (the queue always
    advances); far_wait = ceil(n_far / k_far). near_wait is 1 if n_near > 0, else 0."""
    raise NotImplementedError("predicted_wait")


# ---------------------------------------------------------------- maps and A*
MAPS = {
    "wall": ["............",
             "............",
             "....#.......",
             "....#.......",
             "S...#......G",
             "....#.......",
             "....#.......",
             "............"],
    "lake": ["..............",
             "..............",
             "......####....",
             ".........#....",
             "..S......#..G.",
             ".........#....",
             "......####....",
             "..............",
             ".............."],
    "maze": ["S.#.........",
             "..#.######..",
             "..#......#..",
             "..######.#..",
             "..........#.",
             "#########.#.",
             "..........#G"],
}


def find(grid, ch):
    for r, row in enumerate(grid):
        if ch in row:
            return (r, row.index(ch))


def neighbors(grid, cell):
    r, c = cell
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != "#":
            yield (nr, nc)


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(grid, start, goal):
    """Week 4's search, all in one frame. Returns (cost, expanded)."""
    g = {start: 0}
    frontier = [(manhattan(start, goal), manhattan(start, goal), start)]
    closed = set()
    while frontier:
        _, _, cell = heapq.heappop(frontier)
        if cell in closed:
            continue
        closed.add(cell)
        if cell == goal:
            return g[goal], len(closed)
        for nxt in neighbors(grid, cell):
            new_g = g[cell] + 1
            if new_g < g.get(nxt, math.inf):
                g[nxt] = new_g
                hn = manhattan(nxt, goal)
                heapq.heappush(frontier, (new_g + hn, hn, nxt))
    return None, len(closed)


# ---------------------------------------------------------------- TODO 4
def sliced_astar(grid, start, goal, steps_per_frame):
    """astar() as a generator. After every `steps_per_frame` expansions that did not
    reach the goal, yield None (the frame's quota is spent). When the goal is popped,
    yield (cost, expanded) and stop. If the goal is unreachable, yield (None, expanded)."""
    raise NotImplementedError("sliced_astar")


def frames_to_answer(gen):
    """Drive a sliced search one step per frame. Returns (frames, result)."""
    frames = 0
    for result in gen:
        frames += 1
        if result is not None:
            return frames, result
    return frames, None


if __name__ == "__main__":
    guards = fortress()
    rows = [("all at once", lambda: all_at_once(guards, 6)),
            ("staggered", lambda: staggered(guards, 6)),
            ("budgeted", lambda: BudgetScheduler(fortress(near=0), 2_000)),
            ("budgeted + LOD", lambda: BudgetScheduler(guards, 2_000))]
    print(f"{'policy':15}{'worst ms':>9}{'avg ms':>8}{'near wait':>11}{'far wait':>10}")
    for name, make in rows:
        try:
            r = simulate(make(), guards)
        except NotImplementedError:
            print(f"{name:15}{'-':>9}{'-':>8}{'-':>11}{'-':>10}")
            continue
        near = max(r["wait"][i] for i in range(20)) * FRAME_US / 1000
        far = max(r["wait"][i] for i in range(20, 600)) * FRAME_US / 1000
        print(f"{name:15}{r['worst'] / 1000:>9.1f}{r['average'] / 1000:>8.1f}"
              f"{near:>9.1f}ms{far:>8.1f}ms")
