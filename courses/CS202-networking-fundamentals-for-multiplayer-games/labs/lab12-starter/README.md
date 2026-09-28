# Lab 12 starter

Standard library only. One file, `lockstep.py`, in two parts.

Part A, timing. Finish `execution_delay`, `simulate_turns` and `Peer.checksum` (all marked TODO). Then `python lockstep.py --check` should pass every test except the last one, "two peers stay in sync". `python lockstep.py --timing --turn 200 --k 2` prints the effective turn length for worst one-way latencies from 50 to 400 ms. Add `--jitter 60` to see what variable latency does.

Part B, the desync hunt. `python lockstep.py --sync` runs two peers on the same command script and compares checksums every turn. It reports the first turn where they differ and the units that differ. The starter contains more than one determinism bug. Find and fix each one without changing the command script, the tile-reservation rule or the hit chance. When `--check` prints `all checks passed`, you are done.
