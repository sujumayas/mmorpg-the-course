"""GD201 Lab 06: open-field, chokepoint and multi-lane fight simulator. Standard library only.

Model (lecture week 6, sections 2 to 4):
  kill rate          a = 1 / time-to-kill           (kills per second per fighter)
  open field         attackers win if a A^2 > b D^2; survivors sqrt(A^2 - (b/a) D^2)
  chokepoint         only min(A, w) attackers fire; all D defenders fire
  closed form        attacker losses = b D^2 / (2 a w), fall time T = D / (a w)
  cover              the attacker's kill rate is multiplied by c = (aim - defense) / aim
  splash             the defender's kill rate at a choke is multiplied by k targets per hit

Fighter counts may be fractional (read 2.5 as "two fighters and half of a third one's health").

Fill in the TODOs, then run `python check_lab06.py`. Run `python choke_sim.py` for a report.
"""
import math

DT = 0.001  # seconds per tick


def kill_rate(time_to_kill):
    """Kills per second for one fighter with the given average time-to-kill in seconds."""
    # TODO
    raise NotImplementedError("kill_rate")


def square_law(attackers, defenders, a, b):
    """Open-field result. Return ("attackers", survivors) or ("defenders", survivors).
    On an exact tie return ("draw", 0.0)."""
    # TODO: compare a A^2 with b D^2.
    raise NotImplementedError("square_law")


def choke_losses(defenders, a, b, width):
    """Closed-form attacker losses to clear a chokepoint of the given width."""
    # TODO
    raise NotImplementedError("choke_losses")


def fall_time(defenders, a, width):
    """Seconds for `defenders` to fall at a chokepoint while it stays full of attackers."""
    # TODO
    raise NotImplementedError("fall_time")


def fight(attackers, defenders, a, b, width=None, dt=DT):
    """Tick simulation. width=None means open field. Each tick:
         firing = attackers (open field) or min(attackers, width)
         attackers -= b x defenders x dt
         defenders -= a x firing x dt      (both updates use the values from the start of the tick)
    Stop when either side is at or below zero. Return (attackers_left, defenders_left, seconds),
    with negative counts clamped to 0.0."""
    # TODO
    raise NotImplementedError("fight")


def cover_factor(aim, defense):
    """Multiplier on the attacker's kill rate from a hit chance of aim - defense (percent points).
    Never below 0."""
    # TODO
    raise NotImplementedError("cover_factor")


def weakest_lane(split, a, width, rotation_time):
    """Defenders are split across lanes (a list of counts), each lane with the same width.
    The attackers hit the lane with the fewest defenders (the first one on a tie).
    Return (lane_index, fall_time_of_that_lane, holds) where holds is True when the lane's
    fall time is at least the rotation time (help arrives in time)."""
    # TODO
    raise NotImplementedError("weakest_lane")


def report():
    a = b = kill_rate(10)
    print("open field 30 v 10:", square_law(30, 10, a, b))
    for w in (1, 2, 4, 10):
        left = fight(30, 10, a, b, width=w)
        print(f"  w = {w:>2}: formula loses {choke_losses(10, a, b, w):5.1f}; sim leaves "
              f"{left[0]:5.2f} attackers, {left[1]:4.2f} defenders after {left[2]:5.1f} s")
    print("three lanes 4/3/3, w = 2, rotation 20 s:", weakest_lane([4, 3, 3], a, 2, 20))


if __name__ == "__main__":
    try:
        report()
    except NotImplementedError as e:
        print(f"Not finished yet: {e} is still a TODO. Run check_lab to see what passes.")
