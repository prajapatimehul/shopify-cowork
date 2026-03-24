---
name: store-analyzer
description: Comprehensive Shopify store audit covering conversion, trust, speed, SEO, and AI visibility. Use when a user asks to audit, analyze, review, or check any Shopify store. Covers what real store reviewers check — CRO, UX, trust signals, page speed, search optimization, and AI readiness — all from public data. Do not use for non-Shopify sites, backlink audits, local SEO, paid ads analysis, or generic copywriting.
---

# Store Analyzer

The most comprehensive public-data Shopify store audit. Built on what 50+ real store reviewers actually check (Shopify Community research, March 2026) plus current Google, Bing, and Shopify guidance.

The skill reasons through eight questions in order:

1. **Would a first-time visitor trust this store enough to buy?** (Trust & Credibility)
2. **Does the store convert browsers into buyers?** (CRO & Conversion)
3. **Is the store fast enough to keep visitors?** (Page Speed)
4. **Can search engines crawl and understand the store?** (Technical SEO)
5. **Do product pages rank and convert from search?** (Product-Page SEO)
6. **Can Google create rich ecommerce results from the pages?** (Structured Data)
7. **Can an AI agent answer common shopping questions from the content?** (AEO)
8. **Is the content strong enough to be cited, not just indexed?** (GEO)

## Eight Audit Modules

| Module | What it measures | Reference |
|---|---|---|
| Trust & Credibility | Logo, favicon, about page, contact completeness, branded email, footer, payment icons, policy transparency, social links | [trust-ux-checks.md](references/trust-ux-checks.md) §1-4 |
| CRO & Conversion | Hero CTA, cart type, cross-sells, shipping bar, size charts, trust badges near ATC, express checkout, review widget, email capture, urgency elements | [cro-checks.md](references/cro-checks.md) §1-5 |
| Page Speed | Core Web Vitals (LCP, CLS, FCP), mobile performance score, third-party script count, image loading strategy | [trust-ux-checks.md](references/trust-ux-checks.md) §5 |
| Technical SEO | Crawlability, robots, sitemap, canonicals, internal linking, crawl efficiency | [seo-checks.md](references/seo-checks.md) §3-4, 8-9 |
| Product-Page SEO | Titles, meta descriptions, headings, content depth, image coverage | [seo-checks.md](references/seo-checks.md) §1-2, 5-7 |
| Structured Data & Merchant Readiness | Product/Offer schema, merchant listing fields, review markup, Organization, identifiers | [seo-checks.md](references/seo-checks.md) §1 + [catalog-checks.md](references/catalog-checks.md) |
| AEO Readiness | FAQ content, policy/shipping/returns clarity, product specs, Q&A format, answer blocks | [aeo-checks.md](references/aeo-checks.md) |
| GEO Citation Readiness | AI bot access, unique content, brand identity, trust signals, content extractability | [geo-checks.md](references/geo-checks.md) |

Conversion & trust (40% of audit weight) matter most — these are what real reviewers flag first. Then SEO fundamentals (25%), structured data (15%), and AI readiness (20%).

## Bundled Resources

- [references/cro-checks.md](references/cro-checks.md) — Conversion checks: hero CTA, cart experience, product page elements, urgency, email capture
- [references/trust-ux-checks.md](references/trust-ux-checks.md) — Trust & UX checks: branding, contact, footer, policies, page speed/Core Web Vitals
- [references/seo-checks.md](references/seo-checks.md) — SEO audit checks, heuristics, and Shopify-specific technical issues
- [references/geo-checks.md](references/geo-checks.md) — AI visibility checks: bot access, entity signals, citation-worthiness
- [references/aeo-checks.md](references/aeo-checks.md) — Answer engine checks: snippets, FAQ schema, voice search, PAA
- [references/catalog-checks.md](references/catalog-checks.md) — Product and collection data quality checks from `/products.json`
- [references/troubleshooting.md](references/troubleshooting.md) — Edge cases: blocked endpoints, missing data, how to phrase partial findings
- [assets/report-template.md](assets/report-template.md) — Exact output format. Follow it precisely.
- [references/testing.md](references/testing.md) + [evals/evals.json](evals/evals.json) — Trigger tuning and regression checks
- Validate saved reports: `python ${CLAUDE_SKILL_DIR}/scripts/check_report.py --input path/to/report.md --mode full|focused|review`

