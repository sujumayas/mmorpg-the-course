# Lab 01 starter

Standard library only. Run every file with the course Python (`.venv/bin/python` at the repository root, or any Python 3.10+).

- `udp_hello.py`: a complete UDP echo server and client. Run `python udp_hello.py server` in one terminal and `python udp_hello.py client --count 5` in another.
- `tcp_framing.py`: `demo` shows three TCP writes arriving as one read. `test` checks your `send_msg`, `recv_exact` and `recv_msg`, which you write.
- `hol_sim.py`: the week 1 head-of-line model. `udp_delivery` is done; you write `tcp_delivery`. `python hol_sim.py --table` must then print the lecture's table (20 Hz and RTT 100 ms gives a 300 ms TCP gap).
