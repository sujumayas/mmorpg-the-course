# PR201 review: open items

Review of September 2026. Everything else found in the review was fixed in place. The sample team is now *Hollowmarch*, six people (two programmers, designer, artist, audio, producer), building a three-player slice, in all 14 weeks, labs, starters, examples and briefs.

## 1. Week 3 scope baseline does not match the week 2 scope sheet (done)

- **Resolution (September 2026):** week 9's burn-up now starts from week 2's 311 estimate-hours minus every cut made since, restated to week 3 so the scope line shows growth only. Week 9 has a dated table: week 5 term check (F1 and F4's second phase leave, 33; F6 talent choice becomes fixed stat gains, 35 to 10, 25), week 6 (C8 lag compensation, 16), week 8 (content plan A to B, 15; thin bolt, 5), giving 217. Week 5 gained the term check (`check_scope.py --plannable 255`, PASS) and lab 05 a step for it. Growth is now 15 per sprint; scenario cuts are 44, 52, 82 and 92. The week 9 cut list no longer re-cuts F1 and F4 and totals 52, with a 10-hour next cut. Lab 09 starter data, instructor notes, the interactive spec and `examples/w09-burnup-forecast.html` are updated; `check_examples.py` passes and the page shows the spec's test values.

## 2. Weeks 8 and 12 plan in actual hours (done)

- **Resolution (September 2026):** both weeks now plan in estimate-hours against `f × U`. Week 8 explains the ratio route against the focus route (63 against 46 estimate-hours for sprint 3), corrects content only by `k = r_content / r_team = 1.04`, and budgets 46 − 5 − 15 = 26 for content (plan A 40.6 fails, plan B 25.0 holds). Week 12 converts logged fix hours once, by dividing by the estimate ratio, and puts polish items on at their raw estimates. The defaults are U 75, f 0.532, O 5, B 7, N 4, r 0.2, h 2.4, q 1.3, giving a 9.5-hour budget. Labs 08 and 12, their checkers and starter data, the week 12 script, spec and `examples/w12-polish-budget.html`, and exam questions 10 and 11 are updated and rerun.

## 3. M2 persistence and tracking sections come before DB201 teaches them (done)

- **Resolution (September 2026):** M2 section 11 is now a documented save format with a version field and a file-based save with an atomic write and a crash test, linking CS201 week 12 and DB201 week 1. Section 12 is six named server events with their questions. The rubric rows mark only that. The schema, transactions, grant ids and event properties moved to M3 (deliverable 8 and the persistence and A6 rows), and the week 3 table, lab 03 and the TDD template say the same.

## 4. Peer scheme attribution

- **File:** `assessments/peer-assessment-brief.md`.
- **Problem:** the per-rater normalisation resembles the WebPA algorithm (Loughborough University). This was not verified, so the brief presents the scheme as the course's own, which is acceptable.
- **Proposed fix:** if WebPA's documentation confirms the same normalisation, add one source line crediting it.
