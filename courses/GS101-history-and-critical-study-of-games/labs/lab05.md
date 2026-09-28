# GS101 · Lab 05: Close reading a parser game

**Week:** 5 · **Time:** 2 hours in the lab plus up to 3 hours at home · **Weight:** practice for close reading 1 (formative, feedback only)

**Lecture:** [Week 05, text adventures and MUD1](../lectures/w05-text-adventures-and-mud1.md)

## Objective

Play Colossal Cave Adventure with a full transcript, choose one short passage and write a close reading that links a rule (including the parser's limits) to what you did and felt, and then to the game's historical context. Then do a short contrast session in MUD1 to see what a shared world changes. This is a rehearsal for your first graded close reading.

## Starter materials

- **Open Adventure.** The open-source port of Crowther and Woods's Adventure 2.5, BSD-licensed, maintained at gitlab.com/esr/open-adventure. Build it from source or use a package from your system's package manager if one exists. Lab machines have it installed. If you cannot install it, several browser ports of the 350-point version exist. Note which version you used, since the point totals differ.
- **Transcript logging.** Run it in a terminal with logging on. On macOS or Linux, `script GS101-lab05-log.txt` before starting the game records everything. In a browser port, copy the text out every 15 minutes.
- **MUD1 (British Legends).** Playable at british-legends.com with a Telnet client or the site's web client. Create a throwaway character. Expect other players and expect to die.
- **Command-failure log.** A table you fill in as you play:

| Time | What I typed | What the game replied | What I meant | Synonym that finally worked |
|---|---|---|---|---|

- **The five-step close-reading method** from section 4 of the lecture: record, pick a moment, describe the rule, describe the effect, connect.

## Steps

1. **Play Adventure (45 min).** Start the log. Play without a walkthrough. Every time the game fails to understand you, add a row to the command-failure log.
2. **Count.** At the end, count your commands and your failed commands. Compute the failure rate. Group the failures into types (unknown verb, unknown noun, too many words, correct words but wrong situation).
3. **Pick a passage.** Choose one moment of no more than one page of transcript: a puzzle, a room, a death, a surprise. Copy it into your write-up exactly as the game printed it.
4. **Rule and effect.** Write down the rules that produced that passage, including the parser's. Then write down what you did in response, as behavior ("I typed six synonyms," "I drew a map," "I stopped trusting descriptions").
5. **Play MUD1 (20 min).** Explore near the start. Note every moment another player changed what you could do (took an item first, attacked you, helped you, talked). Estimate how many players were online.
6. **Connect.** Using the lecture's shared-treasure model, say in two or three sentences whether the MUD1 world you saw was above or below its crossover population, and what evidence you have.
7. **Write.** Produce a 600-word close reading of your Adventure passage using the five steps, plus a 150-word contrast paragraph on MUD1.

## Deliverable

A single PDF with the passage, the command-failure table with your counts and failure rate, the 600-word close reading, the 150-word MUD1 contrast and the raw transcript as an appendix. Name the file `GS101-lab05-<surname>.pdf`.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Evidence | Full transcript, failure table with counts, rate and types | Transcript or table incomplete | No transcript | 20% |
| Rule to effect | Names specific rules including the parser, and connects each to observed behavior | Rules named but link to behavior is vague | Summary of the plot instead of analysis | 30% |
| Historical context | Links the rule to a real constraint (vocabulary size, memory, network) with a cited fact | Context mentioned but not tied to the passage | No context | 20% |
| MUD1 contrast | Uses the crossover idea with concrete evidence from play | Describes the session without the model | Missing | 15% |
| Writing | Clear claim in the first paragraph, quotes from the transcript used as evidence, within word limits | Claim present but buried; minor overrun | No claim | 15% |
