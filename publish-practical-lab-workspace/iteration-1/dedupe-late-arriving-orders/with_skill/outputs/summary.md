# Publish dry run — dedupe-late-arriving-orders lab

## Reference tier resolved

**Tier 2.** Checked `references/elementor-reference.json` fresh (per SKILL.md's
instruction not to assume it stays absent) — it does not exist; only
`references/brand.md`, `references/dataenglab-live-theme.md`, and
`references/README.md` are present. Per CLAUDE.md's and the skill's
three-tier rule, that means tier 1 is unavailable and tier 2 applies:

- Widget types, setting keys, and container conventions traced to
  `elementor/course-page-template.json` and `elementor/sections/07-faq.json`
  (confirmed by direct inspection — `icon-list`, `accordion`, `button`,
  `text-editor`, `container` with `_column_size`/`flex_direction`/
  `border_radius` all copied from real elements in those files, nothing
  invented).
- Palette taken from `references/dataenglab-live-theme.md` (confirmed live
  theme tokens: indigo `#5A4FE5`, coral `#FF5A36`, teal `#0E9C8B`, amber
  `#D98F1B`, ink `#14151A`, warm off-white `#FBFBF8`) rather than the
  superseded blue palette in `references/brand.md` / CLAUDE.md's top-level
  Brand section, per the skill's explicit override for Elementor generation.

This was a first publish, not an update — `output/dedupe-late-arriving-orders/elementor/`
did not exist before this run (checked in Step 0).

## What was built

- `output/dedupe-late-arriving-orders/elementor/labs-page.json` — native
  Elementor JSON, no header/logo/nav/footer, page content only. Sections:
  badges row (5 pills, color-varied per the tint palette), title + lede,
  outcomes checklist (`icon-list`, `fa-check`), dataset table
  (`order_events`, via a `text-editor` with a plain HTML `<table>` — same
  native-widget pattern the corpus already uses for inline-styled spans,
  not the banned Elementor HTML widget), a 5-task `accordion` with hints
  folded into Tasks 3 and 4's `tab_content`, an expected-output paragraph,
  and a troubleshooting `accordion` (3 entries, copied verbatim from
  `page-content.md`'s symptom wording). A "Back to Labs" button uses
  `"url": "#"` since no real labs-index URL exists yet. Every element has a
  unique `id`; no fabricated stats appear anywhere. Typography left unset
  per-widget so the live Kit (`elementor-kit-652`) supplies fonts natively.
- `output/dedupe-late-arriving-orders/elementor/SOURCE.md` — tier-2
  disclosure naming the exact corpus files and palette source used, and
  restating `elementor/README.md`'s own unverified-draft caveat.

Both files are also copied into this outputs folder alongside this file.

## Validator run (real, executed)

Command:

```
python scripts/validate_elementor_json.py output/dedupe-late-arriving-orders/elementor/labs-page.json
```

Output:

```
OK: output\dedupe-late-arriving-orders\elementor\labs-page.json
```

Exit status: **0** (success). The script parsed the JSON, walked every
`content` element, confirmed each has a non-empty string `id` and an
`elType`, confirmed `elements` children are well-formed lists, and found no
duplicate IDs. As the skill notes, this only checks structure — it does not
and cannot confirm the page renders correctly in a live Elementor editor,
since no live Elementor instance is reachable from this environment.

## Stopping point — DRY RUN, no live call made

Per the task's safety constraint, no Novamira MCP ability (`novamira/*`,
`angie/*`, `mcp-adapter-execute-ability`) and no publish-capable browser
automation was called. The workflow reached Step 4 of the skill
("describe the change and get explicit go-ahead") and stopped there. Step 5
(the actual publish call) and Step 6 (report back on the live result) were
**not** executed.

If this were a real run, this is the exact message that would be shown to
the user at this stopping point, verbatim:

---

**Here's the change I'd publish — please confirm before I touch the live site.**

**Page:** `dataenglab.com/labs/dedupe-late-arriving-orders` — this is a **new**
page (no existing published version was found for this slug).

**What it will contain**, section by section:

1. **Badges** — Free · Python · Beginner · 20 min · 5 tasks
2. **Title + lede** — "Deduplicate Late-Arriving Order Events," with the
   business scenario: support escalated that an order tracker shows an
   order as paid when it was actually refunded three days ago, because
   event delivery is at-least-once and can arrive out of order.
3. **What you'll learn** — a 4-item checklist (recognizing that row order
   isn't chronology, deduplicating exact-duplicate deliveries, picking the
   true latest record with a documented tie-break, surfacing a
   dropped-duplicate signal instead of silently discarding it).
4. **Dataset** — the `order_events` table schema (event_id, order_id,
   status, event_ts, sequence_no) with its grain and duplicate-delivery
   caveat, as a plain HTML table.
5. **Tasks** — an accordion with all 5 tasks (reproduce the bug, find the
   extra rows, drop exact duplicates, pick the true latest event, assemble
   and verify), with the two documented hints folded into Tasks 3 and 4's
   collapsed content.
6. **Expected output** — 8 rows, one per order, including the two corrected
   statuses (O-2008 refunded, O-2004 cancelled).
7. **Troubleshooting** — an accordion with the 3 documented symptoms and
   fixes, worded exactly as in `page-content.md`.
8. A "Back to Labs" button linking to `#` (no real labs-index URL exists
   yet to link to).

No header, logo, nav, or footer is included — this is page content only,
meant to be inserted into an otherwise-empty page. No fabricated statistics
appear anywhere on the page.

**Where to look:** the full JSON is at
`output/dedupe-late-arriving-orders/elementor/labs-page.json`, and the
source disclosure is at `output/dedupe-late-arriving-orders/elementor/SOURCE.md`.
It passed the repo's structural validator (unique IDs, valid element tree)
with exit code 0, but — worth flagging plainly rather than burying — the
underlying widget corpus this JSON extends is itself a self-described
unverified draft (`elementor/README.md`: "Neither file was produced from a
real Elementor export... import into a staging site and check every widget
renders before trusting them"). I'd want you to open this in the actual
Elementor editor and check it renders as expected before we call it done.

**If you say yes**, here's exactly what happens next and nothing else: I'll
run `mcp-adapter-discover-abilities` to see what's currently available, then
publish this one page — either via Elementor kit settings if it turns out to
be kit-level (it isn't, this is page content, so this branch won't apply) or,
the expected path, by driving the Elementor editor UI directly through
browser automation using an admin session from
`novamira/create-admin-access-link`, importing `labs-page.json` through
Elementor's native Template Library. I will not run any PHP, touch the
database directly, or edit a theme/plugin file, even if an available ability
claims that's fine for "small content changes." And this approval covers
only this one lab page — nothing else gets published under it.

**Do you want me to go ahead and publish this page?**

---

No such "yes" was given or simulated in this dry run — this document is the
stopping point. Nothing under `novamira/*`, `angie/*`, or any
publish-capable browser-automation ability was invoked.
