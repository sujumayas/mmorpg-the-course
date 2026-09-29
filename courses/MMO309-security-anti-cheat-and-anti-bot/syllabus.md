# MMO309 — Security, Anti-Cheat and Anti-Bot

Year 3, semester 6 · 3 credits · Prerequisites: MMO302

Defending a persistent world: exploits, duplication, cheats, bots and account security.

## Learning outcomes

- Threat-model an MMO
- Prevent classes of exploits by server design
- Detect bots with behavioral analytics

## Schedule

| Week | Topic | Lecture | Example |
|---|---|---|---|
| 1 | Threat modeling for games | [lecture](lectures/w01-threat-modeling-for-games.md) | [threat-ledger](examples/w01-threat-ledger.html) |
| 2 | Never trust the client | [lecture](lectures/w02-never-trust-the-client.md) | [fog-of-war-leak](examples/w02-fog-of-war-leak.html) |
| 3 | Speed hacks and movement validation | [lecture](lectures/w03-speed-hacks-and-movement-validation.md) | [lag-tolerant-movement-check](examples/w03-lag-tolerant-movement-check.html) |
| 4 | Duplication exploits and transactional design | [lecture](lectures/w04-duplication-exploits-and-transactional-design.md) | [failure-points](examples/w04-failure-points.html) |
| 5 | Memory editing and client integrity | [lecture](lectures/w05-memory-editing-and-client-integrity.md) | [ban-wave-timing](examples/w05-ban-wave-timing.html) |
| 6 | Botting economics | [lecture](lectures/w06-botting-economics.md) | [bot-farm-pnl](examples/w06-bot-farm-pnl.html) |
| 7 | Bot detection: behavioral features | [lecture](lectures/w07-bot-detection-behavioral-features.md) | [click-timing](examples/w07-click-timing.html) |
| 8 | Machine learning for detection (overview) | [lecture](lectures/w08-machine-learning-for-detection-overview.md) | [base-rate-threshold](examples/w08-base-rate-threshold.html) |
| 9 | Account security and takeovers | [lecture](lectures/w09-account-security-and-takeovers.md) | [trade-hold](examples/w09-trade-hold.html) |
| 10 | Gold sellers and RMT networks | [lecture](lectures/w10-gold-sellers-and-rmt-networks.md) | [follow-the-gold](examples/w10-follow-the-gold.html) |
| 11 | Exploit response: rollback vs ban | [lecture](lectures/w11-exploit-response-rollback-vs-ban.md) | [rollback-trace-ban](examples/w11-rollback-trace-ban.html) |
| 12 | Legal and ethical considerations | [lecture](lectures/w12-legal-and-ethical-considerations.md) | [how-sure-to-ban](examples/w12-how-sure-to-ban.html) |
| 13 | Bug bounty and disclosure | [lecture](lectures/w13-bug-bounty-and-disclosure.md) | [bounty-vs-black-market](examples/w13-bounty-vs-black-market.html) |
| 14 | Case studies | [lecture](lectures/w14-case-studies.md) | [response-scorecard](examples/w14-response-scorecard.html) |
| 15 | Final: threat model + detection prototype | [assessments](#assessment-materials) | — |

## Signature worked examples

- Speed-hack validation: server-side max-distance-per-tick check with lag tolerance (interactive)
- Bot vs human click timing distributions

## Labs

- [MMO309 · Lab 01: The threat ledger](labs/lab01.md)
- [MMO309 · Lab 03: The lag-tolerant movement validator](labs/lab03.md)
- [MMO309 · Lab 04: The mailbox under fire](labs/lab04.md)
- [MMO309 · Lab 06: The bot farm ledger](labs/lab06.md)
- [MMO309 · Lab 07: Behavioral features for bot detection](labs/lab07.md)
- [MMO309 · Lab 08: From detector scores to decisions](labs/lab08.md)
- [MMO309 · Lab 10: Follow the gold](labs/lab10.md)
- [MMO309 · Lab 11: Dupe response, rollback, trace or ban](labs/lab11.md)
- [MMO309 · Lab 12: A sanction policy with an error budget](labs/lab12.md)
- [MMO309 · Lab 13: Pricing a bounty table](labs/lab13.md)
- [MMO309 · Lab 14: Response scorecard](labs/lab14.md)

## Assessment materials

- [MMO309 · Exam bank: quiz, practice and viva questions](assessments/exam-bank.md)
- [MMO309 · Final prototype brief: a detection prototype for one threat](assessments/final-prototype-brief.md)
- [MMO309 · Labs brief](assessments/labs-brief.md)
- [MMO309 · Threat model brief: a costed threat model for one MMO](assessments/threat-model-brief.md)

## Readings

- Hoglund & McGraw — Exploiting Online Games (2007)

## Assessment

Threat model (30%), labs (30%), final prototype (40%)
