"""Unit tests. Run with:  python -m unittest discover -s tests -t . -v"""

import unittest

from caesar_cipher import encrypt, decrypt, vigenere
from caesar_cipher.cryptanalysis import brute_force, auto_crack


class TestCaesar(unittest.TestCase):
    def test_known_vector(self):
        self.assertEqual(encrypt("HELLO", 3), "KHOOR")
        self.assertEqual(decrypt("KHOOR", 3), "HELLO")

    def test_case_preserved(self):
        self.assertEqual(encrypt("Hello World", 3), "Khoor Zruog")

    def test_symbols_spaces_digits_unchanged(self):
        text = "Hi, there! 123 #@$ 2026."
        self.assertEqual(encrypt(text, 5)[2], ",")
        self.assertEqual(decrypt(encrypt(text, 5), 5), text)

    def test_wraparound(self):
        self.assertEqual(encrypt("xyz XYZ", 3), "abc ABC")
        self.assertEqual(decrypt("abc ABC", 3), "xyz XYZ")

    def test_large_and_negative_shift(self):
        self.assertEqual(encrypt("abc", 29), encrypt("abc", 3))   # 29 % 26 == 3
        self.assertEqual(encrypt("abc", -3), "xyz")
        self.assertEqual(decrypt(encrypt("Test", -100), -100), "Test")

    def test_zero_and_26_shift_is_identity(self):
        self.assertEqual(encrypt("Same text", 0), "Same text")
        self.assertEqual(encrypt("Same text", 26), "Same text")

    def test_round_trip_all_shifts(self):
        msg = "The Quick Brown Fox, jumps over 13 lazy dogs!"
        for n in range(-30, 60):
            self.assertEqual(decrypt(encrypt(msg, n), n), msg)

    def test_empty_string(self):
        self.assertEqual(encrypt("", 3), "")

    def test_non_ascii_untouched(self):
        self.assertEqual(encrypt("café", 1), "dbgé")

    def test_bad_shift_type(self):
        with self.assertRaises(TypeError):
            encrypt("abc", "3")


class TestAttacks(unittest.TestCase):
    def test_brute_force_contains_plaintext(self):
        cipher = encrypt("Attack at dawn", 7)
        self.assertIn("Attack at dawn", [p for _, p in brute_force(cipher)])

    def test_auto_crack(self):
        plain = "Meet me at the old library after the meeting tonight"
        shift, guess = auto_crack(encrypt(plain, 11))
        self.assertEqual(guess, plain)
        self.assertEqual(shift, 11)


class TestVigenere(unittest.TestCase):
    def test_classic_vector(self):
        self.assertEqual(vigenere.encrypt("ATTACKATDAWN", "LEMON"), "LXFOPVEFRNHR")

    def test_round_trip_with_symbols(self):
        msg = "Hello, World! 42"
        self.assertEqual(vigenere.decrypt(vigenere.encrypt(msg, "Key"), "Key"), msg)

    def test_invalid_key(self):
        with self.assertRaises(ValueError):
            vigenere.encrypt("abc", "1234")


if __name__ == "__main__":
    unittest.main()
