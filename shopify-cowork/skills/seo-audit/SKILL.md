---
name: seo-audit
description: Runs evidence-backed SEO audits for live Shopify stores using public endpoints and sampled HTML. Use when a user asks to audit a Shopify store, review a Shopify domain, sanity-check or validate a Shopify SEO audit report, inspect product or collection SEO, or prioritize Shopify technical and content SEO fixes. Do not use for non-Shopify sites, backlink audits, local SEO, or generic copywriting tasks.
compatibility: Requires network access to public Shopify URLs. Optional code execution can be used to run bundled scoring and report QA scripts.
metadata:
  author: shopify-cowork
  version: 2.1.0
---

# SEO Audit

Run fast, client-facing Shopify SEO audits that are commercially useful and defensible.
Use public Shopify data, sampled HTML, and explicit scope labeling. Make the report feel
urgent without inventing penalties, guarantees, or unsupported sitewide claims.

## Use Bundled Resources Progressively

- Read [references/checks.md](references/checks.md) for the detailed audit workflow,
  issue heuristics, scoring rubric, and final QA checklist.
- Read [references/troubleshooting.md](references/troubleshooting.md) only when public
  endpoints are blocked, incomplete, or conflicting.
- Use [assets/report-template.md](assets/report-template.md) for the final output shape.
- Use [references/testing.md](references/testing.md) and [evals/evals.json](evals/evals.json)
  when improving the skill or checking trigger behavior.
- If the report is saved to disk, validate it with
  `python scripts/check_report.py --input path/to/report.md --strict`.
- If you saved structured metrics to JSON, compute the internal score with
  `python scripts/score_audit.py --input path/to/metrics.json --pretty`.

## Critical Rules

- Use only public Shopify endpoints and public page HTML. Never attempt authentication.
- Report exact counts only when the underlying endpoint set was fully retrieved. If a
  source is partial, blocked, truncated, or inconsistent, say that exact coverage is not
  available from public data.
- Label major findings as `Catalog-wide`, `Sampled`, or `Inference`.
- Never generalize from sampled HTML to the entire site.
- If `products.json` is blocked, empty, or unusable, say so clearly and stop the full
  catalog audit instead of guessing.
- Check the standard HTML meta description tag for snippet findings. Do not treat
  `og:description` or Twitter tags as the page's SEO meta description.
- Treat missing server-rendered JSON-LD carefully. Apps can inject it client-side.
- Product tags are not a primary SEO finding in this audit. Mention them only as
  secondary merchandising or internal-search hygiene when the storefront evidence makes
  that relevant.
- Keep the report easy to scan. A client should understand the top issues in under a minute.

## Workflow

### 1. Confirm the task mode

- `Full audit`: audit the live Shopify store from scratch.
- `Audit review`: the user provided an SEO audit and wants to know what is real,
  overstated, or missing.

If the user supplied an existing audit, extract the main claims first so you can
verify them against store data.

### 2. Normalize the domain and confirm the store is auditable

- Strip scheme, `www.`, trailing slashes, and obvious path fragments.
- Fetch the store metadata endpoint and the products endpoint first.
- Classify the job as either:
  - `Full audit`: the required public catalog endpoints and crawl files are usable.
  - `Partial audit`: one or more required sources are missing, blocked, truncated, or
    inconsistent.
- If the store does not expose usable public Shopify catalog data, explain the limitation
  and stop rather than fabricating results.

### 3. Collect catalog-wide data

Fetch the full set of public Shopify resources described in
[references/checks.md](references/checks.md):

- Store metadata
- Products
- Collections
- Pages
- Robots.txt
- Sitemap

Use exact counts from these endpoints for catalog-wide findings only when the source was
fully retrieved and internally consistent.

### 4. Collect sampled HTML

Fetch representative pages:

- 5 product pages
- 3 collection pages
- the homepage
- 2 article pages if a blog or article sitemap exists

Use varied samples, not just the first few handles.

### 5. Analyze by business impact

Use the prioritization guidance in [references/checks.md](references/checks.md).
Bias toward the fixes that most often matter for ecommerce search:

- Collection page content
- Product content depth
- Merchant listing eligibility and structured data
- URL consolidation and crawl traps
- Weak default titles and snippets

Treat lower-leverage hygiene issues accordingly. Alt text, Open Graph, Twitter cards,
and `product_type` cleanup are worth reporting, but usually should not outrank weak
collection pages or empty product descriptions.

### 6. Write the report

Use [assets/report-template.md](assets/report-template.md).

For a full audit, give the user:

- Executive summary
- Store snapshot
- Limitations or data-quality note
- Prioritized findings with scope and evidence
- Top 5 actions
- Sample fixes for real products or collections
- Internal SEO score with a note that it is a prioritization heuristic

For an audit review, classify each claim into:

- Supported and important
- Supported but secondary
- Real but overstated
- Unsupported from current evidence
- Missing important issue

### 7. Run the quality gate

Before finalizing:

- Save structured evidence to a metrics JSON file before drafting the final prose if you
  plan to show a score.
- Apply the final QA checklist in [references/checks.md](references/checks.md).
- Use [references/troubleshooting.md](references/troubleshooting.md) if data quality is
  partial or conflicting.
- If you saved the report to a file, run
  `python scripts/check_report.py --input path/to/report.md --strict`.
- If you show a score, compute it from
  `python scripts/score_audit.py --input path/to/metrics.json --pretty`.
- Do not invent ad hoc point deductions in prose. Any displayed score must come from the
  bundled scoring script.

## Audit Review Mode

When the user gives you an existing Shopify SEO audit, do not just critique the tone.
Re-run the same public-data workflow and verify the claims.

Classify each claim carefully:

- `Supported and important`: both the evidence and the prioritization hold up.
- `Supported but secondary`: real issue, but lower leverage than the report implies.
- `Real but overstated`: the issue exists, but the report exaggerates the scope,
  severity, or certainty.
- `Unsupported from current evidence`: current data does not verify the claim.
- `Missing important issue`: a higher-impact issue is absent from the report.

Only call a claim overstated if the evidence contradicts its scale, certainty, or rank.

## Examples

**Example 1**

User says: `Audit this Shopify store: example.com`

Result: Run a full Shopify SEO audit using public endpoints, sample HTML, and the bundled
report template.

**Example 2**

User says: `Review this SEO audit for themancompany.com and tell me what is actually important`

Result: Verify the audit's claims against the live store, separate real issues from
overstatement, and explain what should actually be prioritized.

**Example 3**

User says: `Check whether this Shopify store has weak collection SEO and thin product pages`

Result: Focus the audit on collection descriptions, product content depth, titles,
snippets, and URL consolidation.

## When Not To Use This Skill

- The site is not a Shopify storefront.
- The user wants backlink analysis, competitor gap analysis, or local SEO.
- The task is purely copywriting with no audit or verification component.
- The user needs authenticated data from Search Console, GA4, or the Shopify admin.

## Maintenance Notes

For trigger tuning, regression checks, and eval prompts, use:

- [references/testing.md](references/testing.md)
- [evals/evals.json](evals/evals.json)

Keep this main file lean. Put detailed checklists, scoring rules, and troubleshooting in
the bundled resources instead of expanding this file again.
