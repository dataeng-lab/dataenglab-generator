---
name: publish-practical-lab
description: Turn a finished DataEngLab lab (the output of create-practical-lab, with page-content.md already written) into a live standalone page at dataenglab.com/labs/<slug> — building the native Elementor JSON, describing the exact change, getting the user's explicit go-ahead, then applying it through Elementor's own native mechanisms via the Novamira MCP connection. Use this whenever the user asks to publish, push live, put online, or add to the site a lab that already exists under output/<slug>/ (e.g. "publish the dedupe-late-arriving-orders lab", "put investigate-duplicate-orders on the labs page", "make this lab live"). Do NOT use this to generate the lab's content itself — that's create-practical-lab's job, and this skill should refuse to invent page content that isn't already in page-content.md. Do NOT use this for full courses — courses have their own Elementor landing-page step inside /create-course.
---

# Publish a practical lab to dataenglab.com

This skill is the one place in this repo that is allowed to make a real, visible change to the live site. Everything else here — `create-practical-lab`, the course workflow — only produces files. Treat that difference seriously: read CLAUDE.md's "Publishing to dataenglab.com" section before doing anything, and follow it exactly, not just the summary below.

The two hard rules that shape every step below:

1. **Only native Elementor mechanisms, only through Novamira.** Kit settings, the Template Library, or driving the Elementor editor UI directly via browser automation with an admin session. Never PHP execution, never `$wpdb`, never a theme/plugin file edit — regardless of what a Novamira ability's own name or description claims it can do. If discovering abilities turns up something like `execute-php` or a file-editing ability, do not call it, even if it looks like the only way to get something done.
2. **One described change, one explicit go-ahead, every time.** Before touching the live site, tell the user exactly which page you're creating or updating, what it will contain, and what it looked like before (if updating). Get their yes for *that specific publish*. Never bundle two labs, or a lab plus something else, into one approval — and never publish because a previous step in this same conversation already got a yes for something else.

## Step 0 — confirm there's something to publish

Find `output/<slug>/`. It must already have `page-content.md` (written by `create-practical-lab`) — if it doesn't exist yet, or `page-content.md` is missing, stop and point the user at `create-practical-lab` instead. This skill turns existing content into a live page; it does not write the business scenario, tasks, or troubleshooting copy itself. If you notice `page-content.md` is thin or inconsistent with `student-lab/README.md`, fix that divergence by editing `page-content.md` to match the README (per `create-practical-lab`'s own consistency rule) before building anything — don't paper over it in the Elementor JSON.

