# MMO307 review notes

Review of September 2026. Everything the reviewer could fix is fixed in place. These items need someone with access to files the reviewer was told not to edit, or they are facts that rest on a wiki alone.

## For the orchestrator

| File | Problem | Proposed fix |
|---|---|---|
| `curriculum.yaml` (MMO307 week 2/5 topic) | Resolved: the WoW-figures tag is no longer in `curriculum.yaml` (checked 29 September 2026). | None. Every WoW item-level range, squish mapping (8.0.1: 1000 to 265; 9.0.1: 485 to 140; 12.0.0: 730 to 170), the Midnight ranges (TWW 623-730 to 86-170, DF 376-528 to 79-85) and the bonus-damage table (500, 250, 100, 10, 1) match Warcraft Wiki "Stat squish" and the patch pages for 6.0.2, 8.0.1, 9.0.1 and 12.0.0, fetched September 2026. |
| `syllabus.md` | Still has the generated-stub marker. | Run `tools/build_plan.py`, then hand-finish the syllabus. |

## Facts that rest on one wiki

| Lecture | Fact | Status |
|---|---|---|
| w07 | Arena Dampening starts at once in 2v2 and after 5 minutes in 3v3, one 1% stack every 10 seconds. | Warcraft Wiki "Dampening" lists the 14 December 2020 hotfix as the latest change. No Blizzard source for the Midnight-era value. The lecture cites it as the wiki's rule from that hotfix. |
| w08 | Early League of Legends built a team Elo from members' ratings. | League of Legends Wiki says so and says Riot never published the formulas. The lecture already treats it as structure, not a formula. |

## Fact sweep (29 September 2026)

- Verified: arena Dampening. Warcraft Wiki "Dampening" quotes Blizzard's 14 December 2020 hotfix note ("applied immediately in 2v2 and after 5 minutes in 3v3"), and that is still the latest listed change. The w07 source line now quotes the note and gives the URL. The lecture's 30% at ten minutes and the exam answer (18% at eight minutes) match the rule.
- Hedged: none new. Early League of Legends team Elo is already stated as the wiki's description, with formulas unpublished.
- Removed: none.
