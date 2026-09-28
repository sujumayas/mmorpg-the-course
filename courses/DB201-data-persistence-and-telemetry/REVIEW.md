# DB201 review: open items

Items the course reviewer could not fix inside DB201 (September 2026 review).

## Other courses

| File | Problem | Proposed fix |
|---|---|---|
| `courses/MMO302-mmo-server-architecture/lectures/w08-item-ownership-and-transactional-integrity.md`, line 13 | Links DB201 weeks 5 and 6 through `../../DB201-data-persistence-and-telemetry/syllabus.md`, although both lectures now exist. | Link `../../DB201-data-persistence-and-telemetry/lectures/w05-transactions-and-acid.md` and `.../w06-race-conditions-and-the-duplication-bug.md` directly. |
| `courses/DB201-data-persistence-and-telemetry/lectures/w12-dashboards-and-kpis.md`, header | Links MMO308 weeks 2 to 6 through `syllabus.md`, because MMO308 has no lectures yet. | Upgrade the link when MMO308 week 2 exists. |

## Facts not re-checked against a primary source in this review

| File | Fact | Status |
|---|---|---|
| w04, Sources | Kleppmann ch. 3: four-level B-tree, 4 KB pages, branching factor 500, up to 256 TB | Matches the reviewer's knowledge of the book; not re-read against a copy. |
| w05, w06 | Kleppmann ch. 7 paraphrases (lost updates, bank-transfer examples) | Paraphrases only; not re-read against a copy. |
| w06 | New World dupe mechanism | Unpublished by Amazon; the lecture says so and does not guess. |
| w07, w08 | Fortnite postmortem (8 Feb 2018) figures: 9 MongoDB shards, 124k requests/s, 318k reads/s, 132k writes/s, Memcached outage 18:30 to 20:20 UTC | Cited from the Internet Archive copy by the author; not re-fetched in this review. |
| w10 | World of Warcraft 12.0.0 restricting addon registration for the combat log event; GameAnalytics limits (15,000 / 8,000 / 4,000) and the 1 October 2025 change | Cited by the author; not re-fetched in this review. |
| w12 | Roblox 10-K for 2025: 127 million average DAU and the edge cases of the 24-hour midnight rule | The lecture already says the filing leaves edge cases open; the 127 million figure was not re-fetched. |
| w13 | Riot privacy notice (28 April 2026) and Blizzard privacy policy (27 June 2025) retention periods | Cited by the author; not re-fetched in this review. |
| w14 | 3-2-1 backup rule | Given as an unattributed rule of thumb, which is accurate; no attribution needed. |
