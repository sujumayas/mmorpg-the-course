# DB201 — Data, Persistence and Telemetry

Year 2, semester 4 · 3 credits · Prerequisites: CS102

Saving the world: relational modeling of characters and items, transactions, caching, and gameplay telemetry.

## Learning outcomes

- Model game entities relationally and query them with SQL
- Use transactions to prevent item duplication
- Instrument a game with telemetry events and build dashboards

## Schedule

| Week | Topic | Lecture | Example |
|---|---|---|---|
| 1 | Why persistence is hard in games | [lecture](lectures/w01-why-persistence-is-hard-in-games.md) | [save-interval-tradeoff](examples/w01-save-interval-tradeoff.html) |
| 2 | Relational modeling: characters, inventories, items | [lecture](lectures/w02-relational-modeling-characters-inventories-items.md) | [blob-vs-rows](examples/w02-blob-vs-rows.html) |
| 3 | SQL I: select, join, aggregate | [lecture](lectures/w03-sql-i-select-join-aggregate.md) | [join-fan-out](examples/w03-join-fan-out.html) |
| 4 | SQL II: indexes and query plans | [lecture](lectures/w04-sql-ii-indexes-and-query-plans.md) | [index-vs-scan](examples/w04-index-vs-scan.html) |
| 5 | Transactions and ACID | [lecture](lectures/w05-transactions-and-acid.md) | [split-save](examples/w05-split-save.html) |
| 6 | Race conditions and the duplication bug | [lecture](lectures/w06-race-conditions-and-the-duplication-bug.md) | [trade-dupe-stepper](examples/w06-trade-dupe-stepper.html) |
| 7 | NoSQL and key-value stores (Redis) | [lecture](lectures/w07-nosql-and-key-value-stores-redis.md) | [rank-query-cost](examples/w07-rank-query-cost.html) |
| 8 | Caching and write-behind | [lecture](lectures/w08-caching-and-write-behind.md) | [write-behind-tradeoff](examples/w08-write-behind-tradeoff.html) |
| 9 | Schema migrations in a live game | [lecture](lectures/w09-schema-migrations-in-a-live-game.md) | [backfill-batches](examples/w09-backfill-batches.html) |
| 10 | Telemetry design: events and properties | [lecture](lectures/w10-telemetry-design-events-and-properties.md) | [event-schema-designer](examples/w10-event-schema-designer.html) |
| 11 | Pipelines: collect, store, query | [lecture](lectures/w11-pipelines-collect-store-query.md) | [query-cost-ladder](examples/w11-query-cost-ladder.html) |
| 12 | Dashboards and KPIs | [lecture](lectures/w12-dashboards-and-kpis.md) | [dau-definitions](examples/w12-dau-definitions.html) |
| 13 | Privacy, GDPR and data retention | [lecture](lectures/w13-privacy-gdpr-and-data-retention.md) | [retention-and-erasure](examples/w13-retention-and-erasure.html) |
| 14 | Backups and disaster recovery | [lecture](lectures/w14-backups-and-disaster-recovery.md) | [rpo-rto-timeline](examples/w14-rpo-rto-timeline.html) |
| 15 | Final: persistent inventory service with telemetry | [assessments](#assessment-materials) | — |

## Signature worked examples

- The trade dupe: two concurrent trades without a transaction — step-through animation

## Labs

- [DB201 · Lab 01: Save intervals and a crash-proof save](labs/lab01.md)
- [DB201 · Lab 02: An inventory schema that enforces the rules](labs/lab02.md)
- [DB201 · Lab 03: Eight questions about a generated world](labs/lab03.md)
- [DB201 · Lab 04: Scans, indexes and query plans](labs/lab04.md)
- [DB201 · Lab 05: Split saves, real crashes and commit cost](labs/lab05.md)
- [DB201 · Lab 06: Reproduce the dupe, then make it impossible](labs/lab06.md)
- [DB201 · Lab 07: Ranks at scale](labs/lab07.md)
- [DB201 · Lab 08: The write-behind flusher](labs/lab08.md)
- [DB201 · Lab 09: A migration under load](labs/lab09.md)
- [DB201 · Lab 10: Tracking plan and event validator](labs/lab10.md)
- [DB201 · Lab 11: A telemetry pipeline in SQLite](labs/lab11.md)
- [DB201 · Lab 12: KPIs in SQL](labs/lab12.md)
- [DB201 · Lab 13: Retention and erasure](labs/lab13.md)
- [DB201 · Lab 14: Disaster-recovery drill](labs/lab14.md)

## Assessment materials

- [DB201 · Exam bank: quiz, practice and viva questions](assessments/exam-bank.md)
- [DB201 · Final service brief: a persistent inventory service with telemetry](assessments/final-service-brief.md)
- [DB201 · SQL labs brief](assessments/sql-labs-brief.md)

## Readings

- Kleppmann — Designing Data-Intensive Applications, ch. 2, 7

## Assessment

SQL labs (40%), final service (60%)
