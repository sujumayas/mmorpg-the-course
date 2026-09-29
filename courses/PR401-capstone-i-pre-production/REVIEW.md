# PR401 review

Reviewer pass on 29 September 2026 against ORCHESTRATION.md §4, the studio-course rules in docs/BUILD_CONVENTIONS.md and docs/handoff/notes-PR401.md.

## What was fixed

- **Pillar count.** The course uses two to four pillars. Week 6 said three to five; it now says two to four, matching week 3, lab 03, `check_pillars.py` and the m03 rubric.
- **Towns.** Week 10's final design is now four towns of about 22 (levers 1, 3 and 4). That gives 0.84 of evenings without the militia and 0.985 with it. The draft (six towns of 15) is unchanged. Week 11 now says its three extra towns make the four that week 10 needs. Week 14 adds that three towns of 30 hold 96% of evenings without the militia. The w10 example's "Emberfall final" preset (M = 22, readout 0.986, 4 towns), the spec test values, `lab10-starter/liquidity.csv`, the m10 brief and exam question 36 were updated to match.
- **Quest chain.** Week 9's must-have unit is now the "tutorial quest chain", and a bullet explains it is the only quest chain Emberfall launches with. Week 12 and the m12 brief name it as the slice's quest chain. `lab09-starter/content.csv` was renamed too, and the checker still reproduces the guide.
- **Safety at week 14.** Week 14's review checklist now checks all eight week 10 safety minimums. The m13 evidence table has a matching row.
- **Folders.** One convention now applies, stated once in week 1. Each week's hand-in goes in `preproduction/weekNN/`. Living documents go in `docs/`, game data in `data/`, and builds in `prototypes/p1/` and `prototypes/p2/`. All guides, labs 01 to 10 and briefs m01 to m10 were updated. No `production/weekNN` or `docs/<topic>/` folder paths remain.
- **Risk buffer.** Week 4 now calls 104 a forecast. Week 6 re-rates the risks to 54, and week 11 reserves 54. Week 6 now itemises how 104 became 54 (R1 −20, R3 −24, R2 −3, R4 −6, R5 −3, R6 −6, R7 +12). The w04 example text and lab 04 say the same. The checkers and the 224/140/104 burn-down are unchanged.
- **Art bible.** Week 3 now produces a one-page art direction page, the start of the art bible, in section 3, the deliverables and the review checklist. It is also in lab 03, and in m03's deliverables, evidence and rubric row, with the rubric still totalling 100. Week 12 cites that page.
- **Notation.** Week 2's realized-price factor is now `φ` (guide, lab 02, the `--phi` flag in `check_comps.py`, m02, exam question 5). `ρ` is now used only for intra-group correlation (week 5).
- **Week 10 table.** In the M = 20 row, P(≥ 4) is now 0.77 (0.7748 at p = 0.25).
- **Team.** The team is Emberfall with 7 students throughout. No Saltmarch, Driftmoor or "six of you" remains.
- **Syllabus links.** Links that pointed to another course's syllabus now point to lectures: PR301 weeks 3, 4 and 13, and MMO302 week 11, in weeks 1, 4, 6 and 11. The PR402 schedule link in week 11 stays on the syllabus on purpose, because it points to the schedule.
- **Week 1, check yourself 1.** The answer said more content "bought less than a quarter of the gap". It closes about 70% of it (L falls from 1.62 to 1.18). Corrected.
- **Week 2.** Added a hedge on Mortal Online 2's business model (see below) and dated the review-count method in the sources.
- **Week 13.** The prerequisite links read well and all resolve. No change.

## Checks run

- Every table in weeks 1 to 14 was recomputed. All values match, except the two fixed above (week 1 answer 1 and the week 10 M = 20 cell).
- All 14 lab checkers were run on their starters, and their numbers match the guides.
- The peer-assessment script reproduces its printed output exactly.
- The examples were read headlessly. Their defaults match the guides, and so does the w10 final preset.
- `tools/check_examples.py` passes all 6 examples. Every relative link in the course resolves.
- `tools/check_course.py PR401` reports only the syllabus stub marker and `_todo_` example cells. Clearing them needs the orchestrator's `finish_syllabus.py` step and "—" in the example cells for weeks without an interactive. I was told not to edit the syllabus schedule, so I left it.

## Verified facts (29 September 2026)

- Steam review totals and US prices for app IDs 1170950, 3107230, 342940 and 761890 match the week 2 table exactly (13,925, 5,108, 5,080 and 94,048). The same goes for the prices, release dates, the Pantheon pledge-holder note and the short descriptions quoted in week 3.
- New World SteamCharts figures: October 2021 average 410,171 and peak 913,027, January 2022 about 65,107, June 2022 about 13,615.
- GameDiscoverCo NB-number figures (Carless, 3 August 2020).
- The Titan timeline, the OSRS Grand Exchange tax history and the WoW Classic layering dates.
- Guild Wars 2 Living World Season 1 dates, the FFXIV 19-week patch cadence and the 7.0 to 7.3 dates, and Call to Arms (4.1.0, 26 April 2011).

## Still unverified

- Whether Star Vault sells Mortal Online 2 outside Steam, or runs any subscription beyond the one-time Steam price. The guide now hedges this.
- That Project: Gorgon's Steam announcements date from April 2018. Only recent events were fetched.
- Amnesia Fortnight. The Wikipedia summary gives 2010 for both Costume Quest and Stacking. The guide says Stacking is 2011, which I believe is correct (February 2011), but it was not confirmed from a source this pass.
- The EVE Online time-dilation dev blog date (22 April 2011), the Singularity mass-test rewards, the WoW Classic stress-test dates, EverQuest mercenaries (2008), the Horizon Zero Dawn GDC 2017 session, the Polygon report of Yoshida's GDC 2014 talk and Wright (1936). None were re-checked this pass because the web search budget ran out.
- Facts week 8 cites through MMO304 (the WoW Token) and the Diablo III auction house dates. These were not re-checked.

## Open items for the orchestrator

- Finish the syllabus: run `finish_syllabus.py PR401` and replace `_todo_` example cells with "—". Then `check_course.py PR401` should print OK.
- `k` means three things in this course: the authoring ratio (weeks 1 and 9), group size (week 5) and the interest cap (week 7). Each week defines it locally, so it was left as is. Rename the week 7 cap to `a` if a later pass wants no overlap.
- Week 6 computes capacity as H = 112 hours per person over the build window, while week 11 uses the weekly model (12 × 8 × f). The two agree, but week 6 could show the weekly form.
