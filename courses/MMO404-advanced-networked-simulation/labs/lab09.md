# MMO404 · Lab 09: A mesh for a crowd

**Week:** 9 · **Time:** 2 hours in lab plus about 2 hours at home · **Weight:** part of the labs (40%)

## Objective

Implement the meshing cost model from the [week 9 lecture](../lectures/w09-server-meshing-concepts.md), reproduce its table, and compare how a mesh scales for a dense crowd and for spread-out players. Then build the replication layer's authority table with epochs and show that a paused server cannot overwrite the new owner. You finish with a meshing plan for a live event.

## Starter materials

Folder [`lab09-starter/`](lab09-starter/README.md). Standard library Python only.

- `mesh.py`: the cost constants, the paused-server scenario from section 3 of the lecture, a table printer (`--table`), a CSV writer for both capacity curves (`--curves`) and the scenario runner (`--pause`). Stubs for `tick_ms`, `capacity`, `servers_for`, `ghost_updates`, `spread_tick_ms`, `spread_capacity` and the four `AuthorityTable` methods.
- `test_mesh.py`: the lecture's numbers and the fencing rules as tests.

## Steps

1. **By hand.** Compute `capacity(1)` from the quadratic and the tick time of 1,000 players on 4 servers, as the lecture does. Write both down before coding.
2. **Crowd model.** Implement `tick_ms`, `capacity`, `servers_for` and `ghost_updates`. Run the tests until the crowd checks pass, then run `python mesh.py --table` and paste the output.
3. **Spread model.** Implement `spread_tick_ms` and `spread_capacity`. Run `--curves curves.csv` and plot both curves against `k` on log-log axes, with reference lines of slope 1 and slope 1/2 through the `k = 1` points. Measure the slope of each curve between `k = 16` and `k = 256` and explain each slope from the model's terms.
4. **Where ghosts win.** For the crowd model, find the smallest `k` at which ghost work is more than 10% of the tick at capacity. Then change `C_G` to 8 µs and to 2 µs and repeat. Say what a cheaper ghost buys you and what it does not.
5. **Fencing.** Implement the `AuthorityTable` methods. Run the tests until they pass, then run `--pause` and paste the log. Then write a second scenario of your own: authority moves A to B to C while A and B are both paused, and both wake up and write. Show the log and the final state.
6. **Without fencing.** Copy `AuthorityTable` into `NaiveTable`, whose `write` checks only that the server is the recorded owner, not the epoch. Construct a sequence of grants and writes in which `NaiveTable` accepts a stale write that `AuthorityTable` rejects. (Hint: authority can return to a server that is still holding an old epoch.) Explain in two sentences why the owner check alone is not enough.
7. **Meshing plan.** Take one event card from the lecture's in-class activity. In one page, give the servers needed with and without one design change that cuts `c_i` or the crowd, the ghost share and replication layer load per second at 20 Hz, whether you mesh statically or dynamically (and if dynamically, when the split happens and how many entities it moves), and what players see if the event draws twice the expected crowd.

## Deliverable

Your finished `mesh.py` (including `NaiveTable`), the outputs of steps 2 and 5, the log-log plot and slopes from step 3, the table from step 4, the stale-write sequence from step 6, and the plan from step 7, in one Markdown or PDF file plus the code.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Cost model | All tests pass; hand calculation matches; `capacity` fills the budget exactly | Tests pass, hand work missing | Tests fail | 20% |
| Scaling analysis | Both curves plotted log-log with references; slopes measured and explained from the terms | Plot present, slopes unexplained | Missing | 20% |
| Ghost analysis | Threshold `k` found for three ghost costs; the ceiling argument stated | One ghost cost only | Missing | 10% |
| Fencing | Tests pass; own three-server scenario correct; naive table shown to fail with a minimal sequence and explained | Tests pass, naive case missing or unexplained | Tests fail | 25% |
| Meshing plan | Every number traced to the model; static or dynamic choice justified; overflow behaviour named | Numbers present, choice or overflow unjustified | Opinion without numbers | 25% |
