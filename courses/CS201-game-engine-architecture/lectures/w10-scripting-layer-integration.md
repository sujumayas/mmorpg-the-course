# CS201 · Week 10 — Scripting Layer Integration

**Why this matters:** Most of the code that makes a game fun is not engine code. Quests, abilities, UI and mods are written in a second, friendlier language that the engine calls into. Where you draw the line between the two languages, and how often code crosses it, decides whether designers can iterate in seconds and whether 10,000 scripted objects fit in a frame.

**You will be able to:**
- Compute the per-frame cost of script calls with the crossing model `T = X × c_cross + N × c_work`, and find the batch size where crossings stop mattering.
- Design a binding API that passes values and generation-checked handles instead of raw pointers, and explain which bug each rule prevents.
- Apply a work budget to scripts using coroutines, and name what a sandbox removes and why.
- Critique a shipped engine's scripting boundary (Unity, World of Warcraft, Factorio, Roblox) in terms of crossings, handles and capabilities.

**Before class:** Gregory, *Game Engine Architecture* (3rd ed., 2018), chapter 16, the sections on scripting and on script-to-engine interfaces. Ierusalimschy, *Programming in Lua* (4th ed., 2016), chapter 27 "An Overview of the C API", about 15 pages. Skim the Lua 5.4 reference manual, section 4.1 "The Stack".

**Prerequisites from earlier courses:** [CS101 week 7, scenes, nodes and scripts](../../CS101-programming-for-games-i/lectures/w07-engine-intro-scenes-nodes-scripts.md) (you have already written scripts that an engine calls every frame). [CS102 week 9, the component pattern](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w09-pattern-component.md) (the frame as a list of systems). [CS102 week 10, observer and events](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w10-observer-and-events.md) (poll versus push). [CS102 week 13, data-driven design](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w13-data-driven-design-stats-in-json-and-csv.md) (when a table is enough and you need no script at all). [CS201 week 5, ECS design](w05-entity-component-system-design.md) (generational handles). [CS201 week 7, resources and hot reload](w07-resource-management-and-hot-reload.md) (handles, not pointers, and reloading). Looking ahead: [CS203 week 14, AI time-slicing](../../CS203-artificial-intelligence-for-games/lectures/w14-performance-ai-lod-and-time-slicing.md) (next semester) spreads AI work across frames the same way this week spreads scripts.

**Interactive:** [w10-boundary-crossings.html](../examples/w10-boundary-crossings.html). Keep it open during section 2.

---

## 1. Why an engine speaks two languages

Your engine core is C++. It owns memory, the frame loop, the renderer and the physics world, and it is compiled ahead of time for speed. Changing one line of it means recompiling and relinking, then restarting the game and walking back to the spot you were testing. On a large project that loop takes minutes.

Gameplay code changes far more often than engine code. A designer tuning a boss phase may try thirty versions in an afternoon. So most engines add a **scripting layer**. It is a second language, usually interpreted or compiled just in time, in which gameplay rules are written. The engine **embeds** the language's runtime (a virtual machine, or VM) and calls into it. You met this split in CS101 week 7. Godot ran your GDScript `_process` function every frame, and you never saw the C++ that called it.

A scripting layer buys four things.

- **Iteration speed.** Reload a script file while the game runs and see the change in a second. Week 7's hot reload applies to scripts as much as to textures.
- **A wider pool of authors.** Designers and modders can write Lua or a visual graph without learning C++ memory rules.
- **A safety boundary.** Script code cannot corrupt engine memory if the language never gives it a raw pointer. Mods written by strangers run inside the boundary.
- **Data that behaves.** In CS102 week 13 you moved numbers out of code into tables. Scripts are the next step, for rules too irregular to be a table row.

It also costs things. Script code runs slower than C++ doing the same arithmetic. Every call between the two languages pays a toll. And you now debug two languages with two call stacks. The rest of this lecture is about controlling those costs.

Three words you will use all week:

