# CS102 · Lab 05: The item database

**Week:** 5 ([Arrays vs linked lists vs hash maps](../lectures/w05-arrays-linked-lists-and-hash-maps.md))
**Time:** one 2-hour lab session plus up to 2 hours at home
**Work:** individually

## Objective

Replace a list-backed item database with a dictionary behind the same interface, prove with timings that lookups stop depending on the number of items, reproduce the GTA Online-style duplicate-check blow-up at load time, and turn the measurements into a frame-budget recommendation.

## Starter materials

- Python 3.10 or later, no packages. (In this repository, `.venv/bin/python`.)
- `labs/lab05-starter/item_db.py`, which contains:
  - `make_items(n)`: `n` synthetic item records `(id, name, price)` with shuffled ids.
  - `ListItemDB`: complete. `get` scans the list.
  - `DictItemDB`: `add` and `get` raise `NotImplementedError`. You write them.
  - `load_unique_list(records)`: complete, O(n²) duplicate rejection.
  - `load_unique_set(records)`: raises `NotImplementedError`. You write it.
  - `check()` and `bench()`. Run `python item_db.py --check` for correctness only, `python item_db.py` for both.
- Reference values from the lecture's machine: `c_scan ≈ 15 ns` per element (explicit loop), `c_hash ≈ 30 ns` per lookup, list lookup at 10,000 items ≈ 75 µs.
- The frame model from lecture: `T_list = q × c_scan × (n + 1) / 2`, `T_dict = q × c_hash`, `B = 16.67 ms`.

## Steps

### Part A: make it pass (25 minutes)

1. Implement `DictItemDB.add` and `DictItemDB.get`. `get` must return `None` for an unknown id, not raise.
2. Implement `load_unique_set`. It must return exactly the same list as `load_unique_list`, in the same order. (Keep the first copy of each id.)
3. Run `python item_db.py --check` until both lines say `OK`.

### Part B: measure (35 minutes)

4. Run `python item_db.py`. Copy the lookup table and the duplicate-check table into your report.
5. From your list column, compute your `c_scan` at `n = 10,000` (µs per lookup divided by 5,000.5). From your dict column, read `c_hash`.
6. Add a measurement for *missing* ids (ids that are not in the database) for both structures at `n = 10,000`. Predict the list cost from your `c_scan` first, then measure.
7. Add a row for `n = 50,000` to the lookup benchmark.

### Part C: the frame table (25 minutes)

8. Fill in this table from your measurements, with `q = 250` lookups per frame:

| n | list ms/frame | dict ms/frame | list % of 16.67 ms | fits? |
|---|---|---|---|---|
| 100 | | | | |
| 1,000 | | | | |
| 10,000 | | | | |
| 50,000 | | | | |
| 100,000 | | | | |

9. Compute the largest `n` for which the list keeps lookups under 25% of the frame at `q = 250`, using your `c_scan`.
10. Extrapolate your duplicate-check timings to 63,000 items using the O(n²) model. Compare with the set version extrapolated as O(n).

### Part D: recommendation (at home)

11. A designer plans 50,000 item definitions and a UI that resolves up to 400 item ids per frame. Write at most 300 words recommending a structure. Use at least three of your own numbers. Name one operation that the dictionary makes *worse* or does not help with, and say whether it matters for this UI.

## Deliverable

Your completed `item_db.py`, a report (text, Markdown or notebook) with the tables from steps 4, 6, 8 and 10, and the recommendation.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Correctness (20%) | `--check` passes; `get` returns `None` for unknown ids; set loader preserves order | Passes, one edge case untested | One check fails | Does not run |
| Measurement (25%) | Tables complete; `c_scan` and `c_hash` derived; missing-id prediction made first and compared | Tables complete, derivations thin | Missing the missing-id case or the 50,000 row | Missing |
| Frame analysis (25%) | Frame table correct; 25% limit computed; 63,000-item extrapolation for both loaders | Table correct, one derived value missing | Arithmetic errors | Missing |
| Recommendation (20%) | Clear choice, three or more own numbers, a named weakness of the dictionary and why it does or doesn't matter | Choice with numbers, weakness vague | Choice without numbers | Missing |
| Code quality (10%) | Same interface for both classes; no duplicated benchmark code | Minor duplication | Interface changed | Missing |
