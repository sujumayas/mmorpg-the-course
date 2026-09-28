"""CS101 lab 14: the logic behind screen shake and particles, headless.

Run:   python juice.py        (prints a shake timeline and a particle count)
Test:  python test_lab14.py

Nothing here draws anything. You test the numbers in Python, then port the
same few lines to GDScript in your arcade game (step 7 of the lab sheet).
"""
import math
import random


# ---------------------------------------------------------------- trauma ---
class Trauma:
    """A 0..1 'how hurt is the camera' value.

    add(amount)  raises trauma, never above 1.
    update(dt)   lowers trauma by `decay` per SECOND, never below 0.
    shake()      returns trauma ** power, the number you scale offsets by.
    """

    def __init__(self, decay=0.8, power=2):
        self.value = 0.0
        self.decay = decay
        self.power = power

    def add(self, amount):
        # TODO (step 2): clamp so value never goes above 1.0
        self.value = self.value + amount

    def update(self, dt):
        # TODO (step 3): this line is frame-rate DEPENDENT. It removes the
        # same amount every frame, so a 144 Hz monitor stops shaking 2.4x
        # sooner than a 60 Hz one. Use dt, and clamp at 0.
        self.value = self.value - self.decay / 60

    def shake(self):
        return max(self.value, 0.0) ** self.power


# ----------------------------------------------------------------- noise ---
def _lattice(seed, i):
    """A repeatable pseudo-random value in [-1, 1] for integer i."""
    return random.Random(seed * 1_000_003 + i).uniform(-1.0, 1.0)


def value_noise(seed, x):
    """Smooth 1D noise: random values at integers, eased in between.

    Same seed and x always give the same value. Neighbouring x values give
    neighbouring results, which is why the camera glides instead of jitters.
    """
    i = math.floor(x)
    f = x - i
    s = f * f * (3 - 2 * f)  # smoothstep, see MA101 week 9
    a, b = _lattice(seed, i), _lattice(seed, i + 1)
    return a + (b - a) * s


def shake_offset(trauma, t, max_offset=16.0, freq=15.0, seed=1):
    """Camera offset in pixels at time t (seconds) for a Trauma object."""
    amount = trauma.shake()
    dx = max_offset * amount * value_noise(seed, t * freq)
    dy = max_offset * amount * value_noise(seed + 1, t * freq)
    return dx, dy


# ------------------------------------------------------------- particles ---
class Emitter:
    """Emits `rate` particles per second, each living `lifetime` seconds.

    A particle is a dict: {"x", "y", "vx", "vy", "age"}.
    """

    def __init__(self, rate, lifetime, gravity=300.0):
        self.rate = rate
        self.lifetime = lifetime
        self.gravity = gravity
        self.particles = []
        self.to_emit = 0.0  # fractional particles owed, like a timestep accumulator

    def burst(self, rng, n, x=0.0, y=0.0, speed=120.0):
        """Spawn n particles at once, flying out in random directions."""
        for _ in range(n):
            a = rng.uniform(0, 2 * math.pi)
            v = rng.uniform(0.5, 1.0) * speed
            self.particles.append({"x": x, "y": y, "vx": v * math.cos(a),
                                   "vy": v * math.sin(a), "age": 0.0})

    def update(self, dt, rng):
        # 1. Emit. TODO (step 5): add rate * dt to self.to_emit, then call
        #    self.burst(rng, 1) once for every whole particle owed, and keep
        #    the fraction. The line below emits one per frame, whatever the rate.
        self.burst(rng, 1)
        # 2. Move and age every particle.
        for p in self.particles:
            p["vy"] += self.gravity * dt
            p["x"] += p["vx"] * dt
            p["y"] += p["vy"] * dt
            p["age"] += dt
        # 3. TODO (step 6): remove particles whose age >= lifetime.
        #    Build a new list; do not remove items from a list while looping over it.


# ------------------------------------------------------------------ demo ---
def timeline(fps=60, hits=((0.0, 0.5),), seconds=0.8, step=0.1):
    """Return rows (t, trauma, shake, dx) sampled every `step` seconds."""
    tr = Trauma()
    rows, frame, dt = [], 0, 1 / fps
    pending = sorted(hits)
    t = 0.0
    next_sample = 0.0
    while t <= seconds + 1e-9:
        while pending and pending[0][0] <= t + 1e-9:
            tr.add(pending.pop(0)[1])
        if t + 1e-9 >= next_sample:
            dx, _ = shake_offset(tr, t)
            rows.append((round(t, 3), tr.value, tr.shake(), dx))
            next_sample += step
        tr.update(dt)
        frame += 1
        t = frame * dt
    return rows


def main():
    print("One hit of 0.5 trauma at t=0, 60 fps, decay 0.8/s, power 2, 16 px max")
    print(f"{'t (s)':>6}{'trauma':>9}{'shake':>8}{'dx (px)':>9}")
    for t, v, s, dx in timeline():
        print(f"{t:>6.2f}{v:>9.3f}{s:>8.4f}{dx:>9.2f}")
    rng = random.Random(4)
    em = Emitter(rate=60, lifetime=1.5)
    for _ in range(5 * 60):
        em.update(1 / 60, rng)
    print(f"\nEmitter rate 60/s, lifetime 1.5 s, after 5 s: {len(em.particles)} alive "
          f"(model says rate x lifetime = {60 * 1.5:.0f})")


if __name__ == "__main__":
    main()
