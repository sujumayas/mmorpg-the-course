# CS102 · Pattern project brief: Skirmish

**Weight:** 25% of the course grade.
**Assigned:** week 9. **Milestone 1:** start of week 11. **Milestone 2:** start of week 12. **Final submission:** start of week 14, with a 10-minute demo in week 14.
**Work mode:** individual or pairs. Pairs submit one project and a contribution statement.
**Lectures:** [week 9, Component](../lectures/w09-pattern-component.md), [week 10, Observer](../lectures/w10-observer-and-events.md), [week 11, State](../lectures/w11-state-and-state-machines.md), [week 12, Command](../lectures/w12-command-pattern-input-replay-undo.md). It also uses the undo stacks of [week 6](../lectures/w06-queues-and-stacks-undo-and-command-buffers.md).

## What this component is for

Each pattern lecture showed one pattern solving one problem. Real game code uses several at once, and most of the hard decisions sit where they meet. Does a state change emit an event? Does a replayed command go through the same validation as a live one? Does destroying an entity unsubscribe its listeners? This project asks you to build one small game in which all four patterns do real work, to measure what each one costs, and to prove with a replay that the whole thing is deterministic.

It assesses the course outcomes "use classes, interfaces and composition appropriately" and "apply common game programming patterns".

## The game

Build **Skirmish**, a small arena game in Python 3.10 or later, standard library only. You choose the genre within these limits.

- A grid of at most 20 × 20 cells.
- One player-controlled unit and at least three enemy kinds that differ in behaviour, not only in numbers.
- Either a fixed-tick real-time loop (at most 60 ticks per second) or a turn-based loop. Both must advance the simulation in integer ticks or turns.
- At least two status effects with durations (for example stunned and burning).
- A text display is enough. If you add graphics (pygame, or a Godot front end reading a state dump), the simulation must still run headless for tests and replays.

All names, numbers and content are your own invention. Do not reuse art, names or characters from existing games.

## Required patterns

Each pattern must do a job the game needs. A class that exists only to tick a box earns nothing.

| Pattern | Minimum requirement | Reuses |
|---|---|---|
| Component | Entities are a `World` of components with an index. At least five component types. Systems run in a fixed, documented order. Destruction is deferred to a flush. | [lab 09](../labs/lab09.md) |
| Observer | An event bus with unsubscribe handles and a copy-safe `emit`. At least five past-tense events with payloads. At least one queued listener (presentation or bookkeeping). No listener is left subscribed after its entity is destroyed. | [lab 10](../labs/lab10.md) |
| State | Every enemy kind is driven by a table-driven state machine with at least three states and one timed state. The game flow (title, play, pause, game over) is a pushdown machine. | [lab 11](../labs/lab11.md) |
| Command | Every change to the world comes from a command object, whether the player, the AI or a replay issued it. Commands are validated at execute time. A recording holds a versioned header, the seed, one packed command per tick and a checksum every second. Undo and redo work in either the turn-based game or a small level editor. | [lab 06](../labs/lab06.md), [lab 12](../labs/lab12.md) |

## Deliverables

A zip or repository link containing:

- The game package, runnable with four commands from the project root:
  - `python -m skirmish play` to play.
  - `python -m skirmish record out.rep` to play (or run a scripted player) for 30 seconds or 30 turns and save a recording.
  - `python -m skirmish replay out.rep` to replay in a fresh process and report `MATCH` or the first tick that differs.
  - `python -m unittest -v` to run the tests.
- `demo.rep`, a 30-second (or 30-turn) recording that replays with `MATCH` on every checksum, three runs in a row, including with different `PYTHONHASHSEED` values.
- A test suite with at least 15 tests. It must include one test per pattern that would fail if the pattern were removed or broken (for example, a test that a destroyed enemy receives no further events).
- `REPORT.md`, 1,200 to 1,800 words, with these sections.
  1. **Pattern map.** For each pattern, the files and classes that implement it and the one game problem it solves.
  2. **Event and state tables.** The final event table (name, payload, emitter, listeners, S or Q) and the transition table for each enemy kind.
  3. **Measurements.** Index checks against polling checks per tick for your world at its largest. Event calls against polling checks for one full recording, with the `E × L` against `F × N` model beside the measured numbers. Your recording size against a per-tick snapshot of your world, predicted before you measured.
  4. **A determinism bug.** One real desync you caused or found, how the per-second checksums located it, and the fix.
  5. **Trade-offs.** One paragraph per pattern on a cost it added to your code, with a number where you have one.
- Pairs only: `CONTRIBUTIONS.md`, a short list of who wrote which parts. Both partners must be able to explain any part at the demo.

## Milestones

**Milestone 1, design pack (start of week 11, 10 points).** A document of at most three pages with the component table (entity kinds × component types, with expected counts at the largest moment), the event table carried over from lab 10 and adapted to your game, a first-draft transition table for one enemy kind, and the byte layout of one command with a predicted 30-second recording size. Feedback comes back within a week.

