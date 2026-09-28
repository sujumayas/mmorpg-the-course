# Course Architecture Research

This document records why the program is shaped the way it is. It should be revisited whenever `curriculum.yaml` changes substantially.

## 1. Frameworks consulted

**IGDA Curriculum Framework (2003, revised 2008).** Drafted by the IGDA Education Committee (Doug Church, Warren Spector, Robin Hunicke, Eric Zimmerman and others), it deliberately avoids a single prescribed curriculum and instead defines core topic areas that programs combine modularly. Its core areas are critical game studies, games and society, game design, game programming, visual design, audio design, interactive storytelling, game production, and the business of games.

**How it maps here.** Years 1–2 cover every IGDA core area at least once:

| IGDA core area | Courses in this program |
|---|---|
| Critical game studies | GS101 |
| Games and society | UX201, then MMO305/MMO402 in depth |
| Game design | GD101, GD102, GD201, GD203 |
| Game programming | CS101, CS102, CS201, CS202, CS203 |
| Visual design | AR101 |
| Audio design | AU101 |
| Interactive storytelling | GD202, MMO406 |
| Game production | PR101, PR201, capstones |
| Business of games | MMO403 |

## 2. Benchmark programs

**DigiPen, BS in Computer Science and Game Design.** A four-year, eight-semester program (15-week semesters, at least 142 credits) that pairs C/C++ programming, data structures, AI and algorithms with linear algebra, calculus and Newtonian dynamics, alongside design theory, level design, playtesting and repeated team game projects. Two lessons borrowed:

- **Math is taught as a design tool, early.** Here MA101/MA102 run in year 1, alongside design, so the armor formula and loot probability arrive before the balance courses that need them.
- **A team project every year.** PR101 (jam), PR201 (multiplayer slice), PR301 (persistent world), PR401/402 (capstone).

**Richard Bartle, CE317/CE817 Virtual Worlds (University of Essex).** A one-term module of ten lectures plus classes, still running in 2025, taught by the co-creator of MUD1. Evidence that virtual-world design is teachable as its own subject; MMO301 is modelled on its scope and uses Bartle's book, which he made freely available in 2021.

**Edward Castronova's virtual world design courses (Indiana University).** Castronova drafted a "Virtual Worlds 101" syllabus in 2004 and taught virtual world design at Indiana. His economic lens is why the program has two economy courses (MMO304, MMO401) rather than one lecture.

**Other programs.** Staffordshire University's online games module built on Bartle, Mulligan & Patrovsky's *Developing Online Games*, and Hall & Novak's *Online Game Development*; UC Berkeley's "Designing Virtual Worlds" combined architecture theory with social and cultural questions of place. Both reinforced treating MMO design as simultaneously technical, economic and social.

## 3. Why the MMO specialization has these six pillars

The MMO track (years 3–4) is organized around six pillars, each with a two-course depth sequence:

| Pillar | Year 3 | Year 4 | Anchor literature |
|---|---|---|---|
| Worlds | MMO301 Virtual Worlds | MMO406 Worldbuilding | Bartle, *Designing Virtual Worlds*; Koster |
| Technology | MMO302 Server Architecture, MMO309 Security | MMO404 Advanced Networked Simulation | Bernier (Valve), Fiedler, Gambetta; CCP on time dilation |
| Balance | MMO303 Combat & Class | MMO307 PvP, Progression & Endgame | Schreiber & Romero, *Game Balance*; Sirlin; Elo/Glicko/TrueSkill |
| Economy | MMO304 Faucets, Sinks & Markets | MMO401 Markets, Governance & Macro | Lehdonvirta & Castronova, *Virtual Economies* |
| Society | MMO305 Social Systems | MMO402 Emergent Society & Ethics, MMO405 Research Methods | Taylor, *Play Between Worlds*; Ducheneaut et al.; Yee; Boellstorff |
| Operation | MMO306 Content at Scale, MMO308 Live Ops | MMO403 Business, MMO407 Launch & Post-mortems | Seif El-Nasr et al., *Game Analytics* |

**Economy.** Lehdonvirta & Castronova (MIT Press, 2014) teach elementary microeconomics for designers: rational choice, virtual vs information goods, supply and demand, monopoly, pricing, externalities. Their faucet/sink/transformation model underpins MMO304: faucets create currency or items, sinks remove them (fees, repair, decay), and transformations like crafting convert one asset to another; when faucets outrun sinks, inflation follows.

**Balance.** The candlesan armor short shows the teaching model: one formula (`Armor / (Armor + K)`), recognized across games, with a design judgment at the end. MMO303 week 2 is the exemplar lecture for the whole program.

## 4. Pedagogical decisions

1. **Worked examples over abstraction.** Every major concept ships with an interactive, cross-game worked example (see `STYLE_GUIDE.md` §1).
2. **Spiral curriculum.** Key ideas appear three times at rising depth: e.g. `A/(A+K)` in MA101 (as a rational function), GD203 (as a combat formula), MMO303 (as a balance tool across classes). Faucets and sinks appear in GD102, MMO304 and MMO401.
3. **Engine-agnostic concepts, one reference stack.** Godot 4 for the client (open source, free for students), C++ for engine internals, C#/.NET for the reference server, PostgreSQL/Redis for persistence.
4. **Evidence and ethics throughout.** Every MMO course treats players as people: toxicity, addiction, monetization ethics and research ethics are core, not electives.
5. **Verifiability.** Game formulas change across patches; every claim is versioned and sourced, and `(verify)` flags in the YAML block publication until checked.

## 5. Open questions for the program owner

- Language of delivery: English master copy with Spanish translations (`*.es.md`), or Spanish-first?
- Whether AR101/AU101 should be replaced by a single "Game Art & Audio" course to make room for a second math course (calculus) in year 1.
- Whether to add a regional module on the Latin American games industry and player cultures.

## Sources

- IGDA Education Committee, *IGDA Curriculum Framework* v2.3 (2003) and 2008 revision; Gold, Fullerton & El-Nasr, SIGGRAPH 2007 session on the framework.
- DigiPen Institute of Technology, 2020–2021 Course Catalog Addendum; BS in Computer Science and Game Design program page.
- Bartle, R. CE317/CE817 Virtual Worlds, lecture 1 slides (University of Essex, 2025); *Designing Virtual Worlds* (New Riders, 2003).
- Castronova, E. "Virtual Worlds 101: Draft Syllabus", Terra Nova (2004); Indiana University MSCH-G290 Virtual World Design listing.
- Staffordshire University module descriptor (online games); UC Berkeley Townsend Center, "Designing Virtual Worlds".
- Lehdonvirta, V. & Castronova, E. (2014). *Virtual Economies: Design and Analysis*. MIT Press.
- candlesan, "The Simple Math Hiding in Your Favorite Games" (YouTube Short).
