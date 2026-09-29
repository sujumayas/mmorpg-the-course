# PR301 Lab 07: Economy budget and recipe check

**Week:** 7 (Sprint 3: economy and crafting). **Guide:** [week 7](../lectures/w07-sprint-3-economy-and-crafting.md). **Team lab**, submitted once per team.

## Objective

Before sprint 3 builds the economy, write down how much currency each part of it should create and destroy per player-hour, tune it so the first real purchase arrives when your design wants it, and prove that no crafting recipe is a hidden faucet. The same reason codes become your ledger, so the budget is the prediction that week 10 tests.

## Starter materials

In [`labs/lab07-starter/`](lab07-starter/):

- `check_budget.py`. Standard library only. Run it with `.venv/bin/python check_budget.py budget.csv recipes.csv targets.txt`. It prints faucets, sinks, net income, the sink ratio, hours to the goal purchase, the weekend's money supply and a verdict for every recipe, then `PASS` or `NOT READY` (exit code 1).
- `budget.csv`. The first-draft budget from the guide's worked example, plus a starter-copper line with no ledger event.
- `recipes.csv`. Four recipes. One of them leaks.
- `targets.txt`. The guide's goal (600 copper, reached in 5.0 to 7.5 hours) and weekend estimate (33 players at 3.75 hours each, from the week 9 plan).

## Steps

1. **Warm-up (15 minutes).** Run the checker on the starter files. It reports three problems. Fix them the way the guide's team did: option A for the band, a ledger event for starter copper, and a vendor price change for the leaking recipe. Run until `PASS`. Write down what you changed and why in `budget.md`.
2. **Your reason codes.** List every way currency enters or leaves your world: loot, quests, vendors, repairs, consumables, crafting fees, training, market cuts, starter copper, GM commands, login rewards. One code per line. Transfers (`T_` codes) are not budget lines but go in the ledger schema.
3. **Your rates.** Fill `per_player_hour` for each line and set `basis` honestly. Use sprint 2 bot runs for kills and deaths per hour. Anything else is an estimate.
4. **Your target.** Choose the first meaningful purchase in your world and the hours of play by which a player should afford it. Put it in `targets.txt` with your week 9 player estimate.
5. **Tune one line at a time.** If hours to the goal is outside the band, model at least two single-line fixes in `budget.md` (one faucet change, one sink change), state who each one charges, and pick one.
6. **Recipes.** Enter every recipe whose output can be sold to a vendor. Inputs count at their vendor sell value (zero if they cannot be sold). Fix every `LEAKS`.
7. **Where currency lives.** In `budget.md`, list every place currency can sit (character balance, mail, market escrow, guild bank). This list defines money supply for week 10.

## Deliverable

In `production/week07/` in the team repository:

- `budget.csv`, `recipes.csv` and `targets.txt` that pass `check_budget.py`, with its output saved as `check-output.txt`.
- `budget.md`: the options you modelled, the one you chose and who it charges, the list of places currency can live, and a note on which rates are estimates.

**Checkable output:** the instructor reruns `check_budget.py` on your three files. It must print `PASS` and exit with code 0. At the sprint 3 review (start of week 9), the instructor also checks that every `logged_event` appears in the build's ledger.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Checker passes | 4 | `PASS` on rerun, output file matches |
| Complete reason codes | 4 | Every faucet and sink in the design has a line, including starter copper and GM commands |
| Honest basis | 2 | Rates marked bot run or estimate, and bot-run rates traceable to a log |
| Tuning | 4 | Two single-line options modelled with arithmetic, the choice justified by who pays |
| Recipes | 3 | Every vendor-sellable recipe listed, none leaks |
| Money supply definition | 3 | Every place currency can live is listed and matches the schema |
