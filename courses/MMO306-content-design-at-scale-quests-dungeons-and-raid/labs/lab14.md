# MMO306 · Lab 14: An accessibility audit

**Week:** 14 ([lecture](../lectures/w14-accessibility-in-group-content.md))
**Time:** 2 hours in the lab, plus up to 3 hours to finish.
**Work mode:** pairs.
**Counts toward:** final dungeon (60%). Each of your final dungeon's three bosses must ship with a cue table that passes the audit you build here, with `E = 0` on essential mechanics.

## Objective

Implement the week 14 cue-table model, run it on three bosses, and find the cheapest set of added channels that leaves no profile shut out of any essential mechanic. Compare the cheapest fix with the fix that follows XAG 103's two-senses rule. Then audit your own final-dungeon bosses for the barriers the model does not cover.

## Starter materials

All in [`lab14-starter/`](lab14-starter/). Standard-library Python 3, run with `.venv/bin/python` from the repository root or any Python 3.9+.

- [`cue_audit.py`](lab14-starter/cue_audit.py), with `load` written and six functions to write: `shut_out_of`, `fight_shut_out`, `blocked_groups`, `spans_two_senses`, `cheapest_fix` and `audit`. Each docstring gives the exact rule and tie-break the tests expect.
- [`encounters.json`](lab14-starter/encounters.json): the lecture's four profiles, an invented cost in days for adding each channel to a mechanic, and three bosses. The Twin Wardens are the lecture's example. The Hollow King has one non-essential mechanic. The Glass Choir is nearly accessible already.
- [`test_cue_audit.py`](lab14-starter/test_cue_audit.py), five tests: shut-out sets and `E` for each boss (with and without non-essential mechanics), the blocked-group share including the lecture's 1-in-12 hook, the two-senses rule with haptics, cheapest single-mechanic fixes, and whole-boss audits with and without the two-senses rule. All fail on the starter.
- The [interactive](../examples/w14-cue-coverage.html) for checking `E` and `G` by hand.

## Steps

### Part A: the model (30 min)

1. Implement `shut_out_of`, `fight_shut_out` and `blocked_groups`. Check the Twin Wardens against the lecture (`E = 22%`, `G(20) = 99.3%`).
2. Implement `spans_two_senses`. Haptics count as a sense for players, but XAG 103 says they should never be the only extra channel, so the function does not count them toward the two.

### Part B: the cheapest fix (40 min)

3. Implement `cheapest_fix` as an exhaustive search over the subsets of missing channels. There are at most 32, so brute force is fine. Get the tie-break exactly right.
4. Implement `audit` and run the file. Record the cost and fix list for each boss, with and without the two-senses rule.
5. Look at the cheapest fix for the Twin Wardens' whisper. It adds colour to a sound cue. Say in two sentences why that passes the model with these four profiles, and which real player it would still fail. Name the profile you would add to `encounters.json` to make the model catch it, and add it with a share you can justify. Rerun and report how the fixes change.
6. Compare total costs with and without the two-senses rule across the three bosses. Write one paragraph for your producer on whether the extra days are worth it.

### Part C: your own bosses (50 min)

7. Write the cue table for each of your three final-dungeon bosses in the same JSON format. Mark each mechanic as essential or not, with one line of reasoning each.
8. Run the audit with the two-senses rule. Apply the fixes to your encounter documents, and describe each added cue concretely (what the icon looks like, what the sound is, what the alert text says, in at most 6 words).
9. For each boss, list the barriers the cue table cannot see, using the lecture's sections 4 and 5: held or rapid inputs, exact-moment checks, voice-only calls, and the peak number of simultaneous rules per phase. For each, write the fix and classify it as a per-player setting, a shared encounter change or an alternative way to play.
10. Decide whether your dungeon needs an alternative way to play (NPC party members or a story version). Justify the decision in one paragraph with the production cost you expect and the players it reaches.

## Deliverable

- The completed `cue_audit.py` with all tests passing, your extended `encounters.json` from step 5, and `my_bosses.json` from step 7.
- A report of at most 2 pages: the audit table for the three given bosses with and without the two-senses rule, your answer to step 5, the producer paragraph from step 6, the before-and-after cue tables for your own bosses with `E` and `G` for your group size, the barrier list from step 9 and the decision from step 10.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Model and search (Parts A and B) | All five tests pass; search is exhaustive with the specified tie-break | Tests pass but code hard to follow, or one tie-break handled by accident | Tests fail | 30 |
| Critique of the model (steps 5 and 6) | Names the real player the cheapest fix fails, adds a justified profile, and weighs cost against players reached | Critique present but the new profile is unjustified | Missing | 20 |
| Own bosses (steps 7 and 8) | Every essential mechanic at `E = 0` with two senses; added cues described concretely | Passes the audit but cues are vague | Audit not run on own bosses | 25 |
| Barriers beyond perception (steps 9 and 10) | Every section 4 and 5 barrier checked; fixes classified; alternative-play decision backed by cost and reach | Barriers listed but unclassified, or decision unjustified | Missing | 25 |
| **Total** | | | | **100** |
