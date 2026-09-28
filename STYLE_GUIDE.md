# Authoring Standard

Every lecture in this repository follows one standard so that 39 courses written by many authors (human or agent) read like one program. The exemplar that defines "done" is:

- `courses/MMO303-game-balance-i-combat-and-class-balance/lectures/w02-armor-and-damage-mitigation.md`
- `courses/MMO303-game-balance-i-combat-and-class-balance/examples/w02-armor-curve.html`

Read both before writing anything.

## 1. The worked-example standard

The program's teaching signature comes from short-form explainers like candlesan's "The Simple Math Hiding in Your Favorite Games" (the armor formula `Armor / (Armor + K)` traced through Diablo II and League of Legends). What makes that format work, and what every worked example here must reproduce:

1. **Hook from a shipped game.** Open with an observable, surprising fact players have felt. "100 armor halves damage in League, but 200 doesn't quarter it — so is armor getting worse?"
2. **One model, stated once.** The formula, algorithm, or diagram in its simplest form, with every symbol named.
3. **Numbers you can check.** A small table computed from the model, with values a student can verify by hand.
4. **A visual the student can move.** An interactive (slider, simulation, drag) where the key insight is *visible* — ideally two linked views where one looks one way and the other reveals the truth.
5. **Cross-game recognition.** Show the same principle in at least two other games or contexts, rewritten into the same form so the student sees it is one idea.
6. **Eyes-open design judgment.** Close with the trade-offs: when to use it, what problems alternatives create, what a designer should decide deliberately rather than by reflex.
7. **Check yourself.** Two or three questions whose answers require using the model, not recalling the text.

If an example has no step-5 cross-game link or no step-6 judgment, it is a math exercise, not a worked example. Fix it.

## 2. Lecture file template

Path: `courses/<CODE>-<slug>/lectures/wNN-<topic-slug>.md`

```markdown
# <CODE> · Week NN — <Title>

**Why this matters:** one or two sentences in the student's terms.
**You will be able to:** 3-4 measurable outcomes (verbs: compute, derive, design, critique).
**Before class:** readings with page/chapter ranges.
**Prerequisites from earlier courses:** links to earlier lectures.

## 1. <Concept section>
Prose explanation. Short paragraphs. Define every term on first use.

## 2. Worked example: <name>
Follows the 7-step standard above. Links the interactive in examples/.

## 3. <Further concept sections as needed>

## In-class activity (20-30 min)
A concrete task for pairs/groups, with materials and expected output.

## Common misconceptions
2-4 misconceptions with the correction.

## Check yourself
Questions; answers in a collapsed <details> block.

## Lab / assignment hook
Which lab this feeds (labs/labNN.md).

## Sources
Every factual claim about a real game, person, or study cites a source here.
```

Target length: 2,500–5,000 words per lecture (a 90-minute session plus reading).

## 3. Interactive example rules

Path: `courses/<CODE>-<slug>/examples/wNN-<name>.html`

- One self-contained HTML file. No build step, no external requests except fonts from Google Fonts. Must work offline if fonts fail (real fallback stacks).
- Mobile-first, responsive, keyboard accessible, respects `prefers-reduced-motion` and `prefers-color-scheme`.
- The first screen shows the insight, not instructions. Controls change the picture immediately.
- Show exact numbers next to the visual; students must be able to copy them into the lecture's table.
- Use the shared palette in `templates/interactive-tokens.css` (copy it inline) so the program feels coherent.
- No copyrighted characters, logos, screenshots or game art. Name games in text; draw everything generically.

## 4. Accuracy rules (non-negotiable)

- Any formula, number, date, or quote tied to a real game or study must be sourced in the lecture's Sources section. Prefer official sources (developer sites, GDC talks, papers), then well-maintained wikis.
- Items tagged `(verify)` in `curriculum.yaml` must be checked before the lecture is marked complete. If it cannot be verified, rewrite the example so it does not depend on the unverified figure, and say so.
- Distinguish "the game shows X on the tooltip" from "the game computes X".
- Formulas change across patches: always state the version or era ("classic WoW, attacker levels 1–59").
- No invented quotes. Paraphrase sources; quote at most one short phrase per source.

## 5. Voice

- Second person, direct, warm. Assume a smart first- or second-year student who plays games but hasn't studied them.
- Plain words before jargon. Jargon is introduced, defined, then used consistently.
- Every section earns its place: if deleting it loses nothing, delete it.
- Language: English as the master copy. Spanish translations live alongside as `*.es.md` when produced.

## 6. Definition of done for a course

- `syllabus.md` hand-finished (stub marker removed), schedule table links every lecture and example.
- 14 lecture files, each passing the template.
- Every signature worked example from `curriculum.yaml` built as an interactive.
- `labs/`: at least 6 labs with starter materials described and a rubric.
- `assessments/`: assignment briefs + rubrics, an exam bank of ≥40 questions with answers.
- A reviewer (human or agent) has run the QA checklist in `ORCHESTRATION.md` §4.
