# MMO401 · Lab 12: Incident response from a server ledger

**Week:** 12 · **Time:** 2 hours in lab plus about 3 hours at home · **Weight:** part of the ABM labs (40%)

## Objective

You are the economist on call. It is the end of day 20 on a live server, and a community manager has forwarded a forum thread about "gold everywhere". Using only the server ledger and an account table, find the shock, measure it, estimate how fast it is leaking, choose a response with the model from [week 12](../lectures/w12-economic-shocks-exploits-and-rollbacks.md), and write the incident memo.

## Starter materials

- [`lab12-ledger.csv`](lab12-ledger.csv): 30 days of server totals in millions of gold. Columns: `day`, `money_start_M` (a direct count of all wallets at the start of the day), `faucets_M` and `sinks_M` (logged flows) and `money_end_M` (direct count at the end). Days 21 to 30 are there for step 6 only. At the time of the incident you have days 1 to 20.
- [`lab12-accounts.csv`](lab12-accounts.csv): end-of-day balances, in millions, for the 12 accounts with the largest balance changes between days 14 and 22. The account table covers only these 12. The rest of the server is not shown.
- Server facts from the live-ops team: `N = 40,000` active players, playing `h = 2.5` hours a day on average. The last clean backup before the shock is the start of day 17, and a rollback can only go back to a backup. Your studio's incident runbook sets `λ = 15,000` player-hours per point of price rise.
- Any spreadsheet or Python. No other tools needed.

## Steps

1. **Reconcile.** For days 1 to 20, compute the residual `M(end) − M(start) − (faucets − sinks)`. State the noise level on normal days, the days with an abnormal residual, and the total `ΔM`. Express `ΔM` as a share of `M` at the end of day 16.
2. **Find the accounts.** In the account table, classify each account as a likely exploiter, a likely recipient (an innocent trader who sold goods to exploiters) or unrelated. Give one sentence of evidence for each class.
3. **Estimate `q`.** From the exploiter accounts, estimate the daily leak rate `q` over days 19 to 22. Show the calculation. (Use the combined balance above each account's pre-shock level.)
4. **Compare responses** at the end of day 20. Compute `X`, `L`, the price rise after a clawback, and the harm of rollback, clawback and inaction in player-hours. Then compute the same comparison as if a daily residual alert with a 1% threshold had fired at the end of day 17.
5. **Decide and plan clean-up.** Choose a response for the end of day 20. Include whether to freeze trading now, what the clawback rule is for recipients, and a temporary sink that removes the leaked gold within about 8 days. State the size of the sink increase in millions per day.
6. **Look ahead.** Now use days 21 to 30 of the ledger. Did anything else happen? What does the money supply do if you only claw back from exploiters and add no temporary sink?

## Deliverable

1. A spreadsheet or notebook with steps 1 to 6.
2. An incident memo of about 400 words to the game director. It must include the size of the shock, when it started, the response you chose with the harm numbers for all three options, your clawback rule for recipients, the clean-up sink and a one-line lesson for the runbook.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Reconciliation (step 1) | Residuals correct, noise level stated, `ΔM` and its share of `M` correct | Shock found, size or share wrong | Shock not found | 20% |
| Account classification (step 2) | All 12 accounts classified with evidence | Exploiters found, recipients missed | Missing | 15% |
| Leak rate (step 3) | `q` correct with working | Reasonable estimate, working unclear | Missing | 15% |
| Response comparison (step 4) | All harms correct for both detection times | One detection time done | Missing | 20% |
| Decision and clean-up (step 5) | Response, freeze decision, recipient rule and sized sink all justified | Response justified, clean-up vague | Response with no numbers | 15% |
| Memo | Director can act on it: numbers, decision, rule, lesson | Complete but hard to act on | Missing parts | 15% |

<details>
<summary>Instructor check values</summary>

- Step 1: residuals on normal days are within ±0.1 million (logging noise). Day 17 residual +90.0, day 18 residual +60.0, total `ΔM = 150` million. `M` at the end of day 16 is 1,011.2 million, so the shock is 14.8%.
- Step 2: exploiters `acct_7731`, `acct_2204`, `acct_5518`, `acct_9046` (near-empty accounts that jump on day 17 and 18, then fall). Recipients `acct_1180`, `acct_3321`, `acct_6402`, `acct_8870` (steady accounts that start rising on day 18 in step with the exploiters' fall). Unrelated `acct_0415`, `acct_4790`, `acct_7007`, `acct_9312`.
- Step 3: combined exploiter balance above pre-shock levels is 127.5 (day 18), 95.62 (day 19), 71.72 (day 20), 53.79 (day 21), 40.34 (day 22). Each ratio is 0.75, so `q = 0.25`.
- Step 4, end of day 20: `X = 71.72`, `L = 78.28` million, price rise `78.28 / 1,011.2 = 7.74%`. Clawback harm `15,000 × 7.74 ≈ 116,100`. Rollback to the start of day 17 loses 4 days: `40,000 × 2.5 × 4 = 400,000`. Inaction `15,000 × 14.83 ≈ 222,500`. Clawback wins.
- Step 4, end of day 17: the 60 million of day 18 has not been created yet, and none of day 17's 90 million has leaked. Clawback harm 0 (plus the cost of patching the bug before day 18). Rollback of 1 day: 100,000. A same-day alert makes the clawback almost free, which is the runbook lesson.
- Step 5: normal sinks average about 41 million a day. Removing 78 million in 8 days needs about 9.8 million a day, roughly a 24% increase. Accept a clear recipient rule: recipients keep gold received in trades at or near market prices.
- Step 6: days 21 to 30 are normal (residuals within ±0.1). Without a temporary sink, `M` stays about 150 million above trend minus whatever the clawback removes. After clawing back `X` at day 20, about 78 million of excess remains permanently.

</details>
