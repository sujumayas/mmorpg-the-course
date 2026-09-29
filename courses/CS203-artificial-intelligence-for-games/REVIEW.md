# CS203 review: open items

Reviewer pass, September 2026. Everything else found in review was fixed in place.

| File | Problem | Proposed fix |
|---|---|---|
| `syllabus.md` | Still carries the generated-stub marker. All 14 lecture and example links already resolve. | Orchestrator runs `tools/build_plan.py` or finishes the syllabus. Reviewers were told not to edit it. |
| `lectures/w01-game-ai-vs-academic-ai.md` | The Iwatani "single file" phrase is sourced only through Birch (2010), a secondary source. | Keep it as cited via Birch, or find a primary interview and cite that. |
| `lectures/w01-game-ai-vs-academic-ai.md` | Neither source settles Clyde's behavior at exactly 8 tiles. | No change needed. The lecture states the gap, and the lab tests avoid the edge. |
| `labs/lab11-starter/stage.py` | `run_rounds()` lets enemies pick attacks in admission order and stops admitting at the first enemy that does not fit. The interactive's Step button picks heaviest first and skips over enemies that do not fit. | This review documents the difference in `lab11.md` (step 7 builds on the admission difference). If the two should match exactly, change `run_rounds()` to heaviest-first and re-check the rounds-to-600 table (a reference solution now gives 36, 20 and 15 rounds at the default easy, normal and hard settings). |
