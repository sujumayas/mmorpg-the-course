# MMO406 · Lab 13: Roleplay hubs and the community chapter

**Week:** 13, community lore and roleplay ([lecture](../lectures/w13-community-lore-and-roleplay.md), [interactive](../examples/w13-rp-hubs.html)).
**Time:** 2 hours in lab, plus about 3 hours at home.
**Weight:** part of the exercises (40%). The hub plan and policies you write here become the "community" chapter of your world bible.

## Objective

Implement the week 13 hub model and extend it from one hour to a whole day, with an optional night-time fallback hub. Use it to choose a hub plan for Dikeholm, *Thornmere*'s capital. Then write the community chapter of your own bible: named hubs sized with the model, open slots for player characters, a naming guide, and a policy for player history and fanon.

## Starter materials

All in [`lab13-starter/`](lab13-starter/). Standard-library Python, run with `.venv/bin/python`.

- [`rp_hubs.py`](lab13-starter/rp_hubs.py) has the model in its docstring and six empty functions: `p_at_least`, `viable_hubs`, `scene_share`, `best_hubs`, `day_plan` and `choose_plan`. It also has a `report` function and a command line. As shipped it prints a TODO and exits with status 1.
- [`dikeholm_rp.json`](lab13-starter/dikeholm_rp.json) holds 24 hourly counts of roleplayers looking for a scene in Dikeholm (hour 0 is midnight), the minimum cast `k = 4`, a target day-wide share in a scene of 85%, and a fallback threshold of 12.
- [`test_rp_hubs.py`](lab13-starter/test_rp_hubs.py) holds seven tests. They check the lecture's table, the best number of hubs for several crowds, the day plans with and without the fallback, and the plan chooser.

### The day file format

```json
{
  "city": "Dikeholm, Thornmere's capital",
  "k": 4,
  "target_share": 0.85,
  "fallback_below": 12,
  "hourly": [8, 6, 4, 3, 2, 2, 1, 1, 2, 3, 4, 5, 6, 6, 7, 8, 10, 14, 20, 26, 30, 28, 20, 12]
}
```

`fallback_below` means: in any hour with fewer roleplayers than this, everyone uses the one "never closes" hub.

Run the tests and the report from the repository root:

```
.venv/bin/python courses/MMO406-worldbuilding-and-lore-for-persistent-worlds/labs/lab13-starter/test_rp_hubs.py
.venv/bin/python courses/MMO406-worldbuilding-and-lore-for-persistent-worlds/labs/lab13-starter/rp_hubs.py courses/MMO406-worldbuilding-and-lore-for-persistent-worlds/labs/lab13-starter/dikeholm_rp.json
```

On the starter all seven tests report `TODO` and the script exits with status 1.

## Steps

1. **The Poisson tail (15 min).** Implement `p_at_least`. Sum the Poisson probabilities for 0 to `k − 1` and subtract from 1. Return exactly 1.0 when `k <= 0`, because a scene that needs nobody always runs.
2. **One hour (15 min).** Implement `viable_hubs` and `scene_share` from the lecture's formulas, then `best_hubs` (try every `H` from 1 to `h_max`; ties go to the smaller `H`). The first three tests pass.
3. **One day (30 min).** Implement `day_plan`. Loop over the hours, skip hours with zero roleplayers, use one hub in hours below `fallback_below` when it is set, and accumulate live hub-hours, the roleplayer-weighted share (`Σ Λ_h × S_h / Σ Λ_h`) and the worst hour. Then implement `choose_plan`. Run the tests until all seven pass.
4. **Read the report (15 min).** Run the report on `dikeholm_rp.json`. Answer in writing: without a fallback, why does the chooser pick one hub even though six hubs are best at 9 p.m.? With the fallback, which `H` does it pick, and how many live hub-hours does the fallback add compared with the same `H` without it? Which hour is the worst in every plan, and what would you write into the fiction to help it?
5. **Your city (45 min, at home).** Pick the capital (or main social city) of your own world. Write a day file for it: estimate hourly roleplayer counts from a stated assumption (for example, 3% of peak concurrent players roleplay, with the same daily curve as the whole population), and choose `k` for its typical scene. Justify each number in one sentence. Run the chooser with and without a fallback, and for two targets (80% and 90%). Report the four results in one table.
6. **The community chapter (60 min, at home).** Write the chapter, 1,200 to 1,800 words, with these parts:
   - **Hubs.** One entry per hub in your chosen plan, with name, location, owner, scene types, busy hours in the fiction and two standing tensions from your lab 01 ledger. Mark the fallback hub and give it an in-world reason to never close.
   - **Open slots.** At least five: one order with open membership, one set of houses or villages, one distant place, one period from your lab 04 reserved gaps, and one of your choice. Check each for the "last of" trap and say how it passes.
   - **Naming guide.** For each playable culture, the syllables and three example names from your lab 05 naming language, and a reserved-name list.
   - **Player history and fanon policy.** The three rules of lecture section 3 applied to your world, with one example inscription, and your order of preference when a patch meets fanon.
   - **Canon ladder.** The lecture's table filled in with examples from your world, and the tier (from your lab 11 tier table) at which acknowledgements enter canon.

