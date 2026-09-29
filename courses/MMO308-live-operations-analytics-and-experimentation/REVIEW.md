# MMO308 review, September 2026

All 14 lectures, 14 examples, 14 labs and 4 assessment files were checked against ORCHESTRATION.md §4 and docs/BUILD_CONVENTIONS.md. Fixes were made in place. This file lists what the review could not close.

## For the orchestrator

| File | Problem | Proposed fix |
|---|---|---|
| `syllabus.md` | Still the generated stub. The week 8 example cell was `_todo_`, and the week 11 topic reads "(verify thresholds)". The thresholds are now verified (75% until 27 October 2022, then 70%). | Run `tools/build_plan.py` so the schedule links `examples/w08-event-pull-forward.html`. Drop "verify thresholds" from the week 11 topic in `curriculum.yaml`. |
| `lectures/w01` to `w04` header | The Interactive line still says "built from the spec at the end of this lecture". The examples now exist. | Optional wording cleanup. |

## Facts verified only through a wiki or secondary source

| Lecture | Fact | Source used |
|---|---|---|
| w11 | Minecraft Mob Vote discontinued on 9 September 2024 | Minecraft Wiki, "Community Vote" (no Mojang post fetched) |
| w14 | Destiny 2 install size about 115 GB, and a vault cut of 30 to 40% | Lecture's cited Bungie post, not re-fetched in review |
| w05 | Andersen et al. (CHI 2012), "eight tutorial designs" across three games and over 45,000 players | Not re-fetched in review; paper is real and the player count matches memory |
| w12 | Koster's April 2004 Star Wars Galaxies server report, and the OSRS coin-pouch bug of 12 July 2018 (20-minute rollback) | Not re-fetched in review |
| w13 | Roblox postmortem timeline (73 hours; causes found about 54 hours in) | Not re-fetched in review |

Checked in review with a primary or maintained source: SteamCharts monthly averages (w01), Activision Blizzard MAU and WoW subscriber figures from SEC EDGAR (w02, w04), Steam achievement percentages and release dates via the Steam API (w04), OSRS update time, poll types, Sailing release date and the wiki's CC BY-NC-SA 3.0 licence (w01, w10, w11, lab 11), RuneScape Double XP history and Steam's 30-day discount rule (w08), Darkmoon Faire schedule (w08), EVE Trinity boot.ini dev blog (w09), Ducheneaut et al. guild sizes from the author PDF (w10), Duolingo figures from Lenny's Newsletter (w01), Anthem, New World and Stop Killing Games dates from Wikipedia (w14), OSRS potion-storage rollback (w13).
