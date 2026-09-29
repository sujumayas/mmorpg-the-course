# PR401 Lab 08: Economy tables against the live window

**Week:** 8 (Economy and balance design). **Guide:** [week 8](../lectures/w08-economy-and-balance-design.md). **Team lab**, submitted once per team.

## Objective

Put your economy in data files and prove, with a checker, that every priced item is reached by the player type it is for inside the four-week live period, and that at least one sink reaches the players who will hold most of the money.

## Starter materials

In [`labs/lab08-starter/`](lab08-starter/):

- `economy_check.py`. Standard library only. Run `python economy_check.py flows.csv prices.csv players.csv [players_at_launch]`. It prints the net rate `n`, the hours to afford each item, the week the target player type reaches it, and the share of money each player type holds at the end. It prints `PASS` or `NOT READY`.
- `flows.csv`. *Emberfall*'s design A from the guide: two faucets and two recurring sinks.
- `prices.csv`. The house plot and the light player's town banner, with declared values blank.
- `players.csv`. Week 1's four player types with *Emberfall*'s launch shares.

Flow types: `faucet`, `sink` (recurring, subtracted from `n`) and `scaling_sink` (optional spending that grows with activity, like a fee or a vendor with no limit; listed for review, not subtracted). A price row that misses its target week needs a `response`: why the team accepts it.

## Steps

1. **Warm-up (15 minutes).** Run the checker on the starter and read why design A fails. Change the files to design B from the guide (recurring sinks of 70 marks per hour, house plot at 1,200, the stall fee and dye vendor as scaling sinks) and fill the declared values. Run until it prints `PASS`.
2. **Your flows.** Replace `flows.csv` with every faucet and sink in your economy one-pager. Every row needs a source (prototype data with tester count, or `assumed`) and the telemetry event that will measure it.
3. **Your players.** Copy your week 1 player types into `players.csv` with the shares you expect at launch. Explain the shares in one sentence in `docs/economy.md`.
4. **Your prices.** List every item a player saves up for, with the player type it is for and the week they should reach it. Include at least one item for the light player.
5. **Tune.** Change prices or rates until each target is met, or write a response for the ones you accept missing.
6. **Money split.** Read the split. Name in `docs/economy.md` which scaling sink reaches the player type holding the most money, and what it costs a light player (it should be close to nothing).
7. **Balance table.** Write `data/balance.csv` with at least six targets (value, unit, reason), such as time to kill, death penalty and raid length. No checker; the instructor reads it.

## Deliverable

In `data/`, `docs/economy.md` and `preproduction/week08/` in the team repository:

- `flows.csv`, `prices.csv`, `players.csv` and the checker output saved as `check-output.txt`.
- `data/balance.csv` with at least six targets.
- `docs/economy.md`: the one-pager, the player shares explained, and the money-split paragraph from step 6.

**Checkable output:** the instructor reruns `economy_check.py` on your three files. It must print `PASS` and exit with code 0.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Checker passes | 4 | `PASS` on rerun; saved output matches |
| Flows | 4 | Every faucet and sink from the one-pager present, with source and telemetry event |
| Prices | 4 | Every saved-for item listed with target type and week; misses have a reasoned response; the light player has a goal |
| Money split | 3 | Split read correctly; a scaling sink targets the top holders and costs light players little |
| Balance targets | 3 | Six or more targets with values, units and reasons |
| Data, not code | 2 | The game reads these files at start; a price change needs no rebuild |
