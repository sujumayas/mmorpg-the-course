# GD203 review notes

Reviewer pass against `ORCHESTRATION.md` §4, September 2026. Small issues were fixed in place. The items below are still open.

## Unverified facts

The web search budget ran out before these could be checked. Each is cited to a wiki, but no reviewer has opened the page.

| File | Claim | Proposed fix |
|---|---|---|
| lectures/w01-stats-as-design-language.md | WoW Classic gives Warriors and Paladins 2 attack power per Strength, Mages 1, and 10 health per Stamina | Check Warcraft Wiki "Strength" and "Stamina" (classic era). If it doesn't match, correct the numbers or drop the class split |
| lectures/w01-stats-as-design-language.md | Diablo III gives 1% damage per point of main stat | Check the Diablo Wiki "Main stat" page and state the patch era |
| lectures/w01-stats-as-design-language.md | Path of Exile's "increased" versus "more" rules | Check poewiki.net "Modifier" |
| lectures/w11, w12 | *Game Balance Concepts* spreadsheet material cited as level 10, "Final Boss". Level 6 is confirmed as "Situational Balance", so the old citation was wrong. The level 10 attribution rests on the site's front page, which shows the Excel tutorial in the final post | Open the level 10 post and confirm it holds the spreadsheet tutorial |
| lectures/w13-difficulty-modes-and-scaling.md | Guild Wars 2 ascended gear is about 5% stronger than exotic, the Oblivion difficulty slider description, and the FFXIV Armoury citation | Check the GW2 Wiki "Ascended equipment", UESP "Oblivion:Difficulty" and the FFXIV Lodestone or wiki |

## Changes that affect other agents

- `lectures/w13`: Mythic+ scaling now uses the verified patch 7.2.5 rate of 10% per keystone level, not the unconfirmed The War Within season 2 figures. If `assessments/` has questions that use 7% or 8%, update them to match (safety ratio divided by 4.59 from +2 to +10, check-yourself question 2 answer 1.61).
- Labs 04, 05 and 06 had tuning goals with no solution. The goals were widened: lab 04 orc goal 7-11 s (health 121-134), lab 05 carbine goal 800 health against 100 and 240, and lab 06 targets moved off the breakpoints. Assignment briefs that quote the old goals need the same change.
- `assessments/exam-bank.md` links to `final-spec-brief.md` and `spreadsheet-labs-brief.md`, which don't exist yet. Those files belong to the assessments agent.

## Added files

- `labs/lab10-reference.md` is the instructor's lab 10 reference sheet that lab 11 promises. It covers the player curve, stat blocks, the breakpoint pass and room costs before tuning, and lab 11 links it.
