# MMO302 · Load test brief: 500 bots against your world server

**Weight:** 20% of the course grade.
**Test plan due:** end of week 13. **Dry run:** week 14 lab session. **Test run:** week 15 lab session. **Report due:** 48 hours after your test run.
**Work mode:** the same as your [final server](final-server-brief.md), individual or the same pair.
**Lectures:** [week 11, load testing with bots](../lectures/w11-load-testing-with-bots.md) and [week 14, observability](../lectures/w14-observability-logs-metrics-traces.md), with the models of [week 1](../lectures/w01-scale-targets-ccu-messages-and-n-squared.md), [week 3](../lectures/w03-area-of-interest-grids-radius-hysteresis.md), [week 5](../lectures/w05-tick-rate-for-mmos-vs-shooters.md), [week 7](../lectures/w07-persistence-strategies-write-through-periodic-event-sourcing.md) and [week 9](../lectures/w09-login-character-select-gateway-services.md).
**Starting point:** [lab 11](../labs/lab11.md)'s open-loop fleet and [lab 14](../labs/lab14.md)'s tick histogram and stall alert.

## What this component is for

The week 11 lecture opened with a question: if a server is 80% busy at 800 players, how many can it take? This assessment asks it about your own server. You predict the answer from the course's models, write down a pass line before you start, drive the server with 500 bots that behave like players, and then explain every place where the measurement and the prediction disagree.

It is separate from the final server because it measures something the viva cannot. A server can pass every functional test and still stall 12 times a minute with 200 players at a world boss, or lose its audit balance when a zone dies under load. This test finds out, with numbers you can defend.

## The rules of an honest test

These come from the week 11 lecture. A test that breaks one of them cannot score above half marks on the rows it affects.

- **Open loop.** Each bot schedules its sends in advance and measures latency from the intended send time. Report offered load next to achieved load at every step.
- **One connection per bot** to the gateway. Lab 11's fleet shares 50 connections, which is fine for its toy service but does not test a gateway whose job is to hold one connection per player. Change it.
- **Bots off the server's machine.** Run the fleet on a second lab machine, or on your laptop with the server on a lab machine. State both machines' CPU model, core count and memory.
- **A player-shaped mix.** Use the week 11 table as the default: movement at 10 per second while moving, combat at 0.5 to 1 per second in combat, chat at about 0.001 per second, loot, trade and mail a few times a minute, a zone change a few times an hour. Change it only with a stated reason.
- **Seeded bots.** Every bot has its own seeded generator, and the report lists the seeds, so a failing run can be replayed.

## The scenarios

Run all six in the week 15 session. The dry run in week 14 should cover at least scenarios 1 and 2.

