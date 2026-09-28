# Lab 05 starter

Standard library only. Run with the course Python (`.venv/bin/python` at the repository root, or any Python 3.10+).

- `bitpack.py`: bit counting, quantization, a `BitWriter`, a `BitReader` and the lecture's player state. You write every function marked TODO.
- `python bitpack.py --check` must print `all checks passed`.
- `python bitpack.py --demo` packs the sample state and prints each field's bits and error. The total must be 108 bits in 14 bytes.
- `python bitpack.py --fuzz 10000` throws random bytes at `unpack_state`. Every packet must decode or raise `ReadError`. Any other exception is a bug.
