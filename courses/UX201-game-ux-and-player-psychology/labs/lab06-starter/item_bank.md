# UX201 Lab 06 item bank

Original items written for this course. They are not taken from the Bartle Test, Yee's inventory or the Quantic Foundry profile. Types: A = achieving, E = exploring, S = socialising, K = competing against or acting on other players.

## Part 1: rating scale

Instruction to read aloud or print: "For each statement, how much do you enjoy this in games you play? 1 = not at all, 2 = a little, 3 = moderately, 4 = a lot, 5 = it's one of the main reasons I play."

| Code | Statement |
|---|---|
| R_A1 | Reaching the next level or rank. |
| R_A2 | Collecting everything in a set, or filling an achievement list. |
| R_A3 | Getting a character or account as powerful as it can be. |
| R_A4 | Seeing a progress bar fill up because of my own play. |
| R_E1 | Going somewhere in the world just to see what's there. |
| R_E2 | Working out how a game's hidden rules or formulas work. |
| R_E3 | Finding a secret area or item that most players miss. |
| R_E4 | Trying odd things to see whether the game allows them. |
| R_S1 | Chatting with other players while playing. |
| R_S2 | Making friends I keep in touch with outside a single session. |
| R_S3 | Being part of a group, guild or clan. |
| R_S4 | Helping another player who is stuck. |
| R_K1 | Beating other players in a match or duel. |
| R_K2 | Being ranked above other players on a leaderboard. |
| R_K3 | Outplaying someone who thought they would win. |
| R_K4 | Having an effect on other players that they can't ignore. |

## Part 2: forced choice

Instruction: "For each pair, choose the one you would rather do right now in a game. You must choose one." Randomise the order of pairs and of the two options within each pair for each respondent, and record the letter of the type chosen.

| Code | Option 1 | Option 2 |
|---|---|---|
| FC01 | (A) Finish the last step of a long collection. | (E) Walk into an unmapped area. |
| FC02 | (A) Earn the next rank. | (S) Spend the session chatting with your group. |
| FC03 | (A) Upgrade your gear to the best available. | (K) Win a ranked match. |
| FC04 | (E) Test a strange combination of abilities. | (S) Help a new player learn the game. |
| FC05 | (E) Find a hidden room. | (K) Take first place in a tournament bracket. |
| FC06 | (S) Plan the next event with your guild. | (K) Beat a rival you've lost to before. |
| FC07 | (E) Read up on how damage is calculated. | (A) Clear a daily list of tasks. |
| FC08 | (S) Meet new people in a busy town. | (A) Grind the last levels to the cap. |
| FC09 | (K) Climb a leaderboard. | (A) Unlock a rare title. |
| FC10 | (S) Team up with friends for fun, not rewards. | (E) Map a whole region alone. |
| FC11 | (K) Duel the best player online. | (E) Search for an easter egg. |
| FC12 | (K) Outscore everyone in a match. | (S) Welcome someone into your group. |

Each type appears in 6 of the 12 forced-choice items, so a forced-choice score is `wins / 6 × 100%` and the four scores sum to 200%.

## Data entry

One row per respondent in `motivation_data.csv`. Columns: `respondent, age_band`, then `R_A1` to `R_K4` (1 to 5), then `FC01` to `FC12` (one letter, A, E, S or K). Don't record names.
