# MMO407 review notes

Open items from the course review of 28 September 2026. Everything else found in the review was fixed in place.

| File | Problem | Proposed fix |
|---|---|---|
| lectures/w10-recovery-strategies.md, section 3 | Links to the MMO403 syllabus, because MMO403 has no lectures yet. | When MMO403 week lectures exist, link the business-model week directly. |
| lectures/w12-writing-a-post-mortem.md, section 1 and Sources | The counts "technical (116) and game design (112)" come from the body of Politowski et al., arXiv:2009.02440. The abstract confirms 200 post-mortems, 927 problems, 20 types and the people-not-technology conclusion, but the two counts were not rechecked against the full text. | Check the counts in the paper's results table. If they differ, update the sentence and the source line. |
| lectures/w08-eve-large-scale-events.md, Sources | The FWST-8 battle report is cited as "2020". The page's metadata gives 13 December 2020 as its publish date, which may be a republish of an October 2020 post. | Confirm the original post date on archive.org and give the full date in the source line. |
| lectures/w05-case-star-wars-galaxies-and-the-nge.md, section 1 | The Combat Upgrade's exact live date is not in the cited source. The lecture now says "spring 2005" (after publish 14.1 of April 2005, with press criticism archived from May 2005). | If a dated SOE patch note or archived news post is found, give the exact date. |

## Fact sweep (29 September 2026)

- Verified (2): Politowski et al. counts. Figure 3b of arXiv:2009.02440v3 (22 January 2021) gives technical 116 (11%) and game design 112 (11%), matching PR101 w14 and its `politowski_types.csv` (200 post-mortems, 927 problems). The Edholm figures (78 post-mortems, 45% crunch) are also in section 5.6. Combat Upgrade date: SOE's respec notice headed "Combat Upgrade April 27th, 2005" is reproduced on the SWG Fandom wiki with update notes from 29 April 2005. w05 now says 27 April 2005 (timeline) and April 2005 (model section), and a source line was added.
- Hedged (1): FWST-8 battle report. The page is dated 13 December 2020. An earlier first-posting date could not be checked because the Internet Archive was offline. The w08 source line says so.
- Removed: none.
- Note: `syllabus.md` week 6 still shows "(New World 2021, verify)" from the old generated stub. The tag comes from `curriculum.yaml` line 1371. The w06 New World facts were checked in review (PC Gamer, 17 November 2021), so the orchestrator can drop the tag and rerun `tools/build_plan.py`. Neither file was edited, per instructions.
