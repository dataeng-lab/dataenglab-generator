---
paths:
  - "output/**/student-lab/**"
  - "output/**/instructor/**"
  - "output/**/validate.json"
  - "output/**/lab-spec.md"
  - "output/**/page-content.md"
  - ".claude/skills/lab-design/**"
  - ".claude/agents/lab-engineer.md"
---

# Lab Rules

Every lab must have:

- a realistic business context;
- measurable learning objectives;
- deterministic data with deliberate edge cases;
- starter files under `student-lab/starter/`;
- automated tests under `student-lab/tests/`;
- instructor solutions under `instructor/solution/`;
- concrete setup, validation, and reset instructions;
- troubleshooting guidance.

Never put working solutions, answer keys, or instructor-only troubleshooting inside `student-lab/`.

The root `validate.json` must contain argv arrays executed from inside `student-lab/`:

```json
{
  "setup": [["python", "build_db.py"]],
  "validate": [["python", "tests/test_solution.py"]]
}
```

`validate` is mandatory. README validation commands must match `validate.json` exactly. Validation must exit non-zero when the solution is wrong.

