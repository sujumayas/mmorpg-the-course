# MMO302 review: open items

Items the course reviewer could not fix inside the course folder. Everything else from the QA pass was fixed in place.

| File | Problem | Proposed fix |
|---|---|---|
| `syllabus.md` | Still carries the generated-stub marker. The reviewer was told not to edit it. | Orchestrator runs `python tools/build_plan.py` (or `tools/finish_syllabus.py`) for MMO302. |
| `lectures/w13-cloud-deployment-and-autoscaling.md`, `lectures/w14-observability-logs-metrics-traces.md` | Links to the MMO407 and MMO308 syllabi remain, because MMO407 week 2 and MMO308 week 13 have no lectures yet. | Upgrade to lecture links when those weeks are written. |
| `examples/w14-tick-tail.html` | Opens on random ticks (seed 1). The measured stall count at 2% spikes varies with the seed (28 at seed 1), so the lecture now describes it as "high 20s" and quotes the exact formula value 24 separately. | Optional: add a first-screen line to the w14 spec and open on the "Lecture data" set. |
