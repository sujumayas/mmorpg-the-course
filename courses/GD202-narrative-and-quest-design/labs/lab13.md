# GD202 · Lab 13: Phase budget for a zone

**Assigned:** week 13 ([lecture](../lectures/w13-shared-vs-personal-story.md), [interactive](../examples/w13-phase-split.html)). **Due:** start of week 14 class. **Feeds:** the final quest chain (60%), which must include a consequence table for its zone.

## Objective

Turn the visible-share model from the lecture into a small tool, run it on a zone whose story splits its players too much, and redesign the zone until it meets a producer's targets without losing its visible world change. By the end you should be able to defend every phase in your own quest chain with a number.

## Starter materials

The folder [`lab13-starter/`](lab13-starter/) contains:

- [`phasing.py`](lab13-starter/phasing.py). The model with five stub functions: `visible_share`, `expected_visible`, `effective_phases`, `per_phase_visible` and `phase_shares`. It also has a `report` function and a command line. It runs as shipped (`python phasing.py saltmarsh.json`) and prints a TODO until you fill in the stubs.
- [`saltmarsh.json`](lab13-starter/saltmarsh.json). A six-step zone chain with a flood, a dam choice split 60/40, and a boss kill, plus a funnel saying where the zone's 41 players stand.
- [`test_phasing.py`](lab13-starter/test_phasing.py). Seven tests. All seven fail on the starter. They run with `python test_phasing.py` (no packages needed) or with `pytest` if you have it.

### The zone file format

```json
{
  "zone": "Saltmarsh",
  "population": 41,
  "chain": [
    {"id": "warning", "title": "The flood warning", "sets_phase": "flooded"},
    {"id": "dam", "title": "Blow the dam or repair it",
     "sets_phase": {"dam_blown": 0.6, "dam_repaired": 0.4}}
  ],
  "funnel": [0.5, 0.3, 0.2]
}
```

- `sets_phase` is `null` (no world change), a string (one flag), or an object mapping flags to the fraction of players who pick each option.
- `funnel[k]` is the share of the zone standing at position `k`. Position `k` means the player has completed the first `k` steps. The last position means "finished, still in the zone". The funnel has one more entry than the chain.
- A player's phase is the list of flags from their completed steps, in order, joined with `+`. A player with no flags is in phase `base`.

## Steps

1. **Implement the formulas (20 min).** Fill in `visible_share`, `expected_visible`, `effective_phases` and `per_phase_visible`. The first two tests pass when these are right.
2. **Implement `phase_shares` (45 min).** Walk the chain from position 0. Keep a distribution over flag lists for players who have completed the steps so far, starting at `{(): 1.0}`. At each position, add `funnel[k]` times that distribution into the result. Then apply step `k`: a string appends one flag; a choice splits each entry by its fractions. Raise `ValueError` for a funnel of the wrong length, a negative entry, a funnel that does not sum to 1, or choice fractions that do not sum to 1. Drop phases with share exactly 0. Run the tests until all seven pass.
3. **Report the Saltmarsh (15 min).** Run `python phasing.py saltmarsh.json`. Copy the report into your write-up. Check two phase shares by hand and show the arithmetic.
4. **Redesign the Saltmarsh (45 min).** The producer's targets for a peak population of 41:
   - a typical player sees at least 20 of the 40 others (`expected_visible ≥ 20`);
   - a player in the smallest phase sees at least 3 others;
   - at least one step still visibly changes the world, and the dam choice still exists.
   Save your design as `saltmarsh_v2.json`. You may move phase changes, remove them (the change then happens in an instance or in dialogue only), merge the two dam outcomes into one visible phase with the difference kept in a private flag, or change the funnel if you can justify it with a design change (for example, a shorter chain). Record each change in a table: what you changed, which consequence cell it moved to (lecture section 3), and the new numbers.
5. **Your own zone (30 min).** Write a zone file for the quest chain you are building for the final project. Run it. If it misses the targets, say whether you will fix it or accept it, and why.
6. **Write it up.** See the deliverable.

## Deliverable

A zip or repository link containing:

- `phasing.py` with all seven tests passing (paste the test output into the write-up).
- `saltmarsh_v2.json` and your own zone file.
- `lab13.md`, 600 to 900 words, with: the Saltmarsh report and hand checks; the redesign table with before and after numbers for `V`, expected visible and smallest phase; a consequence table for your own zone (scope and duration for every world-changing step); and one paragraph on what the Saltmarsh story lost in your redesign and how you compensated.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Weight |
|---|---|---|---|---|
| Model implementation | All seven tests pass; code handles choices after choices | Formulas correct, `phase_shares` fails on choices | Fewer than four tests pass | 25% |
| Hand checks | Two shares and `V` checked by hand, arithmetic shown and correct | One check, or checks with small errors | No hand checks | 10% |
| Redesign meets targets | Both numeric targets met and the world change and choice kept | One target met, or targets met by deleting the choice | Targets not met | 25% |
| Design reasoning | Each change placed in the consequence table and justified by what players experience | Changes listed with thin justification | Numbers only, no reasoning | 20% |
| Own zone | Zone file runs, numbers reported, decision to fix or accept argued | File runs, no decision | Missing | 10% |
| Writing | Clear, within length, numbers match the files | Minor mismatches | Numbers cannot be reproduced | 10% |
