# MMO303 · Lab 10: Solving a class meta

**Week:** 10 ([lecture](../lectures/w10-game-theory-payoff-matrices-and-nash-equilibria.md), [week 9 counter triangle interactive](../examples/w09-counter-triangle.html))
**Time:** 2 hours in the lab, plus up to 2 hours to finish the memo.
**Work mode:** individual, discussion allowed.
**Counts toward:** problem sets (30% of the course grade).

## Objective

Build a spreadsheet that turns a table of class matchup win rates into a predicted meta. By the end you can remove dominated classes, solve the mixed Nash equilibrium for up to five classes, and predict how a proposed patch shifts every class's share.

## Starter materials

- [`lab10-matchups.csv`](lab10-matchups.csv): a five-class duel win-rate table for a fictional MMO (Knight, Ranger, Mage, Bard, Warden). Each cell is the row class's win rate against the column class, from 10,000 simulated duels between equally skilled players.
- A spreadsheet tool with a linear-programming solver: Excel Solver, LibreOffice Calc Solver, or Google Sheets with the "Solver" add-on. Python with `scipy.optimize.linprog` is an accepted alternative.
- Week 9's three-class stable mix to check your solver: with `a` = Knight over Ranger, `b` = Mage over Knight and `c` = Ranger over Mage (all margins `2w − 1`), Knight `c / S`, Mage `a / S`, Ranger `b / S`, where `S = a + b + c`.

## Steps

### Part A: check the solver on a triangle you can solve by hand (20 min)

1. Enter the three-class launch table from the lecture (all favored matchups 60/40). Convert win rates to margins with `=2*W - 1` (week 9).
2. Set up the linear program for the row player of a zero-sum game:
   - Variables: shares `p1 ... pn` and the game value `v`.
   - Maximize `v`.
   - Constraints: for every column `j`, `sum over i of p_i × M[i][j] ≥ v`. All `p_i ≥ 0`. `sum p_i = 1`.
3. Solve. You should get 33.3% each and `v = 0`. Then change the Knight-vs-Ranger cell to 70/30 (and its mirror to 30/70) and solve again. You should get 25%, 25%, 50%. If you do not, fix the setup before moving on.

### Part B: the five-class meta (40 min)

4. Load `lab10-matchups.csv`. Verify it is zero-sum after conversion: each cell plus its mirror must be 0 within rounding. Record any cell where it is not and explain what that says about the data.
5. Check each pair of classes for strict dominance. Use a helper grid with `=AND(...)` over the column comparisons. Remove any dominated class and repeat until nothing more is removed.
6. Solve the equilibrium for the remaining classes. Record shares to one decimal and the game value.
7. For each class, compute its expected payoff against the equilibrium mix. Every class in the equilibrium should earn `v` (0 for a symmetric game). Every class outside it should earn less. Include this table; it is your proof.

### Part C: predict a patch (40 min)

8. The design team proposes three patch options. Each changes exactly one matchup:
   - Option 1: Knight vs Mage from 42% to 50%.
   - Option 2: Warden vs Ranger from 55% to 62%.
   - Option 3: Bard vs Knight from 47% to 53%.
9. Before solving, write down your prediction for each option: which class's share rises most, and which falls most. Use the lecture's reasoning ("the counter of the buffed class rises").
10. Solve each option. Compare your predictions with the results in a small table. Where you were wrong, explain why in one sentence (hint: in a five-class game, a class can have more than one counter).

### Part D: recommend (20 min)

11. The team's goal: every class at 12% share or more, no class above 30%. Pick the option that comes closest, or propose a fourth single-cell change that meets the goal. Show the solved shares.

## Deliverable

Submit one spreadsheet (or notebook) and one memo of 300 to 400 words.

- The spreadsheet has four clearly labeled tabs or sections: Part A check, Part B equilibrium with the dominance grid and payoff proof, Part C patch options, Part D recommendation.
- The memo is addressed to the class design lead. It states the current predicted meta, the dominated class (if any) and why, your recommended change with its predicted shares, and one risk the model does not capture (for example, sticky class choice, skill differences or team play).

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Solver check (Part A) | Both triangle results reproduced exactly and the setup is readable | One result reproduced, or setup correct with a small error | No working check | 15 |
| Dominance and equilibrium (Part B) | Zero-sum check done, dominance grid correct, equilibrium solved, payoff proof shows every support class at `v` | Equilibrium solved but dominance or proof incomplete | Equilibrium missing or wrong | 30 |
| Patch predictions (Part C) | Written predictions before solving, all three options solved, every miss explained with a correct reason | Options solved, predictions or explanations thin | Options not solved | 25 |
| Recommendation (Part D) | Meets the 12% / 30% goal or argues clearly why none can, with solved shares | Recommendation given without full evidence | No recommendation | 15 |
| Memo | Plain, specific, under 400 words, names one real limit of the model | Clear but generic, or over length | Missing | 15 |
| **Total** | | | | **100** |

<details>
<summary>Instructor check values</summary>

- Part A: 33.3% each, then Knight 25%, Ranger 25%, Mage 50%, value 0.
- Part B: the table is zero-sum as provided. The Bard is strictly dominated by the Knight (Knight is better in all five columns). After removing it, nothing else is dominated. The equilibrium is Knight 52.4%, Ranger 38.1%, Mage 9.5%, Warden 0%, value 0. It matches week 9's triangle formula with `a = 0.04` (Knight over Ranger), `b = 0.16` (Mage over Knight), `c = 0.22` (Ranger over Mage), `S = 0.42`: Knight `0.22 / 0.42`, Mage `0.04 / 0.42`, Ranger `0.16 / 0.42`. The Warden is not dominated but earns −0.021 against the mix, so it stays out. A symmetric zero-sum game usually has an odd number of classes in its equilibrium, which is why four-class support does not appear.
- Option 1: the Knight now wins or ties every matchup, so 100% Knight is an equilibrium. The worst option.
- Option 2: the Knight drops out (Warden now dominates it); Ranger 28.1%, Mage 37.5%, Warden 34.4%.
- Option 3: the Bard is no longer dominated and all five classes appear: Knight 30.2%, Ranger 40.5%, Mage 10.2%, Bard 10.7%, Warden 8.3%. Closest to the goal, but three classes are under 12% and the Ranger is over 30%, so no option meets it. Accept any fourth change whose solved shares meet the goal.

</details>
