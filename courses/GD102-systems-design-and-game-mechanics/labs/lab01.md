# GD102 · Lab 01: Interaction audit

**Week:** 1 ([Systems thinking: parts, relationships, emergence](../lectures/w01-systems-thinking-parts-relationships-emergence.md))
**Time:** one 2-hour lab session plus up to 2 hours at home
**Work:** individually; you may pick the same game as a neighbor but build your own sheet

## Objective

Turn a shipped game's rules into an interaction graph stored as an adjacency matrix, compute degrees and two-step chains with formulas, find the hubs, and use the `d(u) + d(v)` rule to argue for one new element. By the end you should be able to say which part of a game's rule set produces most of its emergent play, with a number attached.

## Starter materials

- Any spreadsheet program (Google Sheets, LibreOffice Calc or Excel). No code needed.
- A game you can play or have played recently with at least 8 interacting elements. Suggestions: a survival or crafting game, a tactics game with terrain or surfaces, a deck-builder with keywords, an immersive sim. Board games are fine.
- The toy chemistry set from lecture section 2, as a check case. Type this into a sheet named `Check` exactly as shown (1 means a rule links the row and column elements):

```
,Fire,Grass,Wind,Water,Metal,Lightning
Fire,0,1,1,1,1,0
Grass,1,0,0,0,0,0
Wind,1,0,0,0,0,0
Water,1,0,0,0,0,1
Metal,1,0,0,0,0,1
Lightning,0,0,0,1,1,0
```

- Check values for that matrix: `E = 6`, degrees `4, 1, 1, 2, 2, 2`, `C2 = 9`.
- Formulas from lecture: `d(v)` = row sum; `E = Σ d(v) / 2`; `C2 = Σ d(v)(d(v) − 1)/2`; a new rule u–v adds `d(u) + d(v)` chains.

## Steps

### Part A: build and verify the machine (25 minutes)

1. In the `Check` sheet, add a column `d` with the row sum of each element's row.
2. Add a column `pairs` with `=d*(d-1)/2`. Below the table, compute `E` and `C2`. Match the check values before going on.
3. Add a "candidate" block: two cells where you type element names, and a formula cell that looks up both degrees and returns their sum. Test it with Grass/Wind (2) and Fire/Lightning (6).
4. Add a symmetry check cell that counts cells where the matrix differs from its transpose. It must read 0. This catches the most common data-entry error.

### Part B: audit your game (50 minutes)

5. Copy the sheet to a new sheet named after your game. Choose 8 to 12 elements. Write them in a separate `Rules` sheet as a list of rules, one sentence each, with the two elements they connect. Every rule must be something you have seen happen in the game, not something you assume.
6. Fill the matrix from the `Rules` list. Recompute `E`, degrees and `C2`. Confirm the symmetry check reads 0 and that the number of rule sentences equals `E`.
7. Sort elements by degree. Mark the top one or two as hubs. Compute the share of all chains that pass through the hubs (`pairs` of the hubs divided by `C2`).
8. Pick three two-step chains through your top hub. For each, write whether players use it on purpose (you have seen it or seen it discussed), whether it looks intended by the designers, and whether it could be an exploit.

### Part C: propose one new element (30 minutes)

9. Design one new element for your game. Give it exactly three rules connecting it to existing elements. Add it as a new row and column.
10. Record how many chains each of the three rules adds, in the order you add them, and the final `C2`. Confirm that the sum of the three increments equals the change in `C2`.
11. Design a second version of the new element that connects only to low-degree elements. Record its chain increase. Compare the two versions.

### Part D: write it up (at home)

12. Write a memo of at most 400 words to the lead designer of your chosen game. Recommend one of your two versions of the new element. Use at least three numbers from your sheet (for example, the hub's share of chains, the chain increase of each version, and the number of chains through the new element). Name one chain your new element creates that you would need to test carefully, and say why.

## Deliverable

One spreadsheet file with sheets `Check`, `Rules`, `<your game>` and `Proposal`, plus the memo as a PDF. All counts must be computed with formulas.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Check sheet (15%) | All check values match; symmetry check and candidate lookup work | Check values match, one helper missing | One check value off | Not attempted |
| Rule evidence (20%) | 8 to 12 elements; every rule is a clear sentence from observed play; rule count equals `E` | Minor gaps in evidence or one mismatch | Several rules vague or assumed | Rules list missing |
| Structural analysis (25%) | Degrees, `C2`, hubs and hub share correct; three chains classified with reasons | Numbers correct, chain classification thin | Arithmetic errors in `C2` or degrees | Missing |
| Proposal (25%) | Both versions built; increments sum to the change in `C2`; comparison uses the `d(u) + d(v)` rule explicitly | Both versions built, comparison vague | One version only | Missing |
| Memo (15%) | Clear recommendation, three or more numbers, a named risky chain with a reason | Recommendation with numbers, risk vague | Recommendation without numbers | Missing |
