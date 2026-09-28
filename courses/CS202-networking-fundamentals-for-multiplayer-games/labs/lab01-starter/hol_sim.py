"""CS202 Lab 01, part C: model head-of-line blocking.

    python hol_sim.py                       # 20 Hz, RTT 100 ms, packet 10 lost
    python hol_sim.py --hz 60 --rtt 100
    python hol_sim.py --hz 20 --rtt 100 --lost 10 11
    python hol_sim.py --table               # the lecture's table, for checking

The model is the one in the week 1 lecture, section 2:
- The sender sends packet i at time i * interval, interval = 1000 / hz ms.
- Every packet takes rtt / 2 ms one way. ACKs also take rtt / 2.
- UDP: a lost packet is simply never delivered. Everything else is delivered on arrival.
- TCP: packets are delivered to the game in order. A lost packet is resent either by
  fast retransmit (3 duplicate ACKs, triggered when packet k+3 arrives) or by the
  retransmission timeout (RTO), whichever comes first. The default RTO is RTT + 200 ms,
  which is what Linux converges to on a steady link. A packet cannot be delivered
  before every earlier packet has been delivered.

This is a teaching model. Real TCP stacks add delayed ACKs, SACK and RACK, and adapt the
RTO. They move the numbers; they do not remove the stall. Standard library only.
"""
import argparse


def udp_delivery(n, interval, one_way, lost):
    """Return a list of (packet, delivery_time_ms) for UDP, lost packets omitted."""
    return [(i, i * interval + one_way) for i in range(n) if i not in lost]


def tcp_delivery(n, interval, one_way, lost, rto):
    """Return a list of (packet, delivery_time_ms) for TCP, every packet delivered once.

    TODO 1: compute arrival[i] for every packet.
            Not lost: i * interval + one_way.
            Lost (lost only once; the retransmission always arrives):
              fast = (i + 3) * interval + 2 * one_way + one_way   if i + 3 < n, else infinity
              timeout = i * interval + rto + one_way
              arrival = min(fast, timeout)
    TODO 2: deliver in order. delivery[0] = arrival[0];
            delivery[i] = max(arrival[i], delivery[i - 1]).
    """
    raise NotImplementedError("tcp_delivery")


def gaps(deliveries):
    """Time between consecutive deliveries to the game, in ms."""
    times = [t for _, t in deliveries]
    return [b - a for a, b in zip(times, times[1:])]


def run(hz, rtt, lost, n=20, rto=None, show=True):
    interval = 1000.0 / hz
    if rto is None:
        rto = rtt + 200.0  # Linux on a steady link: smoothed RTT + variance term floored at 200 ms
    one_way = rtt / 2
    udp = udp_delivery(n, interval, one_way, set(lost))
    tcp = tcp_delivery(n, interval, one_way, set(lost), rto)
    if show:
        print(f"{hz} Hz (interval {interval:.1f} ms), RTT {rtt:.0f} ms, lost {sorted(lost)}, RTO {rto:.0f} ms")
        print(f"{'pkt':>4} {'UDP deliver':>12} {'TCP deliver':>12}")
        u = dict(udp)
        for i, t in tcp:
            ut = f"{u[i]:.1f}" if i in u else "lost"
            print(f"{i:>4} {ut:>12} {t:>12.1f}")
    return max(gaps(udp)), max(gaps(tcp))


def table():
    print(f"{'Hz':>4} {'RTT':>5} {'normal gap':>11} {'UDP max gap':>12} {'TCP max gap':>12}")
    for hz, rtt in [(20, 100), (60, 100), (20, 200), (60, 200), (30, 50)]:
        u, t = run(hz, rtt, [10], show=False)
        print(f"{hz:>4} {rtt:>5} {1000 / hz:>11.1f} {u:>12.1f} {t:>12.1f}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--hz", type=float, default=20)
    ap.add_argument("--rtt", type=float, default=100)
    ap.add_argument("--lost", type=int, nargs="*", default=[10])
    ap.add_argument("--rto", type=float, default=None, help="retransmission timeout, ms (default RTT + 200)")
    ap.add_argument("--n", type=int, default=20)
    ap.add_argument("--table", action="store_true")
    a = ap.parse_args()
    if a.table:
        table()
    else:
        u, t = run(a.hz, a.rtt, a.lost, a.n, a.rto)
        print(f"largest gap between deliveries: UDP {u:.1f} ms, TCP {t:.1f} ms")