- A **binding** is an engine function made callable from script, or a script function made callable from the engine.
- A **crossing** is one call that passes the boundary in either direction. Arguments go across, results come back.
- **Marshalling** is converting values between the two languages' representations during a crossing. A C++ `float` becomes a Lua number, a C++ `std::string` becomes a Lua string (a copy).

## 2. Worked example: the 10,000 Updates

### The hook

In December 2015 Valentin Simonov of Unity Technologies published a post titled "10000 Update() calls." He built a scene with 10,000 objects, each with a C# `Update()` method whose whole body was `i++`. Unity's C++ core called each of those methods once per frame. In a second scene, the 10,000 objects had no `Update()`. Instead one manager object's `Update()` looped over all of them and called a plain C# method on each. Same work, same language, same device (an iPhone 6 on iOS 9.0, Unity 5.2.2f1).

The manager version was much faster. Simonov then profiled the first scene. Out of 9,979 ms of CPU time in his sample, iterating the list of behaviours took 1,517 ms, checking that each object was still alive and active took 2,188 ms, and preparing each native-to-managed invocation took 2,061 ms. Almost all the time went to the machinery around the call, not to `i++`.

Nothing in the scripts was slow. The number of times the engine crossed from C++ into C# was the cost. That is the idea of this section.

### The model

Split a frame's script cost into two parts.

```
T = X × c_cross + N × c_work
X = ceil(N / B)
```

- `N` is the number of entities that need script logic this frame.
- `c_work` is the cost of the useful work for one entity, in microseconds (µs).
- `c_cross` is the fixed cost of one crossing: looking up the function, pushing arguments, validating, switching runtime state, returning.
- `B` is the **batch size**, the number of entities handled per crossing. With per-object callbacks, `B = 1`. With one manager call for everything, `B = N`.
- `X` is the number of crossings per frame.

The ratio `c_cross / c_work` tells you everything. Crossings cost as much as the work itself when `X × c_cross = N × c_work`, which happens at

```
B* = c_cross / c_work
```

Below `B*`, crossings dominate. Well above `B*`, they vanish into the noise and more batching buys nothing.

### Numbers you can check

Take `N = 10,000`, `c_cross = 1.0 µs` and `c_work = 0.1 µs`. These round numbers are illustrative, not Unity's measurements. You will measure your own in the lab. The ratio is 10, so `B* = 10`.

```python
import math

def frame_cost_us(n, batch, c_cross=1.0, c_work=0.1):
    """Cost in microseconds of updating n entities through a script boundary.
    batch = entities handled per crossing; c_cross = cost of one crossing;
    c_work = cost of the useful work for one entity."""
    crossings = math.ceil(n / batch)
    return crossings, crossings * c_cross + n * c_work

for b in (1, 10, 100, 1000, 10000):
    crossings, us = frame_cost_us(10_000, b)
    share = crossings * 1.0 / us
    print(f"batch {b:>5}: {crossings:>6} crossings  {us / 1000:6.3f} ms  crossing share {share:5.1%}")
```

It prints:

```
batch     1:  10000 crossings  11.000 ms  crossing share 90.9%
batch    10:   1000 crossings   2.000 ms  crossing share 50.0%
batch   100:    100 crossings   1.100 ms  crossing share  9.1%
batch  1000:     10 crossings   1.010 ms  crossing share  1.0%
batch 10000:      1 crossings   1.001 ms  crossing share  0.1%
```

| Batch size `B` | Crossings `X` | Frame cost | Share spent crossing |
|---|---|---|---|
| 1 (one callback per object) | 10,000 | 11.0 ms | 90.9% |
| 10 (= `B*`) | 1,000 | 2.0 ms | 50.0% |
| 100 | 100 | 1.1 ms | 9.1% |
| 1,000 | 10 | 1.01 ms | 1.0% |
| 10,000 (one manager call) | 1 | 1.001 ms | 0.1% |

Check the first row by hand: `10,000 × 1.0 + 10,000 × 0.1 = 11,000 µs`. At 60 frames per second you have 16.7 ms per frame. The per-object design spends two thirds of it on script calls that do almost nothing. Batching by 100 gets you a 10× saving. Going from 100 to 10,000 saves only another 0.1 ms.

