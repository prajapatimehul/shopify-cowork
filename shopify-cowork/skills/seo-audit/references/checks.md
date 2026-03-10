# SEO Audit Checks

## Contents

1. Scope and evidence rules
2. Data collection workflow
3. Analysis heuristics by priority
4. Operational thresholds and metric derivation
5. Internal scoring rubric
6. Metrics JSON for `scripts/score_audit.py`
7. Final QA checklist
8. Audit review mode

## 1. Scope and Evidence Rules

Label every major finding with one of these scopes:

- `Catalog-wide`: verified from public Shopify endpoints, sitemap, or robots.txt across
  the store.
- `Sampled`: verified only on the fetched HTML sample.
- `Inference`: a reasoned interpretation of verified data. Mark it as inference, not fact.

Severity guidance:

- Highest leverage:
  - missing or weak collection descriptions
  - missing or thin product descriptions
  - merchant listing eligibility gaps in product schema
  - canonical and internal-link consolidation issues
  - crawl traps in robots.txt
- Medium leverage:
  - repetitive title patterns
  - weak or missing snippets
  - blog/article SEO gaps
  - performance proxy problems
- Lower leverage:
  - Open Graph or Twitter issues
  - missing alt text unless image search is clearly important
  - empty `product_type`
  - cosmetic handle issues

Use calibrated language:

- Prefer: `limits`, `reduces`, `can prevent`, `may dilute`, `is likely hurting`
- Avoid unless directly proven: `penalizing`, `guarantees`, `can't index`, `this is why traffic dropped`

## 2. Data Collection Workflow

### Audit completeness and exact-count rules

Treat the audit as `Full audit` only when all of these are true:

- products endpoint was retrieved completely
- collections endpoint coverage is usable for the visible catalog
- robots.txt was fetched
- sitemap.xml was fetched
- homepage HTML was fetched
- at least 3 product pages and 1 collection page rendered successfully

Treat it as `Partial audit` when any required source is blocked, truncated, inconsistent,
or unavailable.

Only call a count `exact` when the underlying source is complete enough to support it.
Otherwise say the count is unavailable or partial from public data.

### Catalog-wide sources

Fetch these public Shopify endpoints:

1. Store metadata:
   - `https://{domain}/meta.json`
   - extract store name, description, published product count, published collection count,
     currency, and myshopify domain
2. Products:
   - `https://{domain}/products.json?limit=250&page={n}`
   - paginate until fewer than 250 products are returned
   - extract title, handle, body_html, vendor, product_type, tags, image alt values,
     image count, variant prices, compare_at_price, availability, and SKU
3. Collections:
   - `https://{domain}/collections.json?limit=250`
   - extract title, handle, body_html, products_count, and image presence
4. Pages:
   - `https://{domain}/pages.json`
   - extract title, handle, and body_html
5. Robots:
   - `https://{domain}/robots.txt`
6. Sitemap:
   - `https://{domain}/sitemap.xml`
   - identify product, collection, page, and article/blog sub-sitemaps
   - count URLs per type
   - note whether image metadata is present

### Sampled HTML sources

Fetch a varied set of pages:

- 5 product pages
- 3 collection pages
- homepage
- 2 article pages if detected

Extract:

- title text and length
- standard `<meta name="description">` text and length
- canonical URL
- H1 count and values
- JSON-LD blocks and schema types
- Open Graph tags
- Twitter tags
- theme metadata if present
- internal links using collection-prefixed product URLs
- external script count
- primary image loading and priority hints if visible in HTML

### Sampling advice

- Do not sample only the first handles.
- Include at least one product with variants and one from a high-value collection.
  Prefer collections with the highest `products_count` or strongest homepage/navigation
  prominence.
- If blog content exists, sample two distinct article URLs.
- If the store is large, prefer representative pages over purely chronological picks.

## 3. Analysis Heuristics by Priority

### 3.1 Structured Data and Merchant Listings

Check sampled product pages for:

