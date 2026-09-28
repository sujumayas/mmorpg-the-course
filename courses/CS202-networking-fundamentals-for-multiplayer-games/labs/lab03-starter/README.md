# Lab 03 starter

Standard library only.

- `topology.py`: bandwidth and latency functions for mesh, dedicated-server and listen-server topologies. Finish every TODO, then `python topology.py --check` must print `all checks passed`.
- `scenario.json`: the four-player scenario from the week 3 lecture. Copy it to `my_scenario.json` for step 5 and change the numbers.
- `python topology.py scenario.json --n 8` prints the bandwidth table for 8 players (the lab also asks for `--n 64`) and the worst-pair latency for every topology.
