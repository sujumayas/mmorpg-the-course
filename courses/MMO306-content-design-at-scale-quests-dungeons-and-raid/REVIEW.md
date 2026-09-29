# MMO306 review: open items

Reviewer pass, September 2026. Everything below was left open on purpose. Fixes that were made in place are not listed.

| File | Problem | Proposed fix |
|---|---|---|
| `syllabus.md` | The file still has the generated-stub marker. Reviewers may not edit it. | The orchestrator hand-finishes it and runs `tools/build_plan.py`. The schedule links already resolve to all 14 lectures and examples. |
| `lectures/w12-content-tooling-and-pipelines.md` | Links to CS201 weeks 7 and 14 go to CS201's `syllabus.md`, because CS201 has no lectures yet. | Upgrade to lecture links once CS201 weeks 7 and 14 exist. |
| `lectures/w13-content-budgets-and-cadence-planning.md` | The link to PR101 week 6 goes to PR101's `syllabus.md`, because PR101 has no lectures yet. | Upgrade once PR101 week 6 exists. |
| `lectures/w09-procedural-and-systemic-content.md` | MMO301 week 10 already teaches `M_eff = 1 / Σp²`, the birthday approximation and `n_50` for avatar looks. Week 9 now links to it and says it reuses the model, but it still restates the formulas in full. | Done. The model block is now a four-line recap linked to MMO301 week 10's derivation. Week 9 keeps its own additions: runs over time instead of a crowd, and the memory rule (`n_50 + k`), now with simulated numbers, a check-yourself question and spec test values. Lab 09, the exam bank and the example HTML needed no changes. |
| `lectures/w10-player-generated-content.md` | Paragon Wiki, Neverwinter Wiki and Super Mario Wiki sources have no URLs. The September 2015 end of the Foundry daily reward was not re-checked in this pass. | Add URLs and confirm the date on the Neverwinter Wiki "Foundry" page. |
| `lectures/w14-accessibility-in-group-content.md` | The "Story mode" details (nine NPCs, from week two) and the Duty Support coverage as of patch 7.5 were not re-fetched in this pass. The author's report also left out the WoW 10.0.5 colourblind change and the FFXIV colour filter. | Spot-check the two wiki pages before the next release. |
