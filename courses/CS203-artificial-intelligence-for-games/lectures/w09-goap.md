# CS203 · Week 09 — Goal-Oriented Action Planning (GOAP)

**Why this matters:** Behavior trees and utility systems choose among behaviors you wrote. Neither can work out a new *order* of steps. If a soldier's gun is empty and cover is nearby, should it reload first or run for cover first, or charge with a knife? A planner answers that by searching, with the same A* you wrote in week 4, through the states of the world instead of the tiles of a map. You describe what each action needs and what it changes. The NPC works out the sequence, and it keeps working it out when the player breaks its plan.

**You will be able to:**
- Describe an NPC's world as a set of facts and its actions as preconditions, effects and costs.
- Compute the cheapest plan for a goal by hand and with A* over world states, and count the states expanded.
- Predict how a change in the world, an action's cost or a character's action set changes the plan, and trace a replan after an action fails.
- Critique a planning design for cost, readability and designer control, and choose between a planner, a behavior tree and utility scoring for a given NPC.

**Before class:** Orkin, J., "Three States and a Plan: The A.I. of F.E.A.R.", Game Developers Conference 2006 (free online, 18 pages; read all of it, it is the best-known paper in game AI). Humphreys, T., "Exploring HTN Planners through Example", *Game AI Pro* (2013), chapter 12, sections 12.1 and 12.2 (free at gameaipro.com). Millington, *AI for Games* (3rd ed., 2019), chapter 5, the section on goal-oriented behavior.

**Prerequisites from earlier courses:** [CS203 week 4, A* and heuristics](w04-a-star-and-heuristics.md) (the open list, `f = g + h`, admissibility; this week reuses all of it on a new graph). [CS203 week 3, graphs and Dijkstra](w03-graphs-and-dijkstra.md) (nodes, edges, costs). [CS203 week 6, finite state machines](w06-finite-state-machines.md) (transition growth, and the F.E.A.R. three-state machine you met there). [CS203 weeks 7 and 8](w07-behavior-trees.md) (behavior trees and [utility AI](w08-utility-ai.md), the two alternatives compared in section 5). [CS102 week 6, queues and stacks](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w06-queues-and-stacks-undo-and-command-buffers.md) (a plan is a queue of commands).

**Interactive:** [`examples/w09-goap-planner.html`](../examples/w09-goap-planner.html). Keep it open during section 2.

---

## 1. Describing a world so a search can use it

Week 4's A* searched a grid. A node was a tile, an edge was a step to a neighboring tile, and the cost was the distance. Nothing in A* cares that the nodes are tiles. It needs three things: a start node, a way to list each node's neighbors with the cost of reaching them, and a test for "is this the goal?" A heuristic helps if you have one.

A planner feeds A* a different graph.

- A **world state** is a small set of named facts, each true or false: `weapon_loaded`, `has_ammo`, `cover_nearby`, `in_cover`, `near_enemy`, `enemy_dead`. It is the NPC's working knowledge, not the whole game. A fact the NPC has no entry for counts as false.
- An **action** has a **cost**, a set of **preconditions** (facts that must hold before it can run) and a set of **effects** (facts it makes true or false). `Reload` needs `has_ammo` and makes `weapon_loaded` true.
- A **goal** is a set of facts the NPC wants to hold, such as `enemy_dead`.

Now the graph falls out. A node is a world state. An edge from a state is any action whose preconditions hold in it, leading to the state with that action's effects written over it. The edge cost is the action's cost. The search stops when it pops a state in which the goal holds. The list of actions along the path is the **plan**.

This style of description is old. Orkin traces it to STRIPS, the Stanford Research Institute Problem Solver, built around 1970 at the Stanford Research Institute, now SRI International. What Monolith added for F.E.A.R. was making it cheap and controllable enough to run many times a second in a shipped game, and they called the result **Goal-Oriented Action Planning**, or **GOAP**.

## 2. Worked example: the soldier who works out its own plan

### The hook

In F.E.A.R. (Monolith, 2005), a patrolling soldier walks toward a door, and the player, on the other side, holds it shut. The soldier tries to open the door and fails. It kicks the door, and that fails too. It dives through the window beside the door and comes up close enough to hit the player. Orkin describes exactly this sequence in his GDC 2006 paper, and players at the time talked about the soldiers as if they were thinking.

