# MMO302 · Lab 13: An autoscaler for a zone-server fleet

**Assigned:** week 13 ([lecture](../lectures/w13-cloud-deployment-and-autoscaling.md)). **Due:** start of week 14 class. **Feeds:** the final server's deployment plan (week 15).

## Objective

Write the scaling policy for a fleet of stateful zone servers and prove, with a simulator, that it meets a queue target on launch night and a cost target over a normal day, without ever shutting down a server that still has players on it. By the end you should be able to defend each number in your policy (target utilization, ramp window, scale-in wait) with the headroom rule `N = (D + r × L) / c` from the lecture.

## Starter materials

The folder [`lab13-starter/`](lab13-starter/) contains:

- [`fleet.py`](lab13-starter/fleet.py), the simulator. Do not edit it. It steps one minute at a time with `CAP = 500` players per server, `LAG = 8` minutes from launch to ready, and logouts drawn from a 90-minute mean session. It provides three demand traces: `evening_trace()` (12,000 rising to 40,000 over 200 minutes), `launch_trace()` (20,000 then +3,000 per minute for 20 minutes) and `daily_trace()` (the weekday curve from lecture section 4, 1,440 minutes). Terminating a server that holds players raises `PlayersKicked`.
- [`policy.py`](lab13-starter/policy.py), your file. The starter `decide()` never scales and `place()` puts new logins on the least-full server first.
- [`test_fleet.py`](lab13-starter/test_fleet.py), three tests. All three fail on the starter.

Run everything with the course Python:

```
cd labs/lab13-starter
../../../../.venv/bin/python fleet.py          # prints peak queue, queue player-minutes, server-hours
../../../../.venv/bin/python test_fleet.py     # PASS/FAIL per test (pytest also works)
```

The starter prints:

```
evening  peak queue  25,000  queue player-min  3,219,660  server-hours    120.0
launch   peak queue  55,000  queue player-min  5,977,000  server-hours    100.0
daily    peak queue  12,500  queue player-min  3,169,383  server-hours   1320.0
```

## The targets (what the tests check)

| Test | Trace | Pass condition |
|---|---|---|
| `test_evening_has_no_queue` | evening | peak queue = 0 |
| `test_launch_queue_is_bounded` | launch | queue player-minutes ≤ 80,000 **and** server-hours ≤ 400 |
| `test_daily_cost_and_queue` | daily | peak queue = 0 **and** server-hours ≤ 1.35 × the ideal (every minute, exactly `⌈D / 500⌉` servers), about 1,545 |

The launch test is the interesting one. It rejects a policy that simply runs at low utilization all the time (the queue is fine but the bill is too high), and it rejects one that runs hot with no view of the ramp.

## Steps

1. **Read the simulator (20 min).** Trace one minute of `run()` by hand: logouts, then logins placed in `place()` order, then your `decide()`. Write down which servers you pay for. Answer in your report: why can the starter's evening peak queue be exactly 25,000?
2. **Target tracking (30 min).** Implement `decide()` as `need = ⌈D / (u × CAP)⌉` over servers that are not draining, launching the difference. Try `u` = 0.9, 0.7 and 0.5 on all three traces and record a 3 × 3 table of peak queue and server-hours. Which `u`, if any, passes all three tests?
3. **Estimate the ramp (40 min).** Keep the last few minutes of demand in `self`. Estimate the ramp `r` (for example, the largest one-minute increase over the last 3 minutes) and provision for `D + r × LAG`. Before you run it, predict with the lecture's rule how many servers your policy will ask for at minute 1 of the launch trace. Then check. Explain in two sentences why the launch queue cannot reach zero for any reactive policy that starts from the fleet the simulator gives you.
4. **Scale in without kicking anyone (45 min).** When you have more active servers than `need` plus a margin, mark the emptiest ready servers as draining. Terminate draining servers only when they hold 0 players. Reopen (`undrain`) draining servers before you launch new ones when demand rises again. Add hysteresis: only drain after the surplus has lasted a number of minutes you choose. Record server-hours on the daily trace for a wait of 1, 15 and 60 minutes.
5. **Placement (20 min).** Change `place()` to put new logins on the fullest server that still has room. Compare daily server-hours with least-full placement. Explain the difference using the lecture's drain argument.
6. **Stress it (20 min).** Copy `launch_trace` into your report script with a ramp of 6,000 per minute. What happens to your queue and your bill? Name one change outside the policy (not allowed in this lab) that would help most, and quantify it with the headroom rule.
7. **Write it up.**

## Deliverable

A zip or repository link containing:

- Your `policy.py`, with `test_fleet.py` passing (paste the output in the report).
- `report.md`, 600 to 900 words, with: the step 1 answer; the step 2 table; the step 3 prediction versus the simulated value and the two-sentence explanation; the step 4 table of hysteresis waits; the step 5 comparison; the step 6 stress result and your proposed change with its computed effect.
- Every number reproducible from a command you list.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Weight |
|---|---|---|---|---|
| Tests | All three pass, no `PlayersKicked` | Two pass | One or none | 25% |
| Headroom reasoning | Step 3 prediction computed from `N = (D + r × L) / c` and matches the simulation to within a few servers; explanation of the unavoidable launch queue is correct | Prediction made but off without explanation | No prediction | 20% |
| Scale-in design | Drain, undrain and terminate all used correctly; hysteresis wait chosen from the step 4 table with a stated reason | Scale-in works but the wait is arbitrary | No scale-in, or players kicked | 20% |
| Placement analysis | Step 5 difference quantified and explained through drain time | Difference reported, not explained | Not done | 10% |
| Stress test and proposal | Proposed change (shorter `L`, warm pool, pre-scaling for the event) quantified with the rule | Change named, not quantified | Not done | 15% |
| Reproducibility and clarity | Commands listed; tables match reruns | Minor gaps | Cannot be rerun | 10% |
