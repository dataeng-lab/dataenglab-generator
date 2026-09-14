# Instructor Guide — Reconstruct Customer Plan History

## What this lab is really testing

Most students can write a `JOIN`. This lab checks whether they notice that a
"current state" column carries no history at all, and whether they can
rebuild that history from a change log correctly — including refusing to
guess when the log doesn't reach far enough back. That last part (Task 4)
is the habit that separates a report that's "probably fine" from one that's
actually trustworthy.

## Root cause, in one sentence

`customers.current_plan` is overwritten in place on every plan change, so
joining orders to it attributes every historical order — regardless of when
it was placed — to whatever plan the customer happens to be on today.

## Before / after (verified by running the queries against `lab.db`)

Both reports sum to the same total ($1,635.00 across all 15 orders) — the
bug isn't lost or duplicated revenue, it's revenue landing in the *wrong
tier*, which is exactly the kind of error that's easy to miss because the
grand total still reconciles.

| Plan | Naive report (buggy) | Reconstructed (correct) |
|---|---|---|
| Starter | $210.00 | $550.00 |
| Pro | $285.00 | $395.00 |
| Enterprise | $1,140.00 | $650.00 |
| Unattributed (`unknown_pre_history`) | $0.00 (never surfaced) | $40.00 (`O-013`, flagged) |
| **Total** | **$1,635.00** | **$1,635.00** |

The naive report overstates Enterprise revenue by $490.00 and understates
Starter by $340.00 and Pro by $110.00 — and it never reveals that $40.00 of
revenue (`O-013`) can't actually be attributed to any known plan, because it
guesses instead of leaving a gap.

## Dataset cheat sheet

| `customer_id` | Events | Why it's interesting |
|---|---|---|
| C-01 Acme Inc | 3 (Starter→Pro→Enterprise) | Baseline case: three orders, one per plan era — proves the naive report mislabels all three as `Enterprise` |
| C-02 Beta LLC | 2 (Starter→Pro) | Simple control, no ties |
| C-03 Gamma Co | **0** | Never appears in `customer_plan_events` — `current_plan` (`Starter`) is their only history, valid since `signup_ts` forever |
| C-04 Delta Corp | 3, **two with an identical `changed_at`** | `event_id` 7 (`Pro`) and 8 (`Enterprise`) both stamped `2024-04-10 14:00:00` — needs `event_id` as a tie-break in the `LEAD()` window; `O-009` lands exactly on that boundary instant |
| C-05 Epsilon Ltd | 2 (Starter→Enterprise) | Second simple control, confirms Task 2 logic generalizes |
| C-06 Zeta Group | 1 (`Pro`, effective `2024-03-01`) | `O-013` (placed `2024-02-15`) predates that single event — the "before recorded history" case; must resolve to `NULL`/`unknown_pre_history`, not a guess |
| C-07 Theta Partners | 1 (matches `signup_ts`) | Distinguishes "one event that coincides with signup" from C-03's "zero events" — both end up fully known, by different code paths |

## Where students typically go wrong

- Using `ORDER BY changed_at` alone inside the `LEAD()` window with no
  tie-break — for `C-04` this is non-deterministic (SQLite doesn't guarantee
  which of two exactly-tied rows sorts first), so the same query can pass or
  fail on different runs, or silently pick the wrong plan and disagree with
  `customers.current_plan`. Point out that `customers.current_plan` for
  `C-04` (`Enterprise`) is a built-in sanity check students can use against
  their own tie-break direction.
- Using an `INNER JOIN` in Task 4 instead of `LEFT JOIN` — this makes
  `O-013` disappear from the result entirely rather than appearing with
  `plan_at_order = NULL`, which breaks `test_one_row_per_order`'s
  expectation of exactly 15 output rows.
- Treating `C-03` (zero events) and `C-06` (order before the one event that
  exists) as the same situation and applying the Task 3 "current plan
  applies forever" logic to both. They are not the same: `C-06` has proof
  a change happened at some point, so nothing before that first event can
  be assumed known.
- Forgetting to `UNION ALL` the Task 3 branch at all, which leaves `C-03`
  with zero plan versions and turns both of their orders into unmatched
  (`unknown_pre_history`) rows instead of `current_plan_only`.

## Grading

Run `python tests/test_solution.py` against the student's `solution.sql`.
All four checks (`test_has_required_columns`, `test_one_row_per_order`,
`test_plan_source_values_are_valid`, `test_matches_expected_plan_attribution`)
must pass. There's no partial credit built into the script — if the intent
is to grade tasks individually, use the per-order breakdown in
`tests/expected_orders.csv` as an answer key instead of the automated
pass/fail.
