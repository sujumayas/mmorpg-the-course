"""Lab 14 template. Fill in the TODOs; every simulation uses seed 14."""
import csv
import math

from mulberry32 import Mulberry32

SEED = 14


def phi(z: float) -> float:
    """Standard normal cumulative probability."""
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def load(path: str = "tutorial_test.csv") -> list[dict]:
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def two_proportion_z(k_a: int, n_a: int, k_b: int, n_b: int) -> dict:
    """Pooled rate, SE, z and two-sided p-value (lecture week 14, section 2)."""
    # TODO
    raise NotImplementedError


def diff_interval(k_a: int, n_a: int, k_b: int, n_b: int) -> tuple[float, float]:
    """95% interval for p_B - p_A using the unpooled SE."""
    # TODO
    raise NotImplementedError


def n_per_group(p_a: float, p_b: float, z_alpha: float = 1.96, z_beta: float = 0.84) -> float:
    """Power tab: sample size per group for 80% power at alpha = 0.05."""
    # TODO
    raise NotImplementedError


def aa_tests(p: float, n: int, tests: int, peek_every: int | None, rng: Mulberry32) -> float:
    """Step 4: fraction of A/A tests with |z| > 1.96, with or without peeking."""
    # TODO
    raise NotImplementedError


if __name__ == "__main__":
    rows = load()
    print(len(rows), "players")
    rng = Mulberry32(SEED)
