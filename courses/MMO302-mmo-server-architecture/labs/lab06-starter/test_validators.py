"""Run: python test_validators.py   (prints 'all lab 06 tests passed')"""
from validators import (PerPacket, SlidingWindow, TokenBucket, max_sustained_factor, max_blink,
                        honest_trace, corrected_stalls, predicted_corrections, cheater_trace,
                        rejections)


def near(got, want, tol, label):
    assert abs(got - want) <= tol, f"{label}: got {got}, want {want} +- {tol}"


# the lecture's cheater table (v = 7, dt = 0.1, s = 0.25, W = 5)
near(max_sustained_factor(PerPacket), 3.5, 0.011, "per-packet sustained")
near(max_sustained_factor(SlidingWindow), 1.035, 0.02, "window sustained (1.02 to 1.05)")
near(max_sustained_factor(TokenBucket), 1.0, 1e-9, "bucket sustained")
near(max_blink(PerPacket), 2.45, 0.011, "per-packet blink")
near(max_blink(SlidingWindow), 36.75, 0.011, "window blink")
near(max_blink(TokenBucket), 2.45, 0.011, "bucket blink")
near(max_blink(lambda: TokenBucket(slack=0.5)), 4.2, 0.011, "bucket blink at s = 0.5")

# rejected moves must not change state
b = TokenBucket()
assert not b.check(0.0, 100.0), "a huge first move is rejected"
assert b.check(0.0, 2.45), "the rejected move did not spend credit"

# honest player with stalls: none rejected at a generous tolerance, formula at tighter ones
trace, stalls = honest_trace()
assert rejections(PerPacket(), trace) == 0, "per-packet passes every honest burst when s >= dt"
assert corrected_stalls(TokenBucket(slack=0.8), trace) == 0, "s = 0.8 covers every stall"
near(corrected_stalls(TokenBucket(slack=0.5), trace), predicted_corrections(0.5), 8,
     "bucket corrections at s = 0.5")
near(corrected_stalls(TokenBucket(slack=0.25), trace), predicted_corrections(0.25), 10,
     "bucket corrections at s = 0.25")
near(predicted_corrections(0.25), 55.0, 1e-9, "formula at 0.25")

# a legal-speed honest player with no stalls passes every check
clean = cheater_trace(1.0)
for cls in (PerPacket, SlidingWindow, TokenBucket):
    assert rejections(cls(), clean) == 0, f"{cls.__name__} rejected a legal player"

print("all lab 06 tests passed")