No designer wrote "if the door is held, kick it; if kicking fails, use the window". Each action simply stated what it needed and what it did. When an action failed, the soldier recorded why, in its working memory, and planned again from the new facts. Orkin's summary of the benefit is that designers can drop in goals and actions and never have to specify the transitions between them.

### The model

Here is a soldier with seven actions and one goal, `enemy_dead`.

| Action | Cost | Preconditions | Effects |
|---|---|---|---|
| GoToCover | 2 | `cover_nearby` | `in_cover` |
| AttackFromCover | 2 | `weapon_loaded`, `in_cover` | `enemy_dead` |
| AttackInOpen | 6 | `weapon_loaded` | `enemy_dead` |
| Reload | 2 | `has_ammo` | `weapon_loaded` |
| FetchAmmo | 5 | none | `has_ammo` |
| Charge | 4 | none | `near_enemy` |
| Melee | 3 | `near_enemy` | `enemy_dead` |

The costs carry the design. AttackInOpen costs 6 and AttackFromCover costs 2 because the designer wants soldiers to prefer cover. FetchAmmo costs 5 because walking to an ammo crate takes time and exposes the soldier. You will see that changing one number changes the soldier's personality.

The heuristic `h` is the number of goal facts not yet true. For this goal it is 1 until the enemy is dead and 0 after. It never overestimates, because every action costs at least 2 and sets at most one goal fact, so it is admissible in week 4's sense and A* returns a cheapest plan.

### The code

This is week 4's A* with three changes: the node is a world state, the neighbors come from the actions whose preconditions hold, and the goal test checks facts instead of a tile. States are compared by their set of true facts, so a state reached twice by different routes is expanded only once.

```python
import heapq
from itertools import count, product

ACTIONS = [  # name, cost, preconditions, effects
    ("GoToCover",       2, {"cover_nearby": True},                    {"in_cover": True}),
    ("AttackFromCover", 2, {"weapon_loaded": True, "in_cover": True}, {"enemy_dead": True}),
    ("AttackInOpen",    6, {"weapon_loaded": True},                   {"enemy_dead": True}),
    ("Reload",          2, {"has_ammo": True},                        {"weapon_loaded": True}),
    ("FetchAmmo",       5, {},                                        {"has_ammo": True}),
    ("Charge",          4, {},                                        {"near_enemy": True}),
    ("Melee",           3, {"near_enemy": True},                      {"enemy_dead": True}),
]

def holds(state, facts):                  # a missing fact counts as False
    return all(state.get(k, False) == v for k, v in facts.items())

def key(state):                           # the set of true facts names a world
    return frozenset(k for k, v in state.items() if v)

def plan(start, goal, actions=ACTIONS):
    h = lambda s: sum(1 for k, v in goal.items() if s.get(k, False) != v)
    tie = count()
    open_list = [(h(start), next(tie), 0, start, [])]
    closed, expanded = set(), 0
    while open_list:
        f, _, g, state, steps = heapq.heappop(open_list)
        if key(state) in closed:
            continue
        closed.add(key(state))
        if holds(state, goal):
            return g, steps, expanded
        expanded += 1
        for name, cost, pre, eff in actions:
            if holds(state, pre):
                nxt = {**state, **eff}
                if key(nxt) not in closed:
                    heapq.heappush(open_list, (g + cost + h(nxt), next(tie),
                                               g + cost, nxt, steps + [name]))
    return None, [], expanded

print("loaded ammo cover  cost expanded  plan")
for loaded, ammo, cover in product((1, 0), repeat=3):
    world = {"weapon_loaded": bool(loaded), "has_ammo": bool(ammo), "cover_nearby": bool(cover)}
    cost, steps, n = plan(world, {"enemy_dead": True})
    print(f"  {loaded}      {ammo}     {cover}     {cost:>3} {n:>6}     {' > '.join(steps)}")
```

Output:

```
loaded ammo cover  cost expanded  plan
  1      1     1       4      2     GoToCover > AttackFromCover
  1      1     0       6      2     AttackInOpen
  1      0     1       4      2     GoToCover > AttackFromCover
  1      0     0       6      2     AttackInOpen
  0      1     1       6      5     GoToCover > Reload > AttackFromCover
  0      1     0       7      4     Charge > Melee
  0      0     1       7      5     Charge > Melee
  0      0     0       7      3     Charge > Melee
```

The tie-break counter makes the search deterministic. When two entries have the same `f`, the one pushed first comes out first, and actions are tried in the order of the table.

