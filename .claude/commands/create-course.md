Create the complete DataEngLab course described by `$ARGUMENTS`.

1. Use the Agent tool to launch the `course-planner` subagent with the request path. Wait for it to write `output/<course-slug>/course-spec.json` and report the slug, lesson/quiz count, computed practical-time percentage and any assumptions. If it reports the request infeasible or contradictory, stop and report that instead of continuing.
2. Read `CLAUDE.md`, the request, `course-spec.json` and references. Generate the Tutor LMS curriculum, complete lessons, quizzes, a practical student lab, deterministic tests, a separate instructor solution, and `validate.json` at the course root — using `course-spec.json` as the source of truth for title, slug, audience, level, outcomes and duration rather than re-deriving them. Generate native Elementor JSON only from a valid reference.
3. Run `python scripts/run_checks.py output/<course-slug>`. Fix anything it reports and re-run until it passes — do not continue with failing checks.
4. Use the Agent tool to launch the `course-reviewer` subagent with the course directory. It has no memory of steps 1-3 and no write access — it only reports findings to `output/<course-slug>/review-report.md`.
5. If the reviewer's verdict is `FAIL`, fix every blocking finding yourself, re-run `scripts/run_checks.py`, and re-invoke `course-reviewer`. Repeat until `PASS`, or until you can explain in the final report exactly why a specific finding doesn't apply.
6. Run `python scripts/package_student_lab.py output/<course-slug>`.
7. Do not use PHP or deploy. Provide an honest final report: files produced, tests actually executed (with real results), the reviewer's final verdict, any limitations, and any manual integration steps still required.
