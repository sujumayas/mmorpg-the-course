# GS101 · Lab 07: A mod lineage for the timeline project

Assigned in week 7 ([lecture](../lectures/w07-the-pc-era-strategy-simulation-modding.md)). Due at the start of week 9. This lab produces one strand of your timeline project (25% of the course grade); the lab itself is marked pass/revise with the rubric below.

## Objective

Build a sourced lineage table for one genre or game that began as a mod, compute its tool and commercial lags, and write a short argument about what caused the timing. The skill you are practising is turning a "who invented it?" story into a dated, sourced chain with stated coding rules.

## Starter materials

Everything below is included in this file. Copy the tables into a spreadsheet.

**1. Candidate lineages (pick one, or propose your own to your lab instructor by the end of week 7).** Do not pick one of the six rows already worked in the lecture as your main case, though you may use them as comparison rows.

- Doom level editing to a commercial level-design career or product of your choice.
- Aeon of Strife (StarCraft) to DotA (Warcraft III) to one commercial MOBA.
- Team Fortress (Quake) to Team Fortress Classic to Team Fortress 2.
- A tower-defense custom map lineage to a standalone tower-defense game.
- A Minecraft, Skyrim, Half-Life 2 or other mod that became a standalone commercial game.

**2. Lineage table template.** One row per link in the chain. At least five links.

| # | Item (game, mod or map) | Type (host, mod, standalone, tool) | Date (as precise as the source allows) | Precision (day, month, year) | Maker | Owner of the host it runs on | Source (title, publisher, date, URL) | Source type (developer, contemporary press, wiki, interview) |
|---|---|---|---|---|---|---|---|---|
| 1 | | | | | | | | |

**3. Lag sheet template.**

| Chain | `t_H` | `t_M` | `t_S` | `L_M = t_M − t_H` | `L_S = t_S − t_M` | `L = t_S − t_H` | Owner `O` |
|---|---|---|---|---|---|---|---|
| Main coding | | | | | | | |
| Alternative coding A | | | | | | | |
| Alternative coding B | | | | | | | |

**4. Comparison rows from the lecture** (paste into the lag sheet so you can compute medians with your case added).

| Chain | `t_H` | `t_M` | `t_S` | Owner |
|---|---|---|---|---|
| Team Fortress | 1996 | 1996 | 1999 | third-party |
| Counter-Strike | 1998 | 1999 | 2000 | host-owned |
| DotA to League of Legends | 2002 | 2003 | 2009 | third-party |
| DotA to Dota 2 | 2002 | 2003 | 2013 | third-party |
| DayZ | 2009 | 2012 | 2013 | host-owned |
| Battle royale to PUBG | 2009 | 2013 | 2017 | third-party |

**5. Source quality rules.** Every date needs at least one source. Prefer, in order: the developer's own site or announcement, contemporary press (dated within a year of the event), a book or academic paper, a maintained wiki with a citation you have followed. A wiki sentence with no citation does not count on its own. If two sources disagree, record both and say which you used.

## Steps

1. **Choose and scope.** Pick a lineage and write one sentence stating what counts as "the mod" and what counts as "the standalone" in your case.
2. **Collect dates.** Fill the lineage table. Record the precision honestly; "2003" is fine if that is all the source gives.
3. **Code ownership.** For each standalone link, decide whether the company that owned the host (or a company it bought) made it. Write one line justifying each coding.
4. **Compute lags.** Fill the lag sheet for your main coding and two alternatives (for example, early access versus full release, or a different "first public" version of the mod).
5. **Recompute medians.** Add your main coding to the six comparison rows and recompute median `L_S` for host-owned and third-party groups. Then do it again with each alternative coding.
6. **Draw it.** Produce one aligned timeline figure (years since host release on the x axis) with your case and the six comparison rows. The week 7 interactive's "add a row" form is fine; export or screenshot it, or draw it by hand and photograph it.
7. **Argue.** Write the 400-word argument described below.

## Deliverable

A PDF of at most three pages plus the spreadsheet.

- The lineage table (at least five links, every date sourced).
- The lag sheet with main and two alternative codings, and the recomputed medians.
- The aligned timeline figure.
- A 400-word argument answering: what caused the timing in your case? Address tools, ownership and at least one other factor (licence terms, platform, team hiring, market). State whether your case supports, weakens or does not bear on the lecture's pattern, and name the one coding choice most likely to change your conclusion.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Sources | Every date sourced, source types recorded, disagreements noted, citations followed past the wiki | Most dates sourced, some wiki-only | Dates unsourced or invented | 30% |
| Lineage and coding | Five or more links, clear rules for "mod" and "standalone", ownership coding justified | Links present but rules or justifications thin | Fewer than four links or coding unexplained | 20% |
| Calculations | Lags and medians correct for all three codings | Minor errors | Missing or wrong | 15% |
| Figure | Aligned timeline readable, labelled, includes comparison rows | Present but hard to read | Missing | 10% |
| Argument | Names causes beyond "tools", tests the pattern honestly, names the fragile coding choice, avoids "first" claims it cannot support | Reasonable but one-sided | Restates dates without an argument | 25% |
