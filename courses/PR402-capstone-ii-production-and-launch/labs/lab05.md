# PR402 Lab 05: Closed beta plan

**Week:** 5 (Closed beta). **Guide:** [week 5](../lectures/w05-closed-beta-recruiting-and-stress-windows.md). **Team lab**, submitted once per team.

## Objective

Plan a closed beta that puts enough real players on your server at the same moment to test your launch-evening peak. You will set a concurrency target, work backwards through the tester funnel to the invites you need, split them into batches, schedule two stress windows and state what the beta's exposure can and cannot prove. The checker confirms the plan reaches the target and meets the course's conduct rules.

## Starter materials

In [`labs/lab05-starter/`](lab05-starter/):

- `check_beta_plan.py`. Standard library only. Run it with `.venv/bin/python check_beta_plan.py beta.csv batches.csv windows.csv`. It prints the testers and invites needed, the concurrency you would see without windows, the exposure and its rule-of-three bound, then `PASS` or `NOT READY`. It exits with code 1 when a rule fails.
- `beta.csv`. Emberfall's inputs from the guide, with sources. Two of the values break course rules on purpose.
- `batches.csv`. One invite batch, too small.
- `windows.csv`. One stress window.

## Steps

1. **Warm-up (10 minutes).** Run the checker on the starter files and read the six failures. Fix them the way the guide describes: 334 invites in two batches with about 60% first, a second window on another day, a lower friends share and a live consent notice. The checker should print `PASS`.
2. **Your target.** Set `target_ccu` from your own week 3 evening peak forecast. Write the link to lab 03 in `source`.
3. **Your funnel.** Start with guesses for `p_start` and `p_window` and say so in `source`. Use sessions and hours from your alpha playtest.
4. **Batches.** Plan at least two invite batches. The first goes out at the end of the week 5 meeting.
5. **Windows.** Schedule two windows of 60 to 120 minutes on different days, at times your testers can make. Put the times in the invite text.
6. **Conduct and consent.** Publish the consent notice, code of conduct and wipe notice in the launcher before batch 1. Set `consent_notice_live` to `yes` and give the page's location as the source. Keep friends and classmates at or below half of the planned testers.
7. **After 24 hours.** Replace `p_start` with the measured value, rerun the checker, and size batch 2 from the new output. Commit both runs.
8. **After the first window.** Replace `p_window` with the measured value and rerun. If the second window cannot reach the target, say how you will fill the gap and report bots and humans apart.

## Deliverable

In `production/week05/` in the team repository:

- `beta.csv`, `batches.csv` and `windows.csv` passing `check_beta_plan.py`, with the planning run saved as `check-output-plan.txt` and the measured-rate run as `check-output-measured.txt`.
- The invite text, showing the window times.
- Links to the live consent notice, code of conduct and wipe notice.

**Checkable output:** the instructor reruns `check_beta_plan.py` on your three files. It must print `PASS` and exit with code 0.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Checker passes | 4 | `PASS` on rerun; both output files present |
| Target and funnel | 4 | Target tied to the week 3 forecast; rates sourced, then replaced by measured values |
| Batches and windows | 4 | Batch 2 sized from measured `p_start`; two announced windows on different days |
| Consent and conduct | 4 | Notice, code of conduct and wipe notice live before the first invite; telemetry uses game IDs only |
| Exposure statement | 2 | The beta report states the rule-of-three bound and what it means for launch week |
| Honest counts | 2 | Window peaks reported with humans and bots apart |
