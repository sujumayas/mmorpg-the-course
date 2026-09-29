# MMO309 review: open items

Reviewer pass on 28 September 2026. Everything below was left open because it needs a source the reviewer could not reach, or a decision outside the reviewer's files.

| File | Problem | Proposed fix |
|---|---|---|
| `syllabus.md` | Still the generated stub, with `_todo_` schedule cells. The reviewer was told not to edit it. | Orchestrator runs `tools/finish_syllabus.py` or `tools/build_plan.py`, then links all 14 lectures and examples. |
| `lectures/w07-bot-detection-behavioral-features.md` | Details attributed to Gianvecchio et al. (2009, "Battle of Botcraft") are unconfirmed, because the ACM page blocked access. | Check against the paper's PDF. If a figure does not match, cut it rather than restate it. |
| `lectures/w09-account-security-and-takeovers.md` | The March 2016 date for Steam's 15-day trade hold rests on Wikipedia's "Steam" article, which cites GameSpot. The GameSpot page sits behind a bot challenge and has no archive copy. | Find a Valve announcement or a Steam support page with the date, or cut it to "since 2016". |
| `lectures/w10-gold-sellers-and-rmt-networks.md` | Crossref and Semantic Scholar list the authors of Kwon et al. (2016) in different orders. The paper's abstract does not name its game, and the lecture correctly does not name it either. | Take the author order from the published PDF. |
| `lectures/w14-case-studies.md` | Bungie's arbitration award against AimJunkies is "about $4 million" in The Verge (25 May 2024), under appeal at the time, and $4.3 million in Wikipedia. The lecture now uses The Verge's figure. | If a court record of the confirmed award appears, use its exact amount and outcome. |

Everything else in the QA checklist passed or was fixed in place. Fixes include:

- stale week-11 ban-timing references, now pointing to week 5;
- the w07 slack CV figures;
- the w10 threshold claim;
- the w13 `B*` wording;
- the w11 potion-storage account;
- the w14 legal figures;
- the lab run paths.
