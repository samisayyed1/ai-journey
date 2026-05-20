"""json_csv.py — Convert between JSON and CSV, with error handling.

Concepts taught here:
- the `json` and `csv` standard library modules
- inferring the conversion direction from file extensions
- raising and catching errors to fail gracefully

The JSON is expected to be a list of flat objects, e.g.
    [{"name": "Ada", "age": 36}, {"name": "Alan", "age": 41}]
which maps naturally to rows and columns in a CSV.

Run it like:
    python json_csv.py people.json people.csv
    python json_csv.py people.csv people.json
"""

import argparse
import csv
import json
import sys
from pathlib import Path


def json_to_csv(src: Path, dst: Path) -> None:
    """Read a list-of-objects JSON file and write it as CSV."""
    data = json.loads(src.read_text(encoding="utf-8"))

    if not isinstance(data, list) or not data:
        raise ValueError("JSON must be a non-empty list of objects to convert to CSV.")

    # Collect every key seen across all rows so we don't drop columns
    # that only appear in some objects.
    fieldnames: list[str] = []
    for row in data:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)

    with open(dst, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def csv_to_json(src: Path, dst: Path) -> None:
    """Read a CSV file and write it as a list-of-objects JSON file."""
    with open(src, "r", newline="", encoding="utf-8") as f:
        # DictReader turns each row into a dict keyed by the header row.
        rows = list(csv.DictReader(f))

    # indent=2 makes the output human-readable.
    dst.write_text(json.dumps(rows, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert between JSON and CSV.")
    parser.add_argument("source", help="Input file (.json or .csv).")
    parser.add_argument("dest", help="Output file (.csv or .json).")

    args = parser.parse_args()
    src, dst = Path(args.source), Path(args.dest)

    if not src.exists():
        print(f"Error: source file not found — {src}")
        sys.exit(1)

    # Decide direction from the file extensions (case-insensitive).
    src_ext, dst_ext = src.suffix.lower(), dst.suffix.lower()

    try:
        if src_ext == ".json" and dst_ext == ".csv":
            json_to_csv(src, dst)
        elif src_ext == ".csv" and dst_ext == ".json":
            csv_to_json(src, dst)
        else:
            print("Error: unsupported conversion. Use .json -> .csv or .csv -> .json.")
            sys.exit(1)
    except (json.JSONDecodeError, ValueError) as exc:
        # json.JSONDecodeError = malformed JSON; ValueError = our own checks.
        print(f"Error: {exc}")
        sys.exit(1)

    print(f"Converted {src} -> {dst}")


if __name__ == "__main__":
    main()
