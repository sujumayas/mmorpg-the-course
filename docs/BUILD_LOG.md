# Build log

## 2026-09-26 — Session 1 (claude.ai chat)
- Researched course architecture (IGDA framework, DigiPen, Bartle's Essex module, Castronova, Lehdonvirta & Castronova).
- Wrote curriculum.yaml (39 courses, 585 weekly topics, 72 signature worked examples), PLAN.md generator, all 39 syllabus stubs.
- Wrote STYLE_GUIDE.md, ORCHESTRATION.md, subagent definitions.
- Built the exemplar: MMO303 week 2 lecture + interactive (tested desktop/mobile, no console errors).
- Verified: LoL armor K=100; WoW classic K=400+85×level (1–59), 75% cap; Diablo II chance-to-hit; PoE2 armour A/(A+10×hit), 90% cap.
- Correction made during build: PoE1 uses a different multiplier than PoE2 that changed across patches — lecture now cites PoE2 only.

## Next
- Wave 1 per ORCHESTRATION.md: MA101, MA102, GD203, MMO303 (remaining 13 weeks).
- Open questions for the program owner: see docs/00-course-architecture-research.md §5.

## 2026-09-28: Session 2 (Claude Code, orchestrated build)
- Setup: git repo initialized, `.venv` with pyyaml + playwright, initial commit.
- Added `tools/check_course.py` (course linter), `tools/check_examples.py` (headless 390px/1280px, light/dark), richer build status in `build_plan.py`, and `docs/BUILD_CONVENTIONS.md` for parallel agents.
- Decision: lab files are `labs/labNN.md` with NN = the week that assigns the lab. Week 15 gets no lecture.
- Decision: prose follows the owner's plain-writing rules (no em dashes). The template title line keeps its `—`.
- The exemplar (MMO303 w02) was 2,159 words, lacked the prerequisites line and used em dashes. The MMO303 reviewer brings it to standard.
- Wave 1 started: MA101, MA102, GD203, MMO303 (20 author agents).
