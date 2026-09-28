# MMO302 · Lab 08: A dupe-proof item service

**Week:** 8 ([lecture](../lectures/w08-item-ownership-and-transactional-integrity.md))
**Time:** 2 hours in the lab, plus up to 3 hours to finish.
**Work mode:** pairs.
**Counts toward:** labs (40% of the course grade). The transfer and audit functions become part of your final world server.

## Objective

Reproduce a gold duplication bug with an injected crash. Then rewrite the transfer so that it is atomic and idempotent and move items with a conditional ownership update. Finally, prove with a conservation audit that 10,000 randomized operations with crashes and client retries leave exactly zero drift.

## Starter materials

- [`lab08-starter/item_service.py`](lab08-starter/item_service.py) is Python 3, standard library only, with SQLite standing in for PostgreSQL. It provides these pieces:
  - The schema, with `wallet` (with `CHECK (gold >= 0)`), `item` (one row per item, one `owner` column), `ledger` (mint and destroy rows) and `applied_op` (operation IDs).
  - `open_world()`, which creates four players with 1,000 gold and 5 items each, all minted in the ledger.
  - The shipped `transfer_gold_buggy`, which gives first and takes second in two separate writes.
  - `stress()`, which runs 10,000 random transfers. 1% crash between the two writes and 2% lose their reply after success. Every crash and lost reply is followed by a client retry with the same operation ID.
  - Three `TODO` stubs: `transfer_gold`, `move_item` and `audit`.
- [`lab08-starter/test_item_service.py`](lab08-starter/test_item_service.py) has seven tests. All fail on the starter and pass on a correct solution. Run them with `python -m unittest test_item_service.py` from inside `lab08-starter/`.
- Running `python item_service.py` prints the audit for the buggy transfer and for yours once the stubs are filled in.
- The lecture's section 3 code, which you may adapt.

## Steps

### Part A: see the dupe (25 min)

1. Implement `audit` (TODO 3). Gold drift is the sum of all wallets minus (minted minus destroyed). Also return the number of item rows.
2. Run `python item_service.py`. The buggy line shows positive drift. Using the stress parameters (10,000 operations, 1% crashes, average transfer about 25 gold), predict the drift from the lecture's model before you read the number. Explain any gap.
3. In two sentences, say why the 2% of lost replies add no drift to the buggy version, and what they do instead. (Hint: who pays for a transfer that runs twice?)

### Part B: fix it (50 min)

4. Implement `transfer_gold` (TODO 1). Use one transaction. Insert the operation ID first, and if it is already present, return the stored result with " (replayed)". Take from the source, then give to the destination. If the `CHECK` constraint refuses an overdraft, roll back and record "insufficient" under the operation ID. When `crash=True`, raise `Crash` between the two updates after rolling back.
5. Implement `move_item` (TODO 2) with the same operation-ID pattern and a conditional update, `WHERE item_id = ? AND owner = ?`. Return "not owner" when it updates no rows.
6. Run all seven tests.

### Part C: stress and port (35 min)

7. Run `stress(transfer_gold)` for crash rates of 0.001, 0.01, 0.1 and 0.5. Record drift, which must be zero every time, and the run time. How much slower is the safe version than the buggy one?
8. Rewrite `transfer_gold` in PostgreSQL syntax on paper or in a file (it does not need to run). Use `INSERT ... ON CONFLICT (op_id) DO NOTHING RETURNING op_id` in place of catching the integrity error. Say what happens in your version if two retries with the same operation ID arrive at the same instant on two connections.
9. Add a `mail` table and a `claim_mail` function to your copy. Extend `audit` so unclaimed mail gold counts as supply. Show that the audit still reads zero after a mix of transfers and claims.

## Deliverable

- Your completed `item_service.py` passing all seven tests, with the Part C step 9 extension.
- The audit output for the buggy and fixed versions, and the Part C table.
- The PostgreSQL version of `transfer_gold` from step 8.
- A 250-word incident report on the original bug, written as if for your studio's live-ops team. Cover what players could do, how the audit detected it, the size of the drift for a shard doing 2 million transfers a day at the observed crash rate, and the fix.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Audit and reproduction (Part A) | Audit correct; predicted drift within 15% of measured; lost-reply behaviour explained | Audit correct, prediction missing or unexplained | Audit wrong | 15 |
| Atomic, idempotent transfer | All transfer tests pass; replay returns the stored result, including "insufficient" | Tests pass but replays re-execute, or overdraft handled outside the database | Tests fail | 25 |
| Conditional item move | Test passes; the ownership check is inside the update, not a prior `SELECT` | Works with a separate check | Missing | 15 |
| Stress and port (Part C) | Zero drift at all rates; PostgreSQL version correct with a clear answer on concurrent retries; mail extension audited | Two of the three | One or none | 25 |
| Incident report | Clear, numeric, blameless, names the fix and a monitoring change | Accurate but vague on numbers | Missing | 15 |
| Code quality | Readable, runs first time | Runs with minor fixes | Does not run | 5 |
| **Total** | | | | **100** |
