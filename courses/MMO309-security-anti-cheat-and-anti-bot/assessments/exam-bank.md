# MMO309 · Exam bank: quiz, practice and viva questions

MMO309 has no written exam. The grade comes from the [threat model](threat-model-brief.md) (30%), the [labs](labs-brief.md) (30%) and the [final detection prototype](final-prototype-brief.md) (40%). This bank has three other jobs.

- **Practice.** Work a week's questions before its lab is due. If you can answer them with the lecture closed, the lab will go quickly.
- **Lab quizzes.** Each lab session opens with a 10-minute ungraded quiz of two or three questions from this bank. Usually one applies a lecture model to new numbers or traces code, and one asks you to explain or critique.
- **Viva.** The lab spot checks and the week 15 prototype viva ask questions in this style, rewritten with the numbers from your own threat model and your own detector.

Every question is tagged with the week or weeks it draws on and one type.

- **compute**: apply a lecture model (loss ledger, leak, tolerance, Poisson flags, dupe odds, ban delay, break-even lifetime, precision, trade hold, posterior odds, bounty) to values you have not seen before.
- **code**: say what a piece of Python prints or does.
- **explain**: say why something behaves as it does, with a number or a trace as evidence.
- **design**: choose a technique or setting for a stated situation and justify it.
- **critique**: find what is wrong with a piece of code or a proposal and say how to fix it.

All numbers are invented unless a question names a game. Every game fact used here comes from the lecture of the tagged week, which cites its source and version. Every code snippet runs as shown with Python 3.13 (`.venv/bin/python`), and every number was recomputed in Python from the lecture's own model. Write your own answer before you open the solution.

---

## Week 1: Threat modeling for games

1. *Week 1 · compute.* Two threats are proposed for the section 2 loss ledger. A guild officer empties the guild chest and quits about 150 times a year, at about $900 of cleanup and refunds each time. An auction-house sniping bot causes about 50 incidents a year at $1,500 each. Compute each ALE. Where would each rank if it were added on its own to the original eight-row ledger?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Guild chest theft $135,000, rank 3. Sniping bot $75,000, rank 5.

`ALE = f × I`. Guild chest: `150 × 900 = 135,000`. That sits below duplication ($300,000) and bots ($160,000) and above DDoS ($90,000), so it ranks third. Sniping bot: `50 × 1,500 = 75,000`. That is below the stolen GM session ($80,000) and above account takeover ($72,000), so it ranks fifth.

The guild chest threat is also worth a second look in STRIDE terms. Nothing is spoofed or tampered with. The officer uses a permission the design gave them, which makes it a design exploit, one of the three families STRIDE misses.
</details>

2. *Week 1 · compute.* The team replaces the optional authenticator (C2) with a mandatory one for all 200,000 players. It stops 90% of takeovers on every account, so `r = 0.9` against T1's ALE of $72,000. It costs $50,000 to build and $30,000 a year in extra support. The team expects 1% of players to quit over the friction, at $10 a month.
   (a) What is its first-year net value?
   (b) In year 2 the build cost is gone and support continues. How many players a year can quit before the control stops paying?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) −$255,200. (b) At most 290 players a year, about 0.15% of the base.

(a) Saved `0.9 × 72,000 = 64,800`. `B = 50,000 + 30,000 = 80,000`. `P = 2,000 × 120 = 240,000`. Net `64,800 − 80,000 − 240,000 = −255,200`.

(b) Year 2 net is `64,800 − 30,000 − P`. It stays positive while `P ≤ 34,800`, which is `34,800 / 120 = 290` players. Compare C2 in the lecture: making the control mandatory raised `r` from 0.36 to 0.9, and the player cost term swallowed the gain. Almost every argument about a restrictive control is an argument about `P`.
</details>

3. *Week 1 · code.* The ledger team keeps a high and a low estimate of ALE. What does this print, and what should the team do next according to the lecture's design judgment?

```python
ale = {"T1": 72_000, "T2": 300_000, "T5": 160_000, "T6": 90_000, "T7": 80_000}
low = {"T1": 40_000, "T2": 30_000, "T5": 120_000, "T6": 75_000, "T7": 20_000}

def top(table, n):
    return set(sorted(table, key=table.get, reverse=True)[:n])

print(sorted(top(ale, 3) & top(low, 3)))
print(sorted(top(ale, 3) ^ top(low, 3)))
print(next(n for n in range(1, 6) if {"T2", "T5"} <= top(ale, n) & top(low, n)))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
['T5', 'T6']
['T1', 'T2']
4
```

The high estimates rank T2, T5, T6, T7, T1. The low estimates rank T5, T6, T1, T2, T7. Both top threes contain T5 and T6. T2 is in the first only and T1 in the second only, so the symmetric difference is `['T1', 'T2']`. T2 and T5 are both in both top-`n` sets first at `n = 4`.

The top three changed between estimates, and the change comes from T2's cost per incident ($150,000 against $15,000). The lecture's rule says that when the ranking swaps, that one estimate is worth a day of research. Look at past dupe incidents, the price moves they caused and the rollback labor, before arguing further.
</details>

4. *Week 1 · compute.* A cheat seller charges $10 a month. Your detection bans 20% of its users each month, and a banned user loses an account worth $25 to them. The seller launches an "Elite" tier for $5 more a month that halves the detection rate.
   (a) What is a regular user's expected monthly cost of cheating? An Elite user's?
   (b) For what account value does Elite become worth buying?
   (c) Which of the attacker-side levers from section 4 does Elite attack?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) $15.00 and $17.50. (b) Accounts worth more than $50. (c) The expected penalty.

(a) Regular: `10 + 0.2 × 25 = 15`. Elite: `10 + 5 + 0.1 × 25 = 17.50`.

(b) Elite saves `0.1 × V` in expected penalty for $5, so it pays when `0.1 × V > 5`, that is `V > 50`.

(c) The attacker keeps attacking while value exceeds cost plus expected penalty. Elite lowers the chance of detection, which lowers the expected penalty. This is Glider Elite from the lecture. The seller turned your detection rate into its own revenue line. The defender's answer is to raise the loss on detection (confiscate more than the account) or move to the value and cost levers, not only to push detection harder.
</details>

5. *Week 1 · explain.* Classify each threat with one STRIDE letter, or say that it belongs to one of the three game families STRIDE misses. (a) A client replays a captured "claim daily reward" message ten times. (b) A farming bot sends only inputs a human could send. (c) A caller talks a support agent into moving an account to a new email. (d) A GM says they never spawned 40 rare mounts, and there is no log. (e) One malformed packet crashes a zone server.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Tampering (a changed or replayed message the server should reject). (b) Automation of legitimate play, no STRIDE letter. (c) A social attack, which you can also file under Spoofing, since the caller pretends to be the owner. (d) Repudiation. (e) Denial of service.

The point of (b) and (c) is the lecture's fourth question for games: what can a player do, with no hacking, that pays? A request ID on the reward message (week 2) closes (a). A log with server timestamps closes (d) for the price of storage.
</details>

## Week 2: Never trust the client

6. *Week 2 · compute.* A shooter runs a 60-tick server with a fixed look-ahead `τ = 40 ms`. Each enemy peeks 5 times a round.
   (a) For a player with 90 ms ping, what is `τ_min` and the pop-in?
   (b) What does each enemy leak per round at `τ = 40 ms`, and under an adaptive `τ = τ_min + 20`?
   (c) A cheater adds 200 ms of fake latency under the adaptive rule. What does each enemy now leak per round?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `τ_min ≈ 61.7 ms`, pop-in `≈ 21.7 ms`. (b) 0.20 s fixed, about 0.41 s adaptive. (c) About 0.91 s.

(a) `T = 1000 / 60 = 16.7 ms`. `τ_min = 90 / 2 + 16.7 = 61.7 ms`. Pop-in is `61.7 − 40 = 21.7 ms`.

(b) Fixed: `5 × 0.040 = 0.20 s`. Adaptive: `τ = 81.7 ms`, leak `5 × 0.0817 = 0.41 s`.

