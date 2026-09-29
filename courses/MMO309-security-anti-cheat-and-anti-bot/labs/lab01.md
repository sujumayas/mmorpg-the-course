# MMO309 · Lab 01: The threat ledger

**Week:** 1 ([lecture](../lectures/w01-threat-modeling-for-games.md)) · **Time:** 2 hours in the lab plus about 3 hours at home · **Work mode:** pairs · **Counts toward:** labs (30%); the result is the first draft of the threat model assessment (30%).

## Objective

Build a small tool that ranks threats by expected annual loss and values controls, reproduce the week 1 tables with it, then use it to write a costed threat model for a sample MMO. You finish able to defend a priority list with numbers, including the cost each defense puts on honest players.

## Starter materials

Folder [`lab01-starter/`](lab01-starter/README.md). Standard library Python only; use `.venv/bin/python` from the repository root.

- `threat_ledger.py`: CSV loading, the check harness and the report are written. You write four functions.
- `threats.csv` and `controls.csv`: the lecture's data, with `I_low` and `I_high` estimates added to each threat.

### The sample game

*Driftmark* is an invented island-hopping MMO with 60,000 monthly players on a $12 subscription. Its features:

- Player-to-player trade and a player-run auction house with a 5% fee.
- Guild halls whose storage chests any guild officer can empty.
- Open-world PvP on outer islands, with full loot of carried materials.
- A cash shop for cosmetics, paid through an outside payment provider.
- Account recovery by email link, handled by a support team of three.
- A web armory that shows any character's gear by name.
- GM tools that can spawn items and move characters, used from staff laptops.
- Fishing and mining nodes that respawn on fixed timers.

## Steps

### Part A: build and verify (40 min)

1. Implement `ale`, `rank`, `net_value` and `stable_top` following their docstrings. Run `python threat_ledger.py --check` until it prints `all checks passed`.
2. Run `python threat_ledger.py --table` and confirm both rankings and all five net values match the lecture's section 2 tables.
3. Check two rows by hand, T6's ALE and C5's net value, and show the working in one line each.

### Part B: uncertainty (20 min)

4. Read the `I_low` and `I_high` columns. Using `stable_top`, find which threats stay in the top 3 under both estimates. Then find the smallest `n` for which all of T2, T5, T6 and T7 are in the stable top `n`.
5. Pick the one threat whose `I` estimate most changes the ranking. Explain in two sentences what research (logs, surveys, support data) would narrow its range.

### Part C: threat model for Driftmark (60 min in lab, finish at home)

6. Draw the data flow diagram for Driftmark with every trust boundary marked. At least six boundaries.
7. Write `driftmark_threats.csv` with at least 12 threats. Cover every STRIDE letter at least once and each of the three game families from lecture section 3 (automation, design exploits, social attacks) at least once. For every `f` and `I`, add a short note in a separate table saying where the estimate came from.
8. Write `driftmark_controls.csv` with at least 4 controls. At least one must have a nonzero player cost `P`, and at least one must lower the loss of two threats (enter it as two rows, one per threat, and explain the split).
9. Run the tool on your files and include the output.

### Part D: information disclosure (after week 2, 20 min)

10. Using the week 2 leak model, add rows for every information-disclosure threat in Driftmark (the web armory and open-world PvP at least). For PvP, estimate the leak per engagement under Driftmark's current design and under one improvement, and turn the difference into a change in `I`.

## Deliverable

Your finished `threat_ledger.py`, the two Driftmark CSV files, and a PDF of at most 4 pages: the hand checks (step 3), the Part B answers, the diagram, the estimate-source table, the tool output, a 150-word recommendation naming the first two controls you would build and why, and the Part D rows with their working. Submit before the week 3 lecture.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Tool correctness (Part A) | `--check` passes; hand checks shown and correct | Passes, hand checks missing or with errors | Fails the check | 20 |
| Uncertainty (Part B) | Stable top found and smallest `n` correct; research plan specific to the threat | Answers correct, plan vague | Missing | 15 |
| Diagram and threats | Six or more boundaries; 12 or more threats covering all STRIDE letters and the three game families; estimate sources given | Most categories covered, sources thin | Fewer than 8 threats or no diagram | 25 |
| Controls | Four or more, with `r`, `B`, `P` justified; one with player cost; one covering two threats | Four controls with weak justification | Controls without numbers | 20 |
| Recommendation and Part D | Uses the pair's own numbers, names a trade-off, leak estimate worked | Recommendation plausible but not tied to the ledger | Missing | 20 |
| **Total** | | | | **100** |
