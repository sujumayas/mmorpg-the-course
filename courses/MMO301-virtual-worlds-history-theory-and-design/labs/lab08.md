# MMO301 · Lab 08: The Bartle population model

**Assigned:** week 8 ([lecture](../lectures/w08-player-types-bartle-1996-and-the-heros-journey.md)). **Due:** start of week 9. **Feeds:** the player-type critique (20%), together with lab 09.

## Objective

Build the week 8 population model in a spreadsheet, reproduce its test values, add one feature Bartle described that the lecture's model leaves out, and use your runs to critique one specific claim in Bartle's 1996 paper. You should finish able to say which of Bartle's conclusions follow from his stated interactions and which depend on numbers he never gave.

## Starter materials

Everything is in this file.

**1. Parameters.** Put these in named cells on a sheet called `params`. Populations are in hundreds of players.

| Name | Value | Meaning |
|---|---|---|
| `cap` | 40 | Server capacity (hundreds) |
| `h` | 10 | Word-of-mouth half point (hundreds) |
| `aA, aE, aS, aK` | 1.00, 0.15, 0.15, 0.10 | Arrival rates |
| `dA, dE, dS, dK` | 0.03, 0.03, 0.04, 0.08 | Base weekly leaving rates |
| `kA, kE, kS` | 0.08, 0.01, 0.20 | Harm from each hundred killers to achievers, explorers, socialisers |
| `fS` | 0.04 | Socialiser self-attraction |
| `pK` | 0.04 | Killer gain per hundred achievers or socialisers |
| `eK` | 0.05 | Killer loss per hundred explorers |
| `protection` | 0 | Design lever, 0 to 1 |
| `c` | 1 | Explorer content lever |

**2. Weekly update.** On a sheet called `run`, one row per week from 0 to 520, columns `week, A, E, S, K, N, room, w, g`. Row 0 holds the starting mix. Each later row uses only the row above.

```
N    = A + E + S + K
room = MAX(0, 1 − N/cap)
w    = IF(N = 0, 0, N/(N + h))
g    = w × room
q    = 1 − protection
A'   = MAX(0, A + aA·g − A·(dA + kA·q·K))
E'   = MAX(0, E + aE·c·g − E·(dE + kE·q·K))
S'   = MAX(0, S + aS·g + S·(fS·S·room − dS − kS·q·K))
K'   = MAX(0, K + aK·g + K·(pK·q·(A + S) − dK − eK·E))
```

**3. Check values.** Start (A, E, S, K) = (4, 1, 2, 3), protection 0, `c = 1`. Your sheet must show, in players (×100, rounded):

| Week | A | E | S | K |
|---|---|---|---|---|
| 1 | 330 | 100 | 90 | 337 |
| 4 | 184 | 96 | 9 | 344 |
| 156 | 247 | 104 | 17 | 106 |

With protection 1 at week 520: 69, 10, 3,813, 2. With protection 0.5 and `c = 3` at week 520: 797, 501, 287, 30. Fix the sheet until these match.

**4. Bartle's paper.** Use the free text at mud.co.uk/richard/hcds.htm, sections "Player interactions", "Dynamics" and "Overbalancing a MUD".

## Steps

1. **Build and check** (item 3). Add a chart of all four populations against week.
2. **Map the sweep.** For protection 0, 0.25, 0.5, 0.75, 0.9 and 1, and for `c` = 1 and 3, record the week-520 populations (12 runs). Label each with the Bartle configuration it matches (1, 2, 3, 4, or "none of these") and justify the label in one line. Some runs never settle (protection 0.5 with `c = 3` swings between about 1,050 and 2,800 players on a cycle of roughly 100 weeks). For those, report the range of the total over weeks 420 to 520 as well as the week-520 values.
3. **Add a missing effect.** Choose one, and implement it with a coefficient you pick and justify:
   - **(a) Development track.** Each week, a fraction `t` of achievers become socialisers (Bartle's main sequence ends at "friend"). Subtract `t·A` from `A'` and add it to `S'`. Try `t = 0.005` and `t = 0.02`.
   - **(b) Too few killers bore achievers.** Add a loss to achievers that is large when killers are scarce, for example `− A·b·MAX(0, 0.5 − q·K)` with `b = 0.05`.
   - **(c) Explorers help achievers.** Add `+ A·x·E` to `A'` with `x = 0.01`.
   Rerun the 12 cases from step 2 and mark which endings changed.
4. **Find a tipping point.** With your added effect on, starting from (4, 1, 2, 3), find the lowest protection level (to 0.05) at which socialisers exceed 1,000 players at week 520.
5. **Pick one claim and test it.** Choose one sentence from Bartle's "Dynamics" section. Quote at most one short phrase and paraphrase the rest. State what your runs say about it and how much that depends on coefficients you invented.

## Deliverable

The spreadsheet, plus a PDF of at most four pages.

- The step 1 chart and a screenshot of the check values matching.
- The step 2 table of 12 runs with configuration labels.
- A description of your step 3 effect: formula, coefficient, reason, and which endings changed.
- The step 4 tipping point with a chart.
- A 500-word critique for step 5. It must separate what follows from Bartle's signs alone from what depends on the numbers, and it must end with one question a measured study (next week) could answer.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Model correctness | All check values match; updates use the previous row only | Small errors, corrected or explained | Check values do not match | 25% |
| Sweep and labels | 12 runs, each labelled with a one-line reason tied to Bartle's configurations | Runs complete, reasons thin | Missing runs or no labels | 20% |
| Added effect | Clear formula, justified coefficient, effect on endings described | Effect added, weak justification | Missing or broken | 20% |
| Critique | Separates sign-driven from number-driven conclusions; paraphrases Bartle accurately; ends with a testable question | Critique present but mixes the two | Summary instead of critique | 25% |
| Writing | Plain, numbers first, within length | Readable but padded | Hard to follow | 10% |
