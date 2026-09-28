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
- MA101 complete (2026-09-28): 14 lectures, 14 examples, 14 labs with starter code in `labs/starter/`, 5 assessment files. Reviewer fixes: w03 cubic value, w04 halfway level (90 not 89), w06 Dota armor dated 7.20-7.26, w07 ability-haste cap (500) corrected. RuneScape XP totals verified: 6,517,253 at 92, 13,034,431 at 99.
- Tooling: `tools/finish_syllabus.py` finishes a syllabus (links, labs, assessments, removes stub marker). The example checker blocks Google Fonts so it cannot hang offline. Week 15 rows link the assessments.
- Environment: the Mac slept once mid-run and killed four builders; they were resumed. `caffeinate` now keeps it awake.
- GD203 complete (2026-09-28): 14 lectures, 14 examples, labs incl. `lab10-reference.md`, 4 assessment files. Reviewer + fact-check fixed the Doom single-roll figure (about 65%), w10/w11 wording, Minecraft armor (checked on minecraft.wiki), Mythic+ scaling (10% per key level, patch 7.2.5), Oblivion slider (6x / 1/6, UESP), WoW Classic stat rates (unsourced Stamina rate replaced by a generic k).
  - Open question for the owner: `spreadsheet-labs-brief.md` gives lab 10 no late window, because its reference sheet is released at the lab 10 deadline. Confirm or change.
- Note: WebSearch hit a session-wide limit partway through. Agents now fall back to WebFetch on known pages and wiki APIs (added to BUILD_CONVENTIONS).
