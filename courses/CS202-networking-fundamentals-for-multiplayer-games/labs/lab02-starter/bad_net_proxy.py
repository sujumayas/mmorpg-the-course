"""CS202 Lab 02: a UDP proxy that makes a good network bad, on purpose.

    python bad_net_proxy.py --delay 20 --jitter 5 --spike-chance 0.05 --spike 40 --loss 0.02

Point udp_ping.py at the proxy (default 127.0.0.1:40003). The proxy forwards to the echo
server (default 127.0.0.1:40002) and back. Each datagram, in each direction, gets:

    one-way delay = delay + uniform(0, jitter) + (spike, with probability spike_chance)
    dropped with probability loss

Because each datagram gets its own delay, a spike can make packets arrive out of order,
the same as on a real network. The random generator is seeded, so a run is repeatable
given the same timing. Standard library only. Week 14 replaces this with real tools
(netem, clumsy).
"""
import argparse
import heapq
import random
import select
import socket
import time

ap = argparse.ArgumentParser()
ap.add_argument("--listen", type=int, default=40003)
ap.add_argument("--server-host", default="127.0.0.1")
ap.add_argument("--server-port", type=int, default=40002)
ap.add_argument("--delay", type=float, default=20.0, help="base one-way delay, ms")
ap.add_argument("--jitter", type=float, default=5.0, help="uniform extra delay 0..jitter, ms")
ap.add_argument("--spike-chance", type=float, default=0.05)
ap.add_argument("--spike", type=float, default=40.0, help="extra delay of a spike, ms")
ap.add_argument("--loss", type=float, default=0.02, help="drop probability per datagram")
ap.add_argument("--seed", type=int, default=202)
a = ap.parse_args()

rng = random.Random(a.seed)
client_side = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_side.bind(("127.0.0.1", a.listen))
server_side = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_side.bind(("127.0.0.1", 0))
server_addr = (a.server_host, a.server_port)
client_addr = None
queue = []  # (release_time, counter, socket, data, destination)
counter = 0


def schedule(sock, data, dest):
    global counter
    if rng.random() < a.loss:
        return
    ms = a.delay + rng.uniform(0, a.jitter)
    if rng.random() < a.spike_chance:
        ms += a.spike
    counter += 1
    heapq.heappush(queue, (time.perf_counter() + ms / 1000, counter, sock, data, dest))


print(f"proxy :{a.listen} -> {server_addr}, delay {a.delay}+U(0,{a.jitter}) ms, "
      f"spike {a.spike} ms at p={a.spike_chance}, loss p={a.loss}", flush=True)
while True:
    # wake at least every 1 ms: select() often oversleeps its timeout by several ms
    timeout = min(0.001, max(0.0, queue[0][0] - time.perf_counter())) if queue else 0.05
    ready, _, _ = select.select([client_side, server_side], [], [], timeout)
    for s in ready:
        data, addr = s.recvfrom(2048)
        if s is client_side:
            client_addr = addr
            schedule(server_side, data, server_addr)
        elif client_addr is not None:
            schedule(client_side, data, client_addr)
    now = time.perf_counter()
    while queue and queue[0][0] <= now:
        _, _, s, data, dest = heapq.heappop(queue)
        s.sendto(data, dest)