- Product or ProductGroup schema
- required merchant listing fields:
  - `name`
  - `image`
  - `offers.price`
  - `offers.priceCurrency`
  - `offers.availability`
- recommended commerce fields:
  - `brand.name`
  - `sku`, `gtin`, or `mpn`
  - `aggregateRating`
  - `review`
  - `hasMerchantReturnPolicy`
  - `shippingDetails`
- duplicate or conflicting schema blocks
- malformed URLs or obviously broken values

How to frame it:

- Strong finding: sampled pages appear ineligible or weakly eligible for merchant listing
  enhancements.
- Moderate finding: markup exists, but recommended fields are thin or inconsistent.
- Caution: if JSON-LD is absent from server-rendered HTML, say it may be client-side and
  recommend Google's Rich Results Test instead of declaring it missing sitewide.

### 3.2 Titles and Snippets

Check sampled product and collection pages for:

- titles under 30 or over 60 characters
- repetitive templates across sampled pages
- titles that exactly match product names with no useful modifiers
- missing or weak standard meta descriptions
- descriptions that appear templated or generic

Important:

- Use the standard HTML meta description tag for snippet analysis.
- Do not substitute Open Graph or Twitter description tags for SEO snippet checks.

How to frame it:

- Strong finding: default or repetitive snippets leave ranking and click-through
  opportunity on the table.
- Lower finding: titles are acceptable but still not differentiated enough.

### 3.3 Canonicals and URL Consolidation

Check sampled HTML and crawlability files for:

- self-referencing canonical URLs
- clean product canonicals pointing to the base product URL
- inconsistent protocol or host canonicals
- collection-prefixed product links in internal HTML
- tag or filter URL patterns that create duplicates

How to frame it:

- Strong finding: internal links and crawl rules expose multiple URL forms for the same
  products or collections.
- Avoid saying `duplicate content penalty`. The better framing is diluted consolidation,
  crawl waste, and mixed signals.

### 3.4 Robots and Sitemap

Check robots.txt for common Shopify junk patterns:

- sort URLs
- tag-combination URLs
- internal search
- preview theme URLs
- policy pages
- recommendation endpoint URLs
- article tag combinations

Check the sitemap for:

- accessibility
- sub-sitemap completeness
- product count consistency with `meta.json`
- image metadata presence
- blog/article discovery

How to frame it:

- Strong finding: crawl traps or missing sitemap coverage can waste crawl attention or
  make discovery less efficient.
- Do not claim indexation failure unless pages are actually blocked, noindexed, or
  inaccessible.

### 3.5 Product Content

Measure catalog-wide:

- products with empty descriptions
- products with thin descriptions after stripping HTML
- duplicate description groups
- products with zero images
- products with a single image only

How to frame it:

- Strong finding: empty or thin product pages give Google little unique text to rank.
- Collections usually outrank isolated product pages for category intent, so do not let
  minor product hygiene outrank missing collection copy.

### 3.6 Collection and Information Architecture

Measure catalog-wide:

- collections with empty descriptions
- collections with zero products
- very low collection count relative to product count
- suspicious promotional or junk collection handles

How to frame it:

- This is often the highest-leverage ecommerce content finding.
- Collection pages are frequently the best organic landing pages for category-intent
  searches.

### 3.7 Blog and Editorial Content

Check whether blogs exist from the sitemap and sample article pages for:

- unique titles and descriptions
- article schema
- clear H1 tags
- internal links back to collections or products

How to frame it:

- If no blog is detected in the sitemap, say `not detected from public sitemap data`.
- If a blog exists but articles are weakly connected to products or categories, note the
  missed internal-linking opportunity.

### 3.8 Performance Proxies

From sampled HTML, check:

- primary product images marked lazy
- lack of `fetchpriority` or preload hints
- high external script counts
- repeated third-party script vendors

How to frame it:

- These are proxy checks only.
- Recommend PageSpeed Insights or Lighthouse for confirmation.
- Do not claim failed Core Web Vitals from HTML alone.

