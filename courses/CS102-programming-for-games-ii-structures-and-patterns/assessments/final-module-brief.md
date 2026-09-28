# CS102 · Final module brief: a data-driven RPG combat module

**Weight:** 35% of the course grade.
**Assigned:** week 13. **Milestone:** data freeze at the end of week 13. **Final submission:** start of week 15, followed by a 20-minute code review in week 15.
**Work mode:** individual or the same pair as labs 13 and 14. Pairs submit once with a contribution statement.
**Lectures:** [week 13, data-driven design](../lectures/w13-data-driven-design-stats-in-json-and-csv.md) and [week 14, unit testing gameplay rules](../lectures/w14-unit-testing-gameplay-rules.md), resting on [week 11, state machines](../lectures/w11-state-and-state-machines.md), [week 12, the Command pattern](../lectures/w12-command-pattern-input-replay-undo.md) and [week 10, events](../lectures/w10-observer-and-events.md).

## What this component is for

A combat module is the part of an RPG that designers tune most and programmers most fear to touch. This assessment asks you to build one that designers can change without you and that you can change without fear. Numbers live in validated data. Rules live in small pure functions with tests that sweep their domains. Every fight can be replayed exactly from a seed and a command list, so a balance change shows up as a changed fingerprint rather than a player complaint.

It assesses all four course outcomes, and most directly "write testable gameplay code".

## What you build

A Python package, `combat`, Python 3.10 or later, standard library only. It runs fights between a party of up to 4 combatants and a group of up to 6 monsters, in integer ticks or turns. It has no graphics. A command-line tool drives it.

### 1. Data layer (from lab 13)

- `data/weapons.csv` with at least 8 weapons, `data/monsters.json` with at least 6 monsters (at least two using `parent` inheritance), `data/skills.json` with at least 6 skills whose effects are nested lists, and `data/status.csv` with at least 3 status effects (duration, tick damage or modifier).
- One loader per file in the lab 13 style: parse, validate, index by id. It checks syntax, types, ranges, uniqueness and every cross-file reference, collects every problem with a location a designer can act on (`line 7` or `goblin.loot[1]`), and refuses to start on bad data.
- Unknown columns and keys are errors, not silently ignored. Write one sentence in the design notes on why.
- A tuning mode, `python -m combat tune`, that reloads changed files while running and keeps the last good tables when a new file fails validation.

### 2. Rules

- Pure functions for hit chance, damage after armor, critical hits, status ticks and turn order. Randomness always arrives as an argument (`rng`). Time always arrives as an argument (`dt` or a tick count).
- Rules live in code. If some weapons need a different rule, a data column names one of a small set of rules implemented and tested in code. No formulas in data files.

### 3. Patterns

- **State.** Each combatant runs a table-driven state machine with at least these states: ready, casting (timed), stunned (timed), dead. Illegal actions for a state are rejected in one place.
- **Command.** Player choices and AI choices are the same command classes (`Attack`, `Cast`, `Guard`, `UseItem` or your own), validated at execute time against the state machine and the current world.
- **Events.** The module emits past-tense events (`damage_dealt`, `status_applied`, `combatant_died`, `fight_ended`) with snapshot payloads. The combat log and a fight-statistics collector are listeners. At least one listener is queued.

### 4. Deterministic replay

- `python -m combat fight PARTY.json ENCOUNTER.json --seed 42 --record out.rep` runs a fight with scripted or AI choices and records it: a header with a format version, the data-file hashes and the seed, then the command list, then a state checksum every 10 ticks or every turn.
- `python -m combat replay out.rep` replays in a fresh process and prints `MATCH` or the first tick whose checksum differs, with both states side by side (your lab 12 bisect tool).
- A replay recorded against different data files must be refused with a clear message, as Doom refuses a demo from another version.

### 5. Tests (from lab 14)

At least 30 tests in four groups, run with `python -m unittest -v`.

- **Rule tests.** Example tests that explain each rule and property tests that sweep its domain with `subTest`. Every random rule is tested with an injected generator.
- **Data tests.** Design promises about the shipped data, such as "an upgrade always has higher DPS" and "no id that has shipped has disappeared".
- **Regression tests.** One test per bug you fixed, written before the fix. Name the bug in the test's docstring.
- **Replay tests.** At least three recorded fights with stored fingerprints.

### 6. A balance tool

`python -m combat simulate PARTY.json ENCOUNTER.json --fights 1000` runs 1,000 fights with seeds 0 to 999 and prints the party's win rate, the mean and 90th-percentile fight length and the mean damage by source. It must finish in under 30 seconds on the lab machines. Because every fight is seeded, the output is identical on every run.

## Deliverables

