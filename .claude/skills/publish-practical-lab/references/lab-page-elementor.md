# Lab page → Elementor mapping

Concrete section-by-section guidance for turning `output/<slug>/page-content.md`
into `output/<slug>/elementor/labs-page.json`, under the tier-2 reference rule
(no `references/elementor-reference.json` in this repo as of this writing).
Every widget type and setting key below is copied from, or a direct extension
of, real elements already in `elementor/course-page-template.json` and
`elementor/sections/07-faq.json` — check those files yourself if something
here seems ambiguous, rather than guessing a new key.

## Palette (confirmed live tokens — see `references/dataenglab-live-theme.md`)

| Role | Hex |
|---|---|
| Primary text (ink) | `#14151A` |
| Secondary text | `#54575F` |
| Tertiary text | `#92959E` |
| Page background | `#FBFBF8` |
| Card/panel background | `#FFFFFF` |
| Alt surface | `#F3F1EA` |
| Border | `#E7E3D9` |
| Primary accent (indigo) | `#5A4FE5` |
| Primary accent hover | `#372DBF` |
| Primary accent tint bg | `#ECEAFB` |
| Secondary accent (coral) | `#FF5A36` / tint `#FFEAE2` |
| Tertiary accent (teal) | `#0E9C8B` / tint `#E0F4F1` |
| Quaternary accent (amber) | `#D98F1B` / tint `#FBEED9` |

Radii: 10px small, 16px medium, 26px large (cards/sections), 999px pills.

**Do not use `references/brand.md`'s palette** (`#3D73FF` blue) for this JSON — see the note in SKILL.md Step 1 about why that file doesn't apply to Elementor generation even though CLAUDE.md's own top-level Brand section repeats it.

## Section mapping

### Badges (Price / Topic / Level / Duration / Tasks)

One `text-editor` widget per badge row, containing inline-styled pill spans — the exact pattern already used for `{{path_name}} Path` and `{{audience_N_tag}}` in `course-page-template.json`:

```json
{
  "id": "<unique>",
  "elType": "widget",
  "widgetType": "text-editor",
  "settings": {
    "editor": "<span style=\"display:inline-flex;align-items:center;padding:6px 12px;margin:0 8px 8px 0;border-radius:999px;font-size:13px;font-weight:700;background:#E0F4F1;color:#0E9C8B;border:1px solid #E0F4F1;\">Free</span><span style=\"display:inline-flex;align-items:center;padding:6px 12px;margin:0 8px 8px 0;border-radius:999px;font-size:13px;font-weight:700;background:#ECEAFB;color:#5A4FE5;border:1px solid #ECEAFB;\">SQL</span>"
  },
  "elements": []
}
```

Vary the tint per badge (teal/indigo/coral/amber) the same way the corpus varies audience tags — don't make every pill the same color.

### Lede

A `heading` widget (title, `header_size` around `h1`/`h2`) followed by a `text-editor` with the lede paragraph in a `<p>` tag, `text_color: "#54575F"` — same as the course template's pitch line.

### Outcomes (checklist)

`icon-list` widget, one entry per outcome, reusing the exact settings shape from the prerequisites list in `course-page-template.json`:

```json
{
  "widgetType": "icon-list",
  "settings": {
    "icon_list": [
      {"text": "<outcome text>", "selected_icon": {"value": "fas fa-check", "library": "fa-solid"}, "_id": "<unique>"}
    ],
    "icon_color": "#0E9C8B",
    "text_color": "#14151A"
  }
}
```

