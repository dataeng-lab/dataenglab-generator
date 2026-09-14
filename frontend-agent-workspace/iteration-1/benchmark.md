# Skill Benchmark: frontend-agent

**Model**: claude-sonnet-5
**Date**: 2026-09-14T18:00:00Z
**Evals**: 0, 1 (1 run each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|----------------|-------|
| Pass Rate | 100% ± 0% | 92% ± 12% | +0.08 |
| Time | 281.5s ± 50.3s | 278.7s ± 69.4s | +2.9s |
| Tokens | 106466 ± 21454 | 119514 ± 8341 | -13048 |

## Notes

- The one real quality gap in the whole 16-run eval is here: the without_skill run on eval 1 hallucinated a claim about CLAUDE.md's own content ("Brand section lists #3D73FF") that does not exist, inside its own SOURCE.md disclosure — even though the color it actually picked was correct.
- A near-identical hallucination appeared independently in the course-design without_skill run, for a completely different eval — suggests a reproducible failure mode ("this project used to have a blue palette, so CLAUDE.md must still say so") rather than a frontend-agent-specific issue. Neither with_skill run made this mistake.
- Both without_skill runs showed a shortcut tendency under pressure: one reused an existing file verbatim instead of regenerating; the other fabricated a source citation. Neither with_skill run did either.
- Both configurations correctly caught and overrode a stale `REFERENCE_REQUIRED.md` verdict already sitting in the real `output/test-course/` output.
