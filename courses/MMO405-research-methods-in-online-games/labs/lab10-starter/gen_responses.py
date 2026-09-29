"""Regenerate responses.csv for MMO405 lab 10 (invented data, seed 1010).

3,000 adult players answer the same sensitive question twice, in two
randomly split halves of the sample:
  - half A gets the direct question ("Have you ever bought gold?"),
  - half B gets randomized response with truth probability t = 0.5.
The true share of buyers is 12%. Under the direct question only 55% of
buyers admit it. Under randomized response everyone follows the rules.
"""
import csv
import random
from pathlib import Path

SEED, N, PI, T, HONEST = 1010, 3000, 0.12, 0.5, 0.55


def main(path=Path(__file__).parent / "responses.csv"):
    rng = random.Random(SEED)
    rows = []
    for i in range(N):
        bought = rng.random() < PI
        method = "direct" if i % 2 == 0 else "rr"
        if method == "direct":
            answer = bought and rng.random() < HONEST
        else:
            answer = bought if rng.random() < T else rng.random() < 0.5
        rows.append({"respondent": f"r{i:04d}", "method": method,
                     "t": 1.0 if method == "direct" else T, "answer": int(answer)})
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["respondent", "method", "t", "answer"])
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {len(rows)} rows to {path.name}")


if __name__ == "__main__":
    main()
