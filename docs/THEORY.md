# Caesar Cipher - Theory & Security Analysis

## 1. IPO Model (Input -> Process -> Output)

| Stage | What happens in this project |
|-------|------------------------------|
| **Input** | User provides (a) the text and (b) an integer shift key `n` (menu or CLI flags). Input is validated: the key must be an integer, text must be non-empty. |
| **Process** | For every character: if it is a letter, convert with `ord()` to a 0-25 index, apply `(x ± n) % 26`, convert back with `chr()`. Non-letters are copied unchanged. |
| **Output** | The ciphertext, then the decrypted text, plus a round-trip check (`decrypt(encrypt(x)) == x`). |

```
 [plaintext + key] --> [ord -> (x+n)%26 -> chr] --> [ciphertext]
 [ciphertext + key] --> [ord -> (x-n)%26 -> chr] --> [plaintext]
```

## 2. Encryption formula

```
E(x) = (x + n) mod 26
```

* `x` = letter index (A/a = 0 ... Z/z = 25), obtained by `ord(ch) - ord('A')` (or `'a'`).
* `n` = shift key.
* `mod 26` makes the alphabet "wrap around": `Z + 1 -> A`.

Worked example (`n = 3`): `HELLO`

| Letter | x | x + 3 | (x+3) % 26 | Cipher |
|--------|---|-------|-----------|--------|
| H | 7  | 10 | 10 | K |
| E | 4  | 7  | 7  | H |
| L | 11 | 14 | 14 | O |
| L | 11 | 14 | 14 | O |
| O | 14 | 17 | 17 | R |

Result: `KHOOR`. Wrap-around example: `Y` (24) -> (24+3) % 26 = 1 -> `B`.

## 3. Decryption formula

```
D(x) = (x - n) mod 26
```

Decryption is the inverse of encryption. In Python, `%` always returns a
non-negative result for a positive modulus, so `(2 - 5) % 26 = 23` works
without special handling (`C` shifted back by 5 -> `X`).

Proof that it is an inverse: `D(E(x)) = ((x + n) - n) mod 26 = x`.

## 4. Time & space complexity

| Operation | Time | Space |
|-----------|------|-------|
| Encrypt / Decrypt (`n` characters) | **O(n)** - one constant-time step per character | O(n) for the output string |
| Brute-force attack | O(26 * n) = **O(n)** | O(n) per candidate |
| Key space | only **25 useful keys** (shift 0 and 26 do nothing) | - |

Fast for the defender - but equally trivial for the attacker.

## 5. Why the Caesar cipher is weak

1. **Tiny key space** - only 25 possible keys. A computer tries them all instantly (brute force).
2. **Frequency analysis** - each plaintext letter always maps to the same cipher letter, so the statistical fingerprint of the language survives (`E` is the most common English letter). `cryptanalysis.py` implements this with a chi-squared test.
3. **Known-plaintext attack** - one known letter pair reveals the key.
4. **Patterns preserved** - word lengths, spaces, punctuation and repeated letters stay visible.
5. **No diffusion / confusion** - changing one plaintext letter changes only one ciphertext letter.
6. **Kerckhoffs's principle violated in practice** - security depends entirely on a secret so small that it can be guessed.
7. **No integrity or authentication** - an attacker can modify the ciphertext undetected.

**Bottom line: Caesar is an educational tool, never for real data.**

## 6. Improvements

| Upgrade | Idea | Status |
|---------|------|--------|
| **Vigenere cipher** | Keyword gives a *different* shift per letter (polyalphabetic), flattening frequency distribution. | Implemented in `caesar_cipher/vigenere.py` |
| Autokey cipher | Key stream = keyword + the plaintext itself, so it never repeats. | Idea |
| One-time pad | Truly random key as long as the message, used once - provably unbreakable. | Idea |
| Transposition + substitution | Combine ciphers (product cipher) for diffusion. | Idea |
| **Modern crypto** | AES-256-GCM, ChaCha20-Poly1305 (confidentiality + integrity); use a vetted library such as `cryptography`. | Use in production |

Note: Vigenere is also breakable (Kasiski examination, index of coincidence) and
is **not** secure by modern standards - it is simply the next step on the
learning path toward AES.
