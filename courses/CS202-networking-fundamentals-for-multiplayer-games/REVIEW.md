# CS202 review: open items

The reviewer fixed everything else in place. These items need a source or a decision.

## Facts not verified either way

| File | Claim | What is missing | Proposed fix |
|---|---|---|---|
| lectures/w06-reliability-over-udp.md | Tribes networking paper dated 2000 (Frohnmayer & Gift) | The PDF carries no date or venue | Find the GDC 2000 proceedings listing, or cite it as "c. 2000" |
| lectures/w06-reliability-over-udp.md | Tribes 2 sent each move three times | The paper describes the design while Tribes 2 was in development; the shipped game was not checked | Keep the new "as the 2000 paper describes it" wording, or find a post-release source |
| lectures/w07-snapshots-and-delta-compression.md | Quake III `msg.c` per-field change bits and Huffman coding; `sv_fps` default 20 | `msg.c` and `sv_init.c` were not fetched | Check id-Software/Quake-III-Arena `code/qcommon/msg.c` and `code/server/sv_init.c` |
| lectures/w11-lag-compensation-rewind-hit-detection.md | Riot's "about 101 ms" peeker's advantage | Probably in an image in the Riot article, not the text. It matches the 141 ms baseline minus 40 ms | Keep, or cite the lecture's own 100.6 ms computation only |
| lectures/w13-tick-rate-and-bandwidth-budgets.md | Apex Legends has 60 players per match | Only the fan wiki was checked | Cite an EA/Respawn page |
| lectures/w13-tick-rate-and-bandwidth-budgets.md | EVE Time Dilation dev blog of 22 April 2011 | Only the EVE University wiki was checked. The feature may have gone live around January 2012 | Fetch the CCP dev blog |
| lectures/w14-testing-under-bad-networks-netem-clumsy.md | clumsy 0.3 buffer caps (2,000 packets, flush 800) | Checked on master, not on the 0.3 tag | Check the 0.3 tag source |
| lectures/w14-testing-under-bad-networks-netem-clumsy.md | Gilbert (1960) and Elliott (1963) citations | Not fetched | Check the Bell System Technical Journal records |
| lectures/w01-networks-for-game-devs-tcp-vs-udp.md | WoW game traffic runs over TCP | Inferred from the 2.3.2 Nagle patch note and TrinityCore, not stated by Blizzard | Wording already says so. Leave it unless a Blizzard source turns up |

## Known simplifications (no change needed)

- w01 head-of-line model: with two consecutive losses, the Lab 01 model resends packet `k` after packet `k + 3` arrives, while real TCP would need three duplicate ACKs from `k + 2` to `k + 4`. The lecture labels this a teaching model, and check-yourself question 2 says "the Lab 01 model".
- w03 and w12 packet and unit sizes are labelled as illustrative assumptions.

## Fact sweep (29 September 2026)

Verified (7):
- Quake III `msg.c` per-field change bits up to the last changed field, Huffman coding, `PACKET_BACKUP` 32, `sv_fps` default 20 (`sv_init.c`) and `snaps` default 20 (`cl_main.c`). Checked on the id-Software repository. w07 Sources now name the files.
- Riot's figures, from the 28 July 2020 article: ~141 ms baseline, ~40 ms (28%) saved, ~71 ms at 144 FPS (49%). The article never prints "101". w11 now says 101 ms is the subtraction.
- Apex Legends 60 players: EA's "About Apex Legends" page ("classic 60-person Battle Royale matches"). It replaces the fan wiki in w13.
- EVE TiDi dev blog: CCP Veritas, 22 April 2011, read directly. The 10% floor comes from the EVE University wiki, and w13 says so.
- clumsy 0.3 (released 21 October 2023): `KEEP_AT_MOST 2000` and `FLUSH_WHEN_FULL 800` in `src/lag.c`; drop default 10.0 with inbound and outbound on.
- Gilbert (1960, BSTJ 39(5):1253-1265) and Elliott (1963, BSTJ 42(5):1977-1997): checked on Crossref. DOIs and pages added in w02 and w14.

Hedged (2):
- Tribes networking paper: the PDF has no date or venue. The abstract says the model "is being developed for TRIBES II". w04, w06 and w07 now cite it as undated and drop "2000" and "GDC 2000".
- Tribes 2's move sent three times: w06 now says the paper describes the planned design, not the shipped game.

Unchanged: WoW over TCP was already worded as an inference. Removed: 0.