(c) Ping 290 ms gives `τ_min = 145 + 16.7 = 161.7 ms`, adaptive `τ = 181.7 ms`, leak `5 × 0.1817 = 0.91 s`. That is why the lecture says to cap `τ`. An adaptive look-ahead pays cheaters for lag they create.
</details>

7. *Week 2 · compute.* One enemy, one 90-second round. The enemy is visible for 4 s in total over 6 peeks, is within the 60 m area of interest for 30 s, and stands in PVS "could be visible" cells for 8 s. Rank the four policies of section 2 by leak per round, with `τ = 50 ms` for exact line of sight.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Send everything 86 s, AOI 26 s, PVS 4 s, line of sight with look-ahead 0.30 s.

Leak is time sent minus time visible. `90 − 4 = 86`, `30 − 4 = 26`, `8 − 4 = 4`, and `6 × 0.05 = 0.30`. Each step down the list costs more server work per pair of players. The PVS row is the one VALORANT's design built on, with the look-ahead added.
</details>

8. *Week 2 · compute.* An exact line-of-sight test costs 2 µs per ordered pair (the lecture's assumed figure). How much CPU per second does exact visibility need for (a) a 60-player battleground at 20 ticks per second, and (b) a 300-player city at 10 ticks per second? What does (b) tell you about where exact tests belong?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 70,800 pair checks per second, 0.14 CPU-seconds per second. (b) 897,000 checks per second, about 1.8 CPU-seconds per second, nearly two cores.

(a) `60 × 59 × 20 = 70,800`, times 2 µs is 0.1416 s. (b) `300 × 299 × 10 = 897,000`, times 2 µs is 1.794 s.

Pair counts grow with the square of the crowd, so a city pays about 13 times the battleground's cost for five times the players. Cities get cheap tests (distance, grid, PVS). Exact tests go where hidden information decides fights, such as PvP zones.
</details>

9. *Week 2 · code.* What does this print? What does the second number mean for the penalty you apply when the check fires?

```python
def p_caught(p, n):
    return 1 - (1 - p) ** n

p = next(x / 10_000 for x in range(1, 10_000) if p_caught(x / 10_000, 150) >= 0.95)
print(p, round(1_500 / p))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** `0.0198 75758`

The loop finds the smallest sampling rate, in steps of 0.0001, that catches an attacker who performs 150 bad actions with at least 95% probability. The exact value is `1 − 0.05^(1/150) = 0.01977`, which rounds up to 0.0198 on the grid.

The second number is `g / p` with `g = 1,500` gold per action. It is the gold an attacker expects to take before the first check fires. Your penalty on a catch must take back at least that much (all the exploit's proceeds, usually the account), or the exploit still pays on average even at a 95% catch rate over 150 uses.
</details>

## Week 3: Speed hacks and movement validation

10. *Week 3 · compute.* A server ticks at 25 Hz (`T = 40 ms`) and the legal speed is 5 m/s. The team wants to forgive 300 ms lag spikes.
    (a) What rate-check tolerance does that need, and what speed does it give a cheater for free?
    (b) What is the largest single jump under a credit check with `L = 300 ms`?
    (c) The team picks `L = 200 ms` instead. How far is an honest player pulled back after a 350 ms spike?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `tol = 7.5`, so 750%, and a cheater runs at 42.5 m/s. (b) 1.7 m. (c) 0.75 m.

(a) `tol = J / T = 300 / 40 = 7.5`. Free speed `5 × (1 + 7.5) = 42.5 m/s`, on every tick, forever.

(b) `v × (T + L) = 5 × 0.34 = 1.7 m`, once per gap.

(c) `v × (J − L) = 5 × 0.15 = 0.75 m`. That rubber-band is also one violation of false evidence against an honest player, which feeds the detection problem in section 4.
</details>

11. *Week 3 · code.* Use the lecture's section 2 `run` function unchanged (same `TICK_MS = 50`, `SPEED = 6.0`, `LATENCY_MS = 40`). Predict what these three lines print, then explain the pattern.

```python
v, m = run(150, "credit", 100)
print(f"credit L=100: {v} violation(s), pulled back {m:.2f} m")
v, m = run(150, "rate", 2.0)
print(f"rate tol=200%: {v} violation(s), pulled back {m:.2f} m")
v, m = run(150, "rate", 3.0)
print(f"rate tol=300%: {v} violation(s), pulled back {m:.2f} m")
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
credit L=100: 1 violation(s), pulled back 0.30 m
rate tol=200%: 1 violation(s), pulled back 0.30 m
rate tol=300%: 0 violation(s), pulled back 0.00 m
```

A 150 ms spike holds three packets. They arrive with the next one, so one tick sees four steps, 1.2 m. The credit check allows `6 × min(200, 50 + 100) / 1000 = 0.9 m`, so it clamps once and pulls back 0.3 m. The rate check at 200% also allows `0.3 × 3 = 0.9 m`, the same clamp. At 300% the rate check allows 1.2 m and passes.

Both checks need the same setting to forgive this spike (`L ≥ 150 ms` or `tol ≥ J / T = 3`). They give away different things. The credit check at `L = 150` allows one jump of 1.2 m. The rate check at 300% lets a cheater run at 24 m/s all day.
</details>

12. *Week 3 · compute.* Apply the section 4 model with `L = 200 ms`. Honest players have 6 spikes per session with mean length 100 ms, and blink cheaters average 4 violations per session. There are 50,000 sessions a day and 1% are cheating. Compute the false-positive rate, recall, innocent flags, cheaters caught and precision for "flag at `k` or more violations in one session", for `k = 3` and `k = 4`.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

| `k` | FPR | Recall | Innocent flags | Cheaters caught | Precision |
|---|---|---|---|---|---|
| 3 | 0.0492 | 0.762 | 2,434 | 381 | 13.5% |
| 4 | 0.0095 | 0.567 | 473 | 283 | 37.5% |

`λ_h = 6 × e^(−200/100) = 0.812` and `λ_c = 4`. With `P(Poisson(λ) ≥ k)` from the lecture's `p_at_least`, the FPR is 0.0492 at `k = 3`, times 49,500 honest sessions gives 2,434. Recall `0.762 × 500 = 381`. Precision `381 / (381 + 2,434) = 13.5%`.

Compare the lecture's `L = 250 ms`. A lower `L` roughly doubles honest violations (0.81 against 0.49 per session), and this cheater blinks less often, so single-session rules are far worse. The fix is the next question, more sessions of evidence.
</details>

13. *Week 3 · code.* This extends question 12 to a week of evidence. What does it print, and what does waiting for the week cost?

```python
from math import exp, factorial

def p_at_least(k, lam):
    return 1 - sum(exp(-lam) * lam ** i / factorial(i) for i in range(k))

honest, cheaters = 49_500, 500
lam_h = 7 * 6 * exp(-200 / 100)    # 7 sessions, L = 200 ms
lam_c = 7 * 4                      # 7 sessions of a 4-blink cheater
k = next(k for k in range(1, 60) if honest * p_at_least(k, lam_h) < 1)
tp = cheaters * p_at_least(k, lam_c)
fp = honest * p_at_least(k, lam_h)
print(f"weekly honest mean {lam_h:.2f}, smallest k with under 1 innocent flag: {k}")
print(f"innocents {fp:.2f}, cheaters caught {tp:.1f}, precision {tp / (tp + fp):.2%}")
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
weekly honest mean 5.68, smallest k with under 1 innocent flag: 19
innocents 0.42, cheaters caught 485.0, precision 99.91%
```

Honest players average `7 × 0.812 = 5.68` violations a week and cheaters 28. Honest spikes are random from session to session while a cheater cheats again tomorrow, so the gap between the two distributions widens as you add sessions. At `k = 19` the expected innocent flags drop to 0.42 while 97% of cheaters are still caught.

The cost is a week of cheating before the verdict. The lecture's answer is to clamp every bad claim at once (prevention needs no verdict) and to decide on the account later. How long to wait before banning, and whether to ban in a wave, is week 5's model.
</details>

14. *Week 3 · compute.* A movement anomaly detector flags 1.5% of honest sessions and 85% of cheating sessions. The base rate is 0.3%. What share of flagged sessions are cheating? Should the flag trigger an automatic ban?

<details>
<summary>Answer and worked solution</summary>

**Answer:** About 14.6%. No.

Per 100,000 sessions there are 300 cheaters and 99,700 honest. Flags: `0.85 × 300 = 255` cheaters and `0.015 × 99,700 = 1,495.5` honest. Precision `255 / 1,750.5 = 14.6%`. Six of every seven flags are innocent. This flag can feed a more expensive check or a human reviewer, the pipeline design from the end of section 4, but never an automatic ban.
</details>

## Week 4: Duplication exploits and transactional design

15. *Week 4 · compute.* A naive mail handler has an unsafe window of `w = 30 ms` between its two writes. The shard processes 15 mail transfers a second. An attacker can force a failure with timing jitter `J = 150 ms`.
    (a) How many dupes does one accidental crash cause on average?
    (b) What is the attacker's chance per try, within 10 tries, and how many tries give at least 95%?
    (c) Under load `w` rises to 90 ms. What is the chance per try now?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 0.45. (b) 0.2 per try, 89.3% within 10 tries, 14 tries for 95%. (c) 0.6.

(a) `λ × w = 15 × 0.030 = 0.45`.

(b) `p = 30 / 150 = 0.2`. `1 − 0.8^10 = 0.893`. For 95%, the smallest `k` with `0.8^k ≤ 0.05` is `ceil(ln 0.05 / ln 0.8) = ceil(13.4) = 14`. The mean is `1 / 0.2 = 5` tries.

(c) `90 / 150 = 0.6`. The window is your database latency, and it widens exactly when the server is busy.
</details>

16. *Week 4 · code.* A vendor handler is written naively, paying before it takes the item. The client retries once with no reply. What does this print? Classify each row as correct, dupe, loss or double-execution, and say what the player sees in row 3.

```python
import sqlite3

class Crash(Exception):
    pass

def world():
    db = sqlite3.connect(":memory:", isolation_level=None)   # every statement commits
    db.execute("CREATE TABLE bag (who TEXT PRIMARY KEY, swords INTEGER, gold INTEGER)")
    db.execute("INSERT INTO bag VALUES ('cy', 1, 0)")
    return db

def sell_sword(db, crash_at):
    """Vendor buys one sword for 500 gold. Written naively: pay first, then take."""
    swords = db.execute("SELECT swords FROM bag WHERE who='cy'").fetchone()[0]
    if swords < 1:
        return "no sword"
    if crash_at == 1: raise Crash
    db.execute("UPDATE bag SET gold = gold + 500 WHERE who='cy'")
    if crash_at == 2: raise Crash
    db.execute("UPDATE bag SET swords = swords - 1 WHERE who='cy'")
    if crash_at == 3: raise Crash
    return "sold"

for k in (1, 2, 3):
    db = world()
    try:
        sell_sword(db, k)
    except Crash:
        reply = sell_sword(db, 0)              # client saw no reply, so it retries
    print(k, db.execute("SELECT swords, gold FROM bag").fetchone(), reply)
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
1 (0, 500) sold
2 (0, 1000) sold
3 (0, 500) no sword
```

Row 1 is correct. Nothing was written before the crash, and the retry sells once. Row 2 is a dupe of +500 gold. The gold was paid, the sword was never taken, and the retry sees the sword still there and pays again. Row 3 has the correct end state, but the retry is judged against the new state and the player sees "no sword" for a sale that went through.

Swapping the order (take, then pay) would turn row 2 into a loss, a sword gone with no gold, which a log can repair. That is the lecture's "take before give" rule for cases with no shared transaction. Here there is one database, so the fix is one transaction with a conditional `swords = swords - 1 WHERE swords >= 1` and an idempotency key stored in the same commit.
</details>

17. *Week 4 · compute.* A game has 45 value paths, each with a 1.5% chance of shipping a dupe in a release. What is the chance a release ships at least one? The team moves every path onto one audited transfer primitive, leaving 0.4% risk in each path's glue and 1% in the primitive once. What is it now?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 49.3% before, 17.3% after.

`1 − 0.985^45 = 1 − 0.507 = 0.493`. With the primitive, `1 − 0.996^45 × 0.99 = 1 − 0.835 × 0.99 = 0.173`.

The rates are invented, the shape is the lesson. Glue can still be wrong, but it cannot create value, because only the primitive touches quantities.
</details>

18. *Week 4 · compute.* A dupe path has `p = w / J = 25 / 250`. Each attempt takes 12 seconds, and your conservation residual alert fires within 45 minutes. How many successful dupes do you expect before the alert with no rate limit? With a limit of one transfer per 2 minutes per account? What limit keeps the expectation at or below one success?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 22.5 without a limit, 2.25 with it. A limit of one transfer per 4.5 minutes or slower keeps it at or below one.

`p = 0.1`. Without a limit, `2,700 / 12 = 225` attempts give `22.5` successes. With the limit, `45 / 2 = 22.5` attempts give `2.25`. For at most one success you need at most 10 attempts in 45 minutes, one per 4.5 minutes. A limit does not fix the bug. It caps what the bug produces before the residual alert fires, and it costs honest players who move value often, so set it where values are large and legitimate use is rare.
</details>

19. *Week 4 · critique.* A teammate says the new reward-claim service "cannot dupe, because it uses transactions everywhere". The handler commits "grant 500 gold" in one transaction and "mark reward claimed" in a second transaction. Critique the claim and give the fix.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Two transactions are a split write. A failure between the commits leaves the gold granted and the reward unclaimed, and the client's retry grants again, a dupe of +500.

A transaction protects only the writes inside it. Put the grant and the mark in one transaction, write the mark as a conditional update (`SET claimed = 1 WHERE claimed = 0`) and check that exactly one row changed before granting, and store the request ID in the same commit so that a retry after a lost reply returns the stored answer. That is `keyed_send` applied to a reward.
</details>

## Week 5: Memory editing and client integrity

20. *Week 5 · compute.* Use the section 3 ban-delay model with `N = 8,000` users, `q = 0.4`, `R = 2` days and `S = 25` days. Compute `caught` and `sessions` for `W = 0`, `W = 2` and `W = 4`. The minimum is at `W = 3`. Compute that row too.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

| `W` | caught | sessions |
|---|---|---|
| 0 | 5,120 | 28,800 |
| 2 | 6,963 | 15,939 |
| 3 | 7,378 | 15,074 |
| 4 | 7,627 | 15,935 |

`W = 0`: `8,000 × (1 − 0.6²) = 5,120`, and the 2,880 missed users play `0.4 × 2,880 × 25 = 28,800` sessions. `W = 3`: `8,000 × (1 − 0.6⁵) = 7,378`, sessions `0.4 × 8,000 × 3 + 0.4 × 622 × 22 = 9,600 + 5,474 = 15,074`.

Instant bans leave almost twice the cheating of a three-day wait. The bottom of the curve is flat between 2 and 4 days, so an estimate of `q` that is a little off costs little, while a two-week wait would cost a lot.
</details>

21. *Week 5 · code.* Using the lecture's model, what does this print? Explain the second line in the model's terms.

```python
def one_signature(W, N=10_000, q=0.5, R=2, S=30):
    caught = N * (1 - (1 - q) ** (W + R))
    sessions = q * N * W + q * (N - caught) * (S - W)
    return caught, sessions

for q, R in [(0.3, 1), (0.3, 4), (0.7, 1)]:
    best = min(range(0, 21), key=lambda W: one_signature(W, q=q, R=R, S=20)[1])
    caught, sessions = one_signature(best, q=q, R=R, S=20)
    _, instant = one_signature(0, q=q, R=R, S=20)
    print(f"q={q} R={R}: best W={best}, sessions {sessions:,.0f} vs instant {instant:,.0f}")
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
q=0.3 R=1: best W=4, sessions 20,067 vs instant 42,000
q=0.3 R=4: best W=2, sessions 12,353 vs instant 14,406
q=0.7 R=1: best W=2, sessions 17,402 vs instant 42,000
```

The second line has a slow cheat maker (`R = 4`). Their reaction time already gives you four days of catching after the first ban, so an instant ban catches `1 − 0.7⁴ = 76%` of users, and waiting adds little. The best delay falls from 4 days to 2 and the gain over instant bans shrinks from about 22,000 sessions to about 2,000. A fast maker (`R = 1`) makes waiting worth much more, which is the lecture's check-yourself result from the other side.
</details>

22. *Week 5 · compute.* A game has 2,000,000 players and 0.5% cheat. An "unknown module in process" signal fires on 97% of cheaters and 0.3% of honest players, because overlays and recorders inject code too.
    (a) What is its precision?
    (b) You require it together with an independent behavioral anomaly that fires on 75% of cheaters and 1% of honest players. What are the combined recall, false positives and precision?
    (c) Name one honest group for which the independence assumption in (b) is likely to fail.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 61.9%. (b) Recall 72.75%, about 60 innocent flags, precision 99.2%. (c) Players using accessibility or input tools that both inject a module and change how their play looks.

(a) 10,000 cheaters and 1,990,000 honest. `0.97 × 10,000 = 9,700` against `0.003 × 1,990,000 = 5,970`. Precision `9,700 / 15,670 = 61.9%`.

(b) Recall `0.97 × 0.75 = 0.7275`, so 7,275 caught. FPR `0.003 × 0.01 = 0.00003`, so 59.7 innocents. Precision `7,275 / 7,334.7 = 99.2%`.

(c) If the same tool raises both signals for an honest player, the combined false-positive rate is higher than the product, and the 99.2% is an overestimate. The lecture's AMD driver and Modern Warfare 2 cases are both benign changes that moved a whole group's false-positive rate at once.
</details>

23. *Week 5 · explain.* Put each item in one of the three classes (tampered values, revealed information, automated input) and name the defense that fits. (a) A crafting minigame scored on the client. (b) A radar that draws players 100 m away through hills. (c) A fishing bot that reads the screen and sends OS mouse clicks. (d) A memory edit that zeroes the local cooldown timer when the server keeps its own cooldown clock.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Tampered values, fixed by moving scoring to the server or validating a sampled share of results there (week 2). (b) Revealed information, shrunk by sending less (area of interest, visibility checks). (c) Automated input, where only client integrity or behavioral detection can help, and a colour bot gives the client little to see, so behavioral features (week 7) carry the load. (d) Tampered values that win nothing. The server rejects early casts, so only the player's own screen changes.

The lecture's rule follows: spend client integrity on the automated-input class and server design on the other two.
</details>

## Week 6: Botting economics

24. *Week 6 · compute.* A bot farms 25,000 gold an hour for 18 hours a day. Gold sells for $1.20 per 100,000, running cost is $1.40 a day and setup is $30.
    (a) Compute revenue, margin `m` and the break-even lifetime.
    (b) Detection is `d = 0.15` a day and waves run every 10 days. What is the expected profit per account?
    (c) What wave interval makes the farm break even at this `d`? What `d` would you need with bans on detection?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) $5.40, $4.00, 7.5 days. (b) $16.67. (c) `W ≈ 1.7` days, or `d ≥ 0.133` with `W = 0`.

(a) `25,000 × 18 × 1.20 / 100,000 = 5.40`, `m = 5.40 − 1.40 = 4.00`, `A / m = 30 / 4 = 7.5`.

(b) `L = 1 / 0.15 + 10 / 2 = 6.67 + 5 = 11.67` days, profit `4 × 11.67 − 30 = 16.67`.

(c) Break-even needs `6.67 + W / 2 = 7.5`, so `W = 1.67` days. With `W = 0`, `1 / d = 7.5`, so `d = 0.133`. Ten-day waves add five days to every bot's life.
</details>

25. *Week 6 · compute.* A purge of the question 24 farms works, and the black-market gold price rises 40%. Recompute `m` and the break-even lifetime. A defense of `d = 0.15` with bans on detection closed the old farm. Does it close the new one?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `m = $6.16`, break-even 4.9 days. No, profit is now +$11.07 per account.

Price `1.20 × 1.4 = 1.68`. Revenue `25,000 × 18 × 1.68 / 100,000 = 7.56`, `m = 6.16`, `A / m = 30 / 6.16 = 4.87` days. With `W = 0`, `L = 6.67` days. Before the purge the profit was `4 × 6.67 − 30 = −3.33`. After it, `6.16 × 6.67 − 30 = +11.07`.

A successful purge raises the price and invites the next generation of bots. Anti-bot work is a level you hold. A token that caps the price (MMO304 week 11) keeps `m` from rising as far.
</details>

26. *Week 6 · code.* This reuses the section 3 hours model. What does it print? Explain the second and third lines.

```python
def profit_at_hours(H, d8=0.01, dollars_per_hour=0.30, run_cost=1.00, setup=35.0):
    d = d8 * (H / 8) ** 2
    return (dollars_per_hour * H - run_cost) * (1 / d) - setup

for d8, rate in [(0.01, 0.30), (0.01, 0.45), (0.04, 0.30)]:
    best = max(range(1, 25), key=lambda H: profit_at_hours(H, d8, rate))
    print(f"d8={d8} ${rate}/h: best H={best}, profit {profit_at_hours(best, d8, rate):.2f}")
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
d8=0.01 $0.3/h: best H=7, profit 108.67
d8=0.01 $0.45/h: best H=4, profit 285.00
d8=0.04 $0.3/h: best H=7, profit 0.92
```

The revenue term is `(r × H − c) × 64 / (d8 × H²)`. Its maximum sits where the derivative is zero, at `H = 2c / r`, which is 6.7 hours at $0.30 and 4.4 at $0.45. So when gold is worth more per hour, the operator throttles further, because each hour of cover is cheaper relative to what it earns. The faucet per bot shrinks while profit rises.

Quadrupling `d8` divides every lifetime by four. The best `H` does not move, but the revenue term falls to a quarter, `143.67 / 4 = 35.92`, and after the $35 setup the farm clears only $0.92. Detection that scales with hours pushed this farm to the edge without banning more bots per hour played.
</details>

27. *Week 6 · compute.* Start from question 24's farm (`d = 0.15`, `W = 10`, profit $16.67). Change one thing at a time: (a) setup cost doubles, (b) waves are replaced by bans on detection, (c) detection doubles to `d = 0.3` with 10-day waves kept. Which close the farm? What does (c) teach?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) −$13.33, closed. (b) −$3.33, closed. (c) +$3.33, still open.

(a) `4 × 11.67 − 60 = −13.33`. (b) `4 × 6.67 − 30 = −3.33`. (c) `L = 3.33 + 5 = 8.33`, `4 × 8.33 − 30 = +3.33`.

Doubling detection, the most expensive lever, fails here because the wave still gives every bot five extra days. Turning waves off is a policy change. For bots every day alive is income, so the week 5 argument for waiting points the other way.
</details>

## Week 7: Bot detection, behavioral features

28. *Week 7 · compute.* Predict CV for (a) a bot that waits 600 ms plus uniform jitter of ±150 ms, (b) a human with log-normal gaps of shape `s = 0.5`, (c) a human with `s = 0.8`. Which does the rule "flag if CV < 0.35" flag?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 0.144, flagged. (b) 0.533. (c) 0.947. Neither human is flagged.

(a) `j / (d × √3) = 150 / (600 × 1.732) = 0.144`. (b) `√(e^0.25 − 1) = √0.284 = 0.533`. (c) `√(e^0.64 − 1) = √0.896 = 0.947`. The median gap does not enter the human formula, so fast and slow players with the same shape score the same.
</details>

29. *Week 7 · compute.* A healer's gaps are a 1,000 ms global cooldown plus a log-normal reaction with median 250 ms and shape 0.6. Compute the slack CV, the slack mean and standard deviation, and the raw CV. What does the raw rule of question 28 do to this player?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Slack CV 0.658, slack mean about 299 ms, standard deviation about 197 ms, raw CV about 0.152. The raw rule flags this honest player.

Slack CV `√(e^0.36 − 1) = 0.658`. The log-normal mean is `median × e^(s²/2) = 250 × e^0.18 = 299` ms, so the standard deviation is `0.658 × 299 = 197` ms. The raw mean is `1,000 + 299 = 1,299` ms with the same spread, so raw CV is `197 / 1,299 = 0.152`. The cooldown inflated the mean and added nothing to the spread. Measure slack, and log which cooldown gated each action so you can.
</details>

30. *Week 7 · code.* What does this print? What does it say about self-similarity as a feature for fishing bots, and what would you add?

```python
import math
from itertools import combinations

def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))

