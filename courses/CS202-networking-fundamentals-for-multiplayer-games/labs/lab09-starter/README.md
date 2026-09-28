# Lab 09 starter

Standard library only. Run with the course Python (`.venv/bin/python` at the repository root, or any Python 3.10+).

- `netsim.py`: a one-axis player, a shared `step`, an authoritative server, a network with delay and loss, and a scripted two-second walk with a server-side snare at 1.0 s. You write `Client.on_input` (week 8), `Client.on_snapshot` and `Client.displayed_offset` (week 9).
- `python netsim.py --check` must print `all checks passed`.
- `python netsim.py --mode dumb|naive|reconcile [--rtt 150] [--loss 0.05] [--smooth 0.1] [--no-snare] [--input-loss 0.05] [--seed 1] [--csv out.csv]` prints a report and optionally writes one row per tick (server x, predicted x, drawn x, correction, pending inputs).