### 3.9 Lower-Priority Hygiene

Report, but normally do not headline:

- Open Graph issues
- Twitter card issues
- missing alt text
- empty `product_type`
- meaningless compare_at_price data
- messy vendor fields
- product tags, but only as secondary merchandising or internal-search hygiene when
  storefront evidence makes that relevant

Use clear downgrade language:

- `Real but secondary`
- `Worth fixing in bulk`
- `Good cleanup after higher-leverage content and crawl issues`

## 4. Operational Thresholds and Metric Derivation

Use these rules to turn raw public evidence into score inputs. Do not invent your own
thresholds mid-audit.

### Catalog and content thresholds

- `empty description`: stripped visible text length is `0`
- `thin product description`: stripped visible text is `1-120` characters or fewer than
  `25` words
- `substantive product description`: more than `120` visible characters and at least `25`
  words
- `empty collection description`: stripped visible text length is `0`
- `thin or empty page`: public page content has `0-80` visible characters after stripping
  HTML
- `duplicate description group`: `2+` products share the same normalized stripped
  description of at least `40` visible characters
- `too few collections`: catalog has `40+` products and fewer than `1` collection per
  `20` products

### Sampled title and snippet rules

- `out_of_range_titles`: count sampled product and collection pages with title length
  under `30` or over `60` characters
- `missing_meta_descriptions`: count sampled product and collection pages with no
  standard `<meta name="description">`
- `identical_title_pattern`: true when `4+` sampled product titles follow the same
  low-information template
- `identical_or_template_descriptions`: true when `3+` sampled pages reuse the same or
  near-identical standard meta description
- `weak_snippets`: true when `3+` sampled product or collection pages rely on generic
  snippets with no clear product or category modifiers

### Structured data rules

- `missing_json_ld`: true only when `4+` sampled product pages have no visible
  `Product` or `ProductGroup` JSON-LD in server-rendered HTML
- `missing_offers_or_price`: true only when visible product schema exists and `2+`
  sampled product pages lack `offers.price`, `offers.priceCurrency`, or
  `offers.availability`
- `missing_aggregate_rating`: true only when schema is otherwise present on most sampled
  product pages and visible review cues exist but `4+` sampled product pages still lack
  `aggregateRating`
- `missing_brand`: true when `2+` sampled product pages with schema lack `brand.name`
- `bad_description`: true when `2+` sampled product pages expose empty, duplicated, or
  obviously broken schema descriptions
- `missing_breadcrumb_schema`: true when `3+` sampled product or collection pages lack
  breadcrumb schema
- `missing_org_schema`: true when the sampled homepage lacks organization-level schema
- `duplicate_schema_blocks`: true when `2+` sampled pages expose conflicting duplicate
  product schema blocks

### URL, crawl, and performance rules

- `canonical_issues`: true when `2+` sampled pages have non-self-referencing, malformed,
  or mixed canonical targets
- `collection_prefixed_internal_links`: true when sampled internal HTML repeatedly links
  products through collection-prefixed URLs
- `missing_sort_filter_blocking`: true when visible sort, search, or faceted URLs exist
  and robots rules do not control them
- `tag_combination_urls_crawlable`: true when tag-combination or equivalent faceted URLs
  are publicly crawlable and discoverable
- `junk_urls_crawlable`: true when recommendation, preview, or duplicate query URL
  classes are discoverable without control signals
- `inconsistent_canonicals`: true when `2+` sampled pages use the wrong canonical host,
  protocol, or duplicate path pattern
- `important_url_class_absent`: true when public product or collection URLs exist but the
  corresponding sitemap class is missing or incomplete
- `pages_blocked_unintentionally`: true when sampled key pages are blocked, noindexed, or
  otherwise prevented from normal discovery
- `high_external_script_count_penalty`: use the median sampled external script count:
  `0` for `<=12`, `1` for `13-18`, `2` for `19-24`, `3` for `25-30`, `4` for `>30`

