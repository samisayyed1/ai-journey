"""word_freq.py — Count how often each word appears in a text file.

Concepts taught here:
- reading files safely with `with open(...)`
- regular expressions to split text into words
- collections.Counter, a dict subclass built for counting

Run it like:
    python word_freq.py book.txt
    python word_freq.py book.txt --top 20
"""

import argparse
import re
from collections import Counter


def count_words(text: str) -> Counter:
    """Return a Counter mapping each lowercased word to its frequency."""
    # \b\w+\b finds runs of "word characters" (letters, digits, underscore).
    # Lowercasing first means "The" and "the" count as the same word.
    words = re.findall(r"\b\w+\b", text.lower())
    return Counter(words)


def main() -> None:
    parser = argparse.ArgumentParser(description="Count word frequencies in a text file.")
    parser.add_argument("path", help="Path to the text file to analyse.")
    parser.add_argument("--top", type=int, default=10,
                        help="How many of the most common words to show (default: 10).")

    args = parser.parse_args()

    # Wrap file access in try/except so a bad path gives a friendly message
    # instead of a raw traceback.
    try:
        with open(args.path, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: file not found — {args.path}")
        return

    counts = count_words(text)
    total = sum(counts.values())
    print(f"Total words: {total} | Unique words: {len(counts)}\n")

    # Counter.most_common(n) returns the n highest-frequency (word, count) pairs.
    for word, count in counts.most_common(args.top):
        print(f"{count:>6}  {word}")


if __name__ == "__main__":
    main()
