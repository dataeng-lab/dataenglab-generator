# landing-page.json is a fabricated, UNVERIFIED draft — read before importing

## Why this file exists despite the rule against it

`CLAUDE.md` states: *"If the reference is missing or invalid, do not fabricate `landing-page.json`... create `elementor/REFERENCE_REQUIRED.md`."* Root `elementor-reference.json` is still missing from this kit — that has not changed.

`elementor/landing-page.json` was generated anyway, at the user's explicit request, as a **best-effort draft** rather than reused from a real export. This is a deliberate, scoped, one-time override of the CLAUDE.md rule for this course only — it does **not** change the standing policy, and root `elementor-reference.json` was not fabricated. Future course generations in this kit will still correctly refuse to fabricate Elementor JSON until a real reference is supplied.

## What this means concretely

- Widget names (`heading`, `text-editor`, `button`, `icon-box`, `accordion`), setting keys (e.g. `flex_gap`, `background_background`, `border_radius`), and responsive/nesting conventions were written from general knowledge of Elementor's container-based JSON format — **not copied from your actual export**.
- Your Elementor/plugin version may use different key names, different default units, different accordion tab schemas, or reject some of these settings outright.
- It passed `scripts/validate_elementor_json.py` (every element has a unique `id`, an `elType`, and a valid `elements` list) — but that script only checks structural shape, not Elementor-import compatibility. It has **not** been opened in Elementor or confirmed to import cleanly.

## What it contains

A single-page layout, no header/logo/menu/footer, using only native Elementor free-tier widgets:

1. Hero — course title, one-line pitch, "View Curriculum" button (`href="#"`).
2. Three `icon-box` widgets — Level / Duration / Stack (no invented statistics).
3. An `accordion` listing the 3 lessons + the lab, mirroring `tutor-lms/curriculum.md`.
4. A closing CTA — "Start the Course" button (`href="#"`).

Colors use the project theme palette documented in `CLAUDE.md` and `elementor/README.md`. All links are `#` placeholders per CLAUDE.md's rule for unknown links.

## Before publishing this page

1. Import it into a staging Elementor site and check every widget renders and every setting is respected — do not trust it sight-unseen.
2. Fix any settings Elementor rejects or silently ignores.
3. Once you have a real root `elementor-reference.json`, regenerate this page from that reference instead and discard this draft — the real export is still the only trustworthy source of truth for your specific Elementor version's schema.
