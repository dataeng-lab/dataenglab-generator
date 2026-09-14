# Skill Benchmark: lab-design

**Model**: claude-sonnet-5
**Date**: 2026-09-14T18:00:00Z
**Evals**: 0, 1 (1 run each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|----------------|-------|
| Pass Rate | 100% ± 0% | 100% ± 0% | +0.00 |
| Time | 121.1s ± 76.1s | 96.9s ± 49.4s | +24.2s |
| Tokens | 135999 ± 14416 | 127806 ± 1863 | +8194 |

## Notes

- **Caveat: all four runs were rate-limit-interrupted and resumed.** Time/tokens here cover only the resumed continuation, not the full run — do not read the time/tokens delta as a real signal for this skill. Only pass_rate is trustworthy.
- Quality outcome was identical on both evals: required files present, README/`validate.json` matched exactly, no solution leaks, deterministic datasets with real edge cases, checker actually run and passing against the instructor solution while correctly failing against unmodified starters.
