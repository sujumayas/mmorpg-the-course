# MMO406 · Lab 05: Naming languages players can tell apart

**Week:** 5, cultures, languages, names ([lecture](../lectures/w05-cultures-languages-names.md)).
**Time:** 2 hours in lab, plus about 3 hours at home.
**Weight:** part of the exercises (40%). The culture sheets and naming languages go into the cultures chapter of your world bible.

## Objective

Implement the week 5 overlap model and a weighted name generator. Then build naming languages for two cultures of your own, tune them so each is recognizable to a target you set, and test the prediction against real listeners.

## Starter materials

All in [`lab05-starter/`](lab05-starter/). Standard-library Python, run with `.venv/bin/python`.

- [`naming.py`](lab05-starter/naming.py) has the model in its docstring, a finished `could_pass` helper and four empty functions: `overlap`, `ambiguity`, `mixed_ambiguity` and `generate`.
- [`cultures.py`](lab05-starter/cultures.py) holds the lecture's Vessari and Durhk inventories with their weights.
- [`test_naming.py`](lab05-starter/test_naming.py) holds the test values. Count and weighted overlap in both directions (0.333, 0.5, 0.60, 0.25). The lecture table (36%, 21.6%, 6.25%, 18%, 0%). Check-yourself question 1 (9% and 2.7%). Mixed lengths: half two-syllable and half three-syllable Vessari names give 28.8%. The generator must be repeatable for a fixed seed, and over 20,000 names its share of names that could pass for Durhk must land within 1.5 points of the model, with and without a marker.
- The [interactive](../examples/w05-name-overlap.html), whose name strip uses the same generator rule.

Run the tests from the repository root:

```
.venv/bin/python courses/MMO406-worldbuilding-and-lore-for-persistent-worlds/labs/lab05-starter/test_naming.py
```

On the starter all eight tests report `TODO` and the script exits with status 1.

## Steps

1. **Model.** Implement `overlap`, `ambiguity` and `mixed_ambiguity`. Remember that overlap is directional.
2. **Generator.** Implement `generate` exactly as its docstring says, so your output matches the tests and the interactive. Run `naming.py` and confirm three of the twelve sample Vessari names are flagged as passing for Durhk.
3. **Two culture sheets.** Pick two cultures from your bible that live near each other. Fill in the six-row culture sheet from lecture section 1 for each. Every answer must name the system it touches.
4. **Two naming languages.** For each culture write 8 to 16 syllables with usage weights, a length distribution (for example 60% two syllables, 40% three), and at most one structural marker with its share `m`. Justify the marker from the culture sheet in one sentence. Share at least three syllables between the cultures, and say what shared history those syllables stand for.
5. **Tune.** Set a target: each culture's names should pass for the other's at most 10% of the time under `mixed_ambiguity`, in both directions. Adjust weights, lengths or markers until you meet it. Record every change and its effect in a table.
6. **Glosses.** Gloss at least 12 morphemes for one culture (level 2 of the language ladder) and use them to name five places on your week 2 map. One of the five must be a ruin from your week 4 history.
7. **Blind listening test.** Generate 20 names from each culture (40 in total, shuffled, seed recorded). Give the list to three classmates who have not seen your inventories. Tell them only that there are two cultures and give three example names of each. Ask them to sort the list. Report their accuracy and compare it with `1 − P_amb` for each culture.
8. **Reflect.** In at most 250 words, explain any gap between the model and the listeners. Name the cue listeners used that the model ignores (stress, letter shapes, length, a marker you did not intend).

## Deliverable

`naming.py` with all tests passing; a `my_cultures.py` with your two inventories, length distributions and markers; and a report of at most 1,000 words containing the two culture sheets, the tuning table, the gloss list with five place names, the listening-test results with the model's predictions, and the reflection.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Model and generator correctness | All eight tests pass | Six or seven pass | Fewer than six | 25% |
| Culture sheets | Every answer creates play and touches a named system; answers share causes | Most answers touch systems; a few are adjectives | Adjective lists | 20% |
| Naming design and tuning | Target met in both directions; markers justified by culture; shared syllables carry history | Target met one way, or markers unjustified | Target missed with no analysis | 20% |
| Glosses and place names | 12+ glosses; place names decode into facts about the map and history | Glosses present, names only partly meaningful | Missing | 15% |
| Listening test and reflection | Clean blind test, accuracy compared with the model, a specific cue identified | Test run, comparison vague | No test | 20% |

<details>
<summary>Instructor check values</summary>

- `overlap(VESSARI, DURHK)` is 0.60, `overlap(DURHK, VESSARI)` is 0.25; count views 0.333 and 0.5.
- `mixed_ambiguity(0.6, {2: 0.5, 3: 0.5})` is `0.5 × 0.36 + 0.5 × 0.216 = 0.288`.
- With the reference generator, seed 1, `generate(VESSARI, 12, 2)` flags three names (Rara, Anan, Anto). A student whose sample differs has probably drawn the marker test or the syllables in a different order from the docstring.
- Typical listening results: listeners beat the model when one culture uses a marker or distinctive consonant clusters, and do worse than the model when both cultures share vowel patterns. Either is fine if the student explains it.
- Watch for students who reach the 10% target by making one culture unpronounceable. The rubric's "creates play" and the reflection should catch it; ask them to read five names aloud.

</details>
