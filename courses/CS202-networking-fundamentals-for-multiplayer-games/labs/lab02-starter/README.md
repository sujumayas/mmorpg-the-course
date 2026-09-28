# Lab 02 starter

Standard library only. Three terminals:

1. `python echo_server.py` (port 40002)
2. `python bad_net_proxy.py --delay 20 --jitter 5 --spike-chance 0.05 --spike 40 --loss 0.02` (port 40003)
3. `python udp_ping.py --port 40003 --hz 20 --seconds 30 --out run.csv`

Then `python analyze.py run.csv`. Before that, finish the functions marked TODO in `analyze.py` and run `python analyze.py --check`, which tests them on `sample_run.csv` (the 20-packet dataset from the week 2 lecture plus one lost packet).

`sample_run.csv` columns: `seq, send_ms, rtt_ms, arrival_order`. An empty `rtt_ms` means the echo never came back.