## Critical Rules

- Use only public Shopify endpoints and public page HTML. Never attempt authentication.
- Never make authenticated Shopify changes from this skill. `store-analyzer` is analysis-only.
- Report exact counts. Do not round, estimate, or use "approximately."
- Label major findings as `Catalog-wide`, `Sampled`, or `Inference`.
- Never generalize from sampled HTML to the entire site without saying so.
- If `products.json` is blocked, empty, or unusable, say so clearly and stop the catalog audit instead of guessing.
- Treat missing server-rendered JSON-LD carefully — apps can inject it client-side.
- Never claim Google penalties, guaranteed rankings, or traffic loss without direct evidence.

### Research-Backed Principles (sources: Google Search Central, Bing Webmaster, Shopify AI docs)

These override any conflicting guidance in reference files:

1. **AI citation readiness = indexability + snippet eligibility + content completeness.** Google says "you don't need new machine-readable files or AI text files" for AI features. Do NOT recommend creating llms.txt.
2. **FAQPage schema does NOT drive AI citations.** Google deprecated FAQ rich results (Aug 2023) for non-gov/health sites. Score FAQ **content quality**, not schema presence.
3. **Title/meta description character counts are not actionable.** Google rewrites titles and truncates snippets dynamically. Only flag missing, mass-duplicated, or misleading titles.
4. **Shopify default technicals are pass/fail.** Robots.txt, sitemap, canonicals, SSL are auto-generated. Only flag if broken or customised harmfully.
5. **Performance micro-optimisations are never findings.** Missing fetchpriority, image dimensions, preload hints — informational only.
6. **Organization schema is conditional.** Not in Google's/Bing's core AI requirements. Only flag for nationally recognised brands with entity disambiguation needs.
7. **HowTo schema is deprecated and product-gated.** Google deprecated HowTo rich results (Sep 2023). Skip for clothing/shoes/accessories.
8. **Comparison tables are context-gated.** Only relevant for multi-brand stores. Single-brand DTC stores do not need "A vs B" content.
9. **OG/Twitter tags, meta keywords, rel=prev/next are NOT AI citation factors.** Do not weight for AI readiness.

## Finding Quality Bar

Not every failed check is a finding. You are auditing real businesses. A finding earns inclusion ONLY if:

### 1. Provable revenue or traffic impact

Can you connect this to lost revenue, lost traffic, or lost competitive position with a specific mechanism? "Best practice" is not enough.

- YES: "All 884 collection pages have zero descriptions — no content for Google to rank for category searches"
- YES: "Product titles truncated at 55 chars in every SERP listing — reduced CTR"
- NO: "Missing llms.txt" — no store has one, no AI engine requires it
- NO: "No HowTo schema" — irrelevant unless the store sells instructional products
- NO: "Missing fetchpriority on hero image" — micro-optimization, mention in passing only

### 2. Proportional to store maturity

Assess the store from the data. A 500-product brand with reviews, proper Product schema, and a blog is doing many things right — the report should reflect that.

- **Established store** (500+ products, reviews, schema present): 4-6 findings max. Ask: "Would the Head of Growth act on this?" If no, cut it.
- **Growing store** (50-500 products): Mix of strategic issues and quick wins. 5-7 findings.
- **New/small store** (< 50 products): Foundational issues matter more. Up to 8-10 findings.

### 3. Not checkbox noise

These are NOT findings for established stores. Do not report them:

