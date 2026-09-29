w01-03: ESI is_singleton described only by name; EVE SQL Server claim dropped.
w04-06: New World dupe mechanism unpublished (said); Kleppmann ch7 paraphrases and '256 TB B-tree' (ch3) not re-checked against the book. w02 says w04 'measures' recursive queries but w04 doesn't cover them; fix.
w13-14: all verified. 3-2-1 rule unattributed. w12 syllabus link from w13.
w07-09: unverified/avoided: PostgreSQL lock queueing behind waiting ALTER; GW2 no-downtime builds. r=20,000 rows/s is a stated assumption. Links CS102 w4,5,13 to check.
w10-12: unverified: Roblox 24h visit rule edge cases; Supercell AWS case study undated (c. 2015). Syllabus links: CS202 w4, MMO308 w2-6, MMO309.
w09 check-yourself '0.024 s each' is batch running time b/r+o; stall b/r is 0.02 s: clarify wording. w11 table L1 3.3 cores vs spec 3.33; L3 'effectively 0' vs 0.05 us: align.
w02: section 2 says blob bar shorter for 'load one character' but spec bytes make blob longer (10,500 vs 9,000 B); builder added worst-case page-read bar where blob wins (1.23 MB, 150 pages). Fix lecture wording.
w01: table 166.7 vs spec 166.67 (page shows 2 dp). w04: spec slider can't reach 600,000,000; builder added exact-N box. w03: lecture mentions a 'join' button that doesn't exist; reword.
w14 example: failure exactly on archive tick counts as losing full interval (default marker shows 60 s lost). Check lecture wording agrees.
w06 SIGNATURE: 'Naive R T G: 18 of 20' is wrong; correct is 12 of 20 (brute force: only orders starting 12 or 21 dupe). Appears in section 2 and Common misconceptions; also check lab06, exam bank. w08 Minecraft preset N=1 below spec slider min 100; slider extended to 1, fix spec.
