# MMO302 · Lab 11: Ramp test with an open-loop bot fleet

**Week:** 11 ([lecture](../lectures/w11-load-testing-with-bots.md))
**Time:** 2 hours in the lab, plus up to 3 hours to finish.
**Work mode:** pairs. Each pair needs one laptop; two is better (server on one, bots on the other).
**Counts toward:** labs (40% of the course grade). This lab is the dry run for the final 500-bot load test, which uses the same bot fleet against your own world server.

## Objective

Drive a real TCP service with a fleet of open-loop bots, find its knee against a p99 SLO, compare the result with the M/M/1 model, and show with your own numbers how closed-loop bots hide overload.

## Starter materials

All in [`lab11-starter/`](lab11-starter/). Python 3, standard library only.

- [`server.py`](lab11-starter/server.py) is complete; do not edit it. It listens on `127.0.0.1:9302`, queues newline-terminated requests from all connections, and serves them one at a time with a CPU-bound exponential service time (mean 2 ms by default, so capacity is about 500 requests per second). It prints handled requests per second and queue length every 5 s.
- [`bots.py`](lab11-starter/bots.py) is the bot fleet. The network code is done: `run_open` (open loop, latency measured from the intended send time) and `run_closed` (closed loop, latency measured from the actual send). You write three functions: `percentile`, `poisson_schedule` and `find_knee`.
- [`test_bots.py`](lab11-starter/test_bots.py) has six `unittest` tests for your three functions. All fail on the starter. Run `python -m unittest test_bots.py` inside the folder.

## Steps

### Part A: finish the fleet (30 min)

1. Implement `percentile` with the MA102 week 12 rule (position `h = (n − 1) p + 1`, linear interpolation).
2. Implement `poisson_schedule` with exponential gaps drawn from the bot's own `random.Random`. The first send comes after the first gap, and every time is below `duration`.
3. Implement `find_knee`. It returns the last step that meets the SLO and stops at the first step that misses it, so a later lucky step does not count.
4. Run the tests until all six pass.

### Part B: ramp test (45 min)

5. Start the server in one terminal with `python server.py`. Leave it running and watch its 5-second reports.
6. In a second terminal, run the ramp `python bots.py --ramp 200 500 800 900 950 1200`. Each step lasts 20 s.
7. Copy the printed table into your report. Add two columns from the lecture's M/M/1 model, `W = 1/(μ − λ)` and `W99 = 4.605/(μ − λ)`, using `μ = 500` and `λ = 0.5 × bots`. On one chart, plot measured p99 and model p99 against bots.
8. Report the knee for a 100 ms SLO. In our reference run it was 900 bots, with a measured p99 of 77 ms at 900 and 130 ms at 950; your numbers will differ by machine. If yours is lower, look at the server's report lines. A laptop that is also running the bots, a browser and a video call has less than one full core for the server.
9. Look at the 1,200-bot step. Report offered and achieved load, p99, and "unanswered" requests. Explain in two sentences what a player would experience.

### Part C: the closed-loop lie (25 min)

10. Run `python bots.py --ramp 900 1200 --closed`. Record the table.
11. Put the open-loop and closed-loop rows for 1,200 bots side by side. In our reference run the closed-loop p99 was about 130 ms with 507 requests a second done, against about 3,400 ms, 548 done and 795 unanswered for open loop.
12. Explain in up to 150 words why the closed-loop fleet reports a healthy-looking p99, using the words "offered", "achieved" and "coordinated omission." Name the column in the closed-loop table that gives the lie away.

### Part D: move the knee (20 min)

13. Restart the server with `python server.py --service-ms 1.0`. Predict the new knee with the model before you run it. Then run the ramp `--ramp 1000 1600 1800 1900 2000` and compare.
14. In one paragraph, answer the question from the lecture's hook: if your server is 80% busy at 800 players, how many players would you promise the producer for launch, and why?

## Deliverable

- Your finished `bots.py`, passing all tests.
- A report of up to 3 pages (PDF): the Part B table with model columns and the chart, the knee, the Part C comparison and explanation, the Part D prediction and result, and the Part D paragraph. State the machine you ran on (CPU model, core count) and whether bots and server shared it.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Fleet code (Part A) | All six tests pass; code is short and readable | Tests pass with awkward code, or one test fails with a correct diagnosis | Several tests fail | 20 |
| Ramp test and model comparison (Part B) | Full table, model columns correct, chart overlays measured and model p99, knee stated, deviations explained | Table and knee present, model or chart missing | Missing | 30 |
| Coordinated omission (Part C) | Side-by-side numbers, explanation uses offered vs achieved load and names the giveaway column | Numbers present, explanation vague | Missing | 20 |
| Moving the knee (Part D) | Prediction made before the run, result compared, launch recommendation argued with p99 and spare capacity | Run done, prediction or argument missing | Missing | 20 |
| Report quality | Machine stated, units on every number, under 3 pages | Minor omissions | Unreadable or missing | 10 |
| **Total** | | | | **100** |
