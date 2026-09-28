# CS102 · Week 09 — Pattern: Component

**Why this matters:** In week 2 you split a god class into components and watched a design with 169 parts describe 7,300 object types. That solved the *authoring* problem. It opened three runtime questions that every component-based game has to answer. How does the burning system find the 50 burning things among 10,000 entities without checking all 10,000 every frame? How do a Health component and a health bar talk without knowing each other? In what order do the systems run? This week you answer all three in code and measure the first one.

**You will be able to:**
- Implement a `World` that keeps a component index and answers queries like "every entity with Burning and Health" in spawn order.
- Compute and measure the per-frame cost of polling every entity versus querying an index, and compare it with a 16.7 ms frame budget.
- Choose between the three ways components communicate (shared container state, direct references, messages) for a given pair of components, and justify the choice.
- Design a system update order and deferred destruction so that removing entities mid-frame neither crashes nor draws dead objects.

**Before class:** Nystrom, *Game Programming Patterns* (2014), "Component" chapter, the whole "Design Decisions" section, especially "How do components communicate with each other?" (you read the motivation for week 2). Unity Entities documentation (package 1.3), "EntityQuery overview", one page. Godot documentation (stable, 4.x), "Groups".

**Prerequisites from earlier courses:** [CS102 week 2, inheritance vs composition](w02-inheritance-vs-composition.md) (the component pattern itself, Dungeon Siege, Unity GameObjects, and why the class tree fails; this lecture does not repeat it). [CS102 week 5, arrays, linked lists and hash maps](w05-arrays-linked-lists-and-hash-maps.md) (why a dict lookup is fast on average). [CS102 week 4, Big-O](w04-big-o-intuition-for-game-developers.md) (`O(N)` versus `O(k)`). [CS101 week 7, scenes, nodes and scripts](../../CS101-programming-for-games-i/lectures/w07-engine-intro-scenes-nodes-scripts.md) (update order and the one-frame lag). The 16.7 ms frame at 60 fps from [CS101 week 9, delta time](../../CS101-programming-for-games-i/lectures/w09-delta-time-and-frame-rate-independence.md).

**Interactive:** [w09-component-queries.html](../examples/w09-component-queries.html). Keep it open during section 2.

---

## 1. From components to systems

Recall where week 2 ended. An entity is a name plus a bag of components, and each component holds one slice of behaviour: `Health`, `Mover`, `Render`, `AI`. A goblin is `Render + Mover + Health + AI`. A chest is `Render + Health`. Types are data, so a designer makes a mimic by writing a line, not a class.

There are two ways to run such a game each frame.

**Entity-driven update.** Loop over entities, and let each entity update its own components. This is the shape of Nystrom's Bjørn example and of Unity's classic `MonoBehaviour.Update`. Each component's code runs inside its owner's turn.

```python
for e in entities:
    for c in e.components.values():
        c.update(e, dt)
```

**System-driven update.** Components hold data, and **systems** hold behaviour. A system is a function that runs once per frame over every entity that has the components it needs. The move system wants `Mover` and `Position`. The burn system wants `Burning` and `Health`.

```python
def move_system(world, dt):
    for e in world.query(Mover, Position):
        m, p = e.get(Mover), e.get(Position)
        p.x += m.vx * dt
        p.y += m.vy * dt
```

This lecture uses the system-driven form, for two reasons. It makes each frame's order explicit, a list of systems you can read (section 5). And it turns "who needs updating?" into a **query**, and queries can be fast or slow depending on how you store things. That is the worked example.

The vocabulary, fixed for the rest of the term:

- **Entity:** an identity with a set of components. No behaviour of its own.
- **Component:** a small object of data for one concern, plus at most the logic that guards its own data (such as `Health.damage` clamping at 0).
- **System:** a function that runs each frame over the entities matching a query.
- **World:** the object that owns the entities and answers queries.
- **Query:** "give me every entity that has all of these component types."

