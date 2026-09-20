"""
cryptanalysis.py - Shows WHY the Caesar cipher is weak.

Two attacks that need NO key:
  1. Brute force        : only 25 useful keys -> try them all.
  2. Frequency analysis : pick the shift whose letter distribution looks most
                          like English (chi-squared test).
"""

from .caesar import decrypt, ALPHABET_SIZE

# Approximate English letter frequencies in percent (A..Z)
ENGLISH_FREQ = [
    8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966, 0.153,
    0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056,
    2.758, 0.978, 2.360, 0.150, 1.974, 0.074,
]


def brute_force(ciphertext: str):
    """Return [(shift, candidate_plaintext), ...] for all 26 shifts. O(26*n)."""
    return [(s, decrypt(ciphertext, s)) for s in range(ALPHABET_SIZE)]


def _chi_squared(text: str) -> float:
    letters = [c.lower() for c in text if "a" <= c.lower() <= "z"]
    total = len(letters)
    if total == 0:
        return float("inf")
    score = 0.0
    for i in range(ALPHABET_SIZE):
        observed = letters.count(chr(ord("a") + i))
        expected = ENGLISH_FREQ[i] / 100 * total
        score += (observed - expected) ** 2 / expected
    return score


def auto_crack(ciphertext: str):
    """Guess the shift automatically. Returns (best_shift, plaintext)."""
    return min(brute_force(ciphertext), key=lambda pair: _chi_squared(pair[1]))
