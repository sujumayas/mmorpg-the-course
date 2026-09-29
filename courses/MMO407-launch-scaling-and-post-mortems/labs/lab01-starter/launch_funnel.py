"""MMO407 lab 01: launch funnel and readiness review.

All rates are players (or attempts) per minute. Standard library only.
Run the tests from inside lab01-starter/ with:  python -m unittest test_launch_funnel.py
"""

# The lecture's section 2 pipeline, in order. Invented teaching values.
LECTURE_STAGES = {"patch check": 5000, "authentication": 600,
                  "character select": 1500, "world entry": 900}
LECTURE_ARRIVALS = 1000
LECTURE_PLANS = {"as built": {},
                 "2x character select": {"character select": 3000},
                 "2x authentication": {"authentication": 1200},
                 "2x auth + 2x world entry": {"authentication": 1200, "world entry": 1800}}


def throughput(stages, arrivals):
    """Return (narrowest stage name, throughput X) for a serial pipeline.

    X = min(arrivals, every stage capacity). The narrowest stage is the one
    with the smallest capacity, even when arrivals are lower still.
    """
    # TODO 1: return (name of the smallest-capacity stage, min(arrivals, its capacity))
    raise NotImplementedError("TODO 1")


def backlog(stages, arrivals, minutes):
    """Players who arrived but did not get through after `minutes`."""
    _, x = throughput(stages, arrivals)
    return max(0, arrivals - x) * minutes


def simulate_retries(capacity, arrivals, minutes, retry_s=30, reject_cost=0.1):
    """Minute-by-minute successes at a stage that rejects instead of queuing.

    Every rejected player retries every `retry_s` seconds until admitted.
    A success costs 1 unit of the stage's `capacity`; a rejection costs
    `reject_cost` units. Solve successes + reject_cost * rejections = capacity.
    Returns a list of (attempts, successes) per minute, starting at minute 1.
    """
    # TODO 2: loop over minutes; attempts = arrivals + waiting * 60 / retry_s; solve for successes, clamp to [0, attempts]; waiting grows by arrivals - successes
    raise NotImplementedError("TODO 2")


def availability(avails):
    """Chance that every required service is up: the product of availabilities."""
    # TODO 3: multiply the availabilities together
    raise NotImplementedError("TODO 3")


def apply_kill_switches(avails, switched_off):
    """Availabilities of the services a player still needs after the named
    optional services are put behind kill switches (they no longer block login)."""
    return {name: a for name, a in avails.items() if name not in switched_off}


def print_lecture_table():
    for label, change in LECTURE_PLANS.items():
        s = {**LECTURE_STAGES, **change}
        name, x = throughput(s, LECTURE_ARRIVALS)
        print(f"{label:26} narrowest {name:16} through {x:5}/min "
              f"waiting after 60 min {backlog(s, LECTURE_ARRIVALS, 60):6,}")


if __name__ == "__main__":
    try:
        print_lecture_table()
    except NotImplementedError as e:
        print(f"{e} is not done yet. Run the tests to see what is missing.")
