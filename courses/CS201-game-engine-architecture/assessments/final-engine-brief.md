# CS201 · Final engine brief: a mini engine and a demo game

**Weight:** 50% of the course grade.
**Assigned:** week 1 (the plan is the table in [week 1, section 5](../lectures/w01-engine-anatomy-and-runtime-layers.md)). **Milestone 1:** end of week 6. **Milestone 2:** end of week 11. **Final submission:** start of week 15, followed by a 25-minute demo and viva in week 15.
**Work mode:** a pair (usually your lab partner) or individual. A pair submits one engine and a `CONTRIBUTIONS.md`, and each partner answers the viva questions alone.
**Lectures:** all fourteen. Most directly [week 1, runtime layers](../lectures/w01-engine-anatomy-and-runtime-layers.md), [week 3, allocators](../lectures/w03-memory-allocators-stack-pool-and-frame.md), [week 4, the frame](../lectures/w04-the-frame-update-render-present.md), [week 5, ECS design](../lectures/w05-entity-component-system-design.md), [week 6, cache locality](../lectures/w06-cache-locality-and-data-oriented-design.md) and [week 13, profiling](../lectures/w13-profiling-cpu-gpu-frame-budgets.md).

## What this component is for

Each lab builds one subsystem alone, often in Python. This assessment asks you to put them together in one C++ program that runs a small game, and then to prove how it behaves with measurements. An engine that "runs smoothly on my laptop" earns little here. An engine whose documents state its layer violations (zero), its steady-state heap allocations per frame (zero), its median and p99 frame time per subsystem, and one optimization with a measured before and after, earns a lot.

It assesses all three course outcomes.

- **Explain the major subsystems of a game engine and their dependencies.** `ARCHITECTURE.md`, the layer checker's output, the start-up order and the viva.
- **Implement an entity-component-system with cache-friendly storage.** The ECS, its storage choices and the layout benchmark.
- **Profile and optimize frame time.** The profiler, `BUDGET.md` and the optimization you measure.

## What you build

### The engine

A small engine in C++17 or C++20, organized in the layers from week 1: platform, core, resources, engine systems, gameplay foundations, and game code on top. One executable runs as game or editor from a command-line flag, with editor-only code behind a compile-time switch (week 14).

### The demo game

A small game that exercises the engine. Keep the rules simple. A top-down arena, a tower defense or a survival wave game all work. Shapes and flat colors are enough, no art is marked, and you must not use copyrighted characters, sprites, sounds or logos. The game must include:

- at least 10,000 entities that a system updates every frame through your ECS (projectiles, a crowd, particles simulated as entities);
- at least one enemy or object type whose behavior is a script;
- at least 200 dynamic physics bodies that can be knocked over and fall asleep (a pile, a wall, a stack of crates);
- a save and load of the game state, from an in-game key;
- an in-game debug panel that edits at least one component's fields while the game runs;
- a scripted camera path of at least 30 seconds through the busiest part of the game, used for every measurement.

### Technical rules

- **Language.** The engine is C++. Scripts are Lua 5.4 embedded through its C API (week 10). Another scripting language needs the instructor's written approval.
- **Libraries you may use.** The C++ standard library; SDL3 or a similar library for the window, clock, input events and a graphics context; a graphics API (OpenGL, Vulkan, Metal or Direct3D) or SDL3's 2D renderer; Lua 5.4; Box2D v3.1 for rigid bodies (or your own simple physics); Dear ImGui for debug panels. Any other library needs written approval.
- **What you write yourself.** Everything the labs built: allocators, the ECS and its storage, the resource manager with handles and hot reload, the render queue and sort key, the input layer, the script bindings, the physics integration (ownership order, sleep bookkeeping if you write your own physics, buffered events), the save pipeline, the profiler and the reflection layer. No complete engine, no ECS library, no serialization or reflection library.
- **Rendering is a hook, not an art test.** Colored quads are fine. What is assessed is how commands reach the GPU: the queue, the key, the switch count and the measured GPU or frame time.
- **Build.** One command builds the game from a clean copy on the lab machines (a CMake project or a short build script), with `-Wall` and no warnings in your own code. A second command builds a debug version with AddressSanitizer and UndefinedBehaviorSanitizer. If AddressSanitizer does not run on your machine (it hangs at start-up on some recent macOS versions, as Lab 02 notes), build with UndefinedBehaviorSanitizer alone and say so in the README.

