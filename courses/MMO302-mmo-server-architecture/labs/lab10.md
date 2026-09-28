# MMO302 · Lab 10: Chat router under load

**Week:** 10 ([lecture](../lectures/w10-chat-guild-and-social-services.md))
**Time:** 2 hours in the lab, plus up to 3 hours to finish.
**Work mode:** pairs.
**Counts toward:** labs (40% of the course grade). The router's counters come back in week 14, when you export them as metrics.

## Objective

Build a chat router that counts its own fan-out, confirm that its load matches the lecture's model `D = q × L × (L − 1)`, and use it to choose a channel design for a realm with a stated player count.

## Starter materials

- [`lab10-starter/chat_router.py`](lab10-starter/chat_router.py) is Python 3, standard library only. It has a `TokenBucket` class, a `Router` with `subscribe`, `unsubscribe` and `publish`, a `shard_name` helper for splitting a channel, a `simulate` function for one busy channel, and the lecture's `predicted_deliveries` formula. Four function bodies are marked TODO. Running the file prints "not run yet" until `simulate` works.
- [`lab10-starter/test_chat_router.py`](lab10-starter/test_chat_router.py) has nine `unittest` tests. All nine fail on the starter. Run them with `python -m unittest test_chat_router.py` from inside the folder.
- The lecture's fan-out table and token-bucket trace, which are your reference numbers.

## Steps

### Part A: build and verify (50 min)

1. Implement `TokenBucket.allow`. The test `test_lecture_sequence` uses the lecture's trace, so if it passes your bucket matches the lecture.
2. Implement `Router.publish` using the three rules in its docstring. The sender never receives a copy of their own message.
3. Implement `shard_name` with `zlib.crc32`, so a member lands in the same sub-channel after a restart. (Python's built-in `hash` of a string changes between runs. Try it and see.)
4. Implement `simulate`. Generate every member's Poisson post times first, sort all posts by time, then publish them in order.
5. Run `python chat_router.py`. For `L` = 400, 1,000 and 3,000 your simulated copies per second should be within 10% of the model. Record both numbers in a table. Run all nine tests and paste the result into your report.

### Part B: levers (45 min)

6. **Split.** For `L = 3,000`, run `k` = 1, 2, 4, 10 and 30. Plot copies per second against `k` with the model's `q × L × (L/k − 1)` on the same chart.
7. **Spam.** Add an optional `spammers` argument to `simulate`. It adds that many extra members, each posting every 1.0 s on a fixed schedule. With `L = 1,000`, add 10 spammers. Run once with `limit=False` and once with the default bucket (burst 3, one per 5 s). Report copies per second, the share of spammer messages dropped, and the share of normal messages dropped. The normal share should be 0. If it is not, explain which rule caught ordinary players.
8. **Rate by scope.** Change the router so a channel's refill rate depends on its size: `rate = min(1.0, 50 / members)` per second. Explain in two sentences why a raid channel and a realm channel should not share one limit, using copies per post.

### Part C: presence batching (25 min)

9. Write `presence_packets(members, window_s, batch_s)` that returns the push count and the batched count for a guild logging in evenly over the window, using the lecture's rules (section 3). Check that `presence_packets(1000, 600, 5)` returns `(499500, 59540)`.
10. Plot the batched count for batch periods of 1, 2, 5, 10 and 30 seconds. Mark the period you would ship and give the player-facing cost in one sentence.

## Deliverable

- Your finished `chat_router.py` and tests, runnable from a clean folder, with a README of up to 10 lines.
- A report of up to 3 pages (PDF): the Part A table and test output, the Part B split chart and spam results, the Part C chart, and a one-page channel design for the lecture's in-class realm (12,000 players, 4 capitals, 40 zones, `q = 0.001`). The design lists each public channel, its scope, expected `L`, copies per second from your simulator, the rate limit, and the delivery guarantee from the lecture's section 4 table.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Router correctness (Part A) | All nine tests pass; simulated load within 10% of the model at all three sizes | Tests pass but the model comparison is missing or off by more than 10% without a diagnosis | Tests fail | 30 |
| Levers (Part B) | Split chart matches the model; spam run shows drops only for spammers; scope-based rate argued with copies per post | Two of the three parts done well | Missing | 25 |
| Presence (Part C) | Function returns the lecture's numbers; chart and shipping choice with a stated player cost | Function correct, choice not argued | Missing | 15 |
| Channel design | Every public channel has scope, `L`, measured copies, limit and guarantee; totals fit a stated core budget | Design plausible but numbers not from the simulator | Missing | 20 |
| Code quality and README | Readable, runs first time, parameters in one place | Runs with minor fixes | Does not run | 10 |
| **Total** | | | | **100** |
