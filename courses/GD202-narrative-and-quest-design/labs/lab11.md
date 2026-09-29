# GD202 · Lab 11: Localization linter

**Week:** 11, writing for localization ([lecture](../lectures/w11-writing-for-localization.md)).
**Time:** 2 hours in lab, plus about 2 hours at home.
**Weight:** part of the dialogue exercises (40%). Keep the linter; week 14 (narrative testing) reuses it.

## Objective

Build a linter that catches the three localization bugs from the lecture before strings reach translators: missing plural forms, UI strings with no room to grow, and sentence fragments meant for concatenation. Run it on an invented quest's 30 strings, find what it misses, and fix the file by hand.

## Starter materials

All in [`lab11-starter/`](lab11-starter/). Standard-library Python, run with `.venv/bin/python`.

- [`loc_lint.py`](lab11-starter/loc_lint.py) has six empty functions (`plural_category`, `forms_needed`, `missing_forms`, `two_slot_errors`, `budget`, `is_fragment`) and a provided `lint` that combines them into a report. The file format is described at the top.
- [`test_loc_lint.py`](lab11-starter/test_loc_lint.py) holds the lecture's values: the plural table for six languages, French `many` at a million, the two-slot error counts (Russian 35, Polish 27, Arabic 11 of the counts 0 to 100), the width budgets from section 3, and fragment examples.
- [`quest_strings.json`](lab11-starter/quest_strings.json) holds the 30 strings of an invented quest, "The Ferryman's Debt", as a hurried team wrote them: UI labels with widths, dialogue, system messages built from fragments, and three counted strings with incomplete plural forms. Non-English forms are placeholders such as `(ru few)`, since you are checking structure, not translating.
- The interactive [`examples/w11-plural-rules.html`](../examples/w11-plural-rules.html) for spot checks of plural categories.

Run the tests from the repository root:

```
.venv/bin/python courses/GD202-narrative-and-quest-design/labs/lab11-starter/test_loc_lint.py
```

On the starter every test reports `TODO` and the script exits with status 1. When all seven pass it prints `All tests pass.` Then lint the quest:

```
.venv/bin/python courses/GD202-narrative-and-quest-design/labs/lab11-starter/loc_lint.py quest_strings.json
```

## Steps

### Part A: the linter (50 min)

1. **Plural rules.** Implement `plural_category` from the lecture's table. Check French 0, Russian 21, Polish 21 and Arabic 101 by hand before you run the tests.
2. **Forms.** Implement `forms_needed` and `missing_forms`. A language that has no entry in `forms` is missing everything it needs.
3. **Two slots.** Implement `two_slot_errors`. Before running it, predict the Russian number from the lecture and explain it in one sentence.
4. **Width.** Implement `budget`. Note in your report which bands make a shorter string get a larger budget than a longer one.
5. **Fragments.** Implement `is_fragment`. Run all tests until they pass.

### Part B: the quest file (40 min)

6. **Lint.** Run the linter on `quest_strings.json`. Save the output.
7. **What it misses.** Read all 30 strings yourself. List every string that will cause a localization bug but that the linter does not flag, and name the bug. There are at least four. (Hint: look at item names that exist in a singular and a plural version, and at strings that only make sense glued to others.)
8. **Fix the file.** Make a copy, `quest_strings_fixed.json`, and fix every problem from steps 6 and 7:
   - Replace every group of fragments with one whole-sentence string with named placeholders (for example `"You found {item} in {place}."`), and delete the fragments.
   - Give every counted string the plural forms each of the six languages needs, as placeholders like `(ar few)`. Set `count_max` honestly for how the game uses the string.
   - For each UI overflow, either shorten the English (and say what meaning you lost) or widen the field. Record which you chose.
   - Write a context note for every string that lacks one, at most 12 words each.
9. **Clean run.** Rerun the linter on the fixed file until it reports 0 problems.

### Part C: at home

10. **Add a rule.** Add one new check to `lint` for a bug from lecture sections 4 or 5 that the linter doesn't catch yet (for example, a placeholder in a string with no note saying what fills it, or a string whose note mentions a pun without saying its intent). Write a test for it in a new file `test_my_rule.py`, and show it failing on a bad string and passing on a good one.
11. **Pseudo-localize.** Write a short function that turns an English string into a pseudo-localized one: pad it to its `budget` with a visible marker and swap `a e i o u` for accented look-alikes, leaving `{placeholders}` untouched. Print the pseudo-localized fixed file and paste three lines into your report.

## Deliverable

`loc_lint.py` with all tests passing, `quest_strings_fixed.json` linting clean, `test_my_rule.py`, and a report of at most 600 words with:

- the linter output before and after;
- your list of missed bugs from step 7, each with the string ID and the rule it breaks;
- your width decisions from step 8;
- the new rule from step 10, and why a linter can or can't catch that bug reliably;
- three pseudo-localized lines from step 11.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Linter correctness | All seven tests pass; predictions in steps 1 and 3 written before running | Six tests pass | Fewer than six pass | 30% |
| Missed bugs | At least four correct misses, each with the rule named | Two or three correct misses | One or none, or rules misnamed | 20% |
| Fixed file | Lints clean; every fragment group merged into whole sentences with named placeholders; plural forms complete and `count_max` justified | Lints clean but one merge keeps a fragment or one `count_max` is unjustified | Problems remain | 25% |
| Notes and width decisions | Every note says what the string is, who says it or where it shows, in 12 words or fewer; width trade-offs stated | Notes present but vague | Notes missing | 15% |
| New rule | Rule, test and an honest limit of what it catches | Rule without a test, or no discussion of limits | Missing | 10% |

<details>
<summary>Instructor check values</summary>

- Linter output on the starter file once the functions are correct: 30 strings, 21 problems (fragment 5, note 3, plural 7, width 6).
- Width: `BTN_ACCEPT` 18 over 16, `BTN_ABANDON` 26 over 24, `BTN_CLOSE` 15 over 12, `LOCATION_JETTY` 22 over 18, `LOCATION_GREYWOOD` 24 over 18, `ERR_BAGS_FULL` 36 over 24.
- Plural: `TRACK_PELTS` (ru few; ar zero, two, few), `KILLS_WOLVES` (fr, ru, pl, ar missing everything they need), `GOLD_REWARD` (ar other, since counts reach 100).
- Misses the linter can't see: `ITEM_PELT` and `ITEM_PELT_PL` (an English-style two-form plural split across two strings), `PLACE_MILL` (a noun fragment meant for concatenation after "in the"), `ITEM_PELT` again as a concatenation piece in the FOUND message, and `OBJ_3` (no end punctuation, no note, and a verb that could be read as a statement or an order). Accept any well-argued fourth.
- Budget quirk: a 10-character string gets 30 characters, an 11-character string 22.

</details>
