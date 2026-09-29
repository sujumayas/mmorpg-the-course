# MMO404 · Lab 11: Physics budget

**Week:** 11 · **Time:** 2 hours in lab plus about 3 hours at home · **Weight:** part of the labs (40%)

## Objective

Make the [week 11 lecture](../lectures/w11-physics-in-mmos.md) model something you can measure. You implement Box2D's sleep rule in a small live world, derive how long a kicked body stays awake, and check the awake count against Little's law and its exact form. Then you find physics islands with union-find, assign them to servers across a seam, and write a physics budget for a siege mode that states what the server simulates, what clients simulate and what nobody simulates.

## Starter materials

Folder [`lab11-starter/`](lab11-starter/README.md). Standard library Python only. Run with `.venv/bin/python` from the repository root or any Python 3.10+.

- `physics_budget.py`: constants from the lecture (`F = 30`, `C_B = 4 µs`, Box2D's `LIN_TOL = 0.01 m/s` and `T_SLEEP = 0.5 s`, a damping of 2 per second), a live world `run_world` that kicks random bodies and lets them slow down and sleep (given), and TODOs for `update_sleep_time`, `island_should_sleep`, `t_move_for`, `awake_little`, `awake_exact`, `cpu_ms_per_s`, `islands` and `island_owner`. It has `--check`, `--measure` and `--sweep` modes.

## Steps

1. **By hand first.** A body is kicked to 2 m/s and its speed decays as `v0 × e^(−2t)`. Derive, before coding, how long it takes to fall below 0.01 m/s, and so its `τ` with a 0.5 s sleep timer. Then compute Little's law and the exact form for 2,000 bodies at 200 kicks per second.
2. **The sleep rule.** Implement `update_sleep_time`, `island_should_sleep` and `t_move_for`. Read `run_world` and explain in two sentences where your functions are called and what would happen to the awake count if `island_should_sleep` used the maximum sleep time instead of the minimum for a real island.
3. **The model.** Implement `awake_little`, `awake_exact` and `cpu_ms_per_s`. Run `--check` until it stops at `islands`. Then run `--measure` and report the table. At which kick rate does Little's law stop being a good estimate, and why?
4. **Islands.** Implement `islands` with union-find and path halving, and `island_owner` with the majority rule and a fixed tie-break. `--check` includes a chain of 1,000 bodies, so a recursive `root` may fail. Run `--check` until it prints `all checks passed`.
5. **The sleep timer as a budget knob.** Run `--sweep budget.csv` with `T_SLEEP` at 0.5 s, then again at 2.0 s (change the constant). Plot CPU against kick rate for both on one chart with the 200 ms/s budget line. Report the largest kick rate each setting can afford.
6. **A seam scenario.** Write a short script that builds 30 crates in five stacks of six along a seam at `x = 0`, with crate `x` positions from `random.Random(4)` in the range −3 to +3 m per stack, contacts between neighbours in each stack, and owners by the sign of `x`. Print each island, its votes and its owner, and count how many crates must be handed off. Then join two stacks with one extra contact and report what changes.
7. **Your siege budget.** A siege zone has 12,000 props and 300 breakable wall segments of 8 pieces each. At peak, 6 catapult shots per second each wake 35 props and break one segment. Write a one-page budget: `δ`, `τ`, `N_awake` (both forms) and CPU for the server if it simulates everything; then choose an owner for each kind of body (server, predicted, client-only cosmetic) and recompute the server's cost. State the step rate you choose, the sleep timer, and one cheat or visual artifact your choice allows.

## Deliverable

Your finished `physics_budget.py`, both `budget.csv` files with the chart from step 5, the seam script from step 6, and a report (PDF or Markdown, at most three pages) with the derivation from step 1, the answers to steps 2 and 3, the affordable kick rates from step 5, the island output from step 6 and the budget from step 7. Submit before the week 12 lecture.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Sleep rule | `--check` passes; `t_move` derived by hand and matches the code (2.649 s) | Passes, derivation missing | Fails the check | 15% |
| Budget model | Measure table reported; the gap between Little's law and the exact form explained by repeat pushes on awake bodies | Table reported, explanation vague | Fails the check | 20% |
| Islands | Union-find with path halving passes the 1,000-body chain; tie-break is deterministic | Passes with a recursive or quadratic method | Fails the check | 15% |
| Sleep timer analysis | Chart with both settings and budget line; affordable kick rates stated with units | Chart present, rates missing | Step skipped | 15% |
| Seam scenario | Islands, votes, owners and handoff count printed; the joined-stacks change explained | Output present, explanation thin | Missing | 10% |
| Siege budget | Numbers for both forms and both ownership plans; step rate and sleep timer justified; one cheat or artifact named | Numbers present, choices unjustified | Budget missing or copied from the lecture | 20% |
| Writing | Plain, one idea per paragraph, units everywhere | Mostly clear | Hard to follow | 5% |
