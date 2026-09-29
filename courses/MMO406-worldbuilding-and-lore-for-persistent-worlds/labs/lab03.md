# MMO406 · Lab 03: The faction web

**Week:** 3, factions and conflict ([lecture](../lectures/w03-factions-and-conflict.md)).
**Time:** 2 hours in lab, plus up to 3 hours at home.
**Weight:** exercises (40% of the course, shared across the exercise labs). The faction web and flip plan become the factions chapter of the final world bible (60%).

## Objective

Build a structural-balance analyser for faction webs, check it against the lecture's numbers and a real game's structure, then design your own world's faction web with a tension target and plan the first relationship change of your first expansion.

## Starter materials

All in [`lab03-starter/`](lab03-starter/). Standard-library Python, run with the program's `.venv/bin/python`.

- [`factions.py`](lab03-starter/factions.py), with a finished loader, `sign` and `report`, and five empty functions: `triads`, `tension`, `camps`, `edge_triads` and `best_flip`.
- [`bribe.json`](lab03-starter/bribe.json), the four-faction "bribe" web from the lecture's table.
- [`eve_fw.json`](lab03-starter/eve_fw.json), EVE Online's faction warfare relationships with the two pirate militias added in 2023, as described in the lecture. Pairs not at war in faction warfare are left neutral.
- [`test_factions.py`](lab03-starter/test_factions.py), tests built from the lecture: the table (4 of 4, 0 of 4 with camps, 2 of 4 with the two named triads), the check-yourself webs (10 of 10; 3 of 10 after a secret pact), the `n − 2` rule for 3 to 7 factions, the best flip for "all at war," the EVE web (2 of 2, no triad across war zones), and the two-faction case with no triads. The tests fail on the starter and pass once your functions are correct.
- The [interactive](../examples/w03-faction-web.html), for spot checks.

Run the tests from inside the starter folder:

```
cd courses/MMO406-worldbuilding-and-lore-for-persistent-worlds/labs/lab03-starter
../../../../.venv/bin/python test_factions.py
```

## Steps

1. **Triads and tension (20 min).** Implement `triads` and `tension`. Keep the file's faction order, since the tests compare lists.
2. **Camps (15 min).** Implement `camps` using the two-colouring hint. Return `None` for any web with a neutral pair or an unbalanced triad.
3. **Edges and flips (25 min).** Implement `edge_triads` and `best_flip`. Copy the edge dictionary before changing a sign. Ties go to the alphabetically first pair.
4. **Read two reports (10 min).** Run `factions.py bribe.json` and `factions.py eve_fw.json`. For the bribe, the best flip undoes the bribe. In two sentences, say why a writer might prefer the second-best flip instead. For EVE, say which pairs you would change from neutral to create a triad that crosses the two war zones, and what that triad would be.
5. **Your web (at home).** Write `myweb.json` with 5 to 8 factions from your world bible. For each faction, write its want, holding, player contact and face (the lecture's four questions) in a table in your report.
6. **Tune (at home).** Set a target `T` for your launch web and justify it in terms of the kind of game you are making (stable PvP identity, political intrigue, or a mix). Revise until the web meets it. At least one relationship must be backed by a game system (reputation pair, contested region from lab 02, PvP rule). Add it to your lab 01 ledger as a structural tension.
7. **Mark contested edges (at home).** Mark at least two pairs whose sign is contested by history or interest. For each, run the web with that pair flipped and record `T` and the triads that changed.
8. **Plan the first flip (at home).** Choose the flip for your first expansion. Check that `T` after it is above zero. Write the story beat in one paragraph and list the quests or events it would need.

## Deliverable

- Your completed `factions.py` with all seven tests passing, and the step 4 answers.
- `myweb.json`, each revision's report, and the flipped versions from step 7.
- A factions chapter of at most 900 words: the four-question table, your target `T` and why, the system-backed relationship, the contested edges with their flip results, and the first-expansion flip and story beat.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Correctness | All seven tests pass | Six pass | Fewer than six pass | 25% |
| Report reading | Explains the writer's choice of flip and designs a plausible cross-zone EVE triad | One of the two done well | Missing | 10% |
| Faction design | Every faction answers all four questions concretely | Most do; some wants or holdings vague | Factions are names with flavour text | 20% |
| Tension tuning | Target reasoned from the game's goals and met; system-backed relationship clearly linked to the ledger | Target met, reasoning thin | Target missing or not met | 20% |
| Contested edges and flip | Two contested edges measured; first flip keeps `T > 0` and yields a clear, buildable story beat | Flip planned, measurements partial | Missing | 25% |
