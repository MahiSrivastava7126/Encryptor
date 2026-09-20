"""
vigenere.py - Vigenere cipher (a stronger, polyalphabetic improvement).

Instead of ONE fixed shift, a keyword supplies a DIFFERENT shift for each
letter position:
    E(x_i) = (x_i + k_(i mod m)) % 26
    D(y_i) = (y_i - k_(i mod m)) % 26

Example: key "KEY" -> shifts 10, 4, 24, 10, 4, 24, ...
Non-letters are copied as-is and do NOT consume a key letter.
"""

from .caesar import ALPHABET_SIZE


def _key_shifts(key: str):
    """Convert a keyword to a list of numeric shifts (A=0 ... Z=25)."""
    shifts = [ord(c.upper()) - ord("A") for c in key if c.isascii() and c.isalpha()]
    if not shifts:
        raise ValueError("Key must contain at least one letter (A-Z).")
    return shifts


def _process(text: str, key: str, decrypt: bool) -> str:
    shifts = _key_shifts(key)
    out, k = [], 0                       # k = index of the next key letter to use
    for ch in text:
        if "A" <= ch <= "Z":
            base = ord("A")
        elif "a" <= ch <= "z":
            base = ord("a")
        else:
            out.append(ch)               # symbols/spaces: no key consumed
            continue
        n = shifts[k % len(shifts)]
        x = ord(ch) - base
        y = (x - n) % ALPHABET_SIZE if decrypt else (x + n) % ALPHABET_SIZE
        out.append(chr(y + base))
        k += 1
    return "".join(out)


def encrypt(plaintext: str, key: str) -> str:
    """Vigenere encryption. Time O(n), Space O(n)."""
    return _process(plaintext, key, decrypt=False)


def decrypt(ciphertext: str, key: str) -> str:
    """Vigenere decryption. Time O(n), Space O(n)."""
    return _process(ciphertext, key, decrypt=True)
