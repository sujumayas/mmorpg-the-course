# PR401 Lab 10: Social liquidity and safety sheet

**Week:** 10 (Social systems plan). **Guide:** [week 10](../lectures/w10-social-systems-plan.md). **Team lab**, submitted once per team.

## Objective

Show that every social system that needs several players at once will actually have them, at the population and play times you expect, and that the safety minimums for a public launch each have an owner and a date.

## Starter materials

In [`labs/lab10-starter/`](lab10-starter/):

- `social_check.py`. Standard library only. Run `python social_check.py liquidity.csv safety.csv`. For each system it prints the online probability `p` in the play window and off-peak, and the probability that at least `m` of `M` members are online, after any NPC fill. It checks your declared values (tolerance 0.01), requires a response for any window value under 0.80 and an off-peak rule for every system, and checks the eight safety minimums from guide section 3. It prints `PASS` or `NOT READY`.
- `liquidity.csv`. *Emberfall*'s draft and final town defence rows from the guide, with some declared values, the off-peak rule and a response missing.
- `safety.csv`. Seven of the eight safety features, one without an owner.

Column notes. `npc_fill` is how many of the `needed` slots NPCs can fill (the militia); the checker never lets `needed` fall below 1. `window_share` is the share of weekly play inside the window, and `window_hours` its length in hours per week. `status` is `done` or `planned`, and planned items need a `due_week`.

## Steps

1. **Warm-up (10 minutes).** Complete the starter from the guide: fill the declared values, give the draft row a response and an off-peak rule, give the chat filter an owner and add the missing safety feature. Run until the checker prints `PASS`.
2. **List your systems.** Every system in your social plan that needs more than one player at the same moment gets a row: group activities, town or guild defence, raids, trade that needs a buyer online, events with a minimum turnout.
3. **Play time.** Compute `hours_per_week` as the weighted mean of your week 8 player types. Estimate `window_share` and `window_hours` from your prototype session times, or state them as assumed in `docs/social-plan.md`.
4. **Levers.** For every row under 0.80, add a changed row using one of the four levers (bigger pool, more time online, fewer needed, fixed window), and say in `response` what it costs players.
5. **Off-peak.** For every row, write what happens outside the window: blocked, scaled down, or accepted as a risk.
6. **Safety.** Complete `safety.csv` with owners and due weeks. Write the code of conduct and compute the moderation rota hours: hours the server will be open to the public in PR402, and who covers each.
7. **Fallback.** In `docs/social-plan.md`, write the low-population rule: at what player count towns (or guilds, or groups) merge or shrink, and who decides.

## Deliverable

In `preproduction/week10/` and `docs/` in the team repository:

- `liquidity.csv`, `safety.csv` and the checker output saved as `check-output.txt`.
- `docs/social-plan.md` with the six parts, the assumptions behind `p`, the fallback rule and the rota.
- `docs/code-of-conduct.md`, one page.

**Checkable output:** the instructor reruns `social_check.py` on your two files. It must print `PASS` and exit with code 0.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Checker passes | 4 | `PASS` on rerun; saved output matches |
| Coverage | 4 | Every multi-player system in the social plan has a row |
| Play-time inputs | 3 | `h`, window share and window length come from data or are labelled as assumed |
| Levers | 4 | Every row under 0.80 has a lever with its player-facing cost; off-peak decided for all rows |
| Safety | 3 | Eight minimums with owners and dates; rota hours computed and covered; code of conduct written |
| Fallback | 2 | Low-population trigger, action and decision owner stated |