def self_similarity(windows):
    pairs = list(combinations(windows, 2))
    return sum(cosine(a, b) for a, b in pairs) / len(pairs)

# [kills, loots, moves, chats, trades, crafts] per active hour
fisher = [[0, 30, 5, 2, 0, 0], [0, 28, 4, 0, 0, 0], [0, 31, 6, 1, 0, 0]]
fish_bot = [[0, 30, 5, 0, 0, 0], [0, 29, 5, 0, 0, 0], [0, 30, 4, 0, 0, 0]]
print(f"honest fisher {self_similarity(fisher):.4f}")
print(f"fishing bot   {self_similarity(fish_bot):.4f}")
print(f"cross pair    {cosine(fisher[0], [6, 4, 30, 45, 3, 0]):.4f}")
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
honest fisher 0.9983
fishing bot   0.9996
cross pair    0.2161
```

Within three fishing hours, the honest fisher and the bot are both near 1. Self-similarity cannot tell an honest repeater from a bot over a short window. It separates them only when the human drifts to other activities over days, as the third line hints (a fishing hour against a social hour scores 0.22).

Add a purpose feature. A fisher plays three hours and logs off, and a fishing bot plays twenty, so combine repetition with hours per day, as the lecture's third rule clause does (`self_similarity > 0.97 and hours_per_day > 5`).
</details>

31. *Week 7 · compute.* A bot that ran 22 hours a day is changed to play 9 hours a day "like a person". At 50,000 gold per hour, what share of its output does it keep, and how much gold a day does the operator give up? Using the NCSOFT Lineage figure that a bot needed at least 120 hours a month to pay for its account, does the throttled bot still pay?

<details>
<summary>Answer and worked solution</summary>

**Answer:** It keeps 40.9% of its output and gives up 650,000 gold a day. At 9 hours a day it runs about 270 hours a month, so it still pays for its account, with much less margin.

`9 / 22 = 0.409`. `13 × 50,000 = 650,000`. `9 × 30 = 270 > 120`. This is why hours are a purpose feature. The disguise is possible, but it costs the operator most of the income, and every throttled bot is a smaller faucet (the week 6 hours model makes the same point).
</details>

32. *Week 7 · design.* Rank these four features from cheapest to most expensive for a bot operator to fake, and say which you would build the system on: (a) share of reactions under 150 ms, (b) gold per hour against the zone's norm, (c) share of gold sent to a few collector accounts, (d) wobble in movement paths.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Cheapest (a) and (d), then (b), then (c). Build on (b) and (c) and use (a) and (d) as cheap early warnings.

(a) and (d) describe the bot's manner. A delay drawn from a human-shaped distribution or noise on waypoints costs a line of code and little output. (b) and (c) describe its purpose. Earning less per hour is the point of the disguise, and the gold has to reach a seller eventually, so hiding (c) needs extra layers of accounts. The lecture's catalog ranks these families the same way.
</details>

## Week 8: Machine learning for detection

33. *Week 8 · compute.* A detector has recall 92% and a false positive rate of 0.3%. It runs on 500,000 accounts at 4% prevalence. How many bots and humans does it flag, and what is its precision? After a ban wave, prevalence falls to 0.8% with the detector unchanged. Recompute.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Before, 18,400 bots and 1,440 humans, precision 92.7%. After, 3,680 bots and 1,488 humans, precision 71.2%.

Before, 20,000 bots and 480,000 humans. `0.92 × 20,000 = 18,400`, `0.003 × 480,000 = 1,440`. After, 4,000 bots and 496,000 humans. `3,680` against `1,488`. Success at removing bots makes the same detector wrong more often, because there are fewer bots to find and as many humans to misjudge. Re-estimate prevalence with a random audit after every wave.
</details>

34. *Week 8 · compute.* A detector has recall 90%. Prevalence is 1.5%. What false positive rate does it need for 98% precision?

<details>
<summary>Answer and worked solution</summary>

**Answer:** About 0.028%, one human in about 3,600.

Solve `0.9 × 0.015 / (0.9 × 0.015 + F × 0.985) = 0.98`. Then `F × 0.985 = 0.0135 × (1 / 0.98 − 1) = 0.0002755`, so `F = 0.00028`. When bots are rare, the false positive rate is the lever that matters.
</details>

35. *Week 8 · code.* This is the lecture's threshold formula with a weaker detector (`d = 2.5`) and 5% prevalence. What does it print, and what does the second line tell you to build?

```python
import math