When all four are present and components are pure data, people call the design an **entity-component-system (ECS)**. CS201 week 5 builds a fast one in C++. Today you build a small, clear one in Python.

## 2. Worked example: finding 50 burning goblins among 10,000 entities

### The hook

Unity's reference page for `GameObject.Find` carries a warning. The function searches the whole scene on every call, the result is not cached, and calling it inside `Update` degrades performance as the scene grows. The advice is to look the object up once and keep the reference. That warning exists because the obvious code, "search everything, every frame", works perfectly in a test scene of 20 objects and falls over in the shipped game with 20,000.

A component query has the same trap. The first `query` every student writes looks at every entity and keeps the matches. On the author's laptop, in Python, that takes 0.15 ms for 1,000 entities. It looks free. At 100,000 entities it takes 15.9 ms, and a 60 fps frame is 16.7 ms long. One system has eaten the whole frame, and your game has a dozen systems.

### The model

Let `N` be the number of entities and `S` the number of systems. System `s` queries a set of component types `Q_s`. Let `n_c` be the number of entities holding component type `c`.

**Polling.** Each query scans every entity and checks it.

```
checks_poll = S × N                       per frame
```

**Indexing.** The world keeps an **index**: a dict from component type to the set of entities holding that type. It updates the index whenever a component is added or removed. A query starts from the smallest index set among its types and checks only those entities.

```
checks_index = Σ over systems s of  min(n_c for c in Q_s)      per frame
bookkeeping  = 1 extra dict operation per component add or remove
```

The whole idea in one line. **Polling pays for every entity that exists. Indexing pays for the entities that match, plus a small fee each time a component comes or goes.** Polling cost grows with the size of the world. Index cost grows with the size of the answer.

Here is the index in code. It uses a dict with `None` values as an ordered set, because Python dicts keep insertion order (guaranteed since Python 3.7) and plain sets do not. You will see in section 3 why the order matters.

```python
class Entity:
    def __init__(self, name):
        self.name = name
        self.components = {}                   # component class -> component

    def get(self, cls):
        return self.components.get(cls)

    def has(self, *classes):
        return all(c in self.components for c in classes)


class World:
    def __init__(self):
        self.entities = {}                     # name -> Entity, in spawn order
        self.index = {}                        # component class -> {Entity: None}

    def spawn(self, name):
        e = Entity(name)
        self.entities[name] = e
        return e

    def add(self, e, component):
        e.components[type(component)] = component
        self.index.setdefault(type(component), {})[e] = None

    def remove(self, e, cls):
        del e.components[cls]
        del self.index[cls][e]

    def query_poll(self, *classes):            # O(N)
        return [e for e in self.entities.values() if e.has(*classes)]

    def query(self, *classes):                 # O(size of the smallest index set)
        sets = [self.index.get(c, {}) for c in classes]
        return [e for e in min(sets, key=len) if e.has(*classes)]
```

`query` returns a new list, not the index itself. That detail saves you from a crash in section 5.

### Numbers you can check

Take a world of `N = 10,000` entities. Every entity has `Position` and `Health`. 90% render, 30% move, 5% have AI and 0.5% are on fire. Four systems run each frame.

| System | Query | Smallest index set | Poll checks | Index checks |
|---|---|---|---|---|
| Render | Render, Position | Render: 9,000 | 10,000 | 9,000 |
| Move | Mover, Position | Mover: 3,000 | 10,000 | 3,000 |
| AI | AI, Position | AI: 500 | 10,000 | 500 |
| Burn | Burning, Health | Burning: 50 | 10,000 | 50 |
| **Total** | | | **40,000** | **12,550** |

Check the total with the formulas. `S × N = 4 × 10,000 = 40,000`. The index sum is `9,000 + 3,000 + 500 + 50 = 12,550`. Overall the index does about a third of the work. For the render system it saves almost nothing, 10% of checks, because nearly everything renders. For the burn system it does 1/200 of the work. **The rarer the component, the more the index wins.** That is why the gain is largest for exactly the systems you add late in a project: status effects, quest markers, the one boss with a special mechanic.

