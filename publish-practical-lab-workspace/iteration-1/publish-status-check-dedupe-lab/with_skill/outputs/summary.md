# Publish-practical-lab run — dedupe-late-arriving-orders-pub-ws

## Is it live yet?

**No.** This is a fresh, isolated copy of the lab (`output/dedupe-late-arriving-orders-pub-ws/`,
created solely for this evaluation by copying `output/dedupe-late-arriving-orders/`) and it has
never been submitted to the live site. Two things support that conclusion:

- There is no record anywhere in this repo of an actual live-publish action for this exact
  slug — no "published" marker, no distinct history of a Novamira call, nothing beyond local
  build artifacts.
- I did not, and under this evaluation's hard safety rule could not, make any network call or
  browser-automation call to check dataenglab.com directly (and the Novamira MCP connection
  is in any case currently unreachable — it failed to connect with a Cloudflare 525 SSL
  handshake error at the start of this session).

Note: the copied workspace already contained `elementor/labs-page.json` and `elementor/SOURCE.md`,
because those are exactly the artifacts a prior run of this same skill would produce for the
*content step* (Steps 1-3) — but a locally-built JSON file is not evidence that anything was ever
pushed to the live site via Novamira. I verified the content is slug-agnostic (no hardcoded slug or
URL baked into the JSON) and re-validated it structurally rather than assuming it was safe to reuse
blindly. Conclusion: not live. This run proceeds as a first publish, not an update.

## Reference tier used

**Tier 2** (CLAUDE.md / `.claude/rules/elementor.md` reference-tier rule).

- No root `elementor-reference.json` exists in this repo (confirmed fresh: `ls elementor-reference.json` -> "No such file or directory").
- Fell back to the checked-in `elementor/` corpus: `elementor/course-page-template.json` and
  `elementor/sections/07-faq.json` for widget types/setting keys, combined with the live theme
  tokens documented in `elementor/README.md` (indigo `#5A4FE5`, coral `#FF5A36`, teal `#0E9C8B`,
  amber `#D98F1B`, ink `#14151A` text, warm off-white `#FBFBF8` background).
- This is disclosed in `elementor/SOURCE.md`, which also restates the corpus's own
  unverified-draft status per CLAUDE.md's tier-2 requirement.

## Validator command and real result

Command run exactly as specified by the skill's Step 3:

```
python scripts/validate_elementor_json.py output/dedupe-late-arriving-orders-pub-ws/elementor/labs-page.json
```

Real output:

```
OK: output\dedupe-late-arriving-orders-pub-ws\elementor\labs-page.json
EXIT CODE: 0
```

The script confirms every element has a unique `id` and `elType`, and that `elements` arrays are
well-formed. It does **not** confirm the page renders correctly in a real Elementor instance —
nothing in this repo can verify that from here.

I also manually confirmed, by inspecting the JSON:
- The "Back to Labs" button uses `link.url: "#"` (no fabricated URL).
- No fabricated statistics anywhere in the content (only the counts already present in
  `page-content.md`, e.g. "8 rows, one per order").
- Every section of `page-content.md` (badges, lede, outcomes, dataset/environment table, tasks
  with hints folded in, expected output, troubleshooting) maps to a corresponding widget in
  `labs-page.json` (text-editor pill badges, heading + text-editor lede, icon-list outcomes,
  heading + text-editor table, accordion tasks, text-editor expected output, accordion
  troubleshooting).

## Go-ahead description (verbatim, exactly as it would be presented to the user per Step 4)

> I'd like your go-ahead to publish one page:
>
> **Page:** `dataenglab.com/labs/dedupe-late-arriving-orders-pub-ws` — this is a **new** page (it
> is not currently live; nothing at this URL exists yet).
>
> **What it will contain**, built from `output/dedupe-late-arriving-orders-pub-ws/page-content.md`:
>
> - **Header badges:** Free · Python · Beginner · 20 min · 5 tasks, plus the title "Deduplicate
>   Late-Arriving Order Events" and the lede: a support-escalation scenario where a customer's
>   order tracker shows "paid" for an order that was actually refunded three days ago, because
>   event delivery is at-least-once and can arrive out of order.
> - **What you'll learn** (outcomes checklist): recognizing that a raw event log isn't the same as
>   current state; deduplicating exact-duplicate deliveries; deterministically picking the true
>   latest record per key when the ordering column is missing or tied; surfacing a
>   dropped-duplicate signal instead of silently discarding a redelivery.
> - **Dataset section:** the `order_events` table (grain: one row per status-update delivery),
>   with its key/field/type/description breakdown (event_id, order_id, status, event_ts,
>   sequence_no) rendered as a plain HTML table inside a native text-editor widget.
> - **Tasks (accordion, 5 tabs):** Reproduce the Bug; Find Where the Extra Rows Come From; Drop
>   Exact Duplicate Deliveries (with its hint folded into the same tab); Pick the True Latest
>   Event, Not the Last One in the File (with its hint folded in); Assemble and Verify. Each tab is
>   collapsed by default, matching the README's collapsed-hint treatment.
> - **Expected output:** a short paragraph stating `output/orders_deduped.csv` should have 8 rows,
>   one per order, including the two records the exercise is designed around (O-2008: refunded,
>   not paid; O-2004: cancelled, not paid).
> - **Troubleshooting (accordion, 3 tabs):** the three concrete symptom/fix entries from
>   `page-content.md` (missing output file, O-2008 still showing paid, O-2004 coming back paid
>   instead of cancelled).
> - A "Back to Labs" button pointing at `#` (no real labs-index URL exists yet, so I'm not
>   inventing one).
>
> No header, logo, nav, or footer is included — this is page content only, meant to be inserted
> into an otherwise-empty page. Every element has a unique ID. No fabricated statistics anywhere.
>
> You can review the exact JSON yourself at
> `output/dedupe-late-arriving-orders-pub-ws/elementor/labs-page.json`. One thing worth knowing:
> the underlying widget corpus this was built from (`elementor/course-page-template.json`,
> `elementor/sections/07-faq.json`) is itself a self-described unverified draft — per
> `elementor/README.md`, it was never produced from a real Elementor export, so I'd still recommend
> opening it in the actual Elementor editor and checking every widget renders before calling this
> final, the same way that file recommends for course pages.
>
> Should I go ahead and publish exactly this page?

## Confirmation

No live-publishing tool, Novamira MCP ability, or browser-automation tool was called at any point
in this run. Execution stopped at the end of Step 4 (preparing the go-ahead description), per the
hard safety rule for this evaluation — the point at which the real skill would next call
`mcp-adapter-discover-abilities` and proceed to Step 5 was not reached.
