# Quiz: Validation Concepts

## Question 1
- Type: Multiple choice
- Difficulty: Easy
- Related lesson: 01-why-data-validation-matters
- Question: A raw orders file has a row with an empty `unit_price`. What is the correct handling according to the lesson?
- Options:
  A. Treat the missing price as `0` and continue.
  B. Quarantine the row and keep processing the rest of the file.
  C. Drop the row silently with no record.
  D. Stop the whole pipeline run.
- Correct answer: B
- Explanation: Invalid rows must be set aside for review, not guessed at, silently dropped, or allowed to crash the whole run.

## Question 2
- Type: Multiple choice
- Difficulty: Easy
- Related lesson: 01-why-data-validation-matters
- Question: Why is treating a missing price as `0` a mistake?
- Options:
  A. It makes the file larger.
  B. It hides the data quality problem instead of surfacing it, corrupting downstream reports silently.
  C. pandas does not allow zero values.
  D. It is slower than quarantining.
- Correct answer: B
- Explanation: A silent default value looks like real data to any downstream report, masking the underlying issue.

## Question 3
- Type: True/False
- Difficulty: Medium
- Related lesson: 02-detecting-invalid-and-duplicate-records
- Question: `df["unit_price"] == None` correctly detects missing values in a pandas column.
- Options:
  A. True
  B. False
- Correct answer: B
- Explanation: Missing numeric values in pandas are represented as `NaN`, and `NaN` never equals anything with `==`, including `None`. Use `.isna()` instead.

## Question 4
- Type: Multiple choice
- Difficulty: Medium
- Related lesson: 02-detecting-invalid-and-duplicate-records
- Question: Given `invalid_mask = price_invalid | quantity_invalid`, what does `df[~invalid_mask]` return?
- Options:
  A. The rows that are invalid.
  B. The rows that are valid.
  C. Only the duplicate rows.
  D. An error, because `~` cannot be applied to a pandas Series.
- Correct answer: B
- Explanation: `~` inverts a boolean mask, so `~invalid_mask` selects every row that is NOT invalid, i.e. the valid rows.
