# ai-journey
My public build log — 9 months, 12 projects.
Day 1. Started today

---

# Python Learning Scripts

Five small, well-commented Python scripts for going from beginner to intermediate.
Every script uses **only the standard library**, so there is nothing to install —
just Python 3.9+.

Each file is heavily commented to explain the concepts as you read it.

## Setup

```bash
# (optional) create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# nothing to install, but this is the habit to build:
pip install -r requirements.txt
```

---

## 1. `temp_converter.py` — Temperature converter

Converts between Celsius, Fahrenheit and Kelvin using an `argparse` CLI.

**Concepts:** `argparse`, type hints, converting via a common base unit.

```bash
python temp_converter.py 100 --from C --to F      # 100°C = 212.00°F
python temp_converter.py 32 --from F --to K       # 32°F  = 273.15°K
python temp_converter.py 300 --from K --to C      # 300°K = 26.85°C
```

---

## 2. `password_gen.py` — Password generator

Generates secure random passwords with configurable length and character sets.

**Concepts:** the `secrets` module (secure randomness), `string` constants,
on/off CLI flags.

```bash
python password_gen.py                            # 16-char password
python password_gen.py --length 24                # 24-char password
python password_gen.py --length 16 --no-symbols   # letters + digits only
python password_gen.py --length 12 --count 5      # five passwords at once
```

---

## 3. `word_freq.py` — Word frequency counter

Reads any text file and reports the most common words.

**Concepts:** safe file reading with `with`, regular expressions,
`collections.Counter`.

```bash
python word_freq.py book.txt                      # top 10 words
python word_freq.py book.txt --top 20             # top 20 words
```

---

## 4. `json_csv.py` — JSON ⇄ CSV converter

Converts a list-of-objects JSON file to CSV and back, with friendly errors.

**Concepts:** the `json` and `csv` modules, inferring direction from file
extensions, graceful error handling.

```bash
python json_csv.py people.json people.csv         # JSON -> CSV
python json_csv.py people.csv people.json         # CSV  -> JSON
```

Example input (`people.json`):

```json
[{"name": "Ada", "age": 36}, {"name": "Alan", "age": 41}]
```

---

## 5. `expense_tracker.py` — Expense tracker

A tiny expense tracker that saves data to `expenses.json` so it persists
between runs.

**Concepts:** dictionaries as records, JSON persistence, `argparse` subcommands.

```bash
python expense_tracker.py add 12.50 food --note "lunch"
python expense_tracker.py add 40 travel --note "train ticket"
python expense_tracker.py list                    # list every expense
python expense_tracker.py summary                 # totals by category
```

---

## Project files

| File               | Purpose                                  |
|--------------------|------------------------------------------|
| `requirements.txt` | Dependency list (currently empty)        |
| `.gitignore`       | Keeps caches, venvs and local data out of git |
| `README.md`        | This file                                |
