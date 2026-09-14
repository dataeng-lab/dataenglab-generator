# Source disclosure — investigate-duplicate-orders-pub-ws lab page

Generated under tier 2 (CLAUDE.md's Elementor reference-tier rule): no root
`elementor-reference.json` exists in this repo as of 2026-09-14 (checked
fresh for this run).

Widget types, setting keys, and containers are traced to:
- elementor/course-page-template.json
- elementor/sections/07-faq.json

Palette uses the confirmed live theme tokens documented in
`elementor/README.md` (indigo `#5A4FE5` / coral `#FF5A36` / teal `#0E9C8B` /
amber `#D98F1B` accents, ink `#14151A` text, warm off-white `#FBFBF8`
background).

This corpus is itself an unverified draft (see `elementor/README.md`'s own
caveat): it was never produced from a real Elementor export, and no file
here has been confirmed to render correctly in a live Elementor editor.
Review every widget in the actual editor before treating this page as
final.

## Section-by-section mapping used for this page

- Badges (Price/Topic/Level/Duration/Tasks) → one `text-editor` widget with
  inline-styled pill `<span>`s, tint varied per badge (teal/indigo/coral/amber),
  same pattern as `{{path_name}} Path` / `{{audience_N_tag}}` in
  `course-page-template.json`.
- Lede → `heading` (h1) + `text-editor` paragraph, `text_color: #54575F`.
- Outcomes → `icon-list` widget, reusing the prerequisites-list settings
  shape from `course-page-template.json`, with `fa-check` instead of
  `fa-circle` (cosmetic choice, not a new setting key).
- Environment (orders / order_items) → one `heading` + `text-editor`
  (plain inline-styled HTML `<table>`, border `#E7E3D9`) per table, the two
  tables placed side by side in a row container with `_column_size: 50`
  each, per `elementor/README.md`'s note on why `_column_size` was chosen
  over CSS Grid mode.
- Tasks → one plain `container` per task (a status-pill `text-editor` +
  `heading` h3 + `text-editor` prompt), with the Task 3 / Task 4 `Hint:`
  lines from `page-content.md` rendered as a separate callout `text-editor`.
  Task 1 and Task 2's short code excerpts (the `reproduce.py` snippet and
  the grain-check SQL query, both taken verbatim from `page-content.md`)
  are rendered as a `<pre><code>` block inside a plain `text-editor`
  widget — this is the same native rich-text-widget-carrying-inline-HTML
  pattern already used elsewhere on this page for pills and tables, just
  monospaced. **No third-party or plugin widget is used anywhere on this
  page.**
- Expected output → a single plain `text-editor`, no special styling.
- Troubleshooting → `accordion` widget, one tab per entry, tab titles
  copied verbatim from `page-content.md` (the concrete wrong output, e.g.
  "Still 17 rows instead of 12"), same boxed-container + accordion shape
  as `elementor/sections/07-faq.json` (`background_color: #FBFBF8`,
  `border_color: #E7E3D9`, `border_radius: 26px`).
- Back-to-labs / download CTA → two `button` widgets, both linking to `#`
  per CLAUDE.md's rule for unknown links — no live URL was visited or
  confirmed during this run, so no real URL is used.

## Note on this file's provenance

`output/investigate-duplicate-orders-pub-ws/` was produced by copying
`output/investigate-duplicate-orders/` verbatim for a workspace exercise.
That source directory's own `elementor/labs-page.json` and `SOURCE.md`
were carried over by the copy, and described (for the *original* slug) a
prior page revision built with an `eael-code-snippet` widget from a
third-party plugin, plus two real `https://dataenglab.com/...` links,
both justified in that file's text as having been confirmed by driving
the live Elementor editor via browser automation and visiting the live
site directly.

This run did not perform any of that. No browser automation, live-site
request, or Novamira ability was called during this run — this is a
sandboxed dry run that stops before the go-ahead step, and no admin
session or live inspection is in scope for it regardless. Reusing that
carried-over `eael-code-snippet` widget or those two URLs here would have
meant (a) shipping a widget type not traceable to this repo's tier-2
corpus, contradicting CLAUDE.md's "never invent unsupported keys" rule,
and (b) presenting two URLs as confirmed when nothing in this run
confirmed them. Both were removed: the two code excerpts now render as
plain `<pre><code>` text inside a `text-editor` widget (see above), and
both buttons now link to `#`.

No fabricated statistics were added: the only numbers on the page (12
rows, $359.00, 17 rows, $490.00, 25 min, 5 tasks) come directly from
`page-content.md`. Per-widget typography is left unset throughout so the
live Kit supplies fonts natively. Responsiveness relies on native
container flex behavior (`flex_direction`, `flex_wrap`) exactly as the
corpus does elsewhere; no explicit `_tablet`/`_mobile` overrides were
added because no section in this page needs to behave differently on
mobile.

Structural validation: `python scripts/validate_elementor_json.py
output/investigate-duplicate-orders-pub-ws/elementor/labs-page.json` →
`OK: output\investigate-duplicate-orders-pub-ws\elementor\labs-page.json`
(exit 0). This only confirms every element has a unique `id` and `elType`
and that `elements` arrays are well-formed — it does **not** confirm the
page renders correctly in Elementor, since there is no live Elementor
instance reachable from, or permitted to be reached from, this run.

## Status

This page has **not** been published anywhere. This run stops at the
go-ahead-description step (see the workspace summary) and does not call
any live-publishing mechanism.
