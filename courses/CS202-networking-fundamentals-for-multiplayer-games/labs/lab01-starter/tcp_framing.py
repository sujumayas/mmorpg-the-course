"""CS202 Lab 01, part B: TCP is a byte stream, not a message stream.

    python tcp_framing.py demo     # shows the bug: three messages arrive glued together
    python tcp_framing.py test     # tests YOUR send_msg / recv_msg

The demo writes three short messages to a TCP socket, waits, then reads once.
With TCP_NODELAY off (Nagle on) or simply because the receiver read late, one
recv() call can return all three messages at once, or half of one.
Your job: finish send_msg and recv_msg so each call carries exactly one message,
using a 2-byte big-endian length prefix. Standard library only.
"""
import socket
import struct
import sys
import threading
import time


def send_msg(sock, payload: bytes) -> None:
    """Send one message: a 2-byte big-endian length, then the payload.

    TODO: raise ValueError if the payload is longer than 65535 bytes.
    TODO: build the header with struct.pack("!H", len(payload)) and send header + payload
          with sock.sendall (send() may send only part of the buffer).
    """
    raise NotImplementedError("send_msg")


def recv_exact(sock, n: int) -> bytes:
    """Read exactly n bytes, or raise ConnectionError if the peer closes first.

    TODO: loop on sock.recv(n - len(buf)) until buf has n bytes. recv() returning b""
          means the connection closed.
    """
    raise NotImplementedError("recv_exact")


def recv_msg(sock) -> bytes:
    """Read one message written by send_msg.

    TODO: read the 2-byte header with recv_exact, unpack it with struct.unpack("!H", ...),
          then read exactly that many payload bytes.
    """
    raise NotImplementedError("recv_msg")


def _pair():
    """A connected pair of TCP sockets on localhost."""
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.bind(("127.0.0.1", 0))
    srv.listen(1)
    cli = socket.create_connection(srv.getsockname())
    conn, _ = srv.accept()
    srv.close()
    return cli, conn


def demo():
    cli, conn = _pair()
    for text in [b"MOVE 10 4", b"CAST fireball", b"CHAT gg"]:
        cli.send(text)
    time.sleep(0.1)  # the receiver is "busy rendering a frame"
    data = conn.recv(4096)
    print(f"one recv() returned {len(data)} bytes: {data!r}")
    print("Three sends, one read. TCP kept every byte and the order, but not the boundaries.")
    cli.close()
    conn.close()


def test():
    cli, conn = _pair()
    msgs = [b"MOVE 10 4", b"", b"CAST fireball", b"x" * 3000, b"CHAT gg"]
    t = threading.Thread(target=lambda: [send_msg(cli, m) for m in msgs])
    t.start()
    got = [recv_msg(conn) for _ in msgs]
    t.join()
    assert got == msgs, f"expected {msgs!r}, got {got!r}"
    try:
        send_msg(cli, b"y" * 70000)
        raise AssertionError("send_msg accepted a 70,000-byte payload")
    except ValueError:
        pass
    cli.close()
    conn.close()
    print("framing tests passed: 5 messages in, 5 identical messages out")


if __name__ == "__main__":
    {"demo": demo, "test": test}[sys.argv[1] if len(sys.argv) > 1 else "demo"]()
