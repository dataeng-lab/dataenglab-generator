# Instructor Guide: Validate and Clean CSV Data with Python

## Course summary
A 1-hour beginner course: 3 short lessons + 2 quizzes covering why/how to validate CSV data with pandas, followed by a 40-minute practical lab where students implement a clean/quarantine/deduplicate pipeline for a bookstore orders file.

## Timing (suggested)
- Lessons 1–2 + Quiz 1: ~17 minutes.
- Lesson 3 + Quiz 2: ~13 minutes.
- Lab: ~40 minutes (this is the graded deliverable).

Total: ~70 minutes including quizzes; the course overview states "1 hour" as the core lesson+lab time and quizzes as light checkpoints — adjust live-session pacing as needed.

## How grading works
Students complete `student-lab/starter/clean_orders.py` and run:
```bash
pytest student-lab/tests/
```
A fully correct solution passes all 8 tests in `test_clean_orders.py`. There is no partial-credit mechanism built in — treat each failing test as one gap in the implementation to discuss with the student.

## Reference solution
`instructor/solution/clean_orders.py` is the complete, correct implementation. To verify it independently:
```bash
cd output/test-course
python -m pytest student-lab/tests/test_clean_orders.py --override-ini="python_files=test_*.py" -q
```
(the test file imports whatever is in `student-lab/starter/`, so to grade the *instructor* solution specifically, temporarily copy `instructor/solution/clean_orders.py` over `student-lab/starter/clean_orders.py` in a scratch copy of the repo — never overwrite the shipped starter file, since it must keep its TODOs for students).

## Expected numbers (deterministic dataset)
Given the fixed `datasets/orders.csv` (10 rows):
- Quarantined: order IDs `1002` (missing price), `1003` (negative quantity), `1006` (zero quantity), `1007` (missing price) → 4 rows.
- Valid candidates before dedup: `1001, 1004, 1004, 1005, 1008, 1009` → 6 rows.
- Clean (after dedup): `1001, 1004, 1005, 1008, 1009` → 5 rows.

If a student's output differs from these counts, the bug is almost always one of:
- Using `and`/`or` instead of `&`/`|` on pandas Series (raises `ValueError: The truth value of a Series is ambiguous`).
- Comparing to `None` instead of using `.isna()`.
- Deduplicating before validating (usually still produces the right count here since duplicates are valid+identical, but the correct order of operations should still be checked in code review).
- Forgetting `.copy()`, which does not break the tests but triggers `SettingWithCopyWarning` — worth mentioning if a student asks about the warning.

## Discussion points for review
- Ask students why quarantine is preferred over silently dropping invalid rows (traceability, ability to fix and reprocess upstream).
- Ask why validation must run before deduplication in this design.
- Ask what would happen to the pipeline if `orders.csv` had a completely missing `unit_price` column rather than empty values (it would raise a `KeyError` — out of scope for this beginner lab, good discussion seed for a follow-up course).

## Common student questions
- "Why not just use `df.dropna()`?" — it would drop the whole row on any missing value in any column, and it does not separate "invalid" from "duplicate," losing the audit trail the business needs.
- "Why `keep='first'` and not `keep='last'`?" — either is a defensible business rule; this course fixes on `first` (first-seen wins) and the tests assert that specific behavior.
