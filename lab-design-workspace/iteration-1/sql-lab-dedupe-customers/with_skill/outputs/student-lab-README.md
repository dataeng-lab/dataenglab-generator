# Fix Duplicate Customers

**Level:** Beginner · **Duration:** ~25 min · **Tags:** GROUP BY, window functions, deduplication, NULLs

## Business context

Customer support flagged a data quality incident: the weekly "duplicate
cleanup" report just merged two different customers — both named John
Smith — into a single account. One of them called in confused that a
stranger's loyalty points had appeared on his balance overnight.
Meanwhile, finance suspects the opposite problem is *also* happening:
real duplicate accounts (the same person, registered twice with a
slightly different email spelling) aren't being merged at all, so their
loyalty points are scattered across multiple accounts instead of
combined.

You've been asked to write a correct customer-deduplication query using
only the data actually available — no name matching, no fuzzy logic —
matched on normalized email identity instead.

The current report lives in
[`starter/naive_report.sql`](starter/naive_report.sql). Don't edit it —
it's your reference for what's currently in production. Your fixed
version goes in [`starter/solution.sql`](starter/solution.sql).

## Environment

- Python 3.9+ (only the standard library — no installs needed)
- No Docker, no network access required

## Setup

```bash
python build_db.py
```

This (re)builds `lab.db` from `datasets/customers.csv`. Re-run it any
time you want to reset the database to its original state (see **Reset
procedure** below).

## Tasks

### Task 1 — Reproduce the bug

Run the current production report:

```bash
python -c "
import sqlite3
conn = sqlite3.connect('lab.db')
cur = conn.cursor()
cur.execute(open('starter/naive_report.sql').read())
for row in cur.fetchall():
    print(row)
"
```

Find the row for `John`, `Smith`. It shows `row_count = 2` and combined
`loyalty_points`. Now check whether that's actually one person:

```sql
SELECT customer_id, email, phone FROM customers
WHERE first_name = 'John' AND last_name = 'Smith';
```

Two different emails, two different phone numbers — these are two
different customers who happen to share a name. The report merged them
anyway because it matches on `first_name` + `last_name`. That's the bug
support flagged. Confirm this for yourself before moving on.

### Task 2 — Diagnose duplicates the naive way

Now try the "obvious" fix — group by `email` instead of by name:

```sql
SELECT email, COUNT(*) FROM customers
GROUP BY email
HAVING COUNT(*) > 1;
```

This has two problems, in opposite directions:

1. It returns `bob.diallo@example.com` (correctly a real duplicate) but
   **misses Amy Chen's duplicates entirely** — look at her three rows in
   `datasets/customers.csv` and notice the email is spelled three
   different ways (case and surrounding whitespace differ). Raw string
   comparison treats those as three unrelated emails.
2. It also returns one row where `email` is `NULL`, with `COUNT(*) = 2`
   — but query `SELECT customer_id, first_name, last_name FROM customers
   WHERE email IS NULL` and you'll find those two rows are **different
   guest checkouts** (Grace Osei and Priya Nair), not duplicates of each
   other at all.

<details>
<summary>Hint: why does GROUP BY do that with NULLs?</summary>

SQL's `GROUP BY` treats every `NULL` as equal to every other `NULL` for
grouping purposes (this is different from `NULL = NULL`, which is
unknown/false in a `WHERE` clause). Two unrelated guest checkouts with no
email on file will always land in the same `NULL` group — that's a false
positive, not a real duplicate, and your dedupe key needs to prevent it.
</details>

### Task 3 — Build a correct normalized dedupe key

You need a key that:
- treats `amy.chen@example.com`, `AMY.CHEN@example.com`, and
  `  amy.chen@example.com  ` as the *same* key (case- and
  whitespace-insensitive), but
- never lets two different `NULL`-email rows collide with each other.

<details>
<summary>Hint for Task 3</summary>

```sql
CASE
    WHEN email IS NULL THEN 'no-email-' || customer_id
    ELSE LOWER(TRIM(email))
END AS dedupe_key
```

Every guest checkout gets its own unique key derived from its own
`customer_id`, so it can never accidentally group with another guest.
</details>

### Task 4 — Pick a canonical row and merge without losing data

