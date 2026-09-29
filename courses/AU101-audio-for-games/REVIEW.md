# AU101 review: open items

Reviewer pass, September 2026. Everything below could not be fixed or verified in place. Items fixed during the review are not listed.

| # | File | Problem | Proposed fix |
|---|---|---|---|
| 1 | lectures/w01-what-sound-does-feedback-space-emotion.md, section 2 | Collins's interactive, adaptive and dynamic audio distinction was written from memory. The book text could not be searched (WebSearch budget spent, archive.org full-text and Google Books blocked). The chapter titles were confirmed through Open Library. The paragraph now says it is a paraphrase and tells students to check it against the introduction. | Check the definitions against a copy of *Game Sound* (2008), introduction, and add a page number to the Sources line. |
| 2 | lectures/w10-mixing-ducking-and-priority.md, section 4 and Sources | Audiokinetic's Wwise Help returns 403. "Understanding HDR" was confirmed through an Internet Archive snapshot of the 2021.1.4 help, and the version claim was narrowed to match. "Defining playback priority" (priority 1 to 100, the linear distance offset, discard oldest or newest) and "Using side-chaining" have no archived copy. | Open the Wwise 2024.1 or 2025.1 help in a browser and confirm the three pages, or cite an archived copy. |
| 3 | lectures/w04, w06, w08, w09 (FMOD Studio 2.03 manual) | fmod.com renders its manual with JavaScript, so a plain fetch returns no text. These claims were not re-fetched: the Shuffle rule (three or more items, no play percentages), the random modulator's downward range on dB properties, the seek modulator's range-per-second units, and the 120 BPM 4/4 default tempo. They match the FMOD manual as the reviewer knows it. | Spot-check the four claims in a browser against FMOD Studio 2.03.14. |
| 4 | lectures/w12-audio-for-mmos-many-players-one-mix.md, cross-game | The Final Fantasy XIV Lodestone guide on Battle Effects (own, party, others) was not re-fetched. | Confirm on the Lodestone page and add its URL. |
| 5 | lectures/w08-adaptive-music-vertical-layering.md, cross-game | 130 BPM and A minor come from Wikipedia ("Music of Red Dead Redemption"), which cites Rockstar's making-of video. The Rockstar Newswire piece (28 July 2010) was not re-fetched. | Confirm against the archived Newswire post or the video. |
| 6 | lectures/w08, w09 | Super Mario Maker 2 claims (Yoshi bongos in the SMW style, the timer jingle pausing the music) could not be verified on the Super Mario Wiki and were removed. Super Mario World and Super Mario Bros. claims remain and are verified. | None needed unless someone wants the Maker 2 example back. It would then need a source. |
| 7 | courses/UX201-game-ux-and-player-psychology/lectures/w11-accessibility-guidelines.md | Dedup check: AU101 week 13 (subtitle reading rate, hold and clash, directional cues) and UX201 week 11 (contrast, text size, XAG checklist) overlap only on the XAG 104 line limits. AU101 week 13 now links forward to UX201 week 11. UX201 week 11 does not link back. AR101 week 12 (colour) and MMO306 week 14 (group cue coverage) do not overlap. | Add a back-link in UX201 week 11 section 6 to AU101 week 13 for reading-rate timing. That file belongs to another course, so the reviewer did not edit it. |
| 8 | lectures/w02-recording-and-foley-basics.md, Sources | The Riot Games blog post content (128 ticks, 7.8125 ms) is confirmed. Its date, 31 August 2020, was not. | Confirm the date on technology.riotgames.com. |

## Fact sweep (29 September 2026)

- Verified: FMOD Studio 2.03.14 manual (fetched from the manual's content host), all four claims. Shuffle needs at least three items and no play percentages (20.3.8). The random modulator on dB runs from the value down (22.2). Seek speed is a fraction of range per second, 0.1 range/s on −24 to 24 st is 4.8 st/s (22). Events with no tempo markers default to 120 BPM and 4/4 (28, Glossary). Sources in w04, w06, w09 now give section numbers.
- Verified: Wwise Help 2024.1.5 "Defining playback priority" and "Using side-chaining" through Internet Archive snapshots of 14 June 2025 (w10 Sources updated).
- Verified: FFXIV Lodestone UI guide page, with URL and menu path (w12). It now also lists an "Enemy PC" option, which the lecture mentions.
- Verified: Rockstar Newswire post, 28 July 2010, "stem after emotive stem" (archived 24 September 2015).
- Verified: Riot tech blog date, 31 August 2020.
- Hedged: RDR 130 BPM and A minor. The Newswire text does not state it, so w08 says it comes from Wikipedia and has not been confirmed in the video.
- Hedged: Collins's interactive, adaptive and dynamic distinction. The book text was still unreachable (archive.org search-inside 403, Google Books 429). w01 now says the paraphrase was not checked against the book's wording.
- Removed: none.
