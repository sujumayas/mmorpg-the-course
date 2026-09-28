# GD101 · Lab 13: Genre map of your prototype

**Week:** 13 · **Time:** 2 hours in the lab plus up to 1 hour at home · **Weight:** counts toward the analysis essay component (positioning evidence)

**Lecture:** [Week 13, Genres as clusters of mechanics](../lectures/w13-genres-as-clusters-of-mechanics.md)

## Objective

Place your paper prototype in mechanic space. You will code your game and five published games as sets of mechanics, compute every pairwise Jaccard similarity, find your nearest neighbour, cluster the games at two thresholds, and write a positioning note that becomes the "what it is like" line of your week 14 one-pager.

## Starter materials

Everything below is included here. You need a spreadsheet tool (any), your prototype's current rules, and the grid your group made in the week 13 in-class activity if you have it.

**1. Reference grid (from the lecture, for checking your formulas).** Copy this onto a tab called `Reference`. Your formulas must reproduce the lecture's values before you use them on your own data.

| Game | P | R | T | A | M | J | D | U | G |
|---|---|---|---|---|---|---|---|---|---|
| Rogue (1980) | 1 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| Spelunky (2008) | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 1 | 0 |
| Hades (2020) | 1 | 1 | 0 | 1 | 1 | 0 | 0 | 1 | 0 |
| Slay the Spire (2019) | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 0 |
| Dominion (2008) | 0 | 1 | 1 | 0 | 0 | 0 | 1 | 0 | 0 |
| Super Metroid (1994) | 0 | 0 | 0 | 1 | 1 | 1 | 0 | 0 | 1 |

Check values: J(Slay the Spire, Dominion) = 0.60, J(Slay the Spire, Rogue) = 0.50, J(Spelunky, Hades) = 0.83.

**2. Spreadsheet formula for Jaccard on 0/1 rows.** If game A's row is in `B2:J2` and game B's row is in `B3:J3`:

```
intersection = SUMPRODUCT(B2:J2, B3:J3)
union        = SUMPRODUCT(--((B2:J2 + B3:J3) > 0))
J            = IF(union = 0, 0, intersection / union)
```

**3. Column-writing rules.** Each mechanic column must be:

- a rule or procedure, not a feeling ("you can trade cards with other players," not "social");
- checkable by a stranger in one play of the game;
- present in at least one and absent in at least one of your six games (a column that is all 1 or all 0 carries no information).

**4. Candidate columns** (use or replace; you need 10 to 12 in total, and at least 4 must be your own):

| Code | Mechanic |
|---|---|
| TB | Turn-based: nothing happens until the player acts |
| RT | Real-time: the game advances on a clock |
| RS | Randomized setup or content each play |
| HC | Hidden information: some game state is secret from some players |
| DB | Deck-building during play |
| DR | Dice or other random resolution of actions |
| TR | Trading between players |
| EL | Player elimination before the game ends |
| AP | Area or tile placement on a shared board |
| WP | Worker placement: claiming limited action spaces |
| SC | Simultaneous action selection |
| CO | Cooperative: all players win or lose together |

**5. Blank positioning note** (copy into a document):

```
Nearest neighbour: <game>, J = <value> on <n> columns.
Shared mechanics: <list>.
What makes us different (in the union but not the intersection): <list>.
Deliberate break: players of <neighbour> expect <expectation>; our game <break>, because <pillar or experience goal>.
Cluster at t = 0.5: <members>. Cluster at t = 0.3: <members>.
Column most responsible for our position: <code>. Without it, our nearest neighbour becomes <game>.
```

## Steps

1. **Check the formula (15 min).** Build the `Reference` tab and a 6 × 6 similarity table using the formula above. Match the three check values. Do not continue until they match.
2. **Choose your games (10 min).** Pick five published games (board, card or digital) that you think are closest to your prototype. At least two must come from a different medium than your prototype (for a card game, pick at least two digital games, or the reverse).
3. **Write the columns (20 min).** On a tab called `Grid`, write 10 to 12 mechanic columns following the rules in starter item 3. Put the full definition of each column in a row under the codes.
4. **Code the grid (20 min).** Fill the 6 × (10 to 12) grid with 0 and 1. For every published game, add a comment on each cell you were unsure about, and name the version or edition you coded.
5. **Compute (20 min).** On a tab called `Similarity`, build the 6 × 6 J table, a nearest-neighbour column (use `INDEX`/`MATCH` on the row maximum, excluding the diagonal), and cluster lists at t = 0.5 and t = 0.3. Clusters may be worked out by hand from the table; show your chain of links.
6. **Sensitivity (15 min).** For each column, remove it and record whether your prototype's nearest neighbour changes. Record the results on a tab called `Sensitivity`, one row per column. The column that changes it (or changes J the most) is "most responsible."
7. **Swap and check (10 min).** Swap grids with another team. Each team codes one of the other team's published games blind, and you compare cells. Record the number of disagreeing cells.
8. **Write the note (at home).** Fill in the positioning note and add a 300-word paragraph that explains your position to someone who has not played your game.

## Deliverable

- The spreadsheet with tabs `Reference`, `Grid`, `Similarity`, `Sensitivity`.
- The positioning note plus the 300-word paragraph, as one PDF.
- The number of disagreeing cells from step 7 and one sentence on the column that caused most of them.

## Rubric

| Criterion | Excellent (4) | Good (3) | Needs work (2) | Missing (0-1) |
|---|---|---|---|---|
| Formulas (15%) | Reference values reproduced; J table, nearest neighbours and clusters correct | One error that propagates | Several errors, or values typed in instead of computed | Missing |
| Column quality (25%) | 10 to 12 columns, all checkable rules, none constant, at least 4 original | One column is a feeling or is constant | Several vague or constant columns | Missing |
| Coding (20%) | Every cell defensible, versions named, uncertain cells commented | A few uncoded versions or missing comments | Cells contradict the column definitions | Missing |
| Sensitivity (15%) | Every column tested; most responsible column identified and explained | Tested but explanation thin | Only some columns tested | Missing |
| Positioning note (25%) | Nearest neighbour, differences and one deliberate break stated with numbers; the break is tied to a named pillar or experience goal | Complete, break not tied to a goal | Vague, or contradicts the table | Missing |
