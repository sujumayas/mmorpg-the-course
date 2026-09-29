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

## Fact sweep (29 September 2026)

Verified 3, hedged 1, removed 0.

- Verified. Tracy figures (w13) against `manual/tracy.tex` on the master branch (latest release v0.14.1, 22 August 2026). The 2.25 ns zone cost, the 300 ns to 1 µs OS timer range, 8 kHz on Windows and 10 kHz on Linux and Android, and the "sample first, instrument later" advice are all in the manual. The Sources line now carries the date and release.
- Verified. Mantle "up to 9 times more draw calls per second" (w08) is on Wikipedia "Mantle (API)", which cites AMD's GPU14 Tech Day livestream of September 2013. The livestream itself could not be watched. The lecture already presents it as AMD's claim, and the Sources line now names the event.
- Verified. Gregory 3rd-edition section numbers in every week match the author's contents page (gameenginebook.com/toc.html, Internet Archive copy of 7 November 2020). Vague pointers were made exact: w10 section 16.9, w11 section 13.5, w12 sections 16.3 and 16.4, w13 section 2.3. The live site now lists a 4th edition, so the course keeps "3rd ed." on every pointer.
- Hedged (no text change). Apple M4 Pro cache sizes (w06). Apple publishes no cache figures. The lecture already states them as a `sysctl` reading on the reference machine, which is exactly what is known.
