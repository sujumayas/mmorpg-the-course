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
