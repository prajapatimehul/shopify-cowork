---
name: store-fixer
description: Authenticated Shopify implementation skill for fixing or updating a store after an audit or from a specific request. Use when a user wants to fix, patch, implement, roll out, or update Shopify theme code, SEO/GEO/AEO issues, product or collection content, schema markup, robots rules, internal linking, or other store changes that require Shopify authentication. Supports theme access, Admin API updates, and mixed changes. Do not use for public-only audits, non-Shopify sites, backlink work, paid ads, or public app distribution architecture.
---

# Store Fixer

Implement Shopify store changes safely and reversibly. Use this skill when the task is to make authenticated changes, not just analyze the storefront.

## Use Bundled Resources Progressively

- Read [references/access-setup.md](references/access-setup.md) before asking for credentials or choosing commands.
- Read [references/fix-methods.md](references/fix-methods.md) to decide whether the fix belongs in theme code, Admin API, a mixed rollout, or a manual merchant workflow.
- Read [references/safety-and-rollback.md](references/safety-and-rollback.md) before touching a live theme or running bulk mutations.
- Use [assets/fix-summary-template.md](assets/fix-summary-template.md) for the final delivery format.
- Use [references/testing.md](references/testing.md) and [evals/evals.json](evals/evals.json) when improving the skill or checking trigger behavior.
- If the final summary is saved to disk, validate it with `python ${CLAUDE_SKILL_DIR}/scripts/check_fix_summary.py --input path/to/summary.md --mode execute|plan|review`.

## Critical Rules

- Never ask the client for the store owner's login or password.
- Confirm the access path first: `Theme`, `Admin API`, `Mixed`, or `Missing`.
- Before any Shopify write, theme push, or Admin API mutation, show the exact proposed change scope and ask the user for explicit approval.
- Execute only the exact files, objects, fields, and actions the user approved. If scope changes, stop and ask for approval again.
- Prefer the smallest reversible change that solves the problem.
- Record the exact files, resources, objects, or endpoints touched.
- Treat rollback as mandatory, not optional. If a rollback path is not prepared and described, do not execute the change.
- Do not claim a fix is complete without verification evidence.
- Do not push broad content rewrites or bulk catalog edits without an explicit scope.
- If the task requires a third-party app setting, a Shopify admin screen with no API coverage, or merchant-only approval, stop and provide exact manual steps instead of guessing.

## Output Rules

- State whether this is `Execute`, `Plan`, or `Review` mode.
- State the access status up front.
- State `Approval: Pending` until the user explicitly approves execution.
- State whether rollback is ready before any execution step.
- List exact changes, not vague summaries.
- Include verification and rollback notes every time.
- Keep the write-up operational. No marketing language, no filler, no inflated claims.
- If blocked, say exactly what is missing and give the smallest next step for the merchant.

## Workflow

### 1. Confirm the task mode

- `Execute`: user ultimately wants the authenticated change made, but execution is still blocked until the exact change set is approved.
- `Plan`: user wants the exact implementation plan first.
- `Review`: user already changed the store and wants the work checked.

If the user provides a `store-analyzer` report, treat it as an input document. Do not re-run a full audit unless that is necessary to verify the target change.

### 2. Classify the fix channel

Use [references/fix-methods.md](references/fix-methods.md).

- `Theme`: Liquid, JSON templates, sections, snippets, assets, robots template, schema markup in theme files.
- `Admin API`: products, collections, pages, metafields, tags, SEO fields, or other authenticated store data.
- `Mixed`: both theme and Admin API work are required.
- `Manual`: merchant must change an app setting, Shopify admin setting, or external system directly.

### 3. Confirm access before changing anything

Use [references/access-setup.md](references/access-setup.md).

- If the task is `Theme`, confirm Shopify CLI access or Theme Access credentials.
- If the task is `Admin API`, confirm a Dev Dashboard app with the required scopes and a short-lived token path.
- If the task is `Mixed`, confirm both paths before proceeding.
- If access is missing, stop execution and switch to `Plan` mode with exact client asks.

### 4. Prepare rollback before execution

Use [references/safety-and-rollback.md](references/safety-and-rollback.md).

- Theme work: record store domain, theme ID, live or unpublished target, and pull current files before editing.
- Admin API work: capture the current object payloads or essential fields before mutation.
- Bulk changes: define the object count and batch size before writing.

If rollback cannot be prepared, stop and remain in `Plan` mode.

### 5. Ask for explicit approval

Before any write:

- list the exact files, objects, fields, or commands that will be changed
- state whether the target is live or unpublished
- state the rollback method
- ask the user to approve execution

Do not edit Shopify state until the user explicitly approves.

### 6. Implement only the approved scope

- Prefer precise edits over broad rewrites.
- Follow existing repo scripts or patterns if they already solve the task safely.
- Keep theme edits local and diffable before push.
- Keep API changes scoped to the requested objects and fields.

If you discover extra required changes mid-execution, stop and ask for approval again before continuing.

### 7. Verify the result

- Theme work: verify with preview or rendered HTML, not only local file changes.
- Admin API work: verify with follow-up reads, returned object data, or storefront output where relevant.
- Mixed work: verify both channels independently.

If verification fails, do not describe the change as complete.

### 8. Write the final fix summary

Use [assets/fix-summary-template.md](assets/fix-summary-template.md).

The summary must include:

- approval status
- access path used
- exact changes applied
- verification evidence
- rollback method
- remaining merchant action if any

## Examples

**Example 1**: `Take this Shopify audit and implement the top 3 fixes`
Result: classify findings into theme, Admin API, or mixed work; make the changes if access is available; otherwise return an execution plan and access checklist.

**Example 2**: `Fix missing FAQ schema and robots rules on this Shopify store`
Result: theme-oriented fix touching `robots.txt.liquid`, relevant schema snippets, or FAQ sections with preview verification.

**Example 3**: `Update these product titles and descriptions in Shopify`
Result: Admin API content update with exact object scope, verification, and rollback payload capture.

**Example 4**: `Implement the SEO fixes from this analyzer report but do not touch the live theme yet`
Result: unpublished theme workflow, local edits, preview verification, and clear push instructions.

**Example 5**: `Tell me what access the client needs before we can fix product SEO and theme schema`
Result: plan-only response using the access model and fix decision tree.

## When Not To Use This Skill

- The user only wants an audit or public analysis. Use `store-analyzer`.
- The site is not a Shopify storefront.
- The task is backlink outreach, ads work, analytics interpretation, or generic copywriting.
- The task is designing a public Shopify app auth architecture for many merchants.
- The user wants unauthenticated competitor research rather than store changes.

## Maintenance Notes

- Keep the main file focused on workflow.
- Put volatile Shopify access details in [references/access-setup.md](references/access-setup.md).
- Put detailed change mapping in [references/fix-methods.md](references/fix-methods.md).
- Put rollback and verification guardrails in [references/safety-and-rollback.md](references/safety-and-rollback.md).
