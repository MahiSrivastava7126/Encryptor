"""
caesar.py - Core Caesar Cipher implementation.

Encryption : E(x) = (x + n) % 26
Decryption : D(x) = (x - n) % 26

where x is the letter's position in the alphabet (A/a = 0 ... Z/z = 25)
and n is the shift key.

Uppercase and lowercase are handled separately so case is preserved.
Spaces, digits, punctuation and all other symbols pass through unchanged.
"""

ALPHABET_SIZE = 26  # Number of letters in the English alphabet


def _shift_char(ch: str, shift: int, decrypt: bool = False) -> str:
    """
    Shift a single character.

    Steps (Process stage of IPO):
      1. Decide the base: ord('A') = 65 for uppercase, ord('a') = 97 for lowercase.
      2. Convert the letter to a 0-25 index:  x = ord(ch) - base
      3. Apply modular arithmetic:
            encrypt -> (x + n) % 26
            decrypt -> (x - n) % 26
      4. Convert back to a character:  chr(result + base)
    """
    if "A" <= ch <= "Z":          # uppercase letter
        base = ord("A")
    elif "a" <= ch <= "z":        # lowercase letter
        base = ord("a")
    else:                         # space, digit, symbol, emoji, accented char...
        return ch                 # leave untouched

    x = ord(ch) - base            # 0..25

    if decrypt:
        y = (x - shift) % ALPHABET_SIZE   # D(x) = (x - n) % 26
    else:
        y = (x + shift) % ALPHABET_SIZE   # E(x) = (x + n) % 26

    return chr(y + base)


def encrypt(plaintext: str, shift: int) -> str:
    """Encrypt plaintext with the Caesar cipher. Time: O(n), Space: O(n)."""
    if not isinstance(shift, int):
        raise TypeError("shift must be an integer")
    shift %= ALPHABET_SIZE  # normalise: 29 -> 3, -3 -> 23
    return "".join(_shift_char(ch, shift) for ch in plaintext)


def decrypt(ciphertext: str, shift: int) -> str:
    """Decrypt ciphertext with the Caesar cipher. Time: O(n), Space: O(n)."""
    if not isinstance(shift, int):
        raise TypeError("shift must be an integer")
    shift %= ALPHABET_SIZE
    return "".join(_shift_char(ch, shift, decrypt=True) for ch in ciphertext)
