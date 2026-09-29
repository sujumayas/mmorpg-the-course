# PR402 Lab 10: Live triage sheet and weekly capacity

**Week:** 10 (Live-ops week 1). **Guide:** [week 10](../lectures/w10-live-ops-week-1.md). **Team lab**, submitted once per team.

## Objective

Run your live queue by a written rule. You will compute the break-even harm for a hotfix, your fix capacity net of incident follow-up, and a ranked triage sheet in which every hotfix or wait decision follows from its numbers.

## Starter materials

Create `production/week10/triage.csv` with these columns, in this order:

```
id,title,severity,h_basis,h,fix_hours,saved,per_hour,decision,shipped_in
```

- `severity` is `SEV1`, `SEV2` or `SEV3` from your severity table.
- `h_basis` is one line: which telemetry or report the harm estimate comes from, with the arithmetic (for example `6 new/h × 0.22 × 0.5 h`).
- `h` is harm per hour in player-hours. Leave it blank for SEV1 rows.
- `saved = h × T` and `per_hour = saved / fix_hours`, rounded to two decimals.
- `decision` is `sev1`, `hotfix`, `patch-no-capacity` or `patch-below-breakeven`.
- `shipped_in` is the build number that closed it, filled in later.

Create `production/week10/capacity.md`:

```
Scheduled patch: day ___ time ___     T (hours from triage to patch) = ___
Restart: ___ players online × ___ min / 60 = D = ___
Hotfix risk: r ___ × H ___ = ___       Hotfix cost = ___
Break-even h* = ___ / ___ = ___
Fix rota: ___ people × ___ h/day × ___ days = ___
Expected incidents ___ × 6 h = ___     Fix capacity = ___
SEV1 hours taken first: ___            Hours for ranked work: ___
On-call hours per person this week: | Name | Hours | Share of course hours |
```

## Steps

1. **Warm-up (10 minutes).** Fill `capacity.md` and five rows of `triage.csv` with the guide's worked example. You must get a hotfix cost of 7.8, break-even 0.16, capacity 18, 13.5 hours for ranked work, and decisions `sev1`, `hotfix`, `hotfix`, `patch-no-capacity`, `patch-below-breakeven` for A, B, D, C, E. Save as `warmup-triage.csv` and `warmup-capacity.md`.
2. **Capacity.** Fill `capacity.md` for your team this week. Take the expected incident count from the launch log. Take `r` and `H` from your team's judgment and write one line on why.
3. **Queue.** Export every open issue from the tracker. Give each a severity. For each non-SEV1 issue, write `h_basis` and `h` from telemetry where you can. Mark estimates without telemetry with `est` at the start of `h_basis`.
4. **Rank and decide.** Handle SEV1 rows first and subtract their hours. Sort the rest by `per_hour`. Mark issues below break-even as `patch-below-breakeven`. Fill the remaining capacity from the top; the rest become `patch-no-capacity`.
5. **Ship.** Bundle the `sev1` and `hotfix` rows into one hotfix. Record the build number in `shipped_in`.
6. **Tell players.** Update the known-issues post with every `patch-*` row that players can see, including a workaround where one exists.
7. **Retro check.** At the next daily review after the hotfix, compare `h` for each shipped fix against what the telemetry now shows. Add a `note` line under the CSV for any estimate that was off by more than a factor of two.

## Deliverable

In `production/week10/`: the two warm-up files, `triage.csv`, `capacity.md`, and a link to the known-issues post.

**Checkable output:** the instructor recomputes the break-even and fix capacity from `capacity.md`, then recomputes `saved`, `per_hour` and `decision` for three rows of `triage.csv`. All must match. Every row marked `hotfix` must appear in one hotfix build.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Warm-up | 2 | All values and decisions match the guide |
| Capacity | 4 | Rota-based, net of incident follow-up; on-call hours listed per person and within the team's limit |
| Harm estimates | 4 | Every non-SEV1 row has a basis; telemetry used where it exists; estimates marked |
| Decisions | 5 | SEV1 first; break-even applied; capacity filled by rank; three rows recompute |
| Shipping and posts | 3 | Hotfix rows bundled with build numbers; known-issues post updated with workarounds |
| Retro check | 2 | Shipped estimates compared with post-fix telemetry; large misses noted |
