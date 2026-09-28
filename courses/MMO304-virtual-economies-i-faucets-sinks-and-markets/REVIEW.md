# MMO304 review: open items

Reviewed September 2026. The review fixed the small issues directly. Only the items below are still open.

| File | Problem | Proposed fix |
|---|---|---|
| lectures/w02-functional-hedonic-and-social-value.md (Sources) | I could not read the abstract of Lehdonvirta (2009). Springer needs a login and the search budget was spent. Crossref confirms the title, journal and pages, *Electronic Commerce Research* 9(1-2), 97-113. I did not verify whether the paper itself groups attributes as functional, hedonic and social. The source line now claims only the `V = F + H + S` sum and the `log2` form as the course's own. | Check the paper through a library login. If it uses the three-way split, credit it in section 1 ("Lehdonvirta groups purchase drivers into functional, hedonic and social attributes"). |
| lectures/w09-commodity-money-when-an-item-becomes-currency.md, section 3 | The claim that selling Stones of Jordan to vendors triggers the Diablo clone rests on community sources. The Arreat Summit clone page returns 404 and archive.org is blocked from this tool. The lecture already calls it a community claim. | Keep the hedge. If a Blizzard source turns up (the archived Arreat Summit or D2R patch notes), cite it and drop the hedge. |
| lectures/w09 (Sources), exam-bank Q40 | Diablo II realm death penalty (character level in %, capped at 20%, carried and stashed gold) and the 35,000-gold vendor cap. The Arreat Summit pages were unreachable (404, archive blocked), so these were not re-verified. The Stone of Jordan stats and level 29 were confirmed on Fextralife. | Verify both on an archived Arreat Summit copy before the course runs. |
| examples/*.html | Every example passes `check_examples.py`. I compared numbers against the lectures only for w03, w04 and w13. The other examples implement their specs, but I did not check their test values one by one. | Before the course runs, a builder should step through each spec's "Test values" list in the browser. |
| lectures/w13 (Sources), w11 | PLEX "introduced November 2008" and "Eyjólfur Guðmundsson 2007-2014" are cited to Wikipedia only. | Replace with a CCP dev blog or an EVE University page if one is available. |

No change is needed in MMO401. It already uses 7.5% × (1 − 0.11 × 5) = 3.375% for EVE sales tax at Accounting V, which MMO304 now matches (checked on the EVE University wiki: 7.5% base since 22.02, 11% per level, 3.37% at max).