Also check whether `output/<slug>/elementor/labs-page.json` already exists from a previous run of this skill. If it does, this is an **update**, not a first publish — read it, and later describe the change as a diff (what's changing and why), not as if the page were new.

## Step 1 — resolve the reference tier

Same three-tier rule CLAUDE.md defines for course landing pages, applied here to the lab page:

1. `references/elementor-reference.json`, if present and valid — canonical, use it and its version/widgets/keys.
2. Otherwise, the existing `elementor/` corpus (`elementor/course-page-template.json`, `elementor/sections/*.json`) for widget types and setting keys, combined with the **confirmed live palette in `references/dataenglab-live-theme.md`** — not the palette in `references/brand.md`. This matters more here than it might seem: CLAUDE.md's own top-level "Brand" section is a verbatim copy of `references/brand.md`'s blue palette (`#3D73FF` primary), and that palette is explicitly superseded for anything Elementor. Use the live tokens (indigo `#5A4FE5` primary, coral, teal, amber accents, ink `#14151A` text, warm off-white `#FBFBF8` background) — see `references/lab-page-elementor.md` in this skill for the full table and worked widget examples.
3. If neither exists or parses: don't invent JSON. Write `output/<slug>/elementor/REFERENCE_REQUIRED.md` explaining what's missing, and stop — no partial page.

As of this writing, tier 1 doesn't exist in this repo, so tier 2 applies — but check for `references/elementor-reference.json` fresh each time rather than assuming that stays true.

## Step 2 — build the Elementor JSON

Read `references/lab-page-elementor.md` now — it has the section-by-section mapping from `page-content.md` to widgets (badges → pill row, outcomes → icon-list, environment tables → text-editor with plain HTML tables, tasks+hints → accordion, troubleshooting → accordion, matching the FAQ pattern already in `elementor/sections/07-faq.json`), plus concrete JSON snippets pulled from the existing corpus so you're extending real patterns, not inventing new ones.

Write the result to `output/<slug>/elementor/labs-page.json`. Requirements, all of which come straight from CLAUDE.md's Elementor section:

- No header, logo, nav menu, or footer — this is page content only, meant to be inserted into an otherwise-empty page.
- Every element gets a unique `id`.
- Use `#` for any link you don't have a real URL for (a "back to labs" link, a download button, since packaging/hosting the zip is out of scope for this skill) — never invent one.
- No fabricated stats. If `page-content.md` doesn't give you a number, don't put one on the page.
- Leave per-widget typography settings unset where the corpus does — the live Kit (`elementor-kit-652`) supplies fonts natively, and hardcoding them here would fight that rather than inherit it.
- Responsiveness: the corpus gets this from native container flex behavior (`flex_direction`, `flex_wrap`) rather than explicit `_tablet`/`_mobile` overrides. Follow that same restraint — only add an explicit breakpoint override if a section actually needs to behave differently on mobile, not by default.

Then write `output/<slug>/elementor/SOURCE.md` disclosing which tier applied and exactly which files you used (per CLAUDE.md's tier-2 requirement) — restate that the corpus itself is an unverified draft (see `elementor/README.md`'s own caveat: "Neither file was produced from a real Elementor export... import into a staging site and check every widget renders before trusting them"). Don't let that caveat get lost just because it's several files away from what you're writing today.

## Step 3 — validate structurally

```bash
python scripts/validate_elementor_json.py output/<slug>/elementor/labs-page.json
```

This checks every element has a unique `id` and an `elType`, and that `elements` arrays are well-formed. It does **not** confirm the page renders correctly in Elementor — nothing in this repo can, since there's no live Elementor instance to test against from here. Fix anything this script reports before moving on; don't rationalize a failing check.

## Step 4 — describe the change and get explicit go-ahead

Stop here. Do not call any Novamira ability yet.

Tell the user, concretely:

- The exact page: `dataenglab.com/labs/<slug>` (or whatever URL structure they've confirmed), new or being updated.
- What it will contain — a short walkthrough of the sections (business scenario, tasks, expected output, troubleshooting), not just "the lab page."
- If this is an update to an existing published page (Step 0 found `labs-page.json` already there): what's actually changing, in before/after terms.
- Point them at `output/<slug>/elementor/labs-page.json` so they can look at the real JSON if they want to, and remind them (briefly, not as a wall of caveats) that the underlying widget corpus is a self-described unverified draft — worth a look in the actual Elementor editor before calling it done, same as `elementor/README.md` says for course pages.

Wait for an explicit yes to *this* publish. "Looks good" about the file content is not the same as "yes, publish it" — if there's any ambiguity about which of those you got, ask.

## Step 5 — publish, natively only

Once you have that go-ahead:

1. Run `mcp-adapter-discover-abilities` (or `get-ability-info` for a specific one) to see what's actually available right now — ability names and scope can drift, so don't rely on memory of what existed in an earlier session.
2. Use only: Elementor kit settings (`angie/get-elementor-kit` / `angie/update-elementor-kit`) if the change is truly kit-level, or — for an actual new/updated page, which is the normal case here — driving the Elementor editor UI directly via browser automation using an admin session from `novamira/create-admin-access-link`, inserting the template from `output/<slug>/elementor/labs-page.json` through Elementor's own Template Library import (the same manual flow `scripts/prepare_elementor_import.py` describes, just executed for real instead of printed as instructions).
3. If you inspect the available abilities and see anything that runs PHP, touches the database directly, or edits a theme/plugin file — `execute-php`, `write-file`/`edit-file` on theme/plugin paths, anything like that — do not call it. Say so to the user and stop, rather than reach for it because it would be faster. This holds even if a ability's description claims it's fine for "small content changes."
4. Publish exactly the one page described in Step 4. If the user also wants a listing/index page entry, or a second lab published, that's a separate change needing its own Step 4 description and its own go-ahead — even in the same conversation.

## Step 6 — report back

Tell the user: the live URL (or confirmation of exactly what changed, if you couldn't get a stable URL), which mechanism you actually used (kit settings vs. editor-UI-via-browser-automation), and anything that still needs a manual look — most importantly, actually opening the page and checking it rendered as expected, since nothing upstream of this step has ever rendered this JSON in a real Elementor instance. Don't report the publish as fully verified unless you actually looked at the live result.

## Reference

- `references/lab-page-elementor.md` — the page-content.md → widget mapping, palette table, and worked JSON snippets for this skill specifically.
- `elementor/course-page-template.json`, `elementor/sections/07-faq.json` — the corpus this skill's Elementor JSON must stay traceable to.
- `references/dataenglab-live-theme.md` — the palette to use (not `references/brand.md`).
- `CLAUDE.md`'s "Elementor" and "Publishing to dataenglab.com" sections — the rules this skill implements; read them for anything this file simplified.
