"""expense_tracker.py — A tiny expense tracker using dicts and file I/O.

Concepts taught here:
- representing records as dictionaries
- persisting data to disk as JSON so it survives between runs
- a small command-driven CLI with argparse subcommands

Data is stored in `expenses.json` next to this script. Each expense is a dict:
    {"amount": 12.5, "category": "food", "note": "lunch"}

Run it like:
    python expense_tracker.py add 12.50 food --note "lunch"
    python expense_tracker.py list
    python expense_tracker.py summary
"""

import argparse
import json
from pathlib import Path

# The data file lives next to this script regardless of where you run it from.
DATA_FILE = Path(__file__).with_name("expenses.json")


def load_expenses() -> list[dict]:
    """Load saved expenses, returning an empty list if none exist yet."""
    if not DATA_FILE.exists():
        return []
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def save_expenses(expenses: list[dict]) -> None:
    """Write the full expense list back to disk."""
    DATA_FILE.write_text(json.dumps(expenses, indent=2), encoding="utf-8")


def add_expense(amount: float, category: str, note: str) -> None:
    expenses = load_expenses()
    expenses.append({"amount": amount, "category": category, "note": note})
    save_expenses(expenses)
    print(f"Added: {amount:.2f} ({category}) {note}".rstrip())


def list_expenses() -> None:
    expenses = load_expenses()
    if not expenses:
        print("No expenses recorded yet.")
        return
    # enumerate(..., start=1) gives us a human-friendly 1-based index.
    for i, e in enumerate(expenses, start=1):
        note = f" — {e['note']}" if e["note"] else ""
        print(f"{i:>3}. {e['amount']:>8.2f}  {e['category']}{note}")


def summary() -> None:
    expenses = load_expenses()
    if not expenses:
        print("No expenses recorded yet.")
        return

    # Build a {category: total} dict by accumulating as we loop.
    totals: dict[str, float] = {}
    for e in expenses:
        totals[e["category"]] = totals.get(e["category"], 0) + e["amount"]

    print("Spending by category:")
    for category, total in sorted(totals.items()):
        print(f"  {category:<15} {total:>10.2f}")
    print(f"  {'TOTAL':<15} {sum(totals.values()):>10.2f}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Track expenses from the command line.")
    # Subparsers let one tool expose several commands (add / list / summary).
    sub = parser.add_subparsers(dest="command", required=True)

    add_p = sub.add_parser("add", help="Record a new expense.")
    add_p.add_argument("amount", type=float, help="Amount spent.")
    add_p.add_argument("category", help="Category, e.g. food, travel, rent.")
    add_p.add_argument("--note", default="", help="Optional note.")

    sub.add_parser("list", help="List all recorded expenses.")
    sub.add_parser("summary", help="Show totals grouped by category.")

    args = parser.parse_args()

    if args.command == "add":
        add_expense(args.amount, args.category, args.note)
    elif args.command == "list":
        list_expenses()
    elif args.command == "summary":
        summary()


if __name__ == "__main__":
    main()
