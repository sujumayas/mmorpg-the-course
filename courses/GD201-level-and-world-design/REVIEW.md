# GD201 review: open items

Items the reviewer could not close. Everything else found in review was fixed in place.

## Unverified facts

| File | Problem | Proposed fix |
|---|---|---|
| lectures/w04, w05, w07, w08, w09 (Sources and Before class) | Totten, *An Architectural Approach to Level Design* (2nd ed., 2019) chapter numbers (w04: ch. 4, 5, 6; w05: ch. 5; w07: ch. 4 and 6; w08: ch. 9; w09: ch. 7 and 10) could not be checked. The publisher and O'Reilly pages did not return a table of contents. Section titles in w04 ("Pathfinding with Architectural Weenies", "Organizing the Sandbox") are consistent with the book but also unconfirmed. | Check against a library copy of the 2nd edition. If a number is wrong, cite the section title only, as w12 already does with index entries. |
| lectures/w02 | Neon White "more than 50 changes to one level over three years" is second-hand: The Level Design Book quoting Blake Hester, Game Informer #350. The quote was confirmed on the Level Design Book page; the magazine itself was not seen. | Acceptable as cited. Optionally add "Game Informer #350" to the source line. |

## Notes for the orchestrator

- `syllabus.md` still carries the generated-stub marker. All 14 schedule rows already link to existing lectures and examples, so `tools/build_plan.py` only needs to clear the marker.
- MA201 has no lectures yet. w07 and w13 still link to `MA201/syllabus.md`. Upgrade when MA201 kinematics is written.
