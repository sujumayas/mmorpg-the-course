# Build conventions for subagents

`STYLE_GUIDE.md` sets the standard. This file fixes the details that many parallel agents would otherwise decide differently.

## Tools

- Python is `.venv/bin/python` (has pyyaml and playwright). Do not install packages globally.
- `tools/check_course.py <CODE>` lints a course: word counts, template sections, links, `(verify)`, em dashes, lab and exam counts, syllabus state.
- `tools/check_examples.py <files>` loads examples headless at 390px and 1280px in light and dark mode. It reports console errors, horizontal overflow and missing focusable controls, and saves screenshots to `/tmp/example-shots/`.
- `tools/build_plan.py` regenerates `PLAN.md` and fills schedule links in syllabi that still carry the stub marker.

## File names

- Lectures: `lectures/wNN-<topic-slug>.md`, NN is the two-digit week (01-14). Week 15 is exam/showcase and gets no lecture; the assessments cover it.
- Examples: `examples/wNN-<name>.html`, NN is the week of the lecture that specifies it.
- Labs: `labs/labNN.md`, NN is the week that assigns the lab. A course needs at least 6.
- Assessments: `assessments/exam-bank.md` (at least 40 numbered questions `1.` `2.` ... with answers in `<details>` blocks), plus `assessments/<name>-brief.md` for each graded assignment in the course's assessment line, each with a rubric table.

## Writing

- Plain writing, per the program owner. No em dashes in prose; use periods or commas. The one exception is the lecture title line, which keeps the template form `# CODE · Week NN — Title`. Table cells may use `—` for "no value".
- No filler words (crucial, delve, enhance, foster, leverage, utilize, showcase, pivotal, additionally). No "not just X, but Y". Name the number or the mechanism.
- Second person, jargon defined on first use.
- The header block has four bold lines in this order: `**Why this matters:**`, `**You will be able to:**`, `**Before class:**`, `**Prerequisites from earlier courses:**`. Add `**Interactive:**` with the example link when there is one.
- Put each interactive spec under `## Interactive spec: examples/wNN-<name>.html` at the end of the lecture, after Sources. Word counts exclude the spec.

## Code

- Code blocks in lectures must run as shown and print what the lecture says. Run every Python block with `.venv/bin/python` before you finish. Watch float comparisons: use integer ticks or an explicit tolerance.
- Lab starters must run; their tests must fail on the starter and pass on a correct solution.

## Links

- Relative links only. From a lecture, another course's lecture is `../../<CODE>-<dir-slug>/lectures/wNN-<slug>.md`. Course directory names are the folders under `courses/`.
- If the lecture you want to link has not been written yet, link to that course's `syllabus.md` and name the week in the text ("MA101 week 6"). The reviewer upgrades these later.

## Facts

- Verify every real-game number with web search and cite it with version or era. Prefer official sources, then maintained wikis.
- If a fact cannot be verified, redesign the example so it does not need it. List it in your report so it goes to `docs/BUILD_LOG.md`.
- If WebSearch is unavailable or rate-limited, verify with WebFetch on known pages instead: official sites, wiki API endpoints (for example `https://<wiki>/api.php?action=parse&page=<Page>&format=json`), or source code on GitHub. Never skip verification because search failed.
- No invented quotes. At most one short quoted phrase per source.

## Parallel work

- Several agents write the same course at once. Touch only your assigned weeks, their labs and their examples. Do not edit `syllabus.md`, `PLAN.md`, `docs/BUILD_LOG.md` or other agents' files; the orchestrator does that.
- Keep your final report under 200 words: files written, facts you could not verify, cross-course links to check.

## Studio courses (PR201, PR301, PR401, PR402)

Studio courses are team projects. Per ORCHESTRATION.md they are mostly briefs, milestones and rubrics, so each week is a studio session guide, not a lecture.

- `lectures/wNN-<slug>.md` is the session guide, 1,500 to 4,000 words. Header block as for lectures. Sections: `## 1.` to `## N.` short teaching blocks, one `## N. Worked example` (a real production calculation: burn-down, velocity, scope cut, bug triage, playtest sample size), `## Studio session plan` (timed agenda for the class meeting), `## Deliverables` (what the team hands in this week and how it is checked), `## Common failure modes`, `## Review checklist` (what the instructor checks at the milestone), `## Sources`.
- An `## Interactive spec` is optional. Add one only where a model helps (burn-down, scope, risk).
- `labs/labNN.md` is a sprint worksheet or template (at least 6), with a checkable output.
- `assessments/` holds one brief per milestone with a rubric totalling 100, a peer-assessment brief, and `exam-bank.md` as a viva and reflection bank of at least 40 numbered questions with model answers or marking guidance.
- Link to the courses that teach each skill (CS202 networking, PR101 production, GD201 levels) instead of re-teaching them.
- `tools/check_course.py` applies these rules to the studio course codes.
