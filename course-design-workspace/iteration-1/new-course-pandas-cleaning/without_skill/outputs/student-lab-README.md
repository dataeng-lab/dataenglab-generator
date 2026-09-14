# Practical Lab: Cleaning GreenLeaf Analytics Customer Feedback

**Level:** Beginner · **Duration:** ~25 min (Lesson 4's 23 practical minutes, per `../tutor-lms/curriculum.md`, plus a couple of minutes reading this page) · **Tags:** pandas, null handling, deduplication, pytest

## Business context

GreenLeaf Analytics runs a customer feedback form for a small retail
chain. The raw daily export, `customer_feedback_raw.csv`, comes straight
from the form backend and is messy:

- some customers left the **rating** field blank;
- some entries are missing the **customer_email** needed to identify who
  submitted them;
- some optional fields (**comments**, **region**) are blank;
- a number of customers accidentally **submitted the form twice** for the
  same date — sometimes an exact repeat, sometimes a corrected second
  answer.

Before the weekly satisfaction report can be trusted, this raw export
must be cleaned: rows missing a required field must be removed, optional
blanks must be filled with clear placeholder text instead of staying
null, and duplicate submissions for the same customer and date must be
collapsed down to a single, most-recent row.

Your job: complete `starter/clean_customer_feedback.py` so it reads
`datasets/customer_feedback_raw.csv`, applies these three cleaning steps
in order, and writes `output/clean_feedback.csv`.

## Environment

- Python 3.11 or later.
- Packages listed in `requirements.txt` (`pandas`, `pytest`).
- No Docker required.
- No network access is required once `pip install` has completed. No
  credentials and no machine-specific paths are used anywhere in this lab.

Setup:
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Starter files

```text
starter/
└── clean_customer_feedback.py   # complete the TODOs in Tasks 2-5 - do not rename functions
```

## Dataset

`datasets/customer_feedback_raw.csv` - 20 rows, one per form submission.
Columns: `submission_id`, `customer_email`, `survey_date`, `rating`,
`comments`, `region`.

14 rows are usable as-is or after filling an optional blank. The other 6
are deliberately broken, plus 4 rows are exact-or-corrected duplicates of
an earlier row for the same customer and date:

- `S003` - `rating` is missing (blank field).
- `S006` - `customer_email` is missing (blank field).
- `S012` - `rating` is missing (blank field).
- `S017` - `customer_email` is missing (blank field).
- `S004`, `S010`, `S020` - `comments` is missing (optional - fill, don't drop).
- `S011` - `region` is missing (optional - fill, don't drop).
- `S005` is an exact repeat of `S001` (same `customer_email` and
  `survey_date`) - keep the later one, `S005`.
- `S009` is a corrected second answer from the same customer/date as
  `S008` - keep the later one, `S009`.
- `S014` is an exact repeat of `S013` - keep the later one, `S014`.
- `S019` is a corrected second answer from the same customer/date as
  `S018` - keep the later one, `S019`.

## Tasks

### Task 1 - Inspect the raw export and find the broken rows

Open `datasets/customer_feedback_raw.csv` and, without running any code,
find:
- every row with a missing `rating`,
- every row with a missing `customer_email`,
- every pair of rows that share the same `customer_email` and
  `survey_date`.

Write down their `submission_id`s. You'll use them in Task 6 to
sanity-check your own output.

### Task 2 - Drop rows missing a required field

Implement `drop_missing_required()` in `starter/clean_customer_feedback.py`
so it returns a DataFrame with every row removed that is missing
`customer_email`, `rating`, or both (`REQUIRED_COLUMNS`, defined at the top
of the file, names them). Do not remove a row just because `comments` or
`region` is missing here - those are optional and handled in Task 3.
Lesson 2 covers the pandas DataFrame method built specifically for removing
rows based on which columns have a missing value.

### Task 3 - Fill optional blanks with placeholder text

Implement `fill_optional_nulls()` so every remaining blank in `comments` or
`region` is replaced with the placeholder text defined in
`OPTIONAL_FILL_VALUES` (top of the file) - without dropping any rows, and
without changing `customer_email` or `rating`. Lesson 2 covers the pandas
DataFrame method built for replacing missing values with a value you
choose, including how to pass a different value per column.

### Task 4 - Deduplicate repeat submissions

Implement `deduplicate_submissions()` so that, for every
`(customer_email, survey_date)` pair that appears more than once
(`DEDUPLICATION_KEY`, top of the file), only the most recently submitted
row survives - the one with the higher `submission_id`. You'll need to put
the rows into a meaningful order first, then apply the pandas DataFrame
method built for removing duplicate rows on a subset of columns, choosing
the option that keeps the *last* row in each group rather than the first.
Lesson 3 covers both pieces.

### Task 5 - Wire up the full pipeline

Implement `clean_pipeline()` so it produces the final cleaned DataFrame by
running the four functions above - in the order Lessons 2-3 explained is
necessary (required-field cleanup before anything else; a meaningful sort
before deduplication) - then returns the result sorted by `submission_id`
with a freshly reset index.

### Task 6 - Run the full pipeline and validate

```bash
python clean_customer_feedback.py
```

This prints the cleaned table and writes `output/clean_feedback.csv`.
Check that none of the `submission_id`s you wrote down in Task 1 as
"missing required field" or "earlier duplicate" show up in the output,
then run the automated checks (see **Validation** below).

## Hints

These are nudges, not answers - each leaves at least one real decision for
you to make. If you're not sure which pandas method a hint is pointing at,
re-read the matching lesson before filling in the blanks.

<details>
<summary>Hint for Task 2 (drop missing required fields)</summary>

```python
def drop_missing_required(df):
    return df.____(subset=____)
```
One pandas DataFrame method removes whole rows based on which columns are
missing a value. Which method is it, and which list already defined at the
top of the file names the columns that must never be missing?
</details>

<details>
<summary>Hint for Task 3 (fill optional blanks)</summary>

```python
def fill_optional_nulls(df):
    return df.____(value=____)
```
A different pandas DataFrame method replaces missing values in place
without removing any rows, and accepts a dict mapping each column name to
its own fill value. Which dict, already defined at the top of the file,
already has the right shape for that argument?
</details>

<details>
<summary>Hint for Task 4 (deduplicate)</summary>

```python
def deduplicate_submissions(df):
    sorted_df = df.sort_values(____)
    return sorted_df.____(subset=____, keep=____)
```
Sort ascending by whichever column reflects the order submissions actually
happened in. Then, of the three `keep` options pandas offers
(`"first"`, `"last"`, `False`), which one means "the row that comes later
in that sorted order wins"?
</details>

<details>
<summary>Hint for Task 5 (wire up the pipeline)</summary>

```python
def clean_pipeline(raw_path):
    df = ____(raw_path)
    df = ____(df)
    df = ____(df)
    df = ____(df)
    return df.sort_values("submission_id").reset_index(drop=True)
```
Call the four functions from Tasks 2-4 (plus `load_raw_data`) by name, in
the order Lessons 2-3 explained matters: a row has to survive the
required-field check before it's worth filling in optional blanks for, and
the data has to be sorted before "keep the last one" means anything
chronological.
</details>

## Expected output

`output/clean_feedback.csv` - exactly 12 rows, no blank/NaN cells in any
column, sorted by `submission_id`:

| submission_id | customer_email | survey_date | rating | comments | region |
|---|---|---|---|---|---|
| S002 | bob@example.com | 2026-01-05 | 4 | Good, but slow shipping | West |
| S004 | dave@example.com | 2026-01-06 | 3 | No comment provided | South |
| S005 | alice@example.com | 2026-01-05 | 5 | Great service! | East |
| S007 | erin@example.com | 2026-01-07 | 4 | Solid experience | West |
| S009 | frank@example.com | 2026-01-08 | 5 | Actually it was fine after follow-up | East |
| S010 | grace@example.com | 2026-01-08 | 3 | No comment provided | West |
| S011 | heidi@example.com | 2026-01-09 | 4 | Pretty good | Unknown |
| S014 | judy@example.com | 2026-01-10 | 5 | Excellent! | East |
| S015 | karl@example.com | 2026-01-10 | 2 | Could be better | North |
| S016 | laura@example.com | 2026-01-11 | 4 | Nice | West |
| S019 | mallory@example.com | 2026-01-12 | 3 | Changed my mind | South |
| S020 | nathan@example.com | 2026-01-12 | 4 | No comment provided | North |

## Validation

From `student-lab/`, run:
```bash
python -m pytest tests/ -q
```
Imports `starter/clean_customer_feedback.py` directly and checks that:
the raw dataset loads with 20 rows; `drop_missing_required()` drops
exactly `S003`, `S006`, `S012`, `S017` and leaves no nulls in
`customer_email`/`rating`; `fill_optional_nulls()` leaves no nulls in
`comments`/`region` and does not change `customer_email`/`rating`;
`deduplicate_submissions()` keeps exactly 12 rows, keeping `S009` over
`S008` and dropping `S001`, `S008`, `S013`, `S018`; and the full
`clean_pipeline()` plus `output/clean_feedback.csv` match the expected
result above. Exits non-zero (via pytest) if any check fails.

## Reset procedure

Delete the `output/` directory and re-run Task 6 -
`write_output()`/`to_csv()` always overwrites, so re-running
`python clean_customer_feedback.py` is always safe and never needs a
separate reset script:
```bash
python -c "import shutil; shutil.rmtree('output', ignore_errors=True)"
python clean_customer_feedback.py
```

## Troubleshooting

- **`NotImplementedError` when you run the script** - you haven't
  implemented one of the TODOs yet; the traceback names the function.
- **`output/clean_feedback.csv` has more than 12 rows** - Task 4 is
  probably comparing the wrong set of columns across rows (re-read what
  `DEDUPLICATION_KEY` is meant to represent), or it's finding the
  duplicate rows but not actually removing them from what gets
  returned.
- **`output/clean_feedback.csv` still has blank cells in `comments` or
  `region`** - check that Task 3 is actually *replacing* values in both
  optional columns, not just one of them, and that it runs on the
  output of Task 2 rather than the original raw data.
- **Row `S008` appears instead of `S009`** - Task 4 is keeping the
  *wrong* occurrence within each duplicate group; re-read the "Hint for
  Task 4" above for which sort order and which option make "the one
  that comes later" the one that survives.
- **`pytest` fails with `ModuleNotFoundError: No module named 'pandas'`**
  - you ran `pytest`/`python` from an environment where
  `pip install -r requirements.txt` didn't run; re-activate the virtualenv
  from **Environment** above and reinstall.
- Still stuck after the hints above? Ask your instructor - deeper coaching
  notes for this lab exist, but they live outside the materials shipped to
  students.

## Instructor solution

Not included in this folder or in the student ZIP. If you're taking this
course through an instructor, they have access to a working reference
solution and can help you compare your approach against it.
