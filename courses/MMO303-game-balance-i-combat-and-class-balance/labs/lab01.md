# MMO303 · Lab 01: Reading a balance dashboard

**Week:** 1 · **Time:** 2 hours in lab plus about 2 hours at home · **Weight:** part of the problem sets (30%)

## Objective

Turn a raw match summary into a diagnosis. By the end you will have computed fairness, viability and diversity for one fictional game across three rating brackets, found the one problem the summary hides, and written balance targets a team could test every week.

This lab uses the models from [week 1](../lectures/w01-what-balanced-means.md): the effective number of classes `N_eff = 1 / Σ p_i²`, HHI, and the mirror-corrected win rate `w = (observed − 0.5m) / (1 − m)`. The [effective-classes interactive](../examples/w01-effective-classes.html) checks your `N_eff` and HHI for any set of shares.

## Starter materials

The game is a fictional MMO's rated duel ladder (1v1). Every game has two appearances, one per player. When both players pick the same spec, the game is a **mirror**, and it contributes one win and one loss to that spec. "Mirror appearances" counts both players in such games.

Copy the three tables below into a spreadsheet, one sheet per bracket, or into a CSV with columns `bracket, spec, appearances, wins, mirror_appearances`.

**Low bracket (7,000 games, 14,000 appearances)**

| Spec | Appearances | Wins | Mirror appearances |
|---|---|---|---|
| Guardian | 1,800 | 905 | 180 |
| Warden | 1,500 | 760 | 120 |
| Mender | 2,200 | 1,081 | 308 |
| Chanter | 900 | 398 | 28 |
| Striker | 2,100 | 1,068 | 272 |
| Arcanist | 1,300 | 655 | 78 |
| Ranger | 1,700 | 842 | 152 |
| Reaver | 2,500 | 1,291 | 450 |

**Mid bracket (6,000 games, 12,000 appearances)**

| Spec | Appearances | Wins | Mirror appearances |
|---|---|---|---|
| Guardian | 1,400 | 690 | 112 |
| Warden | 1,200 | 590 | 72 |
| Mender | 1,900 | 935 | 228 |
| Chanter | 800 | 385 | 24 |
| Striker | 1,800 | 895 | 198 |
| Arcanist | 1,100 | 540 | 56 |
| Ranger | 1,300 | 645 | 92 |
| Reaver | 2,500 | 1,320 | 500 |

**Top bracket (2,000 games, 4,000 appearances)**

| Spec | Appearances | Wins | Mirror appearances |
|---|---|---|---|
| Guardian | 300 | 139 | 12 |
| Warden | 250 | 118 | 8 |
| Mender | 700 | 330 | 84 |
| Chanter | 200 | 106 | 2 |
| Striker | 450 | 209 | 28 |
| Arcanist | 150 | 70 | 2 |
| Ranger | 250 | 117 | 8 |
| Reaver | 1,700 | 911 | 680 |

**Faction results.** Players belong to one of two factions, Dawn and Dusk. In duels between players of opposite factions, Dawn won 3,640 of 7,000 games in Low, 3,060 of 6,000 in Mid and 1,010 of 2,000 in Top. (For this lab, assume every game was cross-faction.)

## Steps

1. **Shares and diversity.** For each bracket, compute every spec's pick share `p_i = appearances / total appearances`. Compute `Σ p_i²`, `N_eff` and HHI. Plot `N_eff` by bracket.
2. **Observed win rates.** Compute `wins / appearances` for every spec in every bracket. Mark any spec outside a 48-54% band.
3. **Mirror correction.** Compute each spec's mirror share `m = mirror appearances / appearances` and its non-mirror win rate `(wins − mirror/2) / (appearances − mirror)`. Put observed and corrected rates side by side. Which spec changes category?
4. **Sample size.** For every spec in the Top bracket, compute the approximate 95% margin `1.96 × √(0.25 / (appearances − mirror))`. Which win rates can you not distinguish from 50%?
5. **Fairness.** Compute Dawn's win rate in each bracket and its 95% margin. In which bracket, if any, is there a faction fairness problem?
6. **Diagnosis.** Write one paragraph per property (fairness, viability, diversity) stating what is wrong, in which bracket, and which number shows it. Explain how Reaver's observed win rate hid its strength.
7. **Targets.** Write four testable balance targets in the format from week 1, section 4 (property, metric, population, threshold, minimum sample). State which target wins if two conflict.
8. **One change.** Propose one balance change for the next patch. Predict, with numbers, what it does to each of your targets, and name one risk.

## Deliverable

One spreadsheet (all steps visible as formulas, not typed values) and a document of at most two pages containing the diagnosis, the four targets and the proposed change. Submit both to the course site before next week's lecture.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Diversity metrics | `N_eff` and HHI correct for all three brackets, trend explained | Minor arithmetic slips or trend not discussed | Shares or `N_eff` wrong in method | 20% |
| Win rates and mirror correction | Corrected rates correct, the spec that changes category identified with its true rate | Correction applied but one error or no discussion | No correction, or wrong formula | 25% |
| Sample size and fairness | Margins computed, small samples flagged, fairness judged per bracket with margins | Margins computed but not used in the judgment | Faction or sample analysis missing | 15% |
| Diagnosis | Each property diagnosed with a named number and bracket | Diagnosis present but partly unsupported by numbers | Opinions without numbers | 20% |
| Targets and proposed change | Four testable targets with populations and thresholds, conflict rule stated, change predicted numerically with a named risk | Targets testable but incomplete, or prediction qualitative | Untestable targets ("feel balanced") | 20% |

<details>
<summary>Instructor check values</summary>

- `N_eff`: Low 7.43 (HHI 1,346), Mid 7.19 (HHI 1,392), Top 4.15 (HHI 2,412.5, which rounds to 2,413). Each bracket's wins sum to its number of games, which is a quick check that the data were copied correctly. Diversity collapses only at the top.
- Reaver: observed 51.6% / 52.8% / 53.6% in Low / Mid / Top, mirror-corrected 52.0% / 53.5% / 56.0%. In Top it has 42.5% of picks and 40% of its appearances are mirrors. Observed, it sits inside the band; corrected, it is well above it. Its wins come from the other specs: in Top, every spec except Chanter sits between 46.3% and 47.2% observed, just below the band, though each is within its own margin (±3.9 to ±8.1 points) of 48%.
- Chanter: 44.2% in Low (outside the band), 53.0% in Top on only 198 non-mirror appearances (margin about ±7.0 points, so not distinguishable from 50%). A likely story is a hard spec with many struggling beginners, not a weak spec.
- Dawn: 52.0% in Low (margin ±1.2, a real gap), 51.0% in Mid (±1.3, borderline), 50.5% in Top (±2.2, no evidence). The faction gap is a low-bracket problem.

</details>
