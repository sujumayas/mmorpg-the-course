# PR201 · Lab 03: Technical design document and risk register

**Week:** 3 · **Time:** 2 hours in the studio session plus about 4 hours as a team · **Weight:** [milestone 2, technical design document](../assessments/m2-technical-design-document-brief.md)

## Objective

Write version 1.0 of your team's TDD and a risk register that ranks spikes by return, then choose the sprint 1 spike list. The model is in section 2 of the [week 3 guide](../lectures/w03-technical-design-document.md).

## Starter materials

Folder `lab03-starter/`. Standard library Python only.

- `tdd-template.md`: the twelve TDD sections from the guide, each with an owner line and prompts. Sections 11 (persistence) and 12 (tracking plan) feed alpha criteria A2 and A6. Version 1 of section 11 is a documented save format and a file save with an atomic write. The database version comes at alpha.
- `risks.csv`: `id`, `risk`, `owner`, `p`, `loss_h`, `spike_h`, `p_after` and `spike_question`. The starter holds the six *Hollowmarch* risks, with R6's owner missing.
- `check_risks.py`: computes exposure, spike value, net and return, funds spikes from the top within `--budget` (default 20), and checks owners, probabilities and that each spike question ends with a question mark.

## Steps

1. **Reproduce the guide.** Run `python check_risks.py risks.csv`. It prints `NOT READY`, because R6 has no owner. Give R6 to Fay, the producer who owns the build, and rerun. Confirm `PASS`, total exposure 68 hours and the spike list R4, R3, R1, R6 for 15 hours.
2. **Late discovery.** Change R2's `loss_h` to 80 and rerun. Report the new order and which spike drops out of the budget. Change it back.
3. **TDD sections.** Fill in `tdd-template.md` as `docs/tdd.md`. Each section's owner writes it. Art and audio write their own pipeline sections. Write version 1 of persistence now: the save format with a version field, one example file, and a save routine that writes a temporary file, flushes it and renames it over the old one ([CS201 week 12](../../CS201-game-engine-architecture/lectures/w12-serialization-and-save-files.md), [DB201 week 1](../../DB201-data-persistence-and-telemetry/lectures/w01-why-persistence-is-hard-in-games.md)). Kill the server during a save once and record that the file still loads. Name six server-side events for the tracking plan, each with its question. Both sections get version 2 for alpha, after DB201 weeks 2 to 6 and 10.
4. **Bandwidth.** In the rates section, compute bytes per snapshot, per-client download and server upload for your slice, as in section 3 of the guide. Set the send rate in the TDD, and in the project if it exists.
5. **Risks.** Each person writes risks alone for 10 minutes. Merge, then estimate `p`, `loss_h` (the cost if found at the date you would find it), `spike_h` and `p_after`. At least six risks.
6. **Swap.** Exchange registers with another team. Add at least one risk they missed, and challenge one loss estimate with a reason.
7. **Rank and decide.** Run the checker with your budget. For every accepted risk, write a watcher and a fallback. For every deferred spike, write the date it runs and the loss that applies if it slips.
8. **Tag.** Commit the TDD, the register and your locked scope sheet, and tag `tdd-1.0`.

## Deliverable

`docs/tdd.md`, `docs/risks.csv`, the checker output in `docs/risks.md`, the step 2 result, and the tag `tdd-1.0`.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| TDD decisions | Every section is a decision about this slice, with an owner and a reason; no bare TBD | Most sections decided | Engine tutorial or mostly TBD | 30% |
| Networking numbers | Topology, authority, tick and send rates, per-client bandwidth computed and consistent with the replication list | Numbers present, one inconsistent | Missing | 20% |
| Pipelines | Art and audio sections written by their primaries with scale, naming and import settings | Present but generic | Missing | 15% |
| Risk register | At least six risks, testable spike questions, `check_risks.py` passes, swap additions included | Passes, questions vague | Does not pass | 25% |
| Deferred and accepted risks | Each has a date, watcher or fallback; step 2 explained | Partial | Missing | 10% |