### Hygiene and confidence rules

- `h1_issues`: true when `2+` sampled pages have zero H1s or more than one H1
- `og_issues`: true when `2+` sampled pages miss core Open Graph fields such as
  `og:title`, `og:url`, or `og:image`
- `twitter_issues`: true when `2+` sampled pages miss core Twitter fields such as
  `twitter:card`, `twitter:title`, or `twitter:description`
- `url_structure_issues`: true only for genuinely messy or duplicate-prone handles, not
  for normal readable slugs
- `data_quality_issues`: true when public endpoints conflict materially, HTML sampling is
  blocked enough to reduce confidence, or the audit must be downgraded to partial
- Product tags are not a score input. Mention them only as secondary site-merchandising
  context when relevant.

## 5. Internal Scoring Rubric

Use this only as an internal prioritization heuristic. The weighted categories sum to
`100`, not `115`.

### Structured Data: 15 points

- missing JSON-LD on sampled product pages: minus 6
- markup present but missing offers price data: minus 4
- missing aggregate rating: minus 1
- missing brand name: minus 1
- bad description values in schema: minus 1
- missing breadcrumb schema: minus 1
- missing organization schema on homepage: minus 1
- duplicate schema blocks: minus 1

### Titles and Snippets: 10 points

- sampled titles out of range: minus 2 per occurrence, max minus 4
- identical sampled title pattern: minus 2
- missing sampled standard meta descriptions: minus 1 per occurrence, max minus 3
- identical or templated sampled descriptions: minus 1
- weak product-specific snippet detail across samples: minus 1

### URL Consolidation: 10 points

- canonical issues on sampled pages: minus 3
- collection-prefixed internal links: minus 2
- missing robots rules for sort or filter URLs: minus 2
- tag-combination URLs crawlable: minus 1
- junk query or duplicate URL classes exposed: minus 1
- inconsistent canonical host or protocol: minus 1

### Content Depth: 25 points

- products missing descriptions: minus 1 per 5 percent affected, max minus 10
- thin product content: minus 1 per 10 percent affected, max minus 5
- duplicate product description groups: minus 1 per group, max minus 3
- collections missing descriptions: minus 1 per 20 percent affected, max minus 5
- important thin or empty pages: minus 1 per 3 pages, max minus 2

### Crawlability: 15 points

- missing search, preview, policy, or recommendation blocking rules: minus 1 each,
  max minus 4
- sitemap inaccessible: minus 3
- missing sub-sitemap types: minus 1 each, max minus 3
- product count mismatch between metadata and sitemap: minus 2
- important URL class absent from sitemap: minus 1
- unintentionally blocked key pages: minus 3

### Collection and Blog IA: 15 points

- empty collections: minus 1 per 3, max minus 3
- too few collections for the catalog size: minus 4
- junk collections exposed: minus 3
- weak sampled article titles, snippets, or product links: minus 2
- orphaned products or weak collection coverage: minus 3

### Performance Risk: 5 points

- lazy primary image on sampled product template: minus 1
- high external script count: minus 0 to 2 depending on severity
- missing priority hints for primary image: minus 1
- repeated third-party bloat indicators: minus 1

### Hygiene: 5 points

- H1 issues: minus 1
- Open Graph issues: minus 1
- Twitter card issues: minus 1
- image alt coverage: minus 1 per 50 percent missing, max minus 1
- URL handle quality issues: minus 1
- data quality issues: minus 1

## 6. Metrics JSON for `scripts/score_audit.py`

The scoring script expects a JSON object with these top-level keys:

- `audit_context`
- `structured_data`
- `titles_snippets`
- `url_consolidation`
- `content_depth`
- `crawlability`
- `collection_blog_ia`
- `performance_risk`
- `hygiene`

The `audit_context` block is required so the scorer can validate whether a score is being
computed from a full audit or a partial audit.

Example:

