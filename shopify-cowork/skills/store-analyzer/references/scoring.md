# Store Readiness Score

## Score Framing

Call this the **Store Readiness Score** — a diagnostic benchmark measuring how well the store is positioned for search engines, AI assistants, and answer engines today.

**Never present as a grade or verdict.** Always show with its breakdown.

### Score Bands

| Range | Label | Meaning |
|---|---|---|
| 85-100 | Strong | Well-optimized across all dimensions. Focus on maintenance. |
| 65-84 | Good foundation | Key gaps in 1-2 areas limiting visibility. Prioritized fixes will move the needle. |
| 40-64 | Significant opportunities | Leaving traffic and AI citations on the table. Structured plan needed. |
| Below 40 | Foundational work needed | Critical issues blocking visibility. |

---

## Category Weights (Sum = 100)

| Category | Points | What It Covers |
|---|---|---|
| A. Technical SEO | 20 | Crawlability, speed proxies, canonicals, sitemap, robots.txt |
| B. Content & On-Page SEO | 25 | Titles, descriptions, product/collection content depth, IA |
| C. Structured Data | 20 | Product schema, Organization, BreadcrumbList, reviews, merchant listing |
| D. GEO: AI Visibility | 20 | AI bot access, entity clarity, citation-worthiness, extractability |
| E. AEO: Answer Readiness | 15 | FAQ/HowTo schema, snippet readiness, voice search, PAA |

**Rationale:** SEO (A+B+C) = 65 points. Still the majority — SEO drives most ecommerce traffic today. GEO = 20 points (rapid growth). AEO = 15 points (important for brand queries, narrower scope).

---

## Detailed Scoring Rubric

### A. Technical SEO (20 points)

| Check | Max | Deduction |
|---|---|---|
| **A1. Robots.txt blocks crawl traps** | 3 | -1 per missing rule (sort, tag, search, preview), max -3 |
| **A2. Sitemap accessible and valid** | 3 | -3 if inaccessible. -1 per issue (missing sub-sitemaps, count mismatch, missing image metadata), max -3 |
| **A3. Canonicals correct** | 3 | -3 if canonical issues on sampled pages. -2 if inconsistent host/protocol. |
| **A4. No collection-prefixed product links** | 3 | -3 if sampled collection pages link to `/collections/x/products/y` |
| **A5. LCP image not lazy-loaded** | 2 | -2 if hero image has `loading="lazy"` |
| **A6. Hero image has fetchpriority** | 1 | -1 if missing `fetchpriority="high"` on LCP image |
| **A7. Image dimensions present** | 1 | -1 if sampled images lack `width`/`height` |
| **A8. External script count reasonable** | 2 | -1 if 10-15 external domains, -2 if > 15 |
| **A9. No render-blocking scripts** | 2 | -1 per blocking script in head (without async/defer), max -2 |

### B. Content & On-Page SEO (25 points)

| Check | Max | Deduction |
|---|---|---|
| **B1. Products with descriptions** | 5 | -1 per 10% of products missing description, max -5 |
| **B2. Product description depth** | 3 | -1 per 15% of products with thin (<150 word) descriptions, max -3 |
| **B3. No duplicate descriptions** | 2 | -1 per duplicate group, max -2 |
| **B4. Collection descriptions present** | 4 | -1 per 20% of collections missing description, max -4 |
| **B5. Title tags within range** | 2 | -1 per out-of-range title in sample (< 30 or > 60 chars), max -2 |
| **B6. Title tags unique** | 2 | -2 if sampled titles follow identical template |
| **B7. Meta descriptions present** | 2 | -1 per missing meta description in sample, max -2 |
| **B8. H1 tags correct** | 1 | -1 if multiple H1s or missing H1 on sampled pages |
| **B9. Product type consistency** | 1 | -1 if inconsistent casing/naming in product_type values |
| **B10. Vendor consistency** | 1 | -1 if inconsistent casing in vendor values |
| **B11. Collection count adequate** | 1 | -1 if too few collections for catalog size (ratio > 25:1) |
| **B12. No zero-price products** | 1 | -1 if any product priced at zero |

### C. Structured Data (20 points)

| Check | Max | Deduction |
|---|---|---|
| **C1. Product JSON-LD present** | 4 | -4 if missing from sampled product pages entirely |
| **C2. Required merchant fields** | 3 | -1 per missing required field (name, image, price, currency, availability), max -3 |
| **C3. Product identifiers present** | 2 | -2 if no sku/gtin/mpn in Product schema |
| **C4. Brand in schema** | 1 | -1 if brand.name missing from Product schema |
| **C5. AggregateRating present** | 2 | -2 if no aggregateRating on sampled product pages |
| **C6. Review schema present** | 1 | -1 if no review objects in Product schema |
| **C7. BreadcrumbList schema** | 2 | -2 if no BreadcrumbList JSON-LD on sampled pages |
| **C8. Organization schema on homepage** | 2 | -2 if no Organization/OnlineStore JSON-LD on homepage |
| **C9. Schema server-rendered** | 2 | -2 if JSON-LD only appears via JS injection (not in raw HTML). Note: say it may be client-side if uncertain. |
| **C10. No schema errors** | 1 | -1 if duplicate or conflicting schema blocks found |

