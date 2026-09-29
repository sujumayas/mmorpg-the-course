# PR402 Lab 13: Economy review worksheet

**Week:** 13 (Economy review). **Guide:** [week 13](../lectures/w13-economy-review.md). **Team lab**, submitted once per team.

## Objective

Turn your live currency ledger into one economy decision. You will build the weekly table per active player, check the simple model against a direct query, size an intervention to a growth target you choose, and write the decision in a form someone else could implement and reverse.

## Starter materials

- Your ledger export, weekly active accounts and three item prices (see "Before class" in the guide).
- The script in section 3 of the guide. Save an adapted copy as `production/week13/review.py` that reads your weekly numbers from `production/week13/ledger.csv` and prints the Part A table and the Part C options.
- `ledger.csv` columns: `week,faucet,sink,active_accounts,active_held,trade_volume,price_1,price_2,price_3`. `active_held` is the currency held by accounts active that week, from a direct database query, not from the model.
- Copy this template into `production/week13/lab13.md`:

```markdown
## Part A. Weekly table
Denominator: weekly active accounts, bots excluded by __, alts handled by __
(paste the table printed by review.py: week, F, S, net, S/F, N, net per player, m, total stock, prices)

## Part B. Model check
| Week | m × N (model) | active_held (query) | Gap % | Explanation if > 10% |
|---|---|---|---|---|

## Part C. Options
Allowed growth g = __ % per week, because __
φ = __  σ = __  v = __  m (latest) = __  cut needed = __

| Option | c | f | e | Removes per player | Net per player | Growth of m |
|---|---|---|---|---|---|---|

## Part D. Decision (intervention spec)
Change and parameter values: __
Who pays (which players, from the cohort table): __
Announcement text (draft): __
Metric, expected value, check date: __
Rollback (what, how fast): __
Or: no change, and the level of m growth at which we would act: __
```

## Steps

1. **Warm-up (10 minutes).** Put the Emberfall numbers from the guide into `ledger.csv` and confirm `review.py` prints `m = 6,095.4` for week 12 and the three option rows. Then replace them with your data.
2. **Part A.** Fill `ledger.csv` for every week since launch from queries you can show. State how bots and alts are handled.
3. **Part B.** Compare `m × N` with `active_held` for every week. Where the gap exceeds 10%, explain it (poor players leaving, many new accounts, a duplication bug, currency held in mail or escrow).
4. **Part C.** Choose `g` and write the reason before you run the options. Cost at least three options, one of which assumes a behavioural response (`e > 0`) or a similar reaction you can name.
5. **Part D.** Decide. Write the spec. If you ship, the change goes out with a patch note and a configuration diff in the repository.

## Deliverable

`production/week13/lab13.md`, `ledger.csv`, `review.py` and its saved output `review-output.txt`, plus the economy review of at most two pages.

**Checkable output:** the instructor runs `.venv/bin/python production/week13/review.py`. Its output must match `review-output.txt` and the tables in the worksheet. Two rows of Part A and one option in Part C are also recomputed by hand from `ledger.csv`.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Table and script | 5 | Script runs; output matches the worksheet; every week since launch present; denominator stated |
| Model check | 4 | Every week compared; every gap over 10% explained with evidence |
| Target and options | 5 | `g` stated with a reason before options; three or more options; one behavioural scenario; arithmetic correct |
| Decision | 4 | Who pays, announcement, metric with expected value, rollback; or a no-change decision with an action level |
| Review document | 2 | Two pages or fewer; a reader outside the team can follow it |
