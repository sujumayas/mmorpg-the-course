# CS201 — Game Engine Architecture

Year 2, semester 3 · 4 credits · Prerequisites: CS102

Build a small engine in C++: the loop, memory, entities, rendering hooks, resources and tooling.

## Learning outcomes

- Explain the major subsystems of a game engine and their dependencies
- Implement an entity-component-system with cache-friendly storage
- Profile and optimize frame time

## Schedule

| Week | Topic | Lecture | Example |
|---|---|---|---|
| 1 | Engine anatomy and runtime layers | [lecture](lectures/w01-engine-anatomy-and-runtime-layers.md) | [port-size](examples/w01-port-size.html) |
| 2 | C++ for engines: memory, RAII, move semantics | [lecture](lectures/w02-cpp-for-engines-memory-raii-and-move-semantics.md) | [vector-growth](examples/w02-vector-growth.html) |
| 3 | Memory allocators: stack, pool, frame | [lecture](lectures/w03-memory-allocators-stack-pool-and-frame.md) | [fragmentation](examples/w03-fragmentation.html) |
| 4 | The frame: update, render, present | [lecture](lectures/w04-the-frame-update-render-present.md) | [frame-budget](examples/w04-frame-budget.html) |
| 5 | Entity-component-system design | [lecture](lectures/w05-entity-component-system-design.md) | [sparse-set-vs-archetype](examples/w05-sparse-set-vs-archetype.html) |
| 6 | Cache locality and data-oriented design | [lecture](lectures/w06-cache-locality-and-data-oriented-design.md) | [aos-vs-soa-cache-lines](examples/w06-aos-vs-soa-cache-lines.html) |
| 7 | Resource management and hot reload | [lecture](lectures/w07-resource-management-and-hot-reload.md) | [seeks-vs-bytes](examples/w07-seeks-vs-bytes.html) |
| 8 | Rendering pipeline overview | [lecture](lectures/w08-rendering-pipeline-overview.md) | [draw-order](examples/w08-draw-order.html) |
| 9 | Input and event systems | [lecture](lectures/w09-input-and-event-systems.md) | [missed-taps](examples/w09-missed-taps.html) |
| 10 | Scripting layer integration | [lecture](lectures/w10-scripting-layer-integration.md) | [boundary-crossings](examples/w10-boundary-crossings.html) |
| 11 | Physics integration basics | [lecture](lectures/w11-physics-integration-basics.md) | [sleeping-islands](examples/w11-sleeping-islands.html) |
| 12 | Serialization and save files | [lecture](lectures/w12-serialization-and-save-files.md) | [save-migration-chain](examples/w12-save-migration-chain.html) |
| 13 | Profiling: CPU, GPU, frame budgets | [lecture](lectures/w13-profiling-cpu-gpu-frame-budgets.md) | [two-profilers](examples/w13-two-profilers.html) |
| 14 | Tools and editors | [lecture](lectures/w14-tools-and-editors.md) | [fields-times-systems](examples/w14-fields-times-systems.html) |
| 15 | Final: mini engine + demo game | [assessments](#assessment-materials) | — |

## Signature worked examples

- Array-of-structs vs struct-of-arrays: iterate 1M entities, visualize cache lines
- 16.6 ms budget pie chart: where a frame's time goes

## Labs

- [CS201 · Lab 01: A layer checker](labs/lab01.md)
- [CS201 · Lab 02: An owning buffer and a move-only handle](labs/lab02.md)
- [CS201 · Lab 03: Three allocators](labs/lab03.md)
- [CS201 · Lab 04: Frame pacer](labs/lab04.md)
- [CS201 · Lab 05: A sparse-set ECS](labs/lab05.md)
- [CS201 · Lab 06: AoS to SoA](labs/lab06.md)
- [CS201 · Lab 07: A resource manager with handles and hot reload](labs/lab07.md)
- [CS201 · Lab 08: A sorted render queue](labs/lab08.md)
- [CS201 · Lab 09: An event-built input layer](labs/lab09.md)
- [CS201 · Lab 10: A script host](labs/lab10.md)
- [CS201 · Lab 11: Islands, sleep and a safe event queue](labs/lab11.md)
- [CS201 · Lab 12: A save system that survives patches](labs/lab12.md)
- [CS201 · Lab 13: A frame profiler](labs/lab13.md)
- [CS201 · Lab 14: A reflected inspector](labs/lab14.md)

## Assessment materials

- [CS201 · Exam bank: quiz, practice and viva questions](assessments/exam-bank.md)
- [CS201 · Final engine brief: a mini engine and a demo game](assessments/final-engine-brief.md)
- [CS201 · Subsystem labs brief](assessments/subsystem-labs-brief.md)

## Readings

- Gregory — Game Engine Architecture (3rd ed.), selected chapters

## Assessment

Subsystem labs (50%), final engine (50%)