### Numbers you can check

Trace the first row by hand. The soldier's gun is loaded, it has ammo, and there is cover nearby.

| Step | Pop (state, `g`, `f`) | Expanded so far | Pushed (action, `g`, `h`, `f`) | Skipped |
|---|---|---|---|---|
| 1 | start, 0, 1 | 1 | GoToCover 2, 1, **3**; AttackInOpen 6, 0, **6**; Charge 4, 1, **5** | Reload, FetchAmmo (their effects are already true, so they lead back to the start, which is closed) |
| 2 | +in_cover, 2, 3 | 2 | AttackFromCover 4, 0, **4**; AttackInOpen 8, 0, **8**; Charge 6, 1, **7** | GoToCover, Reload, FetchAmmo (same state) |
| 3 | +enemy_dead, 4, 4 | 2 | goal holds: return | |

Plan: GoToCover then AttackFromCover, cost 4, two states expanded. AttackInOpen at cost 6 was sitting on the open list the whole time and never came out.

Now read the whole table as a designer would. Eight starting worlds produce four different behaviors.

| Starting world | Plan | Cost | Why |
|---|---|---|---|
| loaded, cover | GoToCover, AttackFromCover | 4 | cover is cheap and makes the attack cheap |
| loaded, no cover | AttackInOpen | 6 | the only gun option left |
| empty, ammo, cover | GoToCover, Reload, AttackFromCover | 6 | reload behind cover; the other order also costs 6 |
| empty, ammo, no cover | Charge, Melee | 7 | Reload and AttackInOpen cost 8, so the knife wins by 1 |
| empty, no ammo | Charge, Melee | 7 | fetching ammo costs at least 5 + 2 + 2 + 2 = 11 |

Two rows deserve a second look. With an empty gun, ammo and no cover, the soldier charges with a knife rather than reloading, because 4 + 3 = 7 beats 2 + 6 = 8. Is that what you wanted? Nobody wrote that rule. It is a consequence of three costs, and you only find it by reading the plans. And the ammo crate is never used by this soldier in any world. FetchAmmo is too expensive to beat a charge. That is a dead action, and a planner will happily let you ship one.

The costs are the personality. Drop AttackInOpen from 6 to 3 and, with a loaded gun and cover nearby, the plan becomes AttackInOpen alone, at cost 3. You have made a reckless soldier by changing one number. Drop Melee from 3 to 1 and every soldier without cover charges, even with a loaded gun, because 4 + 1 = 5 beats 6.

### Move it yourself

Open [the interactive](../examples/w09-goap-planner.html). The left panel lists the three starting facts as toggles and the seven actions with editable costs and on/off switches. The right panel draws the search. Every world state the planner reached is a box labelled with its true facts. Arrows are actions with their costs. Expanded states are solid, states left on the open list are outlined, and the returned plan is drawn thick. Readouts show plan cost and states expanded. Toggle "loaded" off and watch the plan reroute through Charge and Melee. Raise Melee's cost to 5 and watch it switch back to reloading. Turn off every attack action and watch the search expand every reachable state and return nothing, which is the rat in F.E.A.R.'s level, described below.

### Cross-game recognition

**F.E.A.R. (Monolith, 2005), goal sets and action sets.** Orkin describes placing a soldier, an assassin and a rat in the same warehouse with the same goal set, Patrol and KillEnemy. The soldier patrols and then fires. The assassin, whose action set holds lunges and melee attacks, runs cloaked, sticks to walls and drops onto the player. The rat's action set has no attacks at all, so it cannot form any plan for KillEnemy and falls back to Patrol. In our form, the three characters share the goal and the planner and differ only in their `ACTIONS` list. Turning off our soldier's three attack actions reproduces the rat exactly: 4 states expanded, no plan. Orkin also describes adding flying drones late in development by combining the ghost's movement actions with the soldier's weapon actions, and he notes that F.E.A.R.'s world state was a fixed-size array of variables, which is our dictionary of facts.

**The same architecture in other games.** Orkin's own GOAP page lists shipped games that used GOAP architectures, among them Condemned: Criminal Origins (Monolith, 2005), which ran on the same AI system as F.E.A.R., S.T.A.L.K.E.R.: Shadow of Chernobyl (GSC Game World, 2007), Fallout 3 (Bethesda, 2008), Empire: Total War (Creative Assembly, 2009), Just Cause 2 (Avalanche, 2010) and Deus Ex: Human Revolution (Eidos, 2011). The list says the architecture was used. It does not say how, so treat it as evidence of spread, not as a description of any one game.

