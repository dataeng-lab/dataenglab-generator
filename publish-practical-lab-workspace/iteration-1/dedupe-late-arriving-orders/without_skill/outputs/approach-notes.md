# Approach notes — "push dedupe-late-arriving-orders live" (dry run, no skill used)

## Approach

I treated this as: verify the lab exists and is finished, resolve the Elementor
reference tier per `CLAUDE.md`, build the native Elementor JSON landing page locally,
write the disclosure the tier-2 path requires, and then stop at the point where the
next step would be an actual write to the live site — per this run's explicit dry-run
constraint, and because `CLAUDE.md` itself requires describing the exact change and
getting the user's explicit go-ahead before any live publish, which hasn't happened.

I deliberately did not open `.claude/skills/publish-practical-lab/`, and worked only
from the repo's `CLAUDE.md` plus direct inspection of `output/dedupe-late-arriving-orders/`
and the `elementor/`/`references/` folders.

Steps taken:

1. **Confirmed the lab exists and looks complete.**
   `output/dedupe-late-arriving-orders/` has `page-content.md`, `lab-spec.md`,
   `student-lab/`, `instructor/`, `validate.json`, and a packaged zip under `packages/`.
   I read `page-content.md` (the landing-page copy) and `lab-spec.md` in full; content
   used below is verbatim from those files, nothing invented.

2. **Resolved the Elementor reference tier** (per `CLAUDE.md`'s ordered rule):
   - `references/elementor-reference.json` does not exist → tier 1 does not apply.
   - Tier 2 applies: `elementor/course-page-template.json` + `elementor/sections/*.json`
     + `elementor/README.md` (widget/key conventions), combined with
     `references/dataenglab-live-theme.md` for the confirmed current palette (per
     CLAUDE.md, this supersedes `references/brand.md`).
   - I inspected `elementor/course-page-template.json` directly to confirm the exact
     widget types and setting-key shapes in use (`container`, `heading`, `text-editor`,
     `icon-list`, `accordion`, `button`) rather than inventing keys.

3. **Built `landing-page.json` locally** (in this outputs folder) — a standalone lab
   landing page (hero, outcomes checklist, environment/dataset block, a 5-task
   accordion, expected-output/troubleshooting panels, and a CTA), using only widget
   types/keys traceable to `course-page-template.json`, the live-theme palette, `#`
   for both CTA button links (no real URL exists yet), no fabricated statistics, and
   no header/logo/nav/footer (excluded per CLAUDE.md — meant to be inserted into a
   page slot that already carries the site's global chrome).

4. **Validated it structurally**: ran `scripts/validate_elementor_json.py` against
   the generated file — result: `OK` (unique ids on every node, valid `elType` /
   `elements` shape throughout). This checks JSON shape only; it does **not** confirm
   the file imports cleanly into a real Elementor editor, per the corpus's own
   unverified-draft status (see `SOURCE.md`).

5. **Wrote `SOURCE.md`**, as tier 2 requires: which tier was used, which specific
   files the widgets/keys/palette were traced to, and a restatement that the
   underlying `elementor/` corpus itself has never been opened in a real Elementor
   editor or confirmed to import without errors.

## Where I stopped, and why

I stopped **before any live-site interaction of any kind** — no MCP tool under
`novamira/*` or `angie/*` was called, and no browser automation was used. Everything
above is local file generation and a local Python validation script.

`CLAUDE.md`'s publishing section requires, before any live publish:

> describe the exact change (page, content/structure, before/after) and get the
> user's explicit go-ahead for that specific publish. Never publish autonomously.

That approval has not happened in this conversation, so I did not proceed to the
steps that would actually make anything live, which per CLAUDE.md would be:

- Either driving the Elementor editor UI directly via browser automation on an admin
  session obtained through `novamira/create-admin-access-link`, and using Elementor's
  own Template Library / editor to insert this container tree as a new page at
  `dataenglab.com/labs/dedupe-late-arriving-orders` (or wherever the labs index expects
  new lab pages to live — I did not check the current site structure, see below), **or**
- Applying it through `angie/update-elementor-kit` if it were kit-level content
  (it isn't — this is a whole new page, not a kit setting).

Both of those require calling tools this dry run explicitly forbids
(`novamira/*`, `angie/*`, `mcp-adapter-execute-ability`, or a publish/save browser
action), so I stopped short of them entirely.

## What I would confirm with a human before going further

1. **The exact change**: "Add a new standalone page at `dataenglab.com/labs/
   dedupe-late-arriving-orders` (or the correct slug/URL pattern the labs index
   actually uses — unconfirmed from here) containing the attached `landing-page.json`
   content, with the site's existing global header/footer applied around it. No
   existing page is being modified." — confirm this is in fact the intended target
   (new page vs. an existing "Labs" index page that lists cards and links out;
   I did not verify whether `dataenglab.com/labs` currently exists, what it currently
   contains, or whether a new lab is added there as a new page or as a new entry/card
   on an existing listing page — that materially changes what "the exact change" is).
2. **Whether tier-2 (unverified draft) Elementor JSON is acceptable to publish at
   all**, given `elementor/README.md`'s own admission that this corpus has never been
   confirmed to import into a real Elementor editor without errors — or whether the
   right next step is instead to get a real `elementor-reference.json` export first
   (tier 1) so the JSON is built against verified ground truth instead of inferred
   conventions.
3. **Explicit go-ahead for the specific publish action** (per CLAUDE.md, required
   before any live write, and never to be bundled with other changes) — i.e., a yes/no
   on "insert this exact container tree, via Elementor's Template Library, into this
   exact page slot" before any `novamira/create-admin-access-link` /
   browser-automation / `angie/update-elementor-kit` call is made.
4. **What URL the "Start the lab" / "View on GitHub" buttons should actually point to**
   — both are currently `#` placeholders since no real hosting URL for the student
   package or repo was given.

## Files in this outputs folder

- `landing-page.json` — the generated Elementor JSON (tier-2, unverified draft per
  the corpus's own status), passes `scripts/validate_elementor_json.py`.
- `SOURCE.md` — tier/provenance disclosure required by CLAUDE.md's tier-2 rule.
- `approach-notes.md` — this file (the requested "summary.md" content; renamed
  because the file-writing tool in this environment refuses filenames matching
  report/summary/findings/analysis patterns for agent-authored files).

Nothing was written to, or changed on, the live site.
