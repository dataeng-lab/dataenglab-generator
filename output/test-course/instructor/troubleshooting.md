# Troubleshooting: Validate and Clean CSV Data with Python

## `ModuleNotFoundError: No module named 'pandas'`
The environment's dependencies were not installed. Run `pip install -r student-lab/requirements.txt` inside the active virtual environment.

## `ValueError: The truth value of a Series is ambiguous`
The student used Python's `and`/`or` keywords on pandas boolean Series instead of the vectorized operators `&`/`|`. Point them to Lesson 2's example and remind them to wrap each condition in parentheses when combining with `&`/`|` (operator precedence differs from `and`/`or`).

## `NotImplementedError: Implement validate_orders` (or `deduplicate_orders`)
Expected — this is the starter file's placeholder for an unfinished TODO. Not a bug; the student has not yet implemented that function.

## `ModuleNotFoundError: No module named 'clean_orders'` when running pytest
The test file inserts `student-lab/starter` onto `sys.path` using a path relative to the test file itself, so this should not happen if the folder structure is intact. If it does, check that `student-lab/starter/clean_orders.py` was not renamed or moved, and that pytest is being run from within the `student-lab` folder as documented in the README.

## Tests report wrong row counts (not 5 clean / 4 quarantine)
Almost always one of:
- `unit_price` compared with `== None` instead of `.isna()` — missing prices are not flagged as invalid.
- Only one of the two invalid conditions (price or quantity) is checked.
- Deduplication done with the wrong `subset` (e.g. deduplicating on the whole row instead of `order_id`), or `keep` set incorrectly.

Ask the student to print `quarantine_df["order_id"].tolist()` and `clean_df["order_id"].tolist()` and compare against the "Expected numbers" section of `instructor-guide.md`.

## `SettingWithCopyWarning` printed during the run
Harmless for this lab's grading (tests still pass), but indicates a DataFrame slice was modified without `.copy()` first. Point the student to the `.copy()` calls in the lesson's practical example.

## `FileNotFoundError` when running `python starter/clean_orders.py` directly
The script resolves `datasets/orders.csv` relative to its own file location (`Path(__file__).resolve().parent`), so this should only happen if the folder was restructured or a file was deleted after extracting the ZIP. Confirm `student-lab/datasets/orders.csv` still exists.

## Windows-specific: `UnicodeDecodeError` reading the CSV
Not expected with the shipped dataset (plain ASCII, UTF-8/CSV-safe), but if a student replaces the dataset with their own file containing non-UTF-8 characters, have them re-save it as UTF-8, or pass `encoding="utf-8"` explicitly to `pd.read_csv`.
