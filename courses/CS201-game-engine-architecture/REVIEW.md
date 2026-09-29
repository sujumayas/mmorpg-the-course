# CS201 review: open items

Reviewer pass, September 2026. Everything else found in review was fixed in place. These items need the orchestrator or a later pass.

## 1. Syllabus still carries the generated-stub marker

- **File:** `syllabus.md`
- **Problem:** `tools/check_course.py CS201` reports the stub marker. The reviewer was told not to edit the syllabus or run `build_plan.py`. All 14 lecture and example links in the schedule table already resolve.
- **Fix:** run `python tools/build_plan.py` or `tools/finish_syllabus.py`, then remove the marker when the syllabus is hand-finished.

## 2. Facts not re-verified in this pass

- **Mantle draw-call claim (w08).** "Up to nine times more draw calls per second", cited to Wikipedia "Mantle (API)". Wikipedia's API rate-limited the reviewer. Proposed fix: confirm on the page, or soften to "many times more" if the figure is not there.
- **Tracy zone cost 2.25 ns and default sampling rates (w13, example w13).** Cited to Tracy's manual. Not opened in this pass. Proposed fix: check `manual/tracy.tex` for the benchmark table.
- **Apple M4 Pro cache figures (w06).** 128 KB L1D, 16 MB L2 per five-core cluster, 128-byte lines. Read with `sysctl` on the author's reference machine; not independently checked.
- **Gregory chapter and section numbers (all weeks).** Taken from the 3rd edition table of contents only (author note). A reviewer with the book should spot-check sections 1.6, 3.5, 6.1, 6.2, 8.6 and chapter 16.
- **Unity 6.6, Unreal 5.8, Godot 4.7 documentation claims.** Taken from current docs by the authors. Spot checks passed for Godot exports (RPC transfer), Godot 4.3 sleep settings, Box2D v2.4.1 and v3.1.0 constants, the Unity "10000 Update() calls" figures, Factorio's Lua sandbox, Minecraft data versions, Doom and Quake line counts, EASTL N2271 and the Android frame-pacing example.

## 3. Cross-course item outside CS201

- **File:** `courses/MMO404-advanced-networked-simulation/lectures/w11-physics-in-mmos.md`
- **Change made:** added a prerequisite link to CS201 week 11 and a one-line pointer before MMO404 restates sleep and islands. MMO404's own reviewer should confirm the wording and consider trimming its definition paragraph further, since CS201 week 11 now teaches it in full.

## 4. Forward references to later courses

- CS202, CS203 and DB201 run in semester 4, after CS201. Weeks 4, 9, 10, 12 and 13 cited them as prerequisites. They are now marked "next semester" or "looking ahead", and w10 and w12 define lockstep, time-slicing, little-endian and the atomic write inline. If the program ever moves CS201 later than those courses, restore them as prerequisites.

## 5. Lab solutions

- Reference solutions for all 14 labs were written in the reviewer's scratchpad to confirm the tests pass; they are not stored in the repo. If instructors need them, keep them in a private instructor repo, not under `labs/`.
