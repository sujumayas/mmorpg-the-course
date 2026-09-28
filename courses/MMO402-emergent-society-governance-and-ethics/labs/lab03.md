# MMO402 · Lab 03: Count the council

**Week:** 3 · **Time:** 2 hours in lab plus about 3 hours at home · **Weight:** one of the case analyses (30% of the course in total)

## Objective

Count a ten-seat player council election under single transferable vote (STV) and under block voting, measure how each group's seats move as casual turnout changes, and recommend a council design. This lab applies the quota arithmetic from [week 3](../lectures/w03-eves-council-of-stellar-management.md) to a full count with transfers.

## Starter materials

- `lab03-starter.py`: a Python 3 script (standard library only) with a working STV count (Droop quota, fractional surplus transfer, lowest-candidate elimination, ties broken alphabetically), a block-voting count, and a helper `scale_group(ballots, prefix, factor)` that multiplies every ballot group whose first choice starts with `prefix`. Run `python lab03-starter.py lab03-ballots.csv 10`.
- `lab03-ballots.csv`: a made-up election with 20,700 ballots in 18 groups. Candidates are named by group. N1 to N5 are a disciplined bloc (6,000 ballots). L1 and L2 are an organized low-security group (2,000). W1 and W2 are an organized wormhole group (1,500). H1 to H8 are backed by unorganized players (10,500 ballots, each naming two to four candidates). S1 and S2 are two solo candidates (700 ballots). Together H and S make up the lecture's 11,200 unorganized ballots. No real player or group is represented.
- The file format is `count,ranking`, with `ranking` written as `A>B>C`. You may add rows.

## Steps

1. **Baseline.** Run the starter. Record the Droop quota and the winners under both rules. Group the winners by letter and confirm that STV gives N 3, L 1, W 1, H 5 and block voting gives N 5, H 5.
2. **Read the count.** From the STV log, identify the round in which the first H candidate is elected and explain where their votes came from. Which eliminated candidates' ballots decided the last three seats?
3. **Turnout sweep.** Using `scale_group(b, "H", f)`, recount both ways for `f` = 1.0, 0.75, 0.5, 0.25 and 1.5. Record each group's seats in a table and plot bloc N's seats against the H turnout factor for both rules on one chart.
4. **Check the guarantee.** For each run in step 3, compute `floor(6,000 / Q)` by hand and confirm that bloc N never wins fewer seats than that under STV. Note any run where it wins more, and explain which transfers gave it the extra seat.
5. **Break the bloc's discipline.** Edit the file so that 1,000 of the bloc's ballots rank only N1. Recount under STV. What happens to the bloc's seats, and why?
6. **Design.** Propose one change to the council's rules (reserved seats, some members chosen by lottery, a turnout drive, more or fewer seats, or your own). Implement it in code if you can. Otherwise argue it with quota arithmetic. Show the seats by group under your rule at `f` = 1.0 and 0.5.

## Deliverable

Your modified script or a clear record of the changes, the turnout table and chart from step 3, and a recommendation of about 500 words to a studio planning its first player council. The recommendation must state the voting rule, the number of seats, any reserved or random seats, and the powers and information rules (NDA or not) you propose, and must cite at least three numbers from your runs.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Baseline and reading the count | Winners correct, transfers explained round by round | Winners correct, explanation thin | Winners wrong | 15% |
| Turnout sweep | All five runs, both rules, correct table and labelled chart | One run or one rule missing | Fewer than three runs | 25% |
| Guarantee and discipline checks | Hand-computed guarantees match, extra seats explained, step 5 explained with quota arithmetic | One check done | Neither done | 20% |
| Design proposal | Rule change implemented or argued with correct arithmetic, results at two turnouts | Proposal without numbers at both turnouts | Missing | 20% |
| Recommendation | Covers rule, seats, powers and information, three or more numbers, trade-offs named | Covers some elements | Opinion without numbers | 20% |

<details>
<summary>Instructor check values</summary>

- Baseline: 20,700 ballots, quota 1,882. STV winners N1, N2, N3, H1, H2, L1, H6, H4, H5, W1. Block winners N1 to N5, H1, H2, H3, H6, H4.
- `f = 0.5`: 15,450 ballots. STV gives N 4 (N1 to N4), L 1, W 1, H 4. Block gives N 5, L 1, W 1, H 3.
- `f = 0.25`: 12,825 ballots. STV gives N 5, L 2, W 1, H 2. Block gives N 5, L 2, W 2, H 1.
- Guarantees: at `f = 0.5`, `Q = 1,405` and `floor(6,000 / 1,405) = 4`; at `f = 0.25`, `Q = 1,166` and the guarantee is 5.

</details>