**Transformers: Fall of Cybertron (High Moon, 2012) and Killzone 3's multiplayer bots (Guerrilla, 2011).** Both used a close relative, the **hierarchical task network** (HTN) planner. Troy Humphreys describes Fall of Cybertron's version. It has a world state that sensors update, and primitive tasks with conditions and effects, exactly our actions. The difference is how the plan is found. Instead of searching over every order of actions, the designer writes compound tasks, each with a ranked list of methods ("if the enemy is in range, do these steps; otherwise these"), and the planner decomposes them top-down. Straatman and colleagues describe Killzone 3's bots running an HTN planner based on SHOP and rerunning it at a fixed rate. Rewritten in our terms, HTN is GOAP where the designer supplies the likely orders and the planner checks them against the world. It is faster and more controllable, and it finds only the plans a designer anticipated.

Three families, one principle. Describe actions by what they need and what they change, let search find the sequence, and let a change in the world produce a new sequence without new code.

### Eyes-open design judgment

- **You trade authorship for coverage.** In our table, 8 worlds give 4 behaviors, including the knife charge nobody asked for. A planner covers situations you never imagined, and some of what it does there will surprise you. Budget time to read plans, the way section 2 did, before players read them for you.
- **Costs are a design language with no grammar.** The difference between a cautious soldier and a reckless one was a single cost. That is powerful and fragile. Changing one cost can reroute plans in worlds you were not looking at. Keep a table like the one above as a regression test, as the lab does.
- **Search is not free.** Our soldier expanded at most 5 states. Each extra true-or-false fact can double the number of reachable worlds, and each extra action adds edges to every one of them. Orkin kept F.E.A.R.'s world state small and pushed expensive questions, such as "is there a path to safety?", into **procedural preconditions**, code that runs only when the planner considers that action.
- **Players cannot see a plan.** The dive through the window reads as clever only because the player saw the door attempts first. Orkin's paper spends pages on squad dialogue for this reason. Soldiers call out what they are doing, and he reports that F.E.A.R. had no complex squad behaviors at all. Flanking and pincers emerged from simple ones and were sold to the player by the dialogue. A planner makes behavior possible. Barks and animation make it visible.

## 3. How big is the search?

A world of `n` true-or-false facts has at most `2^n` states. Our soldier has 6 facts, so at most 64 states, and the planner never came close, because A* with a heuristic only expands states that look promising and because most states cannot be reached from a given start.

Three habits keep planning cheap in practice.

1. **Keep facts coarse.** `enemy_in_range` as one boolean, not a distance. Humphreys makes the same point for HTN: the world state only needs to represent what the planner reasons about, not everything the game knows.
2. **Plan rarely, execute often.** A plan is a queue of actions (CS102 week 6). The NPC runs the front action every tick and only replans when an action fails, the goal changes, or a watched fact changes. Killzone 3's bots replanned at a fixed rate. F.E.A.R.'s soldiers replanned when an action failed.
3. **Let something else choose the goal.** F.E.A.R.'s goals competed for activation, and the planner worked on the highest-priority one. Choosing the goal is a utility or behavior-tree problem. Choosing the steps is the planner's.

Orkin also notes one limitation of the fixed world state. Since there is one slot for "the target" and one for "the weapon", a soldier can only plan about one of each at a time. F.E.A.R. used separate targeting and weapon systems to pick which enemy and which gun the planner should think about.

## 4. When the plan breaks: replanning

Here is the door from the hook, as data. The soldier's goal is `in_room`.

| Action | Cost | Preconditions | Effects |
|---|---|---|---|
| OpenDoor | 1 | not `door_jammed` | `door_open` |
| KickDoor | 3 | not `door_barred` | `door_open` |
| WalkThroughDoor | 1 | `door_open` | `in_room` |
| DiveThroughWindow | 5 | none | `in_room` |

The soldier starts knowing nothing about the door, so both "not" preconditions hold. Each time an action fails, the soldier adds what it learned to its working memory and plans again.

| Plan number | What the soldier believes | Plan found | Cost | What happens |
|---|---|---|---|---|
| 1 | nothing | OpenDoor, WalkThroughDoor | 2 | OpenDoor fails: the player is holding it. Learn `door_jammed`. |
| 2 | `door_jammed` | KickDoor, WalkThroughDoor | 4 | KickDoor fails. Learn `door_barred`. |
| 3 | `door_jammed`, `door_barred` | DiveThroughWindow | 5 | Succeeds. |

