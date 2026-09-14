# Fix Duplicate Customer Records

**Level:** Beginner · **Duration:** ~25 min · **Tags:** SQL, deduplication, data quality, SQLite, window functions

## Business context

CustomerConnect accepts new customer signups from three channels -- the
public web form, the mobile app, and a nightly CRM import -- all writing
into the same `customers` table. There is no uniqueness constraint on
email, and the three systems don't check each other before inserting a
row. The result: the same real person can end up with more than one
customer record, sometimes an exact re-submission, sometimes the same
address typed with different capitalization or stray whitespace.

Marketing just complained that some customers are getting the same
promotional email two or three times, and Support can't find a
customer's full history because it's split across multiple
`customer_id`s. You've been asked to write the SQL that finds every
duplicate customer and produces one clean, canonical record per real
person -- without accidentally merging two different people who simply
share a name.

## Environment

- Python 3.9+ (standard library `sqlite3` module only -- no `pip
  install`, no Docker, no network access)
- Any SQLite client if you want to explore interactively (the `sqlite3`
  CLI, DB Browser for SQLite, a VS Code extension, etc.) -- optional,
  since the automated check runs your SQL for you either way.

## Setup

```bash
python build_db.py
```

This (re)builds `customers.db` from `datasets/customers_seed.csv`: it
drops and recreates the `customers` table and discards any
`customers_clean` table a previous attempt left behind. Re-run it any
time you want a clean slate (see **Reset procedure** below) -- it never
touches `datasets/` or `starter/`.

## Dataset

`customers` (built into `customers.db`): 16 raw rows, one per signup
event, columns `customer_id, full_name, email, phone, signup_date,
source_system`. Only 11 of those rows represent distinct real
customers. Edge cases baked in on purpose:

- **Exact duplicate** (`C1002` / `C1003`, Bob Smith) -- byte-for-byte
  the same row twice, just a different `customer_id`.
- **Case + whitespace duplicate** (`C1004` / `C1005`, Carol Davis) --
  `Carol.Davis@Example.com` vs. `" carol.davis@example.com "`; same
  person once you normalize the email.
- **Triple duplicate with out-of-order signup dates** (`C1007` /
  `C1008` / `C1009`, Emma Wilson) -- three channels, three
  capitalizations/whitespace variants of the same email, and the
  earliest real signup (`C1009`, CRM import, 2024-01-28) is neither the
  first row in the table nor the smallest `customer_id`.
- **Same-day duplicate** (`C1010` / `C1011`, Frank Miller) -- both rows
  share the exact same `signup_date`, so you need a deterministic
  tie-break.
