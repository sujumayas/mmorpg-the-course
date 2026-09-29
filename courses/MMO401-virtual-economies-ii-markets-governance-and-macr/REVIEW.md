# MMO401 review notes (course-reviewer, 2026-09-28)

These are the open items the reviewer did not fix directly. The small fixes are already applied in the files.

| File | Problem | Proposed fix |
|---|---|---|
| lectures/w12 (EverQuest II 2005 dupe) | The primary source (Terdiman, ZDNet/CNET, 11 August 2005) could not be fetched in September 2026. The 20% rise, the tracking and removal, the Station Exchange attempt, the US$70,000 or more from online auctions, and SOE stopping Station Exchange auctions all rest on the Wikipedia summary. The lecture says so in Sources. | Verify against the CNET article or an archive copy and drop the caveat. |
| lectures/w01, w04-w14 (reading lists) | The table of contents of Lehdonvirta & Castronova (2014) could not be reached (MIT Press and library catalogues returned 403). The lectures cite only "the course's assigned chapters 9-12" by topic. Chapter-number-to-topic mappings in w10, w11 and w12 were removed. | Confirm the chapter titles of ch. 9-12 from a copy of the book and name them in the syllabus reading list. |
| lectures/w13 (CCP report definitions) | The October 2024 report pages give no definition or formula for money supply or velocity, and none for how the price indices are chained. The lecture now says so. | If CCP publishes a methodology note, cite it and state the velocity period. |
| lectures/w04 (Mod Ash figure) | w04 says "about 5.73 trillion coins", while w13, w14 and the wiki say about 5.7 trillion. Both round the same Jagex figure. | Harmless. Pick one rounding across the course when next edited. |
| examples/*.html | The automated check passes all 14 at 390 px and 1,280 px in light and dark mode. Readouts were compared with the lecture by reading the JS for w08, w10 and w13 only. | Spot-check the default readouts of the other 11 interactives against each spec's test values in a browser. |
| syllabus.md | Still the generated stub with `_todo_` cells. Not edited by the reviewer. | The orchestrator fills it. |

## Fact sweep (2026-09-29)

- Verified: EverQuest II 2005 dupe (w12). Terdiman's CNET article (11 August 2005) is live on cnet.com. It confirms that money rose "by a fifth in about 24 hours", that SOE tracked and removed the duped platinum, and that it shut the auctions. The US$70,000 figure appears there only as an allegation from other sites, so the text now says so. The chapter titles for Lehdonvirta & Castronova ch. 9-12 were confirmed via Crossref chapter DOIs and are now named in the w01, w07, w08 and w09 sources.
- Hedged: the PLEX month (w11) is now "2008, Wikipedia gives November". Guðmundsson's 2014 departure (w01, w13) is now attributed to Wikipedia citing Morgunblaðið, which blocked automated reads. His 2007 start is cited to CCP's 3 September 2007 dev blog.
- Unchanged: the CCP report definitions are already stated as unpublished. The Mod Ash rounding item no longer applies, because no 5.73 trillion figure remains.
- The only "(verify" text is in syllabus.md line 35 (PLEX mechanics), which this pass may not edit.
- Counts: verified 2, hedged 2, removed 0.
