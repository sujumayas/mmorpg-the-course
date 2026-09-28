# MMO402 · Lab 09: Case briefs with the layer test

**Week:** 9 · **Time:** 2 hours in lab plus about 3 hours at home · **Weight:** part of the case analyses (30%)

## Objective

Practise the reasoning of [week 9](../lectures/w09-virtual-property-and-law.md) on cases you have not seen worked. You write short case briefs, run each case through the four-question layer test, and then write the loss policy for a fictional MMO so that none of its own cases fall between layers.

## Starter materials

**The layer test** (from the lecture, section 2):

```
Q1  Who took it?                          Operator → Contract layer
Q2  Control taken by outside means?       Yes → Law layer
Q3  Operator's rules forbid the method?   Yes → Operator layer
Q4  Mechanics, victim's own action or     Yes → Play layer
    granted permissions?                  No (a bug) → Operator layer (exploit)
```

**Brief template (one page per case).**

1. Facts (five sentences at most, in your own words).
2. The question (one sentence: "Is X's loss a matter for play, the operator, the law or the contract?").
3. Layer test: your answer to each of Q1 to Q4 with one line of reasoning.
4. Verdict: the layer, and what remedy that layer can offer.
5. The hard point: the question where a reasonable person could answer differently, and what fact would change your answer.
6. Design note: one change to the game or its rules that would have moved this case to a better layer, or prevented it.

**Fact sheets.** Cases A and B are real and summarized from the week 9 lecture and its sources. Cases C to F are invented for this lab and describe no real game.

- **Case A: EBank (EVE Online, 2009).** The chief executive of a player-run bank withdrew 200 billion ISK of depositors' money and sold it to an outside buyer for £3,115 (BBC News, 3 July 2009). Depositors had handed over their ISK voluntarily in the game. EVE's scam policy says scams by legal in-game means are not compensated and generally not punished. EVE's EULA forbids selling currency for real money outside CCP's permitted route. Brief the withdrawal and the cash-out separately.
- **Case B: the Leeuwarden amulet (RuneScape, events of 2007, Dutch Supreme Court 2012).** Two teenagers used threats and violence to force a 13-year-old to log in and transfer a virtual amulet and mask to one of their accounts. The Supreme Court upheld a theft conviction, holding that the items had real value to the victim and that he had exclusive control through his login, which was taken from him.
- **Case C: the borrowed mount (invented).** In *Grayhaven*, rare mounts can be lent to a friend for 24 hours through a lending window. Mira lends her mount to Tomas. The lending window has a bug: if the borrower logs out at the exact moment the loan expires, the mount stays with the borrower permanently. Tomas learns this from a forum post, uses it, and refuses to return the mount. Grayhaven's rules forbid "using any bug to gain an advantage" but do not mention lending.
- **Case D: the guild vault (invented).** In *Ironreach*, guild leaders can grant vault access to officers. Kael, an officer for two years, empties the vault (worth about US$300 on grey-market sites) and joins a rival guild. The guild's leader argues that Kael "stole" the items. Ironreach's rules say nothing about guild vaults. The game shows a vault log naming Kael.
- **Case E: the fake support message (invented).** In *Starfall Drift*, a player sends a whisper styled to look like an official support message, telling the victim that their account will be deleted unless they hand over their best ship "for verification." The victim does so through the normal trade window. Starfall Drift's rules allow in-game scams but forbid impersonating staff.
- **Case F: the land reclaim (invented).** In *Hearthland*, players buy plots with real money through the official store. The operator's marketing page says "own your piece of Hearthland." The operator reclaims Noor's three plots without notice after an automated system flags her for using a bot to win plot auctions. Noor says she never used a bot. Hearthland's terms say plots are licensed and may be removed "for violations of the rules."

**Loss policy template.** A table with columns: Way an item can leave a player's control · Layer · Remedy (none, reversal, compensation, ban, refer to police) · Policy text players read (two sentences at most).

## Steps

1. **Warm-up (15 minutes).** In pairs, brief case A orally. Agree on where the withdrawal and the cash-out land.
2. **Brief four cases (60 minutes).** Individually, write briefs for cases B, C, D and E. Use the interactive `examples/w09-whose-sword.html` to check your path if it is built; otherwise use the flowchart above.
3. **Brief case F (20 minutes).** This is the Bragg pattern with a twist: an automated verdict. Brief it, and in the design note connect it to the week 7 pipeline. What notice, reasons and appeal would Noor need for the reclaim to be defensible?
4. **Peer challenge (15 minutes).** Swap briefs for cases C and D with another student. Each writes one sentence arguing for a different verdict. Respond in writing.
5. **Loss policy (at home).** Write the loss policy for *Grayhaven*, the world of case C. It must cover at least ten ways an item can leave a player's control, including lending, trading, guild vaults, death in PvP, scams in chat, impersonation of staff, account hacking, bugs, bans and server shutdown (week 13). Every row must name a layer. No row may fall between layers.

## Deliverable

- Five case briefs (B to F), one page each, plus the case A notes from step 1.
- Your written response to the peer challenge.
- The Grayhaven loss policy table and a 300-word note explaining your two hardest Q3 choices (where you decided whether a method is allowed play or forbidden).

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Layer test applied correctly | All five cases run through Q1 to Q4 in order, each step justified; verdicts defensible | One case misrouted or a step skipped | Several cases misrouted | 30% |
| Hard points | Each brief names the genuinely contestable question and the fact that would change it | Hard points named but generic | Missing | 15% |
| Case F and due process | Links the reclaim to notice, reasons and appeal from week 7, and to the marketing-versus-contract issue from Bragg | One of the two links made | Neither | 15% |
| Peer challenge | Response engages the counter-argument and either defends or revises the verdict with reasons | Response restates the original | Missing | 10% |
| Loss policy | Ten or more rows, every row has a layer and remedy, no gaps, player-facing text is blunt and clear | Minor gaps or vague text | Fewer than eight rows or many gaps | 20% |
| Writing | Concise, own words, no copied source text | Some padding | Unclear | 10% |

<details>
<summary>Instructor notes</summary>

- A: withdrawal is Play (Q4); cash-out is Operator (Q3, real-money trading).
- B: Law (Q2, threats and violence). Strong answers note that the EULA's ownership clause did not stop the court treating the items as goods.
- C: Q2 no; Q3 yes (a bug used for advantage) so Operator, even though the lending itself was allowed. Hard point: whether Tomas "used a bug" or simply kept what the game gave him. Design note: loans that the server returns automatically, independent of client state.
- D: Play under the rules as written (Q4, granted permissions), as EVE's corp theft policy would treat it. Hard point: whether real-money value pushes it toward law; under the lecture's model it does not, because the means are in-game. Design note: vault withdrawal limits or multi-officer approval (week 2's keys-to-the-vault model).
- E: Operator (Q3, impersonating staff is forbidden). Some students will argue Q2 (deception about the real account); accept either if argued. EVE's scam policy treats imitation of CCP services as forbidden, which supports Operator.
- F: Contract (Q1). Strong answers note the "own your piece" marketing line, the lack of notice, the automated verdict with no human review (DSA Article 20 requires human involvement in complaint handling), and propose a pause on reclaim pending appeal.

</details>
