"""CS101 Lab 09: one game, every frame rate.

Standard-library Python 3.10+. Run the tests with:  python test_lab09.py

Part A (read, do not edit): BrokenGame, a tiny game update written by someone
who tested only at 60 fps. It has four frame-rate bugs.
Part B (you write): FixedGame, the same game made frame-rate independent,
plus the accumulator loop and two runners.
Part C (you run): prints a comparison table across frame rates.
"""

FRAME_RATES = (30, 60, 144, 240)
SIM_DT = 1 / 60

# ---------------------------------------------------------------- Part A ---

class BrokenGame:
    """Tuned at 60 fps. Every commented number was 'correct' there."""

    def __init__(self):
        self.x = 0.0            # player position, px
        self.slide = 600.0      # knock-back speed that should fade out, px/s
        self.slide_x = 0.0      # distance travelled by the knock-back, px
        self.cooldown = 90      # dash cooldown: 90 frames = 1.5 s at 60 fps
        self.dashes = 0         # how many dashes happened
        self.y = 0.0            # jump height, px
        self.vy = 400.0         # jump starts upward at 400 px/s
        self.apex = 0.0

    def update(self, dt):
        self.x += 5                             # meant: 300 px/s
        self.slide_x += self.slide * dt
        self.slide *= 0.9                       # meant: lose 10% per 1/60 s
        self.cooldown -= 1                      # meant: 1.5 seconds
        if self.cooldown <= 0:
            self.dashes += 1
            self.cooldown = 90
        self.vy -= 1000 * dt                    # gravity 1000 px/s^2
        self.y += self.vy * dt
        self.apex = max(self.apex, self.y)


# ---------------------------------------------------------------- Part B ---

class FixedGame(BrokenGame):
    """Same fields and same intended behaviour, frame-rate independent.
    Hint: store the cooldown in seconds; use a power for the damping."""

    def __init__(self):
        super().__init__()
        # change what you need here (for example the cooldown's unit)

    def update(self, dt):
        raise NotImplementedError


def run_variable(game, fps, seconds):
    """Call game.update(1 / fps) once per frame for round(fps * seconds)
    frames. Return the game."""
    raise NotImplementedError


def accumulate(frame_times, sim_dt=SIM_DT, max_frame=0.25):
    """Fiedler's accumulator without the game: for each frame time, clamp it
    to max_frame, add it to the accumulator, then count how many whole sim_dt
    steps fit (subtracting each). Return a list of (steps, leftover_seconds,
    alpha) per frame. Compare with `acc >= sim_dt - 1e-9` so exact multiples
    are not lost to floating-point rounding."""
    raise NotImplementedError


def run_fixed(game, fps, seconds, sim_dt=SIM_DT):
    """Drive game.update(sim_dt) from display frames of 1 / fps, using the
    same accumulator logic as accumulate(). Return the game."""
    raise NotImplementedError


# ---------------------------------------------------------------- Part C ---

if __name__ == "__main__":
    print("fps  | broken x  slide_x  dashes  apex   | fixed(var) x  slide_x  dashes  apex  | fixed(step) apex")
    for fps in FRAME_RATES:
        b = BrokenGame()
        for _ in range(round(fps * 3)):
            b.update(1 / fps)
        f = run_variable(FixedGame(), fps, 3)
        s = run_fixed(FixedGame(), fps, 3)
        print(f"{fps:4d} | {b.x:8.1f} {b.slide_x:7.1f} {b.dashes:6d} {b.apex:6.2f} |"
              f" {f.x:11.1f} {f.slide_x:8.1f} {f.dashes:6d} {f.apex:6.2f} | {s.apex:6.2f}")
