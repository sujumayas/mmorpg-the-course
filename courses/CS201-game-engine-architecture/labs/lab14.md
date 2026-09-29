# CS201 · Lab 14: A reflected inspector

**Week:** 14 ([lecture](../lectures/w14-tools-and-editors.md))
**Time:** 2 hours in the lab, plus up to 3 hours to finish Part C at home.
**Work mode:** pairs for Parts A and B; Part C in your own final-project engine.
**Counts toward:** subsystem labs (50% of the course grade). Part C's descriptor tables and debug panel are expected in the final engine demo.

## Objective

Write the tool half of a reflection layer: an inspector, a save and load pair that clamps values, warns about unknown keys and follows rename redirects, a field-by-field diff, and an undo history with transactions and redo. Every tool must work for any component, including one the tests declare that your code has never seen. Then bring the same idea to your C++ engine with a descriptor table and a generic debug panel.

## Starter materials

All in [`lab14-starter/`](lab14-starter/). Python 3.10 or later, standard library only (in this repository, `.venv/bin/python`).

- [`reflect.py`](lab14-starter/reflect.py). Provided: `prop()` (the lecture's field declaration with range, `save`, `edit` and `net` flags), a `@component` decorator that registers each component class by name, `descriptors()`, `clamp()`, and three components (`Health`, `Spawner`, `Door`). You write five parts marked `TODO 1` to `TODO 5`; each docstring states exactly what the checks expect. Run `python reflect.py` for a short demo; unwritten parts print a dash.
- [`test_reflect.py`](lab14-starter/test_reflect.py). Run `python test_reflect.py` from inside the starter folder. It prints PASS or FAIL for eight checks and exits with status 1 until all pass. On the untouched starter all eight fail. The test file declares its own `Lamp` component, so a tool that names fields cannot pass.
- The interactive [`examples/w14-fields-times-systems.html`](../examples/w14-fields-times-systems.html), for Part B.
- For Part C: your engine, the member-pointer table from lecture section 3, and optionally Dear ImGui (https://github.com/ocornut/imgui) if your engine already draws a debug overlay.

## Steps

### Part A: the tools (70 min)

1. Write `inspector_rows(obj)` (TODO 1). It returns `(name, value, lo, hi)` for each field whose metadata says `edit=True`. The step 1 check runs it on `Spawner` and on the test's `Lamp`.
2. Write `save(obj)` (TODO 2). Only fields with `save=True` go into the output. The step 2 check confirms that `Health.last_hit_by` stays out.
3. Write `load(data, redirects)` (TODO 3). Follow the docstring in order: apply redirects, skip and warn about undeclared keys, clamp and warn, keep defaults for missing fields. The three step 3 checks test a clean round trip for all four components, a saved file with a rename, an out-of-range value and a misspelled key, and a saved runtime-only field. In your README, explain in two sentences why a saved `last_hit_by` should produce a warning rather than be loaded.
4. Write `diff(a, b)` (TODO 4). It compares only saved fields, in declaration order, and raises `TypeError` for two different component types. In your README, say what a level-merge tool would do with this output when two designers edit the same door.
5. Write `History` (TODO 5): `begin`, `set`, `end`, `undo` and `redo`. `set` clamps through the field metadata, and repeated sets of one field inside a transaction keep the first old value. An empty transaction is dropped. A new transaction clears the redo stack. The two step 5 checks replay a 27-event slider drag, a multi-object edit, and an undo-redo sequence.

### Part B: count your own project (15 min)

6. List every component in your final-project engine with its fields. Count `F`. List the tool systems you have or plan (inspector, save, load, undo, network, anything else). Count `S`. Enter both in the interactive and record: code sites by hand, code sites reflected, and the expected number of fields with a hole at `q = 2%` if you add 30 fields before the final demo.
7. Pick the one system in your engine most likely to be forgotten when someone adds a field. Say why, in one sentence.

### Part C: your engine (at home)

8. For at least three of your components, write a descriptor table in C++ in the style of lecture section 3. Support at least `float`, `int` and `bool` fields. A tagged union or one table per field type are both fine; state which you chose and why.
9. Write two generic tools that loop over the tables: a save/load pair that writes and reads one component as `name=value` lines (or your week 12 format), and a debug panel that shows every editable field of the selected entity. With Dear ImGui, the panel is one `SliderFloat`, `SliderInt` or `Checkbox` per descriptor using its range. Without it, print the fields to your debug overlay and let a console command set a field by name.
10. Route every panel edit through an undo history with transactions, so that one slider drag is one undo step. Demonstrate it on video or with a log.
11. Add one field to one component. Record every file you had to touch to make it appear in the panel, save, load and undo. The target is one file.

## Deliverable

- Your completed `reflect.py` with `test_reflect.py` output pasted into a `README.md` (all eight checks passing).
- In the README: the notes from steps 3 and 4, the Part B counts and the answer to step 7.
- From Part C: the code diff, a short screen capture or log of the panel editing a field and one undo undoing a whole drag, and the step 11 list of touched files.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Generic tools (35%) | All eight checks pass; no tool names a component or field; README notes for steps 3 and 4 are correct and specific | All checks pass, notes vague | Five to seven checks pass | Four or fewer |
| Project count (15%) | `F`, `S`, both site counts and the expected holes computed from the formulas; step 7 names a system with a concrete reason | Counts present, one missing or unexplained | Counts guessed | Missing |
| Engine reflection (30%) | Descriptor tables for three components and three field types; save/load and debug panel loop over them; a new field needs one edit (step 11) | Works for two components or two types, or a new field needs two edits | Panel or save/load hand-written per field | Missing |
| Undo in the engine (20%) | Every panel edit goes through the history; one drag is one undo step, shown in the capture or log | Undo works, one entry per event | Undo for some fields only | Missing |