```json
{
  "audit_context": {
    "audit_mode": "full",
    "catalog_products_complete": true,
    "catalog_collections_complete": true,
    "catalog_pages_complete": true,
    "robots_fetched": true,
    "sitemap_fetched": true,
    "homepage_sampled": true,
    "sampled_product_pages": 5,
    "sampled_collection_pages": 3,
    "sampled_article_pages": 0
  },
  "structured_data": {
    "missing_json_ld": false,
    "missing_offers_or_price": true,
    "missing_aggregate_rating": false,
    "missing_brand": false,
    "bad_description": false,
    "missing_breadcrumb_schema": false,
    "missing_org_schema": false,
    "duplicate_schema_blocks": false
  },
  "titles_snippets": {
    "out_of_range_titles": 2,
    "identical_title_pattern": true,
    "missing_meta_descriptions": 1,
    "identical_or_template_descriptions": false,
    "weak_snippets": true
  },
  "url_consolidation": {
    "canonical_issues": false,
    "collection_prefixed_internal_links": true,
    "missing_sort_filter_blocking": true,
    "tag_combination_urls_crawlable": false,
    "junk_urls_crawlable": false,
    "inconsistent_canonicals": false
  },
  "content_depth": {
    "percent_products_missing_description": 4.8,
    "percent_products_thin": 12.0,
    "duplicate_description_groups": 2,
    "percent_collections_missing_description": 40.0,
    "thin_or_empty_pages": 1
  },
  "crawlability": {
    "missing_search_preview_policy_recommendation_rules": 2,
    "sitemap_not_accessible": false,
    "missing_sub_sitemaps": 0,
    "product_count_mismatch": false,
    "important_url_class_absent": false,
    "pages_blocked_unintentionally": false
  },
  "collection_blog_ia": {
    "empty_collections": 0,
    "too_few_collections": false,
    "junk_collections_exposed": false,
    "weak_blog_posts_or_links": false,
    "orphaned_products_or_weak_coverage": false
  },
  "performance_risk": {
    "primary_image_lazy_loaded": true,
    "high_external_script_count_penalty": 1,
    "no_primary_image_priority_hints": true,
    "repeated_third_party_bloat": false
  },
  "hygiene": {
    "h1_issues": false,
    "og_issues": false,
    "twitter_issues": false,
    "percent_images_missing_alt": 48.0,
    "url_structure_issues": false,
    "data_quality_issues": false
  }
}
```

## 7. Final QA Checklist

- The report states whether it is a `Full audit` or `Partial audit`.
- The report uses exact counts only for sources that were fully retrieved.
- The report distinguishes `Catalog-wide`, `Sampled`, and `Inference`.
- Sampled findings are not rewritten as sitewide facts.
- The executive summary names one biggest issue and one credible quick win.
- Top 5 actions are ordered by impact, not by how dramatic they sound.
- Collections and product content are not buried beneath low-impact hygiene issues.
- If a score is shown, it comes from `scripts/score_audit.py` and is labeled as an
  internal heuristic.
- Snippet findings are based on the standard meta description tag, not Open Graph tags.
- Product tags are not presented as a primary SEO issue.
- No unsupported claims about penalties, guaranteed rankings, or traffic loss.
- If JSON-LD was not visible in HTML, the report says it may be client-side.
- Sample fixes are based on real products or collections from the store.

## 8. Audit Review Mode

If the user provides an existing audit:

1. Extract the report's core claims.
2. Verify each claim against public data and sampled HTML.
3. Reclassify claims as:
   - supported and important
   - supported but secondary
   - real but overstated
   - unsupported from current evidence
   - missing important issue
4. Explain why the claim moved categories.

Common downgrade patterns:

- sitewide claim built from a 5-page sample
- accessibility issue described as the top SEO ranking issue
- `Google can't index` when the issue is really weak content or missing markup
- schema or speed claims made without confirming the rendered page
- arbitrary numeric score presented like a Google metric