- The `combat` package with the data files, the tests, three `.rep` files and one example party and encounter.
- `README.md` for a **designer**, not a programmer. How to add a weapon, a monster that inherits from another, and a skill, without touching Python. What the validator's messages mean. How to run the tuning mode and the balance tool.
- `DESIGN.md`, 1,500 to 2,000 words, with these sections.
  1. **Data schema.** Every file, every column or key, its type, its range, its default (or "required"), and which ids it references.
  2. **Rules.** Each formula once, with symbols named, and the test properties that guard it.
  3. **State machine.** The transition table and where each side effect lives.
  4. **Replay format.** The byte or JSON layout, a size prediction for a 60-tick fight made before measuring, and the measured size.
  5. **A balance change, end to end.** Change one number in the data to meet a stated goal (for example, raise the warrior's win rate against the troll pack from 40% to 55%). Show the simulate output before and after, which replay fingerprints changed and why, and the commit that updates them.
  6. **What your tests cannot see.** Two bugs your suite would miss, and why.
- Pairs only: `CONTRIBUTIONS.md`.

## Milestone: data freeze (end of week 13, 10 points)

Submit the four data files, the loaders passing their validation on your data, and three deliberately broken copies that your loader rejects with the right locations. This is your lab 13 work extended to all four files. After the freeze you may add rows freely, but a change to a column or key name must be listed in `DESIGN.md` with a reason, the way a real team would announce a schema change.

## Code review (week 15, 20 minutes)

You run your submission on a lab machine from a clean copy while two examiners watch. Each review follows the same five steps so that every student gets the same test.

1. **Designer change (3 min).** The examiner names a weapon and a new value. You edit one cell in the tuning mode and show the change take effect without a restart.
2. **Broken data (3 min).** The examiner gives you a data file with five planted problems of the week 13 kinds. Your loader must report all five with locations and refuse to start.
3. **Hidden mutants (4 min).** The examiner runs your test suite against three hidden mutated copies of your own `rules.py` (for example, `<` changed to `<=` at a boundary, a cap removed, a remainder dropped). Each mutant your suite catches scores.
4. **Replay (3 min).** You replay one of your `.rep` files, then the examiner changes one number in the data and you show that the replay is refused or reports the first differing tick.
5. **Questions (7 min).** Three questions in the style of the [exam bank](exam-bank.md), rewritten with your code, data and numbers. At least one is a trace or a compute question.

## Rubric

### Milestone (10 points)

| Criterion | Excellent | Good | Weak | Missing | Points |
|---|---|---|---|---|---|
| Data files | 4: all four files, counts met, ids stable and lowercase | 3: one file short of its count | 1 to 2: two or more files missing or thin | 0 | 4 |
| Validation | 6: all three broken copies rejected with every problem located | 4 to 5: one problem unlocated or one copy accepted | 1 to 3: stops at the first error | 0 | 6 |

### Final submission and code review (90 points)

| Criterion | Excellent | Good | Adequate | Weak or missing | Points |
|---|---|---|---|---|---|
| Data layer and designer workflow | 12 to 14: all five check kinds with locations; unknown keys rejected; live reload keeps the last good table; designer README works as written | 9 to 11: one check kind or the reload guard missing | 5 to 8: validation partial, README for programmers | 0 to 4: hard-coded numbers remain | 14 |
| Rules | 9 to 10: pure functions, injected `rng` and time, no formulas in data, rule selection by named id | 7 to 8: one rule reads global state | 4 to 6: rules mixed into classes with side effects | 0 to 3: untestable | 10 |
| Patterns (state, command, events) | 12 to 14: table-driven machines with timers; one command path for player and AI validated at execute time; snapshot payloads and a queued listener | 9 to 11: one pattern weak | 5 to 8: two patterns weak | 0 to 4: patterns missing | 14 |
| Deterministic replay | 10: `MATCH` in a fresh process; data hashes in the header; mismatch reported at the first tick with both states | 7 to 9: matches, but data changes are not detected | 4 to 6: matches in one process only | 0 to 3: drifts or missing | 10 |
| Test suite | 12 to 14: 30 or more tests in all four groups; properties sweep domains; regression tests name their bugs | 9 to 11: one group thin | 5 to 8: mostly examples, no injected randomness | 0 to 4: few or failing | 14 |
| Balance tool and `DESIGN.md` | 11 to 12: all six sections; prediction before measurement; balance change shown end to end with fingerprints | 8 to 10: one section thin | 5 to 7: balance change missing | 0 to 4: missing | 12 |
| Code review | 15 to 16: all five steps pass, catches 3 of 3 mutants, answers with reference to code and numbers | 11 to 14: catches 2 mutants, or one step needs help | 6 to 10: two steps fail, or answers vague | 0 to 5: cannot run or explain | 16 |
| **Total** | | | | | **90** |

The module mark is the milestone plus the final, out of 100, multiplied by 0.35.

## Rules and advice

- **Your labs are the start.** Lab 13 is the loader and lab 14 the test suite. Labs 11 and 12 give you the `FSM` and the recorder. The pattern project gave you a bus. Most of the work in weeks 13 to 15 is joining them, extending the data, and writing the tests and the design notes.
- **Record fights early.** Record your first fight the day your commands work. Every later change then tells you whether it changed a fight, which is the whole point of the module.
- **Keep content invented.** Weapon, monster and skill names and numbers are your own. You may borrow structure from the games the lectures discuss (a `parent` field, weighted loot pools), not their content.
- **Late submission.** Up to 48 hours late, the final is marked out of 80 instead of 90, and the code review is rescheduled if the timetable allows. The milestone cannot be late.
- **Integrity.** The rules in the [labs brief](labs-brief.md#academic-integrity) apply. In the code review you must be able to explain every file you submit.