Now the measured times. This is `query_poll(Burning, Health)` against `query(Burning, Health)`, with the burning share at 0.5% and random membership from a fixed seed. Best of 30 runs, Python 3.13 on an Apple M4 Pro laptop, September 2026. Lab 09 prints this table on your machine.

| N | Burning entities | Poll (ms) | Index (ms) | Poll ÷ index |
|---|---|---|---|---|
| 1,000 | 3 | 0.145 | 0.0008 | about 180 |
| 10,000 | 54 | 1.608 | 0.0113 | about 140 |
| 100,000 | 471 | 15.889 | 0.0953 | about 170 |

The poll column grows tenfold with each tenfold jump in `N`, which is `O(N)`. The index column grows with the number of burning entities, which also happens to grow tenfold here because the share is fixed. Set the fire on a single boss among 100,000 entities and the indexed query takes 0.0004 ms, while polling still takes 15.9 ms. Your numbers will differ from these. The ratio and the shape will not.

Put the last row against the frame budget. At 60 fps a frame is `1000 / 60 = 16.7 ms`. One polling query on 100,000 entities uses 15.9 ms of it, 95%, before any system does real work. The indexed query uses 0.095 ms, about 0.6% of the frame.

### A visual you can move

Open the interactive. The left panel is the world: a grid of up to 10,000 small squares, one per entity, coloured by the components each has. Pick a system from the list. In **poll** mode a scan line sweeps across every square and a counter climbs to `N`. In **index** mode only the matching squares light up, one by one, and the counter stops at the index size. The right panel is a chart of checks per frame against `N`, from 1,000 to 100,000 on a log scale, with one line for polling and one for the index, and a horizontal band for the 16.7 ms budget converted to checks with a per-check cost you can set.

Drag the "Burning share" slider down to 0.01%. The index line drops to the floor of the chart and the poll line does not move at all. That flat poll line is the insight. **Polling does not care how many entities match. It pays for the world.**

### Cross-game recognition

- **Unity, `GameObject.Find` (Unity 6).** The reference warns that each call performs the full search again and recommends caching the result at startup. A cached reference is an index of size one, built once.
- **Unity Entities package (1.3).** An `EntityQuery` finds every **archetype**, a group of entities with exactly the same set of component types, that contains the requested types. It then gathers those archetypes' storage chunks for a system to process. That is our index at a coarser grain. Instead of one set per component type, the engine keeps one group per distinct combination and skips whole groups that cannot match.
- **Godot 4, groups.** You add a node to named groups, in the editor or with `add_to_group()`. The `SceneTree` then hands you every node in a group and can call a method on all of them. A group called `"burning"` is a hand-maintained index. Your code keeps it correct by calling `add_to_group` and `remove_from_group` at the right moments, which is exactly the bookkeeping fee in our model.
- **Overwatch (Blizzard, GDC 2017).** Timothy Ford's talk on Overwatch's gameplay architecture describes an entity component system at the centre of the game's hero mechanics and netcode. Systems that act on components are the organising unit of a large shipped game, not a classroom idea.

Four tools, one rule. **Don't search the world for the few things you need every frame. Keep a list of them, and keep the list correct when things change.**

### Eyes-open design judgment

