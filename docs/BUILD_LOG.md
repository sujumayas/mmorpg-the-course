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
- MA102 complete (2026-09-28): 14 lectures, 15 examples, 14 labs with starters (`labs/starter/`, `lab11-starter/` to `lab14-starter/`), 5 assessment files. Fixes: several table roundings (w08, w10 PRD and gacha), w11 simulation tables regenerated so they reproduce with seed 42, Warcraft III "wrong C values" claim removed (unsourced).
  - Partly verified: SimCity A/B test (Optimizely pages unreachable, attributed only), Halo 3 playtest lab (one attributed sentence), Genshin rates (official notices defer to the in-game Details page), Catan red 6/8 and dots (secondary sources; rulebook covers only the discard rule).
- MMO303 complete (2026-09-28): 14 lectures (w02 exemplar brought to standard: 2,832 words, prerequisites line, no prose em dashes), 15 example files, 14 labs with starter folders and tests, 4 assessment files plus `final-roster.yaml`. Fixes: w05 uses the strict survival rule HP > S(1 − m); w10 rewritten to build on w09 with a new two-guild world boss example; w12 Diablo IV damage-bucket note corrected to Season 13; Midnight DR reset now 20 s since 12.1.0 (2026-08-11); March 4, 2025 hotfix cited to the official Blizzard post.
  - Needs the owner: `examples/w10-counter-triangle.html` is orphaned (week 10's old example, replaced by `w10-world-boss-game.html`). A subagent's delete was blocked, so it is still on disk but unlinked from the syllabus. Delete it if you agree.
- Wave 1 complete: MA101, MA102, GD203, MMO303.
- MMO304 complete (2026-09-28): 14 lectures, 14 examples, labs with data files, 4 assessment files (68-question bank). Reviewer fixes: EVE sales tax at Accounting V is 3.375% (7.5% base since 22.02, EVE University wiki), matching MMO401; w14 doubling the faucet raises W* 2.67× (flat sinks fixed), not 2×; w04 example opens on the 1% sink preset so the insight shows first; w03 unsourced 5.7 trillion item-sink total replaced; money-meeting count 2(G − 1) unified across w09/w10.
  - Still unverified, hedged in text (see the course REVIEW.md): Lehdonvirta (2009) functional/hedonic/social grouping (paywalled); Diablo II clone trigger (community sources); Diablo II death penalty and 35,000-gold vendor cap (Arreat Summit unreachable); PLEX launch date and Guðmundsson tenure (Wikipedia only).
- GD101 complete (2026-09-28): 14 lectures, 14 examples, labs, 5 assessment files (60-question bank). Reviewer fixes: w04 tipping turn 42 (not 41), w10 best-of-67 (not 69), w03 98.1%, Diablo pitch timeline corrected (the text wrongly said Blizzard owned Condor before the real-time request), Fullerton 4th ed. chapters checked against Crossref, Minecraft 300M as of October 2023, venues cited for MDA (AAAI 2004), TF2 (NPAR 2007), L4D (AIIDE 2009).
  - Design note: MA101 runs in the same semester as GD101, so GD101 treats logarithms as a calculator step and does not assume MA101 week 5.
  - Still unverified (course REVIEW.md): Rules of Play chapter numbers and "Rules on Three Levels" title; Fullerton's eight-element list (secondary sources only); 1996 Blizzard-Condor acquisition date; flOw's 20 levels; Celeste speed steps.
- MMO401 complete (2026-09-28): 14 lectures, 14 examples, 14 labs with starters and data, 4 assessment files (69-question bank, labs brief, final brief, scenario cards). Reviewer fixes: w08 deposit ceiling (δ > s means stealing pays at every size; exam Q35 ceiling 50 not 74), w10 stock-build wording, w12 5,901, w07 off-book trades (~36), w08 reserve ratio 80%. EVE 7.5% sales-tax base since 12 March 2025 (release 22.02) confirmed; 3.375% at Accounting V.
  - Still unverified: EverQuest II 2005 dupe primary article (cited via secondary source); Lehdonvirta & Castronova (2014) chapter titles (chapter mapping removed). CCP publishes no definitions for its MER money supply, velocity or price indices; the lectures say so.

## Handoff (usage limit reached, 2026-09-28)
- Complete and committed: MA101, MA102, GD203, MMO303 (wave 1); GD101, MMO304, MMO401 (wave 2).
- GD102: reviewed; a fact-check agent was running. Next: `tools/finish_syllabus.py GD102`, check, commit.
- GS101: all lectures, examples and assessments written; reviewer was running. Then finish and commit.
- Wave 3 in progress: UX201 (weeks 4-6 author was running; then builders, assessments, review), MMO301 (weeks 7-9 author running), MMO305 (weeks 1-3 author running), MMO402 (weeks 4-14 authors running or queued).
- Wave 4 started: CS101 and CS102 authors were running; CS202 weeks 1-3 running. Remaining author tasks are in `docs/handoff/queue.txt`.
- Per-course reviewer notes (known number and wording fixes found by builders) are in `docs/handoff/notes-*.md`. Pass them to each course's reviewer.
- Waves 5-7 not started.
- Process per course: authors (5 batches) → one builder per Interactive spec → assessment writer → reviewer (fixes + reconciles assessments) → `tools/finish_syllabus.py` → `tools/check_course.py` must print OK → commit "<CODE>: complete".
- Owner decisions pending: delete orphaned `courses/MMO303-*/examples/w10-counter-triangle.html`; confirm GD203 lab 10 has no late window.
