# MMO309 · Lab 04: The mailbox under fire

Assigned in week 4 ([lecture](../lectures/w04-duplication-exploits-and-transactional-design.md)). Due at the start of week 5. Part of the labs component (30% of the course).

## Objective

Take a small mail system that moves gold between players, find every failure point where an attacker who controls a crash or a lost reply can dupe or double-spend, and rebuild it so that no failure point is unsafe. Then add the conservation audit that would catch the dupe you missed.

## Starter materials

All in [`lab04-starter/`](lab04-starter/):

- `mailbox.py`, the file you edit. A SQLite schema (players, mail, ledger, and a `done` table for idempotency keys), two naive handlers, `send_mail` and `collect_mail`, and a stub `audit(db)`. Each handler calls `crash_point(crash_at, k)` at three marked moments so the checker can inject failures.
- `check_lab04.py`, the checker. For each handler and each failure point (0 = none, 1, 2, 3) it runs the handler, simulates the process dying by rolling back any open transaction, retries once with the same request ID, and checks that gold is conserved and that the send or collect happened exactly once. It also checks replays, overdrafts, double collection and the audit.
- `README.md`, how to run it.

You need Python 3.11 or later and nothing else. From the `lab04-starter` folder run `python check_lab04.py` (in this repository, `../../../../.venv/bin/python check_lab04.py`). On the starter code 8 of 15 checks pass and 7 fail. That is expected.

This lab is about defending your own server code. It contains no techniques for attacking a real game, and you must not try any of this against a live service.

## Steps

1. **Read and predict (15 min).** Before running anything, draw the failure-point table from the lecture for both naive handlers: for points 1, 2 and 3, write what the database holds after the failure and after the retry, and classify each row as correct, dupe, loss or double-execution.
2. **Run the checker (5 min).** Compare its output with your table. Explain in one sentence each any row you got wrong.
3. **Rewrite `send_mail` (30 min).** One transaction. Debit the sender with a conditional update that cannot go below zero, and check the row count. Store the reply in `done` under the request ID in the same transaction, and return the stored reply when a request ID comes back. Keep the three `crash_point` calls in order: after the first check, after the first write, and after `COMMIT`.
4. **Rewrite `collect_mail` (20 min).** Same pattern. Mark the mail collected with a conditional update (`... AND collected = 0`) so that two different requests cannot both collect it.
5. **Implement `audit(db)` (15 min).** Return `held` (purses plus uncollected mail), `created` (the ledger's grants) and `residual`. Run the checker until all 15 checks pass.
6. **Extend the inventory (at home).** Add one more value path of your choice: cash-on-delivery mail, returning expired mail to the sender, or a guild-bank deposit. Write it on top of the same transaction pattern and add at least three checks of your own to a copy of the checker, including one failure-point sweep. Say in your notes which invariant your new path could break and how the audit would see it.
7. **Attack your own code (at home).** List three ways a player could still abuse your system that the checker does not test (for example, keys kept too briefly, a sender who is also the recipient, or two servers sharing one database). For each, say whether the fix belongs in the handler, the schema or a rate limit.

## Deliverable

A zip or repository link containing:

- `mailbox.py` with both handlers rewritten, `audit` implemented and your step 6 path.
- Your extended checker, with its output pasted into `RESULTS.txt`. All 15 original checks must pass unchanged.
- `NOTES.md`, at most 400 words: your step 1 prediction table and the rows you got wrong; the failure-point table for your step 6 path; the three abuses from step 7 with where each fix belongs.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Correctness | All 15 provided checks pass without editing the checker | 12-14 pass | Fewer than 12 | 30% |
| Transaction design | Each handler is one transaction with a conditional write and an idempotency key written in the same commit; no stale values written back | One of the three elements missing in one handler | Separate commits or read-then-write of stale values remain | 25% |
| New value path | Built on the same pattern, three or more checks including a failure sweep, invariant named | Works, but checks miss the failure sweep | Missing or dupes under the checker | 20% |
| Prediction and analysis | Step 1 table complete, every mismatch explained in terms of commits and retries | Table complete, explanations thin | Missing | 15% |
| Abuse list | Three concrete abuses, each assigned to handler, schema or rate limit with a reason | Two, or reasons missing | None | 10% |
