# Source disclosure — investigate-duplicate-orders lab page

Generated under tier 2 (CLAUDE.md's Elementor reference-tier rule): no
No root `elementor-reference.json` exists in this repo as of 2026-09-14.

Widget types, setting keys, and containers are traced to:
- elementor/course-page-template.json
- elementor/sections/07-faq.json

Palette uses the confirmed live theme tokens documented in `elementor/README.md`
(indigo/coral/teal/amber accents).

This corpus is itself an unverified draft (see elementor/README.md): it was
never produced from a real Elementor export, and no file here has been
confirmed to render correctly in a live Elementor editor. Review every
widget in the actual editor before treating this page as final.

## Section-by-section mapping used for this page

- Badges (Price/Topic/Level/Duration/Tasks) → one `text-editor` widget with
  inline-styled pill `<span>`s, tint varied per badge (teal/indigo/coral/amber),
  same pattern as `{{path_name}} Path` / `{{audience_N_tag}}` in
  `course-page-template.json`.
- Lede → `heading` (h1) + `text-editor` paragraph, `text_color: #54575F`.
- Outcomes → `icon-list` widget, reusing the prerequisites-list settings
  shape from `course-page-template.json`, with `fa-check` instead of
  `fa-circle` (cosmetic choice per the reference doc).
- Environment (orders / order_items) → one `heading` + `text-editor`
  (plain HTML `<table>`, inline-styled, border `#E7E3D9`) per table, the
  two tables placed side by side in a row container with `_column_size: 50`
  each, per `elementor/README.md`'s note on why `_column_size` was chosen
  over CSS Grid mode.
- Tasks → one plain `container` per task (`heading` h3 + `text-editor`
  prompt), **not** the `accordion` widget used elsewhere on this page.
  This is a deliberate departure from tier 2: the classic `accordion`
  widget's `tab_content` is a plain HTML string, so it cannot host a real
  nested widget — and Task 1 and Task 2 need one (see below). Tasks 3 and
  4's `Hint:` lines from `page-content.md` are appended inside their
  `text-editor` as an `<em>` paragraph, same as before.
- Task 1 and Task 2 code blocks → `eael-code-snippet` widget (from
  **Essential Addons for Elementor**, confirmed active on this site — not
  invented, not this repo's tier-2 corpus, and not custom-authored code).
  Found by inspecting the site's own existing `py-code-container` template
  (Saved Template ID 35461) in the live Elementor editor: its structure is
  `container > eael-code-snippet, button`, and its widget settings were
  read directly from `elementor.config.document.elements` in that editor
  (the raw stored values, not the full control-default schema) rather than
  guessed. Settings used here: `language` (`"py"` / `"sql"`, confirmed
  against the widget's own control options, which also lists `sql` as a
  distinct value from generic script languages), `code_content` (verbatim
  from the live page's `reproduce.py` / `find_grain_problem.sql` blocks,
  captured by reading the live page before this replacement), `file_name`,
  and `show_line_numbers: "yes"`. Every other one of this widget's ~80
  styling settings was left unset to inherit its plugin defaults, same
  principle as leaving typography unset elsewhere on this page.
- Expected output → a single plain `text-editor`, no special styling.
- Troubleshooting → `accordion` widget, one tab per entry, tab titles copied
  verbatim from `page-content.md` (the concrete wrong output, e.g. "Still
  17 rows instead of 12"), same boxed-container + accordion shape as
  `elementor/sections/07-faq.json` (`background_color: #FBFBF8`,
  `border_color: #E7E3D9`, `border_radius: 26px`).
- Back-to-labs / download CTA → two `button` widgets. Originally both
  linked to `#`; updated after confirming the real URLs by visiting the
  live site directly — "Back to Labs" now points to
  `https://dataenglab.com/labs/` (an existing, published page) and
  "Download starter files" to
  `https://dataenglab.com/wp-content/uploads/dataenglab-labs/investigate-duplicate-orders-lab.zip`
  (the same file already linked from the live page this replaces).

## Note: this replaces an already-published, richer page

Before this publish, `dataenglab.com/labs/investigate-duplicate-orders/`
already existed (published 2026-09-13) with content this repo did not
produce and does not have a record of: inline code snippets per task, a
working download link (now reused above), and an interactive "Solution
Checklist" with progress tracking. This page intentionally replaces that
version at the user's explicit instruction, given after being shown
exactly what would be lost.

The code snippets were recovered by finding and reusing the site's own
`eael-code-snippet` widget (see above) rather than accepting that loss.
The interactive "Solution Checklist" (client-side progress state, "0/5
complete") was **not** recovered and is dropped from this page: no
existing widget on this site provides stateful per-viewer progress
tracking, and building one would require custom JavaScript, which is
banned outright regardless of reference tier.

No fabricated statistics were added: the only numbers on the page (12 rows,
$359.00, 17 rows, $490.00, 25 min, 5 tasks) come directly from
`page-content.md`. Per-widget typography is left unset throughout so the
live Kit (`elementor-kit-652`) supplies fonts natively. Responsiveness
relies on native container flex behavior (`flex_direction`, `flex_wrap`)
exactly as the corpus does elsewhere; no explicit `_tablet`/`_mobile`
overrides were added because no section in this page needs to behave
differently on mobile.

Structural validation: `python scripts/validate_elementor_json.py
output/investigate-duplicate-orders/elementor/labs-page.json` → `OK` (exit
0). This only confirms every element has a unique `id` and `elType` and
that `elements` arrays are well-formed — it does **not** confirm the page
renders correctly in Elementor, since there is no live Elementor instance
reachable from this environment.

## 2026-09-14 update: copy pass on Environment / Task 3 / Task 4

No structural change — same widgets, same `id`s, same layout, same
palette. Only the `editor` string on five existing `text-editor` widgets
was rewritten, mirrored identically in `page-content.md` and
`student-lab/README.md`:

- The `orders` and `order_items` descriptions in Environment now use
  standard analytics-warehouse terminology (fact table, business/natural
  key, surrogate key, append-only/event-sourced) instead of plain prose.
- Task 3 and Task 4 now explain *why* the obvious-looking SQL fails —
  `GROUP BY`'s bare-column behavior on non-aggregated columns (SQLite
  returns an arbitrary row's value, it does not error), NULL comparison
  semantics on `updated_at`, and why `SUM()` silently drops a NULL
  `unit_price` instead of propagating it — rather than just stating the
  fix.

No schema field, key, row count, or dollar figure changed: `orders` and
`order_items` still have the same columns; expected output is still 12
rows / $359.00 fixed vs. 17 rows / $490.00 unfixed. Re-ran
`scripts/validate_elementor_json.py` (OK) and
`scripts/validate_lab_execution.py output/investigate-duplicate-orders`
(instructor solution still passes) after the edit — neither the lab logic
nor its tests were touched, only prose.

This update exists only in this repo's `output/` directory. It has **not**
been published to dataenglab.com; the live page still reflects whatever
was last approved and pushed there.
