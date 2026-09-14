# DataEngLab Course Factory

This repository generates content-only Data Engineering learning assets for
DataEngLab:

- complete Tutor LMS courses with a practical lab;
- standalone practical labs;
- native Elementor JSON when a valid reference tier exists;
- validation reports, instructor-only material, and student ZIP packages.

Claude Code loads this file together with project rules in `.claude/rules/`.
Keep this file as the short project overview. Put durable, topic-specific
instructions in `.claude/rules/*.md`, detailed workflows in `.claude/skills/`,
and specialized subagent behavior in `.claude/agents/`.

Use the repo skills for substantial work:

- `course-design` for complete courses;
- `lab-design` for standalone labs;
- `frontend-agent` for course Elementor output;
- `publish-practical-lab` only for approved live publishing of an existing lab.

Never claim validation, review, Elementor import, or publishing succeeded unless
you actually performed the relevant action and saw it succeed.
