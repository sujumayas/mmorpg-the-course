# PR401 Lab 02: Comparables sheet, review coding and launch audience

**Week:** 2 (Market analysis). **Guide:** [week 2](../lectures/w02-market-analysis.md). **Team lab**, submitted once per team.

## Objective

Produce the evidence behind your pitch's market section. You will estimate owner and revenue ranges for your comparables from public review counts, code a sample of their negative reviews into a small codebook, and compute how many daily players your PR402 launch needs to reach its target peak concurrency. The checker confirms that the sheet is complete, that no free-to-play game has been run through the review multiplier, and that your audience number follows from its inputs.

## Starter materials

In [`labs/lab02-starter/`](lab02-starter/):

- `check_comps.py`. Standard library only. Run it with `.venv/bin/python check_comps.py comps.csv audience.csv`. Optional flags `--m-low`, `--m-high`, `--phi` (the realized-price factor `φ`) and `--fee` change the defaults (38, 58, 0.5, 0.30). If you change one, justify it in your market section.
- `comps.csv`. The four games from the guide. *Project: Gorgon* has no reason, so the starter prints `NOT READY` on purpose.
- `audience.csv`. The section 4 example, with `D_claimed` left blank.

Business model values: `paid` (estimated), `paid_plus_offsite` (estimated as a lower bound), `free` and `subscription` (listed, not estimated).

## Steps

1. **Warm-up (10 minutes).** Run the checker on the starter files. Confirm the guide's section 2 table and the `D = 364` result. Fill the missing reason and set `D_claimed` to 364. The checker should print `PASS`.
2. **Lock your comps.** Before looking up any numbers, write two to four comps and a one-line reason each in `comps.csv`. Commit the file. At least one comp must be small or unsuccessful. The commit history shows the order you worked in.
3. **Pull the numbers.** Take review counts from each store page or the public Steam reviews endpoint (no account or personal data needed), with the date. Record the current list price in US dollars and the business model.
4. **Run and read.** Run the checker. Write two sentences about what the ranges say about your niche's size, and one sentence on the least reliable row.
5. **Sample reviews.** For each comp, take the 40 most recent negative English reviews longer than two sentences. Record review IDs or links, not usernames.
6. **Code.** Build a codebook of six to eight codes plus "other" in `codebook.md`, each with a one-line definition and an example paraphrase. Two people code the same 20 reviews independently. Record percent agreement and Cohen's kappa ([MMO405 week 6](../../MMO405-research-methods-in-online-games/lectures/w06-qualitative-methods-interviews.md)). Tighten definitions, then code the rest.
7. **Count.** Tally codes by comp in `codes.csv` with columns `comp,code,count,n_reviews`.
8. **Audience.** Set your target peak CCU and your assumed `q` and `h_day` in `audience.csv`. Fill `D_claimed`.
9. **Write** the one-page market section with the four answers from section 1 of the guide and a positioning sentence built on the most common shared complaint.

## Deliverable

In `preproduction/week02/` in the team repository:

- `comps.csv`, `audience.csv` and the checker output as `check-output.txt`.
- `codebook.md` and `codes.csv`, including the agreement figures for the double-coded 20.

In `docs/`: `market.md`, the one-page market section, and the updated `claims.csv`.

**Checkable output:** the instructor reruns `check_comps.py comps.csv audience.csv` with the defaults, or with the flags your market section justifies. It must print `PASS` and exit with code 0.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Checker passes | 3 | `PASS` on rerun; output file matches |
| Comp choice | 4 | Comps locked before numbers (visible in history); each is close in what the player does; one is small or failed |
| Ranges and caveats | 3 | Low and high reported; `φ` marked as an assumption; least reliable row named |
| Coding | 5 | Codebook has definitions; 20 reviews double-coded with agreement and kappa; counts per comp; no usernames or long quotes |
| Positioning | 3 | Built on a complaint found in more than one comp |
| Audience | 2 | `D` computed and entered as a claim in `claims.csv` |
