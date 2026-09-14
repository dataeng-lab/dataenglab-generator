---
paths:
  - "scripts/**"
  - "output/**"
  - ".claude/agents/course-reviewer.md"
  - ".claude/skills/course-design/**"
  - ".claude/skills/lab-design/**"
---

# Validation And Reporting Rules

- Never claim a check passed unless you ran it and saw it pass.
- Never claim review passed unless `course-reviewer` produced a PASS verdict.
- Never claim Elementor import/rendering was verified unless you actually opened the output in a real Elementor editor and checked it.
- Never claim publishing succeeded unless the live change was actually applied and inspected.

Use the combined checker first:

```powershell
python scripts/run_checks.py output/<slug>
```

For focused debugging:

```powershell
python scripts/validate_spec.py output/<slug>
python scripts/validate_course.py output/<slug>
python scripts/validate_content.py output/<slug>
python scripts/validate_lab.py output/<slug>/student-lab
python scripts/validate_lab_execution.py output/<slug>
python scripts/validate_elementor_json.py output/<slug>/elementor/landing-page.json
```

Report the slug, files changed, validation commands and real results, review verdict, package path when created, Context7 status for technical content, and any remaining limitations.

