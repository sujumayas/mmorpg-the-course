# GD101 · Lab 14: One-page design and pitch

**Week:** 14 · **Time:** 2 hours in the lab plus up to 3 hours at home · **Weight:** part of the paper prototype component (40%); the one-pager is submitted with the final prototype in week 15

**Lecture:** [Week 14, Design documents: one-pagers and pitch](../lectures/w14-design-documents-one-pagers-and-pitch.md)

## Objective

Write a one-page design for your paper prototype whose pillars are each held up by at least two mechanics, run the swap test on it, and record a three-minute pitch in which every claim points to a line on the page. Showcase playtesters in week 15 will read your one-pager before they play.

## Starter materials

Everything below is included here. You also need your positioning note from [Lab 13](lab13.md), your current rules, and your playtest notes from earlier labs.

**1. One-pager template.** Copy it into a document. The whole page, excluding the grid, must be 400 to 650 words and fit on one A4 or Letter page at 10-point type or larger.

```
<Title>                                   v<n>, <date>
One line (under 25 words): <what the player does, present tense>

What it is like (under 60 words):
  Nearest neighbour: <game> (J = <value>, from Lab 13).
  Deliberate break: <what we change and why>.

Pillars (3 to 5, written as what a tester says after playing):
  P1 "<...>"
  P2 "<...>"
  P3 "<...>"

Core loop (4 to 6 steps, or a diagram):
  1. ...

Mechanics (only those that differ from the nearest neighbour):
  m1 ...
  m2 ...

Pillar-mechanic grid: (table, see item 2)

Out of scope (3 to 5 bullets):
  - ...

Evidence so far (under 80 words, with numbers):
  ...

Open questions (2 or 3, each with how you will find out):
  - ...

Change log (below the page, not counted in the word limit):
  v<n>  <date>  <change>  <reason and evidence>
```

**2. Grid template.** Mechanics as rows, pillars as columns, 0 or 1 in each cell, totals on both edges.

| Mechanic | P1 | P2 | P3 | Load | Note |
|---|---|---|---|---|---|
| m1 | | | | | |
| m2 | | | | | |
| ... | | | | | |
| **Support** | | | | | |

**3. Swap test table.** One row per mechanic.

| Remove | P1 | P2 | P3 | Verdict (safe / structural / critical) |
|---|---|---|---|---|
| m1 | | | | |

Verdicts: critical if any pillar drops to 0; structural if any pillar drops from 2 or more to 1; otherwise safe.

**4. Worked reference (to check your method).** A hypothetical one-pager for a two-player tile game, "Flood Map." Pillars: P1 "I had to choose between helping myself and hurting you," P2 "The board kept changing under me," P3 "I could see the end coming and plan for it." Mechanics: m1 shared tile draft (P1), m2 rising water removes edge tiles each round (P2, P3), m3 tiles can block the rival's path (P1), m4 public round counter (P3), m5 bonus for longest path (P1), m6 decorative map art on tiles (none). Correct results: support P1 = 3, P2 = 1, P3 = 2; loads 1, 2, 1, 1, 1, 0; total links 6 both ways; m6 orphan; P2 fragile; m2 is critical (removing it leaves P2 at 0) and also drops P3 to 1; m4 is structural (P3 to 1); m1, m3, m5 are safe. A good revision adds a second support for P2 (for example, "random event card each round shifts two tiles") and either cuts m6 or labels it "kept for readability, no pillar."

**5. Pitch timing sheet.**

| Part | Time | Line on the page it points to |
|---|---|---|
| Hook | 0:00 to 0:20 | |
| What it is like | 0:20 to 0:40 | |
| One turn | 0:40 to 1:40 | |
| Why it holds together | 1:40 to 2:20 | |
| Evidence | 2:20 to 2:45 | |
| Ask | 2:45 to 3:00 | |

## Steps

1. **Check the method (15 min).** Compute the grid, supports, loads and swap test for the "Flood Map" reference. Match the correct results before you start on your own game.
2. **Draft pillars (15 min).** Write three to five pillars as tester quotes. Test each one: if it links to every mechanic, or to none, rewrite it.
3. **Build your grid (20 min).** List the mechanics that make your game different from its nearest neighbour. Fill the grid, add both totals and confirm they agree.
4. **Run the swap test (15 min).** Fill the swap test table. For every fragile pillar, either add a second support, or add one sentence to the page explaining why one is enough for now. For every orphan, cut it or label the reason it stays.
5. **Cross-read (20 min).** Give your one-pager, without the grid, to another team. They fill in a grid from the text alone. Compare and circle every cell that differs. Fix the page so the links are visible in the text, or add a playtest question for links your testers never confirmed.
6. **Write the page (at home).** Fill in the template. Put the grid and swap test at the bottom. Add at least three change-log lines that record real decisions from weeks 8 to 14.
7. **Record the pitch (at home).** Record a pitch of 2:45 to 3:15 using the timing sheet. Fill the right-hand column so each part names the line on the page it points to. Watch the recording once and cut any claim that points to nothing.

## Deliverable

- The one-pager as a PDF, one page plus the grid, swap test and change log on a second page.
- The pitch recording (video or audio, 2:45 to 3:15) and the completed timing sheet.
- The cross-read grid from step 5 with circled disagreements and one sentence per disagreement on what you changed.

## Rubric

| Criterion | Excellent (4) | Good (3) | Needs work (2) | Missing (0-1) |
|---|---|---|---|---|
| Structure and length (15%) | All nine parts present, within word limits, fits on one page, versioned and dated | One part missing or over length | Several parts missing, or over one page | Missing |
| Pillars (15%) | 3 to 5 specific pillars written as tester quotes; none links to everything | One pillar vague | Pillars are adjectives or features | Missing |
| Grid and swap test (25%) | Totals correct and agree; every fragile pillar and orphan handled with a written reason; swap verdicts correct | One wrong verdict or one unhandled orphan | Totals wrong or swap test missing | Missing |
| Evidence and change log (15%) | Evidence uses numbers from playtests; at least three change-log lines with reasons and evidence | Evidence qualitative, or log thin | No evidence, or log invented after the fact | Missing |
| Cross-read (10%) | Disagreements circled and each resolved on the page or turned into a playtest question | Most resolved | Grid swapped but not used | Missing |
| Pitch (20%) | 2:45 to 3:15; one concrete turn with a real decision; every claim points to the page; the deliberate break named in the first 40 seconds | One part rushed or one unsupported claim | Feature list or adjective pitch; over time | Missing |
