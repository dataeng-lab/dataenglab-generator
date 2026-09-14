# Troubleshooting — Reconstruct Customer Plan History (instructor-facing)

**"My query passes test_one_row_per_order but fails
test_matches_expected_plan_attribution"**
Grain is right but a value is wrong. Ask the student to check, in order:
1. Is the mismatch specifically on `C-04`'s orders around
   `2024-04-10 14:00:00`? That's almost always the missing `event_id`
   tie-break in the `LEAD()` window — see the next item.
2. Is the mismatch on `O-013` (`C-06`)? Check whether they're using an
   `INNER JOIN` (which drops the row — see `test_one_row_per_order` failure
   instead) or a `LEFT JOIN` that's still matching it to `C-06`'s single
   `Pro` event despite the order being before that event's `changed_at`.
   That means their interval condition (`o.order_ts >= v.valid_from`) isn't
   actually being enforced, or they added a fallback like
   `COALESCE(v.plan, (SELECT plan FROM customer_plan_events WHERE ... LIMIT 1))`
   that reintroduces a guess.
3. Is the mismatch on `C-03`'s two orders? Confirm the Task 3 branch is
   present in the `UNION ALL` and that its column list/order lines up with
   the Task 2 branch (a silently mismatched column order can put the wrong
   value in the wrong output column without SQLite complaining).

**"C-04's orders on or after 2024-04-10 14:00:00 come out `Pro` instead of
`Enterprise`, and it's inconsistent between runs"**
This is the exact-timestamp tie (`event_id` 7 and 8, both
`changed_at = '2024-04-10 14:00:00'`). Without `event_id` as a secondary
`ORDER BY` key inside the `LEAD()` window, SQLite doesn't guarantee which of
the two tied rows it treats as coming "first," so `LEAD()` can assign
`valid_to` inconsistently across runs. Have the student add `, event_id` to
the `ORDER BY` (ascending, since higher `event_id` = happened later even
when the timestamp can't prove it) and re-run — the result should become
stable and match `customers.current_plan` (`Enterprise`) for `C-04`.

**"Row count is less than 15"**
An `INNER JOIN` in Task 4 instead of `LEFT JOIN`. `O-013` has no matching
plan version by design (it predates `C-06`'s earliest event) and must still
appear in the output with `plan_at_order = NULL`.

**"O-013 shows plan_source = NULL instead of 'unknown_pre_history'"**
The `LEFT JOIN` is correct (the row survives), but the `plan_source` column
needs its own `COALESCE`/`CASE` fallback for the unmatched case — it isn't
automatically populated just because `plan_at_order` came out `NULL`.

**"I get a syntax error near SELECT"**
The starter `solution.sql` ships with a placeholder `SELECT 1;` — make sure
the whole placeholder block (including the outline comment above it) was
replaced, not appended to.

**"Should C-06's O-013 just inherit the Pro plan from their first event,
since that's the closest thing we know?"**
This is a good discussion prompt, not a bug. The lab's position is
deliberate: `C-06` clearly changed plans at least once (an event exists),
so there is no basis for assuming which plan came before it — it could have
been any plan, including one that was never logged. Silently backfilling
with the first known plan is exactly the kind of unearned confidence this
lab is trying to train students out of. If a real team decided backfilling
was an acceptable business tradeoff, that should be an explicit, documented
decision — not something a query does by default.

**A student "fixes" this by dropping C-06 or C-03 from the dataset in their
head and only handling the "normal" customers**
There's nothing to drop — both are real edge cases the automated check
grades on. If a student's query only handles customers who have plan
history that fully covers their order history, `test_matches_expected_plan_attribution`
will catch the gap on `C-03` and/or `C-06`'s rows.