(Use `fa-check` rather than the course template's `fa-circle` — an outcome checklist reads better with a checkmark; this is a cosmetic choice, not a new setting key.)

### Environment (one block per table/data source)

There's no native Elementor "table" widget in this corpus. Follow the same pattern the corpus already uses for the pill spans — raw, plainly-styled HTML inside a `text-editor` widget's `editor` field. This is not the banned "Elementor HTML widget"; it's the same native rich-text widget already carrying inline HTML elsewhere in this corpus, just with a `<table>` instead of `<span>`s. One `text-editor` per table, preceded by a `heading` for the table name + grain description:

```json
{
  "widgetType": "text-editor",
  "settings": {
    "editor": "<table style=\"width:100%;border-collapse:collapse;font-size:14px;\"><tr style=\"border-bottom:1px solid #E7E3D9;\"><th style=\"text-align:left;padding:8px;color:#54575F;\">Field</th><th style=\"text-align:left;padding:8px;color:#54575F;\">Type</th><th style=\"text-align:left;padding:8px;color:#54575F;\">Description</th></tr><tr style=\"border-bottom:1px solid #E7E3D9;\"><td style=\"padding:8px;\">order_id</td><td style=\"padding:8px;\">text</td><td style=\"padding:8px;\">The order's business ID</td></tr></table>"
  }
}
```

Keep the styling minimal and consistent across every table on the page — border color `#E7E3D9`, text color `#54575F` for headers, `#14151A` for body — rather than inventing a new look per table.

### Tasks (with hints folded in)

`accordion` widget, one tab per task — directly modeled on the module accordion in `course-page-template.json`:

```json
{
  "widgetType": "accordion",
  "settings": {
    "tabs": [
      {
        "tab_title": "Task 1 — Reproduce the Bug",
        "tab_content": "<p>Run the current dashboard query...</p>",
        "_id": "<unique>"
      },
      {
        "tab_title": "Task 3 — Deduplicate to One Row per Order",
        "tab_content": "<p>Keep only the latest version...</p><p><em>Hint: Partition by order_id, order by the coalesced timestamp then version, keep rn = 1.</em></p>",
        "_id": "<unique>"
      }
    ],
    "title_color": "#14151A",
    "content_color": "#54575F",
    "border_color": "#E7E3D9"
  }
}
```

Where `page-content.md` has a `Hint:` line under a task, append it inside that same tab's `tab_content` as an `<em>` line, exactly like the second example above — this mirrors the collapsed-by-default `<details>` treatment hints get in the README, since the whole tab (prompt + hint) stays collapsed until a student opens it.

### Expected output

A single `text-editor`, plain paragraph(s), no special styling — this section is short and factual in every existing lab.

### Troubleshooting

Another `accordion`, one tab per troubleshooting entry, `tab_title` the symptom the student would actually see (copy `page-content.md` verbatim — that file was already written to name the concrete wrong output, e.g. "Still 17 rows instead of 12" not "dedup didn't work"), `tab_content` the explanation. This is the same shape as the FAQ accordion already built in `elementor/sections/07-faq.json` — reuse its `heading` + `accordion` container pattern (boxed container, `background_color: "#FBFBF8"`, `border_color: "#E7E3D9"`, `border_radius: 26px`) for the section wrapper.

## Container conventions (from the corpus)

Wrap each major section in a `container` with settings like:

```json
{
  "elType": "container",
  "settings": {
    "content_width": "boxed",
    "flex_direction": "column",
    "flex_gap": {"unit": "px", "size": 20},
    "padding": {"unit": "px", "top": "48", "right": "28", "bottom": "48", "left": "28", "isLinked": false},
    "background_background": "classic",
    "background_color": "#FBFBF8",
    "border_border": "solid",
    "border_color": "#E7E3D9",
    "border_width": {"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": true},
    "border_radius": {"unit": "px", "top": "26", "right": "26", "bottom": "26", "left": "26", "isLinked": true}
  },
  "elements": []
}
```

Alternate `background_color` between `#FBFBF8` (page bg) and `#FFFFFF` (card surface) between adjacent sections so they read as distinct cards, the same way the course template alternates them.

For a row of side-by-side items (e.g. two environment tables), use an inner `container` with `flex_direction: "row"`, `flex_wrap: "wrap"`, and `_column_size` on each child (e.g. `50` for two-up) — not CSS Grid mode, per `elementor/README.md`'s note on why `_column_size` was chosen.

## SOURCE.md template

Write `output/<slug>/elementor/SOURCE.md` with this shape:

```markdown
# Source disclosure — <slug> lab page

Generated under tier 2 (CLAUDE.md's Elementor reference-tier rule): no
`references/elementor-reference.json` exists in this repo as of <date>.

Widget types, setting keys, and containers are traced to:
- elementor/course-page-template.json
- elementor/sections/07-faq.json

Palette is the confirmed live theme from references/dataenglab-live-theme.md
(indigo/coral/teal/amber accents), not references/brand.md.

This corpus is itself an unverified draft (see elementor/README.md): it was
never produced from a real Elementor export, and no file here has been
confirmed to render correctly in a live Elementor editor. Review every
widget in the actual editor before treating this page as final.
```
