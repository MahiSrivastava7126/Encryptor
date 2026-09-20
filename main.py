#!/usr/bin/env python3
"""
main.py - Command-line front end for the Caesar Cipher project.

IPO MODEL
  INPUT   : text + shift key (typed by the user, or passed as CLI arguments)
  PROCESS : per-character  ord() -> (x +/- n) % 26 -> chr()
  OUTPUT  : encrypted text, then decrypted text (proves the round trip works)

Usage:
  python main.py                                   # interactive menu
  python main.py -m encrypt -t "Hello" -s 3        # one-shot encrypt
  python main.py -m decrypt -t "Khoor" -s 3        # one-shot decrypt
  python main.py -m crack   -t "Khoor Zruog"       # attack without the key
"""

import argparse

from caesar_cipher import encrypt, decrypt, vigenere
from caesar_cipher.cryptanalysis import brute_force, auto_crack


# ---------- INPUT helpers ----------

def read_shift(prompt: str = "Enter shift key (integer, e.g. 3): ") -> int:
    """Keep asking until the user types a valid integer."""
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("  [!] Shift key must be a whole number. Try again.")


def read_text(prompt: str = "Enter your text: ") -> str:
    """Keep asking until the user types something non-empty."""
    while True:
        text = input(prompt)
        if text.strip():
            return text
        print("  [!] Text cannot be empty. Try again.")


# ---------- menu actions ----------

def full_demo() -> None:
    """INPUT -> PROCESS -> OUTPUT in one go: encrypt, then decrypt back."""
    text = read_text()
    shift = read_shift()

    encrypted = encrypt(text, shift)       # PROCESS 1
    decrypted = decrypt(encrypted, shift)  # PROCESS 2

    print("\n----- OUTPUT -----")
    print(f"Original  : {text}")
    print(f"Shift key : {shift}  (effective: {shift % 26})")
    print(f"Encrypted : {encrypted}")
    print(f"Decrypted : {decrypted}")
    print("Round trip:", "OK" if decrypted == text else "FAILED")


def encrypt_only() -> None:
    print("Encrypted:", encrypt(read_text(), read_shift()))


def decrypt_only() -> None:
    print("Decrypted:", decrypt(read_text("Enter ciphertext: "), read_shift()))


def crack_demo() -> None:
    """Demonstrate that Caesar is weak: recover text WITHOUT the key."""
    cipher = read_text("Enter ciphertext to attack: ")
    print("\n--- Brute force (all 26 shifts) ---")
    for s, candidate in brute_force(cipher):
        print(f"  shift {s:2d}: {candidate}")
    shift, guess = auto_crack(cipher)
    print(f"\nFrequency analysis best guess -> shift {shift}: {guess}")


def vigenere_demo() -> None:
    """Show the stronger polyalphabetic upgrade."""
    text = read_text()
    key = read_text("Enter keyword (letters only, e.g. LEMON): ")
    try:
        enc = vigenere.encrypt(text, key)
    except ValueError as err:
        print(f"  [!] {err}")
        return
    print("Encrypted:", enc)
    print("Decrypted:", vigenere.decrypt(enc, key))


def menu() -> None:
    options = {
        "1": ("Encrypt + Decrypt demo (full IPO)", full_demo),
        "2": ("Encrypt only", encrypt_only),
        "3": ("Decrypt only", decrypt_only),
        "4": ("Crack a Caesar ciphertext (no key)", crack_demo),
        "5": ("Vigenere cipher demo (improvement)", vigenere_demo),
    }
    while True:
        print("\n=== Caesar Cipher Toolkit ===")
        for k, (label, _) in options.items():
            print(f"  {k}. {label}")
        print("  0. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye!")
            return
        if choice in options:
            print()
            options[choice][1]()
        else:
            print("  [!] Invalid choice.")


# ---------- entry point ----------

def main() -> None:
    parser = argparse.ArgumentParser(description="Caesar cipher toolkit")
    parser.add_argument("-m", "--mode", choices=["encrypt", "decrypt", "crack"])
    parser.add_argument("-t", "--text", help="text to process")
    parser.add_argument("-s", "--shift", type=int, help="integer shift key")
    args = parser.parse_args()

    if args.mode is None:          # no flags -> interactive menu
        menu()
        return

    if args.text is None:
        parser.error("--text is required with --mode")
    if args.mode in ("encrypt", "decrypt") and args.shift is None:
        parser.error("--shift is required for encrypt/decrypt")

    if args.mode == "encrypt":
        print(encrypt(args.text, args.shift))
    elif args.mode == "decrypt":
        print(decrypt(args.text, args.shift))
    else:
        shift, guess = auto_crack(args.text)
        print(f"Best guess (shift {shift}): {guess}")


if __name__ == "__main__":
    main()
