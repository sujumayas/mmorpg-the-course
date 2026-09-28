# CS202 · Lab 04: Policing movement

**Week:** 4 · **Time:** 2 hours in lab plus about 2 hours at home · **Weight:** part of the labs (40%)

## Objective

Build the two movement checks from the [week 4 lecture](../lectures/w04-server-authority-never-trust-the-client.md), reproduce its table, and choose a budget for a real connection you measured. Then rewrite a badly designed protocol so the client sends only intent. You finish able to say, with a number, what any server check gives away to a cheater and what it costs an honest player.

## Starter materials

Folder [`lab04-starter/`](lab04-starter/README.md). Standard library Python only. Use the course interpreter (`.venv/bin/python` at the repository root) or any Python 3.10 or later.

- `movement_check.py`: the arrival model and report code are written. You write `min_tolerance`, `speed_check`, `tick_budget` and `min_budget`.
- Your Lab 02 latency log (`sample_run.csv` from [Lab 02's starter](lab02-starter/README.md) if you do not have your own).

## Steps

1. **Policy A.** Implement `min_tolerance` and `speed_check` following their docstrings. Keep the `1e-9` in the comparison and explain in one sentence why it is there.
2. **Policy B.** Implement `tick_budget` in the order the docstring gives (queue, credit, run, drop), then `min_budget`. Run `python movement_check.py --check` until it prints `all checks passed`.
3. **Reproduce the lecture.** Run `python movement_check.py --table` and confirm it matches the table in section 2. Check the 30 ms row by hand, both `tol_min` and `B_min`, and show the working.
4. **Break the order.** Swap steps 2 and 3 inside `tick_budget` (run commands before adding the tick's credit) and rerun `--table`. Only one cell of the table changes. Find it, and explain why the ordering can shift a result by at most one command per burst. Then say which order your specification should require and put it back.
5. **Your jitter.** From your Lab 02 log, take the 99th-percentile RTT minus the median RTT, halve it as an estimate of one-way jitter, and round up to a whole millisecond. Run `python movement_check.py --jitter <yours>`. Report `tol_min`, `B_min`, the policy A cheater's lead and the policy B cheater's lead.
6. **Lag switch.** Add a function `lag_switch(budget, hold)` that holds `hold` consecutive packets starting at packet 40 and releases them with the next one, then returns the largest number of commands run in one tick and the number dropped. Reproduce the lecture's rows for `B = 5` and `B = 24` with `hold = 6`. Then find the largest `B` for which the jump stays under 1 m, and say how much jitter that `B` forgives.
7. **Protocol audit.** Take this message list from a fictional prototype: `SET_POSITION x y z`, `SET_ROTATION yaw`, `DEAL_DAMAGE target_id amount`, `LOOT item_id`, `SELL item_id count price`, `SET_HEALTH hp`, `CHAT text`, `OPEN_DOOR door_id`. For each, describe one exploit in one line, rewrite it as intent (or delete it), and fill in the range, rate, state, ownership and reach checks from section 3 of the lecture.

## Deliverable

Your finished `movement_check.py` including `lag_switch`, and one Markdown or PDF file with the step 1 sentence, the outputs from steps 3, 5 and 6, the hand check from step 3, the explanation from step 4, and the step 7 audit as a table. Submit before next week's lecture.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Policies A and B | `--check` passes; `tick_budget` follows the stated order; step 4 explained with the tick that changes | Passes, but the order experiment is missing or vague | Fails the check | 25% |
| Reproduction and hand check | Table matches; both 30 ms values derived by hand with the formulas | Table matches, hand check partial | Table does not match | 15% |
| Your jitter (step 5) | Jitter derived from a real log with the method shown; all four numbers reported and interpreted | Numbers reported without derivation | Missing | 15% |
| Lag switch | Function reproduces both rows; largest `B` under 1 m found by code and translated into forgiven jitter | Rows reproduced, limit guessed | Missing | 20% |
| Protocol audit | Every message has a plausible exploit, an intent rewrite and all five checks; at least one message correctly deleted | Most messages covered, checks thin | Rewrites still trust client results | 25% |
