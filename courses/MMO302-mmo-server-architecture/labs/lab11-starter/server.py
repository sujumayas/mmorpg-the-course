"""MMO302 lab 11: a toy world-server service to load test. Complete; do not edit.

It accepts TCP connections on 127.0.0.1:9302. Each request is one line of text
(a request id). One worker handles requests in arrival order and spends a
random, CPU-bound service time on each (exponential, mean --service-ms), the way
a single-threaded zone server spends CPU on each player action. The reply is the
same line sent back.

Run:  python server.py [--service-ms 2.0] [--port 9302]
Stop: Ctrl+C. The server prints requests handled per second every 5 s.
"""
import argparse
import asyncio
import random
import time


async def main(service_ms, port, seed):
    rng = random.Random(seed)
    queue = asyncio.Queue()
    handled = 0

    async def handle(reader, writer):
        try:
            while True:
                line = await reader.readline()
                if not line:
                    break
                await queue.put((line, writer))
        except ConnectionError:
            pass

    async def worker():
        nonlocal handled
        while True:
            line, writer = await queue.get()
            end = time.perf_counter() + rng.expovariate(1000.0 / service_ms)
            while time.perf_counter() < end:       # burn CPU, like real game logic
                pass
            try:
                writer.write(line)
                await writer.drain()
            except ConnectionError:
                pass
            handled += 1
            await asyncio.sleep(0)                  # let new requests be read

    async def report():
        nonlocal handled
        while True:
            await asyncio.sleep(5)
            print(f"{handled / 5:7.1f} req/s handled, queue {queue.qsize()}", flush=True)
            handled = 0

    server = await asyncio.start_server(handle, "127.0.0.1", port)
    print(f"listening on 127.0.0.1:{port}, mean service {service_ms} ms "
          f"(capacity about {1000 / service_ms:.0f} req/s)", flush=True)
    async with server:
        await asyncio.gather(server.serve_forever(), worker(), report())


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--service-ms", type=float, default=2.0)
    ap.add_argument("--port", type=int, default=9302)
    ap.add_argument("--seed", type=int, default=1)
    a = ap.parse_args()
    try:
        asyncio.run(main(a.service_ms, a.port, a.seed))
    except KeyboardInterrupt:
        pass
