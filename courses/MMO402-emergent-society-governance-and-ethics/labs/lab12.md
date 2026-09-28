# MMO402 · Lab 12: Release audit

**Week:** 12 ([lecture](../lectures/w12-research-ethics-in-online-worlds.md))
**Time:** 2 hours in the lab, plus up to 2 hours to finish.
**Work mode:** individual.
**Counts toward:** case analyses (30% of the course grade).

## Objective

A university team has asked your studio for character-level data to answer one question: are characters in small guilds more likely to quit within 30 days than characters in large guilds or in no guild? Your job is to audit the release they asked for, show how many characters an outsider could re-identify, and design a release that is 5-anonymous and still answers the question.

## Starter materials

- [`lab12-starter.py`](lab12-starter.py): a Python 3 script (standard library only). It contains:
  - `generate(seed=412)`: a synthetic server of 10,000 characters with a name, class (10 values), race (10), level (1 to 60, with 40% at the cap), guild (200 guilds with Zipf-distributed sizes, 25% unguilded), zone (40), guild size, and the outcome `quit_30d`. Class and race follow Zipf weights, so a few combinations are common and many are rare.
  - `uniform_estimate(n, value_counts, k)`: the lecture's formula (`λ`, unique share, share in classes smaller than `k`).
  - `equivalence_classes` and `class_report`: actual class counts for any field list.
  - `public_profiles(records, n=500)`: 500 characters with name, class, race, level and guild, standing in for public character pages an attacker could read.
  - `release(records, fields)`: drops the name and keeps the chosen fields plus the outcome.
  - Four stubs for you: `link_attack`, `generalize`, `suppress`, `answer_question`.
- Run it once before you start. With the default seed it prints the uniform estimate (18.9% unique for class, race and level) and the actual count (14.4% unique for the same fields on this skewed server, 61.9% once guild is added).
- The lecture's section 2 table, and the uniqueness interactive `examples/w12-unique-players.html` once it is built.

## Steps

### Part A: model against reality (20 min)

1. For the requested fields `class, race, level, guild`, and for each prefix (`class`; `class, race`; `class, race, level`), record the uniform estimate and the actual count: unique share and share in classes smaller than 5.
2. Explain in three or four sentences why the actual numbers differ from the uniform estimate. Which part of the skew lowers uniqueness, and which records stay unique anyway? Name one kind of character that is unique under every release you try.

### Part B: the linkage attack (25 min)

3. Implement `link_attack(released, profiles, fields)`. For each public profile, count the released rows that match it on `fields`. A profile that matches exactly one row is re-identified, and the attacker now knows that character's `quit_30d` value.
4. Run it on the requested release. Report how many of the 500 profiles are re-identified and what share that implies for the whole server. Compare with the unique share from step 1.

### Part C: make the release 5-anonymous (40 min)

5. Implement `generalize`. At minimum, support level brackets (widths of your choice) and a guild group (`none`, `small` under 20 members, `medium` 20 to 99, `large` 100 or more). You may also drop fields.
6. Try at least three generalization plans. For each, report the number of equivalence classes, the unique share, the share in classes smaller than 5, and the link-attack result.
7. Implement `suppress(records, fields, k)`. Apply it to your best plan to remove the remaining classes smaller than 5. Report how many records you removed, and which guild groups and levels they came from.

### Part D: does the release still answer the question? (20 min)

8. Implement `answer_question`. Compute the 30-day quit rate for each guild group on the raw data and on your final release.
9. Report both sets of rates side by side. If suppression changed any rate by more than 1 percentage point, explain why, using what you found in step 7.

### Part E: time series (15 min)

10. The research team now asks for each character's zone at 30 daily snapshots. Without writing code, estimate `C` for 30 snapshots of 40 zones with the lecture's formula, and state whether any row-level release of that series can be 5-anonymous. Propose what you would offer instead.

## Deliverable

- The completed script, runnable with the default seed.
- A before-and-after table (requested release against your final release) with classes, unique share, share below 5, link-attack re-identifications and quit rates by guild group.
- A one-page release memo to the research team: what you will release, what you will not and why, the `λ` calculation, the records suppressed, and the consent or waiver basis you are relying on (see lecture section 3).

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Model against reality (Part A) | Both sets of numbers; the skew explanation names crowding and rare combinations correctly | Numbers present, explanation vague | Missing | 15 |
| Linkage attack (Part B) | Correct implementation; re-identification count compared with unique share | Runs, comparison missing | Does not run | 20 |
| 5-anonymous release (Part C) | Three plans compared; final release passes k = 5; suppression reported by group | Passes k = 5 with weak comparison | Fails k = 5 | 25 |
| Research question preserved (Part D) | Rates compared; any shift over 1 point explained by the suppressed records | Rates compared without explanation | Missing | 15 |
| Time series judgment (Part E) | Correct `C` estimate, clear decision, a workable alternative (aggregates or enclave) | Decision without estimate | Missing | 10 |
| Release memo | Specific, cites the numbers, states a consent or waiver basis | Generic | Missing | 15 |
| **Total** | | | | **100** |
