# PR401 · Milestone 1 brief: the capstone pitch

**Weight:** 6% of the course grade, inside the pitch component (20%).
**Assigned:** week 1. **Due:** before the week 2 studio session, in `preproduction/week01/`, with the pitch draft and claims sheet in `docs/`. **Reviewed:** at the start of week 2.
**Work mode:** team. One team mark, adjusted per person by the [peer assessment](peer-assessment-brief.md).
**Session guide and lab:** [week 1, pitch development](../lectures/w01-pitch-development.md) with [lab 01](../labs/lab01.md).
**Builds on:** [PR301 week 1, pitch and world pillars](../../PR301-mmo-studio-project-i-persistent-world-prototype/lectures/w01-pitch-and-world-pillars.md) (the persistence promise), [MMO403 week 14, pitching to publishers and investors](../../MMO403-business-monetization-and-ethics-of-live-games/lectures/w14-pitching-to-publishers-and-investors.md), sections 1 and 4 (what a funder is buying), and [PR101 week 4, scope and cut lists](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w04-scope-mvp-vertical-slice-cut-lists.md).

## What this milestone proves

That your team has pitched a game it can fill for four weeks of live operation in PR402, and that it knows which claim the pitch rests on. The week 1 guide showed that the *Emberfall* pitch passed its content test only because the team wrote `r = 8`, a number nobody had measured. Naming that claim and tagging it "assumed" earns marks. Hiding it does not.

This milestone does not mark how original the idea is. A plain pitch with an honest claims sheet scores higher than a striking one whose median `L` is 1.6 with no explanation.

## Deliverables

In `preproduction/week01/` in the team repository, except the pitch draft (`docs/pitch.md`) and the claims sheet (`docs/claims.csv`), which later weeks keep updating. The lab 01 rubric is feedback in the studio. This brief sets the milestone mark.

1. **Pitch draft**, two pages plus a one-page numbers appendix, with the seven sections from week 1 section 3: the moment, why persistent and why together, the content engine, the live period, comparables (names are enough this week), team fit, and claims and unknowns.
2. **Pitch sheet** (`pitch.csv`) and the saved output of `check_pitch.py` for the chosen pitch (`check-output.txt`) and for the rejected pitch (`check-output-rejected.txt`).
3. **Claims sheet** (`claims.csv`) with 8 to 15 claims, each with an evidence level (assumed, estimated, tested), a load-bearing flag and an owner.
4. **Team charter update** from PR301, with the two PR301 lessons, the hours convention (`H = 8` in PR401, `H = 12` in PR402) and every member's agreement.

## Evidence required

| Evidence | Format | How the instructor checks it |
|---|---|---|
| Content test | `check-output.txt` | Reruns `check_pitch.py pitch.csv claims.csv` and compares the output |
| Replay threshold | A row in `claims.csv` | Finds `r_needed` for the median player as a load-bearing claim with an owner |
| Sources for `k` and `r` | Notes column of `pitch.csv` | Each value is marked assumed or estimated, with where it came from |
| Rejected pitch | `check-output-rejected.txt` and one sentence in the draft | Reads why it lost |
| Charter sign-off | Names and dates in the charter | Counts names against the team list |

## How it is marked

The instructor reruns the checker, reads the draft and meets the team for 10 minutes at the start of week 2. Any member may be asked to recompute the median player's exhaustion time or explain a claim's evidence level. If only one person can answer, the team ownership row loses marks.

## Rubric

| Criterion | Points | Full marks when | Low marks when |
|---|---|---|---|
| Content test passes | 15 | `PASS` on rerun; median `L ≤ 1`, or a higher value accepted with a written reason | Checker fails, or the saved output does not match |
| MMO scope | 15 | All four MMO-scope requirements from week 1 section 1 are met and the draft says how | "You can see other players" is the only social element |
| Replay claim | 15 | `r` has a stated source; `r_needed` for the median player appears as a load-bearing claim with an owner | `r` is typed in with no note, or the threshold is missing |
| Claims sheet | 15 | 8 to 15 real claims, not tasks; at least one load-bearing claim tagged assumed; evidence levels honest | Every claim tagged tested in week 1, or a list of tasks |
| The live period | 10 | Names what a player does in live-ops weeks 1, 2 and 4 | "Players keep playing" |
| Team fit | 10 | The PR201 discipline load table is present with the charter's hours | Only a whole-team total |
| Rejected pitch | 5 | Its output is saved and the reason it lost fits in one clear sentence | No second pitch, or no reason |
| Pitch writing | 10 | Two pages, the moment is concrete, every section present | Over length, or sections missing |
| Team ownership | 5 | Any member explains any number in the meeting | One member answers everything |
| **Total** | **100** | | |

## Late and missing work

A milestone handed in up to 48 hours late is capped at 70. After that it scores 0 but must still be handed in, because weeks 2 to 6 build on it. Extensions follow the university's mitigating circumstances process.
