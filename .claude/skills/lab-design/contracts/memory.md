# Lab Engineer / Lab Design Memory

Durable, empirically-observed facts for building DataEngLab practical labs.
These come from an actual lab build in this repo (the
`apache-spark-for-beginners` course-embedded lab), not speculation. Read this
before writing lab files; still verify everything fresh — this is pattern
memory, not a substitute for reading `.claude/rules/labs.md` and this skill's
own contract fresh each run.

## Environment facts that actually mattered

- **Context7 MCP tools were unavailable inside a `lab-engineer` subagent's
  own tool session**, even though the orchestrating/parent session had them.
  Don't assume Context7 access just because CLAUDE.md/the skill says to use
  it — try it, and if it errors as unavailable, proceed with stable,
  well-established API patterns (verified elsewhere if possible) and state
  the limitation plainly in the final report rather than silently skipping
  the disclosure.
- **The build sandbox has no outbound network access**, so a fresh
  `pip install` cannot fetch new packages inside that sandbox. To actually
  execute the validation loop (not just assume it would pass),
  `apache-spark-for-beginners`'s build bootstrapped a local `.venv` from
  already-cached local wheels (pyspark 3.5.0, py4j 0.10.9.7, pytest 8.4.2).
  This was local test infrastructure only — the shipped lab's own
  `requirements.txt` + plain `pip install -r requirements.txt` is what
  students actually use, and that works fine outside this sandbox. If a
  cached wheel isn't available for a needed package, say so explicitly
  rather than claiming validation passed without having run it.
- **PySpark/Spark labs need a JDK (8, 11, or 17) on `PATH`** — a real,
  recurring prerequisite specific to Spark-based labs (not needed for
  pandas/SQLite labs). Call this out in the student README's Environment
  section and in troubleshooting every time a lab uses PySpark, since it's
  the single most common way a student's first run fails
  (`RuntimeError: Java gateway process exited before sending its port
  number`).

## Validated patterns worth reusing

- **Local-mode PySpark testing**: a `scope="module"` (or `scope="session"`)
  pytest fixture that does
  `SparkSession.builder.master("local[*]").getOrCreate()`, with the test file
  importing the student's script directly via `sys.path.insert(0, str(STARTER_DIR))`
  rather than subprocessing it. This is the concrete working shape of "prefer
  Python plus pytest for file and ETL labs" when the ETL is specifically
  PySpark. See `apache-spark-for-beginners/student-lab/tests/test_analyze_orders.py`.
- **CSV NULL convention** (already in `lab-engineer.md`, confirmed applied
  correctly in practice): a blank CSV field represents SQL `NULL`; write
  tests that normalize incidental `""`, `NULL`, and `None` differences rather
  than asserting on the raw string.
- **Deterministic dataset sizing that worked well**: ~26-36 rows total across
  2-3 related files, with a handful (5-6) of deliberately broken rows
  covering every edge case the lab's tasks teach — small enough for a
  student to hand-verify expected output (Task 1 of
  `apache-spark-for-beginners`'s lab has students manually find the bad rows
  before writing code), large enough to be a real filter/join/aggregate
  exercise.