def phi(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))

d, prevalence = 2.5, 0.05
for c_fp, c_fn in [(10, 10), (50, 1)]:
    ratio = (c_fp / c_fn) * (1 - prevalence) / prevalence
    t = (math.log(ratio) + d * d / 2) / d
    fpr, tpr = 1 - phi(t), 1 - phi(t - d)
    precision = tpr * prevalence / (tpr * prevalence + fpr * (1 - prevalence))
    print(f"ratio {c_fp / c_fn:4.0f}  t {t:.2f}  recall {tpr:.1%}  FPR {fpr:.3%}  precision {precision:.1%}")
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
ratio    1  t 2.43  recall 52.9%  FPR 0.760%  precision 78.6%
ratio   50  t 3.99  recall 6.8%  FPR 0.003%  precision 99.1%
```

If a wrongful ban costs 50 missed bots, the best automatic threshold catches under 7% of bots. That is the right answer to "whom may we punish without a second look", and it says the automatic band should be small. Build the three bands. A narrow automatic band above `t_act`, a review band sized to your reviewers' daily capacity, and silence below `t_review`.
</details>

36. *Week 8 · compute.* The section 1 model has weights `[−2.72, −4.3, 4.34]` on `[1, slack_cv, hours / 10]`. Score three accounts: (a) CV 0.3, 18 hours a day, (b) CV 0.7, 3 hours, (c) CV 0.7, 14 hours. Is account (c) 59% likely to be a bot?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `z = 3.80`, score 0.978. (b) `z = −4.43`, score 0.012. (c) `z = 0.35`, score 0.586. No.

(a) `−2.72 − 4.3 × 0.3 + 4.34 × 1.8 = −2.72 − 1.29 + 7.81 = 3.80`, and `1 / (1 + e^(−3.80)) = 0.978`. (b) `−2.72 − 3.01 + 1.30 = −4.43`. (c) `−2.72 − 3.01 + 6.08 = 0.35`.

The model was trained on equal numbers of bots and humans and runs at about 2% prevalence, so its scores overstate the chance of being a bot. Account (c) looks like a heavy honest player with human timing. Calibrate scores on a sample at live prevalence, or pick thresholds from measured precision there.
</details>

37. *Week 8 · critique.* A team trains on 12 months of past bans, evaluates on a random 20% of the same accounts, and reports "recall 94%, accuracy 99%". Name three problems with that evaluation and one fix for each.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

- **Labels from past bans.** The set holds only bots the old methods caught, so recall is measured on the easy kinds. Label a random sample of accounts with at least two reviewers, as the NCSOFT team did.
- **A random split hides drift.** Future behavior leaks into training. Train on older months and test on newer ones.
- **Accuracy hides the base rate.** At low prevalence a 1% false positive rate gives 99% accuracy and thousands of wrongful flags. Report recall, false positive rate and precision at today's measured prevalence.
</details>

## Week 9: Account security and takeovers

38. *Week 9 · compute.* Victims notice a theft after an exponential time with mean `m = 30` hours. What share of stolen value does a 2-day trade hold recover? What hold recovers 95%?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 79.8%. About 90 hours, 3.7 days.

`1 − e^(−48/30) = 1 − e^(−1.6) = 1 − 0.202 = 0.798`. For 95%, `H = −30 × ln(0.05) = 30 × 3.0 = 89.9` hours.
</details>

39. *Week 9 · compute.* Victims are 60% active players (`m = 8` hours) and 40% lapsed players (`m = 720` hours, 30 days). Compute recovery for holds of 1, 3, 14 and 30 days. What design does the result point to?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 58.3%, 63.8%, 74.9% and 85.3%.

At 1 day, `0.6 × (1 − e^(−3)) + 0.4 × (1 − e^(−24/720)) = 0.570 + 0.013 = 0.583`. The active group is almost fully recovered after a day. Everything after that comes from the lapsed group, a few points per extra week, while the honest cost of the hold grows in a straight line.

The design is a risk-based hold. Keep the routine hold short and give a long hold to the first trades after a long absence, a new device or a security change, which is where thieves strike idle accounts.
</details>

40. *Week 9 · compute.* A game has 800,000 accounts, 60,000 trades a day and 30% authenticator adoption. A median of 20 hours passes from theft to report.
    (a) A stuffing campaign finds working passwords on 1.2% of accounts, and a new-device challenge stops 70% of logins that 2FA does not. Expected takeovers?
    (b) What `m` does the median imply, and what hold recovers 90% under the single exponential?
    (c) What delay cost does a 3-day hold impose each day if authenticated accounts are exempt, and what adoption would cut that cost by 40%?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 2,016. (b) `m ≈ 28.9` hours, hold about 66 hours. (c) 126,000 trade-days a day. Adoption of 58%.

(a) `800,000 × 0.012 × (1 − 0.3) × (1 − 0.7) = 2,016`.

(b) The median of an exponential is `m × ln 2`, so `m = 20 / 0.693 = 28.9`. `H = 28.9 × ln 10 = 66.4` hours.

(c) `(1 − 0.3) × 60,000 × 3 = 126,000`. A 40% cut needs `1 − a = 0.7 × 0.6 = 0.42`, so `a = 58%`. That is the case for rewards that raise adoption, like WoW's pet and bag slots.
</details>

41. *Week 9 · critique.* A studio's recovery flow is this. A player who lost access fills a form with the account name, the email on file and the last character name. Support moves the account to a new email the same day and ends the old sessions. Name the step a thief with the player's email address and a convincing story can pass, and redesign the flow using the lecture's rule that security changes should be slow and loud.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Every proof on the form is public or easy to guess (character names show on the web armory and in game), so the form proves nothing. The same-day email change gives the owner no time to notice.

Redesign. Require a proof the thief is unlikely to have, such as past purchase details or account creation data, from a written list staff may not bend under pressure. Notify the old email and phone of the request. Start a hold of several days on the change itself, on trades and on further security changes, the Bank PIN design applied to the whole account. Encourage 2FA on the email account, since email-only recovery makes the email the real key.
</details>

## Week 10: Gold sellers and RMT networks

42. *Week 10 · compute.* On the section 2 toy server, replace R1 with "flag every account that plays 18 or more hours a day". Compute TP, FP, FN, precision, recall and gold seized. Would you run this rule in production?

<details>
<summary>Answer and worked solution</summary>

**Answer:** TP 180, FP 0, FN 24, precision 100%, recall 88.2%, seized 900,000 gold. No.

The heavy honest players play 17 hours and the 180 long-shift farms play 20, so a threshold of 18 falls in a gap that exists only in the toy data. Real heavy players spread above 18, and an operator who learns the rule runs farms at 17. The rule still misses the four mules, which hold 89% of the operation's gold on hand. A hub rule seizes more with a handful of bans.
</details>

43. *Week 10 · code.* What does this print? With the lecture's hub test at fan-in `≥ 3` and stranger share `≥ 0.5`, which accounts are hubs?

```python
gifts = [("f1", "m", 20_000), ("f2", "m", 20_000), ("f3", "m", 20_000),
         ("m", "b1", 50_000), ("m", "b2", 50_000), ("m", "g1", 5_000),
         ("g1", "g2", 1_000), ("g2", "g1", 1_000), ("g3", "g1", 2_000)]
