# MMO404 review: open items

Items the September 2026 review could not fix inside its scope.

| File | Problem | Proposed fix |
|---|---|---|
| `syllabus.md` | Still carries the generated-stub marker. The review was told not to edit it or run `tools/build_plan.py`, which rewrites `PLAN.md`. | Orchestrator runs `python tools/build_plan.py` and hand-finishes the syllabus. The schedule links to all 14 lectures and examples already resolve. |
| `lectures/w14-case-study-presentations.md` | The hook opens with B-R5RB, which is also week 1's hook. Week 14 uses it as data for the B-R5RB vs FWST-8 comparison, so the worked example is different, but the opening repeats. | Open week 14 with FWST-8 and bring in B-R5RB as a callback to week 1. |
| `lectures/w04-replication-prioritization-and-relevancy.md` | The Tribes networking paper (Frohnmayer and Gift) is cited without a GDC date. No dated source was found. | Find the GDC proceedings year, or keep the paper cited as undated. |
| `lectures/w09`, `lectures/w03` | Star Citizen "about 100 players per server before Alpha 4.0" could not be verified. The lectures do not depend on it. | Verify against a Cloud Imperium source, or leave it out. |
| `lectures/w06-massive-battles.md`, `lectures/w08`, `lectures/w10` | Week 6 now links CS202 week 12 for lockstep and Age of Empires. Weeks 8 and 10 also open their hooks by recalling Age of Empires. Each week's worked example is different (fan-out, lookahead, consistency), but students meet the same case three times. | Consider a different opening case for week 10, for example a shooter's client prediction first. |