1. **Ramp.** 100, 200, 300, 400 and 500 bots spread over both zones, each step held 3 minutes after a 1-minute warm-up. If the SLO still holds at 500, add steps of 100 until it breaks or you reach 1,000.
2. **World boss.** At 500 bots, move 40% of them (200) into one 50 m circle in one zone for 3 minutes, then let them disperse.
3. **Past the limit.** One step above your knee (or double every bot's action rate at 500), held for 2 minutes, then drop back to 300. Measure how long the server takes to meet the SLO again, or show that it does not recover.
4. **Login storm.** Disconnect all bots, then have all 500 reconnect with the jitter window your lab 09 work chose. Measure login p99, queue length and failed logins.
5. **Soak.** 70% of your knee (or 500 bots if you never found one) for 45 minutes. Plot memory, send-queue depth and commits per second against time and state whether any grows without limit.
6. **Crash under load.** During the soak, kill one zone server with `kill -9` in the middle of trading. Restart it. Measure the recovery time, the players who could not reconnect, the committed progress lost (it must be zero) and the audit drift after recovery (it must be exactly zero).

## The service level objectives

Write your own in the test plan. The defaults below are the pass line unless you argue for different ones before the run.

| Quantity | Default SLO |
|---|---|
| Action response, p99 (intended send to server acknowledgment) | ≤ 100 ms |
| Tick time, p99, per zone | ≤ the tick budget `1000 / T` |
| Stalls per minute, per zone (ticks over budget) | ≤ 2, over any 5-minute window |
| Login time, p99, in scenario 4 | ≤ 5 s |
| Audit drift after every scenario | exactly 0 |
| Committed progress lost in scenario 6 | 0 |

Stalls per minute come from lab 14's histogram, which has a bucket edge at the budget, so the count is exact. Report them per zone. A fleet-wide number hides the zone players complain about.

## Predict before you measure

Your test plan, handed in at the end of week 13 and dated, must predict these numbers. You will not lose marks for a wrong prediction with honest working. You will lose them for a missing one, or for one changed after the run.

- **Tick cost at each ramp step and at the world boss,** from your lab 05 fit `c = a + d·n + e·n·k`, with `k` estimated from the week 3 model for your map, cell size and radius (`N × ρ × 9c²` spread out, `g(g − 1)` in the crowd).
- **The knee,** as the bot count where your predicted tick cost reaches 60% of the budget and where it reaches 100%.
- **Commits per second** at 500 bots from the week 7 formulas and your persistence policy.
- **Recovery time** in scenario 6 from `N·c·K/2/r` with your snapshot interval and a measured replay rate.
- **Chat copies per second** at 500 bots from the week 10 model, to check chat is not your bottleneck.

## The report

`LOADTEST.md`, at most 2,000 words plus tables and charts, with every number carrying its unit, its settings and its seeds.

1. **Setup.** Both machines, the server build (commit hash), bot count per step, message mix and seeds, and the SLO table.
2. **Ramp table.** One row per step: bots, offered actions per second, achieved actions per second, action p50, p99 and max, tick p99 per zone, stalls per minute per zone, CPU per core, memory. Then the sentence the lecture asks for: "the knee for this build is between N and M bots, limited by X."
3. **Predicted against measured.** Your predictions from the plan beside the measurements, with each gap of more than 20% explained. Typical causes are garbage-collection pauses, a lock around the database pool, burstier arrivals than the model, or AOI candidate scans that the `k` term does not count.
4. **Scenarios 2 to 6.** For each, one chart and one paragraph with the numbers. For scenario 2, the tick strip of the boss zone with the budget line and the stalls marked. For scenario 6, a timeline from the kill to the first successful reconnect and the audit output.
5. **What you would change.** The one change that would move the knee most, with the model's estimate of how far (for example "halving `u` for players beyond 30 m cuts the boss zone's neighbour term from 62 to 31 ms").

Include the raw per-step CSVs and the command lines that produced them, so a marker can rerun a step.

## Rubric

Each criterion is scored Excellent (full points), Adequate (half), or Missing or wrong (0). A marker may give a quarter or three quarters of the points where the work falls clearly between two cells.

| Criterion | Excellent | Adequate | Missing or wrong | Points |
|---|---|---|---|---|
| Test plan and SLO | Plan handed in on time, dated, with SLOs, scenarios and seeds; any change from the defaults argued | Plan late or SLOs incomplete | No plan before the run | 10 |
| Predictions | All five predictions made before the run from the lecture models, with working | Three or four predictions, or working thin | Predictions missing or written after the run | 15 |
| Honest fleet | Open loop, one connection per bot, bots on a separate machine, player-shaped mix, offered and achieved reported and matching | One rule broken with the effect acknowledged | Closed-loop bots or offered load not reported | 15 |
| Ramp results and knee | Full ramp table with per-zone tick p99 and stalls; knee stated with its limiting resource; charts labelled | Table present but per-zone numbers or the limiting resource missing | No ramp, or only means reported | 20 |
| Crowd, overload, storm and soak | Scenarios 2 to 5 run, each with its chart and numbers; recovery after overload measured; soak slopes stated | Two or three of the four scenarios done well | One or none | 15 |
| Integrity under load | Crash run with zero committed loss and exactly zero drift after every scenario, shown with audit output; recovery time compared with the model | Integrity shown for some scenarios, or recovery time not compared | Drift nonzero and unexplained, or no crash run | 15 |
| Explanation and reproducibility | Every prediction gap over 20% explained with a mechanism; raw CSVs and commands included; a marker can rerun a step | Most gaps explained, some data missing | Numbers cannot be traced or rerun | 10 |
| **Total** | | | | **100** |

A server that fails its SLO at 300 bots can still earn full marks here. This component grades the test, not the server's speed. A clear, honest report that finds the knee at 300 and names the lock that causes it is worth more than a vague report that claims 500 passed.

## Academic integrity

The measurements must come from your own runs with your own server, on the machines you state. You may share bot code with other groups if you credit it in the report, since the fleet is a tool and not the thing being assessed. You may not share measurements. Use of AI assistants and documentation is allowed and must be listed in one line per use.