guild = {"f1": None, "f2": None, "f3": None, "m": None,
         "b1": 7, "b2": 9, "g1": 3, "g2": 3, "g3": 3}

senders, receivers = {}, {}
for s, r, _ in gifts:
    senders.setdefault(r, set()).add(s)
    receivers.setdefault(s, set()).add(r)

def stranger_share(a):
    out = receivers.get(a, set())
    g = guild[a]
    return sum(guild[r] != g or g is None for r in out) / len(out) if out else 0

for a in ("m", "g1", "g2"):
    print(a, len(senders.get(a, ())), len(receivers.get(a, ())), round(stranger_share(a), 2))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
m 3 3 1.0
g1 3 1 0.0
g2 1 1 0.0
```

Only `m` is a hub. It has fan-in 3 from the three farms and pays three receivers, and because it has no guild every receiver counts as a stranger. `g1` also has fan-in 3 (from `m`, `g2` and `g3`), but its only outgoing gift goes to a guildmate, so its stranger share is 0. That second condition is what removed 49 of 50 guild banks from R2 in the lecture. Note that `g1` bought gold from `m`. It is a buyer, not part of the operation, and a one-hop expansion from `m` never reaches it because expansion follows senders, not receivers.
</details>

44. *Week 10 · compute.* Using the section 3 prices ($15 per replacement account, $5 per million gold), what does it cost an operation to lose (a) its 6 mules holding 1.5 million gold each, (b) its 300 farms holding 8,000 gold each, (c) all 306 accounts? Why can (a) hurt the operation more than the dollars say?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) $135. (b) $4,512. (c) $4,647.

(a) `6 × 15 + 9 × 5 = 90 + 45 = 135`. (b) `300 × 15 + 2.4 × 5 = 4,500 + 12 = 4,512`. (c) `4,590 + 57 = 4,647`.

The table counts accounts and stock only. A mule carries buyer trust, delivery routines and the identity the storefront uses, and it has to be built and aged. When every mule goes at once, orders cannot be delivered, and a storefront that misses deliveries loses customers to competitors. Downtime is what the dollar table does not show.
</details>

45. *Week 10 · design.* After you ban a confirmed mule, you want to expand one hop to the accounts that sent it gifts. The senders include farms, a few stolen accounts that were stripped into the mule, and members of a guild that donated to it during a giveaway. Write an expansion rule, say what happens to each group under it, and say where the stolen accounts should go.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Expand only to senders that are young (for example under 30 days) and have no guild, the lecture's R5. Farms are new and unguilded, so they are caught. Guild donors are old and guilded, so they are not. Stolen accounts are old and usually guilded, so they are not caught either, and they should go to account recovery (week 9), not the ban queue.

Every expansion step needs its own evidence. One edge to a hub looks the same for a farm and a victim. The account's history tells them apart. Expect the operation to adapt by aging bought accounts, which is why Lab 10's second operation includes aged farms.
</details>

## Week 11: Exploit response

46. *Week 11 · compute.* Use the section 2 model with the lecture's parameters (`D = 50,000`, `p = 1,000`, `M = 500` million, `k = 0.2`, `b = 0.6`, `P = 4,000`, `w = 0.5`, `λ = 20,000`). The dupe is found after 4 hours. (a) Compute the rollback's harm and the trace's total harm, and say which the model recommends. (b) How much gold does the ring keep under each? (c) Which kind of damage, state or incentive, does each response repair, and what must you add?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Rollback 16,000 player-hours, trace about 52,300. Roll back. (b) Rollback 0, trace about 27.5 million gold. (c) Both repair state only. Add sanctions sized to what the ring keeps or converted.

`m = 1 − e^(−0.8) = 0.5507`, so 27,534 items left the ring: 16,520 bought and 11,013 gone. Rollback `= 4,000 × 4 = 16,000`. Trace: buyers lose `0.5 × 16,520 = 8,260` hours, and the residual is `11.01` million gold, `2.20%` of `M`, so the total is `8,260 + 20,000 × 2.20 ≈ 52,314`. Four hours is well before the 23.5-hour crossover.

Neither lineage response touches incentives. After a trace the ring keeps `27,534 × 1,000 ≈ 27.5` million gold. After a rollback it keeps nothing, which is where it started, so exploiting cost it nothing. The OSRS coin glitch of July 2018 needed both halves, a rollback for the state plus removal of bond-bought membership and temporary bans for the incentives.
</details>

47. *Week 11 · design.* A crafting exploit is found. The logs show 2,500 players who triggered it once, 120 who triggered it more than 100 times and kept the output, 15 who moved the output to alts and sold it for real money, 1 who triggered it twice and reported it the same day, and 2 who sold a script that automated it. Assign the lecture's tiers and a response to each group. Which group is the largest, and why does that decide how mild its response should be?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Tier 0, the reporter, gets gains removed, thanks and possibly a reward (week 13). Tier 1, the 2,500, gets gains removed and a notice. Tier 2, the 120, gets gains removed and a temporary suspension. Tier 3, the 15, gets gains and conversions removed and a longer suspension or ban. Tier 4, the 2 sellers, get a permanent ban, and legal action is worth considering (week 12).

Tier 1 is by far the largest. Banning it would ban a large slice of ordinary players for the studio's own bug. Tier on behavior the logs show, and remove the gains at every tier.
</details>

48. *Week 11 · compute.* A ban wave list holds 20,000 accounts. Before firing, you review a simple random sample of 200. What is the chance the sample contains at least one account from an innocent group of (a) 1,100 accounts, (b) 30 accounts, both sharing one harmless tool? What should the pre-wave review do instead of relying on a random sample alone?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Almost certain, above 99.99%. (b) About 26%. Add a stratified sample of accounts with unusual setups, and look for clusters in the flag list.

This is the complement rule from week 2. (a) `1 − (1 − 1,100 / 20,000)^200 = 1 − 0.945^200 ≈ 1`. (b) `1 − (1 − 0.0015)^200 = 1 − 0.741 = 0.259`.

A small affected group, like the Cedega users in 2006, usually slips past a random sample. Sample rare operating systems, compatibility layers, accessibility tools and old hardware on purpose, check whether flagged accounts share a trait that is not about cheating, stage the wave and keep banned items restorable during the appeal period.
</details>

## Week 12: Legal and ethical considerations

49. *Week 12 · compute.* The base rate of cheating is 0.5%. A detector has `TPR = 0.85`, `FPR = 0.004`. A known-cheat file hash has `TPR = 0.5`, `FPR = 0.0005`. The sanction ladder has `C = 2` (a queue restriction), `C = 10` (a 14-day suspension) and `C = 40` (a permanent ban). Assuming independence, compute `P(cheat)` for the detector alone, the hash alone and both, and say which rungs each allows.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Detector alone 0.516, no rung. Hash alone 0.834, the queue restriction only. Both 0.9991, all three rungs.

Thresholds `C / (C + 1)` are 0.667, 0.909 and 0.976. Prior odds `0.005 / 0.995 = 0.005025`. Detector `LR = 212.5`, odds `1.068`, `P = 0.516`. Hash `LR = 1,000`, odds `5.03`, `P = 0.834`. Both, odds `0.005025 × 212.5 × 1,000 = 1,068`, `P = 0.9991`.

The strongest signal came from scanning the player's files. Section 3 asks what that scan costs honest players in privacy and security.
</details>

50. *Week 12 · code.* What does this print? Explain why the second rule's innocent count is not a promise of one innocent ban per 500,000 players.

```python
players, prior = 500_000, 0.02
cheaters = players * prior
honest = players - cheaters
rules = {"detector alone": [(0.85, 0.004)],
         "detector + hash": [(0.85, 0.004), (0.50, 0.0005)]}
