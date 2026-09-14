# Practical Lab: Clean the Bookstore Orders File

## Business context
A small online bookstore receives a daily CSV export of book orders from its e-commerce platform (`datasets/orders.csv`). The export regularly contains rows with a missing unit price, a zero or negative quantity, and duplicated order IDs caused by webhook retries. The reporting team cannot trust the numbers until the file is validated and cleaned.

## Learning objectives
By the end of this lab you will be able to:
- Detect rows with missing or invalid required fields using pandas boolean masks.
- Separate invalid rows into a quarantine file instead of dropping or crashing on them.
- Deduplicate valid rows deterministically by a business key (`order_id`).
- Verify a small data pipeline with an automated test suite.

## Environment
- Python 3.11 or later (any recent Python 3 works).
- Packages listed in `requirements.txt` (`pandas`, `pytest`).
- No Docker required for this lab — it is a plain Python script.
- Works on Windows, macOS and Linux. No credentials and no machine-specific paths are used anywhere in this lab.

Setup:
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

## Estimated duration
40 minutes.

## Starter files
```text
starter/
└── clean_orders.py   # complete the 5 TODOs — do not rename functions
```

## Dataset
`datasets/orders.csv` — 10 fixed, deterministic rows. Columns: `order_id`, `book_title`, `quantity`, `unit_price`, `order_date`. It intentionally contains:
- 2 rows with a missing `unit_price`.
- 1 row with a negative `quantity`.
- 1 row with a `quantity` of `0`.
- 1 duplicated `order_id` (appears twice, identical data).

## Tasks
1. Open `starter/clean_orders.py`.
2. Implement `validate_orders(df)`: build a mask for rows with a missing/non-positive `unit_price`, a mask for rows with a non-positive `quantity`, combine them, and return `(valid_rows, invalid_rows)`.
3. Implement `deduplicate_orders(df)`: remove rows with a repeated `order_id`, keeping the first occurrence.
4. Run the script: `python starter/clean_orders.py`. It writes `clean_orders.csv` and `quarantine_orders.csv` into `student-lab/output/`.
5. Run the tests until they all pass (see Validation below).

## Hints
- `df["unit_price"].isna()` finds missing prices; `NaN == None` is always `False`, so never compare with `==`.
- Combine two boolean masks with `|` (or) / `&` (and) — not the Python keywords `or` / `and`.
- `~mask` inverts a boolean mask.
- `df.drop_duplicates(subset=["order_id"], keep="first")` does the deduplication in one call.
- Validate before you deduplicate, not after.

## Validation
From `student-lab/`, run:
```bash
pytest tests/
```
All tests must pass (exit status 0). The tests import `starter/clean_orders.py` directly and check both the returned DataFrames and the files written to a temporary directory — they do not depend on you running `python starter/clean_orders.py` first.

## Expected output
- `clean_orders.csv`: 5 rows — order IDs `1001, 1004, 1005, 1008, 1009` (each appearing once).
- `quarantine_orders.csv`: 4 rows — order IDs `1002, 1003, 1006, 1007`.
- `pytest tests/` reports all tests passed.

## Reset procedure
To start over: delete `student-lab/output/` (if created) and revert `starter/clean_orders.py` to its original TODO state from version control, or re-extract the student ZIP package.

## Troubleshooting
See `../instructor/troubleshooting.md` for common errors and fixes (instructor-only; not shipped in the student ZIP).

## Instructor solution
Not included in this folder. See `instructor/solution/` in the course package (instructor-only; excluded from the student ZIP).