- **Look-alike, NOT a duplicate** (`C1013` / `C1014`, both named "Henry
  Osei") -- different email addresses, so they must stay two separate
  customers. Deduplicating by name instead of email would wrongly merge
  them.
- Six more rows (`Alice Johnson`, `David Lee`, `Grace Chen`, `Isabel
  Rossi`, `Jack Nguyen`) are already unique and should pass through
  untouched.

## Tasks

Work in `starter/dedupe.sql`. It already contains the queries for Task
1 -- run the file as-is once to see the gap between "raw rows" and
"distinct customers" before you touch anything.

### Task 1 -- See the gap

Run the exploration queries at the top of `starter/dedupe.sql` (via the
`sqlite3` CLI or your client of choice, against `customers.db`):

```sql
SELECT COUNT(*) AS total_rows FROM customers;
SELECT COUNT(DISTINCT LOWER(TRIM(email))) AS distinct_customers FROM customers;
```

`total_rows` (16) is larger than `distinct_customers` (11). That gap is
the duplicates.

### Task 2 -- Find the duplicate groups

Uncomment and complete the `GROUP BY` / `HAVING` query in Task 2 of
`starter/dedupe.sql` so it lists every normalized email that appears
more than once, with a count. Confirm that the two "Henry Osei" rows do
**not** show up as a group -- they have different emails, so they are
not duplicates of each other even though they share a name.

### Task 3 -- Pick one canonical row per group

For each duplicate group, the canonical record is the one with the
**earliest `signup_date`**. If two rows in the same group share the
same `signup_date`, break the tie with the smaller `customer_id`. Do
not assume "first row in the table" or "smallest `customer_id`
overall" is the answer -- check what that would do to the Emma Wilson
group once Task 2 is working.

### Task 4 -- Build `customers_clean`

Replace the placeholder `CREATE TABLE customers_clean AS SELECT ...` at
the bottom of `starter/dedupe.sql` with a real query that produces
exactly one row per real customer, with columns:

| column | source |
|---|---|
| `customer_id` | the canonical row's `customer_id` |
| `full_name` | the canonical row's `full_name` |
| `email` | the **normalized** (`LOWER(TRIM(...))`) email |
| `phone` | the canonical row's `phone` (may be `NULL`) |
| `signup_date` | the canonical row's `signup_date` |
| `source_system` | the canonical row's `source_system` |
| `duplicate_count` | how many raw rows were merged into this one (`1` if it was never duplicated) |

### Task 5 -- Verify

Run the automated check:

```bash
python tests/test_solution.py
```

It executes your `starter/dedupe.sql` against a freshly built database
and checks that `customers_clean` has exactly 11 rows, no two rows
share a normalized email, and every column matches the expected
answer key exactly.

## Hints

Stuck? Expand only the hint you need.

<details>
<summary>Hint for Task 3 (pick the canonical row deterministically)</summary>

```sql
SELECT
    *,
    ROW_NUMBER() OVER (
        PARTITION BY LOWER(TRIM(email))
        ORDER BY signup_date ASC, customer_id ASC
    ) AS row_rank
FROM customers;
```

The row with `row_rank = 1` in each `LOWER(TRIM(email))` group is the
canonical row.
</details>

<details>
<summary>Hint for Task 4 (count how many rows were merged)</summary>

```sql
COUNT(*) OVER (PARTITION BY LOWER(TRIM(email))) AS duplicate_count
```

Combine this with the `ROW_NUMBER()` from the Task 3 hint in the same
`WITH` / window-function query, then filter down to `row_rank = 1` in
your final `SELECT`.
</details>

## Expected output

`customers_clean` should have exactly **11 rows** -- see
`tests/expected_customers.csv` for the full answer key. Notably: Emma
Wilson's canonical row is `C1009` (signup `2024-01-28`, source
`crm_import`) with `duplicate_count = 3`, not `C1007` or `C1008`; and
Henry Osei appears **twice** (`C1013` and `C1014`), each with
`duplicate_count = 1`, because they are different people.

## Validation

```bash
python build_db.py
python tests/test_solution.py
```

Both commands run from inside `student-lab/`. `test_solution.py` runs
`starter/dedupe.sql` against a freshly built `customers.db`, then
checks that `customers_clean` exists with the required columns, has no
duplicate normalized emails, has exactly one row per real customer, and
matches `tests/expected_customers.csv` exactly. It exits non-zero on
any failure. Matches `validate.json` at this lab's root exactly.

## Reset procedure

```bash
python build_db.py
```

Rebuilds `customers.db` from scratch at any time; `datasets/` and the
starter files are never modified by setup/reset.

## Troubleshooting

- **`customers_clean` has 16 rows, not 11** -- you're still running the
  unedited placeholder query (or a query that doesn't group by
  normalized email at all). Replace it with a real `GROUP BY`/window
  function query as described in Task 4.
- **Emma Wilson's canonical row is `C1007`, not `C1009`** -- you're
  probably picking "the first row in the table" or "the smallest
  `customer_id`" instead of sorting by `signup_date`. `C1009`'s CRM
  import row has the earliest `signup_date` even though it is not the
  first physical row for that email.
- **Henry Osei's two records got merged into one** -- check that you
  are grouping by normalized **email**, not by `full_name`. `C1013` and
  `C1014` have different emails and must stay separate.
- **`sqlite3.OperationalError: no such table: customers_clean` when
  running the test** -- your SQL raised an error before reaching the
  `CREATE TABLE` statement (a typo, or a query referencing a column
  that doesn't exist yet). Run the file yourself against `customers.db`
  with the `sqlite3` CLI to see the real error message.
- **`duplicate_count` is always `1`** -- you added the `COUNT(*) OVER
  (...)` window function but forgot to partition it by the normalized
  email, so each row is counting only itself.