For each real duplicate group (grouped by your `dedupe_key`), you need to:
- pick exactly one canonical row — the one with the **earliest**
  `created_at` (the original account) — deterministically, not whatever a
  plain `GROUP BY` happens to return;
- **backfill** `phone` from any duplicate in the group that has one (some
  of the earliest rows have a `NULL` phone that a later duplicate filled
  in);
- **sum** `loyalty_points` across the whole group, so consolidating
  accounts doesn't destroy points the customer already earned;
- count how many raw rows fed into each canonical customer
  (`duplicate_count`).

<details>
<summary>Hint for Task 4</summary>

```sql
SELECT
    n.*,
    ROW_NUMBER() OVER (
        PARTITION BY dedupe_key
        ORDER BY created_at ASC, customer_id ASC
    ) AS rn,
    MAX(phone) OVER (PARTITION BY dedupe_key) AS filled_phone,
    SUM(loyalty_points) OVER (PARTITION BY dedupe_key) AS total_points,
    COUNT(*) OVER (PARTITION BY dedupe_key) AS duplicate_count
FROM normalized n
```

`MAX()` and `SUM()` as **window** functions (with `OVER (PARTITION BY
...)` and no `GROUP BY`) compute one value per row within its partition
without collapsing the rows — which is exactly what you need before
filtering down to `rn = 1`. `MAX()` also ignores `NULL`s, so it correctly
picks up the one non-`NULL` phone in a group even if the canonical row's
own phone is `NULL`.
</details>

### Task 5 — Assemble and verify the trusted query

Combine Tasks 3 and 4 into a single query in `starter/solution.sql` that
returns exactly one row per real customer, with columns: `customer_id,
email, first_name, last_name, phone, loyalty_points, duplicate_count`.

Verify it yourself before running the automated check:

```sql
-- should return 9 rows total, and this should return 0 rows:
SELECT customer_id, COUNT(*) FROM (<your query>) GROUP BY customer_id HAVING COUNT(*) > 1;
```

Also double check that `C-004` and `C-021` (the two John Smiths) both
still appear as separate rows.

## Hints

Hints are inlined as `<details>` blocks above, next to the task they
help with.

## Expected output

Your query, run against `lab.db`, should return **9 rows** — one per real
customer — with total `loyalty_points` of **590** across the result (the
same total as the 12 raw rows; deduplication redistributes points, it
never loses or invents them). The unfixed `naive_report.sql` returns 8
rows because it wrongly merges the two John Smiths.

## Validation

```bash
python tests/test_solution.py
```

Checks that `starter/solution.sql`:
1. returns the required columns,
2. returns exactly one row per real customer (9 rows, no duplicate `customer_id`),
3. keeps the two John Smiths (`C-004`, `C-021`) separate,
4. conserves total `loyalty_points` (590) across the result,
5. matches the trusted values for every customer in `tests/expected_customers.csv`.

Exits non-zero if any check fails.

## Reset procedure

```bash
python build_db.py
```

Rebuilding always starts from the original CSV in `datasets/`, so you can
reset at any point without losing the starter files.

## Troubleshooting

- **`lab.db not found`** — run `python build_db.py` first.
- **`sqlite3.OperationalError: near "SELECT": syntax error`** — check for
  a stray semicolon or comment left over from `solution.sql`'s starter
  template.
- **Still 8 rows instead of 9** — you're still matching by name somewhere,
  or your `NULL`-email fallback key isn't actually unique per row (check
  it includes `customer_id`).
- **10 rows instead of 9, with two John-Smith-looking rows still combined
  into one wrong row and one extra split-off row** — check your
  `dedupe_key`'s `CASE` logic; a common mistake is normalizing the whole
  key (including the `NULL` branch) with `LOWER(TRIM(...))`, which can
  produce accidental collisions.
- **Total loyalty_points isn't 590** — you're likely missing the
  `SUM(loyalty_points) OVER (PARTITION BY dedupe_key)` step and instead
  only keeping the canonical row's own points, dropping the other
  duplicates' balances.
- **Phone is `NULL` for `C-001` or `C-002` when it shouldn't be** —
  you're selecting the canonical row's raw `phone` instead of the
  window-aggregated `MAX(phone) OVER (PARTITION BY dedupe_key)` backfill.
