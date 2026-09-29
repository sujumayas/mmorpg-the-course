"""Tests for Lab 02. Values come from the week 2 lecture, section 2.
Run with `python3 test_ltv.py` or `pytest test_ltv.py`."""
from dataclasses import replace

from ltv import Game, channel_report, lifetime_ltv, load_channels, ltv, payback_day, retention

G = Game()


def test_retention_table():
    assert abs(retention(G, 0) - 1.0) < 1e-12
    assert abs(retention(G, 1) - 0.545) < 1e-9
    assert abs(retention(G, 7) - 0.2183) < 1e-4
    assert abs(retention(G, 30) - 0.1364) < 1e-4


def test_ltv_curve():
    assert abs(ltv(G, 1) - 0.14) < 1e-9          # install day only
    assert abs(ltv(G, 31) - 0.989) < 1e-3         # days 0-30
    assert abs(ltv(G, 91) - 1.647) < 1e-3         # days 0-90
    assert ltv(G, 0) == 0


def test_lifetime():
    assert abs(lifetime_ltv(G) - 1.925) < 1e-9
    assert abs(ltv(G, 5000) - lifetime_ltv(G)) < 1e-6


def test_payback():
    assert payback_day(G, 1.50) == 70
    assert payback_day(G, 1.00) == 31
    assert payback_day(G, 0.14) == 0
    assert payback_day(G, 2.00) is None           # above lifetime LTV


def test_fee_scales_everything():
    no_fee = replace(G, fee=0.0)
    assert abs(lifetime_ltv(no_fee) - 2.75) < 1e-9
    assert payback_day(no_fee, 1.50) < payback_day(G, 1.50)


def test_channel_report():
    rows = {r[0]: r for r in channel_report(load_channels())}
    name, life, ratio, pay, at_h = rows["video_ads"]
    assert abs(life - 1.925) < 1e-9 and abs(ratio - 1.925 / 1.5) < 1e-9 and pay == 70
    assert rows["organic_referral"][2] == float("inf")
    assert rows["incentivized_installs"][3] is None or rows["incentivized_installs"][2] < 1.5


if __name__ == "__main__":
    failed = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print("PASS", name)
            except Exception as e:  # noqa: BLE001
                failed += 1
                print("FAIL", name, type(e).__name__, e)
    raise SystemExit(1 if failed else 0)
