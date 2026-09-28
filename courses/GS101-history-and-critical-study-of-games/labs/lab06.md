# GS101 · Lab 06: Lineage graph and dice audit

**Week:** 6 · **Time:** 2 hours in the lab plus up to 3 hours at home · **Weight:** part of the timeline project (one lineage entry)

**Lecture:** [Week 06, the RPG lineage: D&D to Ultima and Wizardry](../lectures/w06-the-rpg-lineage-dnd-to-ultima-and-wizardry.md)

## Objective

Trace one role-playing game you choose back to Dungeons & Dragons as a sourced lineage graph, not a tree. Then audit one of its hit or skill-check rules against the d20 model from the lecture, and decide whether the game kept, changed or dropped the die's 5% steps and clamps.

## Starter materials

- **Seed nodes.** Your graph must include at least four of these, with the dates from the lecture: Chainmail (1971), Dungeons & Dragons (1974), dnd on PLATO (1974 to 1975), Oubliette (1977), Akalabeth (1979 or 1980, disputed), Ultima (June 1981), Wizardry (September 1981), MUD1 (1978), Dragon Quest (May 1986), Baldur's Gate (1998).
- **Edge template.** Every arrow in your graph gets a label in this form:

| From | To | Inherited feature (specific) | Evidence the later designer knew the earlier work | Source |
|---|---|---|---|---|
| Wizardry | Dragon Quest | (name one specific feature you can show in both games) | Horii's own statements that he played Wizardry and Ultima | Wikipedia, "Dragon Quest (video game)" |

- **Evidence strength scale.** Mark each edge as one of these:
  - **A** the designer said so (interview, postmortem, book).
  - **B** a named historian or journalist makes the link with a citation.
  - **C** resemblance only. Allowed in the graph, but drawn dashed and never counted as proof.
- **Dice audit sheet.** A spreadsheet with columns: situation, displayed or measured hit chance, your predicted `B` and `AC` (or equivalent), predicted chance from `P = min(0.95, max(0.05, (21 + B − AC)/20))`, difference.
- **Drawing tool.** Paper, draw.io, or any diagram tool. No game logos or screenshots in the graph.

## Steps

1. **Choose your game.** Any role-playing game released after 1990 that shows or documents a hit chance or a skill-check roll. Get approval from your tutor if it has no public documentation of its rolls.
2. **Build the graph.** At least eight nodes and ten labeled edges, including your game and four seed nodes. At least one edge must point "backward" in geography (for example, a Japanese game influencing a Western one).
3. **Grade the evidence.** Mark each edge A, B or C. At least five edges must be A or B.
4. **Audit the dice.** Find the game's hit or check rule in official documentation or a maintained wiki, noting the version or patch. Rewrite it in the lecture's form, or explain why it cannot be. Record at least six observed or documented chances in the audit sheet, compare them with your prediction and explain any difference.
5. **Verdict.** Answer in one paragraph each. (a) Stepped or smooth? (b) Where are the floor and the ceiling, if any? (c) Using the "what +1 is worth" idea, name the range of bonuses where a +1 is worth the most, and say whether the game's items and levels actually give players bonuses in that range.
6. **Critique.** In 250 words, name one thing your graph leaves out (a game with no surviving sales data, a co-creator, a non-commercial influence) and how you would find evidence for it.

## Deliverable

The graph as an image or PDF, the edge table with evidence grades and sources, the audit spreadsheet, and the three verdict paragraphs plus the 250-word critique in one PDF. Name the files `GS101-lab06-<surname>`.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Lineage graph | 8+ nodes, 10+ labeled edges, specific inherited features, one backward edge, correct dates | Meets counts but features vague or a date wrong | Tree with unlabeled arrows | 25% |
| Evidence grading | 5+ edges at A or B, every edge sourced, C edges dashed | Sources present but grades inconsistent | No sources | 20% |
| Dice audit | Rule found with version cited, rewritten into the d20 form, six+ comparisons with differences explained | Rule found, fewer comparisons or differences unexplained | No rule or no comparison | 25% |
| Verdicts | All three answered with numbers from the audit | Answers present without numbers | Missing | 15% |
| Critique | Names a concrete omission and a realistic way to find evidence | Omission named, no method | Missing | 15% |
