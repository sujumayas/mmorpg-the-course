# MMO406 review notes

Reviewed September 2026 against ORCHESTRATION.md §4 and docs/BUILD_CONVENTIONS.md. These items were left open because they need a source or a decision that the reviewer could not settle.

| File | Problem | Proposed fix |
|---|---|---|
| lectures/w01, w02, w04, w05, w06 (Before class) | The Wolf chapter titles match the Routledge contents page. The sub-parts named inside chapter 3 (maps, natural world, timelines, culture and language, mythology and philosophy) come from memory. No online contents list below chapter level could be fetched. | Check against a library copy and add page ranges. The pointers already tell students to use the contents page. |
| lectures/w12, Sources (Harbingers) | The Warcraft Wiki dates the first short 21 June 2016. Its own source announces the Comic-Con panel as upcoming on 11 July 2016. The lecture says July 2016. | Confirm the exact premiere day from a Blizzard news post, if the course ever needs the day. |
| labs/lab08 to lab14 tests | The docstrings say the tests run "or with pytest", but pytest is not installed in `.venv`. Running the file as a script, as each brief says, works. | Install pytest in `.venv`, or remove "or pytest" from the docstrings. |
| syllabus.md | The generated stub marker is still present. The schedule links all resolve. | The orchestrator finishes the syllabus and runs `tools/build_plan.py`. |