## Required subsystems

Each item names the lab that gives you a starting point. The labs are the parts; the new work is joining them.

1. **Layers and start-up (Lab 01).** One folder per layer. Your Lab 01 checker, pointed at the engine with a `layers.json` you write, reports zero upward dependencies and zero OS leaks, or lists each exception with a one-line justification. Subsystems start and stop through explicit functions in one written order, printed at start-up.
2. **Ownership (Lab 02).** Every resource with a create and a destroy call has a single RAII owner. Every type stored in a growing container has a `static_assert(std::is_nothrow_move_constructible_v<T>)`. The sanitizer build runs the demo for 60 seconds with no reports.
3. **Memory (Lab 03).** A frame allocator reset at the end of every frame, a level stack freed with a marker when the level unloads, and at least one per-type pool. A global `operator new` counter (Lab 03's G1 idea) shows zero heap allocations per frame in the steady state of the demo scene, or lists every remaining one with its reason.
4. **The frame (Lab 04).** A fixed-timestep update, a stated queue depth and swap interval with the reason, and an overlay showing CPU time, GPU or present-to-present time, and the displayed frame time from your `shown_ms`.
5. **ECS and data layout (Labs 05 and 06).** Generational entity handles; a stated storage choice (sparse set, archetype or enable flag) for every component with the reason; struct-of-arrays or hot/cold storage for the components the 10,000-entity system reads; structural changes deferred to one point in the frame.
6. **Resources (Lab 07).** A reference-counted cache behind generational handles, hot reload of at least one asset type (a texture or a data file) swapped at a frame boundary with the last good version kept on a bad file, and dependency-ordered rebuilds.
7. **Rendering hook (Lab 08).** A render queue sorted by 64-bit keys with opaque, translucent and UI passes, and a switch counter in the overlay.
8. **Input (Lab 09).** A queue of timestamped events drained each frame into a frame summary with press and release counts, an action map loaded from a data file, and a context stack with press ownership and release-on-focus-loss.
9. **Scripting (Lab 10).** Every binding checks its handle and returns nil for a stale one. Every call from the engine into Lua is a protected call. At least one high-count behavior uses a batched call instead of a per-entity callback, and a budget limits script work per frame.
10. **Physics (Lab 11).** Body types chosen by ownership, the frame order from week 11 section 3, sleeping islands, and contact events buffered and handled after the step.
11. **Saves (Lab 12).** A header with magic number, version, length and CRC-32; persistent IDs and a two-pass loader; an atomic write with a backup; and at least one migration, with a golden save from the older version that still loads.
12. **Profiler (Lab 13).** Scoped timers into a per-thread buffer, a Chrome JSON trace export on a key press, and your measured scope cost `o` for a debug and an optimized build.
13. **Tools (Lab 14).** Descriptor tables for at least three components; save, load and the debug panel written once as loops over the tables; every panel edit routed through an undo history with transactions.

## The documents

### `ARCHITECTURE.md` (1,200 to 2,000 words)

1. **Layers.** A diagram of your folders by layer, the checker output, and every exception with its reason.
2. **Start-up.** The subsystem dependency list and the start and stop order that follows from it.
3. **Memory plan.** A table of every allocation class in the engine (permanent, level, frame, object, unpredictable), its allocator, and the measured peak use in the demo scene.
4. **Storage choices.** A table of every component with its size, its storage (archetype column, sparse set or enable flag), its estimated changes per second and the systems that join it.
5. **Boundaries.** How input reaches gameplay without an upward dependency, what crosses the script boundary, and who owns each transform property at each point of the frame.

### `BUDGET.md` (the profiling report)

1. **Conditions.** Build type, machine, OS, compiler and flags, the scene, the camera path and the display refresh rate.
2. **Budget.** A target frame rate and a budget per subsystem that keeps at least 10% of the frame in reserve.
3. **Measurements.** Median and p99 per subsystem, per thread and for the whole frame, over at least 600 frames of the camera path, plus GPU time from timestamp queries if your renderer has them (if not, say so and use present-to-present time). What the player sees at your refresh rate, from week 4's model.
4. **The bottleneck** by week 4's `max`, and the evidence.
5. **One optimization.** A hypothesis tied to a lecture model (for example "the crowd system reads 128-byte structs for 24 hot bytes", week 6), the change, and the median and p99 before and after under the same conditions. Keep it only if it beats the frame-to-frame noise, and say what the new bottleneck is.
6. **The layout benchmark.** Your 10,000-entity system in AoS and in your chosen layout at 10,000, 100,000 and 1,000,000 entities, next to the byte model's prediction for your cache line size.
7. **Overhead check.** The measured `n × o` of your scopes against the uninstrumented frame time.

### `README.md` and `CONTRIBUTIONS.md`

`README.md` gives the commands to build, run the game, run the editor mode, run the camera path, export a trace and run the layer checker, all from a clean copy. Pairs add `CONTRIBUTIONS.md`: one paragraph each, naming the subsystems and files each partner wrote.

## Milestone 1: engine skeleton (end of week 6, 10 points)

A 5-minute demo in the lab session. The platform layer opens a window and reads the clock, files and input events. Subsystems start and stop in a printed order. The frame allocator, a level stack and one pool are in use. An ECS moves 100,000 entities every frame with struct-of-arrays storage for the hot components, and the frame time shows in a text overlay. Bring a one-page note with the layer checker's output, the storage choice for the first five components, and the demo game in three sentences.

## Milestone 2: systems joined (end of week 11, 10 points)

A 5-minute demo in the lab session. The demo game is playable in rough form. A texture or data file hot reloads while the game runs. Draws go through the sorted render queue. Input goes through the event layer and a context stack. One entity type is scripted in Lua through checked bindings. A pile of physics bodies falls asleep. Bring a one-page note with a first median and p99 frame time from coarse scopes, and the subsystem you expect to be the bottleneck.

## Demo and viva (week 15, 25 minutes)

You build and run your submission from a clean copy on a lab machine while two examiners watch. Every team follows the same steps.

1. **Build and start (3 min).** The two build commands from the README. The start-up order prints.
2. **Play (4 min).** Play the demo game briefly, then run the camera path with the overlay on. The examiner compares the overlay with `BUDGET.md`.
3. **Live changes (6 min).** The examiner asks for three of these: edit a texture or data file and watch it reload, including a broken edit; change a script and reload it; knock over the pile and watch it sleep, then bump it; hold a movement key, open the debug console, release the key and close the console; drag a field in the debug panel and undo the whole drag in one step; load the golden save from the older version.
4. **Trace (4 min).** Export a trace, open it in Perfetto, and walk the examiner through one frame: the bottleneck, the largest self time, and where your optimization shows.
5. **Questions (8 min).** Three questions in the style of the [exam bank](exam-bank.md), rewritten with your own code and numbers. At least one is a compute question on your own measurements, and one is a trace through code you wrote.

## Rubric

### Milestones (20 points)

| Criterion | Excellent | Good | Weak | Missing | Points |
|---|---|---|---|---|---|
| M1: skeleton | 7: every listed part runs; 100,000 entities moved in SoA; start and stop order printed | 5 to 6: one part missing or stubbed | 2 to 4: window and loop only | 0 to 1 | 7 |
| M1: note | 3: checker output clean or explained; storage choices justified | 2: one element missing | 1: note without numbers | 0 | 3 |
| M2: systems joined | 7: hot reload, sorted queue, event input, a checked Lua binding and a sleeping pile all shown | 5 to 6: one missing | 2 to 4: two or more missing | 0 to 1 | 7 |
| M2: first measurement | 3: median and p99 from scopes, a named suspect | 2: one number, or no suspect | 1: an fps counter only | 0 | 3 |

### Final submission, demo and viva (80 points)

| Criterion | Excellent | Good | Adequate | Weak or missing | Points |
|---|---|---|---|---|---|
| Architecture and layering | 7 to 8: checker reports zero violations or only justified ones; explicit start and stop order; `ARCHITECTURE.md` complete and consistent with the code | 5 to 6: one unexplained violation or a thin section | 3 to 4: layers by folder only, checker not run | 0 to 2: no layer structure | 8 |
| Memory and ownership | 9 to 10: RAII owners everywhere; `noexcept` asserts; frame, level and pool allocators in use; zero steady-state heap allocations shown by a counter; sanitizer build clean for 60 s | 7 to 8: one of these missing | 4 to 6: allocators present but unused in the frame, or sanitizer reports | 0 to 3: raw `new`/`delete` throughout | 10 |
| ECS and data layout | 13 to 14: generational handles; storage choice per component with reasons; SoA or hot/cold for the hot system; deferred structural changes; layout benchmark at three sizes next to the model | 10 to 12: benchmark or storage table thin | 5 to 9: ECS works but stores components as objects, or no benchmark | 0 to 4: no ECS | 14 |
| Frame, input and rendering hook | 9 to 10: fixed step; stated `Q` and `S` with reason; event-built input with press ownership and focus-loss release; sorted queue with switch counter | 7 to 8: one element missing | 4 to 6: polled input or unsorted draws | 0 to 3: missing | 10 |
| Resources, scripting, physics and saves | 11 to 12: hot reload with last-good fallback; checked, protected, batched Lua bindings; sleeping islands and buffered events; versioned, checksummed saves with a working golden file | 8 to 10: one subsystem simplified | 4 to 7: two simplified, or one missing | 0 to 3: most missing | 12 |
| Profiling and budget report | 13 to 14: fixed conditions; budget with reserve; median and p99 per subsystem and thread; bottleneck with evidence; one optimization measured before and after beyond noise; overhead check | 10 to 12: one section thin, or the optimization not measured under the same conditions | 5 to 9: averages only, or no optimization | 0 to 4: fps counter only | 14 |
| Tools | 6: descriptor tables for three or more components; save, load and panel as loops; one drag is one undo step | 4 to 5: panel or undo hand-written per field | 2 to 3: a debug panel without reflection | 0 to 1: missing | 6 |
| Demo and viva | 6: all five steps work from a clean copy; answers use your own code and numbers | 4 to 5: one step needs help | 2 to 3: two steps fail, or answers vague | 0 to 1: cannot run or explain | 6 |
| **Total** | | | | | **80** |

The final engine mark is the milestones plus the final, out of 100, multiplied by 0.50 for the course grade.

## Rules and advice

- **Your labs are the parts.** Most of the engine is Lab 01's checker, Lab 02's owners, Lab 03's allocators, Lab 05's ECS in Lab 06's layout, Lab 07's resource manager, Lab 08's queue, Lab 09's input layer, Lab 13's profiler and Lab 14's descriptor tables, ported to C++ where the lab used Python.
- **Measure from week 4.** Put the frame-time overlay in early and add coarse scopes as each subsystem arrives. A budget written the night before submission has nothing to compare with.
- **Predict, then measure.** `BUDGET.md` rewards a prediction written before the run and an honest account of the gap.
- **Keep the game small.** Extra features earn nothing, and each one is another thing that can break in the demo.
- **Late submission.** Up to 48 hours late, the final is marked out of 64 instead of 80, and the demo is rescheduled if the timetable allows. Milestones cannot be late, but a missed milestone can be shown at the next lab session for half marks.
- **Integrity.** The rules in the [labs brief](subsystem-labs-brief.md#academic-integrity) apply. Every measurement must come from your own runs, with conditions recorded. In the viva you must be able to explain every file you submit.
