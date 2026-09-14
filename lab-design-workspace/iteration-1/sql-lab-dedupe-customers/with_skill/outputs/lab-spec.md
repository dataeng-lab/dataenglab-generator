# Practical Lab Specification

## Business context
Customer support at an online store flagged a data quality problem: the
"duplicate cleanup" report the ops team runs every week just merged two
different customers named John Smith into one account, and one of them is
now complaining that a stranger's loyalty points appeared on his balance
overnight. At the same time, finance suspects other real duplicate
accounts (same person, slightly different email spelling) are *not* being
merged, so loyalty points are scattered across multiple accounts instead
of consolidated. The student plays the data engineer asked to write a
correct, trustworthy customer-deduplication query using only the data
actually available (no name matching, no fuzzy logic) — matching on
normalized email identity instead.

## Learning objectives
By the end of the lab, students can:
- Explain why matching duplicate records on `first_name`/`last_name` is
  unsafe (different people can share a name) and why a normalized unique
  identifier (email) is the safer join/grouping key.
- Normalize a text key (`LOWER(TRIM(email))`) before using it to detect
  duplicates, and recognize case- and whitespace-only "duplicates" that a
  naive raw-column `GROUP BY` misses entirely.
- Recognize and work around SQL's `NULL`-grouping behavior (`GROUP BY`
  treats all `NULL`s as one group), which silently produces false-positive
  "duplicates" out of unrelated `NULL`-email guest checkouts.
- Pick a single canonical row per real duplicate group deterministically
  (earliest `created_at`, via `ROW_NUMBER() OVER (PARTITION BY ... ORDER
  BY ...)`), instead of an undefined/arbitrary `GROUP BY` result.
- Merge non-authoritative fields across a duplicate group without losing
  data: backfill a missing `phone` from any duplicate that has one
  (`MAX(phone) OVER (PARTITION BY ...)`, which ignores `NULL`s), and sum
  `loyalty_points` across the group so consolidating accounts doesn't
  destroy a customer's earned balance.

## Environment
Python 3.9+ (standard library only — `sqlite3` and `unittest` ship with
Python; no `pip install`, no Docker, no network access).

## Estimated duration
25 minutes.

## Starter files
- `student-lab/build_db.py` — builds `lab.db` from the CSV dataset.
- `student-lab/starter/schema.sql` — table definition (informational; applied automatically by `build_db.py`).
- `student-lab/starter/naive_report.sql` — the current, buggy weekly cleanup report (read-only reference; don't edit).
- `student-lab/starter/solution.sql` — where the student writes the fixed query.

## Dataset
`student-lab/datasets/customers.csv` — 12 rows / 9 distinct real customers,
one table, deliberately containing:
- a 3-row true duplicate group for the same person (`amy.chen@example.com`)
  spread across exact, upper-case, and leading/trailing-whitespace email
  spellings, with the earliest row missing a `phone` that a later
  duplicate has, and loyalty points split 120 / 40 / 15 across the three
  accounts;
- a 2-row true duplicate group (`bob.diallo@example.com`, exact email
  match) with the same missing-phone-on-the-earliest-row pattern and
  points split 60 / 25;
- two unrelated guest checkouts with `NULL` email (Grace Osei, Priya Nair)
  that a naive `GROUP BY email` incorrectly clusters together as
  "duplicates" purely because SQL groups `NULL`s together;
- two unrelated real customers who happen to share the exact name "John
  Smith" but have different emails and phone numbers — the pair the
  naive, name-based cleanup report wrongly merges into one account;
- three ordinary customers with no duplicates at all (Dana Osei, Felix
  Wong, Hana Kim), one of whom (Hana) has a `NULL` phone that legitimately
  has nothing to backfill from.

## Tasks
1. Run `starter/naive_report.sql` (the current production report) and
   discover it has merged the two different "John Smith" customers into
   one row, combining their loyalty points and losing the fact they're
   different people.
2. Diagnose duplicates the naive way (`GROUP BY email` on the raw column)
   and observe both of its failure modes: it misses the Amy Chen group
   entirely (case/whitespace differences make the raw strings look
   distinct) and it falsely flags the two `NULL`-email guests as
   duplicates of each other.
3. Build a correct normalized dedupe key: `LOWER(TRIM(email))` for real
   emails, and a per-row-unique key for `NULL` emails so guest checkouts
   never collide with each other.
4. Using that key, pick one canonical row per real duplicate group
   (earliest `created_at`), backfill a missing `phone` from any duplicate
   that has one, and sum `loyalty_points` across the group.
5. Assemble the final query in `starter/solution.sql` and verify it
   returns exactly one row per real customer with total loyalty points
   conserved and the two John Smiths still separate.

## Hints
Provided as `<details>` blocks in `student-lab/README.md`: one for the
`NULL`-grouping trap in Task 2, one for the dedupe-key construction in
Task 3, and one for the backfill/sum window functions in Task 4.

## Validation
```bash
python build_db.py
python tests/test_solution.py
```
Both commands run from inside `student-lab/`. `test_solution.py` checks
required columns, exactly one row per real customer (9 rows), that total
`loyalty_points` across the result equals the total across the raw
dataset (590 — no points lost or invented), and an exact match against
`tests/expected_customers.csv` for every canonical customer. It exits
non-zero on any failure. Matches `validate.json` at this lab's root
exactly.

## Expected output
9 rows (down from 12 raw rows), total `loyalty_points` = **590** across
the result (unchanged from the raw data — see
`instructor/instructor-guide.md` for the full per-group breakdown). The
two John Smith customers (`C-004`, `C-021`) remain separate rows.

## Reset procedure
`python build_db.py` — rebuilds `lab.db` from the original CSV at any
time; the starter files themselves are never modified by setup/reset.

## Troubleshooting
See `student-lab/README.md`'s Troubleshooting section (student-facing)
and `instructor/troubleshooting.md` (instructor-facing, covers common
wrong turns and how to steer students back).

## Instructor solution
`instructor/solution/solution.sql`, with `instructor/instructor-guide.md`
explaining the reasoning behind each fix and `instructor/troubleshooting.md`
covering common student mistakes.
