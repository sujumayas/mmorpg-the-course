# CS102 review: open items

Reviewer pass, 28 September 2026. Everything listed in the author notes was fixed in place. These items need an author or the orchestrator.

| File | Problem | Proposed fix |
|---|---|---|
| `lectures/w11-state-and-state-machines.md` | **Done, 28 September 2026.** Hook and worked example rewritten around Super Mario 64's jump chain (`m->action`, 4-frame landings, `doubleJumpTimer` 5, triple jump needs speed above 20), verified from the n64decomp source. Pac-Man is now a short cross-game section that links CS101 week 11 and says what CS102 adds. New example `examples/w11-triple-jump-window.html` built to the new spec and checked (check_examples plus a Playwright check of every spec test value). Lab 11 step 5, its starter and tests, check-yourself answers and exam-bank questions 48, 49 and 51 now use the jump-chain numbers. | `syllabus.md` still links `examples/w11-ghost-modes.html`. That file is kept (the cross-game section links it) but the syllabus row should point at `w11-triple-jump-window.html`. Orchestrator to update. |
| `lectures/w02`, `w05`, `w09`, `w10`, `w11`, `w12` | Links to CS201 (weeks 5, 6, 9), CS203 (week 7) and MA201 (week 14) still point at those courses' syllabi, because no lectures exist on disk yet. | Upgrade when those lectures are written. |
| `lectures/w08-graphs-maps-and-dialogue.md` | Mentions "CS203 weeks 3 and 4" and "GD202 week 4" as plain text with no link. | Add links when those lectures exist. |
| `labs/lab02/`, `labs/lab03/` | **Done, 28 September 2026.** Lab 02 ships `test_mine.py` (`make("mine")` must not raise, and the mine explodes on the first overlap). Lab 03 ships `test_table_agrees.py` (table and classes agree on the starter materials). Both fail on the starter and pass on reference solutions, run with `.venv/bin/python -m unittest`. Handouts updated. | None. |
| `labs/lab04.md`, `labs/lab05.md` | **Done, 28 September 2026.** Lab 04 `proximity.py --check` asserts `naive_pairs` and `grid_pairs` agree on hits for uniform and clustered layouts at two radii and for the step 9 mixed-cluster layouts. It exits 1 on the starter (no `cluster_fraction_units`) and 0 on a solution. Handout updated. | None. |
| `syllabus.md` | Still carries the generated-stub marker (reviewer did not edit it, per instructions). | Hand-finish the syllabus. |