- **Polling is fine when `N` is small.** At 1,000 entities a polling query costs 0.15 ms here. If your game will never have more than a few hundred objects, the simpler code wins, and a bug-free index is extra code to get right.
- **Indexing moves cost from reads to writes.** Every `add` and `remove` now touches the index. A component that is added and removed thousands of times a frame, such as a one-frame "was hit" flag, can cost more to index than to poll. For those, use a field on an existing component, or a list rebuilt once per frame.
- **The index must never go stale.** An entity destroyed without leaving the index will be updated after death, frame after frame, the classic "ghost" bug. Section 5 fixes this with deferred destruction, which removes every doomed entity from every index set at one point in the frame.
- **Order is a design decision.** Iterating a Python `set` of objects can give a different order in two runs of the same game, because objects hash by identity. Most of the time nobody notices. Then you build deterministic replay (week 12) and two runs diverge on frame 3,000 because two goblins attacked in a different order. Ordered dicts, or sorting by entity id, remove the problem.
- **Archetypes are the next step, not this one.** Grouping entities by exact component set, as Unity Entities does, also makes memory access fast. CS201 weeks 5 and 6 cover why. Build the simple per-type index first and measure before reaching for it.

### Check yourself (worked example)

1. A world has 50,000 entities and 6 systems. How many checks does polling do per frame?
2. In that world, the systems' smallest index sets are 45,000, 15,000, 2,500, 400, 100 and 5. How many checks does the index do? What fraction of polling is that?
3. Using the measured poll cost from the table, about 0.16 microseconds per entity check, how many polling systems over 100,000 entities fit in a 16.7 ms frame with nothing else running?

<details>
<summary>Answers</summary>

1. `6 × 50,000 = 300,000` checks.
2. `45,000 + 15,000 + 2,500 + 400 + 100 + 5 = 63,005` checks, about 21% of polling.
3. One query costs `100,000 × 0.16 µs = 16 ms`, so just 1. A second polling system already blows the frame.

</details>

## 3. How components talk to each other

Components never live fully apart. The health bar needs the health. The animation needs to know whether the body is on the ground. Nystrom lists three ways for components to communicate, and notes that real games use more than one.

**1. Through shared state on the container.** One component writes a value the entity (or a shared component) owns, and another reads it. In our code, `AI` writes `Mover.vx` and `vy`, and the move system reads them. Neither knows the other exists. This keeps components decoupled, but the shared data must live somewhere both can see, and it tends to pile up in a few "everyone uses this" components such as `Position`.

**2. By direct reference.** One component holds a reference to another and calls it.

```python
class HealthBar:
    def __init__(self, health):
        self.health = health                   # a reference to one Health component

    def fraction(self):
        return self.health.hp / 100.0
```

Fast and obvious. Also tight coupling, because `HealthBar` breaks if the entity has no `Health`. Use it for pairs that always come together and are really one feature split for tidiness. Week 2 noted that Neversoft moved to direct pointers on the *Tony Hawk* games because routing every lookup through a manager cost CPU time.

**3. By message.** A component announces something happened ("damaged by 12"), and whoever cares reacts. The sender does not know the receivers. That is the most decoupled and the hardest to debug, since cause and effect are far apart in the code. Next week's lecture, [week 10, observer and events](w10-observer-and-events.md), is entirely about this option.

A rule of thumb for picking:

| Relationship | Example | Use |
|---|---|---|
| Many systems read one fact every frame | Position, velocity | Shared state |
| Two components that always travel together | Health and its health bar | Direct reference |
| One event, unknown or changing listeners | "died", "picked up item" | Message (week 10) |

## 4. Swapping a component changes who is in control

Nystrom's example ends with the trick that sells the pattern. Bjørn reads the controller through an `InputComponent`. For the game's demo mode, the team writes a `DemoInputComponent` that drives Bjørn with AI, and builds Bjørn with that instead. Physics, graphics and sound code do not change at all.

The same move gives you three kinds of control from one entity type:

```python
class PlayerInput:                            # reads the real controller
    def intent(self, e, frame):
        return read_gamepad()

class ChaseInput:                             # AI drives the entity
    def intent(self, e, frame):
        return direction_toward(e, "player")

class ReplayInput:                            # plays back recorded intents
    def __init__(self, recording):
        self.recording = recording            # list of intents, one per frame
    def intent(self, e, frame):
        return self.recording[frame]
```

