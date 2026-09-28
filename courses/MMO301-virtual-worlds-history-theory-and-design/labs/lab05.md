# MMO301 · Lab 05: Auditing a death rule

**Week:** 5 · **Time:** 2 hours in lab plus about 2 hours at home · **Weight:** part of the case-studies assignment (40%)

## Objective

Write the death rules of three MMOs in the same `(t, x)` form, find the player each rule hurts most, and recommend a death rule for your own world concept with numbers to back it.

This lab uses [week 5](../lectures/w05-world-of-warcraft-accessibility-and-the-themepark.md): net progress `P = g × (1 − λ × t) − λ × x`, break-even death rate `λ* = g / (g × t + x)`, and waste `λ × (t + x / g)`.

## Starter materials

- A blank spreadsheet.
- The three player profiles below. Everyone uses them so results can be compared.

| Profile | Progress rate `g` (levels per hour) | Deaths per hour `λ` | Session length (hours) |
|---|---|---|---|
| New player | 0.40 | 1.5 | 1 |
| Regular | 0.25 | 0.5 | 2 |
| Veteran | 0.15 | 0.2 | 4 |

- Rule A, given to everyone: World of Warcraft after patch 1.1.0, as documented in week 5's Sources. You choose `t` from your own reasoning about runback time, `x = 0`, and record the gold cost separately.
- Two more games of your choice. At least one must have an experience or item penalty. Suggested: EverQuest classic (Project 1999 Wiki, "Experience" and "Corpse"), Final Fantasy XI (BG Wiki, "Experience Points"), Old School RuneScape (OSRS Wiki, "Items Kept on Death"), Ultima Online, Guild Wars 2, or a recent MMO. Use a wiki or official source and record its date or version.

## Steps

1. **Rule sheet.** For each of the three games, write the rule in one sentence, then as `(t, x)` plus any item or currency loss, with the source and era. Where the source gives no number (for example EverQuest's experience loss), choose a value, label it as an assumption and say why.
2. **Progress table.** For each game and each profile, compute `P`, `λ*` and waste.
3. **Session simulation.** For each profile, simulate one session in one-minute steps with deaths drawn at random (probability `λ / 60` per minute, frozen random numbers). Plot level against time for all three games on one chart per profile.
4. **Who hurts most.** For each game, name the profile with the highest waste and the profile most likely to end a session behind where they started. Repeat the simulation 20 times per profile (a new frozen column each time) and report how many sessions ended with negative progress.
5. **Your rule.** Design a death rule for your world concept, with different `(t, x)` in at least two level bands. Run it through steps 2 to 4.

## Deliverable

The spreadsheet and a 500-word recommendation for your world design bible's risk section. It must state your rule in `(t, x)` form, give `λ*` for each profile, report the share of simulated sessions with negative progress, name the player your rule hurts most and say why you accept that cost.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Rule sheet | All three games sourced with era, correctly rewritten, assumptions labelled | One rule mis-stated or unsourced | Two or more | 20% |
| Progress table | `P`, `λ*` and waste correct for all nine cells | One or two arithmetic errors | More | 20% |
| Simulation | Random deaths drawn correctly, frozen, charts clear, 20 repeats counted | Simulation works but not repeated, or charts unclear | Missing | 20% |
| Own rule | Two or more bands, fully computed, compared with the three games | Rule given, analysis thin | Missing | 15% |
| Recommendation | Argued from numbers, names the hurt player, trade-off stated plainly | Recommendation with weak support | Opinion without numbers | 25% |

<details>
<summary>Instructor check values</summary>

- Rule A with `t = 0.05`, `x = 0`: new player `P = 0.40 × (1 − 0.075) = 0.370`, `λ* = 20`, waste 7.5%. Regular `P = 0.244`, waste 2.5%. Veteran `P = 0.1485`, waste 1%.
- EverQuest-style assumption `t = 1/3`, `x = 0.1`: new player `P = 0.40 × 0.5 − 0.15 = 0.050`, `λ* = 0.40 / (0.133 + 0.1) ≈ 1.71`, waste 87.5%. Regular `P = 0.25 × 0.8333 − 0.05 = 0.158`. Veteran `P = 0.15 × 0.9333 − 0.02 = 0.120`, `λ* = 0.15 / 0.15 = 1.0`, waste 20%.
- The new player is hurt most by any experience rule, because they die most and each death also costs the most time relative to a short session.

</details>
