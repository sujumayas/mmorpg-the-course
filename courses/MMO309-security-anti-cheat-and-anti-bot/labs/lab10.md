# MMO309 · Lab 10: Follow the gold

Assigned in week 10 ([lecture](../lectures/w10-gold-sellers-and-rmt-networks.md)). Due at the start of week 11. Part of the labs component (30% of the course). About 2 hours in lab and 2 at home.

## Objective

Build the trade-graph detector from the week 10 lecture, reproduce the lecture's numbers on its toy server, then take it to a noisier server where one operation hides behind a second layer of accounts and some of its farms are aged, bought accounts. Recommend a rule you would let run in production, with its precision, recall and gold seized, and name the honest players it still puts at risk.

## Starter materials

All in [`lab10-starter/`](lab10-starter/). Standard-library Python 3 only.

- [`make_server.py`](lab10-starter/make_server.py). Two generators, do not edit. `toy_server()` rebuilds the lecture's 10,054-account server exactly. `lab_server(seed=10)` builds about 11,900 accounts: 11,000 guilded players, 300 unguilded newcomers, 60 guild banks (two of them giveaway banks that pay strangers and receive donations from newcomers), friend gifts inside guilds, 20 stolen accounts stripped into the operations, and two operations. Operation A has 5 mules and 250 farms. Operation B has 3 mules, 30 collectors and 240 farms, so its farms are two hops from a mule, and about a fifth of its farms are 40 to 120 days old. Every account carries its true label (`kind`, `op`), which your rules must not read.
- [`rmt_graph.py`](lab10-starter/rmt_graph.py). Six stub functions marked TODO: `build_index`, `stranger_share`, `find_hubs`, `expand`, `score` and `best_rule`. The docstring states the model. Running it prints a results table once the stubs work.
- [`test_lab10.py`](lab10-starter/test_lab10.py). Six checks. Four reproduce the lecture's toy-server numbers (mule 0 has fan-in 56; R4 gives 204/27/0; R5 gives 204/1/0 and 9,000,000 gold seized). One checks that `expand` does not modify its input. The last requires `best_rule` to reach precision of at least 0.95 and recall of at least 0.90 on `lab_server(10)`. Run it from inside `lab10-starter/` with `../../../../.venv/bin/python test_lab10.py`. All six fail on the starter.

## Steps

1. **Predict first.** Before coding, look at the lab server's description. Write down which accounts you expect the default hub rule (`k = 10`, `s = 0.5`) to flag, and which RMT accounts one careful hop will miss. Keep the note. You will grade your own prediction in step 4.
2. **Implement the model.** Fill in `build_index`, `stranger_share`, `find_hubs`, `expand` and `score`. Run the tests until the first five pass. Run `rmt_graph.py` and confirm the toy rows match the lecture's R3 and R5 rows.
3. **Explore the lab server.** Print the results for the default hub rule, one careful hop and two careful hops. For each false positive, print the account's id, guild, age and why it was flagged (which hub it sent to, or which rule made it a hub).
4. **Diagnose.** Explain every false positive and every false negative group in one sentence each. Compare with your step 1 prediction. Expect at least these groups: giveaway banks, newcomers who donated to them, and aged farms.
5. **Design `best_rule`.** Use only features you could compute from real logs (fan-in, fan-out, stranger share, guild, age, hours, gold). No labels. Make the test pass. Then try to raise recall above 0.95 without dropping precision below 0.95, and report whether you can.
6. **Stress it.** Run your rule on `lab_server(seed)` for seeds 11 to 20. Report the minimum, mean and maximum of precision and recall. A rule tuned to one seed that collapses on another is overfitted to the noise.
7. **Price it.** Using the section 3 prices from the lecture ($15 per replacement account, $5 per million gold), compute what your rule costs each operation on seed 10. Which operation loses more, and why?

## Deliverable

1. Your completed `rmt_graph.py`, with all six tests passing.
2. A results table: default hubs, one hop, two hops and your rule, on seed 10, plus the seed 11 to 20 summary from step 6.
3. A note of about 300 words to a live-ops lead recommending your rule. State its precision, recall and gold seized, name the honest groups it can still hit, and say what the team should do with the buyers it finds.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Model implementation | All tests pass, code clear, `expand` handles hops and the careful filter correctly | Tests pass with awkward or duplicated code | Tests fail | 25% |
| Diagnosis (steps 3-4) | Every false positive and false negative group explained with evidence, prediction compared honestly | Most groups explained | Few or no explanations | 20% |
| Rule design (step 5) | Label-free rule, target met, recall push attempted and reported | Target met, reasoning thin | Target missed or labels used | 20% |
| Robustness (step 6) | Ten seeds summarized, overfitting discussed | Seeds run, no discussion | Not done | 15% |
| Note to live-ops | Clear recommendation backed by numbers, honest risks, buyer policy | Recommendation with few numbers | Opinion without numbers | 20% |

<details>
<summary>Instructor check values</summary>

- Toy server, as in the lecture: default hubs flag the 4 mules and `bank0`. One careful hop gives TP 204, FP 1, FN 0, seized 9,000,000.
- Lab server, seed 10, default settings (tested with Python 3.13): hubs alone TP 8, FP 2, FN 520 (the 5 A mules, 3 B mules and both giveaway banks; the B collectors have fan-in 8, below 10). One careful hop: TP 288, FP 32, FN 240, precision 90.0%. Two careful hops: TP 480, FP 32, FN 48, precision 93.8%, recall 90.9%, seized 27,576,383.
- The 32 false positives are the two giveaway banks and the 30 newcomers who donated to them. Excluding hubs older than 60 days removes all 32 and passes the test with TP 480, FP 0, FN 48.
- The 48 false negatives are aged B farms (40 to 120 days). Students who drop the age condition on the second hop only, keeping "no guild", recover them: TP 528, FP 0, FN 0 on seed 10. It works here because no newcomer sends gold to a B collector. Ask them whether that would survive an operation that recruits newcomers as farms. The reference rule (hub age under 60, two careful hops) keeps precision 1.0 and recall between 0.90 and 0.93 on seeds 11 to 20.
- Strong notes point out that the stolen accounts were never flagged by careful expansion and should be routed to account recovery, and that buyers include unguilded newcomers, a group a studio should treat with care.

</details>
