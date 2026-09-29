# Lab 02 starter

Standard library only. Run from this folder with the course Python (`.venv/bin/python` at the repository root).

Part A, the protocol:

1. `python handoff.py --check` runs a dithering player across the border 30 times (three link delays, two band widths, five seeds). It checks that no two servers are ever authoritative at once, that every input is applied exactly once and in order, and that the final position is right.
2. `python handoff.py --trace` prints the messages of one handoff with a 2-tick link delay.

Part B, the cost:

3. `python seam.py --check` tests `update_owner`, `ghost_count` and `seam_cost_ms_per_s` and reproduces the handoff rates in the week 2 lecture.
4. `python seam.py --sweep seam.csv` writes handoffs per second, ghost count and seam CPU cost for band widths from 0 to 60 m.

Expected once finished: `all checks passed` from both scripts. The seam sweep runs in about 10 seconds.