**Milestone 2, vertical slice (start of week 12, 10 points).** A runnable slice with the `World`, the event bus and one enemy kind driven by its state machine, plus at least six passing tests. A scripted 60-tick run prints the events it emitted. No replay yet.

**Final submission and demo (start of week 14, 80 points).** The full game, the recording, the tests and the report. In week 14 you give a 10-minute demo: 3 minutes playing, 2 minutes replaying `demo.rep` in a fresh process, then 5 minutes of questions in the style of the [exam bank](exam-bank.md), rewritten with your code. A typical question is "Your recording is 1,931 bytes. Show me where the header is written and predict the size if you doubled the tick rate."

## Rubric

### Milestone 1 (10 points)

| Criterion | Excellent | Good | Weak | Missing | Points |
|---|---|---|---|---|---|
| Component and event tables | 4: complete, counts estimated, payloads sufficient | 3: complete, counts or payloads thin | 1 to 2: partial | 0 | 4 |
| Transition table | 3: every cell filled, timed state and side effects placed on transitions or states with reasons | 2: filled, side effects unplaced | 1: partial | 0 | 3 |
| Command layout and size prediction | 3: byte layout and arithmetic correct | 2: layout correct, arithmetic slip | 1: layout only | 0 | 3 |

### Milestone 2 (10 points)

| Criterion | Excellent | Good | Weak | Missing | Points |
|---|---|---|---|---|---|
| Slice runs headless and prints its events | 5: runs from a clean copy, events match the table | 3 to 4: runs, events differ from the table without a note | 1 to 2: runs only on the author's machine | 0 | 5 |
| Tests | 5: six or more, each named as a sentence, all pass | 3 to 4: six tests, some vague or failing | 1 to 2: fewer than six | 0 | 5 |

### Final submission and demo (80 points)

| Criterion | Excellent | Good | Adequate | Weak or missing | Points |
|---|---|---|---|---|---|
| Component world | 11 to 12: index always agrees with components; queries in spawn order; systems ordered and documented; deferred destruction with no ghost or crash | 8 to 10: works, one of order, determinism of iteration or deferral is weak | 5 to 7: world works but queries poll or order is accidental | 0 to 4: god class or components in name only | 12 |
| Events | 11 to 12: five or more events with snapshot payloads; unsubscribe on destroy tested; one queued listener with a stated reason | 8 to 10: events work, one bug class untested | 5 to 7: events used, listeners reach back into the world | 0 to 4: direct calls dressed as events | 12 |
| State machines | 11 to 12: table-driven, every enemy kind, timers part of the state, pushdown game flow, no illegal state reachable | 8 to 10: works, one kind uses flags or the game flow is flat | 5 to 7: machines exist but transitions are scattered `if` chains | 0 to 4: booleans | 12 |
| Commands, replay and undo | 14 to 16: every change is a command; `demo.rep` matches in a fresh process under different hash seeds; checksums locate a planted bug; undo and redo clear correctly | 10 to 13: replay matches in one process only, or undo has an edge-case bug | 6 to 9: replay drifts but commands and recording exist | 0 to 5: no replay | 16 |
| Tests | 7 to 8: 15 or more, one per pattern that fails when the pattern breaks, readable names | 5 to 6: 15 tests, pattern coverage uneven | 3 to 4: fewer than 15 or mostly trivial | 0 to 2: none run | 8 |
| Report | 9 to 10: every section present; measurements predicted then measured; a real desync story; trade-offs name numbers | 7 to 8: complete, one section thin | 4 to 6: measurements missing or unexplained | 0 to 3: missing | 10 |
| Demo and questions | 9 to 10: plays, replays live, answers questions with reference to the code and numbers | 7 to 8: one question needs help | 4 to 6: demo works, answers vague | 0 to 3: cannot run or explain | 10 |
| **Total** | | | | | **80** |

The project mark is the sum of the three parts, out of 100, multiplied by 0.25.

## Rules and advice

- **Start from your labs.** Labs 9 to 12 give you the `World`, the bus, the `FSM` and the recorder. Copy them in during week 9 and let them evolve. If you dropped one of those labs, you still need the code.
- **Determinism is a feature, so test it from day one.** Add the replay test in the week you add commands, not the night before the deadline. The checksum bisect tool from lab 12 saves hours.
- **Keep the game small.** A 10 × 10 grid with three enemy kinds that each use their states well earns full marks. Scope beyond the requirements earns nothing extra.
- **Late submission.** Up to 48 hours late, the final part is marked out of 70 instead of 80. Milestones cannot be late, because their value is the feedback.
- **Integrity.** The rules in the [labs brief](labs-brief.md#academic-integrity) apply. In the demo you must be able to explain every file you submit.