That is the insight. **The first factor of `B*` in batching is worth nearly everything, and the rest is worth almost nothing.** You do not need one giant manager for the whole game. You need to stop paying a crossing per object.

### A visual you can move

Open `examples/w10-boundary-crossings.html`. The top view shows 10,000 entities as a grid of dots on the script side and the engine on the other side of a vertical line. Each crossing is drawn as an arrow over the line, so at `B = 1` the line is a solid wall of arrows. The bottom view is a stacked bar of frame time, crossing cost in one color and work in another, against the 16.7 ms budget.

Drag the batch-size slider from 1 to 10,000 on a log scale. The arrows thin out and the crossing bar collapses, and past the marker for `B*` the total barely moves. Now drag the `c_cross / c_work` ratio slider. With a cheap boundary (ratio 1), batching hardly matters. With an expensive one (ratio 100, typical of a reflection-based binding), even `B = 10` is a disaster. The marker for `B*` moves with the ratio.

### Cross-game recognition

**Lua's C API (Lua 5.1 through 5.4).** Lua and C exchange every value through a virtual stack. The C side pushes the function and its arguments, calls, then reads and pops the results. The Lua 5.4 manual (section 4.1) describes this stack as the only channel. Every value pushed is a marshalling step, so a call with ten arguments costs roughly ten pushes plus the call. Reading one entity's position per crossing means three pushes and three reads. Handing Lua one array of 1,000 positions per crossing turns that into one push and 1,000 table reads inside the VM. Same `B`, different name.

**World of Warcraft UI (current retail and classic clients).** Addons are written in a subset of Lua 5.1. The client can call an addon's `OnUpdate` handler every time it draws a frame, which on a fast machine is hundreds of times a second. The Warcraft Wiki's page on `OnUpdate` calls it resource intensive and recommends `C_Timer.After` or `C_Timer.NewTicker`, or throttling inside the handler, instead. The other tool is events. An addon registers for, say, a change in the player's health, and the client calls it only when that event fires. That reduces `X` by making most frames cost zero crossings. It is CS102 week 10's poll-versus-push argument, priced in crossings.

**Unity (2015 post).** Simonov's fix was the manager, which sets `B = N` for one class of object. He also noted that the comparison is not entirely fair. Unity's per-call checks protect you from calling a destroyed or inactive object, and a real manager would need some of those checks too. In the crossing model the move is the same as in Lua. One call, many entities.

Three engines, three vocabularies, one equation. When someone asks "is our scripting language fast enough?", the better question is "how many times per frame do we cross, and what does one crossing cost?"

### Eyes-open design judgment

- **Batch where the count is large and the logic is uniform.** Projectiles, particles and crowd agents are thousands of copies of the same rule. Give them one system call per frame. A boss with a unique script is one object, so its crossing cost is irrelevant.
- **Batching fights readability.** "Each object has an `update()`" is how designers think. A manager that loops over arrays is less obvious and harder to hot reload per object. Unity kept `Update()` because it is easy to learn. Pick per-object callbacks for rare, varied logic and batched systems for common, uniform logic.
- **Events beat polling when the event is rare.** A quest waiting for "player enters zone" should not check every frame. But if the event fires every frame anyway, push costs the same crossings as poll plus the dispatch overhead.
- **Measure `c_cross` in your engine, not in someone's blog.** It varies by more than 10× between a hand-written Lua binding, a generated one, and a reflection-based one. The model is only as good as the constant you put in it.
- **The boundary moves.** When a script system becomes hot, you can move it into C++ and expose only its tuning numbers to script. That is a design decision with a cost too, since designers lose the ability to change its logic without a programmer.

### Check yourself (worked example)

1. `N = 4,000`, `c_cross = 2 µs`, `c_work = 0.5 µs`. What is `B*`? What is the frame cost at `B = 1` and at `B = 40`?
2. A binding costs 5 µs per crossing. How many per-object callbacks can you afford in a 2 ms scripting budget if each object's work costs 0.5 µs?

