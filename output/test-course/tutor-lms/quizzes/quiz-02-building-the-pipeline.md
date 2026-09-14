# Quiz: Building the Pipeline

## Question 1
- Type: Multiple choice
- Difficulty: Medium
- Related lesson: 03-building-a-clean-quarantine-pipeline
- Question: In the pipeline, in what order should validation and deduplication run?
- Options:
  A. Deduplicate first, then validate.
  B. Validate first, then deduplicate the valid rows.
  C. Order does not matter.
  D. Run both at the same time on the raw file.
- Correct answer: B
- Explanation: Validating first ensures duplicate detection only considers trustworthy rows, so an invalid row can't "protect" a later valid one from being treated as canonical.

## Question 2
- Type: Multiple choice
- Difficulty: Medium
- Related lesson: 03-building-a-clean-quarantine-pipeline
- Question: An order's `order_id` appears twice, both times with valid, identical data. What should happen to the second occurrence?
- Options:
  A. It is written to `quarantine_orders.csv` because it is a duplicate.
  B. It is dropped and does not appear in either output file.
  C. It is written to `clean_orders.csv` as well, doubling the total.
  D. The whole file is rejected.
- Correct answer: B
- Explanation: A duplicate of an already-valid row is redundant, not invalid data — it is dropped during deduplication and does not appear in either output file.

## Question 3
- Type: True/False
- Difficulty: Easy
- Related lesson: 03-building-a-clean-quarantine-pipeline
- Question: In a correct implementation, every row from the input file ends up in exactly one of the two output files (clean or quarantine), except duplicates which are dropped.
- Options:
  A. True
  B. False
- Correct answer: A
- Explanation: Each raw row is either invalid (quarantined), a duplicate of a valid row (dropped), or valid and unique (clean) — nothing silently disappears without explanation.

## Question 4
- Type: Multiple choice
- Difficulty: Hard
- Related lesson: 03-building-a-clean-quarantine-pipeline
- Question: Why does the lesson recommend splitting the pipeline into `load_orders`, `validate_orders`, `deduplicate_orders` and `write_outputs` instead of one large function?
- Options:
  A. It runs faster.
  B. Tutor LMS requires four functions per lesson.
  C. Each function can be tested in isolation with small, known inputs.
  D. pandas requires functions to be under 10 lines.
- Correct answer: C
- Explanation: Small, single-purpose functions can be unit tested independently, which is exactly how the lab's automated test suite verifies the solution.
