# MMO302 · Lab 09: Login queue and session tickets

**Week:** 9 ([lecture](../lectures/w09-login-character-select-gateway-services.md))
**Time:** 2 hours in the lab, plus up to 2 hours to finish.
**Work mode:** pairs.
**Counts toward:** labs (40% of the course grade). The ticket service is reused as the login path of your final world server.

## Objective

Build the two halves of a login path. The first is a capped world with a login queue, a reconnect grace period and queue abandonment, checked against the lecture's `C / L` model. The second is a ticket service that issues signed, short-lived, single-use session tickets and rejects forged, expired, misdirected and replayed ones. Then use both to write a launch plan with numbers.

## Starter materials

- [`lab09-starter/login_service.py`](lab09-starter/login_service.py) is Python 3, standard library only. It provides these pieces:
  - A `World` class with `arrive`, `reconnect` and a `step` stub (TODO 1).
  - An `estimate_wait` stub (TODO 2).
  - A `TicketService` with a working `issue` and a `verify` stub (TODO 3).
  - An `evening` function that replays the lecture's section 2 evening through your `World`.
- [`lab09-starter/test_login_service.py`](lab09-starter/test_login_service.py) has seven tests. All fail on the starter and pass on a correct solution. Run them with `python -m unittest test_login_service.py` from inside `lab09-starter/`.
- The lecture's section 2 formulas and the `examples/w09-login-queue.html` interactive once it is built.

## Steps

### Part A: the queue (45 min)

1. Implement `World.step` (TODO 1). First, a fraction `1 / session_min` of online players logs out. Next, free slots go to `priority` (reconnecting players) first, then to the ordinary queue. Last, if `abandon_min` is set, a fraction `1 / abandon_min` of the ordinary queue gives up. Return the number admitted.
2. Implement `estimate_wait` (TODO 2) with the lecture's formula.
3. Run the four queue tests. `test_matches_lecture_evening` must reproduce the lecture's table exactly.
4. Add abandonment with a mean patience of 60 minutes to the lecture's evening. Record the peak queue, the time the queue empties and the total number of players who gave up. Write two sentences on why abandonment makes the queue look better and the launch worse.
5. Measure the real wait of a player who joins at minute 150 in the no-abandonment evening. Count the minutes until that many people ahead of them have been admitted. Compare it with `estimate_wait` at the moment they joined, and explain any difference.

### Part B: tickets (40 min)

6. Implement `TicketService.verify` (TODO 3). Check the field count (malformed), the signature with `hmac.compare_digest` (forged), the audience (wrong world), the expiry (expired), and single use (replayed). Remember accepted ticket IDs until they expire and forget expired ones.
7. Run all seven tests.
8. Write a short timing experiment. Verify 100,000 forged tickets whose tags share 0, 8, 16 and 31 leading characters with the correct tag, once with `==` and once with `compare_digest`, and report mean times. Say whether you can see the leak on your machine, and why the fix matters even if you cannot.

### Part C: the launch plan (35 min)

9. Use your `World` to simulate the lecture's in-class launch night (8 worlds of 4,000, `L = 150`, 60,000 arrivals between 20:00 and midnight, all worlds full at 20:00). Report each world's queue at midnight and the back-of-queue wait.
10. Add a crash of one world at 21:00. Its 4,000 players reconnect through `reconnect()` over a jitter window `J`. Assume the login tier admits at most 150 players per second across all worlds, including new arrivals. Find the smallest `J` that keeps the tier under capacity. Report how long the crashed world's players wait with and without the grace period.

## Deliverable

- Your completed `login_service.py` passing all seven tests, plus your code for steps 4, 5, 8, 9 and 10.
- A one-page launch plan for the in-class MMO. Give the cap per world, when to open layers, the jitter window, the grace period and what the queue screen shows players. Justify each value with a number from your simulations.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Queue model (Part A, steps 1 to 3) | All four queue tests pass; evening matches the lecture exactly | Tests pass with small numeric drift | Tests fail | 20 |
| Abandonment and real wait (steps 4 and 5) | Both measured, differences explained with the model | Measured, explanation vague | Missing | 15 |
| Ticket verifier (steps 6 and 7) | All ticket tests pass; replay memory is bounded | Tests pass, used IDs never forgotten | Tests fail | 25 |
| Timing experiment (step 8) | Clear method, results reported honestly, correct reasoning | Results without reasoning | Missing | 10 |
| Launch plan (Part C) | Every parameter backed by a simulation number; crash handled with jitter and grace period | Plan plausible but partly unsupported | Missing | 25 |
| Code quality | Readable, runs first time | Runs with minor fixes | Does not run | 5 |
| **Total** | | | | **100** |
