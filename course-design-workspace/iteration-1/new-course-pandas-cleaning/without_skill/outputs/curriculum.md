# Curriculum: Pandas Data Cleaning Basics

Tutor LMS structure: **Course > Topics > Lessons > Quizzes**. No Tutor LMS
Pro features required.

## Topic 1: Understanding and Handling Missing Data

Total: 20 min lecture, 18 min practical.

### Lesson 1.1 — Why Nulls and Duplicates Break Analysis
- File: `lessons/01-why-nulls-and-duplicates-break-analysis.md`
- Objective: Explain how unnoticed missing values and duplicate rows
  silently distort counts, averages, and downstream reports.
- Time: 12 min lecture, 3 min practical.

### Lesson 1.2 — Finding and Handling Missing Values with pandas
- File: `lessons/02-finding-and-handling-missing-values.md`
- Objective: Detect missing values with `isna()` and apply `dropna()` or
  `fillna()` based on whether a column is required or optional.
- Time: 8 min lecture, 15 min practical.

### Quiz 1 — Missing Data
- File: `quizzes/quiz-01-missing-data.md`
- Covers Lessons 1.1 and 1.2.

## Topic 2: Deduplicating and Shipping Clean Data

Total: 14 min lecture, 38 min practical.

### Lesson 2.1 — Finding and Removing Duplicate Rows with pandas
- File: `lessons/03-finding-and-removing-duplicate-rows.md`
- Objective: Detect duplicate rows with `duplicated()` and remove them
  deterministically with `drop_duplicates()`, choosing which occurrence
  to keep.
- Time: 8 min lecture, 15 min practical.

### Lesson 2.2 — Building a Clean, Validated Data-Cleaning Pipeline
- File: `lessons/04-building-a-clean-data-pipeline.md`
- Objective: Combine null-handling and deduplication into one small
  pipeline script and validate its output with pytest.
- Time: 6 min lecture, 23 min practical (includes the practical lab).

### Quiz 2 — Duplicates and Pipelines
- File: `quizzes/quiz-02-duplicates-and-pipeline.md`
- Covers Lessons 2.1 and 2.2.

## Totals

- Lecture: 34 minutes.
- Practical: 56 minutes.
- Total: 90 minutes.
- Practical share: 56 / 90 = **62%** (meets the 50% minimum).

## Practical lab

Lesson 2.2's practical time is spent in the course's one practical lab:
`../student-lab/README.md` — "Cleaning GreenLeaf Analytics Customer
Feedback". See that README for the full task list, dataset description,
hints, expected output, and validation commands.
