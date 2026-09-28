"""CS202 Lab 02: UDP echo server. Sends every datagram straight back to its sender.

    python echo_server.py                 # listens on 127.0.0.1:40002
    python echo_server.py --host 0.0.0.0  # let a classmate's machine reach you (lab network only)
"""
import argparse
import socket

ap = argparse.ArgumentParser()
ap.add_argument("--host", default="127.0.0.1")
ap.add_argument("--port", type=int, default=40002)
a = ap.parse_args()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((a.host, a.port))
print(f"echo server on {a.host}:{a.port} (Ctrl+C to stop)", flush=True)
while True:
    data, addr = sock.recvfrom(2048)
    sock.sendto(data, addr)
