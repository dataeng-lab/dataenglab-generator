# Skill Benchmark: course-design

**Model**: claude-sonnet-5
**Date**: 2026-09-14T18:00:00Z
**Evals**: 0, 1 (1 run each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|----------------|-------|
| Pass Rate | 100% ± 0% | 100% ± 0% | +0.00 |
| Time | 1734.7s ± 1877.0s | 1953.3s ± 2378.9s | -218.6s |
| Tokens | 161116 ± 101258 | 186341 ± 167595 | -25226 |

## Notes

- Both configurations ultimately reached PASS on both evals — the review gate (`scripts/run_checks.py` + the `course-reviewer` agent) enforces quality regardless of whether the skill's own workflow prose is followed, because `course-reviewer` is reachable directly as an Agent-tool subagent_type even without the skill.
- The real differentiator was convergence speed on a recurring leaked-solution defect: with_skill needed 2 review rounds to stop it from relocating between files; without_skill needed 4.
- With_skill used ~14% less time and ~14% fewer tokens on average across both evals for the same real PASS outcome.
