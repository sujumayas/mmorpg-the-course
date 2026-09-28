"""MMO302 lab 09: login queue and session tickets.

Time for the queue is in whole minutes; time for tickets is in whole seconds.
Standard library only. Run the tests with:  python -m unittest test_login_service.py
"""
import hashlib
import hmac
import secrets


class World:
    """A capped world with a login queue, simulated one minute at a time.

    Counts are floats because logouts are an average (online / L per minute),
    exactly as in the lecture's model.
    """

    def __init__(self, cap, session_min, online=None, abandon_min=None):
        self.cap = cap
        self.session_min = session_min
        self.online = cap if online is None else online
        self.queue = 0.0            # ordinary queue
        self.priority = 0.0         # reconnecting players inside the grace period
        self.abandon_min = abandon_min   # mean patience in minutes, or None

    def arrive(self, n):
        self.queue += n

    def reconnect(self, n):
        """Players who were disconnected less than the grace period ago."""
        self.priority += n

    def step(self):
        """Advance one minute. Returns the number admitted this minute."""
        # TODO 1: (a) a fraction 1/session_min of online players log out;
        # (b) fill free slots from self.priority first, then self.queue;
        # (c) if abandon_min is set, a fraction 1/abandon_min of the ordinary
        # queue gives up (after admission). Return the total admitted.
        raise NotImplementedError("TODO 1")


def estimate_wait(position, cap, session_min):
    """Minutes until `position` is admitted at a full world (lecture formula)."""
    # TODO 2
    raise NotImplementedError("TODO 2")


class TicketService:
    """Signed, short-lived, single-use session tickets."""

    def __init__(self, secret, ttl=60):
        self.secret = secret
        self.ttl = ttl
        self.used = {}              # ticket id -> expiry time, for replay protection

    def _tag(self, body):
        return hmac.new(self.secret, body.encode(), hashlib.sha256).hexdigest()[:32]

    def issue(self, account_id, world, now, ticket_id=None):
        """Provided. ticket_id is random unless a test fixes it."""
        tid = ticket_id or secrets.token_hex(8)
        body = f"{tid}|{account_id}|{world}|{now + self.ttl}"
        return f"{body}|{self._tag(body)}"

    def verify(self, ticket, world, now):
        """Return "accept <account>" or "reject: <reason>" where reason is one
        of malformed, forged, wrong world, expired, replayed."""
        # TODO 3: split into 5 fields (else malformed); constant-time tag check
        # (forged); world must match; now must not be past expiry; the ticket
        # id must not have been accepted before (replayed). Remember accepted
        # ids until they expire, and forget expired ones so memory stays small.
        raise NotImplementedError("TODO 3")


def evening(cap=3000, session_min=120, peak=45, peak_min=180, later=10, minutes=480):
    """The lecture's evening, using your World. Provided."""
    w = World(cap, session_min)
    log = []
    for t in range(minutes):
        w.arrive(peak if t < peak_min else later)
        w.step()
        log.append(round(w.queue))
    return log


if __name__ == "__main__":
    try:
        log = evening()
        print("queue at 0, 60, 120, 180:", [log[t] for t in (0, 60, 120, 180)])
        print("position 1,500 waits", estimate_wait(1500, 3000, 120), "min")
    except NotImplementedError as e:
        print(f"not run yet: {e} is still a stub. Fill in the TODOs, then run the tests.")
