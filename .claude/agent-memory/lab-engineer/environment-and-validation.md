# Environment And Validation Notes

Durable facts from prior DataEngLab lab builds.

## Environment Facts

- Context7 MCP tools may be unavailable inside a `lab-engineer` subagent even
  when the parent session can use them. Try Context7 when needed; if it is not
  available, proceed with stable patterns and report the limitation.
- The sandbox may lack outbound network access, so fresh `pip install` can fail.
  For local validation, prefer already-cached wheels or standard-library labs
  when possible. Do not claim validation passed unless it really ran.
- PySpark/Spark labs need a JDK on `PATH` (commonly Java 8, 11, or 17). Include
  this in the student README and troubleshooting because missing Java commonly
  fails with a Java gateway error.

## Validated Patterns

- Local-mode PySpark tests can use a module/session-scoped pytest fixture with
  `SparkSession.builder.master("local[*]").getOrCreate()`, importing the
  student's starter script directly with `sys.path.insert`.
- Blank CSV fields represent SQL `NULL`; tests should normalize incidental
  `""`, `NULL`, and `None` differences when those distinctions are not the
  lesson objective.
- Effective lab datasets have been small and inspectable: roughly 25-40 rows
  across 2-3 related files, with a handful of deliberate broken rows covering
  every edge case the tasks teach.