That is Orkin's door sequence, produced by three plans and two learned facts. The window was in the soldier's action set from the start. It only became the cheapest option once the cheaper ones were ruled out by experience. The lab's `execute()` function runs exactly this loop.

Two design questions come with replanning. First, how long does a learned fact last? If `door_barred` never expires, the soldier will never try that door again, even after the player walks away. Give memories a lifetime. Second, what does the player see between plans? Three plans in a row with no pause look like twitching. A short "that didn't work" animation or bark between them makes the same behavior look deliberate.

## 5. Choosing a decision method

You have now met four ways for an NPC to decide. They are not ranked. They answer different questions.

| Method | The designer writes | The NPC decides | Good for | Watch out for |
|---|---|---|---|---|
| State machine (week 6) | states and every transition | which transition fires | few modes, strict control, readable rules | transitions grow as `N(N − 1)` |
| Behavior tree (week 7) | a priority tree of steps | which branch runs this tick | ordered steps with fixed priorities | tick rule; fixed priorities |
| Utility (week 8) | curves and considerations | which action scores highest | priorities that slide with the situation | switch points hidden in curves; dithering |
| Planner (this week) | actions with preconditions, effects, costs | the order of actions | multi-step problems that change at run time | search cost; plans nobody reviewed |

Shipped games mix them. F.E.A.R. had a three-state machine underneath its planner. Dragon Age: Inquisition scored actions with small trees. A common modern pattern is utility scoring to pick the goal, a planner or HTN to pick the steps, and a behavior tree or state machine to run each step's animation. When you choose, ask the week 1 questions. Will a player be able to read it? Can a designer tune it? Does it fit in the frame for every NPC on screen?

## In-class activity (25 minutes)

Groups of three. Each group gets cards for the soldier's seven actions and a blank "world" card with three fact checkboxes.

1. **Plan by hand (8 min).** Two members pick a starting world in secret and each writes the cheapest plan with its cost. The third checks them by running the open-list trace on paper. Repeat with a new world.
2. **Make a character (10 min).** Design a medic for the same squad using the same planner. Its goal is `ally_healed`. Write four to six actions with costs, including at least one that the soldier also has. Find one starting world where the medic's plan surprises you.
3. **Break it (7 min).** Pass your medic to another group. They must find a starting world where the medic has no plan at all, or a plan a player would call stupid. They write the world and the plan on your card.

Expected output: two checked hand plans, a medic action table, and the other group's breaking world with its plan.

## Common misconceptions

- **"GOAP is a different algorithm from A*."** It is A* on a different graph. The nodes are world states and the edges are actions. Everything from week 4, including admissibility, carries over.
- **"The planner makes the NPC smart."** It makes the NPC consistent with its action descriptions. If the costs say a knife charge beats reloading in the open, the planner will charge every time. The intelligence is in the action set, and so are the bugs.
- **"The NPC replans every frame."** Shipped planners replan on events (an action fails, the goal changes) or at a slow fixed rate. Between plans the NPC just runs the next action in its queue.
- **"Planning AI is unpredictable, so it is bad for games."** Given the same facts, a planner with a fixed tie-break returns the same plan every time. What changes is the world. Players can learn a planner's habits if its actions and costs stay consistent and its intentions are voiced.

## Check yourself

1. The soldier starts with an empty gun, ammo, and cover nearby. Give the plan and its cost. Name another plan with the same cost, and say why the search returns the one it does.
2. Change Melee's cost from 3 to 1. For each of the worlds "loaded, ammo, no cover" and "loaded, ammo, cover", give the new plan and cost.
3. In Orkin's pizza example, Alma can OrderPizza (cost 2) or BakePie (cost 8). Suppose OrderPizza now needs `has_money`, and DriveToBank (cost 7) gives `has_money`. Alma has a recipe but no money. What does she plan? What if she has neither?
4. A designer adds the goal `{enemy_dead, in_cover}` with the same heuristic, the number of unmet goal facts. Is the heuristic still admissible for the soldier's actions? Describe one new action that would make it inadmissible.
5. In the door example, the soldier's memory of `door_barred` never expires. The player walks away and the soldier needs to enter the same room ten minutes later. What does it do, and what would a player think? Propose a rule.

