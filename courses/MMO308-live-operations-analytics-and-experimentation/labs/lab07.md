# MMO308 · Lab 07: Segment the retention drop

**Week:** 7, segmentation ([lecture](../lectures/w07-segmentation.md)).
**Time:** 2 hours in the lab, plus up to 2 hours to finish.
**Work mode:** pairs.
**Counts toward:** analytics labs (40% of the course grade).

## Objective

A game went free to play between install week 0 and install week 1, and D7 retention of new accounts fell from 37.5% to 23.2%. Write the segment tools from the lecture, decompose the drop along two axes, and find the one real regression that the blended number and the obvious split both hide.

## Starter materials

All in [`lab07-starter/`](lab07-starter/). Standard-library Python.

- [`segments.py`](lab07-starter/segments.py): a CSV loader and stubs for `rate`, `segment_table`, `shares`, `overall`, `decompose` (three orderings) and `margin95`.
- [`new_players.csv`](lab07-starter/new_players.csv): 8,000 new accounts, one row each, with `player_id`, `install_week` (0 or 1), `account` (paid or free), `region` (NA, EU, ASIA) and `retained_d7` (0 or 1). The data is synthetic.
- [`test_segments.py`](lab07-starter/test_segments.py): seven tests built from the lecture's numbers and the CSV. Run it first from the repository root. All seven fail on the starter.

```
.venv/bin/python courses/MMO308-live-operations-analytics-and-experimentation/labs/lab07-starter/test_segments.py
```

- The segment-mix interactive, `examples/w07-segment-mix.html`, for checking two-segment cases.

## Steps

1. **Rates and tables.** Implement `rate`, `segment_table` (a single column name or a tuple of names), `shares` and `overall`. Confirm that `overall` of a segment table equals `rate` of the same rows.
2. **Decompose.** Implement `decompose` with the three orderings. The tests check the lecture's values (mix −0.175, rate +0.028 with old rates) and that mix plus rate equals the total change in every ordering.
3. **Margins.** Implement `margin95`. Run the tests until all seven pass.
4. **Axis one, account type.** Decompose the week 0 to week 1 change by account type. Report both orderings and the midpoint. Which effect dominates?
5. **Axis two, region.** Decompose by region instead. You should find a mix effect of zero. Explain in two sentences why a split by region blames the whole drop on "rates", and why that story is wrong.
6. **Both axes.** Build the table by `("account", "region")`, six cells per week. Add a margin of error to every cell. Find the cell whose rate fell. Is the fall itself measurable from week 0 to week 1, given that cell's week-0 size? If not, find a comparison inside week 1 that is measurable, and state it with margins.
7. **Size the regression.** Compute that cell's contribution to the rate effect, `w1 × (m1 − m0)`, and the number of week-1 players it cost if the cell had matched the other free cells in week 1.

## Deliverable

Your completed `segments.py` with all tests passing, and a memo of at most 300 words to the live-ops producer. It must say how much of the 14.3-point drop is mix and how much is rate (with the ordering named), which segment regressed, how confident you are and why, and one next action.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Code correctness | All seven tests pass; code is readable and handles tuple keys | Tests pass with hard-coded cases | Tests fail | 30% |
| Decomposition | Both axes and all orderings reported correctly, and the region result explained | One axis or ordering missing | Mix and rate confused | 25% |
| Hidden regression | Cell found, margins used to judge what is measurable, contribution sized in players | Cell found without margins | Not found | 25% |
| Memo | Plain, numeric, one clear next action, within 300 words | Correct but vague or long | Hard to act on | 20% |
