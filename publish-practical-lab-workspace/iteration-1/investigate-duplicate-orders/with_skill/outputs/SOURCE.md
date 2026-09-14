# Source disclosure — investigate-duplicate-orders lab page

Generated under tier 2 (CLAUDE.md's Elementor reference-tier rule): no
`references/elementor-reference.json` exists in this repo as of 2026-09-14.

Widget types, setting keys, and containers are traced to:
- elementor/course-page-template.json
- elementor/sections/07-faq.json

Palette is the confirmed live theme from references/dataenglab-live-theme.md
(indigo/coral/teal/amber accents), not references/brand.md.

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
- Tasks (with hints folded in) → `accordion` widget, one tab per task,
  modeled on the module accordion in `course-page-template.json`. Tasks 3
  and 4's `Hint:` lines from `page-content.md` are appended inside their
  tab's `tab_content` as an `<em>` paragraph.
- Expected output → a single plain `text-editor`, no special styling.
- Troubleshooting → `accordion` widget, one tab per entry, tab titles copied
  verbatim from `page-content.md` (the concrete wrong output, e.g. "Still
  17 rows instead of 12"), same boxed-container + accordion shape as
  `elementor/sections/07-faq.json` (`background_color: #FBFBF8`,
  `border_color: #E7E3D9`, `border_radius: 26px`).
- Back-to-labs / download CTA → two `button` widgets, both linking to `#`
  since no real labs-index URL or packaged-zip URL exists yet — never
  invented per CLAUDE.md's Elementor rules.

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
