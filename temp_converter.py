"""temp_converter.py — Temperature converter using an argparse CLI.

Concepts taught here:
- argparse: the standard library way to build command-line tools
- functions with type hints
- a simple "dispatch" pattern (mapping names to functions)

Run it like:
    python temp_converter.py 100 --from C --to F
    python temp_converter.py 32 --from F --to K
"""

import argparse


# Every converter goes *through* Celsius as a common middle step.
# This keeps the logic simple: we only need "X -> Celsius" and
# "Celsius -> X" formulas instead of one formula for every pair.

def to_celsius(value: float, unit: str) -> float:
    """Convert a value in the given unit into Celsius."""
    if unit == "C":
        return value
    if unit == "F":
        return (value - 32) * 5 / 9
    if unit == "K":
        return value - 273.15
    raise ValueError(f"Unknown unit: {unit}")


def from_celsius(celsius: float, unit: str) -> float:
    """Convert a Celsius value into the given unit."""
    if unit == "C":
        return celsius
    if unit == "F":
        return celsius * 9 / 5 + 32
    if unit == "K":
        return celsius + 273.15
    raise ValueError(f"Unknown unit: {unit}")


def convert(value: float, from_unit: str, to_unit: str) -> float:
    """Convert between any two supported units (C, F, K)."""
    celsius = to_celsius(value, from_unit)
    return from_celsius(celsius, to_unit)


def main() -> None:
    # ArgumentParser reads sys.argv for us and generates --help automatically.
    parser = argparse.ArgumentParser(description="Convert temperatures between C, F and K.")
    parser.add_argument("value", type=float, help="The temperature value to convert.")
    # choices=[...] makes argparse reject anything that isn't in the list.
    parser.add_argument("--from", dest="from_unit", choices=["C", "F", "K"],
                        default="C", help="Unit to convert from (default: C).")
    parser.add_argument("--to", dest="to_unit", choices=["C", "F", "K"],
                        default="F", help="Unit to convert to (default: F).")

    args = parser.parse_args()
    result = convert(args.value, args.from_unit, args.to_unit)

    # :.2f formats the number to 2 decimal places.
    print(f"{args.value}°{args.from_unit} = {result:.2f}°{args.to_unit}")


# This guard means main() only runs when the file is executed directly,
# not when it is imported by another script.
if __name__ == "__main__":
    main()
