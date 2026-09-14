# Detecting Missing Values with isna()

## Learning objective

Use `isna()`/`isnull()` and column-level summaries to find and count missing
values in a pandas DataFrame.

## Prerequisites

- Basic Python: variables, functions, lists, running a `.py` script.
- No prior pandas experience is required for this lesson.
- A working Python 3.11+ environment with `pandas` installed.

## Concept

Every night, the newsletter platform's signup form exports a file called
`subscribers.csv`. Some rows have a blank `name` or `referral_source` because
those fields are optional on the form, and visitors often skip them. Blank
values in a CSV become **missing values** once pandas loads them into a
DataFrame - pandas represents them as `NaN` (Not a Number), regardless of
whether the original column held text or numbers.

Missing values are dangerous precisely because they are invisible if you do
not look for them. A missing `name` will not crash your script, but it will
quietly produce a broken welcome email ("Hi ,") or a wrong subscriber count if
you filter or group by that column later.

pandas gives you two equivalent methods to detect missing values:

- `DataFrame.isna()` returns a same-shaped DataFrame of booleans, `True`
  wherever a value is missing.
- `DataFrame.isnull()` is an alias for `isna()` - they behave identically.
  This course uses `isna()` for consistency, but you will see `isnull()` in
  other codebases and pandas documentation.

You rarely want the full boolean grid by itself. Combine `isna()` with
`sum()` to get a per-column count of missing values, or with `any()` to get
a per-column or per-row `True`/`False` flag.

## Architecture or data flow

```text
subscribers.csv (raw nightly export)
        |
        v
pd.read_csv("subscribers.csv")
        |
        v
DataFrame in memory
        |
        v
df.isna()              -> boolean grid, same shape as df
df.isna().sum()        -> missing-value count per column
df.isna().sum(axis=1)  -> missing-value count per row
        |
        v
Inspection / reporting step
(this lesson stops here - lesson 2 acts on what you find)
```

At this stage you are only *observing* the data. Nothing is filled or
dropped yet - that comes in the next lesson, once you know exactly which
columns and how many rows are affected.

## Practical example

Assume `subscribers.csv` has columns `email`, `name`, `referral_source`, and
`signup_date`, and looks like this:

```csv
email,name,referral_source,signup_date
amina@example.com,Amina,newsletter-ad,2026-01-04
,Boris,,2026-01-04
carla@example.com,,social,2026-01-05
carla@example.com,Carla,social,2026-01-05
```

Load it and inspect missing values column by column:

```python
import pandas as pd

df = pd.read_csv("subscribers.csv")

# Boolean grid: True wherever a value is missing
missing_grid = df.isna()

# How many missing values does each column have?
missing_per_column = df.isna().sum()
print(missing_per_column)
# email              1
# name               1
# referral_source    1
# signup_date        0
# dtype: int64

# Which rows have at least one missing value?
rows_with_any_missing = df[df.isna().any(axis=1)]
print(rows_with_any_missing)

# Rows missing specifically the email (the field this course treats as
# required, per the course's validation criteria)
rows_missing_email = df[df["email"].isna()]
print(rows_missing_email)
```

`df.isna().sum()` is the single most useful line in this lesson: run it on
any new file before writing a single line of cleaning code, so your cleaning
strategy is based on facts, not assumptions.

## Common mistakes

- **Confusing missing values with the string `"NaN"` or empty string `""`.**
  `isna()` only detects pandas' internal missing marker (created from blank
  CSV cells, `None`, or actual `NaN`). A literal string like `"N/A"` typed
  into the form will *not* be flagged by `isna()` unless you first tell
  `read_csv()` to treat it as missing (for example, via `na_values`).
- **Checking only `df.isna().sum()` and stopping there.** A zero on
  `email` does not mean the file is clean - it only means the `email` column
  has no missing values. You still need to check other columns, and later,
  duplicates.
- **Using `== None` or `== "NaN"` to detect missing values.** This does not
  work reliably in pandas; always use `isna()`/`isnull()`, or their opposite,
  `notna()`/`notnull()`.
- **Forgetting `axis=1` when you want per-row counts.** `df.isna().sum()`
  without an axis argument sums down each column (per-column counts), not
  across each row.

## Mini exercise

Using the sample `subscribers.csv` shown in the practical example above (or
recreate it as a small CSV file yourself):

1. Load the file into a DataFrame called `df`.
2. Print the number of missing values per column using `isna()` and `sum()`.
3. Print only the rows where `email` is missing.
4. Print how many rows in total have at least one missing value, in any
   column, using `any(axis=1)`.

## Expected result

Running your script should print something equivalent to:

```text
email              1
name               1
referral_source    1
signup_date        0
dtype: int64

                name referral_source signup_date  email
1               Boris             NaN  2026-01-04    NaN

Rows with at least one missing value: 2
```

The exact formatting can vary, but the counts must match: 1 missing `email`,
1 missing `name`, 1 missing `referral_source`, 0 missing `signup_date`, and 2
rows total with at least one missing value.

## Summary

`isna()` (and its alias `isnull()`) turns "is this file clean?" from a guess
into a measurable fact. Combined with `sum()` and `any(axis=1)`, it tells you
exactly which columns and rows are affected by missing data before you decide
what to do about it. For the newsletter subscriber file, this means knowing
precisely how many rows have a blank `email`, `name`, or `referral_source`
before writing any cleaning logic.

## Next step

Now that you can find missing values, the next lesson shows you how to act on
them deliberately - dropping rows where a required field like `email` is
missing, and filling optional fields like `name` and `referral_source` with a
default value, using `dropna()` and `fillna()`.