<details>
<summary>Answers</summary>

1. `B* = 2 / 0.5 = 4`. At `B = 1`: `4,000 × 2 + 4,000 × 0.5 = 10,000 µs = 10 ms`. At `B = 40`: `100 × 2 + 2,000 = 2,200 µs = 2.2 ms`.
2. Each callback costs `5 + 0.5 = 5.5 µs`, so `2,000 / 5.5 ≈ 363` objects.

</details>

## 3. What crosses the boundary: values and handles

Crossing count is the performance half of the design. The correctness half is *what* you let cross.

### Never hand a script a raw pointer

A script that stores a goblin's address and uses it after the goblin dies writes into whatever reused that memory. That is the dangling pointer from [week 7 section 4](w07-resource-management-and-hot-reload.md), and scripts make it more likely, because they keep references across frames, inside coroutines and in saved tables. So scripts get the generational handles `(index, generation)` from [week 5](w05-entity-component-system-design.md) and week 7, and nothing else. What is new here is *where* the check goes. Scripts are the least careful callers in the engine, so the binding layer checks every handle on every call before any engine code touches it. The toy below stands in for week 5's handle table with a dictionary keyed by live handles.

```python
live = {(7, 1): {"name": "arrow", "hp": 1}}          # the engine's world after the goblin (7, 0) died

def alive(h):
    return h in live                                   # week 5: generation must match

def bound(fn):
    """Wrap an engine function so every call from script checks its handle first."""
    def call_from_script(h, *args):
        if not alive(h):
            return None                                # the script sees nil, never a stranger
        return fn(live[h], *args)
    return call_from_script

@bound
def apply_damage(target, amount):
    target["hp"] -= amount
    return target["hp"]

print("damage old goblin (7, 0):", apply_damage((7, 0), 5))
print("damage arrow (7, 1):", apply_damage((7, 1), 5))
```

```
damage old goblin (7, 0): None
damage arrow (7, 1): -4
```

The old goblin handle `(7, 0)` fails `alive`, so the call returns `None` (in Lua, `nil`) and the arrow in slot 7 is untouched. Write the check once, in the wrapper, and every bound function gets it. This is also what Unity's per-call validity checks in section 2 were paying for. A safe boundary is not free, and you decide how much safety to buy per crossing.

### Copy small values, share nothing mutable

The second rule is that values crossing the boundary are copies. A position crosses as three numbers. A string crosses as a new string. If a script could hold a live reference to an engine array, it could keep it after the array is resized and read freed memory, the same bug by another route. When you do want bulk data to cross (the batched API from section 2), copy it into a script-owned array once per crossing. The copy costs `N × c_work`-sized time, which the model already counts.

### Keep the list of bindings short

Every bound function is a promise. Scripts, and mods written by strangers, will call it with every possible argument, and you must keep it working after every engine change. A common layout:

- **Queries** read state: `get_position(h)`, `get_health(h)`, `find_in_radius(x, y, r)`.
- **Commands** request changes: `move_to(h, x, y)`, `apply_damage(h, amount)`, `spawn(template, x, y)`. Commands can be queued and applied at a safe point in the frame, the way CS102 week 12's command objects were.
- **Callbacks** the engine calls: `on_spawn`, `on_hit`, `on_timer`. Each one is a crossing, so make them events, not per-frame polls, where you can.

A short list of queries and queued commands is easy to validate, easy to sandbox, and easy to batch.

## 4. Sandboxes and budgets

### Capabilities: what a script is allowed to see

A script can only do what the functions you bind let it do. That makes the binding list a security policy. Removing a function is the strongest guard you have.