## Deliverable

A zip or repository link containing:

- `rp_hubs.py` with all seven tests passing (paste the test output into the report).
- Your day file.
- `lab13.md`, 500 to 800 words, with the step 4 answers and the step 5 table and assumptions.
- `community-chapter.md`, the chapter from step 6.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Model correctness | All seven tests pass; empty hours and `k <= 0` handled as specified | Five or six pass | Four or fewer | 25% |
| Reading the Dikeholm report | Explains the no-fallback choice through the night hours' `S`; fallback gain computed; worst hour named with a fiction fix | Numbers right, explanation thin | Report pasted without reading | 15% |
| Own city model | Hourly counts and `k` justified from stated assumptions; four runs compared and a plan chosen with a reason | Runs complete, assumptions weak | Numbers invented without reasons, or runs missing | 15% |
| Hubs and open slots | Hubs sized by the model, each with owner, scenes, busy hours and ledger tensions; five open slots that pass the "last of" check | Hubs and slots present, some generic or unsized | Hubs not tied to the model, or slots that close the space | 25% |
| Naming, history and canon ladder | Naming guide built from lab 05; policy applies all three rules with an example; ladder filled with the world's own examples and tier | Parts present but generic | Parts missing | 20% |

<details>
<summary>Instructor check values</summary>

- Lecture table (`Λ = 24`, `k = 4`): `V` 1.00, 2.00, 2.87, 3.40, 3.53, 3.40, 2.82, 1.71 for `H` = 1, 2, 3, 4, 5, 6, 8, 12; `S` 100%, 99.9%, 98.6%, 93.8%, 85.7%, 76.2%, 57.7%, 32.3%.
- Best hubs: (24, 4) → 5; (6, 4) → 1; (30, 4) → 6; (30, 10) → 2; (8, 4) → 2; (15, 3) → 4. The day's total is 228 roleplayer-hours and its peak is 30 at 20:00.
- Without fallback: `H = 1` gives 16.41 live hub-hours and share 94.5%; `H = 2` gives 21.71 and 83.9%; `H = 4` gives 23.82 and 65.6%. The chooser picks `H = 1` at an 85% target, because every extra hub also splits the thin night crowds, and the night hours drag the day-wide share below target.
- With fallback below 12: `H = 4` gives 29.54 live hub-hours and share 87.0% and is chosen at 85%; `H = 5` gives 29.82 and 81.4% and is chosen at 80%. The fallback adds `29.54 − 23.82 = 5.72` live hub-hours to `H = 4`. At 99% no plan qualifies.
- Worst hour: 06:00 (one roleplayer, share 8.0% with one hub) in every plan. Good fiction fixes give the early morning a gathering reason (a dawn market, the watch changing at the fallback tavern). Students who propose "more hubs" for the worst hour have misread the model.
- Common student bugs: summing `j` up to `k` instead of `k − 1`; using `k` instead of `k − 1` in `scene_share`; averaging `S` over hours instead of weighting by roleplayers; counting zero-roleplayer hours as worst hours; ties going to the larger `H`.

</details>
