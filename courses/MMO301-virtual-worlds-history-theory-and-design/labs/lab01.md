# MMO301 · Lab 01: World audit and density sheet

**Week:** 1 · **Time:** 2 hours in lab plus about 3 hours at home · **Weight:** part of the case-studies assignment (40%)

## Objective

Apply Bartle's definition to one real online game, then build a spreadsheet that computes how often a player in each band of an invented world sees nobody else, and design a pooling and splitting policy that keeps every band inside a density target you choose and defend.

This lab uses [week 1](../lectures/w01-what-is-a-virtual-world-bartles-definition.md): the six properties, the persistence ladder, the persistence-versus-change grid, and the density model `n = k × f × C`, `M = Z × v`, `λ = n / M`, `P(alone) = (1 − 1/M)^n ≈ e^(−λ)`.

## Starter materials

- A spreadsheet (any) or Python 3 with the standard library. No other software.
- One online game you can play or watch for at least 45 minutes this week. It may be a current MMO, a survival server, a social platform or a match-based game with a persistent hub. Recorded play from a video site is acceptable if you cite it.
- The invented world **Saltreach**, described by this parameter block. Put the values in named cells.

| Band | Share of online players `f` | Zones `Z` | View cells per zone `v` |
|---|---|---|---|
| Starter | 0.15 | 4 | 40 |
| Mid-levels | 0.25 | 20 | 50 |
| Endgame | 0.60 | 6 | 60 |

- Saltreach runs realms of equal size. Each realm has `C = 1,500` players online at peak (20:00 local) and `C = 400` off-peak (02:00 local). All realms are in one time zone.
- Sheet layout, one row per band and time:

| Column | Header | Formula |
|---|---|---|
| A | Band | text |
| B | Time | "peak" or "off-peak" |
| C | `C` | 1,500 or 400 |
| D | `f` | from the table |
| E | `Z` | from the table |
| F | `v` | from the table |
| G | `k` | 1 to start; your policy changes it |
| H | `n` | `= G × D × C` |
| I | `M` | `= E × F` |
| J | `λ` | `= H / I` |
| K | `P(alone)` exact | `= (1 − 1/I)^H` |
| L | `P(alone)` approx | `= EXP(−J)` |

- An audit template with these rows: physics, character, real time, shared, persistent, not the real world, persistence ladder level (1-5), who can build (coders, trained administrators, trusted players, experienced players, anyone), and quadrant on the persistence-versus-change grid. Each row needs a score (0 absent, 1 partial, 2 present) and one sentence of evidence from your play session.

## Steps

1. **Audit (in lab, 40 min).** Play or watch your chosen game with notes open. Fill in the audit template. For "shared," count how many other players you could see at five moments spaced ten minutes apart, and record the counts.
2. **Place it.** Put your game on the persistence-versus-change grid and state whose world it is, in Bartle's quadrant terms, in two sentences.
3. **Build the sheet.** Enter the six Saltreach rows (three bands, two times) with `k = 1`. Check your peak starter row against the check values below before going on.
4. **Read it.** Mark each row as "empty" (`λ < 1`), "target" (`1 ≤ λ ≤ 3`), or "crowded" (`λ > 3`). You may replace these thresholds with your own if you justify them in the memo.
5. **Design a policy.** For each band and time, choose a `k`: pool `k` realms (`k > 1`), or split into `L` copies (`k = 1/L`). Your goal is every row inside your target band. You may also change one world-design number per band (`Z`, by closing or opening zones, or `f`, by a scheduled event that pulls players into a band for an hour). State each change.
6. **Price the policy.** For each pooling decision, write down what it costs in continuity, the chance of meeting the same player again. As a rough measure, if you pool `k` realms, a player you meet is from your own realm with probability `1/k`. Record `1/k` for each row.
7. **Compare with your game.** Use your five counts from step 1 as a rough `λ` for your game (their mean). Say which Saltreach row it resembles and whether your game appears to pool or split.

## Deliverable

The sheet (or script) with your final policy, the filled audit template, and a design memo of about 400 words. The memo must give your target band and why, the final `λ` and `P(alone)` for all six rows, the continuity cost `1/k` for each pooled row, one world-design change you made and what it costs, and one sentence comparing your real game to a Saltreach row.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Audit | All rows scored with specific evidence from play; quadrant reasoning follows Bartle | Scores present, evidence generic | Rows missing or no evidence | 20% |
| Sheet correctness | All six base rows match the check values to one decimal | One row off | Two or more rows off | 20% |
| Policy | Every row inside the stated target; uses both pooling and splitting where each fits; one world-design change | Most rows inside target, or only one tool used | Rows outside target with no explanation | 25% |
| Costs | Continuity cost stated for each pooled row; the world-design change's cost named | Costs stated for some rows | Costs absent | 15% |
| Memo | Numbers from the sheet, a defended target, honest trade-offs, real-game comparison | Some numbers, thin reasoning | Opinion without numbers | 20% |

<details>
<summary>Instructor check values</summary>

Base case, `k = 1`:

| Band | Time | `n` | `M` | `λ` | `P(alone)` exact |
|---|---|---|---|---|---|
| Starter | peak | 225 | 160 | 1.41 | 24.4% |
| Mid-levels | peak | 375 | 1,000 | 0.38 | 68.7% |
| Endgame | peak | 900 | 360 | 2.50 | 8.2% |
| Starter | off-peak | 60 | 160 | 0.38 | 68.6% |
| Mid-levels | off-peak | 100 | 1,000 | 0.10 | 90.5% |
| Endgame | off-peak | 240 | 360 | 0.67 | 51.3% |

With the default 1-3 target, only the peak starter and peak endgame rows are inside it. The mid-level band is empty even at peak and needs `k ≥ 3` there (`λ = 1.13`). Off-peak it needs `k ≥ 10` for `λ ≥ 1`. That is a heavy continuity cost (`1/k = 10%`), so good submissions often combine a smaller `k` with a world-design change, for example closing half the mid-level zones off-peak (`Z = 10`), which gives `λ = 1.0` with `k = 5`. Accept any policy that meets the student's stated target and prices its costs honestly.

</details>