### D. GEO: AI Visibility (20 points)

| Check | Max | Deduction |
|---|---|---|
| **D1. AI search bots not blocked** | 5 | -1 per major search bot blocked (OAI-SearchBot, ChatGPT-User, PerplexityBot), max -5 |
| **D2. llms.txt present** | 2 | -2 if no llms.txt file exists |
| **D3. Organization sameAs links** | 3 | -1 per missing major platform (Wikipedia/Wikidata, social profiles), max -3 |
| **D4. Brand name consistency** | 1 | -1 if brand name differs across title tag, schema, og:site_name |
| **D5. About page exists with depth** | 1 | -1 if no About page or < 100 words |
| **D6. Question-based headings** | 4 | -4 if no question-based headings in sample. *(Sole scoring location — AEO references this but does not deduct again.)* |
| **D7. Tables and structured lists** | 2 | -2 if no tables or structured lists on sampled pages |
| **D8. Content freshness** | 2 | -1 if > 50% of products not updated in 6 months. -1 if no blog posts in 6 months. |

> **De-duplication note:** Review signals are scored in C5/C6 only, not here. Knowledge Panel signals (Organization schema, sameAs) are scored in C8 and D3 only.

### E. AEO: Answer Readiness (15 points)

| Check | Max | Deduction |
|---|---|---|
| **E1. FAQ schema present** | 3 | -3 if no FAQPage schema on any sampled page |
| **E2. Answer-first paragraphs** | 3 | -3 if question headings exist but answers are not 40-60 words |
| **E3. Comparison content exists** | 3 | -3 if no comparison tables or buying guide content detected |
| **E4. HowTo or instructional content** | 3 | -3 if no instructional content detected (styling guides, care instructions) |

> **De-duplication note:** Question headings scored in D6 only. Review snippet eligibility scored in C5 only. Knowledge Panel signals scored in C8 + D3 only. AEO scores only checks that do not overlap with other categories. Max total AEO deduction is 12/15.

---

## Metrics JSON Structure

The scoring script expects a JSON object:

```json
{
  "technical_seo": {
    "robots_missing_rules": 0,
    "sitemap_not_accessible": false,
    "sitemap_issues": 0,
    "canonical_issues": false,
    "collection_prefixed_links": false,
    "lcp_image_lazy": false,
    "missing_fetchpriority": false,
    "missing_image_dimensions": false,
    "external_script_domains": 8,
    "render_blocking_scripts": 0
  },
  "content_onpage": {
    "percent_products_missing_description": 4.0,
    "percent_products_thin": 12.0,
    "duplicate_description_groups": 1,
    "percent_collections_missing_description": 33.0,
    "out_of_range_titles": 1,
    "identical_title_pattern": false,
    "missing_meta_descriptions": 1,
    "h1_issues": false,
    "product_type_inconsistent": true,
    "vendor_inconsistent": true,
    "too_few_collections": false,
    "zero_price_products": true
  },
  "structured_data": {
    "missing_product_jsonld": false,
    "missing_required_merchant_fields": 1,
    "missing_product_identifiers": true,
    "missing_brand": false,
    "missing_aggregate_rating": true,
    "missing_review_schema": true,
    "missing_breadcrumb_schema": true,
    "missing_org_schema": true,
    "schema_not_server_rendered": false,
    "schema_errors": false
  },
  "geo_ai_visibility": {
    "ai_search_bots_blocked": 3,
    "no_llms_txt": true,
    "missing_sameas_platforms": 2,
    "brand_name_inconsistent": false,
    "weak_about_page": true,
    "no_question_headings": true,
    "no_tables_or_lists": false,
    "no_review_signals": true,
    "stale_products_percent": 20.0,
    "no_recent_blog": true
  },
  "aeo_answer_readiness": {
    "no_faq_schema": true,
    "page_types_without_question_headings": 2,
    "poor_answer_format": true,
    "no_comparison_content": true,
    "review_snippet_ineligible": true,
    "no_instructional_content": true
  }
}
```

---

## QA Checklist

Before finalizing the report:

- [ ] Report uses exact counts for catalog-wide claims
- [ ] Report distinguishes `Catalog-wide`, `Sampled`, and `Inference`
- [ ] Sampled findings are not rewritten as sitewide facts
- [ ] Executive summary names one biggest issue and one credible quick win
- [ ] Top 5 actions ordered by impact, not how dramatic they sound
- [ ] Collections and product content not buried beneath low-impact hygiene issues
- [ ] Score labeled as "Store Readiness Score" — a diagnostic benchmark, not a grade
- [ ] No unsupported claims about penalties, guaranteed rankings, or traffic loss
- [ ] If JSON-LD was not visible in HTML, report says it may be client-side
- [ ] Sample fixes use real products or collections from the store
- [ ] GEO section does not overstate AI visibility impact for stores where SEO basics are broken
- [ ] AEO checks acknowledge deprecated rich results where applicable (FAQ, HowTo)
- [ ] AI bot blocking finding explains the search vs. training bot distinction
