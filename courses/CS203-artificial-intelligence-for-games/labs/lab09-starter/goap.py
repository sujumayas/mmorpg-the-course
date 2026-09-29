"""CS203 Lab 09 starter: a goal-oriented action planner. Standard library only.

Fill in the TODO functions, then run the tests:

    python3 test_goap.py

Then run this file to print the plan for every starting world:

    python3 goap.py

Conventions follow the week 9 lecture. A world state is a dict of fact name ->
bool. A missing fact counts as False. An action is a tuple
(name, cost, preconditions, effects), where preconditions and effects are dicts
of the same kind.
"""
import heapq
from itertools import count, product

# ------------------------------------------------------------ the lecture's soldier

ACTIONS = [
    # name,            cost, preconditions,                              effects
    ("GoToCover",       2, {"cover_nearby": True},                        {"in_cover": True}),
    ("AttackFromCover", 2, {"weapon_loaded": True, "in_cover": True},     {"enemy_dead": True}),
    ("AttackInOpen",    6, {"weapon_loaded": True},                       {"enemy_dead": True}),
    ("Reload",          2, {"has_ammo": True},                            {"weapon_loaded": True}),
    ("FetchAmmo",       5, {},                                            {"has_ammo": True}),
    ("Charge",          4, {},                                            {"near_enemy": True}),
    ("Melee",           3, {"near_enemy": True},                          {"enemy_dead": True}),
]
GOAL = {"enemy_dead": True}

# ------------------------------------------------------------ your code


def satisfied(state, facts):
    """TODO step 1. True when every fact in `facts` has the same value in
    `state`. A fact missing from `state` counts as False."""
    raise NotImplementedError("satisfied() is yours to write")


def apply(state, effects):
    """TODO step 1. Return a NEW dict: a copy of `state` with `effects`
    written over it. Do not modify `state`."""
    raise NotImplementedError("apply() is yours to write")


def unmet(state, goal):
    """TODO step 2. The heuristic: how many goal facts `state` does not yet
    satisfy."""
    raise NotImplementedError("unmet() is yours to write")


def plan(start, goal, actions=ACTIONS):
    """TODO step 3. A* over world states (week 4's search, new graph).

    Nodes are world states, edges are actions whose preconditions hold, edge
    cost is the action's cost, h is unmet(state, goal).
    - Push (f, tiebreak, g, state, steps) on a heapq, with tiebreak from
      itertools.count() so that equal f pops in push order.
    - Keep a closed set of expanded states. Use key(state) as the set key.
    - When you pop a state: skip it if closed; otherwise close it. If it
      satisfies the goal, return (g, steps, expanded). Otherwise add 1 to
      `expanded` and push every action whose preconditions hold, in the
      order of `actions`, unless the resulting state is already closed.
    - If the open list empties, return (None, [], expanded).
    `steps` is the list of action names from start to this state."""
    raise NotImplementedError("plan() is yours to write")


# ------------------------------------------------------------ provided


def key(state):
    """A hashable version of a state that ignores False facts, so that
    {"a": False} and {} count as the same world."""
    return frozenset(k for k, v in state.items() if v)


# The lecture's door (section 4). The player may be holding the door shut.
DOOR_ACTIONS = [
    ("OpenDoor",          1, {"door_jammed": False}, {"door_open": True}),
    ("KickDoor",          3, {"door_barred": False}, {"door_open": True}),
    ("WalkThroughDoor",   1, {"door_open": True},    {"in_room": True}),
    ("DiveThroughWindow", 5, {},                     {"in_room": True}),
]


def execute(start, goal, actions, failures):
    """Plan, then carry out the plan one action at a time. `failures` maps an
    action name to the fact the NPC learns when that action fails, for example
    {"OpenDoor": {"door_jammed": True}}. A failing action adds its fact to the
    NPC's working memory and triggers a replan; each action fails at most once.
    Returns (actions attempted in order, number of plans made, final state)."""
    state, failures = dict(start), dict(failures)
    attempted, plans = [], 0
    while not satisfied(state, goal):
        cost, steps, _ = plan(state, goal, actions)
        plans += 1
        if cost is None:
            break                                 # no plan: fall back to another goal
        for name in steps:
            attempted.append(name)
            if name in failures:
                state = apply(state, failures.pop(name))   # learn why, then replan
                break
            eff = next(e for n, _, _, e in actions if n == name)
            state = apply(state, eff)
    return attempted, plans, state


def world(loaded, ammo, cover):
    return {"weapon_loaded": loaded, "has_ammo": ammo, "cover_nearby": cover}


if __name__ == "__main__":
    print("loaded ammo cover | cost expanded  plan")
    for loaded, ammo, cover in product((True, False), repeat=3):
        cost, steps, n = plan(world(loaded, ammo, cover), GOAL)
        print(f"  {int(loaded)}      {int(ammo)}     {int(cover)}   |  {cost}      {n}     "
              + " -> ".join(steps))
