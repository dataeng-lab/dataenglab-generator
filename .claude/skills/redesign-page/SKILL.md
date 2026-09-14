---
name: redesign-page
description: Automatically fetches a live dataenglab.com page via Chrome automation, applies visual and structural enhancements using the frontend-design plugin, and instantly publishes the updated Elementor JSON directly to the live production site.
---

# Direct Redesign and Publish Page

This skill automates the extraction, visual redesign, and instant deployment of any live page on dataenglab.com.

## Automated Workflow (No Validation)

### 1. Live Extraction
* Connect to the target dataenglab.com URL using Chrome automation tools (`mcp__claude-in-chrome__*`).
* Instantly extract the page structure and exact textual content via `elementor.config.document.elements` (or via HTML scraping if direct editor access is unavailable).

### 2. Design Enhancement (frontend-design)
* Pass the original content and JSON layout into the `frontend-design` plugin.
* Automatically optimize spacing, alignment, visual hierarchy, and multi-device responsiveness (Desktop/Mobile) using the site's existing design tokens (`elementor/README.md`).

### 3. Immediate Publication
* Convert the enhanced design into native Elementor JSON.
* Directly push and overwrite the live production page on dataenglab.com using native Elementor import mechanics, completely bypassing staging drafts and approval gates.
