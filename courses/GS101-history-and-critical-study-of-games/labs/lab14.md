# GS101 · Lab 14: A virtual census of one game

**Week:** 14 · **Time:** 2 hours in the lab plus up to 3 hours at home · **Weight:** formative, feedback only; the data and reading may be used as evidence in the final essay

**Lecture:** [Week 14, games and representation](../lectures/w14-games-and-representation.md)

## Objective

Run a small content analysis the way the virtual census studies did. With a partner, code every human character in 30 minutes of one game, measure how well you agree, compute representation indexes against two references you choose and justify, and write a reading that combines the count with one portrayal finding and one rules-layer finding.

## Starter materials

Everything below is described here. There is nothing to download except the game and a screen recorder.

- **A game.** Any commercially released game with human characters, approved by your tutor. Record the platform and version. Avoid games where you only ever see one character. Good choices include a story-driven action game, an RPG town, a sports title or a hero shooter's character-select screen plus its tutorial.
- **A recording.** Record the first 30 minutes of play from a new save on the default difficulty. If the game has a character creator, keep the default appearance, as both published censuses did, and note what the default was. Store the recording so both partners can watch it separately.
- **The codebook.** Use exactly these rules so the class's data can be pooled.
  - *Character:* any human figure whose face or body is visible long enough to judge, or who speaks. Crowds of more than 10 identical figures count as one entry marked "crowd".
  - *Human:* yes, no (robot, animal, monster, alien), or cannot determine. Only "yes" rows enter the census.
  - *Role:* primary (controlled by the player at any point in the recording) or secondary (all others).
  - *Gender as presented:* woman, man, nonbinary (only if the game states it), cannot determine.
  - *Age band as presented:* child (under 13), teen (13-19), adult (20-64), older adult (65+), cannot determine.
  - *Agency (portrayal):* for each named secondary character, yes if they make at least one decision in the recording that changes what happens next, otherwise no.
  - *Rule of thumb:* code what the game shows and says, not what you know from outside the recording. When unsure, choose "cannot determine" and write why in the notes column.
- **The code sheet** (each partner fills one independently).

| # | Time stamp | Description (a few words) | Human | Role | Gender as presented | Age band | Named? | Agency | Notes |
|---|---|---|---|---|---|---|---|---|---|

- **Agreement table** for gender (fill in after both partners finish). Rows are partner A's code, columns are partner B's.

| A \ B | Woman | Man | Cannot determine | Row total |
|---|---|---|---|---|
| Woman | | | | |
| Man | | | | |
| Cannot determine | | | | |
| Column total | | | | N |

- **Cohen's kappa, worked.** `κ = (p_o − p_e) / (1 − p_e)`, where `p_o` is the share of characters you coded the same, and `p_e` is the agreement you would expect by chance: for each category, multiply A's row total by B's column total, add these products, and divide by `N²`. Example with 40 characters: A's totals are woman 9, man 29, cannot determine 2; B's are woman 10, man 27, cannot determine 3; you agreed on 8 women, 26 men and 2 cannot-determine. Then `p_o = 36 / 40 = 0.90`, `p_e = (9×10 + 29×27 + 2×3) / 1600 = 879 / 1600 = 0.549`, and `κ = (0.90 − 0.549) / (1 − 0.549) = 0.78`.
- **The interactive's Custom tab** ([`examples/w14-representation-index.html`](../examples/w14-representation-index.html)), or a spreadsheet, to compute shares and indexes. Enter a name, an on-screen count and a reference share for each group.

## Steps

1. **Record (35 min).** Play and record 30 minutes. Note the version and any character-creator default.
2. **Code independently (40 min).** Each partner watches the recording and fills a code sheet without talking to the other. Pause as often as you need.
3. **Agree (15 min).** Match rows by time stamp. Fill in the agreement table for gender and compute `κ`. Do the same for age band if time allows. Then discuss disagreements and produce one reconciled sheet. Keep both original sheets; they are part of the deliverable.
4. **Compute (15 min).** From the reconciled sheet, compute each group's share of human characters, overall and by role. Choose two references and justify each in one sentence: for example the population of the country the game is set in or sold in, the game's reported player base, the source material (a real sports league, a historical setting), or the studio's published workforce figures. Record the source and year for each reference. Compute `RI` and `P` for each group against each reference.
5. **Portrayal and rules (15 min).** Count how many named secondary characters of each gender had agency. Then find one rules-layer fact that bears on representation, for example which characters are playable, what stats or abilities different characters have, or which characters the tutorial makes you protect, follow or fight.
6. **Write (at home).** Write the reading described below.

## Deliverable

One document with:
- Game, version, recording length and character-creator default if any.
- Both original code sheets and the reconciled sheet.
- The agreement table and `κ`, with one sentence on what caused your largest disagreement.
- A results table: group, count, share, and `RI` and `P` against each of your two references, overall and for primary characters.
- A 700-word reading in three parts, kept separate: description (what the numbers show, with denominators), comparison (what changes between your two references and why), and judgment (one arguable claim that uses the count, the agency finding and the rules-layer fact together). State the limits of a 30-minute sample.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Coding discipline | Codebook followed exactly; independent sheets; "cannot determine" used and explained | Minor codebook drift or notes missing | Sheets not independent or codebook ignored | 20% |
| Reliability | `κ` computed correctly; cause of main disagreement identified | `κ` with a small arithmetic slip, or no explanation | No agreement measure | 15% |
| Indexes and references | Both references sourced, dated and justified for a stated question; `RI` and `P` correct overall and by role | References given but one is not justified, or role split missing | Indexes wrong, or reference unnamed | 25% |
| Portrayal and rules finding | Agency count and a specific rules-layer fact, both used in the argument | One of the two present, or both present but not used | Neither present | 15% |
| Claim and structure | Description, comparison and judgment kept separate; one arguable claim; sample limits stated | Parts blur together, or limits not stated | Judgment presented as description | 15% |
| Writing | 650-750 words, plain and precise, sources cited | Within 20% of length, some unclear sentences | Far off length or hard to follow | 10% |
