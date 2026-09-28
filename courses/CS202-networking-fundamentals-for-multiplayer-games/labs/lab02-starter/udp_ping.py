"""CS202 Lab 02: a game-style UDP ping. Sends small numbered packets at a fixed rate and
records the round trip of each echo.

    python udp_ping.py --port 40003 --hz 20 --seconds 30 --out run.csv

Each packet carries a 4-byte sequence number and an 8-byte send timestamp (12 bytes of
payload, 40 bytes on the wire with IPv4 and UDP headers). The output CSV has one row per
packet sent:

    seq, send_ms, rtt_ms, arrival_order

rtt_ms is empty if no echo came back before the run ended plus a 1-second grace period.
arrival_order is the position in which the echo arrived (0, 1, 2, ...), so you can find
reordering. Standard library only.
"""
import argparse
import csv
import socket
import struct
import time

ap = argparse.ArgumentParser()
ap.add_argument("--host", default="127.0.0.1")
ap.add_argument("--port", type=int, default=40003, help="40003 = through the proxy, 40002 = direct")
ap.add_argument("--hz", type=float, default=20.0)
ap.add_argument("--seconds", type=float, default=30.0)
ap.add_argument("--out", default="run.csv")
a = ap.parse_args()

FMT = "!Id"  # uint32 sequence, float64 send time in ms
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setblocking(False)
dest = (a.host, a.port)
interval = 1.0 / a.hz
total = int(a.seconds * a.hz)
t0 = time.perf_counter()
sent = {}      # seq -> send_ms
rtt = {}       # seq -> rtt_ms
order = {}     # seq -> arrival position
next_send = t0
seq = 0
deadline = t0 + a.seconds + 1.0

while True:
    now = time.perf_counter()
    if seq < total and now >= next_send:
        send_ms = (now - t0) * 1000
        sock.sendto(struct.pack(FMT, seq, send_ms), dest)
        sent[seq] = send_ms
        seq += 1
        next_send += interval
    try:
        while True:
            data, _ = sock.recvfrom(64)
            s, send_ms = struct.unpack(FMT, data)
            if s not in rtt:  # ignore duplicates
                rtt[s] = (time.perf_counter() - t0) * 1000 - send_ms
                order[s] = len(order)
    except BlockingIOError:
        pass
    if now > deadline:
        break
    time.sleep(0.0005)

with open(a.out, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["seq", "send_ms", "rtt_ms", "arrival_order"])
    for s in range(seq):
        w.writerow([s, f"{sent[s]:.3f}",
                    f"{rtt[s]:.3f}" if s in rtt else "",
                    order.get(s, "")])
print(f"sent {seq}, echoed {len(rtt)}, wrote {a.out}")
