# Summary — "Publish the investigate-duplicate-orders lab to the live site" (dry run, no skill)

## Approach

Followed only `CLAUDE.md` at the repo root (no skill loaded, per instructions). Its Elementor
section gives a strict reference-tier resolution order before any JSON may be generated:

1. `references/elementor-reference.json` (canonical export) — checked, **absent**.
2. Fallback tier: the existing `elementor/` template corpus (`course-page-template.json`,
   `elementor/sections/*.json`, `elementor/README.md`) + the confirmed palette in
   `references/dataenglab-live-theme.md` — **present and used**, provided every widget/key is
   traceable to that corpus and a `SOURCE.md` disclosure is written alongside the output.
3. `elementor/REFERENCE_REQUIRED.md` fallback — not needed, since tier 2 applied.

Read `output/investigate-duplicate-orders/` to confirm the lab itself was already finished
(`page-content.md`, `lab-spec.md`, `student-lab/`, `instructor/`, `validate.json`, a packaged
`.zip` all present) — publishing is content-packaging + Elementor JSON, not lab authoring.

Read `elementor/course-page-template.json` in full (via a small Python inspection script) to
extract the exact, real widget types and setting-key shapes already in use — `container`,
`heading`, `text-editor`, `icon-list`, `accordion`, `button` — including the pill-chip pattern
(`text-editor` with inline-styled `<span>` chips), the card pattern (bordered/rounded inner
containers with `_column_size`), and the accordion `tabs` repeater used for both curriculum and
FAQ-style content. Cross-checked `references/dataenglab-live-theme.md` for the actual confirmed
color tokens, and deliberately did **not** use the palette in `references/brand.md` / the
`CLAUDE.md` "Brand" section's `#3D73FF`-based palette, because the Elementor section of
`CLAUDE.md` explicitly says the live-theme palette supersedes it for this tier.

## What was built

- `output/investigate-duplicate-orders/elementor/landing-page.json` — a new native Elementor page
  (45 elements, validated with `scripts/validate_elementor_json.py` -> `OK`, 0 duplicate IDs) built
  strictly from the widget/key vocabulary confirmed in `course-page-template.json`. Structure:
  hero (badges, title, lede, CTA buttons) -> outcomes (Icon List) -> environment (two bordered
  cards describing `orders`/`order_items` grain, each with a plain unstyled `<table>` of fields)
  -> tasks (Accordion, 5 tabs, one per numbered task with hints) -> expected-output callout ->
  troubleshooting (Accordion, `faq_schema: yes`, 3 tabs) -> closing CTA band on a dark panel.
  Header/logo/menu/footer excluded; all links are `#` (no real lab URL/asset exists yet); no
  fabricated statistics — the only numbers on the page (12 rows / $359 vs. 17 rows / $490, 25 min,
  5 tasks) come straight from the lab's own `page-content.md` / `lab-spec.md`.
- `output/investigate-duplicate-orders/elementor/SOURCE.md` — the disclosure `CLAUDE.md` mandates
  for tier-2 generation: which tier, which specific files, every widget/key traced back to a real
  example, and the corpus's own unverified-draft status restated (the template files were never
  produced from a real Elementor export or opened in a real Elementor editor).
- Both files copied into this `outputs/` folder under `elementor/`.

## Where I stopped, and why

I stopped **before any live-site write of any kind**. No `novamira/*` or `angie/*` MCP tool was
called — not even read-only discovery ones — for the duration of this task.

Two independent reasons converge on the same stopping point:

1. **The dry-run safety constraint** given for this task explicitly forbids calling any MCP
   tool/ability that would write to, publish to, or otherwise modify the live site or any external
   system, naming `novamira/*` and `angie/*` by pattern.
2. **`CLAUDE.md` itself requires the same pause independent of the dry run.** Its Publishing
   section says: "Before any live publish, describe the exact change (page, content/structure,
   before/after) and get the user's explicit go-ahead for that specific publish. Never publish
   autonomously." That explicit, specific go-ahead has not been obtained in this conversation — the
   task instruction to "publish the lab to the live site" is not itself that per-change approval.

So the next real steps — which I did **not** take, and which need a human decision first — are:

- **Confirm the exact change** with the user: a new standalone Elementor page at
  `dataenglab.com/labs/investigate-duplicate-orders` (content per `page-content.md`, structure per
  `landing-page.json` above) — this is a *new* page, not an edit to an existing live page, so there
  is no "before" state on the live site to diff against; the "after" is entirely what's in
  `landing-page.json`.
- Ask the user which native mechanism they want used to apply it — Elementor's Template
  Library/editor (via `novamira/create-admin-access-link` + browser automation), or
  `angie/get-elementor-kit`/`update-elementor-kit` if this should instead live inside kit-level
  settings — since `CLAUDE.md` allows either but they have different blast radii.
  `angie/get-elementor-kit` (a **read**, not a write) would be the safe first call in a real
  (non-dry-run) session to see the current kit before proposing exactly how the new page slots in,
  but it was not called here either, to keep this dry run strictly clean of any MCP call to that
  connection.
- Get explicit confirmation that `landing-page.json` should first be imported into a **staging**
  Elementor site (per the corpus's own README warning) before touching production, since neither
  the template corpus this file derives from, nor this new file, has ever been confirmed to import
  without errors into the site's actual installed Elementor version.
- Only after that go-ahead: actually apply the JSON via the approved native mechanism, then report
  back the real before/after and get sign-off.

None of that happened here. This dry run's deliverable is the prepared, validated, disclosed
Elementor JSON and the exact plan above — not a live change.
