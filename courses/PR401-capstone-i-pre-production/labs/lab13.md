# PR401 Lab 13: Stability evidence for the review build

**Week:** 13 (Vertical slice sprint 2). **Guide:** [week 13](../lectures/w13-vertical-slice-sprint-2.md). **Team lab**, submitted once per team.

## Objective

Show, with numbers, how likely your review build is to survive the week 14 demo. You will log every playtest and soak on the build, count client and server exposure separately, compute 95% upper bounds on both crash rates, and collect enough evidence (or make failures cheap enough) to meet a target the team sets in advance.

## Starter materials

In [`labs/lab13-starter/`](lab13-starter/):

- `stability.py`. Standard library only. Run it with `.venv/bin/python stability.py sessions.csv review.csv`. It counts exposure on the review build only, prints point estimates, exact 95% upper bounds and the pessimistic chance of a clean demo, then `PASS` or `NOT READY`, and exits with code 1 when anything fails.
- `sessions.csv`. The four *Emberfall* sprint 1 playtests from the guide, on build `slice-0.1`.
- `review.csv`. Demo settings: build tag, 8 demo players, 30 minutes, target 0.9, reconnect not tested, longest expected PR402 session 3 hours.

Rules the checker applies. Client exposure is player-hours from playtests only, because headless bots skip the client code where most client crashes happen. Server exposure is hours from any session whose steady concurrency (`min_concurrent`) is at least the demo player count. The build **passes** when the server's pessimistic survival chance meets the target, the client's does too or a reconnect test is recorded, and at least one soak on the review build lasts as long as the longest expected PR402 session.

## Steps

1. **Warm-up (10 minutes).** Run the checker on the starter files and confirm the guide's numbers: client upper bound 0.175, server upper bound about 1.0, pessimistic clean demo 0.30. Note the server-hours the checker says you need.
2. **Set the target first.** In `review.csv`, set your demo player count and length from the review format, and a target agreed by the team before you look at your own data. Write one sentence in `stability.md` on why you chose it.
3. **Log sprint 1.** Enter every slice sprint 1 playtest in `sessions.csv`, with the build tag it ran on. Use the lowest steady concurrency for `min_concurrent`, ignoring the first and last five minutes of a session.
4. **Plan the evidence.** From the checker's output, decide how many server-hours at load you need and how you will get them (bots from MMO302 week 11, class soak). Decide whether client crashes will be made rare (more player-hours) or cheap (reconnect with state restored). Put the plan in `stability.md`.
5. **Collect on the review build.** Run the soaks and playtests on the tagged build. Log every session, including ones that crashed early. If you fix a crash, tag a new build and start counting again.
6. **Reconnect test.** If you chose "cheap", record a test in which a client is killed mid-quest and reconnects with position, inventory and quest state restored. Attach the capture and set `reconnect_tested` to `yes`.
7. **Run the checker** until it prints `PASS`, or until the review. If you can't reach `PASS`, the stability statement says so and the demo script plans around it (a recorded run as primary, for example).

## Deliverable

In `preproduction/week13/` in the team repository:

- `sessions.csv`, `review.csv`, and the checker output as `check-output.txt`.
- `stability.md`: the target and its reason, the evidence plan, the reconnect test (if used), and the stability statement table for the review.

**Checkable output:** the instructor reruns `stability.py` on your two CSV files. It must print `PASS` and exit with code 0, or print `NOT READY` with a `stability.md` that states the shortfall and the demo plan that allows for it. The output must match `check-output.txt`.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Checker result | 5 | `PASS` on rerun; or an honest `NOT READY` with the shortfall and a matching demo plan |
| Exposure logged correctly | 4 | Every session on its real build tag; `min_concurrent` from the steady part of the session; nothing omitted |
| Target set in advance | 2 | Target and reason written before the review-build data |
| Evidence plan | 4 | Server-hours needed computed and obtained by a named method; rare-or-cheap decision for the client made and justified |
| Reconnect test | 2 | Captured and state restoration shown, or not claimed |
| Long soak | 3 | At least one soak on the review build at least as long as the longest expected PR402 session, with its result |
