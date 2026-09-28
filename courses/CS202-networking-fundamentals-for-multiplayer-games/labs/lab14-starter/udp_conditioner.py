"""CS202 Lab 14: the conditioner model as a live UDP proxy (works on any OS).

    python udp_conditioner.py --delay 30 --jitter 15 --loss 0.01 --burst 0.5 --direction both

Use it with Lab 02's echo server and ping (../lab02-starter): the proxy listens on 40004
and forwards to the echo server on 40002. Each datagram in a conditioned direction gets
netem-style delay (delay +/- jitter, uniform) and Gilbert-Elliott loss with average rate
--loss and P(loss | previous lost) = --burst. Omit --burst for independent loss.
Seeded. Standard library only.
"""
import argparse
import heapq
import random
import select
import socket
import time

from conditioner import GilbertLoss

ap = argparse.ArgumentParser()
ap.add_argument("--listen", type=int, default=40004)
ap.add_argument("--server-host", default="127.0.0.1")
ap.add_argument("--server-port", type=int, default=40002)
ap.add_argument("--delay", type=float, default=30.0, help="one-way delay, ms")
ap.add_argument("--jitter", type=float, default=0.0, help="+/- uniform jitter, ms")
ap.add_argument("--loss", type=float, default=0.0, help="average loss rate p")
ap.add_argument("--burst", type=float, default=None, help="q = P(loss | previous lost)")
ap.add_argument("--direction", choices=["both", "up", "down"], default="both",
                help="up = client to server, down = server to client")
ap.add_argument("--seed", type=int, default=14)
a = ap.parse_args()

rng = random.Random(a.seed)
q = a.loss if a.burst is None else a.burst
losses = {"up": GilbertLoss(a.loss, q, rng), "down": GilbertLoss(a.loss, q, rng)}
client_side = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_side.bind(("127.0.0.1", a.listen))
server_side = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_side.bind(("127.0.0.1", 0))
server_addr = (a.server_host, a.server_port)
client_addr = None
queue, counter = [], 0


def schedule(direction, sock, data, dest):
    global counter
    ms = 0.0
    if a.direction in ("both", direction):
        if a.loss > 0 and losses[direction].drop():
            return
        ms = a.delay + rng.uniform(-a.jitter, a.jitter)
    counter += 1
    heapq.heappush(queue, (time.perf_counter() + ms / 1000, counter, sock, data, dest))


print(f"conditioner :{a.listen} -> {server_addr}, {a.direction}: delay {a.delay} +/- {a.jitter} ms, "
      f"loss p={a.loss} q={q}", flush=True)
while True:
    timeout = max(0.0, queue[0][0] - time.perf_counter()) if queue else 0.05
    ready, _, _ = select.select([client_side, server_side], [], [], timeout)
    for s in ready:
        data, addr = s.recvfrom(2048)
        if s is client_side:
            client_addr = addr
            schedule("up", server_side, data, server_addr)
        elif client_addr is not None:
            schedule("down", client_side, data, client_addr)
    now = time.perf_counter()
    while queue and queue[0][0] <= now:
        _, _, s, data, dest = heapq.heappop(queue)
        s.sendto(data, dest)
