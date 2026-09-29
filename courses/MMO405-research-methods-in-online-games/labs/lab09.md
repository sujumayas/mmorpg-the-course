# MMO405 · Lab 09: A guild network from census snapshots

**Week:** 9 ([Social network analysis of guilds](../lectures/w09-social-network-analysis-of-guilds.md))
**Time:** 2 hours in lab plus about 2 hours at home
**Counts toward:** methods labs (30%); the sensitivity table and memo feed the analysis section of the final paper (50%)
**Work:** in pairs; submit one folder per pair

## Objective

You will turn four weeks of `/who`-style snapshots into a weighted co-activity network for one guild, following the tie rule of Ducheneaut and colleagues (2007). You will implement degree, strength, betweenness and eigenvector centrality, compare the results with the guild's rank list, and show how the answer to "who is central?" moves with the tie threshold. You will also find at least one tie that the zone rule created by mistake.

## Starter materials

All in [`lab09-starter/`](lab09-starter/README.md). Python 3.10 or later, standard library only.

- `gen_census.py` writes `census.csv` from seed 809. It holds a snapshot every 10 minutes from 19:00 to 22:00 on 28 evenings, one row per character online, with guild, zone and a grouped flag. The guild under study is Lanternfall. Other characters are noise from other guilds. Cities are Capital and Harbor.
- `ranks.csv`, Lanternfall's rank list (a guild master, three officers, members).
- `sna.py` holds eight functions to write: `members`, `build_ties`, `graph`, `degree_centrality`, `strength`, `betweenness`, `eigenvector` and `top_by_threshold`. Each docstring gives the exact rule, and the lecture's code is a model for the last four. `main()` prints the centrality table and the threshold comparison once they work.
- `check_lab09.py` prints PASS, FAIL or TODO per function, plus one check on the generated census.

```
python gen_census.py
python sna.py
python check_lab09.py
```

## Steps

1. **Build the ties (25 min).** Write `members` and `build_ties`. Two members are tied in a snapshot when both are grouped, in the same zone, outside a city. Report the number of members and ties, and the five heaviest ties in minutes.
2. **Centralities (30 min).** Write `graph` and the four measures. Run `sna.py` and copy the table into `RESULTS.md`. Hand-check one member's degree and strength from the tie list.
3. **Rank against position (15 min).** Mark the guild master and officers in your table. For each of them, say in one sentence what the network shows and what it cannot show about their role.
4. **Artefacts of the tie rule (15 min).** Find the lightest ties involving the guild master. Using `census.csv`, look at the snapshots that created one of them. Was the pair really playing together? Explain which part of the tie rule produced it, and relate it to the limitation Ducheneaut and colleagues reported. Propose a stricter rule you could apply with the data you have.
5. **Sensitivity (20 min).** Write `top_by_threshold`. Then build a sensitivity table in `RESULTS.md` with thresholds 0, 100, 200, 300, 400 and 600 minutes. For each, give the top three members by betweenness with their scores, and any members who become isolated. Which conclusions hold at every threshold, and which depend on your choice?
6. **Memo (at home, 400 words).** Write for a reader who is deciding whom to interview about how Lanternfall is led. State your boundary, tie rule, weights, threshold and window. Name the member you would interview first and the one you would interview second, and justify both with specific numbers and with the limits from step 4. Close with two sentences on the ethics of sharing this table with the guild's leadership.

## Deliverable

One folder named `lab09-<name1>-<name2>` containing `sna.py` (passing `check_lab09.py`), `RESULTS.md` with steps 1 to 5, and `memo.md` from step 6.

## Rubric (20 points)

| Criterion | Excellent (full) | Adequate (half) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Code passes the checker | All nine checks PASS | Six to eight PASS | Five or fewer | 4 |
| Table, hand-check and rank comparison (steps 2 and 3) | Hand-check shown; each ranked role discussed with what the network can and cannot show | Table present, discussion thin | Missing | 4 |
| Tie artefact (step 4) | Specific snapshots identified; the zone rule named as the cause; a workable stricter rule proposed | Artefact found, cause or fix vague | Missing | 4 |
| Sensitivity (step 5) | Full table; robust and fragile conclusions clearly separated | Table incomplete or conclusions not separated | Missing | 4 |
| Memo (step 6) | All four construction choices stated; interview choices justified by numbers and limits; ethics addressed concretely | Choices stated but justification or ethics generic | Missing | 4 |
