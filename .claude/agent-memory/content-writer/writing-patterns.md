# Tutor LMS Writing Patterns

Durable notes for writing DataEngLab course prose and quizzes.

## Alignment Habits

- Treat `course-spec.json` as the single source of truth. If a lesson needs a
  new tool, outcome, or deliverable, the spec should change first.
- Lesson practical examples should prepare students for the final lab. Avoid
  polished examples that teach different function names, schemas, or outputs
  than the lab actually uses.
- If `student-lab/README.md` exists, skim it to avoid naming drift, but do not
  edit lab files from the content-writer agent.

## Validation Habits

- Preserve every required lesson heading from the course output contract; empty
  sections fail validation.
- Quiz questions need unique option letters, at least two options, a matching
  correct-answer letter, a real related lesson ID, and an explanation that
  teaches the concept.
- Prefer concrete files, table names, commands, and data-flow details over
  generic conceptual prose.

## Pandas Cleaning Lesson Pattern

- When a course teaches missing-value + duplicate-row cleaning together
  (isna/isnull, fillna, dropna, duplicated, drop_duplicates), sequence lessons
  as: detect missing -> fix missing -> detect duplicates -> remove
  duplicates. Handle missing values in required key columns (e.g. the column
  used for dedup, like `email`) *before* deduplicating, so dropna doesn't
  interact unpredictably with duplicate comparisons.
- For "keep the earliest/first-by-column row per key" requirements, always
  pair `sort_values(<tiebreak column>)` with
  `drop_duplicates(subset=[...], keep="first")` in examples and exercises.
  `keep="first"` only means "first in current row order", not "first
  chronologically" - the sort step is what makes it deterministic, and this
  is a very natural place for a common-mistakes bullet and a quiz question.
- `isna()` and `isnull()` are aliases; note that in lesson 1 of this kind of
  pair so students aren't confused seeing both across codebases/docs.
