# Quiz 1: Finding and Handling Missing Data

## Question 1
- Type: single choice
- Difficulty: beginner
- Related lesson: 01-detecting-missing-values
- Question: A subscriber's `name` field was left blank in the web form and the row was loaded from `subscribers.csv` into a pandas DataFrame `df`. Which method call correctly detects that this value is missing?
- Options:
  A. `df["name"] == "NaN"`
  B. `df["name"].isna()`
  C. `df["name"] == None`
- Correct answer: B
- Explanation: `isna()` (and its alias `isnull()`) is the correct way to detect pandas' internal missing-value marker. Comparing with `== "NaN"` checks for a literal string, not a real missing value, and comparing with `== None` does not reliably detect missing values in pandas - both are common mistakes covered in lesson 01.

## Question 2
- Type: single choice
- Difficulty: beginner
- Related lesson: 01-detecting-missing-values
- Question: You want to know how many missing values exist in each column of `df`, not just whether any exist. Which line of code gives you that?
- Options:
  A. `df.isna().sum()`
  B. `df.isna().any()`
  C. `df.dropna()`
- Correct answer: A
- Explanation: `df.isna()` produces a boolean grid, and `.sum()` adds up the `True` values down each column, giving a per-column count of missing values. `.any()` only tells you whether a column has at least one missing value (True/False), not how many, and `dropna()` removes rows rather than counting anything.

## Question 3
- Type: single choice
- Difficulty: intermediate
- Related lesson: 02-filling-and-dropping-missing-values
- Question: In the newsletter subscriber scenario, `email` is a required field and `referral_source` is optional. Which approach correctly reflects the course's business rule?
- Options:
  A. Call `df.dropna()` once with no arguments to remove every row with any missing value.
  B. Call `df.dropna(subset=["email"])` to drop rows missing an email, then `df.fillna({"referral_source": "unknown"})` to fill the optional field.
  C. Call `df.fillna("unknown")` on the whole DataFrame so no rows are ever dropped.
- Correct answer: B
- Explanation: Dropping is reserved for the required field (`email`) using a scoped `subset`, while the optional field (`referral_source`) is filled with a placeholder instead of being dropped. Option A would incorrectly drop rows that are only missing the optional field, and option C would incorrectly fill a missing `email` with the text "unknown" instead of removing that unusable row.

## Question 4
- Type: single choice
- Difficulty: intermediate
- Related lesson: 02-filling-and-dropping-missing-values
- Question: What is wrong with the following code, given the course's validation criteria for `clean_subscribers.py`?
  ```python
  df.fillna({"name": "unknown", "referral_source": "unknown"})
  df = df.dropna(subset=["email"])
  ```
- Options:
  A. Nothing is wrong; the order of operations does not matter here.
  B. The result of `fillna()` is discarded because it is not reassigned to `df`, so the fill never actually applies.
  C. `dropna(subset=["email"])` should be replaced with `dropna()` with no arguments.
- Correct answer: B
- Explanation: `fillna()` returns a new DataFrame by default and does not modify `df` in place unless `inplace=True` is passed. Because the first line's result is never assigned back to `df`, the fill is silently lost. The `subset=["email"]` scoping on `dropna()` in the second line is correct as written, so option C would make the code worse, not better.