An input system asks whichever input component the entity has for this frame's intent and writes it to `Mover`. Put `ReplayInput` on the player and the game replays a recorded session. That is the heart of the course's signature example in week 12, where you record 30 seconds of inputs and replay them exactly. Replay only works if everything else in the frame is deterministic, which is one more reason the index must iterate in a fixed order.

## 5. The frame as a list of systems

With system-driven update, one frame is a list you can read top to bottom:

```python
SYSTEMS = [input_system, ai_system, move_system, collision_system,
           burn_system, render_system]

def frame(world, dt):
    for system in SYSTEMS:
        system(world, dt)
    world.flush()                              # destroy doomed entities last
```

Two problems show up as soon as entities die during a frame.

**Modifying what you are iterating.** If `burn_system` removed a dead entity from the index while looping over `world.query(...)`, and `query` returned the live index set, Python would stop with `RuntimeError: dictionary changed size during iteration`. Returning a copy avoids the crash, but now entities leave the world at scattered points in the middle of the frame, wherever some system happens to kill them, and what each later system sees depends on which systems ran before it. The fix engines use is **deferred destruction**. Mark the entity doomed and remove it once, at a fixed point after all systems run. Godot's `queue_free` does exactly this, queueing the node for deletion at the end of the current frame.

```python
def destroy(self, e):
    self.doomed.append(e)

def flush(self):
    for e in self.doomed:
        self.entities.pop(e.name, None)
        for cls in e.components:
            self.index.get(cls, {}).pop(e, None)
    self.doomed.clear()
```

Be clear about what deferral buys and what it costs. It buys one place where entities leave the world, so no loop crashes and the index never holds a half-removed entity. It does not hide the dead. A doomed entity stays in every query until `flush()` runs, so every system that runs after `destroy()` in the same frame still sees it. A system that must not act on the dead, such as render or AI targeting, has to skip doomed entities itself, for example by checking `hp > 0` or a `doomed` flag that `destroy` sets.

**Order-dependence.** Now the order of the list matters. Put `burn_system` before `render_system`, and a chest that burns to 0 hp this frame is still in the render query, because it is only doomed, not gone. Unless render skips doomed entities, the player sees one frame of a 0-hp chest before it vanishes. Put `render_system` first instead and the chest is drawn at its hp from before the tick, then disappears after the flush. Every picture is then one frame behind the damage. At 60 fps either effect lasts 16.7 ms and is usually invisible, though a 0-hp health bar can show up as a flicker. Put `collision_system` before `move_system`, and every collision is tested against last frame's positions, the same one-frame lag you measured in CS101 week 7, now between systems instead of nodes. Scott Bilas listed "operations can end up being order-dependent" among the pitfalls of Dungeon Siege's component system. The list makes the order visible. It does not choose it for you.

A sensible default order reads the way cause and effect flow: gather intent (input, AI), apply it (move), resolve consequences (collision, damage, burn), show the result (render, skipping anything doomed), then clean up (flush).

## In-class activity (25 minutes)

Pairs. You are given the component shares for a city-builder world of 40,000 entities: `Position` 100%, `Render` 85%, `Citizen` 40%, `Mover` 25%, `OnFire` 0.2%, `Selected` 0.01%, and six systems: render, citizen needs, move, fire spread, fire damage (`OnFire + Health`), selection highlight.

1. **Compute (10 min).** For each system, write its query, its smallest index set and its poll and index checks. Total both columns.
2. **Decide (8 min).** `Selected` changes whenever the player clicks, and a new `WasHitThisFrame` component would be added and removed about 2,000 times per frame in a battle. For each one, decide "index it" or "poll or use a field", and give the number that decided it.
3. **Order (7 min).** Write the six systems plus `flush` in an order for one frame. Mark one place where swapping two systems would cause a one-frame visual bug, and say what the player would see.

Expected output: a table with two totals, two decisions with numbers, and an ordered system list with one annotated risk.

## Common misconceptions

