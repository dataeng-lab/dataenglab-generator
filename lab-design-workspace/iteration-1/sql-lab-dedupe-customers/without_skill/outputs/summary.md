# Summary -- fix-duplicate-customers-eval-bl (without_skill / baseline condition)

## Method note
Built per explicit instruction NOT to use the Skill tool and NOT to read
anything under .claude/skills/. Guidance sources actually used:
CLAUDE.md (project root) and every file under .claude/rules/*.md
(core.md, course-contract.md, elementor.md, labs.md, publishing.md,
validation.md), plus inspection of two existing sibling lab outputs
(output/dedupe-late-arriving-orders/, output/investigate-duplicate-orders/)
and the relevant scripts under scripts/ (run_checks.py, run_lab_checks.py,
validate_lab.py, validate_lab_execution.py) to learn the expected
structure and validation contract, plus general judgment on lab design.

## Real output path
E:\dataeng-lab\dataenglab-generator\output\fix-duplicate-customers-eval-bl\

## Every file/directory created

output/fix-duplicate-customers-eval-bl/
  lab-spec.md
  page-content.md
  validate.json
  student-lab/
    README.md
    build_db.py                     (build script: seed CSV -> customers.db)
    datasets/
      customers_seed.csv            (16 raw rows, deterministic)
    starter/
      dedupe.sql                    (student worksheet, intentionally incomplete)
    tests/
      expected_customers.csv        (11-row answer key)
      test_solution.py              (automated checker, exits non-zero on failure)
  instructor/
    solution/
      dedupe.sql                    (working solution, same filename as starter)
    instructor-guide.md
    troubleshooting.md

Also created (this eval-workspace deliverable, not part of the lab
output itself):

lab-design-workspace/iteration-1/sql-lab-dedupe-customers/without_skill/outputs/
  summary.md
  lab-spec.md            (copy)
  README.md              (copy of student-lab/README.md)
  validate.json          (copy)
  dedupe.sql             (copy of instructor/solution/dedupe.sql)

No elementor/ or packages/ directories were created -- the task
instructions enumerated the exact deliverable list (lab-spec.md,
page-content.md, student-lab/{README.md, build script, datasets/,
starter/, tests/}, instructor/{solution/, instructor-guide.md,
troubleshooting.md}, root validate.json) and neither a landing page nor
a packaged ZIP was in that list.

## Lab design

- Dataset: customers table, 16 raw signup rows / 11 distinct real
  customers, built deterministically by build_db.py from
  datasets/customers_seed.csv into a fresh customers.db (SQLite,
  Python standard-library sqlite3 only, no network/Docker/credentials).
- Edge cases encoded: an exact-duplicate row (Bob Smith), a
  case/whitespace-only duplicate email (Carol Davis), a triple duplicate
  where the chronologically earliest signup is neither the first
  physical row nor the smallest customer_id (Emma Wilson), a
  same-signup_date duplicate needing a customer_id tie-break (Frank
  Miller), and two distinct real people sharing a full name but with
  different emails (Henry Osei x2) as a false-positive guard against
  deduplicating by name.
- Student task: edit starter/dedupe.sql to build a customers_clean
  table (one row per real customer: customer_id, full_name, email
  normalized via LOWER(TRIM(...)), phone, signup_date, source_system,
  duplicate_count), using the canonical rule "earliest signup_date
  wins, tie-break by smaller customer_id."
- Instructor solution: instructor/solution/dedupe.sql, a CTE using
  ROW_NUMBER() OVER (PARTITION BY normalized_email ORDER BY
  signup_date ASC, customer_id ASC) plus COUNT(*) OVER (...) for
  duplicate_count. Same filename as the starter file so
  scripts/validate_lab_execution.py's overlay step (solution file
  copied onto the matching starter path) works.

## Every command run, with real results

1. mkdir -p for student-lab/{datasets,starter,tests}, instructor/solution,
   and the eval-workspace outputs/ dir -- succeeded, no output.
2. python build_db.py (from inside student-lab/) --
   Result: "Built customers.db with 16 raw customer rows." (exit 0)
3. python tests/test_solution.py run against the UNEDITED starter
   (before any solution overlay) --
   Result: FAILED (exit 1), as expected/required for a student starter
   file. Real output:
     FAILED:
      - customers_clean has 16 rows but only 11 distinct normalized emails -- duplicates were not fully removed.
      - Expected 11 rows in customers_clean, found 16.
      - Row mismatch. (x9, one per non-matching expected row)
   This confirms the starter genuinely does not pass and the checker
   correctly detects an unfixed placeholder.
4. Removed the test-generated customers.db and a stray backup file
   created during manual testing, to leave the output directory clean --
   succeeded, no output.
5. python scripts/run_checks.py output/fix-duplicate-customers-eval-bl
   (run from the repo root; this is run_checks.py's auto-detected "lab"
   mode, since lab-spec.md exists and course-spec.json does not -- it
   internally invokes run_lab_checks.py, which in turn runs
   validate_lab.py on student-lab/ and validate_lab_execution.py on the
   whole lab directory) --
   Result: ALL CHECKS PASSED (exit 0). Real captured output:
     Detected validation mode: lab

     $ python scripts/run_lab_checks.py output\fix-duplicate-customers-eval-bl

     $ python scripts/validate_lab.py output\fix-duplicate-customers-eval-bl\student-lab
     OK: output\fix-duplicate-customers-eval-bl\student-lab
     PASS: python scripts/validate_lab.py ...

     $ python scripts/validate_lab_execution.py output\fix-duplicate-customers-eval-bl
     OK: instructor solution passes the lab tests - output\fix-duplicate-customers-eval-bl
     PASS: python scripts/validate_lab_execution.py ...
     ALL LAB CHECKS PASSED
     PASS: python scripts/run_lab_checks.py ...
     ALL CHECKS PASSED

   validate_lab.py confirmed: required README.md/starter/datasets/tests
   all present with content, no cache/bytecode files, no
   solution-filename leaks into student-lab/, no secret patterns (AWS
   keys, private keys, hardcoded user home paths) in any lab file.
   validate_lab_execution.py confirmed the actual mechanism required by
   the project rules: it copied student-lab/ to a temp directory,
   overlaid instructor/solution/dedupe.sql onto starter/dedupe.sql, ran
   python build_db.py (setup) then python tests/test_solution.py
   (validate) there, and both succeeded -- i.e., the instructor
   solution genuinely solves the lab as specified in validate.json.
6. Final cleanup: removed the customers.db left behind by the manual
   test run in step 3, and re-listed the output directory to confirm
   only the intended 12 files remain (verified with find ... -type f).
7. Copied 4 files (lab-spec.md, student-lab/README.md, validate.json,
   instructor/solution/dedupe.sql) into this outputs/ directory as
   required by the eval harness -- succeeded, confirmed by directory
   listing.

Total real commands executed: 7 (numbered above; each was actually run
in this session via the Bash tool, not simulated).

## Validation result (authoritative)

python scripts/run_checks.py output/fix-duplicate-customers-eval-bl ->
ALL CHECKS PASSED (exit code 0), covering:
- required-file/directory presence and non-emptiness for the lab
  contract (validate_lab.py's check_required_lab_paths);
- no secret patterns or solution-file leaks inside student-lab/;
- the instructor solution, overlaid onto the starter and run through
  the exact validate.json setup/validate commands (python build_db.py
  then python tests/test_solution.py), passes end-to-end in an
  isolated temp copy of the lab.

Separately confirmed (step 3 above) that the UNEDITED student starter
correctly FAILS test_solution.py -- this is the intended behavior per
the project's lab rules (starter/ must not already contain a working
solution) and was verified by actually running it, not assumed.

## Limitations / manual steps not performed
- No elementor/ landing page or publish step was requested or
  attempted; page-content.md was still written (per the explicit file
  list) but not turned into any Elementor JSON, and nothing was
  published to dataenglab.com.
- No course-reviewer or other subagent review was run (task said to
  build directly and run "whatever validation script under scripts/
  seems appropriate," which was interpreted as the automated checker,
  not the independent review step from the full course workflow).
- No package/ZIP was produced (not in the requested deliverable list).
- Context7 MCP was not invoked for SQLite/SQL syntax claims; the SQL
  used (ROW_NUMBER() OVER (...), COUNT(*) OVER (...), LOWER, TRIM) is
  core SQLite window-function syntax stable since SQLite 3.25 (2018),
  and was verified empirically by actually executing it successfully
  against a real SQLite database in step 5, which is direct evidence
  rather than a documentation lookup.
