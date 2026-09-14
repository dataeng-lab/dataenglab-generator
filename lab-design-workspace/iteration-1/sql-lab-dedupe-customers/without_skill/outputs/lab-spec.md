# Practical Lab Specification

## Title
Fix Duplicate Customer Records

## Slug
fix-duplicate-customers-eval-bl

## Audience
Beginner-to-intermediate data/analytics engineers who know basic `SELECT`
/ `WHERE` / `GROUP BY` SQL and want practice with deduplication logic and
window functions.

## Level
Beginner

## Prerequisites
- Basic SQL: `SELECT`, `WHERE`, `GROUP BY`, `HAVING`, joins.
- Comfortable running a script from a terminal.
- No prior window-function experience required -- the lab introduces
  `ROW_NUMBER()`/`COUNT() OVER (...)` with a worked hint.

## Business context
CustomerConnect accepts new customer signups from three channels (public
web form, mobile app, nightly CRM import) into a single `customers`
table with no uniqueness constraint on email. The same real person can
therefore end up with more than one customer record -- sometimes an
exact re-submission, sometimes the same address typed with different
capitalization or stray whitespace. Marketing is sending duplicate
promotional emails and Support can't find a customer's full history
because it's split across multiple `customer_id`s. The student's job is
to find every true duplicate and produce one clean, canonical record per
real customer -- without merging two different people who happen to
share a name.

## Deliverable
A single SQL file (`starter/dedupe.sql`, edited by the student) that,
run against `customers.db`, creates a `customers_clean` table with
exactly one row per real customer: `customer_id, full_name, email
(normalized), phone, signup_date, source_system, duplicate_count`.

## Environment
Python 3.9+ (standard library `sqlite3` module only -- no `pip install`,
no Docker, no network access). SQLite ships with Python, so no separate
database server or credentials are needed.

## Estimated duration
25 minutes.

## Technologies
SQLite, SQL (window functions: `ROW_NUMBER()`, `COUNT() OVER (...)`),
Python (only as the harness that builds the database and runs the
checks -- students do not need to write Python).

## Starter files
- `student-lab/build_db.py` -- builds `customers.db` from the seed CSV
  (also serves as the reset procedure).
- `student-lab/starter/dedupe.sql` -- exploration queries for Task 1
  provided as-is; Tasks 2-4 contain commented-out/placeholder SQL for
  the student to complete.

## Dataset
`student-lab/datasets/customers_seed.csv` (16 rows / 11 distinct real
customers). Edge cases encoded: an exact-duplicate row (Bob Smith), a
case/whitespace-only email duplicate (Carol Davis), a triple duplicate
where the chronologically earliest signup is neither the first physical
row nor the smallest `customer_id` (Emma Wilson), a same-`signup_date`
duplicate requiring a `customer_id` tie-break (Frank Miller), and two
distinct real customers who share a full name but have different emails
(Henry Osei x2) -- a deliberate false-positive guard against
deduplicating on `full_name`.

## Tasks
1. Run the provided exploration queries to see the gap between raw row
   count and distinct normalized-email count.
2. Write a `GROUP BY` / `HAVING` query that lists every duplicate group
   by normalized email, and confirm the two "Henry Osei" rows do not
   form a group.
3. Define the canonical-row rule: earliest `signup_date` per normalized
   email, tie-broken by the smaller `customer_id`.
4. Build `customers_clean` with the canonical row's fields, a
   normalized email, and a `duplicate_count` per group.
5. Run the automated check and verify no duplicate normalized emails
   remain and the grain is exactly one row per real customer.

## Hints
Provided as `<details>` blocks in `student-lab/README.md`, one for the
canonical-row window function (Task 3) and one for `duplicate_count`
(Task 4).

## Validation
```bash
python build_db.py
python tests/test_solution.py
```
Both commands run from inside `student-lab/`. `test_solution.py` executes
`starter/dedupe.sql` against a freshly built `customers.db`, then checks
that `customers_clean` exists with the required columns, has zero
duplicate normalized emails, has exactly 11 rows, and matches
`tests/expected_customers.csv` exactly. It exits non-zero on any
failure. Matches `validate.json` at this lab's root exactly.

## Validation criteria
- `customers_clean` table exists with columns `customer_id, full_name,
  email, phone, signup_date, source_system, duplicate_count`.
- Exactly 11 rows (one per real customer).
- `COUNT(*) == COUNT(DISTINCT LOWER(TRIM(email)))` over `customers_clean`.
- Row-for-row exact match against `tests/expected_customers.csv`,
  including that the two "Henry Osei" customers remain two separate
  rows and Emma Wilson's canonical row is `C1009` (not `C1007`/`C1008`).

## Expected output
11 rows in `customers_clean`, matching `tests/expected_customers.csv`
exactly -- see `instructor/instructor-guide.md` for the full
before/after breakdown and dataset cheat sheet.

## Reset procedure
`python build_db.py` -- rebuilds `customers.db` from scratch at any
time; `datasets/` and the starter files are never modified by
setup/reset.

## Acquired skills
- Distinguishing exact duplicates from near-duplicates that require
  normalization (trim/case) before comparison.
- Defining and applying a deterministic canonical-record rule instead
  of relying on physical row order or a surrogate key's ordering.
- Using SQL window functions (`ROW_NUMBER()`, `COUNT() OVER (...)`) to
  rank and count within groups in a single query.
- Recognizing that a human-readable field (name) is not a safe dedup
  key and can produce false-positive merges.

## Troubleshooting
See `student-lab/README.md`'s Troubleshooting section (student-facing)
and `instructor/troubleshooting.md` (instructor-facing, covers common
wrong turns and how to steer students back).

## Instructor solution
`instructor/solution/dedupe.sql`, with `instructor/instructor-guide.md`
explaining the reasoning behind the canonical-row rule and
`instructor/troubleshooting.md` covering common student mistakes.