- **"Components make the game faster."** The pattern organises code. Speed comes from how you store and query components. A component design that polls every entity every frame can be slower than a well-written class hierarchy.
- **"An index is always better."** It trades faster reads for slower writes and extra memory. For components that churn every frame, or worlds of a few hundred entities, polling or a field is often the better call.
- **"Removing an entity immediately is safest."** Removing during iteration either crashes or makes entities vanish at scattered points mid-frame, so what each system sees depends on the systems before it. Defer destruction to one fixed point, and have the systems that must ignore the dead skip doomed entities until then.
- **"Iteration order doesn't matter, it's just a loop."** It decides which goblin attacks first, and whether a replay matches the original. Make it deterministic on purpose.

## Check yourself

1. Write a one-line body for `World.query` that returns entities having all of `classes`, starting from the smallest index set.
2. A world has 20,000 entities, 5% with `AI`. The AI system polls. By what factor would an index cut its checks?
3. `Stunned` is added to about 300 entities and removed from about 300 each frame during a big fight, in a world of 5,000 entities. One system queries `Stunned`. Count per-frame operations for polling versus indexing (count one index update per add or remove, and one check per entity visited). Which is cheaper, and by how much?
4. A player reports that a boss killed by a burn tick is sometimes drawn at 0 hp for one frame. The frame runs `burn_system` before `render_system` and uses deferred destruction. Explain why it happens and give two fixes.
5. Your index uses a Python `set` for each component type. A replay of the same inputs diverges after a few minutes. Explain how the index could cause this and what to change.

<details>
<summary>Answers</summary>

1. `return [e for e in min((self.index.get(c, {}) for c in classes), key=len) if e.has(*classes)]`
2. Polling checks 20,000 and the index checks 1,000, a factor of 20.
3. Polling: 5,000 checks. Indexing: 600 updates plus about 300 checks (the size of the `Stunned` set) is 900. Indexing is still cheaper here, by about 5.5 times. It would lose once churn passed about 4,700 changes a frame, since `changes + 300` would then exceed 5,000.
4. The burn tick kills the boss and calls `destroy`, but the boss stays in every query until `flush()` at the end of the frame. Render runs after burn, so it still finds the boss and draws it at 0 hp. Fix one: have render skip doomed entities (check `hp > 0` or a `doomed` flag). Fix two: run render before burn, which hides the 0-hp frame but draws every frame's damage one frame late. The first keeps cause-then-effect order and is usually the better choice.
5. A set of objects can iterate in a different order between runs, since objects hash by identity. If two systems' results depend on order (who attacks first, who picks up the item), runs diverge. Use a dict as an ordered set, or sort query results by a stable entity id.

</details>

## Lab / assignment hook

[Lab 09, a world with a component index](../labs/lab09.md). Implement `World.add`, `remove`, `query_poll`, `query` and deferred destruction, write the AI, move and burn systems, add two new entity types as data, then run the timing table on your own machine. Deliverable: the completed Python file passing all tests, your timing table, and a 150-word note on where your game's index would not be worth it.

## Sources

- Nystrom, R. (2014). *Game Programming Patterns*, "Component" chapter (gameprogrammingpatterns.com). The Bjørn example, `DemoInputComponent` for demo mode, and the three ways components communicate (container state, direct references, messages), paraphrased.
- Unity Scripting API, `GameObject.Find` (Unity 6, accessed September 2026). Performance warning; no automatic caching; full search on every call; recommendation to cache at startup.
- Unity Entities package documentation 1.3, "EntityQuery overview" (accessed September 2026). A query finds archetypes containing the requested component types and gathers their chunks for a system to process.
- Godot Engine documentation, "Groups" and class reference `SceneTree` (stable, 4.x, accessed September 2026). Adding nodes to groups, getting all nodes in a group, calling methods on a group.
- Godot Engine documentation, class reference `Node` (stable, 4.7). `queue_free` queues the node for deletion at the end of the current frame.
- Ford, T. (2017). "'Overwatch' Gameplay Architecture and Netcode." GDC 2017, GDC Vault. The session description names an entity component system as the core of Overwatch's gameplay architecture.
- Bilas, S. (2002). "A Data-Driven Game Object System." GDC 2002 slides (Gas Powered Games, *Dungeon Siege*). Listed pitfalls include components becoming intertwined and operations becoming order-dependent.
- Python documentation, "Mapping types, dict" (Python 3). Dictionaries preserve insertion order, guaranteed since 3.7.
- Timing table: measured by the author with the code in lab 09 (Python 3.13.5, Apple M4 Pro, September 2026). Component shares and entity counts are invented for teaching.

