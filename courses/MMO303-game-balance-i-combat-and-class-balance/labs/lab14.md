# MMO303 · Lab 14: Patch notes from simulation evidence

**Assigned:** week 14 ([lecture](../lectures/w14-communicating-balance-changes.md)). **Due:** one week later. **Builds on:** [Lab 13](lab13.md). **Prepares for:** the week 15 final 4-class balance pass.

## Objective

Use your Lab 13 simulator to bring four classes inside a ±3% band of the role average, then publish the changes as patch notes that a reader can decode correctly without seeing your simulator. You will measure how well your notes communicate by having a classmate predict each change blind.

## Starter materials

- Your Lab 13 `sim.py`, balance matrix and report.
- The patch entry template below. It is the five-part checklist from lecture section 3. Copy it into `patch-notes.md` once per changed class.
- The blind-read sheet below. Copy it into `blind_read_sheet.md` and give it to your classmate with one row per patch line.

**Patch entry template.** Fill every part. Write "unchanged" rather than leaving a part out.

```
<Class name>
  <Ability or stat, by its in-game name>
  - <Value name>: <old> ⇒ <new>   (game units; ranks as a/b/c if they differ)
  - <Related value players may assume changed>: unchanged (<value>)
  Context: <1 to 3 sentences. What the data showed, for which audience.>
  Intended effect: <outcome in plain words>. Simulated total damage change
  <+x.x% ± y.y%> (95% interval) at <fight length> s, <+x.x% ± y.y%> at <fight length> s.
```

The five parts map to the lines as follows: target (class and ability lines), old ⇒ new (the value lines), context, intended effect, and what did not change (the "unchanged" line).

**Blind-read sheet.** One row per patch line. The reader fills the last three columns using only your notes and a calculator.

| Patch line (copied verbatim) | Buff or nerf | For whom (class, and fight length if it matters) | Total damage change for that class (estimate, %) |
|---|---|---|---|
| | | | |
- The week 14 interactive, [`examples/w14-patch-line-translator.html`](../examples/w14-patch-line-translator.html), for checking per-rank and breakpoint effects.

If your Lab 13 matrix had errors, the instructor will provide a reference matrix. Use it and say so in your report.

## Steps

1. **Set the target (15 min).** From your Lab 13 matrix, compute the role average for the 60-second and 300-second fight lengths. Mark every cell whose 95% interval lies entirely outside ±3% of that average.
2. **Find each class's damage shares (30 min).** Extend your simulator to record damage per ability (for the Berserker, split Frenzied and normal hits; for the Ritualist, Hit versus Rite). Report each ability's share `s` per class and fight length.
3. **Design changes (45 min).** For each out-of-band class, choose at most two changes. Use `δ_total = Σ sᵢ δᵢ` to predict the change you need before you run anything. Prefer changes that fix the out-of-band fight length without pushing the other one out of band.
4. **Verify with the simulator (45 min).** Rerun the full matrix with your changes. Use common random numbers against the old version so each class's change has a tight error bar. Every cell must now have its 95% interval inside ±3%, or you must explain why it cannot be.
5. **Check for breakpoints (15 min).** Add a target with 500 health to your simulator and compute hits to kill per class before and after. Flag any change that crosses a hits-to-kill threshold.
6. **Write the notes (45 min).** One entry per changed class, following the checklist. Every percentage stat is written old ⇒ new. Every intended-effect line gives the simulated total change with its 95% interval and the fight length it applies to.
7. **Blind read (30 min, in the lab session).** Swap notes with a classmate. They fill in their copy of the blind-read sheet (`blind_read_sheet.md`) using only your notes and a calculator. Collect their sheet.
8. **Score the mismatch (20 min).** For each line, compare their "buff or nerf" and "for whom" with the truth, and their estimated total change with your simulated value. Rewrite any line where they got the direction wrong or were off by more than 1 percentage point.

## Deliverable

- `patch-notes.md`: the final notes (after the rewrite in step 8), plus the original version as an appendix.
- `report.md` (600 to 1,000 words): the before and after matrices with error bars; the share table; for each change, the predicted `δ_total` from shares next to the simulated value; the breakpoint check; the blind-read results and what you rewrote and why.
- Your classmate's completed `blind_read_sheet.md`.
- Seeds and commands for every simulated table.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Weight |
|---|---|---|---|---|
| Balance result | Every cell's 95% interval inside ±3%, or a convincing reason given for any exception | Most cells in band; exceptions unexplained | Classes still clearly out of band | 25% |
| Prediction from shares | Share-based predictions within 0.5 points of simulation, or the gap explained (state, procs, breakpoints) | Predictions made, gaps unexplained | No predictions before simulating | 20% |
| Patch-note quality | All five checklist parts on every entry; units unambiguous; audience named | Most parts present; one ambiguous percent | Numbers only, or ambiguous units throughout | 25% |
| Evidence in notes | Intended-effect lines carry simulated totals with intervals and fight length | Totals given without intervals | No measured effect stated | 10% |
| Blind-read loop | Mismatches scored, every flagged line rewritten, rewrite reasons given | Scored but not rewritten | Not done | 15% |
| Reproducibility | Seeds and commands for every table | Partial | None | 5% |
