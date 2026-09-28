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

## Links

- Relative links only. From a lecture, another course's lecture is `../../<CODE>-<dir-slug>/lectures/wNN-<slug>.md`. Course directory names are the folders under `courses/`.
- If the lecture you want to link has not been written yet, link to that course's `syllabus.md` and name the week in the text ("MA101 week 6"). The reviewer upgrades these later.

## Facts

- Verify every real-game number with web search and cite it with version or era. Prefer official sources, then maintained wikis.
- If a fact cannot be verified, redesign the example so it does not need it. List it in your report so it goes to `docs/BUILD_LOG.md`.
- No invented quotes. At most one short quoted phrase per source.

## Parallel work

- Several agents write the same course at once. Touch only your assigned weeks, their labs and their examples. Do not edit `syllabus.md`, `PLAN.md`, `docs/BUILD_LOG.md` or other agents' files; the orchestrator does that.
- Keep your final report under 200 words: files written, facts you could not verify, cross-course links to check.
