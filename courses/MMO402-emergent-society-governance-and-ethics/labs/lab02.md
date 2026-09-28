# MMO402 · Lab 02: Keys to the vault

**Week:** 2 · **Time:** 2 hours in lab plus about 2 hours at home · **Weight:** one of the case analyses (30% of the course in total)

## Objective

Build a small calculator for K-of-N approval rules, check it against the numbers in [week 2](../lectures/w02-emergent-player-government-alliances-and-councils.md), then design and defend the full permission table for a guild system. Your design must match the number of required approvals to the cost of each action, treat duties differently from powers, and use at least one rate limit or delay.

## Starter materials

- `lab02-starter.py` in this folder: a Python 3 file with the binomial tail function written and the cost function left for you. Pure standard library. Run `python lab02-starter.py`.
- The design brief below.
- A spreadsheet is acceptable instead of Python, if it computes the same columns.

**Design brief.** You are designing guilds for a fantasy MMO. Guilds own a hall that costs weekly upkeep from the guild treasury; if upkeep lapses for 7 days the hall and its storage are lost. Guilds have a treasury, a bank with four tabs, a roster, and can declare feuds on other guilds (open-world combat between members without penalty). Telemetry from the beta gives these estimates for a typical mid-size guild: 6 officers, each online on a given day with probability 0.5; about 3% of officer accounts are stolen or turn hostile over a season. Players have told you they want protection from theft but hate waiting for approvals.

## Steps

1. **Finish the calculator.** Implement `cost(N, K, q, a, H, L)` in the starter. Print a table for `N = 5, q = 0.1, a = 0.6, H = 100, L = 10` and confirm it matches the lecture's table to two decimals.
2. **Extend to duties.** Add a function `missed_duty(N, a, days)` for "any of N" duties that can be done on any of `days` days: the chance all officers miss every day is `(1 − a)^(N × days)`, assuming independence. Compute it for the hall upkeep with the brief's numbers and `days = 7`.
3. **List actions.** Write down at least eight guild actions from the brief, from minor to severe. For each, estimate `H` and `L` (0 to 200) and write one sentence justifying each number.
4. **Choose K.** For each action, use your calculator with the brief's `N`, `q` and `a` to pick the `K` with the lowest expected cost. Record `P(hijack)`, `P(timely)` and the cost.
5. **Add limits.** For the two most severe actions, add a rate limit (lowers `H`) or a public delay (lowers the chance a hijack succeeds; model it as dividing `P(hijack)` by 5). Recompute and show whether you can now use a smaller `K`.
6. **Stress test.** Rerun your table with correlated availability: assume that on a bad day (probability 0.2) every officer's availability falls to 0.2, and on a normal day it is 0.575, which keeps the average at 0.5. Compute `P(timely)` as `0.2 × tail(N, K, 0.2) + 0.8 × tail(N, K, 0.575)`. Which of your choices change?

## Deliverable

The calculator (code or spreadsheet), the permission table from steps 3 to 6, and a memo of about 400 words to the lead designer recommending the permission system. The memo must quote at least three numbers from your table, explain the duty-versus-power distinction, and say whether the system should allow a single officer to betray the guild, with a reason tied to the game's intended tone.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Calculator | Matches the lecture's table exactly; duty function correct | Small numeric errors | Does not run or wrong formulas | 20% |
| Action list and costs | Eight or more actions, `H` and `L` justified in context | Actions listed, justifications thin | Fewer than five actions | 20% |
| Choice of K | Every K is the cost minimum at the brief's numbers; duties handled as any-of-N | One or two choices off | K chosen without calculation | 20% |
| Limits and stress test | Limits reduce K with numbers shown; correlated case analysed and changes named | One of the two done | Neither done | 20% |
| Memo | Clear recommendation, three or more numbers, tone decision argued | Recommendation without clear numbers | Missing | 20% |

<details>
<summary>Instructor check values</summary>

- `N = 5, q = 0.1, a = 0.6, H = 100, L = 10`: costs 41.05, 9.02, 4.03, 6.68, 9.22.
- Brief's numbers, `N = 6, q = 0.03, a = 0.5`: `P(hijack)` for K = 1 is `1 − 0.97^6 ≈ 16.7%`; K = 2 is about 1.2%. `P(timely)` for K = 1 is `1 − 0.5^6 ≈ 98.4%`; K = 2 is about 89.1%; K = 3 is about 65.6%.
- Upkeep as any-of-6 over 7 days: `0.5^42 ≈ 2.3 × 10^-13`, effectively never, if independent. The stress test shows why a warning system is still worth building.

</details>
