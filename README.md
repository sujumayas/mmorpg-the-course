# Game Development Curriculum — MMORPG Specialization

A complete university course-materials repository: a four-year BSc in Game Development whose first two years build the full foundation (design, programming, math, art, audio, production) and whose last two years specialize in MMORPG development — virtual worlds, server architecture, combat and class balance, virtual economies, social behaviour, content at scale, live operations, security, and the ethics and business of running persistent worlds.

Every concept is taught through **worked examples from shipped games**, in the style of short explainers like candlesan's breakdown of the armor formula `Armor / (Armor + K)`: one model, real numbers, an interactive you can move, the same idea recognized across several games, and an honest design judgment.

## Start here

| File | What it is |
|---|---|
| `PLAN.md` | The full program: curriculum map, prerequisite graph, every course's outcomes, 15-week topics, signature examples, readings and assessment, plus build status |
| `docs/00-course-architecture-research.md` | Why the program is shaped this way: IGDA framework, benchmark programs, MMO literature |
| `STYLE_GUIDE.md` | The authoring standard every lecture and interactive follows |
| `courses/MMO303-…/lectures/w02-armor-and-damage-mitigation.md` | **The exemplar lecture** |
| `courses/MMO303-…/examples/w02-armor-curve.html` | **The exemplar interactive** (open in any browser) |
| `ORCHESTRATION.md` | How to generate the remaining courses with Claude Code subagents, and the QA checklist |
| `curriculum.yaml` | Source of truth; `tools/build_plan.py` regenerates `PLAN.md` and every syllabus |

## Program at a glance

- **39 courses**, 8 semesters, 15 weeks each
- **Years 1–2 (core):** 20 courses across design, programming, math, art, audio, production
- **Years 3–4 (MMO track):** 19 courses organized in six pillars — worlds, technology, balance, economy, society, operations
- **72 signature worked examples** specified; each becomes an interactive

## Repository layout

```
courses/<CODE>-<slug>/
  syllabus.md        generated, links lectures/examples as they appear
  lectures/          wNN-<topic>.md
  examples/          wNN-<name>.html  (self-contained interactives)
  labs/              labNN.md
  assessments/       briefs, rubrics, exam bank
docs/                research and build log
templates/           shared design tokens for interactives
tools/               generators
.claude/agents/      subagent definitions for scaling the work
```
