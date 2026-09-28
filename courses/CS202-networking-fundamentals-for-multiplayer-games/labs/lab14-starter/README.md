# Lab 14 starter

Standard library only. Run from this folder.

1. `python conditioner.py` tests `GilbertLoss.drop`, `burst_lengths`, `reorder_count` and `bursts_per_minute`, including a million-packet check of the loss rate and burst length and a 200-seed check of the week 14 formula. It fails with `NotImplementedError` until you fill in the TODOs.
2. `python run_matrix.py` runs `toy_client.py` under every profile in `profiles.json`, 10 seeds each, 60 simulated seconds per run. `python run_matrix.py --repro <profile> <seed>` replays one run and describes its first failure.
3. `python udp_conditioner.py --delay 30 --jitter 15 --loss 0.01 --burst 0.5` is the same model as a live UDP proxy on port 40004, for use with `../lab02-starter/echo_server.py` and `udp_ping.py --port 40004`.

`toy_client.py` has bugs on purpose. Do not read it closely until step 3 of the lab tells you to.
