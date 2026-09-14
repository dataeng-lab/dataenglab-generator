# dataenglab.com live theme tokens

Captured 2026-08-04 via in-browser DOM/computed-style inspection of the live
homepage (`https://dataenglab.com`, WordPress 6.9.5, Elementor page,
`elementor-kit-652`, `elementor-page-35747`). Confirmed as real Elementor
(`elementor-element` classes present, 143 elements on the page) with these
values declared as page-scoped CSS custom properties in an inline `<style>`
block (`href: null` in `document.styleSheets`, not a shared stylesheet).

This is **not** a full `elementor-reference.json` export — the WordPress REST
API does not expose `_elementor_data` (protected meta), so the underlying
widget/setting-key schema still cannot be verified from here. What this *does*
give is a confirmed, current color/radius/font source, replacing the earlier
inferred palette from `docs/learning-path-improved.html` (which is no longer
even present in this repo).

## Colors

| Token | Hex | Role |
|---|---|---|
| `--ink` | `#14151A` | primary text |
| `--ink-soft` | `#54575F` | secondary/muted text |
| `--ink-faint` | `#92959E` | tertiary/placeholder text |
| `--bg` | `#FBFBF8` | page background (warm off-white) |
| `--surface` | `#FFFFFF` | card/panel background |
| `--surface-tint` | `#F3F1EA` | subtle alternate surface |
| `--border` | `#E7E3D9` | default border |
| `--border-soft` | `#EFEDE5` | lighter border |
| `--indigo` | `#5A4FE5` | primary accent (links, primary buttons) |
| `--indigo-dark` | `#372DBF` | primary accent hover |
| `--indigo-bg` | `#ECEAFB` | primary accent tint background |
| `--indigo-ink` | `#2E2599` | text on indigo tint |
| `--coral` | `#FF5A36` | secondary accent |
| `--coral-bg` | `#FFEAE2` | coral tint background |
| `--coral-ink` | `#9A2E14` | text on coral tint |
| `--teal` | `#0E9C8B` | tertiary accent |
| `--teal-bg` | `#E0F4F1` | teal tint background |
| `--teal-ink` | `#0B5A50` | text on teal tint |
| `--amber` | `#D98F1B` | quaternary accent |
| `--amber-bg` | `#FBEED9` | amber tint background |
| `--amber-ink` | `#5C3B08` | text on amber tint |
| `--panel-dark` | `#1B1940` | dark panel background |

## Radius scale

- `--radius-sm`: 10px
- `--radius-md`: 16px
- `--radius-lg`: 26px
- Pills/badges: fully round (999px / border-radius 100px), unchanged from
  before — matches the live site's own button radius (100px).

## Typography

- `--font-display`: `'Instrument Sans', system-ui, sans-serif` (headings)
- `--font-body`: `'Inter', system-ui, sans-serif` (body text)
- `--font-mono`: `'IBM Plex Mono', ui-monospace, monospace` (code blocks)
- `--container`: 1200px max width

These are **not** hardcoded per-widget in the templates in this folder —
templates left `typography_typography` unset so that inserting them via
Elementor's Template Library into the live site inherits these fonts
automatically from the active Kit (`elementor-kit-652`), which is the
correct native behavior rather than a per-widget override.

## Previous palette (retired)

`elementor/course-page-template.json`, `elementor/learning-path-template.json`,
and every file under `elementor/sections/` previously used a different,
inferred palette (teal `#0F766E`, orange `#E85D2A`, blue `#1A73E8`, ink
`#192330`, muted `#576271`, border `#E4E4EC`, warm bg `#FFFAF4`, light-teal
`#E3F1EF`, light-blue `#E7EFFC`). On 2026-08-04 every occurrence was mapped
1:1 to the live tokens above (see git history / diff for the mechanical
remap). `#FFFFFF` was already correct and left unchanged.
