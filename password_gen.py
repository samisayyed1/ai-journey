"""password_gen.py — Configurable password generator.

Concepts taught here:
- the `secrets` module (cryptographically secure randomness — better than `random`
  for anything security-related)
- building character pools from `string` constants
- argparse flags that turn features on/off (store_true)

Run it like:
    python password_gen.py
    python password_gen.py --length 24
    python password_gen.py --length 16 --no-symbols
    python password_gen.py --length 12 --count 5
"""

import argparse
import secrets
import string


def build_alphabet(use_upper: bool, use_lower: bool,
                   use_digits: bool, use_symbols: bool) -> str:
    """Assemble the pool of characters a password may be drawn from."""
    alphabet = ""
    if use_lower:
        alphabet += string.ascii_lowercase   # "abc...z"
    if use_upper:
        alphabet += string.ascii_uppercase   # "ABC...Z"
    if use_digits:
        alphabet += string.digits            # "0123456789"
    if use_symbols:
        alphabet += "!@#$%^&*()-_=+[]{};:,.?"

    if not alphabet:
        # Defensive check: if the user disabled every category there is
        # nothing to choose from, so we fail loudly instead of silently.
        raise ValueError("No character types selected — cannot generate a password.")
    return alphabet


def generate_password(length: int, alphabet: str) -> str:
    """Pick `length` random characters from `alphabet`."""
    # secrets.choice() is the secure equivalent of random.choice().
    return "".join(secrets.choice(alphabet) for _ in range(length))


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate one or more random passwords.")
    parser.add_argument("--length", type=int, default=16, help="Password length (default: 16).")
    parser.add_argument("--count", type=int, default=1, help="How many passwords to generate (default: 1).")
    # store_true flags default to False and become True only when passed.
    parser.add_argument("--no-upper", action="store_true", help="Exclude uppercase letters.")
    parser.add_argument("--no-lower", action="store_true", help="Exclude lowercase letters.")
    parser.add_argument("--no-digits", action="store_true", help="Exclude digits.")
    parser.add_argument("--no-symbols", action="store_true", help="Exclude symbols.")

    args = parser.parse_args()

    if args.length < 1:
        parser.error("--length must be at least 1")

    alphabet = build_alphabet(
        use_upper=not args.no_upper,
        use_lower=not args.no_lower,
        use_digits=not args.no_digits,
        use_symbols=not args.no_symbols,
    )

    for _ in range(args.count):
        print(generate_password(args.length, alphabet))


if __name__ == "__main__":
    main()
