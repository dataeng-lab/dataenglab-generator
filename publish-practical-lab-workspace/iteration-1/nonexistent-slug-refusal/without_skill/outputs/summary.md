# Task
"Publish the customer-churn-detection lab."

# Verbatim reply given to the user

I can't publish a "customer-churn-detection" lab because it doesn't exist yet. I checked output/ in this repo and it only contains:

- dedupe-late-arriving-orders/
- investigate-duplicate-orders/
- reconstruct-customer-plan-history/
- test-course/

There is no output/customer-churn-detection/ directory, no course-spec.json or page-content.md for it, and nothing else in the repo referencing that slug. Per CLAUDE.md, publishing to dataenglab.com is content-only and must be built from real, already-generated material -- I'm not able to invent lab content (business scenario, tasks, dataset, validation, page copy) on the spot just to have something to publish, and I haven't touched the Novamira MCP connection or any live-site tooling for this request.

To move forward, I would need you to either:
1. Confirm the correct slug if this lab already exists under a different name, or
2. Have the lab generated first (this is a separate content-creation step, not a publishing step) before there is anything to publish.

I have not created any files under output/customer-churn-detection/ and have not made any live-site changes.

# Verification performed

- Ran ls on output/ -- confirmed it contains only: dedupe-late-arriving-orders/, investigate-duplicate-orders/, reconstruct-customer-plan-history/, test-course/.
- Ran ls on output/customer-churn-detection -- confirmed: "No such file or directory".
- Confirmed no files or directories were created under output/customer-churn-detection/ by this task (none existed before, none exist after).
- No MCP tools (Novamira, browser automation, etc.) were called at any point -- no live-site or external-system writes occurred.
