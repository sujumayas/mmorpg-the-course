"""Run with:  python test_tickmetrics.py   (or pytest)."""
import tickmetrics as tm
import zones

LECTURE = [12 + (i * 7) % 13 for i in range(970)] + [45] * 20 + [140] * 10
QUIET = [8 + i % 6 for i in range(1000)]


def hist(values):
    h = tm.TickHistogram()
    for v in values:
        h.observe(v)
    return h


def test_nearest_rank_matches_lecture():
    assert tm.nearest_rank(LECTURE, 0.50) == 18
    assert tm.nearest_rank(LECTURE, 0.95) == 24
    assert tm.nearest_rank(LECTURE, 0.99) == 45
    assert tm.nearest_rank(LECTURE, 0.999) == 140


def test_histogram_quantile_and_count():
    h = hist(LECTURE)
    assert h.total == 1000 and h.count_over(50) == 10
    assert abs(h.quantile(0.99) - 50.0) < 1e-9
    assert abs(hist(QUIET).quantile(0.99) - 14.9) < 0.05


def test_merge_equals_combined():
    merged = hist(LECTURE)
    for _ in range(9):
        merged = merged.merge(hist(QUIET))
    combined = hist(LECTURE + QUIET * 9)
    assert merged.counts == combined.counts and merged.total == combined.total
    assert abs(merged.quantile(0.99) - 23.8) < 0.05


def test_stall_formulas():
    assert abs(tm.stalls_per_minute(0.01, 20) - 12) < 1e-9
    assert abs(tm.share_of_seconds_with_stall(0.01, 20) - 0.18209306) < 1e-6
    assert abs(tm.stalls_per_minute(0.005, 30) - 9) < 1e-9


def test_alert_finds_the_gc_zone_only():
    assert tm.stall_alert(zones.all_zones()) == ["harbor-07"]


if __name__ == "__main__":
    failed = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print("PASS", name)
            except Exception as e:
                failed += 1
                print("FAIL", name, "-", type(e).__name__, e)
    raise SystemExit(1 if failed else 0)
