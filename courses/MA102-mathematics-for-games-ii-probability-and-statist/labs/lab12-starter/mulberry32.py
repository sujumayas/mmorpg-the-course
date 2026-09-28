"""Seeded random generator used across MA102 labs 12 to 14.

mulberry32 is the same generator the course interactives use, so a seed
gives the same stream in Python and in the browser.

    rng = Mulberry32(13)
    rng.random()        # float in [0, 1)
    rng.bernoulli(0.02) # 1 with probability 0.02, else 0

Spreadsheet users: RAND() cannot be seeded. Generate your random numbers
once with this script (or paste a fixed column of values) and keep them.
"""


class Mulberry32:
    def __init__(self, seed: int):
        self.state = seed & 0xFFFFFFFF

    def next_uint32(self) -> int:
        self.state = (self.state + 0x6D2B79F5) & 0xFFFFFFFF
        t = self.state
        t = ((t ^ (t >> 15)) * (t | 1)) & 0xFFFFFFFF
        t ^= (t + (((t ^ (t >> 7)) * (t | 61)) & 0xFFFFFFFF)) & 0xFFFFFFFF
        return (t ^ (t >> 14)) & 0xFFFFFFFF

    def random(self) -> float:
        return self.next_uint32() / 4294967296

    def bernoulli(self, p: float) -> int:
        return 1 if self.random() < p else 0


if __name__ == "__main__":
    rng = Mulberry32(13)
    print([round(rng.random(), 6) for _ in range(5)])
