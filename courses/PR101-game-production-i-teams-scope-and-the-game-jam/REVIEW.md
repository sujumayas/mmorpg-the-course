# PR101 review: open items

Reviewed September 2026 against ORCHESTRATION.md §4 and docs/BUILD_CONVENTIONS.md. Everything else found in review was fixed in place.

## Outside this course

- **MMO308 week 10 re-teaches capture-recapture.** File: `courses/MMO308-live-operations-analytics-and-experimentation/lectures/w10-*.md`, section "Capture-recapture". PR101 week 10 teaches Lincoln-Petersen first (lab 10 has `lincoln_petersen`). Proposed fix: in MMO308 w10, add a prerequisite link to `../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w10-bug-tracking-and-qa-basics.md` and shorten the derivation to a recap. Not edited here because the review scope excluded MMO308.
- **syllabus.md still carries the generated-stub marker.** The schedule links all resolve. The orchestrator owns this file and `build_plan.py`.

## Design decisions to confirm

- **Notation `L`, `λ`, `W`.** Week 5 uses them for sprint length, wrong-turn rate and capacity. Week 7 and week 10 use them for Little's law (WIP, throughput, cycle time). The review kept both: Little's law is always written `L = λW` (it is the title of the cited 1961 paper), and renaming week 5's symbols would touch its lecture, example, lab and five exam questions. Week 7 now has an explicit notation warning where the symbols are defined, and week 10 has a one-line reminder. If the program owner prefers distinct symbols, rename week 7 to `WIP = TH × CT` and update `examples/w07-wip-limit.html` (readout line) and exam-bank questions 29 to 31 and 47.
- **Week 8 says the jam log will give better `q` values "next week".** Week 9 does not estimate `q`. Proposed fix: either add one line to lab 09 part B (count post-freeze changes that broke the build, divide by post-freeze changes) or reword week 8 to "your post-mortem can check them".

## Minor

- `labs/lab13-starter/test_lab13.py`: `test_fixed_build_passes` passes on the unmodified starter, because the stubs pass everything. The suite still fails overall (1 of 9), and the test is meaningful once the stubs are replaced, so it was left as is.

## Fact sweep (29 September 2026)

- No items were listed as unverified, and no "(verify" tags remain. Real-game facts cite dated Wikipedia articles or the primary sources checked in review (Buehler et al. on Crossref, Kotaku on Anthem, the archived Construx cone page). Nothing was changed.