- **Factorio (API docs for version 2.1).** Mods run on a modified Lua 5.2.1. The docs state that `loadfile()`, `dofile()`, `coroutine`, `io` and `os` are not accessible, mostly to ensure determinism, and that `pairs()` and `math.random()` were changed to be deterministic. Factorio's multiplayer runs in **lockstep**: every client simulates the same inputs in the same order and must reach the same state (CS202 week 12 builds one next semester). So a mod that read the wall clock or iterated a table in memory-address order would desync the game. The sandbox exists to protect determinism more than to stop cheating.
- **World of Warcraft (since patch 2.0, 2006).** Blizzard's secure execution model marks all third-party addon code and data as **tainted**. Taint spreads to any value that tainted code touches. Protected functions, many of them the ones that act for the player in combat, refuse to run on a tainted execution path. The goal is to make sure a human decides each combat action. The capability here is not a function the addon lacks. It is a function that checks who is asking.
- **Roblox (Luau, current).** Roblox started from Lua 5.1 around 2006 and gradually changed the runtime to give a safe, sandboxed environment for code written by millions of creators. That work became Luau, a separate language derived from Lua 5.1.

Three games face three threats. Factorio guards against desync, WoW against automation, Roblox against hostile code. In each case the defense sits in the binding layer, not in the script.

### Budgets: stopping a script that runs too long

A script with an infinite loop freezes the whole frame, because the engine is waiting for the call to return. Two tools help.

- **An instruction hook.** Lua's `lua_sethook` with `LUA_MASKCOUNT` calls a C function every `count` VM instructions. That function can raise an error to abort a script that has run too long. It is a hard stop, useful against bugs and hostile mods.
- **Coroutines.** For legitimate long jobs (a cutscene, a patrol, a crafting queue), let the script yield back to the engine and resume next frame. This is **time-slicing**, spreading a job across frames so no single frame pays for all of it. CS203 week 14 applies it to AI next semester.

Here is a budgeted script scheduler, using Python generators as coroutines. Each `yield` is one unit of script work.

```python
def patrol(name, steps):
    for i in range(steps):
        yield f"{name} step {i}"          # each yield = one unit of script work

def run_frame(scripts, budget):
    """Resume scripts round-robin until the budget of work units is spent."""
    done, log = 0, []
    while scripts and done < budget:
        s = scripts.pop(0)
        try:
            log.append(next(s))
            scripts.append(s)                # not finished: back of the queue
        except StopIteration:
            continue                         # finished: drop it, costs nothing
        done += 1
    return log

queue = [patrol("guard", 3), patrol("merchant", 5)]
frame = 1
while queue:
    print(frame, run_frame(queue, budget=3))
    frame += 1
```

```
1 ['guard step 0', 'merchant step 0', 'guard step 1']
2 ['merchant step 1', 'guard step 2', 'merchant step 2']
3 ['merchant step 3', 'merchant step 4']
```

Eight units of work, a budget of three per frame, so `ceil(8 / 3) = 3` frames. No frame does more than three units, whatever the scripts ask for. Notice the price. The merchant's last step lands two frames later than it would with no budget. A budget converts frame spikes into latency, the same trade CS203 week 14 makes for AI thinks next semester.

## 5. Errors and reloading

A script error must never take the engine down. Every crossing from engine into script should be a **protected call**, such as Lua's `lua_pcall` or a `try` block around the call in other runtimes. On error, the engine logs the message with the script's file and line, disables that one script or object, and keeps running. A designer who mistypes a variable name should see a red line in the console, not a crashed build.

Reloading a script while the game runs (week 7) raises a question about state. Where does the object's state live? If a script keeps state in its own local variables, reloading the file throws that state away. If state lives in engine components and the script holds only handles, you can swap the code and the goblins keep their health. That is one more reason to keep scripts as thin rules over engine-owned data. It also makes batching easy, since the data is already in arrays.

## In-class activity (25 minutes)

In groups of three, design the scripting boundary for a tower-defense game. It has 2,000 enemies on screen at peak, 60 towers, and one scripted boss per level.

1. For each of enemies, towers and the boss, decide: per-object callback, batched system call, or event-driven. Assume `c_cross = 1.5 µs` and `c_work = 0.3 µs`. Compute the frame cost of your choices.
2. Write the list of bound functions (queries, commands, callbacks), at most 12. Mark which ones take handles.
3. Name one thing a modder must not be able to do, and the binding decision that prevents it.
4. Swap with another group. Find one crossing they could remove, or one stale-handle bug their API allows.

