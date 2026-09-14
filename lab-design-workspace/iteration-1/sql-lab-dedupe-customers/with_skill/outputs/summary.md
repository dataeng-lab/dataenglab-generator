# Summary: fix-duplicate-customers-eval-ws (built with the lab-design skill)

## Real output path

`E:\dataeng-lab\dataenglab-generator\output\fix-duplicate-customers-eval-ws\`

## Method

Invoked the `lab-design` skill via the Skill tool with the task prompt,
then followed its documented workflow exactly: read
`contracts/lab-output-contract.md` and `contracts/memory.md`, inspected
the canonical example `output/investigate-duplicate-orders/` for shape
conventions, wrote `lab-spec.md` first, then built `student-lab/`,
`page-content.md`, `instructor/`, and `validate.json`, then ran the
skill's validation scripts and the packaging script. All files below are
real, on disk, and all commands were actually executed (none simulated).

## Scenario

A single-table SQLite dataset (`customers`, 12 raw rows / 9 real
customers) with three deliberate defects layered on top of each other:

1. A production report that "merges" customers by matching
   `first_name`+`last_name` -- which wrongly merges two different real
   customers who share the name "John Smith" (a genuine false-merge bug:
   support reported a customer's loyalty balance changing unexpectedly).
2. A true duplicate group (Amy Chen, 3 rows) spread across
   case/whitespace-different email spellings, invisible to a raw
   `GROUP BY email`.
3. Two unrelated `NULL`-email guest checkouts that a raw `GROUP BY email`
   falsely flags as duplicates of each other (SQL groups `NULL`s
   together).

Students write one SQL query that: builds a normalized dedupe key
(`LOWER(TRIM(email))`, with a per-row-unique fallback for `NULL` email),
picks one canonical row per real duplicate via
`ROW_NUMBER() OVER (PARTITION BY ... ORDER BY created_at ASC)`, backfills
a missing `phone` via `MAX(phone) OVER (PARTITION BY ...)`, and sums
`loyalty_points` via `SUM(...) OVER (PARTITION BY ...)` so consolidating
accounts never loses a customer's earned points.

## Files and directories created

```
output/fix-duplicate-customers-eval-ws/
|-- lab-spec.md
|-- page-content.md
|-- validate.json
|-- student-lab/
|   |-- README.md
|   |-- build_db.py
|   |-- datasets/
|   |   `-- customers.csv
|   |-- starter/
|   |   |-- schema.sql
|   |   |-- naive_report.sql        (buggy production report, read-only reference)
|   |   `-- solution.sql            (placeholder -- SELECT 1; students replace this)
|   `-- tests/
|       |-- expected_customers.csv
|       `-- test_solution.py
|-- instructor/
|   |-- solution/
|   |   `-- solution.sql            (working solution -- never shipped to students)
|   |-- instructor-guide.md
|   `-- troubleshooting.md
`-- packages/
    `-- fix-duplicate-customers-eval-ws-student-lab.zip   (8 files, student-facing only)
