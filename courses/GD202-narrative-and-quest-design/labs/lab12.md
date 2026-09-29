# GD202 · Lab 12: Variation engine

**Week:** 12, tools: Ink and Yarn Spinner ([lecture](../lectures/w12-tools-ink-and-yarn-spinner.md)).
**Time:** 2 hours in lab, plus about 3 hours at home.
**Weight:** part of the dialogue exercises (40%). The scene you write in Part B can become a scene in your final quest chain.

## Objective

Implement the line-selection rules that ink and Yarn Spinner offer, check them against the lecture's repetition formulas, and then write a gate-guard scene in one of the two tools that uses stopping for escalation, a bag for ambient barks, state for a condition, and a once-only option.

## Starter materials

- [`lab12-starter/variation.py`](lab12-starter/variation.py): Python, standard library only. `Stopping` is written for you as a model. You write `Once`, `Cycle`, `RandomPick`, `ShuffleBag`, `NoRepeatBag`, `count_back_to_back`, `first_repeat`, `p_any_repeat` and `lines_needed`. A provided `compare` function measures back-to-back repeats for every rule.
- [`lab12-starter/test_variation.py`](lab12-starter/test_variation.py): the three deterministic rules, uniformity of random picks, bag blocks as permutations, zero back-to-back repeats for the no-repeat bag over 3,000 plays, the lecture's formula values (`0.52`, `0.496`, 97, 59 and 17 lines), and a simulation check that 100 plays of a 5-line bark give about 19.8 back-to-back repeats under random selection and about 3.8 under a shuffle bag.
- The gate scene from lecture sections 3 and 4, in both languages.
- Inky (inkle's free editor, github.com/inkle/inky) or Try Yarn Spinner (in the browser, linked from docs.yarnspinner.dev), or the Yarn Spinner extension for VS Code. You need one.
- The interactive `examples/w12-bark-repetition.html`, when it is built, for spot checks.

Run the tests from the repository root:

```
.venv/bin/python courses/GD202-narrative-and-quest-design/labs/lab12-starter/test_variation.py
```

On the starter every test reports `TODO` and the script exits with status 1. When all seven pass it prints `All tests pass.` Then run the comparison:

```
.venv/bin/python courses/GD202-narrative-and-quest-design/labs/lab12-starter/variation.py
```

## Steps

### Part A: the engine (50 min)

1. **Deterministic rules.** Write `Once` and `Cycle`, following `Stopping`. Match ink's `{!...}` and `{&...}`.
2. **Random rules.** Write `RandomPick` and `ShuffleBag`. Use only the `rng` you are given, never the global `random` functions, so a seed repeats a run.
3. **The fix.** Write `NoRepeatBag`. In a comment, explain why swapping the first line with a *random* other position is better than always swapping it with the second.
4. **Measure.** Write `count_back_to_back`, `first_repeat`, `p_any_repeat` and `lines_needed`. Run the tests until all pass.
5. **Compare.** Run `variation.py`. Copy its table into your report and put the lecture's expected value next to each measured number. Explain the `stopping` column in one sentence.

### Part B: the scene (40 min in lab, finish at home)

6. **Design first.** On paper, plan a gate guard the player meets many times over a quest chain. The guard needs:
   - an ambient greeting bark group of at least 5 variants, played from a bag;
   - an escalating line for repeat visits that uses stopping ("Back again?" then something warmer or ruder), at least 3 steps;
   - one condition on game state (a flag the game sets, such as a pass, a reputation or a quest stage);
   - one once-only option;
   - a way out of every branch (no loose ends).
7. **Write it.** Write the scene in ink or Yarn Spinner. Use the tool's own features for each item in step 6: ink's `{~...}`, `{...|...}`, conditional choices and `*`; or Yarn Spinner's `=>` line groups, `<<once>>` with `<<else>>`, `<<if>>` and `visited_count`. All lines must be your own writing.
8. **Play it.** Play through at least 12 visits in your editor, with the flag both off and on. Log the greeting variant you heard each visit.
9. **Check it against the model.** Count back-to-back repeats in your log. Compare with the expected number for your rule and `n` from the lecture. With only 12 visits, say whether the difference means anything.

### Part C: at home

10. **Port it.** Rewrite the same scene in the other tool. Note every construct that didn't translate directly and what you did instead.
11. **Budget.** Your guard's greeting fires about 150 times per play-through. Using your engine, decide how many variants the greeting needs, under which rule, for no more than 2 expected back-to-back repeats per play-through. Show the numbers.

## Deliverable

`variation.py` with all tests passing; your scene in both tools (`.ink` and `.yarn`); and a report of at most 600 words with the step 5 table, the step 3 comment, your visit log and the step 9 comparison, the step 10 porting notes, and the step 11 budget with arithmetic.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Engine correctness | All seven tests pass; measured table matches the lecture's expected values with a note on each | Six tests pass, or table without expected values | Fewer than six pass | 30% |
| Scene structure | All five required features present, each using the tool's own construct; no loose ends; plays with the flag on and off | One feature missing or faked by hand | Several missing, or the script doesn't run | 25% |
| Writing | Barks are short, distinct and in one voice; the stopping sequence escalates and pays off | Lines work but repeat ideas or drift in voice | Placeholder or copied lines | 15% |
| Porting | Every construct mapped, with the awkward ones explained | Port works, notes thin | Port missing or broken | 15% |
| Budget | Correct rule and `n` with arithmetic from the lecture's formulas | Right answer, reasoning incomplete | Missing or wrong | 15% |

<details>
<summary>Instructor check values</summary>

- `compare` with the provided seed prints about: n = 3, random 33.0, shuffle bag 11.0; n = 5, random 19.8, shuffle bag 3.9; n = 10, random 9.9, shuffle bag 0.9; no-repeat bag and cycle 0; stopping `100 − n`.
- Step 3: always swapping with the second position makes the old bag's last line predictable in second place, so the start of each bag is less random. A random swap target keeps every other order possible.
- Step 11, 150 plays: a shuffle bag gives `floor(149 / n) / n` expected back-to-back repeats. `n = 8` gives `18 / 8 = 2.25`, too many. `n = 9` gives `16 / 9 ≈ 1.78`, which meets the target. A no-repeat bag or cycle meets it with any `n ≥ 2`. Random selection needs `149 / n ≤ 2`, so `n ≥ 75`.

</details>