Expected output: a table of the three object kinds with call style and cost, the function list, and the bug your partners found.

## Common misconceptions

- **"Scripts are slow, so move everything to C++."** Often the script body is cheap and the crossing is expensive. Batching crossings can recover most of the time without rewriting any logic, and moving code to C++ costs designers their iteration speed.
- **"One manager for everything is always best."** Past `B*` the gains flatten. `B = 100` versus `B = 10,000` in section 2 differs by 0.1 ms. Pick the batch that keeps code readable once crossings are below about 10% of the total.
- **"Events are always cheaper than polling."** Only when the event is rarer than the poll. An event that fires every frame costs the same crossings as polling, plus the cost of dispatching it. Count crossings for the case you expect, not the case that sounds tidy.
- **"The sandbox is there to stop hackers."** Sometimes. Factorio's exists mainly for determinism, and WoW's for keeping a human in the loop. Name the threat before you pick which functions to remove.

## Check yourself

1. An MMO client calls a Lua `OnUpdate` on 300 nameplates every frame at 144 fps. One crossing costs 2 µs and each nameplate's work costs 1 µs. How many milliseconds per second does this spend, and how much does it save to update nameplates at 20 Hz in one batched call per update?
2. Slot 7 of a handle table has generation 3. A script holds `(7, 2)`. What does `get((7, 2))` return, and what sequence of events produced this situation?
3. Your engine's binding does a full validity check (alive, active, initialized) costing 0.8 µs on every crossing. Where in the crossing model does this cost go, and how does batching change how often you pay it?
4. A mod calls `os.time()` to seed its random numbers. In which of this lecture's three example games would that break something, and what?

<details>
<summary>Answers</summary>

1. Per frame: `300 × (2 + 1) = 900 µs`. Per second: `900 × 144 = 129,600 µs ≈ 129.6 ms`. At 20 Hz, one batched call: `(2 + 300 × 1) × 20 = 6,040 µs ≈ 6.0 ms` per second, a saving of about 123.6 ms per second, and the nameplates still refresh faster than a player reads them.
2. It returns `None` (nil). The object created with generation 2 in slot 7 was destroyed (generation became 3), and possibly a new object now lives there with generation 3. The script's handle is stale.
3. It is part of `c_cross`. With batching, you validate once per crossing, or once per entity in a tight engine-side loop that is much cheaper than a full crossing. Either way you stop paying it through the expensive path `N` times.
4. Factorio. `os` is not available, and if it were, each client in lockstep would read a different clock, seed differently and desync.

</details>

## Lab / assignment hook

[Lab 10, a script host](../labs/lab10.md). You build the engine side of a scripting layer in Python: a binding wrapper that checks every handle, a marshalling check that refuses raw objects, a batched query API that counts crossings, and a budgeted coroutine scheduler. Then you measure `c_cross` and `c_work` on your own machine and predict where batching stops paying.

## Sources

- Simonov, V. "10000 Update() calls." Unity blog, 23 December 2015. Unity 5.2.2f1, iOS 9.0, iPhone 6. Test design, the manager alternative, and the Instruments breakdown (1,517 ms iteration, 2,188 ms validity checks, 2,061 ms invocation setup out of 9,979 ms). https://unity.com/blog/engine-platform/10000-update-calls
- Lua 5.4 Reference Manual, section 4.1 "The Stack" (values pass between Lua and C through a virtual stack) and `lua_sethook` (`LUA_MASKCOUNT` calls the hook after every `count` instructions). https://www.lua.org/manual/5.4/manual.html
- Warcraft Wiki, "Lua" (WoW implements a subset of Lua 5.1; upgraded to 5.1.1 in patch 2.0.1). "UIHANDLER OnUpdate" (fires every drawn frame; recommends `C_Timer` or throttling). "Secure Execution and Tainting" (taint model, largely introduced in patch 2.0). Retrieved September 2026. https://warcraft.wiki.gg
- Factorio Lua API, Auxiliary docs, "Libraries and functions," version 2.1.20. Modified Lua 5.2.1; `loadfile`, `dofile`, `coroutine`, `io`, `os` inaccessible; deterministic `pairs` and `math.random`. https://lua-api.factorio.com/latest/auxiliary/libraries.html
- Luau, "Why Luau?" Roblox adopted Lua 5.1 around 2006 and evolved it into a sandboxed runtime, now Luau. https://luau.org/why
- Gregory, J. (2018). *Game Engine Architecture*, 3rd ed. CRC Press. Chapter 16.
- Ierusalimschy, R. (2016). *Programming in Lua*, 4th ed. Lua.org.