for name, sig in rules.items():
    tp, fp = cheaters, honest
    for tpr, fpr in sig:
        tp, fp = tp * tpr, fp * fpr
    print(f"{name:16} caught {tp:7,.0f}  innocents {fp:7,.1f}  precision {tp / (tp + fp):.2%}")
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
detector alone   caught   8,500  innocents 1,960.0  precision 81.26%
detector + hash  caught   4,250  innocents     1.0  precision 99.98%
```

The code multiplies the two false positive rates, which assumes the signals are independent among honest players. If some honest group trips both (the Cedega pattern, or a tool that looks like a known cheat file), the real rate is higher. Measure how often the pair fires together on labelled honest accounts before trusting the product. Lab 12's data has one pair that breaks the assumption.
</details>

51. *Week 12 · compute.* With the detector from question 49 (`LR = 212.5`) and a 7-day suspension at `C = 5`, what base rate lets the detector alone justify the suspension? What threshold does Blackstone's ten-to-one ratio set, in the model's terms?

<details>
<summary>Answer and worked solution</summary>

**Answer:** A base rate of at least about 2.3%. Blackstone's ratio is `C = 10`, a threshold of `10 / 11 ≈ 0.909`.

The suspension needs `P ≥ 5 / 6`, posterior odds of at least 5. Prior odds must be at least `5 / 212.5 = 0.0235`, so `π ≥ 0.0235 / 1.0235 = 2.30%`. The same detector that justifies a suspension on a ranked ladder full of cheaters may justify nothing in a casual queue. Rules tuned on one population misfire on another.
</details>

52. *Week 12 · design.* A proposed anti-cheat uploads a full screenshot and the list of running processes whenever the aim detector fires, and keeps both for two years. Redesign it to meet data minimization and storage limitation while keeping most of its detection value, and name one security duty the studio takes on if the scanner runs as a kernel driver.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Check processes on the client against a signed, versioned list of known cheat signatures and upload only the IDs that matched, not the list. Drop the screenshot, or capture only the game window and only when a human reviewer requests it for a case in the review band. Scan only while the game runs. Keep results for the appeal window, then delete them.

A kernel driver becomes part of every player's security. The studio must keep it minimal, get it reviewed, run a bug bounty for it and plan how to revoke a vulnerable signed version, because, as the Genshin Impact `mhyprot2.sys` case showed, attackers can reuse an old signed driver on machines that never ran the game.
</details>

## Week 13: Bug bounties and disclosure

53. *Week 13 · compute.* A finder can sell $250 a day of duped gold. Your team detects such dupes in 12 days on average. You catch the exploiter half the time, and they lose an account worth $400. Reports are accepted 85% of the time. Compute `B*`. The dupe costs the studio $6,000 a day plus $30,000 at discovery. What is the expected cost of an unreported dupe?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `B* ≈ $3,294`. `C_x = $102,000`.

`v / h = 250 × 12 = 3,000`. `q × L = 0.5 × 400 = 200`. `E_x = 2,800`. `B* = 2,800 / 0.85 = 3,294`. `C_x = 6,000 × 12 + 30,000 = 102,000`. The bounty is about 3% of the harm it prevents.
</details>

54. *Week 13 · code.* What does this print? From the 12-day to the 6-day row, `B*` falls to less than half. Why?

```python
def bounty_needed(v, h, q, L, a):
    return max(0.0, (v / h - q * L) / a)

