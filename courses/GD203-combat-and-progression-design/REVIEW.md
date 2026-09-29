# GD203 review notes

Reviewer pass against `ORCHESTRATION.md` §4, September 2026. Small issues were fixed in place. The items below are still open.

## Unverified facts (closed September 2026)

All six groups were checked on 28 September 2026. Sources are cited with era in each lecture's Sources section.

| File | Claim | Status |
|---|---|---|
| lectures/w01-stats-as-design-language.md | WoW Strength and Stamina rates | Partly rewritten. 2 AP per Strength for Warriors and Paladins, 1 for Mages, and 1 DPS per 14 AP are confirmed (WoWWiki archive table before patch 4.0.1; Warcraft Wiki "Attack power"). The Sources line wrongly listed Shamans and Druids at 2 and was fixed. No source for 10 health per Stamina in the classic era was found, so the text and graph now use a generic rate `k` |
| lectures/w01-stats-as-design-language.md | Diablo III gives 1% damage per point of main stat | Resolved. Diablo Wiki "Primary stat" confirms the 1% rule and the class mapping |
| lectures/w01-stats-as-design-language.md | Path of Exile "increased" versus "more" | Resolved. poewiki.net blocks automated reads, so the citation is now the Path of Exile Wiki (Fandom) "Stat" page plus Path of Building's `ModDB.lua` |
| lectures/w11, w12 | *Game Balance Concepts* level 10 holds the spreadsheet tutorial | Resolved. The level 10 post ("Final Boss", 8 September 2010) has an "Excel" section. The citation now links the post itself |
| lectures/w14-horizontal-vs-vertical-progression.md | GW2 ascended gear is 5% stronger than exotic | Resolved. Guild Wars 2 Wiki "Ascended equipment" quotes the 5% figure. The claim is in w14, not w13 |
| lectures/w13-difficulty-modes-and-scaling.md | Oblivion difficulty slider | Resolved. UESP confirms that the slider changes only damage, from 6x dealt and 1/6 taken at the easy end to the reverse at the hard end. The text now gives the factor, and the Construction Set Wiki citation (site down) was replaced |
| lectures/w14-horizontal-vs-vertical-progression.md | FFXIV Armoury citation | Resolved. Final Fantasy XIV Online Wiki "Job" confirms that a character switches jobs by equipping that job's weapon. The Massively Overpowered and Gamer Escape citations (not opened) were replaced |

## Changes that affect other agents

- `lectures/w13`: Mythic+ scaling now uses the verified patch 7.2.5 rate of 10% per keystone level, not the unconfirmed The War Within season 2 figures. If `assessments/` has questions that use 7% or 8%, update them to match (safety ratio divided by 4.59 from +2 to +10, check-yourself question 2 answer 1.61).
- Labs 04, 05 and 06 had tuning goals with no solution. The goals were widened: lab 04 orc goal 7-11 s (health 121-134), lab 05 carbine goal 800 health against 100 and 240, and lab 06 targets moved off the breakpoints. Assignment briefs that quote the old goals need the same change.
- `assessments/exam-bank.md` links to `final-spec-brief.md` and `spreadsheet-labs-brief.md`, which don't exist yet. Those files belong to the assessments agent.

## Added files

- `labs/lab10-reference.md` is the instructor's lab 10 reference sheet that lab 11 promises. It covers the player curve, stat blocks, the breakpoint pass and room costs before tuning, and lab 11 links it.

## Fact sweep (2026-09-29)

No open items. All facts were closed on 28 September 2026 (see the table above). No "(verify" markers. Verified 0, hedged 0, removed 0.