```

## Every real command run, with real results

1. `python --version` / `python -c "import sqlite3; print(sqlite3.sqlite_version)"`
   -> Python 3.11.6, SQLite 3.42.0 (confirms window-function support before
   designing around `ROW_NUMBER()`/`MAX() OVER`/`SUM() OVER`).

2. `mkdir -p student-lab/datasets student-lab/starter student-lab/tests instructor/solution`
   -> created the required directory tree.

3. `python build_db.py` (from inside `student-lab/`)
   -> `Built lab.db` -- deterministic SQLite database built from
   `datasets/customers.csv`.

4. Ran the instructor solution query directly via `sqlite3`/Python inline
   script -> confirmed exactly the 9 expected canonical rows and a raw
   `SUM(loyalty_points)` of 590, matching `tests/expected_customers.csv`
   exactly before the test suite was even run.

5. Ran `starter/naive_report.sql` and a raw `GROUP BY email` directly ->
   confirmed both designed bugs actually reproduce: the naive report
   shows `(C-004, John, Smith, 115, 2)` (false merge of two real
   customers), and raw `GROUP BY email` returns `(NULL, 2)` (false
   positive on two unrelated guests) while never surfacing Amy Chen's
   3-row group at all.

6. `python tests/test_solution.py` against the placeholder
   `starter/solution.sql` (`SELECT 1;`)
   -> FAILED, exit code 1 (1 failure + 4 errors, all `KeyError`/`ValueError`
   on missing columns) -- confirms the starter is genuinely unsolved and
   the test suite actually discriminates.

7. Copied `instructor/solution/solution.sql` over
   `student-lab/starter/solution.sql` and re-ran
   `python tests/test_solution.py`
   -> PASSED, exit code 0, `Ran 5 tests in 0.006s / OK` -- confirms the
   real solution is genuinely correct and solvable.
   The placeholder was then restored to `starter/solution.sql` immediately
   afterward so no working solution leaked into `student-lab/`.

8. `rm -f student-lab/lab.db`
   -> removed the locally generated build artifact so the committed tree
   matches the reference lab's convention (`lab.db` is a build product,
   not shipped).

9. `python scripts/run_lab_checks.py output/fix-duplicate-customers-eval-ws`
   (from the repo root, using the repo's own `.venv`)
   -> ALL LAB CHECKS PASSED:
   - `validate_lab.py output/fix-duplicate-customers-eval-ws/student-lab`
     -> OK / PASS
   - `validate_lab_execution.py output/fix-duplicate-customers-eval-ws`
     -> OK: instructor solution passes the lab tests / PASS
     (this stage copies `student-lab/` to a temp dir, overlays
     `instructor/solution/solution.sql` onto the matching starter path,
     and actually runs `validate.json`'s setup+validate commands there --
     it is the authoritative proof the lab is solvable, independent of
     step 7's manual check.)

10. `python scripts/package_student_lab.py output/fix-duplicate-customers-eval-ws`
    -> OK: .../packages/fix-duplicate-customers-eval-ws-student-lab.zip,
    Files: 8.

11. Verified the ZIP's contents directly (`zipfile.ZipFile(...).namelist()`)
    -> confirmed exactly 8 student-facing files, no `instructor/`, no
    `page-content.md`, no `lab-spec.md`, and `starter/solution.sql` inside
    the zip is the placeholder, not the working solution.

Total real commands executed: 11 (numbered above; several bash
invocations bundled more than one shell command, but each numbered item
above corresponds to one distinct verification step actually run against
real files/processes, not simulated or predicted).

## Validation result

`python scripts/run_lab_checks.py output/fix-duplicate-customers-eval-ws`
-> PASS (both `validate_lab.py` and `validate_lab_execution.py`
reported PASS; final line `ALL LAB CHECKS PASSED`).

## Limitations

- This is a standalone lab-design run, not a full course: no
  `course-reviewer` pass, no Elementor landing page, and no
  `scripts/run_checks.py` (that wrapper auto-detects standalone labs but
  was not invoked here -- `run_lab_checks.py` is the direct/authoritative
  checker for this shape and was used per the skill's own instructions).
- No live publish was attempted or implied; `page-content.md` was
  written as the skill's `publish-practical-lab` handoff artifact but
  publishing itself is out of scope for this task and was not performed.
- The lab intentionally covers only email-based identity matching (case/
  whitespace normalization + NULL-safety); phone-based fuzzy matching or
  a human-review merge queue are explicitly out of scope, called out in
  both the student README and `instructor/troubleshooting.md`.
- Dataset size (12 raw rows / 9 canonical customers) is smaller than the
  ~26-36 row range noted as a sweet spot in the skill's own memory file
  for multi-table ETL labs; this lab is single-table and scenario-driven
  by the requested edge cases rather than by a target row count, and 12
  rows was sufficient to encode every edge case (case-insensitive
  duplicate, whitespace duplicate, exact duplicate, NULL-grouping false
  positive, same-name-different-person false positive, phone backfill,
  point conservation, and an ordinary no-op case) while staying small
  enough for a student to hand-verify by eye.
