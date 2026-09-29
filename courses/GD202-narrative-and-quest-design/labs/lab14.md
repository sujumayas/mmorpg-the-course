# GD202 · Lab 14: A narrative test harness

**Assigned:** week 14 ([lecture](../lectures/w14-narrative-testing.md), [interactive](../examples/w14-playthrough-coverage.html)). **Due:** with the final quest chain in week 15. **Feeds:** the final quest chain (60%). The harness report on your own chain is a required appendix.

## Objective

Build a small tool that tests a branching story the way the lecture recommends. It searches every reachable (node, flags) state, checks invariants, computes each ending's exact probability for a random bot, and runs seeded random playthroughs to confirm it. Use it to find three planted bugs, fix them, and then test your own final-project chain.

## Starter materials

The folder [`lab14-starter/`](lab14-starter/) contains:

- [`lantern.json`](lab14-starter/lantern.json). "The Lantern Keeper", a ten-node story about a lighthouse, with three planted bugs. Read it before you write any code.
- [`harness.py`](lab14-starter/harness.py). Eight stub functions (`available`, `explore`, `unreachable_nodes`, `dead_ends`, `speaker_violations`, `outcome_probabilities`, `random_playthroughs`, `runs_needed`), a loader and a `report` function. It runs as shipped (`python harness.py lantern.json`) and prints a TODO until you fill in the stubs.
- [`test_harness.py`](lab14-starter/test_harness.py). Six tests. All six fail on the starter. They run with `python test_harness.py` (no packages needed) or with `pytest` if you have it.

### The story file format

```json
{
  "start": "dock",
  "dead_flags": {"Keeper": "keeper_dead"},
  "nodes": {
    "door": {"speaker": "Keeper", "ending": false, "choices": [
      {"text": "Offer to help", "to": "stairs", "sets": ["trusted"]},
      {"text": "Light the lamp", "to": "lit", "requires": ["oil"], "forbids": ["keeper_dead"]}
    ]}
  }
}
```

- A choice is available when every flag in `requires` is set and no flag in `forbids` is set. Missing lists are empty.
- Taking a choice moves to `to` and adds the flags in `sets`. Flags are never cleared in this lab.
- `dead_flags` maps a speaker to the flag that means they are dead. A node spoken by that speaker must never be reached with that flag set.
- Stories in this lab have no cycles, so every playthrough ends at an ending or gets stuck.

## Steps

1. **Read the story (15 min).** Draw `lantern.json` as a flowchart on paper. Before running anything, list every bug you can find by hand and the path that shows it. Keep this list. You will compare it with the tool's list.
2. **Search the states (40 min).** Implement `available` and `explore`. `explore` is a breadth-first search from `(start, frozenset())`, exactly like the forge example in lecture section 3. Then implement `unreachable_nodes`, `dead_ends` and `speaker_violations`. The first three tests pass when these are right. The story has 32 reachable states.
3. **Exact probabilities (30 min).** Implement `outcome_probabilities` for a bot that picks uniformly among available choices. Recurse from the start state. An ending returns probability 1 for itself. A stuck state returns 1 for `DEAD_END`. Otherwise, average over the available choices. Memoise on the state if you like. Check one value by multiplying the choice probabilities along its path by hand.
4. **Random playthroughs (20 min).** Implement `random_playthroughs` with `random.Random(seed)` and `runs_needed` with the lecture's formula. The tests check that 4,000 seeded runs land within 3 percentage points of your exact values, and that the same seed gives the same counts.
5. **Fix the story (25 min).** Save a corrected copy as `lantern_fixed.json`. It must report no unreachable nodes, no dead ends and no dead speakers. The fixes must be narrative, not deletions. For each bug, write one sentence on what the player would have experienced and one on your fix. Rerun the report and note how the outcome probabilities changed.
6. **Test your own chain (30 min).** Convert the dialogue and quest logic of your final-project chain into this format (or write an adapter from your Ink or Yarn Spinner file, see week 12). Run the harness. Fix what it finds, or argue why a flagged state is intended.
7. **Write it up.**

## Deliverable

A zip or repository link containing:

- `harness.py` with all six tests passing (paste the test output into the write-up).
- `lantern_fixed.json` and the harness report for it.
- Your own chain in the story format, and its harness report.
- `lab14.md`, 600 to 900 words, with: your hand-found bug list compared with the tool's list; for each Lantern bug, its path, its probability for a uniform bot, and the runs a random tester would need for 95% confidence of hitting it; the before and after outcome probabilities; and a short test plan for your final chain that names which checks you will run on every build and which need people.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Weight |
|---|---|---|---|---|
| State search and invariants | Tests 1 to 3 pass; code is general, not special-cased to the Lantern | Search works, one invariant check wrong | Search does not work | 25% |
| Probabilities and random runs | Tests 4 to 6 pass; one value checked by hand with the path shown | Exact or random part works, not both | Neither works | 20% |
| Story fixes | All three bugs fixed with narrative changes; report clean; each fix explained | Report clean but a fix deletes content without reason | Bugs remain | 20% |
| Own chain tested | Chain converted, harness run, findings fixed or argued | Chain converted, findings listed without action | Not attempted | 15% |
| Analysis | Hand list compared with tool list; runs-needed figures correct; test plan separates automatic from human checks | Most figures correct, plan vague | No analysis | 15% |
| Writing | Clear, within length, numbers reproducible from the files | Minor mismatches | Numbers cannot be reproduced | 5% |
