"""Stability forecast for your team. Edit the numbers, then run:

    python forecast.py

Needs a working triage.py.
"""
import triage

B0 = 30          # open must-fix bugs today
F0 = 20          # new bugs found on day 1
DECAY = 0.8      # fraction of yesterday's find rate that survives
CAPACITY = 8     # fixes per day
REGRESSION = 0.0 # fraction of fixes that break something else
DAYS = 30
SHIP_DAY = 14

found = triage.find_rates(F0, DECAY, DAYS)
open_counts = triage.backlog(B0, found, CAPACITY, REGRESSION)
print("day  found  open")
for day, (f, b) in enumerate(zip(found, open_counts), start=1):
    marker = "  <- ship day" if day == SHIP_DAY else ""
    print(f"{day:>3}  {f:>5}  {b:>5.1f}{marker}")
print("peak on day(s):", triage.peak_days(open_counts))
print("zero on day:", triage.zero_day(open_counts))
print("open on ship day:", round(open_counts[SHIP_DAY - 1], 1))