## Interactive spec: examples/w09-component-queries.html

**The one insight:** polling cost depends on how many entities exist, and index cost depends on how many match. Drag the rare component's share toward zero and the index line falls to the floor while the polling line does not move.

**Layout.** Two linked views, side by side at 1280 px, stacked at 390 px (chart on top on mobile, since the grid is less readable when small).

- **Left, "World":** a square grid of `min(N, 10,000)` cells (when `N` exceeds 10,000, show a caption "showing a 10,000-entity sample; counts use full N"). Each cell is coloured by the rarest component it has among the five (Burning, AI, Mover, Render, Health-only), using the shared categorical palette with a legend. Membership is generated from a seeded pseudo-random generator (seed 1, mulberry32 or similar) so the grid is stable between reloads and between modes.
- **Right, "Checks per frame":** x axis `N` from 1,000 to 100,000 (log scale), y axis checks per frame (log scale). Line "Poll" = `S × N` for the selected systems. Line "Index" = sum over selected systems of the expected smallest index set, `min_share × N`. A horizontal band marks the frame budget in checks, `16,700 µs ÷ cost per check`. A vertical marker shows the current `N`, with both values labelled.
- **Readouts (copyable):** for the selected systems, a table with System, Query, Smallest set, Poll checks, Index checks; a totals row; "Poll uses X% of the frame budget, index uses Y%".

**Controls (keyboard accessible, labelled):**

1. Entities `N`: slider on a log scale from 1,000 to 100,000, default 10,000.
2. Shares: Render (default 90%), Mover (30%), AI (5%), Burning (0.5%), each a slider from 0.01% to 100%. Position and Health are always 100%.
3. System checkboxes: Render (Render, Position), Move (Mover, Position), AI (AI, Position), Burn (Burning, Health). All on by default.
4. Mode for the grid animation: Poll or Index. "Play" runs the selected system's scan: in Poll, a highlight visits every cell in order and the counter climbs to `N`; in Index, only matching cells light, in spawn order, and the counter stops at the set size. Animation lasts at most 2 s; under `prefers-reduced-motion`, skip to the final state.
5. Cost per check in microseconds: number input, default 0.159 (poll, the lecture's 15.889 ms ÷ 100,000) and a separate 0.2 for index checks, labelled "from the lecture's measurement; replace with your lab 09 numbers".

**Formulas.** `poll_checks = S × N`. For each system, `smallest = min(share_c for c in query) × N`, rounded to the nearest integer. `index_checks = Σ smallest`. `poll_ms = poll_checks × cost_poll / 1000`, `index_ms = index_checks × cost_index / 1000`. Budget = 16.7 ms.

**Test values (defaults, all four systems):** `N = 10,000`: Render 9,000, Move 3,000, AI 500, Burn 50; poll 40,000, index 12,550; poll_ms 6.4, index_ms 2.51. Burn system only, `N = 100,000`: poll 100,000 checks, 15.9 ms (95% of budget); index 500 checks, 0.10 ms. Burn only, Burning share 0.01%, `N = 100,000`: index 10 checks, poll still 100,000.

**First screen.** Burn system only selected, `N = 100,000`, so the poll bar sits at the budget line and the index bar near zero. Caption: "One system, 100,000 entities, 500 on fire. Which query fits in a frame?"
