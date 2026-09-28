# CS101 · Lab 06: The item database

**Week:** 6, dictionaries ([lecture](../lectures/w06-dictionaries-item-databases.md)).
**Time:** 2 hours in lab, plus up to 2 hours at home.
**Weight:** part of the weekly exercises (40%). The item keys you choose here are the ones your later games use.

## Objective

Load an item database from JSON into a dictionary of dictionaries, write functions that validate and query it, fix the data errors your validator finds, and migrate a "version 1" save file that stored items as list positions to "version 2" string keys.

## Starter materials

All in [`lab06-starter/`](lab06-starter/). Standard-library Python 3.10 or later. Run everything from inside that folder, because the tests open the JSON files by relative path.

- [`itemdb.py`](lab06-starter/itemdb.py) with `load_json` done for you and five empty functions: `validate`, `find` (with an alias table for renamed items), `items_of_type`, `total_value` and `migrate_save`. Each docstring is the spec.
- [`items.json`](lab06-starter/items.json), eight items with three deliberate data errors. You will fix this file.
- [`items_original.json`](lab06-starter/items_original.json), an untouched copy the tests use to check that your validator finds the errors. Do not edit it.
- [`ids_v1.json`](lab06-starter/ids_v1.json), the version 1 item list, where an item's ID was `256 + index`, the same scheme as the lecture's section 2 table.
- [`save_v1.json`](lab06-starter/save_v1.json), a version 1 save with numeric IDs in its slots.
- [`test_lab06.py`](lab06-starter/test_lab06.py), seven tests. The starter reports `0/7 tests passed`.

## Steps

1. **Explore.** In a Python shell, `import itemdb`, then `db = itemdb.load_json("items.json")`. Print `db["potion"]`, `db["potion"]["heal"]` and `list(db)`. Write down the type of each result.
2. **`validate`.** Implement the three checks from lecture section 3. Each problem string must start with the item key and a colon, because the test groups problems by key. Run the tests: `test_validate_finds_the_three_errors` should pass and name three items.
3. **Fix the data.** Edit `items.json` (not the original) so `test_your_items_json_is_fixed` passes. Choose sensible values and write one sentence per fix explaining your number. Use the prices of neighbouring items as a guide (GD203 week 9, in year 2, covers the design reasoning).
4. **Queries.** Implement `find`, `items_of_type` and `total_value`. `find` follows `ALIASES` so an old save that says `"short_sword"` still works, and raises `KeyError` for keys that don't exist. Don't use `.get` to hide the error.
5. **Migrate.** Implement `migrate_save`. Return a new dictionary; the test checks that the old one is unchanged. Then write a five-line script that loads `save_v1.json`, migrates it, and writes `save_v2.json` with `json.dump(..., indent=2)`. Open the output and check that every slot reads as a word.
6. **Break it on purpose.** Insert `"bronze_sword"` at index 1 of a copy of `ids_v1.json` and migrate the old save with that list instead. Record which slots now hold the wrong item. That is the lecture's stability table, produced by your own code.
7. **Stretch.** Add a `"version"` check: `migrate_save` should return a version 2 save unchanged, and raise `ValueError` for an unknown version. Write the tests first.

## Deliverable

`itemdb.py` with `python test_lab06.py` reporting `7/7 tests passed`, your fixed `items.json`, `save_v2.json`, and a note of at most 250 words with your three data fixes and the result of step 6.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Tests pass | 7/7 | 5-6 | 4 or fewer | 35% |
| Data fixes | All three fixed with values justified against neighbouring items | Fixed, values arbitrary | Not fixed, or validator weakened to pass | 15% |
| Migration | New dict returned, old unchanged, `save_v2.json` written and readable | Works but mutates the input or skips the file | Missing | 20% |
| Step 6 analysis | Names each wrong slot and ties it to position-based IDs | Observes breakage without explaining | Missing | 20% |
| Use of `.get` and `KeyError` | `.get` only for optional fields; missing required keys fail loudly | Some over-use of `.get` | Errors hidden everywhere | 10% |