def studio_cost(d, h, R):
    return d / h + R

for days in (30, 12, 6, 3):
    h = 1 / days
    print(f"{days:2} days  B* {bounty_needed(250, h, 0.5, 400, 0.85):7,.0f}"
          f"  studio {studio_cost(6_000, h, 30_000):9,.0f}")
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
30 days  B*   8,588  studio   210,000
12 days  B*   3,294  studio   102,000
 6 days  B*   1,529  studio    66,000
 3 days  B*     647  studio    48,000
```

Halving detection time halves `v / h` (3,000 to 1,500), but the penalty `q × L = 200` does not shrink. So `E_x` goes from 2,800 to 1,300, less than half, and `B*` from 3,294 to 1,529. Detection and bounties are complements. Money spent on detection lowers the price of every future bounty.
</details>

55. *Week 13 · compute.* For the dupe in question 53, you pay exactly `B*`, so `a × B = $2,800`. A double-dipper uses the bug for 4 days at $250 a day and then reports. If your logs catch prior use, you void the bounty and apply the $400 penalty. What audit probability `p` makes the double dip no better than an honest report?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `p ≥ 0.3125`.

The double dip stops paying when `v × k ≤ p × (a × B + L)`, so `1,000 ≤ p × 3,200` and `p ≥ 0.3125`. If you cannot tell whether a reporter used the bug first, your advertised bounty is partly paying abusers. Logs that show who triggered the bug, and when, are part of the program.
</details>

56. *Week 13 · compute.* Your program's headline dupe bounty is $2,000, but 40% of valid reports are rejected as duplicates. A rival accepts 90%. What headline bounty does the rival need to match your expected payout? What is the cheapest way for you to become more attractive to finders?

<details>
<summary>Answer and worked solution</summary>

**Answer:** About $1,333. Raise `a`.

Your expected payout is `0.6 × 2,000 = 1,200`. The rival needs `1,200 / 0.9 = 1,333`. Fast triage, a published duplicate rule, and partial bounties for duplicates filed within a short window raise `a` without raising the headline number.
</details>

## Week 14: Case studies

57. *Week 14 · explain.* Fill the course's seven-row case template (asset, attacker economics, control, detection, response, outcome, transferable rule) for the Old School RuneScape potion storage glitch of 1 October 2024, using only the facts in the week 4 lecture. Mark one row where you are stating an assumption rather than a recorded fact.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

| Row | Entry |
|---|---|
| Asset | Potions, and through them the value in players' banks |
| Attacker economics | Potions withdrawn into the chugging barrel while storage went negative, value created from nothing |
| Control | None at the storage layer. A second view of the same quantity skipped the check |
| Detection | Not described in the week 4 account. Anything you write here, such as "noticed through player reports within hours", is an assumption and must be marked as one |
| Response | 15-minute warning, trading, the Grand Exchange and ground items locked, rollback to before the timer, reopening at 13:00 UTC after a tested fix |
| Outcome | Worlds back at 13:00 UTC with the fix in place. The rollback restored play to before the timer, at the price of lost progress for everyone since that point (week 11 notes it also restored untradeable items lost under the lock) |
| Transferable rule | Enforce non-negativity in the transfer primitive or the storage layer, so every interface inherits it. Every new container declares its value paths at design review |

The detection row is the assumption row. Marking it is the template's first habit, separating what was recorded from what you infer.
</details>

58. *Week 14 · explain.* RuneScape tried two trade limits. The 2008 limit blocked unbalanced trades for everyone and was voted out in 2011. The November 2011 limit caps what never-paid accounts can give away at 25,000 coins a day. Explain in the week 1 ledger's terms why the first failed, and in the week 6 or week 10 terms why the second lasts.

<details>
<summary>Answer and worked solution</summary>

**Answer:** In week 1 terms the 2008 limit had a player cost `P` so large that 91% of voting players asked for it to go. It charged every honest gift to reach a small attacking population.

The 2011 limit bites on the attacker's cheapest input. In week 10 terms it slows the consolidation step, since a free farm account can no longer ship its gold to a mule quickly. In week 6 terms, a farm that must pay for membership has a higher setup cost `A` and a longer break-even lifetime. Honest new players rarely need to give away large sums and can still receive gifts, so `P` stays small. Narrow controls on edges only an RMT network uses heavily outlast blanket ones.
</details>

59. *Week 14 · explain.* In *MDY v. Blizzard*, what did the Ninth Circuit reverse in December 2010, and what did it uphold? What does the result tell a studio about keeping technical controls like Warden in place even when detection is imperfect?

<details>
<summary>Answer and worked solution</summary>

**Answer:** It reversed the copyright infringement finding, holding that breaking a license term is infringement only when the term is tied to the copyright holder's exclusive rights, and a no-bots rule is not. It upheld the finding that MDY violated the DMCA's ban on trafficking in circumvention technology, at least for content the servers supply.

The claim that survived was about getting past a technical control. Warden mattered in court as well as in detection, so a studio should keep such controls in place and write its terms knowing which clauses it may need to enforce (MMO402 week 5).
</details>

60. *Week 14 · compute and explain.* In November 2021 Amazon disabled Steam family sharing for New World, citing bots, gold sellers and ban evaders. (a) Which term of the week 6 profit model did this move, why can that end a farm without any change to detection, and who pays the collateral cost? (b) On the week 14 scorecard, instant bans have `detect = 6`, `act = 0`, `down = 2`. Closing the free account raises `down` to 60. Compute the uptime before and after, and how many days of faster detection one day of extra downtime was worth before the change.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) It raised the setup cost `A` of a replacement account from nearly zero to the price of a copy of the game. (b) Uptime falls from 0.750 to 0.091. Before the change, one day of downtime was worth 3 days of detection.

(a) With `A` near zero, a bot pays for itself almost at once and a ban costs the operator little. Raising `A` raises the break-even lifetime `A / m`. If detection already keeps bots alive for less than the new `A / m`, farming loses money and banned operators stop coming back, even though detection and bans did not change. Families who shared the game for ordinary reasons pay the collateral cost, which is why Amazon offered them help.

(b) `uptime = live / (live + down)`. Before, `6 / 8 = 0.750`. After, `6 / 66 = 0.091`. The rule `live / down = 6 / 2 = 3` says a day of downtime was worth three days of detection, so the downtime lever was the right one to pull.
</details>

## Week 15: Threat model and detection prototype

61. *Weeks 6 and 8 · compute.* Your prototype's automatic band flags each live bot with probability 0.12 a day, and its review band catches a further 0.10 a day after reviewer confirmation. Bans happen on detection. Use the week 6 card (`m = $5`, `A = $35`). Is the farm open with both bands? With the automatic band only, if the review team is cut to save money?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Both bands, `d = 0.22`, lifetime 4.5 days, profit −$12.27, closed. Automatic band only, `d = 0.12`, lifetime 8.3 days, profit +$6.67, open.

`5 × (1 / 0.22) − 35 = 22.73 − 35 = −12.27`. `5 × (1 / 0.12) − 35 = 41.67 − 35 = 6.67`. The break-even lifetime is 7 days, and the review band is what pushes lifetime below it. Cutting reviewers looks like a saving on the detection budget and reopens the farm. Write this link into your prototype report.
</details>

62. *Weeks 8 and 15 · critique.* A prototype report says "precision 97% on the test set". The test set has equal numbers of bots and humans, and the detector's recall is 90% with a false positive rate of 3%. The student's threat model estimates 1% prevalence. What precision should the report state, and what should it say about the automatic band?

<details>
<summary>Answer and worked solution</summary>

**Answer:** About 23%. The detector may feed a review queue but must not act on its own.

At 50% prevalence, `0.45 / (0.45 + 0.015) = 96.8%`, the reported figure. At 1%, `0.009 / (0.009 + 0.03 × 0.99) = 0.009 / 0.0387 = 23.3%`. Three of every four flags would be honest players. The report should state precision at the threat model's prevalence, show how it moves after a ban wave, and set `t_act` from measured precision in the live population. A 50/50 test set flatters every detector.
</details>
