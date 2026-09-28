# MMO303 review: open items

Reviewer pass on 2026-09-28. Small fixes were made in place. The items below are larger or need a decision.

## 1. Labs name starter files that do not exist

Labs 10, 11 and 12 now ship working starters (`labs/lab10-matchups.csv`, `labs/lab11-starter.py`, `labs/lab12-starter.py`). Lab 04 now describes its sheet in full. These still name files that are not in the repo:

| Lab | Named file(s) | Proposed fix |
|---|---|---|
| lab05.md | `composition_solver.py`, `composition-solver.xlsx`, `roles.csv`, `test_solver.py` | Add a stdlib Python stub plus `roles.csv` (the lecture's three roles). Put the test values from lab05 line 15 in `test_solver.py`. The spike check is strict (`HP > S(1 − m)`). |
| lab06.md | `threat_sim.py`, `test_threat.py` | Add a stub and tests with the listed values (melee 700 pulls at 11.0 s, ranged at 39.0 s, melee 550 never). |
| lab07.md | `mana-budget-template.xlsx` | Describe the four tabs' headers in full, or ship a CSV per tab. |
| lab08.md | `cc-planner-template.xlsx`, `cc_planner.py` | Ship the Python stub with a test for the 6-second stun chain (10.5 s, ceiling 36.8%). |
| lab09.md | `counter-sim-template.xlsx`, `counter_sim.py` | Ship the Python stub. Its tests should include the Knight-buff step (35.6 / 33.3 / 31.1). |
| lab13.md | `lab13-starter/` (`sim.py`, `classes.yaml`, `test_sim.py`, `report_template.md`) | Ship the folder. The class table in lab13 already gives `classes.yaml`'s content. |
| lab14.md | `patch_template.md` | Inline the five-part checklist from w14 section 3 in the lab. |

## 2. Weeks 9 and 10 teach the same result twice

Both weeks build the Knight/Ranger/Mage triangle. Both prove that buffing Knight over Ranger to 70/30 moves the stable mix to 25/25/50. Both use Pokémon and Fire Emblem as cross-game cases. The letters also differ between the weeks. In w09, `a` is Knight over Ranger and `c` is Ranger over Mage, with Knight's share `c/S`. In w10, `b` is Ranger over Mage, with Knight's share `b/S`.

Proposed fix: w10 should take the triangle result from w09 as known and recap it in one paragraph using w09's letters. Its worked example should then cover something new. Candidates are dominance plus a solved 4- or 5-class matrix (the lab 10 table would work), or the Hawk-Dove world-boss game. Swap one of w10's cross-game cases for a case w09 does not use.

## 3. Facts not re-verified in this pass

The session ran out of web searches, so these were checked against memory or a secondary source only.

- w13: that Frank Karsten's mana tables come from mulligan-aware simulation code. The only source is a secondary GitHub gist. The lecture now says so and attributes the claim to the gist. Find Karsten's own article (the ChannelFireball URL is dead; try the TCGplayer archive) and restore the plain statement if it confirms.
- w02: the Path of Exile 2 armour formula, `armour / (armour + 10 × damage)` with a 90% cap. poe2wiki.net blocks automated fetches. Check it by hand and confirm it is still current for the latest early-access patch.
- w05: the Final Fantasy XIV party sizes, the Overwatch role-queue dates and the Guild Wars 2 Spirit Vale date. These were checked against memory only.
- w01 and w03, from the w01-w04 review: Overwatch role queue, Hearthstone's The Coin and the Diablo IV damage buckets. Also checked against memory only.

## Resolution (2026-09-28)

### 1. Missing starter files: resolved

Every starter below is standard-library Python. Its tests fail on the stub and pass against a reference solution that was run and kept out of the repo.

- lab05: `labs/lab05-starter/` (`composition_solver.py`, `roles.csv`, `test_solver.py`). The tests include the strict spike rule, where a DPS target survives `S = 3,749` and dies at exactly 3,750. The `.xlsx` mention was replaced with a spreadsheet layout.
- lab06: `labs/lab06-starter/` (`threat_sim.py`, `test_threat.py`). The closed form gives 11.0 s, 39.0 s and never. The tick sim matches within one tick. The taunt case lands within two ticks of 16.13 s, and the lab now says why.
- lab07: `labs/lab07-starter/`, one CSV per tab (`Spells`, `Frontier`, `Curve`, `Encounter`). The lab lists every header.
- lab08: `labs/lab08-starter/` (`cc_planner.py`, `test_cc_planner.py`). Tests cover 10.5 s, immunity, 8.75 s against 6.5 s, the 18 s reset and the 36.8% ceiling.
- lab09: `labs/lab09-starter/` (`counter_sim.py`, `test_counter_sim.py`, `five-class.csv`). Tests cover 25/50/25, 53.3/50.0/46.7 and 35.6/33.3/31.1. The five-class order is Knight, Ranger, Cleric, Mage, Rogue, which keeps the triangle's links.
- lab13: `labs/lab13-starter/` (`sim.py`, `classes.yaml` in JSON-style YAML, `test_sim.py`, `report_template.md`). The stub deals zero damage, and one test fails until hits are implemented. The reference run gives Marksman 80.70 DPS with SD 3.46 (lecture: 80.67, 3.48).
- lab14: the five-part patch template and the blind-read sheet are now in the lab itself.

### 2. Weeks 9 and 10 overlap: resolved

- Week 9's letters are now the only notation: `a` = Knight over Ranger, `b` = Mage over Knight, `c` = Ranger over Mage, with Knight `c/S`, Mage `a/S` and Ranger `b/S`. Week 10 recaps the week 9 result in one paragraph as a Nash equilibrium. Lab 10 and exam questions 44 and 47 now use the same letters, and the "doubled margin" wording is now week 9's `2w − 1`.
- Week 10's new worked example is the two-guild world boss game (Hawk-Dove). It opens on WoW tapping: classic first-damage tap, patch 5.1.0 tap-to-faction world bosses and patch 7.0.3 shared tapping. The example derives `p* = V/(2C)` and models the loot-rule edit. The cross-game cases are now WoW 7.0.3, Maynard Smith's Hawk-Dove and penalty kicks, so Pokémon and Fire Emblem are dropped. Section 4 builds on week 9's drift rule. The only new result there is that the time-average equals the equilibrium.
- New interactive: `examples/w10-world-boss-game.html`. It passes `check_examples.py`, and all spec test values were confirmed headless. Lab 10 now links to the week 9 interactive.
- Open: `examples/w10-counter-triangle.html` is orphaned and should be deleted. This pass was not allowed to delete files. Until someone removes it, `build_plan.py` lists it next to the new example.

### 3. Facts: resolved

- Karsten: his archived ChannelFireball article (October 2018) confirms the simulation code and the mulligan rule. The plain statement is restored in w13, and both sources are cited.
- PoE2 armour: `armour / (armour + 10 × damage)` and the 90% player cap are confirmed in the Path of Building PoE2 source (v0.23.1, July 2026, trees up to 0.5). The monster cap is 75%. The w02 text and sources now give the era and cite this source. poe2wiki.net still blocks fetches.
- FFXIV 1/1/2 and 2/2/4: confirmed on the consolegameswiki "Party" page.
- Overwatch: patch notes confirm Role Queue went live on August 13, 2019. OWL enforced it from Stage 4, and Season 18 ran September 3 to November 7, 2019. The w05 citation now points to the patch page, and w01 gained a source.
- Guild Wars 2: release August 28, 2012. Heart of Thorns released October 23, 2015, and Spirit Vale November 17, 2015. All confirmed on the GW2 wiki.
- Hearthstone: The Coin (GAME_005, "Gain 1 Mana Crystal this turn only"), 3 cards for the first player and 4 for the second. Confirmed and cited.
- Diablo IV: `[+]`/`[x]` buckets confirmed. The w12 claim that Season 4 "reworked the damage calculation" was wrong, because Season 4 overhauled itemization. It is now replaced with the Season 13 (2026) note on summed multipliers. w04 now scopes its claim to the 2023-2024 seasons.

### Assessments reconciled

- Exam question 25 now uses the strict spike rule (`S < 3,750`). Question 21 was recomputed with the solver and is unchanged.
- Exam question 50 notes the near mutual wipe at parity in the step simulation. Questions 51 and 53 were checked and are unchanged.
- The w13 separation change and the w02 Q5 addition do not affect any assessment answer. Q5's arithmetic was checked (A = 18.75, HP = 1,900, EHP ≈ 2,256).
- `assessments/final-roster.yaml` was created from the brief's table and rules and is linked from the brief.
