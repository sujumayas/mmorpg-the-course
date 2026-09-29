# CS201 · Subsystem labs brief

**Weight:** 50% of the course grade.
**What counts:** all 14 labs, weighted as in the rubric table at the end of this brief. No lab is dropped, because every lab builds a piece of your final engine.
**When:** each lab is assigned in its week's lab session and is due at the start of the next week's lab session. Lab 14 is due at the start of week 15, before the engine demos.
**Work mode:** labs 01 to 09 in pairs, labs 10 to 12 individually, labs 13 and 14 in pairs for Parts A and B, with Part C done in your own final-project engine. Each lab file states its mode.

## What this component is for

The lectures give you a model for each subsystem: port share, relocation cost, fragmentation, the frame budget, the join-versus-toggle trade, cache lines, seeks versus bytes, state switches, missed taps, boundary crossings, sleeping islands, migration chains, profiler error and code sites. The labs make you build the subsystem, check it against the model's numbers, and then measure it on your own machine. A lab that "works" but has no measurement earns about half its marks.

Each course outcome is assessed here and again in the [final engine](final-engine-brief.md).

| Outcome | Labs that assess it most directly |
|---|---|
| Explain the major subsystems of a game engine and their dependencies | [01](../labs/lab01.md) (layers and start-up order), [07](../labs/lab07.md) (resource dependencies), [09](../labs/lab09.md) (input routing), [10](../labs/lab10.md) (the script boundary), [11](../labs/lab11.md) (who owns the transform) |
| Implement an entity-component-system with cache-friendly storage | [02](../labs/lab02.md), [03](../labs/lab03.md), [05](../labs/lab05.md), [06](../labs/lab06.md) |
| Profile and optimize frame time | [04](../labs/lab04.md), [08](../labs/lab08.md), [13](../labs/lab13.md), and the measurement parts of every lab |

## The labs

| Lab | Week | Title | Work mode | Automatic check | Becomes this part of your engine |
|---|---|---|---|---|---|
| [01](../labs/lab01.md) | 1 | A layer checker | pairs | `python check_lab01.py` (7 checks) | the layer checker you run on the final engine |
| [02](../labs/lab02.md) | 2 | An owning buffer and a move-only handle | pairs | `python run_tests.py` (11 tests) | the core layer's owning types |
| [03](../labs/lab03.md) | 3 | Three allocators | pairs | `python run_tests.py` (12 tests) | stack, double-ended stack, pool and frame memory |
| [04](../labs/lab04.md) | 4 | Frame pacer | pairs | `./test_frame` (11 checks) | the budget and pacing readout |
| [05](../labs/lab05.md) | 5 | A sparse-set ECS | pairs | `./test_ecs` (9 checks) | the entity layer |
| [06](../labs/lab06.md) | 6 | AoS to SoA | pairs | `./test_layout` (6 checks) | component storage layout |
| [07](../labs/lab07.md) | 7 | A resource manager with handles and hot reload | pairs | `python check_lab07.py` (10 checks) | the resource manager |
| [08](../labs/lab08.md) | 8 | A sorted render queue | pairs | `./test_render_queue` (15 checks) | the render queue and switch counter |
| [09](../labs/lab09.md) | 9 | An event-built input layer | pairs | `python check_lab09.py` (10 checks) | the input stage (ported to C++) |
| [10](../labs/lab10.md) | 10 | A script host | individual | `python test_script_host.py` (7 checks) | the binding rules for the scripting layer |
| [11](../labs/lab11.md) | 11 | Islands, sleep and a safe event queue | individual | `python test_physics_sleep.py` (7 checks) | physics integration rules |
| [12](../labs/lab12.md) | 12 | A save system that survives patches | individual | `python test_save_system.py` (7 checks) | the save pipeline |
| [13](../labs/lab13.md) | 13 | A frame profiler | pairs, Part C in your engine | `python test_frameprof.py` (7 checks) | the profiler and budget report |
| [14](../labs/lab14.md) | 14 | A reflected inspector | pairs, Part C in your engine | `python test_reflect.py` (8 checks) | descriptor tables, debug panel, undo |

Pairs submit one zip and receive the same mark, subject to the spot checks below. Keep the same partner from lab 01 to lab 09 if you can. Your final-engine partner is usually your lab partner, which makes labs 13 and 14's Part C one piece of shared work.

## How each lab is marked

Every lab ends with its own rubric out of 100. Two formats are in use.

- **Labs 01 to 09** give each criterion a number of points. The marker awards full marks (Excellent), half marks (Adequate) or zero (Missing or wrong) for that row, exactly as the lab's table describes.
- **Labs 10 to 14** give each criterion a percentage weight and score it in bands. A criterion earns `weight × band ÷ 4`, so a criterion weighted 30% and marked Good (3) earns 22.5 points.

| Band in labs 10 to 14 | Label | Share of the criterion's weight | What the marker sees |
|---|---|---|---|
| 4 | Excellent | 100% | Everything the Excellent cell asks for, with numbers that match the lecture model or the checker |
| 3 | Good | 75% | Correct, one explanation or piece of evidence thin |
| 2 | Partial | 50% | The core works, but a named part fails or the numbers are missing |
| 1 | Missing, attempted | 25% | Attempted, but broken or reasoned from the wrong model |
| 0 | Missing | 0% | Not submitted, or unrelated to the lab |

