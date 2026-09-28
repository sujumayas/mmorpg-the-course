# GS101 · Lab 09: Auditing MMO numbers for the timeline

Assigned in week 9 ([lecture](../lectures/w09-graphical-mmos-meridian-59-ultima-online-everquest.md)). Due at the start of week 12, so that week 10 stays clear for close reading 1. The World of Warcraft extension from week 10 is part of this submission. This lab produces the MMO strand of your timeline project (25% of the course grade); the lab itself is marked pass/revise with the rubric below.

## Objective

Build a sourced dataset of at least 15 figures for three MMOs, classify each figure by what it measures and who published it, chart the business view and the world view side by side, and write a short note on what the published record hides. The skill you are practising is treating every number as a claim with a date, a definition and a speaker.

## Starter materials

Everything below is included in this file.

**1. Seed dataset.** These are the figures used in the week 9 lecture. Its Sources section names the original report behind most of them (press articles, CCP news posts and economic reports, mostly available as archived copies at web.archive.org). You must open at least five of those originals and record what you find, including any place where the original's wording or date differs from the lecture. You may reuse up to five seed rows in your 15; the other ten must be new.

| Game | Date | Figure | Measure | Peak or average | Reported by |
|---|---|---|---|---|---|
| Neverwinter Nights (AOL) | 1991 | 50 per server | W (cap) | cap | to trace |
| Neverwinter Nights (AOL) | 1995 | 500 per server | W (cap) | cap | to trace |
| Neverwinter Nights (AOL) | about 1997 | about 115,000 players; about 2,000 in prime time | S (loose), C | typical | to trace |
| Meridian 59 | 1996 | a few hundred per world | W | not stated | to trace |
| Ultima Online | Dec 1998 | 100,000 subscribers; 12,500 simultaneous | S, C | average | to trace |
| Ultima Online | Oct 2000 | 250,000 | S | not stated | to trace |
| Ultima Online | Jul 2003 | about 250,000 | S | peak | to trace |
| EverQuest | Apr 1999 | 60,000 | S | not stated | to trace |
| EverQuest | Sep 2000 | 259,000 | S | not stated | to trace |
| EverQuest | end 2004 | 550,000 | S | peak | to trace |
| EverQuest | early 2000s | more than 3,000 per server | W | peak | to trace |
| Eve Online | Feb 2013 | over 500,000 | S | not stated | to trace |
| Eve Online | 23 Jan 2011 | 63,170 | C and W (single shard) | peak | to trace |
| Eve Online | 5 May 2013 | 65,303 | C and W (single shard) | peak | to trace |

**2. Dataset template (one row per figure).**

| # | Game | Date (and precision) | Figure as stated | Measure (S, C, W, other) | Peak, average, cap or not stated | Definition used by the source (quote at most a short phrase) | Published by (company, press, third party) | Source (title, publisher, date, URL) | Traced to original? (yes/no, and where) |
|---|---|---|---|---|---|---|---|---|---|

**3. Chart instructions.** Two charts sharing one x axis (years). Top: all `S` figures, log scale. Bottom: all `W` figures (and `C` for single-world games), log scale. Use marker shape for who published the figure, not only colour. Draw undated claims as bands, not points. Any spreadsheet tool is fine; the week 9 interactive's layout is a good model.

**4. Estimate box.** For one gap in your data (a missing `C` or `N`), compute an estimate with `C = r × S` and `N = C / W`, showing the result for three values of `r`. Write the estimate as a sentence that states its assumptions, as in the lecture.

## Steps

1. Choose three MMOs. At least one must be from 1996 to 2003 and at least one must have launched after 2004. World of Warcraft, Lineage, RuneScape, Final Fantasy XI, Star Wars Galaxies, Guild Wars 2, Final Fantasy XIV and Old School RuneScape are all good choices; check any other with your lab instructor.
2. Collect at least 15 figures across the three games (at least four per game), filling every column of the dataset template.
3. Trace at least five seed rows and five of your own rows to the original source. Record where the chain ended (press release, interview, financial report, earnings call, dead link).
4. Classify each figure. When the definition is unclear, say so in the definition column.
5. Build the two charts.
6. Complete the estimate box.
7. Write the note described below.

## Deliverable

- The dataset spreadsheet (15 or more rows, every column filled or marked "not stated").
- The two charts, exported as images or PDF.
- The estimate box.
- A 500-word note answering: what does the published record of your three games hide, and why? Refer to at least three specific gaps or definition changes in your dataset, and to who published which kinds of numbers.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Dataset | 15 or more rows, every figure dated and sourced, definitions recorded, ten or more traced to the original | Most rows complete, fewer traced | Rows missing dates or sources | 30% |
| Classification | S, C and W used correctly; peak and average separated; publishers identified | Minor misclassifications | Measures confused | 15% |
| Charts | Two linked charts, log scales labelled, publisher shown by shape, undated claims drawn as bands | Charts present but hard to compare | Missing or misleading | 15% |
| Estimate | Correct arithmetic, three values of `r`, stated as a publishable, qualified sentence | Arithmetic right, statement overclaims | Estimate presented as fact | 15% |
| Note | Specific, evidence-based account of gaps and who benefits from them, avoids unsupported "biggest" claims | General points with some evidence | Restates the numbers | 25% |
