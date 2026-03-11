---
name: store-analyzer
description: Comprehensive Shopify store audit covering SEO, GEO (AI visibility), and AEO (answer engine readiness). Use when a user asks to audit, analyze, review, or check any Shopify store's search visibility, AI readiness, or discoverability. Covers traditional search optimization, AI engine citation-worthiness, and answer/snippet readiness from public data only. Do not use for non-Shopify sites, backlink audits, local SEO, paid ads analysis, or generic copywriting.
compatibility: Requires network access to public Shopify URLs. Optional code execution for bundled scoring and QA scripts.
metadata:
  author: shopify-cowork
  version: 1.0.0
---

# Store Analyzer

Run comprehensive Shopify store audits covering three dimensions of modern search visibility:

- **SEO** — Traditional search engine optimization (crawlability, structured data, content, technical health)
- **GEO** — Generative Engine Optimization (AI bot access, entity clarity, citation-worthiness, content extractability)
- **AEO** — Answer Engine Optimization (featured snippet readiness, FAQ/HowTo schema, voice search, PAA optimization)

Use public Shopify data, sampled HTML, and explicit scope labeling. Make the report commercially useful and defensible without inventing penalties or unsupported claims.

## Use Bundled Resources Progressively

- Read [references/seo-checks.md](references/seo-checks.md) for SEO audit checks, heuristics, and Shopify-specific technical issues.
- Read [references/geo-checks.md](references/geo-checks.md) for AI visibility checks — bot access, entity signals, citation-worthiness.
- Read [references/aeo-checks.md](references/aeo-checks.md) for answer engine checks — snippets, FAQ schema, voice search, PAA.
- Read [references/catalog-checks.md](references/catalog-checks.md) for product and collection data quality checks from `/products.json`.
- Read [references/troubleshooting.md](references/troubleshooting.md) when endpoints are blocked, incomplete, or conflicting.
- Use [assets/report-template.md](assets/report-template.md) for the final output shape.
- Use [references/testing.md](references/testing.md) and [evals/evals.json](evals/evals.json) when improving the skill or checking trigger behavior.
- If the report is saved to disk, validate with `python scripts/check_report.py --input path/to/report.md --mode full|focused|review` (mode must match the audit type).

## Critical Rules

- Use only public Shopify endpoints and public page HTML. Never attempt authentication.
- Report exact counts. Do not round, estimate, or use "approximately."
- Label major findings as `Catalog-wide`, `Sampled`, or `Inference`.
- Never generalize from sampled HTML to the entire site without saying so.
- If `products.json` is blocked, empty, or unusable, say so clearly and stop the full catalog audit instead of guessing.
- Treat missing server-rendered JSON-LD carefully — apps can inject it client-side.
- Keep the report easy to scan. A client should understand the top issues in under a minute.
- Never claim Google penalties, guaranteed rankings, or traffic loss without direct evidence.

## Workflow

### 1. Confirm the task mode

- `Full audit`: audit the live Shopify store from scratch across SEO + GEO + AEO.
- `Focused audit`: user wants a specific dimension only (e.g., "check AI readiness" = GEO focus).
- `Audit review`: user provided an existing audit and wants verification.

If the user supplied an existing audit, extract its claims first so you can verify them against store data.

### 2. Normalize the domain and confirm the store is auditable

- Strip scheme, `www.`, trailing slashes, and obvious path fragments.
- Fetch store metadata and products endpoint first.
- If the store does not expose public Shopify catalog data, explain the limitation and stop.

### 3. Collect catalog-wide data

Fetch public Shopify resources:

1. **Store metadata**: `https://{domain}/meta.json`
2. **Products**: `https://{domain}/products.json?limit=250&page={n}` — paginate until < 250 returned
3. **Collections**: `https://{domain}/collections.json?limit=250`
4. **Pages**: `https://{domain}/pages.json`
5. **Robots.txt**: `https://{domain}/robots.txt`
6. **Sitemap**: `https://{domain}/sitemap.xml`
7. **llms.txt**: `https://{domain}/llms.txt` (check if exists)

Run catalog-wide checks from [references/catalog-checks.md](references/catalog-checks.md).

### 4. Collect sampled HTML

Fetch representative pages:

- 5 product pages (varied, not just the first handles)
- 3 collection pages
- Homepage
- 2 article/blog pages if detected from sitemap
- 1 About page (`/pages/about` or similar) if it exists

