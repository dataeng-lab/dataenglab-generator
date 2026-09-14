# Finding and Handling Missing Values with pandas

## Learning objective
Detect missing values with `isna()` and apply `dropna()` or `fillna()` based on whether a column is required or optional.

## Prerequisites
Lesson 1 (Why Nulls and Duplicates Break Analysis). Basic Python.

## Concept
pandas represents a missing value as `NaN` (from NumPy), regardless of
whether the column holds numbers or text. Two methods are used
constantly to work with it:

- **`df.isna()`** (alias `df.isnull()`) returns a same-shaped DataFrame
  of `True`/`False`, `True` wherever a value is missing. Chaining
  `.sum()` on top (`df.isna().sum()`) counts the missing values per
  column — the first thing to check on any new dataset.
- Once you know *where* the nulls are, you choose one of two tools per
  column, based on what that column means for your task:
  - **`df.dropna(subset=[...])`** removes entire rows that are missing a
    value in any of the listed columns. Use this for **required**
    fields — a row without one is not usable.
  - **`df.fillna(value={...})`** replaces missing values with a value
    you choose (a dict lets you use a different fill value per column).
    Use this for **optional** fields — the row is still useful even
    without that value, so you keep it and fill in a clear placeholder
    instead of leaving `NaN` in the output.

The column, not the row, decides which tool to use. The same row can
have one missing value that gets it dropped (a missing required field)
or, on a different row, a missing value that gets filled (a missing
optional field) — the decision is made independently per column.

## Architecture or data flow
```text
df.isna().sum()
      │
      ▼
 per-column null counts
      │
      ├── required column has nulls  ──▶  df.dropna(subset=[required_cols])
      │
      └── optional column has nulls  ──▶  df.fillna(value={optional_col: placeholder})
```

## Practical example
This example uses a different, smaller dataset than the practical lab —
a newsletter signup export — so you can see the *pattern* here and still
have real work left to do when you apply it to the lab's own dataset.

```python
import pandas as pd

signups = pd.read_csv("signups.csv")
# columns: signup_id, email, plan, referral_source

# Step 1: see where the nulls are.
print(signups.isna().sum())
# email               1
# plan                1
# referral_source     3

# Step 2: required fields -> drop the row if either is missing.
# email identifies the subscriber; plan is what they signed up for.
signups = signups.dropna(subset=["email", "plan"])

# Step 3: optional fields -> fill with a clear placeholder, don't drop.
# referral_source is nice-to-know marketing context, not required.
signups = signups.fillna(value={"referral_source": "Not specified"})

print(signups.isna().sum())  # every column: 0
```

Note the order: required-field dropping happens *before* optional-field
filling. If you filled first, a row missing `plan` would still get
dropped later — the order doesn't change *that* outcome — but it's
clearer and cheaper to drop unusable rows first, before spending work
filling placeholders into rows that are about to be discarded anyway.

## Common mistakes
- Calling `fillna()` on a required column — this "fixes" the null count but manufactures a fake value that shouldn't exist, which is worse than dropping the row.
- Calling `dropna()` with no `subset`, which drops a row if *any* column has a null — including optional ones, discarding perfectly usable rows just because an optional field was blank.
- Forgetting that `fillna(value={...})` only fills the columns you list; columns not in the dict keep their `NaN`s untouched (this is usually what you want, but check `isna().sum()` again after to confirm).
- Checking for missing values with `df["col"] == None` or `== "NaN"` — neither works reliably; always use `isna()`/`notna()`.

## Mini exercise
A different scenario again — an online store's `orders` DataFrame has
columns `customer_id` (required), `total_amount` (required), and
`promo_code` (optional). Write the two lines of code that: (1) drop rows
missing a required field, and (2) fill missing `promo_code` values with
`"none"`.

## Expected result
```python
orders = orders.dropna(subset=["customer_id", "total_amount"])
orders = orders.fillna(value={"promo_code": "none"})
```

## Summary
`isna().sum()` shows you where nulls are, per column. From there,
`dropna(subset=[...])` removes rows missing a required field, and
`fillna(value={...})` fills optional blanks with a clear placeholder —
never the other way around for the same column. The lab asks you to
apply this same pattern to its own dataset and its own required/optional
columns — you'll need to decide the right `subset` and fill values for
that dataset yourself.

## Next step
Lesson 3 moves to the second half of the cleaning problem: finding and
removing duplicate rows with `duplicated()` and `drop_duplicates()`.
