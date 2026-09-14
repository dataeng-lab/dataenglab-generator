# Quiz: Duplicates and Pipelines

## Question 1
- Type: Multiple choice
- Difficulty: Easy
- Related lesson: 03-finding-and-removing-duplicate-rows
- Question: What does `df.duplicated(subset=["customer_email", "survey_date"])` flag as a duplicate?
- Options:
  A. Only rows that are identical across every single column.
  B. Rows that share the same customer_email and survey_date, even if other columns (like rating) differ.
  C. Rows where customer_email is missing.
  D. Nothing — duplicated() requires no subset argument to work at all.
- Correct answer: B
- Explanation: Passing `subset` narrows the comparison to just the listed columns, so two rows sharing the same customer_email and survey_date are flagged as duplicates of each other even if the rest of the row (like a corrected rating) is different.

## Question 2
- Type: Multiple choice
- Difficulty: Medium
- Related lesson: 03-finding-and-removing-duplicate-rows
- Question: A customer submits feedback, then resubmits a corrected answer for the same date. Which `keep` value for `drop_duplicates()` keeps the corrected (later) submission, assuming the DataFrame is sorted ascending by submission order first?
- Options:
  A. keep="first"
  B. keep="last"
  C. keep=False
  D. keep is not needed; the default already does this.
- Correct answer: B
- Explanation: After sorting ascending by submission order, `keep="last"` keeps the row that comes later in that order for each duplicate group — the corrected resubmission. The default, `keep="first"`, would keep the original, wrong answer instead.

## Question 3
- Type: True/False
- Difficulty: Medium
- Related lesson: 03-finding-and-removing-duplicate-rows
- Question: `keep=False` in `drop_duplicates()` keeps one row from each duplicate group — whichever one is more complete.
- Options:
  A. True
  B. False
- Correct answer: B
- Explanation: `keep=False` drops every row that is part of a duplicate group, keeping none of them. To keep exactly one row per group, use `keep="first"` or `keep="last"` instead.

## Question 4
- Type: Multiple choice
- Difficulty: Medium
- Related lesson: 04-building-a-clean-data-pipeline
- Question: Why is it useful to write `drop_missing_required()`, `fill_optional_nulls()`, and `deduplicate_submissions()` as three separate functions instead of one long function?
- Options:
  A. pandas requires each cleaning step to be its own function or it raises an error.
  B. Separate functions run faster because pandas parallelizes across functions automatically.
  C. Each function can be called and tested on its own, and the pipeline's step order becomes an explicit, readable list of calls.
  D. There is no real benefit; it is purely a stylistic preference with no testing impact.
- Correct answer: C
- Explanation: Small, single-purpose functions can each be unit tested in isolation (as the lab's test suite does), and chaining them in `clean_pipeline()` makes the required order of operations explicit and easy to read, instead of buried inside one large block.

## Question 5
- Type: Multiple choice
- Difficulty: Hard
- Related lesson: 04-building-a-clean-data-pipeline
- Question: A pytest test function ends with `assert len(cleaned_df) == 12`, but the pipeline actually produces 13 rows. What happens when you run `python -m pytest tests/ -q`?
- Options:
  A. pytest silently ignores the mismatch and reports success.
  B. pytest reports that test as failed and the overall pytest process exits with a non-zero status code.
  C. pytest raises an uncatchable crash that stops the whole test file from running any other tests.
  D. pandas automatically fixes the row count to match the assertion.
- Correct answer: B
- Explanation: A failed `assert` inside a pytest test function makes pytest report that specific test as FAILED and, after running the remaining tests, exit with a non-zero status code — the signal a validation script or CI system checks to know the lab isn't solved correctly yet.
