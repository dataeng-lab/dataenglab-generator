# Practical Lab: Clean the Newsletter Subscriber Export

## Business context
A small online newsletter platform exports its subscriber signup list from a
web form to a CSV file every night (`datasets/subscribers.csv`). The export
regularly contains rows with a missing email address (a rare client-side bug
lets the form submit without one), and it contains duplicate rows for the
same email address because the signup form silently retries when a visitor
double-clicks "Subscribe". The optional `name` and `referral_source` fields
are sometimes left blank because the visitor skipped them. The marketing
team cannot count real subscribers or send a clean welcome-email batch until
the file is cleaned.

## Learning objectives
By the end of this lab you will be able to:
- Detect missing values in a DataFrame with `.isna()` / `.notna()`.
- Remove rows with a missing required field (`email`) instead of leaving
  them in the data or crashing on them.
- Fill blank optional fields deliberately with `.fillna()` instead of
  leaving them blank or dropping the whole row.
- Deduplicate rows deterministically by a business key (`email`), keeping
  the earliest signup per subscriber with `.sort_values()` +
  `.drop_duplicates(subset=..., keep="first")`.
- Verify a small data pipeline with an automated test suite.

## Environment
- Python 3.11 or later (any recent Python 3 works).
- Packages listed in `requirements.txt` (`pandas`, `pytest`).
- No Docker required for this lab — it is a plain Python script.
- Works on Windows, macOS and Linux. No credentials and no machine-specific
  paths are used anywhere in this lab.

Setup:
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

## Estimated duration
30 minutes. This is a separate block from the four lessons' own short
mini-exercises (5 minutes each, 20 minutes total, done on small illustrative
examples as part of Lessons 01-04) — it is the capstone integration
exercise, done once, after Lesson 04, that combines all four lessons'
skills on the course's real dataset. 20 (mini-exercises) + 30 (this lab) =
50 practical minutes for the whole course.

## Starter files
```text
starter/
└── clean_subscribers.py   # complete the 4 TODOs — do not rename functions
```

## Dataset
`datasets/subscribers.csv` — 13 fixed, deterministic rows. Columns: `email`,
`name`, `referral_source`, `signup_date`. It intentionally contains:
- 1 row with a missing `email`.
- 2 emails that each appear as an exact duplicate row (`alice@example.com`).
- 3 emails that each appear twice with a different `referral_source` and/or
  `signup_date`, to test the "keep the earliest signup" rule
  (`bob@example.com`, `carol@example.com`, `dave@example.com`,
  `grace@example.com`).
- 2 rows with a blank `name` or blank `referral_source` on the row that ends
  up being kept, to test the "unknown" fill rule.

## Tasks
1. Open `starter/clean_subscribers.py`.
2. Implement `drop_missing_email(df)`. `email` is a required field — a row
   without one cannot go into the clean output. Revisit Lesson 01 for how
   to build a mask that tells you which rows have a value in a column
   versus which ones don't, then use it to keep only the rows you want.
3. Implement `fill_missing_optional_fields(df)`. `name` and
   `referral_source` are optional, but every row in the clean output must
   show the placeholder text `"unknown"` instead of a blank cell when one
   of these was left empty. Lesson 02 covers the pandas method for filling
   missing values, including how to give a *different* fill value per
   column in one call.
4. Implement `deduplicate_subscribers(df)`. Each email must appear exactly
   once in the output, and the row that survives must be that subscriber's
   *earliest* signup — not simply whichever copy happens to appear first in
   the raw file. Lessons 03 and 04 cover finding duplicate rows and
   removing them while controlling which occurrence survives; think about
   what you need to do to the rows *before* removing duplicates so that
   "the one that survives" and "the earliest one" end up being the same
   row.
5. Run the script: `python starter/clean_subscribers.py`. It writes
   `clean_subscribers.csv` and `subscribers_report.txt` into
   `student-lab/output/`.
6. Run the tests until they all pass (see Validation below).

## Hints
- A boolean mask is just a `True`/`False` Series, one value per row. The
  lessons cover the pair of methods pandas gives you for building one out
  of a column's missing/non-missing values — one is the opposite of the
  other.
- The fill method used in Lesson 02 accepts a dictionary of
  `{column: fill_value}`, so a single call can fill several columns with
  different values without touching any other column.
- `run_pipeline()` already calls your three functions in the correct
  order — you do not need to reorder anything yourself, but it is worth
  tracing through by hand what state the DataFrame is in right before each
  of your functions runs.
- Whichever row is physically first for a given key is the one a
  "keep the first occurrence" duplicate-removal call keeps. That means row
  order matters *before* you deduplicate.
- `NaN == None` is always `False` in pandas — never test for missing values
  with `==`.
- Stuck on an exact method or argument name? Re-read the "Practical
  example" section of the matching lesson (01-04) — each one walks through
  the same method on a similar small dataset.

## Validation
From `student-lab/`, run:
```bash
pytest tests/ -q
```
All tests must pass (exit status 0). The tests import
`starter/clean_subscribers.py` directly and check both the returned
DataFrames and the files written to a temporary directory — they do not
depend on you running `python starter/clean_subscribers.py` first.

## Expected output
- `clean_subscribers.csv`: 7 rows, one per unique email —
  `grace@example.com, carol@example.com, alice@example.com,
  bob@example.com, dave@example.com, frank@example.com, heidi@example.com`
  — with no missing `email`, `name`, or `referral_source` values.
- `subscribers_report.txt` reports: 13 rows read, 1 row dropped for a
  missing email, 5 duplicate rows removed, 7 unique subscribers.
- `pytest tests/ -q` reports all tests passed.

## Reset procedure
To start over: delete `student-lab/output/` (if created) and revert
`starter/clean_subscribers.py` to its original TODO state from version
control, or re-extract the student ZIP package.

## Troubleshooting
If you get stuck on an error you can't resolve from the Hints above, ask
your instructor — they have a troubleshooting guide covering the common
mistakes for this exact lab.

## Instructor solution
Not included in this folder or in the student ZIP. Ask your instructor if
you need your work checked against a reference solution.
