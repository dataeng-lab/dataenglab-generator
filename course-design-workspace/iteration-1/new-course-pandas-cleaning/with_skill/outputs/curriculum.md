# Curriculum: Pandas Data Cleaning Basics: Nulls and Duplicates

Total duration: 90 minutes (40 minutes lecture, 50 minutes practical).

The 50 practical minutes are split into two DIFFERENT kinds of practical
time, which are never the same minutes counted twice:
- 20 minutes across the four lessons' own short mini-exercises below (5
  minutes each), each done on a small illustrative example, separate from
  the course's main dataset.
- 30 minutes for the final practical lab (see "Final practical lab" below),
  a separate, longer capstone exercise on the course's real
  `subscribers.csv` dataset.

20 + 30 = 50 practical minutes; 40 + 50 = 90 minutes total.

## Topic 1: Finding and Handling Missing Data

| Lesson ID | Title | Lecture | Mini-exercise (practical) | Practical work |
|---|---|---|---|---|
| `01-detecting-missing-values` | Detecting Missing Values with isna() | 10 min | 5 min | Load a sample subscribers CSV and count missing values per column with `isna()`/`isnull()`. |
| `02-filling-and-dropping-missing-values` | Filling and Dropping Missing Values Deliberately | 10 min | 5 min | Apply a column-specific strategy: `dropna()` on rows with a missing `email`, `fillna("unknown")` on `name` and `referral_source`. |

Topic 1 subtotal: 20 min lecture, 10 min mini-exercise practical (30 min).

Quiz: `quiz-01-missing-values.md` (covers lessons `01-detecting-missing-values`
and `02-filling-and-dropping-missing-values`).

## Topic 2: Detecting and Removing Duplicate Rows

| Lesson ID | Title | Lecture | Mini-exercise (practical) | Practical work |
|---|---|---|---|---|
| `03-detecting-duplicate-rows` | Detecting Duplicate Rows with duplicated() | 10 min | 5 min | Use `duplicated()` with default arguments and with `subset=["email"]` to find exact-row and same-email duplicates in sample signup data. |
| `04-removing-duplicates-deterministically` | Removing Duplicates Deterministically with drop_duplicates() | 10 min | 5 min | Use `drop_duplicates(subset=["email"], keep=...)` after sorting by `signup_date`, to keep the earliest signup per email deterministically. |

Topic 2 subtotal: 20 min lecture, 10 min mini-exercise practical (30 min).

Quiz: `quiz-02-duplicate-rows.md` (covers lessons `03-detecting-duplicate-rows`
and `04-removing-duplicates-deterministically`).

## Final practical lab

30 minutes, AFTER both topics, their mini-exercises, and both quizzes are
done — not included in either topic's subtotal above. Students move to the
practical lab (`student-lab/`), where they combine every technique from all
four lessons into a single script, `clean_subscribers.py`. The script reads
`subscribers.csv` (13 rows, distinct from and larger than the lessons' small
illustrative examples), applies the missing-value strategy from Topic 1 and
the duplicate-removal strategy from Topic 2, and writes
`clean_subscribers.csv` plus a `subscribers_report.txt` summary. The lab is
validated by the `tests/test_clean_subscribers.py` pytest suite described in
the course's validation criteria.

## Total time reconciliation

40 min lecture (10 x 4 lessons) + 10 min Topic 1 mini-exercises + 10 min
Topic 2 mini-exercises + 30 min final lab = 90 minutes total, 50 of which
(55.6%) are practical.

## Ordering note

Lesson order and topic order above match `course-spec.json` exactly. Lesson
IDs, titles, and quiz filenames are not renamed or reordered anywhere in this
course's Tutor LMS content.
