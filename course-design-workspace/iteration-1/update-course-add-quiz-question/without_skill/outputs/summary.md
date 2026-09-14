# Summary: Add quiz question about partition pruning (baseline / no-skill run)

## Task

Add one more quiz question about partition pruning to the
`apache-spark-for-beginners-eval-bl` course (a copy of `apache-spark-for-beginners`
made for this evaluation).

## Setup performed

1. Copied `output/apache-spark-for-beginners/` to
   `output/apache-spark-for-beginners-eval-bl/` (recursive copy of everything).
   The original `output/apache-spark-for-beginners/` was not modified.
2. Edited `output/apache-spark-for-beginners-eval-bl/course-spec.json`, changing
   `"slug": "apache-spark-for-beginners"` to
   `"slug": "apache-spark-for-beginners-eval-bl"`.

## Guidance followed

Read `CLAUDE.md` and every file under `.claude/rules/*.md` (`core.md`,
`course-contract.md`, `elementor.md`, `labs.md`, `publishing.md`,
`validation.md`) for project-specific requirements. Per CLAUDE.md, "Each quiz
question includes type, options, correct answer, explanation, difficulty and
related lesson." I inspected the existing quiz files
(`quiz-01-spark-architecture.md`, `quiz-02-dataframe-operations.md`,
`quiz-03-spark-sql.md`, `quiz-04-building-and-testing-pipelines.md`) as a style
reference and matched their exact Markdown structure (heading level, field
order, option lettering, one-paragraph explanation).

## Where the question was placed and why

The course curriculum never teaches partitioned storage layouts (no
`partitionBy` write or partitioned read is covered). The closest existing
concept is `04-selecting-filtering-deriving-columns` (filtering DataFrames with
`.filter()`), since partition pruning is the query-optimization consequence of
filtering on a partition column. I appended the new question as Question 5
to the end of `quiz-02-dataframe-operations.md` (the quiz already covering
lessons 03-05, including lesson 04), tagged with
`Related lesson: 04-selecting-filtering-deriving-columns`.

## Exact change made

File edited: `output/apache-spark-for-beginners-eval-bl/tutor-lms/quizzes/quiz-02-dataframe-operations.md`

Appended this new question at the end of the file:

```
## Question 5
- Type: Multiple choice
- Difficulty: Medium
- Related lesson: 04-selecting-filtering-deriving-columns
- Question: order_items is stored on disk as a dataset partitioned by order_date (one folder per date, e.g. order_date=2024-01-15/). What does "partition pruning" do when you run df.filter(df.order_date == "2024-01-15")?
- Options:
  A. It converts the DataFrame to a pandas DataFrame before filtering.
  B. It lets Spark skip reading the files in partitions that cannot match the predicate, instead of reading every partition and filtering in memory afterward.
  C. It permanently deletes the non-matching partitions from disk.
  D. It has no effect unless .coalesce(1) is called first.
- Correct answer: B
- Explanation: When a dataset is physically partitioned by a column, Spark's planner can use a filter on that column to skip scanning entire partition directories that cannot contain matching rows, avoiding unnecessary disk I/O. It doesn't move data to pandas, delete anything from disk, or depend on coalesce().
```

## Files touched

- `output/apache-spark-for-beginners-eval-bl/course-spec.json` (slug field only, part of the required setup)
- `output/apache-spark-for-beginners-eval-bl/tutor-lms/quizzes/quiz-02-dataframe-operations.md` (added Question 5)

No other files in the copied course were modified. The original
`output/apache-spark-for-beginners/` directory was left untouched, and
`output/apache-spark-for-beginners-eval-ws/` was not touched.

## Commands actually run and their real results

1. `cp -r output/apache-spark-for-beginners output/apache-spark-for-beginners-eval-bl`
   -> succeeded, no output (directory copy).
2. `ls output/apache-spark-for-beginners-eval-bl` and `ls .../tutor-lms/quizzes`
   -> listed directory contents (exploration only, no state change).
3. `python scripts/run_checks.py output/apache-spark-for-beginners-eval-bl`
   -> ran the full combined checker. Real output:

```
Detected validation mode: course

$ ...\python.exe ...\scripts\validate_spec.py output\apache-spark-for-beginners-eval-bl
OK: ...\output\apache-spark-for-beginners-eval-bl
PASS: ...\scripts\validate_spec.py output\apache-spark-for-beginners-eval-bl

$ ...\scripts\validate_course.py output\apache-spark-for-beginners-eval-bl
OK: ...\output\apache-spark-for-beginners-eval-bl
PASS: ...\scripts\validate_course.py output\apache-spark-for-beginners-eval-bl

$ ...\scripts\validate_content.py output\apache-spark-for-beginners-eval-bl
OK: output\apache-spark-for-beginners-eval-bl
PASS: ...\scripts\validate_content.py output\apache-spark-for-beginners-eval-bl

$ ...\scripts\validate_lab.py output\apache-spark-for-beginners-eval-bl\student-lab
OK: output\apache-spark-for-beginners-eval-bl\student-lab
PASS: ...\scripts\validate_lab.py output\apache-spark-for-beginners-eval-bl\student-lab

$ ...\scripts\validate_lab_execution.py output\apache-spark-for-beginners-eval-bl
OK: instructor solution passes the lab tests - output\apache-spark-for-beginners-eval-bl
PASS: ...\scripts\validate_lab_execution.py output\apache-spark-for-beginners-eval-bl

$ ...\scripts\validate_elementor_json.py output\apache-spark-for-beginners-eval-bl\elementor\landing-page.json
OK: output\apache-spark-for-beginners-eval-bl\elementor\landing-page.json
PASS: ...\scripts\validate_elementor_json.py output\apache-spark-for-beginners-eval-bl\elementor\landing-page.json
ALL CHECKS PASSED
```

This actually executed, including running the instructor's PySpark solution
against pytest in local mode (`validate_lab_execution.py`) - it was not
skipped or assumed.

## Result

`ALL CHECKS PASSED` - real result from `scripts/run_checks.py`, including
content/spec/course structure validation and actual execution of the lab's
`validate.json` setup/validate commands against the instructor solution.

## Constraints honored

- Did not use the `Skill` tool for any skill.
- Did not read any file under `.claude/skills/`.
- Did not modify `output/apache-spark-for-beginners/` (original course).
- Did not touch `output/apache-spark-for-beginners-eval-ws/`.
