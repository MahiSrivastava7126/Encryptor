# Caesar Cipher Toolkit (Python)

A beginner-friendly cybersecurity project: encrypt and decrypt text with the
Caesar cipher, see why it is insecure by cracking it, and explore the Vigenere
cipher as an upgrade.

## Features
- Encrypt / decrypt with any integer shift (positive, negative, > 26)
- Preserves uppercase, lowercase, spaces, digits and symbols
- Uses `ord()`, `chr()` and modular arithmetic (`% 26`)
- Cryptanalysis: brute force + frequency analysis (no key needed)
- Vigenere cipher implementation
- Interactive menu **and** command-line flags
- Unit tests (standard library `unittest`)

## Project structure
```
caesar-cipher-project/
├── main.py                    # CLI / interactive menu
├── caesar_cipher/
│   ├── __init__.py
│   ├── caesar.py              # E(x)=(x+n)%26, D(x)=(x-n)%26
│   ├── vigenere.py            # polyalphabetic improvement
│   └── cryptanalysis.py       # brute force + frequency analysis
├── tests/
│   ├── __init__.py
│   └── test_caesar.py
├── docs/THEORY.md             # IPO, formulas, complexity, weaknesses
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

## Run it
```bash
python main.py                                    # interactive menu
python main.py -m encrypt -t "Hello, World!" -s 3 # Khoor, Zruog!
python main.py -m decrypt -t "Khoor, Zruog!" -s 3 # Hello, World!
python main.py -m crack   -t "Khoor Zruog"        # no key needed
```

## Run the tests
```bash
python -m unittest discover -s tests -t . -v
```

## Theory
See [docs/THEORY.md](docs/THEORY.md) for the IPO model, formulas, time
complexity, why Caesar is weak, and suggested improvements.

## Disclaimer
Educational use only. The Caesar and Vigenere ciphers are **not secure**.
For real data use AES-GCM or ChaCha20-Poly1305 from a vetted library.

## License
MIT