### Automatic checks

Every lab has a checker (the table above). Markers run it on a clean copy of your submitted folder, with `.venv/bin/python` for Python and the build command in the lab file for C++. If the checker fails there, the code criterion (the first row of the lab's rubric) cannot score above half marks in labs 01 to 09 or above band 2 in labs 10 to 14. Code that only works on your machine because of an absolute path, a missing file or a compiler extension counts as failing. Sanitizer builds (`--asan`, UBSan) are run where the lab provides them, and a sanitizer report counts as a failed check.

### Measurements and predictions

Most labs ask for a number measured on your machine next to the number a lecture model predicts: Lab 02's relocation counts, Lab 03's benchmark medians, Lab 04's replayed log, Lab 05's break-even, Lab 06's layout timings, Lab 07's load-time memo, Lab 08's switch counts, Lab 09's sampled presses, Lab 10's fitted `c_cross` and `c_work`, Lab 11's awake body-seconds, Lab 12's migration timing, Lab 13's scope cost `o`. Always record the machine, OS, compiler, flags and the number of runs. A measurement without them earns at most half of its row.

Some steps ask you to predict before you run: Lab 02 step 6 (the bytes copied without `noexcept`), Lab 04 step 3 (a hand trace before any code), and the "predict with the interactive before you measure" notes in labs 10, 11 and 13. A prediction written after the run, or changed to match it, earns the lowest band for that criterion. A wrong prediction with honest working loses nothing, as long as you then explain the difference.

### Bonus parts

Lab 01 Part E, Lab 07 Part E, Lab 08 Part D and Lab 09 Part D are optional and worth up to 5 bonus points each. A lab's mark, bonus included, is capped at 100.

## Spot checks

From week 2 on, a marker picks a few students at the start of each lab session and asks two short questions about their previous lab, in the style of the [exam bank](exam-bank.md) and rewritten with the student's own code and numbers. Examples: "Your `bench_storage` run gave 45 ns and 7 ns per toggle. What break-even does that give for two join systems?" or "Point to the line in your `remove` that fixes `sparse` for the moved element, and say what breaks if you delete it." In a pair, each partner answers alone.

| Band | Share of the lab mark kept | What the student shows |
|---|---|---|
| Full | 100% | Explains each function they wrote, traces one input through it, and says why the lab's key number came out as it did |
| Partial | 70% | Explains the main function and the key number, but cannot trace a second function or handle a "what if this number doubled" change |
| Weak | 40% | Recognizes the code and can run it, but cannot say what it does or where a number came from |
| None | 0% | Cannot explain the submitted work |

A spot check never lowers a mark for a slip. It exists to confirm the work is yours.

## Late work

Each student has one 48-hour extension to use on any one lab, no questions asked; tell the instructor before the deadline. Otherwise a lab submitted up to 48 hours late is marked out of 80, and after 48 hours it is marked for feedback only and scores 0. Because no lab is dropped, talk to the instructor early if you fall behind; a missing lab also leaves a hole in your engine. Extensions for illness or other documented reasons follow the university policy and do not use up your free extension.

## Academic integrity

You may use any code from the lectures and the starter files. You may use documentation, forums and AI assistants to understand an error or an API, and you must say so in one line in the lab README ("used cppreference for `std::move_if_noexcept`; asked an assistant why ASan hung on macOS"). You may not submit code you cannot explain, and you may not copy another pair's measurements. Every timing and count must come from your own runs, with the machine and flags recorded.

## Rubric: how the 100 points are made up

Your labs component is the weighted sum of your lab marks, then multiplied by 0.50 for the course grade. Labs 13 and 14 carry a little more weight because their Part C is done in your engine at home.

| Lab | What its mark rewards most | Weight (points of 100) |
|---|---|---|
| 01 | Include parsing, violations, start-up order, the Kiln refactor | 7 |
| 02 | Rule-of-five owners, `noexcept` moves, the relocation measurement | 7 |
| 03 | Aligned stack, double-ended stack, embedded free list, the benchmark | 7 |
| 04 | Budget and queue rules, the replayed log, pacing choices | 7 |
| 05 | Generational handles, swap-and-pop pools, your break-even | 7 |
| 06 | Layout conversions, the byte model against measurement, the design table | 7 |
| 07 | Load-time model, handles and counts, hot reload, dependency order | 7 |
| 08 | Sort key, switch counts against the model, the slab trade-off | 7 |
| 09 | Event-built frames, action maps, press ownership, the sampling comparison | 7 |
| 10 | Checked bindings, marshalling, batching, the fitted crossing cost | 7 |
| 11 | Islands, sleep, buffered events, the pile measurements | 7 |
| 12 | Migration chain, header checks, two-pass references, three shipped patches | 7 |
| 13 | Analysis functions, the Perfetto trace, `o` in your engine, the budget report | 8 |
| 14 | Generic tools, project counts, descriptor tables and undo in your engine | 8 |
| **Total** | | **100** |

A lab worth 7 points is 3.5% of the course grade; labs 13 and 14 are 4% each.
