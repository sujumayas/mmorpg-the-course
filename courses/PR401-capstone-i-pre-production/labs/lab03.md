# PR401 Lab 03: Pillar sheet and hour audit

**Week:** 3 (Pillars and vision). **Guide:** [week 3](../lectures/w03-pillars-and-vision.md). **Team lab**, submitted once per team.

## Objective

Check that your plan spends its hours on its pillars. You will write your pillars and anti-pillars with a testable question for each pillar, weight every feature against the pillars it serves, and revise the feature list until each pillar gets its minimum share of hours and little work serves nothing. The checker reports the shares and whether the sheets are complete.

## Starter materials

In [`labs/lab03-starter/`](lab03-starter/):

- `check_pillars.py`. Standard library only. Run it with `.venv/bin/python check_pillars.py pillars.csv features.csv`. Flags `--s-min` and `--o-max` change the thresholds (defaults 0.20 and 0.10).
- `pillars.csv`. *Emberfall*'s pillars and anti-pillars. P3 has no test question yet.
- `features.csv`. *Emberfall*'s first feature list from the guide, plus two foundation rows. Pillar columns are named after pillar IDs. Blank means 0.

The starter prints `NOT READY` with five problems on purpose.

## Steps

1. **Warm-up (15 minutes).** Run the checker and confirm the first-draft row of the guide's table. Write P3's question, observable and threshold. Apply the guide's three changes (tutorial chain, smaller customization, bounty board) and confirm the revised row. The checker should print `PASS`.
2. **Your pillars.** Replace the starter pillars with your own two to four, plus at least two anti-pillars. Mark in the `text` column which pillar is about players together and which depends on persistence.
3. **Test lines.** Give every pillar a question, an observable and a threshold. Commit `pillars.csv` now. The threshold must be in the history before week 4 work starts.
4. **Your features.** Each discipline's primary lists its features with hours. The producer moves foundation work to `kind = foundation` rows.
5. **Weights.** Assign weights as a team. For every partial weight, ask the cut question from the guide and record the answer in a `why` column you add.
6. **Audit.** Run the checker. Save the first output as `audit-before.txt`.
7. **Revise.** Cut, reshape or add features until it passes. Each change goes into `changes.md` with the hours freed or added and where freed hours went. Save the final output as `audit-after.txt`.
8. **Capacity check.** Add feature and foundation hours, and compare the total with your week 1 team capacity. If the total is larger, the audit passing does not mean the plan fits. Say so in `changes.md` and name what goes next.

If you choose different thresholds, state them and why at the top of `changes.md`, and run the checker with the matching flags.

## Deliverable

In `preproduction/week03/` in the team repository:

- `pillars.csv`, `features.csv`, `audit-before.txt`, `audit-after.txt`, `changes.md`.

In `docs/`: the one-page vision and pillars page (`vision.md`) and the one-page art direction page (`art-direction.md`) described in the guide's Deliverables section.

**Checkable output:** the instructor reruns `check_pillars.py pillars.csv features.csv` with the flags stated in `changes.md`. It must print `PASS`, exit with code 0 and match `audit-after.txt`. The commit that added the pillar thresholds must be dated before the week 4 studio session.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Checker passes | 3 | `PASS` on rerun; output matches |
| Pillars | 4 | Each rules something out; one is about players together; one depends on persistence; anti-pillars are real choices |
| Test lines | 4 | Every pillar has an observable a prototype can produce and a threshold committed before week 4 |
| Honest weights | 3 | Partial weights have a `why`; foundation is separated |
| Revision | 4 | Change log shows before and after, hours moved, and where freed hours went |
| Capacity check | 2 | Total compared with week 1 capacity, with the consequence stated |