## Interactive spec: examples/w10-boundary-crossings.html

**The one insight:** batching up to about `B* = c_cross / c_work` removes almost all crossing cost, and batching further buys almost nothing.

**Layout.** Two linked views, stacked on mobile, side by side at 1,280 px.

- **Top view, "the boundary".** A vertical line splits the canvas: "script" on the left, "engine" on the right. The left side shows `N` entities as a grid of small dots (cap the drawn dots at 2,500; above that, each dot stands for `N / 2,500` entities and a caption says so). Draw `min(X, 200)` arrows crossing the line, evenly spaced vertically, each arrow grouping `B` dots with a faint bracket when `B ≤ 50`. A caption reads "X crossings this frame".
- **Bottom view, "the frame".** One horizontal stacked bar: crossing cost `X × c_cross` in the accent color, work `N × c_work` in a neutral color. A dashed vertical marker at 16.67 ms labeled "60 fps budget". Below it, a line chart of total `T` (ms) against `B` on a log x-axis from 1 to `N`, with the current `B` as a dot and a vertical marker at `B*` labeled "B* = c_cross / c_work".

**Controls.**
- Batch size `B`: log slider from 1 to `N`, snapping to 1, 2, 5, 10, 20, 50, 100, 200, 500, 1,000, 2,000, 5,000, 10,000 (only values ≤ N). An "Exact B" number field (1 to `N`) next to it sets any integer batch size, for values off the snap list such as the `B = 40` test below.
- Entities `N`: slider 100 to 20,000, default 10,000.
- `c_cross` in µs: slider 0.1 to 10, default 1.0.
- `c_work` in µs: slider 0.01 to 2, default 0.1.
- Preset buttons: "per-object callbacks" (`B = 1`), "manager" (`B = N`), "at B*" (`B` = nearest snap value to `c_cross / c_work`).

**Readouts (exact numbers next to the visual).** `X = ceil(N / B)`, crossing cost (ms), work cost (ms), total `T` (ms, 3 decimals), crossing share (%, 1 decimal), `B*` (1 decimal), share of a 16.67 ms frame.

**Formulas.** `X = ceil(N / B)`; `T = X × c_cross + N × c_work` (µs, display in ms); share = `X × c_cross / T`; `B* = c_cross / c_work`.

**Test values (defaults `N = 10,000`, `c_cross = 1.0`, `c_work = 0.1`).**
- `B = 1`: `X = 10,000`, `T = 11.000 ms`, share 90.9%.
- `B = 10`: `X = 1,000`, `T = 2.000 ms`, share 50.0%.
- `B = 100`: `X = 100`, `T = 1.100 ms`, share 9.1%.
- `B = 10,000`: `X = 1`, `T = 1.001 ms`, share 0.1%.
- `N = 4,000`, `c_cross = 2`, `c_work = 0.5`, `B = 40` (typed into Exact B): `X = 100`, `T = 2.200 ms`, `B* = 4.0`.

**First screen.** Defaults with `B = 1`, so the wall of arrows and the 11 ms bar (two thirds of the budget) are visible before any interaction. Keyboard: all sliders reachable by Tab, arrow keys step through snap values. Respect `prefers-reduced-motion` (no arrow animation; static arrows only).