<details>
<summary>Answers</summary>

1. GoToCover, Reload, AttackFromCover, cost 2 + 2 + 2 = 6. Reload, GoToCover, AttackFromCover also costs 6. Both orders reach the same states with the same `f`, and the tie-break takes whichever was pushed first. From the start, GoToCover comes before Reload in the action list, so the cover branch is pushed and popped first.
2. "Loaded, ammo, no cover": Charge and Melee cost 4 + 1 = 5, which beats AttackInOpen at 6, so the loaded soldier charges with a knife. "Loaded, ammo, cover": GoToCover and AttackFromCover still cost 4, which beats 5, so it takes cover.
3. With the recipe and no money: BakePie at 8 beats DriveToBank then OrderPizza at 7 + 2 = 9, so she bakes. With neither: DriveToBank, OrderPizza, cost 9.
4. Yes. Every action costs at least 2 and sets at most one fact, so two unmet facts need at least two actions and a cost of at least 4, while `h` is at most 2. An action such as "DiveIntoCoverAndFire", costing 1 and setting both `in_cover` and `enemy_dead`, would make the true remaining cost 1 while `h` is 2, so `h` overestimates and A* may return a worse plan.
5. It skips the door, which is now open, and dives through the window at cost 5. A player sees an NPC ignore an open door, which is artificial stupidity from week 1. Rule: learned facts expire after a time, or are cleared when the NPC's sensors see the door open. Either way the planner gets the cheap plan back.

</details>

## Lab / assignment hook

[Lab 09, a goal-oriented action planner](../labs/lab09.md). You write the planner's state test, effect application, heuristic and A* search, reproduce this lecture's eight-world table and Orkin's pizza example, and run the door replanning loop. Then you design a second character that shares the soldier's goal but not its action set, and write a regression table that catches a cost change breaking a plan.

## Sources

- Orkin, J. (2006). "Three States and a Plan: The A.I. of F.E.A.R." Game Developers Conference 2006. F.E.A.R. (Monolith Productions, 2005). The three-state machine (Goto, Animate, UseSmartObject); STRIPS (Stanford Research Institute, about 1970) and the Alma example with OrderPizza cost 2.0 and BakePie cost 8.0; goal sets and action sets with the soldier, assassin and rat; drones built late from existing actions; adding goals and actions without specifying transitions; the door held shut, then kicked, then the window; working memory and re-planning; cost per action and A* over world states; the world state as a fixed-size array; procedural preconditions for expensive checks such as a path to safety; one target and one weapon in the planner at a time; squad behaviors, the absence of complex squad behaviors, and dialogue that makes coordination visible. https://www.gamedevs.org/uploads/three-states-plan-ai-of-fear.pdf
- Orkin, J. "Goal-Oriented Action Planning (GOAP)." Personal page at MIT Media Lab, read via the Internet Archive (2020 capture), September 2026. The list of games using GOAP architectures quoted in section 2, and the note that Condemned: Criminal Origins used the same architecture as F.E.A.R. http://alumni.media.mit.edu/~jorkin/goap.html
- Humphreys, T. (2013). "Exploring HTN Planners through Example." In S. Rabin (ed.), *Game AI Pro*, chapter 12. CRC Press. Free at gameaipro.com. Transformers: Fall of Cybertron (High Moon Studios, 2012). World state updated by sensors; primitive tasks with conditions and effects; compound tasks and methods; the world state only needs what the planner reasons about.
- Straatman, R., Verweij, T., Champandard, A., Morcus, R. and Kleve, H. (2013). "Hierarchical AI for Multiplayer Bots in Killzone 3." In S. Rabin (ed.), *Game AI Pro*, chapter 29. Free at gameaipro.com. Killzone 3 (Guerrilla Games, 2011). Individual bots use an HTN planner based on SHOP; the planner is rerun at a fixed rate.
- Hanlon, S. and Watts, C. (2017). "Behavior Decision System: Dragon Age Inquisition's Utility Scoring Architecture." *Game AI Pro 3*, chapter 31. Scoring with evaluation trees, for section 5; see [CS203 week 8](w08-utility-ai.md).
- Millington, I. (2019). *AI for Games*, 3rd ed. CRC Press. Chapter 5, goal-oriented behavior.
- The soldier's action table, its costs, the door costs and all computed plans are invented for teaching and computed with the code in this lecture and in `labs/lab09-starter/goap.py`.

