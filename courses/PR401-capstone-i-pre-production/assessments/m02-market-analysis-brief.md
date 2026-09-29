# PR401 · Milestone 2 brief: market analysis

**Weight:** 4% of the course grade, inside the pitch component (20%).
**Assigned:** week 2. **Due:** before the week 3 studio session, in `preproduction/week02/`, with the market section in `docs/market.md`. **Reviewed:** at the start of week 3.
**Work mode:** team. One team mark, adjusted per person by the [peer assessment](peer-assessment-brief.md).
**Session guide and lab:** [week 2, market analysis](../lectures/w02-market-analysis.md) with [lab 02](../labs/lab02.md).
**Builds on:** [MMO403 week 2, unit economics](../../MMO403-business-monetization-and-ethics-of-live-games/lectures/w02-unit-economics-ltv-cac-arppu.md), [MMO403 week 12, publishing platforms and fees](../../MMO403-business-monetization-and-ethics-of-live-games/lectures/w12-publishing-platforms-and-fees.md), section 2, and [MMO405 week 6, interviews](../../MMO405-research-methods-in-online-games/lectures/w06-qualitative-methods-interviews.md), sections 2 and 3 (coding agreement and codebooks).

## What this milestone proves

That the team knows who its players are, what they already play, what they complain about, and how many of them PR402 needs to fill a server. The review-count method in week 2 gives a range, not a figure, and it only applies to paid Steam games. A team that reports ranges and says where the method breaks has done the job. A team that reports "*Mortal Online 2* made $9.4 million" has not.

## Deliverables

In `preproduction/week02/` in the team repository, except the market section (`docs/market.md`) and the claims sheet (`docs/claims.csv`), which later weeks keep updating.

1. **Comparables sheet** (`comps.csv`) with review counts, prices and access dates, and the saved checker output.
2. **Review coding**: `codebook.md` with a definition per code, and `codes.csv` with the double-coded sample of at least 20 reviews and the agreement you measured.
3. **Launch audience** (`audience.csv`) with target peak CCU, `q`, `h_day` and the resulting daily players `D`.
4. **Market section** of the pitch (`market.md`, one page) answering the four questions in week 2 section 1, ending in one positioning sentence.
5. **Claims sheet update**: at least one claim moved from assumed to estimated, and `D` added as a claim with an owner.

## Evidence required

| Evidence | Format | How the instructor checks it |
|---|---|---|
| Comps locked before numbers | Commit history of `comps.csv` | The list of names is committed before any review count |
| Estimates as ranges | `check_comps.py` output | Reruns the checker; every estimate has a low and high end |
| Coding agreement | Agreement and kappa in `codebook.md` | Recounts agreement on five rows of `codes.csv` |
| Positioning | One sentence in `market.md` | Finds its complaint in more than one comparable's codes |
| Audience | `audience.csv` and a row in `claims.csv` | Recomputes `D` from peak CCU, `q` and `h_day` |

No usernames and no long review quotes appear anywhere. Paraphrase reviews in your own words.

## How it is marked

The instructor reruns the checker, spot-checks the coding and asks one member to explain the least reliable row in the comparables table.

## Rubric

| Criterion | Points | Full marks when | Low marks when |
|---|---|---|---|
| Checker passes | 10 | `PASS` on rerun, dated review counts | Checker fails, or counts have no dates |
| Comparable choice | 15 | Locked before numbers; each is close in what the player does; at least one is small or failed | Only hits, or chosen after looking at sales |
| Ranges and caveats | 15 | Low and high reported; `φ` (the realized-price factor) marked as an assumption; rows that break the method footnoted, not dropped | Point estimates, or free-to-play games run through the review method |
| Review coding | 20 | Codebook has definitions; 20 or more reviews double-coded; agreement and kappa reported; counts per comparable | Single coder, or codes with no definitions |
| Positioning | 15 | Built on a complaint found in more than one comparable, in one sentence a player would say | A feature list, or a complaint from one review |
| Launch audience | 15 | `D` computed from a stated peak, `q` and `h_day`, entered as a claim with an owner | Missing, or the peak is picked with no reason |
| Team ownership | 10 | Any member explains the method's limits in the meeting | Only the author of the sheet can |
| **Total** | **100** | | |

## Late and missing work

Up to 48 hours late is capped at 70. After that it scores 0 but must still be handed in, because the greenlight package uses it.
