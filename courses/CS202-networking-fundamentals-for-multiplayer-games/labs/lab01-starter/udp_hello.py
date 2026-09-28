"""CS202 Lab 01, part A: the smallest useful UDP program.

Run the server in one terminal and the client in another:

    python udp_hello.py server
    python udp_hello.py client --count 5

The client sends numbered datagrams. The server prints each one and echoes it back.
Nothing here is reliable: if a datagram is lost, nobody resends it.
Standard library only.
"""
import argparse
import socket
import time

HOST = "127.0.0.1"
PORT = 40001


def run_server(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # SOCK_DGRAM = UDP
    sock.bind((HOST, port))
    print(f"UDP server listening on {HOST}:{port} (Ctrl+C to stop)")
    while True:
        data, addr = sock.recvfrom(2048)  # one call returns exactly one datagram
        print(f"from {addr}: {len(data)} bytes: {data!r}")
        sock.sendto(data, addr)  # echo it back to whoever sent it


def run_client(port, count, interval):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1.0)
    for seq in range(count):
        msg = f"seq={seq} t={time.perf_counter():.6f}".encode()
        sent_at = time.perf_counter()
        sock.sendto(msg, (HOST, port))
        try:
            reply, _ = sock.recvfrom(2048)
            rtt_ms = (time.perf_counter() - sent_at) * 1000
            print(f"seq {seq}: echo {len(reply)} bytes, round trip {rtt_ms:.3f} ms")
        except socket.timeout:
            print(f"seq {seq}: no reply within 1 s (lost, or no server running)")
        time.sleep(interval)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["server", "client"])
    ap.add_argument("--port", type=int, default=PORT)
    ap.add_argument("--count", type=int, default=5)
    ap.add_argument("--interval", type=float, default=0.05, help="seconds between sends")
    a = ap.parse_args()
    if a.mode == "server":
        run_server(a.port)
    else:
        run_client(a.port, a.count, a.interval)