## Interactive spec: examples/w09-goap-planner.html

**The one insight:** the designer writes seven actions and no transitions, and the planner turns each world into its own plan. Flip one fact or change one cost and the plan reroutes, sometimes into a behavior nobody asked for (the knife charge). Seeing the search graph redraw, with the chosen plan drawn thick through it, is the moment the lesson lands.

**Layout.** Two linked panels, side by side at 1280 px, stacked at 390 px (controls on top), and a door strip underneath.

- **Left, "World and actions":** three toggles for the starting facts (`weapon_loaded`, `has_ammo`, `cover_nearby`), default all on. Below, a table of the seven actions, one row each: an on/off switch, the name, a cost number input (integer 1 to 20), and the preconditions and effects as small text chips. A Reset button restores the lecture's values.
- **Right, "Search":** every state the planner pushed, drawn as a box listing its true facts (abbreviated: L = loaded, A = ammo, C = cover nearby, IC = in cover, N = near enemy, D = enemy dead). Lay out by depth (number of actions from the start) left to right. Arrows are actions labelled "name (cost)". Expanded states have a solid fill and a small badge with their expansion order (1, 2, ...). States left on the open list are outlined only. The goal state that was returned has a thick border, and the plan's arrows are thick. Readouts above the graph: "plan: A > B > C", "cost N", "states expanded N", or "no plan (N states expanded)".
- **Bottom, "The door":** a four-step strip replaying the section 4 replan. Buttons "OpenDoor fails" and "KickDoor fails" toggle the two failures (default both on). The strip shows each plan in order, what was learned, and the final action, using the lecture's door table.

**Controls (keyboard accessible).** All toggles and inputs reachable by Tab with visible focus; the graph is decorative for screen readers, and a text list of the plan and expansions is provided in a visually hidden live region that updates on every change.

**Formulas.** Implement exactly the planner in the lecture's code block: states are maps of fact to boolean, a missing fact is false; `holds(state, facts)` compares with missing as false; state identity is the set of true facts; `h` = number of unmet goal facts; the open list is ordered by `(f, push counter)` with the counter increasing on every push; pop, skip if closed, close, return if goal holds, otherwise count one expansion and push each enabled action in table order whose resulting state is not closed. Goal is `{enemy_dead: true}`. Door: actions OpenDoor (1, requires not `door_jammed`, gives `door_open`), KickDoor (3, requires not `door_barred`, gives `door_open`), WalkThroughDoor (1, requires `door_open`, gives `in_room`), DiveThroughWindow (5, no requirement, gives `in_room`). Execution: plan, run actions in order; if an action is marked as failing, add its learned fact (`door_jammed` for OpenDoor, `door_barred` for KickDoor), and replan; each action fails at most once.

**Test values (must match).**

- The eight worlds (loaded, ammo, cover as 1/0): 111 cost 4, expanded 2, GoToCover > AttackFromCover. 110 cost 6, 2, AttackInOpen. 101 cost 4, 2, GoToCover > AttackFromCover. 100 cost 6, 2, AttackInOpen. 011 cost 6, 5, GoToCover > Reload > AttackFromCover. 010 cost 7, 4, Charge > Melee. 001 cost 7, 5, Charge > Melee. 000 cost 7, 3, Charge > Melee.
- World 111, AttackInOpen cost 3: plan AttackInOpen, cost 3.
- Melee cost 1: world 110 gives Charge > Melee, cost 5; world 111 still GoToCover > AttackFromCover, cost 4.
- World 111 with AttackFromCover, AttackInOpen and Melee switched off: no plan, 4 states expanded.
- Door with both failures: plans OpenDoor > WalkThroughDoor (2), then KickDoor > WalkThroughDoor (4), then DiveThroughWindow (5); actions attempted OpenDoor, KickDoor, DiveThroughWindow; 3 plans. With no failures: OpenDoor, WalkThroughDoor, 1 plan.

**First screen.** World 011 (empty gun, ammo, cover), so the graph shows the five expanded states and the three-step plan with "cost 6, states expanded 5". Caption: "Seven actions, no transitions. Flip a fact and the plan reroutes."

**Accessibility.** Respects `prefers-reduced-motion` (no animated graph layout; redraw instantly) and `prefers-color-scheme`. Palette from `templates/interactive-tokens.css`. Expanded versus open states are distinguished by fill versus outline, not by color alone. No game art, logos or characters; boxes and arrows only.