Extract from each page:
- `<title>` text and length
- `<meta name="description">` text and length
- `<link rel="canonical">` URL
- H1 count and values
- All `<script type="application/ld+json">` blocks — parse for Product, FAQPage, HowTo, Organization, BreadcrumbList, SpeakableSpecification
- Open Graph and Twitter tags
- Internal link patterns (collection-prefixed product URLs)
- External script count and domains
- Image loading attributes (`loading`, `fetchpriority`, `width`, `height`)
- Question-formatted headings (H2/H3 starting with what/how/why/when/where/who)
- Answer paragraph word counts after question headings
- Table elements, ordered/unordered lists
- Review widget indicators

### 5. Analyze by dimension

Run checks from each reference file:

1. **SEO checks** — [references/seo-checks.md](references/seo-checks.md)
   - Structured data completeness (Product schema, merchant listing eligibility)
   - Titles and meta descriptions
   - Canonicals and URL consolidation
   - Robots.txt and sitemap
   - Content depth (products + collections)
   - Performance proxies (LCP image, scripts, CWV signals)
   - Internal linking and IA

2. **GEO checks** — [references/geo-checks.md](references/geo-checks.md)
   - AI bot access (GPTBot, ChatGPT-User, PerplexityBot, ClaudeBot, Google-Extended)
   - llms.txt presence and quality
   - Entity clarity (Organization schema, sameAs, brand consistency)
   - Citation-worthiness signals (reviews, original data, freshness)
   - Content extractability (answer-first format, tables, lists)

3. **AEO checks** — [references/aeo-checks.md](references/aeo-checks.md)
   - FAQ schema (FAQPage JSON-LD)
   - HowTo schema on relevant content
   - Featured snippet readiness (question headings + concise answers)
   - Voice search readiness (concise answer blocks, conversational language)
   - PAA optimization (question coverage, direct answer format)
   - Review snippet eligibility (AggregateRating, review schema)
   - Knowledge Panel signals (Organization schema, Wikidata, sameAs)

4. **Catalog quality** — [references/catalog-checks.md](references/catalog-checks.md)
   - Product data quality (descriptions, images, pricing, types, vendors, SKUs)
   - Collection data quality (descriptions, product counts, titles)
   - Tag analysis (over-tagging, crawl traps, inconsistencies)

### 6. Write the report

Use [assets/report-template.md](assets/report-template.md).

For a full audit, give the user:

- Bottom line: biggest issue + best quick win
- Store snapshot
- Findings ordered by impact — each with scope, proof, fix, and why it matters
- Top 5 actions ordered by business impact
- Sample fixes using real products or collections from the store

### 7. Run the quality gate

Before finalizing:

- Use [references/troubleshooting.md](references/troubleshooting.md) if data quality is partial.
- If saved to file, run `scripts/check_report.py --input path/to/report.md --mode full|focused|review`.

## Audit Review Mode

When the user gives you an existing Shopify audit, verify its claims against live public data. Classify each claim as:

- `Supported and important`
- `Supported but secondary`
- `Real but overstated`
- `Unsupported from current evidence`
- `Missing important issue`

## Examples

**Example 1**: `Audit this Shopify store: example.com`
Result: Full SEO + GEO + AEO audit from public endpoints.

**Example 2**: `Check if this Shopify store is visible to AI search engines`
Result: GEO-focused audit — AI bot access, entity signals, citation readiness.

**Example 3**: `Review this SEO audit for themancompany.com and tell me what matters`
Result: Verify claims against live store, classify by importance, flag missing issues.

**Example 4**: `Can ChatGPT and Perplexity find products from this store?`
Result: GEO-focused audit — robots.txt AI bot rules, llms.txt, content extractability.

**Example 5**: `Check if this Shopify store can win featured snippets`
Result: AEO-focused audit — FAQ schema, question headings, answer format, snippet readiness.

## When Not To Use This Skill

- The site is not a Shopify storefront.
- The user wants backlink analysis, competitor gap analysis, or local SEO.
- The task is purely copywriting with no audit component.
- The user needs authenticated data from Search Console, GA4, or Shopify admin.
- The user wants to FIX issues (use `store-fixer` skill instead).

## Maintenance Notes

For trigger tuning, regression checks, and eval prompts, use:

- [references/testing.md](references/testing.md)
- [evals/evals.json](evals/evals.json)

Keep this main file lean. All detailed checklists, scoring rules, and troubleshooting go in bundled resources.