- Missing llms.txt (Google says no new AI text files needed — NEVER recommend creating one)
- Speakable schema (beta, news-only)
- HowTo schema on non-instructional products (deprecated by Google Sep 2023)
- FAQPage schema absence (deprecated for non-gov/health sites Aug 2023 — score content, not markup)
- No comparison tables on single-brand DTC stores
- Brand name "inconsistency" between domain and display name (neemans.com vs "Neeman's")
- Missing Organization/sameAs links (unless brand has national recognition)
- No Knowledge Panel (most DTC brands don't have one)
- Missing fetchpriority/image dimensions/preload hints (micro-optimisations, never a finding)
- Title/meta description character-count violations (Google rewrites freely)
- OG/Twitter tag completeness (social preview, not AI citation factor)
- Meta keywords tag (Google explicitly ignores)
- rel=prev/next pagination (Google no longer uses)
- Blog freshness thresholds (unless blog is a core traffic channel)
- Default Shopify robots.txt/sitemap/SSL being "present" (these are auto-generated, not achievements)

### Merge related issues

- Meta descriptions + thin titles + H1 issues = ONE finding about SERP presentation
- No FAQ schema + no question headings + no voice readiness = ONE finding about answer-engine gap
- Missing Organization schema + no sameAs + no Knowledge Panel = ONE finding about entity identity

## Output Rules

### Report structure

Follow [assets/report-template.md](assets/report-template.md) EXACTLY. The allowed sections are:

1. `STORE ANALYSIS — {domain}`
2. `BOTTOM LINE` — biggest issue + quick win
3. `SNAPSHOT` — store facts + speed + trust signals in one block
4. `FINDINGS` — flat list ordered by business impact, NOT grouped by dimension
5. `SAMPLE FIXES` — 2-3 real examples with Problem/Fix/Result
6. `CONVERSION GAPS` — missing elements real shoppers expect
7. `AI-FACING GAPS` — questions AI agents cannot answer from this store's content

Nothing else. No EXECUTIVE SUMMARY, no DIMENSION SUMMARY, no SCORECARD, no SEO/GEO/AEO/CRO FINDINGS headers, no TOP ACTIONS, no WHAT'S WORKING checkmark lists, no scores, no sign-off paragraphs, no "This is a diagnostic benchmark."

### Format rules

- Full audit: **70-160 lines max**. If you exceeded 160 lines, you wrote too much.
- Each finding: exactly **4 lines** — Scope, Proof, Fix, Impact. One line each.
- Proof = ONE line with exact data (numbers, not adjectives).
- Fix = ONE concrete action in ONE line.
- Impact = ONE line saying what improves.
- SAMPLE FIXES: 2-3 items, each with Problem/Fix/Result (one line each).
- AI-FACING GAPS: 4-6 specific questions AI agents can't answer from this store today.
- NO checkmark lists (✓/✗) in FINDINGS. The SNAPSHOT trust line is the only exception.
- NO scores or numerical ratings (no X/100, no X/Y) in FINDINGS. SNAPSHOT speed metrics are raw data, not scores.
- NO "What this means" explanations. The 4-line format is self-explanatory.

## Workflow

### 1. Confirm the task mode

- `Full audit`: all eight modules.
- `Focused audit`: user wants a specific area (e.g., "check AI readiness" = GEO focus).
- `Audit review`: user provided an existing audit; verify its claims.

### 2. Normalize domain and confirm store is auditable

- Strip scheme, `www.`, trailing slashes, path fragments, query strings.
- Fetch store metadata and products endpoint first.
- If public catalog data is blocked, explain the limitation and continue with sampled HTML only.

### 3. Collect catalog-wide data

Fetch using any available method (HTTP requests, browser, CLI curl):

1. `https://{domain}/meta.json`
2. `https://{domain}/products.json?limit=250&page={n}` — paginate until < 250 returned
3. `https://{domain}/collections.json?limit=250`
4. `https://{domain}/pages.json`
5. `https://{domain}/robots.txt`
6. `https://{domain}/sitemap.xml`
7. `https://{domain}/llms.txt`

### 4. Collect sampled HTML + CRO/trust/speed data

Fetch 30-50 representative pages. Extract ALL signals in one pass per page — SEO, CRO, and trust checks all run against the same HTML. Do not fetch any page twice.

**Pages to fetch:**
- 15-20 product pages (varied handles, price points, and collections)
- 8-10 collection pages (prioritize collections with most products)
- Homepage, about page, contact page
- 3-5 blog articles (if blog detected from sitemap)
- Policy pages (shipping, returns, FAQ)

**Extract from every page:** title, meta description, canonical, H1, JSON-LD blocks, OG/Twitter tags, internal link patterns, external scripts, image attributes, question headings, lists/tables.

**Additionally extract per [cro-checks.md](references/cro-checks.md) and [trust-ux-checks.md](references/trust-ux-checks.md):**
- Homepage: hero CTA buttons + text, hero heading, footer (payment icons, policy links, social links, newsletter form), email capture scripts, chat widget scripts
- Product pages: cart drawer/redirect indicators, trust badges near ATC, size chart links, shipping info blocks, return policy blocks, express checkout buttons, review widget + star ratings, image count, product badges
- Contact page: phone, address, email domain, contact form, chat widget
- About page: word count, real content vs placeholder

**Page speed (separate API call):**
- `curl "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://{domain}&category=performance&strategy=mobile"`
- Extract: performance score, LCP, CLS, FCP. Count third-party `<script>` tags on homepage.
- If PSI returns non-200 or times out after 30 seconds, report "PageSpeed data unavailable" in SNAPSHOT and skip speed findings. Do not retry more than once.

### 5. Analyze across all eight modules

Use the data already collected in Steps 3-4. Do not fetch additional pages unless a specific check requires a page not yet sampled. Run checks from each reference file across all eight modules. Start with Trust & CRO — these are what real store reviewers flag first and what store owners care most about. The reference files are comprehensive checklists — not every failed check becomes a finding. Use the Finding Quality Bar to determine which issues earn a spot in the FINDINGS section.

**Module priority order:**
1. Trust & Credibility → [trust-ux-checks.md](references/trust-ux-checks.md) §1-4
2. CRO & Conversion → [cro-checks.md](references/cro-checks.md) §1-5
3. Page Speed → [trust-ux-checks.md](references/trust-ux-checks.md) §5
4. Technical SEO → [seo-checks.md](references/seo-checks.md) §3-4, 8-9
5. Product-Page SEO → [seo-checks.md](references/seo-checks.md) §1-2, 5-7
6. Structured Data → [seo-checks.md](references/seo-checks.md) §1 + [catalog-checks.md](references/catalog-checks.md)
7. AEO Readiness → [aeo-checks.md](references/aeo-checks.md)
8. GEO Citation → [geo-checks.md](references/geo-checks.md)

### 6. Select findings

Apply the Finding Quality Bar:
- Does it have provable revenue/traffic impact?
- Is it proportional to this store's maturity?
- Is it noise or signal?
- Can it be merged with a related issue?

For established stores: 4-6 findings. For struggling stores: up to 8-10.
Order by business impact, not by dimension.

### 7. Write the report

Use [assets/report-template.md](assets/report-template.md). Include: BOTTOM LINE, SNAPSHOT, FINDINGS, SAMPLE FIXES, CONVERSION GAPS, AI-FACING GAPS.

### 8. Validate

- Use [references/troubleshooting.md](references/troubleshooting.md) if data was partial.
- If saved to file, run `python ${CLAUDE_SKILL_DIR}/scripts/check_report.py --input path/to/report.md --mode full|focused|review`.

### 9. Hand off implementation

If the user wants fixes:
- Do NOT execute from `store-analyzer`
- Hand off to `store-fixer` with the prioritized fix list
- State that `store-fixer` requires explicit approval before any write and a rollback path

## Audit Review Mode

When verifying an existing audit, classify each claim as:

- `Supported and important`
- `Supported but secondary`
- `Real but overstated`
- `Unsupported from current evidence`
- `Missing important issues`

## Examples

**Example 1**: `Audit this Shopify store: neemans.com`
Result: Full 8-module audit with 4-5 focused findings, conversion gaps, and AI-facing gaps.

**Example 2**: `Check AI visibility for this store`
Result: GEO-focused audit — AI bot access, entity signals, content extractability, citation readiness.

**Example 3**: `Review this SEO audit and tell me what matters`
Result: Verify claims against live data, classify by importance, flag missing GEO/AEO dimensions.

**Example 4**: `Can ChatGPT find products from this store?`
Result: GEO-focused — robots.txt AI bot rules, content extractability, entity clarity.

**Example 5**: `Check structured data on this Shopify store`
Result: Focused audit on Structured Data module — Product/Offer schema, merchant listing fields, review markup.

**Example 6**: `Implement the fixes from this audit`
Result: Hand off to `store-fixer`. Do not execute changes from `store-analyzer`.

## When Not To Use This Skill

- The site is not a Shopify storefront.
- The user wants backlink analysis, competitor gap analysis, or local SEO.
- The task is purely copywriting with no audit component.
- The user needs authenticated data from Search Console, GA4, or Shopify admin.
- The user wants to FIX issues. Use `store-fixer` (requires approval + rollback).

## Maintenance Notes

For trigger tuning, regression checks, and eval prompts, use:

- [references/testing.md](references/testing.md)
- [evals/evals.json](evals/evals.json)

Keep this file focused on workflow and rules. Detailed checklists go in reference files.
